#!/usr/bin/env python3
"""Codex PreToolUse guard for dangerous shell commands."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shlex
import sys
import time


STATE_PATH = Path(os.environ.get("CODEX_HOOK_STATE", f"/tmp/codex-git-safety-state-{os.getuid()}.json"))
REVIEW_TTL_SECONDS = 300


def emit_block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))


def get_command(payload: dict) -> str:
    tool_input = payload.get("tool_input")
    if isinstance(tool_input, dict):
        for key in ("command", "cmd"):
            value = tool_input.get(key)
            if isinstance(value, str):
                return value
        arguments = tool_input.get("arguments")
        if isinstance(arguments, dict):
            for key in ("command", "cmd"):
                value = arguments.get(key)
                if isinstance(value, str):
                    return value

    for key in ("command", "cmd"):
        value = payload.get(key)
        if isinstance(value, str):
            return value

    return ""


def get_workdir(payload: dict) -> str:
    tool_input = payload.get("tool_input")
    if isinstance(tool_input, dict):
        for key in ("workdir", "cwd"):
            value = tool_input.get(key)
            if isinstance(value, str) and value:
                return str(Path(value).expanduser().resolve())
        arguments = tool_input.get("arguments")
        if isinstance(arguments, dict):
            for key in ("workdir", "cwd"):
                value = arguments.get(key)
                if isinstance(value, str) and value:
                    return str(Path(value).expanduser().resolve())

    for key in ("workdir", "cwd"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return str(Path(value).expanduser().resolve())

    return str(Path(os.getcwd()).resolve())


def read_state() -> dict:
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def write_state(state: dict) -> None:
    try:
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        STATE_PATH.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


def mark_git_review(workdir: str, kind: str) -> None:
    state = read_state()
    entry = state.setdefault(workdir, {})
    entry[kind] = time.time()
    write_state(state)


def has_recent_git_review(workdir: str) -> bool:
    entry = read_state().get(workdir, {})
    now = time.time()
    return all(now - float(entry.get(kind, 0)) <= REVIEW_TTL_SECONDS for kind in ("status", "diff"))


def has_recent_review(workdir: str, *kinds: str) -> bool:
    entry = read_state().get(workdir, {})
    now = time.time()
    return all(now - float(entry.get(kind, 0)) <= REVIEW_TTL_SECONDS for kind in kinds)


def consume_git_review(workdir: str) -> None:
    state = read_state()
    if workdir in state:
        del state[workdir]
        write_state(state)


def split_segments(command: str) -> list[list[str]]:
    segments: list[list[str]] = []
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        return [[command]]

    current: list[str] = []
    for token in tokens:
        if token in {";", "&&", "||", "|"}:
            if current:
                segments.append(current)
                current = []
            continue
        current.append(token)

    if current:
        segments.append(current)
    return segments


def first_program(segment: list[str]) -> str:
    prefixes = {
        "command",
        "env",
        "nohup",
        "time",
        "timeout",
        "sudo",
        "doas",
        "pkexec",
    }
    index = 0
    while index < len(segment):
        token = segment[index]
        if token in prefixes:
            index += 1
            if token == "env":
                while index < len(segment) and "=" in segment[index] and not segment[index].startswith("-"):
                    index += 1
            elif token == "timeout" and index < len(segment):
                index += 1
            continue
        return token.rsplit("/", 1)[-1]
    return ""


def contains_any(tokens: list[str], values: set[str]) -> bool:
    return any(token in values for token in tokens)


def has_option(tokens: list[str], short: str, long: str | None = None) -> bool:
    for token in tokens:
        if token == short or (long and token == long):
            return True
        if token.startswith("-") and short.strip("-") in token[1:] and not token.startswith("--"):
            return True
    return False


def classify(command: str, workdir: str) -> str | None:
    compact = " ".join(command.strip().split())
    if not compact:
        return None

    lowered = compact.lower()
    if re.search(r"\b(drop\s+(database|schema|table)|truncate\s+table)\b", lowered):
        return "SQL drop/truncate detected. First run a read-only inspection (`SELECT ...`, schema/table list) and verify a current backup/rollback path. Do not retry automatically; ask the user for the exact data mutation."

    for segment in split_segments(command):
        invoked = segment[0].rsplit("/", 1)[-1] if segment else ""
        if invoked in {"sudo", "doas", "pkexec", "su"}:
            return "Privilege escalation is blocked by default. First try a non-privileged read-only check. If elevation is still required, ask the user for the exact command and reason; do not retry with sudo automatically."

        program = first_program(segment)
        if not program:
            continue

        tokens = segment
        if program in {"rm", "unlink", "rmdir"}:
            return "Permanent deletion with rm/rmdir/unlink is blocked. Run `ls -ld <path>` and `git status --short`; prefer `gio trash <path>` for recoverable deletion. Do not retry rm automatically."

        if program in {"shred", "srm"}:
            return "Secure deletion is blocked. Run `ls -ld <path>` to confirm the target, then ask the user for explicit permanent deletion. Prefer recoverable `gio trash` when possible."

        if program in {"mkfs", "mkfs.ext4", "mkfs.xfs", "mkfs.btrfs", "mkswap", "wipefs", "fdisk", "parted", "sgdisk", "gdisk"}:
            return "Disk formatting or partition changes are blocked. Run read-only checks (`lsblk`, `blkid`, `df -h`) and report findings; these actions must be explicitly handled by the user."

        if program == "dd" and any(token.startswith("of=/dev/") or token == "of=/dev" for token in tokens):
            return "Raw disk writes to /dev are blocked. Run read-only disk checks (`lsblk`, `blkid`) and use file-level tools where possible; ask for exact approval before any device write."

        if program in {"shutdown", "reboot", "halt", "poweroff"}:
            return "Power-management commands are blocked. If restart is needed, first report service/process state and ask the user to perform or explicitly approve the host power action."

        if program == "systemctl" and contains_any(tokens, {"stop", "restart", "reload", "disable", "mask", "kill"}):
            return "Service mutation is blocked. First run `systemctl status <service> --no-pager`, inspect recent logs with `journalctl -u <service> -n 100 --no-pager`, and test config if applicable (`nginx -t`, `angie -t`, or app-specific check). Then ask for the exact service action."

        if program == "service" and contains_any(tokens, {"stop", "restart", "reload"}):
            return "Service mutation is blocked. First run the equivalent status/log inspection (`service <name> status` or `systemctl status`, plus recent logs), then ask for the exact service action."

        if program == "journalctl" and any(token.startswith("--vacuum-") for token in tokens):
            return "Journal vacuum deletes logs. First run `journalctl --disk-usage` and identify the retention target, then ask the user for exact cleanup approval."

        if program == "go" and len(tokens) >= 3 and tokens[1] == "env" and "-w" in tokens:
            return "go env -w mutates persistent Go configuration. First run `go env <KEY>` or `go env`, explain the intended change, then ask before retrying."

        if program == "npm" and len(tokens) >= 2 and tokens[1] in {"install", "i", "add"} and any(token in {"-g", "--global"} for token in tokens):
            return "Global npm install mutates the user/system toolchain. Prefer local project install; if a global tool is required, explain why and ask before retrying."

        if program in {"npm", "pnpm", "yarn"} and "audit" in tokens and ("fix" in tokens or "--fix" in tokens):
            return "Package-manager audit fix mutates dependencies and lockfiles. First run the matching read-only audit (`npm audit`, `pnpm audit`, or `yarn audit`) and inspect the diff plan, then ask before applying fixes."

        if program == "curl":
            unsafe_methods = {"POST", "PUT", "PATCH", "DELETE"}
            upper_tokens = {token.upper() for token in tokens}
            sends_body = any(token in {"-d", "--data", "--data-raw", "--data-binary", "--form", "-F"} or token.startswith("--data") for token in tokens)
            if upper_tokens & unsafe_methods or sends_body:
                return "curl with mutating HTTP methods or request bodies is not auto-approved. First run a read-only `curl -I <url>` or GET inspection, confirm target environment and payload, then ask before retrying the mutating request."

        if program == "wget" and any(token.startswith("--post-") or token in {"--method=POST", "--method=PUT", "--method=PATCH", "--method=DELETE"} for token in tokens):
            return "wget with mutating HTTP methods or request bodies is not auto-approved. First run a read-only `wget --spider <url>` or GET inspection, confirm target environment and payload, then ask before retrying."

        if program == "chmod":
            broad_path = any(token in {"/", "/home", "/home/ubuntu", ".", ".."} for token in tokens)
            unsafe_mode = any(token in {"777", "0777", "a+rwx", "-R"} for token in tokens)
            if has_option(tokens, "-R", "--recursive") or (broad_path and unsafe_mode):
                return "Recursive or broad chmod is blocked. First run `ls -ld <path>` and `namei -l <path>` if available, choose the least-privilege mode, then ask before retrying."

        if program == "chown" and has_option(tokens, "-R", "--recursive"):
            return "Recursive chown is blocked. First run `ls -ld <path>` and `namei -l <path>` if available, confirm the required owner/group, then ask before retrying."

        if program == "git":
            if len(tokens) >= 2 and tokens[1] == "status":
                mark_git_review(workdir, "status")
            if len(tokens) >= 2 and tokens[1] == "diff":
                mark_git_review(workdir, "diff")
            if len(tokens) >= 2 and tokens[1] == "clean" and (has_option(tokens, "-n", "--dry-run")):
                mark_git_review(workdir, "clean_dry_run")
                continue
            if len(tokens) >= 3 and tokens[1] == "reset" and "--hard" in tokens:
                return "git reset --hard is blocked because it discards tracked work. Run `git status --short` and `git diff`; if only your intended edits would be discarded, use a narrower `git restore <path>` flow instead. Ask before retrying reset --hard."
            if len(tokens) >= 2 and tokens[1] == "clean":
                if has_recent_review(workdir, "status", "clean_dry_run"):
                    consume_git_review(workdir)
                else:
                    return "git clean deletes untracked files. Run `git status --short` and `git clean -nd` (or `git clean -ndx` only if ignored files are intentionally in scope), inspect the exact deletion list, then retry this exact command within 5 minutes."
            if len(tokens) >= 2 and tokens[1] == "push" and any(token in {"--force", "--force-with-lease", "-f"} for token in tokens):
                return "Force push is blocked. First run `git status -sb`, `git fetch`, and compare local/remote history (`git log --oneline --decorate --graph --max-count=20`). Prefer non-force push; if history rewrite is intentional, ask before retrying with `--force-with-lease`."
            if len(tokens) >= 2 and tokens[1] in {"switch", "checkout"} and any(token in {"--force", "--discard-changes", "-f"} for token in tokens):
                if has_recent_git_review(workdir):
                    consume_git_review(workdir)
                else:
                    return "Forced git switch/checkout can discard local work. Run `git status --short` and `git diff`, confirm no user work will be lost, then retry this exact command within 5 minutes."
            if len(tokens) >= 2 and tokens[1] == "checkout" and "--" in tokens:
                if has_recent_git_review(workdir):
                    consume_git_review(workdir)
                else:
                    return "git checkout -- <path> discards local changes. Run `git status --short` and `git diff -- <path>`, confirm the path only contains your intended edits, then retry this exact command within 5 minutes."
            if len(tokens) >= 2 and tokens[1] == "restore" and "--staged" not in tokens:
                if has_recent_git_review(workdir):
                    consume_git_review(workdir)
                else:
                    return "git restore can discard local changes. Run `git status --short` and `git diff -- <path>`, confirm the path only contains your intended edits, then retry this exact command within 5 minutes."
            if len(tokens) >= 3 and tokens[1] == "branch" and "-D" in tokens:
                return "Forced branch deletion is blocked. First run `git branch --list`, `git status -sb`, and verify the branch is merged or no longer needed. Ask before retrying `git branch -D <branch>`."
            if len(tokens) >= 3 and tokens[1] == "stash" and tokens[2] in {"clear", "drop"}:
                return "git stash deletion is blocked. First run `git stash list` and, for a specific stash, `git stash show -p <stash>`. Ask before retrying stash deletion."

        if program in {"docker", "podman"}:
            if "prune" in tokens or (len(tokens) >= 3 and tokens[1] == "volume" and tokens[2] in {"rm", "prune"}):
                return "Container prune/volume deletion is blocked. First run `docker system df`, `docker ps -a`, and `docker volume ls` if volumes are involved; report what would be removed, then ask for exact cleanup approval."
            if len(tokens) >= 3 and tokens[1] in {"compose", "container"} and tokens[2] == "down" and "-v" in tokens:
                return "Container teardown with volume deletion is blocked. First run `docker compose ps` and `docker volume ls`, confirm no persistent data will be lost, then ask before removing volumes."

        if program in {"kubectl", "oc"} and len(tokens) >= 2 and tokens[1] in {"delete", "drain", "cordon"}:
            return "Cluster mutation is blocked. First run `kubectl config current-context`, `kubectl get ...`, and `kubectl describe ...` for the target. Confirm namespace/context and blast radius, then ask for exact approval."

        if program == "helm" and len(tokens) >= 2 and tokens[1] in {"uninstall", "delete", "rollback", "upgrade"}:
            return "Helm release mutation is blocked. First run `helm status <release>`, `helm history <release>`, and inspect values/manifests if relevant. Confirm namespace and rollback path, then ask for exact approval."

        if program == "dropdb" or (program == "mysqladmin" and any(token.lower() == "drop" for token in tokens[1:])):
            return "Database deletion is blocked. First list the target database, verify a current backup/restore path, and ask the user for explicit data deletion approval."

    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    command = get_command(payload)
    workdir = get_workdir(payload)
    reason = classify(command, workdir)
    if reason:
        emit_block(reason)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

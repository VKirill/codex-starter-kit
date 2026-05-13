#!/usr/bin/env python3
"""Codex PreToolUse guard for dangerous shell commands."""

from __future__ import annotations

import json
import re
import shlex
import sys


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


def classify(command: str) -> str | None:
    compact = " ".join(command.strip().split())
    if not compact:
        return None

    lowered = compact.lower()
    if re.search(r"\b(drop\s+(database|schema|table)|truncate\s+table)\b", lowered):
        return "SQL drop/truncate detected. Use a read-only query first, make a backup, and ask the user for the exact data mutation."

    for segment in split_segments(command):
        invoked = segment[0].rsplit("/", 1)[-1] if segment else ""
        if invoked in {"sudo", "doas", "pkexec", "su"}:
            return "Privilege escalation is blocked by default. Ask the user for the exact elevated command and run only that approved command."

        program = first_program(segment)
        if not program:
            continue

        tokens = segment
        if program in {"rm", "unlink", "rmdir"}:
            return "Permanent deletion with rm/rmdir/unlink is blocked. Use: ls -ld <path> && gio trash <path> && test ! -e <path>."

        if program in {"shred", "srm"}:
            return "Secure deletion is blocked. Use trash for recoverable deletion, or ask the user for explicit permanent deletion."

        if program in {"mkfs", "mkfs.ext4", "mkfs.xfs", "mkfs.btrfs", "mkswap", "wipefs", "fdisk", "parted", "sgdisk", "gdisk"}:
            return "Disk formatting or partition changes are blocked. These actions must be performed manually by the user."

        if program == "dd" and any(token.startswith("of=/dev/") or token == "of=/dev" for token in tokens):
            return "Raw disk writes to /dev are blocked. Use file-level tools, or ask the user for an exact approved disk command."

        if program in {"shutdown", "reboot", "halt", "poweroff"}:
            return "Power-management commands are blocked. The user must shut down or reboot the host manually."

        if program == "systemctl" and contains_any(tokens, {"stop", "restart", "reload", "disable", "mask", "kill"}):
            return "Service mutation is blocked. Use status/log inspection first, then ask the user for the exact service action."

        if program == "service" and contains_any(tokens, {"stop", "restart", "reload"}):
            return "Service mutation is blocked. Use status/log inspection first, then ask the user for the exact service action."

        if program == "journalctl" and any(token.startswith("--vacuum-") for token in tokens):
            return "Journal vacuum deletes logs. Inspect journal size first and ask the user for exact cleanup approval."

        if program == "go" and len(tokens) >= 3 and tokens[1] == "env" and "-w" in tokens:
            return "go env -w mutates Go configuration. Inspect go env first and ask before changing persistent Go settings."

        if program in {"npm", "pnpm", "yarn"} and "audit" in tokens and ("fix" in tokens or "--fix" in tokens):
            return "Package-manager audit fix mutates dependencies. Run audit first, then ask before applying dependency changes."

        if program == "curl":
            unsafe_methods = {"POST", "PUT", "PATCH", "DELETE"}
            upper_tokens = {token.upper() for token in tokens}
            sends_body = any(token in {"-d", "--data", "--data-raw", "--data-binary", "--form", "-F"} or token.startswith("--data") for token in tokens)
            if upper_tokens & unsafe_methods or sends_body:
                return "curl with mutating HTTP methods or request bodies is not auto-approved. Use read-only HEAD/GET checks first, then ask."

        if program == "wget" and any(token.startswith("--post-") or token in {"--method=POST", "--method=PUT", "--method=PATCH", "--method=DELETE"} for token in tokens):
            return "wget with mutating HTTP methods or request bodies is not auto-approved. Use read-only checks first, then ask."

        if program == "chmod":
            broad_path = any(token in {"/", "/home", "/home/ubuntu", ".", ".."} for token in tokens)
            unsafe_mode = any(token in {"777", "0777", "a+rwx", "-R"} for token in tokens)
            if has_option(tokens, "-R", "--recursive") or (broad_path and unsafe_mode):
                return "Recursive or broad chmod is blocked. Ask the user for the exact target and least-privilege mode."

        if program == "chown" and has_option(tokens, "-R", "--recursive"):
            return "Recursive chown is blocked. Ask the user for the exact target and ownership change."

        if program == "git":
            if len(tokens) >= 3 and tokens[1] == "reset" and "--hard" in tokens:
                return "git reset --hard is blocked because it discards work. Use git status/git diff first, then ask for explicit reset approval."
            if len(tokens) >= 2 and tokens[1] == "clean":
                return "git clean deletes untracked files. Use git clean -nd first and ask the user before deleting."
            if len(tokens) >= 2 and tokens[1] == "push" and any(token in {"--force", "--force-with-lease", "-f"} for token in tokens):
                return "Force push is blocked. Ask the user for explicit approval and prefer --force-with-lease only when justified."
            if len(tokens) >= 3 and tokens[1] == "branch" and "-D" in tokens:
                return "Forced branch deletion is blocked. Ask the user for the exact branch deletion."
            if len(tokens) >= 3 and tokens[1] == "stash" and tokens[2] in {"clear", "drop"}:
                return "git stash deletion is blocked. List stashes first and ask the user for the exact stash."

        if program in {"docker", "podman"}:
            if "prune" in tokens or (len(tokens) >= 3 and tokens[1] == "volume" and tokens[2] in {"rm", "prune"}):
                return "Container prune/volume deletion is blocked. Inspect usage first and ask for exact cleanup approval."
            if len(tokens) >= 3 and tokens[1] in {"compose", "container"} and tokens[2] == "down" and "-v" in tokens:
                return "Container teardown with volume deletion is blocked. Ask the user before removing volumes."

        if program in {"kubectl", "oc"} and len(tokens) >= 2 and tokens[1] in {"delete", "drain", "cordon"}:
            return "Cluster mutation is blocked. Use get/describe/logs first, then ask for exact approval."

        if program == "helm" and len(tokens) >= 2 and tokens[1] in {"uninstall", "delete", "rollback", "upgrade"}:
            return "Helm release mutation is blocked. Inspect release status first, then ask for exact approval."

        if program == "dropdb" or (program == "mysqladmin" and any(token.lower() == "drop" for token in tokens[1:])):
            return "Database deletion is blocked. Create/verify a backup and ask the user for explicit data mutation."

    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    command = get_command(payload)
    reason = classify(command)
    if reason:
        emit_block(reason)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

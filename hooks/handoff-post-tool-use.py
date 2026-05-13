#!/usr/bin/env python3
"""Codex PostToolUse hook with lightweight handoff guidance."""

from __future__ import annotations

import json
import shlex
import sys


SHELL_TOOLS = {"Bash", "shell", "unified_exec", "exec_command"}


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
    return ""


def response_failed(payload: dict) -> bool:
    response = payload.get("tool_response")
    if isinstance(response, dict):
        for key in ("returncode", "exit_code", "status"):
            value = response.get(key)
            if isinstance(value, int) and value != 0:
                return True
            if isinstance(value, str) and value.lower() not in {"0", "success", "ok", "completed"}:
                return True
    text = json.dumps(response, ensure_ascii=False).lower()
    return any(marker in text for marker in ("process exited with code 1", "exit code: 1", "returncode\": 1"))


def package_install_command(command: str) -> bool:
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        return False
    if not tokens:
        return False
    package_managers = {"npm", "pnpm", "yarn", "bun"}
    program = tokens[0].rsplit("/", 1)[-1]
    return program in package_managers and any(token in {"install", "i", "add"} for token in tokens[1:])


def tokenized(command: str) -> list[str]:
    try:
        return shlex.split(command, posix=True)
    except ValueError:
        return []


def git_diff_command(command: str) -> bool:
    tokens = tokenized(command)
    return len(tokens) >= 2 and tokens[0].rsplit("/", 1)[-1] == "git" and tokens[1] == "diff"


def verification_command(command: str) -> bool:
    tokens = tokenized(command)
    if not tokens:
        return False

    program = tokens[0].rsplit("/", 1)[-1]
    lower = [token.lower() for token in tokens]
    joined = " ".join(lower)
    direct = {
        "pytest",
        "vitest",
        "jest",
        "phpunit",
        "rspec",
        "mypy",
        "pyright",
        "basedpyright",
        "eslint",
        "tsc",
        "ruff",
        "black",
        "isort",
    }
    if program in direct:
        return True
    if program in {"npm", "pnpm", "yarn", "bun"} and any(part in joined for part in ("test", "lint", "typecheck", "check", "build", "validate")):
        return True
    if program in {"cargo", "go", "dotnet", "mvn", "gradle", "make", "just", "task"} and any(token in lower for token in ("test", "lint", "check", "build", "verify", "vet")):
        return True
    if program == "python" or program == "python3":
        return "-m" in lower and any(token in lower for token in ("pytest", "mypy", "ruff"))
    return False


def emit_context(context: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": context,
                }
            },
            ensure_ascii=False,
        )
    )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    if str(payload.get("tool_name", "")) not in SHELL_TOOLS:
        return 0

    command = get_command(payload)
    if not command:
        return 0

    if response_failed(payload):
        emit_context(
            "The last shell command failed. Read the full command output, fix the smallest concrete cause, and do not repeat the same command unchanged unless you can explain why the environment has changed."
        )
        return 0

    if package_install_command(command):
        emit_context(
            "A package-manager install/add command completed. Before claiming completion, inspect `git status --short` and relevant package/lockfile diffs, then run the narrowest useful test/build/check command."
        )
        return 0

    if git_diff_command(command):
        emit_context(
            "Use this diff as a self-review checkpoint: verify every changed line maps to the user's task ledger or a discovered shared root cause, and make sure unrelated user work was not touched."
        )
        return 0

    if verification_command(command):
        emit_context(
            "A verification command completed. Before final response, map the result back to each task-ledger acceptance check, inspect `git status --short`/diff, and state any unverified residual risk."
        )
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

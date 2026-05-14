#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path


DEFAULT_SESSION = "codex-claude-bridge"


class BridgeError(RuntimeError):
    pass


def run_tmux(args: list[str], *, input_text: str | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["tmux", *args],
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def require_binary(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise BridgeError(f"required binary not found in PATH: {name}")
    return path


def session_exists(session: str) -> bool:
    result = run_tmux(["has-session", "-t", session], check=False)
    return result.returncode == 0


def start_claude_session(session: str, cwd: Path, claude_args: list[str]) -> bool:
    if session_exists(session):
        return False

    command = ["claude", *claude_args]
    result = subprocess.run(
        ["tmux", "new-session", "-d", "-s", session, "-c", str(cwd), *command],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise BridgeError(result.stderr.strip() or "failed to start tmux session")
    return True


def send_prompt(session: str, prompt: str) -> None:
    buffer_name = f"codex-claude-bridge-{uuid.uuid4().hex}"
    try:
        run_tmux(["load-buffer", "-b", buffer_name, "-"], input_text=prompt)
        run_tmux(["paste-buffer", "-b", buffer_name, "-t", session])
        run_tmux(["send-keys", "-t", session, "Enter"])
    finally:
        run_tmux(["delete-buffer", "-b", buffer_name], check=False)


def capture_pane(session: str, history_lines: int) -> str:
    start = f"-{history_lines}"
    result = run_tmux(["capture-pane", "-t", session, "-p", "-S", start])
    return result.stdout


def extract_marked_response(text: str, request_id: str) -> str | None:
    begin = f"CODEX_TMUX_BRIDGE_BEGIN {request_id}"
    end = f"CODEX_TMUX_BRIDGE_END {request_id}"
    search_end = len(text)
    while True:
        begin_index = text.rfind(begin, 0, search_end)
        if begin_index < 0:
            return None

        content_start = begin_index + len(begin)
        end_index = text.find(end, content_start)
        if end_index < 0:
            return None

        content = text[content_start:end_index].strip()
        if content and content != "<your answer>":
            return content
        search_end = begin_index


def wait_for_response(session: str, request_id: str, timeout: float, interval: float, history_lines: int) -> tuple[str, str]:
    deadline = time.monotonic() + timeout
    last_capture = ""

    while time.monotonic() < deadline:
        last_capture = capture_pane(session, history_lines)
        parsed = extract_marked_response(last_capture, request_id)
        if parsed is not None:
            return parsed, last_capture
        time.sleep(interval)

    return "", last_capture


def build_marked_prompt(user_prompt: str, request_id: str) -> str:
    return f"""You are running in an interactive Claude Code terminal session controlled by tmux.

Return your answer between these exact marker lines:

CODEX_TMUX_BRIDGE_BEGIN {request_id}
<your answer>
CODEX_TMUX_BRIDGE_END {request_id}

Keep the answer concise. Do not edit files or run commands for this smoke test.

User request:
{user_prompt}
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Experimental tmux bridge for an interactive Claude Code session.",
    )
    parser.add_argument("--session", default=DEFAULT_SESSION, help=f"tmux session name (default: {DEFAULT_SESSION})")
    parser.add_argument("--cwd", type=Path, default=Path.cwd(), help="working directory for a new Claude session")
    parser.add_argument("--prompt", help="prompt text to send")
    parser.add_argument("--prompt-file", type=Path, help="file containing prompt text")
    parser.add_argument("--timeout", type=float, default=90.0, help="seconds to wait for marked response")
    parser.add_argument("--interval", type=float, default=2.0, help="poll interval in seconds")
    parser.add_argument("--history-lines", type=int, default=4000, help="tmux capture history lines")
    parser.add_argument("--model", help="model alias for a newly created Claude session, e.g. sonnet or opus")
    parser.add_argument("--raw-prompt", action="store_true", help="send the prompt without marker instructions")
    parser.add_argument("--tail-lines", type=int, default=80, help="raw captured tail lines to include on timeout")
    return parser.parse_args(argv)


def load_prompt(args: argparse.Namespace) -> str:
    if args.prompt and args.prompt_file:
        raise BridgeError("use either --prompt or --prompt-file, not both")
    if args.prompt_file:
        return args.prompt_file.read_text(encoding="utf-8")
    if args.prompt:
        return args.prompt
    return "Reply with a one-sentence smoke-test confirmation."


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        require_binary("tmux")
        require_binary("claude")

        prompt = load_prompt(args)
        request_id = uuid.uuid4().hex[:12]
        claude_args = ["--no-chrome"]
        if args.model:
            claude_args.extend(["--model", args.model])

        created = start_claude_session(args.session, args.cwd.resolve(), claude_args)
        time.sleep(3 if created else 0.5)

        outbound = prompt if args.raw_prompt else build_marked_prompt(prompt, request_id)
        send_prompt(args.session, outbound)
        parsed, raw_capture = wait_for_response(
            args.session,
            request_id,
            args.timeout,
            args.interval,
            args.history_lines,
        )

        output = {
            "ok": bool(parsed) if not args.raw_prompt else True,
            "session": args.session,
            "created_session": created,
            "request_id": request_id,
            "parsed_response": parsed,
            "raw_tail": "\n".join(raw_capture.splitlines()[-args.tail_lines :]),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0 if output["ok"] else 2
    except BridgeError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        error = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        print(json.dumps({"ok": False, "error": error}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

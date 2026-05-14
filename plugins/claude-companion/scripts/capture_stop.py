#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


MARKER_RE = re.compile(r"CODEX_CLAUDE_REVIEW_ID:\s*([A-Za-z0-9_.-]+)")


def sanitize_request_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]", "-", value.strip())[:120]
    return cleaned


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    if os.environ.get("CODEX_CLAUDE_BRIDGE") != "1":
        return 0

    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError as exc:
        print(f"claude-companion capture: invalid hook JSON: {exc}", file=sys.stderr)
        return 0

    if payload.get("stop_hook_active"):
        return 0

    message = payload.get("last_assistant_message") or ""
    match = MARKER_RE.search(message)
    if not match:
        return 0

    request_id = sanitize_request_id(match.group(1))
    expected_id = sanitize_request_id(os.environ.get("CODEX_CLAUDE_BRIDGE_REQUEST_ID", ""))
    if not request_id or request_id != expected_id:
        return 0

    cwd = Path(payload.get("cwd") or os.getcwd()).resolve()
    expected_root = Path(os.environ.get("CODEX_CLAUDE_BRIDGE_PROJECT_ROOT", str(cwd))).resolve()
    try:
        cwd.relative_to(expected_root)
    except ValueError:
        return 0

    bridge_root = Path(os.environ.get("CODEX_CLAUDE_BRIDGE_ROOT", str(expected_root / ".codex" / "claude-bridge"))).resolve()
    inbox_path = bridge_root / "inbox" / f"{request_id}.md"
    if not inbox_path.exists():
        return 0

    outbox = bridge_root / "outbox"
    outbox.mkdir(parents=True, exist_ok=True)
    md_path = outbox / f"{request_id}.md"
    meta_path = outbox / f"{request_id}.json"

    md_path.write_text(message.rstrip() + "\n", encoding="utf-8")
    write_json(
        meta_path,
        {
            "request_id": request_id,
            "review_type": os.environ.get("CODEX_CLAUDE_BRIDGE_MODE"),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "session_id": payload.get("session_id"),
            "transcript_path": payload.get("transcript_path"),
            "cwd": str(cwd),
            "markdown_path": str(md_path),
            "inbox_path": str(inbox_path),
            "status": "captured",
        },
    )

    print(
        json.dumps(
            {
                "systemMessage": f"Claude Companion saved review to {md_path}",
                "suppressOutput": True,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

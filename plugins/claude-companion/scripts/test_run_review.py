#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


def load_runner_module():
    path = Path(__file__).with_name("run_review.py")
    spec = importlib.util.spec_from_file_location("claude_companion_run_review", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


runner = load_runner_module()


class RunReviewHelperTests(unittest.TestCase):
    def test_prompt_visible_wins_over_startup_warning(self) -> None:
        text = "SessionStart:startup hook error\nwarning details\n❯ "
        self.assertEqual(runner.classify_tmux_state(text), "prompt_visible")

    def test_awaiting_input_is_detected_before_prompt_markers(self) -> None:
        text = "Press Enter to continue > "
        self.assertEqual(runner.classify_tmux_state(text), "awaiting_input")

    def test_review_fingerprint_is_order_stable(self) -> None:
        self.assertEqual(
            runner.review_fingerprint({"b": 1, "a": {"d": 4, "c": 3}}),
            runner.review_fingerprint({"a": {"c": 3, "d": 4}, "b": 1}),
        )

    def test_extract_marked_review_ignores_claude_ui_footer(self) -> None:
        text = """noise
CODEX_CLAUDE_REVIEW_ID: abc-123

# Claude Fast Check

## Verdict
OK
────────────────────────────────
❯
Session ───── 1%
"""
        self.assertEqual(
            runner.extract_marked_review("abc-123", text),
            "CODEX_CLAUDE_REVIEW_ID: abc-123\n\n# Claude Fast Check\n\n## Verdict\nOK\n",
        )

    def test_extract_marked_review_rejects_prompt_template_marker(self) -> None:
        text = """Return exactly:

CODEX_CLAUDE_REVIEW_ID: abc-123

# Claude Fast Check

## Verdict
One of: OK | FIX_SMALL_ISSUES | NEEDS_ATTENTION

## High-Signal Issues
- ...
"""
        self.assertIsNone(runner.extract_marked_review("abc-123", text))

    def test_prior_review_ignores_bad_manifest(self) -> None:
        self.assertIsNone(runner.load_prior_review(Path("/path/that/does/not/exist.json")))


if __name__ == "__main__":
    unittest.main()

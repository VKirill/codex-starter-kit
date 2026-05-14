---
name: claude-code-review
description: Use when a completed Codex implementation or current git diff should be reviewed by interactive Claude Code. Trigger on `$claude:diff-review`, `$claude:security-review`, `$claude:test-gap-review`, `$claude:release-readiness-review`, or requests for Claude code review.
---

# Claude Code Review

Use this skill after implementation, before final completion claims, merge, deploy, or handoff.

## Command

```bash
python3 plugins/claude-companion/scripts/run_review.py \
  --mode diff-review \
  --prompt "Review the current diff" \
  --mcp-profile code
```

For specialized modes:

```bash
python3 plugins/claude-companion/scripts/run_review.py --mode security-review --prompt "Review the current diff for security risk" --mcp-profile code
python3 plugins/claude-companion/scripts/run_review.py --mode test-gap-review --prompt "Find missing verification for this diff" --mcp-profile code
python3 plugins/claude-companion/scripts/run_review.py --mode release-readiness-review --prompt "Check whether this is ready to report complete" --mcp-profile code
```

## Integration Contract

When Claude returns findings:

1. Read the returned `outbox_path`.
2. Prioritize P0/P1/P2 findings.
3. Fix accepted findings or explain why they are rejected.
4. Run the narrowest relevant verification after changes.
5. Mention remaining test gaps or residual risks in the final answer.

## Safety

Do not run Claude review if `claude` is missing. This plugin is not an installer and never reads Claude credentials.

Use `--mcp-profile code` for code, security, data, test, and release reviews. It gives Claude read-only Serena and GitNexus context when available. Use `--no-diff` with an explicit `--input` file if the current diff contains unrelated work, secrets risk, or noisy generated files.

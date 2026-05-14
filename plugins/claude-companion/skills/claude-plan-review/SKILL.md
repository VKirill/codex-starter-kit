---
name: claude-plan-review
description: Use when a Superpowers/Codex implementation plan should be reviewed by interactive Claude Code before implementation. Trigger on `$claude:superpowers-plan-review`, `$claude:plan-red-team`, or requests to send a plan to Claude for review.
---

# Claude Plan Review

Use this skill after Codex has drafted a plan and before implementation begins.

## Command

```bash
python3 plugins/claude-companion/scripts/run_review.py \
  --mode superpowers-plan-review \
  --input <plan-path> \
  --prompt "Review this implementation plan before Codex executes it"
```

Use `plan-red-team` for high-risk plans:

```bash
python3 plugins/claude-companion/scripts/run_review.py \
  --mode plan-red-team \
  --input <plan-path> \
  --prompt "Red-team this plan before implementation"
```

## Integration Contract

When Claude returns recommendations:

1. Save a sibling suggestions file named `<plan>.claude-suggestions.md`.
2. Split findings into accepted, partially accepted, rejected, and needs-user-decision.
3. Patch the original plan with accepted recommendations.
4. Do not proceed to implementation while Claude verdict is `NEEDS_REVISION` unless the remaining items require a user decision.

## Safety

Claude is reviewer-only. Do not let it edit files or run commands. The runner sends context through the prompt and captures the answer through the Stop hook.

---
name: claude-companion
description: Use when the user invokes `$claude:<mode>` or asks Codex to run an interactive Claude Code review through tmux. Supports plan, code, security, test, UX, release, and meta review modes. Requires existing `claude` and `tmux`; never installs them.
---

# Claude Companion

Use this skill when the user asks for a Claude review from Codex, especially with command-style prompts like:

- `$claude:superpowers-plan-review`
- `$claude:diff-review`
- `$claude:security-review`
- `$claude:test-gap-review`
- `$claude:release-readiness-review`

## Hard Rules

- Do not install Claude Code.
- Do not install tmux.
- If `claude` is missing, stop and tell the user Claude Companion only works when Claude Code is already installed and authenticated.
- If `claude` exists but `tmux` is missing, stop and tell the user to install tmux manually.
- Do not read, copy, parse, print, or move Claude credentials.
- Do not modify global Claude settings.
- Treat Claude output as advisory. Codex decides what to accept.
- Preserve user work and do not revert unrelated changes.

## Invocation

From the project root, run:

```bash
python3 plugins/claude-companion/scripts/run_review.py --mode <mode> --prompt "<user request>"
```

The runner uses adaptive tmux monitoring. It waits for the Stop hook to create the outbox file, keeps watching while Claude is visibly thinking, fails if the tmux session exits, and uses idle/absolute timeouts only as safety guards.

For deep reviews:

```bash
python3 plugins/claude-companion/scripts/run_review.py \
  --mode second-opinion-opus \
  --prompt "Deep review this plan" \
  --wait-forever \
  --idle-timeout 0
```

For a plan file:

```bash
python3 plugins/claude-companion/scripts/run_review.py \
  --mode superpowers-plan-review \
  --input docs/superpowers/plans/example-plan.md \
  --prompt "Review this plan before implementation"
```

For the current diff:

```bash
python3 plugins/claude-companion/scripts/run_review.py \
  --mode diff-review \
  --prompt "Review the current diff"
```

The runner writes to `.codex/claude-bridge/` when that path is writable. If a project has a read-only `.codex` directory, it falls back to `.claude-bridge/`.

The runner writes:

- `<bridge-root>/inbox/<request_id>.md`
- `<bridge-root>/outbox/<request_id>.md`
- `<bridge-root>/outbox/<request_id>.json`

## Mode Catalog

Planning:

- `superpowers-plan-review`
- `plan-red-team`
- `scope-trimmer`
- `acceptance-checker`
- `risk-register`
- `architecture-decision-review`

Implementation:

- `implementation-strategy`
- `diff-review`
- `minimal-change-review`
- `legacy-safety-review`
- `api-contract-review`
- `data-consistency-review`

Quality:

- `test-gap-review`
- `failure-mode-review`
- `observability-review`
- `performance-review`
- `security-review`
- `privacy-review`

Frontend and product:

- `ux-flow-review`
- `accessibility-review`
- `responsive-review`
- `copy-review`
- `visual-regression-plan`

Delivery:

- `release-readiness-review`
- `rollback-review`
- `incident-premortem`
- `handoff-summary-review`
- `documentation-review`

Meta:

- `second-opinion-opus`
- `fast-sonnet-check`
- `multi-perspective-review`
- `contradiction-finder`
- `user-intent-audit`
- `prompt-quality-review`

## Codex Follow-Up

After the runner succeeds:

1. Read the returned `outbox_path`.
2. Classify each recommendation as `accept`, `partially_accept`, `reject`, or `needs_user_decision`.
3. Patch the plan or implementation only for accepted recommendations.
4. Record rejected recommendations with rationale grounded in user request, AGENTS.md, or code constraints.
5. Run the narrowest relevant verification.

For plan reviews, create or update a sibling file:

```text
<plan>.claude-suggestions.md
```

Then patch the original plan before presenting it as ready.

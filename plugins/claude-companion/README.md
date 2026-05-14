# Claude Companion

Claude Companion is a local Codex plugin for advisory reviews through interactive Claude Code.

It does not install Claude Code and it does not install tmux. If `claude` is not already available, the runner exits before checking tmux. This plugin is only for users who already have Claude Code installed and authenticated.

## Commands

Use the skill command style in Codex:

```text
$claude:superpowers-plan-review review docs/superpowers/plans/example.md
$claude:diff-review review the current diff
$claude:security-review check the current change
```

Or run the script directly:

```bash
python3 plugins/claude-companion/scripts/run_review.py --mode diff-review --prompt "Review the current diff"
```

Long-running reviews use adaptive tmux monitoring. The runner waits for `outbox/<request_id>.md`, checks whether the Claude tmux session is still alive, watches pane activity, and only fails on session exit, idle timeout, or the absolute safety cap.

Useful options:

```bash
python3 plugins/claude-companion/scripts/run_review.py \
  --mode security-review \
  --prompt "Review the current diff" \
  --idle-timeout 300 \
  --timeout 1800

python3 plugins/claude-companion/scripts/run_review.py \
  --mode second-opinion-opus \
  --prompt "Deep review this plan" \
  --wait-forever \
  --idle-timeout 0
```

## Flow

1. Codex builds `.codex/claude-bridge/inbox/<request_id>.md`, or `.claude-bridge/inbox/<request_id>.md` if `.codex` is not writable.
2. The runner starts `claude` in a dedicated `tmux` session with bridge-only settings.
3. Claude answers in interactive mode.
4. The Stop hook writes the matching `outbox/<request_id>.md` and metadata JSON.
5. The runner closes only its own tmux session and returns the outbox path.

## Safety

- No direct credential reads.
- No Claude or tmux auto-install.
- No global Claude settings mutation.
- Claude output is advisory; Codex decides what to accept.

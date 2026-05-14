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

Claude Companion also starts Claude with a strict, runtime-only MCP profile. The runner writes `<bridge-root>/runtime/<request_id>/mcp-config.json` and launches Claude with `--mcp-config ... --strict-mcp-config`, so the review session sees only the curated MCP servers for that mode instead of the user's full MCP environment.

Default profiles:

| Profile | Modes | MCP servers |
| --- | --- | --- |
| `auto` | default; resolves from `--mode` | plan/code/docs profile by mode |
| `plan` | plan and strategy reviews | Serena + GitNexus |
| `code` | diff, security, data, release, incident, test reviews | Serena + GitNexus |
| `docs` | documentation reviews | Serena + GitNexus + Context7 |
| `none` | copy/UX/simple reviews or manual isolation | no MCP servers |

The local profile uses stdio `gitnexus mcp` when `gitnexus` exists and stdio Serena through `uvx`. If a server is unavailable, the prompt tells Claude what evidence is missing and the review continues with supplied context. No MCP configuration is written to the target project's `.mcp.json`.

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

python3 plugins/claude-companion/scripts/run_review.py \
  --mode data-consistency-review \
  --prompt "Audit persistence risks" \
  --mcp-profile code
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

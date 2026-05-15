# Claude Companion

Claude Companion is a local Codex plugin for advisory reviews through interactive Claude Code.

It does not install Claude Code and it does not install tmux. If `claude` is not already available, the runner exits before checking tmux. This plugin is only for users who already have Claude Code installed and authenticated.

## Commands

Use the skill command style in Codex:

```text
$claude:superpowers-plan-review review docs/superpowers/plans/example.md
$claude:code-review review the completed implementation with plan path, changed files, verification, and concrete questions
$claude:security-review check the current change
```

Long-running reviews use adaptive tmux monitoring. The runner first waits for Claude's interactive prompt before sending the review pack, then waits for `outbox/<request_id>.md`, checks whether the Claude tmux session is still alive, watches pane activity, and only fails on session exit, idle timeout, or the absolute safety cap. If Claude prints a marked review but the Stop hook does not write the outbox, the runner captures the marked answer from the tmux pane and writes the outbox itself.

Identical reviews are de-duplicated by a stable request fingerprint. If the same mode, model, MCP profile, input, git status, and verification context already produced an outbox, the runner returns that outbox instead of sending the same prompt again. If the matching review is still running, the runner waits for that tmux session instead of creating a second one. Use `--force` only when you intentionally want a fresh Claude run.

Claude Companion also starts Claude with a strict, runtime-only MCP profile. The runner writes `<bridge-root>/runtime/<request_id>/mcp-config.json` and launches Claude with `--mcp-config ... --strict-mcp-config`, so the review session sees only the curated MCP servers for that mode instead of the user's full MCP environment.

Default profiles:

| Profile | Modes | MCP servers |
| --- | --- | --- |
| `auto` | default; resolves from `--mode` | plan/code/docs profile by mode |
| `plan` | plan and strategy reviews | Serena + GitNexus |
| `code` | code, security, data, release, incident, test reviews | Serena + GitNexus |
| `docs` | documentation reviews | Serena + GitNexus + Context7 |
| `none` | copy/UX/simple reviews or manual isolation | no MCP servers |

The local profile uses stdio `gitnexus mcp` when `gitnexus` exists and stdio Serena through `uvx`. If a server is unavailable, the prompt tells Claude what evidence is missing and the review continues with supplied context. No MCP configuration is written to the target project's `.mcp.json`.

Review requests should include plan path, changed-file list, worker/stage scope,
verification commands and results, known risks, and concrete questions. Codex
invokes the runner internally through the plugin command path.

Each mode injects a compact senior-review methodology into the prompt. The
methodology stays short, but tells Claude how to review that mode: plan review,
code review, security, data consistency, release readiness, UX, accessibility,
or another focused lens.

## Flow

1. Codex builds `.codex/claude-bridge/inbox/<request_id>.md`, or `.claude-bridge/inbox/<request_id>.md` if `.codex` is not writable.
2. The runner starts `claude` in a dedicated `tmux` session with bridge-only settings.
3. The runner waits for Claude's prompt to be ready, then sends the review pack.
4. Claude answers in interactive mode.
5. The Stop hook writes the matching `outbox/<request_id>.md` and metadata JSON; the runner has a tmux-pane fallback if the hook misses a marked answer.
6. The runner closes only its own tmux session and returns the outbox path.

## Safety

- No direct credential reads.
- No Claude or tmux auto-install.
- No global Claude settings mutation.
- Claude output is advisory; Codex decides what to accept.

# Codex Runtime Setup

This starter kit configures runtime integration through `templates/config.recommended.toml`, which the installer writes to `~/.codex/config.toml` by default.

## Installed By Config

The baseline config enables:

- `github@openai-curated`
- `superpowers@openai-curated`
- `plugin_hooks = true`
- Context7 MCP: `https://mcp.context7.com/mcp`
- Vue docs MCP: `https://mcp.vue-mcp.org/mcp`
- Nuxt UI MCP: `https://ui.nuxt.com/mcp`
- Nuxt MCP: `https://nuxt.com/mcp`

Codex should fetch/cache enabled plugin capabilities after restart when the configured plugin system is available.

## Manual Checks

Run these after installation if you want to verify the runtime layer from a terminal:

```bash
codex plugin marketplace upgrade
codex mcp list
```

## Manual MCP Commands

If you do not want to use the starter-kit `config.toml`, add the public docs MCP servers manually:

```bash
codex mcp add context7 --url https://mcp.context7.com/mcp
codex mcp add vue-docs --url https://mcp.vue-mcp.org/mcp
codex mcp add nuxt-ui-remote --url https://ui.nuxt.com/mcp
codex mcp add nuxt-remote --url https://nuxt.com/mcp
```

## Local MCP Servers

Serena, GitNexus, Postgres, browser automation, and other local MCP servers are not enabled by default because they depend on local daemons, ports, tokens, and project-specific indexes. Add them in a project setup layer or uncomment the examples in `templates/config.recommended.toml` after installing those servers.

## Full Local Self-Setup

The one-prompt bootstrap asks Codex to perform a full local workflow preflight and, with approval, install missing tools for the recommended workflow:

- `uv`/`uvx` for Serena
- Serena through `uv tool install -p 3.13 serena-agent@latest --prerelease=allow`
- GitNexus through `npm install -g gitnexus` or `npx -y gitnexus@latest`
- claude-mem through `npx claude-mem@latest install`

Claude Companion is different: it is enabled only when Claude Code CLI already exists on the machine. The starter kit must not install Claude Code automatically. If `claude` is missing, Codex reports Claude Companion as disabled and skips tmux setup for that feature. If `claude` exists but `tmux` is missing, Codex shows the manual tmux install command for the detected package manager instead of installing it automatically.

The bootstrap prompt intentionally keeps approval gates for `sudo`, package-manager installs, global npm installs, daemon startup, and large repository indexing.

Claude credentials must remain owned by Claude Code. The starter kit may detect whether `claude` exists and may open an interactive login flow, but it must not read, copy, parse, print, or move `~/.claude/.credentials.json`, keychain data, cookies, bearer tokens, or API keys.

## Claude Companion Plugin

The starter kit includes a repo-local Claude Companion plugin at:

```text
plugins/claude-companion
```

It is intentionally opt-in. It should be used only on machines where `claude` is already installed and authenticated.

Manual local testing from this repository:

```bash
python3 plugins/claude-companion/scripts/run_review.py \
  --mode fast-sonnet-check \
  --prompt "Smoke test Claude Companion"
```

When Codex supports local marketplace installation for this repository, add this repo as a local marketplace and install `claude-companion`. Until then, the skills document the command-style workflow:

Marketplace metadata is included at:

```text
.agents/plugins/marketplace.json
```

```text
$claude:superpowers-plan-review
$claude:diff-review
$claude:security-review
```

The command-style prefix is handled by the plugin skills: Codex should translate `$claude:<mode>` into a call to `plugins/claude-companion/scripts/run_review.py --mode <mode>`.

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

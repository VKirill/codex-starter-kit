<div align="center">
  <img src="assets/avatar-round.png" alt="Codex Starter Kit" width="112" height="112">

  <h1>Codex Starter Kit</h1>

  <p><em>OpenAI Codex agents, Codex skills, AGENTS.md, hooks, plugins, and MCP setup in one baseline installer.</em></p>

  <p>
    <strong>Reusable OpenAI Codex CLI agents, skills, hooks, MCP baseline config, and global AGENTS.md defaults.</strong>
  </p>

  <p>
    Reset Codex to a ready-to-work baseline with practical AI coding agents, role-based skill allowlists, safe shell hooks, plugins, MCP docs servers, and a one-prompt bootstrap workflow.
  </p>

  <p>
    <a href="https://github.com/VKirill/codex-starter-kit">GitHub Repository</a>
    ·
    <a href="https://t.me/pomogay_marketing">Telegram: @pomogay_marketing</a>
  </p>

  <p>
    <img alt="OpenAI Codex CLI" src="https://img.shields.io/badge/OpenAI-Codex%20CLI-111111">
    <img alt="Custom Agents" src="https://img.shields.io/badge/Codex-Custom%20Agents-blue">
    <img alt="Skills" src="https://img.shields.io/badge/Codex-Skills-purple">
    <img alt="MCP" src="https://img.shields.io/badge/MCP-Ready-green">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green">
  </p>
</div>

## Overview

Codex Starter Kit is a portable OpenAI Codex CLI baseline setup for developers who want production-ready Codex agents, Codex skills, AGENTS.md instructions, hooks, plugin config, and MCP documentation servers without building every workflow from scratch.

It includes:

- global `AGENTS.md` working agreements for any project
- custom Codex subagents in TOML format
- reusable Codex skills under `~/.agents/skills`
- role-based `skills.config` allowlist emulation for subagents
- a defensive shell-command hook for dangerous commands
- a baseline `config.toml` for plugins, project docs, approval defaults, and remote docs MCP servers
- automatic enablement of GitHub and Superpowers plugin entries through Codex config
- public docs MCP servers for Context7, Vue, Nuxt UI, and Nuxt
- a one-prompt Codex bootstrap workflow
- a baseline installer with dry-run, backups, runtime refresh, and validation

Search keywords: OpenAI Codex agents, Codex CLI agents, Codex skills, Codex subagents, AGENTS.md template, Codex MCP setup, Codex hooks, AI coding agents, custom Codex agents and skills, Codex developer workflow, coding agent starter kit.

## Who This Is For

Use this repository if you want to:

- bootstrap Codex on a fresh machine
- share a reusable Codex setup with a team
- install practical custom agents for backend, frontend, review, QA, DevOps, product, design, data, and security work
- reduce skill noise with role-specific subagent skill allowlists
- add safer shell-command guardrails to Codex
- keep global instructions project-agnostic while allowing every repository to define local rules

## Repository Layout

```text
codex-starter-kit/
├── agents/                     # Custom Codex subagents (*.toml)
├── skills/                     # Global Codex skills copied to ~/.agents/skills
├── hooks/                      # Shell safety hook and hook template
├── templates/
│   ├── AGENTS.md               # Global project-agnostic Codex instructions
│   └── config.recommended.toml # Baseline ~/.codex/config.toml
├── prompts/
│   └── bootstrap-codex-starter-kit.md
├── scripts/
│   └── validate-pack.py
├── install.py
└── install.sh
```

## What Gets Installed

By default, the installer replaces these starter-kit managed paths:

```text
~/.codex/AGENTS.md
~/.codex/agents/
~/.agents/skills/
~/.codex/hooks/
~/.codex/hooks.json
~/.codex/config.toml
```

Existing files and directories are moved to timestamped `.bak-*` backups before replacement unless you explicitly run with `--force` or `--no-backup`.

The installer rewrites bundled agent paths from the author machine to your own home directory, so `skills.config` entries point to:

```text
~/.agents/skills/<skill-name>/SKILL.md
```

## Safety Model

The installer is opinionated by default: it turns Codex into this starter kit baseline instead of merging small pieces into an unknown existing setup. It still preserves user work by making timestamped backups first.

- `--dry-run` shows planned replacements without writing
- existing managed files and directories are backed up by default
- `~/.codex/config.toml` is replaced by the baseline config by default
- `~/.codex/agents` and `~/.agents/skills` are replaced as complete starter-kit trees
- agent TOML files are validated after installation
- generated `skills.config` paths are checked after installation
- `codex plugin marketplace upgrade` and `codex mcp list` are run after install when the `codex` CLI is available

Default install with backups:

```bash
./install.sh
```

## Install

Clone the repository:

```bash
git clone https://github.com/VKirill/codex-starter-kit ~/projects/codex-starter-kit
cd ~/projects/codex-starter-kit
```

Validate the pack:

```bash
python3 scripts/validate-pack.py
```

Run a dry run:

```bash
./install.sh --dry-run
```

Install as the baseline with backups:

```bash
./install.sh
```

Validate the installed agents:

```bash
./install.sh --validate-only
```

Restart Codex after installation so global instructions, agents, skills, hooks, and plugin settings are reloaded.

## Baseline Config, Plugins, And MCP

The baseline config lives here:

```text
templates/config.recommended.toml
```

The installer writes it directly to:

```text
~/.codex/config.toml
```

That file enables the official/curated GitHub and Superpowers plugin entries, plugin hooks, project-document discovery defaults, agent concurrency defaults, and public remote docs MCP servers for Context7, Vue, Nuxt UI, and Nuxt. On the next Codex restart, Codex can fetch/cache enabled plugin capabilities from its configured plugin system.

The config intentionally avoids project-specific paths, private bearer tokens, local database settings, and local-only MCP ports. Optional local code-intelligence servers such as Serena, GitNexus, and Postgres are included as commented examples because they require local daemons and environment-specific tokens.

Manual commands for checking runtime integration:

```bash
codex plugin marketplace upgrade
codex mcp list
```

Manual MCP add commands if you do not want to use the baseline config file:

```bash
codex mcp add context7 --url https://mcp.context7.com/mcp
codex mcp add vue-docs --url https://mcp.vue-mcp.org/mcp
codex mcp add nuxt-ui-remote --url https://ui.nuxt.com/mcp
codex mcp add nuxt-remote --url https://nuxt.com/mcp
```

## One-Prompt Codex Setup

If you want Codex to install the starter kit for you, open Codex on the target machine and paste the prompt from:

```text
prompts/bootstrap-codex-starter-kit.md
```

Short version:

```text
Install the Codex Starter Kit from https://github.com/VKirill/codex-starter-kit into ~/projects/codex-starter-kit. Read README.md and install.py, run python3 scripts/validate-pack.py, run ./install.sh --dry-run, show me the planned baseline replacements, then install with ./install.sh if safe. This intentionally replaces starter-kit managed Codex files, but must keep timestamped backups. Validate with ./install.sh --validate-only and tell me to restart Codex.
```

## Agents

The `agents/` directory contains Codex custom agents for common software work:

- backend architecture and API implementation
- frontend development and UI implementation
- code review and minimal-change engineering
- QA, evidence collection, API testing, performance, and accessibility
- DevOps, SRE, sysadmin, and incident response
- data engineering and database optimization
- AI/ML engineering and model QA
- product, project management, workflow architecture, and knowledge work
- design, UX, research, brand, and visual storytelling

Each agent is designed to be narrow enough to be useful and includes role-appropriate settings such as `model_reasoning_effort`, `nickname_candidates`, MCP visibility, and role-based skill pruning.

## Skills

The `skills/` directory contains reusable Codex skills for process and domain work, including:

- planning, task decomposition, and implementation methodology
- clean code, debugging, refactoring, and review
- frontend, React, Vue, Next.js, TypeScript, and UI work
- backend, APIs, Node.js, Fastify, databases, Redis, GraphQL, and auth
- testing, Playwright, QA, performance, and security
- DevOps, Docker, Terraform, sysadmin, Git, and GitHub Actions
- product, roadmap, copywriting, and documentation

Subagents use role-based allowlist emulation through `[[skills.config]] enabled = false` so they see a focused skill menu instead of every installed skill.

## Hooks

The starter kit includes a defensive `PreToolUse` shell hook:

```text
hooks/block-dangerous-shell.py
```

It blocks common destructive shell actions such as:

- `rm`, `rmdir`, `unlink`
- `git reset --hard`, `git clean`, force push
- disk formatting and raw device writes
- broad recursive permission changes
- service shutdown/restart commands
- Docker volume deletion and prune operations
- database drop/truncate commands

The hook is not a replacement for judgment. It is a safety net for common accidents.

## Custom Paths

Install to a custom Codex home:

```bash
./install.sh --codex-home /path/to/.codex
```

Install skills to a custom location:

```bash
./install.sh --skills-home /path/to/skills
```

Skip parts of the baseline install:

```bash
./install.sh --skip-hooks
./install.sh --skip-skills
./install.sh --skip-agents
./install.sh --skip-config
./install.sh --skip-global-agents-md
./install.sh --skip-runtime-refresh
```

## Overwriting Existing Files

Default install replaces managed paths with backups. Use force only when you intentionally want to replace existing files without backups:

```bash
./install.sh --force
```

For first-time setup, prefer the default backup mode:

```bash
./install.sh
```

## Recommended GitHub Topics

Use these topics if you publish the repository:

```text
openai-codex
codex-cli
codex-agents
codex-skills
agents-md
ai-coding-agents
mcp
subagents
developer-tools
coding-agent
```

## Development

Validate the pack:

```bash
python3 scripts/validate-pack.py
```

Run installer dry-run:

```bash
./install.sh --dry-run
```

Validate installed agents:

```bash
./install.sh --validate-only
```

## Safety Notes

- Do not commit secrets, bearer tokens, local project paths, or private MCP config.
- Keep project-specific instructions in each repository's `AGENTS.md`.
- Keep global `AGENTS.md` project-agnostic.
- Use role-based subagent skill allowlists to reduce prompt noise.
- Restart Codex after changing global agents, skills, hooks, or plugins.

## License

MIT

# One-Prompt Codex Bootstrap

Paste this into Codex on a fresh machine to let Codex install this starter kit as the machine's Codex baseline.

```text
Install Codex Starter Kit for OpenAI Codex CLI and verify that the installation is safe.

Repository:
https://github.com/VKirill/codex-starter-kit

Goal:
- make this starter kit the baseline Codex setup on this machine
- install global ~/.codex/AGENTS.md from templates/AGENTS.md
- install custom agents into ~/.codex/agents
- install skills into ~/.agents/skills
- install safety hooks into ~/.codex/hooks and ~/.codex/hooks.json
- install safe command approval rules into ~/.codex/rules
- install the recommended ~/.codex/config.toml from templates/config.recommended.toml
- enable GitHub and Superpowers plugin entries through config.toml
- enable public docs MCP servers for Context7, Vue, Nuxt UI, and Nuxt
- check and document recommended local MCP/plugin routes for Serena, GitNexus, Postgres, Open Design, and claude-mem
- include GitHub/source links for every enabled plugin and recommended MCP/plugin route
- preserve old files with timestamped .bak-* backups

Work step by step:
1. If the repository is missing, clone it into ~/projects/codex-starter-kit.
2. If the repository already exists, enter it and check the current git status.
3. Read README.md, install.py, and templates/config.recommended.toml.
4. Run the pack validation:
   python3 scripts/validate-pack.py
5. Run a dry run:
   ./install.sh --dry-run
6. Show me which paths will be replaced, then count agents and skills separately.
7. If the dry run looks safe, run the install with backups:
   ./install.sh
8. Verify that ~/.codex/config.toml contains GitHub and Superpowers plugins, plus MCP servers context7, vue-docs, nuxt-ui-remote, and nuxt-remote.
9. Report that Serena, GitNexus, Postgres, Open Design, and claude-mem are recommended local/plugin routes for the full starter-kit workflow.
10. For each enabled plugin and recommended MCP/plugin route, show its GitHub/source link from README.md or templates/config.recommended.toml.
11. If any recommended local MCP/plugin is already installed and safe to verify, check it with `codex mcp list` or its own status command. Do not write private ports, local paths, bearer tokens, or database credentials into the public starter-kit files.
12. If the codex command is available, run:
   codex plugin marketplace upgrade
   codex mcp list
13. Validate installed agents:
   ./install.sh --validate-only
14. At the end, briefly summarize what changed, where backups were written, which recommended MCP/plugin routes are active or missing, and that Codex must be restarted.

Safety rules:
- do not delete ~/.codex, ~/.agents, or existing agents/skills without backups
- do not use --force or --no-backup without my explicit approval
- do not copy secrets, bearer tokens, private MCP settings, or local database credentials
- if a command needs elevated access or network approval, explain why first
- if a check fails, stop, show the error, and suggest the smallest safe fix
```

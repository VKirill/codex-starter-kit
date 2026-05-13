# One-Prompt Codex Bootstrap

Paste this into Codex on a fresh machine to let Codex install this starter kit as the machine's Codex baseline.

```text
Install the Codex Starter Kit for OpenAI Codex CLI from GitHub.

Repository:
https://github.com/VKirill/codex-starter-kit

Goal:
- Make this starter kit the baseline Codex setup on this machine
- Replace ~/.codex/AGENTS.md with the starter-kit global instructions
- Replace ~/.codex/agents with the starter-kit custom Codex subagents
- Replace ~/.agents/skills with the starter-kit skill library
- Replace ~/.codex/hooks and ~/.codex/hooks.json with the starter-kit safety hook setup
- Replace ~/.codex/config.toml with the starter-kit baseline config
- Enable GitHub and Superpowers plugin entries through ~/.codex/config.toml
- Enable public docs MCP servers for Context7, Vue, Nuxt UI, and Nuxt through ~/.codex/config.toml
- Preserve previous user files by keeping timestamped .bak-* backups

Steps:
1. Clone the repository into ~/projects/codex-starter-kit, or pull it if it already exists.
2. Read README.md and install.py before making changes.
3. Run the pack validation:
   python3 scripts/validate-pack.py
4. Run a dry run:
   ./install.sh --dry-run
5. Show me the planned baseline replacements and count how many agents and skills will be installed.
6. If the dry run is safe, run the baseline install with backups:
   ./install.sh
7. Confirm that ~/.codex/config.toml now contains the GitHub and Superpowers plugin entries and the Context7/Vue/Nuxt MCP servers.
8. If the codex CLI is available, run:
   codex plugin marketplace upgrade
   codex mcp list
9. Validate generated agents:
   ./install.sh --validate-only
10. Summarize what changed, where backups were written, and tell me to restart Codex.

Safety:
- Do not permanently delete ~/.codex, ~/.agents, or existing agents/skills.
- The installer should move replaced managed files/directories to .bak-* backups.
- Do not use --force or --no-backup unless I explicitly approve it.
- Do not copy secrets, tokens, project-specific paths, local database config, or machine-specific MCP bearer tokens.
- Keep sandboxing and approvals enabled unless I explicitly ask for a specific change.
```

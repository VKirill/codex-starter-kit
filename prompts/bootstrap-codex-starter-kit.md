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
- perform full local workflow self-setup when safe: Serena, GitNexus, and claude-mem
- enable Claude Companion only when Claude Code CLI is already installed; do not install Claude or tmux automatically
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
11. Run full local workflow preflight:
   - detect OS and package manager: apt, dnf, pacman, zypper, brew, or none
   - check commands: tmux, claude, uv, uvx, node, npm, npx, gitnexus
   - check Codex runtime: codex, `codex plugin marketplace upgrade`, `codex mcp list`
   - report missing tools before installing anything
12. If Claude Code CLI is missing, do not install Claude and do not install tmux for Claude Companion. Report that Claude Companion is disabled on this machine until the user installs and authenticates Claude Code manually.
13. If Claude Code CLI exists, verify it with `claude --version`. Then check tmux. If tmux is missing, do not install it automatically; show the manual install command for the detected package manager:
   - Ubuntu/Debian: `sudo apt-get update && sudo apt-get install -y tmux`
   - Fedora/RHEL: `sudo dnf install -y tmux`
   - Arch: `sudo pacman -S --needed tmux`
   - openSUSE: `sudo zypper install -y tmux`
   - macOS: `brew install tmux`
14. Do not read, copy, parse, print, or move Claude credentials. Use Claude Code's own authentication flow only. If Claude is installed but not authenticated, open an interactive `claude` session and ask the user to run `/login`; then re-check. Do not inspect `~/.claude/.credentials.json`, cookies, keychains, bearer tokens, or API keys.
15. If uv/uvx is missing and Serena is requested or absent, install uv after approval using the official Astral installer or the system package manager. Then install and initialize Serena:
   `uv tool install -p 3.13 serena-agent@latest --prerelease=allow`
   `serena init`
   Verify that `serena` is on PATH. Do not hardcode private ports or bearer tokens in public starter-kit files.
16. If GitNexus is missing, install or use it after approval:
   `npm install -g gitnexus`
   or for one-off MCP use:
   `npx -y gitnexus@latest mcp`
   Then run safe checks: `gitnexus --help`, `gitnexus status` in the current repo if applicable. Ask before indexing large repositories. If the user approves indexing this starter-kit repo, run `gitnexus analyze` from the repo root.
17. If claude-mem is missing and the user wants memory continuity, install it after approval:
   `npx claude-mem@latest install`
   Then restart Codex and verify available MCP/tools if safe. If install fails or appears unstable, report the failure and leave it disabled.
18. If recommended local MCP/plugin routes are already installed and safe to verify, check them with `codex mcp list` or their own read-only status command. Do not write private ports, local paths, bearer tokens, or database credentials into public starter-kit files.
19. If the codex command is available, run:
   codex plugin marketplace upgrade
   codex mcp list
20. Validate installed agents:
   ./install.sh --validate-only
21. At the end, briefly summarize what changed, where backups were written, which tools were installed, which recommended MCP/plugin routes are active or missing, what still needs manual login, and that Codex must be restarted.

Safety rules:
- do not delete ~/.codex, ~/.agents, or existing agents/skills without backups
- do not use --force or --no-backup without my explicit approval
- do not copy secrets, bearer tokens, private MCP settings, or local database credentials
- do not install Claude Code or tmux automatically; Claude Companion is opt-in for machines where Claude already exists
- do not read Claude credentials directly; always delegate authentication to Claude Code
- ask before sudo, package-manager installs, global npm installs, `curl | sh`, large repo indexing, daemon startup, or service changes
- prefer read-only checks before mutation; if an install fails, stop and show the smallest safe fix
- if a command needs elevated access or network approval, explain why first
- if a check fails, stop, show the error, and suggest the smallest safe fix
```

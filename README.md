<div align="center">
  <img src="assets/avatar-round.png" alt="Codex Starter Kit" width="112" height="112">

  <h1>Codex Starter Kit</h1>

  <p><strong>A ready-to-use baseline for OpenAI Codex CLI: agents, skills, hooks, MCP, plugins, and global AGENTS.md.</strong></p>

  <p>
    Install it once, restart Codex, and get a practical working setup for development, review, QA, DevOps, design, product, data, and security work.
  </p>

  <p>
    <a href="README.md">English</a>
    ·
    <a href="README-RU.md">Русская версия</a>
  </p>

  <p>
    <a href="https://github.com/VKirill/codex-starter-kit">GitHub Repository</a>
    ·
    <a href="https://t.me/pomogay_marketing">Telegram: @pomogay_marketing</a>
  </p>

  <p>
    <img alt="OpenAI Codex CLI" src="https://img.shields.io/badge/OpenAI-Codex%20CLI-111111">
    <img alt="Agents" src="https://img.shields.io/badge/62-Custom%20Agents-2563eb">
    <img alt="Skills" src="https://img.shields.io/badge/101-Skills-7c3aed">
    <img alt="MCP" src="https://img.shields.io/badge/MCP-Context7%20%7C%20Vue%20%7C%20Nuxt-16a34a">
    <img alt="Hooks" src="https://img.shields.io/badge/Hooks-Safety%20Guard-f97316">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-059669">
  </p>
</div>

## What This Is

`codex-starter-kit` turns a clean Codex CLI setup into a ready working environment.

It includes:

- 62 custom Codex agents in `agents/*.toml`
- 101 reusable skills in `skills/*/SKILL.md`
- global Codex working rules in `templates/AGENTS.md`
- a shell safety hook for risky commands
- default command approval rules in `rules/default.rules`
- a baseline `~/.codex/config.toml` with GitHub and Superpowers plugins
- public docs MCP servers: Context7, Vue, Nuxt UI, and Nuxt
- recommended local MCP routes for Serena, GitNexus, Postgres, Open Design, and claude-mem
- an installer with `--dry-run`, backups, runtime refresh, and validation

The point is simple: you do not rebuild a Codex workflow from scratch. Install the baseline, verify it, then keep project-specific rules in each repository's local `AGENTS.md`.

## Fast Path

If you want Codex to install this kit for you, open Codex on the target machine and paste this prompt.

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

## Manual Install

Clone the repository:

```bash
git clone https://github.com/VKirill/codex-starter-kit ~/projects/codex-starter-kit
cd ~/projects/codex-starter-kit
```

Validate the pack:

```bash
python3 scripts/validate-pack.py
```

Preview what the installer will replace:

```bash
./install.sh --dry-run
```

Install the baseline with backups:

```bash
./install.sh
```

Validate installed agents:

```bash
./install.sh --validate-only
```

Restart Codex after installation. Global instructions, agents, skills, hooks, and plugins may not load until the next Codex session.

## What Gets Installed

| Path | What goes there | Why |
| --- | --- | --- |
| `~/.codex/AGENTS.md` | global working rules | consistent Codex behavior across projects |
| `~/.codex/agents/` | 62 custom subagents | roles for development, review, QA, DevOps, product, design, and copywriting |
| `~/.agents/skills/` | 101 skills | reusable instructions for tasks and domains |
| `~/.codex/hooks/` | safety and handoff hook scripts | guards risky shell commands, auto-approves known safe permission prompts, and nudges verification after installs/failures |
| `~/.codex/hooks.json` | hook config | connects PermissionRequest, PreToolUse, and PostToolUse hooks to Codex |
| `~/.codex/rules/` | command approval rules | auto-approves common read-only development, Linux, package metadata, and diagnostics commands |
| `~/.codex/config.toml` | baseline config | plugins, MCP servers, approvals, docs discovery |

By default, the installer replaces managed paths only after moving existing files to timestamped `.bak-*` backups.

## Agent Map

Agents live in `agents/*.toml`. Each agent has a narrow role, its own `model_reasoning_effort`, nickname candidates, and a focused skill set.

| Category | Use it for | Agents |
| --- | --- | --- |
| <img alt="Orchestration" src="https://img.shields.io/badge/Flow-Orchestration-0f172a"> | handoff intake scoring, task ledgers, planning, workflows, coordination | `agents_orchestrator`, `project_manager_senior`, `specialized_workflow_architect`, `automation_governance_architect` |
| <img alt="Engineering" src="https://img.shields.io/badge/Build-Engineering-2563eb"> | backend, frontend, mobile, CMS, architecture, code | `engineering_backend_architect`, `engineering_frontend_developer`, `engineering_senior_developer`, `engineering_software_architect`, `engineering_minimal_change_engineer`, `engineering_rapid_prototyper`, `engineering_mobile_app_builder`, `engineering_cms_developer`, `engineering_codebase_onboarding_engineer`, `engineering_code_reviewer`, `engineering_technical_writer`, `engineering_git_workflow_master`, `lsp_index_engineer`, `terminal_integration_specialist`, `specialized_mcp_builder`, `specialized_developer_advocate` |
| <img alt="Data and AI" src="https://img.shields.io/badge/Data-AI%20%26%20Pipelines-7c3aed"> | ML, data pipelines, databases, email/audio intelligence | `engineering_ai_engineer`, `engineering_ai_data_remediation_engineer`, `engineering_data_engineer`, `engineering_database_optimizer`, `engineering_email_intelligence_engineer`, `engineering_voice_ai_integration_engineer`, `specialized_model_qa` |
| <img alt="Ops and Security" src="https://img.shields.io/badge/Ops-Security%20%26%20Reliability-dc2626"> | infrastructure, incidents, security, compliance | `engineering_devops_automator`, `engineering_sre`, `engineering_security_engineer`, `engineering_threat_detection_engineer`, `engineering_incident_response_commander`, `engineering_autonomous_optimization_architect`, `compliance_auditor` |
| <img alt="Testing" src="https://img.shields.io/badge/Proof-Testing%20%26%20QA-16a34a"> | checks, evidence, accessibility, performance | `testing_api_tester`, `testing_evidence_collector`, `testing_accessibility_auditor`, `testing_performance_benchmarker`, `testing_reality_checker`, `testing_tool_evaluator`, `testing_test_results_analyzer`, `testing_workflow_optimizer` |
| <img alt="Product" src="https://img.shields.io/badge/Product-Delivery%20%26%20Research-f97316"> | roadmaps, feedback, sprints, experiments, delivery | `product_manager`, `product_feedback_synthesizer`, `product_trend_researcher`, `product_sprint_prioritizer`, `product_behavioral_nudge_engine`, `project_management_project_shepherd`, `project_management_experiment_tracker`, `project_management_jira_workflow_steward`, `project_management_studio_operations`, `project_management_studio_producer` |
| <img alt="Design" src="https://img.shields.io/badge/Design-UX%20%26%20Brand-ec4899"> | UI, UX, brand, visuals, research | `design_ui_designer`, `design_ux_architect`, `design_ux_researcher`, `design_brand_guardian`, `design_visual_storyteller`, `design_image_prompt_engineer`, `design_inclusive_visuals_specialist`, `design_whimsy_injector` |
| <img alt="Knowledge" src="https://img.shields.io/badge/Knowledge-Notes%20%26%20Systems-0891b2"> | knowledge bases, notes, cross-domain reasoning | `zk_steward` |

## Skill Groups

Skills live in `skills/`. The installer copies them to `~/.agents/skills`, where agents can use them for sharper task behavior.

| Group | Examples |
| --- | --- |
| Process | `planning-methodology`, `task-decomposition`, `testing-patterns`, `bug-hunter`, `code-review-checklist` |
| Frontend | `frontend-developer`, `react-patterns`, `nextjs-best-practices`, `vue-developer`, `ui-designer`, `playwright-skill` |
| Backend | `nodejs-expert`, `fastify-pro`, `fastapi-pro`, `api-patterns`, `auth-implementation-patterns`, `graphql` |
| Data | `postgresql`, `database-design`, `prisma-expert`, `drizzle-orm-expert`, `redis-patterns`, `data-engineer` |
| Ops | `docker-expert`, `terraform-specialist`, `linux-sysadmin`, `github-actions-templates`, `server-management` |
| Security | `security-audit`, `backend-security-coder`, `find-bugs`, `incident-responder` |
| Product and Docs | `copywriter`, `ru-text`, `roadmap-methodology`, `goal-achievement-review`, `software-architecture` |

Subagents use role-based allowlist emulation through `[[skills.config]] enabled = false`, so each role sees a focused skill menu instead of the whole library.

## Safety Model

The installer runs in baseline mode: it makes this starter kit the main Codex setup on the machine.

Default safeguards:

- `./install.sh --dry-run` previews replacements without writing
- old managed paths are moved to timestamped `.bak-*` backups
- agent TOML files are validated after install
- `skills.config` paths are rewritten for your home directory
- `codex plugin marketplace upgrade` and `codex mcp list` run only when `codex` is available in `PATH`
- `rules/default.rules` reduces routine approval prompts for read-only commands such as package metadata checks, Linux inspection commands, service status checks, Docker/Kubernetes/Terraform read-only inspection, and GitHub CLI view/list commands
- npm workspace forms (`npm --workspace`, `npm -w`, `npm --workspaces`, `npm --prefix`) and pnpm workspace forms (`pnpm --filter`, `pnpm -F`, `pnpm --recursive`, `pnpm -r`, `pnpm --dir`, `pnpm -C`) are approved for handoff development workflows
- `hooks/handoff-permission-request.py` auto-approves safe PermissionRequest prompts for MCP calls and commands already covered by `rules/default.rules`, which helps current sessions continue when normal rules were not reloaded yet
- handoff service controls are approved for common app/process managers: `pm2 start|stop|restart|reload`, `supervisorctl start|stop|restart`, `systemctl start|stop|restart|reload`, `service <name> restart`, `docker compose restart`, `docker compose up -d`, direct `docker|podman restart`, and web-server reload commands for nginx/Angie/Apache/Caddy
- the safety hook still blocks destructive or mutating variants such as `git reset --hard`, `git clean`, force pushes, `npm audit fix`, `go env -w`, `journalctl --vacuum-*`, and mutating `curl`/`wget` requests
- persistent host/service mutations such as `systemctl disable`, `systemctl mask`, `systemctl kill`, Docker volume deletion, container prune, and host reboot/shutdown remain blocked or require explicit approval
- hook block messages include the read-only checks Codex should run next; selected Git cleanup/restore commands are allowed once after fresh `git status` plus `git diff` or `git clean -nd` review in the same working directory
- `hooks/handoff-post-tool-use.py` adds follow-up context after package installs and failed shell commands so Codex checks diffs/tests or fixes the concrete failure before repeating work
- MCP servers in this kit use `default_tools_approval_mode = "approve"` for handoff flow; agents must still keep database and local-machine MCP usage read-only unless the user explicitly asks for mutation
- `templates/AGENTS.md` treats "run this plan" as inline execution. Subagents are used only when the user explicitly authorizes delegation, parallel work, or subagents.

Dangerous mode:

```bash
./install.sh --force
```

Use it only when you intentionally want to replace managed files without backups.

## Config, Plugins, MCP

The baseline config lives here:

```text
templates/config.recommended.toml
```

The installer writes it here:

```text
~/.codex/config.toml
```

The config enables:

- GitHub plugin entry: https://github.com/openai/plugins/tree/main/plugins/github
- Superpowers plugin entry: https://github.com/openai/plugins/tree/main/plugins/superpowers
- project docs discovery defaults
- agent concurrency defaults
- public remote docs MCP servers for Context7, Vue, Nuxt UI, and Nuxt

## MCP Coverage

The starter kit separates portable MCP defaults from recommended local integrations. The local entries are part of the recommended full setup, but they stay commented in the public baseline because they need local daemons, paths, ports, bearer tokens, plugin state, or database credentials.

| MCP or plugin | Status in this repo | Source | Why |
| --- | --- | --- | --- |
| `github@openai-curated` | enabled in `templates/config.recommended.toml` | https://github.com/openai/plugins/tree/main/plugins/github | GitHub repository, issues, pull request, and review workflow support |
| `superpowers@openai-curated` | enabled in `templates/config.recommended.toml` | https://github.com/openai/plugins/tree/main/plugins/superpowers | planning, TDD, debugging, verification, and development workflow skills |
| `context7` | enabled in `templates/config.recommended.toml` | https://github.com/upstash/context7 | public docs server, no local daemon required |
| `vue-docs` | enabled in `templates/config.recommended.toml` | https://github.com/joelbarmettlerUZH/vue-mcp | public Vue ecosystem docs |
| `nuxt-ui-remote` | enabled in `templates/config.recommended.toml` | https://github.com/nuxt/ui | public Nuxt UI docs |
| `nuxt-remote` | enabled in `templates/config.recommended.toml` | https://github.com/nuxt/nuxt | public Nuxt docs |
| `serena` | recommended local MCP; commented example in `templates/config.recommended.toml`; referenced by `templates/AGENTS.md` and agents | https://github.com/oraios/serena | semantic code navigation, references, and targeted edits |
| `gitnexus` | recommended local MCP; commented example in `templates/config.recommended.toml`; referenced by `templates/AGENTS.md` and many agents | https://github.com/abhigyanpatwari/GitNexus | code graph, impact analysis, route maps, execution flows, and repo context |
| `postgres` | recommended local MCP; commented example in `templates/config.recommended.toml`; referenced by `templates/AGENTS.md` and data/API agents | https://github.com/modelcontextprotocol/servers | local database inspection; tool calls are auto-approved for handoff, but agents should stay read-only unless explicitly asked to mutate data |
| `open-design` | recommended local MCP for design workspaces | https://github.com/nexu-io/open-design | local design artifacts, design-system context, and visual handoff |
| `claude-mem` | recommended local plugin/runtime for memory continuity | https://github.com/thedotmack/claude-mem | durable cross-session memory under `~/.claude-mem` and `mcp-search` tools |

`templates/AGENTS.md` intentionally tells Codex to use Serena, GitNexus, Context7, framework docs MCP, Open Design MCP, claude-mem, and database MCP when available. The baseline config enables only the portable public docs servers by default; recommended local integrations must be enabled after their daemons/plugins are installed.

For claude-mem, use its own installer/runtime flow, for example:

```bash
npx claude-mem@latest install
```

After setup, restart Codex and check what the runtime exposes:

```bash
codex mcp list
```

Manual runtime checks:

```bash
codex plugin marketplace upgrade
codex mcp list
```

Manual MCP add commands if you do not use the baseline config:

```bash
codex mcp add context7 --url https://mcp.context7.com/mcp
codex mcp add vue-docs --url https://mcp.vue-mcp.org/mcp
codex mcp add nuxt-ui-remote --url https://ui.nuxt.com/mcp
codex mcp add nuxt-remote --url https://nuxt.com/mcp
```

## Custom Paths

Use a different Codex home:

```bash
./install.sh --codex-home /path/to/.codex
```

Use a different skills home:

```bash
./install.sh --skills-home /path/to/skills
```

Skip parts of the install:

```bash
./install.sh --skip-hooks
./install.sh --skip-rules
./install.sh --skip-skills
./install.sh --skip-agents
./install.sh --skip-config
./install.sh --skip-global-agents-md
./install.sh --skip-runtime-refresh
```

## Repository Layout

```text
codex-starter-kit/
├── agents/                     # Custom Codex subagents (*.toml)
├── skills/                     # Skills copied to ~/.agents/skills
├── hooks/                      # Shell safety hook and hook template
├── rules/                      # Codex command approval rules
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

## Development

Validate the pack:

```bash
python3 scripts/validate-pack.py
```

Check installer dry run:

```bash
./install.sh --dry-run
```

Validate installed agents:

```bash
./install.sh --validate-only
```

## What Not To Do

- Do not commit secrets, bearer tokens, or private MCP config.
- Do not put project-specific rules in the global `AGENTS.md`.
- Do not run `--force` if you need backups.
- Do not add local-only MCP ports to the public baseline config.

Keep project-specific instructions in each repository's local `AGENTS.md`.

## GitHub Topics

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

Search keywords: OpenAI Codex agents, Codex CLI agents, Codex skills, Codex subagents, AGENTS.md template, Codex MCP setup, Codex hooks, AI coding agents, custom Codex agents and skills, Codex developer workflow, coding agent starter kit.

## License

MIT

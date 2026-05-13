<div align="center">
  <img src="assets/avatar-round.png" alt="Codex Starter Kit" width="112" height="112">

  <h1>Codex Starter Kit</h1>

  <p><strong>Готовый стартовый набор для OpenAI Codex CLI: агенты, skills, hooks, MCP, plugins и глобальный AGENTS.md.</strong></p>

  <p>
    Установите один раз, перезапустите Codex и получите рабочую базу для разработки, ревью, QA, DevOps, дизайна, продукта, данных и безопасности.
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
    <img alt="Agents" src="https://img.shields.io/badge/61-Custom%20Agents-2563eb">
    <img alt="Skills" src="https://img.shields.io/badge/100-Skills-7c3aed">
    <img alt="MCP" src="https://img.shields.io/badge/MCP-Context7%20%7C%20Vue%20%7C%20Nuxt-16a34a">
    <img alt="Hooks" src="https://img.shields.io/badge/Hooks-Safety%20Guard-f97316">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-059669">
  </p>
</div>

## Что Это

`codex-starter-kit` превращает чистый Codex CLI в готовую рабочую среду.

Внутри уже лежат:

- 61 кастомный Codex-агент в `agents/*.toml`
- 100 reusable skills в `skills/*/SKILL.md`
- глобальные правила работы Codex в `templates/AGENTS.md`
- безопасный shell hook против опасных команд
- базовый `~/.codex/config.toml` с GitHub и Superpowers plugins
- публичные docs MCP: Context7, Vue, Nuxt UI, Nuxt
- рекомендованные локальные MCP-маршруты для Serena, GitNexus, Postgres, Open Design и claude-mem
- установщик с `--dry-run`, backup-режимом и валидацией

Главная идея простая: вы не собираете рабочий Codex-процесс с нуля. Вы ставите базу, проверяете ее и дальше настраиваете под свои проекты через локальные `AGENTS.md`.

## Быстрый Путь

Если вы хотите, чтобы Codex сам сделал установку, откройте Codex на нужной машине и вставьте prompt из следующего блока.

```text
Ты должен установить Codex Starter Kit для OpenAI Codex CLI и проверить, что установка безопасна.

Репозиторий:
https://github.com/VKirill/codex-starter-kit

Цель:
- сделать этот starter kit базовой настройкой Codex на этой машине
- установить глобальный ~/.codex/AGENTS.md из templates/AGENTS.md
- установить кастомных агентов в ~/.codex/agents
- установить skills в ~/.agents/skills
- установить safety hooks в ~/.codex/hooks и ~/.codex/hooks.json
- установить рекомендуемый ~/.codex/config.toml из templates/config.recommended.toml
- включить GitHub и Superpowers plugin entries через config.toml
- включить public docs MCP servers для Context7, Vue, Nuxt UI и Nuxt
- проверить и описать recommended local MCP/plugin routes для Serena, GitNexus, Postgres, Open Design и claude-mem
- добавить GitHub/source links для каждого включенного plugin и recommended MCP/plugin route
- сохранить старые файлы через timestamped .bak-* backups

Работай пошагово:
1. Если репозитория еще нет, клонируй его в ~/projects/codex-starter-kit.
2. Если репозиторий уже есть, перейди в него и проверь текущее состояние git.
3. Прочитай README.md, README-RU.md, install.py и templates/config.recommended.toml.
4. Запусти проверку пакета:
   python3 scripts/validate-pack.py
5. Запусти dry run:
   ./install.sh --dry-run
6. Покажи мне, какие пути будут заменены, и отдельно посчитай агентов и skills.
7. Если dry run выглядит безопасно, запусти установку с backup-режимом:
   ./install.sh
8. Проверь, что ~/.codex/config.toml содержит GitHub и Superpowers plugins, а также MCP servers context7, vue-docs, nuxt-ui-remote и nuxt-remote.
9. Сообщи, что Serena, GitNexus, Postgres, Open Design и claude-mem — recommended local/plugin routes для полноценного starter-kit workflow.
10. Для каждого включенного plugin и recommended MCP/plugin route покажи GitHub/source link из README.md или templates/config.recommended.toml.
11. Если recommended local MCP/plugin уже установлен и его безопасно проверить, проверь через `codex mcp list` или его status-команду. Не записывай private ports, local paths, bearer tokens или database credentials в публичные файлы starter kit.
12. Если команда codex доступна, запусти:
   codex plugin marketplace upgrade
   codex mcp list
13. Проверь установленных агентов:
   ./install.sh --validate-only
14. В конце кратко напиши, что изменилось, где лежат backups, какие recommended MCP/plugin routes активны или отсутствуют, и что нужно перезапустить Codex.

Правила безопасности:
- не удаляй ~/.codex, ~/.agents или существующие agents/skills без backup
- не используй --force и --no-backup без моего явного разрешения
- не копируй secrets, bearer tokens, приватные MCP настройки и локальные database credentials
- если команда требует повышенного доступа или сетевого разрешения, сначала объясни зачем
- если проверка падает, остановись, покажи ошибку и предложи самый маленький безопасный fix
```

## Ручная Установка

Клонируйте репозиторий:

```bash
git clone https://github.com/VKirill/codex-starter-kit ~/projects/codex-starter-kit
cd ~/projects/codex-starter-kit
```

Проверьте пакет:

```bash
python3 scripts/validate-pack.py
```

Посмотрите, что установщик собирается заменить:

```bash
./install.sh --dry-run
```

Установите baseline с backup-режимом:

```bash
./install.sh
```

Проверьте установленных агентов:

```bash
./install.sh --validate-only
```

После установки перезапустите Codex. Без перезапуска глобальные инструкции, agents, skills, hooks и plugins могут не подхватиться.

## Что Будет Установлено

| Путь | Что туда попадет | Зачем |
| --- | --- | --- |
| `~/.codex/AGENTS.md` | глобальные рабочие правила | единое поведение Codex во всех проектах |
| `~/.codex/agents/` | 61 кастомный subagent | роли для разработки, ревью, QA, DevOps, продукта и дизайна |
| `~/.agents/skills/` | 100 skills | reusable инструкции для задач и доменов |
| `~/.codex/hooks/` | safety hook scripts | блокировка частых опасных shell-команд |
| `~/.codex/hooks.json` | hook config | подключение safety hook к Codex |
| `~/.codex/config.toml` | baseline config | plugins, MCP servers, approvals, docs discovery |

По умолчанию установщик заменяет managed paths и сначала переносит старые файлы в `.bak-*` backups.

## Карта Агентов

Агенты лежат в `agents/*.toml`. Каждый агент имеет узкую роль, свой `model_reasoning_effort`, варианты nickname и ограниченный набор skills.

| Категория | Когда выбирать | Агенты |
| --- | --- | --- |
| <img alt="Orchestration" src="https://img.shields.io/badge/Flow-Orchestration-0f172a"> | большая задача, план, workflow, координация | `agents_orchestrator`, `project_manager_senior`, `specialized_workflow_architect`, `automation_governance_architect` |
| <img alt="Engineering" src="https://img.shields.io/badge/Build-Engineering-2563eb"> | backend, frontend, mobile, CMS, архитектура, код | `engineering_backend_architect`, `engineering_frontend_developer`, `engineering_senior_developer`, `engineering_software_architect`, `engineering_minimal_change_engineer`, `engineering_rapid_prototyper`, `engineering_mobile_app_builder`, `engineering_cms_developer`, `engineering_codebase_onboarding_engineer`, `engineering_code_reviewer`, `engineering_technical_writer`, `engineering_git_workflow_master`, `lsp_index_engineer`, `terminal_integration_specialist`, `specialized_mcp_builder`, `specialized_developer_advocate` |
| <img alt="Data and AI" src="https://img.shields.io/badge/Data-AI%20%26%20Pipelines-7c3aed"> | ML, data pipelines, databases, email/audio intelligence | `engineering_ai_engineer`, `engineering_ai_data_remediation_engineer`, `engineering_data_engineer`, `engineering_database_optimizer`, `engineering_email_intelligence_engineer`, `engineering_voice_ai_integration_engineer`, `specialized_model_qa` |
| <img alt="Ops and Security" src="https://img.shields.io/badge/Ops-Security%20%26%20Reliability-dc2626"> | infrastructure, incidents, security, compliance | `engineering_devops_automator`, `engineering_sre`, `engineering_security_engineer`, `engineering_threat_detection_engineer`, `engineering_incident_response_commander`, `engineering_autonomous_optimization_architect`, `compliance_auditor` |
| <img alt="Testing" src="https://img.shields.io/badge/Proof-Testing%20%26%20QA-16a34a"> | проверки, evidence, accessibility, performance | `testing_api_tester`, `testing_evidence_collector`, `testing_accessibility_auditor`, `testing_performance_benchmarker`, `testing_reality_checker`, `testing_tool_evaluator`, `testing_test_results_analyzer`, `testing_workflow_optimizer` |
| <img alt="Product" src="https://img.shields.io/badge/Product-Delivery%20%26%20Research-f97316"> | roadmap, feedback, sprint, эксперименты, delivery | `product_manager`, `product_feedback_synthesizer`, `product_trend_researcher`, `product_sprint_prioritizer`, `product_behavioral_nudge_engine`, `project_management_project_shepherd`, `project_management_experiment_tracker`, `project_management_jira_workflow_steward`, `project_management_studio_operations`, `project_management_studio_producer` |
| <img alt="Design" src="https://img.shields.io/badge/Design-UX%20%26%20Brand-ec4899"> | UI, UX, brand, визуалы, research | `design_ui_designer`, `design_ux_architect`, `design_ux_researcher`, `design_brand_guardian`, `design_visual_storyteller`, `design_image_prompt_engineer`, `design_inclusive_visuals_specialist`, `design_whimsy_injector` |
| <img alt="Knowledge" src="https://img.shields.io/badge/Knowledge-Notes%20%26%20Systems-0891b2"> | knowledge base, notes, cross-domain reasoning | `zk_steward` |

## Skills По Смыслу

Skills находятся в `skills/`. Они ставятся в `~/.agents/skills` и помогают агентам работать точнее.

| Группа | Примеры |
| --- | --- |
| Process | `planning-methodology`, `task-decomposition`, `testing-patterns`, `bug-hunter`, `code-review-checklist` |
| Frontend | `frontend-developer`, `react-patterns`, `nextjs-best-practices`, `vue-developer`, `ui-designer`, `playwright-skill` |
| Backend | `nodejs-expert`, `fastify-pro`, `fastapi-pro`, `api-patterns`, `auth-implementation-patterns`, `graphql` |
| Data | `postgresql`, `database-design`, `prisma-expert`, `drizzle-orm-expert`, `redis-patterns`, `data-engineer` |
| Ops | `docker-expert`, `terraform-specialist`, `linux-sysadmin`, `github-actions-templates`, `server-management` |
| Security | `security-audit`, `backend-security-coder`, `find-bugs`, `incident-responder` |
| Product and Docs | `copywriter`, `roadmap-methodology`, `goal-achievement-review`, `software-architecture` |

Subagents use role-based allowlist emulation through `[[skills.config]] enabled = false`, so each role sees a focused skill menu instead of the whole library.

## Safety Model

Installer работает в baseline mode: он делает этот starter kit главным набором Codex-настроек.

Защита по умолчанию:

- `./install.sh --dry-run` показывает будущие замены без записи
- старые managed paths уходят в timestamped `.bak-*` backups
- agent TOML проверяется после установки
- `skills.config` paths переписываются под ваш home directory
- `codex plugin marketplace upgrade` и `codex mcp list` запускаются только если `codex` есть в `PATH`

Опасный режим:

```bash
./install.sh --force
```

Используйте его только если точно хотите заменить managed files без backups.

## Config, Plugins, MCP

Baseline config лежит здесь:

```text
templates/config.recommended.toml
```

Установщик записывает его сюда:

```text
~/.codex/config.toml
```

В config включены:

- GitHub plugin entry: https://github.com/openai/plugins/tree/main/plugins/github
- Superpowers plugin entry: https://github.com/openai/plugins/tree/main/plugins/superpowers
- project docs discovery defaults
- agent concurrency defaults
- public remote docs MCP servers для Context7, Vue, Nuxt UI и Nuxt

## MCP Coverage

Starter kit разделяет переносимые MCP defaults и recommended local integrations. Локальные entries входят в рекомендованный full setup, но остаются commented в public baseline, потому что им нужны local daemons, paths, ports, bearer tokens, plugin state или database credentials.

| MCP или plugin | Статус в репозитории | Source | Почему |
| --- | --- | --- | --- |
| `github@openai-curated` | включен в `templates/config.recommended.toml` | https://github.com/openai/plugins/tree/main/plugins/github | GitHub repositories, issues, pull requests и review workflow |
| `superpowers@openai-curated` | включен в `templates/config.recommended.toml` | https://github.com/openai/plugins/tree/main/plugins/superpowers | planning, TDD, debugging, verification и development workflow skills |
| `context7` | включен в `templates/config.recommended.toml` | https://github.com/upstash/context7 | публичный docs server, локальный daemon не нужен |
| `vue-docs` | включен в `templates/config.recommended.toml` | https://github.com/joelbarmettlerUZH/vue-mcp | публичная документация Vue ecosystem |
| `nuxt-ui-remote` | включен в `templates/config.recommended.toml` | https://github.com/nuxt/ui | публичная документация Nuxt UI |
| `nuxt-remote` | включен в `templates/config.recommended.toml` | https://github.com/nuxt/nuxt | публичная документация Nuxt |
| `serena` | recommended local MCP; commented example в `templates/config.recommended.toml`; упоминается в `templates/AGENTS.md` и agents | https://github.com/oraios/serena | semantic code navigation, references и targeted edits |
| `gitnexus` | recommended local MCP; commented example в `templates/config.recommended.toml`; упоминается в `templates/AGENTS.md` и многих agents | https://github.com/abhigyanpatwari/GitNexus | code graph, impact analysis, route maps, execution flows и repo context |
| `postgres` | recommended local MCP; commented example в `templates/config.recommended.toml`; упоминается в `templates/AGENTS.md` и data/API agents | https://github.com/modelcontextprotocol/servers | local database inspection; лучше read-only без явного подтверждения |
| `open-design` | recommended local MCP для design workspaces | https://github.com/nexu-io/open-design | local design artifacts, design-system context и visual handoff |
| `claude-mem` | recommended local plugin/runtime для memory continuity | https://github.com/thedotmack/claude-mem | durable cross-session memory в `~/.claude-mem` и `mcp-search` tools |

`templates/AGENTS.md` намеренно просит Codex использовать Serena, GitNexus, Context7, framework docs MCP, Open Design MCP, claude-mem и database MCP, когда они доступны. Baseline config по умолчанию включает только переносимые public docs servers; recommended local integrations нужно включать после установки их daemons/plugins.

Для claude-mem используйте его собственный installer/runtime flow, например:

```bash
npx claude-mem@latest install
```

После настройки перезапустите Codex и проверьте, что видит runtime:

```bash
codex mcp list
```

Ручная проверка runtime-интеграции:

```bash
codex plugin marketplace upgrade
codex mcp list
```

Ручное добавление MCP, если вы не используете baseline config:

```bash
codex mcp add context7 --url https://mcp.context7.com/mcp
codex mcp add vue-docs --url https://mcp.vue-mcp.org/mcp
codex mcp add nuxt-ui-remote --url https://ui.nuxt.com/mcp
codex mcp add nuxt-remote --url https://nuxt.com/mcp
```

## Настройка Путей

Другой Codex home:

```bash
./install.sh --codex-home /path/to/.codex
```

Другой skills home:

```bash
./install.sh --skills-home /path/to/skills
```

Установить не все части:

```bash
./install.sh --skip-hooks
./install.sh --skip-skills
./install.sh --skip-agents
./install.sh --skip-config
./install.sh --skip-global-agents-md
./install.sh --skip-runtime-refresh
```

## Структура Репозитория

```text
codex-starter-kit/
├── agents/                     # Custom Codex subagents (*.toml)
├── skills/                     # Skills copied to ~/.agents/skills
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

## Разработка

Проверить пакет:

```bash
python3 scripts/validate-pack.py
```

Проверить dry run:

```bash
./install.sh --dry-run
```

Проверить установленных агентов:

```bash
./install.sh --validate-only
```

## Что Не Делать

- Не коммитьте secrets, bearer tokens и private MCP config.
- Не кладите project-specific правила в global `AGENTS.md`.
- Не запускайте `--force`, если вам нужны backups.
- Не добавляйте local-only MCP ports в public baseline config.

Project-specific инструкции держите в `AGENTS.md` конкретного репозитория.

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

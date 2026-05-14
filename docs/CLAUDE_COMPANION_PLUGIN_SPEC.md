# Claude Companion для Codex: спецификация полноценного plugin-like workflow

Дата: 2026-05-14
Статус: реализованный локальный prototype plugin
Цель: дать Codex управляемый способ отправлять планы и завершённые задачи на ревью в интерактивный Claude Code, получать ответ через файл и автоматически дорабатывать план или работу по рекомендациям.

## 1. Краткое описание

`Claude Companion` — локальный companion-плагин для Codex Starter Kit. Он запускает Claude Code в отдельной интерактивной `tmux`-сессии, отправляет ему подготовленный review-pack и получает результат через проектный `Stop` hook. Hook сохраняет последний ответ Claude в `.codex/claude-bridge/outbox/`, после чего Codex читает файл, анализирует рекомендации и либо вносит правки в план, либо возвращает пользователю review findings.

Главная идея: Claude работает как независимый второй reviewer, но не получает скрытый бесконтрольный доступ к обычным интерактивным сессиям пользователя. Bridge включается только для Codex-запусков.

## 2. Зачем это нужно

Codex хорошо ведёт реализацию, держит контекст текущего workspace и умеет редактировать проект. Claude полезен как независимый reviewer, особенно для:

- проверки плана перед реализацией;
- поиска слабых acceptance checks;
- архитектурной критики;
- code review уже выполненной задачи;
- выявления пропущенных тестов;
- проверки миграций, данных, безопасности и UX-рисков;
- второго мнения перед крупным изменением.

Bridge нужен, чтобы получить эту проверку без `claude -p` и без Agent SDK. Используется обычный interactive Claude Code, но запуск, prompt и сбор результата автоматизируются через `tmux` и project-local hooks.

Текущая реализация находится в `plugins/claude-companion`. Runner использует adaptive tmux monitoring: ждёт появления `outbox/<request_id>.md`, проверяет живость tmux-сессии, отслеживает активность pane и завершает работу по session exit, idle timeout или абсолютному safety cap. Для ручных глубоких аудитов доступен режим `--wait-forever` с отдельным `--idle-timeout`.

Runner также создаёт runtime-only MCP profile для каждой проверки. Временный файл `<bridge-root>/runtime/<request_id>/mcp-config.json` передаётся в Claude через `--mcp-config ... --strict-mcp-config`, поэтому companion-сессия не наследует весь пользовательский или проектный набор MCP. Профиль `auto` включает Serena и GitNexus для plan/code/data/security/release review, Context7 добавляется только для documentation-oriented режимов. Если нужный MCP недоступен, это явно попадает в prompt как missing evidence, а review продолжается на переданном context pack.

## 3. Нецели

Первая версия не должна:

- запускать Claude в глобальных пользовательских настройках;
- менять обычные ручные Claude-сессии;
- давать Claude право редактировать файлы без отдельного режима;
- использовать `claude -p`, Agent SDK или GitHub Actions;
- подменять Codex как основного исполнителя;
- автоматически принимать все рекомендации Claude;
- запускаться в CI;
- отправлять секреты, `.env`, bearer tokens, приватные базы данных или production dumps.

## 4. Ожидаемый результат

После реализации должны быть верны такие наблюдаемые факты:

1. Codex может создать review-pack для плана или diff.
2. Codex может запустить отдельную `tmux`-сессию Claude Code с bridge-only settings.
3. Claude получает проработанный prompt и отвечает в интерактивном режиме.
4. Project-local `Stop` hook сохраняет ответ в markdown-файл.
5. Bridge закрывает только свою `tmux`-сессию после получения результата.
6. Codex читает файл с рекомендациями и применяет их к плану или выводит как findings.
7. Обычный запуск `claude` в проекте не включает bridge hook.

## 5. Архитектура

### 5.1. Компоненты

```text
Codex
  -> claude_companion runner
  -> review-pack builder
  -> bridge-only Claude settings
  -> tmux interactive Claude Code session
  -> Claude Stop hook
  -> outbox markdown/json
  -> Codex recommendation analyzer
```

### 5.2. Директории

Рекомендуемая структура внутри каждого проекта:

```text
.codex/claude-bridge/
  inbox/
    <request_id>.md
  outbox/
    <request_id>.md
    <request_id>.json
  runtime/
    <request_id>.prompt.md
    <request_id>.tmux.json
  hooks/
    capture-stop.py
  claude-settings.json
  run-review.py
  README.md
```

Если это будет оформлено как Codex plugin, исходники плагина могут жить в starter-kit:

```text
plugins/claude-companion/
  .codex-plugin/plugin.json
  skills/
    claude-plan-review/SKILL.md
    claude-code-review/SKILL.md
  scripts/
    run_review.py
    build_review_pack.py
    capture_stop.py
    analyze_recommendations.py
  templates/
    claude-settings.json
    prompts/
      plan-review.md
      code-review.md
      adversarial-review.md
      security-review.md
      ux-review.md
```

### 5.3. Почему hook не в `.claude/settings.json`

Bridge hook нельзя включать в обычный проектный `.claude/settings.json`, иначе он будет срабатывать в ручной работе пользователя.

Правильный вариант: отдельный settings-файл:

```text
.codex/claude-bridge/claude-settings.json
```

Claude запускается так:

```bash
claude --settings .codex/claude-bridge/claude-settings.json --model sonnet
```

Обычный ручной запуск:

```bash
claude
```

не должен загружать bridge hook.

### 5.4. Двойной предохранитель

Даже если bridge settings подключили случайно, hook должен ничего не делать без явных маркеров.

Hook сохраняет ответ только если одновременно выполнены условия:

- переменная окружения `CODEX_CLAUDE_BRIDGE=1`;
- в ответе есть `CODEX_CLAUDE_REVIEW_ID: <request_id>`;
- существует `.codex/claude-bridge/inbox/<request_id>.md`;
- `request_id` проходит allowlist символов;
- `cwd` совпадает с ожидаемым проектным корнем или лежит внутри него.

## 6. Основной lifecycle

### 6.1. Plan review

```text
1. Codex пишет план через Superpowers / planning workflow.
2. Codex сохраняет план:
   docs/superpowers/plans/<topic>-plan.md
3. Codex создаёт review-pack:
   .codex/claude-bridge/inbox/<request_id>.md
4. Codex запускает Claude Companion:
   run-review.py --type plan --request-id <id>
5. Claude пишет рекомендации.
6. Stop hook сохраняет:
   .codex/claude-bridge/outbox/<request_id>.md
7. Codex читает рекомендации.
8. Codex создаёт соседний файл:
   docs/superpowers/plans/<topic>-plan.claude-suggestions.md
9. Codex анализирует предложения и правит исходный план.
10. Codex показывает пользователю финальный план и кратко указывает, какие рекомендации учёл.
```

### 6.2. Code review

```text
1. Codex завершает реализацию.
2. Codex собирает diff, touched files, commands, test output и risks.
3. Claude Companion запускает code review.
4. Claude возвращает findings с severity.
5. Codex читает findings.
6. Codex исправляет подтверждённые P0/P1/P2 проблемы или объясняет, почему не принимает рекомендацию.
7. Codex запускает проверку повторно или сообщает residual risk.
```

## 7. Контракты файлов

### 7.1. Inbox markdown

Файл `.codex/claude-bridge/inbox/<request_id>.md` должен быть самодостаточным.

Обязательные секции:

```md
# Claude Companion Review Pack

Request ID: <request_id>
Review type: plan | code | adversarial | security | ux | tests
Project root: <path>
Created at: <iso8601>
Requested by: Codex

## Objective
...

## Current Plan Or Completed Work
...

## Context Files
...

## Diff Summary
...

## Verification Already Run
...

## Known Risks
...

## Requested Output Contract
...
```

### 7.2. Outbox markdown

Claude должен начинать ответ с маркера:

```md
CODEX_CLAUDE_REVIEW_ID: <request_id>

# Claude Review
...
```

Для plan review обязательны секции:

```md
## Verdict
## Must Fix Before Implementation
## Should Improve
## Missing Acceptance Checks
## Risk Register
## Suggested Plan Patch
## Questions For Codex
```

Для code review обязательны секции:

```md
## Verdict
## Findings
## Missing Tests
## Regression Risks
## Suggested Fix Order
## What Looks Sound
```

### 7.3. Outbox JSON

Metadata-файл:

```json
{
  "request_id": "plan-review-20260514-001",
  "review_type": "plan",
  "created_at": "2026-05-14T01:00:00Z",
  "session_id": "claude-session-id",
  "transcript_path": "/home/ubuntu/.claude/projects/...",
  "cwd": "/home/ubuntu/projects/example",
  "markdown_path": ".codex/claude-bridge/outbox/plan-review-20260514-001.md",
  "status": "captured"
}
```

## 8. Модель безопасности

### 8.1. Разрешения Claude

В первой production-версии Claude должен работать в read-only reviewer mode.

Рекомендуемые настройки:

- запретить `Edit`, `Write`, `MultiEdit`, `NotebookEdit`;
- запретить shell-команды, кроме явно разрешённых read-only команд, если они вообще нужны;
- не подключать MCP с mutation tools;
- не передавать `.env`, secrets, приватные credentials;
- не включать `--dangerously-skip-permissions`;
- не давать Claude право закрывать чужие tmux-сессии.

### 8.2. Закрытие tmux-сессии

Bridge закрывает только свою сессию:

```text
codex-claude-bridge-<request_id>
```

Нельзя закрывать:

- `claude`;
- любые attached-сессии пользователя;
- сессии, имя которых не содержит request id;
- сессии без metadata-файла bridge runtime.

### 8.3. Секреты

Review-pack builder должен исключать:

- `.env`;
- `.env.*`;
- private keys;
- tokens;
- cookies;
- database dumps;
- production logs с персональными данными;
- local MCP bearer tokens;
- `.claude` auth/cache directories;
- `node_modules`, `.git`, build artifacts.

## 9. Режимы работы

### 9.1. `plan-review`

Используется после написания плана и до реализации.

Цель: проверить, что план можно отдать другому coder-agent без дополнительных вопросов.

### 9.2. `code-review`

Используется после реализации.

Цель: найти реальные bugs, regressions, missing tests, unsafe assumptions.

### 9.3. `adversarial-review`

Используется для спорных архитектурных решений.

Цель: заставить reviewer атаковать решение как будущий incident reviewer.

### 9.4. `security-review`

Используется при auth, payments, permissions, file upload, external APIs, database writes.

Цель: проверить threat model, trust boundaries, input validation, secrets handling.

### 9.5. `test-review`

Используется, когда план или diff затрагивает shared behavior.

Цель: найти слабые проверки и предложить минимальный достаточный verification path.

## 10. Методическая база ревью

Промты ниже не пересказывают книги, а превращают профессиональные практики в рабочие чек-листы для reviewer-agent.

Используемые подходы:

- Clean Code: ясность, малые функции, понятные имена, отсутствие скрытых побочных эффектов.
- Code Complete: defensive programming, edge cases, construction quality.
- The Pragmatic Programmer: reversibility, tracer bullets, orthogonality, automation.
- Refactoring: code smells, минимально безопасные изменения, поведение до структуры.
- Working Effectively with Legacy Code: characterization tests, seams, минимизация blast radius.
- Software Engineering at Google: maintainability, ownership, long-term readability.
- Accelerate: small batches, fast feedback, deploy safety.
- Site Reliability Engineering: failure modes, observability, rollback, error budgets.
- Threat Modeling / STRIDE: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege.
- OWASP ASVS style: auth, sessions, input validation, output encoding, secrets.
- ADR practice: context, decision, alternatives, consequences.
- TDD / testing pyramid: unit, integration, contract, E2E по риску.
- Design review practice: user journey, accessibility, responsive constraints, state transitions.

## 11. Prompt: Plan Review

```md
You are Claude acting as an independent senior planning reviewer for Codex.

You are reviewing a plan before implementation. Your job is not to rewrite the whole plan. Your job is to find ambiguity, missing acceptance checks, weak sequencing, hidden dependencies, unsafe assumptions, and verification gaps.

Operating rules:
- Do not edit files.
- Do not run commands.
- Do not ask for broad rewrites if a small patch is enough.
- Be concrete: every recommendation must point to a plan section or a missing artifact.
- Prefer implementation-ready changes over abstract advice.
- Separate blockers from nice-to-have improvements.
- Assume Codex will read your output and patch the plan before implementation.

Use these review lenses:
1. Goal-backward planning: Does the plan start from observable truths?
2. Acceptance checks: Can a coder prove each outcome?
3. Blast radius: Are shared contracts, data, auth, payments, permissions, dates, links, or IDs affected?
4. Sequencing: Are discovery, implementation, migration, verification, and rollback ordered correctly?
5. Testability: Are narrow and broad verification steps matched to risk?
6. Maintainability: Does the plan avoid speculative abstractions and drive-by refactors?
7. Failure modes: What breaks if dependencies, APIs, data, or user input behave unexpectedly?
8. Handoff quality: Could another coder execute this plan without asking clarifying questions?

Output exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Plan Review

## Verdict
One of: APPROVE | APPROVE_WITH_CHANGES | NEEDS_REVISION

## Must Fix Before Implementation
- [severity] [plan section or missing section] Concrete issue and exact recommended change.

## Should Improve
- Concrete improvement.

## Missing Acceptance Checks
- Observable check Codex should add.

## Risk Register
| Risk | Why it matters | Mitigation |
| --- | --- | --- |

## Suggested Plan Patch
Write patch-style markdown bullets that Codex can merge into the plan.

## Questions For Codex
Only ask questions that block implementation. If none, write: None.
```

## 12. Prompt: Superpowers Plan Review

Этот prompt включается после Superpowers writing-plans flow.

```md
You are reviewing a Superpowers-style implementation plan.

Check whether the plan is ready for execution by a coding agent.

Specific checks:
- Does each step fit in one focused coding pass?
- Does each step name exact files or discovery targets?
- Does each step state what must be true after completion?
- Are verification commands attached to the relevant step instead of only at the end?
- Are user-visible behavior changes separated from refactors?
- Are risky operations gated behind explicit confirmation?
- Are subagents used only if the user explicitly authorized delegation?
- Does the plan preserve user work and avoid unrelated cleanup?

Return the standard Claude Plan Review format.
```

## 13. Prompt: Code Review

```md
You are Claude acting as an independent senior code reviewer for Codex.

Review the completed change. Prioritize correctness, regressions, security, data safety, and missing tests. Do not comment on style unless it affects behavior or maintainability.

Severity:
- P0: likely data loss, security issue, production outage, billing/payment/permission breakage.
- P1: likely user-visible bug or broken workflow.
- P2: maintainability or edge-case issue worth fixing before merge.
- P3: minor improvement; do not include unless it is very cheap and concrete.

Review lenses:
1. Correctness: Does the diff satisfy the requested behavior?
2. Regression risk: What existing path may break?
3. Data consistency: Are writes, IDs, dates, links, cache keys, migrations, and concurrency safe?
4. Error handling: Are failure modes explicit and recoverable?
5. Security: Are permissions, auth, validation, secrets, and external inputs handled safely?
6. Tests: Are the most important success and failure paths covered?
7. Simplicity: Did the change add unnecessary abstraction or scope creep?

Output exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Code Review

## Verdict
One of: APPROVE | APPROVE_WITH_FIXES | NEEDS_WORK

## Findings
- P0/P1/P2: File/path/section, problem, why it matters, concrete fix.

## Missing Tests
- Test or verification that should be added or run.

## Regression Risks
- Existing workflow that may be affected.

## Suggested Fix Order
1. Highest-value next fix.

## What Looks Sound
- Mention only meaningful strengths that reduce risk.
```

## 14. Prompt: Adversarial Architecture Review

```md
You are Claude acting as an adversarial architecture reviewer.

Your task is to argue against the proposed design as if you will be accountable for the incident report six months later.

Do not be vague. Find the most plausible ways this plan fails in production or becomes expensive to maintain.

Review lenses:
- Hidden coupling.
- State ownership.
- Race conditions.
- Schema and contract drift.
- Observability gaps.
- Rollback difficulty.
- Migration ordering.
- Cost or token growth.
- Operational burden.
- Human workflow failure.

Output:
CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Adversarial Review

## Verdict
PROCEED | PROCEED_WITH_GUARDS | REDESIGN

## Strongest Objections
- Objection, concrete failure scenario, mitigation.

## Required Guardrails
- Guardrail Codex should add to the plan.

## Simpler Alternative
If a simpler design exists, describe it. If not, write: None.

## Decision Notes
What should be recorded in an ADR or plan note.
```

## 15. Prompt: Security Review

```md
You are Claude acting as an application security reviewer.

Focus on realistic security and abuse risks, not generic warnings.

Review lenses:
- Trust boundaries.
- Authentication and authorization.
- Tenant/user isolation.
- Input validation.
- Output encoding.
- Secrets and token exposure.
- File upload and path traversal.
- SSRF, command injection, SQL/NoSQL injection.
- Dependency and supply-chain assumptions.
- Auditability and repudiation.
- Rate limits and denial of service.

Output:
CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Security Review

## Verdict
LOW_RISK | NEEDS_GUARDS | HIGH_RISK

## Threat Findings
- Severity, attack path, affected asset, recommended mitigation.

## Required Checks
- Concrete checks Codex should add.

## Safe Defaults
- Defaults or deny rules the implementation should enforce.
```

## 16. Prompt: Test Strategy Review

```md
You are Claude acting as a test strategy reviewer.

Your job is to make verification proportional to risk. Do not demand broad test suites for a tiny change. Do demand stronger checks when shared contracts, data, auth, payments, permissions, dates, or external APIs are affected.

Review lenses:
- Happy path.
- Error path.
- Boundary values.
- Backward compatibility.
- Persistence and concurrency.
- UI states and responsive behavior.
- Observability and logs.
- Manual verification when automation is unavailable.

Output:
CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Test Review

## Verdict
ENOUGH | ADD_NARROW_CHECKS | ADD_BROAD_CHECKS

## Required Verification
- Command or manual check, why it matters, expected result.

## Optional Verification
- Useful but not blocking.

## Gaps In Current Plan
- Missing check and suggested placement in the plan.
```

## 17. Prompt: UX/UI Review

```md
You are Claude acting as a pragmatic UX reviewer for a working product, not a marketing page.

Focus on user workflows, visible states, accessibility, text fit, responsive behavior, and failure states.

Review lenses:
- Primary task completion.
- Empty/loading/error/success states.
- Keyboard and screen-reader basics.
- Text overflow and layout stability.
- Mobile and desktop constraints.
- Destructive action confirmation.
- Form validation and recovery.
- Consistency with existing UI patterns.

Output:
CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude UX Review

## Verdict
READY | NEEDS_UX_FIXES | NEEDS_REWORK

## Workflow Findings
- User-visible problem, affected screen/state, recommended fix.

## Accessibility And Responsive Checks
- Concrete check.

## Copy Improvements
- Exact replacement text if needed.
```

## 18. Codex recommendation analyzer

После получения Claude output Codex не должен слепо применять рекомендации. Нужен отдельный анализ:

```text
For each Claude recommendation:
1. Classify: accept | partially_accept | reject | needs_user_decision.
2. Reason: grounded in code, plan, or project constraints.
3. Action:
   - patch plan;
   - patch implementation;
   - add verification;
   - ask user;
   - record as residual risk.
4. Avoid applying recommendations that contradict user instructions or local AGENTS.md.
```

Для plan review Codex создаёт файл:

```text
<plan>.claude-suggestions.md
```

и затем обновляет исходный plan.

## 19. Plan refinement loop

```text
Draft plan
  -> Claude plan review
  -> Codex recommendation analysis
  -> Plan patch
  -> Optional second Claude review if verdict was NEEDS_REVISION
  -> Final plan ready for implementation
```

Stop conditions:

- Claude verdict is `APPROVE`;
- or Codex accepted all blockers and can explain residual risk;
- or recommendation requires user decision.

Maximum automatic review loops: 2.

## 20. Code review loop

```text
Implementation complete
  -> Claude code review
  -> Codex triage
  -> Fix accepted P0/P1/P2 findings
  -> Run verification
  -> Optional second Claude review on changed diff
  -> Final summary
```

Stop conditions:

- no accepted P0/P1/P2 findings remain;
- tests/verification pass;
- user decision needed.

## 21. CLI surface

Минимальная команда:

```bash
python3 .codex/claude-bridge/run-review.py \
  --type plan \
  --input docs/superpowers/plans/example-plan.md \
  --model sonnet \
  --timeout 300
```

Для реализации:

```bash
python3 .codex/claude-bridge/run-review.py \
  --type code \
  --base main \
  --include-diff \
  --include-tests \
  --model opus
```

Вывод runner:

```json
{
  "ok": true,
  "request_id": "plan-review-20260514-001",
  "session_closed": true,
  "inbox_path": ".codex/claude-bridge/inbox/plan-review-20260514-001.md",
  "outbox_path": ".codex/claude-bridge/outbox/plan-review-20260514-001.md",
  "metadata_path": ".codex/claude-bridge/outbox/plan-review-20260514-001.json"
}
```

## 22. Codex skill surface

Плагин должен дать Codex skills:

### `claude-plan-review`

Use when:

- Codex has written an implementation plan;
- user asks for Claude/Opus/Sonnet review;
- plan is high-risk or multi-step;
- Superpowers plan needs independent review before execution.

Behavior:

- build review-pack;
- run Claude Companion;
- read outbox;
- create suggestions file;
- patch plan;
- report final plan readiness.

### `claude-code-review`

Use when:

- implementation is complete;
- user asks for external review;
- diff touches risky surfaces;
- Codex wants second reviewer before final answer.

Behavior:

- collect diff and verification;
- run Claude Companion;
- triage findings;
- fix accepted issues;
- report residual risks.

## 23. Implementation plan

### Phase 1: Harden local prototype

Artifacts:

- `.codex/claude-bridge/hooks/capture-stop.py`
- `.codex/claude-bridge/claude-settings.json`
- `.codex/claude-bridge/run-review.py`

Acceptance:

- ordinary `claude` does not trigger hook;
- bridge-launched Claude saves outbox markdown;
- bridge tmux session closes after capture;
- invalid request id is ignored;
- missing inbox file is ignored.

### Phase 2: Review-pack builder

Artifacts:

- `build_review_pack.py`
- prompt templates
- redaction rules

Acceptance:

- plan review-pack includes plan, objective, acceptance checks and risks;
- code review-pack includes diff summary, changed files and verification output;
- secrets and ignored directories are excluded.

### Phase 3: Codex-side analyzer

Artifacts:

- `analyze_recommendations.py`
- suggestions file format
- plan patch workflow

Acceptance:

- Claude recommendations are classified;
- accepted plan suggestions are merged into the plan;
- rejected recommendations include rationale;
- user-decision items are surfaced.

### Phase 4: Plugin packaging

Artifacts:

- `plugins/claude-companion/.codex-plugin/plugin.json`
- skills
- scripts
- templates
- README

Acceptance:

- plugin installs without touching global Claude settings;
- scripts work from project root;
- docs explain billing/usage boundaries and safety model.

### Phase 5: Optional MCP wrapper

Artifacts:

- MCP tool `claude_plan_review`
- MCP tool `claude_code_review`

Acceptance:

- Codex can call review tools directly;
- tools return outbox paths and structured status;
- no mutation is performed by MCP tools.

## 24. Verification strategy

### Unit-level checks

- parse hook input JSON;
- sanitize request ids;
- detect review marker;
- ignore missing marker;
- ignore missing inbox;
- write markdown and metadata.

### Integration checks

- launch tmux session;
- send prompt;
- capture outbox file;
- close own session;
- keep unrelated tmux sessions alive.

### Manual checks

- run ordinary `claude` and verify no outbox file appears;
- run bridge review and verify outbox appears;
- interrupt Claude and verify timeout cleanup;
- run with malformed request id and verify no path traversal.

## 25. Failure modes

| Failure | Expected behavior |
| --- | --- |
| Claude does not start | runner returns structured error |
| Claude asks permission | runner times out and leaves diagnostic tail |
| Hook not loaded | runner times out and points to settings path |
| Hook writes invalid metadata | runner reports capture error |
| tmux session already exists | runner refuses unless request id matches |
| User manual session exists | runner does not touch it |
| Claude gives no marker | hook ignores response; runner times out |
| Output file already exists | runner refuses overwrite unless `--force` |

## 26. Open decisions

1. Default model: `sonnet` for routine reviews, `opus` for high-risk/adversarial reviews.
2. Whether to allow Claude read-only shell commands in review mode.
3. Whether to store transcript links in final Codex answers.
4. Whether plugin should live inside starter-kit or be a separate local plugin repo.
5. Whether second review loop should be automatic or user-approved.

## 27. Recommended MVP

The MVP should be:

- project-local only;
- no global Claude settings;
- `plan-review` mode first;
- read-only Claude;
- one tmux session per request;
- outbox markdown/json;
- Codex creates `<plan>.claude-suggestions.md`;
- Codex patches plan once;
- no automatic code edits based on Claude until user asks for implementation.

This gives the core value: Superpowers writes a plan, Claude critiques it, Codex improves it, then the final plan is ready for implementation.

## 28. Full mode catalog

The plugin should treat every Claude invocation as a named mode. A mode defines:

- when Codex may use it;
- what context builder must collect;
- which model is recommended;
- which prompt template is used;
- which output sections Claude must return;
- how Codex should consume the recommendations.

### 28.1. Planning modes

| Mode | Use when | Default model | Codex action after review |
| --- | --- | --- | --- |
| `superpowers-plan-review` | Superpowers produced an implementation plan | `sonnet` | patch plan and create suggestions file |
| `plan-red-team` | plan is complex, risky, or ambiguous | `opus` | add guardrails or ask user |
| `scope-trimmer` | plan may be too broad | `sonnet` | remove or defer non-essential work |
| `acceptance-checker` | plan lacks observable checks | `sonnet` | add acceptance checks |
| `risk-register` | plan touches risky surfaces | `sonnet` | add risk table and mitigations |
| `architecture-decision-review` | plan contains architecture choice | `opus` | update ADR/decision notes |

### 28.2. Implementation modes

| Mode | Use when | Default model | Codex action after review |
| --- | --- | --- | --- |
| `implementation-strategy` | before editing multi-file change | `sonnet` | reorder implementation steps |
| `diff-review` | implementation is complete | `sonnet` | fix accepted findings |
| `minimal-change-review` | task may have scope creep | `sonnet` | reduce diff or explain necessity |
| `legacy-safety-review` | old/high-blast-radius code is touched | `opus` | add characterization checks and sequencing |
| `api-contract-review` | public/API contracts are touched | `sonnet` | fix compatibility and response shape |
| `data-consistency-review` | writes, migrations, JSON/DB state are touched | `opus` | add consistency guardrails |

### 28.3. Quality modes

| Mode | Use when | Default model | Codex action after review |
| --- | --- | --- | --- |
| `test-gap-review` | verification is weak or risky | `sonnet` | add tests/checks |
| `failure-mode-review` | external systems or async paths are touched | `sonnet` | add error handling checks |
| `observability-review` | behavior may be hard to debug | `sonnet` | add logging/diagnostic notes |
| `performance-review` | runtime, DB, bundle, or loop cost matters | `opus` | add targeted performance fixes |
| `security-review` | auth, permissions, uploads, payments, secrets | `opus` | fix or gate security issues |
| `privacy-review` | user data, logs, transcripts, analytics | `opus` | add redaction and retention rules |

### 28.4. Frontend and product modes

| Mode | Use when | Default model | Codex action after review |
| --- | --- | --- | --- |
| `ux-flow-review` | user workflow changed | `sonnet` | adjust flow/states |
| `accessibility-review` | UI changed | `sonnet` | add a11y fixes/checks |
| `responsive-review` | responsive UI changed | `sonnet` | add viewport checks |
| `copy-review` | UI copy, errors, docs, messages changed | `sonnet` | patch text |
| `visual-regression-plan` | visual UI needs proof | `sonnet` | add screenshot plan |

### 28.5. Delivery modes

| Mode | Use when | Default model | Codex action after review |
| --- | --- | --- | --- |
| `release-readiness-review` | before final answer, deploy, merge, handoff | `sonnet` | run missing checks or report risk |
| `rollback-review` | deployment or migration risk exists | `opus` | add rollback plan |
| `incident-premortem` | high-risk release or unclear failure modes | `opus` | add safeguards |
| `handoff-summary-review` | final response must be accurate | `sonnet` | correct final summary |
| `documentation-review` | docs/readme/AGENTS/API changed | `sonnet` | update missing docs |

### 28.6. Meta modes

| Mode | Use when | Default model | Codex action after review |
| --- | --- | --- | --- |
| `second-opinion-opus` | high-risk decision needs strongest review | `opus` | compare and decide |
| `fast-sonnet-check` | cheap sanity check is enough | `sonnet` | apply obvious fixes |
| `multi-perspective-review` | one pass should cover multiple roles | `opus` | split findings by role |
| `contradiction-finder` | specs, code, docs, prompts may conflict | `sonnet` | resolve contradictions |
| `user-intent-audit` | Codex may have drifted from request | `sonnet` | realign plan/diff |
| `prompt-quality-review` | prompt/plan will be sent to another agent | `sonnet` | make prompt executable |

## 29. Auto-fill data contract

Every mode receives the same canonical context object. Mode-specific prompts may ignore unused fields, but the runner should keep field names stable.

### 29.1. Canonical fields

```yaml
request:
  request_id: string
  review_type: string
  created_at: iso8601
  user_request: string
  codex_current_goal: string
  urgency: normal | high
  risk_flags: string[]

project:
  root: string
  name: string
  branch: string
  git_status_short: string
  agent_instructions: string
  relevant_docs: string
  package_profile: string
  runtime_profile: string

plan:
  plan_path: string
  plan_text: string
  suggestions_path: string
  acceptance_checks: string
  task_ledger: string

implementation:
  changed_files: string
  diff_stat: string
  diff_patch: string
  touched_symbols: string
  verification_run: string
  verification_output: string
  known_failures: string

contracts:
  api_routes: string
  schemas: string
  database_changes: string
  migrations: string
  external_integrations: string

frontend:
  affected_screens: string
  states: string
  viewport_targets: string
  screenshots: string
  copy_changes: string

delivery:
  deploy_target: string
  rollback_plan: string
  observability_notes: string
  release_notes: string

constraints:
  do_not_touch: string
  secrets_policy: string
  sandbox_policy: string
  user_confirmations_required: string
```

### 29.2. Placeholder syntax

Templates use double braces:

```text
{{REQUEST_ID}}
{{REVIEW_TYPE}}
{{USER_REQUEST}}
{{PROJECT_ROOT}}
{{AGENT_INSTRUCTIONS}}
{{PLAN_TEXT}}
{{DIFF_PATCH}}
{{VERIFICATION_OUTPUT}}
```

Renderer rules:

- missing optional values become `Not provided`;
- missing required values fail before Claude launch;
- secrets are redacted before rendering;
- large fields are summarized before rendering if they exceed mode budget;
- full file contents are included only when required by the mode.

### 29.3. Required fields by mode

| Mode | Required auto-filled fields |
| --- | --- |
| `superpowers-plan-review` | `user_request`, `agent_instructions`, `plan_path`, `plan_text`, `acceptance_checks` |
| `plan-red-team` | `user_request`, `plan_text`, `risk_flags`, `relevant_docs` |
| `scope-trimmer` | `user_request`, `plan_text`, `codex_current_goal` |
| `acceptance-checker` | `user_request`, `plan_text`, `acceptance_checks` |
| `risk-register` | `plan_text`, `risk_flags`, `contracts`, `delivery` |
| `architecture-decision-review` | `plan_text`, `relevant_docs`, `contracts`, `external_integrations` |
| `implementation-strategy` | `user_request`, `plan_text`, `changed_files`, `agent_instructions` |
| `diff-review` | `user_request`, `diff_stat`, `diff_patch`, `verification_output` |
| `minimal-change-review` | `user_request`, `diff_stat`, `diff_patch`, `plan_text` |
| `legacy-safety-review` | `agent_instructions`, `changed_files`, `diff_patch`, `known_failures` |
| `api-contract-review` | `api_routes`, `schemas`, `diff_patch`, `verification_output` |
| `data-consistency-review` | `database_changes`, `migrations`, `diff_patch`, `known_failures` |
| `test-gap-review` | `plan_text`, `diff_patch`, `verification_run`, `verification_output` |
| `failure-mode-review` | `external_integrations`, `diff_patch`, `known_failures` |
| `observability-review` | `diff_patch`, `observability_notes`, `known_failures` |
| `performance-review` | `runtime_profile`, `diff_patch`, `verification_output` |
| `security-review` | `agent_instructions`, `diff_patch`, `contracts`, `risk_flags` |
| `privacy-review` | `diff_patch`, `observability_notes`, `external_integrations` |
| `ux-flow-review` | `affected_screens`, `states`, `diff_patch`, `user_request` |
| `accessibility-review` | `affected_screens`, `states`, `diff_patch` |
| `responsive-review` | `affected_screens`, `viewport_targets`, `screenshots`, `diff_patch` |
| `copy-review` | `copy_changes`, `affected_screens`, `user_request` |
| `visual-regression-plan` | `affected_screens`, `viewport_targets`, `diff_patch` |
| `release-readiness-review` | `user_request`, `diff_patch`, `verification_output`, `known_failures` |
| `rollback-review` | `delivery`, `database_changes`, `migrations`, `diff_patch` |
| `incident-premortem` | `plan_text`, `diff_patch`, `risk_flags`, `delivery` |
| `handoff-summary-review` | `user_request`, `diff_stat`, `verification_output`, `known_failures` |
| `documentation-review` | `relevant_docs`, `diff_patch`, `user_request` |
| `second-opinion-opus` | `user_request`, `plan_text`, `diff_patch`, `risk_flags` |
| `fast-sonnet-check` | `user_request`, `plan_text`, `diff_patch` |
| `multi-perspective-review` | `user_request`, `plan_text`, `diff_patch`, `risk_flags` |
| `contradiction-finder` | `user_request`, `agent_instructions`, `plan_text`, `relevant_docs`, `diff_patch` |
| `user-intent-audit` | `user_request`, `plan_text`, `diff_patch`, `codex_current_goal` |
| `prompt-quality-review` | `user_request`, `plan_text`, `codex_current_goal` |

## 30. Prompt template rules

Every prompt must include:

```md
CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}
```

as the first line of the expected response.

Every prompt must also say:

- do not edit files;
- do not run commands;
- do not reveal secrets;
- ground findings in provided context;
- prefer concrete patches/checks over general advice;
- separate blockers from optional improvements.

Claude output is advisory. Codex decides what to accept.

## 31. Full prompt library

The templates in this section are implementation-ready. The runner fills placeholders from the canonical context object before sending the prompt to Claude.

### 31.1. `superpowers-plan-review`

Auto-fill: `{{USER_REQUEST}}`, `{{AGENT_INSTRUCTIONS}}`, `{{PLAN_PATH}}`, `{{PLAN_TEXT}}`, `{{ACCEPTANCE_CHECKS}}`.

```md
You are Claude acting as an independent senior reviewer for a Superpowers-style Codex implementation plan.

Do not edit files. Do not run commands. Review only the supplied plan and context.

User request:
{{USER_REQUEST}}

Project instructions:
{{AGENT_INSTRUCTIONS}}

Plan path:
{{PLAN_PATH}}

Plan:
{{PLAN_TEXT}}

Acceptance checks already present:
{{ACCEPTANCE_CHECKS}}

Review the plan using these lenses:
- Is each step executable by a coding agent without hidden context?
- Does each step produce an observable truth?
- Are discovery, implementation, verification, and user confirmation ordered correctly?
- Are risky operations gated?
- Does the plan avoid drive-by refactors?
- Does the plan preserve user work?
- Are acceptance checks narrow enough to run and strong enough to prove the result?

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Superpowers Plan Review

## Verdict
APPROVE | APPROVE_WITH_CHANGES | NEEDS_REVISION

## Blocking Plan Issues
- Issue, why it blocks execution, exact plan patch.

## Suggested Improvements
- Improvement, where to place it, why it helps.

## Missing Acceptance Checks
- Check, command/manual action, expected result.

## Suggested Plan Patch
Patch-style markdown Codex can merge into the plan.

## Residual Risk
What remains risky even after patching.
```

### 31.2. `plan-red-team`

Auto-fill: `{{USER_REQUEST}}`, `{{PLAN_TEXT}}`, `{{RISK_FLAGS}}`, `{{RELEVANT_DOCS}}`.

```md
You are Claude acting as a red-team reviewer for a Codex plan.

Do not edit files. Do not run commands. Attack the plan as if you are responsible for the postmortem if it fails.

User request:
{{USER_REQUEST}}

Risk flags:
{{RISK_FLAGS}}

Relevant docs:
{{RELEVANT_DOCS}}

Plan:
{{PLAN_TEXT}}

Find the strongest realistic objections. Avoid generic warnings.

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Plan Red-Team Review

## Verdict
PROCEED | PROCEED_WITH_GUARDS | REDESIGN

## Strongest Failure Scenarios
- Scenario, trigger, user/business impact, mitigation.

## Missing Guardrails
- Guardrail Codex should add before implementation.

## Simplification Opportunity
- Smaller path that preserves the user goal, or `None`.

## Decision Notes
Notes Codex should add to the plan or ADR.
```

### 31.3. `scope-trimmer`

Auto-fill: `{{USER_REQUEST}}`, `{{CODEX_CURRENT_GOAL}}`, `{{PLAN_TEXT}}`.

```md
You are Claude acting as a strict scope reviewer.

Do not edit files. Do not run commands. Your job is to protect the user request from scope creep.

Original user request:
{{USER_REQUEST}}

Codex current goal:
{{CODEX_CURRENT_GOAL}}

Plan:
{{PLAN_TEXT}}

Classify every questionable item as essential, defer, or remove. Prefer the smallest plan that satisfies the request.

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Scope Trim Review

## Verdict
TIGHT | TRIM_RECOMMENDED | OVER_SCOPED

## Essential Work
- Keep this because...

## Defer
- Defer this because...

## Remove
- Remove this because...

## Minimal Plan Patch
Patch-style markdown that narrows the plan.
```

### 31.4. `acceptance-checker`

Auto-fill: `{{USER_REQUEST}}`, `{{PLAN_TEXT}}`, `{{ACCEPTANCE_CHECKS}}`.

```md
You are Claude acting as an acceptance-check specialist.

Do not edit files. Do not run commands. Convert vague outcomes into observable checks.

User request:
{{USER_REQUEST}}

Plan:
{{PLAN_TEXT}}

Existing acceptance checks:
{{ACCEPTANCE_CHECKS}}

Review whether a separate agent could prove the work is done.

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Acceptance Check Review

## Verdict
CHECKS_READY | ADD_CHECKS | CHECKS_TOO_VAGUE

## Missing Observable Truths
- Outcome that must be true from the user's perspective.

## Required Checks
- Check, command or manual action, expected result.

## Plan Patch
Markdown bullets Codex should add under acceptance checks.
```

### 31.5. `risk-register`

Auto-fill: `{{PLAN_TEXT}}`, `{{RISK_FLAGS}}`, `{{CONTRACTS}}`, `{{DELIVERY}}`.

```md
You are Claude acting as a delivery risk analyst.

Do not edit files. Do not run commands. Build a practical risk register for the plan.

Plan:
{{PLAN_TEXT}}

Risk flags:
{{RISK_FLAGS}}

Contracts and data surfaces:
{{CONTRACTS}}

Delivery context:
{{DELIVERY}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Risk Register

## Verdict
LOW_RISK | MANAGEABLE_RISK | HIGH_RISK

## Risk Register
| Risk | Probability | Impact | Early Signal | Mitigation | Owner |
| --- | --- | --- | --- | --- | --- |

## Required Plan Additions
- Addition Codex should make.

## User Decisions Needed
- Decision, options, consequence. If none, write `None`.
```

### 31.6. `architecture-decision-review`

Auto-fill: `{{PLAN_TEXT}}`, `{{RELEVANT_DOCS}}`, `{{CONTRACTS}}`, `{{EXTERNAL_INTEGRATIONS}}`.

```md
You are Claude acting as an architecture decision reviewer.

Do not edit files. Do not run commands. Review the design decision, alternatives, and consequences.

Plan:
{{PLAN_TEXT}}

Relevant docs:
{{RELEVANT_DOCS}}

Contracts:
{{CONTRACTS}}

External integrations:
{{EXTERNAL_INTEGRATIONS}}

Use decision-review lenses: reversibility, coupling, state ownership, operational burden, migration path, rollback, and long-term maintainability.

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Architecture Decision Review

## Verdict
ACCEPT | ACCEPT_WITH_CONSTRAINTS | RECONSIDER

## Decision Quality
- What is clear and what is missing.

## Alternatives Not Considered
- Alternative, tradeoff, when it would be better.

## Consequences
- Positive and negative consequences Codex should document.

## ADR Patch
Markdown Codex can place in an ADR or plan decision section.
```

### 31.7. `implementation-strategy`

Auto-fill: `{{USER_REQUEST}}`, `{{PLAN_TEXT}}`, `{{CHANGED_FILES}}`, `{{AGENT_INSTRUCTIONS}}`.

```md
You are Claude acting as an implementation sequencing reviewer.

Do not edit files. Do not run commands. Recommend the safest order of work.

User request:
{{USER_REQUEST}}

Project instructions:
{{AGENT_INSTRUCTIONS}}

Plan:
{{PLAN_TEXT}}

Known files or likely files:
{{CHANGED_FILES}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Implementation Strategy

## Verdict
ORDER_OK | REORDER_RECOMMENDED | DISCOVERY_NEEDED

## Recommended Sequence
1. Step, files, completion signal.

## Discovery Before Edits
- Question or code area to inspect first.

## Risky Steps
- Step, risk, guardrail.

## Verification Placement
- Where to run each check.
```

### 31.8. `diff-review`

Auto-fill: `{{USER_REQUEST}}`, `{{DIFF_STAT}}`, `{{DIFF_PATCH}}`, `{{VERIFICATION_OUTPUT}}`.

```md
You are Claude acting as a senior code reviewer.

Do not edit files. Do not run commands. Review the completed diff for real bugs and regressions.

User request:
{{USER_REQUEST}}

Diff stat:
{{DIFF_STAT}}

Diff:
{{DIFF_PATCH}}

Verification output:
{{VERIFICATION_OUTPUT}}

Prioritize correctness, data safety, security, and missing tests. Do not nitpick style.

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Diff Review

## Verdict
APPROVE | APPROVE_WITH_FIXES | NEEDS_WORK

## Findings
- P0/P1/P2, file/section, issue, impact, concrete fix.

## Missing Tests
- Check that should be added or run.

## Regression Risks
- Existing workflow that may break.

## Fix Order
1. Highest-value fix first.
```

### 31.9. `minimal-change-review`

Auto-fill: `{{USER_REQUEST}}`, `{{PLAN_TEXT}}`, `{{DIFF_STAT}}`, `{{DIFF_PATCH}}`.

```md
You are Claude acting as a minimal-change reviewer.

Do not edit files. Do not run commands. Check whether the change exceeds the user's request.

User request:
{{USER_REQUEST}}

Plan:
{{PLAN_TEXT}}

Diff stat:
{{DIFF_STAT}}

Diff:
{{DIFF_PATCH}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Minimal Change Review

## Verdict
SCOPED | MINOR_SCOPE_RISK | OVERREACH

## Necessary Changes
- Change and why it directly serves the request.

## Questionable Changes
- Change, why it may be unnecessary, recommended action.

## Revert Or Keep
- File/section, recommendation, rationale.
```

### 31.10. `legacy-safety-review`

Auto-fill: `{{AGENT_INSTRUCTIONS}}`, `{{CHANGED_FILES}}`, `{{DIFF_PATCH}}`, `{{KNOWN_FAILURES}}`.

```md
You are Claude acting as a legacy-code safety reviewer.

Do not edit files. Do not run commands. Assume the code has hidden behavior and weak tests.

Project instructions:
{{AGENT_INSTRUCTIONS}}

Changed files:
{{CHANGED_FILES}}

Diff:
{{DIFF_PATCH}}

Known failures:
{{KNOWN_FAILURES}}

Use legacy-work lenses: characterization checks, blast radius, hidden dependencies, mutation safety, and rollback.

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Legacy Safety Review

## Verdict
SAFE_ENOUGH | ADD_CHARACTERIZATION | HIGH_BLAST_RADIUS

## Hidden Behavior Risks
- Risk, affected path, how to characterize it.

## Characterization Checks
- Check, expected current behavior, why it matters.

## Safer Change Shape
- Smaller or safer implementation shape.
```

### 31.11. `api-contract-review`

Auto-fill: `{{API_ROUTES}}`, `{{SCHEMAS}}`, `{{DIFF_PATCH}}`, `{{VERIFICATION_OUTPUT}}`.

```md
You are Claude acting as an API contract reviewer.

Do not edit files. Do not run commands. Review compatibility and contract correctness.

API routes:
{{API_ROUTES}}

Schemas:
{{SCHEMAS}}

Diff:
{{DIFF_PATCH}}

Verification:
{{VERIFICATION_OUTPUT}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude API Contract Review

## Verdict
COMPATIBLE | COMPATIBLE_WITH_FIXES | BREAKING_RISK

## Contract Findings
- Endpoint/schema, problem, client impact, fix.

## Backward Compatibility Checks
- Check and expected result.

## Error Response Review
- Missing or inconsistent error behavior.
```

### 31.12. `data-consistency-review`

Auto-fill: `{{DATABASE_CHANGES}}`, `{{MIGRATIONS}}`, `{{DIFF_PATCH}}`, `{{KNOWN_FAILURES}}`.

```md
You are Claude acting as a data consistency reviewer.

Do not edit files. Do not run commands. Focus on persistence correctness.

Database or state changes:
{{DATABASE_CHANGES}}

Migrations:
{{MIGRATIONS}}

Diff:
{{DIFF_PATCH}}

Known failures:
{{KNOWN_FAILURES}}

Review writes, transactions, locks, IDs, timestamps, migrations, rollback, duplicate handling, and partial failure.

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Data Consistency Review

## Verdict
CONSISTENT | NEEDS_GUARDS | DATA_RISK

## Consistency Findings
- Surface, issue, data impact, mitigation.

## Migration/Rollback Notes
- Required step or warning.

## Verification Checks
- Check, fixture/data setup, expected result.
```

### 31.13. `test-gap-review`

Auto-fill: `{{PLAN_TEXT}}`, `{{DIFF_PATCH}}`, `{{VERIFICATION_RUN}}`, `{{VERIFICATION_OUTPUT}}`.

```md
You are Claude acting as a test gap reviewer.

Do not edit files. Do not run commands. Make verification proportional to risk.

Plan:
{{PLAN_TEXT}}

Diff:
{{DIFF_PATCH}}

Verification run:
{{VERIFICATION_RUN}}

Verification output:
{{VERIFICATION_OUTPUT}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Test Gap Review

## Verdict
ENOUGH | ADD_NARROW_CHECKS | ADD_BROAD_CHECKS

## Missing Checks
- Check, why it matters, expected result.

## Over-Testing To Avoid
- Check that is unnecessary for this scope.

## Verification Patch
Markdown Codex can add to plan or final checklist.
```

### 31.14. `failure-mode-review`

Auto-fill: `{{EXTERNAL_INTEGRATIONS}}`, `{{DIFF_PATCH}}`, `{{KNOWN_FAILURES}}`.

```md
You are Claude acting as a failure-mode reviewer.

Do not edit files. Do not run commands. Focus on error paths and degraded behavior.

External integrations:
{{EXTERNAL_INTEGRATIONS}}

Diff:
{{DIFF_PATCH}}

Known failures:
{{KNOWN_FAILURES}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Failure Mode Review

## Verdict
ROBUST | NEEDS_ERROR_HANDLING | FRAGILE

## Failure Scenarios
- Trigger, observed/likely behavior, user impact, fix.

## Recovery And Retry
- Missing retry, timeout, fallback, or cleanup behavior.

## Verification
- How Codex should simulate or verify the failure.
```

### 31.15. `observability-review`

Auto-fill: `{{DIFF_PATCH}}`, `{{OBSERVABILITY_NOTES}}`, `{{KNOWN_FAILURES}}`.

```md
You are Claude acting as an observability reviewer.

Do not edit files. Do not run commands. Focus on whether future debugging will be possible.

Diff:
{{DIFF_PATCH}}

Existing observability notes:
{{OBSERVABILITY_NOTES}}

Known failures:
{{KNOWN_FAILURES}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Observability Review

## Verdict
DEBUGGABLE | ADD_SIGNALS | BLIND_SPOTS

## Missing Signals
- Event/log/metric, where it belongs, why it helps.

## Noise To Avoid
- Log or metric that would be misleading or too noisy.

## Diagnostic Checklist
- Commands or places to inspect after release.
```

### 31.16. `performance-review`

Auto-fill: `{{RUNTIME_PROFILE}}`, `{{DIFF_PATCH}}`, `{{VERIFICATION_OUTPUT}}`.

```md
You are Claude acting as a performance reviewer.

Do not edit files. Do not run commands. Look for realistic performance risks, not theoretical micro-optimizations.

Runtime profile:
{{RUNTIME_PROFILE}}

Diff:
{{DIFF_PATCH}}

Verification output:
{{VERIFICATION_OUTPUT}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Performance Review

## Verdict
OK | WATCH | PERFORMANCE_RISK

## Performance Findings
- Hot path, issue, expected impact, fix.

## Measurement Needed
- What to measure and acceptable threshold.

## Avoid Premature Optimization
- Work that should not be done now.
```

### 31.17. `security-review`

Auto-fill: `{{AGENT_INSTRUCTIONS}}`, `{{DIFF_PATCH}}`, `{{CONTRACTS}}`, `{{RISK_FLAGS}}`.

```md
You are Claude acting as an application security reviewer.

Do not edit files. Do not run commands. Focus on realistic exploit paths.

Project instructions:
{{AGENT_INSTRUCTIONS}}

Risk flags:
{{RISK_FLAGS}}

Contracts:
{{CONTRACTS}}

Diff:
{{DIFF_PATCH}}

Review trust boundaries, auth, permissions, validation, secrets, injection, SSRF, file paths, dependency assumptions, and auditability.

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Security Review

## Verdict
LOW_RISK | NEEDS_GUARDS | HIGH_RISK

## Threat Findings
- Severity, attack path, asset, fix.

## Required Guards
- Guardrail Codex should implement or verify.

## Security Verification
- Check and expected result.
```

### 31.18. `privacy-review`

Auto-fill: `{{DIFF_PATCH}}`, `{{OBSERVABILITY_NOTES}}`, `{{EXTERNAL_INTEGRATIONS}}`.

```md
You are Claude acting as a privacy and data-retention reviewer.

Do not edit files. Do not run commands. Focus on user data exposure and retention.

Diff:
{{DIFF_PATCH}}

Observability notes:
{{OBSERVABILITY_NOTES}}

External integrations:
{{EXTERNAL_INTEGRATIONS}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Privacy Review

## Verdict
OK | NEEDS_REDACTION | PRIVACY_RISK

## Data Exposure Findings
- Data type, exposure path, user impact, mitigation.

## Retention And Deletion
- Missing retention, deletion, or minimization rule.

## Logging/Transcript Safety
- What must be redacted or avoided.
```

### 31.19. `ux-flow-review`

Auto-fill: `{{USER_REQUEST}}`, `{{AFFECTED_SCREENS}}`, `{{STATES}}`, `{{DIFF_PATCH}}`.

```md
You are Claude acting as a UX flow reviewer for a working product.

Do not edit files. Do not run commands. Focus on task completion and user-visible states.

User request:
{{USER_REQUEST}}

Affected screens:
{{AFFECTED_SCREENS}}

States:
{{STATES}}

Diff:
{{DIFF_PATCH}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude UX Flow Review

## Verdict
READY | NEEDS_UX_FIXES | FLOW_RISK

## Workflow Findings
- Screen/state, user problem, fix.

## Missing States
- Empty/loading/error/success state that should exist.

## Manual UX Checks
- Check and expected result.
```

### 31.20. `accessibility-review`

Auto-fill: `{{AFFECTED_SCREENS}}`, `{{STATES}}`, `{{DIFF_PATCH}}`.

```md
You are Claude acting as an accessibility reviewer.

Do not edit files. Do not run commands. Focus on practical WCAG-style barriers.

Affected screens:
{{AFFECTED_SCREENS}}

States:
{{STATES}}

Diff:
{{DIFF_PATCH}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Accessibility Review

## Verdict
PASS_LIKELY | NEEDS_A11Y_CHECKS | ACCESSIBILITY_RISK

## Barriers
- Element/state, barrier, affected user, fix.

## Required Checks
- Keyboard, focus, label, contrast, or screen-reader check.

## Acceptance Patch
- Accessibility acceptance checks Codex should add.
```

### 31.21. `responsive-review`

Auto-fill: `{{AFFECTED_SCREENS}}`, `{{VIEWPORT_TARGETS}}`, `{{SCREENSHOTS}}`, `{{DIFF_PATCH}}`.

```md
You are Claude acting as a responsive UI reviewer.

Do not edit files. Do not run commands. Focus on text fit, overflow, layout stability, and viewport behavior.

Affected screens:
{{AFFECTED_SCREENS}}

Viewport targets:
{{VIEWPORT_TARGETS}}

Screenshots or notes:
{{SCREENSHOTS}}

Diff:
{{DIFF_PATCH}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Responsive Review

## Verdict
LIKELY_OK | NEEDS_VIEWPORT_CHECKS | RESPONSIVE_RISK

## Layout Risks
- Viewport/state, risk, fix.

## Required Screenshots
- Viewport and state to capture.

## Text Fit Checks
- Element and expected behavior.
```

### 31.22. `copy-review`

Auto-fill: `{{COPY_CHANGES}}`, `{{AFFECTED_SCREENS}}`, `{{USER_REQUEST}}`.

```md
You are Claude acting as a product copy reviewer.

Do not edit files. Do not run commands. Improve clarity, accuracy, and tone. Avoid marketing fluff unless the surface is marketing.

User request:
{{USER_REQUEST}}

Affected screens:
{{AFFECTED_SCREENS}}

Copy changes:
{{COPY_CHANGES}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Copy Review

## Verdict
COPY_OK | COPY_FIXES | COPY_RISK

## Copy Findings
- Location, issue, replacement text.

## Error/Empty State Text
- Suggested exact text.

## Consistency Notes
- Terms or labels to align.
```

### 31.23. `visual-regression-plan`

Auto-fill: `{{AFFECTED_SCREENS}}`, `{{VIEWPORT_TARGETS}}`, `{{DIFF_PATCH}}`.

```md
You are Claude acting as a visual QA planner.

Do not edit files. Do not run commands. Create the smallest useful screenshot plan.

Affected screens:
{{AFFECTED_SCREENS}}

Viewport targets:
{{VIEWPORT_TARGETS}}

Diff:
{{DIFF_PATCH}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Visual Regression Plan

## Verdict
LIGHT_CHECK | STANDARD_SCREENSHOTS | BROAD_VISUAL_QA

## Screenshot Matrix
| Screen | State | Viewport | Why |
| --- | --- | --- | --- |

## Pixel/Interaction Checks
- Check and expected result.

## Out Of Scope
- Visual checks not needed for this change.
```

### 31.24. `release-readiness-review`

Auto-fill: `{{USER_REQUEST}}`, `{{DIFF_PATCH}}`, `{{VERIFICATION_OUTPUT}}`, `{{KNOWN_FAILURES}}`.

```md
You are Claude acting as a release-readiness reviewer.

Do not edit files. Do not run commands. Decide whether Codex can present the work as complete.

User request:
{{USER_REQUEST}}

Diff:
{{DIFF_PATCH}}

Verification output:
{{VERIFICATION_OUTPUT}}

Known failures:
{{KNOWN_FAILURES}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Release Readiness Review

## Verdict
READY | READY_WITH_RISK | NOT_READY

## Blocking Gaps
- Gap, why it blocks, required action.

## Residual Risks
- Risk Codex should mention in final answer.

## Final Answer Notes
- What Codex should include or avoid saying.
```

### 31.25. `rollback-review`

Auto-fill: `{{DELIVERY}}`, `{{DATABASE_CHANGES}}`, `{{MIGRATIONS}}`, `{{DIFF_PATCH}}`.

```md
You are Claude acting as a rollback reviewer.

Do not edit files. Do not run commands. Check whether the change can be safely undone.

Delivery context:
{{DELIVERY}}

Database changes:
{{DATABASE_CHANGES}}

Migrations:
{{MIGRATIONS}}

Diff:
{{DIFF_PATCH}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Rollback Review

## Verdict
ROLLBACK_READY | NEEDS_ROLLBACK_PLAN | HARD_TO_ROLLBACK

## Rollback Steps
1. Step, owner, expected result.

## Irreversible Changes
- Change, consequence, mitigation.

## Pre-Deploy Backup Checks
- Backup/check required before release.
```

### 31.26. `incident-premortem`

Auto-fill: `{{PLAN_TEXT}}`, `{{DIFF_PATCH}}`, `{{RISK_FLAGS}}`, `{{DELIVERY}}`.

```md
You are Claude acting as an incident premortem facilitator.

Do not edit files. Do not run commands. Imagine this change caused an incident after release. Identify plausible causes and prevention.

Plan:
{{PLAN_TEXT}}

Diff:
{{DIFF_PATCH}}

Risk flags:
{{RISK_FLAGS}}

Delivery:
{{DELIVERY}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Incident Premortem

## Verdict
LOW_INCIDENT_RISK | ADD_GUARDS | HIGH_INCIDENT_RISK

## Plausible Incident Stories
- Story, trigger, detection signal, prevention.

## Pre-Release Safeguards
- Guardrail to add before release.

## Monitoring After Release
- What to watch first.
```

### 31.27. `handoff-summary-review`

Auto-fill: `{{USER_REQUEST}}`, `{{DIFF_STAT}}`, `{{VERIFICATION_OUTPUT}}`, `{{KNOWN_FAILURES}}`.

```md
You are Claude acting as a final handoff reviewer.

Do not edit files. Do not run commands. Check whether Codex's final summary would be truthful and complete.

User request:
{{USER_REQUEST}}

Diff stat:
{{DIFF_STAT}}

Verification:
{{VERIFICATION_OUTPUT}}

Known failures:
{{KNOWN_FAILURES}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Handoff Summary Review

## Verdict
SUMMARY_READY | ADD_CONTEXT | DO_NOT_CLAIM_DONE

## Must Mention
- Fact Codex should include.

## Must Not Claim
- Claim that would be unsupported.

## Suggested Final Summary
Short final-answer draft.
```

### 31.28. `documentation-review`

Auto-fill: `{{USER_REQUEST}}`, `{{RELEVANT_DOCS}}`, `{{DIFF_PATCH}}`.

```md
You are Claude acting as a documentation reviewer.

Do not edit files. Do not run commands. Check whether docs need to change with the work.

User request:
{{USER_REQUEST}}

Relevant docs:
{{RELEVANT_DOCS}}

Diff:
{{DIFF_PATCH}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Documentation Review

## Verdict
DOCS_OK | DOCS_SHOULD_CHANGE | DOCS_BLOCKING

## Missing Documentation
- File/section, missing detail, suggested text.

## Stale Documentation
- Existing doc that may become inaccurate.

## No-Docs Rationale
If docs do not need changes, explain why.
```

### 31.29. `second-opinion-opus`

Auto-fill: `{{USER_REQUEST}}`, `{{PLAN_TEXT}}`, `{{DIFF_PATCH}}`, `{{RISK_FLAGS}}`.

```md
You are Claude Opus acting as a high-stakes second opinion reviewer.

Do not edit files. Do not run commands. Spend your attention on the few issues that matter most.

User request:
{{USER_REQUEST}}

Risk flags:
{{RISK_FLAGS}}

Plan:
{{PLAN_TEXT}}

Diff:
{{DIFF_PATCH}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Opus Second Opinion

## Verdict
CONFIDENT | CONCERNS | STOP_AND_RETHINK

## Top Concerns
- Concern, evidence, recommended action.

## Best Next Move
One concise recommendation for Codex.

## What Not To Overthink
- Area that is acceptable as-is.
```

### 31.30. `fast-sonnet-check`

Auto-fill: `{{USER_REQUEST}}`, `{{PLAN_TEXT}}`, `{{DIFF_PATCH}}`.

```md
You are Claude Sonnet acting as a fast sanity checker.

Do not edit files. Do not run commands. Return only high-signal issues.

User request:
{{USER_REQUEST}}

Plan:
{{PLAN_TEXT}}

Diff:
{{DIFF_PATCH}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Fast Check

## Verdict
OK | FIX_SMALL_ISSUES | NEEDS_ATTENTION

## High-Signal Issues
- Issue, fix.

## Quick Win
- One small improvement if any, otherwise `None`.
```

### 31.31. `multi-perspective-review`

Auto-fill: `{{USER_REQUEST}}`, `{{PLAN_TEXT}}`, `{{DIFF_PATCH}}`, `{{RISK_FLAGS}}`.

```md
You are Claude acting as a panel of reviewers. Keep roles separate and avoid duplicate findings.

Do not edit files. Do not run commands.

User request:
{{USER_REQUEST}}

Risk flags:
{{RISK_FLAGS}}

Plan:
{{PLAN_TEXT}}

Diff:
{{DIFF_PATCH}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Multi-Perspective Review

## Verdict
APPROVE | APPROVE_WITH_FIXES | NEEDS_WORK

## Architect View
- Finding or `No major concern`.

## Security View
- Finding or `No major concern`.

## QA View
- Finding or `No major concern`.

## Product/UX View
- Finding or `No major concern`.

## Prioritized Actions
1. Most important action.
```

### 31.32. `contradiction-finder`

Auto-fill: `{{USER_REQUEST}}`, `{{AGENT_INSTRUCTIONS}}`, `{{PLAN_TEXT}}`, `{{RELEVANT_DOCS}}`, `{{DIFF_PATCH}}`.

```md
You are Claude acting as a contradiction finder.

Do not edit files. Do not run commands. Compare instructions, plan, docs, and diff for conflicts.

User request:
{{USER_REQUEST}}

Agent instructions:
{{AGENT_INSTRUCTIONS}}

Relevant docs:
{{RELEVANT_DOCS}}

Plan:
{{PLAN_TEXT}}

Diff:
{{DIFF_PATCH}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Contradiction Review

## Verdict
CONSISTENT | MINOR_CONFLICTS | CONTRADICTIONS

## Contradictions
- Source A vs Source B, conflict, recommended resolution.

## Ambiguities
- Ambiguity, why it matters, default assumption.

## Patch Recommendations
- Plan/doc/code note Codex should update.
```

### 31.33. `user-intent-audit`

Auto-fill: `{{USER_REQUEST}}`, `{{CODEX_CURRENT_GOAL}}`, `{{PLAN_TEXT}}`, `{{DIFF_PATCH}}`.

```md
You are Claude acting as a user-intent auditor.

Do not edit files. Do not run commands. Check whether Codex is still solving the user's actual request.

User request:
{{USER_REQUEST}}

Codex current goal:
{{CODEX_CURRENT_GOAL}}

Plan:
{{PLAN_TEXT}}

Diff:
{{DIFF_PATCH}}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude User Intent Audit

## Verdict
ALIGNED | PARTIAL_DRIFT | MISALIGNED

## Alignment
- What directly satisfies the request.

## Drift
- Work that does not clearly follow from the request.

## Realignment Patch
- Concrete plan/diff/final-answer adjustment.
```

### 31.34. `prompt-quality-review`

Auto-fill: `{{USER_REQUEST}}`, `{{CODEX_CURRENT_GOAL}}`, `{{PLAN_TEXT}}`.

```md
You are Claude acting as a prompt and instruction quality reviewer.

Do not edit files. Do not run commands. Review whether the supplied prompt/plan can be executed by another agent without confusion.

User request:
{{USER_REQUEST}}

Codex current goal:
{{CODEX_CURRENT_GOAL}}

Prompt or plan:
{{PLAN_TEXT}}

Review for specificity, missing inputs, unclear success criteria, conflicting constraints, and over-broad delegation.

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {{REQUEST_ID}}

# Claude Prompt Quality Review

## Verdict
READY | NEEDS_CLARITY | NOT_EXECUTABLE

## Ambiguous Instructions
- Instruction, possible interpretations, preferred rewrite.

## Missing Inputs
- Input the receiving agent would need.

## Improved Prompt Patch
Concrete replacement text.
```

## 32. Mode selection policy

Codex should not run every mode by default. The mode selector should choose the smallest useful review set.

Recommended defaults:

- small direct fix: no Claude review or `fast-sonnet-check`;
- Superpowers plan: `superpowers-plan-review`;
- high-risk plan: `superpowers-plan-review` + `plan-red-team` or `second-opinion-opus`;
- completed implementation: `diff-review` + `test-gap-review`;
- auth/payments/permissions/secrets/uploads: add `security-review`;
- DB/migrations/state writes: add `data-consistency-review` + `rollback-review`;
- UI work: add `ux-flow-review`, `accessibility-review`, `responsive-review`;
- pre-release/deploy: add `release-readiness-review`;
- confusing context: add `contradiction-finder` or `user-intent-audit`.

Hard limits:

- maximum automatic Claude review modes per user request: 3;
- maximum automatic review loops: 2;
- `opus` modes require explicit high-risk reason in metadata;
- user can always request a specific mode by name.

## 33. Suggestions file format

For plan refinement, Codex writes a sibling file:

```text
<plan>.claude-suggestions.md
```

Format:

```md
# Claude Suggestions For <plan>

Request ID: <request_id>
Modes run: superpowers-plan-review, plan-red-team
Created at: <iso8601>

## Accepted
- Recommendation, source mode, applied patch location.

## Partially Accepted
- Recommendation, accepted part, rejected part, reason.

## Rejected
- Recommendation, reason grounded in user request or repo constraints.

## Needs User Decision
- Question, options, tradeoff.

## Plan Patch Summary
- Section changed and why.

## Source Files
- `.codex/claude-bridge/outbox/<request_id>.md`
```

Codex then patches the original plan and includes a short note:

```md
## Claude Review Integration

Reviewed with Claude Companion modes: ...
Accepted changes: ...
Residual risks: ...
```

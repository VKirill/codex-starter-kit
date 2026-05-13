# One-Prompt Codex Bootstrap

Paste this into Codex on a fresh machine to let Codex install this starter kit as the machine's Codex baseline.

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
- сохранить старые файлы через timestamped .bak-* backups

Работай пошагово:
1. Если репозитория еще нет, клонируй его в ~/projects/codex-starter-kit.
2. Если репозиторий уже есть, перейди в него и проверь текущее состояние git.
3. Прочитай README.md, install.py и templates/config.recommended.toml.
4. Запусти проверку пакета:
   python3 scripts/validate-pack.py
5. Запусти dry run:
   ./install.sh --dry-run
6. Покажи мне, какие пути будут заменены, и отдельно посчитай агентов и skills.
7. Если dry run выглядит безопасно, запусти установку с backup-режимом:
   ./install.sh
8. Проверь, что ~/.codex/config.toml содержит GitHub и Superpowers plugins, а также MCP servers context7, vue-docs, nuxt-ui-remote и nuxt-remote.
9. Если команда codex доступна, запусти:
   codex plugin marketplace upgrade
   codex mcp list
10. Проверь установленных агентов:
   ./install.sh --validate-only
11. В конце кратко напиши, что изменилось, где лежат backups и что нужно перезапустить Codex.

Правила безопасности:
- не удаляй ~/.codex, ~/.agents или существующие agents/skills без backup
- не используй --force и --no-backup без моего явного разрешения
- не копируй secrets, bearer tokens, приватные MCP настройки и локальные database credentials
- если команда требует повышенного доступа или сетевого разрешения, сначала объясни зачем
- если проверка падает, остановись, покажи ошибку и предложи самый маленький безопасный fix
```

---
name: vibe-code-auditor
description: Методология аудита кодовой базы по 7 измерениям. Паттерны обнаружения, scoring, поведенческие правила.
tags: [audit, review, code-quality, refactor]
stacks: [refactor]
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


# Vibe Code Auditor — Методология анализа

## Правила поведения

- Каждая находка должна быть обоснована реальным кодом. Не выдумывай проблемы.
- Указывай точное расположение (файл, функция, строка).
- НЕ предлагай стилевые правки (отступы, именование) если они не создают багов.
- НЕ рекомендуй архитектурные переписывания без веской причины.
- Группируй одинаковые проблемы (3 места с hardcoded credentials = 1 находка).
- Сначала критичное (security, data loss, crashes), потом остальное.

## Pattern Recognition — быстрые эвристики

| Паттерн | Вероятная проблема | Как проверить |
|---------|-------------------|---------------|
| `eval()`, `exec()`, `os.system()` | Security critical | Поиск строк |
| `except:` или `except Exception:` | Silent failures | Grep bare excepts |
| `password`, `secret`, `key`, `token` в коде | Hardcoded credentials | Поиск + проверка literal string |
| `if DEBUG`, `debug=True` | Insecure defaults | Проверка конфигов |
| Функции >50 строк | Maintainability risk | Подсчёт строк |
| Вложенность `if` >3 уровня | Complexity hotspot | Визуальный скан |
| Нет тестов в репозитории | Quality gap | Поиск `test_` файлов |
| Прямая конкатенация SQL | SQL injection | Поиск `f"SELECT` или `+ "SELECT` |
| `requests.get` без timeout | Production risk | Проверка HTTP-клиентов |
| `while True` без break | Unbounded loop | Поиск бесконечных циклов |

## 7 измерений анализа

### 1. Architecture & Design
- Можно ли найти entry point за 10 секунд?
- Есть ли чёткие границы между слоями (API, бизнес-логика, данные)?
- Есть ли файлы >300 строк?
- Нарушения separation of concerns (бизнес-логика в route handlers)
- God-объекты, монолитные модули
- Tight coupling без абстракций
- Циклические зависимости

### 2. Consistency & Maintainability
- Одинаковые операции названы единообразно?
- Copy-paste логика (3+ повторений = extract)
- Магические числа/строки без констант
- Смешение парадигм без обоснования
- Непоследовательная обработка ошибок

### 3. Robustness & Error Handling
- Каждый внешний вызов (API, DB, файл) имеет обработку ошибок?
- Есть ли bare `except:` блоки?
- Что происходит при пустых/null/malformed входных данных?
- Missing input validation на entry points
- Нет retry для transient failures
- Missing timeouts на блокирующих операциях

### 4. Production Risks
- Hardcoded URLs, IP, пути
- Отсутствие логирования
- Database queries в циклах (N+1)
- Blocking I/O в async контексте
- Нет graceful shutdown
- Нет health checks
- Нет rate limiting

### 5. Security & Safety
- `eval`, `exec`, `os.system`, `subprocess` без санитизации
- Credentials в source code или логах
- Insecure defaults (`DEBUG=True`, permissive CORS)
- SQL injection через string concatenation
- Path traversal через user input
- Missing auth/authz на чувствительных операциях

### 6. Dead / Hallucinated Code
- Определённые но никогда не вызываемые функции/классы
- Импорты несуществующих зависимостей
- Ссылки на несуществующие API/методы библиотек
- Комментарии противоречащие коду
- Unreachable code blocks
- Feature flags всегда true/false

### 7. Technical Debt Hotspots
- Логика которая сломается при росте нагрузки
- Глубокая вложенность (>3-4 уровня)
- Boolean параметры меняющие поведение функции
- Функции с >5-6 параметрами
- Нет тестов для критических путей

## Scoring (для приоритизации)

```
Старт: 100 баллов
Каждый CRITICAL: -15 (security: -20)
Каждый HIGH: -8
Каждый MEDIUM: -3
Массовый паттерн (3+ похожих): -5 дополнительно
Диапазон: 0-100
```

| Диапазон | Значение |
|----------|----------|
| 0-30 | Не деплоить. Критические отказы при нормальном использовании |
| 31-50 | Высокий риск. Требуется серьёзная доработка |
| 51-70 | Деплой только для внутреннего использования с мониторингом |
| 71-85 | Можно в прод с точечными исправлениями |
| 86-100 | Production-ready. Только мелкие улучшения |

#!/usr/bin/env python3
"""Codex UserPromptSubmit hook for handoff intake classification.

The hook is deliberately fail-open: when parsing, network, model access, or
credentials fail, Codex continues without blocking the user's prompt.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any
from urllib import request, error


ENV_PATH = Path.home() / ".codex" / "private" / "handoff-classifier.env"
PRIVATE_STATE_PATH = Path.home() / ".codex" / "private" / "handoff-classifier-state.json"
MEMORY_STATE_PATH = Path.home() / ".codex" / "memories" / "handoff-classifier-state.json"
API_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-5.4-nano"
MAX_PROMPT_CHARS = 1800
MAX_LOG_LINES = 12
MAX_BRIEF_CHARS = 1200
MAX_REPO_PROFILE_CHARS = 950
MAX_PREVIOUS_CONTEXT_CHARS = 1200
MAX_STATE_SESSIONS = 30


ARCHITECTURE_DEPENDENCIES: dict[str, tuple[str, str]] = {
    # Frameworks and app runtimes
    "next": ("framework", "Next.js"),
    "nuxt": ("framework", "Nuxt"),
    "vue": ("framework", "Vue"),
    "react": ("framework", "React"),
    "@angular/core": ("framework", "Angular"),
    "svelte": ("framework", "Svelte"),
    "@sveltejs/kit": ("framework", "SvelteKit"),
    "astro": ("framework", "Astro"),
    "remix": ("framework", "Remix"),
    "@remix-run/node": ("framework", "Remix"),
    "hono": ("backend", "Hono"),
    "fastify": ("backend", "Fastify"),
    "express": ("backend", "Express"),
    "@nestjs/core": ("backend", "NestJS"),
    "@hono/node-server": ("backend", "Hono Node server"),
    # Language and build tooling
    "typescript": ("language", "TypeScript"),
    "tsx": ("runtime", "tsx"),
    "vite": ("build", "Vite"),
    "webpack": ("build", "Webpack"),
    "rollup": ("build", "Rollup"),
    "esbuild": ("build", "esbuild"),
    "turbo": ("monorepo", "Turbo"),
    "lerna": ("monorepo", "Lerna"),
    "nx": ("monorepo", "Nx"),
    # Testing and quality
    "vitest": ("test", "Vitest"),
    "jest": ("test", "Jest"),
    "@playwright/test": ("e2e", "Playwright"),
    "playwright": ("e2e", "Playwright"),
    "cypress": ("e2e", "Cypress"),
    "eslint": ("quality", "ESLint"),
    "prettier": ("quality", "Prettier"),
    "knip": ("quality", "Knip"),
    # Data and backend infrastructure
    "prisma": ("orm", "Prisma"),
    "@prisma/client": ("orm", "Prisma Client"),
    "drizzle-orm": ("orm", "Drizzle ORM"),
    "sequelize": ("orm", "Sequelize"),
    "typeorm": ("orm", "TypeORM"),
    "pg": ("database", "PostgreSQL"),
    "mysql2": ("database", "MySQL"),
    "better-sqlite3": ("database", "SQLite"),
    "mongodb": ("database", "MongoDB"),
    "mongoose": ("database", "Mongoose"),
    "redis": ("cache", "Redis"),
    "ioredis": ("cache", "ioredis"),
    "bullmq": ("queue", "BullMQ"),
    "zod": ("contracts", "Zod"),
    "valibot": ("contracts", "Valibot"),
    "graphql": ("api", "GraphQL"),
    "@trpc/server": ("api", "tRPC"),
    # UI and styling
    "tailwindcss": ("ui", "Tailwind CSS"),
    "@nuxt/ui": ("ui", "Nuxt UI"),
    "reka-ui": ("ui", "Reka UI"),
    "lucide-react": ("ui", "Lucide React"),
    "lucide-vue-next": ("ui", "Lucide Vue"),
    # Observability and jobs
    "@opentelemetry/sdk-node": ("observability", "OpenTelemetry SDK"),
    "@opentelemetry/auto-instrumentations-node": ("observability", "OpenTelemetry auto-instrumentation"),
    "pino": ("logging", "Pino"),
    "winston": ("logging", "Winston"),
}


ARCHITECTURE_KEYWORDS = (
    "архитектур",
    "правильн",
    "без легаси",
    "legacy",
    "временн",
    "костыл",
    "production",
    "production-grade",
    "root cause",
    "root-cause",
    "корнев",
    "bounded context",
    "контракт",
    "типиз",
    "рефактор",
    "clean code",
    "ddd",
    "solid",
)


FOLLOW_UP_KEYWORDS = (
    "доработай",
    "доработать",
    "доделай",
    "доделать",
    "продолжай",
    "продолжить",
    "дальше",
    "ещё",
    "еще",
    "тогда",
    "сделай так",
    "так и сделай",
    "вот это",
    "это тоже",
    "тут тоже",
    "там тоже",
    "исправляй",
    "с учетом",
    "с учётом",
)


def load_private_env() -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        text = ENV_PATH.read_text(encoding="utf-8")
    except OSError:
        return values
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key:
            values[key] = value
    return values


def enabled() -> bool:
    return ENV_PATH.is_file()


def setting(name: str, default: str = "") -> str:
    private = load_private_env()
    return os.environ.get(name) or private.get(name) or default


def redact_sensitive(text: str) -> str:
    redacted = re.sub(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b", "[REDACTED_OPENAI_KEY]", text)
    redacted = re.sub(
        r"(?i)\b(OPENAI_API_KEY|ANTHROPIC_API_KEY|GITHUB_TOKEN|GH_TOKEN|API_KEY|SECRET|TOKEN)\s*=\s*[^\s]+",
        r"\1=[REDACTED]",
        redacted,
    )
    redacted = re.sub(r"(?i)\bAuthorization:\s*Bearer\s+[A-Za-z0-9._~+/=-]+", "Authorization: Bearer [REDACTED]", redacted)
    return redacted


def emit_context(context: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": context,
                }
            },
            ensure_ascii=False,
        )
    )


def normalize_prompt(prompt: str) -> str:
    lines = redact_sensitive(prompt).strip().splitlines()
    compacted: list[str] = []
    log_lines = 0
    for line in lines:
        stripped = line.strip()
        looks_like_log = bool(
            re.search(r"\b(GET|POST|PUT|PATCH|DELETE)\s+https?://", stripped)
            or re.search(r"\b(4\d\d|5\d\d)\b", stripped)
            or re.search(r"\bat\s+[\w.$-]+", stripped)
            or ".js:" in stripped
        )
        if looks_like_log:
            log_lines += 1
            if log_lines > MAX_LOG_LINES:
                continue
        compacted.append(stripped)
    text = "\n".join(compacted)
    if len(text) > MAX_PROMPT_CHARS:
        return text[:MAX_PROMPT_CHARS] + "\n[truncated for intake classification]"
    return text


def has_any(text: str, needles: tuple[str, ...]) -> bool:
    return any(needle in text for needle in needles)


def compact_text(text: str, limit: int) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."


def normalize_version(version: Any) -> str:
    if not isinstance(version, str):
        return ""
    cleaned = version.strip()
    if not cleaned:
        return ""
    if cleaned.startswith(("workspace:", "file:", "link:", "portal:", "github:", "git+")):
        return cleaned.split(":", 1)[0]
    cleaned = re.sub(r"^[~^<>=\s]+", "", cleaned)
    if " " in cleaned:
        cleaned = cleaned.split(" ", 1)[0]
    if "||" in cleaned:
        cleaned = cleaned.split("||", 1)[0].strip()
    return cleaned[:24]


def package_dependency_versions(package: dict[str, Any]) -> dict[str, str]:
    versions: dict[str, str] = {}
    for field in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        deps = package.get(field)
        if not isinstance(deps, dict):
            continue
        for name, version in deps.items():
            if isinstance(name, str) and name not in versions:
                versions[name] = normalize_version(version)
    return versions


def merge_dependency_versions(packages: list[dict[str, Any]]) -> dict[str, str]:
    merged: dict[str, str] = {}
    for package in packages:
        for name, version in package_dependency_versions(package).items():
            if name not in merged:
                merged[name] = version
    return merged


def architecture_stack_summary(packages: list[dict[str, Any]]) -> str:
    versions = merge_dependency_versions(packages)
    by_category: dict[str, list[str]] = {}
    for package_name, (category, label) in ARCHITECTURE_DEPENDENCIES.items():
        version = versions.get(package_name)
        if version is None:
            continue
        display = f"{label} {version}" if version else label
        by_category.setdefault(category, []).append(display)

    ordered_categories = (
        "framework",
        "backend",
        "language",
        "runtime",
        "build",
        "monorepo",
        "orm",
        "database",
        "cache",
        "queue",
        "contracts",
        "api",
        "ui",
        "test",
        "e2e",
        "quality",
        "observability",
        "logging",
    )
    parts: list[str] = []
    for category in ordered_categories:
        values = by_category.get(category)
        if values:
            parts.append(f"{category}=" + ", ".join(values[:4]))
    return "; ".join(parts)


def runtime_summary(package: dict[str, Any]) -> str:
    parts: list[str] = []
    engines = package.get("engines")
    if isinstance(engines, dict):
        node = engines.get("node")
        npm = engines.get("npm")
        if isinstance(node, str) and node.strip():
            parts.append(f"node {node.strip()}")
        if isinstance(npm, str) and npm.strip():
            parts.append(f"npm {npm.strip()}")
    package_manager = package.get("packageManager")
    if isinstance(package_manager, str) and package_manager.strip():
        parts.append(f"packageManager {package_manager.strip()}")
    return ", ".join(parts)


def read_package_json(path: Path) -> dict[str, Any]:
    try:
        package = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return package if isinstance(package, dict) else {}


def nearest_package_path(start: Path, root: Path) -> Path | None:
    try:
        current = start.resolve()
        root_resolved = root.resolve()
    except OSError:
        return None
    if current.is_file():
        current = current.parent
    for candidate in [current, *current.parents]:
        if root_resolved not in [candidate, *candidate.parents]:
            break
        package_path = candidate / "package.json"
        if package_path.is_file():
            return package_path
        if candidate == root_resolved or candidate == candidate.parent:
            break
    return None


def state_scope_key(payload: dict[str, Any]) -> str:
    for key in ("session_id", "sessionId", "conversation_id", "conversationId", "thread_id", "threadId"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return "session:" + value.strip()
    cwd = payload_cwd(payload)
    if cwd is not None:
        root = find_repo_root(cwd)
        if root is not None:
            return "repo:" + str(root)
        return "cwd:" + str(cwd)
    return "global"


def state_hash_key(scope: str) -> str:
    return hashlib.sha256(scope.encode("utf-8", errors="ignore")).hexdigest()[:32]


def load_state() -> dict[str, Any]:
    override = setting("HANDOFF_CLASSIFIER_STATE_PATH")
    paths = [Path(override)] if override else [PRIVATE_STATE_PATH, MEMORY_STATE_PATH]
    for path in paths:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        return payload if isinstance(payload, dict) else {"sessions": {}}
    return {"sessions": {}}


def save_state(state: dict[str, Any]) -> None:
    try:
        sessions = state.get("sessions")
        if isinstance(sessions, dict) and len(sessions) > MAX_STATE_SESSIONS:
            ordered = sorted(
                sessions.items(),
                key=lambda item: item[1].get("updated_at", 0) if isinstance(item[1], dict) else 0,
                reverse=True,
            )
            state["sessions"] = dict(ordered[:MAX_STATE_SESSIONS])
    except OSError:
        pass

    override = setting("HANDOFF_CLASSIFIER_STATE_PATH")
    paths = [Path(override)] if override else [PRIVATE_STATE_PATH, MEMORY_STATE_PATH]
    for path in paths:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = path.with_suffix(".tmp")
            tmp_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            os.chmod(tmp_path, 0o600)
            tmp_path.replace(path)
            return
        except OSError:
            continue


def follow_up_context_requested(prompt: str) -> bool:
    lower = prompt.lower().strip()
    if len(lower) <= 120 and has_any(lower, FOLLOW_UP_KEYWORDS):
        return True
    if re.fullmatch(r"(да|ок|окей|ага|угу|согласен|делай|доработай|продолжай)[\s!.]*", lower):
        return True
    return False


def previous_context_for_prompt(prompt: str, payload: dict[str, Any]) -> str:
    if not follow_up_context_requested(prompt):
        return ""
    state = load_state()
    sessions = state.get("sessions")
    if not isinstance(sessions, dict):
        return ""
    entry = sessions.get(state_hash_key(state_scope_key(payload)))
    if not isinstance(entry, dict):
        return ""
    previous_prompt = str(entry.get("last_prompt", "") or "").strip()
    previous_context = str(entry.get("last_context", "") or "").strip()
    if not previous_prompt and not previous_context:
        return ""

    parts = ["Previous local hook context for this session/repo."]
    if previous_prompt:
        parts.append("Previous user prompt: " + compact_text(redact_sensitive(previous_prompt), 500))
    if previous_context:
        parts.append("Previous classifier context: " + compact_text(redact_sensitive(previous_context), 650))
    parts.append("Use this only to resolve follow-up references like 'доработай', 'ещё', 'тогда', or 'сделай так'. Do not broaden scope beyond the current user prompt.")
    return compact_text(" ".join(parts), MAX_PREVIOUS_CONTEXT_CHARS)


def update_state(payload: dict[str, Any], prompt: str, context: str) -> None:
    state = load_state()
    sessions = state.get("sessions")
    if not isinstance(sessions, dict):
        sessions = {}
        state["sessions"] = sessions
    sessions[state_hash_key(state_scope_key(payload))] = {
        "updated_at": time.time(),
        "last_prompt": compact_text(redact_sensitive(prompt), 1600),
        "last_context": compact_text(redact_sensitive(context), 1800),
    }
    save_state(state)


def llm_input_from_prompt(prompt: str, payload: dict[str, Any]) -> str:
    previous_context = previous_context_for_prompt(prompt, payload)
    current = "Current user prompt:\n" + normalize_prompt(prompt)
    if previous_context:
        return previous_context + "\n\n" + current
    return normalize_prompt(prompt)


def has_action_request(text: str) -> bool:
    patterns = (
        r"\bсделай\b",
        r"\bсделать\s+надо\b",
        r"\bисправ(ь|ляй|ить)\b",
        r"\bдобав(ь|ить)\b",
        r"\bобнов(и|ить)\b",
        r"\bперезапуст(и|ить)\b",
        r"\bперезапускай\b",
        r"\bпочини\b",
        r"\bпочинить\b",
        r"\bпередел(ай|ать)\b",
        r"\bдоработай\b",
        r"\bвнеси\b",
        r"\bзапушь\b",
        r"\bзакоммит(ь|ьте)?\b",
        r"\bреализ(уй|овать)\b",
        r"\bприступай\s+к\s+реализации\b",
    )
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def deterministic_classify(prompt: str) -> dict[str, Any]:
    lower = prompt.lower()
    score = 0
    reasons: list[str] = []

    question_mark = "?" in prompt
    action_requested = has_action_request(lower)
    planning_words = (
        "план",
        "сплан",
        "архитектур",
        "исслед",
        "проанализ",
        "посмотри как",
        "как лучше",
        "миграц",
    )
    question_words = (
        "почему",
        "зачем",
        "разве",
        "есть ли",
        "можно ли",
        "как понять",
        "вопрос",
        "пока это просто вопрос",
        "пока вопрос",
    )
    continuation_words = ("продолжай", "лимиты обновились", "continue")
    multi_surface_words = (
        "дашборд",
        "crm",
        "бот",
        "api",
        "бд",
        "база",
        "платеж",
        "модел",
        "провайдер",
        "статист",
        "таб",
        "фильтр",
        "лента событий",
        "bot_legacy",
        "google analytics",
        "метрик",
    )
    bug_words = (
        "не работает",
        "не работают",
        "пусто",
        "по нулям",
        "ошибк",
        "500",
        "0 токенов",
        "не меняется",
        "отсутств",
    )

    if has_any(lower, continuation_words):
        return {
            "intent": "continue",
            "score": 3,
            "confidence": 0.9,
            "should_edit": False,
            "should_plan": False,
            "should_use_task_ledger": False,
            "subagents_authorized": False,
            "reason": "User asks to continue an existing task after limits reset.",
        }

    if action_requested:
        score += 5
        reasons.append("action verb")
    if has_any(lower, planning_words):
        score += 4
        reasons.append("planning/discovery language")
    if has_any(lower, multi_surface_words):
        score += 4
        reasons.append("multi-surface product/system terms")
    if has_any(lower, bug_words):
        score += 3
        reasons.append("bug/regression symptoms")
    if question_mark or has_any(lower, question_words):
        score += 2
        reasons.append("question language")
    if prompt.count("\n\n") >= 2 or len(prompt) > 900:
        score += 2
        reasons.append("multi-item prompt")
    if "$superpowers" in lower or "plugin://superpowers" in lower:
        score += 2
        reasons.append("Superpowers requested")

    score = min(score, 15)
    subagents_authorized = has_any(lower, ("сабагент", "subagent", "делег", "параллел", "parallel"))

    if "$superpowers" in lower and "приступай к реализации" in lower:
        intent = "execute_approved_plan"
        should_edit = True
        should_plan = False
    elif has_any(lower, ("начинай", "пиши план", "план писать")) and has_any(lower, planning_words):
        intent = "planning"
        should_edit = False
        should_plan = True
    elif action_requested:
        intent = "implementation"
        should_edit = True
        should_plan = score >= 10
    elif question_mark or has_any(lower, question_words):
        if score >= 8 and not has_any(lower, ("пока вопрос", "просто вопрос")):
            intent = "analysis"
            should_edit = False
            should_plan = True
        else:
            intent = "question_only"
            should_edit = False
            should_plan = False
    elif has_any(lower, planning_words):
        intent = "planning"
        should_edit = False
        should_plan = True
    else:
        intent = "analysis"
        should_edit = False
        should_plan = score >= 7

    should_use_task_ledger = score >= 7 and intent not in {"question_only", "continue"}
    confidence = 0.86
    if question_mark and action_requested:
        confidence = 0.68
    elif intent == "analysis" and score in range(6, 9):
        confidence = 0.7
    elif len(prompt.strip()) < 20:
        confidence = 0.72

    return {
        "intent": intent,
        "score": score,
        "confidence": confidence,
        "should_edit": should_edit,
        "should_plan": should_plan,
        "should_use_task_ledger": should_use_task_ledger,
        "subagents_authorized": subagents_authorized,
        "reason": ", ".join(reasons[:3]) or "simple prompt",
    }


def architecture_grade_requested(prompt: str, classification: dict[str, Any]) -> bool:
    lower = prompt.lower()
    intent = str(classification.get("intent", "analysis"))
    if intent in {"implementation", "execute_approved_plan"} and has_any(lower, ARCHITECTURE_KEYWORDS):
        return True
    if "делай как правильно" in lower or "как будет правильно" in lower:
        return True
    return False


def should_call_llm(classification: dict[str, Any], prompt: str) -> bool:
    mode = setting("HANDOFF_CLASSIFIER_LLM", "auto").lower()
    if mode in {"0", "false", "off", "none", "no"}:
        return False
    if mode in {"1", "true", "on", "always", "yes"}:
        return True
    if not setting("OPENAI_API_KEY"):
        return False
    if follow_up_context_requested(prompt):
        return True
    if float(classification.get("confidence", 1.0)) < 0.78:
        return True
    lower = prompt.lower()
    return "?" in prompt and has_any(lower, ("сделай", "исправ", "надо", "план", "реализ"))


def extract_output_text(response_payload: dict[str, Any]) -> str:
    if isinstance(response_payload.get("output_text"), str):
        return response_payload["output_text"]
    chunks: list[str] = []
    for item in response_payload.get("output", []) or []:
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []) or []:
            if isinstance(content, dict) and content.get("type") == "output_text":
                text = content.get("text")
                if isinstance(text, str):
                    chunks.append(text)
    return "".join(chunks)


def llm_classify(prompt: str, hook_payload: dict[str, Any]) -> dict[str, Any] | None:
    api_key = setting("OPENAI_API_KEY")
    if not api_key:
        return None
    model = setting("HANDOFF_CLASSIFIER_MODEL", DEFAULT_MODEL)
    try:
        timeout = float(setting("HANDOFF_CLASSIFIER_TIMEOUT", "4.0"))
    except ValueError:
        timeout = 4.0

    instructions = (
        "Classify a Russian user prompt for a Codex handoff/intake hook. "
        "Return only compact JSON with keys: intent, should_edit, should_plan, "
        "should_use_task_ledger, handoff_score_0_15, subagents_authorized, "
        "confidence_0_1, one_sentence_reason, normalized_task_brief, "
        "architecture_focus_terms. "
        "Intent must be one of question_only, analysis, planning, implementation, "
        "continue, execute_approved_plan. "
        "Subagents are authorized only when the user explicitly mentions subagents, "
        "delegation, or parallel work. "
        "When the prompt asks for implementation, fixes, refactoring, architecture, "
        "production-grade work, removal of legacy code, or 'do it properly', "
        "write normalized_task_brief as a professional engineering brief that preserves "
        "the user's scope and uses precise software-engineering terms. Prefer concrete "
        "process and architecture constraints over generic phrases like 'best practices'. "
        "Mention root-cause analysis, architecture boundaries, typed contracts, canonical "
        "source of truth, call graph impact, migration/removal of obsolete paths, and "
        "scoped verification only when relevant. Do not invent new product requirements. "
        "If the input includes 'Previous local hook context' and the current prompt is a "
        "short imperative follow-up like 'доработай', 'продолжай', 'ещё', or 'сделай так', "
        "resolve the missing object from the previous context. Do not classify it as "
        "ambiguous merely because the current prompt is short; carry forward the previous "
        "implementation/planning intent unless the current prompt changes or narrows scope."
    )
    request_payload = {
        "model": model,
        "instructions": instructions,
        "input": llm_input_from_prompt(prompt, hook_payload),
        "max_output_tokens": 420,
        "store": False,
    }
    data = json.dumps(request_payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
    except (OSError, error.HTTPError, error.URLError, TimeoutError):
        return None

    try:
        parsed = json.loads(body)
        text = extract_output_text(parsed).strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
        result = json.loads(text)
    except (json.JSONDecodeError, TypeError, ValueError):
        return None
    if not isinstance(result, dict):
        return None
    return result


def merged_classification(prompt: str, payload: dict[str, Any]) -> tuple[dict[str, Any], str]:
    base = deterministic_classify(prompt)
    if should_call_llm(base, prompt):
        start = time.monotonic()
        llm = llm_classify(prompt, payload)
        if llm:
            elapsed_ms = int((time.monotonic() - start) * 1000)
            return llm, f"llm:{elapsed_ms}ms"
    return base, "deterministic"


def find_repo_root(start: Path) -> Path | None:
    try:
        current = start.resolve()
    except OSError:
        return None
    if current.is_file():
        current = current.parent
    candidates = [current, *current.parents]
    for candidate in candidates:
        if (candidate / ".git").exists():
            return candidate
        if candidate == candidate.parent:
            break
    for candidate in candidates:
        if (candidate / "AGENTS.md").is_file():
            return candidate
        if candidate == candidate.parent:
            break
    for candidate in candidates:
        if (candidate / ".git").exists() or (candidate / "package.json").is_file() or (candidate / "AGENTS.md").is_file():
            return candidate
        if candidate == candidate.parent:
            break
    return None


def payload_cwd(payload: dict[str, Any]) -> Path | None:
    for key in ("cwd", "workingDirectory", "working_directory", "workspace", "repoPath", "repo_path"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return Path(value)
    return None


def repo_profile_from_payload(payload: dict[str, Any]) -> str:
    cwd = payload_cwd(payload)
    if cwd is None:
        return ""
    root = find_repo_root(cwd)
    if root is None:
        return ""

    facts: list[str] = []
    packages_for_stack: list[dict[str, Any]] = []
    package_path = root / "package.json"
    package = read_package_json(package_path)
    if package:
        packages_for_stack.append(package)
    nearest_path = nearest_package_path(cwd, root)
    nearest_package: dict[str, Any] = {}
    if nearest_path is not None and nearest_path != package_path:
        nearest_package = read_package_json(nearest_path)
        if nearest_package:
            packages_for_stack.insert(0, nearest_package)
    if isinstance(package, dict):
        name = package.get("name")
        package_manager = package.get("packageManager")
        if isinstance(name, str) and name:
            facts.append(f"project={name}")
        nearest_name = nearest_package.get("name")
        if isinstance(nearest_name, str) and nearest_name and nearest_name != name:
            facts.append(f"workspace={nearest_name}")
        runtime = runtime_summary(package)
        if runtime:
            facts.append(f"runtime: {runtime}")
        workspaces = package.get("workspaces")
        if isinstance(workspaces, list) and workspaces:
            facts.append("npm workspaces present")
        scripts = package.get("scripts") if isinstance(package.get("scripts"), dict) else {}
        stack = architecture_stack_summary(packages_for_stack)
        if stack:
            facts.append("stack: " + stack)
        deps_blob = json.dumps(
            {
                "scripts": scripts,
                "dependencies": package.get("dependencies", {}),
                "devDependencies": package.get("devDependencies", {}),
            },
            ensure_ascii=False,
        )
        if "turbo" in deps_blob:
            facts.append("Turbo monorepo workflow")
        verification = [name for name in ("lint", "typecheck", "test", "verify", "test:architecture") if name in scripts]
        if verification:
            facts.append("verification scripts: " + ", ".join(verification))

    agents_path = root / "AGENTS.md"
    try:
        agents_text = agents_path.read_text(encoding="utf-8")[:12000].lower()
    except OSError:
        agents_text = ""
    if "gitnexus" in agents_text and "impact analysis" in agents_text:
        facts.append("AGENTS.md requires GitNexus impact analysis before symbol edits")
    if "detect_changes" in agents_text:
        facts.append("AGENTS.md requires GitNexus detect_changes before commit")

    if (root / "apps").is_dir() and (root / "packages").is_dir():
        facts.append("apps/* and packages/* layout")

    if not facts:
        return ""
    return compact_text("Project profile: " + "; ".join(dict.fromkeys(facts)) + ".", MAX_REPO_PROFILE_CHARS)


def deterministic_normalized_brief(prompt: str, classification: dict[str, Any]) -> str:
    intent = str(classification.get("intent", "analysis"))
    should_edit = bool(classification.get("should_edit", False))
    should_ledger = bool(classification.get("should_use_task_ledger", False))
    architecture_grade = architecture_grade_requested(prompt, classification)

    if intent == "question_only":
        return ""
    if intent == "planning":
        return (
            "Normalized task brief: treat this as a planning/discovery request. Map the affected domain, data flow, "
            "public contracts, risks, and verification path before proposing implementation steps."
        )
    if intent == "analysis" and not should_edit:
        return ""
    if not should_edit:
        return ""

    if architecture_grade:
        brief = (
            "Normalized task brief: treat this as a production-grade architectural change, not a quick patch. "
            "Before editing, identify the root cause, affected bounded context, public contracts, data flow, "
            "and call graph impact. Preserve existing domain/application/infrastructure boundaries; avoid hidden "
            "coupling, duplicated business logic, global mutable state, and ad-hoc parsing when typed contracts "
            "or project abstractions exist. Update the canonical source of truth first, then adapters, callers, "
            "tests, and docs. Remove obsolete execution paths after references are migrated. Do not add temporary "
            "compatibility shims, fallback branches, TODO-based transitional code, or legacy aliases unless the "
            "user explicitly approves a migration window. Before the first edit, summarize dirty-worktree risk, "
            "affected apps/packages, architecture risk, migration steps, and scoped verification commands."
        )
    else:
        brief = (
            "Normalized task brief: treat this as an implementation request. Diagnose the root cause before edits, "
            "preserve project boundaries, prefer existing abstractions and typed contracts, keep changes scoped to "
            "the requested behavior, update callers/tests together, and verify the narrowest relevant surface."
        )
    if should_ledger:
        brief += " Maintain a task ledger for multi-issue work and map verification results back to it."
    return compact_text(brief, MAX_BRIEF_CHARS)


def context_from_classification(classification: dict[str, Any], source: str, prompt: str, payload: dict[str, Any]) -> str:
    intent = str(classification.get("intent", "analysis"))
    score = classification.get("handoff_score_0_15", classification.get("score", 0))
    confidence = classification.get("confidence_0_1", classification.get("confidence", 0))
    should_edit = bool(classification.get("should_edit", False))
    should_plan = bool(classification.get("should_plan", False))
    should_ledger = bool(classification.get("should_use_task_ledger", False))
    subagents = bool(classification.get("subagents_authorized", False))
    reason = str(classification.get("one_sentence_reason", classification.get("reason", "")))
    normalized_brief = str(classification.get("normalized_task_brief", "") or "").strip()
    architecture_terms = classification.get("architecture_focus_terms", [])

    guidance = [
        f"Handoff intake classifier ({source}): intent={intent}, score={score}, confidence={confidence}.",
        f"Flags: should_edit={str(should_edit).lower()}, should_plan={str(should_plan).lower()}, task_ledger={str(should_ledger).lower()}, subagents_authorized={str(subagents).lower()}.",
    ]
    if reason:
        guidance.append(f"Reason: {reason}")
    if intent == "question_only":
        guidance.append("Answer the question directly. Do not edit files or run implementation commands unless the user explicitly asks for work.")
    elif intent == "planning":
        guidance.append("Do discovery and produce a plan. Do not implement yet unless the user explicitly asks for implementation.")
    elif intent == "analysis":
        guidance.append("Investigate enough to answer or plan. Avoid edits unless the prompt clearly asks for a fix.")
    elif intent in {"implementation", "execute_approved_plan"}:
        guidance.append("Proceed with implementation inline. Build a task ledger for multi-issue work and verify before completion.")
        if should_plan:
            guidance.append("Before the first edit, produce a short implementation plan with affected surfaces, architecture risks, and verification commands.")
    elif intent == "continue":
        guidance.append("Continue the prior task using the current context; first recover the last known state if needed.")
    if normalized_brief:
        guidance.append("Normalized task brief: " + compact_text(normalized_brief, MAX_BRIEF_CHARS))
    else:
        deterministic_brief = deterministic_normalized_brief(prompt, classification)
        if deterministic_brief:
            guidance.append(deterministic_brief)
    if isinstance(architecture_terms, list) and architecture_terms:
        terms = ", ".join(str(term).strip() for term in architecture_terms if str(term).strip())
        if terms:
            guidance.append("Architecture focus terms: " + compact_text(terms, 240) + ".")
    repo_profile = repo_profile_from_payload(payload)
    if repo_profile:
        guidance.append(repo_profile)
    if source.startswith("llm") and previous_context_for_prompt(prompt, payload):
        guidance.append("Follow-up context: previous local prompt/context was included for resolving short references; keep scope anchored to the current user request.")
    if not subagents:
        guidance.append("Do not spawn subagents unless the user explicitly authorizes delegation, parallel work, or subagents.")
    return " ".join(guidance)


def main() -> int:
    if not enabled():
        return 0

    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    prompt = payload.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        return 0

    try:
        classification, source = merged_classification(prompt, payload)
        context = context_from_classification(classification, source, prompt, payload)
        emit_context(context)
        update_state(payload, prompt, context)
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

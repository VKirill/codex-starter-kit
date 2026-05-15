#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import socket
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
CAPTURE_STOP = PLUGIN_ROOT / "scripts" / "capture_stop.py"
SETTINGS_TEMPLATE = PLUGIN_ROOT / "templates" / "claude-settings.json"
DEFAULT_TIMEOUT_SECONDS = 1800
DEFAULT_IDLE_TIMEOUT_SECONDS = 180
DEFAULT_STARTUP_TIMEOUT_SECONDS = 60
DEFAULT_POLL_INTERVAL_SECONDS = 2.0
CAPTURE_HISTORY_LINES = 240


@dataclass(frozen=True)
class Mode:
    name: str
    title: str
    default_model: str
    purpose: str
    lenses: tuple[str, ...]
    verdicts: tuple[str, ...]
    sections: tuple[str, ...]


MODES: dict[str, Mode] = {
    "superpowers-plan-review": Mode("superpowers-plan-review", "Claude Superpowers Plan Review", "sonnet", "Review a Superpowers-style implementation plan before execution.", ("agent-executable steps", "observable truths", "acceptance checks", "risk gates", "preserve user work"), ("APPROVE", "APPROVE_WITH_CHANGES", "NEEDS_REVISION"), ("Blocking Plan Issues", "Suggested Improvements", "Missing Acceptance Checks", "Suggested Plan Patch", "Residual Risk")),
    "plan-red-team": Mode("plan-red-team", "Claude Plan Red-Team Review", "opus", "Attack a complex or risky plan before implementation.", ("failure scenarios", "missing guardrails", "rollback difficulty", "unsafe assumptions"), ("PROCEED", "PROCEED_WITH_GUARDS", "REDESIGN"), ("Strongest Failure Scenarios", "Missing Guardrails", "Simplification Opportunity", "Decision Notes")),
    "scope-trimmer": Mode("scope-trimmer", "Claude Scope Trim Review", "sonnet", "Remove unnecessary scope and speculative work.", ("original request fit", "minimum viable change", "defer/remove decisions"), ("TIGHT", "TRIM_RECOMMENDED", "OVER_SCOPED"), ("Essential Work", "Defer", "Remove", "Minimal Plan Patch")),
    "acceptance-checker": Mode("acceptance-checker", "Claude Acceptance Check Review", "sonnet", "Turn vague outcomes into observable checks.", ("observable truth", "expected result", "manual vs automated proof"), ("CHECKS_READY", "ADD_CHECKS", "CHECKS_TOO_VAGUE"), ("Missing Observable Truths", "Required Checks", "Plan Patch")),
    "risk-register": Mode("risk-register", "Claude Risk Register", "sonnet", "Create a practical risk register.", ("data", "auth", "permissions", "delivery", "operational signals"), ("LOW_RISK", "MANAGEABLE_RISK", "HIGH_RISK"), ("Risk Register", "Required Plan Additions", "User Decisions Needed")),
    "architecture-decision-review": Mode("architecture-decision-review", "Claude Architecture Decision Review", "opus", "Review an architectural decision and alternatives.", ("reversibility", "coupling", "state ownership", "operational burden", "migration path"), ("ACCEPT", "ACCEPT_WITH_CONSTRAINTS", "RECONSIDER"), ("Decision Quality", "Alternatives Not Considered", "Consequences", "ADR Patch")),
    "implementation-strategy": Mode("implementation-strategy", "Claude Implementation Strategy", "sonnet", "Recommend safe implementation sequencing.", ("discovery first", "file order", "risk placement", "verification placement"), ("ORDER_OK", "REORDER_RECOMMENDED", "DISCOVERY_NEEDED"), ("Recommended Sequence", "Discovery Before Edits", "Risky Steps", "Verification Placement")),
    "code-review": Mode("code-review", "Claude Code Review", "sonnet", "Review completed implementation work for bugs and regressions.", ("plan compliance", "correctness", "regressions", "data safety", "security", "missing tests"), ("APPROVE", "APPROVE_WITH_FIXES", "NEEDS_WORK"), ("Findings", "Missing Tests", "Regression Risks", "Fix Order")),
    "minimal-change-review": Mode("minimal-change-review", "Claude Minimal Change Review", "sonnet", "Check whether the change exceeds the user request.", ("scope creep", "drive-by refactors", "necessary vs questionable changes"), ("SCOPED", "MINOR_SCOPE_RISK", "OVERREACH"), ("Necessary Changes", "Questionable Changes", "Revert Or Keep")),
    "legacy-safety-review": Mode("legacy-safety-review", "Claude Legacy Safety Review", "opus", "Review old or high-blast-radius code safely.", ("characterization checks", "hidden behavior", "blast radius", "rollback"), ("SAFE_ENOUGH", "ADD_CHARACTERIZATION", "HIGH_BLAST_RADIUS"), ("Hidden Behavior Risks", "Characterization Checks", "Safer Change Shape")),
    "api-contract-review": Mode("api-contract-review", "Claude API Contract Review", "sonnet", "Review public API compatibility.", ("routes", "schemas", "error shapes", "backward compatibility"), ("COMPATIBLE", "COMPATIBLE_WITH_FIXES", "BREAKING_RISK"), ("Contract Findings", "Backward Compatibility Checks", "Error Response Review")),
    "data-consistency-review": Mode("data-consistency-review", "Claude Data Consistency Review", "opus", "Review writes, migrations, and state consistency.", ("transactions", "locks", "IDs", "timestamps", "partial failure"), ("CONSISTENT", "NEEDS_GUARDS", "DATA_RISK"), ("Consistency Findings", "Migration/Rollback Notes", "Verification Checks")),
    "test-gap-review": Mode("test-gap-review", "Claude Test Gap Review", "sonnet", "Find missing verification proportional to risk.", ("happy path", "error path", "boundaries", "compatibility"), ("ENOUGH", "ADD_NARROW_CHECKS", "ADD_BROAD_CHECKS"), ("Missing Checks", "Over-Testing To Avoid", "Verification Patch")),
    "failure-mode-review": Mode("failure-mode-review", "Claude Failure Mode Review", "sonnet", "Review error paths and degraded behavior.", ("timeouts", "retries", "fallbacks", "cleanup"), ("ROBUST", "NEEDS_ERROR_HANDLING", "FRAGILE"), ("Failure Scenarios", "Recovery And Retry", "Verification")),
    "observability-review": Mode("observability-review", "Claude Observability Review", "sonnet", "Check whether future debugging will be possible.", ("logs", "metrics", "diagnostics", "noise"), ("DEBUGGABLE", "ADD_SIGNALS", "BLIND_SPOTS"), ("Missing Signals", "Noise To Avoid", "Diagnostic Checklist")),
    "performance-review": Mode("performance-review", "Claude Performance Review", "opus", "Look for realistic performance risks.", ("hot paths", "N+1", "bundle/runtime cost", "measurement"), ("OK", "WATCH", "PERFORMANCE_RISK"), ("Performance Findings", "Measurement Needed", "Avoid Premature Optimization")),
    "security-review": Mode("security-review", "Claude Security Review", "opus", "Review realistic security risks.", ("trust boundaries", "auth", "permissions", "validation", "secrets", "injection"), ("LOW_RISK", "NEEDS_GUARDS", "HIGH_RISK"), ("Threat Findings", "Required Guards", "Security Verification")),
    "privacy-review": Mode("privacy-review", "Claude Privacy Review", "opus", "Review user data exposure and retention.", ("PII", "logs", "transcripts", "retention", "redaction"), ("OK", "NEEDS_REDACTION", "PRIVACY_RISK"), ("Data Exposure Findings", "Retention And Deletion", "Logging/Transcript Safety")),
    "ux-flow-review": Mode("ux-flow-review", "Claude UX Flow Review", "sonnet", "Review user-visible workflows.", ("primary task", "empty/loading/error/success states", "recovery"), ("READY", "NEEDS_UX_FIXES", "FLOW_RISK"), ("Workflow Findings", "Missing States", "Manual UX Checks")),
    "accessibility-review": Mode("accessibility-review", "Claude Accessibility Review", "sonnet", "Review practical accessibility barriers.", ("keyboard", "focus", "labels", "contrast", "screen reader"), ("PASS_LIKELY", "NEEDS_A11Y_CHECKS", "ACCESSIBILITY_RISK"), ("Barriers", "Required Checks", "Acceptance Patch")),
    "responsive-review": Mode("responsive-review", "Claude Responsive Review", "sonnet", "Review responsive layout and text fit.", ("viewport behavior", "overflow", "layout stability", "text fit"), ("LIKELY_OK", "NEEDS_VIEWPORT_CHECKS", "RESPONSIVE_RISK"), ("Layout Risks", "Required Screenshots", "Text Fit Checks")),
    "copy-review": Mode("copy-review", "Claude Copy Review", "sonnet", "Review product copy and UI text.", ("clarity", "tone", "errors", "empty states", "consistency"), ("COPY_OK", "COPY_FIXES", "COPY_RISK"), ("Copy Findings", "Error/Empty State Text", "Consistency Notes")),
    "visual-regression-plan": Mode("visual-regression-plan", "Claude Visual Regression Plan", "sonnet", "Create the smallest useful screenshot plan.", ("screen matrix", "states", "viewports", "interaction checks"), ("LIGHT_CHECK", "STANDARD_SCREENSHOTS", "BROAD_VISUAL_QA"), ("Screenshot Matrix", "Pixel/Interaction Checks", "Out Of Scope")),
    "release-readiness-review": Mode("release-readiness-review", "Claude Release Readiness Review", "sonnet", "Decide whether Codex can present the work as complete.", ("verification", "known failures", "residual risk", "truthful final answer"), ("READY", "READY_WITH_RISK", "NOT_READY"), ("Blocking Gaps", "Residual Risks", "Final Answer Notes")),
    "rollback-review": Mode("rollback-review", "Claude Rollback Review", "opus", "Check whether the change can be safely undone.", ("rollback steps", "irreversible changes", "backup checks"), ("ROLLBACK_READY", "NEEDS_ROLLBACK_PLAN", "HARD_TO_ROLLBACK"), ("Rollback Steps", "Irreversible Changes", "Pre-Deploy Backup Checks")),
    "incident-premortem": Mode("incident-premortem", "Claude Incident Premortem", "opus", "Imagine a post-release incident and prevent it.", ("incident stories", "detection signal", "prevention", "monitoring"), ("LOW_INCIDENT_RISK", "ADD_GUARDS", "HIGH_INCIDENT_RISK"), ("Plausible Incident Stories", "Pre-Release Safeguards", "Monitoring After Release")),
    "handoff-summary-review": Mode("handoff-summary-review", "Claude Handoff Summary Review", "sonnet", "Check final summary truthfulness.", ("must mention", "unsupported claims", "known failures"), ("SUMMARY_READY", "ADD_CONTEXT", "DO_NOT_CLAIM_DONE"), ("Must Mention", "Must Not Claim", "Suggested Final Summary")),
    "documentation-review": Mode("documentation-review", "Claude Documentation Review", "sonnet", "Check whether docs need to change.", ("missing docs", "stale docs", "no-docs rationale"), ("DOCS_OK", "DOCS_SHOULD_CHANGE", "DOCS_BLOCKING"), ("Missing Documentation", "Stale Documentation", "No-Docs Rationale")),
    "second-opinion-opus": Mode("second-opinion-opus", "Claude Opus Second Opinion", "opus", "High-stakes second opinion review.", ("top concerns", "best next move", "what not to overthink"), ("CONFIDENT", "CONCERNS", "STOP_AND_RETHINK"), ("Top Concerns", "Best Next Move", "What Not To Overthink")),
    "fast-sonnet-check": Mode("fast-sonnet-check", "Claude Fast Check", "sonnet", "Fast sanity check with high-signal findings only.", ("obvious issues", "quick wins"), ("OK", "FIX_SMALL_ISSUES", "NEEDS_ATTENTION"), ("High-Signal Issues", "Quick Win")),
    "multi-perspective-review": Mode("multi-perspective-review", "Claude Multi-Perspective Review", "opus", "Review from multiple roles in one pass.", ("architect", "security", "QA", "product/UX"), ("APPROVE", "APPROVE_WITH_FIXES", "NEEDS_WORK"), ("Architect View", "Security View", "QA View", "Product/UX View", "Prioritized Actions")),
    "contradiction-finder": Mode("contradiction-finder", "Claude Contradiction Review", "sonnet", "Find conflicts between request, docs, plan, and changed files.", ("instruction conflicts", "ambiguity", "resolution"), ("CONSISTENT", "MINOR_CONFLICTS", "CONTRADICTIONS"), ("Contradictions", "Ambiguities", "Patch Recommendations")),
    "user-intent-audit": Mode("user-intent-audit", "Claude User Intent Audit", "sonnet", "Check whether Codex is still solving the user request.", ("alignment", "drift", "realignment"), ("ALIGNED", "PARTIAL_DRIFT", "MISALIGNED"), ("Alignment", "Drift", "Realignment Patch")),
    "prompt-quality-review": Mode("prompt-quality-review", "Claude Prompt Quality Review", "sonnet", "Review prompt/plan executable quality.", ("specificity", "missing inputs", "success criteria", "conflicts"), ("READY", "NEEDS_CLARITY", "NOT_EXECUTABLE"), ("Ambiguous Instructions", "Missing Inputs", "Improved Prompt Patch")),
}


MODE_METHODOLOGIES: dict[str, str] = {
    "superpowers-plan-review": "Check whether the plan is executable by Codex: clear worker routing, scoped files, dependency gates, acceptance checks, review checkpoints, and verification commands. Flag missing sequencing, unsafe assumptions, and places where the plan cannot be tested.",
    "plan-red-team": "Attack the plan like a release incident review: identify the most likely failure paths, hidden dependencies, data loss paths, rollback gaps, and decisions that should be made before implementation.",
    "scope-trimmer": "Separate must-have work from speculative work. Recommend the smallest path that satisfies the user request, and list what should be deferred or removed.",
    "acceptance-checker": "Turn goals into observable truths. Check that each major requirement has a concrete automated or manual proof, expected result, and ownership.",
    "risk-register": "Produce a practical risk register: risk, trigger, impact, mitigation, verification, and owner. Prioritize data, auth, permissions, delivery, and operational blind spots.",
    "architecture-decision-review": "Evaluate the decision as a senior architect: reversibility, coupling, state ownership, migration path, operational burden, and better alternatives.",
    "implementation-strategy": "Review sequencing before edits: discovery first, safest file order, dependency gates, risky operations, and where verification should happen.",
    "code-review": "Review as a senior code reviewer. Start from plan compliance, inspect changed files and nearby code, check correctness/error paths/tests/security/data risks, then return findings with fix order.",
    "minimal-change-review": "Check whether the implementation exceeded the user request. Separate necessary changes from drive-by refactors, questionable churn, and safer smaller alternatives.",
    "legacy-safety-review": "Treat the code as high-blast-radius legacy. Look for hidden behavior, characterization gaps, compatibility risk, and a safer staged change shape.",
    "api-contract-review": "Review public contract compatibility: routes, schemas, error shapes, status codes, clients, versioning, and migration or backward-compatibility needs.",
    "data-consistency-review": "Review state correctness: transactions, partial failures, idempotency, identity mapping, migrations, timestamps, locks, and rollback or repair paths.",
    "test-gap-review": "Compare verification to risk. Identify missing narrow tests first, then integration/e2e checks only where behavior crosses boundaries.",
    "failure-mode-review": "Walk through degraded paths: timeouts, retries, cleanup, cancellation, fallback behavior, and user-visible failure states.",
    "observability-review": "Ask whether the next incident can be debugged. Check logs, metrics, correlation IDs, diagnostic context, noise, and privacy-safe signals.",
    "performance-review": "Look for realistic performance risks: hot paths, N+1 queries, unbounded work, bundle/runtime costs, and missing measurements.",
    "security-review": "Review trust boundaries: authn/authz, input validation, secrets, injection, uploads, SSRF/path traversal, dependency exposure, and least privilege.",
    "privacy-review": "Review user data handling: PII exposure, logs, retention, redaction, third-party transfer, transcripts, and deletion expectations.",
    "ux-flow-review": "Trace the user workflow through loading, empty, error, success, undo/retry, and recovery states. Flag friction that blocks the primary task.",
    "accessibility-review": "Check practical accessibility: keyboard path, focus order, labels, names, contrast, screen-reader affordances, and motion/interaction barriers.",
    "responsive-review": "Review layout resilience: viewport matrix, text fit, overflow, stable dimensions, interaction targets, and screenshots needed.",
    "copy-review": "Review product text for clarity, tone, consistency, empty/error states, user actionability, and misleading claims.",
    "visual-regression-plan": "Define the smallest useful visual proof: pages/states/viewports/interactions, expected screenshots, and what is intentionally out of scope.",
    "release-readiness-review": "Decide whether Codex can truthfully report completion. Check verification evidence, known failures, migrations, rollback notes, docs, and residual risk.",
    "rollback-review": "Check undo safety: reversible migrations, backups, feature flags, data repair, deployment order, and exact rollback commands or blockers.",
    "incident-premortem": "Imagine the post-release incident. Name plausible incident stories, detection signals, prevention patches, and monitoring after release.",
    "handoff-summary-review": "Audit the final report for truthfulness: what changed, what was verified, what failed, what remains risky, and what must not be claimed.",
    "documentation-review": "Check docs impact: public API, setup, runbooks, README, architecture decisions, changelog, and whether no-docs is defensible.",
    "second-opinion-opus": "Give the strongest independent second opinion. Focus on the top few concerns, the best next move, and what not to over-optimize.",
    "fast-sonnet-check": "Perform a short high-signal pass. Return only blockers, obvious regressions, and small fixes with high confidence.",
    "multi-perspective-review": "Review from architect, security, QA, and product/UX viewpoints, then merge findings into one prioritized action list.",
    "contradiction-finder": "Compare user request, plan, docs, changed files, and verification. Find contradictions, ambiguous instructions, and the safest resolution.",
    "user-intent-audit": "Check whether Codex is still solving the newest user request. Flag drift, missing requested behavior, and a concise realignment patch.",
    "prompt-quality-review": "Review the prompt or plan as executable instructions: specificity, missing inputs, conflicting constraints, success criteria, and improved wording.",
}


def mode_methodology(mode_name: str) -> str:
    return MODE_METHODOLOGIES.get(
        mode_name,
        "Review the supplied scope as a senior second-opinion reviewer. Inspect the listed files, compare against the request and verification, and return concrete findings with fix order.",
    )


class RunnerError(RuntimeError):
    pass


@dataclass(frozen=True)
class MonitorResult:
    wait_seconds: float
    exit_reason: str
    tmux_state: str


@dataclass(frozen=True)
class McpRuntime:
    profile: str
    config_path: Path
    enabled: tuple[str, ...]
    unavailable: tuple[str, ...]


@dataclass(frozen=True)
class PriorReview:
    request_id: str
    session: str
    inbox_path: Path
    outbox_path: Path
    metadata_path: Path
    status: str


def run(args: list[str], cwd: Path, *, check: bool = True, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def discover_claude() -> str:
    explicit = os.environ.get("CLAUDE_BIN")
    candidates = [explicit] if explicit else []
    found = shutil.which("claude")
    if found:
        candidates.append(found)
    candidates.extend(
        [
            str(Path.home() / ".local" / "bin" / "claude"),
            str(Path.home() / ".npm-global" / "bin" / "claude"),
            "/usr/local/bin/claude",
            "/opt/homebrew/bin/claude",
        ]
    )
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise RunnerError("Claude Code CLI was not found. Claude Companion does not install Claude; install/login to Claude Code first.")


def require_tmux_after_claude() -> str:
    tmux = shutil.which("tmux")
    if not tmux:
        raise RunnerError("tmux was not found. Claude is installed, but this plugin requires tmux to be installed manually.")
    return tmux


def git_text(project_root: Path, args: list[str], fallback: str = "Not available") -> str:
    result = run(["git", *args], project_root, check=False)
    text = (result.stdout or result.stderr).strip()
    return text if text else fallback


def git_changed_files(project_root: Path) -> str:
    result = run(["git", "status", "--porcelain=v1", "-uall"], project_root, check=False)
    text = (result.stdout or result.stderr).strip()
    if not text:
        return "No changed files reported by git status."

    files: list[str] = []
    for line in text.splitlines():
        if not line:
            continue
        path = line[3:] if len(line) > 3 else line
        if " -> " in path:
            old_path, new_path = path.split(" -> ", 1)
            files.append(f"{old_path} -> {new_path}")
        else:
            files.append(path)
    return "\n".join(f"- {path}" for path in files)


def read_optional(path: str | None, project_root: Path) -> str:
    if not path:
        return "Not provided"
    input_path = Path(path)
    if not input_path.is_absolute():
        input_path = project_root / input_path
    if not input_path.exists():
        raise RunnerError(f"input file not found: {input_path}")
    return input_path.read_text(encoding="utf-8", errors="replace")


def redact(text: str) -> str:
    patterns = [
        (r"(?i)(api[_-]?key|token|secret|password|bearer)\s*[:=]\s*['\"]?[^'\"\s]+", r"\1=[REDACTED]"),
        (r"(?i)authorization:\s*bearer\s+[A-Za-z0-9._~+/=-]+", "authorization: bearer [REDACTED]"),
    ]
    redacted = text
    for pattern, replacement in patterns:
        redacted = re.sub(pattern, replacement, redacted)
    return redacted


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, object] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def review_fingerprint(payload: dict[str, object]) -> str:
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:24]


def load_prior_review(index_path: Path) -> PriorReview | None:
    payload = read_json(index_path)
    if not payload:
        return None
    try:
        return PriorReview(
            request_id=str(payload["request_id"]),
            session=str(payload["session"]),
            inbox_path=Path(str(payload["inbox_path"])),
            outbox_path=Path(str(payload["outbox_path"])),
            metadata_path=Path(str(payload["metadata_path"])),
            status=str(payload.get("status") or "unknown"),
        )
    except KeyError:
        return None


def mode_mcp_profile(mode_name: str) -> str:
    if mode_name in {
        "superpowers-plan-review",
        "plan-red-team",
        "scope-trimmer",
        "acceptance-checker",
        "risk-register",
        "architecture-decision-review",
        "implementation-strategy",
        "prompt-quality-review",
    }:
        return "plan"
    if mode_name in {
        "code-review",
        "minimal-change-review",
        "legacy-safety-review",
        "api-contract-review",
        "data-consistency-review",
        "test-gap-review",
        "failure-mode-review",
        "observability-review",
        "performance-review",
        "security-review",
        "privacy-review",
        "release-readiness-review",
        "rollback-review",
        "incident-premortem",
        "handoff-summary-review",
        "second-opinion-opus",
        "fast-sonnet-check",
        "multi-perspective-review",
        "contradiction-finder",
        "user-intent-audit",
    }:
        return "code"
    if mode_name == "documentation-review":
        return "docs"
    return "none"


def profile_server_names(profile: str, mode_name: str) -> tuple[str, ...]:
    resolved = mode_mcp_profile(mode_name) if profile == "auto" else profile
    if resolved == "docs":
        return ("serena", "gitnexus", "context7")
    if resolved in {"plan", "code", "data"}:
        return ("serena", "gitnexus")
    return ()


def can_connect_tcp(url: str, timeout: float = 0.35) -> bool:
    match = re.match(r"^https?://([^/:]+)(?::(\d+))?/", url)
    if not match:
        return False
    host = match.group(1)
    port = int(match.group(2) or (443 if url.startswith("https://") else 80))
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def bearer_headers_helper(env_name: str) -> str:
    script = (
        "import json, os, sys; "
        f"token=os.environ.get({env_name!r}, ''); "
        "sys.exit(1) if not token else print(json.dumps({'Authorization':'Bearer '+token}))"
    )
    return f"python3 -c {shlex.quote(script)}"


def build_mcp_runtime(profile: str, mode_name: str, runtime_dir: Path) -> McpRuntime:
    wanted = profile_server_names(profile, mode_name)
    servers: dict[str, dict[str, object]] = {}
    unavailable: list[str] = []

    if "serena" in wanted:
        uvx = shutil.which("uvx")
        if uvx:
            serena_context = os.environ.get("CLAUDE_COMPANION_SERENA_CONTEXT", "codex")
            servers["serena"] = {
                "type": "stdio",
                "command": uvx,
                "args": [
                    "--from",
                    "git+https://github.com/oraios/serena",
                    "serena",
                    "start-mcp-server",
                    f"--context={serena_context}",
                ],
                "env": {},
            }
        else:
            unavailable.append("serena: uvx not found")

    if "gitnexus" in wanted:
        gitnexus = shutil.which("gitnexus")
        if gitnexus:
            servers["gitnexus"] = {
                "type": "stdio",
                "command": gitnexus,
                "args": ["mcp"],
                "env": {},
            }
        else:
            gitnexus_url = os.environ.get("CLAUDE_COMPANION_GITNEXUS_URL", "http://127.0.0.1:9401/api/mcp")
            token_env = os.environ.get("CLAUDE_COMPANION_GITNEXUS_TOKEN_ENV", "SELFY_MCP_BEARER")
            if os.environ.get(token_env) and can_connect_tcp(gitnexus_url):
                servers["gitnexus"] = {
                    "type": "http",
                    "url": gitnexus_url,
                    "headersHelper": bearer_headers_helper(token_env),
                }
            else:
                unavailable.append("gitnexus: gitnexus command not found and local HTTP MCP unavailable")

    if "context7" in wanted:
        servers["context7"] = {
            "type": "http",
            "url": os.environ.get("CLAUDE_COMPANION_CONTEXT7_URL", "https://mcp.context7.com/mcp"),
        }

    config_path = runtime_dir / "mcp-config.json"
    config_path.write_text(json.dumps({"mcpServers": servers}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return McpRuntime(
        profile=mode_mcp_profile(mode_name) if profile == "auto" else profile,
        config_path=config_path,
        enabled=tuple(sorted(servers)),
        unavailable=tuple(unavailable),
    )


def mcp_prompt_context(runtime: McpRuntime) -> str:
    enabled = ", ".join(runtime.enabled) if runtime.enabled else "none"
    unavailable = "; ".join(runtime.unavailable) if runtime.unavailable else "none"
    return f"""Profile: {runtime.profile}
Enabled MCP servers: {enabled}
Unavailable MCP servers: {unavailable}

Tool routing rules:
- Use Serena for semantic code navigation, symbol lookup, references, and targeted source understanding.
- Use GitNexus for call graph, impact analysis, affected-scope checks, execution flows, and cross-file risk mapping.
- Use Context7 only for current library/framework/API behavior when the review depends on external docs.
- Keep all MCP usage read-only. Do not edit files, write files, mutate databases, change services, or run implementation commands.
- Ground findings in supplied context, file paths, symbols, MCP output, or explicit uncertainty.
- If an MCP server is unavailable, state the missing evidence and continue with the supplied context instead of guessing."""


def build_prompt(mode: Mode, request_id: str, context: dict[str, str]) -> str:
    sections = "\n".join(f"## {section}\n- ..." for section in mode.sections)
    lenses = "\n".join(f"- {lens}" for lens in mode.lenses)
    verdicts = " | ".join(mode.verdicts)
    return f"""You are Claude acting as an independent reviewer for Codex.

Mode: {mode.name}
Purpose: {mode.purpose}

Do not edit files. Do not run commands. Do not reveal secrets. Use only the supplied context and read-only MCP tools.
Ground every finding in the plan, changed-file list, repository files you inspect, project docs, or verification output.
Prefer concrete patches/checks over general advice. Separate blockers from optional improvements.

Review in stages:
1. Check the plan/request against the changed-file scope.
2. Inspect the listed repository files and nearby code needed to understand behavior.
3. Check tests and verification evidence against the risk of the change.
4. Return concrete findings and a proposed fix order. Do not implement fixes.

Review lenses:
{lenses}

## Mode Methodology
{context["mode_methodology"]}

## MCP And Tool Routing
{context["mcp_context"]}

Context:

## User Request
{context["user_request"]}

## Codex Current Goal
{context["codex_current_goal"]}

## Project Instructions
{context["agent_instructions"]}

## Plan Or Input
{context["input_text"]}

## Git Status
{context["git_status"]}

## Changed Files
{context["changed_files"]}

## Review Scope
{context["review_scope"]}

## Verification Output
{context["verification_output"]}

Return exactly:

CODEX_CLAUDE_REVIEW_ID: {request_id}

# {mode.title}

## Verdict
One of: {verdicts}

{sections}
"""


def write_settings(runtime_dir: Path) -> Path:
    rendered = SETTINGS_TEMPLATE.read_text(encoding="utf-8").replace("{{CAPTURE_STOP_PATH}}", str(CAPTURE_STOP))
    path = runtime_dir / "claude-settings.json"
    path.write_text(rendered, encoding="utf-8")
    return path


def select_bridge_root(project_root: Path) -> Path:
    preferred = project_root / ".codex" / "claude-bridge"
    fallback = project_root / ".claude-bridge"
    preferred_error: OSError | None = None
    try:
        preferred.mkdir(parents=True, exist_ok=True)
        probe = preferred / ".write-test"
        probe.write_text("ok\n", encoding="utf-8")
        probe.unlink()
        return preferred
    except OSError as exc:
        preferred_error = exc
    try:
        fallback.mkdir(parents=True, exist_ok=True)
        probe = fallback / ".write-test"
        probe.write_text("ok\n", encoding="utf-8")
        probe.unlink()
        return fallback
    except OSError as fallback_error:
        raise RunnerError(
            "Claude Companion could not create a writable bridge root. "
            f"Tried {preferred} ({preferred_error}) and {fallback} ({fallback_error})."
        ) from fallback_error


def tmux_has_session(session: str, project_root: Path) -> bool:
    result = run(["tmux", "has-session", "-t", session], project_root, check=False)
    return result.returncode == 0


def capture_tmux(session: str, project_root: Path, history_lines: int = CAPTURE_HISTORY_LINES) -> str:
    capture = run(["tmux", "capture-pane", "-t", session, "-p", "-S", f"-{history_lines}"], project_root, check=False)
    return capture.stdout if capture.stdout else capture.stderr


def capture_tail(text: str, max_chars: int = 4000) -> str:
    return text[-max_chars:] if text else ""


def review_marker(request_id: str) -> str:
    return f"CODEX_CLAUDE_REVIEW_ID: {request_id}"


def extract_marked_review(request_id: str, text: str) -> str | None:
    marker = review_marker(request_id)
    marker_index = text.rfind(marker)
    if marker_index < 0:
        return None

    review = text[marker_index:]
    lines: list[str] = []
    for line in review.splitlines():
        stripped = line.strip()
        if stripped.startswith("─") or stripped == "❯" or stripped.startswith("Session "):
            break
        lines.append(line.rstrip())

    rendered = "\n".join(lines).strip()
    if marker not in rendered:
        return None
    template_window = rendered[:800]
    if "One of:" in template_window or "\n- ..." in template_window:
        return None
    return rendered + "\n"


def write_fallback_outbox(
    *,
    request_id: str,
    mode: str,
    inbox_path: Path,
    outbox_path: Path,
    metadata_path: Path,
    project_root: Path,
    session: str,
    capture: str,
) -> bool:
    review = extract_marked_review(request_id, capture)
    if not review:
        return False

    outbox_path.parent.mkdir(parents=True, exist_ok=True)
    outbox_path.write_text(review, encoding="utf-8")
    write_json(
        metadata_path,
        {
            "request_id": request_id,
            "review_type": mode,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "session_id": session,
            "transcript_path": None,
            "cwd": str(project_root),
            "markdown_path": str(outbox_path),
            "inbox_path": str(inbox_path),
            "status": "captured_from_tmux_fallback",
        },
    )
    return True


def pane_activity_fingerprint(text: str) -> str:
    ignored_fragments = (
        "Session ",
        "Weekly ",
        "Context ",
        "Max ",
        "Sonnet ",
        "Opus ",
        "Pulse ",
    )
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if any(fragment in stripped for fragment in ignored_fragments):
            continue
        lines.append(stripped)
    return "\n".join(lines)


def classify_tmux_state(text: str) -> str:
    lower = text.lower()
    if "do you want to" in lower or "would you like to" in lower or "press enter to continue" in lower:
        return "awaiting_input"
    if "❯" in text or "> " in text:
        return "prompt_visible"
    if "still thinking" in lower or "thinking with" in lower or "thinking..." in lower:
        return "thinking"
    if "sessionstart:startup hook error" in lower:
        return "startup_hook_warning"
    if "error:" in lower or "failed" in lower:
        return "error_visible"
    return "unknown"


def send_enter_to_tmux(session: str, project_root: Path) -> None:
    run(["tmux", "send-keys", "-t", session, "Enter"], project_root)


def send_to_tmux(session: str, prompt: str, project_root: Path) -> None:
    buffer_name = f"codex-claude-{uuid.uuid4().hex}"
    try:
        subprocess.run(["tmux", "load-buffer", "-b", buffer_name, "-"], input=prompt, text=True, check=True)
        run(["tmux", "paste-buffer", "-b", buffer_name, "-t", session], project_root)
        run(["tmux", "send-keys", "-t", session, "Enter"], project_root)
    finally:
        run(["tmux", "delete-buffer", "-b", buffer_name], project_root, check=False)


def wait_for_claude_prompt(
    *,
    startup_timeout: int,
    poll_interval: float,
    project_root: Path,
    session: str,
) -> MonitorResult:
    started_at = time.monotonic()
    deadline = started_at + startup_timeout
    last_capture = ""
    last_state = "unknown"
    continued_once = False

    while True:
        now = time.monotonic()
        if not tmux_has_session(session, project_root):
            raise RunnerError(
                "Claude tmux session exited before the prompt was ready.\n\n"
                f"Last tmux output:\n{capture_tail(last_capture)}"
            )

        last_capture = capture_tmux(session, project_root)
        last_state = classify_tmux_state(last_capture)
        if last_state == "prompt_visible":
            return MonitorResult(round(now - started_at, 2), "prompt_ready", last_state)

        if last_state == "awaiting_input" and not continued_once:
            send_enter_to_tmux(session, project_root)
            continued_once = True

        if now >= deadline:
            raise RunnerError(
                f"Claude prompt was not ready after {startup_timeout}s; review prompt was not sent.\n"
                f"tmux_state={last_state}\n\n"
                f"Last tmux output:\n{capture_tail(last_capture)}"
            )

        time.sleep(poll_interval)


def start_claude_tmux(
    *,
    session: str,
    project_root: Path,
    claude_bin: str,
    settings_path: Path,
    model: str,
    request_id: str,
    mode: str,
    bridge_root: Path,
    mcp_config_path: Path,
) -> None:
    if tmux_has_session(session, project_root):
        raise RunnerError(f"tmux session already exists: {session}")
    env_prefix = {
        "CODEX_CLAUDE_BRIDGE": "1",
        "CODEX_CLAUDE_BRIDGE_REQUEST_ID": request_id,
        "CODEX_CLAUDE_BRIDGE_PROJECT_ROOT": str(project_root),
        "CODEX_CLAUDE_BRIDGE_ROOT": str(bridge_root),
        "CODEX_CLAUDE_BRIDGE_MODE": mode,
    }
    exports = " ".join(f"{key}={shlex.quote(value)}" for key, value in env_prefix.items())
    command = (
        f"{exports} {shlex.quote(claude_bin)} "
        f"--no-chrome --settings {shlex.quote(str(settings_path))} --model {shlex.quote(model)} "
        f"--mcp-config {shlex.quote(str(mcp_config_path))} --strict-mcp-config "
        f"--tools default --disallowedTools {shlex.quote('Edit,Write,MultiEdit,NotebookEdit,Bash')}"
    )
    result = run(["tmux", "new-session", "-d", "-s", session, "-c", str(project_root), "sh", "-lc", command], project_root, check=False)
    if result.returncode != 0:
        raise RunnerError(result.stderr.strip() or "failed to start Claude tmux session")


def wait_for_review_output(
    path: Path,
    *,
    request_id: str,
    mode: str,
    inbox_path: Path,
    metadata_path: Path,
    max_timeout: int,
    idle_timeout: int,
    poll_interval: float,
    project_root: Path,
    session: str,
) -> MonitorResult:
    started_at = time.monotonic()
    deadline = None if max_timeout <= 0 else started_at + max_timeout
    last_activity_at = started_at
    last_fingerprint = ""
    last_capture = ""
    last_state = "unknown"

    while True:
        now = time.monotonic()
        if path.exists():
            return MonitorResult(round(now - started_at, 2), "outbox_created", last_state)

        session_alive = tmux_has_session(session, project_root)
        if not session_alive:
            if write_fallback_outbox(
                request_id=request_id,
                mode=mode,
                inbox_path=inbox_path,
                outbox_path=path,
                metadata_path=metadata_path,
                project_root=project_root,
                session=session,
                capture=last_capture,
            ):
                return MonitorResult(round(now - started_at, 2), "outbox_captured_from_tmux_after_session_exit", last_state)
            if path.exists():
                return MonitorResult(round(now - started_at, 2), "outbox_created_after_session_exit", last_state)
            raise RunnerError(
                f"Claude tmux session exited before producing review output: {path}\n\n"
                f"Last tmux output:\n{capture_tail(last_capture)}"
            )

        last_capture = capture_tmux(session, project_root)
        last_state = classify_tmux_state(last_capture)
        if write_fallback_outbox(
            request_id=request_id,
            mode=mode,
            inbox_path=inbox_path,
            outbox_path=path,
            metadata_path=metadata_path,
            project_root=project_root,
            session=session,
            capture=last_capture,
        ):
            return MonitorResult(round(now - started_at, 2), "outbox_captured_from_tmux", last_state)

        fingerprint = pane_activity_fingerprint(last_capture)
        if fingerprint and fingerprint != last_fingerprint:
            last_fingerprint = fingerprint
            last_activity_at = now

        if deadline is not None and now >= deadline:
            raise RunnerError(
                f"timed out waiting for Claude review output after {max_timeout}s: {path}\n"
                f"tmux_state={last_state}; idle_for={round(now - last_activity_at, 1)}s\n\n"
                f"Last tmux output:\n{capture_tail(last_capture)}"
            )

        idle_expired = idle_timeout > 0 and (now - last_activity_at) >= idle_timeout
        if idle_expired and last_state not in {"thinking"}:
            raise RunnerError(
                f"Claude appears idle while waiting for review output: {path}\n"
                f"tmux_state={last_state}; idle_for={round(now - last_activity_at, 1)}s\n\n"
                f"Last tmux output:\n{capture_tail(last_capture)}"
            )

        time.sleep(poll_interval)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an interactive Claude Code review through tmux.")
    parser.add_argument("--mode", required=True, choices=sorted(MODES))
    parser.add_argument("--prompt", default="", help="User request or review instruction")
    parser.add_argument("--input", help="Plan/input file to include")
    parser.add_argument("--verification-file", help="Verification output file to include")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--model", default="auto", help="auto, sonnet, opus, or Claude model name")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="absolute max seconds to wait; use 0 with --wait-forever for no absolute cap")
    parser.add_argument("--idle-timeout", type=int, default=DEFAULT_IDLE_TIMEOUT_SECONDS, help="seconds without meaningful tmux activity before failing; 0 disables idle timeout")
    parser.add_argument("--poll-interval", type=float, default=DEFAULT_POLL_INTERVAL_SECONDS, help="seconds between outbox/tmux checks")
    parser.add_argument("--startup-timeout", type=int, default=DEFAULT_STARTUP_TIMEOUT_SECONDS, help="seconds to wait for Claude's interactive prompt before sending the review")
    parser.add_argument("--wait-forever", action="store_true", help="disable the absolute timeout and rely on idle/session/outbox monitoring")
    parser.add_argument("--mcp-profile", choices=("auto", "none", "plan", "code", "data", "docs"), default="auto", help="trimmed MCP profile for this Claude review session")
    parser.add_argument("--keep-session-on-failure", action="store_true")
    parser.add_argument("--force", action="store_true", help="start a fresh Claude review even if an identical completed or in-flight review exists")
    parser.add_argument("--json", action="store_true", help="Print machine-readable result only")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    project_root = Path(args.project_root).resolve()
    mode = MODES[args.mode]
    request_id = f"{args.mode}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"
    session = f"codex-claude-{request_id}"
    review_index_path: Path | None = None

    try:
        claude_bin = discover_claude()
        require_tmux_after_claude()

        bridge_root = select_bridge_root(project_root)
        inbox_dir = bridge_root / "inbox"
        outbox_dir = bridge_root / "outbox"
        requests_dir = bridge_root / "requests"
        runtime_dir = bridge_root / "runtime" / request_id
        for directory in [inbox_dir, outbox_dir, requests_dir, runtime_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        mcp_runtime = build_mcp_runtime(args.mcp_profile, args.mode, runtime_dir)

        input_text = read_optional(args.input, project_root)
        verification_output = read_optional(args.verification_file, project_root)
        changed_files = git_changed_files(project_root)

        context = {
            "user_request": args.prompt or "Not provided",
            "codex_current_goal": args.prompt or f"Run Claude Companion mode {args.mode}",
            "agent_instructions": read_optional("AGENTS.md", project_root) if (project_root / "AGENTS.md").exists() else "Not provided",
            "input_text": input_text,
            "git_status": git_text(project_root, ["status", "--short"]),
            "changed_files": changed_files,
            "review_scope": args.prompt or "Use the changed-file list and plan/input above.",
            "verification_output": verification_output,
            "mcp_context": mcp_prompt_context(mcp_runtime),
            "mode_methodology": mode_methodology(args.mode),
        }
        context = {key: redact(value) for key, value in context.items()}

        model = mode.default_model if args.model == "auto" else args.model
        review_key = review_fingerprint(
            {
                "mode": args.mode,
                "model": model,
                "project_root": str(project_root),
                "mcp": {
                    "profile": mcp_runtime.profile,
                    "enabled": list(mcp_runtime.enabled),
                    "unavailable": list(mcp_runtime.unavailable),
                },
                "context": context,
            }
        )
        review_index_path = requests_dir / f"{review_key}.json"
        prior = None if args.force else load_prior_review(review_index_path)
        if prior and prior.outbox_path.exists():
            result = {
                "ok": True,
                "mode": args.mode,
                "request_id": prior.request_id,
                "model": model,
                "inbox_path": str(prior.inbox_path),
                "outbox_path": str(prior.outbox_path),
                "metadata_path": str(prior.metadata_path),
                "session_closed": not tmux_has_session(prior.session, project_root),
                "reused": True,
                "review_key": review_key,
                "monitor": {
                    "wait_seconds": 0,
                    "exit_reason": "reused_existing_outbox",
                    "tmux_state": "not_checked",
                    "max_timeout": 0 if args.wait_forever else args.timeout,
                    "idle_timeout": args.idle_timeout,
                },
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if prior and tmux_has_session(prior.session, project_root):
            max_timeout = 0 if args.wait_forever else args.timeout
            monitor = wait_for_review_output(
                prior.outbox_path,
                request_id=prior.request_id,
                mode=args.mode,
                inbox_path=prior.inbox_path,
                metadata_path=prior.metadata_path,
                max_timeout=max_timeout,
                idle_timeout=args.idle_timeout,
                poll_interval=args.poll_interval,
                project_root=project_root,
                session=prior.session,
            )
            run(["tmux", "kill-session", "-t", prior.session], project_root, check=False)
            result = {
                "ok": True,
                "mode": args.mode,
                "request_id": prior.request_id,
                "model": model,
                "inbox_path": str(prior.inbox_path),
                "outbox_path": str(prior.outbox_path),
                "metadata_path": str(prior.metadata_path),
                "session_closed": not tmux_has_session(prior.session, project_root),
                "reused": True,
                "review_key": review_key,
                "monitor": {
                    "wait_seconds": monitor.wait_seconds,
                    "exit_reason": f"reused_in_flight_{monitor.exit_reason}",
                    "tmux_state": monitor.tmux_state,
                    "max_timeout": max_timeout,
                    "idle_timeout": args.idle_timeout,
                },
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0

        prompt = build_prompt(mode, request_id, context)

        inbox_path = inbox_dir / f"{request_id}.md"
        prompt_path = runtime_dir / "prompt.md"
        settings_path = write_settings(runtime_dir)
        inbox_path.write_text(prompt, encoding="utf-8")
        prompt_path.write_text(prompt, encoding="utf-8")
        outbox_path = outbox_dir / f"{request_id}.md"
        metadata_path = outbox_dir / f"{request_id}.json"
        write_json(
            review_index_path,
            {
                "review_key": review_key,
                "status": "started",
                "mode": args.mode,
                "request_id": request_id,
                "session": session,
                "inbox_path": str(inbox_path),
                "outbox_path": str(outbox_path),
                "metadata_path": str(metadata_path),
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
        )

        start_claude_tmux(
            session=session,
            project_root=project_root,
            claude_bin=claude_bin,
            settings_path=settings_path,
            model=model,
            request_id=request_id,
            mode=args.mode,
            bridge_root=bridge_root,
            mcp_config_path=mcp_runtime.config_path,
        )
        wait_for_claude_prompt(
            startup_timeout=args.startup_timeout,
            poll_interval=args.poll_interval,
            project_root=project_root,
            session=session,
        )
        send_to_tmux(session, prompt, project_root)

        max_timeout = 0 if args.wait_forever else args.timeout
        monitor = wait_for_review_output(
            outbox_path,
            request_id=request_id,
            mode=args.mode,
            inbox_path=inbox_path,
            metadata_path=metadata_path,
            max_timeout=max_timeout,
            idle_timeout=args.idle_timeout,
            poll_interval=args.poll_interval,
            project_root=project_root,
            session=session,
        )
        run(["tmux", "kill-session", "-t", session], project_root, check=False)
        write_json(
            review_index_path,
            {
                "review_key": review_key,
                "status": "completed",
                "mode": args.mode,
                "request_id": request_id,
                "session": session,
                "inbox_path": str(inbox_path),
                "outbox_path": str(outbox_path),
                "metadata_path": str(metadata_path),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "completed_at": datetime.now(timezone.utc).isoformat(),
            },
        )

        result = {
            "ok": True,
            "mode": args.mode,
            "request_id": request_id,
            "model": model,
            "inbox_path": str(inbox_path),
            "outbox_path": str(outbox_path),
            "metadata_path": str(metadata_path),
            "session_closed": not tmux_has_session(session, project_root),
            "reused": False,
            "review_key": review_key,
            "mcp": {
                "profile": mcp_runtime.profile,
                "config_path": str(mcp_runtime.config_path),
                "enabled": list(mcp_runtime.enabled),
                "unavailable": list(mcp_runtime.unavailable),
                "strict": True,
            },
            "monitor": {
                "wait_seconds": monitor.wait_seconds,
                "exit_reason": monitor.exit_reason,
                "tmux_state": monitor.tmux_state,
                "max_timeout": max_timeout,
                "idle_timeout": args.idle_timeout,
            },
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except RunnerError as exc:
        if "session" in locals() and not args.keep_session_on_failure:
            run(["tmux", "kill-session", "-t", session], project_root, check=False)
        if review_index_path:
            prior = read_json(review_index_path) or {}
            prior.update(
                {
                    "status": "failed",
                    "failed_at": datetime.now(timezone.utc).isoformat(),
                    "error": str(exc),
                }
            )
            write_json(review_index_path, prior)
        payload = {"ok": False, "error": str(exc), "mode": args.mode}
        print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

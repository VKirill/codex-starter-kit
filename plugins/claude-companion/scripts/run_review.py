#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
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
    "diff-review": Mode("diff-review", "Claude Diff Review", "sonnet", "Review a completed diff for bugs and regressions.", ("correctness", "regressions", "data safety", "security", "missing tests"), ("APPROVE", "APPROVE_WITH_FIXES", "NEEDS_WORK"), ("Findings", "Missing Tests", "Regression Risks", "Fix Order")),
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
    "contradiction-finder": Mode("contradiction-finder", "Claude Contradiction Review", "sonnet", "Find conflicts between request, docs, plan, and diff.", ("instruction conflicts", "ambiguity", "resolution"), ("CONSISTENT", "MINOR_CONFLICTS", "CONTRADICTIONS"), ("Contradictions", "Ambiguities", "Patch Recommendations")),
    "user-intent-audit": Mode("user-intent-audit", "Claude User Intent Audit", "sonnet", "Check whether Codex is still solving the user request.", ("alignment", "drift", "realignment"), ("ALIGNED", "PARTIAL_DRIFT", "MISALIGNED"), ("Alignment", "Drift", "Realignment Patch")),
    "prompt-quality-review": Mode("prompt-quality-review", "Claude Prompt Quality Review", "sonnet", "Review prompt/plan executable quality.", ("specificity", "missing inputs", "success criteria", "conflicts"), ("READY", "NEEDS_CLARITY", "NOT_EXECUTABLE"), ("Ambiguous Instructions", "Missing Inputs", "Improved Prompt Patch")),
}


class RunnerError(RuntimeError):
    pass


@dataclass(frozen=True)
class MonitorResult:
    wait_seconds: float
    exit_reason: str
    tmux_state: str


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


def build_prompt(mode: Mode, request_id: str, context: dict[str, str]) -> str:
    sections = "\n".join(f"## {section}\n- ..." for section in mode.sections)
    lenses = "\n".join(f"- {lens}" for lens in mode.lenses)
    verdicts = " | ".join(mode.verdicts)
    return f"""You are Claude acting as an independent reviewer for Codex.

Mode: {mode.name}
Purpose: {mode.purpose}

Do not edit files. Do not run commands. Do not reveal secrets. Use only the supplied context.
Ground every finding in the provided plan, diff, docs, or verification output.
Prefer concrete patches/checks over general advice. Separate blockers from optional improvements.

Review lenses:
{lenses}

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

## Diff Stat
{context["diff_stat"]}

## Diff Patch
{context["diff_patch"]}

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
    if "still thinking" in lower or "thinking with" in lower or "thinking..." in lower:
        return "thinking"
    if "do you want to" in lower or "would you like to" in lower or "press enter to continue" in lower:
        return "awaiting_input"
    if "sessionstart:startup hook error" in lower:
        return "startup_hook_warning"
    if "error:" in lower or "failed" in lower:
        return "error_visible"
    if "❯" in text or "> " in text:
        return "prompt_visible"
    return "unknown"


def send_to_tmux(session: str, prompt: str, project_root: Path) -> None:
    buffer_name = f"codex-claude-{uuid.uuid4().hex}"
    try:
        subprocess.run(["tmux", "load-buffer", "-b", buffer_name, "-"], input=prompt, text=True, check=True)
        run(["tmux", "paste-buffer", "-b", buffer_name, "-t", session], project_root)
        run(["tmux", "send-keys", "-t", session, "Enter"], project_root)
    finally:
        run(["tmux", "delete-buffer", "-b", buffer_name], project_root, check=False)


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
        f"--no-chrome --settings {shlex.quote(str(settings_path))} --model {shlex.quote(model)} --tools ''"
    )
    result = run(["tmux", "new-session", "-d", "-s", session, "-c", str(project_root), "sh", "-lc", command], project_root, check=False)
    if result.returncode != 0:
        raise RunnerError(result.stderr.strip() or "failed to start Claude tmux session")


def wait_for_review_output(
    path: Path,
    *,
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
            if path.exists():
                return MonitorResult(round(now - started_at, 2), "outbox_created_after_session_exit", last_state)
            raise RunnerError(
                f"Claude tmux session exited before producing review output: {path}\n\n"
                f"Last tmux output:\n{capture_tail(last_capture)}"
            )

        last_capture = capture_tmux(session, project_root)
        last_state = classify_tmux_state(last_capture)
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
    parser.add_argument("--wait-forever", action="store_true", help="disable the absolute timeout and rely on idle/session/outbox monitoring")
    parser.add_argument("--no-diff", action="store_true", help="Do not include git diff")
    parser.add_argument("--keep-session-on-failure", action="store_true")
    parser.add_argument("--json", action="store_true", help="Print machine-readable result only")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    project_root = Path(args.project_root).resolve()
    mode = MODES[args.mode]
    request_id = f"{args.mode}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"
    session = f"codex-claude-{request_id}"

    try:
        claude_bin = discover_claude()
        require_tmux_after_claude()

        bridge_root = select_bridge_root(project_root)
        inbox_dir = bridge_root / "inbox"
        outbox_dir = bridge_root / "outbox"
        runtime_dir = bridge_root / "runtime" / request_id
        for directory in [inbox_dir, outbox_dir, runtime_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        input_text = read_optional(args.input, project_root)
        verification_output = read_optional(args.verification_file, project_root)
        diff_patch = "Not included" if args.no_diff else git_text(project_root, ["diff", "--", "."])
        diff_stat = "Not included" if args.no_diff else git_text(project_root, ["diff", "--stat", "--", "."])

        context = {
            "user_request": args.prompt or "Not provided",
            "codex_current_goal": args.prompt or f"Run Claude Companion mode {args.mode}",
            "agent_instructions": read_optional("AGENTS.md", project_root) if (project_root / "AGENTS.md").exists() else "Not provided",
            "input_text": input_text,
            "git_status": git_text(project_root, ["status", "--short"]),
            "diff_stat": diff_stat,
            "diff_patch": diff_patch,
            "verification_output": verification_output,
        }
        context = {key: redact(value) for key, value in context.items()}
        prompt = build_prompt(mode, request_id, context)

        inbox_path = inbox_dir / f"{request_id}.md"
        prompt_path = runtime_dir / "prompt.md"
        settings_path = write_settings(runtime_dir)
        inbox_path.write_text(prompt, encoding="utf-8")
        prompt_path.write_text(prompt, encoding="utf-8")

        model = mode.default_model if args.model == "auto" else args.model
        start_claude_tmux(
            session=session,
            project_root=project_root,
            claude_bin=claude_bin,
            settings_path=settings_path,
            model=model,
            request_id=request_id,
            mode=args.mode,
            bridge_root=bridge_root,
        )
        time.sleep(3)
        send_to_tmux(session, prompt, project_root)

        outbox_path = outbox_dir / f"{request_id}.md"
        metadata_path = outbox_dir / f"{request_id}.json"
        max_timeout = 0 if args.wait_forever else args.timeout
        monitor = wait_for_review_output(
            outbox_path,
            max_timeout=max_timeout,
            idle_timeout=args.idle_timeout,
            poll_interval=args.poll_interval,
            project_root=project_root,
            session=session,
        )
        run(["tmux", "kill-session", "-t", session], project_root, check=False)

        result = {
            "ok": True,
            "mode": args.mode,
            "request_id": request_id,
            "model": model,
            "inbox_path": str(inbox_path),
            "outbox_path": str(outbox_path),
            "metadata_path": str(metadata_path),
            "session_closed": not tmux_has_session(session, project_root),
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
        payload = {"ok": False, "error": str(exc), "mode": args.mode}
        print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import tomllib

root = Path(__file__).resolve().parents[1]
errors = []
for path in sorted((root / "agents").glob("*.toml")):
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}: {exc}")
        continue
    if data.get("name") != path.stem:
        errors.append(f"{path}: name does not match filename")
    for item in data.get("skills", {}).get("config", []):
        skill_path = str(item.get("path", ""))
        if "/.codex/plugins/cache/" in skill_path or "/.codex/skills/.system/" in skill_path:
            errors.append(f"{path}: non-portable skill path {skill_path}")
for path in sorted((root / "skills").glob("*/SKILL.md")):
    text = path.read_text(errors="replace")
    if not text.startswith("---"):
        errors.append(f"{path}: missing YAML frontmatter")
try:
    config = tomllib.loads((root / "templates" / "config.recommended.toml").read_text(encoding="utf-8"))
except Exception as exc:
    errors.append(f"templates/config.recommended.toml: {exc}")
else:
    if not config.get("features", {}).get("hooks"):
        errors.append("templates/config.recommended.toml: hooks feature is not enabled")
    for plugin in ["github@openai-curated", "superpowers@openai-curated"]:
        if not config.get("plugins", {}).get(plugin, {}).get("enabled"):
            errors.append(f"templates/config.recommended.toml: plugin {plugin} is not enabled")
    for server in ["context7", "vue-docs", "nuxt-ui-remote", "nuxt-remote"]:
        if server not in config.get("mcp_servers", {}):
            errors.append(f"templates/config.recommended.toml: missing MCP server {server}")
for hook_name in [
    "block-dangerous-shell.py",
    "handoff-permission-request.py",
    "handoff-post-tool-use.py",
    "handoff-intake-classifier.py",
]:
    try:
        ast.parse((root / "hooks" / hook_name).read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"hooks/{hook_name}: syntax check failed: {exc}")
try:
    hooks_config = json.loads((root / "hooks" / "hooks.template.json").read_text(encoding="utf-8"))
except Exception as exc:
    errors.append(f"hooks/hooks.template.json: {exc}")
else:
    for event in ["PermissionRequest", "UserPromptSubmit", "PreToolUse", "PostToolUse"]:
        if event not in hooks_config.get("hooks", {}):
            errors.append(f"hooks/hooks.template.json: missing {event} hook")
rules_path = root / "rules" / "default.rules"
if not rules_path.exists():
    errors.append("rules/default.rules: missing command approval rules")
else:
    rules_text = rules_path.read_text(encoding="utf-8")
    prefix_rules = re.findall(r"prefix_rule\(pattern=\[(.*?)\]", rules_text)
    if len(prefix_rules) < 100:
        errors.append("rules/default.rules: expected broad read-only command allowlist")
    for unsafe in [
        'pattern=["pnpm", "install"]',
        'pattern=["yarn", "install"]',
        'pattern=["gh", "repo"]',
        'pattern=["kubectl", "apply"]',
        'pattern=["docker", "compose", "up"]',
    ]:
        if unsafe in rules_text:
            errors.append(f"rules/default.rules: unsafe broad allow rule {unsafe}")
if errors:
    print("Validation failed:")
    for err in errors:
        print("-", err)
    raise SystemExit(1)
print("Pack validation passed.")

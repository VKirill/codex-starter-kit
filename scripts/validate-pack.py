#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
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
    for plugin in ["github@openai-curated", "superpowers@openai-curated"]:
        if not config.get("plugins", {}).get(plugin, {}).get("enabled"):
            errors.append(f"templates/config.recommended.toml: plugin {plugin} is not enabled")
    for server in ["context7", "vue-docs", "nuxt-ui-remote", "nuxt-remote"]:
        if server not in config.get("mcp_servers", {}):
            errors.append(f"templates/config.recommended.toml: missing MCP server {server}")
if errors:
    print("Validation failed:")
    for err in errors:
        print("-", err)
    raise SystemExit(1)
print("Pack validation passed.")

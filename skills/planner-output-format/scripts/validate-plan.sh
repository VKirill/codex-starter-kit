#!/usr/bin/env bash
# Validate planner output format
# Usage: bash validate-plan.sh < plan.md
#   OR:  bash validate-plan.sh plan.md
set -euo pipefail

INPUT="${1:-/dev/stdin}"
CONTENT=$(cat "$INPUT")
ERRORS=0

check() {
  local label="$1" pattern="$2"
  if ! echo "$CONTENT" | grep -qP "$pattern"; then
    echo "[FAIL] $label"
    ERRORS=$((ERRORS + 1))
  else
    echo "[OK]   $label"
  fi
}

echo "=== Plan Format Validation ==="

# YAML frontmatter
check "Has YAML frontmatter" "^---"
check "Has complexity field" "^complexity:\s*(low|medium|high)"
check "Has steps_count field" "^steps_count:\s*\d+"

# Steps
check "Has at least one step" "### Step \d+"
check "Steps have agent field" "\*\*agent\*\*:\s*coder"
check "Steps have file field" "\*\*file\*\*:"
check "Steps have content field" "\*\*content\*\*:"
check "Steps have verify_steps" "\*\*verify_steps\*\*:"

# Step IDs
check "Steps have id field" "\*\*id\*\*:"

# Count steps
STEP_COUNT=$(echo "$CONTENT" | grep -cP "^### Step \d+" || true)
DECLARED=$(echo "$CONTENT" | grep -oP "^steps_count:\s*\K\d+" || echo "0")

if [[ "$STEP_COUNT" -ne "$DECLARED" ]]; then
  echo "[FAIL] steps_count=$DECLARED but found $STEP_COUNT steps"
  ERRORS=$((ERRORS + 1))
else
  echo "[OK]   Step count matches ($STEP_COUNT)"
fi

if [[ "$STEP_COUNT" -gt 5 ]]; then
  echo "[WARN] $STEP_COUNT steps — consider splitting task"
fi

echo "==============================="
if [[ $ERRORS -eq 0 ]]; then
  echo "Plan format: VALID"
else
  echo "Plan format: $ERRORS errors found"
  exit 1
fi

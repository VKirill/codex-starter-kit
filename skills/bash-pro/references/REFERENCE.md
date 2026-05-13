# Bash — Project-Specific Reference

<!-- Generated from model knowledge -->
> Project: ai-pipeline | Deploy/health scripts | Generated: 2026-03-10

## Паттерны используемые в проекте

### Strict mode boilerplate

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

# Script directory detection (works even with symlinks)
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

# Cleanup trap
cleanup() {
  # Remove temp files, restore state
  rm -rf -- "${TMPDIR:-}"
}
trap cleanup EXIT
trap 'echo "Error at line $LINENO: exit $?" >&2' ERR
```

### Deploy script паттерн (PM2 + git)

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

APP_NAME="ai-pipeline"
APP_DIR="/home/ubuntu/apps/${APP_NAME}"
PORT=9090

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; }

# Pre-flight checks
check_prereqs() {
  command -v pm2 &>/dev/null || { log "ERROR: pm2 not found"; exit 1; }
  command -v node &>/dev/null || { log "ERROR: node not found"; exit 1; }
  [[ -d "$APP_DIR" ]] || { log "ERROR: $APP_DIR not found"; exit 1; }
}

# Kill stale process on port (PM2 restart gotcha)
kill_port() {
  local pid
  pid=$(lsof -ti :"$PORT" 2>/dev/null || true)
  if [[ -n "$pid" ]]; then
    log "Killing stale process on port $PORT (PID: $pid)"
    kill "$pid" 2>/dev/null || true
    sleep 1
  fi
}

deploy() {
  log "=== Deploy started ==="
  cd "$APP_DIR"

  log "Pulling latest changes..."
  git pull --ff-only origin main

  log "Installing dependencies..."
  npm ci --production=false

  log "Building..."
  npm run build

  log "Restarting PM2..."
  kill_port
  pm2 delete "$APP_NAME" 2>/dev/null || true
  pm2 start ecosystem.config.js
  pm2 save

  log "Waiting for startup..."
  sleep 3

  log "Health check..."
  if curl -sf "http://localhost:${PORT}/healthz" >/dev/null; then
    log "✅ Deploy successful"
  else
    log "❌ Health check failed!"
    pm2 logs "$APP_NAME" --lines 20 --nostream
    exit 1
  fi
}

check_prereqs
deploy
```

### Health check script

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

URL="${1:-http://localhost:9090/healthz}"
TIMEOUT="${2:-10}"
RETRIES="${3:-3}"

for ((i=1; i<=RETRIES; i++)); do
  status=$(curl -sf -o /dev/null -w '%{http_code}' --max-time "$TIMEOUT" "$URL" || echo "000")
  if [[ "$status" == "200" ]]; then
    echo "OK (attempt $i)"
    exit 0
  fi
  echo "Attempt $i/$RETRIES: HTTP $status"
  sleep 2
done

echo "FAILED after $RETRIES attempts"
exit 1
```

## Git операции в bash

### Worktree management

```bash
# Create worktree for task isolation
create_worktree() {
  local repo_dir="$1"
  local branch="$2"
  local worktree_dir="${repo_dir}-worktrees/${branch}"

  if [[ -d "$worktree_dir" ]]; then
    echo "Worktree exists: $worktree_dir"
    return 0
  fi

  git -C "$repo_dir" worktree add "$worktree_dir" -b "$branch" 2>/dev/null \
    || git -C "$repo_dir" worktree add "$worktree_dir" "$branch"

  echo "$worktree_dir"
}

# Cleanup stale worktrees
cleanup_worktrees() {
  local repo_dir="$1"
  git -C "$repo_dir" worktree prune
  git -C "$repo_dir" worktree list | while IFS= read -r line; do
    local wt_dir
    wt_dir=$(echo "$line" | awk '{print $1}')
    if [[ "$wt_dir" == *"-worktrees/"* ]] && ! git -C "$wt_dir" status &>/dev/null; then
      rm -rf -- "$wt_dir"
    fi
  done
}
```

## Argument parsing

```bash
# getopt-based parsing with long options
usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Options:
  -p, --project NAME    Project slug
  -e, --env ENV         Environment (dev|staging|prod)
  -d, --dry-run         Show what would be done
  -v, --verbose         Enable verbose output
  -h, --help            Show this help
EOF
}

PROJECT=""
ENV="dev"
DRY_RUN=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--project) PROJECT="$2"; shift 2 ;;
    -e|--env)     ENV="$2"; shift 2 ;;
    -d|--dry-run) DRY_RUN=true; shift ;;
    -v|--verbose) VERBOSE=true; shift ;;
    -h|--help)    usage; exit 0 ;;
    --)           shift; break ;;
    -*)           echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
    *)            break ;;
  esac
done

: "${PROJECT:?--project is required}"
```

## Logging и error handling

```bash
# Structured logging with levels
readonly LOG_LEVELS=([0]="ERROR" [1]="WARN" [2]="INFO" [3]="DEBUG")
LOG_LEVEL=2  # Default: INFO

log() {
  local level="${1:-2}"
  shift
  if (( level <= LOG_LEVEL )); then
    printf '[%s] [%s] %s\n' \
      "$(date '+%Y-%m-%d %H:%M:%S')" \
      "${LOG_LEVELS[$level]}" \
      "$*" >&2
  fi
}

log_error() { log 0 "$@"; }
log_warn()  { log 1 "$@"; }
log_info()  { log 2 "$@"; }
log_debug() { log 3 "$@"; }

# Error trap with context
on_error() {
  local exit_code=$?
  local line_no=$1
  log_error "Script failed at line $line_no (exit code: $exit_code)"
  log_error "Command: ${BASH_COMMAND}"
}
trap 'on_error $LINENO' ERR
```

## Safe file operations

```bash
# Atomic file write (write to temp, then move)
atomic_write() {
  local target="$1"
  local content="$2"
  local tmp
  tmp=$(mktemp "${target}.XXXXXX")
  printf '%s' "$content" > "$tmp"
  mv -f -- "$tmp" "$target"
}

# Backup before edit
backup_config() {
  local file="$1"
  local backup="${file}.bak.$(date +%s)"
  cp -- "$file" "$backup"
  echo "Backed up: $backup"
}

# Safe temp directory
TMPDIR=$(mktemp -d)
trap 'rm -rf -- "$TMPDIR"' EXIT
```

## Process management helpers

```bash
# Wait for port to become available
wait_for_port() {
  local port="$1"
  local timeout="${2:-30}"
  local elapsed=0

  while ! ss -tlnp | grep -q ":${port} "; do
    if (( elapsed >= timeout )); then
      echo "Timeout waiting for port $port" >&2
      return 1
    fi
    sleep 1
    ((elapsed++))
  done
}

# Check if process is running by PID file
is_running() {
  local pidfile="$1"
  [[ -f "$pidfile" ]] && kill -0 "$(cat "$pidfile")" 2>/dev/null
}

# Service status check
check_service() {
  local svc="$1"
  if systemctl is-active --quiet "$svc"; then
    echo "✅ $svc: running"
  else
    echo "❌ $svc: stopped"
    return 1
  fi
}
```

## Cron и automation

```bash
# Cron-safe script header
exec 200>/var/lock/my-script.lock
flock -n 200 || { echo "Already running"; exit 0; }

# Redirect all output to log
exec >> /var/log/my-script.log 2>&1

# Timestamp
echo "=== Run: $(date -Iseconds) ==="
```

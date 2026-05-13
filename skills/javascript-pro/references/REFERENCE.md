# Node.js / JavaScript — Project-Specific Reference

<!-- Generated from model knowledge -->
> Project: ai-pipeline | Node.js 22+ ESM | Generated: 2026-03-10

## Паттерны используемые в проекте

### ESM модули (type: "module")

```javascript
// package.json: "type": "module"
// All imports use ESM syntax with .js suffix

// Node built-ins — use node: prefix
import { readFile, writeFile } from 'node:fs/promises';
import { readFileSync, existsSync, mkdirSync } from 'node:fs';
import { join, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'module';
import type { Server } from 'node:http';

// Dynamic import for conditional loading
const { execSync } = await import('node:child_process');
```

### AsyncLocalStorage для контекстного логирования

```typescript
import { AsyncLocalStorage } from 'node:async_hooks';

interface LogContext {
  taskId?: string;
  sessionId?: string;
  phase?: string;
}

const asyncStorage = new AsyncLocalStorage<LogContext>();

// Set context for an async operation scope
function runWithContext<T>(ctx: LogContext, fn: () => Promise<T>): Promise<T> {
  return asyncStorage.run(ctx, fn);
}

// Read context in any nested call
function getLogContext(): LogContext {
  return asyncStorage.getStore() ?? {};
}

// Usage — all logs within scope automatically get taskId
await runWithContext({ taskId: 'TASK-42' }, async () => {
  log('Starting work');  // log reads taskId from AsyncLocalStorage
  await doSomething();
  log('Done');
});
```

## Async паттерны проекта

### Promise с timeout

```typescript
// Timeout wrapper — used for agent calls and external ops
function withTimeout<T>(promise: Promise<T>, ms: number, label = ''): Promise<T> {
  return new Promise<T>((resolve, reject) => {
    const timer = setTimeout(
      () => reject(new Error(`Timeout ${label} after ${ms}ms`)),
      ms,
    );
    promise
      .then((v) => { clearTimeout(timer); resolve(v); })
      .catch((e) => { clearTimeout(timer); reject(e); });
  });
}

// Usage
const result = await withTimeout(
  queryAgent(prompt),
  120_000,
  'agent-query',
);
```

### Controlled concurrency

```typescript
// Process tasks with max concurrency (no external lib needed)
async function processWithConcurrency<T, R>(
  items: T[],
  fn: (item: T) => Promise<R>,
  maxConcurrent: number,
): Promise<R[]> {
  const results: R[] = [];
  const executing = new Set<Promise<void>>();

  for (const item of items) {
    const p = fn(item).then((r) => { results.push(r); });
    executing.add(p);
    p.finally(() => executing.delete(p));

    if (executing.size >= maxConcurrent) {
      await Promise.race(executing);
    }
  }

  await Promise.all(executing);
  return results;
}
```

### Graceful shutdown

```typescript
import { setShuttingDown, isShuttingDown } from './core/shutdown.js';

let httpServer: Server | undefined;

async function shutdown(signal: string): Promise<void> {
  if (isShuttingDown()) return;
  setShuttingDown(true);
  log(`[Shutdown] ${signal} received`);

  // 1. Stop accepting new work
  httpServer?.close();

  // 2. Wait for running tasks (with hard timeout)
  const waitPromise = waitForRunningTasks();
  const hardTimeout = new Promise<void>((resolve) =>
    setTimeout(resolve, 120_000),
  );
  await Promise.race([waitPromise, hardTimeout]);

  // 3. Cleanup resources
  await closeRedis();
  await closeEventsPool();

  // 4. Force exit if still alive
  setTimeout(() => process.exit(1), 5000);
  process.exit(0);
}

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));
process.on('uncaughtException', (err) => {
  logError('[Fatal]', err);
  process.exit(1);
});
```

## Event Loop и таймеры

### Polling loop с backoff

```typescript
// Main pipeline loop pattern
const MIN_INTERVAL_MS = 5_000;

async function mainLoop(): Promise<void> {
  while (!isShuttingDown()) {
    const start = Date.now();
    try {
      await pollAndProcess();
    } catch (err) {
      logError('[Loop] Error', err);
      await new Promise((r) => setTimeout(r, 5000)); // backoff on error
    }
    const elapsed = Date.now() - start;
    if (elapsed < MIN_INTERVAL_MS) {
      await new Promise((r) => setTimeout(r, MIN_INTERVAL_MS - elapsed));
    }
  }
}
```

### Heartbeat с setInterval

```typescript
// Heartbeat for long-running tasks
function startHeartbeat(taskId: string, intervalMs = 30_000): () => void {
  const timer = setInterval(() => {
    updateHeartbeat(taskId).catch(() => {});  // fire-and-forget
  }, intervalMs);

  // Return cleanup function
  return () => clearInterval(timer);
}

// Usage
const stopHeartbeat = startHeartbeat(task.id);
try {
  await executeTask(task);
} finally {
  stopHeartbeat();
}
```

## Process и ресурсы

### Memory monitoring

```typescript
function getMemoryUsage(): { heapMB: number; rssMB: number; external: number } {
  const mem = process.memoryUsage();
  return {
    heapMB: Math.round(mem.heapUsed / 1024 / 1024),
    rssMB: Math.round(mem.rss / 1024 / 1024),
    external: Math.round(mem.external / 1024 / 1024),
  };
}

// Health check pattern
function isHealthy(): { ok: boolean; details: Record<string, unknown> } {
  const mem = getMemoryUsage();
  const uptime = process.uptime();
  return {
    ok: mem.heapMB < 1024,  // under 1GB heap
    details: { mem, uptime, pid: process.pid, nodeVersion: process.version },
  };
}
```

### Environment variables с fallback

```typescript
// Pattern from project's config.ts
function envInt(name: string, fallback: number): number {
  const val = process.env[name];
  if (!val) return fallback;
  const num = parseInt(val, 10);
  return Number.isNaN(num) ? fallback : num;
}

function envStr(name: string, fallback: string): string {
  return process.env[name] || fallback;
}

// Usage
export const GLOBAL_MAX_CONCURRENT = envInt('MAX_CONCURRENT', 3);
export const PROJECT_DIR = process.env.PROJECT_DIR || process.cwd();
export const NODE_ENV = process.env.NODE_ENV || 'development';
```

## File system операции

### Sync vs Async выбор

```typescript
// Sync — for startup/config loading (blocking OK at init)
import { readFileSync, existsSync, mkdirSync } from 'node:fs';

if (!existsSync(logsDir)) {
  mkdirSync(logsDir, { recursive: true });
}
const config = JSON.parse(readFileSync(configPath, 'utf-8'));

// Async — for runtime operations (non-blocking)
import { readFile, writeFile, mkdir } from 'node:fs/promises';

await mkdir(outputDir, { recursive: true });
const data = await readFile(filePath, 'utf-8');
await writeFile(outputPath, JSON.stringify(result, null, 2));
```

### Structured JSON logging

```typescript
// Append-only log file (sync for reliability in error paths)
import { appendFileSync } from 'node:fs';

function logToFile(level: string, message: string, meta?: object): void {
  const entry = JSON.stringify({
    ts: new Date().toISOString(),
    level,
    msg: message,
    ...meta,
  });
  appendFileSync(logFilePath, entry + '\n');
}
```

## Child process для git/shell

```typescript
import { execSync, spawn } from 'node:child_process';

// Sync — quick git commands
function gitCurrentBranch(cwd: string): string {
  return execSync('git rev-parse --abbrev-ref HEAD', {
    cwd,
    encoding: 'utf-8',
    timeout: 10_000,
  }).trim();
}

// Async with spawn — long-running commands
function runCommand(cmd: string, args: string[], cwd: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const proc = spawn(cmd, args, { cwd, stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '';
    let stderr = '';
    proc.stdout.on('data', (d) => { stdout += d; });
    proc.stderr.on('data', (d) => { stderr += d; });
    proc.on('close', (code) => {
      if (code === 0) resolve(stdout.trim());
      else reject(new Error(`${cmd} exited ${code}: ${stderr}`));
    });
  });
}
```

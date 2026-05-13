# ioredis — Project-Specific Reference

> Source: github.com/redis/ioredis | Project: ai-pipeline | Generated: 2026-03-04

## Singleton connection — паттерн проекта (redis.ts)

Pipeline использует lazy singleton с `getRedis()` — единственная точка доступа к Redis.

```typescript
import { Redis } from 'ioredis';

let _redis: Redis | null = null;

export function getRedis(): Redis {
  if (!_redis) {
    _redis = new Redis({
      host: '127.0.0.1',
      port: 6379,
      password: REDIS_PASSWORD,           // from config.ts env var
      maxRetriesPerRequest: 3,            // flush pending after 3 retries
      retryStrategy(times: number) {
        return Math.min(times * 500, 5000); // 500ms, 1s, 1.5s, ... max 5s
      },
    });

    // MANDATORY: error handler prevents unhandled rejection crash
    _redis.on('error', (err: Error) => {
      console.error('[redis] Connection error:', err.message);
    });
  }
  return _redis;
}
```

### Connection options — когда какие значения

```typescript
interface RedisOptions {
  host: string;                    // default: '127.0.0.1'
  port: number;                    // default: 6379
  password: string;                // AUTH password
  db: number;                      // database index (default: 0)
  maxRetriesPerRequest: number | null;
  // 3 = flush pending commands after 3 reconnect attempts (pipeline default)
  // null = never flush, commands wait forever (use for BLPOP consumers)
  // 20 = ioredis default

  retryStrategy: (times: number) => number | void | null;
  // return ms delay before next reconnect attempt
  // return null/void = stop retrying
  // pipeline: exponential backoff capped at 5s

  lazyConnect: boolean;            // false = connect immediately (pipeline default)
  // true = connect on first command (useful for optional Redis)

  connectionName: string;          // CLIENT SETNAME — visible in CLIENT LIST
  // pipeline could use: 'ai-pipeline-consumer'

  autoResendUnfulfilledCommands: boolean;  // default: true
  // resend BLPOP etc after reconnect — keep true for consumers
}
```

## BLPOP wake queue — основной паттерн pipeline

Redis используется как wake-up queue: CRM webhook → LPUSH → pipeline BLPOP.

```typescript
// Consumer side — block-wait for wake signal
export async function waitForWake(timeoutSeconds: number = 30): Promise<string | null> {
  const redis = getRedis();
  try {
    const result = await redis.blpop(REDIS_QUEUE, timeoutSeconds);
    // result: [key, value] | null (timeout)
    if (result) {
      return result[1]; // value part
    }
    return null;
  } catch {
    return null; // connection error — treat as timeout
  }
}

// Producer side — push wake signal
export async function pushWake(value: string = 'wake'): Promise<void> {
  const redis = getRedis();
  await redis.lpush(REDIS_QUEUE, value);
}
```

### BLPOP — детали API

```typescript
// Signature: redis.blpop(key1, [key2, ...], timeout) → Promise<[string, string] | null>
// timeout in SECONDS (not ms!)
// Returns: [keyName, poppedValue] or null on timeout

// Multiple keys — pops from first non-empty
const result = await redis.blpop('high-priority', 'low-priority', 10);

// IMPORTANT: maxRetriesPerRequest для BLPOP consumers
// Если maxRetriesPerRequest = 3 (default), при reconnect BLPOP получит
// MaxRetriesPerRequestError. Для dedicated consumer → set null.
// Pipeline использует maxRetriesPerRequest: 3 т.к. BLPOP обёрнут в try/catch.
```

## Drain queue — prevent rapid looping

```typescript
// After processing tasks, drain remaining signals to prevent re-processing
export async function drainWakeQueue(): Promise<number> {
  const redis = getRedis();
  let drained = 0;
  try {
    while (true) {
      const result = await redis.lpop(REDIS_QUEUE);  // non-blocking pop
      if (!result) break;
      drained++;
      if (drained >= 100) break;  // safety cap
    }
  } catch {
    // Non-critical — silently ignore
  }
  return drained;
}
```

## Graceful shutdown — quit() vs disconnect()

```typescript
// quit() — send QUIT command, wait for pending commands, close connection
export async function closeRedis(): Promise<void> {
  if (_redis) {
    await _redis.quit();  // graceful — flushes pending commands
    _redis = null;
  }
}

// disconnect() — immediate close, drops pending commands
// Use only for emergency/force shutdown
redis.disconnect();

// Pipeline integration with PM2 SIGTERM:
process.on('SIGTERM', async () => {
  await Promise.allSettled([closeRedis(), closeEventsPool()]);
  process.exit(0);
});
```

## Pipeline — batch multiple commands

```typescript
// pipeline() — send multiple commands in one round-trip (non-atomic)
const pipe = redis.pipeline();
pipe.set('key1', 'value1');
pipe.set('key2', 'value2');
pipe.get('key1');
const results = await pipe.exec();
// results: [[null, 'OK'], [null, 'OK'], [null, 'value1']]
// Each: [error, result]

// multi() — atomic transaction (all-or-nothing)
const tx = redis.multi();
tx.incr('counter');
tx.lpush('events', JSON.stringify({ type: 'task_complete', ts: Date.now() }));
tx.expire('events', 86400);
const txResults = await tx.exec();
// txResults: [[null, 1], [null, 5], [null, 1]]
```

## Cache-aside — паттерн для pipeline

```typescript
// Cache с fallback в PostgreSQL — типичный паттерн для pipeline
async function getCachedOrFetch<T>(
  key: string,
  ttlSeconds: number,
  fetcher: () => Promise<T>,
): Promise<T> {
  const redis = getRedis();

  // Try cache first
  const cached = await redis.get(key);
  if (cached) {
    return JSON.parse(cached) as T;
  }

  // Fallback to source
  const data = await fetcher();

  // Store in cache (fire-and-forget)
  redis.set(key, JSON.stringify(data), 'EX', ttlSeconds).catch(() => {});

  return data;
}

// Usage:
const project = await getCachedOrFetch(
  `pipeline:project:${slug}`,
  300,  // 5 min TTL
  () => fetchProjectBySlug(slug),
);
```

## Key naming conventions

```typescript
// Pattern: scope:entity[:id]
const PATTERNS = {
  queue:   'pipeline:wake',                    // BLPOP wake queue
  cache:   'pipeline:project:{slug}',          // project config cache
  lock:    'pipeline:lock:task:{taskId}',       // distributed lock
  counter: 'pipeline:stats:tasks_processed',   // metrics counter
  ttl:     'pipeline:rate:{agentName}:{window}', // rate limiting
};

// ALWAYS set TTL on SET (except queue keys):
await redis.set(key, value, 'EX', 3600);  // 1 hour
await redis.setex(key, 3600, value);       // equivalent
```

## Distributed lock — SET NX EX pattern

```typescript
// Acquire lock — atomic SET if Not eXists with EXpiry
async function acquireLock(lockKey: string, ttlSeconds: number = 60): Promise<string | null> {
  const redis = getRedis();
  const lockValue = crypto.randomUUID();  // unique per holder

  const result = await redis.set(lockKey, lockValue, 'EX', ttlSeconds, 'NX');
  return result === 'OK' ? lockValue : null;
}

// Release lock — safe release via Lua (only if we own it)
async function releaseLock(lockKey: string, lockValue: string): Promise<boolean> {
  const redis = getRedis();
  const lua = `
    if redis.call('get', KEYS[1]) == ARGV[1] then
      return redis.call('del', KEYS[1])
    else
      return 0
    end
  `;
  const result = await redis.eval(lua, 1, lockKey, lockValue);
  return result === 1;
}

// Usage:
const lockId = await acquireLock(`pipeline:lock:task:${taskId}`, 300);
if (!lockId) throw new Error('Task already being processed');
try {
  await processTask(task);
} finally {
  await releaseLock(`pipeline:lock:task:${taskId}`, lockId);
}
```

## Lua scripts — defineCommand pattern

```typescript
// Define custom command (auto EVALSHA with fallback to EVAL)
const redis = getRedis();

redis.defineCommand('rateLimit', {
  numberOfKeys: 1,
  lua: `
    local current = redis.call('incr', KEYS[1])
    if current == 1 then
      redis.call('expire', KEYS[1], ARGV[1])
    end
    return current
  `,
});

// Usage — TypeScript type assertion needed
const count = await (redis as any).rateLimit('pipeline:rate:coder:60', '60');
if (count > 10) throw new Error('Rate limit exceeded');
```

## Event handlers — production checklist

```typescript
const redis = new Redis(options);

// MANDATORY — prevents unhandled rejection crash
redis.on('error', (err: Error) => {
  console.error('[redis] Error:', err.message);
  // Don't throw — ioredis will retry automatically
});

// RECOMMENDED — lifecycle logging for PM2 diagnostics
redis.on('ready', () => {
  console.log('[redis] Connected and ready');
});

redis.on('reconnecting', (ms: number) => {
  console.log(`[redis] Reconnecting in ${ms}ms`);
});

redis.on('close', () => {
  console.log('[redis] Connection closed');
});

// For Pub/Sub (if pipeline uses it):
redis.on('message', (channel: string, message: string) => {
  // handle published messages
});
```

## TypeScript типы

```typescript
import { Redis, RedisOptions } from 'ioredis';

// Redis instance type
let client: Redis;

// Options type (partial — most have defaults)
const opts: RedisOptions = {
  host: '127.0.0.1',
  port: 6379,
  password: process.env.REDIS_PASSWORD,
  maxRetriesPerRequest: 3,
};

// Command return types
const str: string | null = await redis.get('key');         // GET → string | null
const num: number = await redis.lpush('list', 'val');      // LPUSH → length
const arr: [string, string] | null = await redis.blpop('q', 30); // BLPOP → [key, val] | null
const ok: 'OK' | null = await redis.set('k', 'v', 'EX', 60, 'NX'); // SET NX → 'OK' | null
const deleted: number = await redis.del('key1', 'key2');   // DEL → count
```

## Тестирование — mock pattern

```typescript
// vi.mock for unit tests (vitest/jest)
import { vi } from 'vitest';

vi.mock('ioredis', () => {
  const mockRedis = {
    get: vi.fn().mockResolvedValue(null),
    set: vi.fn().mockResolvedValue('OK'),
    del: vi.fn().mockResolvedValue(1),
    blpop: vi.fn().mockResolvedValue(['pipeline:wake', 'wake']),
    lpush: vi.fn().mockResolvedValue(1),
    lpop: vi.fn().mockResolvedValue(null),
    quit: vi.fn().mockResolvedValue('OK'),
    on: vi.fn(),
    pipeline: vi.fn(() => ({
      set: vi.fn().returnsThis(),
      get: vi.fn().returnsThis(),
      exec: vi.fn().mockResolvedValue([]),
    })),
  };
  return { Redis: vi.fn(() => mockRedis), default: { Redis: vi.fn(() => mockRedis) } };
});
```

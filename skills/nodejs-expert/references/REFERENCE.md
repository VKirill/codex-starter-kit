# Node.js 20+ — Project-Specific Reference

> Source: Node.js docs + project codebase | Project: mycolormemory | Generated: 2026-03-15

---

## Graceful Shutdown — PM2 + Multi-Service

Правильный порядок: BullMQ workers → HTTP server → bot polling → exit.
Никогда не делай `process.exit()` до `server.close()` — активные соединения упадут.

```ts
// src/app/index.ts
const shutdown = async () => {
  logger.info('Shutting down');

  // 1. Останавливаем workers (BullMQ closes Redis connections internally)
  stopNotificationWorker();
  stopAnalyticsSender();
  stopRestorationWorker();
  stopAnimationWorker();

  // 2. Закрываем HTTP-сервер (ждём завершения in-flight requests)
  await server.close();

  // 3. Останавливаем bot polling
  bot.stop();

  process.exit(0);
};

// process.once гарантирует однократное срабатывание (защита от двойного сигнала)
process.once('SIGINT', shutdown);
process.once('SIGTERM', shutdown);
```

Worker — паттерн singleton с идемпотентным stop:

```ts
let analyticsInterval: NodeJS.Timeout | null = null;

export function startAnalyticsSender(): void {
  if (analyticsInterval) return; // идемпотентный запуск
  // ...
  analyticsInterval = setInterval(() => { ... }, 30 * 60 * 1000);
}

export function stopAnalyticsSender(): void {
  if (analyticsInterval) {
    clearInterval(analyticsInterval);
    analyticsInterval = null; // сброс → следующий start создаст заново
    logger.info('Analytics sender stopped');
  }
}
```

---

## Process Error Handling — Startup & Runtime

Startup validation: падай быстро с exit code 1, не молчи.

```ts
// src/app/index.ts — правильная последовательность startup
async function main() {
  // 1. Первый — env validation (Zod), до любых соединений
  try {
    getEnv();
  } catch (error) {
    logger.error('Environment validation failed', sanitizeError(error));
    process.exit(1); // PM2 не перезапустит если exit_code=1 и max_restarts исчерпан
  }

  // 2. Создание сервисов — каждый в отдельном try/catch
  let server;
  try {
    server = await createServer();
  } catch (error) {
    logger.error('Failed to create server', sanitizeError(error));
    process.exit(1);
  }

  // 3. Специфичные ошибки порта — информативный вывод
  try {
    await server.listen({ port: PORT, host: '127.0.0.1' });
  } catch (error: any) {
    logger.error('Failed to start server', { port: PORT, error: sanitizeError(error) });
    if (error.code === 'EADDRINUSE') {
      logger.error(`Port ${PORT} is already in use`);
    }
    process.exit(1);
  }
}

main().catch((error) => {
  logger.error('Failed to start', sanitizeError(error));
  process.exit(1);
});
```

Для runtime необработанных ошибок — не используем в проекте напрямую, но PM2 ловит крэши и перезапускает.
Если добавляешь: логируй и дай процессу упасть (no swallowing).

```ts
// Только если очень нужно — например для Sentry flush перед смертью
process.on('uncaughtException', (error) => {
  logger.error('Uncaught exception', sanitizeError(error));
  process.exit(1); // ОБЯЗАТЕЛЬНО — продолжать в undefined state опасно
});

process.on('unhandledRejection', (reason) => {
  logger.error('Unhandled rejection', sanitizeError(reason instanceof Error ? reason : new Error(String(reason))));
  process.exit(1);
});
```

---

## Promise Patterns — Parallel & Resilient

`Promise.all` — все обязательны, первый fail = отмена:

```ts
// src/features/profile/services/profile.service.ts
// Использовать когда: оба результата нужны, любой failure = ошибка всей операции
const [animations, restorations] = await Promise.all([
  animationRepository.findByUserId(userId),
  restorationRepository.findByUserId(userId),
]);
```

`Promise.allSettled` — независимые операции, failures не блокируют:

```ts
// src/features/analytics/jobs/analytics-sender.job.ts
// Использовать когда: отправка в Yandex и GA независимы, один failure не блокирует другой
const promises: Promise<void>[] = [];
if (!event.yandexSent && user.yandexClientId) promises.push(sendToYandex(...));
if (!event.gaSent && user.gaClientId) promises.push(sendToGA(...));

await Promise.allSettled(promises); // оба запроса выполняются независимо
```

Когда что использовать:

| Метод | Когда | Поведение при ошибке |
|---|---|---|
| `Promise.all` | Все результаты нужны вместе | Отмена при первом reject |
| `Promise.allSettled` | Независимые side effects | Продолжает, возвращает статус каждого |
| `Promise.race` | Timeout / первый выигрывает | Первый settled (fulfilled или rejected) |

---

## Buffer & Binary Data — AI Image/Video

```ts
// src/features/animation/services/animation.service.ts
// Response → Buffer для передачи в Telegram или записи на диск
const imageBuffer = Buffer.from(await imageResponse.arrayBuffer());
const videoBuffer = Buffer.from(await videoResponse.arrayBuffer());

// src/shared/lib/kie/client.ts
// base64 → Buffer (AI API возвращает base64-encoded image)
const imageBuffer = Buffer.from(base64Image, 'base64');

// src/shared/lib/verification-token/token.service.ts
// Timing-safe comparison для HMAC (защита от timing attacks)
if (!crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expectedSignature))) {
  throw new Error('Invalid signature');
}
```

Для больших файлов (>10MB) — используй streams вместо Buffer (не блокируй event loop):

```ts
import { pipeline } from 'stream/promises';
import { createWriteStream } from 'fs';

// В проекте не используется, но паттерн для будущих задач с большими видео
const response = await fetch(url);
if (!response.body) throw new Error('No response body');
await pipeline(
  response.body as unknown as NodeJS.ReadableStream,
  createWriteStream(filePath)
);
```

---

## fs/promises — File Operations

```ts
// src/app/server.ts
import { readFile, mkdir } from 'fs/promises';

// SSL certs при старте
const sslOptions = {
  key: await readFile(env.SSL_KEY_PATH),
  cert: await readFile(env.SSL_CERT_PATH),
};

// Создание директорий перед записью файлов
await mkdir(restorationsDir, { recursive: true }); // recursive: true — не падает если уже есть
await mkdir(animationsDir, { recursive: true });

// Чтение HTML-шаблонов
const html = await readFile(htmlPath, 'utf-8');
```

```ts
// src/features/restoration/services/restoration.service.ts
// Динамический import fs/promises внутри метода (lazy — не грузим при старте)
const fs = await import('fs/promises');
await fs.mkdir(publicDir, { recursive: true });
await fs.writeFile(filePath, imageBuffer); // imageBuffer: Buffer

// Паттерн пути для публичных файлов
import { join } from 'path';
const publicDir = join(process.cwd(), 'public', 'restorations');
const filePath = join(publicDir, `${jobId}.jpg`);
```

---

## AbortController — Timeouts для AI Calls

В проекте пока не используется — но критично для AI generation (могут висеть 30-120s).

```ts
// Паттерн таймаута для AI API calls (добавить в retryWithBackoff или AI clients)
export async function fetchWithTimeout(url: string, options: RequestInit, timeoutMs: number) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, { ...options, signal: controller.signal });
    return response;
  } catch (error: any) {
    if (error.name === 'AbortError') {
      throw new Error(`Request timed out after ${timeoutMs}ms: ${url}`);
    }
    throw error;
  } finally {
    clearTimeout(timeoutId); // ОБЯЗАТЕЛЬНО — иначе утечка таймера
  }
}

// Использование в AI clients
const response = await fetchWithTimeout(
  'https://api.laozhang.ai/...',
  { method: 'POST', body: JSON.stringify(payload) },
  60_000 // 60 секунд для AI generation
);
```

Отмена параллельных операций:

```ts
// Когда нужно отменить несколько fetch при первом успехе (race pattern)
const controller = new AbortController();
const { signal } = controller;

const result = await Promise.race([
  primaryProvider(signal),
  fallbackProvider(signal),
]).finally(() => controller.abort()); // отменяем проигравший запрос
```

---

## retryWithBackoff — Проектная Утилита

```ts
// src/shared/utils/retry.ts
import { retryWithBackoff } from '@shared/utils/retry';

// Retryable: 429, 500, 502, 503
// Non-retryable: 400, 401, 403, 404 (выбрасывает сразу)
// Exponential backoff: delay = min(baseDelay * 2^attempt + jitter, maxDelay)

const result = await retryWithBackoff(
  () => fetch('https://api.laozhang.ai/v1/...', { method: 'POST', body }),
  {
    maxRetries: 3,
    baseDelay: 1000,  // 1s → 2s → 4s (+ jitter до 1s)
    maxDelay: 8000,
    operation: 'image-restoration',
    provider: 'laozhang',
  }
);
```

---

## Error Handling — Sanitization & Cause Chain

```ts
// src/shared/utils/logger.ts
// sanitizeError — ВСЕГДА используй перед logger.error()
// Убирает стек в production, не логирует сырые объекты с токенами
logger.error('Operation failed', sanitizeError(error));

// Spread для добавления контекста
logger.error('Job failed', {
  ...sanitizeError(error), // { message, name, code? }
  jobId: job.id,
  duration,
});

// sanitizeMessage — для строк с внешними данными (токены, URLs)
import { sanitizeMessage } from '@shared/utils/logger';
logger.info(sanitizeMessage(`Processing request from ${userInput}`));
```

Error cause chain (Node.js 16.9+):

```ts
// Оборачивай ошибки с контекстом
try {
  await aiClient.restore(imageBuffer);
} catch (error) {
  throw new Error('AI restoration failed', { cause: error });
}

// Чтение cause при логировании
function sanitizeErrorWithCause(error: unknown): Record<string, unknown> {
  const base = sanitizeError(error);
  if (error instanceof Error && error.cause) {
    base['cause'] = sanitizeError(error.cause);
  }
  return base;
}
```

---

## Event Loop — setInterval Patterns

setInterval для фоновых задач — не блокируй, обрабатывай ошибки внутри:

```ts
// src/features/analytics/jobs/analytics-sender.job.ts
// Паттерн: запуск сразу + повторение через интервал
sendUnsentEvents(); // первый запуск немедленно

analyticsInterval = setInterval(() => {
  // ВАЖНО: .catch() — иначе unhandled rejection если sendUnsentEvents() бросит
  sendUnsentEvents().catch((error) => {
    logger.error('Error in analytics sender interval', sanitizeError(error));
    // НЕ перебрасываем — interval должен продолжать работу
  });
}, 30 * 60 * 1000); // 30 минут

// src/features/notification/jobs/notification.job.ts
// Альтернативный паттерн — .then().catch() вместо async/await
setInterval(() => {
  const startTime = Date.now();
  notificationService.sendScheduledMessages()
    .then(() => {
      logger.debug('Scheduled messages sent', { duration: Date.now() - startTime });
    })
    .catch((error) => {
      logger.error('Error in scheduled messages interval', {
        ...sanitizeError(error),
        duration: Date.now() - startTime,
      });
    });
}, 5 * 60 * 1000); // 5 минут
```

Не блокируй event loop — CPU-intensive операции в worker threads:

```ts
// Если понадобится CPU-heavy работа (image processing без нативных биндингов)
import { Worker } from 'worker_threads';

// В проекте AI-обработка делегируется внешним API (LaoZhang/KIE),
// поэтому worker_threads не нужны — все I/O-bound
```

---

## Environment & Config — Singleton Pattern

```ts
// src/shared/config/env.ts
import { getEnv } from '@shared/config/env';

// getEnv() кэширует результат — повторные вызовы не перевалидируют
// Первый вызов — валидация Zod, throws если переменные отсутствуют/невалидны
const env = getEnv();

// Использование: вызывай в начале функции/модуля, не в верхнем уровне модуля
// (иначе падает при импорте тестов без .env)
export async function createServer() {
  const env = getEnv(); // безопасно — Zod уже отработал в main()
  // ...
}
```

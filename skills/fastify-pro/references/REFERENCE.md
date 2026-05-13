# Fastify 5.x — Project-Specific Reference

> Source: Fastify 5.x docs + project code | Project: mycolormemory | Generated: 2026-03-15

---

## Типизированные route handlers

Все контроллеры проекта используют `FastifyRequest<RouteGeneric>` — обязательный паттерн.

```ts
import { FastifyRequest, FastifyReply } from 'fastify';
import { z } from 'zod';

// --- Params only ---
export async function getRestorationHandler(
  request: FastifyRequest<{ Params: { id: string } }>,
  reply: FastifyReply
) {
  const { id } = request.params; // string, типизировано
  return reply.code(200).send({ id });
}

// --- Body typed via interface ---
interface CloudPaymentsWebhookPayload {
  InvoiceId: string;
  Amount: number;
  Status: string;
}

export async function handleWebhook(
  request: FastifyRequest<{ Body: CloudPaymentsWebhookPayload }>,
  reply: FastifyReply
) {
  const { InvoiceId, Amount } = request.body; // типизировано
}

// --- Body typed via Zod schema ---
const saveAnalyticsSchema = z.object({
  userId: z.string().uuid(),
  yandexClientId: z.string().nullable().optional(),
});

export async function saveAnalyticsHandler(
  request: FastifyRequest<{ Body: z.infer<typeof saveAnalyticsSchema> }>,
  reply: FastifyReply
) {
  // Fastify не валидирует через Zod автоматически — вызывай parse вручную
  const data = saveAnalyticsSchema.parse(request.body);
  return reply.code(200).send({ success: true });
}

// --- Querystring ---
fastify.get<{ Querystring: { token?: string } }>('/verify', async (request, reply) => {
  const token = request.query.token; // string | undefined
});

// --- Все generic поля ---
// FastifyRequest<{
//   Params: Record<string, string>;
//   Body: unknown;
//   Querystring: Record<string, string | undefined>;
//   Headers: Record<string, string>;
// }>
```

---

## rawBody — правильная типизация без `as any`

Текущий код использует `(req as any).rawBody` — это tech debt. Правильный способ в Fastify 5:

```ts
// Вариант 1: module augmentation (рекомендован для проекта)
// src/shared/types/fastify.d.ts
import 'fastify';

declare module 'fastify' {
  interface FastifyRequest {
    rawBody?: string;
  }
}

// Затем в server.ts — addDecorator перед парсером:
fastify.decorateRequest('rawBody', '');

fastify.addContentTypeParser(
  'application/json',
  { parseAs: 'string' },
  (req, body, done) => {
    try {
      req.rawBody = body as string; // типизировано, без as any
      done(null, JSON.parse(body as string));
    } catch (err) {
      done(err as Error, undefined);
    }
  }
);

// В webhook-обработчике — без as any:
export async function handleCloudPaymentsWebhook(
  request: FastifyRequest<{ Body: CloudPaymentsWebhookPayload }>,
  reply: FastifyReply
) {
  const rawBody = request.rawBody; // string | undefined — типизировано
  if (!rawBody) {
    return reply.code(500).send({ error: 'Internal server error' });
  }
  const sig = crypto.createHmac('sha256', secret).update(rawBody).digest('hex');
}
```

> **Важно**: `decorateRequest` должен вызываться ДО `addContentTypeParser` и ДО регистрации маршрутов.

---

## Plugin Encapsulation — Scoped Rate Limiting

Fastify инкапсулирует плагины: `register` создаёт изолированный контекст.

```ts
// Глобальный rate limit (100 req/min для всего приложения)
await fastify.register(rateLimit, {
  max: 100,
  timeWindow: '1 minute',
});

// Scoped rate limit для чувствительного endpoint (5 req/min)
// Регистрируем как отдельный plugin с prefix
await fastify.register(
  async (scopedFastify) => {
    // Переопределяем rate limit только для этого scope
    await scopedFastify.register(rateLimit, {
      max: 5,
      timeWindow: '1 minute',
    });

    scopedFastify.get<{ Querystring: { token?: string } }>(
      '/verify',
      async (request, reply) => {
        const token = request.query.token;
        if (!token) return reply.code(401).send({ error: 'Unauthorized' });
        // ...
      }
    );
  },
  { prefix: '/api/bot-check' } // итоговый путь: /api/bot-check/verify
);
```

---

## Hooks lifecycle — порядок выполнения в Fastify 5

```
onRequest → preParsing → preValidation → preHandler → handler → preSerialization → onSend → onResponse
```

```ts
// onRequest — логирование каждого запроса (используется в проекте)
fastify.addHook('onRequest', async (request, reply) => {
  logger.debug('Incoming request', {
    method: request.method,
    url: request.url,
    ip: request.ip,
  });
});

// onSend — security headers на каждый ответ (используется в проекте)
fastify.addHook('onSend', async (_request, reply) => {
  reply.header('X-Content-Type-Options', 'nosniff');
  reply.header('X-Frame-Options', 'DENY');
  reply.header('X-XSS-Protection', '1; mode=block');
  if (getEnv().NODE_ENV === 'production') {
    reply.header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  }
});

// preHandler — авторизация, guard перед хендлером
fastify.addHook('preHandler', async (request, reply) => {
  const token = request.headers.authorization;
  if (!token) return reply.code(401).send({ error: 'Unauthorized' });
});

// onError — перехват ошибок до сериализации ответа
fastify.addHook('onError', async (request, reply, error) => {
  logger.error('Unhandled route error', { ...sanitizeError(error), url: request.url });
});
```

---

## @fastify/static — Multiple Registrations

```ts
import fastifyStatic from '@fastify/static';
import { join } from 'path';

const publicDir = join(process.cwd(), 'public');

// Первая регистрация — создаёт декоратор reply.sendFile()
await fastify.register(fastifyStatic, {
  root: publicDir,
  prefix: '/',
  wildcard: false, // не перехватывает API-маршруты
});

// Последующие регистрации — decorateReply: false (декоратор уже есть)
await fastify.register(fastifyStatic, {
  root: join(publicDir, 'restorations'),
  prefix: '/restorations/',
  wildcard: false,
  decorateReply: false, // ОБЯЗАТЕЛЬНО для 2-й и последующих регистраций
});

await fastify.register(fastifyStatic, {
  root: join(publicDir, 'animations'),
  prefix: '/animations/',
  wildcard: false,
  decorateReply: false,
});
```

> **Правило порядка**: API-маршруты (`/api/*`, `/webhooks/*`) регистрируй ДО `@fastify/static`, иначе статик-плагин перехватит запросы.

---

## Error Handling — setErrorHandler

```ts
import { FastifyError } from 'fastify';

// Глобальный обработчик ошибок
fastify.setErrorHandler(async (error: FastifyError, request, reply) => {
  logger.error('Fastify error handler triggered', {
    ...sanitizeError(error),
    url: request.url,
    method: request.method,
    statusCode: error.statusCode,
  });

  // Rate limit ошибка
  if (error.statusCode === 429) {
    return reply.code(429).send({ error: 'Too Many Requests' });
  }

  // Validation error (JSON Schema или Zod)
  if (error.statusCode === 400) {
    return reply.code(400).send({ error: 'Bad Request', details: error.message });
  }

  return reply.code(error.statusCode ?? 500).send({ error: 'Internal server error' });
});

// В route handler — ZodError обрабатывается вручную (Zod не интегрирован нативно)
export async function saveAnalyticsHandler(
  request: FastifyRequest<{ Body: z.infer<typeof saveAnalyticsSchema> }>,
  reply: FastifyReply
) {
  try {
    const data = saveAnalyticsSchema.parse(request.body); // throws ZodError
    // ...
  } catch (error) {
    if (error instanceof z.ZodError) {
      return reply.code(400).send({ error: 'Invalid request data', details: error.issues });
    }
    logger.error('Unexpected error', sanitizeError(error));
    return reply.code(500).send({ error: 'Internal server error' });
  }
}
```

---

## Graceful Shutdown

```ts
// src/app/index.ts — текущий паттерн проекта
import { stopNotificationWorker } from '@features/notification/workers/notification.worker';
import { stopAnalyticsSender } from '@features/analytics/workers/analytics-sender.worker';

const shutdown = async (signal: string) => {
  logger.info(`${signal} received, shutting down gracefully`);

  // 1. Остановить воркеры (перестать брать новые задачи)
  stopNotificationWorker();
  stopAnalyticsSender();

  // 2. Закрыть HTTP-сервер (дождаться in-flight запросов)
  await server.close();

  // 3. Остановить бота
  bot.stop();

  logger.info('Shutdown complete');
  process.exit(0);
};

process.once('SIGINT', () => shutdown('SIGINT'));
process.once('SIGTERM', () => shutdown('SIGTERM'));

// fastify.close() ждёт завершения текущих запросов — не вызывай process.exit() сразу
```

---

## Server Factory Pattern — полная конфигурация

```ts
// src/app/server.ts — структура createServer()
import Fastify from 'fastify';
import cors from '@fastify/cors';
import rateLimit from '@fastify/rate-limit';
import fastifyStatic from '@fastify/static';
import { getEnv } from '@shared/config/env';
import { logger, sanitizeError } from '@shared/utils/logger';

export async function createServer() {
  const env = getEnv();

  const fastify = Fastify({ logger: true });

  // 1. Декораторы и парсеры (до всего)
  fastify.decorateRequest('rawBody', '');
  fastify.addContentTypeParser('application/json', { parseAs: 'string' }, (req, body, done) => {
    try {
      req.rawBody = body as string;
      done(null, JSON.parse(body as string));
    } catch (err) {
      done(err as Error, undefined);
    }
  });

  // 2. Hooks
  fastify.addHook('onSend', async (_request, reply) => { /* security headers */ });
  fastify.addHook('onRequest', async (request) => { /* logging */ });

  // 3. Плагины безопасности
  await fastify.register(cors, { origin: [...], credentials: true });
  await fastify.register(rateLimit, { max: 100, timeWindow: '1 minute' });

  // 4. API-маршруты (ДО статики)
  fastify.get('/health', async () => ({ status: 'ok', timestamp: new Date().toISOString() }));
  fastify.post('/api/analytics/save', saveAnalyticsHandler);
  fastify.post('/webhooks/cloudpayments', handleCloudPaymentsWebhook);

  // 5. Scoped маршруты с другими ограничениями
  await fastify.register(async (f) => {
    await f.register(rateLimit, { max: 5, timeWindow: '1 minute' });
    f.get<{ Querystring: { token?: string } }>('/verify', handler);
  }, { prefix: '/api/bot-check' });

  // 6. Статические файлы (ПОСЛЕ API)
  await fastify.register(fastifyStatic, { root: publicDir, prefix: '/', wildcard: false });
  await fastify.register(fastifyStatic, { root: restorationsDir, prefix: '/restorations/', wildcard: false, decorateReply: false });

  await fastify.ready();
  return fastify;
}
```

---

## Fastify 5 vs 4 — ключевые отличия

| Аспект | Fastify 4 | Fastify 5 |
|--------|-----------|-----------|
| `reply.send()` return | `void` | возвращает `reply` (chainable) |
| Route shorthand generic | `fastify.get<RouteGeneric>` | без изменений |
| `setErrorHandler` type | `FastifyError` | `FastifyError` (без изменений) |
| Нативная поддержка `rawBody` | нет | нет (нужен декоратор) |
| `addHook('onSend')` payload | `string | Buffer | null` | `string | Buffer | null` |
| `fastify.close()` | Promise | Promise (без изменений) |

> Fastify 5 требует Node.js 20+. В проекте Node.js 20 — совместимо.

---

## Известные проблемы проекта (tech debt)

- `(req as any).rawBody` — в `cloudpayments.webhook.ts` и `kie-animation.webhook.ts`. Нужно заменить на module augmentation + `decorateRequest`.
- `(httpsOptions as any)` — в `createServer()` при передаче SSL-опций. Нужно использовать тип `FastifyHttpsOptions`.
- `widgetUrl XSS` — `/web/payment/:invoiceId` инжектирует URL без escaping. Не расширять этот паттерн.

# Server Management — Project-Specific Reference

<!-- Generated from model knowledge, verify against official docs -->

> Stack: PM2 + systemd + Node.js | Project: ai-pipeline | Generated: 2026-03-10

## PM2 — Конфигурация и управление

```bash
# ─── Жизненный цикл ──────────────────────────────────────────────────────────
pm2 start ecosystem.config.js --env production   # первый запуск
pm2 reload ai-pipeline        # zero-downtime (дожидается ready сигнала)
pm2 restart ai-pipeline       # обычный перезапуск (обрывает соединения)
pm2 stop ai-pipeline          # остановить (процесс остаётся в списке)
pm2 delete ai-pipeline        # полностью удалить из PM2
pm2 save                      # сохранить текущий список для autostart
pm2 resurrect                 # восстановить после reboot

# ─── Мониторинг ──────────────────────────────────────────────────────────────
pm2 status                    # таблица: имя, pid, статус, CPU, память, рестарты
pm2 monit                     # realtime dashboard
pm2 show ai-pipeline          # детальная информация
pm2 env 0                     # переменные окружения процесса

# ─── Логи ────────────────────────────────────────────────────────────────────
pm2 logs                      # все приложения
pm2 logs ai-pipeline          # конкретное приложение
pm2 logs ai-pipeline --lines 200
pm2 logs ai-pipeline --err    # только stderr
pm2 flush ai-pipeline         # очистить логи
pm2 reloadLogs                # переоткрыть файлы (после ротации)

# ─── Cluster mode ────────────────────────────────────────────────────────────
# Для stateless приложений — масштабировать
pm2 scale ai-pipeline 4       # запустить 4 инстанса
pm2 scale ai-pipeline +2      # добавить 2 к текущим

# ─── Автозапуск при boot ─────────────────────────────────────────────────────
pm2 startup ubuntu            # сгенерировать systemd unit
# Выполнить команду которую покажет startup
pm2 save
```

## Graceful Shutdown — Node.js + PM2

```typescript
// src/core/shutdown.ts
// PM2 отправляет SIGINT при pm2 reload/stop

let isShuttingDown = false;

export function setupGracefulShutdown(server: http.Server): void {
  const shutdown = async (signal: string) => {
    if (isShuttingDown) return;
    isShuttingDown = true;

    logger.info(`Received ${signal}, starting graceful shutdown`);

    // 1. Перестать принимать новые запросы
    server.close(async () => {
      logger.info('HTTP server closed');

      // 2. Завершить текущие задачи
      await drainTaskQueue();

      // 3. Закрыть соединения с DB
      await db.end();
      await redis.quit();

      logger.info('Graceful shutdown complete');
      process.exit(0);
    });

    // Форс-стоп если завис
    setTimeout(() => {
      logger.error('Graceful shutdown timeout, forcing exit');
      process.exit(1);
    }, 10_000);
  };

  process.on('SIGINT', () => shutdown('SIGINT'));
  process.on('SIGTERM', () => shutdown('SIGTERM'));

  // Сигнал PM2 что приложение готово
  if (process.send) {
    server.on('listening', () => {
      process.send!('ready');
      logger.info('Sent ready signal to PM2');
    });
  }
}
```

## Health Check — Паттерн для мониторинга

```typescript
// src/http/healthz.ts
export interface HealthResponse {
  status: 'ok' | 'degraded' | 'unhealthy';
  version: string;
  uptime: number;
  checks: {
    db: CheckResult;
    redis: CheckResult;
    memory: CheckResult;
    disk?: CheckResult;
  };
}

export async function getHealthStatus(): Promise<HealthResponse> {
  const [dbCheck, redisCheck] = await Promise.allSettled([
    checkDatabase(),
    checkRedis(),
  ]);

  const checks = {
    db:     toCheckResult(dbCheck),
    redis:  toCheckResult(redisCheck),
    memory: checkMemory(),
  };

  const critical = !checks.db.ok || !checks.redis.ok;
  const degraded = Object.values(checks).some(c => !c.ok);

  return {
    status: critical ? 'unhealthy' : degraded ? 'degraded' : 'ok',
    version: process.env.APP_VERSION ?? 'unknown',
    uptime: Math.floor(process.uptime()),
    checks,
  };
}

async function checkDatabase(): Promise<void> {
  await db.query('SELECT 1');
}

async function checkRedis(): Promise<void> {
  const pong = await redis.ping();
  if (pong !== 'PONG') throw new Error('Redis not responding');
}

function checkMemory(): CheckResult {
  const mem = process.memoryUsage();
  const heapUsedMb = mem.heapUsed / 1024 / 1024;
  const heapTotalMb = mem.heapTotal / 1024 / 1024;
  const usagePct = (heapUsedMb / heapTotalMb) * 100;

  return {
    ok: heapUsedMb < 1024,  // < 1GB
    message: `${heapUsedMb.toFixed(0)}MB / ${heapTotalMb.toFixed(0)}MB (${usagePct.toFixed(0)}%)`,
  };
}
```

## Structured Logging — Паттерн проекта

```typescript
// src/core/logging.ts
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  // JSON в production, pretty в dev
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty', options: { colorize: true } }
    : undefined,
  // Добавить контекст ко всем логам
  base: {
    app: 'ai-pipeline',
    version: process.env.APP_VERSION,
    pid: process.pid,
  },
  // Редактировать чувствительные поля
  redact: ['req.headers.authorization', 'body.password', 'apiKey'],
  serializers: pino.stdSerializers,
});

// Использование
logger.info({ taskId, phase }, 'Starting pipeline phase');
logger.warn({ taskId, attempt, maxRetries }, 'Retrying failed operation');
logger.error({ taskId, err }, 'Pipeline failed');

// Child logger для контекста
const taskLogger = logger.child({ taskId: task.id, project: task.projectSlug });
taskLogger.info('Task started');
taskLogger.info({ phase }, 'Entering phase');
```

## Process Monitoring — Prometheus метрики

```typescript
// src/http/api-observability.ts
// Формат для Prometheus scraping (GET /api/metrics)

interface AppMetrics {
  tasksRunning: number;
  tasksCompleted: number;
  tasksFailed: number;
  agentCallsTotal: number;
  agentCallDurationP95: number;
  dbConnectionsActive: number;
  heapUsedBytes: number;
}

function formatPrometheus(metrics: AppMetrics): string {
  const lines: string[] = [
    '# HELP pipeline_tasks_running Number of currently running tasks',
    '# TYPE pipeline_tasks_running gauge',
    `pipeline_tasks_running ${metrics.tasksRunning}`,
    '',
    '# HELP pipeline_tasks_completed_total Total completed tasks',
    '# TYPE pipeline_tasks_completed_total counter',
    `pipeline_tasks_completed_total ${metrics.tasksCompleted}`,
    '',
    '# HELP pipeline_heap_bytes Node.js heap usage',
    '# TYPE pipeline_heap_bytes gauge',
    `pipeline_heap_bytes ${metrics.heapUsedBytes}`,
  ];
  return lines.join('\n');
}

router.get('/api/metrics', async (req, res) => {
  const metrics = await collectMetrics();
  res.set('Content-Type', 'text/plain; version=0.0.4');
  res.send(formatPrometheus(metrics));
});
```

## Scaling Decision Tree

```
Симптом: высокий CPU (>80% sustained)
├── Один поток? → pm2 scale ai-pipeline +2
├── Много sync ops? → profiler: node --prof
└── DB queries? → EXPLAIN ANALYZE + индексы

Симптом: высокая память (>1GB, растёт)
├── Memory leak? → heapdump + Chrome DevTools
│   node --inspect-brk dist/index.js → chrome://inspect
├── Кэш не ограничен? → установить maxmemory в Redis
└── В норме для нагрузки? → increase PM2 memory limit

Симптом: медленные ответы (p95 > 1s)
├── Профилировать: clinic.js или 0x
├── DB slow queries? → pg_stat_statements
└── External API calls? → добавить timeout + circuit breaker

Симптом: спайки трафика
└── Горизонтальное масштабирование:
    pm2 scale ai-pipeline 4
    # или Docker Compose replicas: 4 + load balancer в Angie upstream
```

## Disaster Recovery Checklist

```bash
# ─── Сервис упал ──────────────────────────────────────────────────────────────
pm2 status                      # статус процессов
pm2 logs ai-pipeline --err --lines 50  # последние ошибки
journalctl -u pm2-ubuntu -n 50  # systemd уровень

# Если stuck (из MEMORY.md — важный паттерн!):
pm2 delete ai-pipeline          # remove from PM2
kill $(lsof -ti :9090)          # kill if port held
pm2 start ecosystem.config.js   # clean start
pm2 save

# ─── Порт занят ───────────────────────────────────────────────────────────────
lsof -ti :9090                  # PID процесса
kill -9 $(lsof -ti :9090)
pm2 start ecosystem.config.js

# ─── DB недоступна ────────────────────────────────────────────────────────────
pg_isready -U postgres -d vechkasov_pro
systemctl status postgresql
systemctl start postgresql
# Проверить логи
tail -50 /var/log/postgresql/postgresql-17-main.log

# ─── Диск заполнен ───────────────────────────────────────────────────────────
df -h
du -xsh /home/ubuntu/.pm2/logs/* | sort -rh
pm2 flush                       # очистить PM2 логи
journalctl --vacuum-time=7d     # очистить journal
docker system prune -f          # Docker мусор
```

## Environment Variables — Управление

```bash
# .env.production (НЕ коммитить)
NODE_ENV=production
PORT=9090
DATABASE_URL=postgresql://user:pass@localhost:5432/vechkasov_pro
REDIS_URL=redis://localhost:6379
ANTHROPIC_API_KEY=sk-ant-...
LOG_LEVEL=info
APP_VERSION=1.2.3

# Загрузка в PM2 (ecosystem.config.js)
env_file: '.env.production',  # если PM2 v5+
# или
env: {
  ...require('dotenv').config({ path: '.env.production' }).parsed
}

# Проверить что переменные загружены
pm2 env 0 | grep -E "NODE_ENV|PORT|DATABASE"

# Обновить env без рестарта (только для не-критичных)
pm2 restart ai-pipeline --update-env
```

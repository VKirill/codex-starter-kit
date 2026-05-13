# Linux SysAdmin — Full Stack Integration Reference

<!-- Generated from model knowledge, verify against official docs -->

> Stack: Ubuntu 24.04 | Angie 1.11.3 | PostgreSQL 17 | Redis 7 | PM2 | Docker | UFW
> Generated: 2026-03-10

## Angie — Конфигурация для Node.js приложения

```nginx
# /etc/angie/http.d/ai-pipeline.conf
# или /etc/angie/sites-enabled/ai-pipeline

upstream ai_pipeline {
    server 127.0.0.1:9090;
    keepalive 32;
}

server {
    listen 80;
    server_name pipeline.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    http2 on;
    server_name pipeline.example.com;

    # TLS (certbot)
    ssl_certificate     /etc/letsencrypt/live/pipeline.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/pipeline.example.com/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;
    ssl_session_cache   shared:SSL:10m;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Proxy to Node.js
    location / {
        proxy_pass         http://ai_pipeline;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade    $http_upgrade;
        proxy_set_header   Connection "upgrade";
        proxy_set_header   Host       $host;
        proxy_set_header   X-Real-IP  $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;

        # Timeouts для длинных pipeline операций
        proxy_read_timeout    300s;
        proxy_connect_timeout 10s;
        proxy_send_timeout    300s;
    }

    # Health check — без логирования
    location /healthz {
        proxy_pass http://ai_pipeline;
        access_log off;
    }

    # Static assets (если есть)
    location /static/ {
        alias /var/www/ai-pipeline/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    access_log  /var/log/angie/ai-pipeline.access.log;
    error_log   /var/log/angie/ai-pipeline.error.log;
}
```

```bash
# Workflow обновления конфига Angie
cp /etc/angie/http.d/ai-pipeline.conf /etc/angie/http.d/ai-pipeline.conf.bak.$(date +%s)
vim /etc/angie/http.d/ai-pipeline.conf
angie -t                          # ОБЯЗАТЕЛЬНО перед reload
systemctl reload angie            # graceful reload (не restart)
curl -I https://pipeline.example.com/healthz
```

## PM2 — ecosystem.config.js для ai-pipeline

```javascript
// /home/ubuntu/apps/ai-pipeline/ecosystem.config.js
module.exports = {
  apps: [{
    name: 'ai-pipeline',
    script: 'dist/index.js',
    cwd: '/home/ubuntu/apps/ai-pipeline',
    interpreter: 'node',
    interpreter_args: '--experimental-vm-modules',

    // Кластеризация (для CPU-bound)
    // instances: 'max',  // все ядра
    instances: 1,          // для stateful приложений — 1 инстанс

    // Поведение при перезапуске
    autorestart: true,
    max_restarts: 10,
    min_uptime: '10s',
    restart_delay: 5000,
    watch: false,

    // Env
    env: {
      NODE_ENV: 'production',
      PORT: 9090,
    },
    env_development: {
      NODE_ENV: 'development',
      PORT: 9090,
    },

    // Логирование
    log_file:   '/home/ubuntu/.pm2/logs/ai-pipeline-combined.log',
    out_file:   '/home/ubuntu/.pm2/logs/ai-pipeline-out.log',
    error_file: '/home/ubuntu/.pm2/logs/ai-pipeline-error.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,

    // Graceful shutdown
    kill_timeout: 10000,    // 10 сек на graceful stop
    wait_ready: true,       // ждать process.send('ready')
    listen_timeout: 10000,

    // Ротация логов
    max_size: '100M',
    retain: 7,
  }],
};
```

```bash
# PM2 команды для ai-pipeline
pm2 start ecosystem.config.js --env production  # запуск
pm2 reload ai-pipeline                           # zero-downtime reload
pm2 restart ai-pipeline                          # обычный restart (обрыв соединений)
pm2 stop ai-pipeline                             # остановить
pm2 delete ai-pipeline                           # удалить из PM2
pm2 save                                         # сохранить для autostart
pm2 startup ubuntu                               # autostart при boot

# Мониторинг
pm2 status                   # список процессов
pm2 monit                    # realtime CPU/RAM
pm2 logs ai-pipeline --lines 100
pm2 logs ai-pipeline --err --lines 50   # только errors

# Диагностика зависаний (из MEMORY.md)
# pm2 restart медленный → delete + start
pm2 delete ai-pipeline && pm2 start ecosystem.config.js
# Если порт занят:
kill $(lsof -ti :9090) && pm2 start ecosystem.config.js
```

## PostgreSQL 17 — Мониторинг и обслуживание

```bash
# Статус и подключение
systemctl status postgresql
pg_isready -U postgres -d vechkasov_pro
psql -U postgres -d vechkasov_pro

# Активные соединения и долгие запросы
psql -U postgres -c "
SELECT pid, now() - query_start AS duration, state, left(query, 80) AS query
FROM pg_stat_activity
WHERE datname = 'vechkasov_pro' AND state != 'idle'
ORDER BY duration DESC;"

# Размеры таблиц
psql -U postgres -d vechkasov_pro -c "
SELECT schemaname, tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;"

# Убить зависший запрос
psql -U postgres -c "SELECT pg_terminate_backend(PID);"

# Бэкап и восстановление
pg_dump -U postgres vechkasov_pro | gzip > /var/backups/postgresql/vechkasov_pro_$(date +%Y%m%d_%H%M).sql.gz
gunzip -c backup.sql.gz | psql -U postgres vechkasov_pro

# Мониторинг checkpoint и autovacuum
psql -U postgres -c "SELECT * FROM pg_stat_bgwriter;"
psql -U postgres -d vechkasov_pro -c "SELECT * FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 10;"
```

## Redis 7 — Мониторинг и конфигурация

```bash
# Статус
systemctl status redis-server
redis-cli ping    # PONG

# Мониторинг
redis-cli info server | grep -E "redis_version|uptime|os"
redis-cli info memory | grep -E "used_memory_human|maxmemory_human"
redis-cli info stats | grep -E "total_commands_processed|keyspace_hits|keyspace_misses"
redis-cli info keyspace   # количество ключей по базам

# Просмотр ключей (ОСТОРОЖНО в prod — использовать scan, не keys *)
redis-cli scan 0 match "pipeline:*" count 20
redis-cli type "pipeline:task:123"
redis-cli ttl  "pipeline:task:123"

# Очистка
redis-cli flushdb           # ОСТОРОЖНО: очистить текущую базу
redis-cli del "pipeline:lock:TASK_ID"  # удалить конкретный ключ

# Конфиг
redis-cli config get maxmemory
redis-cli config set maxmemory 512mb
redis-cli config set maxmemory-policy allkeys-lru   # для кэша

# Бэкап
redis-cli bgsave
redis-cli lastsave                                  # timestamp последнего save
cp /var/lib/redis/dump.rdb /var/backups/redis/dump_$(date +%Y%m%d).rdb
```

## UFW — Firewall для сервера

```bash
# Текущие правила
ufw status numbered

# Стандартный набор для ai-pipeline сервера
ufw default deny incoming
ufw default allow outgoing
ufw allow 2222/tcp           # SSH (нестандартный порт)
ufw allow 80/tcp             # HTTP (редирект на HTTPS)
ufw allow 443/tcp            # HTTPS

# Разрешить только с конкретного IP (для admin)
ufw allow from 1.2.3.4 to any port 2222

# НЕ открывать напрямую (только через Angie)
# ufw allow 9090  ← НЕПРАВИЛЬНО для production

# Удалить правило
ufw status numbered
ufw delete 5

# Логирование
ufw logging on
tail -f /var/log/ufw.log
```

## Системный мониторинг — быстрые проверки

```bash
# Общее состояние одной командой
echo "=== Load ===" && uptime && \
echo "=== Memory ===" && free -h && \
echo "=== Disk ===" && df -h / /var/log && \
echo "=== Services ===" && systemctl is-active angie postgresql redis-server && \
echo "=== PM2 ===" && pm2 jlist | node -e "const d=require('fs').readFileSync('/dev/stdin','utf8');const apps=JSON.parse(d);apps.forEach(a=>console.log(a.name,a.pm2_env.status,a.pm2_env.restart_time+'restarts'))"

# Топ процессов по памяти
ps aux --sort=-%mem | head -10

# Проверка портов
ss -tlnp | grep -E ':80|:443|:9090|:5432|:6379'

# Disk usage — найти большие файлы
du -xsh /var/log/* | sort -rh | head -10
du -xsh /home/ubuntu/.pm2/logs/* | sort -rh | head -10

# Journal — последние ошибки системы
journalctl -p err -n 50 --no-pager

# Свободная оперативная память
free -h

# Swap использование (признак нехватки RAM)
vmstat 1 3
```

## Деплой обновления ai-pipeline

```bash
# Безопасный деплой без downtime
cd /home/ubuntu/apps/ai-pipeline

# 1. Получить обновления
git pull origin main

# 2. Установить зависимости (если изменились)
npm ci --only=production

# 3. Сборка TypeScript
npm run build

# 4. Zero-downtime reload (PM2 ждёт process.send('ready'))
pm2 reload ai-pipeline

# 5. Проверка
pm2 status
curl -s http://localhost:9090/healthz | jq .

# Если reload завис или не работает (из MEMORY.md):
pm2 delete ai-pipeline
pm2 start ecosystem.config.js --env production
pm2 save
```

## Ротация логов

```bash
# /etc/logrotate.d/ai-pipeline
/home/ubuntu/.pm2/logs/ai-pipeline*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    copytruncate          # не прерывать запись в процесс
}

# Ручная ротация PM2 логов
pm2 flush ai-pipeline     # очистить текущие
pm2 reloadLogs            # переоткрыть файлы

# Журнал systemd — ограничить размер
journalctl --vacuum-size=500M
journalctl --vacuum-time=30d
```

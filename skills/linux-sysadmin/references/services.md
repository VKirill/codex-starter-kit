# Service Management Reference

Detailed configuration and administration for all services on our stack.

## systemd

### Unit file template
```ini
[Unit]
Description=My Service
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=appuser
Group=appgroup
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/node /opt/myapp/server.js
Restart=on-failure
RestartSec=5
StartLimitBurst=5
StartLimitIntervalSec=60
StandardOutput=journal
StandardError=journal
SyslogIdentifier=myapp
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/opt/myapp/data
PrivateTmp=yes

[Install]
WantedBy=multi-user.target
```

### Key commands
```bash
systemctl start|stop|restart|reload SERVICE
systemctl enable|disable SERVICE
systemctl status SERVICE
journalctl -u SERVICE -n 100 --no-pager
journalctl -u SERVICE --since "1 hour ago"
systemctl list-units --failed
systemctl list-timers --all
```

Unit file locations (priority order):
1. `/etc/systemd/system/` — custom
2. `/run/systemd/system/` — runtime
3. `/lib/systemd/system/` — package-installed

## PM2 (Node.js Process Manager)

### Commands
```bash
pm2 status                    # List all
pm2 logs APP --lines 100     # View logs
pm2 restart APP               # Restart (brief downtime)
pm2 reload APP                # Zero-downtime (cluster mode)
pm2 stop APP                  # Stop
pm2 delete APP                # Remove from list
pm2 save                      # Persist list for reboot
pm2 startup                   # Generate boot script
pm2 monit                     # Real-time dashboard
```

### Ecosystem config
```javascript
module.exports = {
  apps: [{
    name: 'myapp',
    script: './dist/index.js',
    instances: 1,
    exec_mode: 'fork',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    max_memory_restart: '500M',
    error_file: './logs/error.log',
    out_file: './logs/out.log'
  }]
}
```

### Monitoring
```bash
pm2 jlist  # JSON output for parsing
# Parse: name, status, restart_time, monit.cpu, monit.memory
```

Important: `pm2 save` after any change. `pm2 reload` for cluster mode only.

## PostgreSQL 17

### Status & Connections
```bash
pg_isready                    # Quick health check
sudo -u postgres psql -c "SELECT version();"
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"
```

### Database sizes
```sql
SELECT datname, pg_size_pretty(pg_database_size(datname))
FROM pg_database WHERE datistemplate = false
ORDER BY pg_database_size(datname) DESC;
```

### Active queries
```sql
SELECT pid, now() - query_start AS duration, query, state
FROM pg_stat_activity WHERE state != 'idle'
ORDER BY duration DESC;
```

### Kill long query
```sql
SELECT pg_terminate_backend(PID);
```

### Maintenance
```bash
sudo -u postgres psql -c "VACUUM ANALYZE;"
```

### Backup / Restore
```bash
pg_dump -U postgres -Fc DATABASE > backup.dump
pg_dumpall -U postgres > all.sql
pg_restore -U postgres -d DATABASE backup.dump
```

### Config files
- `/etc/postgresql/17/main/postgresql.conf` — server settings
- `/etc/postgresql/17/main/pg_hba.conf` — authentication rules

### Tuning (example for 8GB RAM server — adjust to your hardware)
```
# Rule of thumb: shared_buffers = 25% RAM, effective_cache_size = 75% RAM
shared_buffers = 2GB                # 25% of 8GB
effective_cache_size = 6GB          # 75% of 8GB
work_mem = 64MB                     # RAM / max_connections / 2
maintenance_work_mem = 512MB        # For vacuum, index creation
wal_buffers = 64MB
max_connections = 100
random_page_cost = 1.1              # SSD (use 4.0 for HDD)
effective_io_concurrency = 200      # SSD (use 2 for HDD)
```

## Redis 7

### Status
```bash
redis-cli ping
redis-cli info server
redis-cli info memory
redis-cli info clients
```

### Memory analysis
```bash
redis-cli info memory | grep used_memory_human
redis-cli memory doctor
redis-cli --bigkeys
redis-cli --memkeys
redis-cli dbsize
```

### Persistence
```bash
redis-cli lastsave           # Last RDB save
redis-cli bgsave             # Manual save
redis-cli config get save
redis-cli config get appendonly
```

### Tuning (`/etc/redis/redis.conf`)
```
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
appendonly yes
appendfsync everysec
```

## Docker

### Status
```bash
docker ps -a                          # All containers
docker stats --no-stream              # Resources
docker logs --tail 100 -t CONTAINER   # Logs
docker system df                      # Disk usage
```

### Compose
```bash
docker compose up -d                  # Start
docker compose down                   # Stop
docker compose pull                   # Update images
docker compose logs --tail 50 SVC     # Service logs
```

### Cleanup
```bash
docker container prune -f             # Stopped containers
docker image prune -f                 # Dangling images
docker network prune -f               # Unused networks
# NEVER auto-delete volumes — ask user first
docker volume ls -f dangling=true     # Show dangling volumes
```

## Backup Verification

```bash
# PostgreSQL dump integrity
pg_restore -l backup.dump > /dev/null 2>&1 && echo "OK" || echo "CORRUPT"

# Gzip integrity
gzip -t backup.sql.gz 2>&1 && echo "OK" || echo "CORRUPT"

# Tar integrity
tar tzf backup.tar.gz > /dev/null 2>&1 && echo "OK" || echo "CORRUPT"

# Zero-size check (failed backups)
find /var/backups -type f -size 0 \( -name "*.gz" -o -name "*.dump" \)
```

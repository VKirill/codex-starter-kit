# PostgreSQL 17 Optimization — Project-Specific Reference

> Source: context7 docs (PostgreSQL 17) | Project: vechkasov | Generated: 2026-04-07

## 1. pgvector Query Optimization (9 vector tables)

The project uses `vector(1024)` columns across 9 tables with cosine distance operator `<=>`.
All vector queries go through Prisma `$queryRawUnsafe` since Prisma doesn't support `vector` type.

### HNSW vs IVFFlat Index Selection

```sql
-- HNSW (preferred for this project — better recall, no training needed)
CREATE INDEX CONCURRENTLY idx_brain_entries_embedding
  ON agent_brain_entries USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

-- IVFFlat (for tables > 1M rows — faster build, lower recall)
CREATE INDEX CONCURRENTLY idx_library_chunks_embedding
  ON library_chunks USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);
-- Rule of thumb: lists = sqrt(row_count)
```

### Tuning HNSW Search

```sql
-- Increase probe depth for better recall (default ef_search = 40)
SET hnsw.ef_search = 100;

-- Project pattern: vector similarity with JOIN and threshold filter
-- From library-server.ts — optimize with partial index
SELECT c.id, c.content,
       1 - (c.embedding <=> $1::vector) AS similarity
FROM library_chunks c
JOIN library_documents d ON d.id = c."documentId"
JOIN library_shelves s ON s.id = d."shelfId"
WHERE c.embedding IS NOT NULL
  AND 1 - (c.embedding <=> $1::vector) > $2
ORDER BY c.embedding <=> $1::vector
LIMIT $3;
```

### Partial Index for NOT NULL Embeddings

Many project queries filter `WHERE embedding IS NOT NULL`. A partial index avoids scanning NULL rows:

```sql
CREATE INDEX CONCURRENTLY idx_brain_entries_emb_notnull
  ON agent_brain_entries USING hnsw (embedding vector_cosine_ops)
  WHERE embedding IS NOT NULL;

-- Same pattern for all 9 vector tables:
-- agent_brain_entries, ad_embeddings, architect_memories,
-- content_chunks, content_entities, library_chunks,
-- library_concepts, pipeline_memories, library_knowledge_entities
```

## 2. EXPLAIN ANALYZE for Vector Queries

```sql
-- Check if HNSW index is used
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, embedding <=> '[0.1,0.2,...]'::vector AS distance
FROM library_chunks
WHERE embedding IS NOT NULL
ORDER BY embedding <=> '[0.1,0.2,...]'::vector
LIMIT 20;

-- Expected: "Index Scan using idx_... on library_chunks"
-- Bad sign: "Seq Scan" = index not used, check:
--   1. Index exists? \di+ idx_name
--   2. ANALYZE table run recently?
--   3. Table too small for index scan (planner prefers seq scan < ~1000 rows)
```

### Reading EXPLAIN Output — Key Patterns

```sql
-- Pattern 1: Nested Loop with Index (good for small LIMIT)
-- common in project's vector search + JOIN queries
-- Nested Loop  (cost=0.42..100.50 rows=20 width=100)
--   ->  Index Scan using idx_emb on library_chunks  (actual rows=20)
--   ->  Index Scan using library_documents_pkey  (actual rows=1 loops=20)

-- Pattern 2: Bitmap Heap Scan (good for moderate result sets)
-- Bitmap Heap Scan on pipeline_events  (actual rows=500)
--   Recheck Cond: (task_id = $1)
--   ->  Bitmap Index Scan on idx_events_task_id  (actual rows=500)

-- Pattern 3: Seq Scan (investigate if table > 10K rows)
-- actual vs estimated rows mismatch > 10x = stale statistics
-- Fix: ANALYZE pipeline_tasks;
```

## 3. Connection Pool Optimization (Two Pools Pattern)

The project runs two separate `pg.Pool` instances:

```typescript
// Pipeline ESM pattern — db/events.ts
import pg from 'pg'
const { Pool } = pg

const pool = new Pool({
  connectionString: TASKS_DB_URL,  // or PIPELINE_DB_URL
  max: 5,                          // keep low — single app, not web server
  idleTimeoutMillis: 30_000,       // release idle connections
  connectionTimeoutMillis: 15_000, // fail fast on overload
})

pool.on('error', (err) => {
  console.error('[events] Pool error:', err.message)
})
```

### Pool Sizing Guidelines

```sql
-- Check current connections
SELECT count(*) AS total, state, application_name
FROM pg_stat_activity
WHERE datname = 'vechkasov_pro'
GROUP BY state, application_name;

-- For this project: CRM (Prisma pool ~10) + Pipeline (2 pools x 5) = ~20
-- Safe headroom for maintenance, pg_stat_statements, etc.
SHOW max_connections;  -- default: 100
```

## 4. Index Strategy for Project Tables

### pipeline_tasks — Frequent Filtering by Status

```sql
-- Partial index for active tasks (most queries filter by status)
CREATE INDEX CONCURRENTLY idx_tasks_active
  ON pipeline_tasks (status, priority DESC, "createdAt")
  WHERE status IN ('approved', 'planning', 'coding', 'building');
```

### pipeline_events — High Write Volume

```sql
-- Composite index for task event lookups (most common read pattern)
CREATE INDEX CONCURRENTLY idx_events_task_type
  ON pipeline_events ("taskId", "eventType", "createdAt" DESC);

-- Partial index for recent events only (SSE streaming reads recent)
CREATE INDEX CONCURRENTLY idx_events_recent
  ON pipeline_events ("createdAt" DESC)
  WHERE "createdAt" > NOW() - INTERVAL '7 days';
```

### Covering Indexes with INCLUDE

```sql
-- Avoid heap access for common lookups
CREATE INDEX CONCURRENTLY idx_leads_status_cover
  ON leads (status)
  INCLUDE (name, email, "createdAt");

-- Query uses index-only scan:
-- SELECT name, email, "createdAt" FROM leads WHERE status = 'new'
```

### Expression Indexes

```sql
-- Case-insensitive search
CREATE INDEX CONCURRENTLY idx_clients_name_lower
  ON clients (lower(name));
-- Query must use same expression: WHERE lower(name) = lower($1)
```

## 5. pg_stat_statements — Slow Query Detection

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 slowest queries by total time
SELECT
  queryid, calls,
  round(total_exec_time::numeric, 2) AS total_ms,
  round(mean_exec_time::numeric, 2) AS avg_ms,
  round((shared_blks_hit::numeric /
    NULLIF(shared_blks_hit + shared_blks_read, 0)) * 100, 1) AS cache_hit_pct,
  rows,
  left(query, 80) AS query_preview
FROM pg_stat_statements
WHERE dbid = (SELECT oid FROM pg_database WHERE datname = 'vechkasov_pro')
ORDER BY total_exec_time DESC
LIMIT 10;

-- Queries with worst cache hit ratio (I/O bound)
SELECT queryid, calls, shared_blks_read,
  round((shared_blks_hit::numeric /
    NULLIF(shared_blks_hit + shared_blks_read, 0)) * 100, 1) AS hit_pct,
  left(query, 80) AS query_preview
FROM pg_stat_statements
WHERE calls > 10 AND shared_blks_read > 100
ORDER BY hit_pct ASC LIMIT 10;

-- Reset after optimization round
SELECT pg_stat_statements_reset();
```

### postgresql.conf setup

```ini
shared_preload_libraries = 'pg_stat_statements'
compute_query_id = on
pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

## 6. auto_explain for Production Debugging

```sql
-- Enable in session (no restart)
LOAD 'auto_explain';
SET auto_explain.log_min_duration = '500ms';
SET auto_explain.log_analyze = on;
SET auto_explain.log_buffers = on;

-- Or permanently:
-- shared_preload_libraries = 'pg_stat_statements,auto_explain'
-- auto_explain.log_min_duration = '1000'
```

## 7. VACUUM & Maintenance for High-Write Tables

```sql
-- Check bloat on key tables
SELECT relname, n_live_tup, n_dead_tup,
       round(n_dead_tup::numeric / NULLIF(n_live_tup, 0) * 100, 1) AS dead_pct,
       last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables
WHERE relname IN (
  'pipeline_events', 'pipeline_tasks', 'messages',
  'library_chunks', 'content_chunks', 'agent_brain_entries'
)
ORDER BY n_dead_tup DESC;

-- Aggressive autovacuum for pipeline_events (high churn)
ALTER TABLE pipeline_events SET (
  autovacuum_vacuum_scale_factor = 0.05,    -- 5% dead (vs default 20%)
  autovacuum_analyze_scale_factor = 0.02,
  autovacuum_vacuum_cost_delay = 10
);

-- Manual after bulk operations
VACUUM (ANALYZE, VERBOSE) pipeline_events;
VACUUM (ANALYZE, VERBOSE) library_chunks;
```

## 8. PostgreSQL 17 Config Tuning

```ini
# postgresql.conf — single app server, ~16GB RAM, SSD

# Memory
shared_buffers = '4GB'             # 25% of RAM
effective_cache_size = '12GB'      # 75% of RAM
work_mem = '64MB'                  # per-sort/hash
maintenance_work_mem = '512MB'     # VACUUM, CREATE INDEX

# Planner (SSD optimized)
random_page_cost = 1.1             # default 4.0 for HDD
effective_io_concurrency = 200
default_statistics_target = 200    # better estimates for skewed data

# WAL
wal_buffers = '64MB'
checkpoint_completion_target = 0.9

# Connections
max_connections = 100              # CRM ~10 + Pipeline ~10 + overhead

# Autovacuum
autovacuum_max_workers = 4
autovacuum_naptime = '30s'
```

## 9. Table Size & Index Monitoring

```sql
-- Table sizes with index overhead
SELECT relname AS table_name,
  pg_size_pretty(pg_total_relation_size(c.oid)) AS total,
  pg_size_pretty(pg_relation_size(c.oid)) AS data,
  pg_size_pretty(pg_total_relation_size(c.oid) - pg_relation_size(c.oid)) AS indexes
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind = 'r'
ORDER BY pg_total_relation_size(c.oid) DESC
LIMIT 15;

-- Unused indexes (candidates for removal)
SELECT indexrelname, relname AS table_name,
       idx_scan AS times_used,
       pg_size_pretty(pg_relation_size(i.indexrelid)) AS size
FROM pg_stat_user_indexes i
JOIN pg_index USING (indexrelid)
WHERE idx_scan < 10 AND NOT indisunique
ORDER BY pg_relation_size(i.indexrelid) DESC
LIMIT 10;
```

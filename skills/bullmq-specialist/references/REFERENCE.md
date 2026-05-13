# BullMQ Reference Documentation

> Source: Context7 — `/taskforcesh/bullmq` + `/websites/bullmq_io`
> Generated: 2026-03-11

---

## Overview

BullMQ is a fast and robust Node.js queue system built on Redis, designed for modern microservice architectures to handle distributed job execution with features like job scheduling, retries, and concurrency control.

### Core Classes

BullMQ is built upon four fundamental classes:
- **Queue** — managing jobs: add new jobs, pause the queue, clean up old jobs, retrieve queue data
- **Worker** — consuming and processing jobs, marking them as completed or failed
- **QueueEvents** — listening for global job lifecycle events
- **FlowProducer** — creating parent-child job dependencies

### Key Features

- Minimal CPU usage due to a polling-free design
- Distributed job execution based on Redis
- LIFO and FIFO jobs
- Priorities
- Delayed jobs
- Scheduled and repeatable jobs according to cron specifications
- Retries of failed jobs
- Concurrency setting per worker
- Threaded (sandboxed) processing functions
- Automatic recovery from process crashes
- Parent-Child dependencies

---

## Workers

### Basic Worker

```typescript
import { Worker, Job } from 'bullmq';

const worker = new Worker(queueName, async (job: Job) => {
  // Optionally report some progress
  await job.updateProgress(42);

  // Optionally sending an object as progress
  await job.updateProgress({ foo: 'bar' });

  // Do something with job
  return 'some value';
});
```

### Worker with Concurrency, Rate Limiting, and Events

```typescript
import { Worker, Job } from 'bullmq';

const worker = new Worker('myQueue', async (job: Job) => {
  console.log(`Processing job ${job.id} with data:`, job.data);

  // Report progress (0-100 or custom object)
  await job.updateProgress(25);

  // Simulate work
  await doSomeWork(job.data);
  await job.updateProgress(75);

  // Return value will be stored in job.returnvalue
  return { processed: true, timestamp: Date.now() };
}, {
  connection: {
    host: 'localhost',
    port: 6379,
  },
  concurrency: 5,  // Process up to 5 jobs concurrently
  limiter: {       // Rate limiting: max 10 jobs per second
    max: 10,
    duration: 1000,
  },
});

// Listen to worker events
worker.on('completed', (job: Job, returnvalue: any) => {
  console.log(`Job ${job.id} completed with result:`, returnvalue);
});

worker.on('failed', (job: Job | undefined, error: Error) => {
  console.error(`Job ${job?.id} failed:`, error.message);
});

worker.on('progress', (job: Job, progress: number | object) => {
  console.log(`Job ${job.id} progress:`, progress);
});

worker.on('error', (err: Error) => {
  console.error('Worker error:', err);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  await worker.close();
});
```

### Worker Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `connection` | `ConnectionOptions` | Redis connection (host, port, etc.) |
| `concurrency` | `number` | Max concurrent jobs (default: 1) |
| `limiter` | `{ max, duration }` | Rate limiting config |
| `lockDuration` | `number` | Lock TTL in ms (default: 30000) |
| `stalledInterval` | `number` | Stalled check interval (default: 30000) |
| `maxStalledCount` | `number` | Max stalls before failure (default: 1) |
| `prefix` | `string` | Queue prefix (default: "bull") |
| `autorun` | `boolean` | Start processing immediately (default: true) |

---

## QueueEvents

```typescript
import { QueueEvents } from 'bullmq';

const queueEvents = new QueueEvents('Paint');

queueEvents.on('completed', ({ jobId, returnvalue }) => {
  // Called every time a job is completed by any worker.
});

queueEvents.on('failed', ({ jobId, failedReason }) => {
  // Called whenever a job is moved to failed by any worker.
});

queueEvents.on('progress', ({ jobId, data }) => {
  // jobId received a progress event
});
```

---

## Retry & Backoff Strategies

```typescript
import { Queue, Worker } from 'bullmq';

const queue = new Queue('retryable-jobs');

// Fixed backoff - retry after fixed delay each time
await queue.add('api-call',
  { endpoint: '/users' },
  {
    attempts: 5,
    backoff: {
      type: 'fixed',
      delay: 3000, // Wait 3 seconds between retries
    },
  }
);

// Exponential backoff - delay doubles each retry (1s, 2s, 4s, 8s...)
await queue.add('external-service',
  { url: 'https://api.example.com' },
  {
    attempts: 4,
    backoff: {
      type: 'exponential',
      delay: 1000, // Base delay: 1 second
    },
  }
);

// With jitter to prevent thundering herd
await queue.add('rate-limited-api',
  { data: 'test' },
  {
    attempts: 8,
    backoff: {
      type: 'exponential',
      delay: 2000,
      jitter: 0.5, // Random variance up to 50%
    },
  }
);
```

### Custom Backoff Strategy

```typescript
const worker = new Worker('retryable-jobs',
  async (job) => {
    const response = await callExternalAPI(job.data);
    if (response.status === 429) {
      throw new Error('Rate limited');
    }
    return response.data;
  },
  {
    connection: { host: 'localhost', port: 6379 },
    settings: {
      backoffStrategy: (attemptsMade: number, type: string, err: Error, job: Job) => {
        // Custom logic: longer delays for rate limit errors
        if (err.message === 'Rate limited') {
          return attemptsMade * 5000; // 5s, 10s, 15s...
        }
        // Return -1 to stop retrying
        if (err.message === 'Invalid credentials') {
          return -1;
        }
        // Default: linear backoff
        return attemptsMade * 1000;
      },
    },
  }
);
```

---

## Rate Limiting

### Global Rate Limiting

```typescript
import { Queue, Worker } from 'bullmq';

const queue = new Queue('rate-limited-queue');

// Worker with rate limiting: max 10 jobs per second
const worker = new Worker('rate-limited-queue',
  async (job) => {
    return await callRateLimitedAPI(job.data);
  },
  {
    connection: { host: 'localhost', port: 6379 },
    limiter: {
      max: 10,
      duration: 1000,
    },
  }
);
```

### Manual Rate Limiting Based on API Response

```typescript
const apiWorker = new Worker('api-queue',
  async (job) => {
    const response = await fetch(job.data.url);

    if (response.status === 429) {
      // API returned rate limit, pause worker
      const retryAfter = parseInt(response.headers.get('Retry-After') || '60');
      await apiWorker.rateLimit(retryAfter * 1000);
      // Throw special error to move job back to wait
      throw Worker.RateLimitError();
    }

    return await response.json();
  },
  {
    connection: { host: 'localhost', port: 6379 },
    limiter: { max: 1, duration: 500 }, // Required for manual rate limiting
  }
);

// Check if queue is rate limited
const ttl = await queue.getRateLimitTtl(10);
if (ttl > 0) {
  console.log(`Queue is rate limited for ${ttl}ms`);
}

// Manually remove rate limit
await queue.removeRateLimitKey();
```

---

## Repeatable / Scheduled Jobs

### Job Schedulers (Modern API)

```typescript
const { Queue, Worker } = require('bullmq');

const connection = { host: 'localhost', port: 6379 };
const myQueue = new Queue('my-repeatable-jobs', { connection });

// Repeat every 10 seconds
await myQueue.upsertJobScheduler(
  'repeat-every-10s',
  {
    every: 10000,
  },
  {
    name: 'every-job',
    data: { jobData: 'data' },
    opts: {},
  },
);

// Cron: Runs at 9:00 AM every Monday to Friday
await myQueue.upsertJobScheduler(
  'weekday-morning-job',
  {
    pattern: '0 0 9 * * 1-5',
  },
  {
    name: 'cron-job',
    data: { jobData: 'morning data' },
    opts: {},
  },
);

const worker = new Worker(
  'my-repeatable-jobs',
  async job => {
    console.log(`Processing job ${job.id} at ${new Date()}`);
  },
  { connection },
);
```

### Legacy Repeatable Jobs API

```typescript
import { Queue } from 'bullmq';

const myQueue = new Queue('Paint');

// Repeat job once every day at 3:15 (am)
await myQueue.add(
  'submarine',
  { color: 'yellow' },
  {
    repeat: {
      pattern: '0 15 3 * * *',
    },
  },
);

// Repeat job every 10 seconds but no more than 100 times
await myQueue.add(
  'bird',
  { color: 'bird' },
  {
    repeat: {
      every: 10000,
      limit: 100,
    },
  },
);
```

---

## Flows (Parent-Child Dependencies)

### FlowProducer with continueParentOnFailure

```typescript
const { FlowProducer } = require('bullmq');
const flow = new FlowProducer({ connection });

const originalTree = await flow.add({
  name: 'root-job',
  queueName: 'topQueueName',
  data: {},
  children: [
    {
      name: 'child-job-1',
      data: { idx: 0, foo: 'bar' },
      queueName: 'childrenQueueName',
      opts: { continueParentOnFailure: true },
    },
    {
      name: 'child-job-2',
      data: { idx: 1, foo: 'baz' },
      queueName: 'childrenQueueName',
    },
    {
      name: 'child-job-3',
      data: { idx: 2, foo: 'qux' },
      queueName: 'childrenQueueName',
    },
  ],
});

// Processor for the parent job
const processor = async (job) => {
  const failedChildren = await job.getFailedChildrenValues();
  const hasFailedChildren = Object.keys(failedChildren).length > 0;

  if (hasFailedChildren) {
    console.log(`Parent triggered by child failure(s):`, failedChildren);
    await job.removeUnprocessedChildren();
  } else {
    console.log(`All children completed successfully.`);
  }
};
```

---

## Telemetry / Observability

```typescript
import { Worker } from "bullmq";
import { BullMQOtel } from "bullmq-otel";

const worker = new Worker(
  "myQueue",
  async (job) => {
    console.log("processing job", job.id, job.attemptsMade);
    await new Promise(async (res) => {
      setTimeout(() => res({}), 200);
    });

    if (job.attemptsMade < 1) {
      throw new Error("This was an error");
    }

    return "my result value";
  },
  {
    name: "myWorker",
    connection: { host: "127.0.0.1", port: 6379 },
    telemetry: new BullMQOtel("simple-guide"),
    concurrency: 10,
  }
);
```

---

## Connection Configuration

### Redis Connection Options

```typescript
const connection = {
  host: 'localhost',
  port: 6379,
  password: 'your-password',
  db: 0,
  // maxRetriesPerRequest must be null for BullMQ
  maxRetriesPerRequest: null,
};

// Queue
const queue = new Queue('myQueue', { connection });

// Worker
const worker = new Worker('myQueue', processor, { connection });

// QueueEvents
const queueEvents = new QueueEvents('myQueue', { connection });

// FlowProducer
const flow = new FlowProducer({ connection });
```

### Important: IORedis maxRetriesPerRequest

BullMQ requires `maxRetriesPerRequest: null` when creating IORedis instances manually. Without this, IORedis will throw `MaxRetriesPerRequestError` after a few retries.

---

## Job Options Quick Reference

| Option | Type | Description |
|--------|------|-------------|
| `attempts` | `number` | Number of retry attempts |
| `backoff` | `{ type, delay, jitter? }` | Backoff strategy for retries |
| `delay` | `number` | Delay before job becomes active (ms) |
| `priority` | `number` | Job priority (lower = higher priority) |
| `lifo` | `boolean` | LIFO ordering instead of FIFO |
| `removeOnComplete` | `boolean \| number` | Remove job data on completion (or keep N) |
| `removeOnFail` | `boolean \| number` | Remove job data on failure (or keep N) |
| `repeat` | `{ pattern?, every?, limit? }` | Repeatable job config (legacy) |
| `jobId` | `string` | Custom job ID (deduplication) |
| `timestamp` | `number` | Job creation timestamp |

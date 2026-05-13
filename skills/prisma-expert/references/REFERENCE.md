<!-- Source: https://www.prisma.io/docs/llms-full.txt (llms-full.txt) -->
<!-- Downloaded: 2026-03-21 -->

# Prisma Documentation - Full Content Feed

This file contains the complete Prisma documentation in machine-readable format.
Includes both v7 (current) and v6 documentation.

---

# Introduction to Prisma (/docs)



[**Prisma ORM**](/orm) is an open-source ORM that provides fast, type-safe access to Postgres, MySQL, SQLite, and other databases, and runs smoothly across Node.js, Bun, and Deno.

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --db
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --db
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --db
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --db
    ```
  </CodeBlockTab>
</CodeBlockTabs>

[**Prisma Postgres**](/postgres) is a fully managed PostgreSQL database that scales to zero, integrates with [Prisma ORM](/orm) and [Prisma Studio](/studio), and includes a [generous free tier](https://www.prisma.io/pricing).

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx create-db
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx create-db
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx create-db
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun create-db
    ```
  </CodeBlockTab>
</CodeBlockTabs>

<Cards>
  <Card
    href="/prisma-orm/quickstart/prisma-postgres"
    title="Use Prisma Postgres"
    icon={<div className="text-primary"><svg xmlns="http://www.w3.org/2000/svg" width="159" height="195" viewBox="0 0 640 640" fill="none"><path d="M355.2 85C348.2 72.1 334.7 64 320 64C305.3 64 291.8 72.1 284.8 85L209.7 224L430.2 224L355.1 85zM123.3 384L516.6 384L456.1 272L183.7 272L123.2 384zM97.4 432L68.8 485C62.1 497.4 62.4 512.4 69.6 524.5C76.8 536.6 89.9 544 104 544L536 544C550.1 544 563.1 536.6 570.4 524.5C577.7 512.4 577.9 497.4 571.2 485L542.6 432L97.4 432z" fill="currentColor"/></svg></div>
}
  >
    **Need a database?** Get started with your favorite framework and Prisma Postgres.
  </Card>

  <Card href="/prisma-postgres/quickstart/prisma-orm" title="Bring your own database" icon={<Database className="text-primary" />}>
    **Already have a database?** Use Prisma ORM for a type-safe developer experience and automated migrations.
  </Card>
</Cards>


# Caching queries (/docs/accelerate/caching)



Prisma Accelerate provides global caching for read queries using TTL, Stale-While-Revalidate (SWR), or a combination of both. It's included as part of Prisma Postgres, but can also be used with your own database by enabling Accelerate in the [Prisma Data Platform](https://console.prisma.io?utm_source=docs) and [configuring it with your database](/accelerate/getting-started).


# Compare Accelerate (/docs/accelerate/compare)



Prisma Accelerate supports products that serve a global audience, with a global caching system and connection pool that spans multiple regions, providing consistent access to data with low latency no matter where your user (or your database) is located in the world.

The managed connection pool is designed to support serverless infrastructure, capable of handling high volumes of connections and adapting to traffic spikes with ease.

Explore how Prisma Accelerate compares to other global cache and connection pool solutions on the market, and discover what sets it apart.

What makes Accelerate unique? [#what-makes-accelerate-unique]

Prisma Accelerate is chosen and loved by many for a number of key reasons which make Accelerate unique:

* [**Query-Level policies**](/accelerate/compare#accelerate-global-cache): Accelerate is the only solution that offers query-level cache policies, allowing you to control the cache strategy for each query specifically. It is common to have some values that need to be cached for a long time, others that need caching for a short time, and some that should not be cached at all. With Accelerate you can do this, and even set different cache strategies per query.
* [**Global by default**](/accelerate/compare#accelerate-global-cache): Accelerate is globally distributed by default. You never need to worry about where a user is located with respect to your database location.
* [**Fully managed**](/accelerate/compare#management): You don't need to manage a server or worry about uptime. Accelerate is fully managed for you.
* [**Auto-scaling**](/accelerate/compare#performance): Accelerate automatically adjusts resources to match workload demands, providing fast and consistent performance during traffic spikes.

Accelerate global cache [#accelerate-global-cache]

Prisma Accelerate offers a powerful global cache, so you can serve data to your users at the edge — the closest point to where the users are located — no matter where your database is hosted. This not only speeds up the experience for users, but also reduces read load on your database as well by avoiding roundtrips.

|                                     | Accelerate | Hyperdrive | PlanetScale Boost |
| ----------------------------------- | ---------- | ---------- | ----------------- |
| **Fully Managed**                   | ✅          | ✅          | ✅                 |
| **Globally distributed edge infra** | ✅          | ✅          | ✅                 |
| **Control cache policy from code**  | ✅          | ❌          | ❌                 |
| **Query-level cache policies**      | ✅          | ❌          | ❌                 |
| **Postgres compatible**             | ✅          | ✅          | ❌                 |
| **MySQL compatible**                | ✅          | ❌          | ✅                 |
| **MongoDB compatible**              | ✅          | ❌          | ❌                 |
| **Automatic cache updates**         | ❌          | ❌          | ✅                 |

**Why are these important?**

* Since Accelerate extends the Prisma client, you can control caching policies directly from your codebase with just an extra line of code. Integration is seamless. Here is an example using the stale-while-revalidating caching strategy:
  ```jsx
  await prisma.user.findMany({
    cacheStrategy: {
      swr: 60,
    },
  });
  ```
* Query level cache policies are critical for serious applications, so that you can control which queries are cached, and the characteristics of the policy. You may want certain data in your app to be cached for several days, other data to be cached for a just a few minutes, and other data to be not cached at all. This is only possible with Prisma Accelerate.
* Automatic cache updates means that the cache is automatically updated when a change in the database occurs. With Accelerate, you are in control of how the cache is invalidated, using [various caching strategies](/accelerate/caching).

Accelerate connection pool [#accelerate-connection-pool]

Prisma Accelerate includes a globally hosted connection pooler, which allows you to handle peak loads without any problem. Using a connection pool is important especially for serverless infrastructure, which by nature is not able to control connection volume to the database on its own. Prisma Accelerate offers a fully managed, globally colocated option, which auto scales to support any workload.

Management [#management]

|                                | Accelerate | pgbouncer | pgcat | Digital Ocean (pgbouncer) | Neon (pgbouncer) | Supavisor | Hyperdrive |
| ------------------------------ | ---------- | --------- | ----- | ------------------------- | ---------------- | --------- | ---------- |
| **Fully managed**              | ✅          | ❌         | ❌     | 🟠                        | ✅                | ❌         | ✅          |
| **Globally distributed**       | ✅          | ❌         | ❌     | ❌                         | ❌                | ❌         | ✅          |
| **Integrated with ORM client** | ✅          | ❌         | ❌     | ❌                         | ❌                | ❌         | ❌          |
| **Authenticate with API key**  | ✅          | ❌         | ❌     | ❌                         | ❌                | ❌         | ❌          |
| **Redundancy**                 | ✅          | ❌         | ❌     | ❌                         | ❌                | ❌         | ❌          |

**Why are these important?**

* If you decide to manage a connection pooler yourself (eg. using pgbouncer or pgcat) you will also be responsible for managing its uptime. If the server crashes, your application may be down until you recover it. Accelerate, as a fully managed solution will be recovered for you transparently, in the unlikely case of any infrastructure issue.
* The hosted pgbouncer option on Digital Ocean is semi-managed, you will need to set it up in your Digital Ocean account, and ensure it is running smoothly at all times.
* Authenticating with an API key can be a helpful security measure, allowing you to decouple database credentials from application secrets. Easily rotate API keys as often as you like, without needing any credential changes in your database
* Redundancy is helpful in the unlikely scenario that your connection pool service goes down. With Accelerate, it is automatically and seamlessly handed over to another server and recovered without any interruption.

Performance [#performance]

|                                 | Accelerate | pgbouncer | pgcat | Digital Ocean (pgbouncer) | Neon (pgbouncer) | Supavisor | Hyperdrive |
| ------------------------------- | ---------- | --------- | ----- | ------------------------- | ---------------- | --------- | ---------- |
| **Auto scaling**                | ✅          | ❌         | ❌     | ❌                         | ❌                | ❌         | ❌          |
| **Globally distributed**        | ✅          | ❌         | ❌     | ❌                         | ❌                | ❌         | ✅          |
| **Optimized queries over HTTP** | ✅          | ❌         | ❌     | ❌                         | ❌                | ❌         | ✅          |
| **Isolated compute**            | ✅          | ❌         | ❌     | ❌                         | ❌                | ❌         | ❌          |

**Why are these important?**

* Accelerate will automatically scale up and down to suit your application workload, meaning you'll never run out of compute resource. Additionally, this provides important redundancy to protect against any single compute instance failing — in the unlikely event of an instance going down, Accelerate will automatically spawn a new instance.
* Cross-region TCP handshakes between the application server and PgBouncer or the database are costly and time-consuming. If connections are reused only at the PgBouncer layer, the TCP handshake and connection setup still consume unnecessary time on every single request, which undermines the efficiency of connection reuse. Prisma Accelerate improves this by leveraging HTTP, which is more efficient for connection management. It reduces the overhead associated with TCP handshakes, resulting in faster, more responsive interactions between your application and the database.
* Never worry about 'noisy neighbors' with isolated compute resources. Other customers never impact on your own performance.

Database Support [#database-support]

|                 | Accelerate | pgbouncer | pgcat | Digital Ocean (pgbouncer) | Neon (pgbouncer) | Supavisor | Hyperdrive |
| --------------- | ---------- | --------- | ----- | ------------------------- | ---------------- | --------- | ---------- |
| **PostgreSQL**  | ✅          | ✅         | ✅     | ✅                         | ✅                | ✅         | ✅          |
| **MySQL**       | ✅          | ❌         | ❌     | ❌                         | ❌                | ❌         | ❌          |
| **PlanetScale** | ✅          | ❌         | ❌     | ❌                         | ❌                | ❌         | ❌          |
| **CockroachDB** | ✅          | ❌         | ❌     | ❌                         | ❌                | ❌         | ❌          |
| **MongoDB**     | ✅          | ❌         | ❌     | ❌                         | ❌                | ❌         | ❌          |


# Connection Pooling (/docs/accelerate/connection-pooling)



Accelerate provides built-in connection pooling to efficiently manage database connections. It's included as part of [Prisma Postgres](/postgres), but you can also use it with your own database by enabling Accelerate in the [Prisma Data Platform](https://console.prisma.io?utm_source=docs) and [connecting it to your database](/accelerate/getting-started).
This page has moved, connection pooling in Prisma Accelerate is now documented in the [Prisma Postgres section](/postgres/database/connection-pooling).


# Evaluating (/docs/accelerate/evaluating)



Prisma Accelerate optimizes database interactions through advanced connection pooling and global edge caching. Its connection pooler is available in 16 regions and helps applications load-balance and scale database requests based on demand.

Considering the information above, we recommend evaluating Accelerate with high volume to see it perform under load.

How Accelerate's connection pool optimizes performance under load [#how-accelerates-connection-pool-optimizes-performance-under-load]

Prisma Accelerate employs a dynamic, serverless connection pooling infrastructure. When a request is made, a connection pool is quickly provisioned for the project in the region assigned while configuring Prisma Accelerate. This connection pool remains active, serving many additional requests while reusing established database connections. The connection pool will disconnect after a period of inactivity, so it’s important to evaluate Prisma Accelerate with a consistent stream of traffic.

**Key Benefits:**

* **Optimized Query Performance:** The serverless connection pooler adapts to the query load, ensuring the database connections are managed efficiently during peak demand.

  > Prisma Accelerate’s connection pooler cannot improve the performance of queries in the database. In scenarios where query performance is an issue, we recommend optimizing the Prisma query, applying indexes, or utilizing Accelerate’s edge caching.

* **Maximize Connection Reuse:** Executing a consistent volume of queries helps maintain active instances of Accelerate connection poolers. This increases connection reuse, ensuring faster response times for subsequent queries.

By understanding and harnessing this mechanism, you can ensure that your database queries perform consistently and efficiently at scale.

Evaluating Prisma Accelerate connection pooling performance [#evaluating-prisma-accelerate-connection-pooling-performance]

Below you will find an example of how to evaluate Prisma Accelerate using a sample model:

```prisma
model Notes {
  id        Int       @id @default(autoincrement())
  title     String
  createdAt DateTime  @default(now())
  updatedAt DateTime? @updatedAt
}
```

```typescript
import { PrismaClient } from "@prisma/client";
import { withAccelerate } from "@prisma/extension-accelerate";

const prisma = new PrismaClient().$extends(withAccelerate());

function calculateStatistics(numbers: number[]): {
  average: number;
  p50: number;
  p75: number;
  p99: number;
} {
  if (numbers.length === 0) {
    throw new Error("The input array is empty.");
  }

  // Sort the array in ascending order
  numbers.sort((a, b) => a - b);

  const sum = numbers.reduce((acc, num) => acc + num, 0);
  const count = numbers.length;

  const average = sum / count;
  const p50 = getPercentile(numbers, 50);
  const p75 = getPercentile(numbers, 75);
  const p99 = getPercentile(numbers, 99);

  return { average, p50, p75, p99 };
}

function getPercentile(numbers: number[], percentile: number): number {
  if (percentile <= 0 || percentile >= 100) {
    throw new Error("Percentile must be between 0 and 100.");
  }

  const index = (percentile / 100) * (numbers.length - 1);
  if (Number.isInteger(index)) {
    // If the index is an integer, return the corresponding value
    return numbers[index];
  } else {
    // If the index is not an integer, interpolate between two adjacent values
    const lowerIndex = Math.floor(index);
    const upperIndex = Math.ceil(index);
    const lowerValue = numbers[lowerIndex];
    const upperValue = numbers[upperIndex];
    const interpolationFactor = index - lowerIndex;
    return lowerValue + (upperValue - lowerValue) * interpolationFactor;
  }
}

async function main() {
  const timings = [];

  // fire a query before going to the loop
  await prisma.notes.findMany({
    take: 20,
  });

  // we recommend evaluating Prisma Accelerate with a large loop
  const LOOP_LENGTH = 10000;

  for (let i = 0; i < LOOP_LENGTH; i++) {
    const start = Date.now();
    await prisma.notes.findMany({
      take: 20,
    });

    timings.push(Date.now() - start);
  }

  const statistics = calculateStatistics(timings);
  console.log("Average:", statistics.average);
  console.log("P50:", statistics.p50);
  console.log("P75:", statistics.p75);
  console.log("P99:", statistics.p99);
}

main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch((e) => {
    await prisma.$disconnect();
    process.exit(1);
  });
```

Evaluating Prisma Accelerate caching performance [#evaluating-prisma-accelerate-caching-performance]

Prisma Accelerate’s edge cache is also optimized for a high volume of queries. The cache automatically optimizes for repeated queries. As a result, the cache hit rate will increase as the query frequency does. Adding a query result to the cache is also non-blocking, so a short burst of queries might not utilize the cache or a sustained load.

To evaluate Accelerate’s edge caching, you can modify the above script with the below:

```typescript
import { PrismaClient } from "@prisma/client";
import { withAccelerate } from "@prisma/extension-accelerate";

const prisma = new PrismaClient().$extends(withAccelerate());

function calculateStatistics(numbers: number[]): {
  average: number;
  p50: number;
  p75: number;
  p99: number;
} {
  if (numbers.length === 0) {
    throw new Error("The input array is empty.");
  }

  // Sort the array in ascending order
  numbers.sort((a, b) => a - b);

  const sum = numbers.reduce((acc, num) => acc + num, 0);
  const count = numbers.length;

  const average = sum / count;
  const p50 = getPercentile(numbers, 50);
  const p75 = getPercentile(numbers, 75);
  const p99 = getPercentile(numbers, 99);

  return { average, p50, p75, p99 };
}

function getPercentile(numbers: number[], percentile: number): number {
  if (percentile <= 0 || percentile >= 100) {
    throw new Error("Percentile must be between 0 and 100.");
  }

  const index = (percentile / 100) * (numbers.length - 1);
  if (Number.isInteger(index)) {
    // If the index is an integer, return the corresponding value
    return numbers[index];
  } else {
    // If the index is not an integer, interpolate between two adjacent values
    const lowerIndex = Math.floor(index);
    const upperIndex = Math.ceil(index);
    const lowerValue = numbers[lowerIndex];
    const upperValue = numbers[upperIndex];
    const interpolationFactor = index - lowerIndex;
    return lowerValue + (upperValue - lowerValue) * interpolationFactor;
  }
}

async function main() {
  const timings = [];

  // fire a query before going to the loop
  await prisma.notes.findMany({
    take: 20,
    cacheStrategy: {
      ttl: 30,
    },
  });

  // we recommend evaluating Prisma Accelerate with a large loop
  const LOOP_LENGTH = 10000;

  for (let i = 0; i < LOOP_LENGTH; i++) {
    const start = Date.now();
    await prisma.notes.findMany({
      take: 20,
      cacheStrategy: {
        ttl: 30,
      },
    });

    timings.push(Date.now() - start);
  }

  const statistics = calculateStatistics(timings);
  console.log("Average:", statistics.average);
  console.log("P50:", statistics.p50);
  console.log("P75:", statistics.p75);
  console.log("P99:", statistics.p99);
}

main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch((e) => {
    await prisma.$disconnect();
    process.exit(1);
  });
```


# Examples (/docs/accelerate/examples)



Here is a list of ready-to-run example projects that demonstrate how to use Prisma Accelerate:

| Demo                                                                                                                | Description                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [`nextjs-starter`](https://github.com/prisma/prisma-examples/tree/latest/accelerate/nextjs-starter)                 | A Next.js project using Prisma Accelerate's caching and connection pooling                                     |
| [`svelte-starter`](https://github.com/prisma/prisma-examples/tree/latest/accelerate/svelte-starter)                 | A SvelteKit project using Prisma Accelerate's caching and connection pooling                                   |
| [`solidstart-starter`](https://github.com/prisma/prisma-examples/tree/latest/accelerate/solidstart-starter)         | A Solidstart project using Prisma Accelerate's caching and connection pooling                                  |
| [`remix-starter`](https://github.com/prisma/prisma-examples/tree/latest/accelerate/remix-starter)                   | A Remix project using Prisma Accelerate's caching and connection pooling                                       |
| [`nuxt-starter`](https://github.com/prisma/prisma-examples/tree/latest/accelerate/nuxtjs-starter)                   | A Nuxt.js project using Prisma Accelerate's caching and connection pooling                                     |
| [`astro-starter`](https://github.com/prisma/prisma-examples/tree/latest/accelerate/astro-starter)                   | An Astro project using Prisma Accelerate's caching and connection pooling                                      |
| [`accelerate-hacker-news`](https://github.com/prisma/prisma-examples/tree/latest/accelerate/accelerate-hacker-news) | A simple Hacker News clone built with Prisma Accelerate, demonstrating the use of on-demand cache invalidation |
| [`prisma-accelerate-invalidation`](https://github.com/prisma/prisma-accelerate-invalidation)                        | An app demonstrating how long it takes to invalidate a cached query result using on-demand cache invalidation. |


# Getting started (/docs/accelerate/getting-started)



Prerequisites [#prerequisites]

To get started with Accelerate, you will need the following:

* A [Prisma Data Platform account](https://console.prisma.io)
* A project that uses [Prisma Client](/orm/prisma-client/setup-and-configuration/introduction) `4.16.1` or higher. If your project is using interactive transactions, you need to use `5.1.1` or higher. (We always recommend using the latest version of Prisma.)
* A hosted PostgreSQL, MySQL/MariaDB, PlanetScale, CockroachDB, or MongoDB database

1. Enable Accelerate [#1-enable-accelerate]

Navigate to your Prisma Data Platform project, choose an environment, and enable Accelerate by providing your database connection string and selecting the region nearest your database.

<CalloutContainer type="info">
  <CalloutDescription>
    If you require IP allowlisting or firewall configurations with trusted IP addresses, enable Static IP for enhanced security. Learn more on [how to enable static IP for Accelerate in the Platform Console](/accelerate/static-ip).
  </CalloutDescription>
</CalloutContainer>

2. Add Accelerate to your application [#2-add-accelerate-to-your-application]

2.1. Update your database connection string [#21-update-your-database-connection-string]

Once enabled, you'll be prompted to generate a connection string that you'll use to authenticate requests.

Replace your direct database URL with your new Accelerate connection string.

```bash title=".env"
# New Accelerate connection string with generated API_KEY
DATABASE_URL="prisma://accelerate.prisma-data.net/?api_key=__API_KEY__"

# Previous (direct) database connection string
# DATABASE_URL="postgresql://user:password@host:port/db_name?schema=public"
```

Prisma Client reads the `prisma://` URL from `DATABASE_URL` at runtime, while Prisma CLI commands use the connection string defined in `prisma.config.ts`.

Prisma Migrate and Introspection do not work with a `prisma://` connection string. In order to continue using these features add a new variable to the `.env` file named `DIRECT_DATABASE_URL` whose value is the direct database connection string:

```bash title=".env"
DATABASE_URL="prisma://accelerate.prisma-data.net/?api_key=__API_KEY__"
DIRECT_DATABASE_URL="postgresql://user:password@host:port/db_name?schema=public" # [!code ++]
```

Then point `prisma.config.ts` to the direct connection string:

```ts title="prisma.config.ts" showLineNumbers
import "dotenv/config";
import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  datasource: {
    url: env("DIRECT_DATABASE_URL"),
  },
});
```

Migrations and introspections will use the `directUrl` connection string rather than the one defined in `url` when this configuration is provided.

> `directUrl` is useful for you to carry out migrations and introspections. However, you don't need `directUrl` to use Accelerate in your application.

<CalloutContainer type="info">
  <CalloutDescription>
    If you are using Prisma with PostgreSQL, there is no need for `directUrl`, as Prisma Migrate and Introspection work with the `prisma+postgres://` connection string.
  </CalloutDescription>
</CalloutContainer>

2.2. Install the Accelerate Prisma Client extension [#22-install-the-accelerate-prisma-client-extension]

<CalloutContainer type="info">
  <CalloutDescription>
    💡 Accelerate requires [Prisma Client](/orm/prisma-client/setup-and-configuration/introduction) version `4.16.1` or higher and [`@prisma/extension-accelerate`](https://www.npmjs.com/package/@prisma/extension-accelerate) version `1.0.0` or higher.

    💡 Accelerate extension [`@prisma/extension-accelerate`](https://www.npmjs.com/package/@prisma/extension-accelerate) version `2.0.0` and above requires Node.js version `18` or higher.
  </CalloutDescription>
</CalloutContainer>

Install the latest version of Prisma Client and Accelerate Prisma Client extension

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npm install @prisma/client@latest @prisma/extension-accelerate
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm add @prisma/client@latest @prisma/extension-accelerate
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn add @prisma/client@latest @prisma/extension-accelerate
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bun add @prisma/client@latest @prisma/extension-accelerate
    ```
  </CodeBlockTab>
</CodeBlockTabs>

2.3. Generate Prisma Client for Accelerate [#23-generate-prisma-client-for-accelerate]

If you're using Prisma version `5.2.0` or greater, Prisma Client will automatically determine how it should connect to the database depending on the protocol in the database connection string. If the connection string in the `DATABASE_URL` starts with `prisma://`, Prisma Client will try to connect to your database using Prisma Accelerate.

When using Prisma Accelerate in long-running application servers, such as a server deployed on AWS EC2, you can generate the Prisma Client by executing the following command:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma generate
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma generate
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma generate
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma generate
    ```
  </CodeBlockTab>
</CodeBlockTabs>

When using Prisma Accelerate in a Serverless or an Edge application, we recommend you to run the following command to generate Prisma Client:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma generate --no-engine
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma generate --no-engine
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma generate --no-engine
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma generate --no-engine
    ```
  </CodeBlockTab>
</CodeBlockTabs>

The `--no-engine` flag prevents a Query Engine file from being included in the generated Prisma Client, this ensures the bundle size of your application remains small.

<CalloutContainer type="warning">
  <CalloutDescription>
    If your Prisma version is below `5.2.0`, generate Prisma Client with the `--accelerate` option:

    <CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
      <CodeBlockTabsList>
        <CodeBlockTabsTrigger value="npm">
          npm
        </CodeBlockTabsTrigger>

        <CodeBlockTabsTrigger value="pnpm">
          pnpm
        </CodeBlockTabsTrigger>

        <CodeBlockTabsTrigger value="yarn">
          yarn
        </CodeBlockTabsTrigger>

        <CodeBlockTabsTrigger value="bun">
          bun
        </CodeBlockTabsTrigger>
      </CodeBlockTabsList>

      <CodeBlockTab value="npm">
        ```bash
        npx prisma generate --accelerate
        ```
      </CodeBlockTab>

      <CodeBlockTab value="pnpm">
        ```bash
        pnpm dlx prisma generate --accelerate
        ```
      </CodeBlockTab>

      <CodeBlockTab value="yarn">
        ```bash
        yarn dlx prisma generate --accelerate
        ```
      </CodeBlockTab>

      <CodeBlockTab value="bun">
        ```bash
        bunx --bun prisma generate --accelerate
        ```
      </CodeBlockTab>
    </CodeBlockTabs>

    If your Prisma version is below `5.0.0`, generate Prisma Client with the `--data-proxy` option:

    <CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
      <CodeBlockTabsList>
        <CodeBlockTabsTrigger value="npm">
          npm
        </CodeBlockTabsTrigger>

        <CodeBlockTabsTrigger value="pnpm">
          pnpm
        </CodeBlockTabsTrigger>

        <CodeBlockTabsTrigger value="yarn">
          yarn
        </CodeBlockTabsTrigger>

        <CodeBlockTabsTrigger value="bun">
          bun
        </CodeBlockTabsTrigger>
      </CodeBlockTabsList>

      <CodeBlockTab value="npm">
        ```bash
        npx prisma generate --data-proxy
        ```
      </CodeBlockTab>

      <CodeBlockTab value="pnpm">
        ```bash
        pnpm dlx prisma generate --data-proxy
        ```
      </CodeBlockTab>

      <CodeBlockTab value="yarn">
        ```bash
        yarn dlx prisma generate --data-proxy
        ```
      </CodeBlockTab>

      <CodeBlockTab value="bun">
        ```bash
        bunx --bun prisma generate --data-proxy
        ```
      </CodeBlockTab>
    </CodeBlockTabs>
  </CalloutDescription>
</CalloutContainer>

2.4. Extend your Prisma Client instance with the Accelerate extension [#24-extend-your-prisma-client-instance-with-the-accelerate-extension]

Add the following to extend your existing Prisma Client instance with the Accelerate extension:

```ts
import { PrismaClient } from "@prisma/client";
import { withAccelerate } from "@prisma/extension-accelerate";

const prisma = new PrismaClient({
  accelerateUrl: process.env.DATABASE_URL,
}).$extends(withAccelerate());
```

If you are going to deploy to an edge runtime (like Cloudflare Workers, Vercel Edge Functions, Deno Deploy, or Supabase Edge Functions), use our edge client instead:

```ts
import { PrismaClient } from "@prisma/client/edge";
import { withAccelerate } from "@prisma/extension-accelerate";

const prisma = new PrismaClient({
  accelerateUrl: process.env.DATABASE_URL,
}).$extends(withAccelerate());
```

If VS Code does not recognize the `$extends` method, refer to [this section](/accelerate/more/faq#vs-code-does-not-recognize-the-extends-method) on how to resolve the issue.

Using the Accelerate extension with other extensions [#using-the-accelerate-extension-with-other-extensions]

Since [extensions are applied one after another](/orm/prisma-client/client-extensions#conflicts-in-combined-extensions), make sure you apply them in the correct order. Extensions cannot share behavior and the last extension applied takes precedence.

If you are using [Query Insights](/query-insights) in your application, make sure you apply it *before* the Accelerate extension. For example:

```ts
const prisma = new PrismaClient({
  accelerateUrl: process.env.DATABASE_URL,
})
  .$extends(withOptimize())
  .$extends(withAccelerate());
```

2.5. Use Accelerate in your database queries [#25-use-accelerate-in-your-database-queries]

The `withAccelerate` extension primarily does two things:

* Gives you access to the `cacheStrategy` field within each applicable model method that allows you to define a cache strategy per-query.
* Routes all of your queries through a connection pooler.

No cache strategy to only use connection pool [#no-cache-strategy-to-only-use-connection-pool]

If you simply want to take advantage of Accelerate's connection pooling feature without applying a cache strategy, you may run your query the same way you would have without Accelerate.

By enabling Accelerate and supplying the Accelerate connection string, your queries now use the connection pooler by default.

<CalloutContainer type="info">
  <CalloutDescription>
    As of Prisma version `5.2.0` you can use Prisma Studio with the Accelerate connection string.
  </CalloutDescription>
</CalloutContainer>

Invalidate the cache and keep your cached query results up-to-date [#invalidate-the-cache-and-keep-your-cached-query-results-up-to-date]

If your application requires real-time or near-real-time data, cache invalidation ensures that users see the most current data, even when using a large `ttl` (Time-To-Live) or `swr` (Stale-While-Revalidate) [cache strategy](/accelerate/caching). By invalidating your cache, you can bypass extended caching periods to show live data whenever it's needed.

For example, if a dashboard displays customer information and a customer’s contact details change, cache invalidation allows you to refresh only that data instantly, ensuring support staff always see the latest information without waiting for the cache to expire.

To invalidate a cached query result, you can add tags and then use the `$accelerate.invalidate` API.

<CalloutContainer type="info">
  <CalloutDescription>
    On-demand cache invalidation is available with our paid plans. For more details, please see our [pricing](https://www.prisma.io/pricing#accelerate).
  </CalloutDescription>
</CalloutContainer>

To invalidate the query below:

```ts
await prisma.user.findMany({
  where: {
    email: {
      contains: "alice@prisma.io",
    },
  },
  cacheStrategy: {
    swr: 60,
    ttl: 60,
    tags: ["emails_with_alice"], // [!code highlight]
  },
});
```

You need to provide the cache tag in the `$accelerate.invalidate` API:

```ts
try {
  await prisma.$accelerate.invalidate({
    // [!code highlight]
    tags: ["emails_with_alice"], // [!code highlight]
  }); // [!code highlight]
} catch (e) {
  if (e instanceof Prisma.PrismaClientKnownRequestError) {
    // The .code property can be accessed in a type-safe manner
    if (e.code === "P6003") {
      console.log("You've reached the cache invalidation rate limit. Please try again shortly.");
    }
  }
  throw e;
}
```


# Prisma Accelerate (/docs/accelerate)



[Prisma Accelerate](https://www.prisma.io/accelerate) is a fully managed global connection pool and caching layer for your existing database, enabling query-level cache policies directly from the Prisma ORM.

With 15+ global regions, the connection pool scales your app for a global audience, particularly for serverless deployments that risk connection timeouts during peak times.

Accelerate's global cache, hosted in 300+ locations, ensures a fast experience for users, regardless of your database's location.

You can configure query-level caching strategies directly in your code with Prisma ORM, making setup and tuning easy.

Together, the connection pool and cache allow you to scale effortlessly and handle traffic spikes without infrastructure concerns.

Supported databases [#supported-databases]

Accelerate works with the database you already have, whether it is publicly accessible, or via an IP allowlist.

* PostgreSQL
* MySQL
* MariaDB
* PlanetScale
* CockroachDB
* MongoDB

Getting started [#getting-started]

* [Getting started](/accelerate/getting-started) - Learn how to get up and running with Prisma Accelerate
* [Local development](/accelerate/local-development) - Learn how to use Prisma Accelerate in a development environment
* [Examples](/accelerate/examples) - Check out ready-to-run examples for Prisma Accelerate


# Local development (/docs/accelerate/local-development)



Prisma Accelerate efficiently scales production traffic with integrated connection pooling and a global database cache.

In development environments, you may want to use a local database to minimize expenses. Furthermore, you may consider extending Prisma Client with the Accelerate client extension once so that you can use a local database in development and a hosted database with Accelerate’s connection pooling and caching enabled. This eliminates the need for conditional logic to switch clients between development and production.

This guide will explain how to use Prisma Accelerate client extension in a development environment with a local database.

Using Prisma Accelerate client extension in development and production [#using-prisma-accelerate-client-extension-in-development-and-production]

<br />

<img alt="Using Prisma Accelerate client extension in development" src="/img/accelerate/accelerate-in-dev.png" width="2477" height="600" />

Accelerate does not work with a local database. However, in a development environment, you can still use Prisma Client with the Accelerate client extension. This setup will not provide Accelerate's connection pooling and caching features.

The following steps outline how to use Prisma ORM and Prisma Accelerate with a local PostgreSQL database.

1. Update the `DATABASE_URL` environment variable with your local database's connection string:

   ```bash
   DATABASE_URL="postgres://username:password@127.0.0.1:5432/localdb"
   ```

2. Generate a Prisma Client:

   <CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
     <CodeBlockTabsList>
       <CodeBlockTabsTrigger value="npm">
         npm
       </CodeBlockTabsTrigger>

       <CodeBlockTabsTrigger value="pnpm">
         pnpm
       </CodeBlockTabsTrigger>

       <CodeBlockTabsTrigger value="yarn">
         yarn
       </CodeBlockTabsTrigger>

       <CodeBlockTabsTrigger value="bun">
         bun
       </CodeBlockTabsTrigger>
     </CodeBlockTabsList>

     <CodeBlockTab value="npm">
       ```bash
       npx prisma generate
       ```
     </CodeBlockTab>

     <CodeBlockTab value="pnpm">
       ```bash
       pnpm dlx prisma generate
       ```
     </CodeBlockTab>

     <CodeBlockTab value="yarn">
       ```bash
       yarn dlx prisma generate
       ```
     </CodeBlockTab>

     <CodeBlockTab value="bun">
       ```bash
       bunx --bun prisma generate
       ```
     </CodeBlockTab>
   </CodeBlockTabs>

3. Set up Prisma Client with the Accelerate client extension:

   ```typescript
   import { PrismaClient } from "@prisma/client";
   import { withAccelerate } from "@prisma/extension-accelerate";

   const prisma = new PrismaClient().$extends(withAccelerate());
   ```

   > The extended instance of Prisma Client will use the local database. Hence, Prisma Accelerate will not be used in your development environment to respond to your Prisma Client queries.

<img alt="Using Prisma Accelerate client extension in production" src="/img/accelerate/accelerate-in-prod.png" width="2477" height="626" />

If an Accelerate connection string is used as the `DATABASE_URL` environment variable, Prisma Client will route your queries through Accelerate.

Using Prisma Accelerate locally in an edge function [#using-prisma-accelerate-locally-in-an-edge-function]

When using an edge function, e.g., [Vercel's edge runtime](https://vercel.com/docs/functions/runtimes/edge-runtime), for your development environment, update your Prisma Client import as follows:

```typescript
import { PrismaClient } from "@prisma/client/edge";
```

Generally, edge function environments lack native support for existing APIs enabling TCP-based database connections. Prisma Accelerate provides a connection string that allows querying your database over HTTP, a protocol supported in all edge runtimes.


# Static IP (/docs/accelerate/static-ip)



You can enable static IP for Accelerate when your security setup requires IP allowlisting or if you're implementing firewalls that only permit access from trusted IPs, ensuring controlled and secure database connections.

<img alt="Result of enabling static IP Accelerate with a database using IP allowlisting" src="/img/accelerate/result-of-adding-static-ip-to-accelerate.png" width="2960" height="1406" />

<CalloutContainer type="info">
  <CalloutDescription>
    To enable static IP support for Accelerate within an existing or a new project environment, your workspace will need to be on our Pro or Business plans. Take a look at the [pricing page](https://www.prisma.io/pricing#accelerate) for more information.
  </CalloutDescription>
</CalloutContainer>

Enable static IP in Accelerate [#enable-static-ip-in-accelerate]

You can opt-in to use static IP for Accelerate in the [Platform Console](https://pris.ly/pdp) in two ways:

1. When enabling Accelerate for your project environment: [#1-when-enabling-accelerate-for-your-project-environment]

1. Specify your database connection string and connection pool region.
2. Enable static IP by toggling the **Static IP** switch in the **Network restrictions** section.
3. Click on the **Enable Accelerate** button.

2. For projects already using Accelerate: [#2-for-projects-already-using-accelerate]

1. Navigate to the Accelerate **Settings** tab in the project environment.
2. Enable static IP by toggling the **Static IP** switch in the **Network restrictions** section.

Enabling static IP for Accelerate will provide you with a list of static IPv4 and IPv6 addresses.

Once you have these addresses, configure your database firewall to allow incoming connections only from these IPs and any other trusted IPs that need access to your database.

<CalloutContainer type="info">
  <CalloutDescription>
    Since you cannot enable static IP for an existing Accelerate-enabled environment, we recommend opting for static IP when enabling Accelerate in a new environment. Use the same database URL as your existing Accelerate environment to instantly access static IP support for Accelerate.
  </CalloutDescription>
</CalloutContainer>


# Build faster with Prisma + AI (/docs/ai)



In the era of AI, where code is increasingly written by agents, ensuring clarity, type safety, and reliable infrastructure is essential. With 5+ years of leadership in the TypeScript ecosystem, Prisma ORM and Prisma Postgres provide the proven foundation for AI-assisted development.

Get started [#get-started]

Run the following command to bootstrap your database with a prompt:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --prompt "Create a habit tracker application"
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --prompt "Create a habit tracker application"
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --prompt "Create a habit tracker application"
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --prompt "Create a habit tracker application"
    ```
  </CodeBlockTab>
</CodeBlockTabs>

AI Coding Tools [#ai-coding-tools]

Prisma ORM and Prisma Postgres integrate seamlessly with your AI coding tools. Check out our documentation with tips and tricks for working with Prisma in various AI editors.

* [Cursor](/ai/tools/cursor) - Define project-specific rules and use your schema as context to generate accurate queries and code.
* [Windsurf](/ai/tools/windsurf) - Automate your database workflows by generating schemas, queries, and seed data in this AI-powered editor.
* [Github Copilot](/ai/tools/github-copilot) - Get Prisma-aware code suggestions, run CLI commands from chat, and query the Prisma docs.
* [ChatGPT](/ai/tools/chatgpt) - Learn how to connect the Prisma MCP server to ChatGPT to manage your databases with natural language.

Agent Skills [#agent-skills]

AI agents often generate outdated Prisma v6 code. Install Prisma Skills to give your agent accurate, up-to-date v7 knowledge - CLI commands, Client API, upgrade guides, database setup, and Prisma Postgres workflows.

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx skills add prisma/skills
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx skills add prisma/skills
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx skills add prisma/skills
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun skills add prisma/skills
    ```
  </CodeBlockTab>
</CodeBlockTabs>

* [Available skills and setup](/ai/tools/skills) - See all available skills and learn how to install them.

MCP server [#mcp-server]

With Prisma's MCP server, your AI tool can take database actions on your behalf: Provisioning a new Prisma Postgres instance, creating database backups and executing SQL queries are just a few of its capabilities.

```json title="Integrate in AI tool"
{
  "mcpServers": {
    "Prisma-Remote": {
      "url": "https://mcp.prisma.io/mcp"
    }
  }
}
```

* [Capabilities and tools](/ai/tools/mcp-server#tools) - Discover all the tools that make up the capabilities of the Prisma MCP server.
* [Integrating in AI tools](/ai/tools/mcp-server#integrating-in-ai-tools) - Learn how to integrate Prisma's MCP server in your favorite AI tool, such as Cursor, Claude, Warp, and more.
* [How we built it](https://www.prisma.io/blog/about-mcp-servers-and-how-we-built-one-for-prisma) - Read this technical deep dive about the MCP protocol and how we built the Prisma MCP server.

Vibe Coding Tutorials [#vibe-coding-tutorials]

Build complete, production-ready applications from scratch with AI assistance.

* [Build a Linktree Clone SaaS](/ai/tutorials/linktree-clone) - A complete vibe coding tutorial: build a full Linktree clone SaaS with Next.js, Prisma Postgres, and Clerk auth using AI assistance.

Resources [#resources]

* [Vibe Coding with Limits](https://www.prisma.io/blog/vibe-coding-with-limits-how-to-build-apps-in-the-age-of-ai) - How to Build Apps in the Age of AI
* [Vibe Coding an E-commerce App](https://www.prisma.io/blog/vibe-coding-with-prisma-mcp-and-nextjs) - with Prisma MCP and Next.js
* [Integrating the Vercel AI SDK](/guides/integrations/ai-sdk) - in a Next.js application

Integrations [#integrations]

* [Automate with Pipedream](https://pipedream.com/apps/prisma-management-api) - Connect Prisma Postgres to 2,800+ apps for powerful automation
* [Firebase Studio](/guides/postgres/idx) - Prompt your application with Firebase Studio & Prisma Postgres


# debug (/docs/cli/debug)



The `prisma debug` command prints information helpful for debugging and bug reports.

<CalloutContainer type="info">
  <CalloutDescription>
    Available from version 5.6.0 and newer.
  </CalloutDescription>
</CalloutContainer>

Usage [#usage]

```bash
prisma debug [options]
```

Options [#options]

| Option         | Description                            |
| -------------- | -------------------------------------- |
| `-h`, `--help` | Display help message                   |
| `--config`     | Custom path to your Prisma config file |
| `--schema`     | Custom path to your Prisma schema      |

Examples [#examples]

Display debug information [#display-debug-information]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma debug
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma debug
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma debug
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma debug
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Output:

```text
-- Prisma schema --
Path: /prisma/schema.prisma

-- Local cache directory for engines files --
Path: /.cache/prisma

-- Environment variables --
When not set, the line is dimmed and no value is displayed.
When set, the line is bold and the value is inside the `` backticks.

For general debugging
 - CI:
 - DEBUG:
 - NODE_ENV:
 - RUST_LOG:
 - RUST_BACKTRACE:
 - NO_COLOR:
 - TERM: `xterm-256color`
 - NODE_TLS_REJECT_UNAUTHORIZED:
 - NO_PROXY:
 - http_proxy:
 - HTTP_PROXY:
 - https_proxy:
 - HTTPS_PROXY:

For hiding messages
 - PRISMA_DISABLE_WARNINGS:
 - PRISMA_HIDE_PREVIEW_FLAG_WARNINGS:
 - PRISMA_HIDE_UPDATE_MESSAGE:

For downloading engines
 - PRISMA_ENGINES_MIRROR:
 - PRISMA_BINARIES_MIRROR (deprecated):
 - PRISMA_ENGINES_CHECKSUM_IGNORE_MISSING:
 - BINARY_DOWNLOAD_VERSION:

For custom engines
 - PRISMA_SCHEMA_ENGINE_BINARY:
 - PRISMA_MIGRATION_ENGINE_BINARY:

For Prisma Client
 - PRISMA_SHOW_ALL_TRACES:

For Prisma Migrate
 - PRISMA_SCHEMA_DISABLE_ADVISORY_LOCK:

For Prisma Studio
 - BROWSER:

-- Terminal is interactive? --
true

-- CI detected? --
false
```

Use with older versions [#use-with-older-versions]

If using an older Prisma version:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma@latest debug
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma@latest debug
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma@latest debug
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma@latest debug
    ```
  </CodeBlockTab>
</CodeBlockTabs>


# format (/docs/cli/format)



The `prisma format` command formats your Prisma schema file. It validates, formats, and persists the schema.

Usage [#usage]

```bash
prisma format [options]
```

Options [#options]

| Option         | Description                            |
| -------------- | -------------------------------------- |
| `-h`, `--help` | Display help message                   |
| `--config`     | Custom path to your Prisma config file |
| `--schema`     | Custom path to your Prisma schema      |

Examples [#examples]

Format the default schema [#format-the-default-schema]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma format
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma format
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma format
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma format
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Output on success:

```text
Environment variables loaded from .env
Prisma schema loaded from prisma/schema.prisma
Formatted prisma/schema.prisma in 116ms
```

Format a specific schema [#format-a-specific-schema]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma format --schema=./alternative/schema.prisma
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma format --schema=./alternative/schema.prisma
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma format --schema=./alternative/schema.prisma
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma format --schema=./alternative/schema.prisma
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Error output [#error-output]

If the schema has validation errors, formatting will fail:

```text
Environment variables loaded from .env
Prisma schema loaded from prisma/schema.prisma
Error: Schema validation error - Error (query-engine-node-api library)
Error code: P1012
error: The preview feature "unknownFeatureFlag" is not known. Expected one of: [...]
  schema.prisma:3
   |
 2 |     provider        = "prisma-client"
 3 |     previewFeatures = ["unknownFeatureFlag"]
   |

Validation Error Count: 1
```


# generate (/docs/cli/generate)



The `prisma generate` command generates assets like Prisma Client based on the [`generator`](/orm/prisma-schema/overview/generators) and [`data model`](/orm/prisma-schema/data-model/models) blocks defined in your `schema.prisma` file.

Usage [#usage]

```bash
prisma generate [options]
```

How it works [#how-it-works]

1. Inspects the current directory to find a Prisma schema
2. Generates a customized Prisma Client based on your schema into the output directory specified in the generator block

Prerequisites [#prerequisites]

Add a generator definition in your `schema.prisma` file:

```prisma
generator client {
  provider = "prisma-client"
  output   = "./generated"
}
```

Options [#options]

| Option             | Description                                            |
| ------------------ | ------------------------------------------------------ |
| `-h`, `--help`     | Display help message                                   |
| `--config`         | Custom path to your Prisma config file                 |
| `--schema`         | Custom path to your Prisma schema                      |
| `--sql`            | Generate typed SQL module                              |
| `--watch`          | Watch the Prisma schema and regenerate after changes   |
| `--generator`      | Generator to use (can be provided multiple times)      |
| `--no-hints`       | Hide hint messages (still outputs errors and warnings) |
| `--require-models` | Do not allow generating a client without models        |

Examples [#examples]

Generate Prisma Client [#generate-prisma-client]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma generate
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma generate
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma generate
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma generate
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Output:

```text
✔ Generated Prisma Client to ./node_modules/.prisma/client in 61ms

You can now start using Prisma Client in your code:

import { PrismaClient } from '../prisma/generated/client'

const prisma = new PrismaClient()
```

Generate with a custom schema path [#generate-with-a-custom-schema-path]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma generate --schema=./alternative/schema.prisma
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma generate --schema=./alternative/schema.prisma
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma generate --schema=./alternative/schema.prisma
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma generate --schema=./alternative/schema.prisma
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Watch mode [#watch-mode]

Automatically regenerate when the schema changes:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma generate --watch
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma generate --watch
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma generate --watch
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma generate --watch
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Output:

```text
Watching... /home/prismauser/prisma/schema.prisma

✔ Generated Prisma Client to ./node_modules/.prisma/client in 45ms
```

Generate specific generators [#generate-specific-generators]

Run only specific generators:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma generate --generator client
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma generate --generator client
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma generate --generator client
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma generate --generator client
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Multiple generators:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma generate --generator client --generator zod_schemas
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma generate --generator client --generator zod_schemas
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma generate --generator client --generator zod_schemas
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma generate --generator client --generator zod_schemas
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Generated assets [#generated-assets]

The `prisma-client` generator creates a customized client for working with your database. You can [customize the output folder](/orm/reference/prisma-schema-reference#fields-for-prisma-client-provider) using the `output` field in the generator block.


# CLI Overview (/docs/cli)



The Prisma CLI provides commands for:

* **Project setup**: Initialize new Prisma projects
* **Code generation**: Generate Prisma Client and other artifacts
* **Database management**: Pull schemas, push changes, seed data
* **Migrations**: Create, apply, and manage database migrations
* **Development tools**: Local database servers, schema validation, formatting

Installation [#installation]

The Prisma CLI is available as an npm package. Install it as a development dependency:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npm install prisma --save-dev
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm add prisma --save-dev
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn add prisma --dev
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bun add prisma --dev
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Usage [#usage]

```bash
prisma [command]
```

Commands [#commands]

| Command                     | Description                                          |
| --------------------------- | ---------------------------------------------------- |
| [`init`](/cli/init)         | Set up Prisma for your app                           |
| [`dev`](/cli/dev)           | Start a local Prisma Postgres server for development |
| [`generate`](/cli/generate) | Generate artifacts (e.g. Prisma Client)              |
| [`db`](/cli/db)             | Manage your database schema and lifecycle            |
| [`migrate`](/cli/migrate)   | Migrate your database                                |
| [`studio`](/cli/studio)     | Browse your data with Prisma Studio                  |
| [`validate`](/cli/validate) | Validate your Prisma schema                          |
| [`format`](/cli/format)     | Format your Prisma schema                            |
| [`version`](/cli/version)   | Display Prisma version info                          |
| [`debug`](/cli/debug)       | Display Prisma debug info                            |
| [`mcp`](/cli/mcp)           | Start an MCP server to use with AI development tools |

Global flags [#global-flags]

These flags are available for all commands:

| Flag                | Description                         |
| ------------------- | ----------------------------------- |
| `--help`, `-h`      | Show help information for a command |
| `--preview-feature` | Run Preview Prisma commands         |

Using a HTTP proxy [#using-a-http-proxy]

Prisma CLI supports custom HTTP proxies. This is useful when behind a corporate firewall.

Set one of these environment variables:

* `HTTP_PROXY` or `http_proxy`: Proxy URL for HTTP traffic (e.g., `http://localhost:8080`)
* `HTTPS_PROXY` or `https_proxy`: Proxy URL for HTTPS traffic (e.g., `https://localhost:8080`)


# init (/docs/cli/init)



The `prisma init` command bootstraps a fresh Prisma project within the current directory.

Usage [#usage]

```bash
prisma init [options]
```

The command creates a `prisma` directory containing a `schema.prisma` file. By default, the project is configured for [local Prisma Postgres](/postgres/database/local-development), but you can choose a different database using the `--datasource-provider` option.

Options [#options]

| Option                  | Description                                                                                               |
| ----------------------- | --------------------------------------------------------------------------------------------------------- |
| `-h`, `--help`          | Display help message                                                                                      |
| `--db`                  | Provision a fully managed Prisma Postgres database on the Prisma Data Platform                            |
| `--datasource-provider` | Define the datasource provider: `postgresql`, `mysql`, `sqlite`, `sqlserver`, `mongodb`, or `cockroachdb` |
| `--generator-provider`  | Define the generator provider to use (default: `prisma-client-js`)                                        |
| `--preview-feature`     | Define a preview feature to use (can be specified multiple times)                                         |
| `--output`              | Define Prisma Client generator output path                                                                |
| `--url`                 | Define a custom datasource URL                                                                            |

Flags [#flags]

| Flag           | Description                                     |
| -------------- | ----------------------------------------------- |
| `--with-model` | Add an example model to the created schema file |

Examples [#examples]

Set up a new Prisma project (default) [#set-up-a-new-prisma-project-default]

Sets up a new project configured for local Prisma Postgres:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Specify a datasource provider [#specify-a-datasource-provider]

Set up a new project with MySQL as the datasource provider:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --datasource-provider mysql
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --datasource-provider mysql
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --datasource-provider mysql
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --datasource-provider mysql
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Specify a generator provider [#specify-a-generator-provider]

Set up a project with a specific generator provider:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --generator-provider prisma-client-js
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --generator-provider prisma-client-js
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --generator-provider prisma-client-js
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --generator-provider prisma-client-js
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Specify preview features [#specify-preview-features]

Set up a project with specific preview features enabled:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --preview-feature metrics
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --preview-feature metrics
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --preview-feature metrics
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --preview-feature metrics
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Multiple preview features:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --preview-feature views --preview-feature metrics
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --preview-feature views --preview-feature metrics
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --preview-feature views --preview-feature metrics
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --preview-feature views --preview-feature metrics
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Specify a custom output path [#specify-a-custom-output-path]

Set up a project with a custom output path for Prisma Client:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --output ./generated-client
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --output ./generated-client
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --output ./generated-client
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --output ./generated-client
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Specify a custom datasource URL [#specify-a-custom-datasource-url]

Set up a project with a specific database URL:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --url mysql://user:password@localhost:3306/mydb
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --url mysql://user:password@localhost:3306/mydb
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --url mysql://user:password@localhost:3306/mydb
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --url mysql://user:password@localhost:3306/mydb
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Add an example model [#add-an-example-model]

Set up a project with an example `User` model:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --with-model
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --with-model
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --with-model
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --with-model
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Provision a Prisma Postgres database [#provision-a-prisma-postgres-database]

Create a new project with a managed Prisma Postgres database:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --db
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --db
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --db
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --db
    ```
  </CodeBlockTab>
</CodeBlockTabs>

This requires authentication with the [Prisma Data Platform Console](https://console.prisma.io).

Generated files [#generated-files]

After running `prisma init`, you'll have the following files:

prisma/schema.prisma [#prismaschemaprisma]

The Prisma schema file where you define your data model:

```prisma
generator client {
  provider = "prisma-client"
  output   = "../generated/prisma"
}

datasource db {
  provider = "postgresql"
}
```

prisma.config.ts [#prismaconfigts]

A TypeScript configuration file for Prisma:

```typescript
import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: {
    path: "prisma/migrations",
  },
  datasource: {
    url: env("DATABASE_URL"),
  },
});
```

.env [#env]

Environment variables file for your project:

```bash
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
```

.gitignore [#gitignore]

Git ignore file configured for Prisma projects:

```bash
node_modules
.env
/generated/prisma
```


# mcp (/docs/cli/mcp)



The `prisma mcp` command starts a Model Context Protocol (MCP) server that enables AI development tools to interact with your Prisma project.

Usage [#usage]

```bash
prisma mcp
```

Overview [#overview]

MCP (Model Context Protocol) is a standard for AI tools to interact with development environments. The Prisma MCP server exposes your Prisma schema and database context to AI assistants, enabling them to:

* Understand your data model
* Generate queries and migrations
* Provide context-aware suggestions

See also [#see-also]

* [Prisma MCP Server](/ai/tools/mcp-server)


# studio (/docs/cli/studio)



The `prisma studio` command starts a local web server with a web app to interactively browse and manage your data.

Usage [#usage]

```bash
prisma studio [options]
```

<CalloutContainer type="info">
  <CalloutTitle>
    Supported databases
  </CalloutTitle>

  <CalloutDescription>
    Prisma Studio currently supports PostgreSQL, MySQL, and SQLite. Support for CockroachDB and MongoDB is not available yet but may be added in future releases.
  </CalloutDescription>
</CalloutContainer>

Prerequisites [#prerequisites]

Configure your database connection in `prisma.config.ts`:

```prisma file=schema.prisma
generator client {
  provider = "prisma-client"
  output   = "../generated/prisma"
}

datasource db {
  provider = "sqlite"
}
```

```typescript file=prisma.config.ts
import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: {
    path: "prisma/migrations",
  },
  datasource: {
    url: env("DATABASE_URL"),
  },
});
```

Options [#options]

| Option            | Description                                          | Default        |
| ----------------- | ---------------------------------------------------- | -------------- |
| `-h`, `--help`    | Display help message                                 |                |
| `-p`, `--port`    | Port number to start Studio on                       | `5555`         |
| `-b`, `--browser` | Browser to auto-open Studio in                       | System default |
| `--config`        | Custom path to your Prisma config file               |                |
| `--url`           | Database connection string (overrides Prisma config) |                |

Examples [#examples]

Start Studio on the default port [#start-studio-on-the-default-port]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma studio
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma studio
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma studio
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma studio
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Start Studio on a custom port [#start-studio-on-a-custom-port]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma studio --port 7777
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma studio --port 7777
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma studio --port 7777
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma studio --port 7777
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Start Studio in a specific browser [#start-studio-in-a-specific-browser]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma studio --browser firefox
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma studio --browser firefox
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma studio --browser firefox
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma studio --browser firefox
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Or using the `BROWSER` environment variable:

```bash
BROWSER=firefox prisma studio
```

Start Studio without opening a browser [#start-studio-without-opening-a-browser]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma studio --browser none
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma studio --browser none
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma studio --browser none
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma studio --browser none
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Start Studio with a custom config file [#start-studio-with-a-custom-config-file]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma studio --config=./prisma.config.ts
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma studio --config=./prisma.config.ts
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma studio --config=./prisma.config.ts
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma studio --config=./prisma.config.ts
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Start Studio with a direct database connection string [#start-studio-with-a-direct-database-connection-string]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma studio --url="postgresql://user:password@localhost:5432/dbname"
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma studio --url="postgresql://user:password@localhost:5432/dbname"
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma studio --url="postgresql://user:password@localhost:5432/dbname"
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma studio --url="postgresql://user:password@localhost:5432/dbname"
    ```
  </CodeBlockTab>
</CodeBlockTabs>


# validate (/docs/cli/validate)



The `prisma validate` command validates the [Prisma Schema Language](/orm/prisma-schema/overview) of your Prisma schema file.

Usage [#usage]

```bash
prisma validate [options]
```

Options [#options]

| Option         | Description                            |
| -------------- | -------------------------------------- |
| `-h`, `--help` | Display help message                   |
| `--config`     | Custom path to your Prisma config file |
| `--schema`     | Custom path to your Prisma schema      |

Examples [#examples]

Validate the default schema [#validate-the-default-schema]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma validate
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma validate
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma validate
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma validate
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Output on success:

```text
Environment variables loaded from .env
Prisma schema loaded from prisma/schema.prisma
The schema at /absolute/path/prisma/schema.prisma is valid
```

Validate a specific schema [#validate-a-specific-schema]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma validate --schema=./alternative/schema.prisma
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma validate --schema=./alternative/schema.prisma
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma validate --schema=./alternative/schema.prisma
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma validate --schema=./alternative/schema.prisma
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Validate with a config file [#validate-with-a-config-file]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma validate --config=./prisma.config.ts
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma validate --config=./prisma.config.ts
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma validate --config=./prisma.config.ts
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma validate --config=./prisma.config.ts
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Error output [#error-output]

If the schema has validation errors:

```text
Environment variables loaded from .env
Prisma schema loaded from prisma/schema.prisma
Error: Schema validation error - Error (query-engine-node-api library)
Error code: P1012
error: The preview feature "unknownFeatureFlag" is not known. Expected one of: [...]
  schema.prisma:3
   |
 2 |     provider        = "prisma-client"
 3 |     previewFeatures = ["unknownFeatureFlag"]
   |

Validation Error Count: 1
```


# version (/docs/cli/version)



The `prisma version` command outputs information about your current Prisma version, platform, and engine binaries.

Usage [#usage]

```bash
prisma version [options]
```

Or use the shorthand:

```bash
prisma -v [options]
```

Options [#options]

| Option         | Description                               |
| -------------- | ----------------------------------------- |
| `-h`, `--help` | Display help message                      |
| `--json`       | Output version information in JSON format |

Examples [#examples]

Display version information [#display-version-information]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma version
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma version
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma version
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma version
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Output:

```text
Environment variables loaded from .env
prisma               : 2.21.0-dev.4
@prisma/client       : 2.21.0-dev.4
Current platform     : windows
Query Engine         : query-engine 2fb8f444d9cdf7c0beee7b041194b42d7a9ce1e6
Migration Engine     : migration-engine-cli 2fb8f444d9cdf7c0beee7b041194b42d7a9ce1e6
Format Binary        : prisma-fmt 60ba6551f29b17d7d6ce479e5733c70d9c00860e
Default Engines Hash : 60ba6551f29b17d7d6ce479e5733c70d9c00860e
Studio               : 0.365.0
```

Display version using shorthand [#display-version-using-shorthand]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma -v
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma -v
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma -v
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma -v
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Display version as JSON [#display-version-as-json]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma version --json
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma version --json
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma version --json
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma version --json
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Output:

```json
{
  "prisma": "2.21.0-dev.4",
  "@prisma/client": "2.21.0-dev.4",
  "current-platform": "windows",
  "query-engine": "query-engine 60ba6551f29b17d7d6ce479e5733c70d9c00860e",
  "migration-engine": "migration-engine-cli 60ba6551f29b17d7d6ce479e5733c70d9c00860e",
  "format-binary": "prisma-fmt 60ba6551f29b17d7d6ce479e5733c70d9c00860e",
  "default-engines-hash": "60ba6551f29b17d7d6ce479e5733c70d9c00860e",
  "studio": "0.365.0"
}
```


# Concepts (/docs/console/concepts)



The Console workflows are based on four main concepts:

* [**User account**](#user-account): In order to use Prisma products, you need to have a Console user account. A *user* will typically create one user account to manage all their workspaces, projects and resources. The *user* can also be invited to join other workspaces to collaborate on the projects in that workspace.
* [**Workspaces**](#workspace): A user account can belong to multiple workspaces. A workspace typically represents a *team* of individuals working together on one or more projects. **Billing is on a workspace level**, i.e. the invoice for a workspace at the end of the month captures all costs associated with the projects in that workspace.
* [**Projects**](#project): A project belongs to a workspace. It typically represents the *application* or *service* a team is working on.
* [**Resources**](#resources): Resources represent the actual services or databases within a project. For example, in Prisma Postgres, each project can contain multiple databases. For Accelerate, resources might correspond to different environments (like `Development`, `Staging`, or `Production`). **Connection strings are provisioned at the resource level**, and products are configured per resource as well (e.g., the database connection string used for Accelerate).

Here is a visual illustration of how these concepts relate to each other:

<img alt="How the concepts of the Console (user account, workspaces, projects, and resources) relate to each other" src="/img/platform/pdp-concepts.png" width="1480" height="1127" />

User account [#user-account]

A user account is the prerequisite for any interactions with Prisma products. You can use it to manage your workspaces (and their projects). A user account can be invited to collaborate on workspaces created by other users as well.

If you need to delete your user account, go [here](/console/more/support#deleting-your-pdp-account).

Workspace [#workspace]

You can create several workspaces. A workspace is an isolated space to host projects. A workspace can have multiple user accounts associated with it so that multiple users can collaborate on the projects in the workspace.

In each workspace, you can:

* view and manage all projects (and their resources) in that workspace.
* manage billing, i.e. select a [subscription plan](https://www.prisma.io/pricing?utm_source=docs\&utm_medium=platform-docs), configure payment methods, or view the invoice history.
* view the usage of your enabled Prisma products across all projects in that workspace.
* invite other users to collaborate in the workspace.
* access the [Optimize dashboard](https://console.prisma.io/optimize?utm_source=docs\&utm_medium=optimize-docs) to measure query performance and receive AI-powered recommendations.

CLI commands [#cli-commands]

List all workspaces:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform workspace show --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform workspace show --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform workspace show --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform workspace show --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Project [#project]

In each workspace, you can create several projects. A project typically represents an application (a product or service). You typically have one [Prisma schema](/orm/prisma-schema/overview) per project.

In each project, you can:

* view and manage all resources (like databases) in that project.

The number of projects you can create in a workspace depends on the [subscription plan](https://www.prisma.io/pricing?utm_source=docs\&utm_medium=platform-docs) configured in that workspace.

CLI commands [#cli-commands-1]

List all projects in a workspace:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform project show --workspace $WORKSPACE_ID --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform project show --workspace $WORKSPACE_ID --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform project show --workspace $WORKSPACE_ID --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform project show --workspace $WORKSPACE_ID --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Create a new project:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform project create --workspace $WORKSPACE_ID --name "My Project" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform project create --workspace $WORKSPACE_ID --name "My Project" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform project create --workspace $WORKSPACE_ID --name "My Project" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform project create --workspace $WORKSPACE_ID --name "My Project" --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Delete a project:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform project delete --project $PROJECT_ID --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform project delete --project $PROJECT_ID --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform project delete --project $PROJECT_ID --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform project delete --project $PROJECT_ID --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Resources [#resources]

Resources represent the actual services or databases within a project. The type of resources available depends on the Prisma products you're using:

* **For Prisma Postgres**: Each project can contain multiple databases. These databases are the primary resources you'll manage.
* **For Accelerate**: Resources typically correspond to different deployment stages (like `Development`, `Staging`, or `Production`).

In each project, you can:

* Create and manage multiple resources (databases or environments)
* Generate connection strings specific to each resource
* Configure product-specific settings:
  * **For Prisma Postgres databases**:
    * View database metrics and performance
    * Configure connection settings
    * Manage database users and permissions
  * **For Accelerate resources**:
    * Set your database connection string
    * Configure the region for connection pooling
    * Adjust connection pool size and performance settings
    * Set query duration and response size limits
    * Enable static IP for secure connections

The number of resources you can create in a project depends on your [subscription plan](https://www.prisma.io/pricing?utm_source=docs\&utm_medium=platform-docs).

CLI commands [#cli-commands-2]

List all environments (resources) in a project:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform environment show --project $PROJECT_ID --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform environment show --project $PROJECT_ID --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform environment show --project $PROJECT_ID --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform environment show --project $PROJECT_ID --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Create a new environment:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform environment create --project $PROJECT_ID --name "production" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform environment create --project $PROJECT_ID --name "production" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform environment create --project $PROJECT_ID --name "production" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform environment create --project $PROJECT_ID --name "production" --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Delete an environment:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform environment delete --environment $ENVIRONMENT_ID --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform environment delete --environment $ENVIRONMENT_ID --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform environment delete --environment $ENVIRONMENT_ID --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform environment delete --environment $ENVIRONMENT_ID --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>


# Getting Started (/docs/console/getting-started)



This guide walks you through setting up your Console account and creating your first project.

Prerequisites [#prerequisites]

* A GitHub account (for authentication)
* A Prisma project (optional, but recommended)

Step 1: Create your account [#step-1-create-your-account]

1. Go to [console.prisma.io/login](https://console.prisma.io/login)
2. Click **Sign in with GitHub**
3. Authorize Prisma Console to access your GitHub account

You now have a Console account with a default workspace.

Step 2: Set up a workspace [#step-2-set-up-a-workspace]

When you create an account, a default workspace is automatically created for you. You can create additional workspaces for different teams or organizations.

Create a workspace (optional) [#create-a-workspace-optional]

To create an additional workspace:

1. Click the workspace dropdown in the top navigation
2. Click **Create Workspace**
3. Enter a name for your workspace
4. Click **Create**

Using the CLI [#using-the-cli]

List all workspaces:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform workspace show --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform workspace show --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform workspace show --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform workspace show --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Step 3: Create a project [#step-3-create-a-project]

Projects organize your databases and environments within a workspace.

Using the Console web interface [#using-the-console-web-interface]

1. Navigate to your workspace
2. Click **Create Project**
3. Enter a project name
4. Click **Create**

Using the CLI [#using-the-cli-1]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform project create --workspace $WORKSPACE_ID --name "My Project" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform project create --workspace $WORKSPACE_ID --name "My Project" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform project create --workspace $WORKSPACE_ID --name "My Project" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform project create --workspace $WORKSPACE_ID --name "My Project" --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Step 4: Create a resource [#step-4-create-a-resource]

Resources are the actual databases or environments within your project.

For Prisma Postgres [#for-prisma-postgres]

1. Navigate to your project
2. Click **Create Database**
3. Enter a database name
4. Select a region
5. Click **Create**

For Accelerate [#for-accelerate]

1. Navigate to your project
2. Click **Create Environment**
3. Enter an environment name (e.g., "production")
4. Click **Create**

Using the CLI [#using-the-cli-2]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform environment create --project $PROJECT_ID --name "production" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform environment create --project $PROJECT_ID --name "production" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform environment create --project $PROJECT_ID --name "production" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform environment create --project $PROJECT_ID --name "production" --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Step 5: Generate a connection string [#step-5-generate-a-connection-string]

Connection strings authenticate your application's requests to Prisma products.

Using the Console web interface [#using-the-console-web-interface-1]

1. Navigate to your resource (database or environment)
2. Click **Connection Strings** tab
3. Click **Create Connection String**
4. Enter a name for the connection string
5. Copy the connection string and store it securely
6. Click **Done**

Using the CLI [#using-the-cli-3]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform apikey create --environment $ENVIRONMENT_ID --name "production-key" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform apikey create --environment $ENVIRONMENT_ID --name "production-key" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform apikey create --environment $ENVIRONMENT_ID --name "production-key" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform apikey create --environment $ENVIRONMENT_ID --name "production-key" --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Step 6: Use the connection string in your application [#step-6-use-the-connection-string-in-your-application]

Add the connection string to your `.env` file:

```bash
# For Accelerate
DATABASE_URL="prisma://accelerate.prisma-data.net/?api_key=YOUR_API_KEY"

# For Optimize
OPTIMIZE_API_KEY="YOUR_API_KEY"
```

Next steps [#next-steps]

* Learn more about [Console concepts](/console/concepts)
* Explore [database metrics](/console/features/metrics)
* Check out the [CLI reference](/cli/console)


# Console (/docs/console)



Overview [#overview]

The [Console](https://console.prisma.io/login) enables you to manage and configure your projects that use Prisma products, and helps you integrate them into your application:

* [Query Insights](/query-insights): Inspect slow queries, connect Prisma calls to SQL, and apply focused fixes.
* [Prisma Postgres](/postgres): A managed PostgreSQL database that is optimized for Prisma ORM.

Getting started [#getting-started]

To start using Prisma products, you'll need to:

1. Create a Console account
2. Set up a workspace for your team
3. Create a project for your application
4. Generate connection strings for your resources

Learn more in the [Getting Started](/console/getting-started) guide.

Core concepts [#core-concepts]

The Console is organized around four main concepts:

* **[User account](/console/concepts#user-account)**: Your personal account to manage workspaces and projects
* **[Workspaces](/console/concepts#workspace)**: Team-level container where billing is managed
* **[Projects](/console/concepts#project)**: Application-level container within a workspace
* **[Resources](/console/concepts#resources)**: Actual services or databases within a project (databases for Prisma Postgres)

Read more about [Console concepts](/console/concepts).

Console CLI [#console-cli]

In addition to the web interface, the Prisma CLI provides another way to interact with your Console account and manage Prisma products. This can be useful for programmatic access, such as integrating into CI workflows.

Learn more about the [Console CLI commands](/cli/console).


# Guides (/docs/guides)



Welcome to the Guides section! Here you'll find practical, step-by-step guides to help you accomplish specific tasks with Prisma products, including Prisma ORM, Prisma Accelerate, Prisma Postgres, and more.

Browse through our guides using the sidebar navigation or use the search to find specific topics.

Getting started [#getting-started]

* [Next.js](/guides/frameworks/nextjs) - Learn how to use Prisma ORM in a Next.js app and deploy it to Vercel
* [Hono](/guides/frameworks/hono) - Learn how to use Prisma ORM in a Hono app
* [SvelteKit](/guides/frameworks/sveltekit) - Learn how to use Prisma ORM in a SvelteKit app


# Writing guides (/docs/guides/making-guides)



Introduction [#introduction]

This guide shows you how to write guides for Prisma ORM documentation. It covers the required structure, formatting, and style conventions to ensure consistency across all guides. You'll learn about frontmatter requirements, section organization, and writing style.

Prerequisites [#prerequisites]

Before writing a guide, make sure you have:

* A clear understanding of the topic you're writing about
* Access to the Prisma documentation repository
* Familiarity with Markdown and MDX
* Knowledge of the target audience for your guide

Guide structure [#guide-structure]

Required frontmatter [#required-frontmatter]

Every guide must include the following frontmatter at the top of the file:

```mdx
---
title: '[Descriptive title]'
description: '[One-sentence summary of what the guide covers]'
---
```

* `title`: A clear, descriptive title (e.g., "Next.js", "Multiple databases", "GitHub Actions")
* `description`: A one-sentence summary that describes what you'll learn or accomplish
* `image`: A unique header image for social media sharing (coordinate with the design team)

All frontmatter fields should use sentence case.

Required sections [#required-sections]

1. **Introduction** (H2: `##`)
   * Brief overview of what the guide covers
   * What the reader will learn/accomplish
   * Link to any example repositories or related resources on GitHub

2. **Prerequisites** (H2: `##`)
   * Required software/tools with version numbers (e.g., "Node.js 20+")
   * Required accounts (e.g., "A Prisma Data Platform account")
   * Keep it concise - only list what's truly necessary

3. **Main content sections** (H2: `##`)
   * Use numbered steps (e.g., "## 1. Set up your project", "## 2. Install and Configure Prisma")
   * Use numbered subsections (e.g., "### 2.1. Install dependencies", "### 2.2. Define your Prisma Schema")
   * Each step should build on previous steps
   * Include all commands and code snippets needed

4. **Next steps** (H2: `##`)
   * What to do after completing the guide
   * Related guides or documentation (with links)
   * Additional resources

Writing style and voice [#writing-style-and-voice]

General principles [#general-principles]

* Write in a clear, conversational tone
* Use active voice and present tense
* Address the reader directly using "you" (e.g., "You'll learn how to...")
* Avoid jargon and explain technical terms when necessary
* Be concise but thorough
* Guide readers step-by-step through the process

Code examples [#code-examples]

* Include complete, runnable code examples
* Use syntax highlighting with language specification
* Include file paths in code block metadata using `title=`
* Use ` ```bash title=".env" ` for `.env` files so inline `# [!code ++]`, `# [!code --]`, and `# [!code highlight]` annotations render correctly
* Reserve ` ```text ` for other plain-text files that do not need Fumadocs code annotations
* Use comments sparingly - only when needed to explain complex logic
* Use ` ```npm ` for package manager commands (auto-converts to pnpm/yarn/bun)
* Use ` ```bash ` for shell commands and `.env` files
* Use ` ```text ` for other plain text files
* Use ` ```typescript `, ` ```prisma `, ` ```json ` for respective languages

Example with file path:

```typescript title="src/lib/prisma.ts"
import { PrismaClient } from "../generated/prisma";
import { PrismaPg } from "@prisma/adapter-pg";

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL!,
});

const prisma = new PrismaClient({
  adapter,
});

export default prisma;
```

Example showing changes:

```typescript title="prisma.config.ts"
import "dotenv/config"; // [!code ++]
import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: {
    path: "prisma/migrations",
  },
  datasource: {
    url: env("DATABASE_URL"),
  },
});
```

Formatting conventions [#formatting-conventions]

* Use backticks for inline code:
  * File names: `` `schema.prisma` ``
  * Directory names: `` `prisma/` ``
  * Code elements: `` `PrismaClient` ``
  * Package manager commands: Use ` ```npm ` blocks (see [Package manager commands](#package-manager-commands))
* Use admonitions for important information:
  ```markdown
  :::info
  Context or background information
  :::

  :::note
  Important details to remember
  :::

  :::warning
  Critical information or gotchas
  :::

  :::tip
  Helpful suggestions or best practices
  :::
  ```
* Use proper heading hierarchy (never skip levels)
* Use numbered sections (e.g., "## 1. Setup", "### 1.1. Install")
* Link to other documentation pages using relative paths (e.g., `[Database drivers](/orm/core-concepts/supported-databases/database-drivers)`)

Guide categories [#guide-categories]

| Category            | Directory                      | Description                         | Examples                                                                                                                                                                              |
| ------------------- | ------------------------------ | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Framework**       | `guides/frameworks/`           | Integrate Prisma with frameworks    | [Next.js](/guides/frameworks/nextjs), [NestJS](/guides/frameworks/nestjs), [SvelteKit](/guides/frameworks/sveltekit)                                                                  |
| **Deployment**      | `guides/deployment/`           | Deploy apps and set up monorepos    | [Turborepo](/guides/deployment/turborepo), [Cloudflare Workers](/guides/deployment/cloudflare-workers)                                                                                |
| **Integration**     | `guides/integrations/`         | Use Prisma with platforms and tools | [GitHub Actions](/guides/integrations/github-actions), [Supabase](/guides/integrations/supabase-accelerate)                                                                           |
| **Database**        | `guides/database/`             | Database patterns and migrations    | [Multiple databases](/guides/database/multiple-databases), [Data migration](/guides/database/data-migration)                                                                          |
| **Authentication**  | `guides/authentication/`       | Authentication patterns with Prisma | [Auth.js + Next.js](/guides/authentication/authjs/nextjs), [Better Auth + Next.js](/guides/authentication/better-auth/nextjs), [Clerk + Next.js](/guides/authentication/clerk/nextjs) |
| **Prisma Postgres** | `guides/postgres/`             | Prisma Postgres features            | [Vercel](/guides/postgres/vercel), [Netlify](/guides/postgres/netlify), [Viewing data](/guides/postgres/viewing-data)                                                                 |
| **Migration**       | `guides/switch-to-prisma-orm/` | Switch from other ORMs              | [From Mongoose](/guides/switch-to-prisma-orm/from-mongoose), [From Drizzle](/guides/switch-to-prisma-orm/from-drizzle)                                                                |

Common patterns [#common-patterns]

Package manager commands [#package-manager-commands]

Use ` ```npm ` code blocks for package manager commands. These automatically convert to other package managers (pnpm, yarn, bun) in the UI:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npm install prisma --save-dev
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm add prisma --save-dev
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn add prisma --dev
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bun add prisma --dev
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Environment variables [#environment-variables]

Show `.env` file examples using ` ```bash title=".env" ` blocks:

```bash title=".env"
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
```

If you need to show changes in an `.env` file, use bash comments for the Fumadocs annotations:

```bash title=".env"
DATABASE_URL="postgresql://user:password@localhost:5432/mydb" # [!code --]

DATABASE_URL="postgresql://user:password@db.example.com:5432/mydb" # [!code ++]
```

Database provider compatibility [#database-provider-compatibility]

Include an info admonition when commands or code are PostgreSQL-specific:

```markdown
:::info

If you are using a different database provider (MySQL, SQL Server, SQLite), install the corresponding driver adapter package instead of `@prisma/adapter-pg`. For more information, see [Database drivers](/orm/core-concepts/supported-databases/database-drivers).

:::
```

Prisma Client instantiation [#prisma-client-instantiation]

Show the standard pattern for creating a Prisma Client with database adapters:

```typescript title="lib/prisma.ts"
import { PrismaClient } from "../generated/prisma";
import { PrismaPg } from "@prisma/adapter-pg";

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL!,
});

const prisma = new PrismaClient({
  adapter,
});

export default prisma;
```

Include a warning about connection pooling:

```markdown
:::warning
We recommend using a connection pooler (like [Prisma Accelerate](https://www.prisma.io/accelerate)) to manage database connections efficiently.
:::
```

Best practices [#best-practices]

1. **Keep it focused**
   * Each guide should cover one main topic
   * Break complex topics into multiple guides
   * Link to related guides instead of duplicating content

2. **Show don't tell**
   * Include practical, real-world examples
   * Provide complete, working code samples
   * Explain why certain approaches are recommended

3. **Consider the context**
   * Explain prerequisites clearly
   * Don't assume prior knowledge
   * Link to foundational concepts within or outside of our docs when needed

4. **Maintain consistency**
   * Follow the established guide structure
   * Use consistent terminology
   * Match the style of existing guides

5. **Think about maintenance**
   * Use version numbers where appropriate
   * Avoid time-sensitive references
   * Consider future updates when structuring content

Guide template [#guide-template]

Use this template as a starting point for new guides. The template includes common sections and patterns used across Prisma guides.

Basic template structure [#basic-template-structure]

Copy this template for a new guide:

````markdown
---
title: '[Your guide title]'
description: '[One-sentence summary of what you'll learn]'
image: '/img/guides/[guide-name]-cover.png'
---

## Introduction

[Brief overview of what this guide covers and what you'll accomplish. Include a link to an example repository if available.]

## Prerequisites

- [Node.js 20+](https://nodejs.org)
- [Any other prerequisites]

## 1. Set up your project

[Instructions for creating or setting up the project]

```npm
# Example command
npx create-next-app@latest my-app
cd my-app
```

## 2. Install and Configure Prisma

### 2.1. Install dependencies

To get started with Prisma, you'll need to install a few dependencies:

```npm
npm install prisma tsx @types/pg --save-dev
```

```npm
npm install @prisma/client @prisma/adapter-pg dotenv pg
```

:::info

If you are using a different database provider (MySQL, SQL Server, SQLite), install the corresponding driver adapter package instead of `@prisma/adapter-pg`. For more information, see [Database drivers](/orm/core-concepts/supported-databases/database-drivers).

:::

Once installed, initialize Prisma in your project:

```npm
npx prisma init --db --output ../generated/prisma
```

:::info
You'll need to answer a few questions while setting up your Prisma Postgres database. Select the region closest to your location and a memorable name for your database.
:::

This will create:

- A `prisma` directory with a `schema.prisma` file
- A Prisma Postgres database
- A `.env` file containing the `DATABASE_URL`
- A `prisma.config.ts` file for configuration

### 2.2. Define your Prisma Schema

In the `prisma/schema.prisma` file, add your models:

```prisma title="prisma/schema.prisma"
generator client {
  provider = "prisma-client"
  output   = "../generated/prisma"
}

datasource db {
  provider = "postgresql"
}

model User { // [!code ++]
  id    Int     @id @default(autoincrement()) // [!code ++]
  email String  @unique // [!code ++]
  name  String? // [!code ++]
  posts Post[] // [!code ++]
} // [!code ++]

model Post { // [!code ++]
  id        Int     @id @default(autoincrement()) // [!code ++]
  title     String // [!code ++]
  content   String? // [!code ++]
  published Boolean @default(false) // [!code ++]
  authorId  Int // [!code ++]
  author    User    @relation(fields: [authorId], references: [id]) // [!code ++]
} // [!code ++]
```

### 2.3. Run migrations and generate Prisma Client

Create the database tables:

```npm
npx prisma migrate dev --name init
```

Then generate Prisma Client:

```npm
npx prisma generate
```

## 3. [Integration-specific steps]

[Add framework or platform-specific integration steps here]

## Next steps

Now that you've completed this guide, you can:

- [Suggestion 1]
- [Suggestion 2]
- [Related guide 1](/path/to/guide)
- [Related guide 2](/path/to/guide)

For more information:

- [Prisma documentation](/orm)
- [Related documentation]
````

Adding guides to navigation [#adding-guides-to-navigation]

Guides are organized by category in subdirectories. To add a guide to the navigation, you need to update the appropriate `meta.json` file.

Main categories [#main-categories]

The main guide categories are listed in `meta.json`:

```json title="apps/docs/content/docs/guides/meta.json"
{
  "title": "Guides",
  "root": true,
  "icon": "NotebookTabs",
  "pages": [
    "index",
    "frameworks",
    "deployment",
    "authentication",
    "integrations",
    "postgres",
    "database",
    "switch-to-prisma-orm",
    "upgrade-prisma-orm"
  ]
}
```

Adding a guide to a category [#adding-a-guide-to-a-category]

To add a guide to a category (e.g., `frameworks`), edit the category's `meta.json` file:

```json title="apps/docs/content/docs/guides/frameworks/meta.json"
{
  "title": "Frameworks",
  "defaultOpen": true,
  "pages": [
    "nextjs",
    "astro",
    "nuxt",
    "your-new-guide" // [!code ++]
  ]
}
```

The page name should match your `.mdx` filename without the extension. For example, if your file is `your-new-guide.mdx`, add `"your-new-guide"` to the `pages` array.

Next steps [#next-steps]

After reading this guide, you can:

* Start writing your own guide using the provided template
* Review existing guides in the category you're contributing to
* Coordinate with the design team for a unique header image
* Submit your guide for review


# Using API Clients (/docs/management-api/api-clients)



This guide shows you how to configure popular API clients to work with the Management API using OAuth 2.0 authentication.

Postman [#postman]

Postman is a popular API client with testing, collaboration, and automation features for working with REST APIs.

Prerequisites [#prerequisites]

Before you begin, make sure you have:

* A [Prisma Console account](https://console.prisma.io)
* [Postman installed](https://www.postman.com/downloads/)

1. Create an OAuth2 Application [#1-create-an-oauth2-application]

First, you'll need to register an OAuth2 application in Prisma Console:

1. Navigate to [Prisma Console](https://console.prisma.io) and log in
2. Click the **🧩 Integrations** tab in the left sidebar
3. Under the "Published Applications" section, click **New Application**
4. Fill in your application details:
   * **Name**: Postman API Client
   * **Description**: Brief description of your application *(Optional)*
   * **Redirect URI**: `https://oauth.pstmn.io/v1/callback`
5. Click **Continue**
6. **Important**: Copy your Client ID and Client Secret immediately and store them securely

<CalloutContainer type="info">
  <CalloutDescription>
    The redirect URI `https://oauth.pstmn.io/v1/callback` is Postman's default callback URL when using the "Authorize using browser" option.
  </CalloutDescription>
</CalloutContainer>

2. Configure OAuth 2.0 in Postman [#2-configure-oauth-20-in-postman]

Now you'll set up authentication in Postman:

1. Open Postman and create a new HTTP request
2. Set the request method to **POST**
3. Set the URL to `https://api.prisma.io/v1/projects`
4. Navigate to the **Authorization** tab
5. Set **Auth Type** to **OAuth 2.0**
6. Under **Configure New Token**, enter the following values:

| Parameter            | Value                                |
| -------------------- | ------------------------------------ |
| Token Name           | Management API Token                 |
| Grant Type           | Authorization Code                   |
| Callback URL         | `https://oauth.pstmn.io/v1/callback` |
| Authorize in Browser | `true` *(checked)*                   |
| Auth URL             | `https://auth.prisma.io/authorize`   |
| Access Token URL     | `https://auth.prisma.io/token`       |
| Client ID            | `your-client-id`                     |
| Client Secret        | `your-client-secret`                 |
| Scope                | `workspace:admin`                    |

7. Click **Get New Access Token**
8. A browser window will open and have you complete the authorization flow
9. Return to Postman and click **Use Token** to attach it to your request
10. Verify that your new token appears under **Current Token** at the top of the Authorization tab

3. Make your first request [#3-make-your-first-request]

With authentication configured, you can now create a project:

1. In the request body, select **raw** and **JSON** format
2. Add the following JSON payload:

```json
{
  "name": "My Postman Database",
  "region": "us-east-1"
}
```

3. Click **Send**

You should receive a successful response confirming your project creation.

Insomnia [#insomnia]

Insomnia is an open-source API client with a clean interface for testing and debugging HTTP requests.

Prerequisites [#prerequisites-1]

Before you begin, make sure you have:

* A [Prisma Console account](https://console.prisma.io)
* [Insomnia installed](https://insomnia.rest/download/)

1. Create an OAuth2 Application [#1-create-an-oauth2-application-1]

First, you'll need to register an OAuth2 application in Prisma Console:

1. Navigate to [Prisma Console](https://console.prisma.io) and log in
2. Click the **🧩 Integrations** tab in the left sidebar
3. Under the "Published Applications" section, click **New Application**
4. Fill in your application details:
   * **Name**: Insomnia API Client
   * **Description**: Brief description of your application *(Optional)*
   * **Redirect URI**: `https://app.insomnia.rest/oauth/redirect`
5. Click **Continue**
6. **Important**: Copy your Client ID and Client Secret immediately and store them securely

<CalloutContainer type="info">
  <CalloutDescription>
    Insomnia uses `https://app.insomnia.rest/oauth/redirect` as the default OAuth callback URL for local authentication flows.
  </CalloutDescription>
</CalloutContainer>

2. Configure OAuth 2.0 in Insomnia [#2-configure-oauth-20-in-insomnia]

Now you'll set up authentication in Insomnia:

1. Open Insomnia and create a new HTTP request
2. Set the request method to **POST**
3. Set the URL to `https://api.prisma.io/v1/projects`
4. Navigate to the **Auth** tab
5. Set the authentication type to **OAuth 2.0**
6. Under **Configuration**, enter the following values:

| Parameter                        | Value                                      |
| -------------------------------- | ------------------------------------------ |
| Grant Type                       | Authorization Code                         |
| Authorization URL                | `https://auth.prisma.io/authorize`         |
| Access Token URL                 | `https://auth.prisma.io/token`             |
| Client ID                        | `your-client-id`                           |
| Client Secret                    | `your-client-secret`                       |
| Redirect URL                     | `https://app.insomnia.rest/oauth/redirect` |
| Scope *(Under Advanced Options)* | `workspace:admin`                          |

7. Click **Fetch Tokens**
8. A browser window will open and have you complete the authorization flow
9. Return to Insomnia and verify that the access token has been retrieved
10. The token will be automatically attached to your requests

3. Make your first request [#3-make-your-first-request-1]

With authentication configured, you can now create a project:

1. Navigate to the **Body** tab and select **JSON** format
2. Add the following JSON payload:

```json
{
  "name": "My Insomnia Database",
  "region": "us-east-1"
}
```

3. Click **Send**

You should receive a successful response confirming your project creation.

Yaak [#yaak]

Yaak is a lightweight, open-source, and offline API client that works with Git.

Prerequisites [#prerequisites-2]

Before you begin, make sure you have:

* A [Prisma Console account](https://console.prisma.io)
* [Yaak installed](https://yaak.app)

1. Create an OAuth2 Application [#1-create-an-oauth2-application-2]

First, you'll need to register an OAuth2 application in Prisma Console:

1. Navigate to [Prisma Console](https://console.prisma.io) and log in
2. Click the **🧩 Integrations** tab in the left sidebar
3. Under the "Published Applications" section, click **New Application**
4. Fill in your application details:
   * **Name**: Yaak API Client
   * **Description**: Brief description of your application *(Optional)*
   * **Redirect URI**: `https://devnull.yaak.app/callback`
5. Click **Continue**
6. **Important**: Copy your Client ID and Client Secret immediately and store them securely

<CalloutContainer type="info">
  <CalloutDescription>
    The redirect URI can be any valid URL. Yaak intercepts the OAuth callback regardless of the redirect URI, as long as it matches what's registered with the provider.
  </CalloutDescription>
</CalloutContainer>

2. Configure OAuth 2.0 in Yaak [#2-configure-oauth-20-in-yaak]

Now you'll set up authentication in Yaak:

1. Open Yaak and create a new HTTP request
2. Set the request method to **POST**
3. Set the URL to `https://api.prisma.io/v1/projects`
4. Navigate to the **Auth** tab
5. Set the authentication type to **OAuth 2.0**
6. Enter the following values:

| Parameter         | Value                               |
| ----------------- | ----------------------------------- |
| Grant Type        | Authorization Code                  |
| Authorization URL | `https://auth.prisma.io/authorize`  |
| Token URL         | `https://auth.prisma.io/token`      |
| Client ID         | `your-client-id`                    |
| Client Secret     | `your-client-secret`                |
| Redirect URL      | `https://devnull.yaak.app/callback` |
| Scope             | `workspace:admin`                   |

7. Click **Get Token**
8. A browser window will open and have you complete the authorization flow
9. Return to Yaak and verify that the access token has been retrieved
10. The token will be automatically attached to your requests

3. Make your first request [#3-make-your-first-request-2]

With authentication configured, you can now create a project:

1. Navigate to the **Body** tab and select **JSON** format
2. Add the following JSON payload:

```json
{
  "name": "My Yaak Database",
  "region": "us-east-1"
}
```

3. Click **Send**

You should receive a successful response confirming your project creation.


# Authentication (/docs/management-api/authentication)



The Management API supports two authentication methods:

* **Service Tokens** - Simple bearer tokens for server-to-server integrations
* **OAuth 2.0** - For user-facing applications requiring user consent

Service tokens [#service-tokens]

Service tokens are the simplest way to authenticate. They're ideal for scripts, CI/CD pipelines, and backend services.

Creating a Service token [#creating-a-service-token]

1. Navigate to [Prisma Console](https://console.prisma.io) and log in
2. Select your workspace
3. Go to **Settings → Service Tokens**
4. Click **New Service Token**
5. Copy the generated token immediately and store it securely

Using a Service token [#using-a-service-token]

Include the token in the `Authorization` header:

```bash
curl -X GET "https://api.prisma.io/v1/workspaces" \
  -H "Authorization: Bearer your-service-token"
```

Or with the SDK:

```typescript
import { createManagementApiClient } from "@prisma/management-api-sdk";

const client = createManagementApiClient({
  token: "your-service-token",
});
```

<CalloutContainer type="warning">
  <CalloutTitle>
    Service tokens never expire
  </CalloutTitle>

  <CalloutDescription>
    Service tokens do not have an expiration date. While this provides convenience for long-running integrations, it also means these tokens require careful security management.
  </CalloutDescription>
</CalloutContainer>

OAuth 2.0 [#oauth-20]

OAuth 2.0 is required for applications that act on behalf of users. The API uses OAuth 2.0 with PKCE for secure authentication.

PKCE Support [#pkce-support]

The OAuth implementation supports Proof Key for Code Exchange (PKCE) using the S256 code challenge method:

* **Public clients** (no client secret): PKCE is **mandatory**
* **Confidential clients** (with client secret): PKCE is **optional**, but if you start the flow with PKCE, it must be completed with PKCE

This provides enhanced security, especially for mobile and single-page applications that cannot securely store client secrets.

Creating an OAuth Application [#creating-an-oauth-application]

1. Navigate to [Prisma Console](https://console.prisma.io) and log in
2. Click the **Integrations** tab in the left sidebar
3. Under "Published Applications", click **New Application**
4. Fill in your application details:
   * **Name**: Your application name
   * **Description**: Brief description *(optional)*
   * **Redirect URI**: Your callback URL (e.g., `https://your-app.com/auth/callback`)
5. Click **Continue**
6. Copy your **Client ID** and **Client Secret** immediately

<CalloutContainer type="info">
  <CalloutTitle>
    Development redirect URIs
  </CalloutTitle>

  <CalloutDescription>
    For local development, the following redirect URIs are accepted with any port via wildcard matching:

    * `localhost` (e.g., `http://localhost:3000/callback`)
    * `127.0.0.1` (e.g., `http://127.0.0.1:3000/callback`)
    * `[::1]` - IPv6 loopback (e.g., `http://[::1]:3000/callback`)
  </CalloutDescription>
</CalloutContainer>

OAuth Endpoints [#oauth-endpoints]

| Endpoint      | URL                                                             |
| ------------- | --------------------------------------------------------------- |
| Authorization | `https://auth.prisma.io/authorize`                              |
| Token         | `https://auth.prisma.io/token`                                  |
| Discovery     | `https://auth.prisma.io/.well-known/oauth-authorization-server` |

<CalloutContainer type="info">
  <CalloutDescription>
    The discovery endpoint provides OAuth server metadata that can be used for automatic client configuration. Many OAuth libraries support automatic discovery using this endpoint.
  </CalloutDescription>
</CalloutContainer>

Available Scopes [#available-scopes]

| Scope             | Description                                    |
| ----------------- | ---------------------------------------------- |
| `workspace:admin` | Full access to workspace resources             |
| `offline_access`  | Enables refresh tokens for long-lived sessions |

Token Lifetimes [#token-lifetimes]

| Token Type     | Expiration |
| -------------- | ---------- |
| Access tokens  | 1 hour     |
| Refresh tokens | 90 days    |

OAuth Authorization Flow [#oauth-authorization-flow]

1. Redirect users to authorize [#1-redirect-users-to-authorize]

Redirect users to the authorization endpoint with the following query parameters:

| Parameter       | Description                                                         |
| --------------- | ------------------------------------------------------------------- |
| `client_id`     | Your OAuth application's Client ID                                  |
| `redirect_uri`  | The callback URL where users will be redirected after authorization |
| `response_type` | Must be `code` for the authorization code flow                      |
| `scope`         | Permissions to request (e.g., `workspace:admin`)                    |

```
https://auth.prisma.io/authorize?client_id=$CLIENT_ID&redirect_uri=$REDIRECT_URI&response_type=code&scope=workspace:admin
```

This will redirect the user to the Prisma authorization page where they can grant your application access to their workspace.

2. Receive the authorization code [#2-receive-the-authorization-code]

After authorization, users are redirected to your callback URL with a `code` parameter:

```
https://your-app.com/callback?code=abc123...
```

3. Exchange the code for an access token [#3-exchange-the-code-for-an-access-token]

```bash
curl -X POST https://auth.prisma.io/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "code=$CODE" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri=$REDIRECT_URI"
```

The response will include an access token that can be used to make authenticated requests to the Management API:

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

4. Use the access token [#4-use-the-access-token]

```bash
curl -X GET "https://api.prisma.io/v1/workspaces" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

Token Refresh [#token-refresh]

If you requested the `offline_access` scope, you'll receive a refresh token. Use it to obtain new access tokens:

```bash
curl -X POST https://auth.prisma.io/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "refresh_token=$REFRESH_TOKEN" \
  -d "grant_type=refresh_token"
```

<CalloutContainer type="info">
  <CalloutTitle>
    Refresh token rotation
  </CalloutTitle>

  <CalloutDescription>
    Refresh tokens use single-use rotation with replay attack detection. When you exchange a refresh token for a new access token, you'll receive a new refresh token in the response. The old refresh token is immediately invalidated. If an invalidated refresh token is used again, it indicates a potential security breach, and the system will revoke all tokens associated with that authorization.
  </CalloutDescription>
</CalloutContainer>

Using OAuth with the SDK [#using-oauth-with-the-sdk]

The SDK handles the OAuth flow automatically. See the [SDK documentation](/management-api/sdk#oauth-authentication-flow) for implementation details.

Using API Clients [#using-api-clients]

You can also authenticate using popular API clients like Postman, Insomnia, or Yaak. See the [Using API Clients](/management-api/api-clients) guide for step-by-step instructions.


# Getting Started (/docs/management-api/getting-started)



This guide walks you through setting up a basic TypeScript project that uses the Management API to create a new Prisma Console project with a Prisma Postgres database, and print out all connection details.

You'll authenticate via a service token, set up your environment, and run a script to interact with the API.

Prerequisites [#prerequisites]

* Node.js and `npm` installed
* A [Prisma Data Platform](https://console.prisma.io/) account

1. Create a service token in Prisma Console [#1-create-a-service-token-in-prisma-console]

First, you need to create a service token to be able to access the Management API:

1. Open the [Prisma Console](https://console.prisma.io/)
2. Navigate to the **Settings** page of your workspace and select **Service Tokens**
3. Click **New Service Token**
4. Copy and save the generated service token securely, you'll use it in step 2.2.

2. Set up your project directory [#2-set-up-your-project-directory]

2.1. Create a basic TypeScript project [#21-create-a-basic-typescript-project]

Open your terminal and run the following commands:

```bash
mkdir management-api-demo
cd management-api-demo
```

Next, initialize npm and install dependencies required for using TypeScript:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npm init -y
    npm install tsx typescript @types/node --save-dev
    touch index.ts
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm init -y
    pnpm add tsx typescript @types/node --save-dev
    touch index.ts
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn init -y
    yarn add tsx typescript @types/node --dev
    touch index.ts
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bun init -y
    bun add tsx typescript @types/node --dev
    touch index.ts
    ```
  </CodeBlockTab>
</CodeBlockTabs>

You now have an `index.ts` file that you can execute with `npx tsx index.ts`. It's still empty, you'll start writing code in step 3.

2.2. Configure service token environment variable [#22-configure-service-token-environment-variable]

Create your `.env` file:

```bash
touch .env
```

Next, install the [`dotenv`](https://github.com/motdotla/dotenv) library for loading environment variables from the `.env` file:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npm install dotenv
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm add dotenv

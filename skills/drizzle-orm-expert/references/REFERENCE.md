<!-- Source: https://orm.drizzle.team/llms-full.txt (llms-full.txt) -->
<!-- Downloaded: 2026-03-21 -->

# Drizzle

> Drizzle is a modern TypeScript ORM developers wanna use in their next project. It is lightweight at only ~7.4kb minified+gzipped, and it's tree shakeable with exactly 0 dependencies. It supports every PostgreSQL, MySQL, SQLite and SingleStore database and is serverless-ready by design.

Source: https://orm.drizzle.team/docs/arktype

import Npm from '@mdx/Npm.astro';
import Callout from '@mdx/Callout.astro';

<Callout type="error">
Starting from `drizzle-orm@1.0.0-beta.15`, `drizzle-arktype` has been deprecated in favor of first-class schema generation support within Drizzle ORM itself

You can still use `drizzle-arktype` package but all new update will be added to Drizzle ORM directly
</Callout>

# arktype

### Install the dependencies

<Npm>
arktype
</Npm>

### Select schema

Defines the shape of data queried from the database - can be used to validate API responses.

```ts copy
import { pgTable, text, integer } from 'drizzle-orm/pg-core';
import { createSelectSchema } from 'drizzle-orm/arktype';

const users = pgTable('users', {
  id: integer().generatedAlwaysAsIdentity().primaryKey(),
  name: text().notNull(),
  age: integer().notNull()
});

const userSelectSchema = createSelectSchema(users);

const rows = await db.select({ id: users.id, name: users.name }).from(users).limit(1);
const parsed: { id: number; name: string; age: number } = userSelectSchema(rows[0]); // Error: `age` is not returned in the above query

const rows = await db.select().from(users).limit(1);
const parsed: { id: number; name: string; age: number } = userSelectSchema(rows[0]); // Will parse successfully
```

Views and enums are also supported.

```ts copy
import { pgEnum } from 'drizzle-orm/pg-core';
import { createSelectSchema } from 'drizzle-orm/arktype';

const roles = pgEnum('roles', ['admin', 'basic']);
const rolesSchema = createSelectSchema(roles);
const parsed: 'admin' | 'basic' = rolesSchema(...);

const usersView = pgView('users_view').as((qb) => qb.select().from(users).where(gt(users.age, 18)));
const usersViewSchema = createSelectSchema(usersView);
const parsed: { id: number; name: string; age: number } = usersViewSchema(...);
```

### Insert schema

Defines the shape of data to be inserted into the database - can be used to validate API requests.

```ts copy
import { pgTable, text, integer } from 'drizzle-orm/pg-core';
import { createInsertSchema } from 'drizzle-orm/arktype';

const users = pgTable('users', {
  id: integer().generatedAlwaysAsIdentity().primaryKey(),
  name: text().notNull(),
  age: integer().notNull()
});

const userInsertSchema = createInsertSchema(users);

const user = { name: 'John' };
const parsed: { name: string, age: number } = userInsertSchema(user); // Error: `age` is not defined

const user = { name: 'Jane', age: 30 };
const parsed: { name: string, age: number } = userInsertSchema(user); // Will parse successfully
await db.insert(users).values(parsed);
```

### Update schema

Defines the shape of data to be updated in the database - can be used to validate API requests.

```ts copy
import { pgTable, text, integer } from 'drizzle-orm/pg-core';
import { createUpdateSchema } from 'drizzle-orm/arktype';
import { parse } from 'arktype';

const users = pgTable('users', {
  id: integer().generatedAlwaysAsIdentity().primaryKey(),
  name: text().notNull(),
  age: integer().notNull()
});

const userUpdateSchema = createUpdateSchema(users);

const user = { id: 5, name: 'John' };
const parsed: { name?: string | undefined, age?: number | undefined } = userUpdateSchema(user); // Error: `id` is a generated column, it can't be updated

const user = { age: 35 };
const parsed: { name?: string | undefined, age?: number | undefined } = userUpdateSchema(user); // Will parse successfully
await db.update(users).set(parsed).where(eq(users.name, 'Jane'));
```

### Refinements

Each create schema function accepts an additional optional parameter that you can used to extend, modify or completely overwite a field's schema. Defining a callback function will extend or modify while providing a arktype schema will overwrite it.

```ts copy
import { pgTable, text, integer, json } from 'drizzle-orm/pg-core';
import { createSelectSchema } from 'drizzle-orm/arktype';
import { parse, pipe, maxLength, object, string } from 'arktype';

const users = pgTable('users', {
  id: integer().generatedAlwaysAsIdentity().primaryKey(),
  name: text().notNull(),
  bio: text(),
  preferences: json()
});

const userSelectSchema = createSelectSchema(users, {
  name: (schema) => pipe(schema, maxLength(20)), // Extends schema
  bio: (schema) => pipe(schema, maxLength(1000)), // Extends schema before becoming nullable/optional
  preferences: object({ theme: string() }) // Overwrites the field, including its nullability
});

const parsed: {
  id: number;
  name: string,
  bio?: string | undefined;
  preferences: {
    theme: string;
  };
} = userSelectSchema(...);
```

### Data type reference

```ts
pg.boolean();

mysql.boolean();

sqlite.integer({ mode: 'boolean' });

// Schema
type.boolean;
```

```ts
pg.date({ mode: 'date' });
pg.timestamp({ mode: 'date' });

mysql.date({ mode: 'date' });
mysql.datetime({ mode: 'date' });
mysql.timestamp({ mode: 'date' });

sqlite.integer({ mode: 'timestamp' });
sqlite.integer({ mode: 'timestamp_ms' });

// Schema
type.Date;
```

```ts
pg.date({ mode: 'string' });
pg.timestamp({ mode: 'string' });
pg.cidr();
pg.inet();
pg.interval();
pg.macaddr();
pg.macaddr8();
pg.numeric();
pg.text();
pg.sparsevec();
pg.time();

mysql.binary();
mysql.date({ mode: 'string' });
mysql.datetime({ mode: 'string' });
mysql.decimal();
mysql.time();
mysql.timestamp({ mode: 'string' });
mysql.varbinary();

sqlite.numeric();
sqlite.text({ mode: 'text' });

// Schema
type.string;
```

```ts
pg.bit({ dimensions: ... });

// Schema
type(`/^[01]{${column.dimensions}}$/`);
```

```ts
pg.uuid();

// Schema
type(/^[\da-f]{8}(?:-[\da-f]{4}){3}-[\da-f]{12}$/iu);
```

```ts
pg.char({ length: ... });

mysql.char({ length: ... });

// Schema
type.string.exactlyLength(length);
```

```ts
pg.varchar({ length: ... });

mysql.varchar({ length: ... });

sqlite.text({ mode: 'text', length: ... });

// Schema
type.string.atMostLength(length);
```

```ts
mysql.tinytext();

// Schema
type.string.atMostLength(255); // unsigned 8-bit integer limit
```

```ts
mysql.text();

// Schema
type.string.atMostLength(65_535); // unsigned 16-bit integer limit
```

```ts
mysql.mediumtext();

// Schema
type.string.atMostLength(16_777_215); // unsigned 24-bit integer limit
```

```ts
mysql.longtext();

// Schema
type.string.atMostLength(4_294_967_295); // unsigned 32-bit integer limit
```

```ts
pg.text({ enum: ... });
pg.char({ enum: ... });
pg.varchar({ enum: ... });

mysql.tinytext({ enum: ... });
mysql.mediumtext({ enum: ... });
mysql.text({ enum: ... });
mysql.longtext({ enum: ... });
mysql.char({ enum: ... });
mysql.varchar({ enum: ... });
mysql.mysqlEnum(..., ...);

sqlite.text({ mode: 'text', enum: ... });

// Schema
type.enumerated(...enum);
```

```ts
mysql.tinyint();

// Schema
type.keywords.number.integer.atLeast(-128).atMost(127); // 8-bit integer lower and upper limit
```

```ts
mysql.tinyint({ unsigned: true });

// Schema
type.keywords.number.integer.atLeast(0).atMost(255); // unsigned 8-bit integer lower and upper limit
```

```ts
pg.smallint();
pg.smallserial();

mysql.smallint();

// Schema
type.keywords.number.integer.atLeast(-32_768).atMost(32_767); // 16-bit integer lower and upper limit
```

```ts
mysql.smallint({ unsigned: true });

// Schema
type.keywords.number.integer.atLeast(0).atMost(65_535); // unsigned 16-bit integer lower and upper limit
```

```ts
pg.real();

mysql.float();

// Schema
type.number.atLeast(-8_388_608).atMost(8_388_607); // 24-bit integer lower and upper limit
```

```ts
mysql.mediumint();

// Schema
type.keywords.number.integer.atLeast(-8_388_608).atMost(8_388_607); // 24-bit integer lower and upper limit
```

```ts
mysql.float({ unsigned: true });

// Schema
type.number.atLeast(0).atMost(16_777_215); // unsigned 24-bit integer lower and upper limit
```

```ts
mysql.mediumint({ unsigned: true });

// Schema
type.keywords.number.integer.atLeast(0).atMost(16_777_215); // unsigned 24-bit integer lower and upper limit
```

```ts
pg.integer();
pg.serial();

mysql.int();

// Schema
type.keywords.number.integer.atLeast(-2_147_483_648).atMost(2_147_483_647); // 32-bit integer lower and upper limit
```

```ts
mysql.int({ unsigned: true });

// Schema
type.keywords.number.integer.atLeast(0).atMost(4_294_967_295); // unsgined 32-bit integer lower and upper limit
```

```ts
pg.doublePrecision();

mysql.double();
mysql.real();

sqlite.real();

// Schema
type.number.atLeast(-140_737_488_355_328).atMost(140_737_488_355_327); // 48-bit integer lower and upper limit
```

```ts
mysql.double({ unsigned: true });

// Schema
type.number.atLeast(0).atMost(281_474_976_710_655); // unsigned 48-bit integer lower and upper limit
```

```ts
pg.bigint({ mode: 'number' });
pg.bigserial({ mode: 'number' });

mysql.bigint({ mode: 'number' });
mysql.bigserial({ mode: 'number' });

sqlite.integer({ mode: 'number' });

// Schema
type.keywords.number.integer.atLeast(-9_007_199_254_740_991).atMost(9_007_199_254_740_991); // Javascript min. and max. safe integers
```

```ts
mysql.serial();

// Schema
type.keywords.number.integer.atLeast(0).atMost(9_007_199_254_740_991); // Javascript max. safe integer
```

```ts
pg.bigint({ mode: 'bigint' });
pg.bigserial({ mode: 'bigint' });

mysql.bigint({ mode: 'bigint' });

sqlite.blob({ mode: 'bigint' });

// Schema
type.bigint.narrow(
  (value, ctx) => value < -9_223_372_036_854_775_808n ? ctx.mustBe('greater than') : value > 9_223_372_036_854_775_807n ? ctx.mustBe('less than') : true
); // 64-bit integer lower and upper limit
```

```ts
mysql.bigint({ mode: 'bigint', unsigned: true });

// Schema
type.bigint.narrow(
  (value, ctx) => value < 0n ? ctx.mustBe('greater than') : value > 18_446_744_073_709_551_615n ? ctx.mustBe('less than') : true
); // unsigned 64-bit integer lower and upper limit
```

```ts
mysql.year();

// Schema
type.keywords.number.integer.atLeast(1_901).atMost(2_155);
```

```ts
pg.geometry({ type: 'point', mode: 'tuple' });
pg.point({ mode: 'tuple' });

// Schema
type([type.number, type.number]);
```

```ts
pg.geometry({ type: 'point', mode: 'xy' });
pg.point({ mode: 'xy' });

// Schema
type({ x: type.number, y: type.number });
```

```ts
pg.halfvec({ dimensions: ... });
pg.vector({ dimensions: ... });

// Schema
type.number.array().exactlyLength(dimensions);
```

```ts
pg.line({ mode: 'abc' });

// Schema
type({ a: type.number, b: type.number, c: type.number });
```

```ts
pg.line({ mode: 'tuple' });

// Schema
type([type.number, type.number, type.number]);
```

```ts
pg.json();
pg.jsonb();

mysql.json();

sqlite.blob({ mode: 'json' });
sqlite.text({ mode: 'json' });

// Schema
type('string | number | boolean | null').or(type('unknown.any[] | Record<string, unknown.any>'));
```

```ts
sqlite.blob({ mode: 'buffer' });

// Schema
type.instanceOf(Buffer);
```

```ts
pg.dataType().array(...);

// Schema
baseDataTypeSchema.array().exactlyLength(size);
```


Source: https://orm.drizzle.team/docs/batch-api

import Tab from '@mdx/Tab.astro';
import Tabs from '@mdx/Tabs.astro';

# Batch API

**LibSQL Batch API explanation**:
_[source](https://docs.turso.tech/sdk/ts/reference#batch-transactions)_

> With the libSQL client library, a batch is one or more SQL statements executed in order in an implicit transaction.
The transaction is controlled by the libSQL backend. If all of the statements are successful,
the transaction is committed. If any of the statements fail, the entire transaction is rolled back and no changes are made.

**D1 Batch API explanation**:
_[source](https://developers.cloudflare.com/d1/worker-api/d1-database/#batch)_

> Batching sends multiple SQL statements inside a single call to the database.
This can have a huge performance impact as it reduces latency from network round trips to D1.
D1 operates in auto-commit. Our implementation guarantees that each statement in the list will execute and commit,
sequentially, non-concurrently.
Batched statements are SQL transactions. If a statement in the sequence fails,
then an error is returned for that specific statement, and it aborts or rolls back the entire sequence.

Drizzle ORM provides APIs to run SQL statements in batch for `LibSQL`, `Neon` and `D1`:
```ts
const batchResponse: BatchResponse = await db.batch([
	db.insert(usersTable).values({ id: 1, name: 'John' }).returning({ id: usersTable.id }),
	db.update(usersTable).set({ name: 'Dan' }).where(eq(usersTable.id, 1)),
	db.query.usersTable.findMany({}),
	db.select().from(usersTable).where(eq(usersTable.id, 1)),
	db.select({ id: usersTable.id, invitedBy: usersTable.invitedBy }).from(usersTable),
]);
```
Type for `batchResponse` in this example would be:
<Tabs items={["libSQL", "Neon", "D1"]}>
<Tab>
```ts
type BatchResponse = [
	{
		id: number;
	}[],
	ResultSet,
	{
		id: number;
		name: string;
		verified: number;
		invitedBy: number | null;
	}[],
	{
		id: number;
		name: string;
		verified: number;
		invitedBy: number | null;
	}[],
	{
		id: number;
		invitedBy: number | null;
	}[],
]
```
</Tab>
<Tab>
```ts
type BatchResponse = [
	{
		id: number;
	}[],
	NeonHttpQueryResult,
	{
		id: number;
		name: string;
		verified: number;
		invitedBy: number | null;
	}[],
	{
		id: number;
		name: string;
		verified: number;
		invitedBy: number | null;
	}[],
	{
		id: number;
		invitedBy: number | null;
	}[],
]
```
</Tab>
<Tab>
```ts
type BatchResponse = [
  {
    id: number;
  }[],
  D1Result,
  {
    id: number;
    name: string;
    verified: number;
    invitedBy: number | null;
  }[],
  {
    id: number;
    name: string;
    verified: number;
    invitedBy: number | null;
  }[],
  {
    id: number;
    invitedBy: number | null;
  }[],
]
```
</Tab>
</Tabs>

All possible builders that can be used inside `db.batch`:
```ts
db.all(),
db.get(),
db.values(),
db.run(),
db.execute(),
db.query.<table>.findMany(),
db.query.<table>.findFirst(),
db.select()...,
db.update()...,
db.delete()...,
db.insert()...,
```


Source: https://orm.drizzle.team/docs/cache

import Callout from '@mdx/Callout.astro';
import Npm from '@mdx/Npm.astro';

# Cache

Drizzle sends every query straight to your database by default. There are no hidden actions, no automatic caching
or invalidation - you'll always see exactly what runs. If you want caching, you must opt in.

By default, Drizzle uses a `explicit` caching strategy (i.e. `global: false`), so nothing is ever cached unless you ask.
This prevents surprises or hidden performance traps in your application.
Alternatively, you can flip on `all` caching (`global: true`) so that every select will look in cache first.

## Quickstart

### Upstash integration

Drizzle provides an `upstashCache()` helper out of the box. By default, this uses Upstash Redis with automatic configuration if environment variables are set.

```ts
import { upstashCache } from "drizzle-orm/cache/upstash";
import { drizzle } from "drizzle-orm/...";

const db = drizzle(process.env.DB_URL!, {
  cache: upstashCache(),
});
```

You can also explicitly define your Upstash credentials, enable global caching for all queries by default or pass custom caching options:

```ts
import { upstashCache } from "drizzle-orm/cache/upstash";
import { drizzle } from "drizzle-orm/...";

const db = drizzle(process.env.DB_URL!, {
  cache: upstashCache({
    // 👇 Redis credentials (optional — can also be pulled from env vars)
    url: '<UPSTASH_URL>',
    token: '<UPSTASH_TOKEN>',

    // 👇 Enable caching for all queries by default (optional)
    global: true,

    // 👇 Default cache behavior (optional)
    config: { ex: 60 }
  })
});
```

## Cache config reference

Drizzle supports the following cache config options for Upstash:

```ts
export type CacheConfig = {
  /**
   * Expiration in seconds (positive integer)
   */
  ex?: number;
  /**
   * Set an expiration (TTL or time to live) on one or more fields of a given hash key.
   * Used for HEXPIRE command
   */
  hexOptions?: "NX" | "nx" | "XX" | "xx" | "GT" | "gt" | "LT" | "lt";
};
```

## Cache usage examples

Once you've configured caching, here's how the cache behaves:

**Case 1: Drizzle with `global: false` (default, opt-in caching)**

```ts
import { upstashCache } from "drizzle-orm/cache/upstash";
import { drizzle } from "drizzle-orm/...";

const db = drizzle(process.env.DB_URL!, {
  // 👇 `global: true` is not passed, false by default
  cache: upstashCache({ url: "", token: "" }),
});
```

In this case, the following query won't read from cache

```ts
const res = await db.select().from(users);

// Any mutate operation will still trigger the cache's onMutate handler
// and attempt to invalidate any cached queries that involved the affected tables
await db.insert(users).value({ email: "cacheman@upstash.com" });
```

To make this query read from the cache, call `.$withCache()`

```ts
const res = await db.select().from(users).$withCache();
```

`.$withCache` has a set of options you can use to manage and configure this specific query strategy

```ts
// rewrite the config for this specific query
.$withCache({ config: {} })

// give this query a custom cache key (instead of hashing query+params under the hood)
.$withCache({ tag: 'custom_key' })

// turn off auto-invalidation for this query
// note: this leads to eventual consistency (explained below)
.$withCache({ autoInvalidate: false })
```

<Callout>
**Eventual consistency example**

This example is only relevant if you manually set `autoInvalidate: false`. By default, `autoInvalidate` is enabled.

You might want to turn off `autoInvalidate` if:
- your data doesn't change often, and slight staleness is acceptable (e.g. product listings, blog posts)
- you handle cache invalidation manually

In those cases, turning it off can reduce unnecessary cache invalidation. However, in most cases, we recommend keeping the default enabled.

Example: Imagine you cache the following query on `usersTable` with a 3-second TTL:

``` ts
const recent = await db
  .select().from(usersTable)
  .$withCache({ config: { ex: 3 }, autoInvalidate: false });
```

If someone runs `db.insert(usersTable)...` the cache won't be invalidated immediately. For up to 3 seconds, you'll keep seeing the old data until it eventually becomes consistent.
</Callout>

**Case 2: Drizzle with `global: true` option**

```ts
import { upstashCache } from "drizzle-orm/cache/upstash";
import { drizzle } from "drizzle-orm/...";

const db = drizzle(process.env.DB_URL!, {
  cache: upstashCache({ url: "", token: "", global: true }),
});
```

In this case, the following query will read from cache

```ts
const res = await db.select().from(users);
```

If you want to disable cache for this specific query, call `.$withCache(false)`

```ts
// disable cache for this query
const res = await db.select().from(users).$withCache(false);
```

You can also use cache instance from a `db` to invalidate specific tables or tags

```ts
// Invalidate all queries that use the `users` table. You can do this with the Drizzle instance.
await db.$cache.invalidate({ tables: users });
// or
await db.$cache.invalidate({ tables: [users, posts] });

// Invalidate all queries that use the `usersTable`. You can do this by using just the table name.
await db.$cache.invalidate({ tables: "usersTable" });
// or
await db.$cache.invalidate({ tables: ["usersTable", "postsTable"] });

// You can also invalidate custom tags defined in any previously executed select queries.
await db.$cache.invalidate({ tags: "custom_key" });
// or
await db.$cache.invalidate({ tags: ["custom_key", "custom_key1"] });
```

## Custom cache

This example shows how to plug in a custom `cache` in Drizzle: you provide functions to fetch data from the cache, store results back into cache, and invalidate entries whenever a mutation runs.

Cache extension provides this set of config options
```ts
export type CacheConfig = {
  /** expire time, in seconds */
  ex?: number;
  /** expire time, in milliseconds */
  px?: number;
  /** Unix time (sec) at which the key will expire */
  exat?: number;
  /** Unix time (ms) at which the key will expire */
  pxat?: number;
  /** retain existing TTL when updating a key */
  keepTtl?: boolean;
  /** options for HEXPIRE (hash-field TTL) */
  hexOptions?: 'NX' | 'XX' | 'GT' | 'LT' | 'nx' | 'xx' | 'gt' | 'lt';
};
```

```ts
const db = drizzle(process.env.DB_URL!, { cache: new TestGlobalCache() });
```

```ts
import Keyv from "keyv";

export class TestGlobalCache extends Cache {
  private globalTtl: number = 1000;
  // This object will be used to store which query keys were used
  // for a specific table, so we can later use it for invalidation.
  private usedTablesPerKey: Record<string, string[]> = {};

  constructor(private kv: Keyv = new Keyv()) {
    super();
  }

  // For the strategy, we have two options:
  // - 'explicit': The cache is used only when .$withCache() is added to a query.
  // - 'all': All queries are cached globally.
  // The default behavior is 'explicit'.
  override strategy(): "explicit" | "all" {
    return "all";
  }

  // This function accepts query and parameters that cached into key param,
  // allowing you to retrieve response values for this query from the cache.
  override async get(key: string): Promise<any[] | undefined> {
    const res = (await this.kv.get(key)) ?? undefined;
    return res;
  }

  // This function accepts several options to define how cached data will be stored:
  // - 'key': A hashed query and parameters.
  // - 'response': An array of values returned by Drizzle from the database.
  // - 'tables': An array of tables involved in the select queries. This information is needed for cache invalidation.
  //
  // For example, if a query uses the "users" and "posts" tables, you can store this information. Later, when the app executes
  // any mutation statements on these tables, you can remove the corresponding key from the cache.
  // If you're okay with eventual consistency for your queries, you can skip this option.
  override async put(
    key: string,
    response: any,
    tables: string[],
    config?: CacheConfig,
  ): Promise<void> {
    const ttl = config?.px ?? (config?.ex ? config.ex * 1000 : this.globalTtl);

    await this.kv.set(key, response, ttl);

    for (const table of tables) {
      const keys = this.usedTablesPerKey[table];
      if (keys === undefined) {
        this.usedTablesPerKey[table] = [key];
      } else {
        keys.push(key);
      }
    }
  }

  // This function is called when insert, update, or delete statements are executed.
  // You can either skip this step or invalidate queries that used the affected tables.
  //
  // The function receives an object with two keys:
  // - 'tags': Used for queries labeled with a specific tag, allowing you to invalidate by that tag.
  // - 'tables': The actual tables affected by the insert, update, or delete statements,
  //   helping you track which tables have changed since the last cache update.
  override async onMutate(params: {
    tags: string | string[];
    tables: string | string[] | Table<any> | Table<any>[];
  }): Promise<void> {
    const tagsArray = params.tags
      ? Array.isArray(params.tags)
        ? params.tags
        : [params.tags]
      : [];
    const tablesArray = params.tables
      ? Array.isArray(params.tables)
        ? params.tables
        : [params.tables]
      : [];

    const keysToDelete = new Set<string>();

    for (const table of tablesArray) {
      const tableName = is(table, Table)
        ? getTableName(table)
        : (table as string);
      const keys = this.usedTablesPerKey[tableName] ?? [];
      for (const key of keys) keysToDelete.add(key);
    }

    if (keysToDelete.size > 0 || tagsArray.length > 0) {
      for (const tag of tagsArray) {
        await this.kv.delete(tag);
      }

      for (const key of keysToDelete) {
        await this.kv.delete(key);
        for (const table of tablesArray) {
          const tableName = is(table, Table)
            ? getTableName(table)
            : (table as string);
          this.usedTablesPerKey[tableName] = [];
        }
      }
    }
  }
}
```

## Limitations

#### Queries that won't be handled by the `cache` extension:

- Using cache with raw queries, such as:

```ts
db.execute(sql`select 1`);
```

- Using cache with `batch` feature in `d1` and `libsql`

```ts
db.batch([
    db.insert(users).values(...),
    db.update(users).set(...).where()
])
```

- Using cache in transactions
```ts
await db.transaction(async (tx) => {
  await tx.update(accounts).set(...).where(...);
  await tx.update...
});
```

#### Limitations that are temporary and will be handled soon:

- Using cache with Drizzle Relational Queries
```ts
await db.query.users.findMany();
```

- Using cache with `better-sqlite3`, `Durable Objects`, `expo sqlite`
- Using cache with AWS Data API drivers
- Using cache with views


Source: https://orm.drizzle.team/docs/column-types/cockroach


import Section from '@mdx/Section.astro';
import Callout from '@mdx/Callout.astro';
import Npm from '@mdx/Npm.astro';

<Callout type='error'>
This page explains concepts available on drizzle versions `1.0.0-beta.2` and higher.
</Callout>

<Npm>
drizzle-orm@beta
drizzle-kit@beta -D
</Npm>

<br/>

We have native support for all of them, yet if that's not enough for you, feel free to create **[custom types](/docs/custom-types)**.

<Callout title='important' type='warning'>
All examples in this part of the documentation do not use database column name aliases, and column names are generated from TypeScript keys.

You can use database aliases in column names if you want, and you can also use the `casing` parameter to define a mapping strategy for Drizzle.

You can read more about it [here](/docs/sql-schema-declaration#shape-your-data-schema)
</Callout>

### bigint
`int` `int8` `int64` `integer`

Signed 8-byte integer

If you're expecting values above 2^31 but below 2^53, you can utilize `mode: 'number'` and deal with javascript number as opposed to bigint.
<Section>
```typescript
import { bigint, cockroachTable } from "drizzle-orm/cockroach-core";

export const table = cockroachTable('table', {
	bigint: bigint({ mode: 'number' })
});

// will be inferred as `number`
bigint: bigint({ mode: 'number' })

// will be inferred as `bigint`
bigint: bigint({ mode: 'bigint' })
```

```sql
CREATE TABLE "table" (
	"bigint" bigint
);
```
</Section>

<Section>
```typescript
import { sql } from "drizzle-orm";
import { bigint, cockroachTable } from "drizzle-orm/cockroach-core";

export const table = cockroachTable('table', {
	bigint1: bigint().default(10),
	bigint2: bigint().default(sql`'10'::bigint`)
});
```

```sql
CREATE TABLE "table" (
	"bigint1" bigint DEFAULT 10,
	"bigint2" bigint DEFAULT '10'::bigint
);
```
</Section>

### smallint
`smallint` `int2`
Small-range signed 2-byte integer

<Section>
```typescript
import { smallint, cockroachTable } from "drizzle-orm/cockroach-core";

export const table = cockroachTable('table', {
	smallint: smallint()
});
```

```sql
CREATE TABLE "table" (
	"smallint" smallint
);
```
</Section>

<Section>
```typescript
import { sql } from "drizzle-orm";
import { smallint, cockroachTable } from "drizzle-orm/cockroach-core";

export const table = cockroachTable('table', {
	smallint1: smallint().default(10),
	smallint2: smallint().default(sql`'10'::smallint`)
});
```

```sql
CREATE TABLE "table" (
	"smallint1" smallint DEFAULT 10,
	"smallint2" smallint DEFAULT '10'::smallint
);
```
</Section>

### int4

Signed 4-byte integer

<Section>
```typescript
import { int4, cockroachTable } from "drizzle-orm/cockroach-core";

export const table = cockroachTable('table', {
	int4: int4()
});

```

```sql
CREATE TABLE "table" (
	"int4" int4
);
```
</Section>

<Section>
```typescript
import { sql } from "drizzle-orm";
import { int4, cockroachTable } from "drizzle-orm/cockroach-core";

export const table = cockroachTable('table', {
	int1: int4().default(10),
	int2: int4().default(sql`'10'::int4`)
});
```

```sql
CREATE TABLE "table" (
	"int1" int4 DEFAULT 10,
	"int2" int4 DEFAULT '10'::int4
);
```
</Section>


### int8

An alias of **[bigint.](#bigint)**

### int2

An alias of **[smallint.](#smallint)**

### ---

### bool
Cockroach provides the standard SQL type bool.

For more info please refer to the official Cockroach **[docs.](https://www.cockroachlabs.com/docs/stable/bool)**

<Section>
```typescript
import { bool, cockroachTable } from "drizzle-orm/cockroach-core";

export const table = cockroachTable('table', {
	boolean: bool()
});

```

```sql
CREATE TABLE "table" (
	"boolean" bool
);
```
</Section>

## ---

### string
`text` `varchar`, `char`

The `STRING` data type stores a string of Unicode characters.

<Callout>
For PostgreSQL compatibility, CockroachDB supports the following STRING-related types and their aliases:

`VARCHAR` (and alias `CHARACTER VARYING`)
`CHAR` (and alias `CHARACTER`)
`NAME`
</Callout>

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/string)**

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.
<Section>
```typescript
import { string, cockroachTable } from "drizzle-orm/cockroach-core";

export const table = cockroachTable('table', {
  stringColumn: string(), // equivalent to `text` PostgreSQL type
  stringColumn1: string({ length: 256 }), // equivalent to `varchar(256)` PostgreSQL type
});

// will be inferred as text: "value1" | "value2" | null
stringColumn: string({ enum: ["value1", "value2"] })
```

```sql
CREATE TABLE "table" (
	"stringColumn" string,
    "stringColumn1" string(256),
);
```
</Section>

### text

CockroachDB alias for `STRING`:

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/string)**

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.
<Section>
```typescript
import { text, cockroachTable } from "drizzle-orm/cockroach-core";

export const table = cockroachTable('table', {
  text: text()
});

// will be inferred as text: "value1" | "value2" | null
text: text({ enum: ["value1", "value2"] })
```

```sql
CREATE TABLE "table" (
	"text" text
);
```
</Section>

### varchar
`character varying(n)` `varchar(n)`

`STRING` alias used to stay compatible with PostgreSQL

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/string)**

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.

The `length` parameter is optional according to PostgreSQL docs.
<Section>
```typescript
import { varchar, cockroachTable } from "drizzle-orm/cockroach-core";

export const table = cockroachTable('table', {
  varchar1: varchar(),
  varchar2: varchar({ length: 256 }),
});

// will be inferred as text: "value1" | "value2" | null
varchar: varchar({ enum: ["value1", "value2"] }),
```

```sql
CREATE TABLE "table" (
	"varchar1" varchar,
	"varchar2" varchar(256)
);
```
</Section>

### char
`character(n)` `char(n)`

`STRING` alias used to stay compatible with PostgreSQL

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/string)**

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.

The `length` parameter is optional according to PostgreSQL docs.
<Section>
```typescript
import { char, cockroachTable } from "drizzle-orm/cockroach-core";

export const table = cockroachTable('table', {
  char1: char(),
  char2: char({ length: 256 }),
});

// will be inferred as text: "value1" | "value2" | null
char: char({ enum: ["value1", "value2"] }),
```

```sql
CREATE TABLE "table" (
	"char1" char,
	"char2" char(256)
);
```
</Section>

## ---

https://www.cockroachlabs.com/docs/stable/float

### decimal

`numeric` `decimal` `dec`
The DECIMAL data type stores exact, fixed-point numbers. This type is used when it is important to preserve exact precision, for example, with monetary data.

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/decimal)**

<Section>
```typescript
import { decimal, cockroachTable } from "drizzle-orm/cockroach-core";

export const table = cockroachTable('table', {
  decimal1: decimal(),
  decimal2: decimal({ precision: 100 }),
  decimal3: decimal({ precision: 100, scale: 20 }),
  decimalNum: decimal({ mode: 'number' }),
  decimalBig: decimal({ mode: 'bigint' }),
});
```

```sql
CREATE TABLE "table" (
	"decimal1" decimal,
	"decimal2" decimal(100),
	"decimal3" decimal(100, 20),
	"decimalNum" decimal,
	"decimalBig" decimal
);
```
</Section>

### numeric
An alias of **[decimal.](#decimal)**

### float
`float` `float8` `double precision`

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/float)**

<Section>
```typescript
import { sql } from "drizzle-orm";
import { float, cockroachTable } from "drizzle-orm/cockroach-core";

const table = cockroachTable('table', {
	float1: float(),
	float2: float().default(10.10),
	float3: float().default(sql`'10.10'::float`),
});
```

```sql
CREATE TABLE "table" (
	"float1" float,
	"float2" float default 10.10,
	"float3" float default '10.10'::float
);
```
</Section>

### real
`real` `float4`
Single precision floating-point number (4 bytes)

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/float)**

<Section>
```typescript
import { sql } from "drizzle-orm";
import { real, cockroachTable } from "drizzle-orm/cockroach-core";

const table = cockroachTable('table', {
	real1: real(),
	real2: real().default(10.10),
	real3: real().default(sql`'10.10'::real`),
});
```

```sql
CREATE TABLE "table" (
	"real1" real,
	"real2" real default 10.10,
	"real3" real default '10.10'::real
);
```
</Section>

### double precision

An alias of **[float.](#float)**

## ---

### jsonb
`jsonb`

The JSONB data type stores JSON (JavaScript Object Notation) data as a binary representation of the JSONB value, which eliminates whitespace, duplicate keys, and key ordering

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/jsonb)**
<Section>
```typescript
import { jsonb, cockroachTable } from "drizzle-orm/cockroach-core";

const table = cockroachTable('table', {
	jsonb1: jsonb(),
	jsonb2: jsonb().default({ foo: "bar" }),
	jsonb3: jsonb().default(sql`'{foo: "bar"}'::jsonb`),
});
```
```sql
CREATE TABLE "table" (
	"jsonb1" jsonb,
	"jsonb2" jsonb default '{"foo": "bar"}'::jsonb,
	"jsonb3" jsonb default '{"foo": "bar"}'::jsonb
);
```
</Section>

You can specify `.$type<..>()` for json object inference, it **won't** check runtime values.
It provides compile time protection for default values, insert and select schemas.

```typescript
// will be inferred as { foo: string }
jsonb: jsonb().$type<{ foo: string }>();

// will be inferred as string[]
jsonb: jsonb().$type<string[]>();

// won't compile
jsonb: jsonb().$type<string[]>().default({});
```

## ---

### bit
`bit`

The BIT data types store bit arrays. With BIT, the length is fixed.

<br />

**Size**

The number of bits in a BIT value is determined as follows:

| Type&nbsp;declaration		| Logical&nbsp;size	|
|:------------------		|:--------------	|
| BIT						| 1 bit				|
| BIT(N)					| N bits			|

<br />

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/bit)**
<Section>
```typescript
import { sql } from "drizzle-orm";
import { cockroachTable, bit } from "drizzle-orm/cockroach-core";

export const table = cockroachTable('table', {
	bit1: bit(),
	bit2: bit({ length: 15 }),
	bit3: bit({ length: 15 }).default('10011'),
	bit4: bit({ length: 15 }).default(sql`'10011'`)
});
```
```sql
CREATE TABLE "table" (
	"bit1" bit,
	"bit2" bit(15),
	"bit3" bit(15) DEFAULT '10011',
	"bit4" bit(15) DEFAULT '10011'
);

```
</Section>

### varbit
`varbit`

The VARBIT data types store bit arrays. With VARBIT, the length can be variable.

<br />

**Size**

The number of bits in a VARBIT value is determined as follows:

| Type&nbsp;declaration		| Logical&nbsp;size													|
|:------------------		|:--------------													|
| VARBIT					| variable&nbsp;with&nbsp;no&nbsp;maximum							|
| VARBIT(N)					| variable&nbsp;with&nbsp;a&nbsp;maximum&nbsp;of&nbsp;N&nbsp;bits	|

<br />

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/bit)**
<Section>
```typescript
import { sql } from "drizzle-orm";
import { cockroachTable, bit } from "drizzle-orm/cockroach-core";

export const table = cockroachTable('table', {
	varbit1: varbit(),
	varbit2: varbit({ length: 15 }),
	varbit3: varbit({ length: 15 }).default('10011'),
	varbit4: varbit({ length: 15 }).default(sql`'10011'`)
});
```
```sql
CREATE TABLE "table" (
	"varbit1" varbit,
	"varbit2" varbit(15),
	"varbit3" varbit(15) DEFAULT '10011',
	"varbit4" varbit(15) DEFAULT '10011'
);
```

</Section>

## ---

### uuid
`uuid`

The UUID (Universally Unique Identifier) data type stores a 128-bit value that is unique across both space and time.

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/uuid)**

```ts
import { uuid, cockroachTable } from "drizzle-orm/cockroach-core";

const table = cockroachTable('table', {
  uuid1: uuid(),
  uuid2: uuid().defaultRandom(),
  uuid3: uuid().default('a0ee-bc99-9c0b-4ef8-bb6d-6bb9-bd38-0a11')
});
```

```sql
CREATE TABLE "table" (
	"uuid1" uuid,
	"uuid2" uuid default gen_random_uuid(),
	"uuid3" uuid default 'a0ee-bc99-9c0b-4ef8-bb6d-6bb9-bd38-0a11'
);
```

## ---

### time
`time` `timetz` `time with timezone` `time without timezone`

The `TIME` data type stores the time of day in UTC.
The `TIMETZ` data type stores a time of day with a time zone offset from UTC.

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/time)**

<Section>
```typescript
import { time, cockroachTable } from "drizzle-orm/cockroach-core";

const table = cockroachTable('table', {
  time1: time(),
  time2: time({ withTimezone: true }),
  time3: time({ precision: 6 }),
  time4: time({ precision: 6, withTimezone: true })
});
```

```sql
CREATE TABLE "table" (
	"time1" time,
	"time2" time with timezone,
	"time3" time(6),
	"time4" time(6) with timezone
);
```
</Section>

### timestamp
`timestamp` `timestamptz` `timestamp with time zone` `timestamp without time zone`

The TIMESTAMP and TIMESTAMPTZ data types store a date and time pair in UTC.

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/timestamp)**
<Section>
```typescript
import { sql } from "drizzle-orm";
import { timestamp, cockroachTable } from "drizzle-orm/cockroach-core";

const table = cockroachTable('table', {
  timestamp1: timestamp(),
	timestamp2: timestamp({ precision: 6, withTimezone: true }),
	timestamp3: timestamp().defaultNow(),
	timestamp4: timestamp().default(sql`now()`),
});
```
```sql
CREATE TABLE "table" (
	"timestamp1" timestamp,
	"timestamp2" timestamp (6) with time zone,
	"timestamp3" timestamp default now(),
	"timestamp4" timestamp default now()
);
```
</Section>

You can specify either `date` or `string` infer modes:
```typescript
// will infer as date
timestamp: timestamp({ mode: "date" }),

// will infer as string
timestamp: timestamp({ mode: "string" }),
```

> The `string` mode does not perform any mappings for you. This mode was added to Drizzle ORM to provide developers
with the possibility to handle dates and date mappings themselves, depending on their needs.
Drizzle will pass raw dates as strings `to` and `from` the database, so the behavior should be as predictable as possible
and aligned 100% with the database behavior

> The `date` mode is the regular way to work with dates. Drizzle will take care of all mappings between the database and the JS Date object

### date
`date`

The DATE data type stores a year, month, and day.

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/date)**
<Section>
```typescript
import { date, cockroachTable } from "drizzle-orm/cockroach-core";

const table = cockroachTable('table', {
	date: date(),
});
```

```sql
CREATE TABLE "table" (
	"date" date
);
```
</Section>
You can specify either `date` or `string` infer modes:
```typescript
// will infer as date
date: date({ mode: "date" }),

// will infer as string
date: date({ mode: "string" }),
```
### interval
`interval`

Stores a value that represents a span of time.

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/interval)**

<Section>
```typescript
import { interval, cockroachTable } from "drizzle-orm/cockroach-core";

const table = cockroachTable('table', {
	interval1: interval(),
  interval2: interval({ fields: 'day' }),
  interval3: interval({ fields: 'month' , precision: 6 }),
});

```

```sql
CREATE TABLE "table" (
	"interval1" interval,
	"interval2" interval day,
	"interval3" interval(6) month
);
```
</Section>

## ---

### enum
`enum` `enumerated types`
Enumerated (enum) types are data types that comprise a static, ordered set of values.
They are equivalent to the enum types supported in a number of programming languages.
An example of an enum type might be the days of the week, or a set of status values for a piece of data.

For more info please refer to the official CockroachDB **[docs.](https://www.cockroachlabs.com/docs/stable/enum)**
<Section>
```typescript
import { cockroachEnum, cockroachTable } from "drizzle-orm/cockroach-core";

export const moodEnum = cockroachEnum('mood', ['sad', 'ok', 'happy']);

export const table = cockroachTable('table', {
  mood: moodEnum(),
});
```

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');

CREATE TABLE "table" (
	"mood" mood
);
```
</Section>

## ---

### Customizing data type
Every column builder has a `.$type()` method, which allows you to customize the data type of the column.

This is useful, for example, with unknown or branded types:
```ts
type UserId = number & { __brand: 'user_id' };
type Data = {
	foo: string;
	bar: number;
};

const users = cockroachTable('users', {
  id: int().$type<UserId>().primaryKey(),
  jsonField: json().$type<Data>(),
});
```

### Identity Columns

<Callout type="info">
To use this feature you would need to have `drizzle-orm@0.32.0` or higher and `drizzle-kit@0.23.0` or higher
</Callout>

PostgreSQL and CockroachDB supports identity columns as a way to automatically generate unique integer values for a column. These values are generated using sequences and can be defined using the GENERATED AS IDENTITY clause.

**Types of Identity Columns**
- `GENERATED ALWAYS AS IDENTITY`: The database always generates a value for the column. Manual insertion or updates to this column are not allowed unless the OVERRIDING SYSTEM VALUE clause is used.
- `GENERATED BY DEFAULT AS IDENTITY`: The database generates a value by default, but manual values can also be inserted or updated. If a manual value is provided, it will be used instead of the system-generated value.

**Usage example**
```ts
import { pgTable, integer, text } from 'drizzle-orm/pg-core'

export const ingredients = pgTable("ingredients", {
  id: integer().primaryKey().generatedAlwaysAsIdentity({ startWith: 1000 }),
  name: text().notNull(),
  description: text(),
});
```

You can specify all properties available for sequences in the `.generatedAlwaysAsIdentity()` function. Additionally, you can specify custom names for these sequences

PostgreSQL docs [reference](https://www.postgresql.org/docs/current/sql-createtable.html#SQL-CREATETABLE-PARMS-GENERATED-IDENTITY).

### Default value
The `DEFAULT` clause specifies a default value to use for the column if no value
is explicitly provided by the user when doing an `INSERT`.
If there is no explicit `DEFAULT` clause attached to a column definition,
then the default value of the column is `NULL`.

An explicit `DEFAULT` clause may specify that the default value is `NULL`,
a string constant, a blob constant, a signed-number, or any constant expression enclosed in parentheses.

<Section>
```typescript
import { sql } from "drizzle-orm";
import { integer, pgTable, uuid } from "drizzle-orm/pg-core";

const table = pgTable('table', {
	integer1: integer().default(42),
	integer2: integer().default(sql`'42'::integer`),
	uuid1: uuid().defaultRandom(),
	uuid2: uuid().default(sql`gen_random_uuid()`),
});
```

```sql
CREATE TABLE IF NOT EXISTS "table" (
	"integer1" integer DEFAULT 42,
	"integer2" integer DEFAULT '42'::integer,
	"uuid1" uuid DEFAULT gen_random_uuid(),
	"uuid2" uuid DEFAULT gen_random_uuid()
);
```
</Section>

When using `$default()` or `$defaultFn()`, which are simply different aliases for the same function,
you can generate defaults at runtime and use these values in all insert queries.

These functions can assist you in utilizing various implementations such as `uuid`, `cuid`, `cuid2`, and many more.

<Callout type="info" emoji="ℹ️">
	Note: This value does not affect the `drizzle-kit` behavior, it is only used at runtime in `drizzle-orm`
</Callout>

```ts
import { text, pgTable } from "drizzle-orm/pg-core";
import { createId } from '@paralleldrive/cuid2';

const table = pgTable('table', {
	id: text().$defaultFn(() => createId()),
});
```

When using `$onUpdate()` or `$onUpdateFn()`, which are simply different aliases for the same function,
you can generate defaults at runtime and use these values in all update queries.

Adds a dynamic update value to the column. The function will be called when the row is updated,
and the returned value will be used as the column value if none is provided.
If no default (or $defaultFn) value is provided, the function will be called
when the row is inserted as well, and the returned value will be used as the column value.

<Callout type="info" emoji="ℹ️">
	Note: This value does not affect the `drizzle-kit` behavior, it is only used at runtime in `drizzle-orm`
</Callout>

```ts
import { integer, timestamp, text, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
	updateCounter: integer().default(sql`1`).$onUpdateFn((): SQL => sql`${table.update_counter} + 1`),
	updatedAt: timestamp({ mode: 'date', precision: 3 }).$onUpdate(() => new Date()),
      alwaysNull: text().$type<string | null>().$onUpdate(() => null),
});
```


### Not null
`NOT NULL` constraint dictates that the associated column may not contain a `NULL` value.

<Section>
```typescript
import { integer, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
	integer: integer().notNull(),
});
```

```sql
CREATE TABLE IF NOT EXISTS "table" (
	"integer" integer NOT NULL
);
```
</Section>


### Primary key
A primary key constraint indicates that a column, or group of columns, can be used as a unique identifier for rows in the table.
This requires that the values be both unique and not null.
<Section>
```typescript
import { serial, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
	id: serial().primaryKey(),
});
```

```sql
CREATE TABLE IF NOT EXISTS "table" (
	"id" serial PRIMARY KEY NOT NULL
);
```
</Section>


Source: https://orm.drizzle.team/docs/column-types/mssql


import Section from '@mdx/Section.astro';
import Callout from '@mdx/Callout.astro';
import Npm from '@mdx/Npm.astro';

<Callout type='error'>
This page explains concepts available on drizzle versions `1.0.0-beta.2` and higher.
</Callout>

<Npm>
drizzle-orm@beta
drizzle-kit@beta -D
</Npm>

<br/>

We have native support for all of them, yet if that's not enough for you, feel free to create **[custom types](/docs/custom-types)**.

<Callout title='important' type='warning'>
All examples in this part of the documentation do not use database column name aliases, and column names are generated from TypeScript keys.

You can use database aliases in column names if you want, and you can also use the `casing` parameter to define a mapping strategy for Drizzle.

You can read more about it [here](/docs/sql-schema-declaration#shape-your-data-schema)
</Callout>

### int
Signed 4-byte integer

<Section>
```typescript
import { int, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
	int: int()
});

```

```sql
CREATE TABLE [table] (
	[int] int
);
```
</Section>

<Section>
```typescript
import { sql } from "drizzle-orm";
import { int, mssqlTable } from "drizzle-orm/mssql-core";

export const table = pgTable('table', {
	int1: int().default(10),
});

```

```sql
CREATE TABLE [table] (
	[int1] int DEFAULT 10
);
```
</Section>

### smallint
`smallint`

Small-range signed 2-byte integer

<Section>
```typescript
import { smallint, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
	smallint: smallint()
});
```

```sql
CREATE TABLE [table] (
	[smallint] smallint
);
```
</Section>

<Section>
```typescript
import { sql } from "drizzle-orm";
import { smallint, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
	smallint1: smallint().default(10),
});
```

```sql
CREATE TABLE [table] (
	[smallint1] smallint DEFAULT 10
);
```
</Section>

### tinyint
`tinyint`

Small-range signed 1-byte integer

<Section>
```typescript
import { tinyint, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
	tinyint: tinyint()
});
```

```sql
CREATE TABLE [table] (
	[tinyint] tinyint
);
```
</Section>

<Section>
```typescript
import { sql } from "drizzle-orm";
import { tinyint, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
	tinyint1: tinyint().default(10),
});
```

```sql
CREATE TABLE [table] (
	[tinyint1] tinyint DEFAULT 10
);
```
</Section>

### bigint
`bigint`

Signed 8-byte integer

If you're expecting values above 2^31 but below 2^53, you can utilise `mode: 'number'` and deal with javascript number as opposed to bigint.
<Section>
```typescript
import { bigint, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
	bigint: bigint({ mode: 'number' })
});

// will be inferred as `number`
bigint: bigint({ mode: 'number' })

// will be inferred as `bigint`
bigint: bigint({ mode: 'bigint' })

// will be inferred as `string`
bigint: bigint({ mode: 'string' })
```

```sql
CREATE TABLE [table] (
	[bigint] bigint
);
```
</Section>

<Section>
```typescript
import { sql } from "drizzle-orm";
import { bigint, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
	bigint1: bigint({ mode: 'number' }).default(10)
});
```

```sql
CREATE TABLE [table] (
	[bigint1] bigint DEFAULT 10
);
```
</Section>

## ---

### bit

An integer data type that can take a value of `1`, `0`, or `NULL`

Drizzle will accept `true` or `false` as values instead of `1` and `0`

<Section>
```typescript
import { bit, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
	bit: bit()
});

```

```sql
CREATE TABLE [table] (
	[bit] bit
);
```
</Section>

## ---

### text
`text`
Variable-length non-Unicode data in the code page of the server and with a maximum string length
of 2^31 - 1 (2,147,483,647)

For more info please refer to the official MSSQL **[docs.](https://learn.microsoft.com/en-us/sql/t-sql/data-types/ntext-text-and-image-transact-sql?view=sql-server-ver17#text)**

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.
<Section>
```typescript
import { text, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
  text: text()
});

// will be inferred as text: "value1" | "value2" | null
text: text({ enum: ["value1", "value2"] })
```

```sql
CREATE TABLE [table] (
	[text] text
);
```
</Section>

### ntext
`text`
Variable-length Unicode data with a maximum string length of 2^30 - 1 (1,073,741,823).

For more info please refer to the official MSSQL **[docs.](https://learn.microsoft.com/en-us/sql/t-sql/data-types/ntext-text-and-image-transact-sql?view=sql-server-ver17#text)**

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.
<Section>
```typescript
import { text, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
  ntext: ntext()
});

// will be inferred as text: "value1" | "value2" | null
ntext: ntext({ enum: ["value1", "value2"] })
```

```sql
CREATE TABLE [table] (
	[ntext] ntext
);
```
</Section>

### varchar
`varchar(n|max)`
Variable-size string data. Use n to define the string size in bytes and can be a value from 1 through 8,000

For more info please refer to the official MSSQL **[docs.](https://learn.microsoft.com/en-us/sql/t-sql/data-types/char-and-varchar-transact-sql?view=sql-server-ver17#varchar---n--max--)**

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.

The `length` parameter is optional according to MSSQL docs.
<Section>
```typescript
import { varchar, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
  varchar1: varchar(),
  varchar2: varchar({ length: 256 }),
  varchar3: varchar({ length: 'max' })
});

// will be inferred as text: "value1" | "value2" | null
varchar: varchar({ enum: ["value1", "value2"] }),
```

```sql
CREATE TABLE [table] (
	[varchar1] varchar,
	[varchar2] varchar(256),
	[varchar3] varchar(max)
);
```
</Section>

### nvarchar
`nvarchar(n|max)`
Variable-size string data. The value of n defines the string size in byte-pairs

For more info please refer to the official MSSQL **[docs.](https://learn.microsoft.com/en-us/sql/t-sql/data-types/nchar-and-nvarchar-transact-sql?view=sql-server-ver17#nvarchar---n--max--)**

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.

The `length` parameter is optional according to MSSQL docs.
<Section>
```typescript
import { nvarchar, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
  nvarchar1: nvarchar(),
  nvarchar2: nvarchar({ length: 256 }),
});

// will be inferred as text: "value1" | "value2" | null
nvarchar: nvarchar({ enum: ["value1", "value2"] }),

// will be inferred as `json`
nvarchar: nvarchar({ mode: 'json' })
```

```sql
CREATE TABLE [table] (
	[nvarchar1] nvarchar,
	[nvarchar2] nvarchar(256)
);
```
</Section>

### char
`char(n)`

Fixed-size string data. n defines the string size in bytes and must be a value from 1 through 8,000

For more info please refer to the official MSSQL **[docs.](https://learn.microsoft.com/en-us/sql/t-sql/data-types/char-and-varchar-transact-sql?view=sql-server-ver17#char---n--)**

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.

The `length` parameter is optional according to MSSQL docs.
<Section>
```typescript
import { char, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
  char1: char(),
  char2: char({ length: 256 }),
});

// will be inferred as text: "value1" | "value2" | null
char: char({ enum: ["value1", "value2"] }),
```

```sql
CREATE TABLE [table] (
	[char1] char,
	[char2] char(256)
);
```
</Section>

### nchar
`nchar(n)`

Fixed-size string data. n defines the string size in byte-pairs, and must be a value from 1 through 4,000

For more info please refer to the official MSSQL **[docs.](https://learn.microsoft.com/en-us/sql/t-sql/data-types/nchar-and-nvarchar-transact-sql?view=sql-server-ver17#nchar---n--)**

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.

The `length` parameter is optional according to MSSQL docs.
<Section>
```typescript
import { nchar, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
  nchar1: nchar(),
  nchar2: nchar({ length: 256 }),
});

// will be inferred as text: "value1" | "value2" | null
nchar: nchar({ enum: ["value1", "value2"] }),
```

```sql
CREATE TABLE [table] (
	[nchar1] nchar,
	[nchar2] nchar(256)
);
```
</Section>

## ---

### binary

Fixed-length binary data with a length of n bytes, where n is a value from 1 through 8,000. The storage size is n bytes.

<Section>
```typescript
import { binary, mssqlTable } from "drizzle-orm/mssql-core";

const table = mssqlTable('table', {
	binary: binary(),
	binary1: binary({ length: 256 })
});
```

```sql
CREATE TABLE [table] (
	[binary] binary,
	[binary1] binary(256)
);
```
</Section>

### varbinary

Variable-length binary data. n can be a value from 1 through 8,000. max indicates that the maximum storage size is 2^31-1 bytes

<Section>
```typescript
import { varbinary, mssqlTable } from "drizzle-orm/mssql-core";

const table = mssqlTable('table', {
	varbinary: varbinary(),
	varbinary1: varbinary({ length: 256 }),
	varbinary2: varbinary({ length: 'max' })
});
```

```sql
CREATE TABLE [table] (
	[varbinary] varbinary,
	[varbinary1] varbinary(256),
	[varbinary2] varbinary(max)
);
```
</Section>

## ---

### numeric
`numeric`

Fixed precision and scale numbers. When maximum precision is used, valid values are from -10^38 + 1 through 10^38 - 1

For more info please refer to the official MSSQL **[docs.](https://learn.microsoft.com/en-us/sql/t-sql/data-types/decimal-and-numeric-transact-sql?view=sql-server-ver17#decimal---p---s----and-numeric---p---s---)**

<Section>
```typescript
import { numeric, mssqlTable } from "drizzle-orm/mssql-core";

export const table = mssqlTable('table', {
  numeric1: numeric(),
  numeric2: numeric({ precision: 100 }),
  numeric3: numeric({ precision: 100, scale: 20 })
//   numericNum: numeric({ mode: 'number' }),
//   numericBig: numeric({ mode: 'bigint' }),
});
```

```sql
CREATE TABLE [table] (
	[numeric1] numeric,
	[numeric2] numeric(100),
	[numeric3] numeric(100, 20)
);
```
</Section>

### decimal
An alias of **[numeric.](#numeric)**

### real

The ISO synonym for real is float(24).

For more info please refer to the official MSSQL **[docs.](https://learn.microsoft.com/en-us/sql/t-sql/data-types/float-and-real-transact-sql?view=sql-server-ver17)**

<Section>
```typescript
import { sql } from "drizzle-orm";
import { real, mssqlTable } from "drizzle-orm/mssql-core";

const table = mssqlTable('table', {
	real1: real(),
	real2: real().default(10.10)
});
```

```sql
CREATE TABLE [table] (
	[real1] real,
	[real2] real default 10.10
);
```
</Section>

### float

float [ (n) ] Where n is the number of bits that are used to store the mantissa of the float number in scientific notation and, therefore, dictates the precision and storage size. If n is specified, it must be a value between 1 and 53. The default value of n is 53.

For more info please refer to the official MSSQL **[docs.](https://learn.microsoft.com/en-us/sql/t-sql/data-types/float-and-real-transact-sql?view=sql-server-ver17#syntax)**

<Section>
```typescript
import { sql } from "drizzle-orm";
import { float, mssqlTable } from "drizzle-orm/mssql-core";

const table = mssqlTable('table', {
	float1: float(),
	float1: float({ precision: 16 })
});
```

```sql
CREATE TABLE [table] (
	[float1] float,
	[float2] float(16)
);
```
</Section>

## ---

### time
`time`

Defines a time of a day. The time is without time zone awareness and is based on a 24-hour clock.

For more info please refer to the official MSSQL **[docs.](https://learn.microsoft.com/en-us/sql/t-sql/data-types/time-transact-sql?view=sql-server-ver17#time-description)**

<Section>
```typescript
import { time, mssqlTable } from "drizzle-orm/mssql-core";

const table = mssqlTable('table', {
  time1: time(),
  time2: time({ mode: 'string' }),
  time3: time({ precision: 6 }),
  time4: time({ precision: 6, mode: 'date' })
});
```

```sql
CREATE TABLE [table] (
	[time1] time,
	[time2] time,
	[time3] time(6),
	[time4] time(6)
);
```
</Section>

### date
`date`

Calendar date (year, month, day)

For more info please refer to the official MSSQL **[docs.](https://learn.microsoft.com/en-us/sql/t-sql/data-types/date-transact-sql?view=sql-server-ver17#date-description)**
<Section>
```typescript
import { date, mssqlTable } from "drizzle-orm/mssql-core";

const table = mssqlTable('table', {
	date: date(),
});
```

```sql
CREATE TABLE [table] (
	[date] date
);
```
</Section>
You can specify either `date` or `string` infer modes:
```typescript
// will infer as date
date: date({ mode: "date" }),

// will infer as string
date: date({ mode: "string" }),
```

### datetime
`datetime`

Defines a date that is combined with a time of day with fractional seconds that is based on a 24-hour clock.

<Callout title='MSSQL docs'>
Avoid using datetime for new work. Instead, use the time, date, datetime2, and datetimeoffset data types. These types align with the SQL Standard, and are more portable. time, datetime2 and datetimeoffset provide more seconds precision. datetimeoffset provides time zone support for globally deployed applications.
</Callout>

For more info please refer to the official MSSQL **[docs.](https://learn.microsoft.com/en-us/sql/t-sql/data-types/datetime-transact-sql?view=sql-server-ver17#description)**
<Section>
```typescript
import { datetime, mssqlTable } from "drizzle-orm/mssql-core";

const table = mssqlTable('table', {
	datetime: datetime(),
});
```

```sql
CREATE TABLE [table] (
	[datetime] datetime
);
```
</Section>
You can specify either `date` or `string` infer modes:
```typescript
// will infer as date
datetime: datetime({ mode: "date" }),

// will infer as string
datetime: datetime({ mode: "string" }),
```

### datetime2
`datetime2`

Defines a date that is combined with a time of day that is based on 24-hour clock. datetime2 can be considered as an extension of the existing datetime type that has a larger date range, a larger default fractional precision, and optional user-specified precision.

For more info please refer to the official MSSQL **[docs.](https://learn.microsoft.com/en-us/sql/t-sql/data-types/datetime2-transact-sql?view=sql-server-ver17#datetime2-description)**
<Section>
```typescript
import { datetime2, mssqlTable } from "drizzle-orm/mssql-core";

const table = mssqlTable('table', {
	datetime2: datetime2(),
});
```

```sql
CREATE TABLE [table] (
	[datetime2] datetime2
);
```
</Section>
You can specify either `date` or `string` infer modes:
```typescript
// will infer as date
datetime2: datetime2({ mode: "date" }),

// will infer as string
datetime2: datetime2({ mode: "string" }),
```

### datetimeoffset
`datetimeoffset`

Defines a date that is combined with a time of a day based on a 24-hour clock like datetime2, and adds time zone awareness based on Coordinated Universal Time (UTC).

For more info please refer to the official MSSQL **[docs.](https://learn.microsoft.com/en-us/sql/t-sql/data-types/datetimeoffset-transact-sql?view=sql-server-ver17#datetimeoffset-description)**
<Section>
```typescript
import { datetimeoffset, mssqlTable } from "drizzle-orm/mssql-core";

const table = mssqlTable('table', {
	datetimeoffset: datetimeoffset(),
});
```

```sql
CREATE TABLE [table] (
	[datetimeoffset] datetimeoffset
);
```
</Section>
You can specify either `date` or `string` infer modes:
```typescript
// will infer as date
datetimeoffset: datetimeoffset({ mode: "date" }),

// will infer as string
datetimeoffset: datetimeoffset({ mode: "string" }),
```

## ---

### Customizing data type
Every column builder has a `.$type()` method, which allows you to customize the data type of the column.

This is useful, for example, with unknown or branded types:
```ts
type UserId = number & { __brand: 'user_id' };
type Data = {
	foo: string;
	bar: number;
};

const users = mssqlTable('users', {
  id: int().$type<UserId>().primaryKey(),
  jsonField: json().$type<Data>(),
});
```

### Default value
The `DEFAULT` clause specifies a default value to use for the column if no value
is explicitly provided by the user when doing an `INSERT`.
If there is no explicit `DEFAULT` clause attached to a column definition,
then the default value of the column is `NULL`.

An explicit `DEFAULT` clause may specify that the default value is `NULL`,
a string constant, a blob constant, a signed-number, or any constant expression enclosed in parentheses.

<Section>
```typescript
import { sql } from "drizzle-orm";
import { int, mssqlTable, text } from "drizzle-orm/mssql-core";

const table = mssqlTable('table', {
	integer: integer().default(42),
	text: text().default('text'),
});
```

```sql
CREATE TABLE [table] (
	[integer1] integer DEFAULT 42,
	[text] text DEFAULT 'text',
);
```
</Section>

When using `$default()` or `$defaultFn()`, which are simply different aliases for the same function,
you can generate defaults at runtime and use these values in all insert queries.

<Callout type="info" emoji="ℹ️">
	Note: This value does not affect the `drizzle-kit` behavior, it is only used at runtime in `drizzle-orm`
</Callout>

```ts
import { text, mssqlTable } from "drizzle-orm/mssql-core";
import { createId } from '@paralleldrive/cuid2';

const table = mssqlTable('table', {
	id: text().$defaultFn(() => createId()),
});
```

When using `$onUpdate()` or `$onUpdateFn()`, which are simply different aliases for the same function,
you can generate defaults at runtime and use these values in all update queries.

Adds a dynamic update value to the column. The function will be called when the row is updated,
and the returned value will be used as the column value if none is provided.
If no default (or $defaultFn) value is provided, the function will be called
when the row is inserted as well, and the returned value will be used as the column value.

<Callout type="info" emoji="ℹ️">
	Note: This value does not affect the `drizzle-kit` behavior, it is only used at runtime in `drizzle-orm`
</Callout>

```ts
import { int, datetime2, text, mssqlTable } from "drizzle-orm/mssql-core";

const table = mssqlTable('table', {
	updateCounter: int().default(sql`1`).$onUpdateFn((): SQL => sql`${table.updateCounter} + 1`),
	updatedAt: datetime2({ mode: 'date', precision: 3 }).$onUpdate(() => new Date()),
	alwaysNull: text().$type<string | null>().$onUpdate(() => null),
});
```


### Not null
`NOT NULL` constraint dictates that the associated column may not contain a `NULL` value.

<Section>
```typescript
import { int, mssqlTable } from "drizzle-orm/mssql-core";

const table = mssqlTable('table', {
	int: int().notNull(),
});
```

```sql
CREATE TABLE [table] (
	[int] int NOT NULL
);
```
</Section>


### Primary key
A primary key constraint indicates that a column, or group of columns, can be used as a unique identifier for rows in the table.
This requires that the values be both unique and not null.
<Section>
```typescript
import { int, mssqlTable } from "drizzle-orm/mssql-core";

const table = pgTable('table', {
	id: int().primaryKey(),
});
```

```sql
CREATE TABLE [table] (
	[id] int PRIMARY KEY
);
```
</Section>


Source: https://orm.drizzle.team/docs/column-types/mysql

import Section from '@mdx/Section.astro';
import Callout from '@mdx/Callout.astro';

We have native support for all of them, yet if that's not enough for you, feel free to create **[custom types](/docs/custom-types)**.

<Callout title='important' type='warning'>
All examples in this part of the documentation do not use database column name aliases, and column names are generated from TypeScript keys.

You can use database aliases in column names if you want, and you can also use the `casing` parameter to define a mapping strategy for Drizzle.

You can read more about it [here](/docs/sql-schema-declaration#shape-your-data-schema)
</Callout>

### integer

A signed integer, stored in `0`, `1`, `2`, `3`, `4`, `6`, or `8` bytes depending on the magnitude of the value.

<Section>
```typescript
import { int, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	int: int()
});
```

```sql
CREATE TABLE `table` (
	`int` int
);
```
</Section>

### tinyint

<Section>
```typescript
import { tinyint, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	tinyint: tinyint()
});
```

```sql
CREATE TABLE `table` (
	`tinyint` tinyint
);
```
</Section>

### smallint

<Section>
```typescript
import { smallint, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	smallint: smallint()
});
```

```sql
CREATE TABLE `table` (
	`smallint` smallint
);
```
</Section>

### mediumint

<Section>
```typescript
import { mediumint, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	mediumint: mediumint()
});
```

```sql
CREATE TABLE `table` (
	`mediumint` mediumint
);
```
</Section>

### bigint

<Section>
```typescript
import { bigint, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	bigint: bigint({ mode: 'number' })
	bigintUnsigned: bigint({ mode: 'number', unsigned: true })
});

bigint('...', { mode: 'number' | 'bigint' });

// You can also specify unsigned option for bigint
bigint('...', { mode: 'number' | 'bigint', unsigned: true })
```

```sql
CREATE TABLE `table` (
	`bigint` bigint,
	`bigintUnsigned` bigint unsigned
);
```
</Section>

We've omitted config of `M` in `bigint(M)`, since it indicates the display width of the numeric type

## ---

### real

<Section>
```typescript
import { real, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	real: real()
});
```

```sql
CREATE TABLE `table` (
	`real` real
);
```
</Section>

<Section>
```typescript
import { real, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	realPrecision: real({ precision: 1,}),
	realPrecisionScale: real({ precision: 1, scale: 1,}),
});
```

```sql
CREATE TABLE `table` (
	`realPrecision` real(1),
	`realPrecisionScale` real(1, 1)
);
```
</Section>

### decimal

<Section>
```typescript
import { decimal, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	decimal: decimal(),
	decimalNum: decimal({ scale: 30, mode: 'number' }),
	decimalBig: decimal({ scale: 30, mode: 'bigint' }),
});
```

```sql
CREATE TABLE `table` (
	`decimal` decimal,
	`decimalNum` decimal(30),
	`decimalBig` decimal(30)
);
```
</Section>

<Section>
```typescript
import { decimal, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	decimalPrecision: decimal({ precision: 1,}),
	decimalPrecisionScale: decimal({ precision: 1, scale: 1,}),
});
```

```sql
CREATE TABLE `table` (
	`decimalPrecision` decimal(1),
	`decimalPrecisionScale` decimal(1, 1)
);
```
</Section>

### double

<Section>
```typescript
import { double, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	double: double('double')
});
```

```sql
CREATE TABLE `table` (
	`double` double
);
```
</Section>

<Section>
```typescript
import { double, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	doublePrecision: double({ precision: 1,}),
	doublePrecisionScale: double({ precision: 1, scale: 1,}),
});
```

```sql
CREATE TABLE `table` (
	`doublePrecision` double(1),
	`doublePrecisionScale` double(1, 1)
);
```
</Section>

### float

<Section>
```typescript
import { float, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	float: float()
});
```

```sql
CREATE TABLE `table` (
	`float` float
);
```
</Section>

## ---

### serial

<Section>

`SERIAL` is an alias for `BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE`.

```typescript
import { serial, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	serial: serial()
});
```

```sql
CREATE TABLE `table` (
	`serial` serial AUTO_INCREMENT
);
```
</Section>

## ---

### binary
`BINARY(M)` stores a fixed-length byte string of exactly M bytes.
On insert, shorter values are right-padded with `0x00` bytes to reach M bytes; on retrieval, no padding is stripped.
All bytes—including trailing `0x00`—are significant in comparisons, `ORDER BY`, and `DISTINCT`
<Section>
```typescript
import { binary, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	binary: binary()
});
```

```sql
CREATE TABLE `table` (
	`binary` binary
);
```
</Section>

### varbinary
`VARBINARY(M)` stores a variable-length byte string of exactly M bytes.
On insert, shorter values are right-padded with `0x00` bytes to reach M bytes; on retrieval, no padding is stripped.
All bytes—including trailing `0x00`—are significant in comparisons, `ORDER BY`, and `DISTINCT`
<Section>
```typescript
import { varbinary, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	varbinary: varbinary({ length: 2}),
});
```

```sql
CREATE TABLE `table` (
	`varbinary` varbinary(2)
);
```
</Section>

## ---

### blob

<Callout type='warning'>
Available starting from `drizzle-orm@1.0.0-beta.2`
</Callout>

A `BLOB` is a binary large object that can hold a variable amount of data.
<Section>
```typescript
import { blob, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	blob: blob()
});
```

```sql
CREATE TABLE `table` (
	`blob` blob
);
```
</Section>

### tinyblob

<Callout type='warning'>
Available starting from `drizzle-orm@1.0.0-beta.2`
</Callout>

A `TINYBLOB` is a binary large object that can hold a variable amount of data.
<Section>
```typescript
import { tinyblob, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	tinyblob: tinyblob()
});
```

```sql
CREATE TABLE `table` (
	`tinyblob` tinyblob
);
```
</Section>

### mediumblob

<Callout type='warning'>
Available starting from `drizzle-orm@1.0.0-beta.2`
</Callout>

A `MEDIUMBLOB` is a binary large object that can hold a variable amount of data.
<Section>
```typescript
import { mediumblob, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	mediumblob: mediumblob()
});
```

```sql
CREATE TABLE `table` (
	`mediumblob` mediumblob
);
```
</Section>

### longblob

<Callout type='warning'>
Available starting from `drizzle-orm@1.0.0-beta.2`
</Callout>

A `LONGBLOB` is a binary large object that can hold a variable amount of data.
<Section>
```typescript
import { longblob, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	longblob: longblob()
});
```

```sql
CREATE TABLE `table` (
	`longblob` longblob
);
```
</Section>

## ---

### char

<Section>
```typescript
import { char, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	char: char(),
});
```

```sql
CREATE TABLE `table` (
	`char` char
);
```
</Section>

### varchar
You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.
<Section>
```typescript
import { varchar, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	varchar: varchar({ length: 2 }),
});

// will be inferred as text: "value1" | "value2" | null
varchar: varchar({ length: 6, enum: ["value1", "value2"] })
```

```sql
CREATE TABLE `table` (
	`varchar` varchar(2)
);
```
</Section>

### text

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.

<Section>
```typescript
import { text, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	text: text(),
});

// will be inferred as text: "value1" | "value2" | null
text: text({ enum: ["value1", "value2"] });
```

```sql
CREATE TABLE `table` (
	`text` text
);
```
</Section>

## ---

### boolean

<Section>
```typescript
import { boolean, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	boolean: boolean(),
});
```

```sql
CREATE TABLE `table` (
	`boolean` boolean
);
```
</Section>

## ---

### date

<Section>
```typescript
import { boolean, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	date: date(),
});
```

```sql
CREATE TABLE `table` (
	`date` date
);
```
</Section>

### datetime

<Section>
```typescript
import { datetime, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	datetime: datetime(),
});

datetime('...', { mode: 'date' | "string"}),
datetime('...', { fsp : 0..6}),
```

```sql
CREATE TABLE `table` (
	`datetime` datetime
);
```
</Section>

<Section>
```typescript
import { datetime, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	datetime: datetime({ mode: 'date', fsp: 6 }),
});
```

```sql
CREATE TABLE `table` (
	`datetime` datetime(6)
);
```
</Section>

### time

<Section>
```typescript
import { time, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	time: time(),
	timefsp: time({ fsp: 6 }),
});

time('...', { fsp: 0..6 }),
```

```sql
CREATE TABLE `table` (
	`time` time,
	`timefsp` time(6)
);
```
</Section>

### year

<Section>
```typescript
import { year, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	year: year(),
});
```

```sql
CREATE TABLE `table` (
	`year` year
);
```
</Section>

### timestamp

<Section>
```typescript
import { timestamp, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	timestamp: timestamp(),
});

timestamp('...', { mode: 'date' | "string"}),
timestamp('...', { fsp : 0..6}),
```

```sql
CREATE TABLE `table` (
	`timestamp` timestamp
);
```
</Section>

<Section>
```typescript
import { timestamp, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	timestamp: timestamp({ mode: 'date', fsp: 6 }),
});
```

```sql
CREATE TABLE `table` (
	`timestamp` timestamp(6)
);
```
</Section>

<Section>
```typescript
import { timestamp, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	timestamp: timestamp().defaultNow(),
});
```

```sql
CREATE TABLE `table` (
	`timestamp` timestamp DEFAULT (now())
);
```
</Section>

## ---

### json

<Section>
```typescript
import { json, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	json: json(),
});

```

```sql
CREATE TABLE `table` (
	`json` json
);
```
</Section>

You can specify `.$type<..>()` for json object inference, it **won't** check runtime values.
It provides compile time protection for default values, insert and select schemas.
```typescript
// will be inferred as { foo: string }
json: json().$type<{ foo: string }>();

// will be inferred as string[]
json: json().$type<string[]>();

// won't compile
json: json().$type<string[]>().default({});
```

## ---

### enum

<Section>
```typescript
import { mysqlEnum, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	popularity: mysqlEnum(['unknown', 'known', 'popular']),
});
```

```sql
CREATE TABLE `table` (
	`popularity` enum('unknown','known','popular')
);
```
</Section>

## ---

### Customizing data type

Every column builder has a `.$type()` method, which allows you to customize the data type of the column. This is useful, for example, with unknown or branded types.

```ts
type UserId = number & { __brand: 'user_id' };
type Data = {
	foo: string;
	bar: number;
};

const users = mysqlTable('users', {
  id: int().$type<UserId>().primaryKey(),
  jsonField: json().$type<Data>(),
});
```

### Not null
`NOT NULL` constraint dictates that the associated column may not contain a `NULL` value.

<Section>
```typescript
import { int, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	int: int().notNull(),
});
```

```sql
CREATE TABLE `table` (
	`int` int NOT NULL
);
```
</Section>

### Default value

The `DEFAULT` clause specifies a default value to use for the column if no value
is explicitly provided by the user when doing an `INSERT`.
If there is no explicit `DEFAULT` clause attached to a column definition,
then the default value of the column is `NULL`.

An explicit `DEFAULT` clause may specify that the default value is `NULL`,
a string constant, a blob constant, a signed-number, or any constant expression enclosed in parentheses.

<Section>
```typescript
import { int, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	int: int().default(3),
});
```

```sql
CREATE TABLE `table` (
	`int` int DEFAULT 3
);
```
</Section>

When using `$default()` or `$defaultFn()`, which are simply different aliases for the same function,
you can generate defaults at runtime and use these values in all insert queries.
These functions can assist you in utilizing various implementations such as `uuid`, `cuid`, `cuid2`, and many more.

<Callout type="info" emoji="ℹ️">
	Note: This value does not affect the `drizzle-kit` behavior, it is only used at runtime in `drizzle-orm`
</Callout>

```ts
import { varchar, mysqlTable } from "drizzle-orm/mysql-core";
import { createId } from '@paralleldrive/cuid2';

const table = mysqlTable('table', {
	id: varchar({ length: 128 }).$defaultFn(() => createId()),
});
```

When using `$onUpdate()` or `$onUpdateFn()`, which are simply different aliases for the same function,
you can generate defaults at runtime and use these values in all update queries.

Adds a dynamic update value to the column. The function will be called when the row is updated,
and the returned value will be used as the column value if none is provided.
If no default (or $defaultFn) value is provided, the function will be called
when the row is inserted as well, and the returned value will be used as the column value.

<Callout type="info" emoji="ℹ️">
	Note: This value does not affect the `drizzle-kit` behavior, it is only used at runtime in `drizzle-orm`
</Callout>

```ts
import { text, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
    alwaysNull: text().$type<string | null>().$onUpdate(() => null),
});
```

### Primary key

<Section>
```typescript
import { int, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	int: int().primaryKey(),
});
```

```sql
CREATE TABLE `table` (
	`int` int PRIMARY KEY NOT NULL
);
```
</Section>

### Auto increment

<Section>
```typescript
import { int, mysqlTable } from "drizzle-orm/mysql-core";

const table = mysqlTable('table', {
	int: int().autoincrement(),
});
```

```sql
CREATE TABLE `table` (
	`int` int AUTO_INCREMENT
);
```
</Section>


Source: https://orm.drizzle.team/docs/column-types/pg


import Section from '@mdx/Section.astro';
import Callout from '@mdx/Callout.astro';

We have native support for all of them, yet if that's not enough for you, feel free to create **[custom types](/docs/custom-types)**.

<Callout title='important' type='warning'>
All examples in this part of the documentation do not use database column name aliases, and column names are generated from TypeScript keys.

You can use database aliases in column names if you want, and you can also use the `casing` parameter to define a mapping strategy for Drizzle.

You can read more about it [here](/docs/sql-schema-declaration#shape-your-data-schema)
</Callout>

### integer
`integer` `int` `int4`
Signed 4-byte integer

If you need `integer autoincrement` please refer to **[serial.](#serial)**

<Section>
```typescript
import { integer, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
	int: integer()
});

```

```sql
CREATE TABLE "table" (
	"int" integer
);
```
</Section>

<Section>
```typescript
import { sql } from "drizzle-orm";
import { integer, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
	int1: integer().default(10),
	int2: integer().default(sql`'10'::int`)
});

```

```sql
CREATE TABLE "table" (
	"int1" integer DEFAULT 10,
	"int2" integer DEFAULT '10'::int
);
```
</Section>

### smallint
`smallint` `int2`
Small-range signed 2-byte integer

If you need `smallint autoincrement` please refer to **[smallserial.](#smallserial)**
<Section>
```typescript
import { smallint, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
	smallint: smallint()
});
```

```sql
CREATE TABLE "table" (
	"smallint" smallint
);
```
</Section>

<Section>
```typescript
import { sql } from "drizzle-orm";
import { smallint, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
	smallint1: smallint().default(10),
	smallint2: smallint().default(sql`'10'::smallint`)
});
```

```sql
CREATE TABLE "table" (
	"smallint1" smallint DEFAULT 10,
	"smallint2" smallint DEFAULT '10'::smallint
);
```
</Section>

### bigint
`bigint` `int8`
Signed 8-byte integer

If you need `bigint autoincrement` please refer to **[bigserial.](#bigserial)**

If you're expecting values above 2^31 but below 2^53, you can utilise `mode: 'number'` and deal with javascript number as opposed to bigint.
<Section>
```typescript
import { bigint, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
	bigint: bigint({ mode: 'number' })
});

// will be inferred as `number`
bigint: bigint({ mode: 'number' })

// will be inferred as `bigint`
bigint: bigint({ mode: 'bigint' })
```

```sql
CREATE TABLE "table" (
	"bigint" bigint
);
```
</Section>

<Section>
```typescript
import { sql } from "drizzle-orm";
import { bigint, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
	bigint1: bigint().default(10),
	bigint2: bigint().default(sql`'10'::bigint`)
});
```

```sql
CREATE TABLE "table" (
	"bigint1" bigint DEFAULT 10,
	"bigint2" bigint DEFAULT '10'::bigint
);
```
</Section>

## ---

### serial
`serial` `serial4`
Auto incrementing 4-bytes integer, notational convenience for creating unique identifier columns (similar to the `AUTO_INCREMENT` property supported by some other databases).

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-numeric.html#DATATYPE-SERIAL)**
<Section>
```typescript
import { serial, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
  serial: serial(),
});
```

```sql
CREATE TABLE "table" (
	"serial" serial NOT NULL
);
```
</Section>

### smallserial
`smallserial` `serial2`
Auto incrementing 2-bytes integer, notational convenience for creating unique identifier columns (similar to the `AUTO_INCREMENT` property supported by some other databases).

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-numeric.html#DATATYPE-SERIAL)**
<Section>
```typescript
import { smallserial, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
  smallserial: smallserial(),
});
```

```sql
CREATE TABLE "table" (
	"smallserial" smallserial NOT NULL
);
```
</Section>

### bigserial
`bigserial` `serial8`
Auto incrementing 8-bytes integer, notational convenience for creating unique identifier columns (similar to the `AUTO_INCREMENT` property supported by some other databases).

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-numeric.html#DATATYPE-SERIAL)**

If you're expecting values above 2^31 but below 2^53, you can utilise `mode: 'number'` and deal with javascript number as opposed to bigint.
<Section>
```typescript
import { bigserial, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
  bigserial: bigserial({ mode: 'number' }),
});
```

```sql
CREATE TABLE "table" (
	"bigserial" bigserial NOT NULL
);
```
</Section>

### ---

### boolean
PostgreSQL provides the standard SQL type boolean.

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-boolean.html)**

<Section>
```typescript
import { boolean, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
	boolean: boolean()
});

```

```sql
CREATE TABLE "table" (
	"boolean" boolean
);
```
</Section>

## ---

### bytea

PostgreSQL provides the standard SQL type bytea.

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-binary.html)**

<Section>
```typescript
import { bytea, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
	bytea: bytea()
});

```

```sql
CREATE TABLE IF NOT EXISTS "table" (
	"bytea" bytea,
);
```
</Section>

## ---

### text
`text`
Variable-length(unlimited) character string.

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-character.html)**

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.
<Section>
```typescript
import { text, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
  text: text()
});

// will be inferred as text: "value1" | "value2" | null
text: text({ enum: ["value1", "value2"] })
```

```sql
CREATE TABLE "table" (
	"text" text
);
```
</Section>

### varchar
`character varying(n)` `varchar(n)`
Variable-length character string, can store strings up to **`n`** characters (not bytes).

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-character.html)**

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.

The `length` parameter is optional according to PostgreSQL docs.
<Section>
```typescript
import { varchar, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
  varchar1: varchar(),
  varchar2: varchar({ length: 256 }),
});

// will be inferred as text: "value1" | "value2" | null
varchar: varchar({ enum: ["value1", "value2"] }),
```

```sql
CREATE TABLE "table" (
	"varchar1" varchar,
	"varchar2" varchar(256)
);
```
</Section>

### char
`character(n)` `char(n)`
Fixed-length, blank padded character string, can store strings up to **`n`** characters(not bytes).

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-character.html)**

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.

The `length` parameter is optional according to PostgreSQL docs.
<Section>
```typescript
import { char, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
  char1: char(),
  char2: char({ length: 256 }),
});

// will be inferred as text: "value1" | "value2" | null
char: char({ enum: ["value1", "value2"] }),
```

```sql
CREATE TABLE "table" (
	"char1" char,
	"char2" char(256)
);
```
</Section>

## ---

### numeric
`numeric` `decimal`
Exact numeric of selectable precision. Can store numbers with a very large number of digits, up to 131072 digits before the decimal point and up to 16383 digits after the decimal point.

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-numeric.html#DATATYPE-NUMERIC-DECIMAL)**

<Section>
```typescript
import { numeric, pgTable } from "drizzle-orm/pg-core";

export const table = pgTable('table', {
  numeric1: numeric(),
  numeric2: numeric({ precision: 100 }),
  numeric3: numeric({ precision: 100, scale: 20 }),
  numericNum: numeric({ mode: 'number' }),
  numericBig: numeric({ mode: 'bigint' }),
});
```

```sql
CREATE TABLE "table" (
	"numeric1" numeric,
	"numeric2" numeric(100),
	"numeric3" numeric(100, 20),
	"numericNum" numeric,
	"numericBig" numeric
);
```
</Section>

### decimal
An alias of **[numeric.](#numeric)**

### real
`real` `float4`
Single precision floating-point number (4 bytes)

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-numeric.html)**

<Section>
```typescript
import { sql } from "drizzle-orm";
import { real, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
	real1: real(),
	real2: real().default(10.10),
	real3: real().default(sql`'10.10'::real`),
});
```

```sql
CREATE TABLE "table" (
	"real1" real,
	"real2" real default 10.10,
	"real3" real default '10.10'::real
);
```
</Section>

### double precision
`double precision` `float8`
Double precision floating-point number (8 bytes)

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-numeric.html)**

<Section>
```typescript
import { sql } from "drizzle-orm";
import { doublePrecision, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
	double1: doublePrecision(),
	double2: doublePrecision().default(10.10),
	double3: doublePrecision().default(sql`'10.10'::double precision`),
});
```

```sql
CREATE TABLE "table" (
	"double1" double precision,
	"double2" double precision default 10.10,
	"double3" double precision default '10.10'::double precision
);
```
</Section>

## ---


### json
`json`
Textual JSON data, as specified in **[RFC 7159.](https://tools.ietf.org/html/rfc7159)**

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-json.html)**
<Section>
```typescript
import { sql } from "drizzle-orm";
import { json, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
	json1: json(),
	json2: json().default({ foo: "bar" }),
	json3: json().default(sql`'{foo: "bar"}'::json`),
});
```

```sql
CREATE TABLE "table" (
	"json1" json,
	"json2" json default '{"foo": "bar"}'::json,
	"json3" json default '{"foo": "bar"}'::json
);
```
</Section>

You can specify `.$type<..>()` for json object inference, it **won't** check runtime values.
It provides compile time protection for default values, insert and select schemas.
```typescript
// will be inferred as { foo: string }
json: json().$type<{ foo: string }>();

// will be inferred as string[]
json: json().$type<string[]>();

// won't compile
json: json().$type<string[]>().default({});
```

### jsonb
`jsonb`
Binary JSON data, decomposed.

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-json.html)**
<Section>
```typescript
import { jsonb, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
	jsonb1: jsonb(),
	jsonb2: jsonb().default({ foo: "bar" }),
	jsonb3: jsonb().default(sql`'{foo: "bar"}'::jsonb`),
});
```
```sql
CREATE TABLE "table" (
	"jsonb1" jsonb,
	"jsonb2" jsonb default '{"foo": "bar"}'::jsonb,
	"jsonb3" jsonb default '{"foo": "bar"}'::jsonb
);
```
</Section>

You can specify `.$type<..>()` for json object inference, it **won't** check runtime values.
It provides compile time protection for default values, insert and select schemas.

```typescript
// will be inferred as { foo: string }
jsonb: jsonb().$type<{ foo: string }>();

// will be inferred as string[]
jsonb: jsonb().$type<string[]>();

// won't compile
jsonb: jsonb().$type<string[]>().default({});
```

## ---

### uuid
`uuid`

The data type uuid stores Universally Unique Identifiers (UUID) as defined by RFC 4122, ISO/IEC 9834-8:2005, and related standards

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-uuid.html)**

```ts
import { uuid, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
  uuid1: uuid(),
  uuid2: uuid().defaultRandom(),
  uuid3: uuid().default('a0ee-bc99-9c0b-4ef8-bb6d-6bb9-bd38-0a11')
});
```

```sql
CREATE TABLE "table" (
	"uuid1" uuid,
	"uuid2" uuid default gen_random_uuid(),
	"uuid3" uuid default 'a0ee-bc99-9c0b-4ef8-bb6d-6bb9-bd38-0a11'
);
```

## ---

### time
`time` `timetz` `time with timezone` `time without timezone`
Time of day with or without time zone.

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-datetime.html)**

<Section>
```typescript
import { time, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
  time1: time(),
  time2: time({ withTimezone: true }),
  time3: time({ precision: 6 }),
  time4: time({ precision: 6, withTimezone: true })
});
```

```sql
CREATE TABLE "table" (
	"time1" time,
	"time2" time with timezone,
	"time3" time(6),
	"time4" time(6) with timezone
);
```
</Section>

### timestamp
`timestamp` `timestamptz` `timestamp with time zone` `timestamp without time zone`
Date and time with or without time zone.

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-datetime.html)**
<Section>
```typescript
import { sql } from "drizzle-orm";
import { timestamp, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
  timestamp1: timestamp(),
	timestamp2: timestamp({ precision: 6, withTimezone: true }),
	timestamp3: timestamp().defaultNow(),
	timestamp4: timestamp().default(sql`now()`),
});
```
```sql
CREATE TABLE "table" (
	"timestamp1" timestamp,
	"timestamp2" timestamp (6) with time zone,
	"timestamp3" timestamp default now(),
	"timestamp4" timestamp default now()
);
```
</Section>

You can specify either `date` or `string` infer modes:
```typescript
// will infer as date
timestamp: timestamp({ mode: "date" }),

// will infer as string
timestamp: timestamp({ mode: "string" }),
```

> The `string` mode does not perform any mappings for you. This mode was added to Drizzle ORM to provide developers
with the possibility to handle dates and date mappings themselves, depending on their needs.
Drizzle will pass raw dates as strings `to` and `from` the database, so the behavior should be as predictable as possible
and aligned 100% with the database behavior

> The `date` mode is the regular way to work with dates. Drizzle will take care of all mappings between the database and the JS Date object

<Callout type='info' emoji='ℹ️'>
 How mapping works for `timestamp` and `timestamp with timezone`:

 As PostgreSQL docs stated:
 > In a literal that has been determined to be timestamp without time zone, PostgreSQL will silently ignore any time zone indication.
 > That is, the resulting value is derived from the date/time fields in the input value, and is not adjusted for time zone.
 >
 > For timestamp with time zone, the internally stored value is always in UTC (Universal Coordinated Time, traditionally known as Greenwich Mean Time, GMT).
 An input value that has an explicit time zone specified is converted to UTC using the appropriate offset for that time zone.
 If no time zone is stated in the input string, then it is assumed to be in the time zone indicated by the system's TimeZone parameter,
 and is converted to UTC using the offset for the timezone zone.

 So for `timestamp with timezone` you will get back string converted to a timezone set in your Postgres instance.
 You can check timezone using this sql query:

 ```sql
 show timezone;
 ```


</Callout>

### date
`date`
Calendar date (year, month, day)

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-datetime.html)**
<Section>
```typescript
import { date, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
	date: date(),
});
```

```sql
CREATE TABLE "table" (
	"date" date
);
```
</Section>
You can specify either `date` or `string` infer modes:
```typescript
// will infer as date
date: date({ mode: "date" }),

// will infer as string
date: date({ mode: "string" }),
```
### interval
`interval`
Time span

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-datetime.html)**

<Section>
```typescript
import { interval, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
	interval1: interval(),
  interval2: interval({ fields: 'day' }),
  interval3: interval({ fields: 'month' , precision: 6 }),
});

```

```sql
CREATE TABLE "table" (
	"interval1" interval,
	"interval2" interval day,
	"interval3" interval(6) month
);
```
</Section>

## ---

### point
`point`
Geometric point type

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-geometric.html#DATATYPE-GEOMETRIC-POINTS)**

Type `point` has 2 modes for mappings from the database: `tuple` and `xy`.

- `tuple` will be accepted for insert and mapped on select to a tuple. So, the database Point(1,2) will be typed as [1,2] with drizzle.

- `xy` will be accepted for insert and mapped on select to an object with x, y coordinates. So, the database Point(1,2) will be typed as `{ x: 1, y: 2 }` with drizzle

<Section>
```typescript
const items = pgTable('items', {
 point: point(),
 pointObj: point({ mode: 'xy' }),
});
```

```sql
CREATE TABLE "items" (
	"point" point,
	"pointObj" point
);
```
</Section>

### line
`line`
Geometric line type

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-geometric.html#DATATYPE-LINE)**

Type `line` has 2 modes for mappings from the database: `tuple` and `abc`.

- `tuple` will be accepted for insert and mapped on select to a tuple. So, the database Line{1,2,3} will be typed as [1,2,3] with drizzle.

- `abc` will be accepted for insert and mapped on select to an object with a, b, and c constants from the equation `Ax + By + C = 0`. So, the database Line{1,2,3} will be typed as `{ a: 1, b: 2, c: 3 }` with drizzle.

<Section>
```typescript
const items = pgTable('items', {
 line: line(),
 lineObj: line({ mode: 'abc' }),
});
```

```sql
CREATE TABLE "items" (
	"line" line,
	"lineObj" line
);
```
</Section>

## ---

### enum
`enum` `enumerated types`
Enumerated (enum) types are data types that comprise a static, ordered set of values.
They are equivalent to the enum types supported in a number of programming languages.
An example of an enum type might be the days of the week, or a set of status values for a piece of data.

For more info please refer to the official PostgreSQL **[docs.](https://www.postgresql.org/docs/current/datatype-enum.html)**
<Section>
```typescript
import { pgEnum, pgTable } from "drizzle-orm/pg-core";

export const moodEnum = pgEnum('mood', ['sad', 'ok', 'happy']);

export const table = pgTable('table', {
  mood: moodEnum(),
});
```

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');

CREATE TABLE "table" (
	"mood" mood
);
```
</Section>

## ---

### Customizing data type
Every column builder has a `.$type()` method, which allows you to customize the data type of the column.

This is useful, for example, with unknown or branded types:
```ts
type UserId = number & { __brand: 'user_id' };
type Data = {
	foo: string;
	bar: number;
};

const users = pgTable('users', {
  id: serial().$type<UserId>().primaryKey(),
  jsonField: json().$type<Data>(),
});
```

### Identity Columns

<Callout type="info">
To use this feature you would need to have `drizzle-orm@0.32.0` or higher and `drizzle-kit@0.23.0` or higher
</Callout>

PostgreSQL supports identity columns as a way to automatically generate unique integer values for a column. These values are generated using sequences and can be defined using the GENERATED AS IDENTITY clause.

**Types of Identity Columns**
- `GENERATED ALWAYS AS IDENTITY`: The database always generates a value for the column. Manual insertion or updates to this column are not allowed unless the OVERRIDING SYSTEM VALUE clause is used.
- `GENERATED BY DEFAULT AS IDENTITY`: The database generates a value by default, but manual values can also be inserted or updated. If a manual value is provided, it will be used instead of the system-generated value.

**Key Features**
- Automatic Value Generation: Utilizes sequences to generate unique values for each new row.
- Customizable Sequence Options: You can define starting values, increments, and other sequence options.
- Support for Multiple Identity Columns: PostgreSQL allows more than one identity column per table.

**Limitations**
- Manual Insertion Restrictions: For columns defined with GENERATED ALWAYS AS IDENTITY, manual insertion or updates require the OVERRIDING SYSTEM VALUE clause.
- Sequence Constraints: Identity columns depend on sequences, which must be managed correctly to avoid conflicts or gaps.

**Usage example**
```ts
import { pgTable, integer, text } from 'drizzle-orm/pg-core'

export const ingredients = pgTable("ingredients", {
  id: integer().primaryKey().generatedAlwaysAsIdentity({ startWith: 1000 }),
  name: text().notNull(),
  description: text(),
});
```

You can specify all properties available for sequences in the `.generatedAlwaysAsIdentity()` function. Additionally, you can specify custom names for these sequences

PostgreSQL docs [reference](https://www.postgresql.org/docs/current/sql-createtable.html#SQL-CREATETABLE-PARMS-GENERATED-IDENTITY).

### Default value
The `DEFAULT` clause specifies a default value to use for the column if no value
is explicitly provided by the user when doing an `INSERT`.
If there is no explicit `DEFAULT` clause attached to a column definition,
then the default value of the column is `NULL`.

An explicit `DEFAULT` clause may specify that the default value is `NULL`,
a string constant, a blob constant, a signed-number, or any constant expression enclosed in parentheses.

<Section>
```typescript
import { sql } from "drizzle-orm";
import { integer, pgTable, uuid } from "drizzle-orm/pg-core";

const table = pgTable('table', {
	integer1: integer().default(42),
	integer2: integer().default(sql`'42'::integer`),
	uuid1: uuid().defaultRandom(),
	uuid2: uuid().default(sql`gen_random_uuid()`),
});
```

```sql
CREATE TABLE "table" (
	"integer1" integer DEFAULT 42,
	"integer2" integer DEFAULT '42'::integer,
	"uuid1" uuid DEFAULT gen_random_uuid(),
	"uuid2" uuid DEFAULT gen_random_uuid()
);
```
</Section>

When using `$default()` or `$defaultFn()`, which are simply different aliases for the same function,
you can generate defaults at runtime and use these values in all insert queries.

These functions can assist you in utilizing various implementations such as `uuid`, `cuid`, `cuid2`, and many more.

<Callout type="info" emoji="ℹ️">
	Note: This value does not affect the `drizzle-kit` behavior, it is only used at runtime in `drizzle-orm`
</Callout>

```ts
import { text, pgTable } from "drizzle-orm/pg-core";
import { createId } from '@paralleldrive/cuid2';

const table = pgTable('table', {
	id: text().$defaultFn(() => createId()),
});
```

When using `$onUpdate()` or `$onUpdateFn()`, which are simply different aliases for the same function,
you can generate defaults at runtime and use these values in all update queries.

Adds a dynamic update value to the column. The function will be called when the row is updated,
and the returned value will be used as the column value if none is provided.
If no default (or $defaultFn) value is provided, the function will be called
when the row is inserted as well, and the returned value will be used as the column value.

<Callout type="info" emoji="ℹ️">
	Note: This value does not affect the `drizzle-kit` behavior, it is only used at runtime in `drizzle-orm`
</Callout>

```ts
import { integer, timestamp, text, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
	updateCounter: integer().default(sql`1`).$onUpdateFn((): SQL => sql`${table.update_counter} + 1`),
	updatedAt: timestamp({ mode: 'date', precision: 3 }).$onUpdate(() => new Date()),
      alwaysNull: text().$type<string | null>().$onUpdate(() => null),
});
```


### Not null
`NOT NULL` constraint dictates that the associated column may not contain a `NULL` value.

<Section>
```typescript
import { integer, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
	integer: integer().notNull(),
});
```

```sql
CREATE TABLE "table" (
	"integer" integer NOT NULL
);
```
</Section>


### Primary key
A primary key constraint indicates that a column, or group of columns, can be used as a unique identifier for rows in the table.
This requires that the values be both unique and not null.
<Section>
```typescript
import { serial, pgTable } from "drizzle-orm/pg-core";

const table = pgTable('table', {
	id: serial().primaryKey(),
});
```

```sql
CREATE TABLE "table" (
	"id" serial PRIMARY KEY NOT NULL
);
```
</Section>


Source: https://orm.drizzle.team/docs/column-types/singlestore

import Section from '@mdx/Section.astro';
import Callout from '@mdx/Callout.astro';

We have native support for all of them, yet if that's not enough for you, feel free to create **[custom types](/docs/custom-types)**.

<Callout title='important' type='warning'>
All examples in this part of the documentation do not use database column name aliases, and column names are generated from TypeScript keys.

You can use database aliases in column names if you want, and you can also use the `casing` parameter to define a mapping strategy for Drizzle.

You can read more about it [here](/docs/sql-schema-declaration#shape-your-data-schema)
</Callout>

### integer

A signed integer, stored in `0`, `1`, `2`, `3`, `4`, `6`, or `8` bytes depending on the magnitude of the value.

<Section>
```typescript
import { int, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	int: int()
});
```

```sql
CREATE TABLE `table` (
	`int` int
);
```
</Section>

### tinyint

<Section>
```typescript
import { tinyint, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	tinyint: tinyint()
});
```

```sql
CREATE TABLE `table` (
	`tinyint` tinyint
);
```
</Section>

### smallint

<Section>
```typescript
import { smallint, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	smallint: smallint()
});
```

```sql
CREATE TABLE `table` (
	`smallint` smallint
);
```
</Section>

### mediumint

<Section>
```typescript
import { mediumint, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	mediumint: mediumint()
});
```

```sql
CREATE TABLE `table` (
	`mediumint` mediumint
);
```
</Section>

### bigint

<Section>
```typescript
import { bigint, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	bigint: bigint({ mode: 'number' })
	bigintUnsigned: bigint({ mode: 'number', unsigned: true })
});

bigint('...', { mode: 'number' | 'bigint' });

// You can also specify unsigned option for bigint
bigint('...', { mode: 'number' | 'bigint', unsigned: true })
```

```sql
CREATE TABLE `table` (
	`bigint` bigint,
	`bigintUnsigned` bigint unsigned
);
```
</Section>

We've omitted config of `M` in `bigint(M)`, since it indicates the display width of the numeric type

## ---

### real

<Section>
```typescript
import { real, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	real: real()
});
```

```sql
CREATE TABLE `table` (
	`real` real
);
```
</Section>

<Section>
```typescript
import { real, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	realPrecision: real({ precision: 1,}),
	realPrecisionScale: real({ precision: 1, scale: 1,}),
});
```

```sql
CREATE TABLE `table` (
	`realPrecision` real(1),
	`realPrecisionScale` real(1, 1)
);
```
</Section>

### decimal

<Section>
```typescript
import { decimal, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	decimal: decimal(),
	decimalNum: decimal({ scale: 30, mode: 'number' }),
	decimalBig: decimal({ scale: 30, mode: 'bigint' }),
});
```

```sql
CREATE TABLE `table` (
	`decimal` decimal,
	`decimalNum` decimal(30),
	`decimalBig` decimal(30)
);
```
</Section>

<Section>
```typescript
import { decimal, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	decimalPrecision: decimal({ precision: 1,}),
	decimalPrecisionScale: decimal({ precision: 1, scale: 1,}),
});
```

```sql
CREATE TABLE `table` (
	`decimalPrecision` decimal(1),
	`decimalPrecisionScale` decimal(1, 1)
);
```
</Section>

### double

<Section>
```typescript
import { double, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	double: double('double')
});
```

```sql
CREATE TABLE `table` (
	`double` double
);
```
</Section>

<Section>
```typescript
import { double, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	doublePrecision: double({ precision: 1,}),
	doublePrecisionScale: double({ precision: 1, scale: 1,}),
});
```

```sql
CREATE TABLE `table` (
	`doublePrecision` double(1),
	`doublePrecisionScale` double(1, 1)
);
```
</Section>

### float

<Section>
```typescript
import { float, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	float: float()
});
```

```sql
CREATE TABLE `table` (
	`float` float
);
```
</Section>

## ---

### serial

<Section>

`SERIAL` is an alias for `BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE`.

```typescript
import { serial, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	serial: serial()
});
```

```sql
CREATE TABLE `table` (
	`serial` serial AUTO_INCREMENT
);
```
</Section>

## ---

### binary

<Section>
```typescript
import { binary, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	binary: binary()
});
```

```sql
CREATE TABLE `table` (
	`binary` binary
);
```
</Section>

### varbinary

<Section>
```typescript
import { varbinary, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	varbinary: varbinary({ length: 2}),
});
```

```sql
CREATE TABLE `table` (
	`varbinary` varbinary(2)
);
```
</Section>

## ---

### char

<Section>
```typescript
import { char, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	char: char(),
});
```

```sql
CREATE TABLE `table` (
	`char` char
);
```
</Section>

### varchar
You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.
<Section>
```typescript
import { varchar, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	varchar: varchar({ length: 2 }),
});

// will be inferred as text: "value1" | "value2" | null
varchar: varchar({ length: 6, enum: ["value1", "value2"] })
```

```sql
CREATE TABLE `table` (
	`varchar` varchar(2)
);
```
</Section>

### text

You can define `{ enum: ["value1", "value2"] }` config to infer `insert` and `select` types, it **won't** check runtime values.

<Section>
```typescript
import { text, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	text: text(),
});

// will be inferred as text: "value1" | "value2" | null
text: text({ enum: ["value1", "value2"] });
```

```sql
CREATE TABLE `table` (
	`text` text
);
```
</Section>

## ---

### boolean

<Section>
```typescript
import { boolean, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	boolean: boolean(),
});
```

```sql
CREATE TABLE `table` (
	`boolean` boolean
);
```
</Section>

## ---

### date

<Section>
```typescript
import { boolean, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	date: date(),
});
```

```sql
CREATE TABLE `table` (
	`date` date
);
```
</Section>

### datetime

<Section>
```typescript
import { datetime, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	datetime: datetime(),
});

datetime('...', { mode: 'date' | "string"}),
```

```sql
CREATE TABLE `table` (
	`datetime` datetime
);
```
</Section>

### time

<Section>
```typescript
import { time, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	time: time(),
});
```

```sql
CREATE TABLE `table` (
	`time` time
);
```
</Section>

### year

<Section>
```typescript
import { year, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	year: year(),
});
```

```sql
CREATE TABLE `table` (
	`year` year
);
```
</Section>

### timestamp

<Section>
```typescript
import { timestamp, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	timestamp: timestamp(),
});

timestamp('...', { mode: 'date' | "string"}),
```

```sql
CREATE TABLE `table` (
	`timestamp` timestamp
);
```
</Section>

<Section>
```typescript
import { timestamp, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	timestamp: timestamp().defaultNow(),
});
```

```sql
CREATE TABLE `table` (
	`timestamp` timestamp DEFAULT (now())
);
```
</Section>

## ---

### json

<Section>
```typescript
import { json, singlestoreTable } from "drizzle-orm/singlestore-core";

const table = singlestoreTable('table', {
	json: json(),
});

```

```sql
CREATE TABLE `table` (
	`json` json
);
```
</Section>

You can specify `.$type<..>()` for json object inference, it **won't** check runtime values.
It provides compile time protection for default values, insert and select schemas.
```typescript
// will be inferred as { foo: string }
json: json().$type<{ foo: string }>();

// will be inferred as string[]
json: json().$type<string[]>();

// won't compile
json: json().$type<string[]>().default({});
```

## ---

### enum

<Section>
```typescript
import { singlestoreEnum, singlestoreTable } from "drizzle-orm/singlestore-core";

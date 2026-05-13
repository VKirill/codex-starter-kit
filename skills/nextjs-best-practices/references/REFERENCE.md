# Next.js 15 App Router — Project-Specific Reference

> Source: Next.js docs + project analysis | Project: DesignHub | Generated: 2026-03-21

## Паттерны DesignHub

DesignHub uses Next.js 15.4 + Payload CMS 3.70 + React 19. Key patterns:
- **Payload Local API** for server-side data (no HTTP calls)
- **`unstable_cache`** with tag-based revalidation
- **Route Handlers** for custom API endpoints (auth, search, parser)
- **`revalidatePath` + `revalidateTag`** in Payload lifecycle hooks
- **Route groups**: `(frontend)` for public site, `(payload)` for CMS admin

## Data fetching with Payload Local API

```ts
// src/utilities/getGlobals.ts — cached global data
import configPromise from '@payload-config'
import { getPayload } from 'payload'
import { unstable_cache } from 'next/cache'

type Global = keyof Config['globals']

async function getGlobal(slug: Global, depth = 0) {
  const payload = await getPayload({ config: configPromise })
  const global = await payload.findGlobal({ slug, depth })
  return global
}

// Wrap with unstable_cache + tag for on-demand revalidation
export const getCachedGlobal = (slug: Global, depth = 0) =>
  unstable_cache(async () => getGlobal(slug, depth), [slug], {
    tags: [`global_${slug}`],
  })
```

Usage in Server Component:

```tsx
// src/app/(frontend)/layout.tsx
export default async function Layout({ children }) {
  const header = await getCachedGlobal('header', 1)()
  const footer = await getCachedGlobal('footer', 1)()

  return (
    <html>
      <body>
        <HeaderClient header={header} />
        {children}
        <Footer footer={footer} />
      </body>
    </html>
  )
}
```

## Document fetching with cache tags

```ts
// src/utilities/getDocument.ts
import { unstable_cache } from 'next/cache'
import { getPayload } from 'payload'

async function getDocument(collection: string, slug: string) {
  const payload = await getPayload({ config: configPromise })
  const page = await payload.find({
    collection,
    where: { slug: { equals: slug } },
    depth: 2,
  })
  return page.docs[0] || null
}

// Cache key includes collection + slug, tag enables targeted revalidation
export const getCachedDocument = (collection: string, slug: string) =>
  unstable_cache(async () => getDocument(collection, slug), [collection, slug], {
    tags: [collection, `${collection}_${slug}`],
  })
```

## On-demand revalidation via Payload hooks

```ts
// src/collections/Posts/hooks/revalidatePost.ts
import type { CollectionAfterChangeHook, CollectionAfterDeleteHook } from 'payload'
import { revalidatePath, revalidateTag } from 'next/cache'

export const revalidatePost: CollectionAfterChangeHook<Post> = ({
  doc, previousDoc, req: { payload, context },
}) => {
  if (!context.disableRevalidate) {
    if (doc._status === 'published') {
      const path = `/posts/${doc.slug}`
      payload.logger.info(`Revalidating post at path: ${path}`)
      revalidatePath(path)
      revalidateTag('posts-sitemap')
    }

    // Revalidate old path if post was unpublished
    if (previousDoc._status === 'published' && doc._status !== 'published') {
      const oldPath = `/posts/${previousDoc.slug}`
      revalidatePath(oldPath)
      revalidateTag('posts-sitemap')
    }
  }
  return doc
}

export const revalidateDelete: CollectionAfterDeleteHook<Post> = ({
  doc, req: { context },
}) => {
  if (!context.disableRevalidate) {
    revalidatePath(`/posts/${doc?.slug}`)
    revalidateTag('posts-sitemap')
  }
  return doc
}
```

**Pattern**: `disableRevalidate` context flag prevents infinite loops during seed/import.

## Route Handlers (API endpoints)

```ts
// src/app/api/auth/telegram/route.ts — typical pattern
import { getPayload } from 'payload'
import config from '@payload-config'
import { NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'

export async function POST(request: Request) {
  try {
    const body = await request.json()

    if (!body.id || !body.hash) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 },
      )
    }

    const payload = await getPayload({ config })
    const user = await payload.find({
      collection: 'users',
      where: { telegramId: { equals: body.id } },
      overrideAccess: true,
    })

    const response = NextResponse.json({ success: true, user: userData })
    response.cookies.set('payload-token', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      path: '/',
      maxAge: 60 * 60 * 24 * 30, // 30 days
    })

    return response
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 },
    )
  }
}
```

### Reading cookies in Route Handlers

```ts
// src/app/api/user/status/route.ts
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function GET() {
  const cookieStore = await cookies() // async in Next.js 15!
  const token = cookieStore.get('payload-token')?.value

  if (!token) {
    return NextResponse.json({ authenticated: false }, { status: 401 })
  }

  const meReq = await fetch(`${serverUrl}/api/users/me`, {
    headers: { Authorization: `JWT ${token}` },
  })

  return NextResponse.json({ authenticated: true, user: data })
}
```

## Metadata generation

```ts
// src/utilities/generateMeta.ts
import type { Metadata } from 'next'

export const generateMeta = async (args: {
  doc: Partial<Page> | Partial<Post> | null
}): Promise<Metadata> => {
  const { doc } = args
  const ogImage = getImageURL(doc?.meta?.image)

  const title = doc?.meta?.title
    ? doc?.meta?.title + ' | DesignHub'
    : 'DesignHub'

  return {
    description: doc?.meta?.description,
    openGraph: mergeOpenGraph({
      description: doc?.meta?.description || '',
      images: ogImage ? [{ url: ogImage }] : undefined,
      title,
      url: Array.isArray(doc?.slug) ? doc?.slug.join('/') : '/',
    }),
    title,
  }
}
```

Usage in page:

```tsx
// src/app/(frontend)/posts/[slug]/page.tsx
export async function generateMetadata({ params }: Args): Promise<Metadata> {
  const { slug } = await params // Next.js 15: params is a Promise!
  const post = await getCachedDocument('posts', slug)()
  return generateMeta({ doc: post })
}
```

## Next.js 15 breaking changes (critical for DesignHub)

### Async params and searchParams

```tsx
// ❌ Next.js 14 style (BROKEN in 15)
export default function Page({ params }: { params: { slug: string } }) {
  const { slug } = params
}

// ✅ Next.js 15 style
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
}
```

### Async cookies() and headers()

```tsx
// ❌ Next.js 14
const cookieStore = cookies()

// ✅ Next.js 15
const cookieStore = await cookies()
const headersList = await headers()
```

## Route groups pattern

```
src/app/
├── (frontend)/          # Public SSR site — no URL prefix
│   ├── layout.tsx       # Header + Footer + Providers
│   ├── [slug]/page.tsx  # Dynamic CMS pages
│   ├── posts/           # Blog section
│   └── (sitemaps)/      # XML sitemaps (nested group)
├── (payload)/           # Payload CMS admin — /admin/*
│   ├── admin/
│   └── api/
│       ├── graphql/     # Auto-generated GraphQL
│       └── graphql-playground/
└── api/                 # Custom API routes (NOT inside any group)
    ├── auth/telegram/
    ├── parsing/
    ├── search/
    └── user/
```

## Client vs Server component split

```tsx
// Server Component (default) — fetches data
// src/Header/Component.tsx
import { getCachedGlobal } from '@/utilities/getGlobals'
import { HeaderClient } from './Component.client'

export async function Header() {
  const headerData = await getCachedGlobal('header', 1)()
  return <HeaderClient header={headerData} />
}

// Client Component — handles interactivity
// src/Header/Component.client.tsx
'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

export function HeaderClient({ header }: { header: Header }) {
  const pathname = usePathname()
  // interactive navigation logic
}
```

## Dynamic route config exports

```ts
// Force dynamic rendering (no caching)
export const dynamic = 'force-dynamic'

// Revalidate every 600 seconds
export const revalidate = 600

// Generate static pages at build time
export async function generateStaticParams() {
  const payload = await getPayload({ config: configPromise })
  const posts = await payload.find({ collection: 'posts', limit: 1000 })
  return posts.docs.map((post) => ({ slug: post.slug }))
}
```

## Redirect pattern

```ts
// src/utilities/getMeUser.ts
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export async function getMeUser(args: {
  nullUserRedirect?: string
  validUserRedirect?: string
}) {
  const cookieStore = await cookies()
  const token = cookieStore.get('payload-token')?.value

  const meUserReq = await fetch(...)
  const { user } = await meUserReq.json()

  if (args.validUserRedirect && user) redirect(args.validUserRedirect)
  if (args.nullUserRedirect && !user) redirect(args.nullUserRedirect)

  return { user, token }
}
```

## unstable_cache best practices

```ts
// Always provide:
// 1. Cache key array (unique per data)
// 2. Tags for targeted revalidation

const getCached = unstable_cache(
  async () => fetchData(),
  ['cache-key-1', 'cache-key-2'],
  {
    tags: ['collection-tag'],
    revalidate: 3600, // optional: time-based fallback
  }
)

// Invalidate specifically
revalidateTag('collection-tag')    // all caches with this tag
revalidatePath('/posts/my-post')   // specific route
```

## Image optimization

```tsx
import Image from 'next/image'

// Media from Payload CMS with resize variants
<Image
  src={media.sizes?.medium?.url || media.url}
  alt={media.alt || ''}
  width={media.sizes?.medium?.width || media.width}
  height={media.sizes?.medium?.height || media.height}
  priority={isAboveFold}
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
/>
```

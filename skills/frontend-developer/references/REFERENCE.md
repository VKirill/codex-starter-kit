# Next.js App Router Reference

> Source: Context7 — /vercel/next.js (Next.js official documentation)
> Updated: 2026-03-11

## Data Fetching Patterns

### Static, Dynamic, and Revalidated Data

In the App Router, the `fetch` API controls caching behavior directly.

```tsx
export default async function Page() {
  // Static data — cached until manually invalidated (like getStaticProps)
  // `force-cache` is the default and can be omitted
  const staticData = await fetch(`https://...`, { cache: 'force-cache' })

  // Dynamic data — refetched on every request (like getServerSideProps)
  const dynamicData = await fetch(`https://...`, { cache: 'no-store' })

  // Revalidated data — cached with a lifetime of 10 seconds (like ISR)
  const revalidatedData = await fetch(`https://...`, {
    next: { revalidate: 10 },
  })

  return <div>...</div>
}
```

## Caching — Mixed Rendering Strategies

Comprehensive example combining static content, cached dynamic content, and streaming dynamic content with cache tags and server actions.

```tsx
import { Suspense } from 'react'
import { cookies } from 'next/headers'
import { cacheLife, cacheTag, updateTag } from 'next/cache'
import Link from 'next/link'

export default function BlogPage() {
  return (
    <>
      {/* Static content - prerendered automatically */}
      <header>
        <h1>Our Blog</h1>
        <nav>
          <Link href="/">Home</Link> | <Link href="/about">About</Link>
        </nav>
      </header>

      {/* Cached dynamic content - included in the static shell */}
      <BlogPosts />

      {/* Runtime dynamic content - streams at request time */}
      <Suspense fallback={<p>Loading your preferences...</p>}>
        <UserPreferences />
      </Suspense>

      {/* Mutation - server action that revalidates the cache */}
      <Suspense fallback={<p>Loading...</p>}>
        <CreatePost />
      </Suspense>
    </>
  )
}

// Everyone sees the same blog posts (revalidated every hour)
async function BlogPosts() {
  'use cache'
  cacheLife('hours')
  cacheTag('posts')

  const res = await fetch('https://api.vercel.app/blog')
  const posts = await res.json()

  return (
    <section>
      <h2>Latest Posts</h2>
      <ul>
        {posts.slice(0, 5).map((post: any) => (
          <li key={post.id}>
            <h3>{post.title}</h3>
            <p>By {post.author} on {post.date}</p>
          </li>
        ))}
      </ul>
    </section>
  )
}

// Personalized per user based on their cookie
async function UserPreferences() {
  const theme = (await cookies()).get('theme')?.value || 'light'
  const favoriteCategory = (await cookies()).get('category')?.value

  return (
    <aside>
      <p>Your theme: {theme}</p>
      {favoriteCategory && <p>Favorite category: {favoriteCategory}</p>}
    </aside>
  )
}

// Admin-only form that creates a post and revalidates the cache
async function CreatePost() {
  const isAdmin = (await cookies()).get('role')?.value === 'admin'
  if (!isAdmin) return null

  async function createPost(formData: FormData) {
    'use server'
    await db.post.create({ data: { title: formData.get('title') } })
    updateTag('posts')
  }

  return (
    <form action={createPost}>
      <input name="title" placeholder="Post title" required />
      <button type="submit">Publish</button>
    </form>
  )
}
```

### Cache Directives Summary

| Directive | Description |
|-----------|-------------|
| `'use cache'` | Mark a function/component as cacheable |
| `cacheLife('hours')` | Set cache lifetime (seconds, minutes, hours, days, weeks, max) |
| `cacheTag('name')` | Tag cached data for targeted revalidation |
| `updateTag('name')` | Invalidate all entries with this tag |

## ISR (Incremental Static Regeneration)

ISR allows you to statically generate pages at build time and update them after deployment without rebuilding the entire site.

```typescript
interface Post {
  id: string
  title: string
  content: string
}

// Invalidate cache at most once every 60 seconds
export const revalidate = 60

export async function generateStaticParams() {
  const posts: Post[] = await fetch('https://api.vercel.app/blog').then((res) =>
    res.json()
  )
  return posts.map((post) => ({
    id: String(post.id),
  }))
}

export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const post: Post = await fetch(`https://api.vercel.app/blog/${id}`).then(
    (res) => res.json()
  )
  return (
    <main>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </main>
  )
}
```

### Key ISR Concepts

- `export const revalidate = N` — time-based revalidation in seconds
- `generateStaticParams()` — define which dynamic routes to pre-render at build time
- `dynamicParams = true` (default) — on-demand generate pages for new params
- `dynamicParams = false` — return 404 for unknown params

## Server Actions

Server Actions allow server-side logic to be invoked directly from the client-side UI without creating API routes.

```tsx
// In a Server Component
async function createPost(formData: FormData) {
  'use server'
  await db.post.create({ data: { title: formData.get('title') } })
  updateTag('posts')  // revalidate cache
}

// Usage in form
<form action={createPost}>
  <input name="title" required />
  <button type="submit">Create</button>
</form>
```

### Server Actions in Client Components

```tsx
'use client'
import { useActionState } from 'react'

function ContactForm() {
  const [state, formAction, isPending] = useActionState(submitForm, null)

  return (
    <form action={formAction}>
      <input name="email" type="email" required />
      <button disabled={isPending}>
        {isPending ? 'Sending...' : 'Submit'}
      </button>
      {state?.error && <p>{state.error}</p>}
    </form>
  )
}
```

## Dynamic Metadata

Use `generateMetadata` for dynamic SEO metadata based on route params.

```tsx
import type { Metadata, ResolvingMetadata } from 'next'

type Props = {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}

export async function generateMetadata(
  { params, searchParams }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const slug = (await params).slug
  const post = await fetch(`https://api.vercel.app/blog/${slug}`).then((res) =>
    res.json()
  )

  return {
    title: post.title,
    description: post.description,
  }
}

export default function Page({ params, searchParams }: Props) {}
```

### Static Metadata

```tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My App',
  description: 'Built with Next.js',
  openGraph: {
    title: 'My App',
    description: 'Built with Next.js',
    images: ['/og-image.png'],
  },
}
```

## Server Components vs Client Components

### Server Components (default)

- Run only on the server
- Can use `async/await` directly
- Can access databases, filesystems, server resources
- Cannot use hooks (`useState`, `useEffect`, etc.)
- Cannot use browser APIs
- Not included in client bundle

### Client Components (`'use client'`)

- Run on both server (SSR) and client
- Can use hooks and browser APIs
- Can handle user interactivity (events, state)
- Must opt-in with `'use client'` directive

### When to use what

| Feature | Server Component | Client Component |
|---------|-----------------|-----------------|
| Fetch data | Yes | Yes (but prefer server) |
| Access backend | Yes | No (use API/action) |
| Use hooks | No | Yes |
| Event handlers | No | Yes |
| Browser APIs | No | Yes |
| Reduce bundle | Yes | No |

## App Router File Conventions

| File | Purpose |
|------|---------|
| `page.tsx` | Route UI (makes route publicly accessible) |
| `layout.tsx` | Shared UI that wraps pages and nested layouts |
| `loading.tsx` | Loading UI (wraps page in Suspense) |
| `error.tsx` | Error UI (wraps page in Error Boundary) |
| `not-found.tsx` | 404 UI |
| `template.tsx` | Like layout but re-mounts on navigation |
| `default.tsx` | Fallback for parallel routes |
| `route.ts` | API endpoint (GET, POST, etc.) |
| `middleware.ts` | Runs before request matching |
| `opengraph-image.tsx` | Dynamic OG image generation |

## Middleware

Middleware runs before a request is completed. It can modify the request/response, redirect, or rewrite.

```ts
// middleware.ts (project root)
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Check auth
  const token = request.cookies.get('token')?.value

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Add headers
  const response = NextResponse.next()
  response.headers.set('x-custom-header', 'value')
  return response
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
}
```

## Parallel Routes

Parallel routes allow you to render multiple pages in the same layout simultaneously.

```
app/
  layout.tsx        # Renders both @team and @analytics
  @team/
    page.tsx
  @analytics/
    page.tsx
  page.tsx          # Main content
```

```tsx
// app/layout.tsx
export default function Layout({
  children,
  team,
  analytics,
}: {
  children: React.ReactNode
  team: React.ReactNode
  analytics: React.ReactNode
}) {
  return (
    <>
      {children}
      {team}
      {analytics}
    </>
  )
}
```

## Intercepting Routes

Intercepting routes allow you to load a route from another part of your application within the current layout (e.g., modals).

Convention: `(.)route` (same level), `(..)route` (one level up), `(..)(..)route` (two levels up), `(...)route` (root).

```
app/
  feed/
    page.tsx
    @modal/
      (..)photo/[id]/
        page.tsx      # Intercepted: shows in modal
  photo/[id]/
    page.tsx          # Direct access: full page
```

## Route Handlers (API Routes)

```ts
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const posts = await db.post.findMany()
  return NextResponse.json(posts)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const post = await db.post.create({ data: body })
  return NextResponse.json(post, { status: 201 })
}
```

### Dynamic Route Handlers

```ts
// app/api/posts/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const post = await db.post.findUnique({ where: { id } })
  if (!post) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 })
  }
  return NextResponse.json(post)
}
```

## Image Optimization

```tsx
import Image from 'next/image'

// Local image (auto width/height detection)
import profilePic from './me.png'
<Image src={profilePic} alt="Profile" placeholder="blur" />

// Remote image (must specify width/height)
<Image
  src="https://example.com/photo.jpg"
  alt="Photo"
  width={500}
  height={300}
  priority          // Preload (for above-the-fold images)
/>

// Fill container
<div style={{ position: 'relative', width: '100%', height: 300 }}>
  <Image
    src="/hero.jpg"
    alt="Hero"
    fill
    style={{ objectFit: 'cover' }}
    sizes="(max-width: 768px) 100vw, 50vw"
  />
</div>
```

### Remote Image Configuration

```js
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
        pathname: '/images/**',
      },
    ],
  },
}
```

## Dynamic Routes

```
app/
  blog/
    [slug]/
      page.tsx        # /blog/hello-world
    [...slug]/
      page.tsx        # /blog/a/b/c (catch-all)
    [[...slug]]/
      page.tsx        # /blog OR /blog/a/b/c (optional catch-all)
```

```tsx
// app/blog/[slug]/page.tsx
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  return <h1>{slug}</h1>
}
```

## Route Groups

Organize routes without affecting URL structure.

```
app/
  (marketing)/
    about/page.tsx      # /about
    contact/page.tsx    # /contact
    layout.tsx          # Shared marketing layout
  (shop)/
    products/page.tsx   # /products
    cart/page.tsx        # /cart
    layout.tsx          # Shared shop layout
```

## Streaming with Suspense

```tsx
import { Suspense } from 'react'

export default function Page() {
  return (
    <section>
      <h1>Dashboard</h1>
      <Suspense fallback={<p>Loading revenue...</p>}>
        <RevenueChart />
      </Suspense>
      <Suspense fallback={<p>Loading invoices...</p>}>
        <LatestInvoices />
      </Suspense>
    </section>
  )
}
```

Or use the `loading.tsx` convention for automatic route-level streaming.

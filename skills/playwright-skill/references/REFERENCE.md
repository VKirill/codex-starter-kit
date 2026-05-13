# Playwright 1.56 — Project-Specific Reference

> Source: Playwright docs + project analysis | Project: DesignHub | Generated: 2026-03-21

## Current project setup

DesignHub uses Playwright 1.56.1 for e2e tests. Config: `playwright.config.ts`,
tests dir: `tests/e2e/`, single project (Chromium), webServer auto-starts `pnpm dev`.

```ts
// playwright.config.ts (current)
import { defineConfig, devices } from '@playwright/test'
import 'dotenv/config'

export default defineConfig({
  testDir: './tests/e2e',
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], channel: 'chromium' },
    },
  ],
  webServer: {
    command: 'pnpm dev',
    reuseExistingServer: true,
    url: 'http://localhost:3000',
  },
})
```

**Issue**: `webServer.url` is `localhost:3000` but project runs on port **3010**.
Fix: change to `http://localhost:3010` or use `process.env.PORT || 3010`.

## Recommended config improvements

```ts
import { defineConfig, devices } from '@playwright/test'
import 'dotenv/config'

const PORT = process.env.PORT || '3010'
const BASE_URL = `http://localhost:${PORT}`

export default defineConfig({
  testDir: './tests/e2e',
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI ? 'github' : 'html',
  timeout: 30_000,
  expect: { timeout: 10_000 },
  use: {
    baseURL: BASE_URL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'mobile',
      use: { ...devices['iPhone 14'] },
    },
  ],
  webServer: {
    command: 'pnpm dev',
    url: BASE_URL,
    reuseExistingServer: !process.env.CI,
    timeout: 120_000, // Next.js + Payload startup is slow
  },
})
```

## Test patterns for DesignHub

### Homepage test

```ts
import { test, expect } from '@playwright/test'

test.describe('Homepage', () => {
  test('renders homepage with header and footer', async ({ page }) => {
    await page.goto('/')

    await expect(page).toHaveTitle(/DesignHub/)

    const header = page.locator('header')
    await expect(header).toBeVisible()

    const footer = page.locator('footer')
    await expect(footer).toBeVisible()
  })

  test('homepage has valid meta tags', async ({ page }) => {
    await page.goto('/')

    const description = page.locator('meta[name="description"]')
    await expect(description).toHaveAttribute('content', /.+/)

    const ogImage = page.locator('meta[property="og:image"]')
    await expect(ogImage).toHaveAttribute('content', /.+/)
  })
})
```

### Blog posts navigation

```ts
test.describe('Blog', () => {
  test('blog listing page loads', async ({ page }) => {
    await page.goto('/posts')

    await expect(page).toHaveTitle(/DesignHub/)

    const postCards = page.locator('article, [data-post-card]')
    await expect(postCards.first()).toBeVisible()
  })

  test('can navigate to individual post', async ({ page }) => {
    await page.goto('/posts')

    const firstPostLink = page.locator('a[href^="/posts/"]').first()
    await expect(firstPostLink).toBeVisible()

    const href = await firstPostLink.getAttribute('href')
    await firstPostLink.click()

    await page.waitForURL(`**${href}`)

    const heading = page.locator('h1')
    await expect(heading).toBeVisible()
  })
})
```

### Dynamic CMS pages

```ts
test.describe('CMS Pages', () => {
  test('slug-based page renders blocks', async ({ page }) => {
    const response = await page.goto('/about')

    expect(response?.status()).toBeLessThan(400)

    const blocks = page.locator('[class*="block"], section')
    await expect(blocks.first()).toBeVisible()
  })
})
```

### Telegram auth flow (mocked)

```ts
test.describe('Authentication', () => {
  test('authenticated user sees profile', async ({ page, context }) => {
    await context.addCookies([{
      name: 'payload-token',
      value: 'test-jwt-token',
      domain: 'localhost',
      path: '/',
    }])

    await page.goto('/')
    // Verify authenticated state
  })
})
```

### Search functionality

```ts
test.describe('Search', () => {
  test('search API returns results', async ({ request }) => {
    const response = await request.get('/api/search?q=test')

    expect(response.ok()).toBeTruthy()
    const data = await response.json()
    expect(data).toHaveProperty('results')
  })

  test('search with Russian morphology', async ({ request }) => {
    const response = await request.get('/api/search?q=%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD')

    expect(response.ok()).toBeTruthy()
    const data = await response.json()
    expect(Array.isArray(data.results)).toBeTruthy()
  })
})
```

### API route testing

```ts
test.describe('API Routes', () => {
  test('parser stats endpoint', async ({ request }) => {
    const response = await request.get('/api/parsing/stats')
    expect(response.ok()).toBeTruthy()
  })

  test('auth endpoint rejects invalid data', async ({ request }) => {
    const response = await request.post('/api/auth/telegram', {
      data: { id: 123 },
    })
    expect(response.status()).toBe(400)
  })

  test('protected endpoint requires auth', async ({ request }) => {
    const response = await request.get('/api/user/status')
    expect(response.status()).toBe(401)
  })
})
```

## Playwright API patterns

### Locator strategies (best to worst)

```ts
// ✅ Best: role-based (accessible)
page.getByRole('button', { name: 'Submit' })
page.getByRole('heading', { name: /DesignHub/ })
page.getByRole('link', { name: 'Blog' })

// ✅ Good: text-based
page.getByText('Read more')
page.getByLabel('Email')
page.getByPlaceholder('Search...')

// ✅ Good: test IDs
page.getByTestId('parser-status')

// ⚠️ Acceptable: CSS selectors
page.locator('header nav a')
page.locator('[data-post-card]')

// ❌ Avoid: fragile selectors
page.locator('.css-1a2b3c')
page.locator('div > div > span')
```

### Waiting strategies

```ts
// Wait for navigation
await page.waitForURL('**/posts/**')

// Wait for network idle (after heavy loading)
await page.waitForLoadState('networkidle')

// Wait for specific response
const responsePromise = page.waitForResponse('**/api/search**')
await page.getByRole('button', { name: 'Search' }).click()
const response = await responsePromise

// ❌ Avoid fixed timeouts
await page.waitForTimeout(3000)
```

### Network interception (for Payload CMS/API mocking)

```ts
// Mock API response
await page.route('**/api/search**', async (route) => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      results: [{ title: 'Test Post', slug: 'test-post' }],
      totalDocs: 1,
    }),
  })
})

// Block external requests in tests
await page.route('https://api.telegram.org/**', (route) => route.abort())
```

### Screenshots and visual testing

```ts
await page.goto('/')
await expect(page).toHaveScreenshot('homepage.png', {
  fullPage: true,
  maxDiffPixelRatio: 0.05,
})

const hero = page.locator('[class*="hero"], .hero')
await expect(hero).toHaveScreenshot('hero-section.png')
```

## Test organization for DesignHub

```
tests/e2e/
├── frontend.e2e.spec.ts      # Public pages (homepage, posts, CMS pages)
├── search.e2e.spec.ts         # Search functionality
├── auth.e2e.spec.ts           # Telegram auth flow
├── admin.e2e.spec.ts          # Payload CMS admin panel
├── api.e2e.spec.ts            # API route handlers
├── seo.e2e.spec.ts            # Meta tags, sitemaps, OG images
└── parser.e2e.spec.ts         # Parser dashboard UI
```

## Running tests

```bash
# All e2e tests
pnpm test:e2e

# Specific test file
pnpm exec playwright test tests/e2e/frontend.e2e.spec.ts

# Headed mode (see browser)
pnpm exec playwright test --headed

# Debug mode (step through)
pnpm exec playwright test --debug

# UI mode (interactive)
pnpm exec playwright test --ui

# Generate report
pnpm exec playwright show-report
```

## Fixtures for DesignHub

```ts
// tests/e2e/fixtures.ts
import { test as base, Page } from '@playwright/test'

type DesignHubFixtures = {
  authenticatedPage: Page
}

export const test = base.extend<DesignHubFixtures>({
  authenticatedPage: async ({ browser }, use) => {
    const context = await browser.newContext()
    await context.addCookies([{
      name: 'payload-token',
      value: process.env.TEST_AUTH_TOKEN || 'test-token',
      domain: 'localhost',
      path: '/',
    }])
    const page = await context.newPage()
    await use(page)
    await context.close()
  },
})

export { expect } from '@playwright/test'
```

Usage:

```ts
import { test, expect } from './fixtures'

test('admin can access parser dashboard', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/admin')
  await expect(authenticatedPage).toHaveURL(/\/admin/)
})
```

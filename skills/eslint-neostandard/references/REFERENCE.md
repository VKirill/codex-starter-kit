# ESLint 9 + Next.js — Project-Specific Reference

> Source: ESLint docs + project analysis | Project: DesignHub | Generated: 2026-03-21

## Current project setup

DesignHub uses ESLint 9 flat config with `@eslint/eslintrc` FlatCompat wrapper
to extend Next.js presets. No neostandard — uses `next/core-web-vitals` + `next/typescript`.

```js
// eslint.config.mjs (current)
import { dirname } from 'path'
import { fileURLToPath } from 'url'
import { FlatCompat } from '@eslint/eslintrc'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const compat = new FlatCompat({ baseDirectory: __dirname })

const eslintConfig = [
  ...compat.extends('next/core-web-vitals', 'next/typescript'),
  {
    rules: {
      '@typescript-eslint/ban-ts-comment': 'warn',
      '@typescript-eslint/no-empty-object-type': 'warn',
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-unused-vars': [
        'warn',
        {
          vars: 'all',
          args: 'after-used',
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
          destructuredArrayIgnorePattern: '^_',
          caughtErrorsIgnorePattern: '^(_|ignore)',
        },
      ],
    },
  },
  { ignores: ['.next/'] },
]

export default eslintConfig
```

## ESLint 9 flat config — key concepts

### Config array merge semantics

```js
// Each object in the array is a config layer.
// Later layers override earlier ones for matching files.
export default [
  baseConfig,        // foundation
  typescriptConfig,  // TS overrides
  { ignores: [...] } // global ignores (standalone object = applies to all)
]
```

### FlatCompat — bridging legacy extends

`eslint-config-next` still uses legacy format. FlatCompat wraps it:

```js
import { FlatCompat } from '@eslint/eslintrc'

const compat = new FlatCompat({ baseDirectory: __dirname })

// converts legacy "extends" to flat config objects
...compat.extends('next/core-web-vitals', 'next/typescript')
```

When `eslint-config-next` migrates to flat config natively, FlatCompat can be removed.

### Global ignores vs file-scoped ignores

```js
// GLOBAL ignores — standalone object with only `ignores` key
{ ignores: ['.next/', 'node_modules/', 'cms/'] }

// FILE-SCOPED ignores — ignores inside a config with other keys
{
  files: ['**/*.ts'],
  ignores: ['**/*.test.ts'],  // only affects this config object
  rules: { ... }
}
```

## Adding rules for DesignHub patterns

### Payload CMS collection files

```js
// Override for Payload collection configs (allow default exports)
{
  files: ['src/collections/**/*.ts'],
  rules: {
    '@typescript-eslint/explicit-function-return-type': 'off',
  },
}
```

### Route handlers (`src/app/api/`)

```js
{
  files: ['src/app/api/**/route.ts'],
  rules: {
    'import/prefer-default-export': 'off',
  },
}
```

### Parser module isolation

```js
// Enforce parser module isolation — no imports from app/ or components/
{
  files: ['src/lib/parser/**/*.ts'],
  rules: {
    'no-restricted-imports': ['error', {
      patterns: [
        { group: ['@/app/*', '@/components/*'], message: 'Parser module must be isolated from app layer' },
      ],
    }],
  },
}
```

## Adding new plugins (flat config style)

```js
// ESLint 9: plugins are imported directly, not string references
import importPlugin from 'eslint-plugin-import'

export default [
  ...compat.extends('next/core-web-vitals', 'next/typescript'),
  {
    plugins: {
      import: importPlugin,
    },
    rules: {
      'import/order': ['warn', {
        groups: ['builtin', 'external', 'internal', 'parent', 'sibling'],
        'newlines-between': 'always',
      }],
    },
  },
]
```

## TypeScript strict rules

```js
// Type-checked rules require parserOptions.project
{
  files: ['**/*.ts', '**/*.tsx'],
  languageOptions: {
    parserOptions: {
      project: './tsconfig.json',
    },
  },
  rules: {
    '@typescript-eslint/no-floating-promises': 'error',
    '@typescript-eslint/no-misused-promises': 'error',
    '@typescript-eslint/await-thenable': 'error',
    '@typescript-eslint/require-await': 'warn',
  },
}
```

**Warning**: type-checked rules significantly slow down linting. Use selectively.

## Prettier coexistence

DesignHub uses Prettier 3.4 alongside ESLint. To avoid conflicts:

```js
import prettierConfig from 'eslint-config-prettier'

export default [
  ...compat.extends('next/core-web-vitals', 'next/typescript'),
  { rules: { /* project rules */ } },
  prettierConfig, // MUST be last — disables conflicting rules
]
```

## CI integration

```bash
# CI: strict mode
pnpm lint
# = cross-env NODE_OPTIONS=--no-deprecation next lint

# Direct eslint call with strict flags
npx eslint . --max-warnings 0

# Local: auto-fix
npx eslint . --fix
```

## Common flat config mistakes

```js
// ❌ WRONG: `env` is legacy
{ env: { browser: true, node: true } }

// ✅ RIGHT: use languageOptions.globals
import globals from 'globals'
{ languageOptions: { globals: { ...globals.browser, ...globals.node } } }

// ❌ WRONG: extends as string (legacy)
{ extends: ['next/core-web-vitals'] }

// ✅ RIGHT: use FlatCompat or spread configs
...compat.extends('next/core-web-vitals')

// ❌ WRONG: parser as string
{ parser: '@typescript-eslint/parser' }

// ✅ RIGHT: import parser module
import tsParser from '@typescript-eslint/parser'
{ languageOptions: { parser: tsParser } }
```

## Migrating away from FlatCompat (future)

When `eslint-config-next` supports flat config natively:

```js
import nextConfig from 'eslint-config-next'

export default [
  ...nextConfig,
  {
    rules: {
      '@typescript-eslint/no-explicit-any': 'warn',
    },
  },
  { ignores: ['.next/'] },
]
```

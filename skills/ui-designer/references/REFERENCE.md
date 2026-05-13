# Tailwind CSS 4 + shadcn/ui — Project-Specific Reference

> Source: Tailwind CSS 4 / shadcn/ui docs + project analysis | Project: Vechkasov Pro CRM | Generated: 2026-03-16

## Tailwind CSS 4 конфигурация в проекте

### CSS-first config (globals.css)

```css
/* apps/crm/src/app/globals.css — полная структура */
@import "tailwindcss";
@import "tw-animate-css";
@import "shadcn/tailwind.css";
@plugin "@tailwindcss/typography";

@custom-variant dark (&:is(.dark *));

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --font-sans: var(--font-geist-sans);
  --font-mono: var(--font-geist-mono);
  /* ... sidebar, chart, radius tokens ... */
}
```

**Ключевое отличие Tailwind 4**: конфиг через CSS, не `tailwind.config.ts`.
- `@import "tailwindcss"` — вместо `@tailwind base/components/utilities`
- `@theme inline` — определение design tokens в CSS
- `@plugin` — вместо `plugins: []` в JS
- `@custom-variant` — вместо `darkMode: ['class']`

### Тема проекта — "Parchment" (тёплый off-white)

```css
:root {
  --radius: 0.5rem;

  /* Фон — тёплый пергаментный */
  --background: oklch(0.965 0.008 75);
  --foreground: oklch(0.22 0.02 55);

  /* Primary — терракота */
  --primary: oklch(0.55 0.11 40);
  --primary-foreground: oklch(0.97 0.005 75);

  /* Secondary — тёплый камень */
  --secondary: oklch(0.91 0.018 72);

  /* Custom semantic tokens */
  --sand: oklch(0.91 0.02 72);
  --sand-dark: oklch(0.82 0.03 68);
  --terracotta: oklch(0.55 0.11 40);
  --terracotta-light: oklch(0.88 0.04 45);
  --ink: oklch(0.22 0.02 55);
  --ink-light: oklch(0.48 0.02 55);
  --warm-success: oklch(0.58 0.12 148);
  --warm-warning: oklch(0.72 0.14 68);
}
```

**oklch** — Tailwind 4 default color space. Лучшая перцептивная линейность чем hsl.

### Использование custom tokens в Tailwind

```tsx
// Custom tokens доступны через var() в className
<div className="bg-sand text-ink border-terracotta" />
<div className="bg-terracotta-light text-ink-light" />
<div className="text-warm-success" />   {/* semantic green */}
<div className="text-warm-warning" />   {/* semantic amber */}

// Standard shadcn tokens
<div className="bg-card text-card-foreground border-border" />
<div className="bg-muted text-muted-foreground" />
<div className="bg-primary text-primary-foreground" />
```

## shadcn/ui компоненты в проекте

### Импорты — ТОЛЬКО через @/ alias

```tsx
// ✅ Correct — project convention
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog";
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from "@/components/ui/select";

// ❌ Wrong — no relative imports in CRM
import { Button } from "../../components/ui/button";
```

### cn() utility

```tsx
// apps/crm/src/lib/utils.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Usage pattern:
```tsx
import { cn } from "@/lib/utils";

<div className={cn(
  "rounded-lg border p-4",
  isActive && "border-primary bg-primary/5",
  isDisabled && "opacity-50 pointer-events-none",
  className, // allow className override from props
)} />
```

### Radix UI primitives (Tailwind 4 style)

```tsx
// shadcn/ui в Tailwind 4 использует "radix-ui" package напрямую
import { Switch as SwitchPrimitive } from "radix-ui";
import { Dialog as DialogPrimitive, VisuallyHidden } from "radix-ui";
import { Popover as PopoverPrimitive } from "radix-ui";
import { Select as SelectPrimitive } from "radix-ui";
import { Tabs as TabsPrimitive } from "radix-ui";

// Radix data attributes для анимаций
"data-[state=open]:animate-in data-[state=closed]:animate-out"
"data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0"
"data-[side=bottom]:slide-in-from-top-2"
```

### lucide-react иконки

```tsx
import { Brain, Plus, Send, Loader2, MessageSquare, X, GitFork } from "lucide-react";
import { CheckCircle2, Circle, FileCode, XCircle } from "lucide-react";
import { ChevronLeft, ChevronRight, Clock } from "lucide-react";
import type { LucideIcon } from "lucide-react";

// Icon button pattern
<Button variant="ghost" size="icon">
  <Plus className="h-4 w-4" />
</Button>

// Loading state
<Button disabled>
  <Loader2 className="h-4 w-4 animate-spin mr-2" />
  Processing...
</Button>

// Typed icon component
interface NavItem {
  title: string;
  icon: LucideIcon;
  href: string;
}
```

## Server Components vs Client Components

### По умолчанию — Server Component

```tsx
// app/(dashboard)/page.tsx — NO "use client" directive
import { Card } from "@/components/ui/card";
import { auth } from "@/lib/auth";

export default async function DashboardPage() {
  const session = await auth(); // server-side auth
  const data = await prisma.lead.findMany(); // direct DB access
  return <Card>...</Card>;
}
```

### "use client" — только когда нужна интерактивность

```tsx
"use client";

import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";

export function LeadDialog({ leadId }: { leadId: string }) {
  const [open, setOpen] = useState(false);
  // ... interactive logic
}
```

**Триггеры для "use client"**:
- `useState`, `useEffect`, `useCallback`, `useRef`
- Event handlers: `onClick`, `onChange`, `onSubmit`
- Browser APIs: `window`, `document`, `localStorage`
- Custom hooks: `usePipelineSSE`, `useVoiceRecorder`

## Типовые CRM компоненты

### Dialog + Form pattern

```tsx
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog";
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from "@/components/ui/select";

export function CreateEntityDialog() {
  const [open, setOpen] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    await fetch("/api/entity", {
      method: "POST",
      body: JSON.stringify(Object.fromEntries(formData)),
      headers: { "Content-Type": "application/json" },
    });
    setOpen(false);
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button><Plus className="h-4 w-4 mr-2" />Create</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>New Entity</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input id="name" name="name" required />
          </div>
          <div className="space-y-2">
            <Label>Status</Label>
            <Select name="status" defaultValue="active">
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="archived">Archived</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Button type="submit" className="w-full">Save</Button>
        </form>
      </DialogContent>
    </Dialog>
  );
}
```

### Card с метриками (Pipeline stats pattern)

```tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle2, XCircle, Clock, Zap } from "lucide-react";

interface StatCardProps {
  title: string;
  value: number | string;
  icon: LucideIcon;
  trend?: string;
  className?: string;
}

function StatCard({ title, value, icon: Icon, trend, className }: StatCardProps) {
  return (
    <Card className={cn("", className)}>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {trend && <p className="text-xs text-muted-foreground mt-1">{trend}</p>}
      </CardContent>
    </Card>
  );
}

// Usage
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
  <StatCard title="Completed" value={stats.completed} icon={CheckCircle2} />
  <StatCard title="Failed" value={stats.failed} icon={XCircle} />
  <StatCard title="In Progress" value={stats.inProgress} icon={Zap} />
  <StatCard title="Queued" value={stats.queued} icon={Clock} />
</div>
```

## Tailwind CSS 4 — новые возможности

### @theme vs @theme inline

```css
/* @theme — generates CSS custom properties AND Tailwind utilities */
@theme {
  --color-brand: oklch(0.55 0.11 40);
}
/* → можно использовать: bg-brand, text-brand, border-brand */

/* @theme inline — НЕ генерирует utilities, только CSS vars */
@theme inline {
  --color-background: var(--background);
}
/* → используется для маппинга на существующие CSS vars (shadcn pattern) */
```

### Добавление нового цвета в проект

```css
/* В globals.css — добавь CSS variable */
:root {
  --success-green: oklch(0.58 0.12 148);  /* warm green, matches project palette */
}

/* В @theme inline — замапь на Tailwind */
@theme inline {
  --color-success-green: var(--success-green);
}
```

```tsx
{/* Now available as Tailwind class */}
<Badge className="bg-success-green text-white">Deployed</Badge>
```

### Responsive + dark mode

```tsx
{/* Tailwind 4 responsive syntax — unchanged */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4" />

{/* Dark mode via custom variant from project */}
{/* @custom-variant dark (&:is(.dark *)); */}
<div className="bg-card dark:bg-zinc-900 text-card-foreground dark:text-zinc-100" />
```

## Добавление shadcn/ui компонентов

```bash
# ONLY через CLI — никогда не копировать файлы вручную
cd apps/crm && npx shadcn@latest add <component>

# Примеры:
npx shadcn@latest add table
npx shadcn@latest add toast
npx shadcn@latest add command
npx shadcn@latest add sheet
```

**ВАЖНО** (из CLAUDE.md): `shadcn/ui: только npx shadcn@latest add <component>, не ручное копирование`.

## Анти-паттерны

| Анти-паттерн | Правильно |
|---|---|
| `import from "../components/ui/"` | `import from "@/components/ui/"` |
| `tailwind.config.ts` в Tailwind 4 | `globals.css` с `@theme` |
| `hsl()` цвета | `oklch()` (Tailwind 4 default) |
| `"use client"` на всех компонентах | Server Component по умолчанию |
| Ручное копирование shadcn файлов | `npx shadcn@latest add` |
| `lib/` импортирует `components/` | `lib/` — чистая бизнес-логика |
| `@apply` повсюду | Utility classes в JSX |

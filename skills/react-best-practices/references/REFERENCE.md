# React + Next.js Performance — Project-Specific Reference

> Source: context7 docs (next.js v16.1.6, react.dev) | Project: vechkasov-pro | Generated: 2026-03-03

## Eliminating Waterfalls in API Routes

Project's API routes often make multiple independent DB calls.

```typescript
// ─── BAD: Sequential queries (waterfall) ──────────────────────────
export async function GET() {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const leads = await prisma.lead.findMany();      // ~50ms
  const clients = await prisma.client.findMany();   // ~50ms
  const stats = await prisma.lead.count();           // ~20ms
  // Total: ~120ms (sequential)

  return NextResponse.json({ leads, clients, stats });
}

// ─── GOOD: Parallel with Promise.all ──────────────────────────────
export async function GET() {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const [leads, clients, stats] = await Promise.all([
    prisma.lead.findMany(),
    prisma.client.findMany(),
    prisma.lead.count(),
  ]);
  // Total: ~50ms (parallel)

  return NextResponse.json({ leads, clients, stats });
}

// ─── Start promise early, await late ──────────────────────────────
export async function POST(request: Request) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  // Start brain retrieval immediately (don't await yet)
  const brainPromise = retrieveMemory(query, embedding);

  // Parse body while brain retrieval runs
  const { message, conversationId } = await request.json();
  const validated = validateInput(message);

  // Now await the brain results
  const brainEntries = await brainPromise;
  // ...
}
```

## Server vs Client Component Split

Push "use client" down to minimize client JS bundle.

```typescript
// ─── Server page: data fetching, no interactivity ─────────────────
// src/app/(dashboard)/leads/page.tsx
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { LeadsList } from "@/components/leads/leads-list";

export default async function LeadsPage() {
  const session = await auth();
  if (!session) redirect("/login");

  const leads = await prisma.lead.findMany({
    orderBy: { createdAt: "desc" },
    take: 100,
  });

  // Pass serializable data to client component
  return <LeadsList initialLeads={leads} />;
}

// ─── Client component: only interactive parts ────────────────────
// src/components/leads/leads-list.tsx
"use client";
import { useState } from "react";

export function LeadsList({ initialLeads }: { initialLeads: Lead[] }) {
  const [leads, setLeads] = useState(initialLeads);
  const [filter, setFilter] = useState("all");
  // ... interactive filtering, dialogs
}
```

### Component Boundary Rules for This Project

```
app/(dashboard)/page.tsx         → Server (auth + data fetch)
app/(dashboard)/layout.tsx       → Server (sidebar layout)
components/sidebar.tsx           → Server (static navigation)
components/leads/lead-dialog.tsx → Client (form with useState)
components/agent/tool-call-card.tsx → Client (expand/collapse)
components/brain/brain-entry-dialog.tsx → Client (form)
components/ui/*                  → Client (shadcn primitives)
```

## Dynamic Imports for Heavy Components

```typescript
// ─── Lazy-load heavy AI sandbox components ────────────────────────
import dynamic from "next/dynamic";

const AgentSandbox = dynamic(
  () => import("@/components/agent/sandbox"),
  {
    loading: () => <Skeleton className="h-96 w-full" />,
    ssr: false,  // browser-only component
  }
);

// ─── Lazy-load dialog on demand ───────────────────────────────────
const LeadDialog = dynamic(
  () => import("@/components/leads/lead-dialog").then(m => ({ default: m.LeadDialog })),
);

// Render only when open
{showDialog && <LeadDialog lead={selectedLead} onClose={() => setShowDialog(false)} />}
```

## API Route Auth Pattern

Project uses consistent auth check at the top of every API route.

```typescript
import { NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";

// ─── Standard API route pattern ───────────────────────────────────
export async function GET() {
  // 1. Auth guard (first line)
  const session = await auth();
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    // 2. Business logic
    const data = await prisma.lead.findMany({
      orderBy: { createdAt: "desc" },
    });

    // 3. Success response
    return NextResponse.json(data);
  } catch (error) {
    // 4. Error response
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}

export async function POST(request: Request) {
  const session = await auth();
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const body = await request.json();

    // Validate required fields
    if (!body.name) {
      return NextResponse.json(
        { error: "Name is required" },
        { status: 400 }
      );
    }

    const result = await prisma.lead.create({ data: body });
    return NextResponse.json(result);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
```

## Suspense Boundaries for Streaming

```typescript
import { Suspense } from "react";

// ─── Page with multiple async sections ────────────────────────────
export default function DashboardPage() {
  return (
    <div className="grid grid-cols-2 gap-6">
      <Suspense fallback={<StatsSkeleton />}>
        <StatsPanel />      {/* async server component */}
      </Suspense>
      <Suspense fallback={<LeadsSkeleton />}>
        <RecentLeads />     {/* async server component */}
      </Suspense>
      <Suspense fallback={<ActivitySkeleton />}>
        <ActivityFeed />    {/* async server component */}
      </Suspense>
    </div>
  );
}

// Each section streams independently — fast ones render first
async function StatsPanel() {
  const stats = await prisma.lead.count();
  return <Card><CardContent>{stats} лидов</CardContent></Card>;
}
```

## Bundle Optimization

```typescript
// ─── Direct imports, not barrel files ─────────────────────────────
// BAD: import { Button, Card, Dialog } from "@/components/ui";
// GOOD: import each from its own file
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

// ─── Lucide icons: import only what you need ──────────────────────
// BAD: import * as Icons from "lucide-react";
// GOOD:
import { Search, Plus, Trash2 } from "lucide-react";

// ─── Defer third-party scripts ────────────────────────────────────
// Analytics, tracking — load after hydration
import Script from "next/script";

<Script
  src="https://analytics.example.com/script.js"
  strategy="afterInteractive"
/>
```

## Re-render Optimization

```typescript
"use client";

import { useState, useMemo, useCallback } from "react";

function LeadsList({ leads }: { leads: Lead[] }) {
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");

  // ─── useMemo for expensive computations ─────────────────────────
  const filteredLeads = useMemo(() => {
    return leads
      .filter(l => filter === "all" || l.status === filter)
      .filter(l => l.name.toLowerCase().includes(search.toLowerCase()));
  }, [leads, filter, search]);

  // ─── useCallback for stable handler refs ────────────────────────
  const handleDelete = useCallback(async (id: string) => {
    await fetch(`/api/leads/${id}`, { method: "DELETE" });
  }, []);

  return (
    <>
      <SearchInput value={search} onChange={setSearch} />
      <FilterTabs value={filter} onChange={setFilter} />
      {filteredLeads.map(lead => (
        <LeadCard key={lead.id} lead={lead} onDelete={handleDelete} />
      ))}
    </>
  );
}
```

## Fire-and-Forget in API Routes

```typescript
// Non-blocking writes for analytics/logging
export async function POST(request: Request) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const { message } = await request.json();

  // Critical: must await
  const response = await runAgent(message);

  // Non-critical: fire-and-forget
  prisma.agentReflection.create({
    data: { conversationId, score: response.score },
  }).catch(() => {});  // don't block the response

  // Log implicit signals in background
  detectImplicitSignals(message, response).catch(() => {});

  return NextResponse.json(response);
}
```

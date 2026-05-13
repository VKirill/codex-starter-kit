# Autonomous Agent Patterns — Project-Specific Reference

<!-- Generated from model knowledge, verify against official docs -->

> Project: ai-pipeline (@anthropic-ai/claude-agent-sdk) | Generated: 2026-03-10

## Anthropic Claude Agent SDK — Основной паттерн

Ядро проекта: `src/agent/runner.ts`

```typescript
import Anthropic from '@anthropic-ai/sdk';

// Базовый вызов с tool use
const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

const response = await client.messages.create({
  model: 'claude-opus-4-5',        // Orchestrator
  // model: 'claude-sonnet-4-5',   // Sub-agents (coder, reviewer)
  max_tokens: 8096,
  tools: toolDefinitions,
  tool_choice: { type: 'auto' },
  messages: conversationHistory,
  system: systemPrompt,
});

// Обработка ответа
if (response.stop_reason === 'tool_use') {
  const toolUses = response.content.filter(b => b.type === 'tool_use');
  // Выполнить инструменты, добавить результаты в историю
}
```

## Agent Loop — Паттерн оркестратора

```typescript
// src/agent/runner.ts — упрощённая версия
export async function runAgentLoop(
  task: PipelineTask,
  tools: Tool[],
  systemPrompt: string,
): Promise<AgentResult> {
  const history: Anthropic.Messages.MessageParam[] = [
    { role: 'user', content: buildInitialPrompt(task) },
  ];

  for (let iteration = 0; iteration < MAX_ITERATIONS; iteration++) {
    const response = await client.messages.create({
      model: selectModel(task),
      max_tokens: 8096,
      tools,
      system: systemPrompt,
      messages: history,
    });

    // Добавить ответ ассистента в историю
    history.push({ role: 'assistant', content: response.content });

    if (response.stop_reason === 'end_turn') {
      return { success: true, output: extractText(response.content) };
    }

    if (response.stop_reason === 'tool_use') {
      const toolResults = await executeToolCalls(response.content, task);

      history.push({
        role: 'user',
        content: toolResults.map(r => ({
          type: 'tool_result' as const,
          tool_use_id: r.toolUseId,
          content: r.result,
          is_error: r.isError,
        })),
      });
      continue;
    }

    break;
  }

  return { success: false, error: 'Max iterations reached' };
}
```

## MCP Tool Definition — Формат для этого проекта

```typescript
// src/agent/definitions.ts
import type Anthropic from '@anthropic-ai/sdk';

export const mcpToolDefinitions: Anthropic.Tool[] = [
  {
    name: 'run_step',
    description: 'Run a pipeline step with enriched context',
    input_schema: {
      type: 'object' as const,
      properties: {
        step: {
          type: 'string',
          enum: ['plan', 'code', 'review', 'debug'],
          description: 'Pipeline step to execute',
        },
        task_id: {
          type: 'string',
          description: 'Task ID to operate on',
        },
        context: {
          type: 'object',
          description: 'Additional context for the step',
        },
      },
      required: ['step', 'task_id'],
    },
  },
  {
    name: 'get_task_context',
    description: 'Retrieve full task context including comments, events, git diff',
    input_schema: {
      type: 'object' as const,
      properties: {
        task_id: { type: 'string' },
        include: {
          type: 'array',
          items: { type: 'string', enum: ['comments', 'events', 'diff', 'timeline'] },
        },
      },
      required: ['task_id'],
    },
  },
];

// Обработчик инструментов
export async function executeTool(
  toolName: string,
  toolInput: Record<string, unknown>,
  context: ExecutionContext,
): Promise<string> {
  switch (toolName) {
    case 'run_step':
      return await runStep(toolInput as RunStepInput, context);
    case 'get_task_context':
      return JSON.stringify(await getTaskContext(toolInput.task_id as string));
    default:
      return JSON.stringify({ error: `Unknown tool: ${toolName}` });
  }
}
```

## Multi-Agent Architecture — Sub-agents проекта

```typescript
// src/agent/profiles.ts — профили под-агентов
export const agentProfiles = {
  coder: {
    model: 'claude-sonnet-4-5',
    systemPrompt: `You are an expert TypeScript developer...`,
    tools: ['read_file', 'write_file', 'edit_file', 'run_command', 'search_code'],
    maxTokens: 8096,
  },
  debugger: {
    model: 'claude-sonnet-4-5',
    systemPrompt: `You are an expert debugger...`,
    tools: ['read_file', 'run_command', 'search_code', 'get_logs'],
    maxTokens: 4096,
  },
  reviewer: {
    model: 'claude-sonnet-4-5',
    systemPrompt: `You are a senior code reviewer...`,
    tools: ['read_file', 'search_code', 'get_diff'],
    maxTokens: 4096,
  },
  orchestrator: {
    model: 'claude-opus-4-5',
    systemPrompt: `You are a pipeline orchestrator...`,
    tools: mcpToolDefinitions.map(t => t.name),
    maxTokens: 8096,
  },
} as const;

// Выбор агента на основе фазы
export function resolveCoderAgent(task: PipelineTask): typeof agentProfiles[keyof typeof agentProfiles] {
  if (task.hasTestFailures) return agentProfiles.debugger;
  if (task.phase === 'review') return agentProfiles.reviewer;
  return agentProfiles.coder;
}
```

## API Key Rotation — Circuit Breaker паттерн

```typescript
// src/agent/keys.ts — ротация ключей при rate limit
export class ApiKeyRotator {
  private keys: string[];
  private currentIndex = 0;
  private failures = new Map<string, number>();

  constructor(keys: string[]) {
    this.keys = keys.filter(Boolean);
  }

  getCurrentKey(): string {
    return this.keys[this.currentIndex];
  }

  markFailure(key: string, error: Error): void {
    // При 429 / overload — переключить ключ
    if (this.isRateLimitError(error)) {
      this.failures.set(key, (this.failures.get(key) ?? 0) + 1);
      this.rotateKey();
    }
  }

  private rotateKey(): void {
    const next = (this.currentIndex + 1) % this.keys.length;
    this.currentIndex = next;
    logger.info(`Rotated to API key index ${next}`);
  }

  private isRateLimitError(err: Error): boolean {
    return err.message.includes('rate_limit') ||
           err.message.includes('overloaded') ||
           err.message.includes('529');
  }
}
```

## Session Persistence — Checkpoint паттерн

```typescript
// src/agent/runner.ts — сохранение/восстановление сессии
export interface AgentSession {
  taskId: string;
  sessionId: string;
  history: Anthropic.Messages.MessageParam[];
  phase: string;
  iteration: number;
  createdAt: Date;
  updatedAt: Date;
}

// Сохранить сессию в DB перед каждой итерацией
async function saveSession(session: AgentSession): Promise<void> {
  await db.query(
    `INSERT INTO agent_sessions (id, task_id, data, updated_at)
     VALUES ($1, $2, $3, NOW())
     ON CONFLICT (id) DO UPDATE SET data = $3, updated_at = NOW()`,
    [session.sessionId, session.taskId, JSON.stringify(session)]
  );
}

// Восстановить при рестарте
async function loadSession(taskId: string): Promise<AgentSession | null> {
  const result = await db.query(
    `SELECT data FROM agent_sessions WHERE task_id = $1
     ORDER BY updated_at DESC LIMIT 1`,
    [taskId]
  );
  return result.rows[0]?.data ?? null;
}
```

## Human-in-the-Loop — Approval Workflow

```typescript
// Паттерн из pipeline/orchestrate.ts — пауза для подтверждения

export type ApprovalStatus = 'pending' | 'approved' | 'rejected';

// Запросить подтверждение пользователя
async function requestApproval(
  taskId: string,
  type: 'plan' | 'destructive_action' | 'code_change',
  payload: unknown,
): Promise<ApprovalStatus> {
  // Сохранить в DB, уведомить
  await updateTaskStatus(taskId, 'waiting_approval');
  await notifyUser(taskId, { type, payload });

  // Ждать ответа (polling или webhook)
  return waitForApproval(taskId, { timeoutMs: 24 * 60 * 60 * 1000 });
}

async function waitForApproval(taskId: string, opts: { timeoutMs: number }) {
  const deadline = Date.now() + opts.timeoutMs;
  while (Date.now() < deadline) {
    const status = await getApprovalStatus(taskId);
    if (status !== 'pending') return status;
    await sleep(5000); // poll each 5s
  }
  return 'rejected'; // timeout = reject
}

// POST /api/task/:id/answer handler
router.post('/api/task/:id/answer', async (req, res) => {
  const { approved, comment } = req.body;
  await setApprovalStatus(req.params.id, approved ? 'approved' : 'rejected', comment);
  // Сброс статуса задачи для продолжения
  if (approved) await updateTaskStatus(req.params.id, 'approved');
  res.json({ success: true });
});
```

## Context Injection — buildStepPrompt паттерн

```typescript
// src/pipeline/stages.ts — обогащение контекста для LLM
export async function buildStepPrompt(
  task: PipelineTask,
  step: PipelineStep,
): Promise<string> {
  const parts: string[] = [];

  // Базовый контекст задачи
  parts.push(`## Task: ${task.title}\n${task.description}`);

  // PROJECT.md (кэшируется по hash)
  const projectContext = await getProjectContext(task.projectSlug);
  parts.push(`## Project Context\n${projectContext}`);

  // Релевантный код
  if (step === 'code' || step === 'review') {
    const diff = await getGitDiff(task.worktreePath);
    if (diff) parts.push(`## Current Changes\n\`\`\`diff\n${diff}\n\`\`\``);
  }

  // Уроки из прошлого (mcp-memory)
  const lessons = await getLessons(task.projectSlug);
  if (lessons.length > 0) {
    parts.push(`## Lessons Learned\n${lessons.map(l => `- ${l}`).join('\n')}`);
  }

  // Комментарии пользователя
  const comments = await getTaskComments(task.id);
  if (comments.length > 0) {
    parts.push(`## User Feedback\n${comments.map(c => `- ${c.text}`).join('\n')}`);
  }

  return parts.join('\n\n');
}
```

## Error Handling в Agent Loop

```typescript
// Обработка ошибок Anthropic API
async function callWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      const isRetryable =
        err instanceof Anthropic.APIError &&
        (err.status === 529 || err.status === 429 || err.status === 500);

      if (!isRetryable || attempt === maxRetries) throw err;

      const delay = Math.min(1000 * 2 ** attempt, 30_000);
      logger.warn(`Anthropic API error, retry ${attempt + 1}/${maxRetries}`, { err, delay });
      await sleep(delay);

      // Ротация ключа при overload
      if (err.status === 529 || err.status === 429) {
        keyRotator.markFailure(keyRotator.getCurrentKey(), err);
      }
    }
  }
  throw new Error('unreachable');
}
```

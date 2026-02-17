/**
 * Shared LLM runner module.
 * Used by both wiggum/loop.ts and scripts/run-*.ts to invoke LLM backends
 * with consistent flags, streaming, and logging.
 */

const MAX_RESULT = 500;

export type Backend = "claude" | "copilot" | "codex" | "shelley" | "gemini";

export interface RunOptions {
  prompt: string;
  logFile: string;
  cwd: string;
  model: string;
  signal?: AbortSignal;
  onActivity?: () => void;
}

const DEFAULT_MODELS: Record<Backend, string> = {
  claude: process.env.CLAUDE_MODEL ?? "opus",
  copilot: process.env.COPILOT_MODEL ?? "claude-opus-4.6-fast",
  codex: "gpt-5.3-codex-spark",
  shelley: process.env.SHELLEY_MODEL ?? "claude-opus-4.6",
  gemini: process.env.GEMINI_MODEL ?? "gemini-3-pro-preview",
};

export function defaultModel(backend: Backend): string {
  return DEFAULT_MODELS[backend] ?? DEFAULT_MODELS.copilot;
}

export async function runLLM(backend: Backend, opts: RunOptions): Promise<number> {
  switch (backend) {
    case "claude":  return runClaude(opts);
    case "copilot": return runCopilot(opts);
    case "codex":   return runCodex(opts);
    case "shelley": return runShelley(opts);
    case "gemini":  return runGemini(opts);
    default:
      console.error(`Unknown backend: ${backend}`);
      return 1;
  }
}

// ── Streaming helpers ────────────────────────────────────────────────────────

async function pipeStream(
  proc: ReturnType<typeof Bun.spawn>,
  logFile: string,
  onActivity?: () => void,
): Promise<number> {
  const logFd = Bun.file(logFile).writer();
  const reader = proc.stdout.getReader();
  const decoder = new TextDecoder();
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const text = decoder.decode(value, { stream: true });
      logFd.write(text);
      process.stdout.write(text);
      onActivity?.();
    }
  } finally {
    logFd.end();
  }
  return await proc.exited;
}

// ── Claude ───────────────────────────────────────────────────────────────────

async function runClaude(opts: RunOptions): Promise<number> {
  const { prompt, logFile, cwd, model, signal, onActivity } = opts;
  const proc = Bun.spawn(
    ["claude", "-p", "--dangerously-skip-permissions", "--model", model, "--output-format", "stream-json"],
    { cwd, stdin: new Blob([prompt]), stdout: "pipe", stderr: "pipe", signal },
  );

  const logFd = Bun.file(logFile).writer();
  const reader = proc.stdout.getReader();
  const decoder = new TextDecoder();
  let lineBuf = "";

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      lineBuf += decoder.decode(value, { stream: true });
      const lines = lineBuf.split("\n");
      lineBuf = lines.pop() || "";
      for (const line of lines) {
        logFd.write(line + "\n");
        onActivity?.();
        const formatted = formatClaudeStreamLine(line);
        if (formatted) process.stdout.write(formatted + "\n");
      }
    }
    if (lineBuf.trim()) {
      logFd.write(lineBuf + "\n");
      const formatted = formatClaudeStreamLine(lineBuf);
      if (formatted) process.stdout.write(formatted + "\n");
    }
  } finally {
    logFd.end();
  }
  return await proc.exited;
}

// ── Copilot ──────────────────────────────────────────────────────────────────

async function runCopilot(opts: RunOptions): Promise<number> {
  const { prompt, logFile, cwd, model, signal, onActivity } = opts;
  const browserHint = "\n\nNote: If you need to use a real browser environment (e.g., to render JS-heavy pages), read `chrome-devtools-mcp/skills/chrome-devtools/SKILL.md` for instructions.\n";
  const proc = Bun.spawn(
    ["copilot", "-p", prompt + browserHint, "--model", model,
     "--yolo", "--no-ask-user", "--no-color", "--no-auto-update"],
    { cwd, stdout: "pipe", stderr: "pipe", signal },
  );
  return pipeStream(proc, logFile, onActivity);
}

// ── Codex ────────────────────────────────────────────────────────────────────

async function runCodex(opts: RunOptions): Promise<number> {
  const { prompt, logFile, cwd, model, signal, onActivity } = opts;
  const proc = Bun.spawn(
    ["codex", "exec", "--full-auto", "--sandbox", "danger-full-access", "--model", model, "-"],
    { cwd, stdin: new Blob([prompt]), stdout: "pipe", stderr: "pipe", signal },
  );
  return pipeStream(proc, logFile, onActivity);
}

// ── Gemini ───────────────────────────────────────────────────────────────────

async function runGemini(opts: RunOptions): Promise<number> {
  const { prompt, logFile, cwd, model, signal, onActivity } = opts;
  const proc = Bun.spawn(
    ["gemini", "-p", "", "--yolo", "--output-format", "text", "--model", model],
    { cwd, stdin: new Blob([prompt]), stdout: "pipe", stderr: "pipe", signal },
  );
  return pipeStream(proc, logFile, onActivity);
}

// ── Shelley ──────────────────────────────────────────────────────────────────

const SHELLEY_SERVER = process.env.SHELLEY_SERVER ?? "http://localhost:9999";
const SHELLEY_USER = process.env.SHELLEY_USER ?? "wiggum";

interface ShelleyStreamResponse {
  messages: Array<{
    message_id: string;
    type: string;
    llm_data?: string;
    end_of_turn?: boolean;
  }>;
}

interface LLMContent {
  Type: number; // 2 = text, 3 = tool_use, 6 = tool_result
  Text?: string;
  ToolName?: string;
  ToolInput?: unknown;
  ToolError?: boolean;
  ToolResult?: LLMContent[];
}

interface LLMMessage {
  Content: LLMContent[];
}

async function runShelley(opts: RunOptions): Promise<number> {
  const { prompt, logFile, cwd, model, signal } = opts;
  const logFd = Bun.file(logFile).writer();
  const write = (text: string) => {
    process.stdout.write(text);
    logFd.write(text);
  };

  try {
    const createResp = await fetch(`${SHELLEY_SERVER}/api/conversations/new`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Exedev-Userid": SHELLEY_USER,
        "X-Shelley-Request": "1",
      },
      body: JSON.stringify({ message: prompt, model, cwd }),
      signal,
    });

    if (createResp.status !== 201) {
      write(`[ERROR] Shelley returned ${createResp.status}: ${await createResp.text()}\n`);
      return 1;
    }

    const { conversation_id } = (await createResp.json()) as { conversation_id: string };

    const streamResp = await fetch(
      `${SHELLEY_SERVER}/api/conversation/${conversation_id}/stream`,
      { headers: { "X-Exedev-Userid": SHELLEY_USER, Accept: "text/event-stream" }, signal },
    );

    if (!streamResp.ok) {
      write(`[ERROR] Shelley stream returned ${streamResp.status}: ${await streamResp.text()}\n`);
      return 1;
    }

    const reader = streamResp.body?.getReader();
    if (!reader) { write("[ERROR] No response body from Shelley stream\n"); return 1; }

    const decoder = new TextDecoder();
    const seenMessages = new Set<string>();
    let buffer = "";
    let sawEndOfTurn = false;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        let streamData: ShelleyStreamResponse;
        try { streamData = JSON.parse(line.slice(6)); } catch { continue; }
        if (!streamData.messages) continue;

        for (const msg of streamData.messages) {
          if (seenMessages.has(msg.message_id)) continue;
          seenMessages.add(msg.message_id);
          if (!msg.llm_data) continue;
          let llmMsg: LLMMessage;
          try { llmMsg = JSON.parse(msg.llm_data); } catch { continue; }

          if (msg.type === "agent") {
            for (const content of llmMsg.Content) {
              if (content.Type === 2 && content.Text) write(content.Text);
              if (content.ToolName) write(`\n[TOOL: ${content.ToolName}]\n`);
            }
          } else if (msg.type === "error") {
            for (const content of llmMsg.Content) {
              if (content.Type === 2 && content.Text) write(`[ERROR: ${content.Text}]\n`);
            }
            logFd.end();
            return 1;
          } else if (msg.type === "user") {
            for (const content of llmMsg.Content) {
              if (content.Type === 6 && content.ToolError) write("[TOOL ERROR]\n");
            }
          }

          if (msg.end_of_turn) {
            sawEndOfTurn = true;
            write("\n");
            logFd.end();
            return 0;
          }
        }
      }
    }

    if (!sawEndOfTurn) {
      write("[ERROR: Shelley stream ended without end_of_turn (EOF)]\n");
      logFd.end();
      return 1;
    }
    logFd.end();
    return 0;
  } catch (err: unknown) {
    if (signal?.aborted) { logFd.end(); return 124; }
    write(`[ERROR] Shelley: ${err instanceof Error ? err.message : err}\n`);
    logFd.end();
    return 1;
  }
}

// ── Claude stream-json formatting ────────────────────────────────────────────

function summarizeToolResult(content: unknown): string {
  let text: string;
  if (typeof content === "string") {
    text = content.trim();
  } else if (Array.isArray(content)) {
    const parts: string[] = [];
    for (const block of content) {
      if (typeof block === "object" && block !== null) {
        const b = block as Record<string, unknown>;
        if (b.type === "text") parts.push(String(b.text ?? ""));
        else if (b.type === "tool_result") parts.push(String(b.content ?? ""));
      } else if (typeof block === "string") parts.push(block);
    }
    text = parts.join("\n").trim();
  } else {
    text = String(content).trim();
  }
  return text.length > MAX_RESULT ? text.slice(0, MAX_RESULT) + "..." : text;
}

function formatClaudeStreamLine(line: string): string | null {
  if (!line.trim()) return null;
  let msg: Record<string, unknown>;
  try { msg = JSON.parse(line); } catch { return null; }

  const t = msg.type as string;
  const out: string[] = [];

  if (t === "system" && msg.subtype === "init") {
    out.push(`\n=== init model=${msg.model ?? "?"} ===\n`);
  } else if (t === "assistant" && msg.message) {
    const message = msg.message as Record<string, unknown>;
    const content = (message.content ?? []) as Array<Record<string, unknown>>;
    for (const block of content) {
      if (block.type === "thinking" && block.thinking) {
        for (const tl of String(block.thinking).split("\n")) out.push(`  💭 ${tl}`);
      } else if (block.type === "text") {
        out.push(String(block.text));
      } else if (block.type === "tool_use") {
        const name = String(block.name ?? "?");
        const inp = (block.input ?? {}) as Record<string, unknown>;
        if (name === "Bash") {
          let cmd = String(inp.command ?? "");
          if (cmd.length > 120) cmd = cmd.slice(0, 120) + "...";
          out.push(`  -> Bash: ${cmd}`);
        } else if (name === "Read") { out.push(`  -> Read: ${inp.file_path ?? "?"}`);
        } else if (name === "Write") { out.push(`  -> Write: ${inp.file_path ?? "?"}`);
        } else if (name === "Edit") { out.push(`  -> Edit: ${inp.file_path ?? "?"}`);
        } else if (name === "Grep" || name === "Glob") { out.push(`  -> ${name}: ${inp.pattern ?? "?"}`);
        } else if (name === "WebFetch") { out.push(`  -> WebFetch: ${inp.url ?? "?"}`);
        } else if (name === "Task") { out.push(`  -> Task: ${inp.description ?? "?"}`);
        } else { out.push(`  -> ${name}()`); }
      }
    }
  } else if (t === "user" && msg.message) {
    const message = msg.message as Record<string, unknown>;
    const content = (message.content ?? []) as Array<Record<string, unknown>>;
    for (const block of content) {
      if (typeof block === "object" && block.type === "tool_result") {
        const isError = block.is_error as boolean;
        const summary = summarizeToolResult(block.content);
        const prefix = isError ? "  ✗ " : "  ← ";
        if (summary) { for (const rl of summary.split("\n")) out.push(`${prefix}${rl}`); }
      }
    }
  } else if (t === "result") {
    const cost = msg.total_cost_usd ?? msg.cost_usd ?? "?";
    const duration = ((msg.duration_ms as number) ?? 0) / 1000;
    const turns = msg.num_turns ?? "?";
    const status = msg.subtype === "success" ? "OK" : "FAIL";
    out.push(`\n--- ${status} turns=${turns} cost=$${cost} time=${duration.toFixed(0)}s ---`);
  }

  return out.length > 0 ? out.join("\n") : null;
}

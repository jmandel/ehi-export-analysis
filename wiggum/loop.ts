#!/usr/bin/env bun
// EHI Export Documentation Collection Loop
//
// Single-file Bun TypeScript rewrite of loop.sh + shelley-prompt.ts + log-handler.py.
// Iterates over targets, running one LLM agent per URL per phase.
//
// Usage:
//   bun run wiggum/loop.ts --phase both --targets work/phases/phase-1-comprehensive-ehrs.json --resume --reverse
//   bun run wiggum/loop.ts --phase 1
//   bun run wiggum/loop.ts --phase 2 --resume
//   bun run wiggum/loop.ts --phase 1 --only 42

import { $ } from "bun";
import { mkdir, stat, appendFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { join, dirname } from "node:path";

// ── Types ──────────────────────────────────────────────────────────────────────

interface Target {
  url: string;
  developers: string[];
  family: string;
  focus_product: string;
  focus_version: string;
  products: string[];
  chpl_ids: number[];
  original_index?: number;
  product_count: number;
}

interface PhaseConfig {
  prompt: string;
  marker: string;
  name: string;
}

// ── Config from environment ────────────────────────────────────────────────────

const ROOT = join(dirname(new URL(import.meta.url).pathname), "..");
const RESULTS_DIR = join(ROOT, "results");
const PROMPTS_DIR = join(ROOT, "wiggum", "prompts");
const LOOP_LOG = join(ROOT, "wiggum", "logs", "loop-exit.log");

const LLM_BACKEND = process.env.LLM_BACKEND ?? "claude";
const CLAUDE_MODEL = process.env.CLAUDE_MODEL ?? "opus";
const COPILOT_MODEL = process.env.COPILOT_MODEL ?? "claude-opus-4.6-fast";
const SHELLEY_SERVER = process.env.SHELLEY_SERVER ?? "http://localhost:9999";
const SHELLEY_MODEL = process.env.SHELLEY_MODEL ?? "claude-opus-4.6";
const SHELLEY_USER = process.env.SHELLEY_USER ?? "wiggum";
const GEMINI_MODEL = process.env.GEMINI_MODEL ?? "gemini-3-pro-preview";
const TIMEOUT = parseInt(process.env.TIMEOUT ?? "1800", 10) * 1000; // ms
const STALE_TIMEOUT = parseInt(process.env.STALE_TIMEOUT ?? "300", 10) * 1000; // ms
const DISCOURAGE_SUBAGENTS = process.env.DISCOURAGE_SUBAGENTS ?? "";

const PHASES: Record<string, PhaseConfig> = {
  "1": {
    prompt: join(ROOT, "wiggum", "prompts", "1-research.md"),
    marker: "sources.json",
    name: "research",
  },
  "2": {
    prompt: join(ROOT, "wiggum", "prompts", "2-download.md"),
    marker: "files.json",
    name: "download",
  },
};

// ── CLI Argument Parsing ───────────────────────────────────────────────────────

function parseArgs(): {
  targets: string;
  phase: string;
  resume: boolean;
  reverse: boolean;
  startIndex: number;
  onlyIndex?: number;
} {
  const args = process.argv.slice(2);
  let targets = join(ROOT, "work", "targets.json");
  let phase = "";
  let resume = false;
  let reverse = false;
  let startIndex = 0;
  let onlyIndex: number | undefined;

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--targets": targets = args[++i]; break;
      case "--phase": phase = args[++i]; break;
      case "--resume": resume = true; break;
      case "--reverse": reverse = true; break;
      case "--index": startIndex = parseInt(args[++i], 10); break;
      case "--only": onlyIndex = parseInt(args[++i], 10); break;
      case "--help": case "-h":
        console.log(`Usage: bun run wiggum/loop.ts --phase <1|2|both> [options]

Options:
  --targets <file>   Target list JSON (default: work/targets.json)
  --phase <1|2|both> Agent phase: research, download, or both (required)
  --resume           Skip targets with existing completion marker
  --reverse          Iterate from end of list backwards
  --index <N>        Start from target index N
  --only <N>         Run only target index N

Environment:
  LLM_BACKEND        claude | copilot | shelley | gemini (default: claude)
  CLAUDE_MODEL       Model for claude backend (default: opus)
  COPILOT_MODEL      Model for copilot backend (default: claude-opus-4.6-fast)
  SHELLEY_SERVER     Shelley server URL (default: http://localhost:9999)
  SHELLEY_MODEL      Shelley model (default: claude-opus-4.6)
  GEMINI_MODEL       Gemini model (default: gemini-3-pro-preview)
  TIMEOUT            Per-target timeout in seconds (default: 1800)
  STALE_TIMEOUT      Kill agent if log stale for N seconds (default: 300)
  DISCOURAGE_SUBAGENTS  Set non-empty to discourage subagent use`);
        process.exit(0);
      default:
        console.error(`Unknown arg: ${args[i]}`);
        process.exit(1);
    }
  }

  if (!phase) {
    console.error("Error: --phase is required (1, 2, or both)");
    process.exit(1);
  }
  if (phase !== "both" && !PHASES[phase]) {
    console.error(`Error: unknown phase "${phase}"`);
    process.exit(1);
  }

  return { targets, phase, resume, reverse, startIndex, onlyIndex };
}

// ── Utilities ──────────────────────────────────────────────────────────────────

import { slugify, resultDirName } from "../scripts/naming.ts";

function log(msg: string) {
  const ts = new Date().toISOString().replace("T", " ").slice(0, 19);
  console.log(`[${ts}] ${msg}`);
}

async function logExit(code: number, context?: string) {
  const ts = new Date().toISOString().replace("T", " ").slice(0, 19);
  const msg = code === 0
    ? `[${ts}] Loop finished normally`
    : `[${ts}] Loop exited with code ${code}${context ? ` (${context})` : ""}`;
  await mkdir(dirname(LOOP_LOG), { recursive: true });
  await appendFile(LOOP_LOG, msg + "\n");
  console.error(msg);
}

// ── Template Rendering ─────────────────────────────────────────────────────────

function renderTemplate(
  template: string,
  vars: Record<string, string>,
): string {
  // Simple variable substitution: {{URL}}, {{DEVELOPERS}}, etc.
  let rendered = template;
  for (const [key, value] of Object.entries(vars)) {
    rendered = rendered.replaceAll(`{{${key}}}`, value);
  }

  // File includes: {{EHI_SCOPE_REFERENCE}} → read prompts/ehi-scope-reference.md
  rendered = rendered.replace(/\{\{([A-Z_]+)\}\}/g, (_match, key: string) => {
    const filename = key.toLowerCase().replace(/_/g, "-") + ".md";
    const filepath = join(PROMPTS_DIR, filename);
    try {
      return Bun.file(filepath).textSync?.() ??
        require("node:fs").readFileSync(filepath, "utf-8");
    } catch {
      return _match; // keep placeholder if file not found
    }
  });

  if (DISCOURAGE_SUBAGENTS) {
    rendered += "\n\n> **Note:** Avoid using subagents for this task. Work sequentially in a single conversation.\n";
  }

  return rendered;
}

// ── Claude Stream-JSON Log Handler ─────────────────────────────────────────────

const MAX_RESULT = 500;

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
      } else if (typeof block === "string") {
        parts.push(block);
      }
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
  try {
    msg = JSON.parse(line);
  } catch {
    return null;
  }

  const t = msg.type as string;
  const out: string[] = [];

  if (t === "system" && msg.subtype === "init") {
    out.push(`\n=== init model=${msg.model ?? "?"} ===\n`);
  } else if (t === "assistant" && msg.message) {
    const message = msg.message as Record<string, unknown>;
    const content = (message.content ?? []) as Array<Record<string, unknown>>;
    for (const block of content) {
      if (block.type === "thinking" && block.thinking) {
        for (const tl of String(block.thinking).split("\n")) {
          out.push(`  💭 ${tl}`);
        }
      } else if (block.type === "text") {
        out.push(String(block.text));
      } else if (block.type === "tool_use") {
        const name = String(block.name ?? "?");
        const inp = (block.input ?? {}) as Record<string, unknown>;
        if (name === "Bash") {
          let cmd = String(inp.command ?? "");
          if (cmd.length > 120) cmd = cmd.slice(0, 120) + "...";
          out.push(`  -> Bash: ${cmd}`);
        } else if (name === "Read") {
          out.push(`  -> Read: ${inp.file_path ?? "?"}`);
        } else if (name === "Write") {
          out.push(`  -> Write: ${inp.file_path ?? "?"}`);
        } else if (name === "Edit") {
          out.push(`  -> Edit: ${inp.file_path ?? "?"}`);
        } else if (name === "Grep" || name === "Glob") {
          out.push(`  -> ${name}: ${inp.pattern ?? "?"}`);
        } else if (name === "WebFetch") {
          out.push(`  -> WebFetch: ${inp.url ?? "?"}`);
        } else if (name === "Task") {
          out.push(`  -> Task: ${inp.description ?? "?"}`);
        } else {
          out.push(`  -> ${name}()`);
        }
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
        if (summary) {
          for (const rl of summary.split("\n")) {
            out.push(`${prefix}${rl}`);
          }
        }
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

// ── Shelley Client (inlined) ───────────────────────────────────────────────────

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

async function runShelley(
  prompt: string,
  logFile: string,
  cwd: string,
  signal: AbortSignal,
): Promise<number> {
  const logFd = Bun.file(logFile).writer();
  const write = (text: string) => {
    process.stdout.write(text);
    logFd.write(text);
  };

  try {
    // Create conversation
    const createResp = await fetch(`${SHELLEY_SERVER}/api/conversations/new`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Exedev-Userid": SHELLEY_USER,
        "X-Shelley-Request": "1",
      },
      body: JSON.stringify({
        message: prompt,
        model: SHELLEY_MODEL,
        cwd,
      }),
      signal,
    });

    if (createResp.status !== 201) {
      const text = await createResp.text();
      write(`[ERROR] Shelley returned ${createResp.status}: ${text}\n`);
      return 1;
    }

    const { conversation_id } = (await createResp.json()) as { conversation_id: string };

    // Stream responses
    const streamResp = await fetch(
      `${SHELLEY_SERVER}/api/conversation/${conversation_id}/stream`,
      {
        headers: {
          "X-Exedev-Userid": SHELLEY_USER,
          Accept: "text/event-stream",
        },
        signal,
      },
    );

    if (!streamResp.ok) {
      const text = await streamResp.text();
      write(`[ERROR] Shelley stream returned ${streamResp.status}: ${text}\n`);
      return 1;
    }

    const reader = streamResp.body?.getReader();
    if (!reader) {
      write("[ERROR] No response body from Shelley stream\n");
      return 1;
    }

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
        try {
          streamData = JSON.parse(line.slice(6));
        } catch {
          continue;
        }
        if (!streamData.messages) continue;

        for (const msg of streamData.messages) {
          if (seenMessages.has(msg.message_id)) continue;
          seenMessages.add(msg.message_id);

          if (!msg.llm_data) continue;
          let llmMsg: LLMMessage;
          try {
            llmMsg = JSON.parse(msg.llm_data);
          } catch {
            continue;
          }

          if (msg.type === "agent") {
            for (const content of llmMsg.Content) {
              if (content.Type === 2 && content.Text) {
                write(content.Text);
              }
              if (content.ToolName) {
                const toolLine = `\n[TOOL: ${content.ToolName}]\n`;
                write(toolLine);
              }
            }
          } else if (msg.type === "error") {
            for (const content of llmMsg.Content) {
              if (content.Type === 2 && content.Text) {
                write(`[ERROR: ${content.Text}]\n`);
              }
            }
            logFd.end();
            return 1;
          } else if (msg.type === "user") {
            for (const content of llmMsg.Content) {
              if (content.Type === 6 && content.ToolError) {
                write("[TOOL ERROR]\n");
              }
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
    if (signal.aborted) {
      logFd.end();
      return 124; // timeout convention
    }
    write(`[ERROR] Shelley: ${err instanceof Error ? err.message : err}\n`);
    logFd.end();
    return 1;
  }
}

// ── LLM Backend Dispatch ───────────────────────────────────────────────────────

async function runLlm(
  prompt: string,
  logFile: string,
  cwd: string,
  signal: AbortSignal,
  touchLog: () => void,
): Promise<number> {
  switch (LLM_BACKEND) {
    case "claude":
      return runClaude(prompt, logFile, cwd, signal, touchLog);
    case "copilot":
      return runCopilot(prompt, logFile, cwd, signal, touchLog);
    case "shelley":
      return runShelley(prompt, logFile, cwd, signal);
    case "gemini":
      return runGemini(prompt, logFile, cwd, signal, touchLog);
    default:
      console.error(`Unknown LLM_BACKEND: ${LLM_BACKEND}`);
      return 1;
  }
}

async function runClaude(
  prompt: string,
  logFile: string,
  cwd: string,
  signal: AbortSignal,
  touchLog: () => void,
): Promise<number> {
  const proc = Bun.spawn(
    ["claude", "-p", "--dangerously-skip-permissions", "--model", CLAUDE_MODEL, "--output-format", "stream-json"],
    {
      cwd,
      stdin: new Blob([prompt]),
      stdout: "pipe",
      stderr: "pipe",
      signal,
    },
  );

  const logFd = Bun.file(logFile).writer();

  // Process stdout: parse stream-json, format for human reading, tee to log + stdout
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
        // Write raw stream-json to log file
        logFd.write(line + "\n");
        touchLog();

        // Format for human display
        const formatted = formatClaudeStreamLine(line);
        if (formatted) {
          process.stdout.write(formatted + "\n");
        }
      }
    }
    // Handle any remaining partial line
    if (lineBuf.trim()) {
      logFd.write(lineBuf + "\n");
      const formatted = formatClaudeStreamLine(lineBuf);
      if (formatted) process.stdout.write(formatted + "\n");
    }
  } finally {
    logFd.end();
  }

  const exitCode = await proc.exited;
  return exitCode;
}

async function runCopilot(
  prompt: string,
  logFile: string,
  cwd: string,
  signal: AbortSignal,
  touchLog: () => void,
): Promise<number> {
  const browserHint = "\n\nNote: If you need to use a real browser environment (e.g., to render JS-heavy pages), read `chrome-devtools-mcp/skills/chrome-devtools/SKILL.md` for instructions.\n";
  const fullPrompt = prompt + browserHint;
  const proc = Bun.spawn(
    ["copilot", "-p", fullPrompt, "--model", COPILOT_MODEL,
     "--yolo", "--no-ask-user", "--no-color", "--no-auto-update"],
    {
      cwd,
      stdout: "pipe",
      stderr: "pipe",
      signal,
    },
  );

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
      touchLog();
    }
  } finally {
    logFd.end();
  }

  const exitCode = await proc.exited;
  return exitCode;
}

async function runGemini(
  prompt: string,
  logFile: string,
  cwd: string,
  signal: AbortSignal,
  touchLog: () => void,
): Promise<number> {
  const proc = Bun.spawn(
    ["gemini", "-p", "", "--yolo", "--output-format", "text", "--model", GEMINI_MODEL],
    {
      cwd,
      stdin: new Blob([prompt]),
      stdout: "pipe",
      stderr: "pipe",
      signal,
    },
  );

  const logFd = Bun.file(logFile).writer();
  const reader = proc.stdout.getReader();
  const decoder = new TextDecoder();

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      process.stdout.write(chunk);
      logFd.write(chunk);
      touchLog();
    }
  } finally {
    logFd.end();
  }

  const exitCode = await proc.exited;
  return exitCode;
}

// ── Stale-Output Watchdog + Timeout ────────────────────────────────────────────

function startWatchdog(
  logFile: string,
  killFn: () => void,
): { stop: () => void; touch: () => void } {
  let lastTouchMs = Date.now();

  const touch = () => { lastTouchMs = Date.now(); };

  // Check staleness every 30s
  const watchdogInterval = setInterval(() => {
    const age = Date.now() - lastTouchMs;
    if (age > STALE_TIMEOUT) {
      console.error(`  watchdog: log stale for ${(age / 1000).toFixed(0)}s, killing agent`);
      killFn();
    }
  }, 30_000);

  // Overall timeout
  const timeoutId = setTimeout(() => {
    console.error(`  timeout: ${(TIMEOUT / 1000).toFixed(0)}s exceeded, killing agent`);
    killFn();
  }, TIMEOUT);

  return {
    stop: () => {
      clearInterval(watchdogInterval);
      clearTimeout(timeoutId);
    },
    touch,
  };
}

// ── Git Commit ─────────────────────────────────────────────────────────────────

async function commitResult(slug: string, phaseLabel: string) {
  try {
    await $`git -C ${ROOT} add ${join(RESULTS_DIR, slug)}/`.quiet();
    // Check if anything is actually staged
    const diffResult = await $`git -C ${ROOT} diff --cached --quiet`.nothrow().quiet();
    if (diffResult.exitCode === 0) return; // nothing to commit
    await $`git -C ${ROOT} commit -m ${`${slug}: ${phaseLabel} complete`} --author=${"wiggum <wiggum@ehi-export-analysis>"}`.quiet();
    await $`git -C ${ROOT} push`.nothrow().quiet();
  } catch (err) {
    console.error(`  git commit failed: ${err instanceof Error ? err.message : err}`);
  }
}

// ── Per-Target Runner ──────────────────────────────────────────────────────────

async function runTarget(
  idx: number,
  total: number,
  targets: Target[],
  phasesToRun: string[],
  phaseLabel: string,
  completionMarker: string,
  resume: boolean,
): Promise<"completed" | "failed" | "skipped"> {
  const target = targets[idx];
  const url = target.url;
  const developers = target.developers.join(", ");
  const products = target.products.join(", ");
  const chplIds = target.chpl_ids.map(String).join(", ");
  const family = target.family ?? target.products[0] ?? "unknown";
  const focusProduct = target.focus_product ?? family;
  const focusVersion = target.focus_version ?? "";

  // Slug: <vendor>--<family>
  const slug = resultDirName(target, idx);

  const outputDir = join(RESULTS_DIR, slug);

  // Skip if fully done
  if (resume && existsSync(join(outputDir, completionMarker))) {
    console.log(`[${idx}/${total}] SKIP ${slug}`);
    return "skipped";
  }

  await mkdir(join(outputDir, "downloads"), { recursive: true });

  // Copy & filter CHPL metadata to just this family's products
  const origIdx = target.original_index ?? idx;
  const metaFile = join(ROOT, "work", "target-metadata", String(origIdx).padStart(4, "0") + ".json");
  if (existsSync(metaFile)) {
    const meta = await Bun.file(metaFile).json();
    const familyIds = new Set(target.chpl_ids);
    meta.products = (meta.products ?? []).filter(
      (p: { chpl_id: number }) => familyIds.has(p.chpl_id),
    );
    if (meta.products.length === 0) {
      console.log(`  SKIP: no matching products in metadata`);
      return "skipped";
    }
    await Bun.write(join(outputDir, "chpl-metadata.json"), JSON.stringify(meta, null, 2));
  }

  console.log(`[${idx}/${total}] ${slug}`);
  console.log(`  URL: ${url}`);
  console.log(`  Dev: ${developers}`);
  console.log(`  Family: ${family} (focus: ${focusProduct} ${focusVersion})`);

  const templateVars: Record<string, string> = {
    URL: url,
    DEVELOPERS: developers,
    PRODUCTS: products,
    CHPL_IDS: chplIds,
    FAMILY: family,
    FOCUS_PRODUCT: focusProduct,
    FOCUS_VERSION: focusVersion,
    OUTPUT_DIR: outputDir,
  };

  for (const phase of phasesToRun) {
    const cfg = PHASES[phase];
    if (existsSync(join(outputDir, cfg.marker))) {
      console.log(`  phase ${phase} (${cfg.name}): already done`);
      continue;
    }

    console.log(`  phase ${phase} (${cfg.name}): running...`);

    // Read and render template
    const rawTemplate = await Bun.file(cfg.prompt).text();
    const prompt = renderTemplate(rawTemplate, templateVars);

    const logFile = join(outputDir, `phase${phase}-log.txt`);
    const t0 = Date.now();

    // Create abort controller for timeout/watchdog kills
    const ac = new AbortController();
    const watchdog = startWatchdog(logFile, () => ac.abort());

    const exitCode = await runLlm(prompt, logFile, ROOT, ac.signal, watchdog.touch);
    watchdog.stop();

    const elapsed = ((Date.now() - t0) / 1000).toFixed(0);

    if (exitCode === 0) {
      console.log(`  phase ${phase} (${cfg.name}): done (${elapsed}s)`);
    } else if (ac.signal.aborted) {
      console.log(`  ⏰ phase ${phase} (${cfg.name}): timed out / stale after ${elapsed}s`);
      return "failed";
    } else {
      console.log(`  phase ${phase} (${cfg.name}): FAILED (exit ${exitCode}, ${elapsed}s)`);
      return "failed";
    }
  }

  await commitResult(slug, phaseLabel);
  return "completed";
}

// ── Main ───────────────────────────────────────────────────────────────────────

async function main() {
  const opts = parseArgs();
  await mkdir(RESULTS_DIR, { recursive: true });
  await mkdir(dirname(LOOP_LOG), { recursive: true });

  if (!existsSync(opts.targets)) {
    console.error(`No targets file found: ${opts.targets}`);
    console.error("Run 00-fetch-export-urls.sh first.");
    process.exit(1);
  }

  const targets: Target[] = await Bun.file(opts.targets).json();
  const total = targets.length;

  // Determine which phases to run
  let phasesToRun: string[];
  let phaseLabel: string;
  let completionMarker: string;

  if (opts.phase === "both") {
    phasesToRun = ["1", "2"];
    phaseLabel = "both (research+download)";
    completionMarker = PHASES["2"].marker;
  } else {
    phasesToRun = [opts.phase];
    phaseLabel = PHASES[opts.phase].name;
    completionMarker = PHASES[opts.phase].marker;
  }

  // Banner
  const modelLabel =
    LLM_BACKEND === "claude" ? `claude-${CLAUDE_MODEL}` :
    LLM_BACKEND === "copilot" ? COPILOT_MODEL :
    LLM_BACKEND === "shelley" ? SHELLEY_MODEL :
    LLM_BACKEND === "gemini" ? GEMINI_MODEL :
    LLM_BACKEND;

  console.log("=== EHI Export Documentation Collection ===");
  console.log(`Phase:   ${opts.phase} (${phaseLabel})`);
  console.log(`Backend: ${LLM_BACKEND} (${modelLabel})`);
  console.log(`Targets: ${opts.targets} (${total} families)`);
  console.log(`Results: ${RESULTS_DIR}/`);
  console.log("");

  let completed = 0;
  let failed = 0;
  let skipped = 0;

  const processResult = (result: "completed" | "failed" | "skipped") => {
    if (result === "completed") completed++;
    else if (result === "failed") failed++;
    else skipped++;
  };

  if (opts.onlyIndex !== undefined) {
    processResult(await runTarget(opts.onlyIndex, total, targets, phasesToRun, phaseLabel, completionMarker, opts.resume));
  } else if (opts.reverse) {
    for (let i = total - 1; i >= opts.startIndex; i--) {
      processResult(await runTarget(i, total, targets, phasesToRun, phaseLabel, completionMarker, opts.resume));
    }
  } else {
    for (let i = opts.startIndex; i < total; i++) {
      processResult(await runTarget(i, total, targets, phasesToRun, phaseLabel, completionMarker, opts.resume));
    }
  }

  console.log("");
  console.log("=== Done ===");
  console.log(`Completed: ${completed} | Failed: ${failed} | Skipped: ${skipped}`);

  await logExit(0);
}

// Run with exit logging on failure
main().catch(async (err) => {
  const msg = err instanceof Error ? err.message : String(err);
  await logExit(1, msg);
  process.exit(1);
});

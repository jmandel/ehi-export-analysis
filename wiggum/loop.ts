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

import { runLLM, type Backend } from "./llm-runner";
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
const SHELLEY_MODEL = process.env.SHELLEY_MODEL ?? "claude-opus-4.6";
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

    const model =
      LLM_BACKEND === "claude" ? CLAUDE_MODEL :
      LLM_BACKEND === "copilot" ? COPILOT_MODEL :
      LLM_BACKEND === "shelley" ? SHELLEY_MODEL :
      LLM_BACKEND === "gemini" ? GEMINI_MODEL :
      "";
    const exitCode = await runLLM(LLM_BACKEND as Backend, {
      prompt,
      logFile,
      cwd: ROOT,
      model,
      signal: ac.signal,
      onActivity: watchdog.touch,
    });
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

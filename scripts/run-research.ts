#!/usr/bin/env bun
// Run Phase 1 (product research) for a single vendor's results directory.
//
// Renders the research prompt template, invokes an LLM agent, and
// expects it to produce product-research.md + sources.json.
//
// Usage:
//   bun run scripts/run-research.ts --dir <results-dir-name> [--backend <backend>] [--model <model>]

import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";

const ROOT_DIR = join(dirname(import.meta.path), "..");

// ── CLI parsing ──────────────────────────────────────────────────────────────

function usage(): never {
  console.log(`Usage:
  bun run scripts/run-research.ts --dir <results-dir-name> [options]

Options:
  --dir        Directory name under results/ (required, e.g. "vendor--product")
  --backend    LLM backend: copilot, codex (default: copilot)
  --model      Model override (default: claude-opus-4.6-fast for copilot)
  --prompt     Custom prompt file (default: wiggum/prompts/1-research.md)
  -h, --help   Show this message

Examples:
  bun run scripts/run-research.ts --dir ezemrx-inc--ezemrx
  bun run scripts/run-research.ts --dir epic-systems-corporation--epic-ehr --backend copilot`);
  process.exit(0);
}

let targetDirname = "";
let backend = "copilot";
let model = "";
let customPrompt = "";

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--dir":        targetDirname = args[++i]; break;
    case "--backend":    backend = args[++i]; break;
    case "--model":      model = args[++i]; break;
    case "--prompt":     customPrompt = args[++i]; break;
    case "-h": case "--help": usage();
    default:
      console.error(`Unknown arg: ${args[i]}`);
      usage();
  }
}

if (!targetDirname) {
  console.error("Missing required --dir argument.");
  usage();
}

// ── Default model per backend ────────────────────────────────────────────────

if (!model) {
  switch (backend) {
    case "copilot": model = "claude-opus-4.6-fast"; break;
    case "codex":   model = "gpt-5.3-codex-spark"; break;
    default:
      console.error(`Unknown backend: ${backend}`);
      process.exit(1);
  }
}

// ── Validate paths ───────────────────────────────────────────────────────────

const outputDir = join(ROOT_DIR, "results", targetDirname);

if (!existsSync(outputDir)) {
  console.error(`Results folder not found: ${outputDir}`);
  console.error(`Create it first with: mkdir -p results/${targetDirname}/downloads`);
  process.exit(2);
}

const metadataPath = join(outputDir, "chpl-metadata.json");
if (!existsSync(metadataPath)) {
  console.error(`chpl-metadata.json not found in ${outputDir}`);
  console.error("This file is required for research. Run build-metadata.ts first or copy from work/target-metadata/.");
  process.exit(2);
}

// ── Extract template variables ───────────────────────────────────────────────

const metadata = await Bun.file(metadataPath).json();
const url = metadata.url ?? "";
const developers = [metadata.developer?.name].filter(Boolean).join(", ");
const products = (metadata.products ?? []).map((p: any) => p.product_name).filter(Boolean).join(", ");
const chplIds = (metadata.products ?? []).map((p: any) => p.chpl_id).filter(Boolean).map(String).join(", ");

// ── Render prompt template ───────────────────────────────────────────────────

const promptTemplate = customPrompt || join(ROOT_DIR, "wiggum/prompts/1-research.md");
const promptsDir = join(ROOT_DIR, "wiggum/prompts");

let tmpl = readFileSync(promptTemplate, "utf8");

const vars: Record<string, string> = {
  URL: url,
  DEVELOPERS: developers,
  PRODUCTS: products,
  CHPL_IDS: chplIds,
  OUTPUT_DIR: outputDir,
};

for (const [key, value] of Object.entries(vars)) {
  tmpl = tmpl.replaceAll(`{{${key}}}`, value);
}

// File includes for remaining {{PLACEHOLDERS}}
tmpl = tmpl.replace(/\{\{([A-Z_]+)\}\}/g, (match, key) => {
  const filename = key.toLowerCase().replace(/_/g, "-") + ".md";
  const filepath = join(promptsDir, filename);
  try { return readFileSync(filepath, "utf8"); } catch { return match; }
});

const renderedPrompt = tmpl;

// ── Print banner ─────────────────────────────────────────────────────────────

console.log("=== Phase 1: Product Research ===");
console.log(`Target:     ${targetDirname}`);
console.log(`Developer:  ${developers}`);
console.log(`Products:   ${products}`);
console.log(`Output:     ${outputDir}`);
console.log(`Backend:    ${backend} (${model})`);
console.log(`Prompt:     ${Buffer.byteLength(renderedPrompt)} bytes`);
console.log("");

// ── Log file ─────────────────────────────────────────────────────────────────

const logFile = join(outputDir, "phase1-log.txt");
const logFd = Bun.file(logFile).writer();

// ── Run agent ────────────────────────────────────────────────────────────────

let exitCode: number;

if (backend === "copilot") {
  const proc = Bun.spawn(
    ["copilot", "-p", renderedPrompt, "--model", model,
     "--yolo", "--no-ask-user", "--no-color", "--no-auto-update"],
    {
      cwd: ROOT_DIR,
      stdout: "pipe",
      stderr: "pipe",
    },
  );

  const reader = proc.stdout.getReader();
  const decoder = new TextDecoder();
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const text = decoder.decode(value, { stream: true });
      logFd.write(text);
      process.stdout.write(text);
    }
  } finally {
    logFd.end();
  }

  exitCode = await proc.exited;
} else if (backend === "codex") {
  const tmpFile = join(outputDir, ".prompt-tmp.md");
  writeFileSync(tmpFile, renderedPrompt);

  const proc = Bun.spawn(
    ["codex", "exec", "--full-auto", "--sandbox", "danger-full-access",
     "--model", model, "-"],
    {
      cwd: ROOT_DIR,
      stdin: Bun.file(tmpFile),
      stdout: "pipe",
      stderr: "pipe",
    },
  );

  const reader = proc.stdout.getReader();
  const decoder = new TextDecoder();
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const text = decoder.decode(value, { stream: true });
      logFd.write(text);
      process.stdout.write(text);
    }
  } finally {
    logFd.end();
  }

  exitCode = await proc.exited;
  try { require("fs").unlinkSync(tmpFile); } catch {}
} else {
  console.error(`Unknown backend: ${backend}`);
  process.exit(1);
}

if (exitCode !== 0) {
  console.error(`${backend} exited with code ${exitCode}.`);
  process.exit(exitCode);
}

// ── Verify outputs ───────────────────────────────────────────────────────────

if (!existsSync(join(outputDir, "product-research.md"))) {
  console.error(`WARNING: product-research.md was not created at ${outputDir}/product-research.md`);
  process.exit(7);
}
if (!existsSync(join(outputDir, "sources.json"))) {
  console.error(`WARNING: sources.json was not created at ${outputDir}/sources.json`);
  process.exit(7);
}

console.log("");
console.log("=== Done ===");
console.log(`Research: ${outputDir}/product-research.md`);
console.log(`Sources:  ${outputDir}/sources.json`);

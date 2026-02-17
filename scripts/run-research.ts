#!/usr/bin/env bun
// Run Phase 1 (product research) for a single vendor's results directory.
//
// Usage:
//   bun run scripts/run-research.ts --dir <results-dir-name> [--backend <backend>] [--model <model>]

import { existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { runLLM, defaultModel, type Backend } from "../wiggum/llm-runner";
import { renderTemplate } from "../wiggum/template";

const ROOT_DIR = join(dirname(import.meta.path), "..");

// ── CLI parsing ──────────────────────────────────────────────────────────────

function usage(): never {
  console.log(`Usage:
  bun run scripts/run-research.ts --dir <results-dir-name> [options]

Options:
  --dir        Directory name under results/ (required)
  --backend    LLM backend: claude, copilot, codex (default: copilot)
  --model      Model override
  --prompt     Custom prompt file (default: wiggum/prompts/1-research.md)
  -h, --help   Show this message

Examples:
  bun run scripts/run-research.ts --dir ezemrx-inc--ezemrx
  bun run scripts/run-research.ts --dir epic-systems-corporation--epic-ehr --backend claude`);
  process.exit(0);
}

let targetDirname = "";
let backend: Backend = "copilot";
let model = "";
let customPrompt = "";

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--dir":        targetDirname = args[++i]; break;
    case "--backend":    backend = args[++i] as Backend; break;
    case "--model":      model = args[++i]; break;
    case "--prompt":     customPrompt = args[++i]; break;
    case "-h": case "--help": usage();
    default: console.error(`Unknown arg: ${args[i]}`); usage();
  }
}

if (!targetDirname) { console.error("Missing required --dir argument."); usage(); }
if (!model) model = defaultModel(backend);

// ── Validate paths ───────────────────────────────────────────────────────────

const outputDir = join(ROOT_DIR, "results", targetDirname);
if (!existsSync(outputDir)) { console.error(`Results folder not found: ${outputDir}`); process.exit(2); }

const metadataPath = join(outputDir, "chpl-metadata.json");
if (!existsSync(metadataPath)) { console.error(`chpl-metadata.json not found in ${outputDir}`); process.exit(2); }

// ── Render prompt ────────────────────────────────────────────────────────────

const metadata = await Bun.file(metadataPath).json();
const developers = [metadata.developer?.name].filter(Boolean).join(", ");
const products = (metadata.products ?? []).map((p: any) => p.product_name).filter(Boolean).join(", ");
const chplIds = (metadata.products ?? []).map((p: any) => p.chpl_id).filter(Boolean).map(String).join(", ");

const renderedPrompt = renderTemplate(
  customPrompt || join(ROOT_DIR, "wiggum/prompts/1-research.md"),
  { URL: metadata.url ?? "", DEVELOPERS: developers, PRODUCTS: products, CHPL_IDS: chplIds, OUTPUT_DIR: outputDir },
  join(ROOT_DIR, "wiggum/prompts"),
);

// ── Run ──────────────────────────────────────────────────────────────────────

console.log("=== Phase 1: Product Research ===");
console.log(`Target:     ${targetDirname}`);
console.log(`Developer:  ${developers}`);
console.log(`Products:   ${products}`);
console.log(`Output:     ${outputDir}`);
console.log(`Backend:    ${backend} (${model})`);
console.log(`Prompt:     ${Buffer.byteLength(renderedPrompt)} bytes`);
console.log("");

const exitCode = await runLLM(backend, {
  prompt: renderedPrompt,
  logFile: join(outputDir, "phase1-log.txt"),
  cwd: ROOT_DIR,
  model,
});

if (exitCode !== 0) { console.error(`${backend} exited with code ${exitCode}.`); process.exit(exitCode); }

if (!existsSync(join(outputDir, "product-research.md"))) { console.error("WARNING: product-research.md was not created"); process.exit(7); }
if (!existsSync(join(outputDir, "sources.json"))) { console.error("WARNING: sources.json was not created"); process.exit(7); }

console.log("\n=== Done ===");
console.log(`Research: ${outputDir}/product-research.md`);
console.log(`Sources:  ${outputDir}/sources.json`);

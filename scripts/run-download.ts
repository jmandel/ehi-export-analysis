#!/usr/bin/env bun
// Run Phase 2 (download EHI documentation) for a single vendor's results directory.
//
// Usage:
//   bun run scripts/run-download.ts --dir <results-dir-name> [--backend <backend>] [--model <model>]

import { existsSync, mkdirSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { runLLM, defaultModel, type Backend } from "../wiggum/llm-runner";
import { renderTemplate } from "../wiggum/template";
import { snapshotHtmlFiles } from "./singlefile";

const ROOT_DIR = join(dirname(import.meta.path), "..");

function usage(): never {
  console.log(`Usage:
  bun run scripts/run-download.ts --dir <results-dir-name> [options]

Options:
  --dir        Directory name under results/ (required)
  --backend    LLM backend: claude, copilot, codex (default: copilot)
  --model      Model override
  --prompt     Custom prompt file (default: wiggum/prompts/2-download.md)
  --snapshot   After download, create SingleFile snapshots of HTML files
  -h, --help   Show this message

Examples:
  bun run scripts/run-download.ts --dir ezemrx-inc--ezemrx
  bun run scripts/run-download.ts --dir epic-systems-corporation--epic-ehr --backend claude`);
  process.exit(0);
}

let targetDirname = "";
let backend: Backend = "copilot";
let model = "";
let customPrompt = "";
let snapshot = false;

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--dir":        targetDirname = args[++i]; break;
    case "--backend":    backend = args[++i] as Backend; break;
    case "--model":      model = args[++i]; break;
    case "--prompt":     customPrompt = args[++i]; break;
    case "--snapshot":   snapshot = true; break;
    case "-h": case "--help": usage();
    default: console.error(`Unknown arg: ${args[i]}`); usage();
  }
}

if (!targetDirname) { console.error("Missing required --dir argument."); usage(); }
if (!model) model = defaultModel(backend);

const outputDir = join(ROOT_DIR, "results", targetDirname);
if (!existsSync(outputDir)) { console.error(`Results folder not found: ${outputDir}`); process.exit(2); }
const metadataPath = join(outputDir, "chpl-metadata.json");
if (!existsSync(metadataPath)) { console.error(`chpl-metadata.json not found in ${outputDir}`); process.exit(2); }

mkdirSync(join(outputDir, "downloads"), { recursive: true });

const metadata = await Bun.file(metadataPath).json();
const developers = [metadata.developer?.name].filter(Boolean).join(", ");
const products = (metadata.products ?? []).map((p: any) => p.product_name).filter(Boolean).join(", ");
const chplIds = (metadata.products ?? []).map((p: any) => p.chpl_id).filter(Boolean).map(String).join(", ");

const renderedPrompt = renderTemplate(
  customPrompt || join(ROOT_DIR, "wiggum/prompts/2-download.md"),
  { URL: metadata.url ?? "", DEVELOPERS: developers, PRODUCTS: products, CHPL_IDS: chplIds, OUTPUT_DIR: outputDir },
  join(ROOT_DIR, "wiggum/prompts"),
);

console.log("=== Phase 2: Download EHI Documentation ===");
console.log(`Target:     ${targetDirname}`);
console.log(`URL:        ${metadata.url ?? ""}`);
console.log(`Developer:  ${developers}`);
console.log(`Products:   ${products}`);
console.log(`Output:     ${outputDir}`);
console.log(`Backend:    ${backend} (${model})`);
console.log(`Prompt:     ${Buffer.byteLength(renderedPrompt)} bytes`);
console.log("");

const exitCode = await runLLM(backend, {
  prompt: renderedPrompt,
  logFile: join(outputDir, "phase2-log.txt"),
  cwd: ROOT_DIR,
  model,
});

if (exitCode !== 0) { console.error(`${backend} exited with code ${exitCode}.`); process.exit(exitCode); }
if (!existsSync(join(outputDir, "files.json"))) { console.error("WARNING: files.json was not created"); process.exit(7); }

function countFiles(dir: string): number {
  let n = 0;
  try { for (const e of readdirSync(dir, { withFileTypes: true })) n += e.isFile() ? 1 : countFiles(join(dir, e.name)); } catch {}
  return n;
}

console.log("\n=== Done ===");
console.log(`Files manifest: ${outputDir}/files.json`);
console.log(`Downloads:      ${outputDir}/downloads/ (${countFiles(join(outputDir, "downloads"))} files)`);
if (existsSync(join(outputDir, "ehi-export-report.md"))) console.log(`Report:         ${outputDir}/ehi-export-report.md`);

if (snapshot) {
  console.log("\n=== SingleFile Snapshots ===");
  const snapResult = await snapshotHtmlFiles(outputDir);
  console.log(`Snapshots: created=${snapResult.created} skipped=${snapResult.skipped} failed=${snapResult.failed}`);
}

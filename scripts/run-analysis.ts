#!/usr/bin/env bun
// Run EHI export analysis on a single vendor's collected results.
//
// Usage:
//   bun run scripts/run-analysis.ts --dir <slug> [--results-dir <path>] [--output-dir <dir>] [--focus <text>] [--backend <b>] [--model <m>]

import { existsSync, lstatSync, mkdirSync, readdirSync, readFileSync, writeFileSync, symlinkSync } from "node:fs";
import { join, dirname } from "node:path";
import { defaultModel, runLLM, type Backend } from "../wiggum/llm-runner";
import { renderTemplate } from "../wiggum/template";

const ROOT_DIR = join(dirname(import.meta.path), "..");

function usage(): never {
  console.log(`Usage:
  bun run scripts/run-analysis.ts --dir <slug> [options]

Options:
  --dir          Abstraction slug (required, e.g. "vendor--product")
  --results-dir  Results directory path (default: results/<dir>)
  --output-dir   Output directory (default: abstraction/<dir>)
  --focus        Focusing prompt snippet appended to the analysis prompt
  --backend      LLM backend: claude, copilot, codex (default: copilot)
  --model        Model override
  -h, --help     Show this message

Examples:
  bun run scripts/run-analysis.ts --dir aarista-technology-llc--aarista
  bun run scripts/run-analysis.ts --dir meditech--config-1 --results-dir results/meditech--meditech-ehr --focus "Focus on Config 1..."
  bun run scripts/run-analysis.ts --dir practice-fusion--practice-fusion-ehr --backend claude`);
  process.exit(0);
}

function isBackend(value: string): value is Backend {
  return value === "claude" || value === "copilot" || value === "codex" || value === "gemini" || value === "shelley";
}

let targetDirname = "";
let resultsDirArg = "";
let outputDir = "";
let focus = "";
let backend: Backend = "copilot";
let model = "";

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--dir":
      targetDirname = args[++i];
      break;
    case "--results-dir":
      resultsDirArg = args[++i];
      break;
    case "--output-dir":
      outputDir = args[++i];
      break;
    case "--focus":
      focus = args[++i];
      break;
    case "--backend":
      backend = args[++i];
      if (!isBackend(backend)) {
        console.error(`Unknown backend: ${backend}`);
        usage();
      }
      break;
    case "--model":
      model = args[++i];
      break;
    case "-h":
    case "--help":
      usage();
    default:
      console.error(`Unknown arg: ${args[i]}`);
      usage();
  }
}

if (!targetDirname) {
  console.error("Missing required --dir argument.");
  usage();
}

if (!model) model = defaultModel(backend);

const outputPath = outputDir || join(ROOT_DIR, "abstraction", targetDirname);
const resultsDir = resultsDirArg
  ? (resultsDirArg.startsWith("/") ? resultsDirArg : join(ROOT_DIR, resultsDirArg))
  : join(ROOT_DIR, "results", targetDirname);
const metadataPath = join(resultsDir, "chpl-metadata.json");

if (!existsSync(resultsDir)) {
  console.error(`Results folder not found: ${resultsDir}`);
  process.exit(2);
}
if (!existsSync(metadataPath)) {
  console.error(`chpl-metadata.json not found in ${resultsDir}`);
  process.exit(2);
}

const metadata = await Bun.file(metadataPath).json();
const productName = metadata?.products?.[0]?.product_name || targetDirname;

mkdirSync(outputPath, { recursive: true });

function linkArtifact(filePath: string) {
  const linkName = join(outputPath, filePath.split("/").pop() as string);
  if (existsSync(linkName)) return;
  symlinkSync(filePath, linkName);
}

try {
  linkArtifact(join(resultsDir, "downloads"));
} catch {}

for (const entry of readdirSync(resultsDir, { withFileTypes: true })) {
  if (!entry.isFile()) continue;
  if (!entry.name.endsWith(".md") && !entry.name.endsWith(".json")) continue;
  try { linkArtifact(join(resultsDir, entry.name)); } catch {}
}

writeFileSync(
  join(outputPath, "metadata.json"),
  JSON.stringify({
    dir_slug: targetDirname,
    product_name: productName,
    results_dir: resultsDir.replace(ROOT_DIR + "/", ""),
    created_at: new Date().toISOString(),
    ehi_documentation_url: metadata.url ?? "",
    developer: metadata.developer ?? {},
    certified_products: metadata.products ?? [],
    ...(focus ? { split_focus: focus } : {}),
  }, null, 2),
);

let renderedPrompt = renderTemplate(
  join(ROOT_DIR, "abstraction/abstraction-prompt.md"),
  {
    RESULTS_DIR: resultsDir,
    OUTPUT_DIR: outputPath,
    PRODUCT_NAME: productName,
    EHI_SCOPE_REFERENCE: readFileSync(join(ROOT_DIR, "wiggum/prompts/ehi-scope-reference.md"), "utf8"),
  },
);

if (focus) {
  renderedPrompt += `\n\n## Analysis Focus\n\n${focus}`;
}

console.log("=== EHI Export Analysis ===");
console.log(`Target:  ${targetDirname}`);
console.log(`Product: ${productName}`);
console.log(`Results: ${resultsDir}`);
console.log(`Output:  ${outputPath}`);
if (focus) console.log(`Focus:   ${focus.slice(0, 120)}${focus.length > 120 ? "..." : ""}`);
console.log(`Backend: ${backend} (${model})`);
console.log(`Prompt:  ${Buffer.byteLength(renderedPrompt)} bytes`);
console.log("");

const exitCode = await runLLM(backend, {
  prompt: renderedPrompt,
  logFile: join(outputPath, "analysis-log.txt"),
  cwd: outputPath,
  model,
});

if (exitCode !== 0) {
  console.error(`${backend} exited with code ${exitCode}.`);
  process.exit(exitCode);
}

const analysisFile = join(outputPath, "analysis.md");
if (!existsSync(analysisFile)) {
  console.error(`WARNING: analysis.md was not created at ${analysisFile}`);
  console.error("The agent may have written to a different path.");
  process.exit(7);
}

console.log("");
console.log("=== Done ===");
console.log(`Analysis: ${analysisFile}`);
const analysisArtifacts = join(outputPath, "analysis");
if (existsSync(analysisArtifacts) && lstatSync(analysisArtifacts).isDirectory()) {
  console.log(`Scripts/data: ${analysisArtifacts} (${readdirSync(analysisArtifacts).length} files)`);
}

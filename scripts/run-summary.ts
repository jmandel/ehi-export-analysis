#!/usr/bin/env bun
// Extract structured JSON from a single vendor's analysis.md.
//
// Reads the TypeScript schema (abstraction/ehi-summary-schema.ts) and the
// vendor's analysis.md, then invokes an LLM to produce a conforming JSON file.
// The script is schema-agnostic — all field semantics live in the .ts comments.
//
// Usage:
//   bun run scripts/run-summary.ts --analysis-dir <dir> [options]

import { readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { defaultModel, runLLM, type Backend } from "../wiggum/llm-runner";
import { renderFeedbackSection } from "./feedback";

const ROOT_DIR = join(dirname(import.meta.path), "..");

function usage(): never {
  console.log(`Usage:
  bun run scripts/run-summary.ts --analysis-dir <dir> [options]

Options:
  --analysis-dir  Path to abstraction/<vendor>--<product>/ directory (required)
  --backend       LLM backend: claude, copilot, codex (default: copilot)
  --model         Model override
  -h, --help      Show this message
`);
  process.exit(0);
}

function isBackend(value: string): value is Backend {
  return value === "claude" || value === "copilot" || value === "codex" || value === "gemini" || value === "shelley";
}

let analysisDir = "";
let backend: Backend = "copilot";
let model = "";

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--analysis-dir":
      analysisDir = args[++i];
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

if (!analysisDir) {
  console.error("Missing required --analysis-dir argument.");
  usage();
}

const resolvedAnalysisDir = analysisDir.startsWith("/") ? analysisDir : join(process.cwd(), analysisDir);
if (!existsSync(resolvedAnalysisDir)) {
  console.error(`Analysis folder not found: ${resolvedAnalysisDir}`);
  process.exit(2);
}

const analysisFile = join(resolvedAnalysisDir, "analysis.md");
if (!existsSync(analysisFile)) {
  console.error(`No analysis.md found in ${resolvedAnalysisDir}`);
  process.exit(2);
}

const schemaFile = join(ROOT_DIR, "abstraction/ehi-summary-schema.ts");
if (!existsSync(schemaFile)) {
  console.error(`Schema file not found: ${schemaFile}`);
  process.exit(2);
}

if (!model) model = defaultModel(backend);

const schemaContent = readFileSync(schemaFile, "utf8");
const analysisContent = readFileSync(analysisFile, "utf8");
const vendorSlug = resolvedAnalysisDir.split("/").pop()!;
const outputFile = join(resolvedAnalysisDir, "summary.json");

const prompt = [
  "You are extracting structured data from an EHI export analysis document.",
  "",
  "## Your task",
  "",
  "Read the TypeScript interface below. It defines the exact JSON structure you must produce.",
  "Every field has detailed JSDoc comments explaining how to derive its value from the analysis.",
  "Follow those instructions precisely.",
  "",
  "Read the analysis document below. Extract the required data and write a single JSON file",
  `to: \`${outputFile}\``,
  "",
  `The JSON must conform to the TypeScript interface. Use the vendor slug \`${vendorSlug}\` for`,
  "the vendor_slug field.",
  "",
  "## TypeScript Schema",
  "",
  "```typescript",
  schemaContent,
  "```",
  "",
  "## Analysis Document",
  "",
  analysisContent,
  "",
  "## Output instructions",
  "",
  "1. Write ONLY the JSON file to `summary.json`. Do not create any other files.",
  "2. The JSON must be valid, properly formatted, and match the TypeScript interface exactly.",
  "3. Do not include any fields not in the interface.",
  "4. Do not wrap the JSON in markdown code fences — write raw JSON to the file.",
  "5. If the analysis does not contain enough information to confidently score a field,",
  "   use your best judgment based on what IS available. Never leave a field null.",
  "",
].join("\n") + renderFeedbackSection(vendorSlug, "summary");

console.log("=== EHI Summary Extraction ===");
console.log(`Analysis: ${resolvedAnalysisDir}`);
console.log(`Schema:   ${schemaFile}`);
console.log(`Output:   ${outputFile}`);
console.log(`Backend:  ${backend} (${model})`);
console.log("");

const exitCode = await runLLM(backend, {
  prompt,
  logFile: join(resolvedAnalysisDir, "summary-log.txt"),
  cwd: ROOT_DIR,
  model,
});

if (exitCode !== 0) {
  console.error(`${backend} exited with code ${exitCode}.`);
  process.exit(exitCode);
}

if (!existsSync(outputFile)) {
  console.error(`WARNING: summary.json was not created at ${outputFile}`);
  process.exit(7);
}

try {
  const raw = readFileSync(outputFile, "utf8");
  JSON.parse(raw);
} catch {
  console.error("WARNING: summary.json is not valid JSON");
  process.exit(8);
}

console.log("");
console.log("=== Done ===");
console.log(`Summary: ${outputFile}`);

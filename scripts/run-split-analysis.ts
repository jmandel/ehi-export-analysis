#!/usr/bin/env bun
// Run split abstractions from a shared results directory.
//
// Usage:
//   bun run scripts/run-split-analysis.ts --split-config work/splits/meditech.json [--backend ...] [--model ...]

import { existsSync, mkdirSync, symlinkSync, lstatSync, unlinkSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { runLLM, defaultModel, type Backend } from "../wiggum/llm-runner";
import { renderTemplate } from "../wiggum/template";

const ROOT_DIR = join(dirname(import.meta.path), "..");

function usage(): never {
  console.log(`Usage:
  bun run scripts/run-split-analysis.ts --split-config <file> [options]

Options:
  --split-config  JSON file defining splits (required)
  --backend       LLM backend: claude, copilot, codex (default: copilot)
  --model         Model override
  --force         Remove existing analysis.md and re-run
  --dry-run       Print what would happen without executing
  -h, --help      Show this message

Examples:
  bun run scripts/run-split-analysis.ts --split-config work/splits/meditech.json
  bun run scripts/run-split-analysis.ts --split-config work/splits/meditech.json --force --backend claude`);
  process.exit(0);
}

let splitConfigPath = "";
let backend: Backend = "copilot";
let model = "";
let force = false;
let dryRun = false;

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--split-config": splitConfigPath = args[++i]; break;
    case "--backend":      backend = args[++i] as Backend; break;
    case "--model":        model = args[++i]; break;
    case "--force":        force = true; break;
    case "--dry-run":      dryRun = true; break;
    case "-h": case "--help": usage();
    default: console.error(`Unknown arg: ${args[i]}`); usage();
  }
}

if (!splitConfigPath) { console.error("Missing required --split-config argument."); usage(); }
if (!existsSync(splitConfigPath)) { console.error(`Split config not found: ${splitConfigPath}`); process.exit(2); }
if (!model) model = defaultModel(backend);

const splitConfig = JSON.parse(readFileSync(splitConfigPath, "utf8"));
const sourceDir: string = splitConfig.source_dir;
const sourcePath = join(ROOT_DIR, "results", sourceDir);
const splits: any[] = splitConfig.splits;

if (!existsSync(sourcePath)) { console.error(`Source results directory not found: ${sourcePath}`); process.exit(2); }

console.log("=== Split Analysis ===");
console.log(`Source:  ${sourceDir}`);
console.log(`Splits:  ${splits.length}`);
console.log(`Backend: ${backend} (${model})`);
console.log("");

for (let i = 0; i < splits.length; i++) {
  const split = splits[i];
  const slug: string = split.slug;
  const focus: string = split.focus;
  const products: string = split.products.join(", ");
  const artifacts: string = (split.relevant_artifacts ?? []).join(", ");
  const splitOutput = join(ROOT_DIR, "abstraction", slug);

  console.log(`--- Split ${i + 1}/${splits.length}: ${slug} ---`);
  console.log(`  Focus:    ${focus}`);
  console.log(`  Products: ${products}`);
  if (artifacts) console.log(`  Key artifacts: ${artifacts}`);

  if (existsSync(join(splitOutput, "analysis.md")) && !force) {
    console.log("  SKIP: analysis.md already exists (use --force to redo)");
    console.log("");
    continue;
  }

  if (dryRun) {
    console.log(`  DRY RUN: would create ${splitOutput} and run analysis`);
    console.log("");
    continue;
  }

  if (force && existsSync(join(splitOutput, "analysis.md"))) {
    unlinkSync(join(splitOutput, "analysis.md"));
    try { Bun.spawnSync(["rm", "-rf", join(splitOutput, "analysis")]); } catch {}
  }

  mkdirSync(splitOutput, { recursive: true });

  // Symlink shared downloads and result artifacts
  const items = [join(sourcePath, "downloads")];
  try {
    for (const f of readdirSync(sourcePath)) {
      if (f.endsWith(".md") || f.endsWith(".json")) items.push(join(sourcePath, f));
    }
  } catch {}

  for (const item of items) {
    if (!existsSync(item)) continue;
    const linkname = join(splitOutput, item.split("/").pop()!);
    try { if (lstatSync(linkname).isSymbolicLink()) unlinkSync(linkname); } catch {}
    if (!existsSync(linkname)) {
      try { symlinkSync(item, linkname); } catch {}
    }
  }

  // Write split-specific metadata
  writeFileSync(join(splitOutput, "metadata.json"), JSON.stringify({
    dir_slug: slug,
    source_dir: `results/${sourceDir}`,
    split_focus: focus,
    split_products: products,
    created_at: new Date().toISOString(),
  }, null, 2));

  // Build prompt addendum
  let addendum = `\n\n## Split Analysis Context\n\nThis is a **split analysis**: the downloads/ directory contains documentation\nfor multiple product lines from the same vendor. Your analysis should focus\nspecifically on the following:\n\n**Focus**: ${focus}\n\n**Products to analyze**: ${products}`;

  if (artifacts) {
    addendum += `\n\n**Most relevant artifacts in downloads/**: ${artifacts}\nOther artifacts in downloads/ may be for other product lines — include them\nin your analysis only where they provide shared context (e.g., common export\ninfrastructure) but don't treat them as primary sources for this product line.`;
  }

  addendum += `\n\nWhen assessing coverage, evaluate against what these specific products store,\nnot the vendor's entire portfolio.`;

  // Render prompt
  const productName = products.split(",")[0].trim();
  const renderedPrompt = renderTemplate(
    join(ROOT_DIR, "abstraction/abstraction-prompt.md"),
    {
      RESULTS_DIR: sourcePath,
      OUTPUT_DIR: splitOutput,
      PRODUCT_NAME: productName,
      EHI_SCOPE_REFERENCE: readFileSync(join(ROOT_DIR, "wiggum/prompts/ehi-scope-reference.md"), "utf8"),
    },
  ) + addendum;

  console.log("  Running analysis...");

  const exitCode = await runLLM(backend, {
    prompt: renderedPrompt,
    logFile: join(splitOutput, "split-analysis-log.txt"),
    cwd: splitOutput,
    model,
  });

  if (exitCode !== 0) {
    console.log(`  FAILED: ${backend} exited with code ${exitCode}`);
    console.log("");
    continue;
  }

  if (!existsSync(join(splitOutput, "analysis.md"))) {
    console.log("  WARNING: analysis.md was not created");
  } else {
    console.log(`  Done: ${splitOutput}/analysis.md`);
  }
  console.log("");
}

console.log("=== Split Analysis Complete ===");

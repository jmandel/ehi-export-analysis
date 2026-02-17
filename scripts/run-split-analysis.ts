#!/usr/bin/env bun
// Run split abstractions from a shared results directory.
//
// For vendors like MEDITECH where one results dir covers multiple product lines,
// this script creates per-split abstraction directories with shared downloads
// and runs separate analyses for each.
//
// Usage:
//   bun run scripts/run-split-analysis.ts --split-config work/splits/meditech.json [--backend ...] [--model ...]

import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync, lstatSync, symlinkSync, unlinkSync, rmSync } from "node:fs";
import { join, dirname, basename } from "node:path";

const ROOT_DIR = join(dirname(import.meta.path), "..");

// ── CLI parsing ──────────────────────────────────────────────────────────────

function usage(): never {
  console.log(`Usage:
  bun run scripts/run-split-analysis.ts --split-config <file> [options]

Options:
  --split-config  JSON file defining splits (required)
  --backend       LLM backend: copilot, codex (default: copilot)
  --model         Model override (default: claude-opus-4.6-fast for copilot)
  --force         Remove existing analysis.md and re-run
  --dry-run       Print what would happen without executing
  -h, --help      Show this message

Split config format:
  {
    "source_dir": "vendor--product",
    "splits": [
      {
        "slug": "vendor--product-line-a",
        "focus": "Description of what to focus on",
        "products": ["Product A v1", "Product A v2"],
        "relevant_artifacts": ["config1.html", "data-dict.pdf"]
      }
    ]
  }

Examples:
  bun run scripts/run-split-analysis.ts --split-config work/splits/meditech.json
  bun run scripts/run-split-analysis.ts --split-config work/splits/meditech.json --force`);
  process.exit(0);
}

let splitConfigPath = "";
let backend = "copilot";
let model = "";
let force = false;
let dryRun = false;

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--split-config": splitConfigPath = args[++i]; break;
    case "--backend":      backend = args[++i]; break;
    case "--model":        model = args[++i]; break;
    case "--force":        force = true; break;
    case "--dry-run":      dryRun = true; break;
    case "-h": case "--help": usage();
    default:
      console.error(`Unknown arg: ${args[i]}`);
      usage();
  }
}

if (!splitConfigPath) {
  console.error("Missing required --split-config argument.");
  usage();
}

if (!existsSync(splitConfigPath)) {
  console.error(`Split config not found: ${splitConfigPath}`);
  process.exit(2);
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

// ── Parse split config ───────────────────────────────────────────────────────

const splitConfig = await Bun.file(splitConfigPath).json();
const sourceDir: string = splitConfig.source_dir;
const sourcePath = join(ROOT_DIR, "results", sourceDir);
const splits: any[] = splitConfig.splits;

if (!existsSync(sourcePath)) {
  console.error(`Source results directory not found: ${sourcePath}`);
  process.exit(2);
}

console.log("=== Split Analysis ===");
console.log(`Source:  ${sourceDir}`);
console.log(`Splits:  ${splits.length}`);
console.log(`Backend: ${backend} (${model})`);
console.log("");

// ── Helper: collect items to symlink ─────────────────────────────────────────

function collectSymlinkItems(srcPath: string): string[] {
  const items: string[] = [];
  const downloadsDir = join(srcPath, "downloads");
  if (existsSync(downloadsDir)) items.push(downloadsDir);
  try {
    for (const entry of readdirSync(srcPath)) {
      const full = join(srcPath, entry);
      if (entry.endsWith(".md") || entry.endsWith(".json")) {
        if (lstatSync(full).isFile()) items.push(full);
      }
    }
  } catch {}
  return items;
}

// ── Helper: stream a Bun.spawn process to stdout + log ───────────────────────

async function streamProc(proc: ReturnType<typeof Bun.spawn>, logFd: ReturnType<typeof Bun.file.prototype.writer>): Promise<void> {
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
}

// ── Process each split ───────────────────────────────────────────────────────

for (let i = 0; i < splits.length; i++) {
  const split = splits[i];
  const slug: string = split.slug;
  const focusText: string = split.focus;
  const splitProducts: string = (split.products ?? []).join(", ");
  const artifacts: string = (split.relevant_artifacts ?? []).join(", ");
  const splitOutput = join(ROOT_DIR, "abstraction", slug);

  console.log(`--- Split ${i + 1}/${splits.length}: ${slug} ---`);
  console.log(`  Focus:    ${focusText}`);
  console.log(`  Products: ${splitProducts}`);
  if (artifacts) console.log(`  Key artifacts: ${artifacts}`);

  // Skip if already done (unless --force)
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

  // Remove old analysis if forcing
  if (force && existsSync(join(splitOutput, "analysis.md"))) {
    unlinkSync(join(splitOutput, "analysis.md"));
    const analysisDir = join(splitOutput, "analysis");
    if (existsSync(analysisDir)) rmSync(analysisDir, { recursive: true });
  }

  // Create split output dir
  mkdirSync(splitOutput, { recursive: true });

  // Symlink shared downloads and result artifacts
  for (const item of collectSymlinkItems(sourcePath)) {
    const linkname = join(splitOutput, basename(item));
    // Remove stale symlinks, but don't overwrite real files
    try {
      if (lstatSync(linkname).isSymbolicLink()) unlinkSync(linkname);
    } catch {}
    if (!existsSync(linkname)) {
      symlinkSync(item, linkname);
    }
  }

  // Write split-specific metadata
  const splitMeta = {
    dir_slug: slug,
    source_dir: `results/${sourceDir}`,
    split_focus: focusText,
    split_products: splitProducts,
    created_at: new Date().toISOString(),
  };
  writeFileSync(join(splitOutput, "metadata.json"), JSON.stringify(splitMeta, null, 2) + "\n");

  // Build the prompt addendum for this split
  let addendum = `

## Split Analysis Context

This is a **split analysis**: the downloads/ directory contains documentation
for multiple product lines from the same vendor. Your analysis should focus
specifically on the following:

**Focus**: ${focusText}

**Products to analyze**: ${splitProducts}`;

  if (artifacts) {
    addendum += `

**Most relevant artifacts in downloads/**: ${artifacts}
Other artifacts in downloads/ may be for other product lines — include them
in your analysis only where they provide shared context (e.g., common export
infrastructure) but don't treat them as primary sources for this product line.`;
  }

  addendum += `

When assessing coverage, evaluate against what these specific products store,
not the vendor's entire portfolio.`;

  // Render the prompt
  const productName = splitProducts.split(",")[0].trim();
  const abstractionPromptPath = join(ROOT_DIR, "abstraction/abstraction-prompt.md");
  const ehiScopePath = join(ROOT_DIR, "wiggum/prompts/ehi-scope-reference.md");

  let promptTmpl = readFileSync(abstractionPromptPath, "utf8");
  const promptVars: Record<string, string> = {
    RESULTS_DIR: sourcePath,
    OUTPUT_DIR: splitOutput,
    PRODUCT_NAME: productName,
    EHI_SCOPE_REFERENCE: readFileSync(ehiScopePath, "utf8"),
  };
  promptTmpl = promptTmpl.replace(/\{\{(\w+)\}\}/g, (_, k) => promptVars[k] ?? `{{${k}}}`);
  promptTmpl += addendum;

  const renderedPrompt = promptTmpl;

  console.log("  Running analysis...");

  const logFile = join(splitOutput, "split-analysis-log.txt");
  const logFd = Bun.file(logFile).writer();

  let exitCode: number;

  if (backend === "copilot") {
    const proc = Bun.spawn(
      ["copilot", "-p", renderedPrompt, "--model", model,
       "--yolo", "--no-ask-user", "--no-color", "--no-auto-update"],
      {
        cwd: splitOutput,
        stdout: "pipe",
        stderr: "pipe",
      },
    );
    await streamProc(proc, logFd);
    exitCode = await proc.exited;
  } else if (backend === "codex") {
    const tmpFile = join(splitOutput, ".prompt-tmp.md");
    writeFileSync(tmpFile, renderedPrompt);

    const proc = Bun.spawn(
      ["codex", "exec", "--full-auto", "--sandbox", "danger-full-access",
       "--model", model, "-"],
      {
        cwd: splitOutput,
        stdin: Bun.file(tmpFile),
        stdout: "pipe",
        stderr: "pipe",
      },
    );
    await streamProc(proc, logFd);
    exitCode = await proc.exited;
    try { unlinkSync(tmpFile); } catch {}
  } else {
    console.error(`Unknown backend: ${backend}`);
    process.exit(1);
  }

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

#!/usr/bin/env bun
// Run a fixup agent to diagnose, repair, and cascade EHI export pipeline results.
//
// The fixup agent is autonomous: it reads the issue, determines which pipeline
// stage to intervene at, makes the surgical fix, then runs the downstream
// scripts to cascade the correction through the rest of the pipeline.
//
// Usage:
//   bun run scripts/run-fixup.ts --dir <slug> --issue <N>
//   bun run scripts/run-fixup.ts --dir <slug> --hint "description of what to fix"

import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";

const ROOT_DIR = join(dirname(import.meta.path), "..");

// ── CLI parsing ──────────────────────────────────────────────────────────────

function usage(): never {
  console.log(`Usage:
  bun run scripts/run-fixup.ts --dir <results-dir-name> [options]

Options:
  --dir        Directory name under results/ (required)
  --issue <N>  GitHub issue number to read fixup instructions from
  --hint "..." Inline fixup hint (alternative to --issue)
  --backend    LLM backend: copilot, codex (default: copilot)
  --model      Model override (default: claude-opus-4.6-fast for copilot)
  -h, --help   Show this message

The agent autonomously determines which stage to fix and cascades downstream.

Examples:
  bun run scripts/run-fixup.ts --dir ezemrx-inc--ezemrx --issue 1
  bun run scripts/run-fixup.ts --dir ezemrx-inc--ezemrx --hint "Missed PDF embedded in viewer widget"`);
  process.exit(0);
}

let targetDirname = "";
let issueNum = "";
let hint = "";
let backend = "copilot";
let model = "";

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--dir":        targetDirname = args[++i]; break;
    case "--issue":      issueNum = args[++i]; break;
    case "--hint":       hint = args[++i]; break;
    case "--backend":    backend = args[++i]; break;
    case "--model":      model = args[++i]; break;
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

if (!issueNum && !hint) {
  console.error('Must provide either --issue <N> or --hint "text".');
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
  process.exit(2);
}

// ── Get fixup hint ───────────────────────────────────────────────────────────

let fixupHint = "";

if (issueNum) {
  console.log(`Fetching issue #${issueNum}...`);

  // Determine repo from git remote
  const gitProc = Bun.spawnSync(
    ["git", "-C", ROOT_DIR, "remote", "get-url", "origin"],
    { stdout: "pipe", stderr: "pipe" },
  );
  const remoteUrl = new TextDecoder().decode(gitProc.stdout).trim();
  const repoMatch = remoteUrl.match(/github\.com[:/](.+?)(?:\.git)?$/);
  const repo = repoMatch ? repoMatch[1] : "";

  const ghProc = Bun.spawnSync(
    ["gh", "issue", "view", issueNum, "--repo", repo, "--json", "title,body"],
    { stdout: "pipe", stderr: "pipe" },
  );

  const ghOut = new TextDecoder().decode(ghProc.stdout).trim();
  if (!ghOut) {
    console.error(`Failed to fetch issue #${issueNum}. Provide --hint instead.`);
    process.exit(4);
  }

  const issueJson = JSON.parse(ghOut);
  fixupHint = `GitHub Issue #${issueNum}: ${issueJson.title}\n\n${issueJson.body}`;
} else {
  fixupHint = hint;
}

// ── Extract template variables ───────────────────────────────────────────────

const metadataPath = join(outputDir, "chpl-metadata.json");
let url = "", developers = "", products = "";
if (existsSync(metadataPath)) {
  const metadata = await Bun.file(metadataPath).json();
  url = metadata.url ?? "";
  developers = [metadata.developer?.name].filter(Boolean).join(", ");
  products = (metadata.products ?? []).map((p: any) => p.product_name).filter(Boolean).join(", ");
}

// ── Render prompt template ───────────────────────────────────────────────────

const promptTemplate = join(ROOT_DIR, "wiggum/prompts/fixup.md");
const promptsDir = join(ROOT_DIR, "wiggum/prompts");

let tmpl = readFileSync(promptTemplate, "utf8");

const vars: Record<string, string> = {
  URL: url,
  DEVELOPERS: developers,
  PRODUCTS: products,
  OUTPUT_DIR: outputDir,
  FIXUP_HINT: fixupHint,
  ROOT_DIR: ROOT_DIR,
  DIR_SLUG: targetDirname,
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

console.log("=== Fixup Agent ===");
console.log(`Target:     ${targetDirname}`);
console.log(`Developer:  ${developers}`);
console.log(`Issue:      ${issueNum || "inline hint"}`);
console.log(`Hint:       ${fixupHint.split("\n")[0]}`);
console.log(`Output:     ${outputDir}`);
console.log(`Backend:    ${backend} (${model})`);
console.log("");
console.log("The agent will diagnose, fix, and cascade downstream stages autonomously.");
console.log("");

// ── Log file ─────────────────────────────────────────────────────────────────

const logFile = join(outputDir, "fixup-log.txt");
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

console.log("");
console.log("=== Fixup Agent Complete ===");
if (existsSync(join(outputDir, "fixup-log.md"))) {
  console.log(`Fixup log: ${outputDir}/fixup-log.md`);
}

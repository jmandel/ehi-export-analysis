#!/usr/bin/env bun
// Run a fixup agent to diagnose, repair, and cascade EHI export pipeline results.
//
// Usage:
//   bun run scripts/run-fixup.ts --dir <slug> --issue <N>
//   bun run scripts/run-fixup.ts --dir <slug> --hint "description of what to fix"

import { existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { runLLM, defaultModel, type Backend } from "../wiggum/llm-runner";
import { renderTemplate } from "../wiggum/template";

const ROOT_DIR = join(dirname(import.meta.path), "..");

function usage(): never {
  console.log(`Usage:
  bun run scripts/run-fixup.ts --dir <results-dir-name> [options]

Options:
  --dir        Directory name under results/ (required)
  --issue <N>  GitHub issue number to read fixup instructions from
  --hint "..." Inline fixup hint (alternative to --issue)
  --backend    LLM backend: claude, copilot, codex (default: copilot)
  --model      Model override
  -h, --help   Show this message

Examples:
  bun run scripts/run-fixup.ts --dir ezemrx-inc--ezemrx --issue 1
  bun run scripts/run-fixup.ts --dir ezemrx-inc--ezemrx --hint "Missed PDF embedded in viewer widget"`);
  process.exit(0);
}

let targetDirname = "";
let issueNum = "";
let hint = "";
let backend: Backend = "copilot";
let model = "";

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--dir":     targetDirname = args[++i]; break;
    case "--issue":   issueNum = args[++i]; break;
    case "--hint":    hint = args[++i]; break;
    case "--backend": backend = args[++i] as Backend; break;
    case "--model":   model = args[++i]; break;
    case "-h": case "--help": usage();
    default: console.error(`Unknown arg: ${args[i]}`); usage();
  }
}

if (!targetDirname) { console.error("Missing required --dir argument."); usage(); }
if (!issueNum && !hint) { console.error("Must provide either --issue <N> or --hint \"text\"."); usage(); }
if (!model) model = defaultModel(backend);

const outputDir = join(ROOT_DIR, "results", targetDirname);
if (!existsSync(outputDir)) { console.error(`Results folder not found: ${outputDir}`); process.exit(2); }

// Get fixup hint from GitHub issue or inline
let fixupHint = "";
if (issueNum) {
  console.log(`Fetching issue #${issueNum}...`);
  const repoUrl = Bun.spawnSync(["git", "-C", ROOT_DIR, "remote", "get-url", "origin"]).stdout.toString().trim();
  const repo = repoUrl.replace(/.*github\.com[:/]/, "").replace(/\.git$/, "");
  const result = Bun.spawnSync(["gh", "issue", "view", issueNum, "--repo", repo, "--json", "title,body"]);
  if (result.exitCode !== 0) { console.error(`Failed to fetch issue #${issueNum}.`); process.exit(4); }
  const issue = JSON.parse(result.stdout.toString());
  fixupHint = `GitHub Issue #${issueNum}: ${issue.title}\n\n${issue.body}`;
} else {
  fixupHint = hint;
}

const metadata = await Bun.file(join(outputDir, "chpl-metadata.json")).json();
const developers = [metadata.developer?.name].filter(Boolean).join(", ");
const products = (metadata.products ?? []).map((p: any) => p.product_name).filter(Boolean).join(", ");

const renderedPrompt = renderTemplate(
  join(ROOT_DIR, "wiggum/prompts/fixup.md"),
  {
    URL: metadata.url ?? "", DEVELOPERS: developers, PRODUCTS: products,
    OUTPUT_DIR: outputDir, FIXUP_HINT: fixupHint,
    ROOT_DIR: ROOT_DIR, DIR_SLUG: targetDirname,
  },
  join(ROOT_DIR, "wiggum/prompts"),
);

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

const exitCode = await runLLM(backend, {
  prompt: renderedPrompt,
  logFile: join(outputDir, "fixup-log.txt"),
  cwd: ROOT_DIR,
  model,
});

if (exitCode !== 0) { console.error(`${backend} exited with code ${exitCode}.`); process.exit(exitCode); }

console.log("\n=== Fixup Agent Complete ===");
if (existsSync(join(outputDir, "fixup-log.md"))) console.log(`Fixup log: ${outputDir}/fixup-log.md`);

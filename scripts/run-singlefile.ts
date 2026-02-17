#!/usr/bin/env bun
// Create SingleFile snapshots of HTML files in a results directory.
//
// For each HTML file listed in files.json that has a source_url, runs SingleFile
// to produce a self-contained .singlefile.html alongside it, then updates the
// files.json manifest with the new entries.
//
// Usage:
//   bun run scripts/run-singlefile.ts --dir <results-dir-name>
//   bun run scripts/run-singlefile.ts --dir vendor--product --force

import { join, dirname } from "node:path";
import { snapshotHtmlFiles } from "./singlefile";

const ROOT_DIR = join(dirname(import.meta.path), "..");

function usage(): never {
  console.log(`Usage:
  bun run scripts/run-singlefile.ts --dir <results-dir-name> [options]

Options:
  --dir              Directory name under results/ (required)
  --per-dir N        Max snapshots per directory (default: 3)
  --all              No per-directory cap (snapshot everything)
  --browser-server U Connect to existing Chrome at URL (e.g. http://localhost:9222)
  --force            Re-snapshot even if .singlefile.html already exists
  -h, --help         Show this message

Examples:
  bun run scripts/run-singlefile.ts --dir 1life-healthcare-inc--1life
  bun run scripts/run-singlefile.ts --dir adaptamed-llc--ehr-your-way --force
  bun run scripts/run-singlefile.ts --dir eclinicalworks-llc--eclinicalworks --all`);
  process.exit(0);
}

let targetDirname = "";
let force = false;
let perDir: number | undefined;
let browserServer: string | undefined;

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--dir":            targetDirname = args[++i]; break;
    case "--per-dir":        perDir = parseInt(args[++i]); break;
    case "--all":            perDir = Infinity; break;
    case "--browser-server": browserServer = args[++i]; break;
    case "--force":          force = true; break;
    case "-h": case "--help": usage();
    default: console.error(`Unknown arg: ${args[i]}`); usage();
  }
}

if (!targetDirname) { console.error("Missing required --dir argument."); usage(); }

const resultsDir = join(ROOT_DIR, "results", targetDirname);

console.log("=== SingleFile Snapshots ===");
console.log(`Target: ${targetDirname}`);
console.log("");

const result = await snapshotHtmlFiles(resultsDir, { force, perDir, browserServer });

console.log(`\n=== Done ===`);
console.log(`Created: ${result.created}  Skipped: ${result.skipped}  Failed: ${result.failed}`);

if (result.failed > 0) process.exit(1);

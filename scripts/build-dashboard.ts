#!/usr/bin/env bun
// Build the static dashboard data directory.
//
// Merges summary.json + metadata.json for each vendor into vendors.json,
// copies all artifacts (analyses, research, reports, downloads, scripts)
// into static/data/ for a self-contained archive.
//
// Usage:
//   bun run scripts/build-dashboard.ts

import { join, dirname, basename } from "node:path";
import { mkdirSync, existsSync, readdirSync, cpSync } from "node:fs";

const ROOT = join(dirname(new URL(import.meta.url).pathname), "..");
const ABSTRACTION = join(ROOT, "abstraction");
const RESULTS = join(ROOT, "results");
const STATIC = join(ROOT, "static");
const DATA = join(STATIC, "data");

interface Vendor {
  slug: string;
  developer: string;
  family: string;
  product_name: string;
  summary: string;
  holistic_score: number;
  chpl_ids: number[];
  has_analysis: boolean;
  has_research: boolean;
  has_report: boolean;
  analysis_files: string[];
  download_files: string[];
}

// Ensure output dirs
for (const d of ["analyses", "research", "reports", "downloads", "analysis-scripts"]) {
  mkdirSync(join(DATA, d), { recursive: true });
}

const vendors: Vendor[] = [];

// Find all abstraction dirs with summary.json
const absDirs = readdirSync(ABSTRACTION).filter((d) => {
  return d.includes("--") && existsSync(join(ABSTRACTION, d, "summary.json"));
});

for (const slug of absDirs) {
  const absDir = join(ABSTRACTION, slug);
  const resDir = join(RESULTS, slug);

  // Read summary
  const summary = await Bun.file(join(absDir, "summary.json")).json();

  // Read metadata (may not exist)
  let developer = "";
  let family = "";
  let chplIds: number[] = [];
  const metaPath = join(absDir, "metadata.json");
  if (existsSync(metaPath)) {
    const meta = await Bun.file(metaPath).json();
    developer = meta.developer?.name ?? meta.vendor_slug ?? "";
    family = meta.product_name ?? slug.split("--")[1] ?? "";
    chplIds = (meta.certified_products ?? []).map((p: any) => p.chpl_id);
  } else {
    // Derive from slug
    const parts = slug.split("--");
    developer = parts[0].replace(/-/g, " ");
    family = (parts[1] ?? "").replace(/-/g, " ");
  }

  // Check for files
  const hasAnalysis = existsSync(join(absDir, "analysis.md"));
  const hasResearch = existsSync(join(resDir, "product-research.md"));
  const hasReport = existsSync(join(resDir, "ehi-export-report.md"));

  // Copy analysis.md
  if (hasAnalysis) {
    cpSync(join(absDir, "analysis.md"), join(DATA, "analyses", `${slug}.md`));
  }

  // Copy product-research.md
  if (hasResearch) {
    cpSync(
      join(resDir, "product-research.md"),
      join(DATA, "research", `${slug}.md`),
    );
  }

  // Copy ehi-export-report.md
  if (hasReport) {
    cpSync(
      join(resDir, "ehi-export-report.md"),
      join(DATA, "reports", `${slug}.md`),
    );
  }

  // Copy downloads
  let downloadFiles: string[] = [];
  const dlDir = join(resDir, "downloads");
  if (existsSync(dlDir)) {
    const destDl = join(DATA, "downloads", slug);
    mkdirSync(destDl, { recursive: true });
    cpSync(dlDir, destDl, { recursive: true });
    downloadFiles = readdirSync(dlDir).filter(
      (f) => !f.startsWith("."),
    );
  }

  // Copy analysis scripts
  let analysisFiles: string[] = [];
  const scriptDir = join(absDir, "analysis");
  if (existsSync(scriptDir)) {
    const destScripts = join(DATA, "analysis-scripts", slug);
    mkdirSync(destScripts, { recursive: true });
    cpSync(scriptDir, destScripts, { recursive: true });
    analysisFiles = readdirSync(scriptDir).filter(
      (f) => !f.startsWith("."),
    );
  }

  vendors.push({
    slug,
    developer,
    family,
    product_name: summary.product_name ?? "",
    summary: summary.summary ?? "",
    holistic_score: summary.holistic_score ?? 0,
    chpl_ids: chplIds,
    has_analysis: hasAnalysis,
    has_research: hasResearch,
    has_report: hasReport,
    analysis_files: analysisFiles,
    download_files: downloadFiles,
  });
}

// Sort by score ascending
vendors.sort((a, b) => a.holistic_score - b.holistic_score);

await Bun.write(join(DATA, "vendors.json"), JSON.stringify(vendors, null, 2));

console.log(`Dashboard data built: ${vendors.length} vendors`);
console.log(`  Analyses: ${vendors.filter((v) => v.has_analysis).length}`);
console.log(`  Research: ${vendors.filter((v) => v.has_research).length}`);
console.log(`  Reports:  ${vendors.filter((v) => v.has_report).length}`);
console.log(`Output: ${DATA}/`);

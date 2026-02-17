#!/usr/bin/env bun
// Build the dashboard data directory.
//
// Merges summary.json + metadata.json for each vendor into vendors.json,
// copies all artifacts (analyses, research, reports, downloads, scripts)
// into dist/data/ for a self-contained archive.
//
// Usage:
//   bun run build-data.ts

import { join, dirname } from "node:path";
import { mkdirSync, existsSync, readdirSync, cpSync } from "node:fs";

const DASHBOARD = dirname(new URL(import.meta.url).pathname);
const ROOT = join(DASHBOARD, "..");
const ABSTRACTION = join(ROOT, "abstraction");
const RESULTS = join(ROOT, "results");
const DIST = join(DASHBOARD, "dist");
const DATA = join(DIST, "data");

interface Vendor {
  slug: string;
  developer: string;
  family: string;
  product_name: string;
  summary: string;
  grade: string;
  coverage: string;
  approach: string;
  export_formats: string[];
  entity_count: number | null;
  field_count: number | null;
  has_data_dictionary: boolean;
  has_sample_data: boolean;
  billing_included: boolean | null;
  patient_communications: string;
  chpl_ids: number[];
  ehi_documentation_url: string;
  has_analysis: boolean;
  has_research: boolean;
  has_report: boolean;
  has_entity_inventory: boolean;
  has_analysis_stats: boolean;
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

  // Read summary
  const summary = await Bun.file(join(absDir, "summary.json")).json();

  // Read metadata (may not exist)
  let developer = "";
  let family = "";
  let chplIds: number[] = [];
  let ehiDocUrl = "";
  let resultsDir = join(RESULTS, slug);
  const metaPath = join(absDir, "metadata.json");
  if (existsSync(metaPath)) {
    const meta = await Bun.file(metaPath).json();
    developer = meta.developer?.name ?? meta.vendor_slug ?? "";
    family = meta.product_name ?? slug.split("--")[1] ?? "";
    chplIds = (meta.certified_products ?? []).map((p: any) => p.chpl_id);
    ehiDocUrl = meta.ehi_documentation_url ?? "";
    if (meta.results_dir) {
      resultsDir = join(ROOT, meta.results_dir);
    }
  } else {
    // Derive from slug
    const parts = slug.split("--");
    developer = parts[0].replace(/-/g, " ");
    family = (parts[1] ?? "").replace(/-/g, " ");
  }

  // Check for files
  const hasAnalysis = existsSync(join(absDir, "analysis.md"));
  const hasResearch = existsSync(join(resultsDir, "product-research.md"));
  const hasReport = existsSync(join(resultsDir, "ehi-export-report.md"));

  // Copy analysis.md
  if (hasAnalysis) {
    cpSync(join(absDir, "analysis.md"), join(DATA, "analyses", `${slug}.md`));
  }

  // Copy product-research.md
  if (hasResearch) {
    cpSync(
      join(resultsDir, "product-research.md"),
      join(DATA, "research", `${slug}.md`),
    );
  }

  // Copy ehi-export-report.md
  if (hasReport) {
    cpSync(
      join(resultsDir, "ehi-export-report.md"),
      join(DATA, "reports", `${slug}.md`),
    );
  }

  // Copy downloads
  let downloadFiles: string[] = [];
  const dlDir = join(resultsDir, "downloads");
  if (existsSync(dlDir)) {
    const destDl = join(DATA, "downloads", slug);
    mkdirSync(destDl, { recursive: true });
    cpSync(dlDir, destDl, { recursive: true });
    downloadFiles = readdirSync(dlDir).filter(
      (f) => !f.startsWith("."),
    );
  }

  // Copy analysis scripts (exclude build artifacts)
  const ANALYSIS_EXCLUDE = new Set(["node_modules", "bun.lock", "package.json", "tsconfig.json", "CLAUDE.md"]);
  let analysisFiles: string[] = [];
  const scriptDir = join(absDir, "analysis");
  if (existsSync(scriptDir)) {
    const destScripts = join(DATA, "analysis-scripts", slug);
    mkdirSync(destScripts, { recursive: true });
    cpSync(scriptDir, destScripts, {
      recursive: true,
      filter: (src) => !ANALYSIS_EXCLUDE.has(src.split("/").pop()!),
    });
    analysisFiles = readdirSync(scriptDir).filter(
      (f) => !f.startsWith(".") && !ANALYSIS_EXCLUDE.has(f),
    );
  }

  // Check for entity inventory and stats in analysis dir
  const hasEntityInventory = existsSync(join(absDir, "analysis", "entity-inventory-full.json"));
  const hasAnalysisStats = existsSync(join(absDir, "analysis", "analysis-stats.json"));

  vendors.push({
    slug,
    developer,
    family,
    product_name: summary.product_name ?? "",
    summary: summary.summary ?? "",
    grade: summary.grade ?? "F",
    coverage: summary.coverage ?? "",
    approach: summary.approach ?? "",
    export_formats: summary.export_formats ?? [],
    entity_count: summary.entity_count ?? null,
    field_count: summary.field_count ?? null,
    has_data_dictionary: summary.has_data_dictionary ?? false,
    has_sample_data: summary.has_sample_data ?? false,
    billing_included: summary.billing_included ?? null,
    patient_communications: summary.patient_communications ?? "",
    chpl_ids: chplIds,
    ehi_documentation_url: ehiDocUrl,
    has_analysis: hasAnalysis,
    has_research: hasResearch,
    has_report: hasReport,
    has_entity_inventory: hasEntityInventory,
    has_analysis_stats: hasAnalysisStats,
    analysis_files: analysisFiles,
    download_files: downloadFiles,
  });
}

// Sort by grade (A first)
const GRADE_ORDER = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"];
vendors.sort((a, b) => {
  const ai = GRADE_ORDER.indexOf(a.grade);
  const bi = GRADE_ORDER.indexOf(b.grade);
  return (ai >= 0 ? ai : GRADE_ORDER.length) - (bi >= 0 ? bi : GRADE_ORDER.length);
});

await Bun.write(join(DATA, "vendors.json"), JSON.stringify(vendors, null, 2));

// Build file index for in-app folder viewer — recursive nested representation
import { statSync } from "fs";
interface DirEntry { name: string; type: "file" | "dir"; children?: DirEntry[]; }
function buildTree(dir: string): DirEntry[] {
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter(f => !f.startsWith(".")).map(f => {
    const full = join(dir, f);
    const isDir = statSync(full).isDirectory();
    return isDir
      ? { name: f, type: "dir" as const, children: buildTree(full) }
      : { name: f, type: "file" as const };
  });
}
const fileIndex: Record<string, { downloads: DirEntry[]; analysis: DirEntry[] }> = {};
for (const v of vendors) {
  fileIndex[v.slug] = {
    downloads: buildTree(join(DATA, "downloads", v.slug)),
    analysis: buildTree(join(DATA, "analysis-scripts", v.slug)),
  };
}
await Bun.write(join(DATA, "file-index.json"), JSON.stringify(fileIndex));

console.log(`Dashboard data built: ${vendors.length} vendors`);
console.log(`  Analyses: ${vendors.filter((v) => v.has_analysis).length}`);
console.log(`  Research: ${vendors.filter((v) => v.has_research).length}`);
console.log(`  Reports:  ${vendors.filter((v) => v.has_report).length}`);
console.log(`Output: ${DATA}/`);

#!/usr/bin/env bun
// Build Phase 1 family targets using bottom-up methodology:
//
//   Step 1: Every CHPL product matching phase criteria starts as its own family
//   Step 2: Merge products with same (developer, product_name, url) — version dedup
//   Step 3: Apply merge rules from work/url-group-merges.json — content-verified merges
//
// Replaces the old product-families.json approach which was top-down and error-prone.
//
// Outputs:
//   work/family-targets.json              — all family targets
//   work/phases/phase-{N}-{slug}.json     — per-phase family target lists
//   work/phases/manifest.json             — phase summary
//
// Usage:
//   bun run scripts/build-phase-families.ts

import { join, dirname } from "node:path";
import { mkdirSync } from "node:fs";

const ROOT = join(dirname(new URL(import.meta.url).pathname), "..");

import { slugify } from "./naming.ts";

// ── Phase definitions ───────────────────────────────────────────────────────
const CPOE = new Set(["170.315 (a)(1)", "170.315 (a)(2)", "170.315 (a)(3)"]);
const G10 = new Set(["170.315 (g)(10)"]);

interface PhaseDef {
  phase: number;
  name: string;
  slug: string;
  description: string;
}

const PHASES: PhaseDef[] = [
  {
    phase: 1,
    name: "Comprehensive EHRs",
    slug: "comprehensive-ehrs",
    description:
      "CPOE + FHIR API (g)(10). Full-featured EHRs with order entry and standards-based API access.",
  },
  {
    phase: 2,
    name: "CPOE systems without FHIR API",
    slug: "cpoe-no-fhir",
    description:
      "CPOE certified but no (g)(10). EHRs with order entry but no standardized FHIR API.",
  },
  {
    phase: 3,
    name: "Other certified products",
    slug: "other",
    description:
      "Everything else: no CPOE. Patient portals, lab systems, specialty modules, minimal certifications.",
  },
];

function classifyPhase(criteria: string[]): number {
  const hasCpoe = criteria.some((c) => CPOE.has(c));
  const hasG10 = criteria.some((c) => G10.has(c));
  if (hasCpoe && hasG10) return 1;
  if (hasCpoe) return 2;
  return 3;
}

function classifyFamily(allCriteria: string[][]): number {
  const flat = allCriteria.flat();
  return classifyPhase(flat);
}

// ── Load data ───────────────────────────────────────────────────────────────

interface ChplListing {
  id: number;
  developer: { name: string };
  product: { name: string };
  version: { name: string };
  certificationDate: string;
  certificationResults: {
    success: boolean;
    exportDocumentation?: string;
    criterion: { number: string };
  }[];
}

interface MergeRule {
  developer: string;
  url: string;
  rationale: string;
  families: { name: string; products: string[] }[];
}

interface MergeFile {
  merges: MergeRule[];
  no_merge: { developer: string; url: string; products: string[] }[];
}

const listings: ChplListing[] = await Bun.file(
  join(ROOT, "chpl-data", "all-active-listings.json"),
).json();

const mergeFile: MergeFile = await Bun.file(
  join(ROOT, "work", "url-group-merges.json"),
).json();

// Also load targets.json for original_index mapping
interface UrlTarget {
  url: string;
  developers: string[];
  products: string[];
  chpl_ids: number[];
  original_index?: number;
  product_count: number;
}
const urlTargets: UrlTarget[] = await Bun.file(
  join(ROOT, "work", "targets.json"),
).json();

// Build URL → original_index map
const urlToOrigIndex = new Map<string, number>();
for (let i = 0; i < urlTargets.length; i++) {
  urlToOrigIndex.set(urlTargets[i].url, urlTargets[i].original_index ?? i);
}

// ── Step 1: Extract product records ─────────────────────────────────────────

interface ProductRecord {
  developer: string;
  product: string;
  version: string;
  chpl_id: number;
  certification_date: number;
  ehi_url: string | null;
  criteria: string[];
  phase: number;
}

const allProducts: ProductRecord[] = [];

for (const l of listings) {
  const criteria: string[] = [];
  let ehiUrl: string | null = null;

  for (const cr of l.certificationResults ?? []) {
    if (cr.success) {
      const num = cr.criterion?.number ?? "";
      criteria.push(num);
      if (num.includes("b)(10)") && cr.exportDocumentation) {
        ehiUrl = cr.exportDocumentation;
      }
    }
  }

  allProducts.push({
    developer: l.developer.name,
    product: l.product.name,
    version: l.version.name,
    chpl_id: l.id,
    certification_date: l.certificationDate ?? 0,
    ehi_url: ehiUrl,
    criteria,
    phase: classifyPhase(criteria),
  });
}

console.log(`Total CHPL listings: ${allProducts.length}`);

// ── Step 2: Version dedup — group by (developer, product, url) ──────────────

interface FamilyGroup {
  developer: string;
  familyName: string;
  url: string | null;
  products: ProductRecord[];
}

const step2Key = (p: ProductRecord) =>
  `${p.developer}\0${p.product}\0${p.ehi_url ?? ""}`;
const step2Map = new Map<string, ProductRecord[]>();

for (const p of allProducts) {
  const key = step2Key(p);
  if (!step2Map.has(key)) step2Map.set(key, []);
  step2Map.get(key)!.push(p);
}

let families: FamilyGroup[] = [];
for (const [, products] of step2Map) {
  families.push({
    developer: products[0].developer,
    familyName: products[0].product,
    url: products[0].ehi_url,
    products,
  });
}

console.log(`Step 2 (version dedup): ${families.length} families`);

// ── Step 3: Apply merge rules from url-group-merges.json ────────────────────

// Build merge lookup: (developer, product_name) → merged family name
const mergeMap = new Map<string, string>();
for (const rule of mergeFile.merges) {
  for (const fam of rule.families) {
    for (const prodName of fam.products) {
      mergeMap.set(`${rule.developer}\0${prodName}`, fam.name);
    }
  }
}

// Apply merges: group families by merged name
const mergedMap = new Map<string, FamilyGroup>();
for (const fam of families) {
  const mergeKey = `${fam.developer}\0${fam.familyName}`;
  const mergedName = mergeMap.get(mergeKey);

  if (mergedName) {
    const groupKey = `${fam.developer}\0${mergedName}`;
    if (!mergedMap.has(groupKey)) {
      mergedMap.set(groupKey, {
        developer: fam.developer,
        familyName: mergedName,
        url: fam.url,
        products: [],
      });
    }
    mergedMap.get(groupKey)!.products.push(...fam.products);
  } else {
    // No merge — keep as-is
    const key = `${fam.developer}\0${fam.familyName}\0${fam.url}`;
    mergedMap.set(key, fam);
  }
}

families = [...mergedMap.values()];
console.log(`Step 3 (content merges): ${families.length} families`);

// ── Build output ────────────────────────────────────────────────────────────

interface FamilyTarget {
  url: string;
  developers: string[];
  family: string;
  focus_product: string;
  focus_version: string;
  products: string[];
  chpl_ids: number[];
  original_index: number;
  product_count: number;
  phase: number;
}

const output: FamilyTarget[] = [];

for (const fam of families) {
  if (!fam.url) continue; // Skip products without EHI URL

  // Pick newest product as focus
  const sorted = [...fam.products].sort((a, b) =>
    (b.certification_date ?? 0) - (a.certification_date ?? 0),
  );
  const focus = sorted[0];

  const phase = classifyFamily(fam.products.map((p) => p.criteria));
  const origIdx = urlToOrigIndex.get(fam.url) ?? -1;

  output.push({
    url: fam.url,
    developers: [fam.developer],
    family: fam.familyName,
    focus_product: focus.product,
    focus_version: focus.version,
    products: [...new Set(fam.products.map((p) => p.product))],
    chpl_ids: fam.products.map((p) => p.chpl_id),
    original_index: origIdx,
    product_count: fam.products.length,
    phase,
  });
}

// Sort: big vendors first (by product count desc, then name).
// In --reverse mode this puts big vendors last.
output.sort((a, b) =>
  (b.chpl_ids.length - a.chpl_ids.length) ||
  a.developers[0].localeCompare(b.developers[0])
);

const outputPath = join(ROOT, "work", "family-targets.json");
await Bun.write(outputPath, JSON.stringify(output, null, 2));
console.log(`\nWrote ${output.length} family targets to ${outputPath}`);

// ── Write per-phase files ───────────────────────────────────────────────────
const phasesDir = join(ROOT, "work", "phases");
mkdirSync(phasesDir, { recursive: true });

const manifest: {
  phase: number;
  name: string;
  slug: string;
  file: string;
  description: string;
  family_count: number;
}[] = [];

for (const phaseDef of PHASES) {
  const phaseTargets = output.filter((t) => t.phase === phaseDef.phase);
  const filename = `phase-${phaseDef.phase}-${phaseDef.slug}.json`;
  await Bun.write(
    join(phasesDir, filename),
    JSON.stringify(phaseTargets, null, 2),
  );
  manifest.push({
    phase: phaseDef.phase,
    name: phaseDef.name,
    slug: phaseDef.slug,
    file: filename,
    description: phaseDef.description,
    family_count: phaseTargets.length,
  });
  console.log(
    `  Phase ${phaseDef.phase} (${phaseDef.name}): ${phaseTargets.length} families`,
  );
}

await Bun.write(
  join(phasesDir, "manifest.json"),
  JSON.stringify(manifest, null, 2),
);

// ── Summary ─────────────────────────────────────────────────────────────────
const multiFamily = new Set(
  output
    .filter((t) => {
      const dev = t.developers[0];
      return output.filter((o) => o.developers[0] === dev).length > 1;
    })
    .map((t) => t.developers[0]),
);
console.log(`\n${multiFamily.size} vendors with multiple families`);

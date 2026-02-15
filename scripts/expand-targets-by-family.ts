#!/usr/bin/env bun
// Expand targets.json into per-family targets using product-families.json,
// then classify each family into a priority phase based on certification criteria.
//
// For each URL target, looks up the vendor's product families and emits
// one target entry per family. Single-product vendors get one entry with
// family = product name. Multi-product vendors not in product-families.json
// get one entry per unique product name.
//
// The "focus_product" is the newest certified product in each family
// (by certification_date), which collection prompts should prioritize.
//
// Phase classification (highest-priority match across all products in family):
//   Phase 1 (comprehensive-ehrs): any product has CPOE (a)(1-3) AND FHIR API (g)(10)
//   Phase 2 (cpoe-no-fhir):       any product has CPOE but none have (g)(10)
//   Phase 3 (other):              everything else
//
// Outputs:
//   work/family-targets.json              — all family targets
//   work/phases/phase-{N}-{slug}.json     — per-phase family target lists
//   work/phases/manifest.json             — phase summary
//
// Usage:
//   bun run scripts/expand-targets-by-family.ts [--targets work/targets.json] [--output work/family-targets.json]

import { join, dirname } from "node:path";
import { mkdirSync } from "node:fs";

const ROOT = join(dirname(new URL(import.meta.url).pathname), "..");

function slugify(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 60);
}

// Parse args
let targetsPath = join(ROOT, "work", "targets.json");
let outputPath = join(ROOT, "work", "family-targets.json");

const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--targets") targetsPath = args[++i];
  else if (args[i] === "--output") outputPath = args[++i];
  else if (args[i] === "-h" || args[i] === "--help") {
    console.log("Usage: bun run scripts/expand-targets-by-family.ts [--targets <file>] [--output <file>]");
    process.exit(0);
  }
}

// ── Phase definitions ───────────────────────────────────────────────────────
const CPOE = new Set(["170.315 (a)(1)", "170.315 (a)(2)", "170.315 (a)(3)"]);
const G10 = new Set(["170.315 (g)(10)"]);

function hasCPOE(criteria: string[]): boolean {
  return criteria.some((c) => CPOE.has(c));
}
function hasG10(criteria: string[]): boolean {
  return criteria.some((c) => G10.has(c));
}

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
    description: "CPOE + FHIR API (g)(10). Full-featured EHRs with order entry and standards-based API access.",
  },
  {
    phase: 2,
    name: "CPOE systems without FHIR API",
    slug: "cpoe-no-fhir",
    description: "CPOE certified but no (g)(10). EHRs with order entry but no standardized FHIR API.",
  },
  {
    phase: 3,
    name: "Other certified products",
    slug: "other",
    description: "Everything else: no CPOE. Patient portals, lab systems, specialty modules, minimal certifications.",
  },
];

// Classify a family by its products' criteria (highest-priority match)
function classifyFamily(allCriteria: string[][]): number {
  const anyCPOE = allCriteria.some((c) => hasCPOE(c));
  const anyG10 = allCriteria.some((c) => hasG10(c));
  if (anyCPOE && anyG10) return 1;
  if (anyCPOE) return 2;
  return 3;
}

interface Target {
  url: string;
  developers: string[];
  products: string[];
  chpl_ids: number[];
  original_index?: number;
  product_count: number;
}

interface ProductDetail {
  chpl_id: number;
  chpl_product_number: string;
  product_name: string;
  version: string;
  certification_date: string;
  certification_status: string;
  practice_type: string | null;
  certified_criteria: string[];
}

interface TargetMetadata {
  url: string;
  developer: { name: string; [k: string]: unknown };
  mandatory_disclosures_url: string;
  products: ProductDetail[];
}

interface FamilyDef {
  family: string;
  products: string[];
}

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

const targets: Target[] = await Bun.file(targetsPath).json();
const familiesMap: Record<string, FamilyDef[]> = await Bun.file(
  join(ROOT, "work", "product-families.json"),
).json();

const output: FamilyTarget[] = [];

for (let idx = 0; idx < targets.length; idx++) {
  const target = targets[idx];
  const origIdx = target.original_index ?? idx;
  const vendorSlug = slugify(target.developers[0]);

  // Load target metadata for product details
  const metaPath = join(
    ROOT, "work", "target-metadata",
    String(origIdx).padStart(4, "0") + ".json",
  );
  let metadata: TargetMetadata | null = null;
  try {
    metadata = await Bun.file(metaPath).json();
  } catch {
    // No metadata file — use target info directly
  }

  // Build product name → detail map
  const productDetails = new Map<string, ProductDetail>();
  if (metadata) {
    for (const p of metadata.products) {
      // Keep the newest version if duplicates
      const existing = productDetails.get(p.product_name);
      if (!existing || p.certification_date > existing.certification_date) {
        productDetails.set(p.product_name, p);
      }
    }
  }

  // Determine families
  const families = familiesMap[vendorSlug];

  if (families) {
    // Use defined families
    const claimedIds = new Set<number>();
    for (const fam of families) {
      // Find matching products and their CHPL IDs
      const matchedProducts: ProductDetail[] = [];
      for (const pName of fam.products) {
        if (metadata) {
          for (const p of metadata.products) {
            if (p.product_name === pName) {
              matchedProducts.push(p);
            }
          }
        }
      }

      // Filter to only products that are in this target's chpl_ids
      const targetIdSet = new Set(target.chpl_ids);
      const inScope = matchedProducts.filter((p) => targetIdSet.has(p.chpl_id));

      if (inScope.length === 0) continue; // family not in this target

      for (const p of inScope) claimedIds.add(p.chpl_id);

      // Pick newest as focus
      inScope.sort((a, b) => b.certification_date.localeCompare(a.certification_date));
      const focus = inScope[0];

      output.push({
        url: target.url,
        developers: target.developers,
        family: fam.family,
        focus_product: focus.product_name,
        focus_version: focus.version,
        products: inScope.map((p) => p.product_name),
        chpl_ids: inScope.map((p) => p.chpl_id),
        original_index: origIdx,
        product_count: inScope.length,
        phase: classifyFamily(inScope.map((p) => p.certified_criteria)),
      });
    }

    // Warn about products not claimed by any defined family
    const unclaimed = metadata
      ? metadata.products.filter((p) => target.chpl_ids.includes(p.chpl_id) && !claimedIds.has(p.chpl_id))
      : [];
    if (unclaimed.length > 0) {
      console.warn(`WARNING: ${vendorSlug} has ${unclaimed.length} product(s) not in any family:`);
      for (const p of unclaimed) {
        console.warn(`  - ${p.product_name} (chpl_id=${p.chpl_id})`);
      }
      console.warn(`  → Add to work/product-families.json and re-run`);
    }
  } else {
    // No family definition — one entry per unique product name
    const uniqueProducts = [...new Set(target.products)];

    for (const productName of uniqueProducts) {
      const detail = productDetails.get(productName);
      const matchingIds = metadata
        ? metadata.products
            .filter((p) => p.product_name === productName)
            .map((p) => p.chpl_id)
            .filter((id) => target.chpl_ids.includes(id))
        : target.chpl_ids;

      if (matchingIds.length === 0) continue;

      output.push({
        url: target.url,
        developers: target.developers,
        family: productName,
        focus_product: productName,
        focus_version: detail?.version ?? "",
        products: [productName],
        chpl_ids: matchingIds,
        original_index: origIdx,
        product_count: matchingIds.length,
        phase: classifyFamily(
          matchingIds
            .map((id) => metadata?.products.find((p) => p.chpl_id === id)?.certified_criteria)
            .filter((c): c is string[] => !!c),
        ),
      });
    }
  }
}

await Bun.write(outputPath, JSON.stringify(output, null, 2));
console.log(`Wrote ${output.length} family targets to ${outputPath}`);

// Summary stats
const multiFamily = new Set(
  output.filter((t) => {
    const slug = slugify(t.developers[0]);
    return output.filter((o) => slugify(o.developers[0]) === slug).length > 1;
  }).map((t) => slugify(t.developers[0])),
);
console.log(`  ${targets.length} URL targets → ${output.length} family targets`);
console.log(`  ${multiFamily.size} vendors with multiple families`);

// ── Write per-phase family target files ─────────────────────────────────────
const phasesDir = join(ROOT, "work", "phases");
mkdirSync(phasesDir, { recursive: true });

const manifest: { phase: number; name: string; slug: string; file: string; description: string; family_count: number }[] = [];

for (const phaseDef of PHASES) {
  const phaseTargets = output.filter((t) => t.phase === phaseDef.phase);
  const filename = `phase-${phaseDef.phase}-${phaseDef.slug}.json`;
  await Bun.write(join(phasesDir, filename), JSON.stringify(phaseTargets, null, 2));
  manifest.push({
    phase: phaseDef.phase,
    name: phaseDef.name,
    slug: phaseDef.slug,
    file: filename,
    description: phaseDef.description,
    family_count: phaseTargets.length,
  });
  console.log(`  Phase ${phaseDef.phase} (${phaseDef.name}): ${phaseTargets.length} families`);
}

await Bun.write(join(phasesDir, "manifest.json"), JSON.stringify(manifest, null, 2));
console.log(`  Manifest: work/phases/manifest.json`);

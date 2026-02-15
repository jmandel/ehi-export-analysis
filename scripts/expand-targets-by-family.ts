#!/usr/bin/env bun
// Expand targets.json into per-family targets using product-families.json.
//
// For each URL target, looks up the vendor's product families and emits
// one target entry per family. Single-product vendors get one entry with
// family = product name. Multi-product vendors not in product-families.json
// get one entry per unique product name.
//
// The "focus_product" is the newest certified product in each family
// (by certification_date), which collection prompts should prioritize.
//
// Usage:
//   bun run scripts/expand-targets-by-family.ts [--targets work/targets.json] [--output work/family-targets.json]

import { join, dirname } from "node:path";

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
      });
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

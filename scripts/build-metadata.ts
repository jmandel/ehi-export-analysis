#!/usr/bin/env bun
// Generate per-target CHPL metadata files from the bulk download.
//
// Reads:  chpl-data/all-active-listings.json, work/targets.json
// Writes: work/target-metadata/NNNN.json (one per target)
//
// Usage:
//   bun run scripts/build-metadata.ts

import { join, dirname } from "node:path";
import { mkdirSync } from "node:fs";

const ROOT = join(dirname(new URL(import.meta.url).pathname), "..");
const BULK = join(ROOT, "chpl-data", "all-active-listings.json");
const TARGETS = join(ROOT, "work", "targets.json");
const OUTDIR = join(ROOT, "work", "target-metadata");

function fmtDate(val: unknown): string | null {
  if (typeof val === "number") {
    return new Date(val).toISOString().slice(0, 10);
  }
  if (typeof val === "string" && val) return val.slice(0, 10);
  return null;
}

function getStatus(listing: any): string {
  for (const key of ["currentStatus", "certificationStatus"]) {
    const cs = listing[key];
    if (typeof cs === "object" && cs?.name) return cs.name;
    if (typeof cs === "string" && cs) return cs;
  }
  return "Active";
}

function stripEmpty(obj: unknown): unknown {
  if (Array.isArray(obj)) return obj.map(stripEmpty);
  if (typeof obj === "object" && obj !== null) {
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(obj)) {
      if (v !== "") out[k] = stripEmpty(v);
    }
    return out;
  }
  return obj;
}

console.log("Loading CHPL bulk data...");
const listings: any[] = await Bun.file(BULK).json();
const byId = new Map<number, any>();
for (const l of listings) byId.set(l.id, l);
console.log(`  ${listings.length} listings loaded`);

const targets: { url: string; chpl_ids: number[] }[] = await Bun.file(TARGETS).json();
mkdirSync(OUTDIR, { recursive: true });

for (let idx = 0; idx < targets.length; idx++) {
  const target = targets[idx];
  const products = [];

  for (const chplId of target.chpl_ids) {
    const listing = byId.get(chplId);
    if (!listing) continue;

    const criteria = (listing.certificationResults ?? [])
      .filter((cr: any) => cr.success && cr.criterion?.number)
      .map((cr: any) => cr.criterion.number as string)
      .sort();

    products.push({
      chpl_id: listing.id,
      chpl_product_number: listing.chplProductNumber ?? "",
      product_name: listing.product?.name ?? "",
      version: listing.version?.version ?? "",
      certification_date: fmtDate(listing.certificationDate),
      certification_status: getStatus(listing),
      practice_type: listing.practiceType?.name ?? null,
      certified_criteria: criteria,
    });
  }

  const first = byId.get(target.chpl_ids[0]) ?? {};
  const dev = first.developer ?? {};
  const contact = dev.contact ?? {};

  const meta = {
    url: target.url,
    developer: {
      name: dev.name ?? "",
      website: dev.website ?? "",
      contact_name: contact.fullName ?? "",
      contact_email: contact.email ?? "",
      contact_phone: contact.phoneNumber ?? "",
    },
    sed_intended_user_description: first.sedIntendedUserDescription ?? "",
    mandatory_disclosures_url: first.mandatoryDisclosures ?? "",
    products,
  };

  await Bun.write(
    join(OUTDIR, `${String(idx).padStart(4, "0")}.json`),
    JSON.stringify(stripEmpty(meta), null, 2),
  );
}

console.log(`Wrote ${targets.length} metadata files to ${OUTDIR}/`);

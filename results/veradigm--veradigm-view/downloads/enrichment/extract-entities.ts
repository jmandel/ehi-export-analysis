#!/usr/bin/env bun
/**
 * Extract structured entity/field data from Veradigm View EHI Export
 * Documentation V6 HTML pages.
 *
 * Usage:  bun run extract-entities.ts
 * Input:  ../v6-entities/*.html  +  ../v6-index.html
 * Output: entities-catalog.json, coverage-accounting.json
 */

import { readdir, readFile } from "node:fs/promises";
import { join, basename } from "node:path";

const ENTITIES_DIR = join(import.meta.dir, "..", "v6-entities");
const INDEX_PATH = join(import.meta.dir, "..", "v6-index.html");
const OUT_CATALOG = join(import.meta.dir, "entities-catalog.json");
const OUT_ACCOUNTING = join(import.meta.dir, "coverage-accounting.json");

interface Field {
  name: string;
  dataType: string;
  description: string;
}

interface Entity {
  slug: string;
  tsvFilename: string;
  description: string;
  category: string;
  fields: Field[];
  sourceFile: string;
}

// Parse the index page to get category assignments
async function parseIndex(): Promise<Map<string, { description: string; category: string }>> {
  const html = await readFile(INDEX_PATH, "utf-8");
  const map = new Map<string, { description: string; category: string }>();

  // Find the content area
  const contentMatch = html.match(
    /class="col-xxl-10 mx-auto feature-documentation">([\s\S]*?)<div class="row" id="feature-documentation"/
  );
  if (!contentMatch) return map;
  const content = contentMatch[1];

  // Split by h3 headings to get categories
  const categoryBlocks = content.split(/<h3[^>]*>/);
  for (const block of categoryBlocks) {
    const catMatch = block.match(/^([^<]+)<\/h3>/);
    const category = catMatch ? catMatch[1].trim() : "Uncategorized";

    // Find all entity links within this category block
    const linkRe =
      /href="\/legal\/veradigm-view-ehi-export-documentation\/v6\/([^/"]+)\/"[^>]*>([^<]+)<\/a>\s*([\s\S]*?)(?=<li>|<\/ul>)/g;
    let m;
    while ((m = linkRe.exec(block)) !== null) {
      const slug = m[1];
      const desc = m[3].trim().replace(/\s+/g, " ");
      map.set(slug, { description: desc, category });
    }
  }
  return map;
}

// Parse a single entity HTML page
function parseEntityPage(html: string, slug: string): { tsvFilename: string; description: string; fields: Field[] } {
  // Extract TSV filename from <h2>
  const h2Match = html.match(/<h2[^>]*>([^<]+\.tsv)<\/h2>/i);
  const tsvFilename = h2Match ? h2Match[1].trim() : `${slug}.tsv`;

  // Extract description from <h4>
  const h4Match = html.match(/<h4[^>]*>([^<]+)<\/h4>/i);
  const description = h4Match ? h4Match[1].trim() : "";

  // Extract fields from the table
  const fields: Field[] = [];
  const tableMatch = html.match(/<table[^>]*class="table[^"]*"[^>]*>([\s\S]*?)<\/table>/i);
  if (tableMatch) {
    const tbody = tableMatch[1];
    const rowRe = /<tr>\s*<td>([^<]*)<\/td>\s*<td>([^<]*)<\/td>\s*<td>([\s\S]*?)<\/td>\s*<\/tr>/gi;
    let rm;
    while ((rm = rowRe.exec(tbody)) !== null) {
      fields.push({
        name: rm[1].trim(),
        dataType: rm[2].trim(),
        description: rm[3].replace(/<[^>]*>/g, "").trim().replace(/\s+/g, " "),
      });
    }
  }

  return { tsvFilename, description, fields };
}

async function main() {
  const indexMap = await parseIndex();
  const files = (await readdir(ENTITIES_DIR)).filter((f) => f.endsWith(".html")).sort();

  const entities: Entity[] = [];
  const failures: { file: string; error: string }[] = [];

  for (const file of files) {
    const slug = file.replace(/\.html$/, "");
    try {
      const html = await readFile(join(ENTITIES_DIR, file), "utf-8");
      const { tsvFilename, description: pageDesc, fields } = parseEntityPage(html, slug);

      const indexInfo = indexMap.get(slug);
      const description = pageDesc || indexInfo?.description || "";
      const category = indexInfo?.category || "Unknown";

      if (fields.length === 0) {
        failures.push({ file, error: "No fields found in table" });
      }

      entities.push({
        slug,
        tsvFilename,
        description,
        category,
        fields,
        sourceFile: `v6-entities/${file}`,
      });
    } catch (e: any) {
      failures.push({ file, error: e.message });
    }
  }

  // Write catalog
  const totalFields = entities.reduce((s, e) => s + e.fields.length, 0);
  const catalog = {
    version: "v6",
    exportFormat: "TSV (tab-separated values)",
    collectionDate: new Date().toISOString().slice(0, 10),
    summary: {
      totalEntities: entities.length,
      totalFields,
      categories: [...new Set(entities.map((e) => e.category))],
    },
    entities,
  };
  await Bun.write(OUT_CATALOG, JSON.stringify(catalog, null, 2));

  // Write accounting
  const accounting = {
    totalFilesDiscovered: files.length,
    totalFilesParsed: entities.length,
    totalFieldsExtracted: totalFields,
    parseFailures: failures,
    entitiesWithNoFields: entities.filter((e) => e.fields.length === 0).map((e) => e.slug),
    fieldCountByEntity: Object.fromEntries(entities.map((e) => [e.slug, e.fields.length])),
    fieldCountByCategory: Object.fromEntries(
      [...new Set(entities.map((e) => e.category))].map((cat) => [
        cat,
        entities.filter((e) => e.category === cat).reduce((s, e) => s + e.fields.length, 0),
      ])
    ),
  };
  await Bun.write(OUT_ACCOUNTING, JSON.stringify(accounting, null, 2));

  console.log(`Parsed ${entities.length}/${files.length} entity files`);
  console.log(`Extracted ${totalFields} total fields`);
  console.log(`Failures: ${failures.length}`);
  if (failures.length > 0) {
    for (const f of failures) console.log(`  - ${f.file}: ${f.error}`);
  }
}

main();

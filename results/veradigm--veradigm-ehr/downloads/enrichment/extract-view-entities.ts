/**
 * Extract structured entity/field data from Veradigm View EHI Export HTML pages.
 *
 * Usage:  bun run extract-view-entities.ts
 * Input:  ../veradigm-view-v6/*.html
 * Output: view-entities-catalog.json, view-coverage-accounting.json
 */

import { readdir, readFile } from "fs/promises";
import { join, basename } from "path";

const INPUT_DIR = join(import.meta.dir, "..", "veradigm-view-v6");
const OUTPUT_CATALOG = join(import.meta.dir, "view-entities-catalog.json");
const OUTPUT_ACCOUNTING = join(import.meta.dir, "view-coverage-accounting.json");

interface Field {
  name: string;
  dataType: string;
  description: string;
}

interface Entity {
  pageTitle: string;
  tsvFilename: string;
  entityDescription: string;
  sourceFile: string;
  fields: Field[];
}

function extractEntities(html: string, sourceFile: string): Entity[] {
  const entities: Entity[] = [];

  // Extract page title from <h1>
  const h1Match = html.match(/<h1[^>]*>(.*?)<\/h1>/i);
  const pageTitle = h1Match ? h1Match[1].replace(/<[^>]*>/g, "").trim() : basename(sourceFile, ".html");

  // Find all h2 elements with tsv filenames
  const h2Regex = /<h2[^>]*id="([^"]*)"[^>]*>(.*?)<\/h2>/gi;
  const tableRegex = /<table[^>]*>([\s\S]*?)<\/table>/gi;
  const h4Regex = /<h4[^>]*>(.*?)<\/h4>/gi;

  // Collect all sections: h2 (tsv filename) -> h4 (description) -> table (fields)
  const sections: Array<{ h2Text: string; h4Text: string; tableHtml: string }> = [];

  // Simple approach: find h2 with .tsv, then find next h4 and table
  const h2Matches = [...html.matchAll(/<h2[^>]*>(.*?)<\/h2>/gi)];
  const tableMatches = [...html.matchAll(/<table[^>]*>([\s\S]*?)<\/table>/gi)];
  const h4Matches = [...html.matchAll(/<h4[^>]*>(.*?)<\/h4>/gi)];

  // Filter h2s that are TSV filenames (contain .tsv)
  const tsvH2s = h2Matches.filter(m => m[1].includes(".tsv"));

  for (let i = 0; i < tsvH2s.length; i++) {
    const h2 = tsvH2s[i];
    const h2Text = h2[1].replace(/<[^>]*>/g, "").trim();
    const h2Pos = h2.index!;

    // Find next h4 after this h2 (but before next tsv h2 if any)
    const nextH2Pos = i + 1 < tsvH2s.length ? tsvH2s[i + 1].index! : html.length;
    const regionH4s = h4Matches.filter(m => m.index! > h2Pos && m.index! < nextH2Pos);
    const h4Text = regionH4s.length > 0 ? regionH4s[0][1].replace(/<[^>]*>/g, "").trim() : "";

    // Find table(s) in this region
    const regionTables = tableMatches.filter(m => m.index! > h2Pos && m.index! < nextH2Pos);

    for (const table of regionTables) {
      const fields = extractFields(table[0]);
      entities.push({
        pageTitle,
        tsvFilename: h2Text,
        entityDescription: h4Text,
        sourceFile: basename(sourceFile),
        fields,
      });
    }

    // If no table found, still record the entity
    if (regionTables.length === 0) {
      entities.push({
        pageTitle,
        tsvFilename: h2Text,
        entityDescription: h4Text,
        sourceFile: basename(sourceFile),
        fields: [],
      });
    }
  }

  return entities;
}

function extractFields(tableHtml: string): Field[] {
  const fields: Field[] = [];
  const rowRegex = /<tr>\s*<td>(.*?)<\/td>\s*<td>(.*?)<\/td>\s*<td>(.*?)<\/td>\s*<\/tr>/gi;

  for (const match of tableHtml.matchAll(rowRegex)) {
    fields.push({
      name: match[1].replace(/<[^>]*>/g, "").trim(),
      dataType: match[2].replace(/<[^>]*>/g, "").trim(),
      description: match[3].replace(/<[^>]*>/g, "").trim(),
    });
  }

  return fields;
}

async function main() {
  const files = (await readdir(INPUT_DIR)).filter(f => f.endsWith(".html")).sort();
  const allEntities: Entity[] = [];
  const errors: Array<{ file: string; error: string }> = [];

  for (const file of files) {
    try {
      const html = await readFile(join(INPUT_DIR, file), "utf-8");
      const entities = extractEntities(html, file);
      allEntities.push(...entities);
    } catch (e: any) {
      errors.push({ file, error: e.message });
    }
  }

  // Write catalog
  await Bun.write(OUTPUT_CATALOG, JSON.stringify(allEntities, null, 2));

  // Write accounting
  const accounting = {
    totalFilesDiscovered: files.length,
    totalFilesParsed: files.length - errors.length,
    totalEntitiesExtracted: allEntities.length,
    totalFieldsExtracted: allEntities.reduce((sum, e) => sum + e.fields.length, 0),
    entitiesWithFields: allEntities.filter(e => e.fields.length > 0).length,
    entitiesWithoutFields: allEntities.filter(e => e.fields.length === 0).length,
    parseFailures: errors,
    entitySummary: allEntities.map(e => ({
      tsvFilename: e.tsvFilename,
      fieldCount: e.fields.length,
      sourceFile: e.sourceFile,
    })),
  };
  await Bun.write(OUTPUT_ACCOUNTING, JSON.stringify(accounting, null, 2));

  console.log(`Parsed ${files.length} files, extracted ${allEntities.length} entities with ${accounting.totalFieldsExtracted} total fields`);
  if (errors.length > 0) {
    console.log(`Parse failures: ${errors.length}`);
    errors.forEach(e => console.log(`  ${e.file}: ${e.error}`));
  }
}

main();

#!/usr/bin/env bun
/**
 * Extracts structured data from Intergy EHI Export data dictionary HTML pages.
 * Parses each table's .htm file to extract fields, datatypes, relationships.
 *
 * Usage: bun run extract-tables.ts
 */

import { readdir, readFile, writeFile } from "fs/promises";
import { join } from "path";

const CONTRACTS_DIR = join(import.meta.dir, "../viewer/Contracts");
const OUTPUT_FILE = join(import.meta.dir, "intergy-data-dictionary.json");
const COVERAGE_FILE = join(import.meta.dir, "extraction-coverage.json");

interface Field {
  name: string;
  datatype: string;
  default_value: string | null;
  null_option: string;
  comment: string;
}

interface Relationship {
  table: string;
  field: string;
}

interface TableDefinition {
  name: string;
  description: string;
  last_updated: string | null;
  intergy_version: string | null;
  fields: Field[];
  parent_tables: Relationship[];
  child_tables: Relationship[];
  source_file: string;
}

function extractText(html: string): string {
  return html.replace(/<[^>]*>/g, " ").replace(/&nbsp;?/g, " ").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/\s+/g, " ").trim();
}

function parseTablePage(html: string, filename: string): TableDefinition | null {
  const name = filename.replace(".htm", "");

  // Extract metadata
  const lastUpdatedMatch = html.match(/Last Updated:\s*([^<]+)/);
  const versionMatch = html.match(/Intergy Version:\s*([^<]+)/);

  // Extract description
  const descMatch = html.match(/<h3>\s*Description:\s*(.*?)<\/h3>/s);
  const description = descMatch ? extractText(descMatch[1]) : "";

  // Extract table definition fields
  const fields: Field[] = [];
  const tableDefSection = html.split(/<a name="table">/i)[1]?.split(/<a name="/i)[0] || html;

  const rowRegex = /<tr>\s*<td[^>]*>(.*?)<\/td>\s*<td[^>]*>(.*?)<\/td>\s*<td[^>]*>(.*?)<\/td>\s*<td[^>]*>(.*?)<\/td>\s*<td[^>]*>(.*?)<\/td>\s*<\/tr>/gs;
  let match;
  while ((match = rowRegex.exec(tableDefSection)) !== null) {
    const fieldName = extractText(match[1]);
    const datatype = extractText(match[2]);
    const defaultVal = extractText(match[3]);
    const nullOption = extractText(match[4]);
    const comment = extractText(match[5]);

    if (fieldName && datatype && fieldName !== "Field") {
      fields.push({
        name: fieldName,
        datatype,
        default_value: defaultVal === "?" || defaultVal === "" ? null : defaultVal,
        null_option: nullOption,
        comment,
      });
    }
  }

  // Extract parent relationships
  const parent_tables: Relationship[] = [];
  const parentSection = html.split(/<a name="parentrel">/i)[1]?.split(/<a name="/i)[0];
  if (parentSection) {
    const relRegex = /<tr>\s*<td[^>]*>(.*?)<\/td>\s*<td[^>]*>(.*?)<\/td>\s*<\/tr>/gs;
    while ((match = relRegex.exec(parentSection)) !== null) {
      const table = extractText(match[1]);
      const field = extractText(match[2]);
      if (table && table !== "Parent Table" && table !== "No parent tables") {
        parent_tables.push({ table, field });
      }
    }
  }

  // Extract child relationships
  const child_tables: Relationship[] = [];
  const childSection = html.split(/<a name="childrel">/i)[1];
  if (childSection) {
    const relRegex = /<tr>\s*<td[^>]*>(.*?)<\/td>\s*<td[^>]*>(.*?)<\/td>\s*<\/tr>/gs;
    while ((match = relRegex.exec(childSection)) !== null) {
      const table = extractText(match[1]);
      const field = extractText(match[2]);
      if (table && table !== "Child Table" && table !== "No child tables") {
        child_tables.push({ table, field });
      }
    }
  }

  return {
    name,
    description,
    last_updated: lastUpdatedMatch ? extractText(lastUpdatedMatch[1]) : null,
    intergy_version: versionMatch ? extractText(versionMatch[1]) : null,
    fields,
    parent_tables,
    child_tables,
    source_file: `viewer/Contracts/${filename}`,
  };
}

async function main() {
  const files = (await readdir(CONTRACTS_DIR)).filter(
    (f) => f.endsWith(".htm") && f !== "DBTOC.htm"
  );

  const tables: TableDefinition[] = [];
  const failures: { file: string; error: string }[] = [];

  for (const file of files.sort()) {
    try {
      const html = await readFile(join(CONTRACTS_DIR, file), "utf-8");
      const table = parseTablePage(html, file);
      if (table && table.fields.length > 0) {
        tables.push(table);
      } else if (table) {
        failures.push({ file, error: "No fields extracted" });
      }
    } catch (e: any) {
      failures.push({ file, error: e.message });
    }
  }

  // Write main output
  await writeFile(OUTPUT_FILE, JSON.stringify(tables, null, 2));

  // Write coverage report
  const totalFields = tables.reduce((sum, t) => sum + t.fields.length, 0);
  const totalParentRels = tables.reduce((sum, t) => sum + t.parent_tables.length, 0);
  const totalChildRels = tables.reduce((sum, t) => sum + t.child_tables.length, 0);

  const coverage = {
    total_files_discovered: files.length,
    total_files_parsed: tables.length,
    total_fields_extracted: totalFields,
    total_parent_relationships: totalParentRels,
    total_child_relationships: totalChildRels,
    parse_failures: failures,
    tables_summary: tables.map((t) => ({
      name: t.name,
      field_count: t.fields.length,
      parent_count: t.parent_tables.length,
      child_count: t.child_tables.length,
      has_description: t.description.length > 0,
    })),
  };

  await writeFile(COVERAGE_FILE, JSON.stringify(coverage, null, 2));

  console.log(`Extracted ${tables.length} tables with ${totalFields} fields`);
  console.log(`${totalParentRels} parent relationships, ${totalChildRels} child relationships`);
  console.log(`Parse failures: ${failures.length}`);
  if (failures.length > 0) {
    console.log("Failures:", failures);
  }
}

main();

/**
 * Final parser for smartEMR data import specification pages.
 * Each page has two tables:
 *   Table 1 (summary): Field | Required | Description
 *   Table 2 (detail): # | Field | Description | Data Type | [Max Length] | Required | Validation Rule | [Standard] | [Notes]
 * Detail table is more complete (has extra fields not in summary).
 * Merges both by field name, preferring detail table as primary source.
 *
 * Also parses the EHI export page prose content.
 */
import { readFileSync, writeFileSync, readdirSync } from "fs";
import { join } from "path";

const DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/vipa-health-solutions-llc--24-7-smartemr/downloads";
const OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/vipa-health-solutions-llc--24-7-smartemr/analysis";

// Simple HTML table parser (no cheerio needed for this)
interface RawTable {
  headers: string[];
  rows: string[][];
}

function extractTables(html: string): RawTable[] {
  const tables: RawTable[] = [];
  const tableRegex = /<table[^>]*>([\s\S]*?)<\/table>/gi;
  let match;
  while ((match = tableRegex.exec(html)) !== null) {
    const tableHtml = match[1];
    const rows: string[][] = [];
    const rowRegex = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
    let rowMatch;
    while ((rowMatch = rowRegex.exec(tableHtml)) !== null) {
      const cells: string[] = [];
      const cellRegex = /<t[dh][^>]*>([\s\S]*?)<\/t[dh]>/gi;
      let cellMatch;
      while ((cellMatch = cellRegex.exec(rowMatch[1])) !== null) {
        cells.push(cellMatch[1].replace(/<[^>]+>/g, "").trim());
      }
      if (cells.length > 0) rows.push(cells);
    }
    if (rows.length > 1) {
      tables.push({
        headers: rows[0].map(h => h.toLowerCase().trim()),
        rows: rows.slice(1),
      });
    }
  }
  return tables;
}

interface Field {
  name: string;
  type: string;
  description: string;
  required: boolean;
  maxLength: string | null;
  validationRule: string | null;
  standard: string | null;
  notes: string | null;
  codeSystem: string | null;
}

interface Entity {
  name: string;
  sourceFile: string;
  sourceUrl: string;
  category: string;
  fieldCount: number;
  fieldsWithDescriptions: number;
  fieldsWithTypes: number;
  requiredFields: number;
  codeSystems: string[];
  fields: Field[];
}

function detectCodeSystem(text: string): string | null {
  const t = text.toLowerCase();
  if (t.includes("rxnorm")) return "RxNorm";
  if (t.includes("snomed")) return "SNOMED CT";
  if (t.includes("icd-10") || t.includes("icd10") || t.includes("icd_code")) return "ICD-10-CM";
  if (t.includes("cpt") || t.includes("hcpcs")) return "CPT/HCPCS";
  if (t.includes("npi") && !t.includes("name")) return "NPI";
  return null;
}

function parsePage(filePath: string, fileName: string): Entity {
  const html = readFileSync(filePath, "utf-8");
  const tables = extractTables(html);

  // Extract title from h1
  const h1Match = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  const title = h1Match ? h1Match[1].replace(/<[^>]+>/g, "").trim() : fileName.replace(".html", "").replace(/-/g, " ");

  // Classify tables
  let summaryTable: RawTable | null = null;
  let detailTable: RawTable | null = null;
  let standardsTable: RawTable | null = null; // allergies page has a 3rd table

  for (const t of tables) {
    const headerStr = t.headers.join("|");
    if (headerStr.includes("data element") || headerStr.includes("supported")) {
      standardsTable = t;
    } else if (headerStr.includes("data type") || headerStr.includes("max length") || headerStr.includes("standard") || headerStr.includes("notes")) {
      // Detail table - has more columns
      if (!detailTable || t.rows.length > detailTable.rows.length) {
        detailTable = t;
      }
    } else if (headerStr.includes("field") && headerStr.includes("description")) {
      summaryTable = t;
    }
  }

  // Build fields from detail table (primary) then fill from summary
  const fieldMap = new Map<string, Field>();

  // Process detail table first (more complete)
  if (detailTable) {
    const h = detailTable.headers;
    const fieldIdx = h.findIndex(x => x === "field");
    const descIdx = h.findIndex(x => x === "description");
    const typeIdx = h.findIndex(x => x.includes("data type") || x === "type");
    const maxLenIdx = h.findIndex(x => x.includes("max length") || x.includes("max"));
    const reqIdx = h.findIndex(x => x === "required");
    const valIdx = h.findIndex(x => x.includes("validation"));
    const stdIdx = h.findIndex(x => x === "standard");
    const notesIdx = h.findIndex(x => x === "notes");

    for (const row of detailTable.rows) {
      const name = fieldIdx >= 0 ? (row[fieldIdx] || "") : (row[1] || "");
      if (!name) continue;
      const desc = descIdx >= 0 ? (row[descIdx] || "") : "";
      const type = typeIdx >= 0 ? (row[typeIdx] || "") : "";
      const maxLen = maxLenIdx >= 0 ? (row[maxLenIdx] || null) : null;
      const reqStr = reqIdx >= 0 ? (row[reqIdx] || "") : "";
      const valRule = valIdx >= 0 ? (row[valIdx] || null) : null;
      const standard = stdIdx >= 0 ? (row[stdIdx] || null) : null;
      const notes = notesIdx >= 0 ? (row[notesIdx] || null) : null;

      const allText = [name, desc, type, standard || "", notes || "", valRule || ""].join(" ");

      fieldMap.set(name.toLowerCase(), {
        name,
        type,
        description: desc,
        required: reqStr.includes("✅"),
        maxLength: maxLen && maxLen !== "—" ? maxLen : null,
        validationRule: valRule && valRule !== "—" ? valRule : null,
        standard: standard && standard !== "—" ? standard : null,
        notes: notes && notes !== "—" ? notes : null,
        codeSystem: detectCodeSystem(allText),
      });
    }
  }

  // Fill from summary table (may have descriptions that are more detailed)
  if (summaryTable) {
    const h = summaryTable.headers;
    const fieldIdx = h.findIndex(x => x === "field");
    const descIdx = h.findIndex(x => x === "description");
    const reqIdx = h.findIndex(x => x === "required");

    for (const row of summaryTable.rows) {
      const name = fieldIdx >= 0 ? (row[fieldIdx] || "") : (row[0] || "");
      if (!name) continue;
      const key = name.toLowerCase();
      const desc = descIdx >= 0 ? (row[descIdx] || "") : "";
      const reqStr = reqIdx >= 0 ? (row[reqIdx] || "") : "";

      const existing = fieldMap.get(key);
      if (existing) {
        // Prefer longer description
        if (desc.length > existing.description.length) {
          existing.description = desc;
        }
      } else {
        // Add field from summary only
        fieldMap.set(key, {
          name,
          type: "",
          description: desc,
          required: reqStr.includes("✅"),
          maxLength: null,
          validationRule: null,
          standard: null,
          notes: null,
          codeSystem: detectCodeSystem(name + " " + desc),
        });
      }
    }
  }

  const fields = Array.from(fieldMap.values());

  // Determine category
  let category = "DATA IMPORT";
  if (fileName.includes("electronic-health-information")) {
    category = "EHI EXPORT";
  } else if (["document-upload", "problem-list", "patient-allergies", "immunization-records"].some(s => fileName.includes(s))) {
    category = "CLINICAL DATA IMPORT (ALT)";
  }

  const slug = fileName.replace(".html", "");
  const codeSystems = [...new Set(fields.filter(f => f.codeSystem).map(f => f.codeSystem!))];

  return {
    name: title,
    sourceFile: fileName,
    sourceUrl: `https://smartemr.readme.io/docs/${slug}`,
    category,
    fieldCount: fields.length,
    fieldsWithDescriptions: fields.filter(f => f.description.length > 0).length,
    fieldsWithTypes: fields.filter(f => f.type.length > 0).length,
    requiredFields: fields.filter(f => f.required).length,
    codeSystems,
    fields,
  };
}

function parseEhiExportPage(filePath: string) {
  const html = readFileSync(filePath, "utf-8");
  // Strip all HTML tags and get text
  const textOnly = html.replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  // Extract article content specifically
  const articleMatch = html.match(/<article[^>]*>([\s\S]*?)<\/article>/i);
  const articleText = articleMatch
    ? articleMatch[1].replace(/<script[\s\S]*?<\/script>/gi, "").replace(/<style[\s\S]*?<\/style>/gi, "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim()
    : "";

  const wordCount = articleText.split(/\s+/).filter(w => w.length > 0).length;

  return {
    wordCount,
    articleText: articleText.substring(0, 5000),
  };
}

// Main
const htmlFiles = readdirSync(DOWNLOADS).filter(f => f.endsWith(".html"));
const entities: Entity[] = [];
let ehiPage: any = null;

for (const file of htmlFiles) {
  const filePath = join(DOWNLOADS, file);
  if (file === "electronic-health-information-export-b10.html") {
    ehiPage = parseEhiExportPage(filePath);
  }
  const entity = parsePage(filePath, file);
  entities.push(entity);
}

const dataEntities = entities.filter(e => e.category !== "EHI EXPORT" && e.fieldCount > 0);
const totalFields = dataEntities.reduce((s, e) => s + e.fieldCount, 0);
const totalWithDesc = dataEntities.reduce((s, e) => s + e.fieldsWithDescriptions, 0);
const totalWithTypes = dataEntities.reduce((s, e) => s + e.fieldsWithTypes, 0);
const totalRequired = dataEntities.reduce((s, e) => s + e.requiredFields, 0);
const allCodeSystems = [...new Set(dataEntities.flatMap(e => e.codeSystems))];

const inventory = {
  extractionDate: new Date().toISOString(),
  sourceDir: DOWNLOADS,
  note: "These are DATA IMPORT specs (not export). They document what the product stores, not what the EHI export outputs. The EHI export page itself has no field-level schema.",
  summary: {
    totalDataEntities: dataEntities.length,
    emptyEntities: entities.filter(e => e.fieldCount === 0).map(e => ({ name: e.name, file: e.sourceFile })),
    totalFields,
    fieldsWithDescriptions: totalWithDesc,
    pctWithDescriptions: totalFields > 0 ? Math.round((totalWithDesc / totalFields) * 100) : 0,
    fieldsWithTypes: totalWithTypes,
    pctWithTypes: totalFields > 0 ? Math.round((totalWithTypes / totalFields) * 100) : 0,
    requiredFields: totalRequired,
    codeSystems: allCodeSystems,
  },
  byCategory: {} as Record<string, { entities: string[]; totalFields: number; fieldsWithTypes: number }>,
  entities: dataEntities,
  ehiExportPage: ehiPage,
};

for (const e of dataEntities) {
  if (!inventory.byCategory[e.category]) {
    inventory.byCategory[e.category] = { entities: [], totalFields: 0, fieldsWithTypes: 0 };
  }
  inventory.byCategory[e.category].entities.push(e.name);
  inventory.byCategory[e.category].totalFields += e.fieldCount;
  inventory.byCategory[e.category].fieldsWithTypes += e.fieldsWithTypes;
}

writeFileSync(join(OUTPUT_DIR, "full-entity-inventory.json"), JSON.stringify(inventory, null, 2));

// Print results
console.log("=== FINAL ENTITY INVENTORY ===");
console.log(`Data entities with fields: ${dataEntities.length}`);
console.log(`Empty entities: ${inventory.summary.emptyEntities.map(e => e.name).join(", ")}`);
console.log(`Total unique fields: ${totalFields}`);
console.log(`Fields with descriptions: ${totalWithDesc} (${inventory.summary.pctWithDescriptions}%)`);
console.log(`Fields with data types: ${totalWithTypes} (${inventory.summary.pctWithTypes}%)`);
console.log(`Required fields: ${totalRequired}`);
console.log(`Code systems: ${allCodeSystems.join(", ")}`);
console.log();

for (const e of dataEntities) {
  console.log(`${e.name} [${e.category}]`);
  console.log(`  ${e.fieldCount} fields, ${e.fieldsWithDescriptions} described, ${e.fieldsWithTypes} typed, ${e.requiredFields} required`);
  console.log(`  Code systems: ${e.codeSystems.join(", ") || "none"}`);
  for (const f of e.fields) {
    const parts = [f.name];
    if (f.type) parts.push(`(${f.type}${f.maxLength ? `[${f.maxLength}]` : ""})`);
    if (f.required) parts.push("[REQ]");
    if (f.codeSystem) parts.push(`{${f.codeSystem}}`);
    parts.push(`- ${f.description || "(no desc)"}`);
    console.log(`    ${parts.join(" ")}`);
  }
}

if (ehiPage) {
  console.log(`\n=== EHI EXPORT PAGE ===`);
  console.log(`Word count: ${ehiPage.wordCount}`);
  console.log(`Content:\n${ehiPage.articleText.substring(0, 2000)}`);
}

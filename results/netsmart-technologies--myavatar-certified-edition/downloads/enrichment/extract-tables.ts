/**
 * Parses the pdftotext output of "EHI Export All Tables - September 2023.pdf"
 * into structured JSON with form, table, and column-level detail.
 *
 * Run: bun run extract-tables.ts
 * Input: ../ehi-export-all-tables.txt (pdftotext output of the PDF)
 * Output: tables.json, coverage-summary.json
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "ehi-export-all-tables.txt");
const outputPath = join(scriptDir, "tables.json");
const summaryPath = join(scriptDir, "coverage-summary.json");

interface Column {
  name: string;
  type: string;
  max_length: number | null;
  description: string | null;
}

interface TableEntry {
  form_name: string;
  table_name: string;
  schema: string;
  table_short_name: string;
  table_description: string | null;
  columns: Column[];
}

const raw = readFileSync(inputPath, "utf-8");
const lines = raw.split("\n");

const tables: TableEntry[] = [];
let parseErrors: { line: number; reason: string }[] = [];

// State machine
let currentForm: string | null = null;
let currentTable: string | null = null;
let currentTableDesc: string | null = null;
let currentColumns: Column[] = [];
let currentColumn: Partial<Column> | null = null;
let descriptionLines: string[] = [];
let inTOC = true; // Skip the TOC at the start

function flushColumn() {
  if (currentColumn?.name && currentColumn?.type) {
    const desc = descriptionLines.join(" ").trim() || null;
    currentColumns.push({
      name: currentColumn.name,
      type: currentColumn.type,
      max_length: currentColumn.max_length ?? null,
      description: desc,
    });
  }
  currentColumn = null;
  descriptionLines = [];
}

function flushTable() {
  flushColumn();
  if (currentTable) {
    const parts = currentTable.split(".");
    tables.push({
      form_name: currentForm ?? "",
      table_name: currentTable,
      schema: parts.length > 1 ? parts[0] : "",
      table_short_name: parts.length > 1 ? parts.slice(1).join(".") : currentTable,
      table_description: currentTableDesc,
      columns: currentColumns,
    });
  }
  currentTable = null;
  currentTableDesc = null;
  currentColumns = [];
}

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  const trimmed = line.trim();

  // Skip blank lines and page numbers
  if (trimmed === "" || /^\d+$/.test(trimmed)) continue;

  // Skip TOC lines (contain ......... page references)
  if (trimmed.includes("..........")) continue;

  // Detect end of TOC / start of content
  if (inTOC) {
    if (trimmed === "Overview") {
      inTOC = false;
    }
    continue;
  }

  // Skip known non-table content
  if (trimmed === "Overview" || trimmed.startsWith("Glossary of Terms")) continue;
  if (trimmed.startsWith("EHI Export: myAvatar")) continue;
  if (trimmed.startsWith("Last Updated:")) continue;
  if (trimmed.startsWith("Table of Contents")) continue;

  // Skip glossary entries (detected by context - they're before the first "Documentation for form:")
  // The glossary is between "Glossary of Terms" and the first form entry at line ~2109

  // Form header
  if (trimmed.startsWith("Documentation for form:")) {
    flushTable();
    currentForm = trimmed.replace("Documentation for form:", "").trim();
    continue;
  }

  // Table name
  if (trimmed.startsWith("Table Name:")) {
    // If we already have a table in progress, flush it
    if (currentTable) {
      flushTable();
    }
    currentTable = trimmed.replace("Table Name:", "").trim();
    continue;
  }

  // Table description
  if (trimmed.startsWith("Table Description:")) {
    currentTableDesc = trimmed.replace("Table Description:", "").trim();
    continue;
  }

  // Separator line
  if (trimmed === "-------------") continue;

  // Column name
  if (trimmed.startsWith("Column Name:")) {
    flushColumn();
    currentColumn = { name: trimmed.replace("Column Name:", "").trim() };
    continue;
  }

  // Column type
  if (trimmed.startsWith("Column Type:") && currentColumn) {
    currentColumn.type = trimmed.replace("Column Type:", "").trim();
    continue;
  }

  // Max length
  if (trimmed.startsWith("Max Length:") && currentColumn) {
    const val = parseInt(trimmed.replace("Max Length:", "").trim(), 10);
    currentColumn.max_length = isNaN(val) ? null : val;
    continue;
  }

  // If we're in a column and the line is descriptive text, accumulate it
  if (currentColumn && currentColumn.type) {
    descriptionLines.push(trimmed);
    continue;
  }

  // If we're in the glossary section (before the first form), skip
  if (!currentForm && !currentTable) continue;

  // Continuation of table description
  if (currentTable && !currentColumn && currentTableDesc !== null) {
    currentTableDesc += " " + trimmed;
    continue;
  }
}

// Flush last table
flushTable();

// Build coverage summary
const uniqueTables = new Set(tables.map((t) => t.table_name));
const uniqueForms = new Set(tables.map((t) => t.form_name).filter(Boolean));
const schemaBreakdown: Record<string, number> = {};
for (const t of tables) {
  schemaBreakdown[t.schema] = (schemaBreakdown[t.schema] || 0) + 1;
}

// Categorize tables by data domain
function categorize(tableName: string, formName: string): string[] {
  const t = tableName.toLowerCase();
  const f = formName.toLowerCase();
  const categories: string[] = [];

  if (/billing|claim|charge|payment|remit|financial|ledger|cash|fee|835|837|276|277|834|selfpay|payor|invoice/.test(t + f))
    categories.push("billing_financial");
  if (/note|progress|document|clinical_rec|cw_patient/.test(t + f))
    categories.push("clinical_notes");
  if (/med|drug|pharm|rx|prescri|emar|methadone|ncpdp/.test(t + f))
    categories.push("medication_pharmacy");
  if (/client|patient|demo|enroll|admit|discharg|episode|patid|outreach|merge|purge|pre_admit/.test(t + f))
    categories.push("demographics_patient");
  if (/appoint|schedul|waiting|check_in|check_out|telehealth|front_desk/.test(t + f))
    categories.push("scheduling");
  if (/diag|problem|condition/.test(t + f))
    categories.push("diagnosis");
  if (/order|lab|result|specimen/.test(t + f))
    categories.push("labs_orders");
  if (/treat|tx_plan|care|assess|goal|pathway/.test(t + f))
    categories.push("treatment_care");
  if (/vital|observation/.test(t + f))
    categories.push("vitals");
  if (/allerg|hypersens/.test(t + f))
    categories.push("allergies");
  if (/immun|vaccine/.test(t + f))
    categories.push("immunizations");
  if (/consent|disclos|privacy/.test(t + f))
    categories.push("consent_disclosure");
  if (/seclus|restrain|incident|leave|acuit|detox/.test(t + f))
    categories.push("behavioral_health_specific");
  if (/stateform|florida|georgia|ohio|michigan|kansas|indiana|louisiana|wams|cimor|bhhf|ca_dcr/.test(t + f))
    categories.push("state_specific");
  if (/service_auth|fund_auth|member_auth|prov_auth|mso_service/.test(t))
    categories.push("service_authorization");
  if (/family|women|health_maint|amput|implant|surgical|hospital/.test(t + f))
    categories.push("health_history");
  if (/bed|room|movement|census/.test(t + f))
    categories.push("bed_management");
  if (/referral|transfer/.test(t + f))
    categories.push("referral_transfer");
  if (/staff|provider|team|nursing/.test(t + f))
    categories.push("staff_provider");

  if (categories.length === 0) categories.push("other");
  return categories;
}

const domainCounts: Record<string, number> = {};
const domainTables: Record<string, string[]> = {};
for (const t of tables) {
  const cats = categorize(t.table_name, t.form_name);
  for (const cat of cats) {
    domainCounts[cat] = (domainCounts[cat] || 0) + 1;
    if (!domainTables[cat]) domainTables[cat] = [];
    if (!domainTables[cat].includes(t.table_name)) {
      domainTables[cat].push(t.table_name);
    }
  }
}

// Column statistics
let totalColumns = 0;
let columnsWithDescription = 0;
let columnsWithMaxLength = 0;
for (const t of tables) {
  for (const c of t.columns) {
    totalColumns++;
    if (c.description) columnsWithDescription++;
    if (c.max_length !== null) columnsWithMaxLength++;
  }
}

const summary = {
  source_file: "EHI Export All Tables - September 2023.pdf",
  last_updated: "2023-09-27T16:00:00-04:00",
  total_table_entries: tables.length,
  unique_tables: uniqueTables.size,
  unique_forms: uniqueForms.size,
  total_columns: totalColumns,
  columns_with_description: columnsWithDescription,
  columns_with_max_length: columnsWithMaxLength,
  description_coverage_pct: Math.round((columnsWithDescription / totalColumns) * 100 * 10) / 10,
  schema_breakdown: Object.fromEntries(
    Object.entries(schemaBreakdown).sort((a, b) => b[1] - a[1])
  ),
  domain_table_counts: Object.fromEntries(
    Object.entries(domainCounts).sort((a, b) => b[1] - a[1])
  ),
  domain_unique_tables: Object.fromEntries(
    Object.entries(domainTables)
      .sort((a, b) => b[1].length - a[1].length)
      .map(([k, v]) => [k, { count: v.length, sample: v.slice(0, 5) }])
  ),
  parse_errors: parseErrors.length,
};

writeFileSync(outputPath, JSON.stringify(tables, null, 2));
writeFileSync(summaryPath, JSON.stringify(summary, null, 2));

console.log(`Parsed ${tables.length} table entries (${uniqueTables.size} unique tables)`);
console.log(`Total columns: ${totalColumns}`);
console.log(`Columns with descriptions: ${columnsWithDescription} (${summary.description_coverage_pct}%)`);
console.log(`Schema breakdown:`, schemaBreakdown);
console.log(`Output: ${outputPath}`);
console.log(`Summary: ${summaryPath}`);

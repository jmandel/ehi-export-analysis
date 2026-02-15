#!/usr/bin/env bun
/**
 * extract-tables.ts
 *
 * Parses the PCIS GOLD EHI Export Data Table Definitions HTML page and
 * extracts all table/field definitions into queryable JSON.
 *
 * Usage:  bun run extract-tables.ts
 * Input:  ../ehi-export-data-table-definitions.html
 * Output: ./tables.json          — full table+field definitions
 *         ./table-index.json     — table names, descriptions, field counts
 *         ./coverage-stats.json  — parsing statistics
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "ehi-export-data-table-definitions.html");
const html = readFileSync(inputPath, "utf-8");

interface Field {
  name: string;
  type: string;
  description: string;
}

interface TableDef {
  name: string;
  anchor: string;
  description: string;
  fields: Field[];
}

interface TableIndex {
  name: string;
  description: string;
  field_count: number;
}

interface CoverageStats {
  input_file: string;
  input_size_bytes: number;
  last_updated: string | null;
  total_h2_sections: number;
  total_tables_parsed: number;
  total_fields: number;
  parse_failures: Array<{ section: string; error: string }>;
  tables_with_no_fields: string[];
  field_type_distribution: Record<string, number>;
  domain_categories: Record<string, string[]>;
}

// Extract "Last Updated" timestamp
const lastUpdatedMatch = html.match(/Last Updated:\s*([^<]+)/);
const lastUpdated = lastUpdatedMatch ? lastUpdatedMatch[1].trim() : null;

// Split the HTML by <h2> tags to get each table section
// Pattern: <h2 id="linkTableName">TableName</h2>
const sectionRegex = /<h2\s+id="(link[^"]+)">([^<]+)<\/h2>/g;
const sections: Array<{ anchor: string; name: string; startIndex: number }> = [];

let match;
while ((match = sectionRegex.exec(html)) !== null) {
  sections.push({
    anchor: match[1],
    name: match[2].trim(),
    startIndex: match.index,
  });
}

const tables: TableDef[] = [];
const parseFailures: Array<{ section: string; error: string }> = [];
const tablesWithNoFields: string[] = [];

for (let i = 0; i < sections.length; i++) {
  const section = sections[i];
  const endIndex = i + 1 < sections.length ? sections[i + 1].startIndex : html.length;
  const sectionHtml = html.substring(section.startIndex, endIndex);

  try {
    // Extract description: first <p> after the h2
    const descMatch = sectionHtml.match(/<\/a>\s*\n?\s*<p>([^<]*)<\/p>/);
    const description = descMatch ? descMatch[1].trim() : "";

    // Extract fields from the table rows
    const fields: Field[] = [];
    // Skip the header row (first <tr> with <th>), then parse data rows
    const rowRegex = /<tr>\s*\n?\s*<td>([^<]*)<\/td>\s*\n?\s*<td>([^<]*)<\/td>\s*\n?\s*<td>([^<]*)<\/td>\s*\n?\s*<\/tr>/g;
    let rowMatch;
    while ((rowMatch = rowRegex.exec(sectionHtml)) !== null) {
      fields.push({
        name: rowMatch[1].trim(),
        type: rowMatch[2].trim(),
        description: rowMatch[3].trim(),
      });
    }

    if (fields.length === 0) {
      tablesWithNoFields.push(section.name);
    }

    tables.push({
      name: section.name,
      anchor: section.anchor,
      description,
      fields,
    });
  } catch (e: any) {
    parseFailures.push({
      section: section.name,
      error: e.message || String(e),
    });
  }
}

// Compute field type distribution
const typeDistribution: Record<string, number> = {};
for (const table of tables) {
  for (const field of table.fields) {
    const normalizedType = field.type.toLowerCase();
    typeDistribution[normalizedType] = (typeDistribution[normalizedType] || 0) + 1;
  }
}

// Categorize tables into data domains
function categorizeTable(name: string, desc: string): string {
  const n = name.toLowerCase();
  const d = desc.toLowerCase();
  if (n.startsWith("allergy_")) return "Allergy/Immunotherapy";
  if (n.startsWith("demo_")) return "Demographics";
  if (n.startsWith("lab_")) return "Laboratory";
  if (n.startsWith("etask_")) return "E-Tasking/Communication";
  if (n.startsWith("colbased_")) return "Custom/Column-Based Data";
  if (n.startsWith("t_vital") || n === "t_vitalsdata" || n.startsWith("t_vitalstemplate")) return "Vitals";
  if (n.startsWith("t_visit")) return "Visits/Encounters";
  if (n.startsWith("t_patient") && (n.includes("eye") || n.includes("refraction") || n.includes("iop") || n.includes("keratometry") || n.includes("visualacuity") || n.includes("contactlens") || n.includes("dilation") || n.includes("ocular"))) return "Ophthalmology/Eye Care";
  if (n.startsWith("t_eye")) return "Ophthalmology/Eye Care";
  if (n.startsWith("t_patientcancer")) return "Oncology/Cancer";
  if (n.startsWith("t_patientimmunization") || n === "t_immunizations" || n === "t_immunmanufacturer") return "Immunizations";
  if (n.startsWith("t_patientmedication") || n.startsWith("t_patienterx") || n === "t_patientrxhistory" || n === "t_patientprintrxdetails") return "Medications/Prescriptions";
  if (n.startsWith("t_patientfamily")) return "Family History";
  if (n.startsWith("t_familyhistory")) return "Family History";
  if (n.startsWith("t_patientreferral") || n === "referrals" || n === "referrals_reps" || n === "t_referraltypes") return "Referrals";
  if (n.startsWith("t_patientalert") || n.startsWith("t_patientallergy")) return "Allergies/Alerts";
  if (n.startsWith("t_recall") || n === "patientrecalls") return "Recalls";
  if (n.startsWith("t_ordertracking") || n === "orders" || n === "orders_reps") return "Orders";
  if (n.startsWith("t_hri")) return "Health Record Items";
  if (n.startsWith("t_flowsheet")) return "Flowsheets";
  if (n.startsWith("t_scribble")) return "Scribble/Drawing Notes";
  if (n.startsWith("problem_")) return "Problem List";
  if (n.startsWith("screening") || n === "patientscreening" || n === "patientscreeninganswer") return "Screening/Assessment";
  if (n.startsWith("toc_")) return "Transitions of Care";
  if (n.startsWith("statement") || n.startsWith("dunning") || n === "paymentplans" || n.startsWith("allocated") || n === "trans" || n === "trans_reps") return "Billing/Financial";
  if (n.startsWith("claim") || n.startsWith("eobrecs") || n.startsWith("estimate")) return "Billing/Financial";
  if (n === "accounts" || n === "accounts_reps" || n.startsWith("acctalert") || n.startsWith("acctnote")) return "Accounts";
  if (n.startsWith("inforelease")) return "Information Release";
  if (n.startsWith("t_blob")) return "Documents/Attachments";
  if (n.startsWith("t_fax")) return "Fax";
  if (n.startsWith("t_patient")) return "Patient Clinical Data";
  if (n.startsWith("t_")) return "System/Reference";
  if (n.startsWith("task")) return "Tasks";
  if (n.startsWith("midmark")) return "Device Integration (Midmark)";
  if (n === "patientformsresponse" || n === "patientformresponsequestions" || n === "patientformresponse") return "Patient Forms";
  if (n === "patients" || n === "patients_reps" || n === "patienthipaa") return "Patient Administrative";
  if (n === "panels" || n === "patientpanels") return "Panels";
  if (n === "visits" || n === "visits_reps") return "Visits/Encounters";
  if (n === "miscaddress") return "Addresses";
  if (n === "patientnotes" || n === "patientnotes_reps") return "Patient Notes";
  if (n === "recordrequest_methods") return "Record Requests";
  return "Other";
}

const domainCategories: Record<string, string[]> = {};
for (const table of tables) {
  const category = categorizeTable(table.name, table.description);
  if (!domainCategories[category]) domainCategories[category] = [];
  domainCategories[category].push(table.name);
}

// Build outputs
const tableIndex: TableIndex[] = tables.map((t) => ({
  name: t.name,
  description: t.description,
  field_count: t.fields.length,
}));

const totalFields = tables.reduce((sum, t) => sum + t.fields.length, 0);

const coverageStats: CoverageStats = {
  input_file: "ehi-export-data-table-definitions.html",
  input_size_bytes: Buffer.byteLength(html, "utf-8"),
  last_updated: lastUpdated,
  total_h2_sections: sections.length,
  total_tables_parsed: tables.length,
  total_fields: totalFields,
  parse_failures: parseFailures,
  tables_with_no_fields: tablesWithNoFields,
  field_type_distribution: Object.fromEntries(
    Object.entries(typeDistribution).sort((a, b) => b[1] - a[1])
  ),
  domain_categories: Object.fromEntries(
    Object.entries(domainCategories).sort((a, b) => b[1].length - a[1].length)
  ),
};

// Write outputs
writeFileSync(join(scriptDir, "tables.json"), JSON.stringify(tables, null, 2));
writeFileSync(join(scriptDir, "table-index.json"), JSON.stringify(tableIndex, null, 2));
writeFileSync(join(scriptDir, "coverage-stats.json"), JSON.stringify(coverageStats, null, 2));

// Summary to stdout
console.log("=== PCIS GOLD EHI Export Data Dictionary Extraction ===");
console.log(`Input: ${inputPath}`);
console.log(`Last Updated: ${lastUpdated}`);
console.log(`Tables parsed: ${tables.length}`);
console.log(`Total fields: ${totalFields}`);
console.log(`Parse failures: ${parseFailures.length}`);
console.log(`Tables with no fields: ${tablesWithNoFields.length}`);
console.log(`\nDomain categories:`);
for (const [cat, tbls] of Object.entries(domainCategories).sort((a, b) => b[1].length - a[1].length)) {
  console.log(`  ${cat}: ${tbls.length} tables`);
}
console.log(`\nField type distribution:`);
for (const [type, count] of Object.entries(typeDistribution).sort((a, b) => b[1] - a[1])) {
  console.log(`  ${type}: ${count}`);
}
console.log(`\nOutput files written to: ${scriptDir}`);

#!/usr/bin/env bun
/**
 * Parses the CareLogic EHI Export Data Dictionary XLS into structured JSON.
 * Produces:
 *   entity-inventory-full.json   — complete extraction of all tables and fields
 *   entity-inventory-summary.json — aggregate statistics and domain breakdowns
 */

import XLSX from "xlsx";
import { writeFileSync } from "fs";
import { resolve, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = resolve(scriptDir, "..", "downloads", "CareLogic_EHI_Export_Data_Dictionary.xls");

// Read workbook
const wb = XLSX.readFile(inputPath);
console.log("Sheet names:", wb.SheetNames);
const ws = wb.Sheets[wb.SheetNames[0]];
const rows: any[][] = XLSX.utils.sheet_to_json(ws, { header: 1 });
console.log(`Total rows in spreadsheet: ${rows.length}`);

// Show header row
console.log("Header row:", rows[0]);
// Show a few sample rows
for (let i = 1; i < Math.min(10, rows.length); i++) {
  console.log(`Row ${i}:`, JSON.stringify(rows[i]));
}

interface Field {
  name: string;
  description: string;
  data_type: string | null;
}

interface Table {
  name: string;
  description: string;
  columns: Field[];
  domain: string;
}

// Parse tables: col A = table name, col B = table description, col C = column name, col D = column description, col E = data type
const tables: Table[] = [];
let current: { name: string; description: string; columns: Field[] } | null = null;

for (let i = 1; i < rows.length; i++) {
  const row = rows[i];
  if (!row || row.length === 0) continue;
  
  const colA = row[0] ? String(row[0]).trim() : "";
  const colB = row[1] ? String(row[1]).trim() : "";
  const colC = row[2] ? String(row[2]).trim() : "";
  const colD = row[3] ? String(row[3]).trim() : "";
  const colE = row[4] ? String(row[4]).trim() : "";

  if (colA) {
    // New table
    if (current) tables.push({ ...current, domain: "" });
    current = {
      name: colA,
      description: colB,
      columns: [],
    };
    // If this row also has column data in cols C-E, add it
    if (colC) {
      current.columns.push({
        name: colC,
        description: colD,
        data_type: colE || null,
      });
    }
  } else if (colC && current) {
    // Column row for current table
    current.columns.push({
      name: colC,
      description: colD,
      data_type: colE || null,
    });
  }
}
if (current) tables.push({ ...current, domain: "" });

console.log(`\nParsed ${tables.length} tables`);
const totalFields = tables.reduce((s, t) => s + t.columns.length, 0);
console.log(`Total fields: ${totalFields}`);

// Domain categorization
function categorize(name: string): string {
  const n = name.toUpperCase();
  
  // Demographics & Patient Identity
  if (/^CLIENT_DEMO|^CLIENT_NAME|^CLIENT_MISC|^CLIENT_PICTURE|^CLIENT_ADDRESS|^CLIENT_CONTACT|^CLIENT_RELATIONSHIP|^CLIENT_SSN|^CLIENT_MARITAL|^CLIENT_RACE|^CLIENT_ETHNICITY|^CLIENT_LANGUAGE/.test(n)) return "Demographics & Contacts";
  
  // Program Enrollment
  if (/^CLIENT_PROGRAM|^CLIENT_EPISODE|^CLIENT_STAFF|^CLIENT_GROUP(?!_ACTIV)|^CLIENT_REGULATION/.test(n)) return "Program Enrollment";
  
  // Insurance & Client Billing
  if (/^CLIENT_PAYER|^CLIENT_GUARANTOR|^CLIENT_BALANCE|^CLIENT_LIABILITY|^CLIENT_SLIDING|^CLIENT_SERVICE_CHARGE|^CLIENT_ASSIST/.test(n)) return "Insurance & Client Billing";
  
  // Billing & Claims
  if (/^ACTIVITY_DETAIL|^CLAIM_|^COLLECTION_|^CS_BATCH|^GL_DETAIL|^EDI_835|^EDI_270|^FFS_|^STMT_|^CASH_SHEET|^BILLING_|^REMIT_/.test(n)) return "Billing & Claims";
  
  // Service Documents & Assessments
  if (/^DOCUMENT|^ADDENDUM|^MOD_/.test(n)) return "Service Documents & Assessments";
  
  // Medications & Allergies
  if (/^ALLERGY|^ERX_|^CLINICIAN_ALLERGY|^CLINICIAN_ORD_MED|^MEDICATION|^MED_RECON|^CLIENT_MED_ALLERGY|^CLIENT_ALLERGY|^CLIENT_MEDICATION/.test(n)) return "Medications & Allergies";
  
  // eMAR
  if (/^ACKNOWLEDGE_MED|^MAR_/.test(n)) return "Medication Administration (eMAR)";
  
  // Clinical Decision Support
  if (/^CLINICAL_RECON|^CXDECISION/.test(n)) return "Clinical Decision Support";
  
  // Diagnoses
  if (/^DIAGNOSIS|^CLIENT_PROGRAM_CODE|^CLIENT_EXTERNAL_DIAG/.test(n)) return "Diagnoses";
  
  // Clinical Document Exchange
  if (/^CCD_|^CCDA_|^EXT_MSG/.test(n)) return "Clinical Document Exchange";
  
  // HL7 / ADT
  if (/^ADT_|^HL7_/.test(n)) return "HL7 / ADT Events";
  
  // Inpatient / Bed Management
  if (/^BED_/.test(n)) return "Inpatient / Bed Management";
  
  // DWI / Substance Abuse
  if (/^DWI_/.test(n)) return "DWI / Substance Abuse";
  
  // State Programs
  if (/^HAP_|^MACSIS_/.test(n)) return "State Programs";
  
  // Intake & Referral
  if (/^INTAKE_|^APPOINTMENT_TRACK|^CLIENT_SRL/.test(n)) return "Intake & Referral";
  
  // Task Management
  if (/^TASK_LIST/.test(n)) return "Task Management";
  
  // Alerts
  if (/^ALERT|^MOB_ALERT/.test(n)) return "Alerts & Notifications";
  
  // Messaging
  if (/^MESSAGE/.test(n)) return "Internal Messaging";
  
  // Provider & Pharmacy Relationships
  if (/^CLIENT_PHARMACY|^CLIENT_PCP|^CLIENT_PROVIDER|^CLIENT_REL_REF/.test(n)) return "Provider & Pharmacy";
  
  // Consent
  if (/^CLIENT_CONSENT/.test(n)) return "Consent Records";
  
  // Pregnancy
  if (/^CLIENT_PREGNANCY/.test(n)) return "Pregnancy Records";
  
  // Document Management
  if (/^CLIENT_SCANNED|^CLIENT_ATTACHMENT|^CLIENT_RECORD_INV|^SCANNED_DOCUMENT|^STAFF_SCANNED/.test(n)) return "Document Management";
  
  // Payments
  if (/^PAYMENT_|^REFUND/.test(n)) return "Payments";
  
  // Authorizations
  if (/^CLIENT_AUTH_/.test(n)) return "Authorizations";
  
  // Portal Access
  if (/^PORTAL_|^MY_HEALTH_|^PAT_ED_RESOURCE/.test(n)) return "Portal & Patient Access";
  
  // Staff / Payroll
  if (/^STAFF_|^PAYROLL_/.test(n)) return "Staff & Payroll";
  
  // Configurable Forms
  if (/^CF_/.test(n)) return "Configurable Forms";
  
  // Quality Measures
  if (/^CQM_|^CRG_/.test(n)) return "Quality Measures";
  
  // Implantable Devices
  if (/^IMPLANTABLE_DEVICE/.test(n)) return "Implantable Devices";
  
  // Inventory
  if (/^INVENTORY_/.test(n)) return "Inventory";
  
  // State Reporting (broader)
  if (/^IL_REG|^GA_CSU|^ADMIN_SR|^SR_|^SRBD_|^STATE_REPORTING/.test(n)) return "State Reporting";
  
  // Audit & Access
  if (/^AUDIT_|^DEBUG|^API_ACCESS|^CLIENT_VIEW/.test(n)) return "Audit & Access";
  
  // Service Document Config
  if (/^SVCDOC_|^TPG_/.test(n)) return "Service Document Config";
  
  // Education & Employment
  if (/^EDU_/.test(n)) return "Education & Employment";
  
  // Encounters
  if (/^ENCOUNTER_/.test(n)) return "Encounter Details";
  
  // Waiver/Authorization
  if (/^WV_/.test(n)) return "Waiver / Authorization";
  
  // Orders (all ORD_* and ORDER_*)
  if (/^CSO_ORDER|^ORD_|^ORDER_/.test(n)) return "Orders";
  
  // Mobile Sync
  if (/^MOB_SYNC/.test(n)) return "Mobile Sync";
  
  // DD/IDD Services
  if (/^CLIENT_DD_|^CLIENT_UMDAP/.test(n)) return "DD/IDD Services";
  
  // Client Access & Follow-up
  if (/^CLIENT_BLACK_BOX|^CLIENT_CACS/.test(n)) return "Client Access & Follow-up";
  
  // Client Messages
  if (/^CLIENT_MESSAGE/.test(n)) return "Client Messages";
  
  // Group Activities
  if (/^CLIENT_GROUP_ACTIV|^GROUP_ACTIVITY/.test(n)) return "Group Activities";
  
  // Immunizations
  if (/^IMMUNIZATION|^CLIENT_IMMUNIZATION/.test(n)) return "Immunizations";
  
  // Vitals / Lab
  if (/^VITAL|^LAB_/.test(n)) return "Vitals & Lab";
  
  // Treatment Plan
  if (/^TREATMENT_PLAN|^TP_/.test(n)) return "Treatment Plans";
  
  // Auto Processing
  if (/^AUTO_PROCESS/.test(n)) return "Auto-Processing";
  
  // MICP
  if (/^MICP_/.test(n)) return "MICP Integration";
  
  // Administration
  if (/^ADMIN_/.test(n)) return "Administration";
  
  // Case Audit
  if (/^CASE_AUDIT/.test(n)) return "Case Audit";
  
  return "Other / Uncategorized";
}

// Apply domain categorization
for (const t of tables) {
  t.domain = categorize(t.name);
}

// Build full inventory
const fullInventory = {
  source_file: "CareLogic_EHI_Export_Data_Dictionary.xls",
  extraction_date: new Date().toISOString().split("T")[0],
  total_tables: tables.length,
  total_fields: totalFields,
  tables: tables.map(t => ({
    name: t.name,
    description: t.description,
    domain: t.domain,
    field_count: t.columns.length,
    fields: t.columns.map(c => ({
      name: c.name,
      description: c.description,
      data_type: c.data_type,
      has_description: c.description.length > 0,
    })),
  })),
};

writeFileSync(resolve(scriptDir, "entity-inventory-full.json"), JSON.stringify(fullInventory, null, 2));

// Build summary
const fieldsWithDescriptions = tables.reduce((s, t) => s + t.columns.filter(c => c.description.length > 0).length, 0);
const fieldsWithTypes = tables.reduce((s, t) => s + t.columns.filter(c => c.data_type !== null).length, 0);
const tablesWithDescriptions = tables.filter(t => t.description.length > 0).length;
const tablesWithNoColumns = tables.filter(t => t.columns.length === 0);

// Domain breakdown
const domainBreakdown: Record<string, { table_count: number; field_count: number; fields_with_descriptions: number; tables: string[] }> = {};
for (const t of tables) {
  if (!domainBreakdown[t.domain]) {
    domainBreakdown[t.domain] = { table_count: 0, field_count: 0, fields_with_descriptions: 0, tables: [] };
  }
  domainBreakdown[t.domain].table_count++;
  domainBreakdown[t.domain].field_count += t.columns.length;
  domainBreakdown[t.domain].fields_with_descriptions += t.columns.filter(c => c.description.length > 0).length;
  domainBreakdown[t.domain].tables.push(t.name);
}

// Sort by field count descending
const sortedDomains = Object.entries(domainBreakdown)
  .sort(([, a], [, b]) => b.field_count - a.field_count);

// Top 20 largest tables
const top20 = [...tables].sort((a, b) => b.columns.length - a.columns.length).slice(0, 20);

const summary = {
  source_file: "CareLogic_EHI_Export_Data_Dictionary.xls",
  extraction_date: new Date().toISOString().split("T")[0],
  totals: {
    tables: tables.length,
    fields: totalFields,
    tables_with_descriptions: tablesWithDescriptions,
    tables_without_descriptions: tables.length - tablesWithDescriptions,
    fields_with_descriptions: fieldsWithDescriptions,
    fields_without_descriptions: totalFields - fieldsWithDescriptions,
    fields_with_types: fieldsWithTypes,
    description_coverage_pct: Math.round((fieldsWithDescriptions / totalFields) * 1000) / 10,
    type_coverage_pct: Math.round((fieldsWithTypes / totalFields) * 1000) / 10,
  },
  tables_with_no_columns: tablesWithNoColumns.map(t => t.name),
  tables_without_descriptions: tables.filter(t => t.description.length === 0).map(t => t.name),
  domain_breakdown: Object.fromEntries(sortedDomains.map(([domain, stats]) => [domain, {
    table_count: stats.table_count,
    field_count: stats.field_count,
    fields_with_descriptions: stats.fields_with_descriptions,
    description_pct: Math.round((stats.fields_with_descriptions / Math.max(stats.field_count, 1)) * 1000) / 10,
    tables: stats.tables.sort(),
  }])),
  top_20_tables_by_field_count: top20.map(t => ({
    name: t.name,
    domain: t.domain,
    field_count: t.columns.length,
    described_fields: t.columns.filter(c => c.description.length > 0).length,
  })),
};

writeFileSync(resolve(scriptDir, "entity-inventory-summary.json"), JSON.stringify(summary, null, 2));

console.log("\n=== SUMMARY ===");
console.log(`Tables: ${tables.length}`);
console.log(`Fields: ${totalFields}`);
console.log(`Tables with descriptions: ${tablesWithDescriptions} / ${tables.length}`);
console.log(`Fields with descriptions: ${fieldsWithDescriptions} / ${totalFields} (${summary.totals.description_coverage_pct}%)`);
console.log(`Fields with types: ${fieldsWithTypes} / ${totalFields} (${summary.totals.type_coverage_pct}%)`);
console.log(`Tables with no columns: ${tablesWithNoColumns.length}`);
console.log(`\nDomain breakdown:`);
for (const [domain, stats] of sortedDomains) {
  console.log(`  ${domain}: ${stats.table_count} tables, ${stats.field_count} fields`);
}
console.log(`\nTop 10 largest tables:`);
for (const t of top20.slice(0, 10)) {
  console.log(`  ${t.name}: ${t.columns.length} fields (${t.domain})`);
}

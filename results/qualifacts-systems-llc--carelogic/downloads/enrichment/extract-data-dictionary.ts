#!/usr/bin/env bun
/**
 * Extracts CareLogic EHI Export Data Dictionary from XLS into queryable JSON.
 *
 * Input:  ../CareLogic_EHI_Export_Data_Dictionary.xls
 * Output: data-dictionary.json   — full structured extraction
 *         coverage-report.json   — parsing stats and domain categorization
 */

import { readFileSync, writeFileSync } from "fs";
import { resolve, dirname } from "path";
import XLSX from "xlsx";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = resolve(scriptDir, "..", "CareLogic_EHI_Export_Data_Dictionary.xls");
const outputPath = resolve(scriptDir, "data-dictionary.json");
const coveragePath = resolve(scriptDir, "coverage-report.json");

interface Column {
  name: string;
  description: string;
  data_type: string | null;
}

interface Table {
  name: string;
  description: string;
  columns: Column[];
}

// Read workbook
const wb = XLSX.readFile(inputPath);
const ws = wb.Sheets[wb.SheetNames[0]];
const rows: any[][] = XLSX.utils.sheet_to_json(ws, { header: 1 });

// Parse tables
const tables: Table[] = [];
let current: Table | null = null;

for (let i = 1; i < rows.length; i++) {
  const row = rows[i];
  if (row[0]) {
    // New table row
    if (current) tables.push(current);
    current = {
      name: String(row[0]).trim(),
      description: String(row[1] || "").trim(),
      columns: [],
    };
  } else if (row[2] && current) {
    // Column row
    current.columns.push({
      name: String(row[2]).trim(),
      description: String(row[3] || "").trim(),
      data_type: row[4] ? String(row[4]).trim() : null,
    });
  }
}
if (current) tables.push(current);

// Domain categorization rules
const domainRules: [RegExp, string][] = [
  [/^CLIENT_DEMO|^CLIENT_NAME|^CLIENT_MISC|^CLIENT_PICTURE|^CLIENT_ADDRESS|^CLIENT_CONTACT|^CLIENT_RELATIONSHIP/i, "Demographics & Contacts"],
  [/^CLIENT_PROGRAM|^CLIENT_EPISODE|^CLIENT_STAFF|^CLIENT_GROUP|^CLIENT_REGULATION/i, "Program Enrollment"],
  [/^CLIENT_PAYER|^CLIENT_GUARANTOR|^CLIENT_BALANCE|^CLIENT_LIABILITY|^CLIENT_SLIDING|^CLIENT_SERVICE_CHARGE|^CLIENT_ASSIST/i, "Insurance & Billing (Client)"],
  [/^ACTIVITY_DETAIL|^CLAIM_|^COLLECTION_|^CS_BATCH|^GL_DETAIL|^EDI_835|^EDI_270|^FFS_|^STMT_|^CASH_SHEET/i, "Billing & Claims"],
  [/^DOCUMENT|^ADDENDUM|^MOD_/i, "Service Documents & Assessments"],
  [/^ALLERGY|^ERX_|^CLINICIAN_ALLERGY|^CLINICIAN_ORD_MED|^MEDICATION|^MED_RECON|^CLIENT_MED_ALLERGY|^CLIENT_ALLERGY|^CLIENT_MEDICATION/i, "Medications & Allergies"],
  [/^ACKNOWLEDGE_MED|^MAR_/i, "Medication Administration (eMAR)"],
  [/^CLINICAL_RECON|^CXDECISION/i, "Clinical Decision Support"],
  [/^DIAGNOSIS|^CLIENT_PROGRAM_CODE|^CLIENT_EXTERNAL_DIAG/i, "Diagnoses"],
  [/^CCD_|^CCDA_|^EXT_MSG/i, "Clinical Document Exchange (CCD/C-CDA)"],
  [/^ADT_|^HL7_/i, "HL7 / ADT Events"],
  [/^BED_/i, "Inpatient / Bed Management"],
  [/^DWI_/i, "DWI / Substance Abuse Programs"],
  [/^HAP_|^MACSIS_/i, "State Programs (HAP/Enrollment)"],
  [/^INTAKE_|^APPOINTMENT_TRACK|^CLIENT_SRL/i, "Intake & Referral Tracking"],
  [/^TASK_LIST/i, "Task Management"],
  [/^ALERT|^MOB_ALERT/i, "Alerts & Notifications"],
  [/^MESSAGE/i, "Internal Messaging"],
  [/^CLIENT_PHARMACY|^CLIENT_PCP|^CLIENT_PROVIDER|^CLIENT_REL_REF/i, "Provider & Pharmacy Relationships"],
  [/^CLIENT_CONSENT/i, "Consent Records"],
  [/^CLIENT_PREGNANCY/i, "Pregnancy Records"],
  [/^CLIENT_SCANNED|^CLIENT_ATTACHMENT|^CLIENT_RECORD_INV/i, "Document Management"],
  [/^CF_/i, "Configurable Forms"],
  [/^CQM_|^CRG_/i, "Quality Measures"],
  [/^IMPLANTABLE_DEVICE/i, "Implantable Devices"],
  [/^INVENTORY_/i, "Inventory"],
  [/^IL_REG|^GA_CSU|^ADMIN_SR/i, "State Reporting"],
  [/^AUDIT_|^DEBUG|^API_ACCESS|^CLIENT_VIEW/i, "Audit & Access Logging"],
  [/^AUTO_PROCESS/i, "Auto-Processing Rules"],
  [/^SVCDOC_|^TPG_/i, "Service Document Config"],
  [/^EDU_/i, "Education & Employment"],
  [/^ENCOUNTER_/i, "Encounter Details"],
  [/^WV_/i, "Waiver/Authorization (WV)"],
  [/^CSO_ORDER/i, "Orders"],
  [/^MOB_SYNC/i, "Mobile Sync"],
  [/^MICP_/i, "MICP Integration"],
  [/^ADMIN_/i, "Administration"],
  [/^CASE_AUDIT/i, "Case Audit"],
  [/^CLIENT_DD_|^CLIENT_UMDAP/i, "DD/IDD Services"],
  [/^CLIENT_BLACK_BOX|^CLIENT_CACS/i, "Client Access & Follow-up"],
  [/^CLIENT_MESSAGE/i, "Client Messages"],
];

function categorize(tableName: string): string {
  for (const [pattern, domain] of domainRules) {
    if (pattern.test(tableName)) return domain;
  }
  return "Other / Uncategorized";
}

// Build domain summary
const domainMap = new Map<string, string[]>();
for (const t of tables) {
  const domain = categorize(t.name);
  if (!domainMap.has(domain)) domainMap.set(domain, []);
  domainMap.get(domain)!.push(t.name);
}

const domainSummary = Object.fromEntries(
  [...domainMap.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([domain, tableNames]) => [domain, {
      table_count: tableNames.length,
      tables: tableNames.sort(),
    }])
);

// Write outputs
const dataDictionary = {
  source_file: "CareLogic_EHI_Export_Data_Dictionary.xls",
  extracted_at: new Date().toISOString(),
  total_tables: tables.length,
  total_columns: tables.reduce((sum, t) => sum + t.columns.length, 0),
  tables: tables.map(t => ({
    ...t,
    domain: categorize(t.name),
  })),
};

writeFileSync(outputPath, JSON.stringify(dataDictionary, null, 2));
console.log(`Wrote ${outputPath}`);
console.log(`  ${tables.length} tables, ${dataDictionary.total_columns} columns`);

const coverageReport = {
  source_file: "CareLogic_EHI_Export_Data_Dictionary.xls",
  extracted_at: new Date().toISOString(),
  total_rows_in_xls: rows.length,
  total_tables_parsed: tables.length,
  total_columns_parsed: dataDictionary.total_columns,
  tables_with_no_columns: tables.filter(t => t.columns.length === 0).map(t => t.name),
  tables_with_no_description: tables.filter(t => !t.description).map(t => t.name),
  parse_failures: [],
  domain_summary: domainSummary,
};

writeFileSync(coveragePath, JSON.stringify(coverageReport, null, 2));
console.log(`Wrote ${coveragePath}`);
console.log(`  Domains: ${domainMap.size}`);
console.log(`  Tables with no columns: ${coverageReport.tables_with_no_columns.length}`);
console.log(`  Tables with no description: ${coverageReport.tables_with_no_description.length}`);

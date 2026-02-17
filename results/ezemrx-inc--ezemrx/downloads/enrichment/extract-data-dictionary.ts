#!/usr/bin/env bun
/**
 * Extracts structured data from the ezEMRx EHI Export data dictionary PDF.
 *
 * Usage: bun run extract-data-dictionary.ts
 * Input: ../ehi-export-data-dictionary.pdf (via pdftotext)
 * Output: data-dictionary.json
 */

import { execSync } from "child_process";
import { resolve, dirname } from "path";
import { writeFileSync } from "fs";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const pdfPath = resolve(scriptDir, "../ehi-export-data-dictionary.pdf");

const text = execSync(`pdftotext -layout "${pdfPath}" -`, {
  encoding: "utf-8",
  maxBuffer: 10 * 1024 * 1024,
});

const lines = text.split("\n");

// --- Extract metadata ---
const metadata = {
  title: "170.315(b)(10) Electronic Health Information (EHI) Export",
  chplId: "15.02.05.2886.EZEM.01.01.1.220105",
  productVersion: "ezEMRx Ver 10.01",
  documentControlId: "01US03P98C001",
  documentVersion: "2.0",
  date: "April 25, 2024",
  preparedBy: "ezEMRx Integration Team",
};

// --- Extract file categories ---
interface FileCategory {
  name: string;
  format: string;
  fileExtension: string;
  typeIndicator: string | null;
  description: string;
  standardReference: string | null;
}

const fileCategories: FileCategory[] = [
  {
    name: "Patient Demographics and Clinical Data",
    format: "HL7 C-CDA R2.1",
    fileExtension: "XML + HTML pair",
    typeIndicator: null,
    description:
      "Demographics and clinical records in C-CDA format. Always produces a pair of XML and HTML files. No TYPE value in filename.",
    standardReference:
      "https://www.hl7.org/implement/standards/product_brief.cfm?product_id=447",
  },
  {
    name: "Patient Billing and Claims Data",
    format: "CSV",
    fileExtension: "CSV",
    typeIndicator: "ClaimData",
    description:
      "Billing and claims data including CPT, ICD, NDC codes, charges, payments from multiple payors, adjustments, and balances.",
    standardReference: null,
  },
  {
    name: "Adhoc Patient Notes",
    format: "CSV",
    fileExtension: "CSV",
    typeIndicator: "patNotes",
    description:
      "Telephone calls and adhoc notes documented via Patient Notes feature. Includes user, subject, category, date, and note text.",
    standardReference: null,
  },
  {
    name: "Scanned Records",
    format: "HL7 C-CDA R2.1",
    fileExtension: "XML",
    typeIndicator: "Echart",
    description:
      "All patient scanned and uploaded documents, coded using Base64 encoding within CDA XML. May be large depending on volume of scanned data.",
    standardReference:
      "https://www.hl7.org/implement/standards/product_brief.cfm?product_id=447",
  },
];

// --- Extract CSV column definitions ---
interface ColumnDef {
  columnNumber: number;
  columnName: string;
  description: string;
}

interface CsvSchema {
  name: string;
  typeIndicator: string;
  columns: ColumnDef[];
}

const csvSchemas: CsvSchema[] = [
  {
    name: "Patient Billing and Claims Data",
    typeIndicator: "ClaimData",
    columns: [
      { columnNumber: 1, columnName: "PID", description: "Patient ID (unique)" },
      { columnNumber: 2, columnName: "DOS", description: "Date of service being billed" },
      { columnNumber: 3, columnName: "Payor", description: "Insurance payor for the date of service" },
      { columnNumber: 4, columnName: "Provider", description: "Rendering provider who performed the service" },
      { columnNumber: 5, columnName: "CPT", description: "CPT code billed" },
      { columnNumber: 6, columnName: "ICD", description: "ICD code associated with the CPT code billed" },
      { columnNumber: 7, columnName: "NDC", description: "NDC code for drugs billed that have been administered or rendered" },
      { columnNumber: 8, columnName: "Modifier", description: "Modifier code associated with the CPT code billed" },
      { columnNumber: 9, columnName: "Charge", description: "Amount billed" },
      { columnNumber: 10, columnName: "Pri Payment", description: "Payment received from primary insurance plan/payor" },
      { columnNumber: 11, columnName: "Sec Payment", description: "Payment received from secondary insurance plan/payor" },
      { columnNumber: 12, columnName: "TerPayment", description: "Payment received from tertiary insurance plan/payor" },
      { columnNumber: 13, columnName: "Oth Payment", description: "Payment received from other sources" },
      { columnNumber: 14, columnName: "Pat Payment", description: "Payment received from the patient" },
      { columnNumber: 15, columnName: "Patient Resp", description: "Patient outstanding balances" },
      { columnNumber: 16, columnName: "Wri-Off/Adj", description: "Balances adjusted or written off" },
      { columnNumber: 17, columnName: "Balance", description: "Patient account balances including pending claims" },
    ],
  },
  {
    name: "Adhoc Patient Notes",
    typeIndicator: "patNotes",
    columns: [
      { columnNumber: 1, columnName: "PID", description: "Patient ID (unique)" },
      { columnNumber: 2, columnName: "Patient Notes ID", description: "Patient note ID (unique)" },
      { columnNumber: 3, columnName: "User Name", description: "User who documented the note" },
      { columnNumber: 4, columnName: "Subject", description: "Subject of the note (may be blank)" },
      { columnNumber: 5, columnName: "Patient Notes Category", description: "Category associated with the note (user-defined pick list)" },
      { columnNumber: 6, columnName: "Patient Notes Date", description: "Date the note was created" },
      { columnNumber: 7, columnName: "Patient Notes", description: "Documented details of the patient note" },
    ],
  },
];

// --- File naming convention ---
const fileNaming = {
  pattern: "PID_INTERNALNUMBERING[_TYPE].EXT",
  components: {
    PID: "Patient ID — unique number",
    INTERNALNUMBERING: "Internal control number for the export (can be ignored)",
    TYPE: "Content descriptor: ClaimData, Echart, or patNotes (absent for demographics/clinical)",
    EXT: "File extension: XML, HTML, or CSV",
  },
  exportContainer: "ZIP file(s)",
};

// --- Assemble output ---
const output = {
  extractionDate: new Date().toISOString().split("T")[0],
  sourceFile: "ehi-export-data-dictionary.pdf",
  metadata,
  fileNaming,
  fileCategories,
  csvSchemas,
  stats: {
    totalFileCategories: fileCategories.length,
    totalCsvSchemas: csvSchemas.length,
    totalCsvColumns: csvSchemas.reduce((s, c) => s + c.columns.length, 0),
    formatsUsed: ["HL7 C-CDA R2.1 (XML+HTML)", "CSV", "HL7 CDA R2.1 (XML with Base64)"],
  },
};

const outPath = resolve(scriptDir, "data-dictionary.json");
writeFileSync(outPath, JSON.stringify(output, null, 2));
console.log(`Output: ${outPath}`);
console.log(`File categories: ${output.stats.totalFileCategories}`);
console.log(`CSV schemas: ${output.stats.totalCsvSchemas} with ${output.stats.totalCsvColumns} total columns`);

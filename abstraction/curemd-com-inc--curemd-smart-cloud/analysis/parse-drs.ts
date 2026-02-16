/**
 * Parse CureMD EHI_Export_DRS.xlsx into entity-inventory-full.json and entity-inventory-summary.json.
 * Reads the raw XLSX, extracts both sheets, and produces complete field-level inventory.
 */
import * as XLSX from "xlsx";
import { writeFileSync } from "fs";

const wb = XLSX.readFile("../downloads/EHI_Export_DRS.xlsx");

// Parse the overview sheet
const overviewSheet = wb.Sheets["EHI Export"];
const overviewData = XLSX.utils.sheet_to_json(overviewSheet, { header: 1 }) as any[][];
const overviewText = overviewData
  .filter((row) => row.some((cell) => cell != null && String(cell).trim() !== ""))
  .map((row) => row.filter((c) => c != null).join(" | "))
  .join("\n");

// Parse the DRS sheet
const drsSheet = wb.Sheets["DRS"];
const drsData = XLSX.utils.sheet_to_json(drsSheet, { header: 1 }) as any[][];

// Header row is row 0
const headers = drsData[0].map((h: any) => String(h).trim());
console.log("Headers:", headers);

interface Field {
  name: string;
  dataType: string;
  description: string;
  hasDescription: boolean;
}

interface DataClass {
  name: string;
  fields: Field[];
  isSpecial: boolean; // For "Documents & Images" and "Provider Notes" which have no tabular fields
  specialNote?: string;
}

const dataClasses: DataClass[] = [];
let currentClassName = "";

for (let i = 1; i < drsData.length; i++) {
  const row = drsData[i];
  if (!row || row.every((c: any) => c == null || String(c).trim() === "")) continue;

  // Column A = Data Class, Column B = Field Name, Column C = Data Type, Column D = Description
  const classCell = row[0] != null ? String(row[0]).trim().replace(/\r\n/g, " ").replace(/\n/g, " ") : "";
  const fieldName = row[1] != null ? String(row[1]).trim() : "";
  const dataType = row[2] != null ? String(row[2]).trim() : "";
  const description = row[3] != null ? String(row[3]).trim() : "";

  if (classCell) {
    currentClassName = classCell;
  }

  if (!currentClassName) continue;

  // Find or create the data class
  let dc = dataClasses.find((d) => d.name === currentClassName);
  if (!dc) {
    dc = { name: currentClassName, fields: [], isSpecial: false };
    dataClasses.push(dc);
  }

  // Check for special entries (no real fields)
  if (fieldName === "-" || fieldName === "") {
    if (description && description !== "-") {
      dc.isSpecial = true;
      dc.specialNote = description;
    }
    continue;
  }

  dc.fields.push({
    name: fieldName,
    dataType: dataType || "unknown",
    description: description,
    hasDescription: description !== "" && description !== "-",
  });
}

// Build full inventory
const fullInventory = {
  source: "CureMD EHI_Export_DRS.xlsx",
  extractedAt: new Date().toISOString(),
  overviewText,
  totalDataClasses: dataClasses.length,
  totalFields: dataClasses.reduce((sum, dc) => sum + dc.fields.length, 0),
  dataClasses: dataClasses.map((dc) => ({
    name: dc.name,
    fieldCount: dc.fields.length,
    isSpecial: dc.isSpecial,
    specialNote: dc.specialNote || null,
    fields: dc.fields,
  })),
};

writeFileSync("entity-inventory-full.json", JSON.stringify(fullInventory, null, 2));

// Build summary
const fieldsWithDescriptions = dataClasses.reduce(
  (sum, dc) => sum + dc.fields.filter((f) => f.hasDescription).length,
  0
);
const totalFields = fullInventory.totalFields;
const uniqueDataTypes = [...new Set(dataClasses.flatMap((dc) => dc.fields.map((f) => f.dataType)))].sort();

const summary = {
  source: "CureMD EHI_Export_DRS.xlsx",
  extractedAt: fullInventory.extractedAt,
  totalDataClasses: fullInventory.totalDataClasses,
  totalFields,
  fieldsWithDescriptions,
  fieldsWithoutDescriptions: totalFields - fieldsWithDescriptions,
  descriptionCoverage: `${((fieldsWithDescriptions / totalFields) * 100).toFixed(1)}%`,
  uniqueDataTypes,
  dataClassBreakdown: dataClasses.map((dc) => ({
    name: dc.name,
    fieldCount: dc.fields.length,
    fieldsWithDescriptions: dc.fields.filter((f) => f.hasDescription).length,
    isSpecial: dc.isSpecial,
    specialNote: dc.specialNote || null,
    dataTypes: [...new Set(dc.fields.map((f) => f.dataType))].sort(),
  })),
  // Categorize by domain
  domainCategories: {
    demographics: ["Patient Demographics", "Patient Contacts"],
    clinical: [
      "Allergies", "Complaints", "Diagnosis", "Diseases History",
      "Family History", "Hospitalization History", "Immunizations",
      "Medications", "Orders", "Results", "Risk",
      "Social History", "Surgery History", "Vitals A", "Vitals B",
    ],
    specialty: [
      "Chemo Admin", "Chemo Admin IVSites", "Chemo Plan",
      "Chemo Plan Diagnosis", "Chemo Plan Drugs", "OBGYN History",
    ],
    billing: [
      "Charges", "Claims", "Electronic Remittance Advice",
      "Payments", "Patient Insurances",
    ],
    documents: ["Documents & Images", "Provider Notes"],
    administrative: [
      "Appointments", "Cases", "Disclosures", "Memos",
      "Patient Consents", "Patient Education", "Patient Note", "Referrals",
    ],
  },
};

// Add domain field counts
const domainFieldCounts: Record<string, { classes: number; fields: number }> = {};
for (const [domain, classNames] of Object.entries(summary.domainCategories)) {
  const classes = dataClasses.filter((dc) => classNames.includes(dc.name));
  domainFieldCounts[domain] = {
    classes: classes.length,
    fields: classes.reduce((sum, dc) => sum + dc.fields.length, 0),
  };
}
(summary as any).domainFieldCounts = domainFieldCounts;

writeFileSync("entity-inventory-summary.json", JSON.stringify(summary, null, 2));

console.log(`\nTotal data classes: ${fullInventory.totalDataClasses}`);
console.log(`Total fields: ${totalFields}`);
console.log(`Fields with descriptions: ${fieldsWithDescriptions} (${summary.descriptionCoverage})`);
console.log(`Unique data types: ${uniqueDataTypes.join(", ")}`);
console.log(`\nData class breakdown:`);
for (const dc of dataClasses) {
  const desc = dc.fields.filter((f) => f.hasDescription).length;
  const special = dc.isSpecial ? " [SPECIAL - no tabular fields]" : "";
  console.log(`  ${dc.name}: ${dc.fields.length} fields, ${desc} with descriptions${special}`);
}
console.log(`\nDomain field counts:`);
for (const [domain, counts] of Object.entries(domainFieldCounts)) {
  console.log(`  ${domain}: ${counts.classes} classes, ${counts.fields} fields`);
}

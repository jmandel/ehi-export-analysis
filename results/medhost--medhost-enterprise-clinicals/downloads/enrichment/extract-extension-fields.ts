#!/usr/bin/env bun
/**
 * Parses MEDHOST-FHIR-Extension-Fields.xlsx into queryable JSON.
 * 
 * Run: bun run extract-extension-fields.ts
 * Input: ../MEDHOST-FHIR-Extension-Fields.xlsx
 * Output: extension-fields.json, extraction-summary.json
 */

import * as XLSX from "xlsx";
import { writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "MEDHOST-FHIR-Extension-Fields.xlsx");
const outputPath = join(scriptDir, "extension-fields.json");
const summaryPath = join(scriptDir, "extraction-summary.json");

const wb = XLSX.readFile(inputPath);

interface SheetData {
  sheetName: string;
  fhirResource: string;
  headers: string[];
  rows: Record<string, string | number | boolean | null>[];
  rowCount: number;
}

const skipSheets = new Set(["MEDHOST", "_reference"]);
const results: SheetData[] = [];
const errors: { sheet: string; error: string }[] = [];

for (const name of wb.SheetNames) {
  if (skipSheets.has(name)) continue;

  try {
    const ws = wb.Sheets[name];
    const data = XLSX.utils.sheet_to_json<Record<string, any>>(ws, { defval: null });
    const headers = data.length > 0 ? Object.keys(data[0]) : [];

    const resourceMap: Record<string, string> = {
      "Allergy": "AllergyIntolerance",
      "Ancillary Order": "ServiceRequest",
      "Charge Item": "ChargeItem",
      "Condition-Past Medical History": "Condition",
      "Detected Issue": "DetectedIssue",
      "Diagnostic Report": "DiagnosticReport",
      "Discharge Plan (CarePlan)": "CarePlan",
      "Family Member History": "FamilyMemberHistory",
      "Implantable Device": "Device",
      "MDRO": "Observation",
      "Medication Administration": "MedicationAdministration",
      "MedicationRequest-Discharge Med": "MedicationRequest",
      "MedicationRequest-InpatientMed": "MedicationRequest",
      "MedicationRequest-Prescriptions": "MedicationRequest",
      "MedicationStatement-HomeMed": "MedicationStatement",
      "Observation Alcohol Use": "Observation",
      "Observation Drug Use": "Observation",
      "Observation Education": "Observation",
      "Observation General Comment": "Observation",
      "Observation Labs": "Observation",
      "Observation Marital Status": "Observation",
      "Observation Occupation": "Observation",
      "Observation Sexual Behavior": "Observation",
      "Observation Travel": "Observation",
      "Past Procedure": "Procedure",
      "PC Orders (Service Request)": "ServiceRequest",
      "Question Answer": "QuestionnaireResponse",
      "Related Person": "RelatedPerson",
      "Smoking Status": "Observation",
    };

    results.push({
      sheetName: name,
      fhirResource: resourceMap[name] || name,
      headers,
      rows: data,
      rowCount: data.length,
    });
  } catch (e: any) {
    errors.push({ sheet: name, error: e.message });
  }
}

writeFileSync(outputPath, JSON.stringify(results, null, 2));

const totalFields = results.reduce((sum, s) => sum + s.rowCount, 0);
const resourceTypes = [...new Set(results.map(s => s.fhirResource))].sort();

const summary = {
  inputFile: "MEDHOST-FHIR-Extension-Fields.xlsx",
  totalSheets: wb.SheetNames.length,
  parsedSheets: results.length,
  skippedSheets: [...skipSheets],
  parseErrors: errors,
  totalExtensionFields: totalFields,
  uniqueFhirResourceTypes: resourceTypes,
  resourceTypeCount: resourceTypes.length,
  sheetSummary: results.map(s => ({
    sheet: s.sheetName,
    fhirResource: s.fhirResource,
    fieldCount: s.rowCount,
    headers: s.headers,
  })),
};

writeFileSync(summaryPath, JSON.stringify(summary, null, 2));

console.log(`Parsed ${results.length} sheets with ${totalFields} total extension fields`);
console.log(`Unique FHIR resource types: ${resourceTypes.length}`);
console.log(`Output: ${outputPath}`);
console.log(`Summary: ${summaryPath}`);
if (errors.length > 0) {
  console.error(`Errors: ${JSON.stringify(errors)}`);
}

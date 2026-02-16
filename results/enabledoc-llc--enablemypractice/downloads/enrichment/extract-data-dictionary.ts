#!/usr/bin/env bun
/**
 * Extracts the data dictionary from the EnableDoc EHI Export Guide PDF.
 *
 * Input: pdftotext output of Enabledoc-Exporting-Data-Guide-2023-updated-11202023.pdf
 * Output: data-dictionary.json — structured entities, fields, and value sets
 *
 * Run: bun run extract-data-dictionary.ts
 */

import { execSync } from "child_process";
import { writeFileSync } from "fs";
import { join, dirname } from "path";

const PDF_PATH = join(
  dirname(import.meta.dir),
  "Enabledoc-Exporting-Data-Guide-2023-updated-11202023.pdf"
);

const rawText = execSync(`pdftotext "${PDF_PATH}" -`).toString();

// Remove page footers and page numbers and form feeds
const text = rawText
  .replace(/\f/g, "\n")
  .replace(/\nEnableDoc LLC Confidential 2023\n/g, "\n")
  .replace(/^\d+\s*$/gm, "");

const lines = text.split("\n");

interface Field {
  name: string;
  description: string;
  required: "Required" | "Preferred" | "Optional";
  dataType: string;
  referenceSection?: string;
  valueSet?: string;
}

interface Entity {
  name: string;
  summary: string;
  fields: Field[];
}

interface ValueSetEntry {
  code: string;
  display: string;
}

interface ValueSet {
  name: string;
  values: ValueSetEntry[];
}

interface ExportFormat {
  name: string;
  description: string;
}

const exportFormats: ExportFormat[] = [
  {
    name: "C-CDA",
    description:
      "Data exported using USCDI v1 AND HL7 CDA R2 Implementation Guide: C-CDA Templates for Clinical Notes R2.1 Companion Guide, Release 2-US Realm, October 2019 standard.",
  },
  {
    name: "Attachments",
    description:
      "Attached files (images, excel, word, PDF) grouped as a .zip file by patient, downloaded by patient name.",
  },
  {
    name: "Notes",
    description:
      "Notes grouped as a .zip file by patient, downloaded by patient name. Notes text can be exported from the PDF.",
  },
  {
    name: "Excel",
    description:
      "Data organized by Excel tab for structured clinical data entities.",
  },
];

const excelTabNames = [
  "Condition",
  "Coverage",
  "Encounter",
  "Organization",
  "Patient",
  "Practitioner",
  "Procedure",
  "ServiceRequest",
  "FamilyMemberHistory",
  "Immunization",
  "Location",
  "MedicationAdministration",
  "MedicationRequest",
  "MedicationStatement",
  "Observation",
];

// Entity headings as they appear in the PDF (these are standalone lines)
const entityHeadings = [
  "Organization",
  "Encounter Data",
  "Patient",
  "Location",
  "Practitioner",
  "Procedure",
  "Service Request",
  "Family Member History",
  "Immunization",
  "AllergyIntolerance",
  "Care Plan",
  "Medication Administration",
  "MedicationRequest",
  "Observation",
  "Medication Statement",
];

const entitySummaries: Record<string, string> = {
  Organization: "A grouping of people or organizations with a common purpose.",
  "Encounter Data": "An interaction between a patient and clinician for the purpose of providing care or assessing the health of a patient.",
  Patient: "Demographics and other administrative information about an individual receiving health related services.",
  Location: "Details and position information for a physical place.",
  Practitioner: "A person who is directly or indirectly involved in the provisioning of healthcare.",
  Procedure: "An action that is or was performed on or for a patient.",
  "Service Request": "A record of a request for service such as diagnostic investigations, treatments, or operations to be performed.",
  "Family Member History": "Information about patient's relatives.",
  Immunization: "A record of the administration of a vaccine to a patient, or a record of an immunization as reported by a patient, a clinician or another party.",
  AllergyIntolerance: "Allergy or intolerance record for a patient.",
  "Care Plan": "A care plan record for a patient.",
  "Medication Administration": "A record of a patient consuming or otherwise being administered a medication.",
  MedicationRequest: "An order or request for both supply of medication and instructions for administration to a patient.",
  Observation: "A measurement or simple assertion made about a patient, device or other subject.",
  "Medication Statement": "A record of a medication that is or was being consumed by a patient.",
};

// Find line indices of entity headings
function findHeadingLines(): Array<{ name: string; lineIdx: number }> {
  const results: Array<{ name: string; lineIdx: number }> = [];
  const excelFileIdx = lines.findIndex((l) => l.trim() === "Excel File");
  if (excelFileIdx === -1) return results;

  const seen = new Set<string>();
  for (let i = excelFileIdx; i < lines.length; i++) {
    const trimmed = lines[i].trim();
    // Stop at VALUES section
    if (trimmed === "VALUES") break;

    for (const heading of entityHeadings) {
      if (trimmed === heading) {
        // Skip if this is in the bullet list area (● items)
        if (i <= excelFileIdx + 10) continue;
        // Skip if the previous non-empty line ends with "Section:" or "section:"
        // (this is a continuation line from a ➢ field reference)
        let prevLineIdx = i - 1;
        while (prevLineIdx >= 0 && !lines[prevLineIdx].trim()) prevLineIdx--;
        const prevLine = prevLineIdx >= 0 ? lines[prevLineIdx].trim() : "";
        if (/[Ss]ection:?\s*$/.test(prevLine)) continue;

        // Allow duplicate heading names only if we haven't seen this one yet
        // OR if the previous entry with the same name was a false positive
        if (seen.has(heading)) continue;

        seen.add(heading);
        results.push({ name: heading, lineIdx: i });
      }
    }
  }
  return results;
}

function parseRequirement(text: string): "Required" | "Preferred" | "Optional" {
  if (/\bRequired\b/i.test(text)) return "Required";
  if (/\bPreferred\b/i.test(text)) return "Preferred";
  if (/\bOptional\b/i.test(text)) return "Optional";
  return "Preferred";
}

function parseDataType(text: string): string {
  const types = ["string", "code", "boolean", "dateTime", "date", "integer", "decimal", "uri"];
  for (const t of types) {
    if (new RegExp(`\\b${t}\\b`, "i").test(text)) return t;
  }
  const seeMatch = text.match(/[Ss]ee\s+[Ss]ection[:\s]+(\w+)/);
  if (seeMatch) return `reference(${seeMatch[1]})`;
  const seeMatch2 = text.match(/[Ss]ee\s+this\s+section[:\s]+(\w+)/);
  if (seeMatch2) return `reference(${seeMatch2[1]})`;
  return "unknown";
}

function parseFieldLine(fullText: string): Field | null {
  const colonIdx = fullText.indexOf(":");
  if (colonIdx === -1) return null;

  const name = fullText.substring(0, colonIdx).trim();
  const rest = fullText.substring(colonIdx + 1).trim();

  if (!name || name.length > 60) return null;

  const requirement = parseRequirement(rest);
  const dataType = parseDataType(rest);

  let referenceSection: string | undefined;
  const refMatch = rest.match(/[Ss]ee\s+[Ss]ection[:\s]+(\w[\w\s]*?)(?:\s*$|\s+(?:Required|Preferred|Optional))/i);
  if (refMatch) referenceSection = refMatch[1].trim();
  const refMatch2 = rest.match(/[Ss]ee\s+this\s+section[:\s]+(\w+)/i);
  if (refMatch2) referenceSection = refMatch2[1].trim();

  let valueSet: string | undefined;
  const vsMatch = rest.match(/[Ss]ee\s+[Vv]alue[s]?[:\s]+(.+?)(?:\s*$)/i);
  if (vsMatch) valueSet = vsMatch[1].trim();

  let description = rest.replace(/\s*(Required|Preferred|Optional)\b.*$/i, "").trim();

  return {
    name,
    description,
    required: requirement,
    dataType,
    ...(referenceSection && { referenceSection }),
    ...(valueSet && { valueSet }),
  };
}

const warnings: string[] = [];
const headings = findHeadingLines();

const entities: Entity[] = [];
for (let h = 0; h < headings.length; h++) {
  const { name, lineIdx } = headings[h];
  const nextLineIdx = h + 1 < headings.length ? headings[h + 1].lineIdx : undefined;

  // Also stop at "VALUES" section
  const valuesLineIdx = lines.findIndex((l, i) => i > lineIdx && l.trim() === "VALUES");
  const endIdx = Math.min(
    nextLineIdx ?? lines.length,
    valuesLineIdx !== -1 ? valuesLineIdx : lines.length
  );

  const sectionLines = lines.slice(lineIdx + 1, endIdx);

  // Collect field text from ➢ markers, and also bare "fieldname:" lines
  const fields: Field[] = [];
  let currentFieldText = "";

  for (const line of sectionLines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    if (trimmed.startsWith("➢")) {
      if (currentFieldText) {
        const field = parseFieldLine(currentFieldText);
        if (field) fields.push(field);
      }
      currentFieldText = trimmed.replace(/^➢\s*/, "");
    } else if (/:/.test(trimmed) && /^[a-z]/.test(trimmed)) {
      // Bare field line without ➢ (Medication Statement section uses this format)
      if (currentFieldText) {
        const field = parseFieldLine(currentFieldText);
        if (field) fields.push(field);
      }
      currentFieldText = trimmed;
    } else if (currentFieldText) {
      // Continuation line
      currentFieldText += " " + trimmed;
    }
  }
  if (currentFieldText) {
    const field = parseFieldLine(currentFieldText);
    if (field) fields.push(field);
  }

  entities.push({ name, summary: entitySummaries[name] || "", fields });
}

// Parse value sets
function parseValueSets(): ValueSet[] {
  const valueSets: ValueSet[] = [];
  const valuesLineIdx = lines.findIndex((l) => l.trim() === "VALUES");
  if (valuesLineIdx === -1) {
    warnings.push("Could not find VALUES section");
    return valueSets;
  }

  let currentVSName = "";
  let currentEntries: ValueSetEntry[] = [];

  for (let i = valuesLineIdx + 1; i < lines.length; i++) {
    const trimmed = lines[i].trim();
    if (!trimmed) continue;

    if (trimmed.startsWith("➢")) {
      // This is a value entry
      const entryText = trimmed.replace(/^➢\s*/, "");
      const dashMatch = entryText.match(/^(\S+)\s+-\s+(.+)/);
      if (dashMatch) {
        currentEntries.push({ code: dashMatch[1], display: dashMatch[2].trim() });
      } else {
        const parts = entryText.match(/^(\S+)\s+(.*)/);
        if (parts) {
          currentEntries.push({ code: parts[1], display: parts[2].trim() || parts[1] });
        } else {
          currentEntries.push({ code: entryText, display: entryText });
        }
      }
    } else {
      // Possible new value set heading
      // Save previous if any
      if (currentVSName && currentEntries.length > 0) {
        valueSets.push({ name: currentVSName, values: currentEntries });
      }
      currentVSName = trimmed;
      currentEntries = [];
    }
  }
  // Save last
  if (currentVSName && currentEntries.length > 0) {
    valueSets.push({ name: currentVSName, values: currentEntries });
  }

  return valueSets;
}

const valueSets = parseValueSets();
const totalFields = entities.reduce((sum, e) => sum + e.fields.length, 0);
const totalValueEntries = valueSets.reduce((sum, vs) => sum + vs.values.length, 0);

const result = {
  exportFormats,
  excelTabNames,
  excelEntities: entities,
  valueSets,
  parsing: {
    totalEntitiesParsed: entities.length,
    totalFieldsParsed: totalFields,
    totalValueSetsParsed: valueSets.length,
    totalValueEntries,
    sourceFile: "Enabledoc-Exporting-Data-Guide-2023-updated-11202023.pdf",
    warnings,
  },
};

const outPath = join(dirname(import.meta.path), "data-dictionary.json");
writeFileSync(outPath, JSON.stringify(result, null, 2));

console.log(`Entities parsed: ${entities.length}`);
console.log(`Total fields parsed: ${totalFields}`);
console.log(`Value sets parsed: ${valueSets.length}`);
console.log(`Total value entries: ${totalValueEntries}`);
if (warnings.length) {
  console.log(`Warnings: ${warnings.join("; ")}`);
}
console.log(`Output: ${outPath}`);

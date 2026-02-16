#!/usr/bin/env bun
/**
 * Extracts structured data from the Benchmark EHR EHI Export PDF.
 * Parses pdftotext output to extract:
 * - Data element types (export categories)
 * - Field lists per category
 * - Descriptions and notes
 *
 * Usage: bun run extract-export-schema.ts
 * Requires: pdftotext (from poppler-utils) on PATH
 */

import { $ } from "bun";

const PDF_PATH = "../b-10-EHI-Export_Benchmark-Support_Self-Attestation-Document_final-1.pdf";
const OUTPUT_PATH = "./benchmark-ehr-export-schema.json";

interface ExportField {
  name: string;
}

interface ExportEntity {
  number: number;
  name: string;
  description: string;
  fields: ExportField[];
  notes: string[];
  has_file_attachments: boolean;
  billing_only: boolean;
}

interface ExportSchema {
  product: string;
  version: string;
  document_title: string;
  export_formats: string[];
  entity_count: number;
  total_field_count: number;
  entities: ExportEntity[];
  billing_entities: string[];
  non_billing_entities: string[];
  parsing_stats: {
    total_entities_found: number;
    entities_with_fields: number;
    entities_without_fields: number;
    parse_failures: string[];
  };
}

function normalizeQuotes(s: string): string {
  return s.replace(/[\u201c\u201d\u201e\u201f\u2033\u2036]/g, '"').replace(/[\u2018\u2019\u201a\u201b\u2032\u2035]/g, "'");
}

function cleanText(s: string): string {
  return normalizeQuotes(s)
    .replace(/147 Crossings Centre Drive \| Forest, Virginia 24551\s*\d*/g, "")
    .replace(/§170\.315\(b\)\(10\) Electronic Health Information export_Self Attestation Document/g, "")
    .replace(/\n/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function extractFieldsFromQuoted(section: string): ExportField[] {
  // Match "FIELD1, FIELD2, ..." pattern (quoted field lists with DB column names)
  // Normalize smart quotes first
  const normalized = normalizeQuotes(section);
  const match = normalized.match(/Exported field list is[^"]*"([^"]+)"/s);
  if (!match) return [];

  const raw = cleanText(match[1]);
  return raw
    .split(/,\s*/)
    .map((f) => f.trim().replace(/^"/, "").replace(/"$/, ""))
    .filter((f) => f.length > 0 && /^[A-Z_]/.test(f))
    .map((f) => ({ name: f }));
}

function extractFieldsFromDash(section: string): ExportField[] {
  // Match "Exported field list is - Field1, Field2, ..." (readable names, no quotes)
  const match = section.match(/Exported field list is\s*-+\s*(.*?)(?=\n\n|\n[A-Z•\d])/s);
  if (!match) return [];

  const raw = cleanText(match[1]);
  return raw
    .split(/,\s*/)
    .map((f) => f.trim())
    .filter((f) => f.length > 0)
    .map((f) => ({ name: f }));
}

async function main() {
  const text = await $`pdftotext ${PDF_PATH} -`.text();

  // Find the "Detailed Description" section
  const detailedStart = text.indexOf("Detailed Description of the Data Export Contents");
  if (detailedStart === -1) {
    console.error("Could not find 'Detailed Description' section");
    process.exit(1);
  }

  const detailedSection = text.slice(detailedStart);

  // Entity definitions from the document
  const entityDefs: Array<{ number: number; name: string; billing_only: boolean }> = [
    { number: 1, name: "Insurance Master", billing_only: false },
    { number: 2, name: "Medics", billing_only: false },
    { number: 3, name: "Referring Doctor", billing_only: false },
    { number: 4, name: "Adjusters", billing_only: false },
    { number: 5, name: "Attorneys", billing_only: false },
    { number: 6, name: "Employers", billing_only: false },
    { number: 7, name: "Guarantor", billing_only: false },
    { number: 8, name: "Patient Demographics", billing_only: false },
    { number: 9, name: "Patient Insurance", billing_only: false },
    { number: 10, name: "Vaccination", billing_only: false },
    { number: 11, name: "Health Maintenance", billing_only: false },
    { number: 12, name: "Family History", billing_only: false },
    { number: 13, name: "Past Medical Hist", billing_only: false },
    { number: 14, name: "Surgery", billing_only: false },
    { number: 15, name: "Allergy", billing_only: false },
    { number: 16, name: "Current Medication", billing_only: false },
    { number: 17, name: "Social History", billing_only: false },
    { number: 18, name: "Legal Documents", billing_only: false },
    { number: 19, name: "Other Documents", billing_only: false },
    { number: 20, name: "Enc Attach Docs", billing_only: false },
    { number: 21, name: "Old Progress Notes", billing_only: false },
    { number: 22, name: "Messages", billing_only: false },
    { number: 23, name: "Future Appointments", billing_only: false },
    { number: 24, name: "Vitals", billing_only: false },
    { number: 25, name: "Diagnosis Code", billing_only: false },
    { number: 26, name: "CPT Codes", billing_only: false },
    { number: 27, name: "HCPC Codes", billing_only: false },
    { number: 28, name: "CCD", billing_only: false },
    { number: 29, name: "Prescriptions", billing_only: false },
    { number: 30, name: "Lab Results", billing_only: false },
    { number: 31, name: "Rad Results", billing_only: false },
    { number: 32, name: "Procedure Orders", billing_only: false },
    { number: 33, name: "Consults", billing_only: false },
    { number: 34, name: "Enc Progress Notes", billing_only: false },
    { number: 35, name: "Procedure Notes", billing_only: false },
    { number: 36, name: "Letters", billing_only: false },
    { number: 37, name: "All Vitals", billing_only: false },
    { number: 38, name: "Lab Test Result Values", billing_only: false },
    { number: 39, name: "Patient Cases", billing_only: false },
    { number: 40, name: "Patient Notes", billing_only: false },
    { number: 41, name: "Patient Alert", billing_only: false },
    { number: 42, name: "Past Appointments", billing_only: false },
    { number: 43, name: "Billing Ledger", billing_only: true },
    { number: 44, name: "Billing Claims", billing_only: true },
    { number: 45, name: "Billing Charges", billing_only: true },
    { number: 46, name: "Patient Advance", billing_only: true },
    { number: 47, name: "Statements", billing_only: true },
  ];

  const entities: ExportEntity[] = [];
  const parseFailures: string[] = [];

  for (let i = 0; i < entityDefs.length; i++) {
    const def = entityDefs[i];
    const nextDef = i < entityDefs.length - 1 ? entityDefs[i + 1] : null;

    // Find the section start - look for "N. Name" pattern
    const escapedName = def.name.replace(/[()]/g, "\\$&");
    const startPattern = new RegExp(`${def.number}\\.\\s+${escapedName}`, "i");
    const startMatch = detailedSection.match(startPattern);

    if (!startMatch || startMatch.index === undefined) {
      parseFailures.push(`Could not find section for #${def.number} ${def.name}`);
      entities.push({
        number: def.number, name: def.name, description: "",
        fields: [], notes: [], has_file_attachments: false, billing_only: def.billing_only,
      });
      continue;
    }

    // Find section end - next numbered entry or end of text
    let sectionEnd = detailedSection.length;
    if (nextDef) {
      const nextEscaped = nextDef.name.replace(/[()]/g, "\\$&");
      const nextPattern = new RegExp(`${nextDef.number}\\.\\s+${nextEscaped}`, "i");
      const nextMatch = detailedSection.slice(startMatch.index + 5).match(nextPattern);
      if (nextMatch && nextMatch.index !== undefined) {
        sectionEnd = startMatch.index + 5 + nextMatch.index;
      }
    }

    const section = detailedSection.slice(startMatch.index, sectionEnd);

    // Try quoted field list first (DB column names), then dash-style
    let fields = extractFieldsFromQuoted(section);
    if (fields.length === 0) {
      // Some sections like Referring Doctor have the field list split by page break
      // Try a more aggressive extraction: find all quoted strings that look like field lists
      const normalizedSection = normalizeQuotes(section);
      const allQuotedMatches = [...normalizedSection.matchAll(/"([A-Z_][A-Z_0-9,\s\n]+)"/gs)];
      if (allQuotedMatches.length > 0) {
        const combined = allQuotedMatches.map(m => m[1]).join(", ");
        fields = cleanText(combined)
          .split(/,\s*/)
          .map(f => f.trim())
          .filter(f => f.length > 0 && /^[A-Z_]/.test(f))
          .map(f => ({ name: f }));
      }
    }

    // Extract description
    const fieldListIdx = section.indexOf("Exported field list");
    const descEnd = fieldListIdx > 0 ? fieldListIdx : Math.min(section.length, 500);
    const descRaw = cleanText(section.slice(startMatch[0].length, descEnd));

    const normSection = normalizeQuotes(section);
    const hasAttachments =
      normSection.includes('column labeled "File"') ||
      normSection.includes("path of the") ||
      (normSection.includes("HTML") && normSection.includes("XML") && normSection.includes("path"));

    const notes: string[] = [];
    if (/[Oo]nly active/.test(section)) notes.push("Only active records exported");
    if (/not exported/i.test(section)) {
      const noteMatches = section.match(/[^.]*not exported[^.]*\./gi);
      if (noteMatches) noteMatches.forEach(n => notes.push(cleanText(n)));
    }
    if (/billed claims only/i.test(section)) notes.push("Only billed claims exported");
    if (/encounters that are closed/i.test(section)) notes.push("Only closed encounters exported");
    if (/latest encounter/i.test(section)) notes.push("Only latest encounter data exported");

    entities.push({
      number: def.number,
      name: def.name,
      description: descRaw,
      fields,
      notes,
      has_file_attachments: hasAttachments,
      billing_only: def.billing_only,
    });
  }

  const totalFields = entities.reduce((sum, e) => sum + e.fields.length, 0);
  const entitiesWithFields = entities.filter((e) => e.fields.length > 0).length;
  const entitiesWithoutFields = entities.filter((e) => e.fields.length === 0).length;

  const schema: ExportSchema = {
    product: "Benchmark EHR",
    version: "Denali 3.1",
    document_title:
      "§170.315(b)(10) Electronic Health Information export_Self Attestation Document",
    export_formats: ["XLS (Excel)", "TXT (tab/pipe delimited)", "PDF (for documents/attachments)"],
    entity_count: entities.length,
    total_field_count: totalFields,
    entities,
    billing_entities: entities.filter((e) => e.billing_only).map((e) => e.name),
    non_billing_entities: entities.filter((e) => !e.billing_only).map((e) => e.name),
    parsing_stats: {
      total_entities_found: entities.length,
      entities_with_fields: entitiesWithFields,
      entities_without_fields: entitiesWithoutFields,
      parse_failures: parseFailures,
    },
  };

  await Bun.write(OUTPUT_PATH, JSON.stringify(schema, null, 2));

  console.log(`Extracted ${entities.length} entities with ${totalFields} total fields`);
  console.log(`  With fields: ${entitiesWithFields}`);
  console.log(`  Without fields: ${entitiesWithoutFields}`);
  console.log(`  Parse failures: ${parseFailures.length}`);
  if (parseFailures.length > 0) {
    for (const f of parseFailures) console.log(`    - ${f}`);
  }
  console.log(`\nEntities without fields:`);
  for (const e of entities.filter(e => e.fields.length === 0)) {
    console.log(`  #${e.number} ${e.name}`);
  }
  console.log(`Output: ${OUTPUT_PATH}`);
}

main().catch(console.error);

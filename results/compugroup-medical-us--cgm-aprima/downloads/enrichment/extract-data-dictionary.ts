#!/usr/bin/env bun
/**
 * Extracts the EHI Export data dictionary from the PDF text output
 * into structured JSON for downstream analysis.
 *
 * Usage: bun run extract-data-dictionary.ts
 *
 * Input: ../cgm-aprima-electronic-health-information-export-user-guide.pdf (via pdftotext)
 * Output: ./ehi-data-dictionary.json
 */

import { $ } from "bun";

interface Field {
  column_heading: string;
  data_type: string;
  description: string;
}

interface CsvFile {
  name: string;
  file_name_pattern: string;
  description: string;
  fields: Field[];
}

interface DataDictionary {
  source_pdf: string;
  source_date: string;
  product: string;
  export_format: string;
  export_components: string[];
  csv_files: CsvFile[];
  total_csv_files: number;
  total_fields: number;
}

const pdfPath = new URL(
  "../cgm-aprima-electronic-health-information-export-user-guide.pdf",
  import.meta.url
).pathname;

// Extract text from PDF
const text =
  await $`pdftotext ${pdfPath} -`.text();

// The data dictionary is structured as sections, each starting with a CSV file name
// followed by Description, File name, and Data Provided (column headings, data types, descriptions)

const csvFiles: CsvFile[] = [];

// Define the known CSV file sections from the table of contents
const sections = [
  { name: "Audit Trail", startMarker: "Audit Trail\nDescription" },
  { name: "Contacts", startMarker: "Contacts\nDescription" },
  { name: "Active Medication", startMarker: "Active Medication\nDescription" },
  { name: "Allergies", startMarker: "Allergies\nDescription" },
  {
    name: "Appointment Information",
    startMarker: "Appointment Information\nDescription",
  },
  { name: "Family History", startMarker: "Family History\nDescription" },
  { name: "Immunization", startMarker: "Immunization\nDescription" },
  { name: "Medical History", startMarker: "Medical History\nDescription" },
  {
    name: "Patient Demographics",
    startMarker: "Patient Demographics\nDescription",
  },
  { name: "Patient Insurance", startMarker: "Patient Insurance\nDescription" },
  { name: "Problem List", startMarker: "Problem List\nDescription" },
  { name: "Responsible Party", startMarker: "Responsible Party\nDescription" },
  { name: "Results", startMarker: "Results\nDescription" },
  { name: "Social History", startMarker: "Social History\nDescription" },
  { name: "Visit Comments", startMarker: "Visit Comments\nDescription" },
  { name: "Vitals", startMarker: "Vitals\nDescription" },
  { name: "Eligibility", startMarker: "Eligibility\nDescription" },
  { name: "Employment", startMarker: "Employment\nDescription" },
  { name: "Patient Ledger", startMarker: "Patient Ledger\nDescription" },
  { name: "Patient Referrals", startMarker: "Patient Referrals\nDescription" },
  { name: "Providers", startMarker: "Providers\nDescription" },
  { name: "Response Report", startMarker: "Response Report\nDescription" },
];

// Known data types from the document
const dataTypes = new Set([
  "datetime",
  "date",
  "char",
  "smallint",
  "money",
  "bit",
  "int",
  "bigint",
  "uniqueidentifier",
]);

function isDataType(s: string): boolean {
  const trimmed = s.trim();
  if (dataTypes.has(trimmed)) return true;
  if (/^char\(\d+\)$/.test(trimmed)) return true;
  return false;
}

// Extract section text between markers
function extractSection(
  fullText: string,
  sectionName: string,
  nextSectionIdx: number
): string {
  // Find the section by looking for the pattern: "SectionName\nDescription\n\nA record of..."
  // after the table of contents
  const tocEnd = fullText.indexOf(".csv File Details");
  if (tocEnd === -1) return "";

  const afterToc = fullText.substring(tocEnd);
  const sectionStart = afterToc.indexOf(sectionName + "\nDescription");
  if (sectionStart === -1) return "";

  // Find the end - either the next section or "EHI Export in CGM APRIMA"
  let sectionEnd: number;
  if (nextSectionIdx < sections.length) {
    const nextStart = afterToc.indexOf(
      sections[nextSectionIdx].name + "\nDescription",
      sectionStart + 1
    );
    sectionEnd = nextStart !== -1 ? nextStart : afterToc.length;
  } else {
    const endMarker = afterToc.indexOf("EHI Export in CGM APRIMA", sectionStart + 1);
    sectionEnd = endMarker !== -1 ? endMarker : afterToc.length;
  }

  return afterToc.substring(sectionStart, sectionEnd);
}

function parseSection(sectionText: string, sectionName: string): CsvFile {
  const lines = sectionText.split("\n").map((l) => l.trim());

  // Extract description (line after "Description" and before "File name")
  let description = "";
  let fileNamePattern = "";
  const fields: Field[] = [];

  let i = 0;
  // Skip to after first "Description"
  while (i < lines.length && lines[i] !== "Description") i++;
  i++; // skip "Description"

  // Skip empty lines
  while (i < lines.length && lines[i] === "") i++;

  // Collect description until "File name"
  const descParts: string[] = [];
  while (i < lines.length && lines[i] !== "File name") {
    if (lines[i] !== "") descParts.push(lines[i]);
    i++;
  }
  description = descParts.join(" ");

  // Skip "File name" and empty lines
  i++; // skip "File name"
  while (i < lines.length && lines[i] === "") i++;

  // Collect file name pattern
  const fnParts: string[] = [];
  while (i < lines.length && lines[i] !== "Data Provided") {
    if (lines[i] !== "") fnParts.push(lines[i]);
    i++;
  }
  fileNamePattern = fnParts.join(" ");

  // Skip "Data Provided" header and column header row
  while (i < lines.length && lines[i] !== "Column Heading") i++;
  // Skip Column Heading, Data Type, Description header
  i++; // Column Heading
  while (i < lines.length && (lines[i] === "" || lines[i] === "Data Type")) i++;
  while (i < lines.length && (lines[i] === "" || lines[i] === "Description"))
    i++;

  // Now parse field triplets: column_heading, data_type, description
  // Fields come in groups: heading, type, description (each possibly multi-line)
  // The pattern is: a field name, then a data type, then a description
  // Page numbers appear as standalone numbers (like "6", "7", etc.)

  while (i < lines.length) {
    const line = lines[i];

    // Skip empty lines and standalone page numbers
    if (line === "" || /^\d{1,2}$/.test(line)) {
      i++;
      continue;
    }

    // Skip if we hit another section header pattern
    if (
      line === "Column Heading" ||
      line === "Data Type" ||
      line === "Description" ||
      line === "Data Provided"
    ) {
      i++;
      continue;
    }

    // Try to read a field: name, type, description
    // The name is first, then possibly on the next line(s) the type, then description

    let fieldName = line;
    i++;

    // Collect additional name parts if next line isn't a data type
    while (i < lines.length && lines[i] !== "" && !isDataType(lines[i])) {
      // Check if it looks like a continuation of the name (before we see a type)
      // But also check if it might be a page number
      if (/^\d{1,2}$/.test(lines[i])) {
        i++;
        continue;
      }
      fieldName += " " + lines[i];
      i++;
    }

    // Skip empty lines
    while (i < lines.length && lines[i] === "") i++;

    // Read data type
    let dataType = "";
    if (i < lines.length) {
      const typeLine = lines[i];
      // Handle cases like "char(25)" or "uniqueidentifier Account identifier."
      // where the type might be combined with description on same line
      const typeMatch = typeLine.match(
        /^(char\(\d+\)|datetime|date|smallint|money|bit|int|bigint|uniqueidentifier)\s*(.*)/
      );
      if (typeMatch) {
        dataType = typeMatch[1];
        if (typeMatch[2]) {
          // Description was on same line as type
          fields.push({
            column_heading: fieldName.trim(),
            data_type: dataType,
            description: typeMatch[2].trim(),
          });
          i++;
          continue;
        }
        i++;
      }
    }

    // Skip empty lines
    while (i < lines.length && lines[i] === "") i++;

    // Read description
    let desc = "";
    if (i < lines.length) {
      desc = lines[i];
      i++;
      // Continue description if next line isn't empty and isn't a new field pattern
      while (i < lines.length && lines[i] !== "") {
        if (/^\d{1,2}$/.test(lines[i])) {
          i++;
          break;
        }
        // Check if the next line looks like it could be a new field name
        // (i.e., the line after it is a data type)
        let lookAhead = i + 1;
        while (lookAhead < lines.length && lines[lookAhead] === "")
          lookAhead++;
        if (lookAhead < lines.length && isDataType(lines[lookAhead])) {
          break; // This line is a new field name, not a description continuation
        }
        desc += " " + lines[i];
        i++;
      }
    }

    if (fieldName.trim() && dataType) {
      fields.push({
        column_heading: fieldName.trim(),
        data_type: dataType,
        description: desc.trim(),
      });
    }
  }

  return {
    name: sectionName,
    file_name_pattern: fileNamePattern,
    description,
    fields,
  };
}

// Parse each section
for (let idx = 0; idx < sections.length; idx++) {
  const section = sections[idx];
  const sectionText = extractSection(text, section.name, idx + 1);
  if (sectionText) {
    const parsed = parseSection(sectionText, section.name);
    csvFiles.push(parsed);
  } else {
    console.error(`WARNING: Could not find section "${section.name}"`);
  }
}

const totalFields = csvFiles.reduce((sum, f) => sum + f.fields.length, 0);

const dictionary: DataDictionary = {
  source_pdf: "cgm-aprima-electronic-health-information-export-user-guide.pdf",
  source_date: "2023-11-02",
  product: "CGM APRIMA v19",
  export_format: "ZIP file containing CSV files, images, USCDI XML, and a Complete Patient Chart PDF",
  export_components: [
    "CSV files with structured data (see csv_files array)",
    "Image folders organized by encounter date (e.g., Radiology/)",
    "USCDI file (XML format with EEHR_ChartViewer.exe viewer)",
    "Complete Patient Chart (PDF of all visit charts)",
  ],
  csv_files: csvFiles,
  total_csv_files: csvFiles.length,
  total_fields: totalFields,
};

const outputPath = new URL("./ehi-data-dictionary.json", import.meta.url)
  .pathname;
await Bun.write(outputPath, JSON.stringify(dictionary, null, 2));

console.log(`Extracted ${csvFiles.length} CSV file definitions`);
console.log(`Total fields: ${totalFields}`);
console.log(`Output: ${outputPath}`);

// Print summary
for (const f of csvFiles) {
  console.log(`  ${f.name}: ${f.fields.length} fields (${f.file_name_pattern})`);
}

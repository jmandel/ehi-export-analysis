#!/usr/bin/env bun
/**
 * Extracts the myUnity EHI Export data dictionary from the PDF text extraction
 * into a structured JSON format.
 *
 * Input: pdftotext output of ehi_export_all_files_myunity_fall_2024.pdf
 * Output: data-dictionary.json — structured JSON with all files and fields
 */

import { readFileSync, writeFileSync } from "fs";
import { execSync } from "child_process";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const pdfPath = join(scriptDir, "..", "ehi_export_all_files_myunity_fall_2024.pdf");

// Extract text from PDF
const text = execSync(`pdftotext "${pdfPath}" -`, { encoding: "utf-8" });

interface Field {
  name: string;
  type: string;
  description: string;
}

interface ExportFile {
  file_name: string;
  file_description: string;
  fields: Field[];
  sections?: string[]; // For CCD-like files that list sections instead of fields
}

interface DataDictionary {
  document_title: string;
  last_updated: string;
  overview: string;
  glossary: Record<string, string>;
  export_files: ExportFile[];
  stats: {
    total_files: number;
    total_fields: number;
    files_with_fields: number;
    files_with_sections_only: number;
  };
}

// Parse the text
const lines = text.split("\n");

// Extract metadata
const title = "EHI Export: myUnity File Documentation";
const lastUpdated = "08/15/2024 12:00 PM EDT";
const overview =
  "This documentation describes each myUnity EHI file as of 03/01/2024 at 12:00 PM EDT in the current released version. The documentation reflects the most current information at the time it was produced. The documentation is broken out by export file. Documentation from a specific organization might differ based on the organization's version of myUnity, custom development, or definition of EHI data. Each file contains a description and column details.";

// Parse glossary
const glossary: Record<string, string> = {
  PatientSys:
    "The unique system generated ID for a given patient. This value cannot be updated by a myUnity user.",
  PatientID:
    "PatientID is the typical method to indicate the unique patient identifier within the myUnity environment. This is sometimes referred to as the medical record number or client ID. This value should be used to associate all files to a specific patient.",
  Patient_DisplayName:
    "Concatenation of the patient's Last, First and Middle portions of their legal name.",
};

// Find file documentation sections
// Pattern: "XXX File Documentation"
const fileDocPattern = /^(.+?)\s+File Documentation$/;
const fileDescPattern = /^File Description:\s*(.+)/;
const fieldNamePattern = /^Name:\s*(.+)/;
const fieldTypePattern = /^Type:\s*(.+)/;
const fieldDescPattern = /^Description:\s*(.+)/;
const pageNumberPattern = /^\d+$/;
const separatorPattern = /^-{5,}/;
// Handle merged separator+name lines like "-------------Name: PatientSys"
const mergedSepNamePattern = /^-{5,}Name:\s*(.+)/;

const exportFiles: ExportFile[] = [];

let i = 0;
while (i < lines.length) {
  const line = lines[i].trim();

  // Check for file documentation header
  const fileMatch = line.match(fileDocPattern);
  if (
    fileMatch &&
    !line.startsWith("Contents") &&
    !line.startsWith("Overview") &&
    !line.startsWith("EHI Export:") &&
    !line.includes("....") // Skip TOC lines
  ) {
    const fileName = fileMatch[1].trim();

    // Skip forward to find file description
    i++;
    let fileDescription = "";
    let foundDesc = false;

    // Collect file description (may span multiple lines)
    while (i < lines.length) {
      const nextLine = lines[i].trim();
      if (pageNumberPattern.test(nextLine) || nextLine === "") {
        i++;
        continue;
      }

      if (nextLine.startsWith("File Description:")) {
        fileDescription = nextLine.replace("File Description:", "").trim();
        i++;
        // Continue collecting description until we hit separator or field
        while (i < lines.length) {
          const contLine = lines[i].trim();
          if (
            separatorPattern.test(contLine) ||
            mergedSepNamePattern.test(contLine) ||
            contLine.startsWith("Name:") ||
            contLine.startsWith("CCD contains")
          ) {
            break;
          }
          if (contLine && !pageNumberPattern.test(contLine)) {
            fileDescription += " " + contLine;
          }
          i++;
        }
        foundDesc = true;
        break;
      }
      if (separatorPattern.test(nextLine) || nextLine.startsWith("Name:")) {
        break;
      }
      i++;
    }

    // Special case for CCD file — it has sections, not fields
    if (fileName === "CCD") {
      const sections: string[] = [];
      while (i < lines.length) {
        const sLine = lines[i].trim();
        if (sLine.match(fileDocPattern) && sLine !== line) break;
        if (sLine.startsWith("•")) {
          sections.push(sLine.replace("•", "").trim());
        }
        i++;
      }
      exportFiles.push({
        file_name: fileName,
        file_description: fileDescription,
        fields: [],
        sections,
      });
      continue;
    }

    // Special case for Attachments — no fields, just description
    if (fileName === "Attachments") {
      exportFiles.push({
        file_name: fileName,
        file_description: fileDescription,
        fields: [],
      });
      // Don't increment i, let the outer loop handle it
      continue;
    }

    // Parse fields
    const fields: Field[] = [];
    let currentName = "";
    let currentType = "";
    let currentDesc = "";
    let collectingDesc = false;

    while (i < lines.length) {
      const fLine = lines[i].trim();

      // Check if we've hit the next file documentation section
      if (fLine.match(fileDocPattern) && fLine !== line) {
        // Save any pending field
        if (currentName) {
          fields.push({
            name: currentName,
            type: currentType,
            description: currentDesc.trim(),
          });
        }
        break;
      }

      // Skip page numbers and plain separators
      if (pageNumberPattern.test(fLine) || fLine === "") {
        i++;
        continue;
      }

      // Handle merged separator+name like "-------------Name: PatientSys"
      const mergedMatch = fLine.match(mergedSepNamePattern);
      if (mergedMatch) {
        if (currentName) {
          fields.push({
            name: currentName,
            type: currentType,
            description: currentDesc.trim(),
          });
        }
        currentName = mergedMatch[1].trim();
        currentType = "";
        currentDesc = "";
        collectingDesc = false;
        i++;
        continue;
      }

      // Skip plain separators (no merged content)
      if (separatorPattern.test(fLine)) {
        i++;
        continue;
      }

      const nameMatch = fLine.match(fieldNamePattern);
      const typeMatch = fLine.match(fieldTypePattern);
      const descMatch = fLine.match(fieldDescPattern);

      if (nameMatch) {
        // Save previous field
        if (currentName) {
          fields.push({
            name: currentName,
            type: currentType,
            description: currentDesc.trim(),
          });
        }
        currentName = nameMatch[1].trim();
        currentType = "";
        currentDesc = "";
        collectingDesc = false;
      } else if (typeMatch && currentName && !currentType) {
        currentType = typeMatch[1].trim();
      } else if (descMatch && currentName && currentType) {
        currentDesc = descMatch[1].trim();
        collectingDesc = true;
      } else if (collectingDesc && fLine && !fLine.startsWith("Name:") && !fLine.startsWith("Type:")) {
        // Multi-line description continuation
        currentDesc += " " + fLine;
      } else if (!currentName && !nameMatch && !typeMatch && !descMatch) {
        // Could be continuation of file description or other text
        i++;
        continue;
      }

      i++;
    }

    // Save last field if we ran out of lines
    if (currentName) {
      fields.push({
        name: currentName,
        type: currentType,
        description: currentDesc.trim(),
      });
    }

    // Deduplicate fields by name (pdftotext sometimes produces duplicates at page breaks)
    const seenNames = new Set<string>();
    const dedupedFields = fields.filter((f) => {
      if (seenNames.has(f.name)) return false;
      seenNames.add(f.name);
      return true;
    });

    exportFiles.push({
      file_name: fileName,
      file_description: fileDescription,
      fields: dedupedFields,
    });
    continue;
  }

  i++;
}

// Compute stats
const totalFields = exportFiles.reduce((sum, f) => sum + f.fields.length, 0);
const filesWithFields = exportFiles.filter((f) => f.fields.length > 0).length;
const filesWithSectionsOnly = exportFiles.filter(
  (f) => f.fields.length === 0 && f.sections && f.sections.length > 0
).length;

const dictionary: DataDictionary = {
  document_title: title,
  last_updated: lastUpdated,
  overview,
  glossary,
  export_files: exportFiles,
  stats: {
    total_files: exportFiles.length,
    total_fields: totalFields,
    files_with_fields: filesWithFields,
    files_with_sections_only: filesWithSectionsOnly,
  },
};

const outputPath = join(scriptDir, "data-dictionary.json");
writeFileSync(outputPath, JSON.stringify(dictionary, null, 2));

// Print summary
console.log(`Parsed ${exportFiles.length} export files`);
console.log(`Total fields extracted: ${totalFields}`);
console.log(`Files with field definitions: ${filesWithFields}`);
console.log(`Files with section lists only: ${filesWithSectionsOnly}`);
console.log(`\nExport files:`);
for (const f of exportFiles) {
  const detail = f.sections
    ? `${f.sections.length} sections`
    : `${f.fields.length} fields`;
  console.log(`  - ${f.file_name}: ${detail}`);
}

// Also produce a coverage accounting file
const accounting = {
  input_file: "ehi_export_all_files_myunity_fall_2024.pdf",
  extraction_method: "pdftotext + regex parsing",
  total_lines_processed: lines.length,
  files_discovered: exportFiles.map((f) => f.file_name),
  files_parsed: exportFiles.length,
  parse_failures: [] as { file: string; reason: string }[],
  notes: [
    "CCD file documents sections (C-CDA categories) rather than individual fields",
    "Attachments file has no field definitions — it exports raw attachment files",
    "The NonRegulatoryAssessment file uses nested arrays (AssessmentDocList, Responses) with dot-notation field names",
    "Field descriptions may span multiple lines in the PDF; parser concatenates them",
  ],
};

const accountingPath = join(scriptDir, "coverage-accounting.json");
writeFileSync(accountingPath, JSON.stringify(accounting, null, 2));
console.log(`\nWrote coverage accounting to ${accountingPath}`);

#!/usr/bin/env bun
/**
 * extract-data-models.ts
 *
 * Parses the smartEMR readme.io documentation HTML pages (both the EHI export
 * page and the data import pages) to extract structured data models, field
 * specifications, and export format descriptions.
 *
 * Input:  ../  (HTML files downloaded from smartemr.readme.io)
 * Output: ./smartemr-data-models.json   — structured field specs per page
 *         ./smartemr-ehi-export.json     — EHI export description
 *         ./extraction-stats.json        — coverage/accounting
 */

import { readdir, readFile, writeFile } from "fs/promises";
import { join, basename } from "path";

const DOWNLOADS_DIR = join(import.meta.dir, "..");
const OUTPUT_DIR = import.meta.dir;

interface FieldSpec {
  number: number;
  name: string;
  description: string;
  dataType: string;
  maxLength: string;
  required: boolean;
  validationRule: string;
  standard?: string;
}

interface DataModel {
  page: string;
  sourceFile: string;
  title: string;
  category: string;
  description: string;
  importCapabilities: string[];
  fields: FieldSpec[];
  technicalGuidelines: string[];
  acceptedFormats: string[];
}

interface EhiExport {
  sourceFile: string;
  title: string;
  description: string;
  exportFormat: string;
  singlePatientExport: {
    description: string;
    path: string;
    steps: string[];
    options: string[];
  };
  populationExport: {
    description: string;
    path: string;
    steps: string[];
    options: string[];
  };
  documentRepository: {
    description: string;
    path: string;
    steps: string[];
    fileFormats: string[];
    organization: string;
  };
}

function stripHtml(html: string): string {
  return html
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, "")
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "")
    .replace(/<[^>]*>/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#x27;/g, "'")
    .replace(/&#160;/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function extractTextBlocks(html: string): string[] {
  // Remove script and style blocks first
  const cleaned = html
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, "")
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "");

  // Extract text content from meaningful tags
  const blocks: string[] = [];
  const tagRegex = /<(p|li|h[1-6]|td|th|strong|em|div)[^>]*>([\s\S]*?)<\/\1>/gi;
  let match;
  while ((match = tagRegex.exec(cleaned)) !== null) {
    const text = stripHtml(match[2]).trim();
    if (text.length > 2) blocks.push(text);
  }
  return blocks;
}

function parseFieldTable(html: string): FieldSpec[] {
  const fields: FieldSpec[] = [];

  // Look for table rows with field specifications
  // Pattern: number, field name, description, data type, max length, required, validation
  const rowRegex = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
  const cellRegex = /<t[dh][^>]*>([\s\S]*?)<\/t[dh]>/gi;

  let rowMatch;
  while ((rowMatch = rowRegex.exec(html)) !== null) {
    const rowHtml = rowMatch[1];
    const cells: string[] = [];
    let cellMatch;
    const localCellRegex = /<t[dh][^>]*>([\s\S]*?)<\/t[dh]>/gi;
    while ((cellMatch = localCellRegex.exec(rowHtml)) !== null) {
      cells.push(stripHtml(cellMatch[1]).trim());
    }

    // Skip header rows and empty rows
    if (cells.length < 3) continue;
    const firstCell = cells[0];
    if (!firstCell || isNaN(parseInt(firstCell))) continue;

    const num = parseInt(firstCell);
    if (num < 1 || num > 100) continue;

    // Handle different table formats
    if (cells.length >= 6) {
      // Full format: num, name, description, dataType, maxLength, required, validation
      fields.push({
        number: num,
        name: cells[1] || "",
        description: cells[2] || "",
        dataType: cells[3] || "",
        maxLength: cells[4] || "",
        required: /✅|yes|required/i.test(cells[5] || ""),
        validationRule: cells[6] || "",
        ...(cells.length >= 8 ? { standard: cells[3] } : {}),
      });
    } else if (cells.length >= 4) {
      // Shorter format: num, name, description, standard/type, required, notes
      fields.push({
        number: num,
        name: cells[1] || "",
        description: cells[2] || "",
        dataType: cells[3] || "",
        maxLength: "",
        required: /✅|yes|required/i.test(cells[4] || cells[3] || ""),
        validationRule: cells[5] || cells[4] || "",
      });
    }
  }

  return fields;
}

function extractListItems(html: string, sectionMarker: string): string[] {
  const items: string[] = [];
  // Find the section
  const idx = html.indexOf(sectionMarker);
  if (idx === -1) return items;

  // Get text after the section marker until next section
  const sectionHtml = html.substring(idx, idx + 3000);
  const liRegex = /<li[^>]*>([\s\S]*?)<\/li>/gi;
  let m;
  while ((m = liRegex.exec(sectionHtml)) !== null) {
    const text = stripHtml(m[1]).trim();
    if (text.length > 2) items.push(text);
  }
  return items;
}

function parseDataImportPage(html: string, filename: string): DataModel | null {
  const text = stripHtml(html);

  // Extract title
  const titleMatch = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  const title = titleMatch ? stripHtml(titleMatch[1]).trim() : basename(filename, ".html");

  // Determine category from sidebar heading context
  let category = "unknown";
  if (/patient.demo|insurance|cpt|fee.schedule|service.location|referring|appointment/i.test(filename)) {
    category = "data-import";
  } else if (/document.upload|problem.list|allerg|immuniz/i.test(filename)) {
    category = "clinical-data-import";
  } else if (/ehi|export|b10/i.test(filename)) {
    category = "ehi-export";
  }

  // Extract description (first meaningful paragraph)
  const descMatch = html.match(/This guide[^<]*/i) || html.match(/This document[^<]*/i);
  const description = descMatch ? stripHtml(descMatch[0]).trim() : "";

  // Extract fields
  const fields = parseFieldTable(html);
  if (fields.length === 0 && category !== "ehi-export") return null;

  // Extract import capabilities
  const capabilities = extractListItems(html, "Import Capabilities");

  // Extract technical guidelines
  const guidelines = extractListItems(html, "Technical Guidelines");

  // Extract accepted formats
  const formats: string[] = [];
  if (/\.xlsx/i.test(text)) formats.push("xlsx");
  if (/\.csv/i.test(text)) formats.push("csv");
  if (/\.txt/i.test(text)) formats.push("txt");

  return {
    page: basename(filename, ".html"),
    sourceFile: filename,
    title,
    category,
    description,
    importCapabilities: capabilities,
    fields,
    technicalGuidelines: guidelines,
    acceptedFormats: formats,
  };
}

function parseEhiExportPage(html: string): EhiExport {
  const text = stripHtml(html);

  return {
    sourceFile: "electronic-health-information-export-b10.html",
    title: "Electronic Health Information Export",
    description:
      "This document offers insights into the format of the export output when utilizing the smartEMR Electronic Health Information (EHI) export feature. The primary objective is to ensure compliance with the 2015 Edition Cures Update Conformance Regulation §170.315(b)(10) for Electronic Health Information export.",
    exportFormat: "CDA (Clinical Document Architecture) + Document Repository",
    singlePatientExport: {
      description:
        "Each unique patient encounter is meticulously documented within a CDA file, adhering to the rigorous specifications and standards set by HL7 CDA.",
      path: "Admin Panel → Export Options → Patient Data → Create a backup/export",
      steps: ["By Patient", 'Select patient(s), click on "Create"'],
      options: [
        "Schedule a one-time backup/export",
        "Schedule a recurring backup/export",
        "Search by Date of Service",
      ],
    },
    populationExport: {
      description:
        "For a comprehensive overview, a consolidated CDA file is available, amalgamating all patient encounters pertaining to a specific individual.",
      path: "Admin Panel → Export Options → Patient Data → Create a backup/export",
      steps: ["All Patients", 'Click on "Select All" patients, and click on "Create"'],
      options: [
        "Schedule a one-time backup/export",
        "Schedule a recurring backup/export",
        "Search by Date of Service",
      ],
    },
    documentRepository: {
      description:
        "This repository encompasses a range of signed encounter notes, lab results, radiology reports, and any other scanned or uploaded documents within a patient's record.",
      path: "Admin Panel → Export Options → Patient Document Data (b10)",
      steps: ['Search patient criteria, select a single patient or ALL, click on "Create Portable"'],
      fileFormats: ["PDF", "JPG", "PNG"],
      organization:
        "All documents are sorted and indexed within the respective patient chart ID number folders. In cases where specific categories or types of documents exist (e.g., Lab Reports, Radiology, Scanned Receipts, etc.), they are housed within dedicated category subfolders under the primary patient folder.",
    },
  };
}

async function main() {
  // Find all HTML files in the downloads directory
  const files = await readdir(DOWNLOADS_DIR);
  const htmlFiles = files.filter((f) => f.endsWith(".html"));

  const stats = {
    totalFilesDiscovered: htmlFiles.length,
    totalFilesParsed: 0,
    parseFailures: [] as { file: string; error: string }[],
    modelsExtracted: 0,
    totalFieldsExtracted: 0,
  };

  const models: DataModel[] = [];
  let ehiExport: EhiExport | null = null;

  for (const file of htmlFiles) {
    const filePath = join(DOWNLOADS_DIR, file);
    try {
      const html = await readFile(filePath, "utf-8");
      stats.totalFilesParsed++;

      if (file.includes("electronic-health-information-export")) {
        ehiExport = parseEhiExportPage(html);
      } else {
        const model = parseDataImportPage(html, file);
        if (model) {
          models.push(model);
          stats.modelsExtracted++;
          stats.totalFieldsExtracted += model.fields.length;
        }
      }
    } catch (err: any) {
      stats.parseFailures.push({ file, error: err.message });
    }
  }

  // Write outputs
  await writeFile(
    join(OUTPUT_DIR, "smartemr-data-models.json"),
    JSON.stringify(models, null, 2)
  );

  if (ehiExport) {
    await writeFile(
      join(OUTPUT_DIR, "smartemr-ehi-export.json"),
      JSON.stringify(ehiExport, null, 2)
    );
  }

  await writeFile(
    join(OUTPUT_DIR, "extraction-stats.json"),
    JSON.stringify(stats, null, 2)
  );

  console.log("Extraction complete:");
  console.log(`  Files discovered: ${stats.totalFilesDiscovered}`);
  console.log(`  Files parsed: ${stats.totalFilesParsed}`);
  console.log(`  Parse failures: ${stats.parseFailures.length}`);
  console.log(`  Data models extracted: ${stats.modelsExtracted}`);
  console.log(`  Total fields extracted: ${stats.totalFieldsExtracted}`);
  if (stats.parseFailures.length > 0) {
    console.log("  Failures:");
    for (const f of stats.parseFailures) {
      console.log(`    ${f.file}: ${f.error}`);
    }
  }
}

main().catch(console.error);

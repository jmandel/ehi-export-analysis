#!/usr/bin/env bun
/**
 * Extracts the Healthie EHI Export data dictionary from the downloaded HTML page
 * into a structured JSON format.
 *
 * Usage: bun run extract-data-dictionary.ts
 *
 * Input: ../ehi-export-page.html
 * Output: ./data-dictionary.json, ./extraction-log.json
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "ehi-export-page.html");
const outputPath = join(scriptDir, "data-dictionary.json");
const logPath = join(scriptDir, "extraction-log.json");

interface Column {
  name: string;
  data_notes: string | null;
}

interface ExportFile {
  filename: string;
  type: "csv" | "pdf" | "html" | "folder";
  description: string | null;
  columns: Column[];
  row_semantics: string | null; // e.g. "For each CMS for the patient, there is a row in the CSV"
}

interface DataDictionary {
  source_url: string;
  extraction_date: string;
  export_overview: {
    format: string;
    population_export_structure: string;
    notes: string[];
  };
  export_generation: {
    single_patient: string;
    population: string;
  };
  files: ExportFile[];
  total_files: number;
  total_csv_files: number;
  total_columns: number;
}

const html = readFileSync(inputPath, "utf-8");

// Extract article content
const articleMatch = html.match(/id="fullArticle"[^>]*>(.*?)<\/article>/s);
if (!articleMatch) {
  console.error("Could not find article content");
  process.exit(1);
}
const article = articleMatch[1];

// Extract the file list from the bullet list
const fileListMatch = article.match(
  /Within the zip file the following.*?<ul>(.*?)<\/ul>/s
);
const fileListItems: string[] = [];
if (fileListMatch) {
  const items = fileListMatch[1].matchAll(/<li>(.*?)<\/li>/gs);
  for (const m of items) {
    const clean = m[1].replace(/<[^>]+>/g, "").trim();
    if (clean) fileListItems.push(clean);
  }
}

// Extract notes after the file list
const notesMatch = article.match(
  /Notes:<\/p>\s*<ul>(.*?)<\/ul>/s
);
const exportNotes: string[] = [];
if (notesMatch) {
  const items = notesMatch[1].matchAll(/<li>(.*?)<\/li>/gs);
  for (const m of items) {
    const clean = m[1].replace(/<[^>]+>/g, "").replace(/&nbsp;/g, " ").replace(/\s+/g, " ").trim();
    if (clean) exportNotes.push(clean);
  }
}

// Parse each file's format definition
// Pattern: <u>Filename format and data elements:</u> or <u>Filename format and data elements</u>
// followed by optional description paragraph, then a <table>

const files: ExportFile[] = [];
const parseErrors: Array<{ filename: string; error: string }> = [];

// Split by file format sections
const fileSections = article.split(/<p><u>/g).slice(1); // skip everything before first file def

for (const section of fileSections) {
  // Extract filename from the underlined header
  const headerMatch = section.match(
    /^([\w_.]+(?:\.csv|\.pdf|\.html)?)\s+format and data elements:?<\/u><\/p>/i
  );
  if (!headerMatch) {
    // Could be a non-file underlined section
    continue;
  }
  let rawFilename = headerMatch[1];

  // Fix known typos in the source HTML
  const typoFixes: Record<string, string> = {
    "MirroEntry": "MirrorEntry",
  };
  for (const [typo, fix] of Object.entries(typoFixes)) {
    if (rawFilename.startsWith(typo)) {
      rawFilename = rawFilename.replace(typo, fix);
    }
  }

  // Determine file type
  let type: "csv" | "pdf" | "html" | "folder" = "csv";
  let filename = rawFilename;
  if (rawFilename.endsWith(".pdf")) type = "pdf";
  else if (rawFilename.endsWith(".html")) type = "html";
  else if (!rawFilename.includes(".")) {
    // Check if it's in fileListItems with an extension
    const match = fileListItems.find(
      (f) => f.toLowerCase().startsWith(rawFilename.toLowerCase())
    );
    if (match) filename = match;
    if (filename.endsWith(".pdf")) type = "pdf";
    else if (filename === "Documents folder") type = "folder";
  }

  // Extract description (paragraph text before table)
  let description: string | null = null;
  let rowSemantics: string | null = null;

  // Look for paragraphs between the header and the table
  const beforeTable = section.split(/<table>/)[0];
  const paragraphs = beforeTable.matchAll(/<p>([^<].*?)<\/p>/gs);
  const descParts: string[] = [];
  for (const p of paragraphs) {
    const text = p[1]
      .replace(/<[^>]+>/g, "")
      .replace(/&nbsp;/g, " ")
      .replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">")
      .replace(/&amp;/g, "&")
      .replace(/\s+/g, " ")
      .trim();
    if (text && !text.startsWith("For example")) {
      if (text.match(/^For each .* there is a row/i)) {
        rowSemantics = text;
      } else {
        descParts.push(text);
      }
    }
  }
  if (descParts.length > 0) description = descParts.join(" ");

  // Extract table columns
  const columns: Column[] = [];
  const tableMatch = section.match(/<table>(.*?)<\/table>/s);
  if (tableMatch) {
    const tableHtml = tableMatch[1];
    const rows = tableHtml.matchAll(/<tr>(.*?)<\/tr>/gs);
    let hasDataNotes = false;
    let isHeaderRow = true;

    for (const row of rows) {
      const rowHtml = row[1];
      // Check if header row
      if (isHeaderRow) {
        hasDataNotes = /Data [Nn]otes/i.test(rowHtml);
        isHeaderRow = false;
        continue;
      }

      // Extract cells
      const cells = [...rowHtml.matchAll(/<t[dh]>(.*?)<\/t[dh]>/gs)];
      if (cells.length > 0) {
        const colName = cells[0][1]
          .replace(/<[^>]+>/g, "")
          .replace(/&nbsp;/g, " ")
          .replace(/\s+/g, " ")
          .trim();

        let dataNotes: string | null = null;
        if (hasDataNotes && cells.length > 1) {
          const raw = cells[1][1]
            .replace(/<[^>]+>/g, "")
            .replace(/&nbsp;/g, " ")
            .replace(/\s+/g, " ")
            .trim();
          if (raw) dataNotes = raw;
        }

        if (colName) {
          columns.push({ name: colName, data_notes: dataNotes });
        }
      }
    }
  }

  files.push({
    filename,
    type,
    description,
    columns,
    row_semantics: rowSemantics,
  });
}

// Add manually-defined entries for files without table definitions
const manualFiles: ExportFile[] = [
  {
    filename: "Documents folder",
    type: "folder",
    description:
      "Contains all documents saved in the patient's Documents page in Healthie. Documents are exported in their original format. Folder structure corresponds to the folder structure in the patient's Documents page.",
    columns: [],
    row_semantics: null,
  },
  {
    filename: "format.html",
    type: "html",
    description:
      "An HTML page included in the export that contains a publicly accessible hyperlink describing the export format.",
    columns: [],
    row_semantics: null,
  },
  {
    filename: "journal_entries.pdf",
    type: "pdf",
    description:
      "Contains all journal entries for the patient. Format and data elements are specific to an organization's and patient's entries.",
    columns: [],
    row_semantics: null,
  },
];

// Only add manual files if not already parsed
for (const mf of manualFiles) {
  const already = files.some(
    (f) => f.filename.toLowerCase() === mf.filename.toLowerCase()
  );
  if (!already) {
    files.push(mf);
  }
}

// Cross-check against the file list
const parsedFilenames = new Set(files.map((f) => f.filename.toLowerCase()));
const listedFiles = fileListItems.map((f) => f.toLowerCase());
const missingParsed = listedFiles.filter((f) => {
  // Check if any parsed file matches
  return !files.some(
    (pf) =>
      pf.filename.toLowerCase() === f ||
      pf.filename.toLowerCase() + ".csv" === f ||
      pf.filename.toLowerCase() === f.replace(" folder", "")
  );
});

const dataDictionary: DataDictionary = {
  source_url:
    "https://help.gethealthie.com/article/1200-b10-electronic-health-information-export-on-healthie",
  extraction_date: new Date().toISOString().split("T")[0],
  export_overview: {
    format:
      "CSV files, PDF files, and a Documents folder per patient, presented as a compressed zip file",
    population_export_structure:
      "One directory per patient named <FirstName><LastName><uniqueidentifier>",
    notes: exportNotes,
  },
  export_generation: {
    single_patient:
      "Navigate to patient profile > Charting section. Requires 'Can generate organization report' permission or non-organization user.",
    population:
      "Administrator-only. Handled by Healthie Support team. Email hello@gethealthie.com with subject 'Patient Population b10 export request'.",
  },
  files,
  total_files: files.length,
  total_csv_files: files.filter((f) => f.type === "csv").length,
  total_columns: files.reduce((sum, f) => sum + f.columns.length, 0),
};

writeFileSync(outputPath, JSON.stringify(dataDictionary, null, 2));

const log = {
  extraction_date: new Date().toISOString(),
  input_file: inputPath,
  output_file: outputPath,
  total_files_in_listing: fileListItems.length,
  total_files_parsed: files.length,
  total_columns_extracted: dataDictionary.total_columns,
  files_in_listing: fileListItems,
  files_parsed: files.map((f) => f.filename),
  missing_from_parse: missingParsed,
  parse_errors: parseErrors,
  files_by_type: {
    csv: files.filter((f) => f.type === "csv").length,
    pdf: files.filter((f) => f.type === "pdf").length,
    html: files.filter((f) => f.type === "html").length,
    folder: files.filter((f) => f.type === "folder").length,
  },
};

writeFileSync(logPath, JSON.stringify(log, null, 2));

console.log(`Extracted ${files.length} file definitions with ${dataDictionary.total_columns} total columns`);
console.log(`Listed files: ${fileListItems.length}, Parsed: ${files.length}`);
if (missingParsed.length > 0) {
  console.log(`Missing from parse: ${missingParsed.join(", ")}`);
}
console.log(`Output: ${outputPath}`);
console.log(`Log: ${logPath}`);

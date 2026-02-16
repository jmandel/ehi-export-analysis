#!/usr/bin/env bun
/**
 * Extract structured field definitions from MEDENT EHI export PDF specifications.
 *
 * Usage: bun run extract-ehi-specs.ts
 *
 * Requires: pdftotext (from poppler-utils) on PATH
 *
 * Input: ../ehi_pdfs/*.pdf
 * Output: ./ehi-specs.json, ./extraction-report.json
 */

import { readdir } from "node:fs/promises";
import { join, basename } from "node:path";

const EHI_DIR = join(import.meta.dir, "..", "ehi_pdfs");
const OUT_FILE = join(import.meta.dir, "ehi-specs.json");
const REPORT_FILE = join(import.meta.dir, "extraction-report.json");

interface Field {
  name: string;
  description: string;
}

interface FileSpec {
  filename: string;
  title: string;
  fields: Field[];
  example_present: boolean;
  raw_text: string;
  notes: string[];
}

interface ExtractionReport {
  total_files_discovered: number;
  total_files_parsed: number;
  parse_failures: { file: string; error: string }[];
  total_fields_extracted: number;
  specs_summary: { filename: string; title: string; field_count: number }[];
}

async function extractPdfText(pdfPath: string): Promise<string> {
  const proc = Bun.spawn(["pdftotext", "-layout", pdfPath, "-"], {
    stdout: "pipe",
    stderr: "pipe",
  });
  const text = await new Response(proc.stdout).text();
  await proc.exited;
  return text;
}

function parseSpecFields(text: string, filename: string): FileSpec {
  const lines = text.split("\n");
  const title = lines.find((l) => l.trim().length > 0)?.trim() || filename;

  // Detect if it's the main setup doc (different format)
  if (filename.includes("EHI_Setup") || filename.includes("Info_File")) {
    return {
      filename,
      title,
      fields: [],
      example_present: false,
      raw_text: text,
      notes: [
        filename.includes("EHI_Setup")
          ? "Setup/configuration document - not a field specification"
          : "Info file describes export metadata, not patient data fields",
      ],
    };
  }

  const fields: Field[] = [];
  const notes: string[] = [];

  // Strategy: find "Field Name" or "Field Names" header, then collect field names
  // and find "Field Description" or "Field Definition" header, then collect descriptions
  // PDFs have two-column layout: field names on left, descriptions on right

  // First try to find field name/description pairs from the raw text
  // The PDFs consistently have field_name entries that are snake_case or camelCase identifiers
  const fieldNamePattern = /^[a-z][a-z0-9_]*(?:_[a-z0-9]+)*$/i;
  const potentialFields: string[] = [];

  // Collect all lines that look like field names
  for (const line of lines) {
    const trimmed = line.trim();
    if (
      trimmed &&
      fieldNamePattern.test(trimmed) &&
      !trimmed.includes(" ") &&
      trimmed.length > 2 &&
      trimmed !== "Example" &&
      trimmed !== "Output"
    ) {
      potentialFields.push(trimmed);
    }
  }

  // Also look for explicit field patterns like "field_name   Description text"
  // In the layout-extracted text, fields and descriptions may be on the same line
  const twoColPattern =
    /^(\s*)([a-z][a-z0-9_]*(?:_[a-z0-9]+)*)\s{3,}(.+)$/i;
  const twoColFields: Field[] = [];

  for (const line of lines) {
    const match = line.match(twoColPattern);
    if (match) {
      const name = match[2].trim();
      const desc = match[3].trim();
      if (
        name.length > 2 &&
        name !== "Example" &&
        name !== "Output" &&
        desc.length > 2
      ) {
        twoColFields.push({ name, description: desc });
      }
    }
  }

  // Use two-column extraction if we got good results
  if (twoColFields.length > 3) {
    fields.push(...twoColFields);
  } else if (potentialFields.length > 0) {
    // Fallback: just list fields without descriptions
    for (const f of potentialFields) {
      fields.push({ name: f, description: "" });
    }
  }

  // Deduplicate fields by name (keep first occurrence)
  const seen = new Set<string>();
  const dedupedFields: Field[] = [];
  for (const f of fields) {
    const key = f.name.toLowerCase();
    if (!seen.has(key)) {
      seen.add(key);
      dedupedFields.push(f);
    }
  }

  const examplePresent =
    text.includes("Example Output") || text.includes("Example Ou");

  return {
    filename,
    title,
    fields: dedupedFields,
    example_present: examplePresent,
    raw_text: text,
    notes,
  };
}

async function main() {
  const files = (await readdir(EHI_DIR)).filter((f) => f.endsWith(".pdf"));
  files.sort();

  console.log(`Found ${files.length} PDF files in ${EHI_DIR}`);

  const specs: FileSpec[] = [];
  const failures: { file: string; error: string }[] = [];

  for (const file of files) {
    const pdfPath = join(EHI_DIR, file);
    try {
      console.log(`Processing: ${file}`);
      const text = await extractPdfText(pdfPath);
      const spec = parseSpecFields(text, file);
      specs.push(spec);
      console.log(`  -> ${spec.fields.length} fields, title: ${spec.title}`);
    } catch (e: any) {
      console.error(`  FAILED: ${e.message}`);
      failures.push({ file, error: e.message });
    }
  }

  // Write specs (without raw_text for the queryable output)
  const queryableSpecs = specs.map(({ raw_text, ...rest }) => rest);
  await Bun.write(OUT_FILE, JSON.stringify(queryableSpecs, null, 2));
  console.log(`\nWrote ${OUT_FILE}`);

  // Write raw text versions too for reference
  const rawSpecs = specs.map((s) => ({
    filename: s.filename,
    title: s.title,
    raw_text: s.raw_text,
  }));
  await Bun.write(
    join(import.meta.dir, "ehi-specs-raw.json"),
    JSON.stringify(rawSpecs, null, 2)
  );

  // Write report
  const totalFields = specs.reduce((sum, s) => sum + s.fields.length, 0);
  const report: ExtractionReport = {
    total_files_discovered: files.length,
    total_files_parsed: specs.length,
    parse_failures: failures,
    total_fields_extracted: totalFields,
    specs_summary: specs.map((s) => ({
      filename: s.filename,
      title: s.title,
      field_count: s.fields.length,
    })),
  };
  await Bun.write(REPORT_FILE, JSON.stringify(report, null, 2));
  console.log(`Wrote ${REPORT_FILE}`);
  console.log(
    `\nSummary: ${specs.length}/${files.length} parsed, ${totalFields} total fields, ${failures.length} failures`
  );
}

main();

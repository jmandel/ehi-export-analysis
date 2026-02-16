/**
 * Extracts document type definitions from the PrimeSuite EHI Export XML Document Reference HTML
 * into structured JSON.
 *
 * Input:  ../PrimeSuiteEHIExport_Document_Reference.html
 * Output: xml-reference.json
 *         xml-reference-stats.json
 *
 * Run: bun run extract-xml-reference.ts
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "PrimeSuiteEHIExport_Document_Reference.html");
const outputPath = join(scriptDir, "xml-reference.json");
const statsPath = join(scriptDir, "xml-reference-stats.json");

interface FileType {
  id: string;
  name: string;
  description: string;
}

interface DocumentSection {
  heading: string;
  level: number;
  textContent: string;
  tables: { headers: string[]; rows: string[][] }[];
}

const html = readFileSync(inputPath, "utf-8");

// Extract file type list (the table at the beginning listing filetypeIDs and names)
const fileTypes: FileType[] = [];
const sections: DocumentSection[] = [];
const failures: { context: string; error: string }[] = [];

// Find all tables in the page
const tablePattern = /<table[\s\S]*?<\/table>/gi;
let tableMatch: RegExpExecArray | null;
const allTables: { index: number; html: string }[] = [];

while ((tableMatch = tablePattern.exec(html)) !== null) {
  allTables.push({ index: tableMatch.index, html: tableMatch[0] });
}

// Extract file type list from the first significant table (if it has filetypeID-like data)
for (const tbl of allTables) {
  const rows = tbl.html.match(/<tr[\s\S]*?<\/tr>/gi);
  if (!rows || rows.length < 2) continue;

  const headerCells = rows[0].match(/<th[^>]*>([\s\S]*?)<\/th>/gi);
  if (!headerCells) continue;

  const headers = headerCells.map((c) => c.replace(/<[^>]*>/g, "").trim());

  for (let r = 1; r < rows.length; r++) {
    const cells = rows[r].match(/<td[^>]*>([\s\S]*?)<\/td>/gi);
    if (!cells) continue;
    const cellTexts = cells.map((c) => c.replace(/<[^>]*>/g, "").trim());

    // If this looks like a file type table with IDs
    if (headers.length >= 2) {
      const row: Record<string, string> = {};
      headers.forEach((h, idx) => {
        row[h] = cellTexts[idx] || "";
      });

      // Check if any cell looks like a numeric file type ID
      const hasId = cellTexts.some((c) => /^\d{3,5}$/.test(c));
      if (hasId) {
        fileTypes.push({
          id: cellTexts[0],
          name: cellTexts.length > 1 ? cellTexts[1] : "",
          description: cellTexts.length > 2 ? cellTexts.slice(2).join(" ") : "",
        });
      }
    }
  }
}

// Extract all headings and their content as sections
const headingPattern = /<h([23])[^>]*>([^<]+(?:<[^/][^>]*>[^<]*)*)/gi;
let headingMatch: RegExpExecArray | null;
const headingPositions: { level: number; heading: string; index: number }[] = [];

// Reset and re-run
headingPattern.lastIndex = 0;
while ((headingMatch = headingPattern.exec(html)) !== null) {
  headingPositions.push({
    level: parseInt(headingMatch[1]),
    heading: headingMatch[2].replace(/<[^>]*>/g, "").trim(),
    index: headingMatch.index,
  });
}

for (let i = 0; i < headingPositions.length; i++) {
  const pos = headingPositions[i];
  const nextIndex = i + 1 < headingPositions.length ? headingPositions[i + 1].index : html.length;
  const sectionHtml = html.slice(pos.index, nextIndex);

  try {
    // Extract text content (strip tags)
    const textContent = sectionHtml
      .replace(/<script[\s\S]*?<\/script>/gi, "")
      .replace(/<style[\s\S]*?<\/style>/gi, "")
      .replace(/<img[^>]*>/gi, "[image]")
      .replace(/<[^>]*>/g, " ")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 2000); // Limit text content

    // Extract tables within this section
    const sectionTables: { headers: string[]; rows: string[][] }[] = [];
    const tblMatches = sectionHtml.match(/<table[\s\S]*?<\/table>/gi);
    if (tblMatches) {
      for (const tblHtml of tblMatches) {
        const rows = tblHtml.match(/<tr[\s\S]*?<\/tr>/gi);
        if (!rows) continue;

        const headerCells = rows[0].match(/<th[^>]*>([\s\S]*?)<\/th>/gi);
        const headers = headerCells
          ? headerCells.map((c) => c.replace(/<[^>]*>/g, "").trim())
          : [];

        const dataRows: string[][] = [];
        for (let r = 1; r < rows.length; r++) {
          const cells = rows[r].match(/<td[^>]*>([\s\S]*?)<\/td>/gi);
          if (cells) {
            dataRows.push(cells.map((c) => c.replace(/<[^>]*>/g, "").trim()));
          }
        }

        sectionTables.push({ headers, rows: dataRows });
      }
    }

    sections.push({
      heading: pos.heading,
      level: pos.level,
      textContent,
      tables: sectionTables,
    });
  } catch (err: any) {
    failures.push({
      context: pos.heading,
      error: err.message || String(err),
    });
  }
}

const output = {
  fileTypes,
  sections,
};

writeFileSync(outputPath, JSON.stringify(output, null, 2));

const stats = {
  input_file: "PrimeSuiteEHIExport_Document_Reference.html",
  total_sections_discovered: headingPositions.length,
  total_sections_parsed: sections.length,
  total_file_types_extracted: fileTypes.length,
  total_tables_in_sections: sections.reduce((sum, s) => sum + s.tables.length, 0),
  parse_failures: failures.length,
  failure_details: failures,
};

writeFileSync(statsPath, JSON.stringify(stats, null, 2));

console.log(`Extracted ${sections.length} sections, ${fileTypes.length} file types`);
console.log(`Parse failures: ${failures.length}`);
console.log(`Output: ${outputPath}`);
console.log(`Stats: ${statsPath}`);

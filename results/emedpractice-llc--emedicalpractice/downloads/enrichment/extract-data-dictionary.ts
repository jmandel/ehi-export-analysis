#!/usr/bin/env bun
/**
 * Extracts EHI data dictionary table schemas from the eMedPractice
 * WordPress JSON API response and the main EHI export page content.
 *
 * Input: ../ehi-data-dictionary-tables-api.json (WP JSON API page response)
 *        ../ehi-export-page-api.json (WP JSON API page response for main page)
 * Output: ./data-dictionary.json — structured table schemas
 *         ./ehi-export-content.json — structured export page content
 *         ./extraction-report.json — accounting of what was parsed
 */

import { readFileSync, writeFileSync } from "fs";
import { join } from "path";

const DOWNLOADS_DIR = join(import.meta.dir, "..");

interface Column {
  name: string;
  dataType: string;
  defaultValue: string | null;
  notNull: boolean;
}

interface TableSchema {
  tableName: string;
  columns: Column[];
}

interface ExportSection {
  heading: string;
  content: string[];
  links: { text: string; url: string }[];
}

interface ExtractionReport {
  inputFiles: {
    path: string;
    sizeBytes: number;
    parsed: boolean;
    error?: string;
  }[];
  tablesExtracted: number;
  totalColumns: number;
  exportSectionsExtracted: number;
  commentedOutSections: string[];
  timestamp: string;
}

function parseHtmlTables(html: string): TableSchema[] {
  const tables: TableSchema[] = [];

  // Find all table headings (h2 elements followed by tables)
  const tablePattern =
    /<h2[^>]*>([^<]+)<\/h2>[\s\S]*?<table[^>]*class="schema"[^>]*>[\s\S]*?<tbody>([\s\S]*?)<\/tbody>/g;

  let match;
  while ((match = tablePattern.exec(html)) !== null) {
    const tableName = match[1].trim();
    const tbodyHtml = match[2];

    const columns: Column[] = [];
    const rowPattern = /<tr>([\s\S]*?)<\/tr>/g;
    let rowMatch;
    while ((rowMatch = rowPattern.exec(tbodyHtml)) !== null) {
      const cells: string[] = [];
      const cellPattern = /<td[^>]*>([\s\S]*?)<\/td>/g;
      let cellMatch;
      while ((cellMatch = cellPattern.exec(rowMatch[1])) !== null) {
        // Strip HTML tags from cell content
        cells.push(cellMatch[1].replace(/<[^>]*>/g, "").trim());
      }
      if (cells.length >= 4) {
        columns.push({
          name: cells[0],
          dataType: cells[1],
          defaultValue: cells[2] || null,
          notNull: cells[3] === "Not Null",
        });
      }
    }

    if (columns.length > 0) {
      tables.push({ tableName, columns });
    }
  }

  return tables;
}

function parseExportPageContent(html: string): {
  sections: ExportSection[];
  commentedOut: string[];
} {
  const sections: ExportSection[] = [];
  const commentedOut: string[] = [];

  // Extract commented-out sections
  const commentPattern = /<!--([\s\S]*?)-->/g;
  let commentMatch;
  while ((commentMatch = commentPattern.exec(html)) !== null) {
    const content = commentMatch[1].trim();
    if (content.length > 50) {
      // Only meaningful comments
      commentedOut.push(
        content.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim()
      );
    }
  }

  // Extract section headings and their content
  const sectionPattern =
    /<h3[^>]*class="sub-header"[^>]*>([\s\S]*?)<\/h3>([\s\S]*?)(?=<h3|<div class="note"|$)/g;
  let sectionMatch;
  while ((sectionMatch = sectionPattern.exec(html)) !== null) {
    const heading = sectionMatch[1].replace(/<[^>]*>/g, "").trim();
    const body = sectionMatch[2];

    // Extract list items
    const items: string[] = [];
    const liPattern = /<li>([\s\S]*?)<\/li>/g;
    let liMatch;
    while ((liMatch = liPattern.exec(body)) !== null) {
      items.push(liMatch[1].replace(/<[^>]*>/g, "").trim());
    }

    // Extract links
    const links: { text: string; url: string }[] = [];
    const linkPattern = /<a[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/g;
    let linkMatch;
    while ((linkMatch = linkPattern.exec(body)) !== null) {
      links.push({
        url: linkMatch[1],
        text: linkMatch[2].replace(/<[^>]*>/g, "").trim(),
      });
    }

    sections.push({ heading, content: items, links });
  }

  // Also extract the Notes section
  const notesPattern =
    /<div class="note">\s*<h3[^>]*>Notes:<\/h3>([\s\S]*?)<\/div>/;
  const notesMatch = notesPattern.exec(html);
  if (notesMatch) {
    const items: string[] = [];
    const liPattern = /<li>([\s\S]*?)<\/li>/g;
    let liMatch;
    while ((liMatch = liPattern.exec(notesMatch[1])) !== null) {
      items.push(liMatch[1].replace(/<[^>]*>/g, "").trim());
    }
    sections.push({ heading: "Notes", content: items, links: [] });
  }

  // Extract the intro paragraph
  const introPattern =
    /<p>(In our commitment[\s\S]*?)<\/p>/;
  const introMatch = introPattern.exec(html);
  if (introMatch) {
    sections.unshift({
      heading: "Introduction",
      content: [introMatch[1].replace(/<[^>]*>/g, "").trim()],
      links: [],
    });
  }

  return { sections, commentedOut };
}

// Main execution
const report: ExtractionReport = {
  inputFiles: [],
  tablesExtracted: 0,
  totalColumns: 0,
  exportSectionsExtracted: 0,
  commentedOutSections: [],
  timestamp: new Date().toISOString(),
};

// Parse data dictionary page
const dictApiPath = join(DOWNLOADS_DIR, "ehi-data-dictionary-tables-api.json");
let allTables: TableSchema[] = [];
try {
  const dictRaw = readFileSync(dictApiPath, "utf-8");
  const dictData = JSON.parse(dictRaw);
  const pageContent = Array.isArray(dictData)
    ? dictData[0].content.rendered
    : dictData.content.rendered;

  allTables = parseHtmlTables(pageContent);

  // Deduplicate: the page has two copies (one hidden with d-none, one visible)
  // Also fix table names: "EHI Data Dictionary Tables" is a page header, not a table name
  const seen = new Set<string>();
  const uniqueTables: TableSchema[] = [];
  for (const t of allTables) {
    // Normalize table names that aren't actual schema names
    if (t.tableName === "EHI Data Dictionary Tables") {
      t.tableName = "Patients Table Schema"; // This is the first patients table
    }
    const key = t.tableName + ":" + t.columns.length;
    if (!seen.has(key)) {
      seen.add(key);
      uniqueTables.push(t);
    }
  }
  allTables = uniqueTables;

  report.inputFiles.push({
    path: "ehi-data-dictionary-tables-api.json",
    sizeBytes: dictRaw.length,
    parsed: true,
  });
} catch (err: any) {
  report.inputFiles.push({
    path: "ehi-data-dictionary-tables-api.json",
    sizeBytes: 0,
    parsed: false,
    error: err.message,
  });
}

report.tablesExtracted = allTables.length;
report.totalColumns = allTables.reduce((s, t) => s + t.columns.length, 0);

// Parse main export page
const exportApiPath = join(DOWNLOADS_DIR, "ehi-export-page-api.json");
let exportContent: { sections: ExportSection[]; commentedOut: string[] } = {
  sections: [],
  commentedOut: [],
};
try {
  const exportRaw = readFileSync(exportApiPath, "utf-8");
  const exportData = JSON.parse(exportRaw);
  const pageContent = exportData.content.rendered;

  exportContent = parseExportPageContent(pageContent);

  report.inputFiles.push({
    path: "ehi-export-page-api.json",
    sizeBytes: exportRaw.length,
    parsed: true,
  });
} catch (err: any) {
  report.inputFiles.push({
    path: "ehi-export-page-api.json",
    sizeBytes: 0,
    parsed: false,
    error: err.message,
  });
}

report.exportSectionsExtracted = exportContent.sections.length;
report.commentedOutSections = exportContent.commentedOut;

// Write outputs
const enrichmentDir = join(DOWNLOADS_DIR, "enrichment");

writeFileSync(
  join(enrichmentDir, "data-dictionary.json"),
  JSON.stringify(
    {
      source: "https://emedpractice.com/electronic-health-information-data-dictionary-tables/",
      extractedAt: new Date().toISOString(),
      tables: allTables,
    },
    null,
    2
  )
);

writeFileSync(
  join(enrichmentDir, "ehi-export-content.json"),
  JSON.stringify(
    {
      source: "https://emedpractice.com/electronic-health-information-export/",
      extractedAt: new Date().toISOString(),
      sections: exportContent.sections,
      commentedOutSections: exportContent.commentedOut,
    },
    null,
    2
  )
);

writeFileSync(
  join(enrichmentDir, "extraction-report.json"),
  JSON.stringify(report, null, 2)
);

console.log("Extraction complete:");
console.log(`  Tables: ${report.tablesExtracted}`);
console.log(`  Columns: ${report.totalColumns}`);
console.log(`  Export sections: ${report.exportSectionsExtracted}`);
console.log(`  Commented-out sections: ${report.commentedOutSections.length}`);
console.log(`  Input files: ${report.inputFiles.length} (${report.inputFiles.filter((f) => f.parsed).length} parsed)`);

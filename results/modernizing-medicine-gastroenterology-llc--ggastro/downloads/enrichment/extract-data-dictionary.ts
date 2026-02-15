/**
 * Parses the gGastro EHI Patient Export Specifications PDF (text extracted with pdftotext -layout)
 * and produces structured JSON with:
 * - CSV file (table) definitions with fields, types, lengths, and translation references
 * - Data schema (table relationships)
 * - Translation tables (value sets)
 * - Patient document instructions
 * - Glossary
 *
 * Usage: bun run extract-data-dictionary.ts
 * Input: main-pdf-layout.txt (from pdftotext -layout on the main PDF)
 * Output: data-dictionary.json
 */

import { readFileSync, writeFileSync } from "fs";
import { join } from "path";

const DIR = import.meta.dir;
const inputFile = join(DIR, "main-pdf-layout.txt");
const outputFile = join(DIR, "data-dictionary.json");

const text = readFileSync(inputFile, "utf-8");
const lines = text.split("\n");

interface Field {
  index: number;
  name: string;
  type: string;
  length: number | null;
  format_or_translation: string | null;
}

interface Table {
  name: string;
  fields: Field[];
  line_number: number;
}

interface Relationship {
  parent: string;
  child: string;
  foreign_key: string;
  depth: number;
}

interface TranslationEntry {
  code: string;
  value: string;
}

interface TranslationTable {
  name: string;
  entries: TranslationEntry[];
}

// === Parse CSV Files Dictionary ===
function parseTables(): Table[] {
  const tables: Table[] = [];

  // Find the CSV Files Dictionary section
  let startLine = 0;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim() === "CSV Files Dictionary" && i > 5) {
      startLine = i + 1;
      break;
    }
  }

  // Find end of CSV Files Dictionary (Data Schema section)
  let endLine = lines.length;
  for (let i = startLine; i < lines.length; i++) {
    if (lines[i].trim() === "Data Schema") {
      endLine = i;
      break;
    }
  }

  let currentTable: Table | null = null;

  for (let i = startLine; i < endLine; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    if (!trimmed) continue;
    if (trimmed === "Column Number - Name") continue;
    if (trimmed.startsWith("Type") && trimmed.length < 10) continue;
    if (trimmed === "Length") continue;
    if (trimmed === "Format/Translation/Comments") continue;

    // Check if this is a table name: standalone PascalCase word not starting with a digit
    // Table names appear before their "0 - " field definition
    const fieldMatch = trimmed.match(/^(\d+)\s+-\s+(\S+)/);

    if (fieldMatch) {
      const index = parseInt(fieldMatch[1]);
      const fieldName = fieldMatch[2];

      // Parse the rest of the line for type, length, format
      // The layout has columns roughly at: Name (~col 0-40), Type (~col 42-56), Length (~col 56-64), Format (~col 64+)
      const typeMatch = line.match(
        /\s+(GUID|Boolean|Numeric|Decimal|Alphanumeric|Date & Time|Score)\s*/
      );
      let type = typeMatch ? typeMatch[1] : "";
      let length: number | null = null;
      let formatOrTranslation: string | null = null;

      if (typeMatch) {
        const afterType =
          line.substring(
            (typeMatch.index || 0) + typeMatch[0].length
          );
        const parts = afterType.trim();
        // Check if it starts with a number (length)
        const lenMatch = parts.match(/^(\d+)\s*(.*)/);
        if (lenMatch) {
          length = parseInt(lenMatch[1]);
          if (lenMatch[2].trim()) {
            formatOrTranslation = lenMatch[2].trim();
          }
        } else if (parts) {
          formatOrTranslation = parts;
        }
      }

      if (currentTable) {
        currentTable.fields.push({
          index,
          name: fieldName,
          type,
          length,
          format_or_translation: formatOrTranslation || null,
        });
      }
    } else if (
      /^[A-Z][a-zA-Z0-9]+$/.test(trimmed) &&
      !["GUID", "Boolean", "Numeric", "Decimal", "Alphanumeric", "Score"].includes(trimmed)
    ) {
      // This looks like a table name
      // Verify by checking if the next non-empty line starts with "0 - " or "Column Number"
      let isTable = false;
      for (let j = i + 1; j < Math.min(i + 5, endLine); j++) {
        const nextTrimmed = lines[j].trim();
        if (!nextTrimmed) continue;
        if (nextTrimmed.startsWith("0 - ") || nextTrimmed.startsWith("Column Number")) {
          isTable = true;
        }
        break;
      }

      if (isTable) {
        if (currentTable) {
          tables.push(currentTable);
        }
        currentTable = { name: trimmed, fields: [], line_number: i + 1 };
      }
    }
  }

  if (currentTable) {
    tables.push(currentTable);
  }

  return tables;
}

// === Parse Data Schema (relationships) ===
function parseRelationships(): Relationship[] {
  const relationships: Relationship[] = [];

  let startLine = 0;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim() === "Data Schema") {
      startLine = i + 1;
      break;
    }
  }

  let endLine = lines.length;
  for (let i = startLine; i < lines.length; i++) {
    if (lines[i].trim() === "Translations") {
      endLine = i;
      break;
    }
  }

  // Parse the tree structure
  // Lines look like: |   |       | |-------- TableName          FieldName
  // or:              +-------- TableName          FieldName
  const tableStack: string[] = [];

  for (let i = startLine; i < endLine; i++) {
    const line = lines[i];
    const trimmed = line.trim();
    if (!trimmed) continue;
    if (trimmed === "Related Tables" || trimmed === "Related Field") continue;

    // Match tree lines
    const match = line.match(
      /^([\s|+\-]*?)(?:\|?\s*[|+]?-{4,8})\s+(\S+)\s+(\S+)\s*$/
    );
    if (match) {
      const prefix = match[1];
      const tableName = match[2];
      const fieldName = match[3];

      // Calculate depth from prefix
      // Each level adds "|   " or "    " (4 chars roughly)
      const depth = Math.floor(prefix.replace(/[^|]/g, "").length);

      // Determine parent
      let parent = "Patient"; // default root
      if (depth === 0) {
        parent = "Patient";
      } else if (tableStack.length >= depth) {
        parent = tableStack[depth - 1];
      }

      // Update stack
      tableStack[depth] = tableName;
      tableStack.length = depth + 1;

      relationships.push({
        parent,
        child: tableName,
        foreign_key: fieldName,
        depth,
      });
    }
  }

  return relationships;
}

// === Parse Translations ===
function parseTranslations(): TranslationTable[] {
  const translations: TranslationTable[] = [];

  let startLine = 0;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim() === "Translations" && i > 100) {
      startLine = i + 1;
      break;
    }
  }

  let endLine = lines.length;
  for (let i = startLine; i < lines.length; i++) {
    if (lines[i].trim() === "Patient Documents") {
      endLine = i;
      break;
    }
  }

  let currentTranslation: TranslationTable | null = null;

  for (let i = startLine; i < endLine; i++) {
    const line = lines[i];
    const trimmed = line.trim();
    if (!trimmed) {
      if (currentTranslation && currentTranslation.entries.length > 0) {
        translations.push(currentTranslation);
        currentTranslation = null;
      }
      continue;
    }

    // Check if this is a section header (a short title line)
    // Translation headers don't contain GUIDs or numeric code patterns
    const hasGuid = /[0-9a-f]{8}-[0-9a-f]{4}/.test(trimmed);
    const hasNumericCodes = /^\d+\s+\S/.test(trimmed);

    if (!hasGuid && !hasNumericCodes && trimmed.length < 100 && /^[A-Z]/.test(trimmed)) {
      // Potential header
      if (currentTranslation && currentTranslation.entries.length > 0) {
        translations.push(currentTranslation);
      }
      currentTranslation = { name: trimmed, entries: [] };
      continue;
    }

    if (!currentTranslation) continue;

    // Parse entries - they come in two formats:
    // 1. GUID: value  (for GUID-based translations)
    // 2. number  value  (for numeric-based translations)

    // GUID-based entries (may have multiple per line)
    const guidPattern =
      /([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}):\s*([^0-9a-fA-F\n][^\n]*?)(?=\s{2,}[0-9a-fA-F]{8}-|$)/g;
    let guidMatch;
    let foundGuid = false;
    while ((guidMatch = guidPattern.exec(trimmed)) !== null) {
      foundGuid = true;
      currentTranslation.entries.push({
        code: guidMatch[1],
        value: guidMatch[2].trim(),
      });
    }

    if (!foundGuid) {
      // Numeric-based entries (multiple per line, separated by spaces)
      // Format: "0  value1  1  value2  2  value3"
      const numPattern = /(\d+)\s{2,}([A-Za-z][A-Za-z0-9 ]*?)(?=\s{2,}\d|\s*$)/g;
      let numMatch;
      while ((numMatch = numPattern.exec(trimmed)) !== null) {
        currentTranslation.entries.push({
          code: numMatch[1],
          value: numMatch[2].trim(),
        });
      }
    }
  }

  if (currentTranslation && currentTranslation.entries.length > 0) {
    translations.push(currentTranslation);
  }

  return translations;
}

// === Parse Glossary ===
function parseGlossary(): Record<string, string> {
  const glossary: Record<string, string> = {};

  let startLine = 0;
  for (let i = lines.length - 1; i >= 0; i--) {
    if (lines[i].trim() === "Glossary") {
      startLine = i + 1;
      break;
    }
  }

  for (let i = startLine; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();
    if (!trimmed) continue;

    // Glossary entries have term followed by spaces then definition
    const match = line.match(/^(\S[\S ]*?)\s{3,}(.+)$/);
    if (match) {
      const term = match[1].trim();
      const def = match[2].trim();
      glossary[term] = def;
    }
  }

  return glossary;
}

// === Main ===
const tables = parseTables();
const relationships = parseRelationships();
const translations = parseTranslations();
const glossary = parseGlossary();

const result = {
  metadata: {
    source: "gGastro EHI Patient Export Specifications",
    version: "6.5.3.20251230",
    extraction_date: new Date().toISOString().split("T")[0],
    source_pdf: "gGastro-EHI-Patient-Export-Specifications.pdf",
  },
  summary: {
    total_tables: tables.length,
    total_fields: tables.reduce((sum, t) => sum + t.fields.length, 0),
    total_relationships: relationships.length,
    total_translation_tables: translations.length,
    total_translation_entries: translations.reduce(
      (sum, t) => sum + t.entries.length,
      0
    ),
    glossary_terms: Object.keys(glossary).length,
  },
  tables,
  relationships,
  translations,
  glossary,
};

writeFileSync(outputFile, JSON.stringify(result, null, 2));

console.log("=== Extraction Summary ===");
console.log(`Tables: ${result.summary.total_tables}`);
console.log(`Fields: ${result.summary.total_fields}`);
console.log(`Relationships: ${result.summary.total_relationships}`);
console.log(`Translation tables: ${result.summary.total_translation_tables}`);
console.log(`Translation entries: ${result.summary.total_translation_entries}`);
console.log(`Glossary terms: ${result.summary.glossary_terms}`);
console.log(`\nOutput: ${outputFile}`);

// Print table names for verification
console.log("\n=== Table Names ===");
tables.forEach((t) => console.log(`  ${t.name} (${t.fields.length} fields)`));

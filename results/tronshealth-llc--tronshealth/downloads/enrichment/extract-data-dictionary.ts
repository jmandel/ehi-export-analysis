#!/usr/bin/env bun
/**
 * Extracts the EHI export data dictionary from the TronsHealth PDF.
 * Uses pdftotext -layout for spatial column preservation, then parses field tables.
 *
 * Run: bun run extract-data-dictionary.ts
 * Input: ../170.315b10-Electronic-Health-Information-Export-EHI.pdf
 * Output: data-dictionary.json, extraction-stats.json
 */

import { $ } from "bun";

const PDF_PATH = new URL(
  "../170.315b10-Electronic-Health-Information-Export-EHI.pdf",
  import.meta.url
).pathname;

interface Field {
  name: string;
  dataType: string;
  description: string;
}

interface Entity {
  sectionNumber: string;
  name: string;
  fields: Field[];
}

interface DataDictionary {
  vendor: string;
  product: string;
  documentDate: string;
  exportFormat: string;
  entities: Entity[];
  tocSections: string[];
  missingSections: string[];
}

// Extract text with layout preservation
const rawText = (
  await $`pdftotext -layout ${PDF_PATH} -`.text()
).toString();

// Parse TOC sections
const tocPattern = /^\s*(3\.\d+)\.\s+Patient\s+[–-]\s+(.+?)\s*\.{2,}/gm;
const tocSections: string[] = [];
let tocMatch;
while ((tocMatch = tocPattern.exec(rawText)) !== null) {
  tocSections.push(`${tocMatch[1]}. Patient – ${tocMatch[2].trim()}`);
}

// Known data types
const DATA_TYPES = new Set([
  "long",
  "varchar",
  "nvarchar",
  "int",
  "boolean",
  "bool",
  "datetime",
  "decimal",
  "string",
  "list",
]);

function isDataType(s: string): boolean {
  return DATA_TYPES.has(s.toLowerCase().trim());
}

// Split the document into sections based on "3.X. Patient – Name" headers
// (excluding TOC entries which have dots after them)
const lines = rawText.split("\n");

interface SectionBlock {
  num: string;
  name: string;
  startLine: number;
}

const sections: SectionBlock[] = [];
const sectionHeaderRe = /^(3\.\d+)\.\s+Patient\s+[–-]\s+(.+?)\s*$/;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i].trim();
  const m = line.match(sectionHeaderRe);
  if (m) {
    // Skip TOC entries - they're indented and have dots
    if (lines[i].includes("...")) continue;
    sections.push({ num: m[1], name: m[2].trim(), startLine: i });
  }
}

const entities: Entity[] = [];

for (let si = 0; si < sections.length; si++) {
  const section = sections[si];
  const endLine =
    si + 1 < sections.length ? sections[si + 1].startLine : lines.length;
  const sectionLines = lines.slice(section.startLine, endLine);

  // Special case: Documents & Images
  if (section.name === "Documents & Images") {
    entities.push({
      sectionNumber: section.num,
      name: `Patient – ${section.name}`,
      fields: [
        {
          name: "Document",
          dataType: "file",
          description:
            "All documents downloaded in their actual/native format (png, jpeg, jpg) under documents folder.",
        },
      ],
    });
    continue;
  }

  // Find the "Field   Data Type   Detail" header row
  let tableStartIdx = -1;
  for (let i = 0; i < sectionLines.length; i++) {
    if (/Field\s+Data\s*Type\s+Detail/i.test(sectionLines[i])) {
      tableStartIdx = i + 1;
      break;
    }
  }

  if (tableStartIdx === -1) {
    entities.push({
      sectionNumber: section.num,
      name: `Patient – ${section.name}`,
      fields: [],
    });
    continue;
  }

  // Parse the table rows using the layout-preserved spacing
  // In layout mode, columns are separated by multiple spaces
  const fields: Field[] = [];
  let currentField: { name: string; dataType: string; desc: string[] } | null =
    null;

  for (let i = tableStartIdx; i < sectionLines.length; i++) {
    const line = sectionLines[i];
    const trimmed = line.trim();

    // Skip empty lines, page numbers, footers
    if (!trimmed) continue;
    if (/^\d+$/.test(trimmed)) continue;
    if (trimmed.startsWith("©2024")) continue;
    if (trimmed === "TronsHealth") continue;
    if (trimmed.includes("All Rights Reserved")) continue;

    // Try to parse as a table row with columns
    // Layout format: "FieldName        datatype    Description text"
    // Columns are separated by 2+ spaces

    // Check if this line starts a new field row
    // A new field row starts with a non-space or minimal indent, followed by spaces then a data type
    const rowMatch = line.match(
      /^\s{0,2}(\S+(?:\s\S+)?)\s{2,}(long|varchar|nvarchar|int|boolean|bool|datetime|decimal|string|list)\s{2,}(.+)/i
    );

    if (rowMatch) {
      // Save previous field
      if (currentField) {
        fields.push({
          name: currentField.name,
          dataType: currentField.dataType,
          description: currentField.desc.join(" ").trim(),
        });
      }
      currentField = {
        name: rowMatch[1].replace(/\s+/g, ""),
        dataType: rowMatch[2].toLowerCase(),
        desc: [rowMatch[3].trim()],
      };
      continue;
    }

    // Check for a field name on its own line (continued from previous line split)
    // or a continuation of the description (indented text)
    // A field name + type but description on next line:
    const fieldTypeOnly = line.match(
      /^\s{0,2}(\S+(?:\s\S+)?)\s{2,}(long|varchar|nvarchar|int|boolean|bool|datetime|decimal|string|list)\s*$/i
    );

    if (fieldTypeOnly) {
      if (currentField) {
        fields.push({
          name: currentField.name,
          dataType: currentField.dataType,
          description: currentField.desc.join(" ").trim(),
        });
      }
      currentField = {
        name: fieldTypeOnly[1].replace(/\s+/g, ""),
        dataType: fieldTypeOnly[2].toLowerCase(),
        desc: [],
      };
      continue;
    }

    // Continuation line (description that wraps to next line)
    // These are typically indented to the description column
    if (currentField && trimmed.length > 0) {
      // Check if it looks like a continuation (starts with lowercase or is heavily indented)
      const leadingSpaces = line.match(/^(\s*)/)?.[1]?.length ?? 0;
      if (leadingSpaces >= 20 || /^[a-z(]/.test(trimmed)) {
        currentField.desc.push(trimmed);
        continue;
      }

      // Could also be a multi-word field name with type on same line
      // e.g. "Chief Complaint   varchar    description"
      const multiWordMatch = line.match(
        /^\s{0,2}(.+?)\s{2,}(long|varchar|nvarchar|int|boolean|bool|datetime|decimal|string|list)\s{2,}(.+)/i
      );
      if (multiWordMatch) {
        if (currentField) {
          fields.push({
            name: currentField.name,
            dataType: currentField.dataType,
            description: currentField.desc.join(" ").trim(),
          });
        }
        currentField = {
          name: multiWordMatch[1].trim(),
          dataType: multiWordMatch[2].toLowerCase(),
          desc: [multiWordMatch[3].trim()],
        };
        continue;
      }

      // Multi-word field name + type only
      const multiWordTypeOnly = line.match(
        /^\s{0,2}(.+?)\s{2,}(long|varchar|nvarchar|int|boolean|bool|datetime|decimal|string|list)\s*$/i
      );
      if (multiWordTypeOnly) {
        if (currentField) {
          fields.push({
            name: currentField.name,
            dataType: currentField.dataType,
            description: currentField.desc.join(" ").trim(),
          });
        }
        currentField = {
          name: multiWordTypeOnly[1].trim(),
          dataType: multiWordTypeOnly[2].toLowerCase(),
          desc: [],
        };
        continue;
      }

      // Otherwise treat as description continuation if indented enough
      if (leadingSpaces >= 10) {
        currentField.desc.push(trimmed);
      }
    }
  }

  // Save last field
  if (currentField) {
    fields.push({
      name: currentField.name,
      dataType: currentField.dataType,
      description: currentField.desc.join(" ").trim(),
    });
  }

  entities.push({
    sectionNumber: section.num,
    name: `Patient – ${section.name}`,
    fields,
  });
}

// Identify missing sections (in TOC but not in body)
const foundSections = new Set(entities.map((e) => e.sectionNumber));
const missingSections = tocSections.filter((s) => {
  const num = s.match(/^(3\.\d+)/)?.[1];
  return num && !foundSections.has(num);
});

const dataDictionary: DataDictionary = {
  vendor: "TronsHealth LLC",
  product: "TronsHealth",
  documentDate: "2024-09-11",
  exportFormat: "CSV files in ZIP archive",
  entities,
  tocSections,
  missingSections,
};

const outputPath = new URL("data-dictionary.json", import.meta.url).pathname;
await Bun.write(outputPath, JSON.stringify(dataDictionary, null, 2));

// Write stats
const stats = {
  totalTocSections: tocSections.length,
  totalEntitiesFound: entities.length,
  totalFieldsParsed: entities.reduce((sum, e) => sum + e.fields.length, 0),
  entitiesWithFields: entities.filter((e) => e.fields.length > 0).length,
  entitiesWithoutFields: entities.filter((e) => e.fields.length === 0).length,
  missingSectionCount: missingSections.length,
  missingSections,
  entitySummary: entities.map((e) => ({
    section: e.sectionNumber,
    name: e.name,
    fieldCount: e.fields.length,
  })),
};

const statsPath = new URL("extraction-stats.json", import.meta.url).pathname;
await Bun.write(statsPath, JSON.stringify(stats, null, 2));

console.log(
  `Extracted ${entities.length} entities with ${stats.totalFieldsParsed} total fields`
);
console.log(`Missing sections: ${missingSections.length}`);
for (const e of stats.entitySummary) {
  console.log(`  ${e.section} ${e.name}: ${e.fieldCount} fields`);
}
console.log(`Output: ${outputPath}`);
console.log(`Stats: ${statsPath}`);

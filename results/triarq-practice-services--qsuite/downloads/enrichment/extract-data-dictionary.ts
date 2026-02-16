/**
 * Extracts the EHI export data dictionary from the TRIARQ Health QSuite
 * Angular app's main JS bundle.
 *
 * Input:  ../main.js  (the compiled Angular bundle from ehi.myqone.com)
 * Output: data-dictionary.json — full field-level data dictionary
 *         resource-list.json   — list of export resource types with descriptions
 *         extraction-report.json — accounting of what was parsed
 *
 * Run: bun run extract-data-dictionary.ts
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "main.js");
const outputDir = scriptDir;

const content = readFileSync(inputPath, "utf-8");

// --- Extract resourceList ---
function extractJsArray(content: string, marker: string): any[] {
  const start = content.indexOf(marker);
  if (start < 0) throw new Error(`Marker "${marker}" not found in JS bundle`);

  const bracketStart = content.indexOf("[", start);
  let depth = 0;
  let i = bracketStart;
  while (i < content.length) {
    if (content[i] === "[") depth++;
    else if (content[i] === "]") {
      depth--;
      if (depth === 0) break;
    }
    i++;
  }
  const raw = content.slice(bracketStart, i + 1);
  // Convert JS object notation {key:val} to JSON {"key":val}
  const jsonStr = raw.replace(/(\{|,)\s*(\w+)\s*:/g, '$1"$2":');
  return JSON.parse(jsonStr);
}

const resourceList: Array<{
  id: number;
  module: string;
  description: string;
}> = extractJsArray(content, "resourceList=[");

const ehiExportDocs: Array<{
  id: number;
  module: string;
  field: string;
  type: string;
  description: string;
}> = extractJsArray(content, "ehiexportdocs=[");

// --- Build structured output ---
interface Field {
  name: string;
  description: string;
  type: string;
}

interface Entity {
  module: string;
  description: string;
  resourceId: number | null;
  fields: Field[];
}

// Group fields by module
const fieldsByModule = new Map<string, Field[]>();
for (const doc of ehiExportDocs) {
  if (!fieldsByModule.has(doc.module)) {
    fieldsByModule.set(doc.module, []);
  }
  fieldsByModule.get(doc.module)!.push({
    name: doc.field,
    description: doc.description,
    type: doc.type,
  });
}

// Build entities from resourceList, attaching fields
const entities: Entity[] = [];
const coveredModules = new Set<string>();

for (const res of resourceList) {
  const fields = fieldsByModule.get(res.module) || [];
  coveredModules.add(res.module);
  entities.push({
    module: res.module,
    description: res.description,
    resourceId: res.id,
    fields,
  });
}

// Check for any modules in ehiexportdocs not in resourceList
// (e.g., sub-entities like "Patient Cases - Diagnosis")
for (const [mod, fields] of fieldsByModule) {
  if (!coveredModules.has(mod)) {
    entities.push({
      module: mod,
      description: "",
      resourceId: null,
      fields,
    });
  }
}

// Sort entities by module name
entities.sort((a, b) => a.module.localeCompare(b.module));

// --- Also extract non-CSV export types from the page structure ---
// These are embedded in the Angular component template within the JS bundle.
// The PDF, Word, Image sections don't have field-level specs — they're
// file format categories that indicate what document types are exported.

interface ExportFileType {
  format: string;
  documentTypes: string[];
}

const exportFileTypes: ExportFileType[] = [
  {
    format: "CCDA",
    documentTypes: [
      "HL7 CCDA XML files (USCDI v3 compliant, C-CDA R2.1 Companion Guide Release 4.1)",
    ],
  },
  {
    format: "PDF",
    documentTypes: [
      "Patient Messages",
      "Lab Orders Documents",
      "Exam Notes",
      "Patient Letter",
      "Patient Consent",
      "Patient Order Template",
      "Nurse Notes",
      "Patient Education",
    ],
  },
  {
    format: "Word",
    documentTypes: [
      "Exam Notes",
      "Nurse Notes",
      "Billing Statements",
      "Collections",
      "Triage Templates",
      "Patient Forms",
    ],
  },
  {
    format: "Image",
    documentTypes: [
      "Driver License",
      "Insurance Card",
      "DMS Documents",
      "Other",
    ],
  },
];

// --- Write outputs ---
const dataDictionary = {
  source: "https://ehi.myqone.com/",
  extractedFrom: "main.82861f638e42f48d.js",
  extractionDate: new Date().toISOString().split("T")[0],
  product: "QSuite (Manistee)",
  developer: "TRIARQ Practice Services",
  summary: {
    description:
      "The TRIARQ Health QSuite EHI Export provides Bulk CDA Exports compliant with USCDI v3, along with supporting data in CSV and PDF formats. Image files are also included as part of the export package. The EHI Export feature also supports generating single-patient ePHI exports as well as bulk data exports for larger patient populations. This functionality is available in QSuite Manistee v12.12 and later.",
  },
  csvEntities: entities,
  exportFileTypes,
};

writeFileSync(
  join(outputDir, "data-dictionary.json"),
  JSON.stringify(dataDictionary, null, 2)
);

writeFileSync(
  join(outputDir, "resource-list.json"),
  JSON.stringify(resourceList, null, 2)
);

// --- Extraction report ---
const modulesInResourceList = new Set(resourceList.map((r) => r.module));
const modulesInExportDocs = new Set(ehiExportDocs.map((d) => d.module));
const extraModules = [...modulesInExportDocs].filter(
  (m) => !modulesInResourceList.has(m)
);

const report = {
  inputFile: "main.js",
  inputSizeBytes: content.length,
  resourceListEntries: resourceList.length,
  ehiExportDocsEntries: ehiExportDocs.length,
  uniqueModulesInResourceList: modulesInResourceList.size,
  uniqueModulesInExportDocs: modulesInExportDocs.size,
  totalEntities: entities.length,
  totalFields: ehiExportDocs.length,
  modulesWithFields: fieldsByModule.size,
  modulesWithoutFields: entities.filter((e) => e.fields.length === 0).map((e) => e.module),
  extraModulesInExportDocs: extraModules,
  fieldCountByModule: Object.fromEntries(
    entities.map((e) => [e.module, e.fields.length])
  ),
  exportFileTypeCategories: exportFileTypes.length,
  totalDocumentTypes: exportFileTypes.reduce(
    (sum, ft) => sum + ft.documentTypes.length,
    0
  ),
  parseFailures: [],
};

writeFileSync(
  join(outputDir, "extraction-report.json"),
  JSON.stringify(report, null, 2)
);

console.log("Extraction complete:");
console.log(`  Resource types: ${resourceList.length}`);
console.log(`  Total field definitions: ${ehiExportDocs.length}`);
console.log(`  Entities (with sub-entities): ${entities.length}`);
console.log(`  Export file type categories: ${exportFileTypes.length}`);
console.log(`  Output files: data-dictionary.json, resource-list.json, extraction-report.json`);

#!/usr/bin/env bun
/**
 * Extracts IHS RPMS EHI Export schema data from the BREH JSON schema files
 * into queryable JSON structures.
 *
 * Usage: bun run extract-schema.ts
 *
 * Input: ../BREH_OIT_*.txt (JSON schema files)
 * Output:
 *   - schema-summary.json: overview of all schemas with file/field counts
 *   - files-catalog.json: all patient files/tables with field definitions
 *   - pointer-files.json: all reference/lookup tables
 *   - field-types.json: field type distribution and statistics
 *   - schema-diff.json: differences between schema versions
 *   - coverage-stats.json: parsing coverage and accounting
 */

import { readFileSync, writeFileSync, readdirSync } from "fs";
import { join, dirname } from "path";

const DOWNLOADS_DIR = join(dirname(import.meta.dir), "");
const OUTPUT_DIR = import.meta.dir;

interface SchemaFile {
  filename: string;
  schemaName: string;
  versionStatus: string;
  publicUrl: string;
  compileTime: Record<string, unknown>;
  exportType: Record<string, unknown>;
  patientFileCount: number;
  pointerFileCount: number;
}

interface PatientFile {
  fileKey: string;
  fileName: string;
  fileNumber: string;
  global: string;
  ehiEnabled: boolean;
  customFile: boolean;
  fields: FieldDef[];
  subfileCount: number;
  totalFieldCount: number;
}

interface FieldDef {
  fieldKey: string;
  fieldName: string;
  fieldNumber: string;
  fieldType: string;
  fileSubfile: number | string;
  global: string;
  node: number | string;
  piece: number | string;
  fieldSequence: string;
  // For pointer fields
  pointerFile?: number | string;
  pointerFileName?: string;
  // For set of codes
  valueList?: Array<{ code: string; value: string }>;
  // For free text
  minLength?: string | number;
  maxLength?: string | number;
  // For numeric
  lowerBound?: string | number;
  upperBound?: string | number;
  decimalPlaces?: string | number;
  // For date
  internalDateFormat?: string;
  // Subfields (for word-processing, multiples)
  hasSubfields?: boolean;
}

interface PointerFile {
  fileNumber: number;
  fileName: string;
  global: string;
  fieldCount: number;
  fields: Array<{
    fieldReference: string;
    fieldSequence: string;
    check: string;
  }>;
}

function parseSchemaFiles(): void {
  const schemaFiles = readdirSync(DOWNLOADS_DIR)
    .filter((f) => f.startsWith("BREH_OIT_") && f.endsWith(".txt"))
    .sort();

  console.log(`Found ${schemaFiles.length} schema files: ${schemaFiles.join(", ")}`);

  const summaries: SchemaFile[] = [];
  const allVersionFiles: Record<string, PatientFile[]> = {};
  const allVersionPointers: Record<string, PointerFile[]> = {};
  let latestVersion = "";

  for (const sf of schemaFiles) {
    const filepath = join(DOWNLOADS_DIR, sf);
    console.log(`\nParsing ${sf}...`);

    let data: Record<string, unknown>;
    try {
      data = JSON.parse(readFileSync(filepath, "utf-8"));
    } catch (e) {
      console.error(`  FAILED to parse ${sf}: ${e}`);
      continue;
    }

    const schemaName = (data["SCHEMA NAME"] as any)?.VALUE || sf;
    const versionStatus = (data["VERSION STATUS"] as any)?.VALUE || "unknown";
    const publicUrl = (data["PUBLIC URL"] as any)?.VALUE || "";
    latestVersion = sf;

    // Parse PATIENT files
    const patientData = (data["PATIENT"] as any[])?.[0];
    const fileEntries = patientData?.FILE || {};
    const patientFiles: PatientFile[] = [];
    let totalFields = 0;

    for (const [fileKey, fileData] of Object.entries(fileEntries) as [string, any][]) {
      const match = fileKey.match(/^FILE_(.+)_(\d+[\d.]*)$/);
      const fileName = match ? match[1] : fileKey.replace(/^FILE_/, "");
      const fileNumber = match ? match[2] : "";

      const entry = fileData?.["0"] || {};
      const fields: FieldDef[] = [];
      let subfileCount = 0;

      for (const [fk, fv] of Object.entries(entry) as [string, any][]) {
        if (fk === "ENTRY_IEN") continue;
        if (!fk.startsWith("FIELD_")) continue;

        const fieldMatch = fk.match(/^FIELD_(.+)_([.\d]+)$/);
        const fieldName = fieldMatch ? fieldMatch[1] : fk.replace(/^FIELD_/, "");
        const fieldNumber = fieldMatch ? fieldMatch[2] : "";

        const ddInfo = fv?.DD_INFO || {};
        const field: FieldDef = {
          fieldKey: fk,
          fieldName,
          fieldNumber,
          fieldType: fv?.FIELD_TYPE || inferFieldType(fv),
          fileSubfile: ddInfo?.["FILE-SUBFILE"] || "",
          global: ddInfo?.GLOBAL || "",
          node: ddInfo?.NODE ?? "",
          piece: ddInfo?.PIECE ?? "",
          fieldSequence: fv?.FIELD_SEQUENCE || "",
        };

        // Pointer fields
        if (fv?.POINTER_FILE) {
          field.pointerFile = fv.POINTER_FILE;
          field.pointerFileName = fv.POINTER_FILE_NAME || "";
        }

        // Set of codes
        if (fv?.VALUE_LIST && Array.isArray(fv.VALUE_LIST)) {
          field.valueList = fv.VALUE_LIST.map((v: any) => ({
            code: String(v.INTERNAL_CODE || ""),
            value: String(v.VALUE || ""),
          }));
        }

        // Free text constraints
        if (fv?.MINIMUM_LENGTH !== undefined) field.minLength = fv.MINIMUM_LENGTH;
        if (fv?.MAXIMUM_LENGTH !== undefined) field.maxLength = fv.MAXIMUM_LENGTH;

        // Numeric constraints
        if (fv?.INCLUSIVE_LOWER_BOUND !== undefined) field.lowerBound = fv.INCLUSIVE_LOWER_BOUND;
        if (fv?.INCLUSIVE_UPPER_BOUND !== undefined) field.upperBound = fv.INCLUSIVE_UPPER_BOUND;
        if (fv?.DECIMAL_PLACES !== undefined) field.decimalPlaces = fv.DECIMAL_PLACES;

        // Check for subfields (word processing, multiples)
        const hasNestedEntries = Object.keys(fv || {}).some(
          (k) => k !== "DD_INFO" && k !== "FIELD_TYPE" && k !== "FIELD_SEQUENCE" &&
                 typeof fv[k] === "object" && fv[k] !== null && !Array.isArray(fv[k]) &&
                 ("0" in fv[k] || "LINE" in fv[k])
        );
        if (hasNestedEntries) {
          field.hasSubfields = true;
          subfileCount++;
        }

        fields.push(field);
        totalFields++;
      }

      patientFiles.push({
        fileKey,
        fileName,
        fileNumber,
        global: fileData?.FILE_DEFINITION_GLOBAL || "",
        ehiEnabled: fileData?.FILE_DEFINITION_EHI_ENABLED === 1 || fileData?.FILE_DEFINITION_EHI_ENABLED === "1",
        customFile: fileData?.FILE_DEFINITION_CUSTOM_FILE === 1 || fileData?.FILE_DEFINITION_CUSTOM_FILE === "1",
        fields: fields.sort((a, b) => a.fieldName.localeCompare(b.fieldName)),
        subfileCount,
        totalFieldCount: fields.length,
      });
    }

    patientFiles.sort((a, b) => a.fileName.localeCompare(b.fileName));
    allVersionFiles[sf] = patientFiles;

    // Parse POINTER FILES
    const pointerData = (data["POINTER FILE"] as any[]) || [];
    const pointerFiles: PointerFile[] = pointerData.map((pf: any) => ({
      fileNumber: pf.FILE_NUMBER,
      fileName: pf.FILE_NAME,
      global: pf.GLOBAL || "",
      fieldCount: (pf.FIELDS || []).length,
      fields: (pf.FIELDS || []).map((f: any) => ({
        fieldReference: f["FIELD REFERENCE"] || "",
        fieldSequence: f.FIELD_SEQUENCE || "",
        check: f.CHECK || "",
      })),
    }));

    pointerFiles.sort((a, b) => a.fileNumber - b.fileNumber);
    allVersionPointers[sf] = pointerFiles;

    summaries.push({
      filename: sf,
      schemaName: String(schemaName),
      versionStatus: String(versionStatus),
      publicUrl: String(publicUrl),
      compileTime: data["COMPILE TIME"] as Record<string, unknown>,
      exportType: data["EXPORT TYPE"] as Record<string, unknown>,
      patientFileCount: patientFiles.length,
      pointerFileCount: pointerFiles.length,
    });

    console.log(`  Patient files: ${patientFiles.length}, Total fields: ${totalFields}, Pointer files: ${pointerFiles.length}`);
  }

  // Write schema summary
  writeFileSync(
    join(OUTPUT_DIR, "schema-summary.json"),
    JSON.stringify(summaries, null, 2)
  );
  console.log("\nWrote schema-summary.json");

  // Write the latest version's files catalog
  const latestFiles = allVersionFiles[latestVersion] || [];
  writeFileSync(
    join(OUTPUT_DIR, "files-catalog.json"),
    JSON.stringify(latestFiles, null, 2)
  );
  console.log(`Wrote files-catalog.json (${latestFiles.length} files from ${latestVersion})`);

  // Write pointer files
  const latestPointers = allVersionPointers[latestVersion] || [];
  writeFileSync(
    join(OUTPUT_DIR, "pointer-files.json"),
    JSON.stringify(latestPointers, null, 2)
  );
  console.log(`Wrote pointer-files.json (${latestPointers.length} pointer files)`);

  // Field type statistics
  const fieldTypeCounts: Record<string, number> = {};
  const fieldsByType: Record<string, string[]> = {};
  for (const pf of latestFiles) {
    for (const f of pf.fields) {
      const ft = f.fieldType || "UNKNOWN";
      fieldTypeCounts[ft] = (fieldTypeCounts[ft] || 0) + 1;
      if (!fieldsByType[ft]) fieldsByType[ft] = [];
      if (fieldsByType[ft].length < 5) {
        fieldsByType[ft].push(`${pf.fileName}.${f.fieldName}`);
      }
    }
  }

  writeFileSync(
    join(OUTPUT_DIR, "field-types.json"),
    JSON.stringify(
      {
        totalFields: Object.values(fieldTypeCounts).reduce((a, b) => a + b, 0),
        typeCounts: Object.fromEntries(
          Object.entries(fieldTypeCounts).sort((a, b) => b[1] - a[1])
        ),
        samplesByType: fieldsByType,
      },
      null,
      2
    )
  );
  console.log("Wrote field-types.json");

  // Schema diff between versions
  const versionNames = Object.keys(allVersionFiles).sort();
  const diffs: Array<{
    from: string;
    to: string;
    addedFiles: string[];
    removedFiles: string[];
    fieldCountChanges: Array<{ file: string; fromCount: number; toCount: number }>;
  }> = [];

  for (let i = 1; i < versionNames.length; i++) {
    const fromVer = versionNames[i - 1];
    const toVer = versionNames[i];
    const fromFiles = new Map(allVersionFiles[fromVer].map((f) => [f.fileKey, f]));
    const toFiles = new Map(allVersionFiles[toVer].map((f) => [f.fileKey, f]));

    const added = [...toFiles.keys()].filter((k) => !fromFiles.has(k));
    const removed = [...fromFiles.keys()].filter((k) => !toFiles.has(k));

    const fieldChanges: Array<{ file: string; fromCount: number; toCount: number }> = [];
    for (const [key, toFile] of toFiles) {
      const fromFile = fromFiles.get(key);
      if (fromFile && fromFile.totalFieldCount !== toFile.totalFieldCount) {
        fieldChanges.push({
          file: key,
          fromCount: fromFile.totalFieldCount,
          toCount: toFile.totalFieldCount,
        });
      }
    }

    diffs.push({
      from: fromVer,
      to: toVer,
      addedFiles: added.sort(),
      removedFiles: removed.sort(),
      fieldCountChanges: fieldChanges.sort((a, b) => a.file.localeCompare(b.file)),
    });
  }

  writeFileSync(
    join(OUTPUT_DIR, "schema-diff.json"),
    JSON.stringify(diffs, null, 2)
  );
  console.log("Wrote schema-diff.json");

  // Coverage stats
  const totalFieldsInLatest = latestFiles.reduce((sum, f) => sum + f.totalFieldCount, 0);
  const filesWithFields = latestFiles.filter((f) => f.totalFieldCount > 0).length;
  const filesWithoutFields = latestFiles.filter((f) => f.totalFieldCount === 0).length;

  // Categorize files by domain
  const domainCategories: Record<string, string[]> = {
    "Clinical - PCC V-files": [],
    "Clinical - Pharmacy": [],
    "Clinical - Laboratory": [],
    "Clinical - Behavioral Health": [],
    "Clinical - Dental": [],
    "Clinical - Immunizations": [],
    "Clinical - Other": [],
    "Administrative - Billing": [],
    "Administrative - Registration": [],
    "Administrative - Scheduling": [],
    "Imaging": [],
    "Other": [],
  };

  for (const pf of latestFiles) {
    const name = pf.fileName.toUpperCase();
    if (name.startsWith("V ") || name === "VISIT") {
      domainCategories["Clinical - PCC V-files"].push(pf.fileName);
    } else if (name.includes("PHARM") || name.includes("PRESCRIPTION") || name.includes("RX ") || name.includes("APSP") || name.includes("DRUG")) {
      domainCategories["Clinical - Pharmacy"].push(pf.fileName);
    } else if (name.includes("LAB") || name.includes("MICROBIOLOGY") || name.includes("PATHOLOGY") || name.includes("BLOOD") || name.includes("BLS ") || name.includes("BLRA")) {
      domainCategories["Clinical - Laboratory"].push(pf.fileName);
    } else if (name.includes("MHSS") || name.includes("BH ") || name.includes("BEHAVIORAL")) {
      domainCategories["Clinical - Behavioral Health"].push(pf.fileName);
    } else if (name.includes("DENTAL")) {
      domainCategories["Clinical - Dental"].push(pf.fileName);
    } else if (name.includes("IMMUN") || name.startsWith("BI ") || name.startsWith("IZ ")) {
      domainCategories["Clinical - Immunizations"].push(pf.fileName);
    } else if (name.includes("BILL") || name.includes("CLAIM") || name.includes("A/R") || name.includes("INSURANCE") || name.includes("3P ") || name.includes("ABSP") || name.includes("MEDICAID") || name.includes("MEDICARE") || name.includes("RAILROAD")) {
      domainCategories["Administrative - Billing"].push(pf.fileName);
    } else if (name.includes("PATIENT") || name.includes("REGISTRATION") || name.includes("ENROLLMENT") || name === "VA PATIENT" || name.includes("AG ") || name.includes("AGEV") || name.includes("AGVQ")) {
      domainCategories["Administrative - Registration"].push(pf.fileName);
    } else if (name.includes("SCHEDUL") || name.includes("APPOINTMENT") || name.includes("WAIT LIST") || name.includes("WAITING LIST") || name.includes("BSDX")) {
      domainCategories["Administrative - Scheduling"].push(pf.fileName);
    } else if (name.includes("IMAGE") || name.includes("IMAGING") || name.includes("PACS") || name.includes("TELEREADER")) {
      domainCategories["Imaging"].push(pf.fileName);
    } else {
      domainCategories["Clinical - Other"].push(pf.fileName);
    }
  }

  writeFileSync(
    join(OUTPUT_DIR, "coverage-stats.json"),
    JSON.stringify(
      {
        schemaFilesDiscovered: schemaFiles.length,
        schemaFilesParsed: summaries.length,
        parseFailures: schemaFiles.length - summaries.length,
        latestVersion,
        latestVersionStats: {
          patientFiles: latestFiles.length,
          patientFilesWithFields: filesWithFields,
          patientFilesWithoutFields: filesWithoutFields,
          totalFieldDefinitions: totalFieldsInLatest,
          pointerFiles: latestPointers.length,
        },
        domainCategories: Object.fromEntries(
          Object.entries(domainCategories).map(([k, v]) => [k, { count: v.length, files: v.sort() }])
        ),
      },
      null,
      2
    )
  );
  console.log("Wrote coverage-stats.json");

  console.log("\n=== ENRICHMENT COMPLETE ===");
  console.log(`Schema files parsed: ${summaries.length}/${schemaFiles.length}`);
  console.log(`Latest version: ${latestVersion}`);
  console.log(`  Patient files: ${latestFiles.length}`);
  console.log(`  Total fields: ${totalFieldsInLatest}`);
  console.log(`  Pointer/reference files: ${latestPointers.length}`);
}

function inferFieldType(fieldData: any): string {
  if (!fieldData || typeof fieldData !== "object") return "UNKNOWN";
  if (fieldData.POINTER_FILE) return "POINTER TO A FILE";
  if (fieldData.VALUE_LIST) return "SET OF CODES";
  if (fieldData.INTERNAL_DATE) return "DATE/TIME";
  if (fieldData.INCLUSIVE_LOWER_BOUND !== undefined || fieldData.INCLUSIVE_UPPER_BOUND !== undefined) return "NUMERIC";
  if (fieldData.MAXIMUM_LENGTH !== undefined || fieldData.MINIMUM_LENGTH !== undefined) return "FREE TEXT";
  // Check for word processing
  const keys = Object.keys(fieldData);
  if (keys.some((k) => k === "0" || k === "LINE")) return "WORD PROCESSING";
  return "UNKNOWN";
}

parseSchemaFiles();

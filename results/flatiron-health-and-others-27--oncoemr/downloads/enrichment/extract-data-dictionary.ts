#!/usr/bin/env bun
/**
 * Extracts structured data from the Flatiron Health EHI Data Dictionary PDF.
 *
 * The PDF is a table with columns: TableName, ColumnName, Type, Nullable, Description.
 * Uses `pdftotext -layout` for extraction and parses the fixed-width layout.
 *
 * Usage: bun run extract-data-dictionary.ts
 * Input:  ../ehi-data-dictionary.pdf
 * Output: data-dictionary.json, coverage-summary.json
 */

import { $ } from "bun";

interface Column {
  table_name: string;
  column_name: string;
  data_type: string;
  nullable: boolean | null;
  description: string;
}

interface Table {
  name: string;
  description: string;
  columns: Column[];
  partition_namespace_present: boolean;
}

interface DataDictionary {
  export_format: {
    single_patient: string;
    population: string;
    additional_files: string;
    access_method: string;
  };
  last_modified: string;
  tables: Table[];
  total_tables: number;
  total_columns: number;
}

async function main() {
  const pdfPath = new URL("../ehi-data-dictionary.pdf", import.meta.url).pathname;

  // Extract text with layout preservation
  const result = await $`pdftotext -layout ${pdfPath} -`.text();
  const lines = result.split("\n");

  // Parse header information (first page)
  const exportFormat = {
    single_patient: "CSV",
    population: "Parquet",
    additional_files: "XML, JPEG, PNG, TIFF, PDF (encounter summaries, faxes, imaging results, scanned clinical documents)",
    access_method: "Single patient: self-service via OncoEMR UI; Population: requested via OncoEMR UI, downloaded via UI or SFTP",
  };

  let lastModified = "";
  for (const line of lines.slice(0, 15)) {
    const m = line.match(/Last Modified:\s*(.+)/);
    if (m) {
      lastModified = m[1].trim();
      break;
    }
  }

  // Parse table data
  // The layout has columns roughly at these positions:
  // TableName (col 0), ColumnName (col ~18-26), Type (col ~40-50), Nullable (col ~55-60), Description (col ~65+)
  // But positions vary. We'll use a heuristic approach.

  const tables = new Map<string, Table>();
  let currentTable = "";
  let currentColumn: Column | null = null;

  // Known data types for matching
  const dataTypes = new Set([
    "datetime", "datetime2", "integer", "int", "binary", "varchar", "nvarchar",
    "bit", "float", "text", "decimal", "bigint", "boolean", "uniqueidentifier",
    "xml", "varbinary", "money", "smallint", "tinyint", "real", "numeric",
    "ntext", "image", "char", "nchar", "date", "time", "timestamp",
    "smallint", "datetimeoffset",
  ]);

  function isDataType(s: string): boolean {
    const clean = s.toLowerCase().replace(/\(.*\)/, "").trim();
    return dataTypes.has(clean);
  }

  // Skip header lines until we find "TableName"
  let startIdx = 0;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes("TableName") && lines[i].includes("ColumnName")) {
      startIdx = i + 1;
      break;
    }
  }

  for (let i = startIdx; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim()) continue;

    // Check for repeated header line
    if (line.includes("TableName") && line.includes("ColumnName") && line.includes("Type")) {
      continue;
    }

    // Try to parse as a data row
    // Pattern: TableName  ColumnName  Type  Nullable  Description
    // Or continuation line (starts with spaces)

    const trimmed = line.trimStart();
    const leadingSpaces = line.length - trimmed.length;

    if (leadingSpaces > 10) {
      // Continuation of previous description
      if (currentColumn) {
        currentColumn.description += " " + trimmed.trim();
      }
      continue;
    }

    // Try to parse as a new column entry
    // Split by multiple spaces (2+)
    const parts = line.trim().split(/\s{2,}/);

    if (parts.length >= 3) {
      const tableName = parts[0].trim();
      const columnName = parts[1].trim();

      // Check if this is a "Table Description" entry
      if (columnName === "Table Description") {
        const desc = parts.slice(2).join(" ").trim();
        const normalizedName = tableName.replace(/^([a-z])/, (_, c) => c.toUpperCase());
        const table = tables.get(tableName) || tables.get(normalizedName);
        if (table) {
          table.description = desc;
        } else {
          // Create table entry if not exists
          const t: Table = {
            name: tableName,
            description: desc,
            columns: [],
            partition_namespace_present: false,
          };
          tables.set(tableName, t);
        }
        currentColumn = null;
        continue;
      }

      // Check if the third part looks like a data type
      let typeStr = parts[2]?.trim() || "";
      // Handle cases where type and nullable are merged or in different positions
      let nullable: boolean | null = null;
      let description = "";

      if (isDataType(typeStr)) {
        // Standard row
        if (parts.length >= 4) {
          const nullStr = parts[3]?.trim().toUpperCase();
          if (nullStr === "TRUE") nullable = true;
          else if (nullStr === "FALSE") nullable = false;
        }
        description = parts.slice(4).join(" ").trim();
      } else if (parts.length >= 4 && isDataType(parts[3]?.trim())) {
        // Sometimes type is in position 3 (column name had space issue)
        typeStr = parts[3].trim();
        if (parts.length >= 5) {
          const nullStr = parts[4]?.trim().toUpperCase();
          if (nullStr === "TRUE") nullable = true;
          else if (nullStr === "FALSE") nullable = false;
        }
        description = parts.slice(5).join(" ").trim();
      } else {
        // Can't parse as data row - might be continuation
        if (currentColumn) {
          currentColumn.description += " " + line.trim();
        }
        continue;
      }

      // Normalize table name - lowercase versions with PARTITION_NAMESPACE
      // are the same table, just the partition key
      const isPartitionRow = columnName === "PARTITION_NAMESPACE";
      const normalizedTableName = tableName.charAt(0).toUpperCase() === tableName.charAt(0)
        ? tableName
        : tableName.replace(/(^|_)([a-z])/g, (_, sep, c) =>
            sep + c.toUpperCase()
          );

      // Get or create table
      let table = tables.get(normalizedTableName);
      if (!table) {
        // Try exact match first
        table = tables.get(tableName);
      }
      if (!table) {
        table = {
          name: normalizedTableName,
          description: "",
          columns: [],
          partition_namespace_present: false,
        };
        tables.set(normalizedTableName, table);
      }

      if (isPartitionRow) {
        table.partition_namespace_present = true;
      }

      currentColumn = {
        table_name: normalizedTableName,
        column_name: columnName,
        data_type: typeStr,
        nullable,
        description,
      };
      table.columns.push(currentColumn);
      currentTable = normalizedTableName;
    } else if (currentColumn) {
      // Continuation line
      currentColumn.description += " " + line.trim();
    }
  }

  // Clean up descriptions
  for (const table of tables.values()) {
    table.description = table.description.replace(/\s+/g, " ").trim();
    for (const col of table.columns) {
      col.description = col.description.replace(/\s+/g, " ").trim();
    }
  }

  // Deduplicate: merge lowercase table entries into their PascalCase counterparts
  const finalTables: Table[] = [];
  const seen = new Set<string>();

  for (const [key, table] of tables.entries()) {
    const normalized = table.name;
    if (seen.has(normalized.toLowerCase())) continue;
    seen.add(normalized.toLowerCase());

    // Find and merge any duplicate with different casing
    for (const [otherKey, otherTable] of tables.entries()) {
      if (otherKey !== key && otherKey.toLowerCase() === key.toLowerCase()) {
        // Merge columns
        for (const col of otherTable.columns) {
          if (!table.columns.some(c => c.column_name === col.column_name)) {
            col.table_name = normalized;
            table.columns.push(col);
          }
        }
        if (otherTable.partition_namespace_present) {
          table.partition_namespace_present = true;
        }
        if (otherTable.description && !table.description) {
          table.description = otherTable.description;
        }
      }
    }

    finalTables.push(table);
  }

  // Sort tables by name
  finalTables.sort((a, b) => a.name.localeCompare(b.name));

  const totalColumns = finalTables.reduce((sum, t) => sum + t.columns.length, 0);

  const dataDictionary: DataDictionary = {
    export_format: exportFormat,
    last_modified: lastModified,
    tables: finalTables,
    total_tables: finalTables.length,
    total_columns: totalColumns,
  };

  // Write data dictionary JSON
  const outPath = new URL("data-dictionary.json", import.meta.url).pathname;
  await Bun.write(outPath, JSON.stringify(dataDictionary, null, 2));
  console.log(`Wrote ${outPath}`);
  console.log(`  Tables: ${finalTables.length}`);
  console.log(`  Columns: ${totalColumns}`);

  // Write coverage summary
  const categorized = categorizeTables(finalTables);
  const summaryPath = new URL("coverage-summary.json", import.meta.url).pathname;
  await Bun.write(summaryPath, JSON.stringify(categorized, null, 2));
  console.log(`Wrote ${summaryPath}`);

  // Print parse quality stats
  const noDesc = finalTables.flatMap(t => t.columns).filter(c => !c.description).length;
  const noType = finalTables.flatMap(t => t.columns).filter(c => !c.data_type).length;
  const noNullable = finalTables.flatMap(t => t.columns).filter(c => c.nullable === null).length;
  console.log(`\nParse quality:`);
  console.log(`  Columns missing description: ${noDesc}`);
  console.log(`  Columns missing type: ${noType}`);
  console.log(`  Columns missing nullable: ${noNullable}`);
}

function categorizeTables(tables: Table[]) {
  const categories: Record<string, string[]> = {
    demographics: [],
    clinical_notes_documents: [],
    diagnoses_conditions: [],
    medications_orders: [],
    labs_results: [],
    allergies: [],
    immunizations: [],
    vital_signs: [],
    family_history: [],
    care_plans_goals: [],
    billing_financial: [],
    insurance: [],
    appointments_scheduling: [],
    imaging: [],
    messaging_tasks: [],
    clinical_trials_pathways: [],
    encounters: [],
    staging_oncology: [],
    devices: [],
    questionnaires: [],
    care_team: [],
    prescriptions: [],
    other: [],
  };

  for (const table of tables) {
    const name = table.name.toLowerCase();
    const desc = table.description.toLowerCase();

    if (name.includes("demographics") || name.includes("address") || name.includes("phone") || name.includes("email") || name.includes("contact") || name.includes("patientother") || name.includes("sexparameter") || name.includes("patient_location")) {
      categories.demographics.push(table.name);
    } else if (name.includes("document") || name.includes("visit_note") || name.includes("data_history") || name.includes("datanew")) {
      categories.clinical_notes_documents.push(table.name);
    } else if (name.includes("diagnosis") || name.includes("condition")) {
      categories.diagnoses_conditions.push(table.name);
    } else if (name.includes("medication") || name.includes("order") || name.includes("dose") || name.includes("drug_rule") || name.includes("inventory_dispense")) {
      categories.medications_orders.push(table.name);
    } else if (name.includes("lab_result") || name.includes("test_history") || name.includes("test_aoe")) {
      categories.labs_results.push(table.name);
    } else if (name.includes("allergy")) {
      categories.allergies.push(table.name);
    } else if (name.includes("immunization")) {
      categories.immunizations.push(table.name);
    } else if (name.includes("vital_sign")) {
      categories.vital_signs.push(table.name);
    } else if (name.includes("familyhist")) {
      categories.family_history.push(table.name);
    } else if (name.includes("care_plan") || name.includes("patientgoals")) {
      categories.care_plans_goals.push(table.name);
    } else if (name.includes("billing") || name.includes("charge") || name.includes("claim") || name.includes("transaction") || name.includes("invoice") || name.includes("insurercredits")) {
      categories.billing_financial.push(table.name);
    } else if (name.includes("insurance") || name.includes("eligibility") || name.includes("guarantor") || name.includes("pbm") || name.includes("apm_") || name.includes("cdg_enrollment") || name.includes("patient_cdgenrollment")) {
      categories.insurance.push(table.name);
    } else if (name.includes("appointment")) {
      categories.appointments_scheduling.push(table.name);
    } else if (name.includes("image")) {
      categories.imaging.push(table.name);
    } else if (name.includes("message") || name.includes("msgstosend") || name.includes("task") || name.includes("reminder") || name.includes("linkclick")) {
      categories.messaging_tasks.push(table.name);
    } else if (name.includes("pathway") || name.includes("treatment") || name.includes("regimen")) {
      categories.clinical_trials_pathways.push(table.name);
    } else if (name.includes("encounter") || name.includes("externalencounter") || name.includes("internaltoexternal")) {
      categories.encounters.push(table.name);
    } else if (name.includes("staging")) {
      categories.staging_oncology.push(table.name);
    } else if (name.includes("implantable") || name.includes("device")) {
      categories.devices.push(table.name);
    } else if (name.includes("questionnaire")) {
      categories.questionnaires.push(table.name);
    } else if (name.includes("careteam")) {
      categories.care_team.push(table.name);
    } else if (name.includes("surescripts") || name.includes("preferred_pharmacy")) {
      categories.prescriptions.push(table.name);
    } else {
      categories.other.push(table.name);
    }
  }

  // Remove empty categories
  for (const key of Object.keys(categories)) {
    if (categories[key].length === 0) delete categories[key];
  }

  return {
    data_domain_categories: categories,
    summary: {
      total_tables: tables.length,
      total_columns: tables.reduce((s, t) => s + t.columns.length, 0),
      categories_with_tables: Object.keys(categories).length,
      tables_with_descriptions: tables.filter(t => t.description).length,
      tables_without_descriptions: tables.filter(t => !t.description).length,
    },
  };
}

main().catch(console.error);

#!/usr/bin/env bun
/**
 * Extracts the myEvolv All EHI Export Data Dictionary Crosswalk XLSX
 * into queryable JSON files.
 *
 * Usage: bun run extract-data-dictionary.ts
 *
 * Input: ../(2) myEvolv All EHI Export Data Dictionary Crosswalk.xlsx
 * Outputs:
 *   - events.json: All event definitions with category, table, and form info
 *   - events-columns.json: All event columns with field-level detail
 *   - non-events.json: All non-event form definitions
 *   - non-events-columns.json: All non-event form columns with field-level detail
 *   - summary.json: Coverage/accounting output with counts and categories
 */

import XLSX from "xlsx";
import { writeFileSync } from "fs";
import { join, dirname } from "path";

const INPUT_FILE = join(
  dirname(import.meta.path),
  "..",
  "(2) myEvolv All EHI Export Data Dictionary Crosswalk.xlsx"
);
const OUTPUT_DIR = dirname(import.meta.path);

console.log(`Reading: ${INPUT_FILE}`);
const wb = XLSX.readFile(INPUT_FILE);

console.log(`Sheets found: ${wb.SheetNames.join(", ")}`);

// --- Events ---
const eventsData = XLSX.utils.sheet_to_json(wb.Sheets["Events"]);
console.log(`Events: ${eventsData.length} rows`);
writeFileSync(
  join(OUTPUT_DIR, "events.json"),
  JSON.stringify(eventsData, null, 2)
);

// --- Events + Columns ---
const eventsColumnsData = XLSX.utils.sheet_to_json(
  wb.Sheets["Events + Columns"]
);
console.log(`Events + Columns: ${eventsColumnsData.length} rows`);
writeFileSync(
  join(OUTPUT_DIR, "events-columns.json"),
  JSON.stringify(eventsColumnsData, null, 2)
);

// --- Non-Events ---
const nonEventsData = XLSX.utils.sheet_to_json(wb.Sheets["Non-Events"]);
console.log(`Non-Events: ${nonEventsData.length} rows`);
writeFileSync(
  join(OUTPUT_DIR, "non-events.json"),
  JSON.stringify(nonEventsData, null, 2)
);

// --- Non-Events + Columns ---
const nonEventsColumnsData = XLSX.utils.sheet_to_json(
  wb.Sheets["Non-Events + Columns"]
);
console.log(`Non-Events + Columns: ${nonEventsColumnsData.length} rows`);
writeFileSync(
  join(OUTPUT_DIR, "non-events-columns.json"),
  JSON.stringify(nonEventsColumnsData, null, 2)
);

// --- Summary ---
const eventCategories = [
  ...new Set(eventsData.map((r: any) => r.category_name)),
].sort();
const eventTables = [
  ...new Set(eventsData.map((r: any) => r.table_name)),
].sort();
const nonEventFormFamilies = [
  ...new Set(nonEventsData.map((r: any) => r.form_family_name)),
].sort();

// Count unique type codes in events+columns
const eventTypeCodes = [
  ...new Set(
    eventsColumnsData.map((r: any) => (r.typeCode || "").toString().trim())
  ),
]
  .filter(Boolean)
  .sort();

const nonEventTypeCodes = [
  ...new Set(
    nonEventsColumnsData
      .map((r: any) => (r.typeCode || "").toString().trim())
      .filter(Boolean)
  ),
].sort();

const summary = {
  extraction_date: new Date().toISOString().split("T")[0],
  input_file:
    "(2) myEvolv All EHI Export Data Dictionary Crosswalk.xlsx",
  sheets_parsed: wb.SheetNames.length,
  sheets: wb.SheetNames,
  counts: {
    events: eventsData.length,
    events_columns: eventsColumnsData.length,
    non_events: nonEventsData.length,
    non_events_columns: nonEventsColumnsData.length,
  },
  event_categories: {
    count: eventCategories.length,
    names: eventCategories,
  },
  event_tables: {
    count: eventTables.length,
    names: eventTables,
  },
  non_event_form_families: {
    count: nonEventFormFamilies.length,
    names: nonEventFormFamilies,
  },
  type_codes_in_events: eventTypeCodes,
  type_codes_in_non_events: nonEventTypeCodes,
  parse_failures: [],
};

writeFileSync(
  join(OUTPUT_DIR, "summary.json"),
  JSON.stringify(summary, null, 2)
);

console.log("\nExtraction complete.");
console.log(`  events.json: ${eventsData.length} records`);
console.log(`  events-columns.json: ${eventsColumnsData.length} records`);
console.log(`  non-events.json: ${nonEventsData.length} records`);
console.log(
  `  non-events-columns.json: ${nonEventsColumnsData.length} records`
);
console.log(`  summary.json: coverage/accounting output`);
console.log(`  Event categories: ${eventCategories.length}`);
console.log(`  Event tables: ${eventTables.length}`);
console.log(`  Non-event form families: ${nonEventFormFamilies.length}`);

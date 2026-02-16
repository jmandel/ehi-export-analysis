#!/usr/bin/env bun
/**
 * Parses the myEvolv EHI Export Data Dictionary Crosswalk XLSX
 * and produces entity-inventory-full.json and entity-inventory-summary.json.
 *
 * Reads the raw XLSX from downloads/ (not enrichment/).
 */

import XLSX from "xlsx";
import { writeFileSync } from "fs";
import { join, dirname } from "path";

const BASE = dirname(import.meta.path);
const INPUT_FILE = join(
  BASE,
  "..",
  "downloads",
  "(2) myEvolv All EHI Export Data Dictionary Crosswalk.xlsx"
);

console.log(`Reading: ${INPUT_FILE}`);
const wb = XLSX.readFile(INPUT_FILE);
console.log(`Sheets: ${wb.SheetNames.join(", ")}`);

// Parse all sheets
const events: any[] = XLSX.utils.sheet_to_json(wb.Sheets["Events"]);
const eventsCols: any[] = XLSX.utils.sheet_to_json(wb.Sheets["Events + Columns"]);
const nonEvents: any[] = XLSX.utils.sheet_to_json(wb.Sheets["Non-Events"]);
const nonEventsCols: any[] = XLSX.utils.sheet_to_json(wb.Sheets["Non-Events + Columns"]);

console.log(`Events: ${events.length}, Events+Cols: ${eventsCols.length}`);
console.log(`Non-Events: ${nonEvents.length}, Non-Events+Cols: ${nonEventsCols.length}`);

// Helper to clean type codes (they have trailing spaces)
function cleanStr(s: any): string | null {
  if (s === undefined || s === null || s === "NULL") return null;
  return String(s).trim();
}

// --- Build entity inventory ---
// Entity = a unique form (identified by form_code)
// For events, we group by form_code and include category info
// For non-events, we group by form_code and include form_family info

interface Field {
  name: string | null;
  caption: string | null;
  type_code: string | null;
  level: "form" | "subform" | "assessment";
  subform_name?: string | null;
  subform_code?: string | null;
  assessment_name?: string | null;
  assessment_code?: string | null;
  assessment_question_id?: string | null;
}

interface Entity {
  entity_type: "event" | "non-event";
  form_name: string;
  form_code: string;
  table_name: string | null;
  category_name: string | null;
  category_code: string | null;
  form_family_name: string | null;
  form_family_id: string | null;
  event_count: number; // how many event definitions use this form
  event_names: string[];
  fields: Field[];
}

// --- Events ---
// Group event definitions by form_code
const eventsByFormCode = new Map<string, any[]>();
for (const e of events) {
  const fc = cleanStr(e.form_code) || "UNKNOWN";
  if (!eventsByFormCode.has(fc)) eventsByFormCode.set(fc, []);
  eventsByFormCode.get(fc)!.push(e);
}

// Group event columns by form_code
const eventsColsByFormCode = new Map<string, any[]>();
for (const c of eventsCols) {
  const fc = cleanStr(c.form_code) || "UNKNOWN";
  if (!eventsColsByFormCode.has(fc)) eventsColsByFormCode.set(fc, []);
  eventsColsByFormCode.get(fc)!.push(c);
}

// Build event entities
const entities: Entity[] = [];

for (const [formCode, defs] of eventsByFormCode) {
  const firstDef = defs[0];
  const cols = eventsColsByFormCode.get(formCode) || [];
  
  const fields: Field[] = [];
  for (const c of cols) {
    const jsonProp = cleanStr(c.jsonPropertyName);
    const caption = cleanStr(c.formFieldCaption);
    const typeCode = cleanStr(c.typeCode);
    const subName = cleanStr(c.subformName);
    const subCode = cleanStr(c.subFormCode);
    const subProp = cleanStr(c.subFormJsonPropertyName);
    const subCaption = cleanStr(c.subFormFieldCaption);
    const subTypeCode = cleanStr(c.typeCode_1);
    const assessName = cleanStr(c.assessmentName);
    const assessCode = cleanStr(c.assessmentCode);
    const assessQId = cleanStr(c.assessmentQuestionID);
    const assessQCaption = cleanStr(c.assessmentQuestionCaption);

    // Determine field level
    if (assessName && assessQCaption) {
      fields.push({
        name: assessQId,
        caption: assessQCaption,
        type_code: subTypeCode || typeCode,
        level: "assessment",
        assessment_name: assessName,
        assessment_code: assessCode,
        assessment_question_id: assessQId,
        subform_name: subName,
        subform_code: subCode,
      });
    } else if (subName && subProp) {
      fields.push({
        name: subProp,
        caption: subCaption,
        type_code: subTypeCode || typeCode,
        level: "subform",
        subform_name: subName,
        subform_code: subCode,
      });
    } else if (jsonProp) {
      fields.push({
        name: jsonProp,
        caption: caption,
        type_code: typeCode,
        level: "form",
      });
    } else if (subName && !subProp && subCaption) {
      // Subform reference without a property name
      fields.push({
        name: null,
        caption: subCaption,
        type_code: subTypeCode || typeCode,
        level: "subform",
        subform_name: subName,
        subform_code: subCode,
      });
    }
    // else: rows that are SF/TESTS pointers without detail - skip
  }

  entities.push({
    entity_type: "event",
    form_name: firstDef.form_name,
    form_code: formCode,
    table_name: firstDef.table_name,
    category_name: firstDef.category_name,
    category_code: cleanStr(firstDef.category_code),
    form_family_name: null,
    form_family_id: null,
    event_count: defs.length,
    event_names: defs.map((d: any) => d.event_name),
    fields,
  });
}

// --- Non-Events ---
// Group non-event columns by form_code
const nonEventsColsByFormCode = new Map<string, any[]>();
for (const c of nonEventsCols) {
  const fc = cleanStr(c.form_code) || "UNKNOWN";
  if (!nonEventsColsByFormCode.has(fc)) nonEventsColsByFormCode.set(fc, []);
  nonEventsColsByFormCode.get(fc)!.push(c);
}

// Build non-event entities
const nonEventsByFormCode = new Map<string, any>();
for (const ne of nonEvents) {
  const fc = cleanStr(ne.form_code) || "UNKNOWN";
  if (!nonEventsByFormCode.has(fc)) nonEventsByFormCode.set(fc, ne);
}

// Some non-event form codes only appear in columns, not in the Non-Events sheet
const allNonEventFormCodes = new Set([
  ...nonEventsByFormCode.keys(),
  ...nonEventsColsByFormCode.keys(),
]);

for (const formCode of allNonEventFormCodes) {
  const def = nonEventsByFormCode.get(formCode);
  const cols = nonEventsColsByFormCode.get(formCode) || [];

  const fields: Field[] = [];
  for (const c of cols) {
    const jsonProp = cleanStr(c.jsonPropertyName);
    const caption = cleanStr(c.formFieldCaption);
    const typeCode = cleanStr(c.typeCode);
    const subName = cleanStr(c.subformName);
    const subCode = cleanStr(c.subFormCode);
    const subProp = cleanStr(c.subFormJsonPropertyName);
    const subCaption = cleanStr(c.subFormFieldCaption);
    const subTypeCode = cleanStr(c.typeCode_1);
    const assessName = cleanStr(c.assessmentName);
    const assessCode = cleanStr(c.assessmentCode);
    const assessQId = cleanStr(c.assessmentQuestionID);
    const assessQCaption = cleanStr(c.assessmentQuestionCaption);

    if (assessName && assessQCaption) {
      fields.push({
        name: assessQId,
        caption: assessQCaption,
        type_code: subTypeCode || typeCode,
        level: "assessment",
        assessment_name: assessName,
        assessment_code: assessCode,
        assessment_question_id: assessQId,
        subform_name: subName,
        subform_code: subCode,
      });
    } else if (subName && subProp) {
      fields.push({
        name: subProp,
        caption: subCaption,
        type_code: subTypeCode || typeCode,
        level: "subform",
        subform_name: subName,
        subform_code: subCode,
      });
    } else if (jsonProp) {
      fields.push({
        name: jsonProp,
        caption: caption,
        type_code: typeCode,
        level: "form",
      });
    } else if (subName && !subProp && subCaption) {
      fields.push({
        name: null,
        caption: subCaption,
        type_code: subTypeCode || typeCode,
        level: "subform",
        subform_name: subName,
        subform_code: subCode,
      });
    }
  }

  entities.push({
    entity_type: "non-event",
    form_name: def?.form_name || formCode,
    form_code: formCode,
    table_name: "people",
    category_name: null,
    category_code: null,
    form_family_name: def?.form_family_name || null,
    form_family_id: def?.form_family_id || null,
    event_count: 0,
    event_names: [],
    fields,
  });
}

// Write full inventory
writeFileSync(
  join(BASE, "entity-inventory-full.json"),
  JSON.stringify(entities, null, 2)
);
console.log(`\nWrote entity-inventory-full.json: ${entities.length} entities`);

// --- Summary ---
const totalFields = entities.reduce((sum, e) => sum + e.fields.length, 0);
const fieldsWithCaption = entities.reduce(
  (sum, e) => sum + e.fields.filter((f) => f.caption).length,
  0
);
const fieldsWithName = entities.reduce(
  (sum, e) => sum + e.fields.filter((f) => f.name).length,
  0
);
const fieldsWithType = entities.reduce(
  (sum, e) => sum + e.fields.filter((f) => f.type_code).length,
  0
);

// Category breakdown for events
const categoryStats = new Map<string, { entities: number; fields: number }>();
for (const e of entities) {
  if (e.entity_type === "event") {
    const cat = e.category_name || "Uncategorized";
    if (!categoryStats.has(cat))
      categoryStats.set(cat, { entities: 0, fields: 0 });
    const s = categoryStats.get(cat)!;
    s.entities++;
    s.fields += e.fields.length;
  }
}

// Form family breakdown for non-events
const familyStats = new Map<string, { entities: number; fields: number }>();
for (const e of entities) {
  if (e.entity_type === "non-event") {
    const fam = e.form_family_name || "Unknown";
    if (!familyStats.has(fam))
      familyStats.set(fam, { entities: 0, fields: 0 });
    const s = familyStats.get(fam)!;
    s.entities++;
    s.fields += e.fields.length;
  }
}

// Unique tables
const allTables = [...new Set(entities.map((e) => e.table_name).filter(Boolean))].sort();

// Field level distribution
const formLevelFields = entities.reduce(
  (sum, e) => sum + e.fields.filter((f) => f.level === "form").length,
  0
);
const subformLevelFields = entities.reduce(
  (sum, e) => sum + e.fields.filter((f) => f.level === "subform").length,
  0
);
const assessmentLevelFields = entities.reduce(
  (sum, e) => sum + e.fields.filter((f) => f.level === "assessment").length,
  0
);

// Type code distribution
const typeCodeDist = new Map<string, number>();
for (const e of entities) {
  for (const f of e.fields) {
    const tc = f.type_code || "UNKNOWN";
    typeCodeDist.set(tc, (typeCodeDist.get(tc) || 0) + 1);
  }
}

// Top 20 largest entities
const largestEntities = [...entities]
  .sort((a, b) => b.fields.length - a.fields.length)
  .slice(0, 20)
  .map((e) => ({
    form_name: e.form_name,
    form_code: e.form_code,
    entity_type: e.entity_type,
    category: e.category_name || e.form_family_name,
    field_count: e.fields.length,
  }));

// Entities with 0 fields
const emptyEntities = entities
  .filter((e) => e.fields.length === 0)
  .map((e) => ({
    form_name: e.form_name,
    form_code: e.form_code,
    entity_type: e.entity_type,
  }));

const summary = {
  total_entities: entities.length,
  event_entities: entities.filter((e) => e.entity_type === "event").length,
  non_event_entities: entities.filter((e) => e.entity_type === "non-event").length,
  total_fields: totalFields,
  fields_with_caption: fieldsWithCaption,
  fields_with_name: fieldsWithName,
  fields_with_type: fieldsWithType,
  pct_fields_with_caption: Math.round((fieldsWithCaption / totalFields) * 1000) / 10,
  pct_fields_with_type: Math.round((fieldsWithType / totalFields) * 1000) / 10,
  field_level_distribution: {
    form: formLevelFields,
    subform: subformLevelFields,
    assessment: assessmentLevelFields,
  },
  unique_tables: allTables.length,
  tables: allTables,
  category_breakdown: Object.fromEntries(
    [...categoryStats.entries()].sort((a, b) => b[1].fields - a[1].fields)
  ),
  form_family_breakdown: Object.fromEntries(
    [...familyStats.entries()].sort((a, b) => b[1].fields - a[1].fields)
  ),
  type_code_distribution: Object.fromEntries(
    [...typeCodeDist.entries()].sort((a, b) => b[1] - a[1])
  ),
  largest_entities: largestEntities,
  empty_entities: emptyEntities,
  raw_xlsx_counts: {
    events_sheet: events.length,
    events_columns_sheet: eventsCols.length,
    non_events_sheet: nonEvents.length,
    non_events_columns_sheet: nonEventsCols.length,
  },
};

writeFileSync(
  join(BASE, "entity-inventory-summary.json"),
  JSON.stringify(summary, null, 2)
);

console.log(`Wrote entity-inventory-summary.json`);
console.log(`\n--- Summary ---`);
console.log(`Total entities: ${summary.total_entities}`);
console.log(`  Event entities: ${summary.event_entities}`);
console.log(`  Non-event entities: ${summary.non_event_entities}`);
console.log(`Total fields: ${summary.total_fields}`);
console.log(`  With caption: ${summary.fields_with_caption} (${summary.pct_fields_with_caption}%)`);
console.log(`  With type: ${summary.fields_with_type} (${summary.pct_fields_with_type}%)`);
console.log(`  Form-level: ${formLevelFields}`);
console.log(`  Subform-level: ${subformLevelFields}`);
console.log(`  Assessment-level: ${assessmentLevelFields}`);
console.log(`Unique tables: ${summary.unique_tables}`);
console.log(`Empty entities: ${emptyEntities.length}`);
console.log(`Event categories: ${categoryStats.size}`);
console.log(`Form families: ${familyStats.size}`);

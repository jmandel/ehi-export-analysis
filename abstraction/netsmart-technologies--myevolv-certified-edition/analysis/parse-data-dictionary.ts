#!/usr/bin/env bun
/**
 * Parses the myEvolv EHI Export Data Dictionary Crosswalk XLSX
 * and produces entity-inventory-full.json and entity-inventory-summary.json.
 *
 * ## myEvolv Export Model (per Companion Guide)
 *
 * The EHI export produces JSON files containing two types of records:
 *
 * 1. **Event-based** — date-based clinical encounters (allergies, vitals,
 *    medications, assessments, etc.). Each event record is stored in a
 *    specific database table (e.g. `contacts`, `test_header`,
 *    `medication_history`). Identified by `event_definition_id`.
 *
 * 2. **Form-based (non-events)** — static, non-date-based records
 *    (demographics, addresses, insurance). Stored in the `people` table.
 *    No `event_definition_id`.
 *
 * Both types can contain:
 *   - **Subforms**: nested child data arrays within a parent record
 *   - **Assessments**: structured questionnaires with questions/answers
 *
 * ## Key insight: forms are *views* over shared tables
 *
 * Multiple form_codes can be different UI views over the same database
 * table, each exposing a different subset of columns. For example,
 * 707 assessment form_codes all write to `test_header` (227 unique cols).
 *
 * The truly unique data exported lives in three orthogonal sets:
 *   1. Database columns: unique (table_name, jsonPropertyName)
 *   2. Subform fields: unique (subFormCode, subFormJsonPropertyName)
 *   3. Assessment questions: unique assessmentQuestionID
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
const nonEventsCols: any[] = XLSX.utils.sheet_to_json(
  wb.Sheets["Non-Events + Columns"]
);

console.log(`Events: ${events.length}, Events+Cols: ${eventsCols.length}`);
console.log(
  `Non-Events: ${nonEvents.length}, Non-Events+Cols: ${nonEventsCols.length}`
);

function clean(s: any): string | null {
  if (s === undefined || s === null || s === "NULL") return null;
  return String(s).trim();
}

// ─────────────────────────────────────────────────────────────
// PHASE 1: Build lookup maps from the catalog sheets
// ─────────────────────────────────────────────────────────────

// Event definitions by form_code (Events sheet)
const eventDefsByFormCode = new Map<string, any[]>();
for (const e of events) {
  const fc = clean(e.form_code) || "UNKNOWN";
  if (!eventDefsByFormCode.has(fc)) eventDefsByFormCode.set(fc, []);
  eventDefsByFormCode.get(fc)!.push(e);
}

// Non-event catalog by form_code (Non-Events sheet)
const nonEventCatalog = new Map<string, any>();
for (const ne of nonEvents) {
  const fc = clean(ne.form_code) || "UNKNOWN";
  if (!nonEventCatalog.has(fc)) nonEventCatalog.set(fc, ne);
}

// ─────────────────────────────────────────────────────────────
// PHASE 2: Parse column sheets into per-form field lists
//
// The XLSX repeats columns when:
//   (a) Multiple event_definition_ids share a form → same columns repeated
//   (b) Non-event SQL UNION brings in print-bundle duplicates
// We deduplicate within each form using composite keys.
// ─────────────────────────────────────────────────────────────

interface Field {
  name: string | null; // jsonPropertyName, subFormJsonPropertyName, or assessmentQuestionID
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
  event_count: number;
  event_names: string[];
  fields: Field[];
}

function parseField(c: any): { field: Field; dedupKey: string } | null {
  const jsonProp = clean(c.jsonPropertyName);
  const caption = clean(c.formFieldCaption);
  const typeCode = clean(c.typeCode);
  const subName = clean(c.subformName);
  const subCode = clean(c.subFormCode);
  const subProp = clean(c.subFormJsonPropertyName);
  const subCaption = clean(c.subFormFieldCaption);
  const subTypeCode = clean(c.typeCode_1);
  const assessName = clean(c.assessmentName);
  const assessCode = clean(c.assessmentCode);
  const assessQId = clean(c.assessmentQuestionID);
  const assessQCaption = clean(c.assessmentQuestionCaption);

  if (assessName && assessQCaption) {
    return {
      dedupKey: `assess:${assessCode}:${assessQId}`,
      field: {
        name: assessQId,
        caption: assessQCaption,
        type_code: subTypeCode || typeCode,
        level: "assessment",
        assessment_name: assessName,
        assessment_code: assessCode,
        assessment_question_id: assessQId,
        subform_name: subName,
        subform_code: subCode,
      },
    };
  } else if (subName && subProp) {
    return {
      dedupKey: `sub:${subCode}:${subProp}`,
      field: {
        name: subProp,
        caption: subCaption,
        type_code: subTypeCode || typeCode,
        level: "subform",
        subform_name: subName,
        subform_code: subCode,
      },
    };
  } else if (jsonProp) {
    return {
      dedupKey: `form:${jsonProp}`,
      field: {
        name: jsonProp,
        caption: caption,
        type_code: typeCode,
        level: "form",
      },
    };
  } else if (subName && !subProp && subCaption) {
    // Display-only subform reference (no jsonPropertyName)
    return {
      dedupKey: `subref:${subCode}:${subCaption}`,
      field: {
        name: null,
        caption: subCaption,
        type_code: subTypeCode || typeCode,
        level: "subform",
        subform_name: subName,
        subform_code: subCode,
      },
    };
  }
  return null; // SF/TESTS type pointers without detail — skip
}

function collectFields(
  rows: any[],
  firstEventDefId?: string
): Field[] {
  // If firstEventDefId is provided, filter to just that event_definition_id
  // to avoid counting shared-form columns N times
  const filtered = firstEventDefId
    ? rows.filter((c: any) => c.event_definition_id === firstEventDefId)
    : rows;

  const seen = new Set<string>();
  const fields: Field[] = [];
  for (const c of filtered) {
    const parsed = parseField(c);
    if (!parsed) continue;
    if (seen.has(parsed.dedupKey)) continue;
    seen.add(parsed.dedupKey);
    fields.push(parsed.field);
  }
  return fields;
}

// ─────────────────────────────────────────────────────────────
// PHASE 3: Build entity inventory (one entity per form_code)
// ─────────────────────────────────────────────────────────────

const entities: Entity[] = [];

// --- Event entities ---
// Group event columns by form_code
const eventsColsByFormCode = new Map<string, any[]>();
for (const c of eventsCols) {
  const fc = clean(c.form_code) || "UNKNOWN";
  if (!eventsColsByFormCode.has(fc)) eventsColsByFormCode.set(fc, []);
  eventsColsByFormCode.get(fc)!.push(c);
}

for (const [formCode, defs] of eventDefsByFormCode) {
  const firstDef = defs[0];
  const allCols = eventsColsByFormCode.get(formCode) || [];
  const fields = collectFields(allCols, firstDef.event_definition_id);

  entities.push({
    entity_type: "event",
    form_name: firstDef.form_name,
    form_code: formCode,
    table_name: firstDef.table_name,
    category_name: firstDef.category_name,
    category_code: clean(firstDef.category_code),
    form_family_name: null,
    form_family_id: null,
    event_count: defs.length,
    event_names: defs.map((d: any) => d.event_name),
    fields,
  });
}

// --- Non-event entities ---
const nonEventsColsByFormCode = new Map<string, any[]>();
for (const c of nonEventsCols) {
  const fc = clean(c.form_code) || "UNKNOWN";
  if (!nonEventsColsByFormCode.has(fc)) nonEventsColsByFormCode.set(fc, []);
  nonEventsColsByFormCode.get(fc)!.push(c);
}

const allNonEventFormCodes = new Set([
  ...nonEventCatalog.keys(),
  ...nonEventsColsByFormCode.keys(),
]);

for (const formCode of allNonEventFormCodes) {
  const def = nonEventCatalog.get(formCode);
  const cols = nonEventsColsByFormCode.get(formCode) || [];
  const fields = collectFields(cols); // no event_definition_id filtering needed

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

// ─────────────────────────────────────────────────────────────
// PHASE 4: Compute unique data concepts
//
// Three orthogonal sets (see companion guide):
//   1. DB columns: unique (table_name, jsonPropertyName) — the actual
//      database columns exported. Multiple forms may expose overlapping
//      subsets of the same table's columns.
//   2. Subform fields: unique (subFormCode, subFormJsonPropertyName) —
//      reusable nested data structures.
//   3. Assessment questions: unique assessmentQuestionID — questionnaire
//      items identified by GUID.
// ─────────────────────────────────────────────────────────────

const dbColumns = new Set<string>();       // table::jsonProp
const subformFields = new Set<string>();   // subFormCode::subFormJsonProp
const assessmentQs = new Set<string>();    // assessmentQuestionID

for (const e of entities) {
  const table = e.table_name || "people";
  for (const f of e.fields) {
    if (f.level === "form" && f.name) {
      dbColumns.add(`${table}::${f.name}`);
    } else if (f.level === "subform" && f.subform_code && f.name) {
      subformFields.add(`${f.subform_code}::${f.name}`);
    } else if (f.level === "assessment" && f.assessment_question_id) {
      assessmentQs.add(f.assessment_question_id);
    }
  }
}

const uniqueDataConcepts =
  dbColumns.size + subformFields.size + assessmentQs.size;
const uniqueTables = new Set(
  [...dbColumns].map((p) => p.split("::")[0])
).size;
const uniqueSubformCodes = new Set(
  [...subformFields].map((p) => p.split("::")[0])
).size;

// Per-entity sum (for reference — shows inflation from table sharing)
const perEntitySum = entities.reduce((sum, e) => sum + e.fields.length, 0);

// ─────────────────────────────────────────────────────────────
// PHASE 5: Build summary with breakdowns
// ─────────────────────────────────────────────────────────────

// Per-entity field stats
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

// Field level distribution (per-entity sum)
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

// Unique tables list
const allTables = [
  ...new Set(entities.map((e) => e.table_name).filter(Boolean)),
].sort();

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
    table_name: e.table_name,
    category: e.category_name || e.form_family_name,
    field_count: e.fields.length,
  }));

// Table-level breakdown: per DB table, how many unique columns + how many forms reference it
const tableDetail = new Map<
  string,
  { columns: Set<string>; form_codes: Set<string> }
>();
for (const e of entities) {
  const table = e.table_name || "people";
  if (!tableDetail.has(table))
    tableDetail.set(table, { columns: new Set(), form_codes: new Set() });
  const td = tableDetail.get(table)!;
  td.form_codes.add(e.form_code);
  for (const f of e.fields) {
    if (f.level === "form" && f.name) td.columns.add(f.name);
  }
}
const tableBreakdown = [...tableDetail.entries()]
  .map(([table, { columns, form_codes }]) => ({
    table,
    unique_columns: columns.size,
    form_count: form_codes.size,
  }))
  .sort((a, b) => b.unique_columns - a.unique_columns);

// Subform breakdown: per subFormCode, how many unique fields + how many parent forms embed it
const subformDetail = new Map<
  string,
  { name: string; fields: Set<string>; parent_forms: Set<string> }
>();
for (const e of entities) {
  for (const f of e.fields) {
    if (f.level === "subform" && f.subform_code) {
      if (!subformDetail.has(f.subform_code))
        subformDetail.set(f.subform_code, {
          name: f.subform_name || f.subform_code,
          fields: new Set(),
          parent_forms: new Set(),
        });
      const sd = subformDetail.get(f.subform_code)!;
      sd.parent_forms.add(e.form_code);
      if (f.name) sd.fields.add(f.name);
    }
  }
}
const subformBreakdown = [...subformDetail.entries()]
  .map(([code, { name, fields, parent_forms }]) => ({
    subform_code: code,
    subform_name: name,
    unique_fields: fields.size,
    parent_form_count: parent_forms.size,
  }))
  .sort((a, b) => b.parent_form_count - a.parent_form_count);

// Assessment breakdown: per assessmentCode, how many unique questions
const assessDetail = new Map<
  string,
  { name: string; questions: Set<string>; parent_forms: Set<string> }
>();
for (const e of entities) {
  for (const f of e.fields) {
    if (f.level === "assessment" && f.assessment_code) {
      if (!assessDetail.has(f.assessment_code))
        assessDetail.set(f.assessment_code, {
          name: f.assessment_name || f.assessment_code,
          questions: new Set(),
          parent_forms: new Set(),
        });
      const ad = assessDetail.get(f.assessment_code)!;
      ad.parent_forms.add(e.form_code);
      if (f.assessment_question_id) ad.questions.add(f.assessment_question_id);
    }
  }
}

// ─────────────────────────────────────────────────────────────
// PHASE 6: Zero-field entity classification
// ─────────────────────────────────────────────────────────────

const eventsColsFormCodes = new Set(
  eventsCols.map((c: any) => clean(c.form_code) || "")
);
const nonEventsColsFormCodes = new Set(
  nonEventsCols.map((c: any) => clean(c.form_code) || "")
);

const zeroFieldEntities = entities
  .filter((e) => e.fields.length === 0)
  .map((e) => {
    const inColumnsSheet =
      e.entity_type === "event"
        ? eventsColsFormCodes.has(e.form_code)
        : nonEventsColsFormCodes.has(e.form_code);
    return {
      form_name: e.form_name,
      form_code: e.form_code,
      entity_type: e.entity_type,
      category: e.category_name || e.form_family_name,
      reason: inColumnsSheet
        ? "no_data_columns" // in sheet but all jsonPropertyName=NULL (UI-only)
        : "not_in_columns_sheet", // excluded by query filters
    };
  });

const entitiesWithFields = entities.filter((e) => e.fields.length > 0);

// Shared forms count
const sharedFormCount = [...eventDefsByFormCode.values()].filter(
  (defs) => defs.length > 1
).length;

// ─────────────────────────────────────────────────────────────
// PHASE 7: Domain-level aggregations for analysis traceability
// ─────────────────────────────────────────────────────────────

function domainStats(filter: (e: Entity) => boolean) {
  const matched = entities.filter(filter);
  return {
    entities: matched.length,
    fields: matched.reduce((sum, e) => sum + e.fields.length, 0),
    form_codes: matched.map((e) => e.form_code),
  };
}

const domainBreakdown = {
  medications: domainStats(
    (e) =>
      [
        "Medication History",
        "Medication Administration",
        "Standing Orders",
      ].includes(e.category_name || "") ||
      (e.category_name || "").includes("PH MV Medication")
  ),
  allergies: domainStats((e) => e.category_name === "Allergies"),
  immunizations: domainStats((e) => e.category_name === "Immunizations"),
  lab_tests: domainStats((e) => e.category_name === "Lab Tests"),
  vitals: domainStats((e) => e.category_name === "Physical Characteristics"),
  diagnoses: domainStats((e) => e.category_name === "Diagnosis"),
  problems: domainStats((e) => e.category_name === "Problems/Needs"),
  treatment_plans: domainStats(
    (e) =>
      (e.category_name || "").includes("Treatment/Service Plan") ||
      (e.category_name || "").includes("Service Plan")
  ),
  consents: domainStats(
    (e) =>
      e.category_name === "Consents" || e.category_name === "System Consents"
  ),
  progress_notes: domainStats(
    (e) =>
      (e.category_name || "").includes("Progress Note") ||
      e.category_name === "Care Manager Notes"
  ),
  aba: domainStats((e) => (e.category_name || "").startsWith("ABA")),
  incidents: domainStats((e) =>
    (e.category_name || "").startsWith("Incident")
  ),
  substance_use: domainStats((e) => e.category_name === "Substance Use"),
  foster_care: domainStats((e) =>
    [
      "Adoption Activities",
      "Placement Disruptions",
      "Placement and Treatment History",
      "Permanency Plan Goals",
    ].includes(e.category_name || "")
  ),
  mst: domainStats((e) => e.category_name === "MST Events"),
  hcbs: domainStats((e) => (e.category_name || "").startsWith("HCBS")),
  referrals: domainStats((e) =>
    (e.category_name || "").startsWith("Referral")
  ),
  authorization: domainStats(
    (e) => e.category_name === "Authorization Requests"
  ),
  benefit_assignment: domainStats(
    (e) => e.category_name === "Benefit Assignment"
  ),
  income: domainStats(
    (e) =>
      e.category_name === "Income Information" ||
      e.category_name === "Monthly Income"
  ),
  smoking: domainStats((e) => e.category_name === "Smoking Status"),
  pregnancy: domainStats((e) => e.category_name === "Pregnancy"),
  billing_info: domainStats((e) => e.form_code === "CLI_BILL_INFO"),
  sliding_fee: domainStats((e) => e.form_code === "SLID_FEE_ELIG"),
  client_login: domainStats((e) => e.form_code === "CLIENT_LOGIN"),
  person_messages: domainStats((e) => e.form_code === "PERS_MESSAGES"),
  claims_stubs: domainStats((e) =>
    ["PERS_CLAIMS", "PERS_CLAIMS_BALANCE", "PERS_CLAIMS_90", "PERS_INV"].includes(
      e.form_code
    )
  ),
  personal_information: domainStats(
    (e) =>
      e.entity_type === "non-event" &&
      e.form_family_name === "Personal Information"
  ),
  assessments_system: domainStats(
    (e) => e.category_name === "Test/Assessments for People - System"
  ),
  assessments_msdp: domainStats(
    (e) => e.category_name === "MSDP Tests and Assessments"
  ),
  assessments_ph: domainStats(
    (e) =>
      e.category_name === "Public Health Tests/Assessments for People" ||
      e.category_name === "Public Health Tests/Assessments"
  ),
  assessments_nyscri: domainStats(
    (e) => e.category_name === "NYSCRI Test and Assessments"
  ),
  assessments_hcbs: domainStats(
    (e) => e.category_name === "HCBS Test/Assessments"
  ),
  state_reporting: domainStats(
    (e) =>
      e.category_name === "State Reporting Forms" ||
      e.category_name === "State Reporting Requirements"
  ),
  public_health_encounters: domainStats(
    (e) => e.category_name === "Public Health Encounters"
  ),
  activities: domainStats(
    (e) =>
      e.category_name === "Activities" ||
      e.category_name === "Activities - Other"
  ),
  nyscri_progress_notes: domainStats(
    (e) => e.category_name === "NYSCRI Progress Notes"
  ),
};

// ─────────────────────────────────────────────────────────────
// Output
// ─────────────────────────────────────────────────────────────

const summary = {
  // --- Unique data concepts (the headline numbers) ---
  unique_data_concepts: uniqueDataConcepts,
  unique_db_columns: dbColumns.size,
  unique_db_tables: uniqueTables,
  unique_subform_fields: subformFields.size,
  unique_subform_codes: uniqueSubformCodes,
  unique_assessment_questions: assessmentQs.size,
  unique_assessment_codes: assessDetail.size,

  // --- Entity inventory ---
  total_entities: entities.length,
  entities_with_fields: entitiesWithFields.length,
  event_entities: entities.filter((e) => e.entity_type === "event").length,
  non_event_entities: entities.filter((e) => e.entity_type === "non-event")
    .length,
  total_event_definitions: events.length,
  shared_event_forms: sharedFormCount,

  // --- Per-entity sums (shows inflation from shared tables/subforms) ---
  per_entity_field_sum: perEntitySum,
  per_entity_field_level: {
    form: formLevelFields,
    subform: subformLevelFields,
    assessment: assessmentLevelFields,
  },
  pct_fields_with_caption:
    Math.round((fieldsWithCaption / perEntitySum) * 1000) / 10,
  pct_fields_with_type:
    Math.round((fieldsWithType / perEntitySum) * 1000) / 10,

  // --- Table-level detail ---
  table_breakdown: tableBreakdown,

  // --- Subform detail (top 30 most shared) ---
  subform_breakdown: subformBreakdown.slice(0, 30),
  subform_total: subformBreakdown.length,

  // --- Category/family breakdowns ---
  unique_tables_list: allTables,
  category_breakdown: Object.fromEntries(
    [...categoryStats.entries()].sort((a, b) => b[1].fields - a[1].fields)
  ),
  form_family_breakdown: Object.fromEntries(
    [...familyStats.entries()].sort((a, b) => b[1].fields - a[1].fields)
  ),
  type_code_distribution: Object.fromEntries(
    [...typeCodeDist.entries()].sort((a, b) => b[1] - a[1])
  ),
  domain_breakdown: domainBreakdown,
  largest_entities: largestEntities,

  // --- Zero-field entities ---
  zero_field_entities: {
    total: zeroFieldEntities.length,
    by_reason: {
      not_in_columns_sheet: zeroFieldEntities.filter(
        (e) => e.reason === "not_in_columns_sheet"
      ).length,
      no_data_columns: zeroFieldEntities.filter(
        (e) => e.reason === "no_data_columns"
      ).length,
    },
    detail: zeroFieldEntities,
  },

  // --- Raw XLSX row counts ---
  raw_xlsx_counts: {
    events_sheet: events.length,
    events_columns_sheet: eventsCols.length,
    non_events_sheet: nonEvents.length,
    non_events_columns_sheet: nonEventsCols.length,
    total_rows: eventsCols.length + nonEventsCols.length,
  },
};

writeFileSync(
  join(BASE, "entity-inventory-summary.json"),
  JSON.stringify(summary, null, 2)
);

console.log(`Wrote entity-inventory-summary.json`);
console.log(`\n--- Summary ---`);
console.log(
  `Entities: ${summary.total_entities} (${summary.entities_with_fields} with fields)`
);
console.log(`  Event: ${summary.event_entities} | Non-event: ${summary.non_event_entities}`);
console.log(
  `  Event definitions: ${summary.total_event_definitions} (${summary.shared_event_forms} forms shared across 2+)`
);
console.log(`\nUnique data concepts: ${uniqueDataConcepts}`);
console.log(
  `  DB columns:          ${dbColumns.size} across ${uniqueTables} tables`
);
console.log(
  `  Subform fields:      ${subformFields.size} across ${uniqueSubformCodes} subforms`
);
console.log(
  `  Assessment questions: ${assessmentQs.size} across ${assessDetail.size} assessments`
);
console.log(
  `  (Per-entity sum for reference: ${perEntitySum} — inflated ${(perEntitySum / uniqueDataConcepts).toFixed(1)}x by table/subform sharing)`
);
console.log(
  `\nZero-field entities: ${zeroFieldEntities.length} (${summary.zero_field_entities.by_reason.not_in_columns_sheet} not in columns sheet, ${summary.zero_field_entities.by_reason.no_data_columns} UI-only)`
);
console.log(`\nTop tables by column count:`);
for (const t of tableBreakdown.slice(0, 10)) {
  console.log(
    `  ${t.table}: ${t.unique_columns} cols, ${t.form_count} forms`
  );
}

/**
 * Parses the PrimeSuite EHI Export Data Dictionary HTML into structured JSON.
 * Produces entity-inventory-full.json and entity-inventory-summary.json.
 *
 * Run: bun run parse-data-dictionary.ts
 */

import { readFileSync, writeFileSync } from "fs";
import { join } from "path";

const basedir = join(import.meta.dir, "..");
const inputPath = join(basedir, "downloads/PrimeSuiteEHIExport_Data_Dictionary.html");
const html = readFileSync(inputPath, "utf-8");

interface Field {
  name: string;
  dataType: string;
  nullable: boolean;
  description: string;
  hasDescription: boolean;
  references?: string; // extracted FK references
}

interface Entity {
  name: string;
  description: string;
  hasDescription: boolean;
  fields: Field[];
  fieldCount: number;
  category: string; // inferred from table name prefix/pattern
}

// Parse tables using the same pattern as enrichment script but with enhancements
const tablePattern = /<h3 id=\s*(?!list-starts-with)(\w+)>([^<]+)<\/h3>/g;
let match: RegExpExecArray | null;
const positions: { name: string; index: number }[] = [];

while ((match = tablePattern.exec(html)) !== null) {
  positions.push({ name: match[2].trim(), index: match.index });
}

const entities: Entity[] = [];

for (let i = 0; i < positions.length; i++) {
  const pos = positions[i];
  const nextIndex = i + 1 < positions.length ? positions[i + 1].index : html.length;
  const section = html.slice(pos.index, nextIndex);

  // Extract description
  const tableStart = section.indexOf("<table");
  let description = "";
  if (tableStart > 0) {
    const beforeTable = section.slice(0, tableStart);
    const pMatches = beforeTable.match(/<p[^>]*>([\s\S]*?)<\/p>/gi);
    if (pMatches) {
      description = pMatches
        .map((p) => p.replace(/<[^>]*>/g, "").trim())
        .filter(Boolean)
        .join(" ");
    }
  }

  // Extract fields from table
  const fields: Field[] = [];
  const tableMatch = section.match(/<table[\s\S]*?<\/table>/i);
  if (tableMatch) {
    const rows = tableMatch[0].match(/<tr[\s\S]*?<\/tr>/gi);
    if (rows) {
      for (let r = 1; r < rows.length; r++) {
        const cells = rows[r].match(/<td[^>]*>([\s\S]*?)<\/td>/gi);
        if (cells && cells.length >= 4) {
          const cellTexts = cells.map((c) => c.replace(/<[^>]*>/g, "").trim());
          const desc = cellTexts[3];

          // Extract FK references from description
          const refMatch = desc.match(/References:\s*(dbo\.)?(\w+)/);

          fields.push({
            name: cellTexts[0],
            dataType: cellTexts[1],
            nullable: cellTexts[2].toUpperCase() === "YES",
            description: desc,
            hasDescription: desc.length > 0,
            ...(refMatch ? { references: refMatch[2] } : {}),
          });
        }
      }
    }
  }

  // Categorize by table name patterns
  const name = pos.name;
  const category = categorize(name, description);

  entities.push({
    name,
    description,
    hasDescription: description.length > 0,
    fields,
    fieldCount: fields.length,
    category,
  });
}

function categorize(name: string, desc: string): string {
  const n = name.toLowerCase();
  const d = desc.toLowerCase();

  // Billing / Financial
  if (/^(payment|charge|claim|billing|invoice|superbill|fee|copay|deductible|revenue|financial|eob|remittance|era|edi)/i.test(n) ||
      /payment|billing|claim|charge|superbill|copay|fee schedule|revenue/i.test(d))
    return "Billing & Financial";

  // Insurance
  if (/^(insurance|payer|eligibility|coverage|authorization|preauth|precert)/i.test(n) ||
      /insurance|payer|eligibility|coverage|authorization/i.test(d))
    return "Insurance & Coverage";

  // Patient Demographics
  if (/^(patient|person|contact|guardian|emergencycontact|patientdem|race|ethnicity|language|employer)/i.test(n) ||
      /patient.*demographic|person.*info|patient.*contact/i.test(d))
    return "Patient Demographics";

  // Encounters / Visits
  if (/^(encounter|visit|appointment|schedule|appt)/i.test(n) ||
      /encounter|visit|appointment/i.test(d))
    return "Encounters & Scheduling";

  // Problems / Diagnoses
  if (/^(problem|diagnosis|condition|icd|dx)/i.test(n) ||
      /problem|diagnosis|condition/i.test(d))
    return "Problems & Diagnoses";

  // Medications
  if (/^(medication|drug|prescription|rx|dispens|refill|formulary|eprescrib|erx)/i.test(n) ||
      /medication|prescription|drug|pharmacy|dispens/i.test(d))
    return "Medications & Prescriptions";

  // Allergies
  if (/^(allergy|allergen|adverse|reaction)/i.test(n) ||
      /allergy|allergen|adverse.*reaction/i.test(d))
    return "Allergies";

  // Immunizations
  if (/^(immuniz|vaccine|vaccination|vfc)/i.test(n) ||
      /immuniz|vaccine|vaccination/i.test(d))
    return "Immunizations";

  // Vitals
  if (/^(vital|bp|bloodpressure|height|weight|bmi|temperature|pulse|respiration)/i.test(n) ||
      /vital.*sign|blood.*pressure/i.test(d))
    return "Vitals";

  // Lab / Results
  if (/^(lab|result|specimen|loinc|observ)/i.test(n) ||
      /lab.*result|laboratory|specimen|test.*result/i.test(d))
    return "Lab & Results";

  // Orders
  if (/^(order|requisition|orderset)/i.test(n) ||
      /order.*track|requisition|order.*entry/i.test(d))
    return "Orders";

  // Clinical Documents / Notes
  if (/^(clinicaldoc|document|note|narrative|template|clinicalnote|chart)/i.test(n) ||
      /clinical.*document|clinical.*note|chart.*note/i.test(d))
    return "Clinical Documents & Notes";

  // Referrals
  if (/^(referral|refer)/i.test(n) ||
      /referral/i.test(d))
    return "Referrals";

  // Care Plans / Goals
  if (/^(careplan|goal|intervention|careteam)/i.test(n) ||
      /care.*plan|goal|intervention/i.test(d))
    return "Care Plans & Goals";

  // Imaging
  if (/^(imaging|radiology|dicom|xray)/i.test(n) ||
      /imaging|radiology|diagnostic.*imag/i.test(d))
    return "Imaging";

  // Procedures
  if (/^(procedure|surgery|surgical|cpt)/i.test(n) ||
      /procedure/i.test(d))
    return "Procedures";

  // Family History
  if (/^(family|familyhistory|familyhx)/i.test(n) ||
      /family.*history/i.test(d))
    return "Family History";

  // Social History
  if (/^(social|smoking|tobacco|alcohol|substance)/i.test(n) ||
      /social.*history|smoking|tobacco|substance/i.test(d))
    return "Social History";

  // Patient Communications / Portal
  if (/^(message|secure.*msg|portal|communication|inbox)/i.test(n) ||
      /message|portal|communication|inbox/i.test(d))
    return "Patient Communications";

  // Consent / Directives
  if (/^(consent|directive|advance.*directive)/i.test(n) ||
      /consent|directive/i.test(d))
    return "Consents & Directives";

  // Lookup / Reference tables
  if (/lu$/i.test(n) || /lookup$/i.test(n) || /^lu_/i.test(n) ||
      /lookup|reference.*table/i.test(d))
    return "Lookup / Reference";

  // If nothing else matches
  return "Other / Uncategorized";
}

// Generate summary
const totalFields = entities.reduce((s, e) => s + e.fieldCount, 0);
const fieldsWithDesc = entities.reduce(
  (s, e) => s + e.fields.filter((f) => f.hasDescription).length,
  0
);
const entitiesWithDesc = entities.filter((e) => e.hasDescription).length;
const fieldsWithRefs = entities.reduce(
  (s, e) => s + e.fields.filter((f) => f.references).length,
  0
);

// Category breakdown
const categoryBreakdown: Record<string, { tables: number; fields: number; fieldsWithDesc: number }> = {};
for (const e of entities) {
  if (!categoryBreakdown[e.category]) {
    categoryBreakdown[e.category] = { tables: 0, fields: 0, fieldsWithDesc: 0 };
  }
  categoryBreakdown[e.category].tables++;
  categoryBreakdown[e.category].fields += e.fieldCount;
  categoryBreakdown[e.category].fieldsWithDesc += e.fields.filter((f) => f.hasDescription).length;
}

// Top 20 largest entities
const top20 = [...entities]
  .sort((a, b) => b.fieldCount - a.fieldCount)
  .slice(0, 20)
  .map((e) => ({ name: e.name, fields: e.fieldCount, category: e.category, description: e.description.substring(0, 120) }));

// Data type distribution
const dataTypes: Record<string, number> = {};
for (const e of entities) {
  for (const f of e.fields) {
    const dt = f.dataType.toLowerCase().replace(/\(.*\)/, "").trim();
    dataTypes[dt] = (dataTypes[dt] || 0) + 1;
  }
}

const summary = {
  totalEntities: entities.length,
  totalFields,
  fieldsWithDescriptions: fieldsWithDesc,
  fieldsWithDescriptionsPct: Math.round((fieldsWithDesc / totalFields) * 100 * 10) / 10,
  entitiesWithDescriptions: entitiesWithDesc,
  entitiesWithDescriptionsPct: Math.round((entitiesWithDesc / entities.length) * 100 * 10) / 10,
  fieldsWithForeignKeyRefs: fieldsWithRefs,
  categoryBreakdown: Object.entries(categoryBreakdown)
    .sort((a, b) => b[1].fields - a[1].fields)
    .map(([cat, stats]) => ({ category: cat, ...stats })),
  top20LargestEntities: top20,
  dataTypeDistribution: Object.entries(dataTypes)
    .sort((a, b) => b[1] - a[1])
    .map(([type, count]) => ({ type, count })),
};

writeFileSync(join(import.meta.dir, "entity-inventory-full.json"), JSON.stringify(entities, null, 2));
writeFileSync(join(import.meta.dir, "entity-inventory-summary.json"), JSON.stringify(summary, null, 2));

console.log("=== Extraction Complete ===");
console.log(`Tables: ${entities.length}`);
console.log(`Fields: ${totalFields}`);
console.log(`Fields with descriptions: ${fieldsWithDesc} (${summary.fieldsWithDescriptionsPct}%)`);
console.log(`Entities with descriptions: ${entitiesWithDesc} (${summary.entitiesWithDescriptionsPct}%)`);
console.log(`Fields with FK references: ${fieldsWithRefs}`);
console.log("\nCategory breakdown:");
for (const c of summary.categoryBreakdown) {
  console.log(`  ${c.category}: ${c.tables} tables, ${c.fields} fields`);
}
console.log("\nTop 10 largest entities:");
for (const t of top20.slice(0, 10)) {
  console.log(`  ${t.name}: ${t.fields} fields (${t.category})`);
}

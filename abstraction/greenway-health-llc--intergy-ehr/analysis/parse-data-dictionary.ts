#!/usr/bin/env bun
/**
 * parse-data-dictionary.ts
 * 
 * Parses all 261 Intergy EHI data dictionary HTML pages and DBDescriptions.js
 * to produce entity-inventory-full.json and entity-inventory-summary.json.
 * 
 * Reads from: ../downloads/viewer/Contracts/*.htm
 *             ../downloads/viewer/Contracts/include/DBDescriptions.js
 * Outputs:    ./entity-inventory-full.json
 *             ./entity-inventory-summary.json
 */

import { readdir, readFile, writeFile } from "fs/promises";
import { join, basename } from "path";

const CONTRACTS_DIR = join(import.meta.dir, "..", "downloads", "viewer", "Contracts");

interface Field {
  name: string;
  datatype: string;
  default_value: string | null;
  nullable: boolean;
  description: string;
  is_foreign_key: boolean;
}

interface Relationship {
  table: string;
  join_condition: string;
  on_delete: string;
}

interface TableDef {
  name: string;
  description: string;
  last_updated: string | null;
  intergy_version: string | null;
  fields: Field[];
  parent_tables: Relationship[];
  child_tables: Relationship[];
  category: string; // assigned during categorization
}

function extractText(html: string): string {
  return html
    .replace(/<br\s*\/?>/gi, " ")
    .replace(/<[^>]*>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, " ")
    .trim();
}

function parseTablePage(html: string, filename: string, descFromJS: string): TableDef {
  const tableName = basename(filename, ".htm");

  const lastUpdatedMatch = html.match(/Last Updated:\s*([^<]+)/);
  const versionMatch = html.match(/Intergy Version:\s*([^<]+)/);
  const descMatch = html.match(/<h3>\s*Description:\s*(.*?)<\/h3>/is);

  const lastUpdated = lastUpdatedMatch ? lastUpdatedMatch[1].trim() : null;
  const intergyVersion = versionMatch ? versionMatch[1].trim() : null;
  let description = descMatch ? extractText(descMatch[1]) : "";
  if (!description && descFromJS) description = descFromJS;

  // Parse fields
  const fields: Field[] = [];
  const tableDefSection = html.split(/<a name="parentrel">/i)[0] || html;

  const rowRegex =
    /<tr>\s*<td[^>]*>([\s\S]*?)<\/td>\s*<td[^>]*>([\s\S]*?)<\/td>\s*<td[^>]*>([\s\S]*?)<\/td>\s*<td[^>]*>([\s\S]*?)<\/td>\s*<td[^>]*>([\s\S]*?)<\/td>\s*<\/tr>/gi;
  let match: RegExpExecArray | null;
  while ((match = rowRegex.exec(tableDefSection)) !== null) {
    const fieldName = extractText(match[1]);
    const datatype = extractText(match[2]);
    const rawDefault = extractText(match[3]);
    const nullOption = extractText(match[4]);
    const comment = extractText(match[5]);

    if (fieldName && fieldName !== "Field") {
      const isFk = comment.startsWith("FK") || comment.includes("FK -") || comment.includes("FK from");
      fields.push({
        name: fieldName,
        datatype,
        default_value: rawDefault === "?" || rawDefault === "" ? null : rawDefault,
        nullable: nullOption.toUpperCase() === "OPTIONAL",
        description: comment,
        is_foreign_key: isFk,
      });
    }
  }

  // Parse parent tables
  const parentTables: Relationship[] = [];
  const parentSection = html.match(
    /<a name="parentrel"><\/a>[\s\S]*?<table[^>]*>([\s\S]*?)<\/table>/i
  );
  if (parentSection) {
    const relRowRegex =
      /<tr>\s*<td>\s*<a[^>]*>([^<]*)<\/a>\s*<\/td>\s*<td>([\s\S]*?)<\/td>\s*<td>([\s\S]*?)<\/td>\s*<\/tr>/gi;
    while ((match = relRowRegex.exec(parentSection[1])) !== null) {
      parentTables.push({
        table: extractText(match[1]),
        join_condition: extractText(match[2]),
        on_delete: extractText(match[3]),
      });
    }
  }

  // Parse child tables
  const childTables: Relationship[] = [];
  const childSection = html.match(
    /<a name="childrel"><\/a>[\s\S]*?<table[^>]*>([\s\S]*?)<\/table>/i
  );
  if (childSection) {
    const relRowRegex =
      /<tr>\s*<td>\s*<a[^>]*>([^<]*)<\/a>\s*<\/td>\s*<td>([\s\S]*?)<\/td>\s*<td>([\s\S]*?)<\/td>\s*<\/tr>/gi;
    while ((match = relRowRegex.exec(childSection[1])) !== null) {
      childTables.push({
        table: extractText(match[1]),
        join_condition: extractText(match[2]),
        on_delete: extractText(match[3]),
      });
    }
  }

  return {
    name: tableName,
    description,
    last_updated: lastUpdated,
    intergy_version: intergyVersion,
    fields,
    parent_tables: parentTables,
    child_tables: childTables,
    category: "", // will be assigned below
  };
}

// Categorize tables based on name patterns and descriptions
function categorize(t: TableDef): string {
  const n = t.name.toLowerCase();
  const d = (t.description || "").toLowerCase();

  // OB/GYN
  if (n.startsWith("ob")) return "OB/GYN";
  // Cardiology
  if (n.startsWith("cardio")) return "Cardiology";
  // Radiology / Imaging
  if (n.startsWith("ris") || n === "documentinterpretation") return "Imaging/Radiology";
  // Lab
  if (n.startsWith("lab")) return "Laboratory";
  // Rx / Medications
  if (n.startsWith("patientrx") || n.startsWith("rx") || n === "duralert" || n === "persondrugineffe" || n === "persondrugineffe") return "Medications/Prescriptions";
  if (n.startsWith("rx") || n === "persondrugineffe" || n === "persondrugineffective") return "Medications/Prescriptions";
  // Immunizations
  if (n.startsWith("patientvac") || n.startsWith("vaccine")) return "Immunizations";
  // Allergies
  if (n.startsWith("personallergy") || n === "allergy") return "Allergies";
  // Vitals
  if (n.startsWith("encountervital") || n === "vitaltype") return "Vitals";
  // Encounters / Clinical
  if (n.startsWith("encounter") || n === "inpatientvisit" || n === "inpatientvisit note" || n === "inpatientvisit note") return "Encounters/Clinical";
  if (n === "inpatientvisit" || n === "inpatientvisitnote") return "Encounters/Clinical";
  // Problems
  if (n.startsWith("patientproblem") || n === "ailment" || n.startsWith("ailment")) return "Problems/Conditions";
  // Care Plans
  if (n.startsWith("patientcp") || n === "patientcareplan" || n === "patientcareprogram" || n === "patientcareprogramhistory") return "Care Plans";
  // Orders
  if (n.startsWith("patientom") || n.startsWith("patientorderset")) return "Orders";
  // Billing / Charges
  if (n.startsWith("charge") || n.startsWith("claim") || n === "adjustment" || n.startsWith("copay") || n === "responsibilitytransfer") return "Billing/Charges";
  // Plan Claims / Insurance Claims
  if (n.startsWith("planclaim")) return "Insurance Claims";
  // Payments
  if (n.startsWith("payment") || n === "patientremitpayment") return "Payments";
  // Insurance / Coverage
  if (n.startsWith("policy") || n === "plan" || n.startsWith("planalt") || n.startsWith("plangroup") || n === "carrier" || n.startsWith("eligibility") || n === "workerscomp" || n.startsWith("workerscomp")) return "Insurance/Coverage";
  // Referrals
  if (n.startsWith("referral") || n.startsWith("reftrea") || n === "refdoctor" || n === "refdocrole" || n === "patientrefdocspecialty") return "Referrals";
  // Prior Auth
  if (n.startsWith("priorauth")) return "Prior Authorization";
  // Demographics / Person
  if (n.startsWith("person") || n === "patient" || n === "patientaccount" || n === "pracperson" || n.startsWith("pracperson") || n === "dobhistory" || n === "sexhistory") return "Demographics/Person";
  // Accounts / Financial
  if (n.startsWith("account")) return "Accounts/Financial";
  // Documents
  if (n.startsWith("document") || n.startsWith("genfile") || n.startsWith("tmscatalog") || n.startsWith("tmsactivity") || n === "clwcorrespondence") return "Documents";
  // Communications
  if (n === "email" || n === "emailhistory" || n === "phone" || n === "phonehistory") return "Communications/Contact";
  // Address
  if (n === "address" || n === "addresshistory") return "Demographics/Person";
  // Appointments/Scheduling
  if (n.startsWith("appt") || n === "appointment") return "Appointments/Scheduling";
  // Questionnaires
  if (n === "questionnaire" || n === "apptquestionnaire") return "Questionnaires";
  // PHI / Consent
  if (n.startsWith("phi")) return "Consent/PHI";
  // Patient Portal
  if (n === "patientportalaccess") return "Patient Portal";
  // Clinical findings
  if (n === "clinicalcustomfinding" || n === "clinicallookupcode" || n === "clinicalcase" || n.startsWith("medcin") || n.startsWith("import")) return "Clinical Findings";
  // Education
  if (n === "encountereducation") return "Education";
  // Advance Directives
  if (n.startsWith("advancedirective")) return "Advance Directives";
  // UB Codes
  if (n.startsWith("ub")) return "Universal Billing Codes";
  // Recall
  if (n === "recallnotice" || n === "apptrecall") return "Appointments/Scheduling";
  // Lookup/Reference
  if (n === "lookupcode" || n === "altlookuplistcode" || n === "extattributecode" || n === "eaobjectdata" || n === "alternateid") return "Reference/Lookup";
  // Org entities
  if (n === "entity" || n === "company" || n === "department" || n === "financecenter" || n === "practice" || n === "servicecenter" || n === "position" || n === "mmuser" || n === "employee" || n === "provider" || n === "staff" || n === "specialty") return "Organization/Staff";
  // Diagnosis/Procedure codes
  if (n === "diagnosis" || n === "procedure" || n === "procedureevent" || n === "procedureeventdiag") return "Procedures/Diagnosis";
  // Implantable devices
  if (n.startsWith("patimplantable")) return "Implantable Devices";
  // Care Team
  if (n === "careteammember") return "Care Team";
  // Patient-specific
  if (n === "patientclinicalsummary" || n === "patientrsrinfo" || n === "patientrsrnote") return "Patient Programs";
  // Occupation
  if (n === "occupation" || n === "occupationindustry" || n === "personoccupation") return "Demographics/Person";

  return "Other";
}

async function main() {
  // Load descriptions from JS
  const descMap = new Map<string, string>();
  const jsContent = await readFile(join(CONTRACTS_DIR, "include", "DBDescriptions.js"), "utf-8");
  const descRegex = /new Table\('([^']+)'\s*,\s*"([^"]*)"\)/g;
  let m: RegExpExecArray | null;
  while ((m = descRegex.exec(jsContent)) !== null) {
    descMap.set(m[1], m[2]);
  }

  // Parse all HTM files
  const files = (await readdir(CONTRACTS_DIR))
    .filter(f => f.endsWith(".htm") && f !== "DBTOC.htm")
    .sort();

  console.log(`Found ${files.length} table files`);

  const tables: TableDef[] = [];
  let parseErrors = 0;

  for (const file of files) {
    try {
      const html = await readFile(join(CONTRACTS_DIR, file), "utf-8");
      const tableName = basename(file, ".htm");
      const table = parseTablePage(html, file, descMap.get(tableName) || "");
      table.category = categorize(table);
      tables.push(table);
    } catch (err: any) {
      console.error(`PARSE ERROR: ${file}: ${err.message}`);
      parseErrors++;
    }
  }

  // Compute stats
  const totalFields = tables.reduce((s, t) => s + t.fields.length, 0);
  const fieldsWithDesc = tables.reduce((s, t) =>
    s + t.fields.filter(f => f.description && f.description !== "FK" && f.description.length > 3).length, 0);
  const totalRelationships = tables.reduce((s, t) => s + t.parent_tables.length + t.child_tables.length, 0);
  const tablesWithDesc = tables.filter(t => t.description && t.description.length > 0).length;

  // Category breakdown
  const categories = new Map<string, { tables: number; fields: number }>();
  for (const t of tables) {
    const cat = t.category;
    const existing = categories.get(cat) || { tables: 0, fields: 0 };
    existing.tables++;
    existing.fields += t.fields.length;
    categories.set(cat, existing);
  }

  // Write full inventory
  await writeFile(join(import.meta.dir, "entity-inventory-full.json"), JSON.stringify(tables, null, 2));

  // Write summary
  const summary = {
    parse_stats: {
      total_tables: tables.length,
      total_fields: totalFields,
      total_relationships: totalRelationships,
      tables_with_descriptions: tablesWithDesc,
      fields_with_descriptions: fieldsWithDesc,
      fields_description_pct: Math.round((fieldsWithDesc / totalFields) * 100),
      parse_errors: parseErrors,
    },
    category_breakdown: Object.fromEntries(
      [...categories.entries()].sort((a, b) => b[1].fields - a[1].fields)
    ),
    tables: tables.map(t => ({
      name: t.name,
      description: t.description,
      category: t.category,
      field_count: t.fields.length,
      parent_count: t.parent_tables.length,
      child_count: t.child_tables.length,
      fields_with_descriptions: t.fields.filter(f => f.description && f.description !== "FK" && f.description.length > 3).length,
    })),
    top_20_largest: tables
      .sort((a, b) => b.fields.length - a.fields.length)
      .slice(0, 20)
      .map(t => ({ name: t.name, category: t.category, fields: t.fields.length })),
  };

  await writeFile(join(import.meta.dir, "entity-inventory-summary.json"), JSON.stringify(summary, null, 2));

  console.log(`\nParse complete:`);
  console.log(`  Tables: ${tables.length}`);
  console.log(`  Fields: ${totalFields}`);
  console.log(`  Fields with descriptions: ${fieldsWithDesc} (${Math.round((fieldsWithDesc / totalFields) * 100)}%)`);
  console.log(`  Relationships: ${totalRelationships}`);
  console.log(`  Tables with descriptions: ${tablesWithDesc}`);
  console.log(`  Parse errors: ${parseErrors}`);
  console.log(`\nCategory breakdown:`);
  for (const [cat, stats] of [...categories.entries()].sort((a, b) => b[1].fields - a[1].fields)) {
    console.log(`  ${cat}: ${stats.tables} tables, ${stats.fields} fields`);
  }
}

main().catch(console.error);

#!/usr/bin/env bun
/**
 * Parses the extracted data-dictionary.json from the Greenway Prime Suite EHI export
 * and produces:
 *  - full-entity-inventory.json: complete machine-readable extraction
 *  - analysis-stats.json: summary statistics and category breakdowns
 */

import { readFileSync, writeFileSync } from "fs";

const DATA_DIR = "../../../results/greenway-health-llc--greenway-prime-suite/downloads/enrichment";
const raw = JSON.parse(readFileSync(`${DATA_DIR}/data-dictionary.json`, "utf8"));

interface Column {
  name: string;
  dataType: string;
  nullable: boolean;
  description: string;
}

interface Table {
  name: string;
  description: string;
  columns: Column[];
}

// Categorize tables by prefix/name pattern into functional domains
function categorize(name: string, desc: string): string {
  const n = name.toLowerCase();
  const d = (desc || "").toLowerCase();

  // CHC / Community Health Center / FQHC
  if (n.startsWith("chc") || n.startsWith("uds")) return "Community Health Center (CHC/FQHC)";
  
  // Billing / Claims / Financial (EDI)
  if (n.startsWith("ascx12") || n.startsWith("asc_x12") || n.startsWith("x12"))
    return "Billing & Claims (EDI/X12)";

  // Claims Processing
  if (n.startsWith("claim") || n.startsWith("era") || n.startsWith("eob"))
    return "Claims Processing";

  // Billing & Finance  
  if (n.startsWith("billing") || n.startsWith("charge") || n.startsWith("superbill") ||
      n.startsWith("payment") || n.startsWith("deposit") || n.startsWith("ledger") ||
      n.startsWith("financial") || n.startsWith("fee") || n.startsWith("guarantor") ||
      n.startsWith("sb") || n.startsWith("br_") || n.startsWith("batchar") ||
      n.startsWith("batchclaims") || n.startsWith("statement") || n.startsWith("check") ||
      n.startsWith("allocation") || n.startsWith("cob") || n.startsWith("cfb") ||
      n.startsWith("aging") || n.startsWith("servicedetail") || n.startsWith("servicelocation") ||
      n.startsWith("servicegroup") || n === "placeofservice")
    return "Billing & Finance";
  
  // Insurance & Eligibility
  if (n.startsWith("insurance") || n.startsWith("payer") || n.startsWith("coverage") ||
      n.startsWith("eligibility") || n.startsWith("planinsurance") || n.startsWith("elig") ||
      n.startsWith("fctpatientinsurance"))
    return "Insurance & Eligibility";

  // ABN
  if (n.startsWith("abn")) return "Advanced Beneficiary Notice (ABN)";

  // Allergy (including allergen tables)
  if (n.startsWith("allergy") || n.startsWith("allergen") || n.startsWith("reaction"))
    return "Allergy";

  // Immunization / Vaccines (including injection, vial, shot, antigen, dose tables)
  if (n.startsWith("vac") || n.startsWith("imm") || n.startsWith("vaccine") ||
      n.startsWith("immunization") || n.startsWith("vfc") || n.startsWith("injection") ||
      n.startsWith("vial") || n.startsWith("shot") || n.startsWith("antigen") ||
      n.startsWith("dose") || n.startsWith("serum") || n.startsWith("potency") ||
      n.startsWith("armcheck") || n.startsWith("standingorder"))
    return "Immunization / Vaccines";

  // Lab Results & Observations (OBR/OBX are HL7 lab segments)
  if (n.startsWith("lab") || n.startsWith("loinc") || n.startsWith("obr") || n.startsWith("obx") ||
      n.startsWith("specimen") || n.startsWith("flowsheet"))
    return "Lab Results & Observations";

  // Orders (including OrdReq, OrdAdmin, etc.)
  if (n.startsWith("order") || n.startsWith("_oldorder") || n.startsWith("ord") ||
      n.startsWith("geneticscan"))
    return "Orders";

  // Medications / Prescriptions / Rx (including eRx, PBM)
  if (n.startsWith("rx") || n.startsWith("med") || n.startsWith("drug") ||
      n.startsWith("prescription") || n.startsWith("formulary") ||
      n.startsWith("ndc") || n.startsWith("epcs") || n.startsWith("erx") ||
      n.startsWith("cancelrx") || n.startsWith("deny") || n.startsWith("discontinue") ||
      n.startsWith("pbm") || n.startsWith("contraceptive"))
    return "Medications / Prescriptions";

  // Diagnoses / Problems (including SDOH)
  if (n.startsWith("diagnos") || n.startsWith("problem") || n.startsWith("icd") ||
      n.startsWith("hcc") || n.startsWith("sdoh"))
    return "Diagnoses / Problems";

  // Clinical Documents (including CTB = Clinical Template Bin)
  if (n.startsWith("clinical") || n.startsWith("document") || n.startsWith("note") ||
      n.startsWith("transcription") || n.startsWith("ctb") || n.startsWith("onbehalfof") ||
      n.startsWith("adamimage") || n.startsWith("imglib") || n.startsWith("referenceDocument") ||
      n.startsWith("referencedocument") || n.startsWith("stickynoteb") || n.startsWith("bincategory") ||
      n.startsWith("hrabin") || n.startsWith("hraheader") || n.startsWith("hrapatient") ||
      n.startsWith("hrarecommend") || n.startsWith("hrasection") || n.startsWith("primeimage") ||
      n.startsWith("externaldocument") || n.startsWith("discreteelement"))
    return "Clinical Documents";

  // Patient History (medical, family, social, surgical, behavioral, pregnancy, genetic)
  if (n.startsWith("pathist") || n.startsWith("fctpatienthistory"))
    return "Patient History";

  // Patient Demographics & Person records
  if (n.startsWith("patdemo") || n.startsWith("patientdemo") || n.startsWith("patient_") ||
      n.startsWith("patientrace") || n.startsWith("patientethn") ||
      n.startsWith("patientlang") || n.startsWith("patientsex") ||
      n.startsWith("patientgender") || n.startsWith("patientcontact") ||
      n.startsWith("patientphone") || n.startsWith("patientaddress") ||
      n === "patient" || n === "patientinfo" || n.startsWith("address") ||
      n.startsWith("person") || n.startsWith("fctperson") || n.startsWith("fctper") ||
      n.startsWith("nextofkin") || n.startsWith("employer") || n.startsWith("prefix") ||
      n.startsWith("suffix") || n.startsWith("pronoun") || n.startsWith("preferredcommunication") ||
      n.startsWith("dataportability") || n.startsWith("ptactive") || n.startsWith("ptresponsible") ||
      n.startsWith("ptarea") || n.startsWith("ptevent") || n.startsWith("pthistory"))
    return "Patient Demographics";

  // Race / Ethnicity / Gender / Language coding
  if (n.startsWith("race") || n.startsWith("ethnicity") || n.startsWith("gender") ||
      n.startsWith("sexual") || n.startsWith("language") || n.startsWith("marital") ||
      n.startsWith("religion") || n.startsWith("country") || n.startsWith("usstate") ||
      n.startsWith("relation"))
    return "Demographics Reference Data";

  // Patient Portal
  if (n.startsWith("patientportal") || n.startsWith("portal") || n.startsWith("pp_"))
    return "Patient Portal";

  // Patient Records (remaining Pat* tables)
  if (n.startsWith("pat") && !n.startsWith("path"))
    return "Patient Records";

  // Visit / Encounter
  if (n.startsWith("visit") || n.startsWith("encounter"))
    return "Encounters / Visits";

  // Referrals
  if (n.startsWith("referral") || n.startsWith("auth"))
    return "Referrals / Authorizations";

  // Scheduling
  if (n.startsWith("schedule") || n.startsWith("appointment") || n.startsWith("appt") ||
      n.startsWith("booking") || n.startsWith("resource") || n.startsWith("slot"))
    return "Scheduling";

  // Procedures / CPT
  if (n.startsWith("procedure") || n.startsWith("cpt") || n.startsWith("surgery") ||
      n.startsWith("hcpcs") || n.startsWith("ambulatory") || n.startsWith("epsdt") ||
      n.startsWith("emg") || n.startsWith("emmethodology"))
    return "Procedures";

  // Vital Signs / Growth Charts
  if (n.startsWith("vital") || n.startsWith("growth") || n.startsWith("bmi") ||
      n.startsWith("whopediatric") || n.startsWith("cdc") || n.startsWith("oldclinicalvital"))
    return "Vitals / Growth";

  // Care Plans / Goals / Population Health
  if (n.startsWith("careplan") || n.startsWith("goal") || n.startsWith("intervention") ||
      n.startsWith("populationhealth"))
    return "Care Plans / Goals";

  // Consent
  if (n.startsWith("consent") || n.startsWith("directive") || n.startsWith("advance"))
    return "Consents / Directives";

  // Clinical Decision Support
  if (n.startsWith("cds") || n.startsWith("alert") || n.startsWith("reminder"))
    return "Clinical Decision Support";

  // Interoperability / Exchange
  if (n.startsWith("ccda") || n.startsWith("cda") || n.startsWith("directmessag") ||
      n.startsWith("continuity") || n.startsWith("transition") || n.startsWith("fhir") ||
      n.startsWith("healthinformationexchange") || n.startsWith("hie") ||
      n.startsWith("ds") || n.startsWith("ihe") || n.startsWith("interfaceevent"))
    return "Interoperability / Exchange";

  // Messaging / Communication
  if (n.startsWith("message")) return "Messaging / Communications";

  // Provider / Care Provider
  if (n.startsWith("careprovider") || n.startsWith("prescriber") || n.startsWith("provider") ||
      n.startsWith("users") || n.startsWith("directory") || n.startsWith("externalorg"))
    return "Providers & Organizations";

  // Quality Measures / Reporting
  if (n.startsWith("quality") || n.startsWith("measure") || n.startsWith("ecqm") ||
      n.startsWith("mips") || n.startsWith("pqrs") || n.startsWith("pqri") || n.startsWith("mu") ||
      n.startsWith("meaningfuluse") || n.startsWith("meaningful_use") || n.startsWith("research"))
    return "Quality Measures / Reporting";

  // Vocabulary / Coding Systems / Lookups
  if (n.startsWith("vocab") || n.startsWith("fctVocab") || n.startsWith("fctvocab") ||
      n.startsWith("coding") || n.startsWith("concept") || n.startsWith("act") ||
      n.startsWith("libsnomed") || n.startsWith("hti"))
    return "Vocabulary / Coding Systems";

  // Coded values / Lookups
  if (n.endsWith("lu") || n.endsWith("lookup") || n.endsWith("type") ||
      n.endsWith("status") || n.endsWith("code") || n.endsWith("codes"))
    return "Lookup / Reference Tables";

  // Pharmacy
  if (n.startsWith("pharmacy")) return "Medications / Prescriptions";

  // Practice / administrative 
  if (n.startsWith("practice") || n.startsWith("datasource") || n.startsWith("special") ||
      n.startsWith("delay") || n.startsWith("days") || n.startsWith("batch") ||
      n.startsWith("erf") || n.startsWith("pwk") || n.startsWith("mdn") ||
      n.startsWith("implanted") || n.startsWith("crstamp") || n.startsWith("divgroup") ||
      n.startsWith("travelmaster") || n.startsWith("casehead") || n.startsWith("pmm"))
    return "Practice Administration";

  // OB/GYN / Pregnancy specific
  if (n.startsWith("edc") || n.startsWith("pregnancy") || n.startsWith("menstrual") ||
      n.startsWith("homepregnancy") || n.startsWith("officepregnancy") || n.startsWith("typeofdelivery"))
    return "OB/GYN & Pregnancy";

  // UB (Uniform Billing) codes
  if (n.startsWith("ub") || n.startsWith("oldprereg"))
    return "Billing & Finance";

  // Use description-based fallback
  if (d.includes("billing") || d.includes("claim") || d.includes("charge") ||
      d.includes("payment") || d.includes("financial"))
    return "Billing & Finance";
  if (d.includes("insurance") || d.includes("payer") || d.includes("coverage"))
    return "Insurance & Eligibility";
  if (d.includes("immuniz") || d.includes("vaccin"))
    return "Immunization / Vaccines";
  if (d.includes("allergy")) return "Allergy";
  if (d.includes("medication") || d.includes("prescription") || d.includes("drug"))
    return "Medications / Prescriptions";
  if (d.includes("lab result") || d.includes("laboratory"))
    return "Lab Results & Observations";
  if (d.includes("diagnosis") || d.includes("problem list"))
    return "Diagnoses / Problems";
  if (d.includes("vital sign")) return "Vitals / Growth";
  if (d.includes("appointment") || d.includes("scheduling"))
    return "Scheduling";
  if (d.includes("referral")) return "Referrals / Authorizations";
  if (d.includes("clinical document") || d.includes("clinical note"))
    return "Clinical Documents";
  if (d.includes("patient portal")) return "Patient Portal";
  if (d.includes("care plan")) return "Care Plans / Goals";
  if (d.includes("account") || d.includes("service detail") || d.includes("superbill"))
    return "Billing & Finance";

  return "Other / Uncategorized";
}

// Analyze foreign key references in descriptions
function extractForeignKeys(desc: string): string[] {
  const refs: string[] = [];
  const matches = desc.matchAll(/References:\s*dbo\.(\w+)/g);
  for (const m of matches) {
    refs.push(m[1]);
  }
  return refs;
}

// Build full entity inventory
const tables: Table[] = raw;
const inventory = tables.map((t: Table) => {
  const category = categorize(t.name, t.description);
  const columnsWithFK = t.columns.map((c: Column) => ({
    ...c,
    foreignKeys: extractForeignKeys(c.description),
    hasDescription: !!(c.description && c.description.trim().length > 0),
    hasType: !!(c.dataType && c.dataType.trim().length > 0),
  }));

  return {
    name: t.name,
    description: t.description,
    category,
    columnCount: t.columns.length,
    columns: columnsWithFK,
    hasDescription: !!(t.description && t.description.trim().length > 0),
    columnsWithDescriptions: columnsWithFK.filter(c => c.hasDescription).length,
    columnsWithTypes: columnsWithFK.filter(c => c.hasType).length,
    columnsWithForeignKeys: columnsWithFK.filter(c => c.foreignKeys.length > 0).length,
  };
});

// Write full inventory
writeFileSync("full-entity-inventory.json", JSON.stringify(inventory, null, 2));

// Compute stats
const totalTables = inventory.length;
const totalColumns = inventory.reduce((s: number, t: any) => s + t.columnCount, 0);
const totalColumnsWithDesc = inventory.reduce((s: number, t: any) => s + t.columnsWithDescriptions, 0);
const totalColumnsWithTypes = inventory.reduce((s: number, t: any) => s + t.columnsWithTypes, 0);
const totalColumnsWithFK = inventory.reduce((s: number, t: any) => s + t.columnsWithForeignKeys, 0);
const tablesWithDesc = inventory.filter((t: any) => t.hasDescription).length;

// Category breakdown
const categories: Record<string, { tables: number; columns: number; describedColumns: number; tableNames: string[] }> = {};
for (const t of inventory) {
  if (!categories[t.category]) {
    categories[t.category] = { tables: 0, columns: 0, describedColumns: 0, tableNames: [] };
  }
  categories[t.category].tables++;
  categories[t.category].columns += t.columnCount;
  categories[t.category].describedColumns += t.columnsWithDescriptions;
  categories[t.category].tableNames.push(t.name);
}

// Sort categories by table count descending
const sortedCategories = Object.entries(categories)
  .sort((a, b) => b[1].tables - a[1].tables)
  .map(([name, data]) => ({
    category: name,
    ...data,
    descriptionRate: data.columns > 0 ? 
      Math.round(data.describedColumns / data.columns * 100) + "%" : "N/A",
  }));

// Top 20 largest tables by column count
const largestTables = [...inventory]
  .sort((a: any, b: any) => b.columnCount - a.columnCount)
  .slice(0, 20)
  .map((t: any) => ({
    name: t.name,
    category: t.category,
    columns: t.columnCount,
    describedColumns: t.columnsWithDescriptions,
    foreignKeys: t.columnsWithForeignKeys,
  }));

// Tables with 0 described columns
const undescribedTables = inventory.filter((t: any) => t.columnsWithDescriptions === 0)
  .map((t: any) => ({
    name: t.name,
    category: t.category,
    columns: t.columnCount,
  }));

const stats = {
  summary: {
    totalTables,
    totalColumns,
    tablesWithDescriptions: tablesWithDesc,
    tablesWithDescriptionsPercent: Math.round(tablesWithDesc / totalTables * 100) + "%",
    columnsWithDescriptions: totalColumnsWithDesc,
    columnsWithDescriptionsPercent: Math.round(totalColumnsWithDesc / totalColumns * 100) + "%",
    columnsWithDataTypes: totalColumnsWithTypes,
    columnsWithDataTypesPercent: Math.round(totalColumnsWithTypes / totalColumns * 100) + "%",
    columnsWithForeignKeys: totalColumnsWithFK,
    avgColumnsPerTable: Math.round(totalColumns / totalTables * 10) / 10,
  },
  categoryBreakdown: sortedCategories,
  largestTables,
  undescribedTables,
  undescribedTableCount: undescribedTables.length,
};

writeFileSync("analysis-stats.json", JSON.stringify(stats, null, 2));

console.log("=== Summary ===");
console.log(`Tables: ${totalTables}`);
console.log(`Total columns: ${totalColumns}`);
console.log(`Columns with descriptions: ${totalColumnsWithDesc} (${stats.summary.columnsWithDescriptionsPercent})`);
console.log(`Columns with data types: ${totalColumnsWithTypes} (${stats.summary.columnsWithDataTypesPercent})`);
console.log(`Columns with FK references: ${totalColumnsWithFK}`);
console.log(`Tables with descriptions: ${tablesWithDesc} (${stats.summary.tablesWithDescriptionsPercent})`);
console.log(`Tables with 0 described columns: ${undescribedTables.length}`);
console.log(`Avg columns/table: ${stats.summary.avgColumnsPerTable}`);
console.log();
console.log("=== Category Breakdown ===");
for (const cat of sortedCategories) {
  console.log(`  ${cat.category}: ${cat.tables} tables, ${cat.columns} columns (${cat.descriptionRate} described)`);
}
console.log();
console.log("=== Top 20 Largest Tables ===");
for (const t of largestTables) {
  console.log(`  ${t.name}: ${t.columns} cols (${t.describedColumns} described, ${t.foreignKeys} FKs) [${t.category}]`);
}

/**
 * Parse all HTML artifacts from the Azalea Health ChartAccess EHI export documentation
 * and produce entity-inventory-full.json and entity-inventory-summary.json
 */
import * as cheerio from "cheerio";
import { readFileSync, writeFileSync } from "fs";
import { join } from "path";

const DOWNLOADS = join(__dirname, "../downloads");

// --- Parse hospital_export.html: EHR concept → FHIR resource mapping table ---
function parseExportMappings(): Array<{
  ehrConcept: string;
  fhirResource: string;
  fhirResourceUrl: string;
  notes: string;
}> {
  const html = readFileSync(join(DOWNLOADS, "hospital_export.html"), "utf-8");
  const $ = cheerio.load(html);
  const mappings: Array<{
    ehrConcept: string;
    fhirResource: string;
    fhirResourceUrl: string;
    notes: string;
  }> = [];

  // Each mapping row is a div.row.border-bottom with 3 col-md divs (skip header)
  const rows = $("div.row.border-bottom.mx-0.p-2");
  rows.each((_, row) => {
    const cols = $(row).find("div");
    if (cols.length >= 3) {
      const concept = $(cols[0]).text().trim();
      const resourceLink = $(cols[1]).find("a");
      const resource = resourceLink.text().trim() || $(cols[1]).text().trim();
      const url = resourceLink.attr("href") || "";
      const notes = $(cols[2]).text().trim();
      // Skip header row
      if (concept === "EHR Concept") return;
      if (concept) {
        mappings.push({
          ehrConcept: concept,
          fhirResource: resource,
          fhirResourceUrl: url,
          notes: notes,
        });
      }
    }
  });
  return mappings;
}

// --- Parse hospital_resources.html: FHIR resource types supported ---
function parseResourceTypes(): Array<{
  resourceType: string;
  interactions: string[];
  description: string;
}> {
  const html = readFileSync(join(DOWNLOADS, "hospital_resources.html"), "utf-8");
  const $ = cheerio.load(html);
  const resources: Array<{
    resourceType: string;
    interactions: string[];
    description: string;
  }> = [];

  // Parse the resource cards/sections
  $("div.row.border-bottom.mx-0.p-2").each((_, row) => {
    const cols = $(row).find("div");
    if (cols.length >= 2) {
      const name = $(cols[0]).text().trim();
      if (name === "Resource" || !name) return;
      const desc = cols.length >= 3 ? $(cols[2]).text().trim() : "";
      resources.push({
        resourceType: name,
        interactions: [],
        description: desc,
      });
    }
  });
  return resources;
}

// --- Parse CapabilityStatement JSON ---
function parseCapabilityStatement() {
  const cs = JSON.parse(
    readFileSync(join(DOWNLOADS, "capability-statement-hospital.json"), "utf-8")
  );
  const rest = cs.rest?.[0] || {};
  const resources = (rest.resource || []).map((r: any) => ({
    type: r.type,
    interactions: (r.interaction || []).map((i: any) => i.code),
    searchParams: (r.searchParam || []).map((s: any) => ({
      name: s.name,
      type: s.type,
      documentation: s.documentation || "",
    })),
    profile: r.profile || null,
    supportedProfiles: r.supportedProfile || [],
  }));

  return {
    version: cs.version,
    date: cs.date,
    fhirVersion: cs.fhirVersion,
    instantiates: cs.instantiates || [],
    resourceCount: resources.length,
    resources,
  };
}

// --- Build entity inventory ---
function buildEntityInventory() {
  const mappings = parseExportMappings();
  const cs = parseCapabilityStatement();

  // Map EHR concepts to a domain category
  function categorize(concept: string): string {
    const c = concept.toLowerCase();
    if (c.includes("demographic") || c.includes("emergency contact") || c.includes("death"))
      return "Demographics & Patient Info";
    if (c.includes("admission") || c.includes("appointment")) return "Encounters & Scheduling";
    if (c.includes("allerg")) return "Allergies";
    if (c.includes("medication") || c.includes("emar")) return "Medications";
    if (c.includes("immuniz")) return "Immunizations";
    if (c.includes("vital")) return "Vitals";
    if (c.includes("lab")) return "Laboratory";
    if (c.includes("radiology")) return "Radiology / Imaging";
    if (c.includes("diagnos") || c.includes("problem") || c.includes("care level") || c.includes("pregnancy") || c.includes("lactating"))
      return "Problems / Conditions";
    if (c.includes("procedure") || c.includes("cardiology execution") || c.includes("therapy execution"))
      return "Procedures";
    if (c.includes("chart note") || c.includes("file") || c.includes("amendment"))
      return "Clinical Notes & Documents";
    if (c.includes("order") || c.includes("supply") || c.includes("dietary") || c.includes("cardiology order") || c.includes("therapy order"))
      return "Orders";
    if (c.includes("flowsheet")) return "Flowsheets / Observations";
    if (c.includes("smoking") || c.includes("social") || c.includes("sexual"))
      return "Social History";
    if (c.includes("portal") || c.includes("memo")) return "Patient Communications";
    if (c.includes("financial") || c.includes("payment")) return "Financial / Billing";
    if (c.includes("pharmacy")) return "Pharmacy";
    if (c.includes("provider") || c.includes("location")) return "Administrative";
    return "Other";
  }

  // Build entities from the export mappings
  const entities = mappings.map((m) => {
    // Find matching CS resource for field detail
    const csResource = cs.resources.find((r: any) => r.type === m.fhirResource);
    return {
      ehrConcept: m.ehrConcept,
      fhirResource: m.fhirResource,
      fhirResourceUrl: m.fhirResourceUrl,
      notes: m.notes || null,
      category: categorize(m.ehrConcept),
      inCapabilityStatement: !!csResource,
      searchParams: csResource?.searchParams?.length || 0,
      supportedProfiles: csResource?.supportedProfiles || [],
    };
  });

  // Resources in CS but NOT in export mappings
  const exportedResourceTypes = new Set(mappings.map((m) => m.fhirResource));
  const csOnlyResources = cs.resources
    .filter((r: any) => !exportedResourceTypes.has(r.type))
    .map((r: any) => ({
      type: r.type,
      interactions: r.interactions,
      inExportMappings: false,
    }));

  // Resources in export mappings but NOT in CS
  const csResourceTypes = new Set(cs.resources.map((r: any) => r.type));
  const exportOnlyResources = [...new Set(mappings.filter(m => !csResourceTypes.has(m.fhirResource)).map(m => m.fhirResource))];

  return {
    entities,
    csOnlyResources,
    exportOnlyResources,
    capabilityStatement: cs,
  };
}

// --- Generate summary ---
function generateSummary(inventory: ReturnType<typeof buildEntityInventory>) {
  const { entities, csOnlyResources, exportOnlyResources, capabilityStatement } = inventory;

  // Category breakdown
  const categories: Record<string, { count: number; concepts: string[] }> = {};
  for (const e of entities) {
    if (!categories[e.category]) categories[e.category] = { count: 0, concepts: [] };
    categories[e.category].count++;
    categories[e.category].concepts.push(e.ehrConcept);
  }

  // Unique FHIR resources used
  const uniqueFhirResources = [...new Set(entities.map((e) => e.fhirResource))];

  // Resources with FHIR path notes (disambiguating)
  const withNotes = entities.filter((e) => e.notes);

  return {
    totalEhrConcepts: entities.length,
    uniqueFhirResources: uniqueFhirResources.length,
    fhirResourceList: uniqueFhirResources.sort(),
    categoryBreakdown: Object.entries(categories)
      .map(([cat, data]) => ({
        category: cat,
        conceptCount: data.count,
        concepts: data.concepts,
      }))
      .sort((a, b) => b.conceptCount - a.conceptCount),
    conceptsWithNotes: withNotes.length,
    conceptsWithoutNotes: entities.length - withNotes.length,
    capabilityStatementResourceCount: capabilityStatement.resourceCount,
    csOnlyResources: csOnlyResources.map((r: any) => r.type),
    exportOnlyResources,
    exportFormat: "FHIR R4 NDJSON via Bulk Data Export",
    exportMechanism: {
      singlePatient: "In-app UI or API (Patient/$export with _typeFilter)",
      populationExport: "Contact support or API (Patient/$export, Group/$export)",
      noCharge: true,
    },
    documentationQuality: {
      hasDataDictionary: false,
      hasFieldLevelDetail: false,
      hasSampleData: false,
      hasValueSets: false,
      hasMachineReadableSchema: true, // CapabilityStatement
      hasExportMappingTable: true,
      mappingGranularity: "EHR concept → FHIR resource type (no field-level mapping)",
    },
  };
}

// --- Main ---
const inventory = buildEntityInventory();
const summary = generateSummary(inventory);

const ANALYSIS_DIR = join(__dirname);
writeFileSync(
  join(ANALYSIS_DIR, "entity-inventory-full.json"),
  JSON.stringify(inventory, null, 2)
);
writeFileSync(
  join(ANALYSIS_DIR, "entity-inventory-summary.json"),
  JSON.stringify(summary, null, 2)
);

console.log("=== Entity Inventory Summary ===");
console.log(`Total EHR concepts mapped: ${summary.totalEhrConcepts}`);
console.log(`Unique FHIR resources used: ${summary.uniqueFhirResources}`);
console.log(`FHIR resources: ${summary.fhirResourceList.join(", ")}`);
console.log(`\nCategory breakdown:`);
for (const cat of summary.categoryBreakdown) {
  console.log(`  ${cat.category}: ${cat.conceptCount} concepts (${cat.concepts.join(", ")})`);
}
console.log(`\nConcepts with FHIR path notes: ${summary.conceptsWithNotes}`);
console.log(`Concepts without notes: ${summary.conceptsWithoutNotes}`);
console.log(`\nCapabilityStatement resources: ${summary.capabilityStatementResourceCount}`);
console.log(`Resources in CS but NOT in export: ${summary.csOnlyResources.join(", ")}`);
console.log(`Resources in export but NOT in CS: ${summary.exportOnlyResources.join(", ")}`);

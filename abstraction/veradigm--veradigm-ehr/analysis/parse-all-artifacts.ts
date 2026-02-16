/**
 * Parse all Veradigm EHI Export artifacts into a unified entity inventory.
 * 
 * Sources:
 * 1. Veradigm View (Practice Fusion) - HTML data dictionary (87 entity pages)
 * 2. Veradigm EHR - PDF data dictionary (43 tables)
 * 3. Veradigm ePrescribe - PDF (6 TSV files)
 * 4. Veradigm Practice Management - PDF (billing JSON)
 * 5. FollowMyHealth - PDF (FHIR R4 resources)
 * 
 * Output: entity-inventory-full.json, entity-inventory-summary.json
 */

import { readdir, readFile, writeFile } from "fs/promises";
import { join, basename } from "path";
import * as cheerio from "cheerio";

const BASE = join(import.meta.dir, "..");
const DOWNLOADS = join(BASE, "downloads");
const VIEW_DIR = join(DOWNLOADS, "veradigm-view-v6");

interface Field {
  name: string;
  dataType: string;
  description: string;
  nullable?: boolean;
  maxLength?: string;
}

interface Entity {
  product: string;
  category: string;
  entityName: string;
  tsvFilename?: string;
  description: string;
  sourceFile: string;
  format: string;
  primaryKey?: string;
  dbTableName?: string;
  fields: Field[];
}

// ─── 1. Parse Veradigm View HTML pages ───
async function parseViewEntities(): Promise<Entity[]> {
  const entities: Entity[] = [];
  const files = (await readdir(VIEW_DIR)).filter(f => f.endsWith(".html") && f !== "index.html").sort();

  // First, parse the index page to get category mappings
  const indexHtml = await readFile(join(VIEW_DIR, "index.html"), "utf-8");
  const $idx = cheerio.load(indexHtml);
  const categoryMap: Record<string, string> = {};
  
  // Find category headings and their associated links
  $idx("h2, h3, h4").each((_, el) => {
    const heading = $idx(el).text().trim();
    // Find the next list or table after this heading
    let next = $idx(el).next();
    while (next.length && !next.is("h2, h3, h4")) {
      next.find("a").each((_, a) => {
        const href = $idx(a).attr("href") || "";
        const match = href.match(/\/([^/]+)\/?$/);
        if (match) {
          categoryMap[match[1]] = heading;
        }
      });
      // Also check for list items
      if (next.is("ul, ol")) {
        next.find("a").each((_, a) => {
          const href = $idx(a).attr("href") || "";
          const match = href.match(/\/([^/]+)\/?$/);
          if (match) {
            categoryMap[match[1]] = heading;
          }
        });
      }
      next = next.next();
    }
  });

  for (const file of files) {
    const html = await readFile(join(VIEW_DIR, file), "utf-8");
    const $ = cheerio.load(html);
    const pageTitle = $("h1").first().text().trim() || basename(file, ".html");
    const slug = basename(file, ".html");

    // Find all h2 elements (TSV filenames)
    const h2s = $("h2").toArray();
    
    for (let i = 0; i < h2s.length; i++) {
      const h2El = $(h2s[i]);
      const h2Text = h2El.text().trim();
      if (!h2Text.includes(".tsv")) continue;

      // Get description from h4 after h2
      let desc = "";
      let next = h2El.next();
      while (next.length) {
        if (next.is("h4")) {
          desc = next.text().trim();
          break;
        }
        if (next.is("h2")) break;
        next = next.next();
      }

      // Get fields from table after h2
      const fields: Field[] = [];
      next = h2El.next();
      while (next.length) {
        if (next.is("table")) {
          next.find("tr").each((_, tr) => {
            const tds = $(tr).find("td");
            if (tds.length >= 3) {
              const name = $(tds[0]).text().trim();
              const dataType = $(tds[1]).text().trim();
              const description = $(tds[2]).text().trim();
              if (name && name !== "Column Name") {
                fields.push({ name, dataType, description });
              }
            }
          });
          break;
        }
        if (next.is("h2")) break;
        next = next.next();
      }

      entities.push({
        product: "Veradigm View (Practice Fusion)",
        category: categoryMap[slug] || "Uncategorized",
        entityName: pageTitle,
        tsvFilename: h2Text,
        description: desc,
        sourceFile: file,
        format: "TSV",
        fields,
      });
    }
  }

  return entities;
}

// ─── 2. Parse Veradigm EHR PDF ───
async function parseEhrEntities(): Promise<Entity[]> {
  const text = await readFile(join(import.meta.dir, "ehr-export-text.txt"), "utf-8");
  const entities: Entity[] = [];

  // Split by "Filename:" markers
  const sections = text.split(/(?=Filename:\s+\S+\.json)/);
  
  // Map domains from section headings
  let currentDomain = "Unknown";
  
  for (const section of sections) {
    const filenameMatch = section.match(/Filename:\s+(\S+\.json)/);
    if (!filenameMatch) {
      // Check for domain heading
      const domainMatch = section.match(/^(Demographics|History|Vitals|Diagnosis|Medications|Procedures|Lab Orders|Referrals|Flowsheet|Risk Management Program|Contact|Encounter|ReasonForVisit|Immunization|Message|Questionnaire|Care Plans|Additional)\b/m);
      if (domainMatch) currentDomain = domainMatch[1];
      continue;
    }

    const filename = filenameMatch[1];
    
    // Extract description
    const descMatch = section.match(/Description:\s*(.+?)(?:\n|$)/);
    const desc = descMatch ? descMatch[1].trim() : "";

    // Extract DB table name
    const dbMatch = section.match(/EHR internal database table name:\s*(.+?)(?:\n|$)/);
    const dbTable = dbMatch ? dbMatch[1].trim() : "";

    // Extract primary key
    const pkMatch = section.match(/Primary key:\s*(.+?)(?:\n|$)/);
    const pk = pkMatch ? pkMatch[1].trim() : "";

    // Determine domain from section context
    const domainMatch = section.match(/(Demographics|History|Vitals|Diagnosis|Medications|Procedures|Lab Orders|Referrals|Flowsheet|Risk Management Program|Contact|Encounter|ReasonForVisit|Immunization|Message|Questionnaire|Care Plans)/);
    if (domainMatch) currentDomain = domainMatch[1];

    // Extract fields from the table
    const fields: Field[] = [];
    // Match field rows: "FieldName    Description    Type"
    const fieldLines = section.split("\n");
    let inFieldDefs = false;
    let headerSeen = false;
    
    for (let i = 0; i < fieldLines.length; i++) {
      const line = fieldLines[i];
      
      if (line.match(/^\s*Field name\s+Description\s+Type/i) || 
          line.match(/^\s*Field name\s+Description\s+Data type/i) ||
          line.match(/^\s*Name\s+Description\s+Data type/i)) {
        inFieldDefs = true;
        headerSeen = true;
        continue;
      }
      
      if (!inFieldDefs) continue;
      
      // Stop at next section marker
      if (line.match(/^(Filename:|Description:|EHR internal|Primary key:|November|Copyright|Version|This page)/)) {
        inFieldDefs = false;
        continue;
      }
      
      // Parse field line - typically has 2+ columns separated by multiple spaces
      const trimmed = line.trim();
      if (!trimmed || trimmed.length < 5) continue;
      
      // Try to split by multiple spaces (at least 2)
      const parts = trimmed.split(/\s{2,}/);
      if (parts.length >= 2) {
        const name = parts[0].trim();
        // Skip header-like rows
        if (name === "Field name" || name === "Name" || name === "Field Definitions") continue;
        // Skip page headers/footers
        if (name.match(/^(November|Copyright|Version|This page|Veradigm)/)) continue;
        
        const description = parts.length >= 3 ? parts.slice(1, -1).join(" ").trim() : parts[1].trim();
        const dataType = parts.length >= 3 ? parts[parts.length - 1].trim() : "";
        
        if (name && !name.match(/^\d+$/)) {
          fields.push({ name, dataType, description });
        }
      }
    }

    entities.push({
      product: "Veradigm EHR",
      category: currentDomain,
      entityName: filename.replace(".json", ""),
      tsvFilename: filename,
      description: desc,
      sourceFile: "VeradigmEHR_EHI_Export_output_format_documentation_v1.pdf",
      format: "JSON",
      primaryKey: pk,
      dbTableName: dbTable,
      fields,
    });
  }

  return entities;
}

// ─── 3. Parse ePrescribe PDF ───
async function parseEprescribeEntities(): Promise<Entity[]> {
  const text = await readFile(join(import.meta.dir, "eprescribe-export-text.txt"), "utf-8");
  const entities: Entity[] = [];

  const sections = text.split(/(?=Filename:\s+\S+\.tsv)/);
  
  for (const section of sections) {
    const filenameMatch = section.match(/Filename:\s+(\S+\.tsv)/);
    if (!filenameMatch) continue;
    
    const filename = filenameMatch[1];
    const descMatch = section.match(/Description:\s*(.+?)(?:\n|$)/);
    const desc = descMatch ? descMatch[1].trim() : "";
    const dbMatch = section.match(/EHR internal database table name:\s*(.+?)(?:\n|$)/);
    const dbTable = dbMatch ? dbMatch[1].trim() : "";
    const pkMatch = section.match(/Primary key:\s*(.+?)(?:\n|$)/);
    const pk = pkMatch ? pkMatch[1].trim() : "";

    const fields: Field[] = [];
    const fieldLines = section.split("\n");
    let inFieldDefs = false;
    
    for (const line of fieldLines) {
      if (line.match(/^\s*(Name|Field name)\s+Description\s+(Data type|Type)/i)) {
        inFieldDefs = true;
        continue;
      }
      if (!inFieldDefs) continue;
      if (line.match(/^(Filename:|November|Copyright|Version|This page|Veradigm)/)) {
        inFieldDefs = false;
        continue;
      }
      
      const trimmed = line.trim();
      if (!trimmed || trimmed.length < 5) continue;
      
      const parts = trimmed.split(/\s{2,}/);
      if (parts.length >= 2) {
        const name = parts[0].trim();
        if (name === "Name" || name === "Field name" || name.match(/^(November|Copyright|Version|This page)/)) continue;
        const description = parts.length >= 3 ? parts.slice(1, -1).join(" ").trim() : parts[1].trim();
        const dataType = parts.length >= 3 ? parts[parts.length - 1].trim() : "";
        
        if (name && !name.match(/^\d+$/)) {
          fields.push({ name, dataType, description });
        }
      }
    }

    entities.push({
      product: "Veradigm ePrescribe",
      category: filename.replace(".tsv", ""),
      entityName: filename.replace(".tsv", ""),
      tsvFilename: filename,
      description: desc,
      sourceFile: "VeradigmePrescribe_EHI_Export_Documentation_v1.pdf",
      format: "TSV",
      primaryKey: pk,
      dbTableName: dbTable,
      fields,
    });
  }

  return entities;
}

// ─── 4. Parse Veradigm PM PDF ───
async function parsePmEntities(): Promise<Entity[]> {
  const text = await readFile(join(import.meta.dir, "pm-export-text.txt"), "utf-8");
  
  // The PM export is a single JSON structure, not multiple tables
  // Parse the field definitions from the text
  const fields: Field[] = [];
  const lines = text.split("\n");
  let inFieldDefs = false;
  
  for (const line of lines) {
    if (line.match(/FIELD NAME\s+DESCRIPTION/i)) {
      inFieldDefs = true;
      continue;
    }
    if (!inFieldDefs) continue;
    if (line.match(/^(May|Copyright|EHI Data|This page|Chapter)/)) continue;
    
    const trimmed = line.trim();
    if (!trimmed || trimmed.length < 3) continue;
    
    const parts = trimmed.split(/\s{2,}/);
    if (parts.length >= 2) {
      const name = parts[0].trim();
      if (name === "FIELD NAME" || name.match(/^(May|Copyright)/)) continue;
      const description = parts.slice(1).join(" ").trim();
      
      if (name) {
        fields.push({ name, dataType: "JSON", description });
      }
    }
  }

  // Also parse appendix fields
  const appendixSections = text.split(/(?=Claim information fields|Ailment information fields|Ambulance information fields|Drug information fields|Anesthesia information fields|Dental information fields)/);
  const appendixEntities: Entity[] = [];
  
  for (const section of appendixSections) {
    const headerMatch = section.match(/^(Claim information|Ailment information|Ambulance information|Drug information|Anesthesia information|Dental information) fields/m);
    if (!headerMatch) continue;
    
    const appFields: Field[] = [];
    const appLines = section.split("\n");
    let inTable = false;
    
    for (const line of appLines) {
      if (line.match(/FIELD NAME\s+DESCRIPTION/i) || line.match(/Field Name\s+Description/i)) {
        inTable = true;
        continue;
      }
      if (!inTable) continue;
      
      const trimmed = line.trim();
      if (!trimmed || trimmed.length < 3) continue;
      if (trimmed.match(/^(May|Copyright|EHI Data|This page|Chapter|Appendix)/)) continue;
      
      const parts = trimmed.split(/\s{2,}/);
      if (parts.length >= 2) {
        const name = parts[0].trim();
        if (name === "FIELD NAME" || name === "Field Name") continue;
        const description = parts.slice(1).join(" ").trim();
        if (name) {
          appFields.push({ name, dataType: "JSON", description });
        }
      }
    }
    
    if (appFields.length > 0) {
      appendixEntities.push({
        product: "Veradigm Practice Management",
        category: "Billing - " + headerMatch[1],
        entityName: headerMatch[1],
        description: `Appendix: ${headerMatch[1]} fields for claim data`,
        sourceFile: "EHIDataExportFile_ReferenceGuide_VeradigmPM_V2.pdf",
        format: "JSON",
        fields: appFields,
      });
    }
  }

  return [{
    product: "Veradigm Practice Management",
    category: "Billing",
    entityName: "Patient Financial Data (Vouchers/Claims)",
    description: "Patient financial data including vouchers, charges, payments, claims, services, and related billing information",
    sourceFile: "EHIDataExportFile_ReferenceGuide_VeradigmPM_V2.pdf",
    format: "JSON",
    fields,
  }, ...appendixEntities];
}

// ─── 5. Parse FollowMyHealth PDF ───
async function parseFmhEntities(): Promise<Entity[]> {
  const text = await readFile(join(import.meta.dir, "fmh-export-text.txt"), "utf-8");
  const entities: Entity[] = [];

  // FMH uses FHIR R4 resources. Parse sections by resource name.
  const resourceNames = [
    "Account", "Allergy Intolerance", "Appointment", "Bundle", "Communication",
    "Condition", "Diagnostic Report", "Document Reference", "Encounter",
    "Family Member History", "Immunization", "Invoice", "Medication",
    "Medication Request", "Observation", "Patient", "Practitioner", "Procedure"
  ];

  for (const resName of resourceNames) {
    // Find the section for this resource
    const sectionRegex = new RegExp(`^${resName.replace(/\s+/g, "\\s+")}\\s*$`, "m");
    const match = text.match(sectionRegex);
    if (!match) continue;

    const startIdx = match.index! + match[0].length;
    // Find end (next resource heading or end of file)
    let endIdx = text.length;
    for (const other of resourceNames) {
      if (other === resName) continue;
      const otherRegex = new RegExp(`^${other.replace(/\s+/g, "\\s+")}\\s*$`, "m");
      const otherMatch = text.substring(startIdx).match(otherRegex);
      if (otherMatch && otherMatch.index! + startIdx < endIdx) {
        endIdx = otherMatch.index! + startIdx;
      }
    }

    const section = text.substring(startIdx, endIdx);
    
    // Extract source info
    const sourceMatch = section.match(/Source[:\s]+(.*?)(?:\n|$)/);
    const source = sourceMatch ? sourceMatch[1].trim() : "";

    entities.push({
      product: "FollowMyHealth",
      category: "FHIR R4",
      entityName: resName,
      description: `FHIR R4 ${resName} resource. ${source}`,
      sourceFile: "VeradigmFMH_EHI_Export_Data_Guide_v2.pdf",
      format: "FHIR R4 JSON",
      fields: [], // FMH doesn't give field-level detail beyond FHIR standard
    });
  }

  return entities;
}

// ─── Main ───
async function main() {
  console.log("Parsing Veradigm View HTML entities...");
  const viewEntities = await parseViewEntities();
  console.log(`  → ${viewEntities.length} entities, ${viewEntities.reduce((s, e) => s + e.fields.length, 0)} fields`);

  console.log("Parsing Veradigm EHR PDF...");
  const ehrEntities = await parseEhrEntities();
  console.log(`  → ${ehrEntities.length} entities, ${ehrEntities.reduce((s, e) => s + e.fields.length, 0)} fields`);

  console.log("Parsing Veradigm ePrescribe PDF...");
  const eprescribeEntities = await parseEprescribeEntities();
  console.log(`  → ${eprescribeEntities.length} entities, ${eprescribeEntities.reduce((s, e) => s + e.fields.length, 0)} fields`);

  console.log("Parsing Veradigm PM PDF...");
  const pmEntities = await parsePmEntities();
  console.log(`  → ${pmEntities.length} entities, ${pmEntities.reduce((s, e) => s + e.fields.length, 0)} fields`);

  console.log("Parsing FollowMyHealth PDF...");
  const fmhEntities = await parseFmhEntities();
  console.log(`  → ${fmhEntities.length} entities`);

  const allEntities = [...viewEntities, ...ehrEntities, ...eprescribeEntities, ...pmEntities, ...fmhEntities];

  // Write full inventory
  await writeFile(
    join(import.meta.dir, "entity-inventory-full.json"),
    JSON.stringify(allEntities, null, 2)
  );

  // Write summary
  const summary = {
    totalProducts: 5,
    products: [
      {
        name: "Veradigm View (Practice Fusion)",
        format: "TSV",
        entityCount: viewEntities.length,
        totalFields: viewEntities.reduce((s, e) => s + e.fields.length, 0),
        fieldsWithDescriptions: viewEntities.reduce((s, e) => s + e.fields.filter(f => f.description.length > 0).length, 0),
        fieldsWithTypes: viewEntities.reduce((s, e) => s + e.fields.filter(f => f.dataType.length > 0).length, 0),
        categories: [...new Set(viewEntities.map(e => e.category))].map(cat => ({
          category: cat,
          entityCount: viewEntities.filter(e => e.category === cat).length,
          fieldCount: viewEntities.filter(e => e.category === cat).reduce((s, e) => s + e.fields.length, 0),
        })),
      },
      {
        name: "Veradigm EHR",
        format: "JSON",
        entityCount: ehrEntities.length,
        totalFields: ehrEntities.reduce((s, e) => s + e.fields.length, 0),
        fieldsWithDescriptions: ehrEntities.reduce((s, e) => s + e.fields.filter(f => f.description.length > 0).length, 0),
        fieldsWithTypes: ehrEntities.reduce((s, e) => s + e.fields.filter(f => f.dataType.length > 0).length, 0),
        categories: [...new Set(ehrEntities.map(e => e.category))].map(cat => ({
          category: cat,
          entityCount: ehrEntities.filter(e => e.category === cat).length,
          fieldCount: ehrEntities.filter(e => e.category === cat).reduce((s, e) => s + e.fields.length, 0),
        })),
      },
      {
        name: "Veradigm ePrescribe",
        format: "TSV",
        entityCount: eprescribeEntities.length,
        totalFields: eprescribeEntities.reduce((s, e) => s + e.fields.length, 0),
        fieldsWithDescriptions: eprescribeEntities.reduce((s, e) => s + e.fields.filter(f => f.description.length > 0).length, 0),
        categories: [...new Set(eprescribeEntities.map(e => e.category))],
      },
      {
        name: "Veradigm Practice Management",
        format: "JSON",
        entityCount: pmEntities.length,
        totalFields: pmEntities.reduce((s, e) => s + e.fields.length, 0),
        fieldsWithDescriptions: pmEntities.reduce((s, e) => s + e.fields.filter(f => f.description.length > 0).length, 0),
      },
      {
        name: "FollowMyHealth",
        format: "FHIR R4 JSON",
        entityCount: fmhEntities.length,
        resourceTypes: fmhEntities.map(e => e.entityName),
      },
    ],
    grandTotals: {
      totalEntities: allEntities.length,
      totalFields: allEntities.reduce((s, e) => s + e.fields.length, 0),
      fieldsWithDescriptions: allEntities.reduce((s, e) => s + e.fields.filter(f => f.description.length > 0).length, 0),
      fieldsWithTypes: allEntities.reduce((s, e) => s + e.fields.filter(f => f.dataType.length > 0).length, 0),
    },
  };

  await writeFile(
    join(import.meta.dir, "entity-inventory-summary.json"),
    JSON.stringify(summary, null, 2)
  );

  console.log("\nGrand totals:");
  console.log(`  Entities: ${summary.grandTotals.totalEntities}`);
  console.log(`  Fields: ${summary.grandTotals.totalFields}`);
  console.log(`  Fields with descriptions: ${summary.grandTotals.fieldsWithDescriptions}`);
  console.log(`  Fields with types: ${summary.grandTotals.fieldsWithTypes}`);
}

main().catch(console.error);

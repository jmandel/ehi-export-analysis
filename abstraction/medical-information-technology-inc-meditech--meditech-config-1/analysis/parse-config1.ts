/**
 * Parse MEDITECH EHI Export Configuration 1 HTML page
 * Extracts: sections, product-version matrix, file/folder structures,
 * NDJSON schema fields, and produces a complete inventory.
 *
 * Usage: bun run parse-config1.ts
 */

import { readFileSync, writeFileSync } from "fs";

const html = readFileSync("../downloads/ehiexportconfig1.html", "utf-8");
const mainHtml = readFileSync("../downloads/ehiexport-main.html", "utf-8");

// --- Helper: strip HTML tags and decode entities ---
function stripHtml(s: string): string {
  return s
    .replace(/<br\s*\/?>/gi, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&ndash;/g, "–")
    .replace(/&sect;/g, "§")
    .replace(/<[^>]+>/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

// =====================================================
// 1. Parse the Product Sections Index table
// =====================================================
// Extract the product-section matrix from the "Product Sections Index" table

interface ProductVersion {
  name: string;
  sections: string[];
}

const productVersions: ProductVersion[] = [];

// Find the Product Sections Index table (second DataTable in the page after the config overview)
const productSectionsMatch = html.match(
  /Product Sections Index[\s\S]*?<table[^>]*>([\s\S]*?)<\/table>/i
);

if (productSectionsMatch) {
  const tableContent = productSectionsMatch[1];
  // Each row (after header) has product version and sections
  const rows = tableContent.match(/<tr>([\s\S]*?)<\/tr>/gi) || [];

  for (let i = 1; i < rows.length; i++) { // skip header row
    const cells = rows[i].match(/<td[^>]*>([\s\S]*?)<\/td>/gi) || [];
    if (cells.length >= 2) {
      const productName = stripHtml(cells[0]);
      // Extract section names from links
      const sectionLinks = cells[1].match(/<a[^>]*>([\s\S]*?)<\/a>/gi) || [];
      const sectionTexts = cells[1].match(/<p[^>]*>([\s\S]*?)<\/p>/gi) || [];

      const sections: string[] = [];
      for (const link of sectionLinks) {
        const text = stripHtml(link);
        if (text) sections.push(text);
      }
      // Also get any sections that might just be in <p> tags without links
      for (const p of sectionTexts) {
        const text = stripHtml(p);
        if (text && !sections.includes(text) && !text.includes("Product Version")) {
          sections.push(text);
        }
      }

      if (productName && sections.length > 0) {
        productVersions.push({ name: productName, sections });
      }
    }
  }
}

// =====================================================
// 2. Parse the Section Information table
// =====================================================

interface ExportSection {
  name: string;
  anchor_id: string;
  folder_or_file: string;
  description: string;
  files: {
    name: string;
    format: string;
    description: string;
  }[];
  sub_folders: string[];
  applicable_versions: string[];
  version_notes: string;
}

const sections: ExportSection[] = [];

// Find the Section Information table
const sectionInfoMatch = html.match(
  /Section Information[\s\S]*?<table[^>]*>([\s\S]*?)<\/table>/i
);

if (sectionInfoMatch) {
  const tableContent = sectionInfoMatch[1];
  const rows = tableContent.match(/<tr>([\s\S]*?)<\/tr>/gi) || [];

  for (let i = 1; i < rows.length; i++) { // skip header row
    const cells = rows[i].match(/<td[^>]*>([\s\S]*?)<\/td>/gi) || [];
    if (cells.length >= 2) {
      const nameCell = cells[0];
      const detailCell = cells[1];

      // Extract section name from h4
      const h4Match = nameCell.match(/<h4[^>]*>([\s\S]*?)<\/h4>/i);
      const sectionName = h4Match ? stripHtml(h4Match[1]) : stripHtml(nameCell);

      // Extract anchor id
      const anchorMatch = nameCell.match(/name="([^"]+)"/i);
      const anchorId = anchorMatch ? anchorMatch[1] : "";

      // Extract folder/file structure from details
      const detailText = stripHtml(detailCell);

      // Extract file names and descriptions from list items
      const files: { name: string; format: string; description: string }[] = [];
      const fileMatches = detailCell.match(/<li[^>]*>([\s\S]*?)<\/li>/gi) || [];

      let folderOrFile = "";
      const folderMatch = detailText.match(/^(?:Folder|File):\s*([^\n]+)/i);
      if (folderMatch) {
        folderOrFile = folderMatch[1].trim();
      }

      // Parse nested list items for files
      const topLevelItems = detailCell.match(/<li[^>]*?aria-level="1"[^>]*>([\s\S]*?)(?=<li|<\/ul>)/gi) || [];
      for (const item of topLevelItems) {
        const pMatch = item.match(/<p>([\s\S]*?)<\/p>/i);
        const itemText = pMatch ? stripHtml(pMatch[1]) : stripHtml(item);

        // Check if this is a file entry (has a file extension)
        const fileExtMatch = itemText.match(/\.(pdf|txt|json|xml|html|png|jpg|tif|bmp)$/i);
        if (fileExtMatch) {
          // Find the nested description
          const nestedLi = item.match(/<ul[\s\S]*?<li[^>]*>([\s\S]*?)<\/li>/i);
          const desc = nestedLi ? stripHtml(nestedLi[1]) : "";
          files.push({
            name: itemText,
            format: fileExtMatch[1].toUpperCase(),
            description: desc
          });
        }
      }

      // Determine version-specific notes
      let versionNotes = "";
      if (detailText.includes("Expanse, 6.1x only")) {
        versionNotes = "Expanse and 6.1x only";
      } else if (detailText.includes("Expanse only")) {
        versionNotes = "Expanse only";
      }

      // Determine applicable versions from the product sections index
      const applicableVersions: string[] = [];
      for (const pv of productVersions) {
        if (pv.sections.some(s =>
          s.toLowerCase().includes(sectionName.toLowerCase()) ||
          sectionName.toLowerCase().includes(s.toLowerCase().replace(/&/g, "&"))
        )) {
          applicableVersions.push(pv.name);
        }
      }

      // Extract sub-folder descriptions
      const subFolders: string[] = [];
      const subFolderMatches = detailText.match(/Folder:\s*[^\n]+/gi) || [];
      for (const sf of subFolderMatches) {
        subFolders.push(sf.replace(/^Folder:\s*/i, "").trim());
      }

      sections.push({
        name: sectionName,
        anchor_id: anchorId,
        folder_or_file: folderOrFile,
        description: detailText,
        files,
        sub_folders: subFolders,
        applicable_versions: applicableVersions,
        version_notes: versionNotes
      });
    }
  }
}

// =====================================================
// 3. Parse the Export Zip Overview files
// =====================================================

interface ZipMetaFile {
  name: string;
  description: string;
}

const zipMetaFiles: ZipMetaFile[] = [];

const zipOverviewMatch = html.match(
  /Export Zip Overview[\s\S]*?<table[^>]*>([\s\S]*?)<\/table>/i
);

if (zipOverviewMatch) {
  const rows = zipOverviewMatch[1].match(/<tr>([\s\S]*?)<\/tr>/gi) || [];
  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].match(/<td[^>]*>([\s\S]*?)<\/td>/gi) || [];
    if (cells.length >= 2) {
      const name = stripHtml(cells[0]);
      const desc = stripHtml(cells[1]);
      if (name) {
        zipMetaFiles.push({ name, description: desc });
      }
    }
  }
}

// =====================================================
// 4. Parse the NDJSON Schema
// =====================================================

interface SchemaField {
  path: string;
  description: string;
  type: string;
}

const ndjsonSchemaFields: SchemaField[] = [
  { path: "resourceType", description: "Always 'DocumentReference'", type: "string" },
  { path: "id", description: "Identifier of this DocumentReference", type: "string" },
  { path: "meta.id", description: "Identifier of this metadata", type: "string" },
  { path: "meta.versionId", description: "Identifier of this version", type: "string" },
  { path: "meta.lastUpdated", description: "When this was last updated", type: "dateTime" },
  { path: "meta.source", description: "Where the resource came from", type: "string" },
  { path: "meta.profile[]", description: "Profile URL (ehi-document-reference)", type: "uri" },
  { path: "meta.tag[].code", description: "Tag code (ehi-export)", type: "string" },
  { path: "meta.tag[].display", description: "Tag display text", type: "string" },
  { path: "implicitRules", description: "A set of rules under which this content was created", type: "uri" },
  { path: "language", description: "Language of the resource content", type: "code" },
  { path: "status", description: "Status (always 'current')", type: "code" },
  { path: "docStatus", description: "preliminary | final | amended | entered-in-error", type: "code" },
  { path: "type", description: "CodeableConcept indicating kind of document", type: "CodeableConcept" },
  { path: "subject.reference", description: "Patient Reference (resource in US Core FHIR Resources.json)", type: "reference" },
  { path: "date", description: "Date the file was created", type: "dateTime" },
  { path: "description", description: "File description", type: "string" },
  { path: "content[].attachment.id", description: "Identifier of this attachment", type: "string" },
  { path: "content[].attachment.contentType", description: "File type (MIME type)", type: "code" },
  { path: "content[].attachment.url", description: "Pathway to the location of the file", type: "url" },
  { path: "content[].attachment.size", description: "File size", type: "integer" },
  { path: "content[].attachment.title", description: "Title", type: "string" },
  { path: "content[].attachment.creation", description: "Date the file was created", type: "dateTime" },
  { path: "context.id", description: "Identifier of this context", type: "string" },
  { path: "context.encounter[].reference", description: "Encounter Reference (resource in US Core FHIR Resources.json)", type: "reference" },
  { path: "context.period.start", description: "Beginning of the context period", type: "dateTime" },
  { path: "context.period.end", description: "End of the context period", type: "dateTime" },
];

// =====================================================
// 5. Manually fix applicable versions from the parsed HTML
// =====================================================
// The HTML parsing may have missed some matches due to name variations
// Let's do a more precise manual mapping based on what we actually read

const sectionToVersionsMap: Record<string, string[]> = {
  "Electronic Chart": [
    "MEDITECH Expanse 2.2", "MEDITECH Expanse 2.1", "MEDITECH 6.15",
    "MEDITECH 6.08 Acute", "MEDITECH Client/Server 5.67 Acute",
    "MEDITECH MAGIC 5.67 Acute", "MEDITECH HCA MAGIC 5.67 Acute"
  ],
  "Ambulatory Results": [
    "MEDITECH Expanse 2.2", "MEDITECH Expanse 2.1", "MEDITECH 6.15"
  ],
  "Authorization & Referral Management Reports": [
    "MEDITECH Expanse 2.2", "MEDITECH Expanse 2.1", "MEDITECH 6.15"
  ],
  "Financial Reports": [
    "MEDITECH Expanse 2.2", "MEDITECH Expanse 2.1", "MEDITECH 6.15",
    "MEDITECH 6.08 Acute", "MEDITECH Client/Server 5.67 Acute",
    "MEDITECH MAGIC 5.67 Acute"
  ],
  "FHIR Resource Bundle": [
    "MEDITECH Expanse 2.2", "MEDITECH Expanse 2.1", "MEDITECH 6.15",
    "MEDITECH 6.08 Acute", "MEDITECH Client/Server 5.67 Acute",
    "MEDITECH MAGIC 5.67 Acute", "MEDITECH HCA MAGIC 5.67 Acute"
  ],
  "Historical Ambulatory Data": [
    "MEDITECH Expanse 2.2", "MEDITECH Expanse 2.1", "MEDITECH 6.15"
  ],
  "Immunization History": [
    "MEDITECH Expanse 2.2", "MEDITECH Expanse 2.1", "MEDITECH 6.15",
    "MEDITECH 6.08 Acute"
  ],
  "Immunizations": [
    "MEDITECH Client/Server 5.67 Acute"
  ],
  "Implantable Devices": [
    "MEDITECH Client/Server 5.67 Acute", "MEDITECH MAGIC 5.67 Acute",
    "MEDITECH HCA MAGIC 5.67 Acute"
  ],
  "Patient Notices": [
    "MEDITECH 6.08 Acute"
  ],
  "Population Health": [
    "MEDITECH Expanse 2.2", "MEDITECH Expanse 2.1"
  ],
  "Provider Messages": [
    "MEDITECH Client/Server 5.67 Acute", "MEDITECH MAGIC 5.67 Acute",
    "MEDITECH HCA MAGIC 5.67 Acute"
  ],
  "Structured Clinical Documents": [
    "MEDITECH Expanse 2.2", "MEDITECH Expanse 2.1", "MEDITECH 6.15",
    "MEDITECH 6.08 Acute", "MEDITECH Client/Server 5.67 Acute",
    "MEDITECH MAGIC 5.67 Acute", "MEDITECH HCA MAGIC 5.67 Acute"
  ],
  "Utilization Review": [
    "MEDITECH Expanse 2.2", "MEDITECH Expanse 2.1", "MEDITECH 6.15"
  ],
  "Ambulatory Order Summary": [
    "MEDITECH 6.08 Acute"
  ]
};

// Update sections with correct version mappings
for (const section of sections) {
  const key = Object.keys(sectionToVersionsMap).find(k =>
    section.name.includes(k) || k.includes(section.name)
  );
  if (key) {
    section.applicable_versions = sectionToVersionsMap[key];
  }
}

// =====================================================
// 6. Build the full inventory
// =====================================================

// Config 1 doesn't have a structured data dictionary with fields.
// The "entities" here are the export sections (folders/files)
// since this is a document-centric export.

interface ExportEntity {
  entity_name: string;
  entity_type: "folder" | "file" | "bundle";
  category: string;
  format: string;
  description: string;
  fields: SchemaField[] | null;
  field_count: number;
  fields_with_descriptions: number;
  files_in_section: { name: string; format: string; description: string }[];
  applicable_versions: string[];
  version_notes: string;
  data_domain: string;
  structured_data: boolean;
}

const entities: ExportEntity[] = [];

// Electronic Chart
entities.push({
  entity_name: "Electronic Chart",
  entity_type: "folder",
  category: "Clinical Documents",
  format: "PNG, JPG, TIF, BMP, PDF",
  description: "Scanned/electronic documents from the eChart system, organized by account, category, and subcategory. Includes account-specific documents, patient-level (Record_Documents) documents, and global documents.",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [
    { name: "Account folders (AANNNNNNNNNN_Patient_Name)", format: "folder", description: "Documents organized by account number, category, and subcategory" },
    { name: "Record_Documents_Patient_Name", format: "folder", description: "Patient-level (not account-specific) documents" },
    { name: "Global_Documents_Patient_Name", format: "folder", description: "Global documents applying across all encounters" },
  ],
  applicable_versions: sectionToVersionsMap["Electronic Chart"],
  version_notes: "",
  data_domain: "Clinical notes, scanned documents, images, reports",
  structured_data: false
});

// Structured Clinical Documents (C-CDA)
entities.push({
  entity_name: "Structured Clinical Documents (CCDA)",
  entity_type: "folder",
  category: "Structured Clinical Documents",
  format: "C-CDA XML (R2.1 or R1.1)",
  description: "All structured Consolidated-CDA documents that have been created and possibly sent outside of the organization.",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [
    { name: "C-CDA XML files", format: "XML", description: "Consolidated CDA documents per C-CDA R2.1 or R1.1 specifications" }
  ],
  applicable_versions: sectionToVersionsMap["Structured Clinical Documents"],
  version_notes: "",
  data_domain: "Clinical summaries, discharge summaries, H&P, consult notes",
  structured_data: true
});

// FHIR Resource Bundle
entities.push({
  entity_name: "US Core FHIR Resources.json",
  entity_type: "file",
  category: "FHIR Clinical Data",
  format: "FHIR R4 JSON (US Core STU 3.1.1)",
  description: "Contains all available FHIR resources for the exported patient leveraging Patient $everything. Conforms to US Core STU 3.1.1.",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [
    { name: "US Core FHIR Resources.json", format: "JSON", description: "FHIR R4 Patient $everything bundle per US Core STU 3.1.1" }
  ],
  applicable_versions: sectionToVersionsMap["FHIR Resource Bundle"],
  version_notes: "",
  data_domain: "USCDI clinical data (demographics, conditions, medications, allergies, observations, encounters, etc.)",
  structured_data: true
});

// Ambulatory Results
entities.push({
  entity_name: "Ambulatory Results",
  entity_type: "folder",
  category: "Lab/Diagnostic Results",
  format: "PDF",
  description: "Contains ambulatory results: manually entered micro/lab results and outside vendor micro/lab results.",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [
    { name: "Ambulatory (Manual Entry) Results.pdf", format: "PDF", description: "Ambulatory results entered manually for micro and lab" },
    { name: "Ambulatory OV Results.pdf", format: "PDF", description: "Ambulatory results from outside/other vendor for micro and lab" }
  ],
  applicable_versions: sectionToVersionsMap["Ambulatory Results"],
  version_notes: "",
  data_domain: "Laboratory results, microbiology results (ambulatory)",
  structured_data: false
});

// Authorization & Referral Management Reports
entities.push({
  entity_name: "Authorization & Referral Management Reports",
  entity_type: "folder",
  category: "Administrative / Insurance",
  format: "PDF",
  description: "Contains authorization/referral data and insurance eligibility/deduction data for the patient.",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [
    { name: "ARMEHI-ArmAuthData.pdf", format: "PDF", description: "Data of all authorizations and referrals for a particular patient" },
    { name: "ARMEHI-InsEligCopayDeductData.pdf", format: "PDF", description: "Insurance eligibility and deduction data" }
  ],
  applicable_versions: sectionToVersionsMap["Authorization & Referral Management Reports"],
  version_notes: "",
  data_domain: "Authorization, referrals, insurance eligibility, copay, deductibles",
  structured_data: false
});

// Financial Reports
entities.push({
  entity_name: "Financial Reports",
  entity_type: "folder",
  category: "Financial / Billing",
  format: "TXT",
  description: "Contains patient accounting reports with financial transactions, resident trust, and cost estimation.",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [
    { name: "FinancialEHI.txt", format: "TXT", description: "Patient Accounting report with financial transactions for the patient" },
    { name: "ResidentTrustEHI.txt", format: "TXT", description: "Resident Trust report with financial transactions (Expanse, 6.1x only)" },
    { name: "CostEstimation.txt", format: "TXT", description: "Cost estimates for the patient (Expanse only)" }
  ],
  applicable_versions: sectionToVersionsMap["Financial Reports"],
  version_notes: "ResidentTrustEHI.txt: Expanse and 6.1x only; CostEstimation.txt: Expanse only",
  data_domain: "Patient billing, financial transactions, cost estimation",
  structured_data: false // TXT format, likely rendered report
});

// Immunization History
entities.push({
  entity_name: "Patient Immunization History",
  entity_type: "folder",
  category: "Immunizations",
  format: "PDF",
  description: "Contains a list of the patient's immunization history.",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [
    { name: "Patient Immunization History.pdf", format: "PDF", description: "List of patient's immunization history" }
  ],
  applicable_versions: sectionToVersionsMap["Immunization History"],
  version_notes: "",
  data_domain: "Immunizations",
  structured_data: false
});

// Immunizations (C/S only)
entities.push({
  entity_name: "Immunization Record",
  entity_type: "folder",
  category: "Immunizations",
  format: "TXT",
  description: "Contains patient immunization data.",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [
    { name: "Immunization Record.txt", format: "TXT", description: "Patient immunization data" }
  ],
  applicable_versions: sectionToVersionsMap["Immunizations"],
  version_notes: "Client/Server 5.67 Acute only",
  data_domain: "Immunizations",
  structured_data: false
});

// Implantable Devices
entities.push({
  entity_name: "Implantable Devices Data",
  entity_type: "folder",
  category: "Medical Devices",
  format: "TXT",
  description: "Contains patient medical/implantable devices.",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [
    { name: "Implantable Devices Data.txt", format: "TXT", description: "Patient medical/implantable devices" }
  ],
  applicable_versions: sectionToVersionsMap["Implantable Devices"],
  version_notes: "Client/Server and MAGIC Acute only",
  data_domain: "Medical devices, implantable devices",
  structured_data: false
});

// Patient Notices
entities.push({
  entity_name: "Patient Notices",
  entity_type: "folder",
  category: "Patient Communications",
  format: "PDF",
  description: "Contains patient and physician interactive messages.",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [
    { name: "Patient Notices.pdf", format: "PDF", description: "Patient and physician interactive messages" }
  ],
  applicable_versions: sectionToVersionsMap["Patient Notices"],
  version_notes: "6.08 Acute only",
  data_domain: "Patient-provider communications",
  structured_data: false
});

// Population Health
entities.push({
  entity_name: "Population Health",
  entity_type: "folder",
  category: "Population Health",
  format: "PDF",
  description: "Contains population health external data (aggregated data received from a vendor).",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [
    { name: "Population Health.pdf", format: "PDF", description: "Population health external aggregated data received from a vendor" }
  ],
  applicable_versions: sectionToVersionsMap["Population Health"],
  version_notes: "",
  data_domain: "Population health, external aggregated data",
  structured_data: false
});

// Provider Messages
entities.push({
  entity_name: "Provider Messages",
  entity_type: "folder",
  category: "Patient Communications",
  format: "TXT",
  description: "Contains patient and physician interactive messages.",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [
    { name: "Provider Messages.txt", format: "TXT", description: "Patient and physician interactive messages" }
  ],
  applicable_versions: sectionToVersionsMap["Provider Messages"],
  version_notes: "Client/Server and MAGIC Acute only",
  data_domain: "Patient-provider communications",
  structured_data: false
});

// Utilization Review
entities.push({
  entity_name: "Utilization Review",
  entity_type: "folder",
  category: "Care Management",
  format: "PDF",
  description: "Contains case management utilization reviews.",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [
    { name: "Utilization Review.pdf", format: "PDF", description: "Case management utilization reviews" }
  ],
  applicable_versions: sectionToVersionsMap["Utilization Review"],
  version_notes: "",
  data_domain: "Case management, utilization review",
  structured_data: false
});

// Historical Ambulatory Data
entities.push({
  entity_name: "Historical Ambulatory Data",
  entity_type: "folder",
  category: "Historical Clinical Data",
  format: "PNG, JPG, TIF, BMP, TXT, PDF",
  description: "Contains historical ambulatory documentation migrated from a previous version of the software.",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [
    { name: "Document files and folders", format: "mixed", description: "Historical ambulatory documentation migrated from previous software version" }
  ],
  applicable_versions: sectionToVersionsMap["Historical Ambulatory Data"],
  version_notes: "Expanse 2.2, 2.1, and 6.15 only",
  data_domain: "Historical ambulatory records",
  structured_data: false
});

// Ambulatory Order Summary (referenced in 6.08 Acute product sections but no section info in docs)
entities.push({
  entity_name: "Ambulatory Order Summary",
  entity_type: "folder",
  category: "Orders",
  format: "Unknown (not documented)",
  description: "Referenced in the 6.08 Acute product sections index but no section detail is provided in the documentation. Presumably contains ambulatory order data.",
  fields: null,
  field_count: 0,
  fields_with_descriptions: 0,
  files_in_section: [],
  applicable_versions: sectionToVersionsMap["Ambulatory Order Summary"],
  version_notes: "6.08 Acute only; documentation gap - no section detail provided",
  data_domain: "Orders (ambulatory)",
  structured_data: false
});

// Table of Contents NDJSON (metadata file)
entities.push({
  entity_name: "Table of Contents.ndjson",
  entity_type: "file",
  category: "Export Metadata",
  format: "NDJSON (FHIR DocumentReference)",
  description: "Machine-readable metadata file containing FHIR DocumentReference resources for all patient data files in the export zip. Conforms to Argonaut EHI Export API IG (draft).",
  fields: ndjsonSchemaFields,
  field_count: ndjsonSchemaFields.length,
  fields_with_descriptions: ndjsonSchemaFields.filter(f => f.description).length,
  files_in_section: [
    { name: "Table of Contents.ndjson", format: "NDJSON", description: "FHIR DocumentReference resources indexing all export files" }
  ],
  applicable_versions: [
    "MEDITECH Expanse 2.2", "MEDITECH Expanse 2.1", "MEDITECH 6.15",
    "MEDITECH 6.08 Acute", "MEDITECH Client/Server 5.67 Acute",
    "MEDITECH MAGIC 5.67 Acute", "MEDITECH HCA MAGIC 5.67 Acute"
  ],
  version_notes: "Included in all product versions",
  data_domain: "Export file metadata/index",
  structured_data: true
});

// =====================================================
// 7. Build the full inventory JSON
// =====================================================

const inventory = {
  export_configuration: "Configuration 1",
  description: "MEDITECH EHI Export Configuration 1 — for sites using Health Information Management (HIM) and Scanning/eChart (SCN) modules",
  source_file: "downloads/ehiexportconfig1.html",
  source_url: "https://home.meditech.com/en/d/restapiresources/pages/ehiexportconfig1.htm",
  applicable_platforms: [
    { name: "Expanse 2.2", settings: "Acute & Ambulatory" },
    { name: "Expanse 2.1", settings: "Acute & Ambulatory" },
    { name: "6.15", settings: "Acute & Ambulatory" },
    { name: "6.08", settings: "Acute only" },
    { name: "Client/Server 5.67", settings: "Acute only" },
    { name: "MAGIC 5.67", settings: "Acute only" },
    { name: "HCA MAGIC 5.67", settings: "Acute only" }
  ],
  required_modules: [
    "Health Information Management (HIM)",
    "Scanning and Archiving with eChart (SCN)",
    "Patient and Consumer Health Portal (PHM) [optional]"
  ],
  export_format: "ZIP file containing multiple formats",
  zip_metadata_files: zipMetaFiles,
  product_version_matrix: productVersions,
  entities: entities,
  ndjson_schema: {
    resource_type: "DocumentReference",
    profile: "http://fhir.org/argonaut/ehi-api/StructureDefinition/ehi-document-reference",
    fields: ndjsonSchemaFields
  },
  statistics: {
    total_export_sections: entities.filter(e => e.category !== "Export Metadata").length,
    total_entities: entities.length,
    sections_with_structured_data: entities.filter(e => e.structured_data).length,
    sections_with_unstructured_data: entities.filter(e => !e.structured_data).length,
    total_documented_files: entities.reduce((sum, e) => sum + e.files_in_section.length, 0),
    ndjson_schema_fields: ndjsonSchemaFields.length,
    product_versions_covered: productVersions.length,
    max_sections_per_version: Math.max(...productVersions.map(pv => pv.sections.length)),
    min_sections_per_version: Math.min(...productVersions.map(pv => pv.sections.length)),
  }
};

writeFileSync("entity-inventory-full.json", JSON.stringify(inventory, null, 2));
console.log("Wrote entity-inventory-full.json");

// =====================================================
// 8. Build summary JSON
// =====================================================

const summary = {
  export_configuration: inventory.export_configuration,
  total_export_sections: inventory.statistics.total_export_sections,
  total_entities_including_metadata: inventory.statistics.total_entities,
  sections_with_structured_data: inventory.statistics.sections_with_structured_data,
  sections_with_unstructured_data: inventory.statistics.sections_with_unstructured_data,
  total_documented_files: inventory.statistics.total_documented_files,
  ndjson_schema_fields: inventory.statistics.ndjson_schema_fields,
  product_versions: productVersions.map(pv => ({
    name: pv.name,
    section_count: pv.sections.length,
    sections: pv.sections
  })),
  categories: (() => {
    const cats: Record<string, { entity_count: number; entities: string[] }> = {};
    for (const e of entities) {
      if (!cats[e.category]) cats[e.category] = { entity_count: 0, entities: [] };
      cats[e.category].entity_count++;
      cats[e.category].entities.push(e.entity_name);
    }
    return cats;
  })(),
  format_breakdown: (() => {
    const formats: Record<string, number> = {};
    for (const e of entities) {
      const f = e.format.split(",")[0].trim();
      formats[f] = (formats[f] || 0) + 1;
    }
    return formats;
  })(),
  structured_vs_unstructured: {
    structured: entities.filter(e => e.structured_data).map(e => ({
      name: e.entity_name,
      format: e.format
    })),
    unstructured: entities.filter(e => !e.structured_data).map(e => ({
      name: e.entity_name,
      format: e.format
    }))
  },
  data_domains_covered: [...new Set(entities.map(e => e.data_domain))],
  documentation_gaps: [
    "No data dictionary with field-level detail for Config 1 (unlike Config 2 which has CSV data dictionaries)",
    "Ambulatory Order Summary section referenced in 6.08 product index but no section detail provided",
    "No sample data or example export files provided",
    "Financial reports (FinancialEHI.txt) format and field structure not documented",
    "Electronic Chart document categories/subcategories are organization-defined, not standardized",
    "FHIR resource bundle documented only by reference to US Core STU 3.1.1 spec — no vendor-specific extensions or customizations documented",
    "C-CDA documents documented only by reference to standard specs — no vendor-specific template details",
    "No documentation of data types, value sets, or relationships within any section",
    "Implementation guides behind customer portal login wall (customer.meditech.com)"
  ]
};

writeFileSync("entity-inventory-summary.json", JSON.stringify(summary, null, 2));
console.log("Wrote entity-inventory-summary.json");

// Print key stats
console.log("\n=== Config 1 Export Inventory Statistics ===");
console.log(`Total export sections: ${summary.total_export_sections}`);
console.log(`Sections with structured data: ${summary.sections_with_structured_data}`);
console.log(`Sections with unstructured/rendered data: ${summary.sections_with_unstructured_data}`);
console.log(`Total documented files across all sections: ${summary.total_documented_files}`);
console.log(`NDJSON schema fields: ${summary.ndjson_schema_fields}`);
console.log(`Product versions covered: ${productVersions.length}`);
console.log(`\nSections per product version:`);
for (const pv of productVersions) {
  console.log(`  ${pv.name}: ${pv.sections.length} sections`);
}
console.log(`\nCategories:`);
for (const [cat, info] of Object.entries(summary.categories)) {
  console.log(`  ${cat}: ${info.entity_count} entities (${info.entities.join(", ")})`);
}
console.log(`\nStructured data sections: ${summary.structured_vs_unstructured.structured.map(s => s.name).join(", ")}`);
console.log(`Unstructured data sections: ${summary.structured_vs_unstructured.unstructured.map(s => s.name).join(", ")}`);

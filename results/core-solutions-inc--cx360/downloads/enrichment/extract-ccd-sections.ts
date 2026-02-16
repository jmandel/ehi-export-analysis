#!/usr/bin/env bun
/**
 * extract-ccd-sections.ts
 *
 * Parses the Core Solutions Cx360 EHI Export Documentation PDF (text extracted
 * via pdftotext) and produces a structured JSON representation of all CCD
 * sections and their data elements, XPATH entries, code systems, and code
 * system names.
 *
 * Because pdftotext mangles the multi-column table layouts (columns merge,
 * lines wrap mid-word), this script uses the visually-verified ground truth
 * from the rendered PDF pages to produce a hand-curated but machine-queryable
 * JSON artifact.
 *
 * Run: bun run extract-ccd-sections.ts
 * Input: ../Electronic-Health-Information-Export-Doc.pdf (via pdftotext)
 * Output: ./ccd-sections.json, ./coverage-accounting.json
 */

import { writeFileSync } from "fs";
import { resolve, dirname } from "path";

const outDir = dirname(new URL(import.meta.url).pathname);

// ----- Types -----

interface DataElement {
  name: string;
  xpath_entry: string | null;
  code_system_oid: string | null;
  code_system_name: string | null;
}

interface CCDSection {
  section_name: string;
  template_id: string | null;
  effective_date: string | null;
  data_elements: DataElement[];
}

interface ExportDocumentation {
  vendor: string;
  product: string;
  version: string;
  document_date: string;
  criterion: string;
  standard_referenced: string;
  export_format: string;
  export_modes: string[];
  selectable_sections: string[];
  ccd_sections: CCDSection[];
}

// ----- Data (hand-curated from visual inspection of all 12 PDF pages) -----

const doc: ExportDocumentation = {
  vendor: "Core Solutions Inc",
  product: "Cx360",
  version: "V7",
  document_date: "2023-12",
  criterion: "170.315(b)(10)",
  standard_referenced:
    "§ 170.205(a)(4) HL7® Implementation Guide for CDA® Release 2: Consolidated CDA Templates for Clinical Notes (US Realm), Draft Standard for Trial Use Release 2.1, August 2015",
  export_format: "CCD (Continuity of Care Document) / C-CDA, plus Adobe PDF human-readable rendering",
  export_modes: [
    "Single Patient Export via Patient Summary Report Screen",
    "Bulk Patient Export via CCDA Management utility (by provider or appointments)",
    "On-demand download of Images / Clinical notes (PDF)"
  ],
  selectable_sections: [
    "Patient Section",
    "Encounter Section",
    "Allergies Section",
    "Medications Section",
    "Problems Section",
    "Diagnosis Section",
    "Referral Section",
    "Procedures Section",
    "Instructions Section",
    "Functional And Cognitive Section",
    "Immunizations Section",
    "Vital Signs Section",
    "Lab Results Section",
    "Care Plan Section",
    "Social History Section"
  ],
  ccd_sections: [
    {
      section_name: "Patient Demographics/Information",
      template_id: null,
      effective_date: null,
      data_elements: [
        { name: "Patient Name", xpath_entry: "patient/name", code_system_oid: null, code_system_name: null },
        { name: "Sex", xpath_entry: "patient/administrativeGenderCode", code_system_oid: "2.16.840.1.113883.5.1", code_system_name: "AdministrativeGender" },
        { name: "Date of Birth", xpath_entry: "patient/birthTime", code_system_oid: null, code_system_name: null },
        { name: "Race", xpath_entry: "patient/raceCode", code_system_oid: "2.16.840.1.113883.6.238", code_system_name: "Race & Ethnicity - CDC" },
        { name: "Ethnicity", xpath_entry: "patient/ethnicGroupCode", code_system_oid: "2.16.840.1.113883.6.238", code_system_name: "Race & Ethnicity - CDC" },
        { name: "Preferred Language", xpath_entry: "patient/languageCommunication/languageCode", code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Provider's name and office contact information",
      template_id: null,
      effective_date: null,
      data_elements: [
        { name: "Performer Name", xpath_entry: "documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name", code_system_oid: null, code_system_name: null },
        { name: "Performer Telecom", xpath_entry: "documentationOf/serviceEvent/performer/assignedEntity/telecom", code_system_oid: null, code_system_name: null },
        { name: "Performer Address", xpath_entry: "documentationOf/serviceEvent/performer/assignedEntity/addr", code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Date and Location of visit",
      template_id: "2.16.840.1.113883.10.20.22.2.22.1",
      effective_date: "2015-08-01",
      data_elements: [
        { name: "Encounter Time", xpath_entry: "entry/encounter/effectiveTime/@value", code_system_oid: null, code_system_name: null },
        { name: "Encounter Location", xpath_entry: "entry/encounter/participant/participantRole/addr", code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Chief Complaint and Reason for visit",
      template_id: "2.16.840.1.113883.10.20.22.2.13",
      effective_date: "2014-06-09",
      data_elements: [
        { name: "Patient visit details/complaints", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Encounters",
      template_id: "2.16.840.1.113883.10.20.22.2.22.1",
      effective_date: "2015-08-01",
      data_elements: [
        { name: "Encounter Code and Code Description", xpath_entry: "2.16.840.1.113883.10.20.22.4.49: 2015-08-01", code_system_oid: "2.16.840.1.113883.6.12", code_system_name: "CPT" },
        { name: "Performer", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Diagnosis", xpath_entry: null, code_system_oid: "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3 (translation code)", code_system_name: "SNOMED and ICD10" },
        { name: "Location", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Date", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Immunizations",
      template_id: "2.16.840.1.113883.10.20.22.2.2.1",
      effective_date: "2015-08-01",
      data_elements: [
        { name: "Vaccine", xpath_entry: "2.16.840.1.113883.10.20.22.4.52: 2015-08-01", code_system_oid: "2.16.840.1.113883.12.292 and 2.16.840.1.113883.6.12 (translation code)", code_system_name: "CVX and CPT-4" },
        { name: "Date", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Status", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Route", xpath_entry: null, code_system_oid: "2.16.840.1.113883.3.26.1.1", code_system_name: "National Cancer Institute (NCI) Thesaurus" },
        { name: "Site", xpath_entry: null, code_system_oid: "2.16.840.1.113883.6.96", code_system_name: "SNOMED" },
        { name: "Manufacturer", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Dose", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Lot Number", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Notes", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Instructions",
      template_id: "2.16.840.1.113883.10.20.22.2.45",
      effective_date: "2014-06-09",
      data_elements: [
        { name: "Patient Instructions/Followup Reasons", xpath_entry: "2.16.840.1.113883.10.20.22.4.20: 2014-06-09", code_system_oid: "2.16.840.1.113883.6.96", code_system_name: "SNOMED" }
      ]
    },
    {
      section_name: "Treatment Plan",
      template_id: "2.16.840.1.113883.10.20.22.2.10",
      effective_date: "2014-06-09",
      data_elements: [
        { name: "Planned Observation", xpath_entry: "2.16.840.1.113883.10.20.22.4.44: 2014-06-09", code_system_oid: "2.16.840.1.113883.6.1", code_system_name: "LOINC" },
        { name: "Planned Date", xpath_entry: "2.16.840.1.113883.10.20.22.4.40: 2014-06-09 / 2.16.840.1.113883.10.20.22.4.39: 2014-06-09 / 2.16.840.1.113883.10.20.22.4.121", code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Social History",
      template_id: "2.16.840.1.113883.10.20.22.2.17",
      effective_date: "2015-08-01",
      data_elements: [
        { name: "Social History Observation", xpath_entry: "2.16.840.1.113883.10.20.22.4.78: 2014-06-09", code_system_oid: "2.16.840.1.113883.6.1", code_system_name: "LOINC" },
        { name: "Description", xpath_entry: null, code_system_oid: "2.16.840.1.113883.6.96", code_system_name: "SNOMED" },
        { name: "Dates Observed", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Problems",
      template_id: "2.16.840.1.113883.10.20.22.2.5.1",
      effective_date: "2015-08-01",
      data_elements: [
        { name: "Problem", xpath_entry: "2.16.840.1.113883.10.20.22.4.3: 2015-08-01", code_system_oid: "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3 (translation code)", code_system_name: "SNOMED and ICD10" },
        { name: "Status", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Active date", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Medications",
      template_id: "2.16.840.1.113883.10.20.22.2.1.1",
      effective_date: "2014-06-09",
      data_elements: [
        { name: "Medication", xpath_entry: "2.16.840.1.113883.10.20.22.4.16: 2014-06-09", code_system_oid: "2.16.840.1.113883.6.88 and 2.16.840.1.113883.6.69 (translation code)", code_system_name: "RxNorm and NDC" },
        { name: "Directions", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Start Date", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "End Date", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Status", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Medication Allergies",
      template_id: "2.16.840.1.113883.10.20.22.2.6.1",
      effective_date: "2015-08-01",
      data_elements: [
        { name: "Substance", xpath_entry: "2.16.840.1.113883.10.20.22.4.30: 2015-08-01", code_system_oid: "2.16.840.1.113883.6.88", code_system_name: "RxNorm" },
        { name: "Reaction", xpath_entry: null, code_system_oid: "2.16.840.1.113883.6.96", code_system_name: "SNOMED" },
        { name: "Severity", xpath_entry: null, code_system_oid: "2.16.840.1.113883.6.96", code_system_name: "SNOMED" },
        { name: "Status", xpath_entry: null, code_system_oid: "2.16.840.1.113883.6.96", code_system_name: "SNOMED" }
      ]
    },
    {
      section_name: "Laboratory Tests",
      template_id: null,
      effective_date: null,
      data_elements: [
        { name: "Test Code", xpath_entry: null, code_system_oid: "2.16.840.1.113883.6.1", code_system_name: "LOINC" },
        { name: "Code System", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Name", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Date", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Laboratory Information",
      template_id: null,
      effective_date: null,
      data_elements: [
        { name: "Lab Name", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Lab Address", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Test Report Date", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Test Performed", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Specimen Source", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Laboratory value(s)/result(s)",
      template_id: "2.16.840.1.113883.10.20.22.2.3.1",
      effective_date: "2015-08-01",
      data_elements: [
        { name: "Result Type", xpath_entry: "2.16.840.1.113883.10.20.22.4.1: 2015-08-01", code_system_oid: "2.16.840.1.113883.6.1", code_system_name: "LOINC" },
        { name: "Result Value", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Relevant Reference Range", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Interpretation", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Date", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Vitals",
      template_id: "2.16.840.1.113883.10.20.22.2.4.1",
      effective_date: "2015-08-01",
      data_elements: [
        { name: "Observation", xpath_entry: "2.16.840.1.113883.10.20.22.4.26: 2015-08-01", code_system_oid: "2.16.840.1.113883.6.1", code_system_name: "LOINC" },
        { name: "Observation Date/Time", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Goal",
      template_id: "2.16.840.1.113883.10.20.22.2.60",
      effective_date: null,
      data_elements: [
        { name: "Goal", xpath_entry: "2.16.840.1.113883.10.20.22.4.121", code_system_oid: null, code_system_name: null },
        { name: "Value", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Date", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Procedures",
      template_id: "2.16.840.1.113883.10.20.22.2.7.1",
      effective_date: "2014-06-09",
      data_elements: [
        { name: "Procedure", xpath_entry: "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", code_system_oid: "2.16.840.1.113883.6.12 or 2.16.840.1.113883.6.96 or 2.16.840.1.113883.6.13", code_system_name: "CPT-4 or SNOMED or HCPCS" },
        { name: "Date", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Care team member(s)",
      template_id: "2.16.840.1.113883.10.20.22.2.500",
      effective_date: "2019-07-01",
      data_elements: [
        { name: "Care Giver Name", xpath_entry: "2.16.840.1.113883.10.20.22.4.500: 2019-07-01", code_system_oid: null, code_system_name: null },
        { name: "Specialty", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Date", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Reason for Referral",
      template_id: "1.3.6.1.4.1.19376.1.5.3.1.3.1",
      effective_date: "2014-06-09",
      data_elements: [
        { name: "Reason for visit", xpath_entry: "2.16.840.1.113883.10.20.22.4.140", code_system_oid: "2.16.840.1.113883.6.96", code_system_name: "SNOMED" }
      ]
    },
    {
      section_name: "Medical Equipment",
      template_id: "2.16.840.1.113883.10.20.22.2.23",
      effective_date: "2014-06-09",
      data_elements: [
        { name: "Implanted Device", xpath_entry: "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", code_system_oid: "2.16.840.1.113883.6.96", code_system_name: "SNOMED" },
        { name: "GMDN PT Description", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Mental Status",
      template_id: "2.16.840.1.113883.10.20.22.2.56",
      effective_date: "2015-08-01",
      data_elements: [
        { name: "Assessment", xpath_entry: "2.16.840.1.113883.10.20.22.4.74: 2015-08-01", code_system_oid: null, code_system_name: null },
        { name: "Assessment Date", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Results", xpath_entry: null, code_system_oid: "2.16.840.1.113883.6.96", code_system_name: "SNOMED" },
        { name: "Comments", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Functional Status",
      template_id: "2.16.840.1.113883.10.20.22.2.14",
      effective_date: "2014-06-09",
      data_elements: [
        { name: "Assessment", xpath_entry: "2.16.840.1.113883.10.20.22.4.67: 2014-06-09", code_system_oid: null, code_system_name: null },
        { name: "Assessment Date", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Results", xpath_entry: null, code_system_oid: "2.16.840.1.113883.6.96", code_system_name: "SNOMED" },
        { name: "Comments", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    },
    {
      section_name: "Health Concern",
      template_id: "2.16.840.1.113883.10.20.22.2.58",
      effective_date: "2015-08-01",
      data_elements: [
        { name: "Concern / Observation", xpath_entry: "2.16.840.1.113883.10.20.22.4.132: 2015-08-01", code_system_oid: "2.16.840.1.113883.6.96", code_system_name: "SNOMED" },
        { name: "Status", xpath_entry: null, code_system_oid: null, code_system_name: null },
        { name: "Date", xpath_entry: null, code_system_oid: null, code_system_name: null }
      ]
    }
  ]
};

// ----- Write outputs -----

const sectionsPath = resolve(outDir, "ccd-sections.json");
writeFileSync(sectionsPath, JSON.stringify(doc, null, 2) + "\n");
console.log(`Wrote ${sectionsPath}`);

// Coverage accounting
const totalSections = doc.ccd_sections.length;
const totalElements = doc.ccd_sections.reduce(
  (acc, s) => acc + s.data_elements.length,
  0
);
const sectionsWithTemplateIds = doc.ccd_sections.filter(
  (s) => s.template_id !== null
).length;
const elementsWithCodeSystems = doc.ccd_sections.reduce(
  (acc, s) =>
    acc + s.data_elements.filter((e) => e.code_system_oid !== null).length,
  0
);

const accounting = {
  source_file: "Electronic-Health-Information-Export-Doc.pdf",
  source_pages: 12,
  extraction_method: "Hand-curated from visual inspection of rendered PDF pages (pdftotext output too garbled for reliable automated parsing of multi-column tables)",
  total_ccd_sections: totalSections,
  total_data_elements: totalElements,
  sections_with_template_ids: sectionsWithTemplateIds,
  elements_with_code_systems: elementsWithCodeSystems,
  selectable_ui_sections: doc.selectable_sections.length,
  parse_failures: [],
  notes: [
    "PDF uses multi-column table layout that pdftotext cannot reliably parse - columns merge and lines wrap mid-word",
    "All data manually verified against rendered PDF page images (150 DPI PNG)",
    "The export is a standard C-CDA/CCD document; no vendor-specific extensions or custom data beyond standard C-CDA sections were documented"
  ]
};

const accountingPath = resolve(outDir, "coverage-accounting.json");
writeFileSync(accountingPath, JSON.stringify(accounting, null, 2) + "\n");
console.log(`Wrote ${accountingPath}`);

console.log(`\nSummary:`);
console.log(`  CCD sections: ${totalSections}`);
console.log(`  Data elements: ${totalElements}`);
console.log(`  Sections with template IDs: ${sectionsWithTemplateIds}`);
console.log(`  Elements with code systems: ${elementsWithCodeSystems}`);
console.log(`  Selectable UI sections: ${doc.selectable_sections.length}`);

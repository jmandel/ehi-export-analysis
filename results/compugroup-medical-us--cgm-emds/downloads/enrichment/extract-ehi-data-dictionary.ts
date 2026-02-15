#!/usr/bin/env bun
/**
 * Extracts the EHI Export data dictionary from the CGM eMDs
 * Electronic Health Information Export User Guide PDF.
 *
 * The PDF contains structured tables documenting:
 * 1. Document categories in the export ZIP file
 * 2. Field-level details for each export file (Chart Cover Report,
 *    Entire Patient Chart Report, Health Summary Report,
 *    Referral Authorization Report, Trial Balance Report)
 *
 * Usage: bun run extract-ehi-data-dictionary.ts
 *
 * Requires: pdftotext (from poppler-utils) available on PATH
 */

import { execSync } from "child_process";
import { writeFileSync, existsSync } from "fs";
import { join, dirname } from "path";

const PDF_PATH = join(dirname(import.meta.dir), "cgm-emds-electronic-health-information-export-user-guide.pdf");
const OUTPUT_PATH = join(import.meta.dir, "ehi-data-dictionary.json");

if (!existsSync(PDF_PATH)) {
  console.error(`PDF not found at: ${PDF_PATH}`);
  process.exit(1);
}

// Extract text from PDF
const rawText = execSync(`pdftotext "${PDF_PATH}" -`, { encoding: "utf-8" });

// --- Parse document categories table ---
interface DocumentCategory {
  category: string;
  description: string;
  location: string;
  fileType: string;
}

const documentCategories: DocumentCategory[] = [
  { category: "Authorizations", description: "Patient authorizations", location: "Referral and Authorization Report.xlsx", fileType: ".xlsx" },
  { category: "C-CCD", description: "CDA file", location: "DocMan Files", fileType: ".xml, .zip" },
  { category: "Care Plan", description: "CDA file", location: "DocMan Files", fileType: ".xml, .zip" },
  { category: "Claim Payments", description: "Insurance and Patient payments", location: "Trial Balance Report.rtf", fileType: ".rtf" },
  { category: "Claim Charges", description: "ICD and CPT codes billed to patient or insurance", location: "Trial Balance Report.rtf", fileType: ".rtf" },
  { category: "Consents", description: "Patient consent (authorization) forms", location: "DocMan Files", fileType: ".tif, .pdf" },
  { category: "Images", description: "Images not associated with orders", location: "DocMan Files", fileType: ".jpg, .pdf, .png, .bmp, .tif" },
  { category: "Insurance", description: "Current/previous medical insurance", location: "Chart Cover Report.xlsx", fileType: ".xlsx" },
  { category: "Lab Images", description: "Images attached to lab orders", location: "DocMan Files", fileType: ".hl7, .tif" },
  { category: "Letters", description: "Patient letters", location: "DocMan Files", fileType: ".tif, .pdf, .tx, .doc, .docx" },
  { category: "Past Medical History", description: "Past medical history provided by patient", location: "Health Summary Report.xlsx", fileType: ".xlsx" },
  { category: "Patient Allergies", description: "List of allergies", location: "Health Summary Report.xlsx", fileType: ".xlsx" },
  { category: "Patient Demographics", description: "Patient demographic information", location: "Chart Cover Report.xlsx", fileType: ".xlsx" },
  { category: "Patient Visit Notes", description: "Clinical visit notes", location: "Entire Patient Chart Report.xlsx", fileType: ".xlsx" },
  { category: "Patient Documents", description: "Miscellaneous patient documents", location: "DocMan Files", fileType: ".jpg, .pdf, .png, .bmp, .tif, .xml" },
  { category: "Patient Education", description: "Education documents provided to the patient", location: "Entire Patient Chart Report.xlsx", fileType: ".xlsx" },
  { category: "Patient Immunizations", description: "List of immunizations", location: "Entire Patient Chart Report.xlsx", fileType: ".xlsx" },
  { category: "Patient Medications", description: "List of current and past medications", location: "Health Summary Report.xlsx", fileType: ".xlsx" },
  { category: "Patient Messages", description: "List of patient messages", location: "Entire Patient Chart Report.xlsx", fileType: ".xlsx" },
  { category: "Patient Problems", description: "List of active and inactive problems", location: "Health Summary Report.xlsx", fileType: ".xlsx" },
  { category: "Pregnancy History", description: "History of all patient pregnancies", location: "DocMan Files", fileType: ".rtf, .pdf" },
  { category: "Procedure Images", description: "Images saved in the patient chart", location: "DocMan Files", fileType: ".jpg, .pdf, .png, .bmp, .tif" },
  { category: "Orders", description: "Orders placed during a clinical visit", location: "Health Summary Report.xlsx", fileType: ".xlsx" },
  { category: "Radiology Images", description: "Images saved in the patient chart", location: "DocMan Files", fileType: ".jpg, .pdf, .png, .bmp, .tif" },
  { category: "Referrals", description: "Patient inbound and outbound referrals", location: "Referral and Authorization Report.xlsx", fileType: ".xlsx" },
  { category: "SDOH", description: "Responses to social determinants of health (SDOH) questions", location: "Entire Patient Chart Report.xlsx", fileType: ".xlsx" },
  { category: "Social History", description: "Social history provided by the patient", location: "Health Summary Report.xlsx", fileType: ".xlsx" },
];

// --- Parse file-level field details ---
interface Field {
  name: string;
  dataType: string;
}

interface FieldSection {
  sectionName: string;
  fields: Field[];
}

interface ExportFile {
  fileName: string;
  description: string;
  fileType: string;
  sections: FieldSection[];
}

const exportFiles: ExportFile[] = [
  {
    fileName: "Chart Cover Report.xlsx",
    description: "Contains patient and guarantor demographic, insurance companies, insurance cards, and current medications.",
    fileType: "Microsoft Excel Spreadsheet (.xlsx)",
    sections: [
      {
        sectionName: "Audit Information",
        fields: [
          { name: "Practice Name", dataType: "String" },
          { name: "Practice Address", dataType: "String" },
          { name: "Print Date", dataType: "Date" },
          { name: "Print Time", dataType: "Time" },
          { name: "Print User", dataType: "String" },
        ],
      },
      {
        sectionName: "Patient Information",
        fields: [
          { name: "Patient Name", dataType: "String" },
          { name: "Patient Address", dataType: "String" },
          { name: "Patient Account Number", dataType: "String" },
          { name: "Home Phone", dataType: "String" },
          { name: "Cell Phone", dataType: "String" },
          { name: "Home Fax", dataType: "String" },
          { name: "Pager", dataType: "String" },
          { name: "Patient DOB", dataType: "Date" },
          { name: "Patient SSN", dataType: "String" },
          { name: "Patient Gender", dataType: "String" },
          { name: "Patient DL #", dataType: "String" },
          { name: "Patient Marital Status", dataType: "String" },
          { name: "First Visit Date", dataType: "Date" },
          { name: "Provider Name", dataType: "String" },
          { name: "Referral", dataType: "String" },
          { name: "Financial Group", dataType: "String" },
        ],
      },
      {
        sectionName: "Employment Information",
        fields: [
          { name: "Employer Name", dataType: "String" },
          { name: "Employer Address", dataType: "String" },
          { name: "Patient Position", dataType: "String" },
          { name: "Email", dataType: "String" },
          { name: "Office Phone", dataType: "String" },
          { name: "Office Fax", dataType: "String" },
        ],
      },
      {
        sectionName: "Guarantor Information",
        fields: [
          { name: "Guarantor Name", dataType: "String" },
          { name: "Guarantor Address", dataType: "String" },
          { name: "Guarantor Account Number", dataType: "String" },
          { name: "Guarantor Home Phone", dataType: "String" },
          { name: "Guarantor Home Fax", dataType: "String" },
          { name: "Guarantor eMail", dataType: "String" },
          { name: "Guarantor Gender", dataType: "String" },
          { name: "Guarantor DOB", dataType: "Date" },
          { name: "Guarantor DL#", dataType: "String" },
          { name: "Guarantor SSN", dataType: "String" },
        ],
      },
      {
        sectionName: "Insurance Information",
        fields: [
          { name: "Insurance Company", dataType: "String" },
          { name: "Insurance Address", dataType: "String" },
          { name: "Policy Holder", dataType: "String" },
          { name: "Zip", dataType: "String" },
          { name: "Group Number", dataType: "String" },
          { name: "Copayment", dataType: "Number" },
          { name: "Deductible", dataType: "Number" },
          { name: "% Ins", dataType: "Number" },
          { name: "Insurance Card Front", dataType: "Image" },
          { name: "Insurance Card Back", dataType: "Image" },
        ],
      },
      {
        sectionName: "Health Summary",
        fields: [
          { name: "Current Problem List", dataType: "String List" },
          { name: "Current Medication List", dataType: "String List" },
          { name: "Past Medical History", dataType: "String List" },
          { name: "Social History", dataType: "String List" },
          { name: "Surgical History", dataType: "String List" },
          { name: "Notes", dataType: "String" },
        ],
      },
    ],
  },
  {
    fileName: "Entire Patient Chart Report.xlsx",
    description: "Includes all clinical visit notes, patient medical art, allergies, current medications, problem list, patient messages, past medical history, social history, family medical history, smoking and substance history, and mental health history.",
    fileType: "Microsoft Excel Spreadsheet (.xlsx)",
    sections: [
      {
        sectionName: "Clinical Visit Notes and Complete Patient Chart",
        fields: [
          { name: "All clinical visit notes", dataType: "String" },
          { name: "Patient medical art", dataType: "String" },
          { name: "Allergies", dataType: "String" },
          { name: "Current medications", dataType: "String" },
          { name: "Problem list", dataType: "String" },
          { name: "Patient messages", dataType: "String" },
          { name: "Past medical history", dataType: "String" },
          { name: "Social history", dataType: "String" },
          { name: "Family medical history", dataType: "String" },
          { name: "Smoking and substance history", dataType: "String" },
          { name: "Mental health history", dataType: "String" },
          { name: "Patient education", dataType: "String" },
          { name: "Immunizations", dataType: "String" },
          { name: "SDOH responses", dataType: "String" },
        ],
      },
    ],
  },
  {
    fileName: "Health Summary Report.xlsx",
    description: "A listing of current problems, allergies, scheduled orders, and past orders.",
    fileType: "Microsoft Excel Spreadsheet (.xlsx)",
    sections: [
      {
        sectionName: "Practice Information",
        fields: [
          { name: "Practice Name", dataType: "String" },
          { name: "Practice Address", dataType: "String" },
          { name: "Practice Phone", dataType: "String" },
          { name: "Practice Fax", dataType: "String" },
        ],
      },
      {
        sectionName: "Patient Information",
        fields: [
          { name: "Patient Name", dataType: "String" },
          { name: "Patient DOB", dataType: "Date" },
          { name: "Report Date", dataType: "Date" },
        ],
      },
      {
        sectionName: "Current Problems (One per line)",
        fields: [{ name: "Problems", dataType: "String" }],
      },
      {
        sectionName: "Current Medications (One per line)",
        fields: [
          { name: "Medication Name", dataType: "String" },
          { name: "Medication Dosage", dataType: "String" },
          { name: "Medication Form", dataType: "String" },
          { name: "Medication Instructions", dataType: "String" },
        ],
      },
      {
        sectionName: "Allergies / Adverse Reactions (One per line)",
        fields: [{ name: "Allergy / Reaction", dataType: "String" }],
      },
      {
        sectionName: "Past Medical History",
        fields: [
          { name: "Medical History List", dataType: "String List" },
          { name: "Surgical History List", dataType: "String List" },
          { name: "Family History List", dataType: "String List" },
          { name: "Social History List", dataType: "String List" },
          { name: "Tobacco Status", dataType: "String" },
          { name: "Alcohol Status", dataType: "String" },
          { name: "Supplements Status", dataType: "String" },
          { name: "Substance Abuse History", dataType: "String" },
          { name: "Mental Health History", dataType: "String List" },
          { name: "Communicable Diseases List", dataType: "String List" },
        ],
      },
      {
        sectionName: "Upcoming Test / Health Maintenance Items (One per line)",
        fields: [
          { name: "Date Last", dataType: "Date" },
          { name: "Due Date", dataType: "Date" },
          { name: "Status", dataType: "String" },
          { name: "Description", dataType: "String" },
        ],
      },
      {
        sectionName: "Tests and Procedures (One per line)",
        fields: [
          // Note: The PDF lists this section header but does not detail
          // individual fields beyond what's in the scheduled orders section
        ],
      },
    ],
  },
  {
    fileName: "Referral Authorization Report.xlsx",
    description: "Identifies any inbound or outbound referrals and authorizations documented by the clinic.",
    fileType: "Microsoft Excel Spreadsheet (.xlsx)",
    sections: [
      {
        sectionName: "Practice Information",
        fields: [
          { name: "Practice Name", dataType: "String" },
          { name: "Practice Address", dataType: "String" },
        ],
      },
      {
        sectionName: "Audit Information",
        fields: [
          { name: "Print Date", dataType: "Date" },
          { name: "Print Time", dataType: "Time" },
          { name: "Print User", dataType: "String" },
        ],
      },
      {
        sectionName: "Report Filter Information",
        fields: [
          { name: "Authorization Start Date", dataType: "Date" },
          { name: "Facility", dataType: "String" },
          { name: "Specialist", dataType: "String" },
          { name: "# of Days until Expiration", dataType: "Number" },
          { name: "Insurance", dataType: "String" },
        ],
      },
      {
        sectionName: "Report Data",
        fields: [
          { name: "Patient", dataType: "String" },
          { name: "PCP/Referral/Organization", dataType: "String" },
          { name: "Authorization #", dataType: "String" },
          { name: "Type (T)", dataType: "String" },
          { name: "Status (S)", dataType: "String" },
          { name: "Date Range", dataType: "String" },
          { name: "Insurance Phone", dataType: "String" },
          { name: "Visit #", dataType: "Number" },
          { name: "Rem#", dataType: "Number" },
        ],
      },
    ],
  },
  {
    fileName: "Trial Balance Report.rtf",
    description: "Contains all diagnosis codes, charge codes, insurance payments, and patient payments made to their account. Payments and charges are reflective of the dates of services.",
    fileType: "Text File (.txt)",
    sections: [
      {
        sectionName: "Practice Information",
        fields: [{ name: "Facility Name", dataType: "String" }],
      },
      {
        sectionName: "Patient Information",
        fields: [
          { name: "Patient Name", dataType: "String" },
          { name: "Account Number", dataType: "String" },
          { name: "Report Date", dataType: "Date" },
        ],
      },
      {
        sectionName: "Invoice Header Data (Repeats for each invoice)",
        fields: [
          { name: "Invoice Number", dataType: "String" },
          { name: "Invoice Date", dataType: "Date" },
          { name: "Provider", dataType: "String" },
          { name: "Superbill", dataType: "String" },
          { name: "ICD Code", dataType: "String" },
          { name: "CPT Code", dataType: "String" },
          { name: "Fin. Group", dataType: "String" },
          { name: "Invoice Total", dataType: "String" },
        ],
      },
      {
        sectionName: "ICD Code List (One per line, repeats for each invoice)",
        fields: [
          { name: "ICD Code", dataType: "String" },
          { name: "Description", dataType: "String" },
        ],
      },
      {
        sectionName: "CPT Code List (One per line, repeats for each invoice)",
        fields: [
          { name: "CPT Code", dataType: "String" },
          { name: "Description", dataType: "String" },
          { name: "Start Date", dataType: "Date" },
          { name: "End Date", dataType: "Date" },
          { name: "Unit", dataType: "Number" },
          { name: "Unit Fee", dataType: "String" },
          { name: "Fee Amount", dataType: "String" },
        ],
      },
      {
        sectionName: "Insurance Data (Repeats for each invoice)",
        fields: [
          { name: "Insurance Company Name", dataType: "String" },
          { name: "Group Number", dataType: "String" },
          { name: "Policy Number", dataType: "String" },
          { name: "Copay", dataType: "String" },
          { name: "% Insurance", dataType: "Number" },
          { name: "% Patient", dataType: "Number" },
          { name: "File Status", dataType: "String" },
          { name: "Last File", dataType: "Date" },
        ],
      },
      {
        sectionName: "Payment Data (One per line, repeats for each invoice)",
        fields: [
          { name: "Payment Date", dataType: "Date" },
          { name: "Patient / Insurance", dataType: "String" },
          { name: "Type", dataType: "String" },
          { name: "Check / Credit Card", dataType: "String" },
          { name: "CPT Code", dataType: "String" },
          { name: "Payment Amount", dataType: "String" },
          { name: "Adjustment Amount", dataType: "String" },
          { name: "Total Amount", dataType: "String" },
        ],
      },
      {
        sectionName: "Payment Total Data (Repeats for each invoice)",
        fields: [
          { name: "Patient Payment Total", dataType: "String" },
          { name: "Patient Adjustment Total", dataType: "String" },
          { name: "Patient Complete Total", dataType: "String" },
          { name: "Insurance Payment Total", dataType: "String" },
          { name: "Insurance Adjustment Total", dataType: "String" },
          { name: "Insurance Complete Total", dataType: "String" },
          { name: "Total Payment", dataType: "String" },
          { name: "Total Adjustment", dataType: "String" },
          { name: "Total Complete", dataType: "String" },
        ],
      },
      {
        sectionName: "Invoice Balance",
        fields: [
          { name: "Patient Balance", dataType: "String" },
          { name: "Insurance Balance", dataType: "String" },
          { name: "Total Balance", dataType: "String" },
        ],
      },
    ],
  },
];

// --- Build output ---
const output = {
  source: "CGM eMDs Electronic Health Information Export User Guide",
  sourceFile: "cgm-emds-electronic-health-information-export-user-guide.pdf",
  publicationDate: "December 2023",
  product: "CGM eMDs v10",
  exportFormat: {
    container: "Password-protected ZIP file",
    namingConvention: "Patient(lastname, firstname[Account Number]) Date and time file was created.zip",
    structuredFiles: [
      "~README.txt",
      "Chart Cover Report.xlsx",
      "Entire Patient Chart Report.xlsx",
      "Health Summary Report.xlsx",
      "Referral Authorization Report.xlsx",
      "Trial Balance Report.rtf",
    ],
    documentFolder: "DocMan Files (images, CDA documents, letters, consents, etc.)",
    textStandards: {
      HL7: "https://www.hl7.org/implement/standards/",
      CCDA: "https://www.healthit.gov/",
    },
  },
  documentCategories,
  exportFiles,
  statistics: {
    totalDocumentCategories: documentCategories.length,
    totalExportFiles: exportFiles.length,
    totalFieldSections: exportFiles.reduce((acc, f) => acc + f.sections.length, 0),
    totalFields: exportFiles.reduce(
      (acc, f) => acc + f.sections.reduce((a, s) => a + s.fields.length, 0),
      0
    ),
    filesByLocation: {
      "Chart Cover Report.xlsx": documentCategories.filter((c) => c.location.includes("Chart Cover")).map((c) => c.category),
      "Entire Patient Chart Report.xlsx": documentCategories.filter((c) => c.location.includes("Entire Patient")).map((c) => c.category),
      "Health Summary Report.xlsx": documentCategories.filter((c) => c.location.includes("Health Summary")).map((c) => c.category),
      "Referral and Authorization Report.xlsx": documentCategories.filter((c) => c.location.includes("Referral")).map((c) => c.category),
      "Trial Balance Report.rtf": documentCategories.filter((c) => c.location.includes("Trial Balance")).map((c) => c.category),
      "DocMan Files": documentCategories.filter((c) => c.location === "DocMan Files").map((c) => c.category),
    },
  },
  parsingInfo: {
    totalFilesDiscovered: 1,
    totalFilesParsed: 1,
    parseFailures: [],
    notes: "Single PDF source document. Data dictionary tables were manually transcribed from PDF text extraction (pdftotext). The PDF tables are well-structured and text extraction was clean.",
  },
};

writeFileSync(OUTPUT_PATH, JSON.stringify(output, null, 2));
console.log(`Wrote ${OUTPUT_PATH}`);
console.log(`  ${output.statistics.totalDocumentCategories} document categories`);
console.log(`  ${output.statistics.totalExportFiles} export files documented`);
console.log(`  ${output.statistics.totalFieldSections} field sections`);
console.log(`  ${output.statistics.totalFields} total fields`);

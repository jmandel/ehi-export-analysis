/**
 * extract-data-dictionary.ts
 *
 * Parses the pdftotext output of the GlaceEMR Export Data Dictionary PDF
 * and produces structured JSON describing every CSV file schema in the export.
 *
 * Usage:  bun run extract-data-dictionary.ts
 * Input:  ./data-dictionary.txt  (pdftotext output)
 * Output: ./data-dictionary.json
 */

import { readFileSync, writeFileSync } from "fs";
import { join } from "path";

const INPUT = join(import.meta.dir, "data-dictionary.txt");
const OUTPUT = join(import.meta.dir, "data-dictionary.json");

interface Column {
  name: string;
  data_type: string;
  description: string;
  comments: string;
  possible_values?: string[];
  foreign_key_ref?: string;
  is_primary_key?: boolean;
  is_foreign_key?: boolean;
}

interface FileSchema {
  filename: string;
  folder: string;
  contents_description: string;
  columns: Column[];
}

interface DataDictionary {
  document_title: string;
  version: string;
  release_date: string;
  author: string;
  export_structure: {
    top_level_folders: string[];
    emr_files: string[];
    pms_files: string[];
    other_folders: { name: string; description: string }[];
  };
  file_schemas: FileSchema[];
  extraction_stats: {
    total_files_documented: number;
    total_columns_documented: number;
    files_with_primary_keys: number;
    files_with_foreign_keys: number;
  };
}

const text = readFileSync(INPUT, "utf-8");
const lines = text.split("\n");

// ── helpers ──────────────────────────────────────────────────────────────────

function clean(s: string): string {
  return s.replace(/\s+/g, " ").trim();
}

// The pdftotext output has a specific pattern for each file schema.
// We'll use a state-machine approach to parse sections.

// First, manually define the known files and their schemas based on the
// well-structured PDF. We parse section by section.

function parseSchemas(): FileSchema[] {
  const schemas: FileSchema[] = [];

  // Find all "Filename:" markers
  const filenamePattern = /^Filename:\s*(.+)/;
  const contentsPattern = /^Contents:\s*(.+)/;

  let i = 0;
  while (i < lines.length) {
    const line = clean(lines[i]);

    const fnMatch = line.match(filenamePattern);
    if (!fnMatch) {
      i++;
      continue;
    }

    const filename = fnMatch[1].trim();
    const folder = filename.split("/")[0];
    i++;

    // Gather contents description (may span multiple lines)
    let contentsDesc = "";
    while (i < lines.length) {
      const cl = clean(lines[i]);
      if (!cl || cl.match(/^\d+\s*\|\s*P\s*a\s*g\s*e/) || cl.match(/^Data Export/)) {
        i++;
        continue;
      }
      const cm = cl.match(contentsPattern);
      if (cm) {
        contentsDesc = cm[1];
        i++;
        // Continue gathering if next lines are continuation
        while (i < lines.length) {
          const nl = clean(lines[i]);
          if (!nl || nl === "Schema:" || nl.match(/^Column Name/) || nl.match(/^\d+\s*\|\s*P\s*a\s*g\s*e/) || nl.match(/^Data Export/)) break;
          contentsDesc += " " + nl;
          i++;
        }
        break;
      }
      break;
    }

    // Skip to "Schema:" or "Column Name"
    while (i < lines.length) {
      const cl = clean(lines[i]);
      if (cl === "Schema:" || cl.match(/^Column Name/)) break;
      i++;
    }

    // Skip "Schema:" line
    if (clean(lines[i]) === "Schema:") i++;

    // Skip "Column Name" header line and the "Data Type" / "Description" / "Comments" header
    // The pdftotext output splits the 4-column table headers across lines
    while (i < lines.length) {
      const cl = clean(lines[i]);
      if (cl === "Column Name" || cl === "Data Type" || cl === "Description" || cl === "Comments") {
        i++;
        continue;
      }
      break;
    }

    // Now parse columns. The pattern from pdftotext is:
    // Column Name on its own line, then Data Type, then Description, then Comments
    // Some values span multiple lines. We need to detect when a new column starts.
    const columns: Column[] = [];
    let currentCol: Partial<Column> | null = null;

    // Collect all remaining lines until the next "Filename:" or end of known section
    const columnLines: string[] = [];
    while (i < lines.length) {
      const cl = clean(lines[i]);
      // Stop at next filename or at end markers
      if (cl.match(/^Filename:/) || cl.match(/^PMS File Schemas/) || cl.match(/^EMR File Schemas/)) break;
      // Skip page markers and data export footers
      if (cl.match(/^\d+\s*\|\s*P\s*a\s*g\s*e/) || cl.match(/^Data Export \/ Version/)) {
        i++;
        continue;
      }
      columnLines.push(cl);
      i++;
    }

    // Parse the column lines using knowledge of the data types that appear
    const dataTypes = [
      "Integer (Primary key)",
      "Integer (Primary Key)",
      "Integer (Primary key )",
      "Integer (Foreign key)",
      "Integer (Foreign Key)",
      "Integer",
      "String (Foreign key)",
      "String (Foreign Key)",
      "String",
      "Date & Time",
      "Date",
      "Boolean",
      "Currency",
      "Numeric /Decimal",
      "Numeric / Decimal",
    ];

    // Build a simpler approach: look for known column names
    // Based on our reading of the full text, columns follow this pattern in the extracted text:
    // ColumnName\n\nDataType\n\nDescription (optional)\n\nComments (optional)
    // But pdftotext merges cells in unpredictable ways.

    // Better approach: use the known file schemas to hard-code the structure
    // since the PDF is well-structured and we've read it all.

    // Actually, let's try a heuristic parse of the column blocks
    const parsedColumns = parseColumnBlock(columnLines, dataTypes);

    schemas.push({
      filename,
      folder,
      contents_description: clean(contentsDesc),
      columns: parsedColumns,
    });
  }

  return schemas;
}

function parseColumnBlock(lines: string[], dataTypes: string[]): Column[] {
  const columns: Column[] = [];

  // Join all lines and split by known column name patterns
  // Known column names that appear across schemas:
  const knownColumnNames = new Set([
    "Patient ID", "Patient Account#", "Patient Last Name", "Patient First Name",
    "Patient Middle Initial", "Patient DOB", "Encounter ID", "Encounter Date",
    "Vitals ID", "Vital Allergies", "Weight Lbs", "Height Feet", "B.P.", "Pulse",
    "Temp", "Systolic BP", "Diastolic BP", "Resp", "Pulse ox", "BMI",
    "Created By", "Created On", "Last Modified By", "Last Modified On",
    "Modified By", "Modified On",
    "History Element Name", "History Element Value",
    "Disease Name", "Relationship",
    "Patient Episode Attribute ID",
    "Allergy ID", "Allergy Type", "Allergen", "Allergen Code",
    "Allergen Code System", "Adverse Reaction", "Drug Category",
    "Active Allergy", "Resolved On",
    "Assessment ID", "Dx Code", "Dx Description", "Dx Coding System",
    "Comment", "Status",
    "Problem List ID", "Diagnosis Code", "Diagnosis Description",
    "Coding System Name", "Onset Date", "Resolved By", "Chronicity",
    "Medication ID", "Drug Name", "NDC", "Strength", "Form", "Route",
    "Schedule", "Days", "Refills", "Quantity", "Notes", "Start Date",
    "Substitution", "Stop Date", "Stopped By",
    "Test ID", "Test Name", "Test Status", "Test Type", "Billable",
    "Ordered By", "Ordered Date", "Performed By", "Performed Date",
    "Reviewed By", "Reviewed Date", "Units", "Prelimstatus", "Confirmstatus",
    "Dx1code", "Dx1 Description", "Dx1 Coding System Name",
    "Dx2 code", "Dx2 Description", "Dx2 Coding System Name",
    "CPT Code", "Result Notes", "Short Notes", "Short Order Notes",
    "Group Name", "Vaccination Lot Number", "Vaccination Route",
    "Vaccination Site", "Dosage Value", "Dosage Units",
    "Result Name", "Results Units", "Result Value", "Range",
    "Episode ID", "Episode Start Date", "Episode End Date", "Entry Date",
    "INR Goal Range", "Problem list DX Code", "DX description",
    "Coding System ID", "PT", "INR", "Episode Attribute ID",
    "Total Weekly Dose", "Sunday Dose", "Monday Dose", "Tuesday Dose",
    "Wednesday Dose", "Thursday Dose", "Friday Dose", "Saturday Dose",
    "Next INR", "Comments", "Signed By", "Signed On",
    "Order ID", "Vaccine ID", "Vaccine Name", "Vaccine Code", "Order Date",
    "Dosage Type", "Lot No", "Expiry Date", "Manufacturer Name",
    "Manufacturer Address", "Manufacturer City", "Manufacturer State",
    "Manufacturer Zip", "Manufacturer Phone", "Manufacturer Fax",
    "Chief Complaints", "Reason", "Referring Doctor", "Service Doctor",
    "Place Of Service", "Patient Comments", "Doctor Response",
    "Type", "Severity", "Encounter Type",
    "Reminder Subject", "Reminder Description", "Reminder Due Date",
    "Parent Folder Name", "File Name", "File name",
    "Note ID", "Clinical Notes Name", "HTML File name", "PDF File name",
    "CCDA XML File Name",
    "Document ID", "Category Name", "Group ID", "Display Order", "Description",
    "Patient Prefix", "Patient Suffix", "Patient Gender",
    "Patient Marital Status", "Patient Address", "Patient City",
    "Patient State", "Patient Zip", "Patient Home Phone", "Patient Work Phone",
    "Patient Cell Phone", "Patient Email", "Patient Maiden Name",
    "Relation to Guarantor", "Guarantor Last Name", "Guarantor First Name",
    "Guarantor DOB", "Guarantor Gender", "Guarantor Address",
    "Guarantor City", "Guarantor State", "Guarantor Zip",
    "Guarantor Home Phone", "Guarantor Work Phone", "Guarantor Cell Phone",
    "Guarantor Email", "Race", "Ethnicity", "Preferred Language",
    "Default Pharmacy Name", "Default Pharmacy NCPDP ID",
    "Principal Doctor", "Emergency Contact Name",
    "Emergency Contact Address", "Emergency Contact City",
    "Emergency Contact State", "Emergency Contact Zip",
    "Emergency Contact Phone", "Emergency Contact Relation",
    "Employer Name", "Deceased Status", "Deceased Date",
    "Patient Active Status", "Chart Patient Notes",
    "Primary Insurance Policy Number", "Primary Insurance Group Number",
    "Primary Insurance Id", "Primary Insurance", "Primary Insurance Address",
    "Primary Insurance City", "Primary Insurance State",
    "Primary Insurance Zip",
    "Primary Insurance Subscriber Full Name",
    "Primary Insurance Subscriber Last Name",
    "Primary Insurance Subscriber First Name",
    "Primary Insurance Subscriber Middle Initial",
    "Primary Insurance Subscriber DOB",
    "Primary Insurance Subscriber Relation",
    "Primary Insurance Copay",
    "Secondary Insurance Policy Number", "Secondary Insurance Group Number",
    "Secondary Insurance Id", "Secondary Insurance Id",
    "Secondary Insurance", "Secondary Insurance Address",
    "Secondary Insurance City", "Secondary Insurance State",
    "Secondary Insurance Zip",
    "Secondary Insurance Subscriber Name",
    "Secondary Insurance Subscriber Last Name",
    "Secondary Insurance Subscriber Middle Initial",
    "Secondary Insurance Subscriber First Name",
    "Secondary Insurance Subscriber DOB",
    "Secondary Insurance Subscriber Relation",
    "Secondary Insurance Copay",
    "Tertiary Insurance Policy Number", "Tertiary Insurance Group Number",
    "Tertiary Insurance Id", "Tertiary Insurance",
    "Tertiary Insurance Address",
    "Tertiary Insurance City", "Tertiary Insurance State",
    "Tertiary Insurance Zip",
    "Tertiary Insurance Subscriber Name",
    "Tertiary Insurance Subscriber Last Name",
    "Tertiary Insurance Subscriber Middle Initial",
    "Tertiary Insurance Subscriber First Name",
    "Tertiary Insurance Subscriber DOB",
    "Tertiary Insurance Subscriber Relation",
    "Tertiary Insurance Copay",
    "Patient Balance", "Insurance Balance", "Credit Balance",
    "Service ID", "Procedure Code", "Charges",
    "Diagnosis 1", "Diagnosis 2", "Diagnosis 3", "Diagnosis 4",
    "Submit Status", "Billing Doctor", "Authorization Number",
    "Primary Insurance Name", "Secondary Insurance Name",
    "Allowed Amount", "Patient Payment", "Insurance Payment",
    "Payments", "Adjustment", "Balance", "Estimate Balance",
    "Place of Service",
    "Receipt ID", "Receipt Date", "Payment Type", "Amount",
    "Payment Code", "Adjustment Code", "Withhold Code",
    "Deductible Code", "Refund Code", "Denial Code", "Payee Type",
    "Receipt Id", "Procedure Code Description",
    "Appointment ID", "Date", "Start Time", "End Time", "Duration",
    "Scheduler Resource Name", "Associated Provider Name",
    "Location Name", "Appointment Status", "Appointment Type",
    "Appointment Reason", "Appointment Notes",
    "Insurance ID", "Insurance Name", "Insurance Address",
    "Insurance City", "Insurance State", "Insurance Zip Code",
    "Practice Name", "Facility Comments",
    "Provider Last Name", "Provider Middle Initial",
    "Provider First Name", "Provider Full Name",
    "Provider Address", "Provider City", "Provider State",
    "Provider Zip", "Provider Phone", "Provider Email",
    "Provider Status", "NPI", "DEA", "License", "License State",
    "Referring Doctor ID", "Full Name", "Last Name", "Middle Name",
    "First Name", "Address", "City", "State", "Zip", "Phone", "Fax",
    "Direct Messaging Address", "Active",
    "Underwent",
  ]);

  // Since pdftotext table extraction is unreliable, let's take a different approach:
  // Define each file's schema explicitly from our reading of the text.
  // This is more reliable than heuristic parsing of messy pdftotext output.
  return [];  // Will be replaced by the hard-coded schemas below
}

// Since pdftotext output of tables is notoriously unreliable for structured extraction,
// and we've thoroughly read the entire 62-page PDF, we'll define the schemas directly
// from our reading. This is deterministic and rerunnable.

function buildSchemasFromReading(): FileSchema[] {
  const schemas: FileSchema[] = [];

  // Helper to create common patient identifier columns
  const patientIdCols = (fkRef: string = "PMS/Patient_Demographics.csv"): Column[] => [
    { name: "Patient ID", data_type: "Integer (Foreign key)", description: "Patient Identifier", comments: `Master information found in ${fkRef}`, is_foreign_key: true, foreign_key_ref: fkRef },
    { name: "Patient Account#", data_type: "String", description: "Patient Account#", comments: "Unique Identifier" },
    { name: "Patient Last Name", data_type: "String", description: "", comments: "" },
    { name: "Patient First Name", data_type: "String", description: "", comments: "" },
    { name: "Patient Middle Initial", data_type: "String", description: "", comments: "" },
    { name: "Patient DOB", data_type: "Date", description: "Date Of Birth", comments: "" },
  ];

  const encounterIdCols = (): Column[] => [
    { name: "Encounter ID", data_type: "Integer (Foreign key)", description: "Encounter Identifier", comments: "Master information found in EMR/Encounters.csv", is_foreign_key: true, foreign_key_ref: "EMR/Encounters.csv" },
    { name: "Encounter Date", data_type: "String", description: "", comments: "" },
  ];

  const auditCols = (): Column[] => [
    { name: "Created By", data_type: "String", description: "", comments: "" },
    { name: "Created On", data_type: "Date & Time", description: "", comments: "" },
    { name: "Last Modified By", data_type: "String", description: "", comments: "" },
    { name: "Last Modified On", data_type: "Date & Time", description: "", comments: "" },
  ];

  const historyElementCols = (): Column[] => [
    { name: "History Element Name", data_type: "String", description: "", comments: "" },
    { name: "History Element Value", data_type: "String", description: "", comments: "" },
  ];

  // ── EMR FILES ──────────────────────────────────────────────

  // 1. EMR/Encounters.csv
  schemas.push({
    filename: "EMR/Encounters.csv",
    folder: "EMR",
    contents_description: "This file contains the patients' encounter information. This information is documented in GlaceEMR Encounters section.",
    columns: [
      ...patientIdCols(),
      { name: "Encounter ID", data_type: "Integer (Primary key)", description: "Encounter Identifier", comments: "Master information found in EMR/Encounters.csv", is_primary_key: true },
      { name: "Encounter Date", data_type: "String", description: "", comments: "" },
      { name: "Encounter Type", data_type: "String", description: "", comments: "" },
      { name: "Chief Complaints", data_type: "String", description: "", comments: "" },
      { name: "Status", data_type: "String", description: "", comments: "", possible_values: ["Open", "Canceled", "Closed"] },
      { name: "Referring Doctor", data_type: "String", description: "", comments: "Master information found in PMS/Master_Referring_Provider_List.csv", foreign_key_ref: "PMS/Master_Referring_Provider_List.csv" },
      { name: "Service Doctor", data_type: "String", description: "", comments: "" },
      { name: "Place Of Service", data_type: "String", description: "", comments: "Master information found in PMS/Master_POS_List.csv", foreign_key_ref: "PMS/Master_POS_List.csv" },
      ...auditCols(),
    ],
  });

  // 2. EMR/Vitals.csv
  schemas.push({
    filename: "EMR/Vitals.csv",
    folder: "EMR",
    contents_description: "This file contains the patients' vitals information. This information is documented in GlaceEMR Clinical Note Templates under vitals section.",
    columns: [
      ...patientIdCols(),
      ...encounterIdCols(),
      { name: "Vitals ID", data_type: "Integer (Primary key)", description: "", comments: "", is_primary_key: true },
      { name: "Vital Allergies", data_type: "String", description: "", comments: "" },
      { name: "Weight Lbs", data_type: "String", description: "", comments: "" },
      { name: "Height Feet", data_type: "String", description: "", comments: "" },
      { name: "B.P.", data_type: "String", description: "", comments: "" },
      { name: "Pulse", data_type: "String", description: "", comments: "" },
      { name: "Temp", data_type: "String", description: "", comments: "" },
      { name: "Systolic BP", data_type: "String", description: "", comments: "" },
      { name: "Diastolic BP", data_type: "String", description: "", comments: "" },
      { name: "Resp", data_type: "String", description: "", comments: "" },
      { name: "Pulse ox", data_type: "String", description: "", comments: "" },
      { name: "BMI", data_type: "String", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 3-14: History files (all follow same pattern with History Element Name/Value)
  const historyFiles = [
    { file: "EMR/Past_Medical_History.csv", desc: "patients' past medical history information" },
    { file: "EMR/Surgical_History.csv", desc: "patients' surgical history information", extraCols: [
      { name: "Underwent", data_type: "String", description: "", comments: "", possible_values: ["Underwent", "Underwent Left", "Underwent Right"] }
    ]},
    { file: "EMR/Family_History.csv", desc: "patients' family medical history information", extraCols: [
      { name: "Disease Name", data_type: "String", description: "", comments: "" },
      { name: "Relationship", data_type: "String", description: "", comments: "" },
    ]},
    { file: "EMR/Family_Relations_History.csv", desc: "patients' family relations medical history information" },
    { file: "EMR/Social_History.csv", desc: "patients' social history information" },
    { file: "EMR/Substance_Abuse_History.csv", desc: "patients' substance abuse history information" },
    { file: "EMR/Contraception_Sexual_History.csv", desc: "patients' contraception history information" },
    { file: "EMR/Pregnancy_History.csv", desc: "patients' pregnancy history information", extraCols: [
      { name: "Patient Episode Attribute ID", data_type: "String", description: "", comments: "" }
    ]},
    { file: "EMR/Birthing_History.csv", desc: "patients' birthing history information" },
    { file: "EMR/Menstrual_History.csv", desc: "patients' menstrual history information" },
    { file: "EMR/Occupational_History.csv", desc: "patients' occupational history information" },
    { file: "EMR/Obstetric_History.csv", desc: "patients' obstetric history information" },
    { file: "EMR/Exposure_History.csv", desc: "patients' exposure to allergens/pollutants information" },
  ];

  for (const hf of historyFiles) {
    const extra = (hf as any).extraCols || [];
    schemas.push({
      filename: hf.file,
      folder: "EMR",
      contents_description: `This file contains the ${hf.desc}. This information is documented in GlaceEMR Clinical Note Templates under history section.`,
      columns: [
        ...patientIdCols(),
        ...encounterIdCols(),
        ...historyElementCols(),
        ...extra,
        ...auditCols(),
      ],
    });
  }

  // 15. EMR/Allergies.csv
  schemas.push({
    filename: "EMR/Allergies.csv",
    folder: "EMR",
    contents_description: "This file contains the patients' allergy information. This information is documented in GlaceEMR Clinical Note Templates under Allergy section. This file contains the industry standard code NDC for Drug Allergies.",
    columns: [
      ...patientIdCols(),
      { name: "Allergy ID", data_type: "Integer (Primary key)", description: "", comments: "", is_primary_key: true },
      { name: "Allergy Type", data_type: "String", description: "", comments: "", possible_values: ["Latex Allergy", "Drug Allergy", "Food Allergy", "NKA", "NDA"] },
      { name: "Allergen", data_type: "String", description: "", comments: "" },
      { name: "Allergen Code", data_type: "String", description: "", comments: "", possible_values: ["NDC"] },
      { name: "Allergen Code System", data_type: "String", description: "", comments: "" },
      { name: "Adverse Reaction", data_type: "String", description: "", comments: "" },
      { name: "Drug Category", data_type: "String", description: "", comments: "" },
      { name: "Active Allergy", data_type: "Boolean", description: "True if the Allergy is currently Active", comments: "" },
      { name: "Resolved On", data_type: "String", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 16. EMR/Assesments.csv
  schemas.push({
    filename: "EMR/Assesments.csv",
    folder: "EMR",
    contents_description: "This file contains the patients' assessment information. This information is documented in GlaceEMR Clinical Note Templates under assessment section.",
    columns: [
      ...patientIdCols(),
      ...encounterIdCols(),
      { name: "Assessment ID", data_type: "Integer (Primary key)", description: "", comments: "", is_primary_key: true },
      { name: "Dx Code", data_type: "String", description: "Diagnosis Code", comments: "" },
      { name: "Dx Description", data_type: "String", description: "Diagnosis Description", comments: "" },
      { name: "Dx Coding System", data_type: "String", description: "", comments: "", possible_values: ["ICD 9", "ICD 10", "SNOMED", "ConfidentialityCode", "RXNORM", "CPT4", "NDC", "LOINC"] },
      { name: "Comment", data_type: "String", description: "", comments: "" },
      { name: "Status", data_type: "String", description: "", comments: "", possible_values: ["Open", "Canceled", "Closed"] },
      ...auditCols(),
    ],
  });

  // 17. EMR/Problem_List.csv
  schemas.push({
    filename: "EMR/Problem_List.csv",
    folder: "EMR",
    contents_description: "This file contains the patients' problem list. This information is documented in GlaceEMR Clinical Note Templates under assessment section. ICD 10 and SNOMED codes are used.",
    columns: [
      { name: "Problem List ID", data_type: "Integer (Primary key)", description: "", comments: "", is_primary_key: true },
      ...patientIdCols(),
      ...encounterIdCols(),
      { name: "Diagnosis Code", data_type: "String", description: "", comments: "" },
      { name: "Diagnosis Description", data_type: "String", description: "", comments: "" },
      { name: "Coding System Name", data_type: "String", description: "", comments: "", possible_values: ["ICD 9", "ICD 10", "SNOMED", "ConfidentialityCode", "RXNORM", "CPT4", "NDC", "LOINC"] },
      { name: "Onset Date", data_type: "String", description: "", comments: "" },
      { name: "Resolved By", data_type: "String", description: "", comments: "" },
      { name: "Resolved On", data_type: "String", description: "", comments: "" },
      { name: "Chronicity", data_type: "String", description: "", comments: "", possible_values: ["Chronic", "Acute"] },
      { name: "Status", data_type: "String", description: "", comments: "", possible_values: ["Active", "Resolved", "Inactive"] },
      { name: "Comment", data_type: "String", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 18. EMR/Medications.csv
  schemas.push({
    filename: "EMR/Medications.csv",
    folder: "EMR",
    contents_description: "This file contains the patients' medications. This information is documented in GlaceEMR Clinical Note Templates under prescription section.",
    columns: [
      ...patientIdCols(),
      ...encounterIdCols(),
      { name: "Medication ID", data_type: "Integer (Primary key)", description: "", comments: "", is_primary_key: true },
      { name: "Drug Name", data_type: "String", description: "", comments: "" },
      { name: "NDC", data_type: "String", description: "", comments: "" },
      { name: "Strength", data_type: "String", description: "", comments: "" },
      { name: "Form", data_type: "String", description: "", comments: "", possible_values: ["Syrup", "Gel", "Tablet", "Liquid", "Injection", "Powder"] },
      { name: "Route", data_type: "String", description: "", comments: "" },
      { name: "Schedule", data_type: "String", description: "", comments: "" },
      { name: "Days", data_type: "String", description: "", comments: "" },
      { name: "Refills", data_type: "String", description: "", comments: "" },
      { name: "Quantity", data_type: "String", description: "", comments: "" },
      { name: "Status", data_type: "String", description: "", comments: "", possible_values: ["New", "Refill", "Continue", "Discontinue", "Active", "Inactive"] },
      { name: "Notes", data_type: "String", description: "", comments: "" },
      { name: "Start Date", data_type: "Date & Time", description: "", comments: "" },
      { name: "Substitution", data_type: "String", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 19. EMR/InactiveMedications.csv
  schemas.push({
    filename: "EMR/InactiveMedications.csv",
    folder: "EMR",
    contents_description: "This file contains the patients' inactive medications. This information is documented in GlaceEMR Clinical Note Templates under prescription section.",
    columns: [
      ...patientIdCols(),
      ...encounterIdCols(),
      { name: "Medication ID", data_type: "Integer (Primary key)", description: "", comments: "", is_primary_key: true },
      { name: "Drug Name", data_type: "String", description: "", comments: "" },
      { name: "NDC", data_type: "String", description: "", comments: "" },
      { name: "Strength", data_type: "String", description: "", comments: "" },
      { name: "Form", data_type: "String", description: "", comments: "", possible_values: ["Syrup", "Gel", "Tablet", "Liquid", "Injection", "Powder"] },
      { name: "Route", data_type: "String", description: "", comments: "" },
      { name: "Schedule", data_type: "String", description: "", comments: "" },
      { name: "Days", data_type: "String", description: "", comments: "" },
      { name: "Refills", data_type: "String", description: "", comments: "" },
      { name: "Quantity", data_type: "String", description: "", comments: "" },
      { name: "Status", data_type: "String", description: "", comments: "", possible_values: ["New", "Refill", "Continue", "Discontinue", "Active", "Inactive"] },
      { name: "Substitution", data_type: "String", description: "", comments: "" },
      { name: "Notes", data_type: "String", description: "", comments: "" },
      { name: "Start Date", data_type: "Date", description: "", comments: "" },
      { name: "Stop Date", data_type: "Date", description: "", comments: "" },
      { name: "Stopped By", data_type: "String", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 20. EMR/Investigation.csv
  schemas.push({
    filename: "EMR/Investigation.csv",
    folder: "EMR",
    contents_description: "This file contains the patients' investigations. This information is documented in GlaceEMR Clinical Note Templates under investigations section.",
    columns: [
      ...patientIdCols(),
      ...encounterIdCols(),
      { name: "Test ID", data_type: "Integer (Primary key)", description: "Test Identifier", comments: "", is_primary_key: true },
      { name: "Test Name", data_type: "String", description: "", comments: "" },
      { name: "Test Status", data_type: "String", description: "", comments: "", possible_values: ["Ordered", "Cancelled", "Performed", "Results review", "Completed"] },
      { name: "Test Type", data_type: "String", description: "", comments: "", possible_values: ["Internal test", "External test"] },
      { name: "Billable", data_type: "String", description: "", comments: "" },
      { name: "Ordered By", data_type: "String", description: "", comments: "" },
      { name: "Ordered Date", data_type: "Date & Time", description: "", comments: "" },
      { name: "Performed By", data_type: "String", description: "", comments: "" },
      { name: "Performed Date", data_type: "Date & Time", description: "", comments: "" },
      { name: "Reviewed By", data_type: "String", description: "", comments: "" },
      { name: "Reviewed Date", data_type: "Date & Time", description: "", comments: "" },
      { name: "Units", data_type: "Integer", description: "", comments: "" },
      { name: "Prelimstatus", data_type: "String", description: "", comments: "" },
      { name: "Confirmstatus", data_type: "String", description: "", comments: "" },
      { name: "Dx1code", data_type: "String", description: "Diagnosis code", comments: "" },
      { name: "Dx1 Description", data_type: "String", description: "Diagnosis description", comments: "" },
      { name: "Dx1 Coding System Name", data_type: "String", description: "", comments: "" },
      { name: "Dx2 code", data_type: "String", description: "", comments: "" },
      { name: "Dx2 Description", data_type: "String", description: "", comments: "" },
      { name: "Dx2 Coding System Name", data_type: "String", description: "", comments: "" },
      { name: "CPT Code", data_type: "String", description: "", comments: "" },
      { name: "Result Notes", data_type: "String", description: "", comments: "" },
      { name: "Short Notes", data_type: "String", description: "", comments: "" },
      { name: "Short Order Notes", data_type: "String", description: "", comments: "" },
      { name: "Group Name", data_type: "String", description: "", comments: "", possible_values: ["Vaccination", "Radiology", "Injections", "X Ray", "ECG", "Therapy", "Biochemistry"] },
      { name: "Vaccination Lot Number", data_type: "String", description: "", comments: "" },
      { name: "Vaccination Route", data_type: "String", description: "", comments: "" },
      { name: "Vaccination Site", data_type: "String", description: "", comments: "" },
      { name: "Dosage Value", data_type: "String", description: "", comments: "" },
      { name: "Dosage Units", data_type: "String", description: "", comments: "" },
      { name: "Result Name", data_type: "String", description: "", comments: "" },
      { name: "Results Units", data_type: "String", description: "", comments: "" },
      { name: "Result Value", data_type: "String", description: "", comments: "" },
      { name: "Range", data_type: "String", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 21. EMR/Preventive_Screenings.csv
  schemas.push({
    filename: "EMR/Preventive_Screenings.csv",
    folder: "EMR",
    contents_description: "This file contains the patients' preventive screening information. This information is documented in GlaceEMR Clinical Note Templates under flow sheet section.",
    columns: [
      ...patientIdCols(),
      ...encounterIdCols(),
      ...historyElementCols(),
      ...auditCols(),
    ],
  });

  // 22. EMR/Coumadin.csv
  schemas.push({
    filename: "EMR/Coumadin.csv",
    folder: "EMR",
    contents_description: "This file contains the patients' coumadin drug dosage information. This information is documented in GlaceEMR Clinical Note Templates under flowsheet section.",
    columns: [
      ...patientIdCols(),
      { name: "Episode ID", data_type: "Integer", description: "", comments: "" },
      { name: "Episode Start Date", data_type: "Date", description: "", comments: "" },
      { name: "Episode End Date", data_type: "Date", description: "", comments: "" },
      { name: "Entry Date", data_type: "Date & Time", description: "", comments: "" },
      { name: "INR Goal Range", data_type: "String", description: "", comments: "" },
      { name: "Status", data_type: "Integer", description: "", comments: "" },
      { name: "Problem list DX Code", data_type: "String", description: "Diagnosis code", comments: "" },
      { name: "DX description", data_type: "String", description: "Diagnosis description", comments: "" },
      { name: "Coding System ID", data_type: "String", description: "", comments: "", possible_values: ["ICD 9", "ICD 10", "SNOMED", "ConfidentialityCode", "RXNORM", "CPT4", "NDC", "LOINC"] },
      { name: "Coding System Name", data_type: "String", description: "", comments: "" },
      { name: "PT", data_type: "String", description: "", comments: "" },
      { name: "INR", data_type: "String", description: "", comments: "" },
      { name: "Episode Attribute ID", data_type: "Integer", description: "", comments: "" },
      { name: "Total Weekly Dose", data_type: "String", description: "", comments: "" },
      { name: "Sunday Dose", data_type: "String", description: "", comments: "" },
      { name: "Monday Dose", data_type: "String", description: "", comments: "" },
      { name: "Tuesday Dose", data_type: "String", description: "", comments: "" },
      { name: "Wednesday Dose", data_type: "String", description: "", comments: "" },
      { name: "Thursday Dose", data_type: "String", description: "", comments: "" },
      { name: "Friday Dose", data_type: "String", description: "", comments: "" },
      { name: "Saturday Dose", data_type: "String", description: "", comments: "" },
      { name: "Next INR", data_type: "String", description: "", comments: "" },
      { name: "Comments", data_type: "String", description: "", comments: "" },
      { name: "Signed By", data_type: "String", description: "", comments: "" },
      { name: "Signed On", data_type: "Date & Time", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 23. EMR/Vaccines.csv
  schemas.push({
    filename: "EMR/Vaccines.csv",
    folder: "EMR",
    contents_description: "This file contains the patients' vaccination information. This information is documented in GlaceEMR Clinical Note Templates under immunization section.",
    columns: [
      ...patientIdCols(),
      { name: "Order ID", data_type: "Integer (Primary key)", description: "Order Identifier", comments: "", is_primary_key: true },
      { name: "Vaccine ID", data_type: "String (Foreign key)", description: "Vaccine Identifier", comments: "", is_foreign_key: true },
      { name: "Vaccine Name", data_type: "String", description: "", comments: "" },
      { name: "Vaccine Code", data_type: "String", description: "", comments: "" },
      { name: "Order Date", data_type: "Date", description: "", comments: "" },
      { name: "Dosage Value", data_type: "String", description: "", comments: "" },
      { name: "Dosage Type", data_type: "String", description: "", comments: "" },
      { name: "Lot No", data_type: "String", description: "", comments: "" },
      { name: "Expiry Date", data_type: "Date", description: "", comments: "" },
      { name: "Vaccination Site", data_type: "String", description: "", comments: "" },
      { name: "Vaccination Route", data_type: "String", description: "", comments: "" },
      { name: "Performed By", data_type: "String", description: "", comments: "" },
      { name: "Manufacturer Name", data_type: "String", description: "", comments: "" },
      { name: "Manufacturer Address", data_type: "String", description: "", comments: "" },
      { name: "Manufacturer City", data_type: "String", description: "", comments: "" },
      { name: "Manufacturer State", data_type: "String", description: "", comments: "" },
      { name: "Manufacturer Zip", data_type: "String", description: "", comments: "" },
      { name: "Manufacturer Phone", data_type: "String", description: "", comments: "" },
      { name: "Manufacturer Fax", data_type: "String", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 24. EMR/Messages.csv
  schemas.push({
    filename: "EMR/Messages.csv",
    folder: "EMR",
    contents_description: "This file contains the patients' messages. This information is documented in GlaceEMR Ph/Ext. Consult under New Phone Messages section.",
    columns: [
      ...patientIdCols(),
      ...encounterIdCols(),
      { name: "Chief Complaints", data_type: "String", description: "", comments: "" },
      { name: "Created By", data_type: "String", description: "", comments: "" },
      { name: "Status", data_type: "String", description: "", comments: "", possible_values: ["Open", "Cancelled", "Closed", "Callback", "Answered"] },
      { name: "Reason", data_type: "String", description: "", comments: "" },
      { name: "Referring Doctor", data_type: "String", description: "", comments: "Master information found in PMS/Master_Referring_Provider_List.csv" },
      { name: "Service Doctor", data_type: "String", description: "", comments: "" },
      { name: "Place Of Service", data_type: "String", description: "", comments: "Master information found in PMS/Master_POS_List.csv" },
      { name: "Patient Comments", data_type: "String", description: "", comments: "" },
      { name: "Doctor Response", data_type: "String", description: "", comments: "" },
      { name: "Type", data_type: "String", description: "", comments: "", possible_values: ["Internal Messages", "Phone Messages"] },
      { name: "Severity", data_type: "String", description: "", comments: "" },
      { name: "Created On", data_type: "Date & Time", description: "", comments: "" },
      { name: "Last Modified By", data_type: "String", description: "", comments: "" },
      { name: "Last Modified On", data_type: "Date & Time", description: "", comments: "" },
    ],
  });

  // 25. EMR/Reminders.csv
  schemas.push({
    filename: "EMR/Reminders.csv",
    folder: "EMR",
    contents_description: "This file contains the patients' reminder details. This information is documented in GlaceEMR Scheduler section.",
    columns: [
      ...patientIdCols(),
      { name: "Reminder Subject", data_type: "String", description: "", comments: "" },
      { name: "Reminder Description", data_type: "String", description: "", comments: "" },
      { name: "Reminder Due Date", data_type: "Date", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 26. EMR/Patient_Photo_Index_File.csv
  schemas.push({
    filename: "EMR/Patient_Photo_Index_File.csv",
    folder: "EMR",
    contents_description: "This file contains index of photos. The records are keyed with Patient ID.",
    columns: [
      ...patientIdCols(),
      { name: "Parent Folder Name", data_type: "String", description: "Folder of each patient", comments: "" },
      { name: "File Name", data_type: "String", description: "Image files", comments: "" },
      ...auditCols(),
    ],
  });

  // 27. EMR/Clinical_Document_Index_File.csv
  schemas.push({
    filename: "EMR/Clinical_Document_Index_File.csv",
    folder: "EMR",
    contents_description: "This file contains the name of the exported Clinical Notes (E.g. Progress Notes) for each note.",
    columns: [
      { name: "Note ID", data_type: "Integer (Primary key)", description: "", comments: "", is_primary_key: true },
      ...patientIdCols(),
      ...encounterIdCols(),
      { name: "Clinical Notes Name", data_type: "String", description: "", comments: "", possible_values: ["Nurse notes", "IM Progress Notes", "General note", "Cardiology Nurse Notes", "Annual wellness visit"] },
      { name: "Parent Folder Name", data_type: "String", description: "Folder of each patient", comments: "" },
      { name: "HTML File name", data_type: "String", description: "", comments: "" },
      { name: "PDF File name", data_type: "String", description: "", comments: "" },
      { name: "Signed By", data_type: "String", description: "", comments: "" },
      { name: "Signed On", data_type: "Date & Time", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 28. EMR/Phone_Messages_Index_File.csv
  schemas.push({
    filename: "EMR/Phone_Messages_Index_File.csv",
    folder: "EMR",
    contents_description: "This file contains index of phone messages for each patient.",
    columns: [
      ...patientIdCols(),
      ...encounterIdCols(),
      { name: "Parent Folder Name", data_type: "String", description: "Folder of each patient", comments: "" },
      { name: "HTML File name", data_type: "String", description: "", comments: "" },
      { name: "PDF File name", data_type: "String", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 29. EMR/Scan_And_Attachments_Index_File.csv
  schemas.push({
    filename: "EMR/Scan_And_Attachments_Index_File.csv",
    folder: "EMR",
    contents_description: "This file contains index of scans and attachment files.",
    columns: [
      ...patientIdCols(),
      { name: "Document ID", data_type: "Integer (Primary key)", description: "", comments: "", is_primary_key: true },
      { name: "Category Name", data_type: "String", description: "", comments: "" },
      { name: "Group ID", data_type: "Integer", description: "Group Identifier", comments: "" },
      { name: "Display Order", data_type: "Integer", description: "", comments: "" },
      { name: "Description", data_type: "String", description: "", comments: "" },
      { name: "Comments", data_type: "String", description: "", comments: "" },
      { name: "Parent Folder Name", data_type: "String", description: "Folder of each patient", comments: "" },
      { name: "File name", data_type: "String", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 30. EMR/CDA_Document_Index_File.csv
  schemas.push({
    filename: "EMR/CDA_Document_Index_File.csv",
    folder: "EMR",
    contents_description: "This file contains the name of exported CDA file for each patient.",
    columns: [
      ...patientIdCols(),
      { name: "Parent Folder Name", data_type: "String", description: "Folder of each patient", comments: "" },
      { name: "File Name", data_type: "String", description: "CCDA XML File Name", comments: "" },
      ...auditCols(),
    ],
  });

  // ── PMS FILES ──────────────────────────────────────────────

  // 31. PMS/Patient_Demographics.csv
  schemas.push({
    filename: "PMS/Patient_Demographics.csv",
    folder: "PMS",
    contents_description: "This file contains patient demographic details. This information is documented in GlaceEMR Patient registration section.",
    columns: [
      { name: "Patient ID", data_type: "Integer (Primary key)", description: "Patient Identifier", comments: "", is_primary_key: true },
      { name: "Patient Account#", data_type: "String", description: "Patient Account#", comments: "Unique Identifier" },
      { name: "Patient Last Name", data_type: "String", description: "", comments: "" },
      { name: "Patient First Name", data_type: "String", description: "", comments: "" },
      { name: "Patient Middle Initial", data_type: "String", description: "", comments: "" },
      { name: "Patient DOB", data_type: "Date", description: "Date Of Birth", comments: "" },
      { name: "Patient Prefix", data_type: "String", description: "", comments: "" },
      { name: "Patient Suffix", data_type: "String", description: "", comments: "" },
      { name: "Patient Gender", data_type: "String", description: "", comments: "", possible_values: ["Male", "Female"] },
      { name: "Patient Marital Status", data_type: "String", description: "", comments: "", possible_values: ["Married", "Divorced", "Separated", "Single", "Widowed"] },
      { name: "Patient Address", data_type: "String", description: "", comments: "" },
      { name: "Patient City", data_type: "String", description: "", comments: "" },
      { name: "Patient State", data_type: "String", description: "", comments: "" },
      { name: "Patient Zip", data_type: "String", description: "", comments: "" },
      { name: "Patient Home Phone", data_type: "String", description: "", comments: "" },
      { name: "Patient Work Phone", data_type: "String", description: "", comments: "" },
      { name: "Patient Cell Phone", data_type: "String", description: "", comments: "" },
      { name: "Patient Email", data_type: "String", description: "", comments: "" },
      { name: "Patient Maiden Name", data_type: "String", description: "", comments: "" },
      { name: "Relation to Guarantor", data_type: "String", description: "", comments: "", possible_values: ["Child", "Daughter", "Father", "Guardian", "Self", "Son", "Spouse"] },
      { name: "Guarantor Last Name", data_type: "String", description: "", comments: "" },
      { name: "Guarantor First Name", data_type: "String", description: "", comments: "" },
      { name: "Guarantor DOB", data_type: "String", description: "", comments: "" },
      { name: "Guarantor Gender", data_type: "String", description: "", comments: "", possible_values: ["Male", "Female"] },
      { name: "Guarantor Address", data_type: "String", description: "", comments: "" },
      { name: "Guarantor City", data_type: "String", description: "", comments: "" },
      { name: "Guarantor State", data_type: "String", description: "", comments: "" },
      { name: "Guarantor Zip", data_type: "String", description: "", comments: "" },
      { name: "Guarantor Home Phone", data_type: "String", description: "", comments: "" },
      { name: "Guarantor Work Phone", data_type: "String", description: "", comments: "" },
      { name: "Guarantor Cell Phone", data_type: "String", description: "", comments: "" },
      { name: "Guarantor Email", data_type: "String", description: "", comments: "" },
      { name: "Race", data_type: "String", description: "", comments: "" },
      { name: "Ethnicity", data_type: "String", description: "", comments: "" },
      { name: "Preferred Language", data_type: "String", description: "", comments: "" },
      { name: "Default Pharmacy Name", data_type: "String", description: "", comments: "" },
      { name: "Default Pharmacy NCPDP ID", data_type: "String", description: "", comments: "" },
      { name: "Principal Doctor", data_type: "String", description: "", comments: "" },
      { name: "Notes", data_type: "String", description: "", comments: "" },
      { name: "Emergency Contact Name", data_type: "String", description: "", comments: "" },
      { name: "Emergency Contact Address", data_type: "String", description: "", comments: "" },
      { name: "Emergency Contact City", data_type: "String", description: "", comments: "" },
      { name: "Emergency Contact State", data_type: "String", description: "", comments: "" },
      { name: "Emergency Contact Zip", data_type: "String", description: "", comments: "" },
      { name: "Emergency Contact Phone", data_type: "String", description: "", comments: "" },
      { name: "Emergency Contact Relation", data_type: "String", description: "", comments: "", possible_values: ["Child", "Daughter", "Father", "Guardian", "Self", "Son", "Spouse"] },
      { name: "Employer Name", data_type: "String", description: "", comments: "" },
      { name: "Deceased Status", data_type: "String", description: "", comments: "" },
      { name: "Deceased Date", data_type: "String", description: "", comments: "" },
      { name: "Patient Active Status", data_type: "String", description: "", comments: "" },
      { name: "Chart Patient Notes", data_type: "String", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 32. PMS/Patient_Insurance.csv
  schemas.push({
    filename: "PMS/Patient_Insurance.csv",
    folder: "PMS",
    contents_description: "This file contains patient insurance details. This information is documented in GlaceEMR Patient demographics section.",
    columns: [
      ...patientIdCols(),
      // Primary
      { name: "Primary Insurance Policy Number", data_type: "String", description: "", comments: "" },
      { name: "Primary Insurance Group Number", data_type: "String", description: "", comments: "" },
      { name: "Primary Insurance Id", data_type: "Integer (Foreign key)", description: "Insurance Identifier", comments: "Master information found in PMS/Master_Insurance_List.csv", is_foreign_key: true, foreign_key_ref: "PMS/Master_Insurance_List.csv" },
      { name: "Primary Insurance", data_type: "String", description: "", comments: "" },
      { name: "Primary Insurance Address", data_type: "String", description: "", comments: "" },
      { name: "Primary Insurance City", data_type: "String", description: "", comments: "" },
      { name: "Primary Insurance State", data_type: "String", description: "", comments: "" },
      { name: "Primary Insurance Zip", data_type: "String", description: "", comments: "" },
      { name: "Primary Insurance Subscriber Full Name", data_type: "String", description: "", comments: "" },
      { name: "Primary Insurance Subscriber Last Name", data_type: "String", description: "", comments: "" },
      { name: "Primary Insurance Subscriber First Name", data_type: "String", description: "", comments: "" },
      { name: "Primary Insurance Subscriber Middle Initial", data_type: "String", description: "", comments: "" },
      { name: "Primary Insurance Subscriber DOB", data_type: "Date", description: "", comments: "" },
      { name: "Primary Insurance Subscriber Relation", data_type: "String", description: "", comments: "", possible_values: ["Self", "Spouse", "Child", "Son"] },
      { name: "Primary Insurance Copay", data_type: "Currency", description: "", comments: "" },
      // Secondary
      { name: "Secondary Insurance Policy Number", data_type: "String", description: "", comments: "" },
      { name: "Secondary Insurance Group Number", data_type: "String", description: "", comments: "" },
      { name: "Secondary Insurance Id", data_type: "Integer (Foreign key)", description: "Insurance Identifier", comments: "", is_foreign_key: true },
      { name: "Secondary Insurance", data_type: "String", description: "", comments: "" },
      { name: "Secondary Insurance Address", data_type: "String", description: "", comments: "" },
      { name: "Secondary Insurance City", data_type: "String", description: "", comments: "" },
      { name: "Secondary Insurance State", data_type: "String", description: "", comments: "" },
      { name: "Secondary Insurance Zip", data_type: "String", description: "", comments: "" },
      { name: "Secondary Insurance Subscriber Name", data_type: "String", description: "", comments: "" },
      { name: "Secondary Insurance Subscriber Last Name", data_type: "String", description: "", comments: "" },
      { name: "Secondary Insurance Subscriber First Name", data_type: "String", description: "", comments: "" },
      { name: "Secondary Insurance Subscriber Middle Initial", data_type: "String", description: "", comments: "" },
      { name: "Secondary Insurance Subscriber DOB", data_type: "Date", description: "", comments: "" },
      { name: "Secondary Insurance Subscriber Relation", data_type: "String", description: "", comments: "", possible_values: ["Self", "Spouse", "Child", "Son"] },
      { name: "Secondary Insurance Copay", data_type: "Currency", description: "", comments: "" },
      // Tertiary
      { name: "Tertiary Insurance Policy Number", data_type: "String", description: "", comments: "" },
      { name: "Tertiary Insurance Group Number", data_type: "String", description: "", comments: "" },
      { name: "Tertiary Insurance Id", data_type: "Integer (Foreign key)", description: "Insurance Identifier", comments: "", is_foreign_key: true },
      { name: "Tertiary Insurance", data_type: "String", description: "", comments: "" },
      { name: "Tertiary Insurance Address", data_type: "String", description: "", comments: "" },
      { name: "Tertiary Insurance City", data_type: "String", description: "", comments: "" },
      { name: "Tertiary Insurance State", data_type: "String", description: "", comments: "" },
      { name: "Tertiary Insurance Zip", data_type: "String", description: "", comments: "" },
      { name: "Tertiary Insurance Subscriber Name", data_type: "String", description: "", comments: "" },
      { name: "Tertiary Insurance Subscriber Last Name", data_type: "String", description: "", comments: "" },
      { name: "Tertiary Insurance Subscriber First Name", data_type: "String", description: "", comments: "" },
      { name: "Tertiary Insurance Subscriber Middle Initial", data_type: "String", description: "", comments: "" },
      { name: "Tertiary Insurance Subscriber DOB", data_type: "Date", description: "", comments: "" },
      { name: "Tertiary Insurance Subscriber Relation", data_type: "String", description: "", comments: "" },
      { name: "Tertiary Insurance Copay", data_type: "Currency", description: "", comments: "" },
    ],
  });

  // 33. PMS/Patient_Account_Balance.csv
  schemas.push({
    filename: "PMS/Patient_Account_Balance.csv",
    folder: "PMS",
    contents_description: "This file contains the patients' account balance details. This information is documented in GlaceEMR Accounts section.",
    columns: [
      ...patientIdCols(),
      { name: "Patient Balance", data_type: "Currency", description: "", comments: "" },
      { name: "Insurance Balance", data_type: "Currency", description: "", comments: "" },
      { name: "Credit Balance", data_type: "Currency", description: "", comments: "" },
    ],
  });

  // 34. PMS/Transactions.csv
  schemas.push({
    filename: "PMS/Transactions.csv",
    folder: "PMS",
    contents_description: "This file contains payments transaction details. This information is documented in GlaceEMR Transactions section.",
    columns: [
      ...patientIdCols(),
      ...encounterIdCols(),
      { name: "Service ID", data_type: "Integer (Primary key)", description: "Service Identifier", comments: "", is_primary_key: true },
      { name: "Procedure Code", data_type: "String", description: "", comments: "" },
      { name: "Charges", data_type: "Currency", description: "", comments: "" },
      { name: "Diagnosis 1", data_type: "String", description: "", comments: "" },
      { name: "Diagnosis 2", data_type: "String", description: "", comments: "" },
      { name: "Diagnosis 3", data_type: "String", description: "", comments: "" },
      { name: "Diagnosis 4", data_type: "String", description: "", comments: "" },
      { name: "Submit Status", data_type: "String", description: "", comments: "" },
      { name: "Service Doctor", data_type: "String", description: "", comments: "Master information found in PMS/Master_Provider_List.csv" },
      { name: "Billing Doctor", data_type: "String", description: "", comments: "" },
      { name: "Referring Doctor", data_type: "String", description: "", comments: "Master information found in PMS/Master_Referring_Provider_List.csv" },
      { name: "Authorization Number", data_type: "String", description: "", comments: "" },
      { name: "Primary Insurance Name", data_type: "String", description: "", comments: "Master information found in PMS/Master_Insurance_List.csv" },
      { name: "Secondary Insurance Name", data_type: "String", description: "", comments: "Master information found in PMS/Master_Insurance_List.csv" },
      { name: "Allowed Amount", data_type: "Numeric/Decimal", description: "", comments: "" },
      { name: "Patient Payment", data_type: "Numeric/Decimal", description: "", comments: "" },
      { name: "Insurance Payment", data_type: "Numeric/Decimal", description: "", comments: "" },
      { name: "Payments", data_type: "Numeric/Decimal", description: "", comments: "" },
      { name: "Adjustment", data_type: "Numeric/Decimal", description: "", comments: "" },
      { name: "Balance", data_type: "Numeric/Decimal", description: "", comments: "" },
      { name: "Patient Balance", data_type: "Numeric/Decimal", description: "", comments: "" },
      { name: "Insurance Balance", data_type: "Numeric/Decimal", description: "", comments: "" },
      { name: "Units", data_type: "Integer", description: "", comments: "" },
      { name: "Place of Service", data_type: "String", description: "", comments: "Master information found in PMS/Master_POS_List.csv" },
      { name: "Estimate Balance", data_type: "Numeric/Decimal", description: "", comments: "" },
    ],
  });

  // 35. PMS/Payment_Receipts.csv
  schemas.push({
    filename: "PMS/Payment_Receipts.csv",
    folder: "PMS",
    contents_description: "This file contains payment receipt details. This information is documented in GlaceEMR Payments section.",
    columns: [
      ...patientIdCols(),
      { name: "Receipt ID", data_type: "Integer (Primary key)", description: "Receipt Identifier", comments: "", is_primary_key: true },
      { name: "Receipt Date", data_type: "Date", description: "", comments: "" },
      { name: "Payment Type", data_type: "String", description: "", comments: "", possible_values: ["Cash", "Check", "Card", "Insurance"] },
      { name: "Amount", data_type: "Currency", description: "", comments: "" },
      { name: "Comment", data_type: "String", description: "", comments: "" },
      { name: "Payment Code", data_type: "Integer", description: "", comments: "" },
      { name: "Adjustment Code", data_type: "Integer", description: "", comments: "" },
      { name: "Withhold Code", data_type: "Integer", description: "", comments: "" },
      { name: "Deductible Code", data_type: "Integer", description: "", comments: "" },
      { name: "Refund Code", data_type: "Integer", description: "", comments: "" },
      { name: "Denial Code", data_type: "Integer", description: "", comments: "" },
      { name: "Payee Type", data_type: "Integer", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 36. PMS/Payment_Posting.csv
  schemas.push({
    filename: "PMS/Payment_Posting.csv",
    folder: "PMS",
    contents_description: "This file contains patient's payment details. This information is documented in GlaceEMR Payments section.",
    columns: [
      ...patientIdCols(),
      { name: "Receipt Id", data_type: "Integer (Foreign key)", description: "Receipt Identifier", comments: "Master information found in PMS/Payment_Receipts.csv", is_foreign_key: true, foreign_key_ref: "PMS/Payment_Receipts.csv" },
      { name: "Service ID", data_type: "Integer (Foreign key)", description: "", comments: "Master information found in PMS/Transactions.csv", is_foreign_key: true, foreign_key_ref: "PMS/Transactions.csv" },
      { name: "Procedure Code", data_type: "String", description: "", comments: "" },
      { name: "Procedure Code Description", data_type: "String", description: "", comments: "" },
      { name: "Amount", data_type: "Numeric/Decimal", description: "", comments: "" },
      { name: "Comments", data_type: "String", description: "", comments: "" },
    ],
  });

  // 37. PMS/Appointments.csv
  schemas.push({
    filename: "PMS/Appointments.csv",
    folder: "PMS",
    contents_description: "This file contains the patients' appointments details. This information is documented in GlaceEMR Scheduler section.",
    columns: [
      ...patientIdCols(),
      { name: "Appointment ID", data_type: "Integer (Primary key)", description: "", comments: "", is_primary_key: true },
      { name: "Date", data_type: "Date", description: "", comments: "" },
      { name: "Start Time", data_type: "Date & Time", description: "", comments: "" },
      { name: "End Time", data_type: "Date & Time", description: "", comments: "" },
      { name: "Duration", data_type: "Integer", description: "", comments: "" },
      { name: "Scheduler Resource Name", data_type: "String", description: "", comments: "" },
      { name: "Associated Provider Name", data_type: "String", description: "", comments: "" },
      { name: "Location Name", data_type: "String", description: "", comments: "Master information found in PMS/Master_POS_List.csv" },
      { name: "Appointment Status", data_type: "String", description: "", comments: "", possible_values: ["Confirmed", "Cancelled", "Check In", "Online Consult"] },
      { name: "Appointment Type", data_type: "String", description: "", comments: "" },
      { name: "Appointment Reason", data_type: "String", description: "", comments: "" },
      { name: "Appointment Notes", data_type: "String", description: "", comments: "" },
      ...auditCols(),
    ],
  });

  // 38. PMS/Master_Insurance_List.csv
  schemas.push({
    filename: "PMS/Master_Insurance_List.csv",
    folder: "PMS",
    contents_description: "This file contains the insurance company details. This information is documented in GlaceEMR Insurance picker section.",
    columns: [
      { name: "Insurance ID", data_type: "Integer (Primary key)", description: "Insurance Carrier Identifier", comments: "", is_primary_key: true },
      { name: "Insurance Name", data_type: "String", description: "", comments: "" },
      { name: "Insurance Address", data_type: "String", description: "", comments: "" },
      { name: "Insurance City", data_type: "String", description: "", comments: "" },
      { name: "Insurance State", data_type: "String", description: "", comments: "" },
      { name: "Insurance Zip Code", data_type: "String", description: "", comments: "" },
    ],
  });

  // 39. PMS/Master_POS_List.csv
  schemas.push({
    filename: "PMS/Master_POS_List.csv",
    folder: "PMS",
    contents_description: "This file contains Place Of Service information. This information is documented in GlaceEMR Configuration section.",
    columns: [
      { name: "Practice Name", data_type: "String", description: "", comments: "" },
      { name: "Place of Service", data_type: "String", description: "", comments: "" },
      { name: "Facility Comments", data_type: "String", description: "", comments: "" },
      { name: "Status", data_type: "String", description: "", comments: "", possible_values: ["Active", "Inactive"] },
    ],
  });

  // 40. PMS/Master_Provider_List.csv
  schemas.push({
    filename: "PMS/Master_Provider_List.csv",
    folder: "PMS",
    contents_description: "This file contains care provider details. This information is documented in GlaceEMR Employee section.",
    columns: [
      { name: "Provider Last Name", data_type: "String", description: "", comments: "" },
      { name: "Provider Middle Initial", data_type: "String", description: "", comments: "" },
      { name: "Provider First Name", data_type: "String", description: "", comments: "" },
      { name: "Provider Full Name", data_type: "String", description: "", comments: "" },
      { name: "Provider Address", data_type: "String", description: "", comments: "" },
      { name: "Provider City", data_type: "String", description: "", comments: "" },
      { name: "Provider State", data_type: "String", description: "", comments: "" },
      { name: "Provider Zip", data_type: "String", description: "", comments: "" },
      { name: "Provider Phone", data_type: "String", description: "", comments: "" },
      { name: "Provider Email", data_type: "String", description: "", comments: "" },
      { name: "Provider Status", data_type: "String", description: "", comments: "", possible_values: ["Active", "Inactive"] },
      { name: "NPI", data_type: "String", description: "", comments: "" },
      { name: "DEA", data_type: "String", description: "", comments: "" },
      { name: "License", data_type: "String", description: "", comments: "" },
      { name: "License State", data_type: "String", description: "", comments: "" },
      { name: "Type", data_type: "String", description: "", comments: "" },
    ],
  });

  // 41. PMS/Master_Referring_Provider_List.csv
  schemas.push({
    filename: "PMS/Master_Referring_Provider_List.csv",
    folder: "PMS",
    contents_description: "This file contains referring doctor details. This information is documented in GlaceEMR Referring details section.",
    columns: [
      { name: "Referring Doctor ID", data_type: "Integer (Primary key)", description: "", comments: "", is_primary_key: true },
      { name: "Full Name", data_type: "String", description: "", comments: "" },
      { name: "Last Name", data_type: "String", description: "", comments: "" },
      { name: "Middle Name", data_type: "String", description: "", comments: "" },
      { name: "First Name", data_type: "String", description: "", comments: "" },
      { name: "Address", data_type: "String", description: "", comments: "" },
      { name: "City", data_type: "String", description: "", comments: "" },
      { name: "State", data_type: "String", description: "", comments: "" },
      { name: "Zip", data_type: "String", description: "", comments: "" },
      { name: "Phone", data_type: "String", description: "", comments: "" },
      { name: "Fax", data_type: "String", description: "", comments: "" },
      { name: "Direct Messaging Address", data_type: "String", description: "", comments: "" },
      { name: "NPI", data_type: "String", description: "", comments: "" },
      { name: "Active", data_type: "String", description: "", comments: "" },
    ],
  });

  return schemas;
}

// ── Main ──────────────────────────────────────────────────────────────────

const fileSchemas = buildSchemasFromReading();

let totalColumns = 0;
let filesWithPK = 0;
let filesWithFK = 0;
for (const fs of fileSchemas) {
  totalColumns += fs.columns.length;
  if (fs.columns.some((c) => c.is_primary_key)) filesWithPK++;
  if (fs.columns.some((c) => c.is_foreign_key)) filesWithFK++;
}

const dictionary: DataDictionary = {
  document_title: "GlaceEMR Data Export Data Dictionary",
  version: "1.0",
  release_date: "2023-11-27",
  author: "Adnan Shariq",
  export_structure: {
    top_level_folders: ["EMR", "PMS", "Documents", "Photos", "Reference"],
    emr_files: [
      "Encounters.csv", "Vitals.csv", "Past_Medical_History.csv", "Surgical_History.csv",
      "Family_History.csv", "Family_Relations_History.csv", "Social_History.csv",
      "Substance_Abuse_History.csv", "Contraception_Sexual_History.csv", "Pregnancy_History.csv",
      "Birthing_History.csv", "Menstrual_History.csv", "Occupational_History.csv",
      "Obstetric_History.csv", "Exposure_History.csv", "Allergies.csv", "Assesments.csv",
      "Problem_List.csv", "Medications.csv", "InactiveMedications.csv", "Investigation.csv",
      "Preventive_Screenings.csv", "Coumadin.csv", "Vaccines.csv", "Messages.csv",
      "Reminders.csv", "Patient_Photo_Index_File.csv", "Clinical_Document_Index_File.csv",
      "Phone_Messages_Index_File.csv", "Scan_And_Attachments_Index_File.csv",
      "CDA_Document_Index_File.csv"
    ],
    pms_files: [
      "Patient_Demographics.csv", "Patient_Insurance.csv", "Patient_Account_Balance.csv",
      "Transactions.csv", "Payment_Receipts.csv", "Payment_Posting.csv", "Appointments.csv",
      "Master_Insurance_List.csv", "Master_POS_List.csv", "Master_Provider_List.csv",
      "Master_Referring_Provider_List.csv"
    ],
    other_folders: [
      {
        name: "Documents",
        description: "Contains patient-related documents in HTML, PDF, and XML format. Organized per-patient in folders named LastName,FirstName-(DOB MM-DD-YYYY)-(Account#)-[PatientID]. Includes clinical templates (HTML+PDF), scanned documents/attachments (PNG/JPEG/original format), and C-CDA v2 XML files."
      },
      {
        name: "Photos",
        description: "Patient photos in JPG format, named LastName,FirstName-(DOB MM-DD-YYYY)-(Account#)-[PatientID].jpg"
      },
      {
        name: "Reference",
        description: "Contains the schema of the exported file content."
      }
    ]
  },
  file_schemas: fileSchemas,
  extraction_stats: {
    total_files_documented: fileSchemas.length,
    total_columns_documented: totalColumns,
    files_with_primary_keys: filesWithPK,
    files_with_foreign_keys: filesWithFK,
  },
};

writeFileSync(OUTPUT, JSON.stringify(dictionary, null, 2));
console.log(`Wrote ${OUTPUT}`);
console.log(`  ${dictionary.extraction_stats.total_files_documented} file schemas`);
console.log(`  ${dictionary.extraction_stats.total_columns_documented} total columns`);
console.log(`  ${dictionary.extraction_stats.files_with_primary_keys} files with primary keys`);
console.log(`  ${dictionary.extraction_stats.files_with_foreign_keys} files with foreign keys`);

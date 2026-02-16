#!/usr/bin/env bun
/**
 * Extracts the data dictionary from the PrognoCIS EHI Export PDF text.
 *
 * Input:  ../b-10-EHI-Export_PrognoCIS-Support.txt  (pdftotext output)
 * Output: ./data-dictionary.json
 *
 * Run:  cd enrichment && bun run extract-data-dictionary.ts
 */

import { readFileSync, writeFileSync } from "fs";
import { join } from "path";

const txtPath = join(__dirname, "..", "b-10-EHI-Export_PrognoCIS-Support.txt");
const raw = readFileSync(txtPath, "utf-8");

// Strip page footers, headers, form feeds, and page numbers
const cleaned = raw
  .replace(/\f/g, "") // form feed chars
  .replace(/2429 Military Suite 300.*?Phone \(Support\):.*?\d+/g, "")
  .replace(
    /§170\.315\(b\)\(10\) Electronic Health Information export_Self Attestation Document/g,
    ""
  )
  .replace(/\n\d{1,2}\n/g, "\n") // page numbers on their own line
  .replace(/\n{3,}/g, "\n\n")
  // Normalize all quote types to ASCII
  .replace(/[\u201C\u201D]/g, '"');

interface DataElement {
  number: number;
  name: string;
  description: string;
  fields: string[];
  hasFileColumn: boolean;
  fileExample: string | null;
  notes: string[];
}

// Known section names from the PDF (47 data element types)
const knownSections: [number, string][] = [
  [1, "Insurance Master"],
  [2, "Medics"],
  [3, "Referring Doctor"],
  [4, "Adjusters"],
  [5, "Attorneys"],
  [6, "Employers"],
  [7, "Guarantor"],
  [8, "Patient Demographics"],
  [9, "Patient Insurance"],
  [10, "Vaccination"],
  [11, "Health Maintenance"],
  [12, "Family History"],
  [13, "Past Medical Hist"],
  [14, "Surgery"],
  [15, "Allergy"],
  [16, "Current Medication"],
  [17, "Social History"],
  [18, "Legal Documents"],
  [19, "Other Documents"],
  [20, "Enc Attach Docs"],
  [21, "Old Progress Notes"],
  [22, "Messages"],
  [23, "Future Appointments"],
  [24, "Vitals"],
  [25, "Diagnosis Code"],
  [26, "CPT Codes"],
  [27, "HCPC Codes"],
  [28, "CCD"],
  [29, "Prescriptions"],
  [30, "Lab Results"],
  [31, "Rad Results"],
  [32, "Procedure Orders"],
  [33, "Consults"],
  [34, "Enc Progress Notes"],
  [35, "Procedure Notes"],
  [36, "Letters"],
  [37, "All Vitals"],
  [38, "Lab Test Result Values"],
  [39, "Patient Cases"],
  [40, "Patient Notes"],
  [41, "Patient Alert"],
  [42, "Past Appointments"],
  [43, "Billing Ledger"],
  [44, "Billing Claims"],
  [45, "Billing Charges"],
  [46, "Patient Advance"],
  [47, "Statements"],
];

const elements: DataElement[] = [];
const parseFailures: { section: string; reason: string }[] = [];

// Find each section by its known header
const detailedStart = cleaned.indexOf(
  "Detailed Description of the Data Export Contents"
);
if (detailedStart === -1) {
  console.error(
    "Could not find 'Detailed Description of the Data Export Contents'"
  );
  process.exit(1);
}

const detailedSection = cleaned.slice(detailedStart);

// Find section boundaries
const sectionPositions: { num: number; name: string; index: number }[] = [];

for (const [num, name] of knownSections) {
  // Match "1. Insurance Master" or "28. CCD"
  const pattern = new RegExp(`(?:^|\\n)${num}\\.\\s+${name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`, "m");
  const m = pattern.exec(detailedSection);
  if (m) {
    sectionPositions.push({ num, name, index: m.index });
  } else {
    parseFailures.push({
      section: `${num}. ${name}`,
      reason: "Section header not found in text",
    });
  }
}

// Sort by position in text
sectionPositions.sort((a, b) => a.index - b.index);

for (let i = 0; i < sectionPositions.length; i++) {
  const sec = sectionPositions[i];
  const nextIndex =
    i + 1 < sectionPositions.length
      ? sectionPositions[i + 1].index
      : detailedSection.length;

  // Get section header line to skip past it
  const headerPattern = new RegExp(`${sec.num}\\.\\s+${sec.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`);
  const headerMatch = headerPattern.exec(detailedSection.slice(sec.index));
  const headerLen = headerMatch ? headerMatch[0].length : sec.name.length + 4;

  const body = detailedSection
    .slice(sec.index + headerLen, nextIndex)
    .trim();

  // Extract fields from "Exported field list is" patterns
  // After normalization, all quotes are ASCII "
  // Some sections have footer residue (e.g. " 3032") between "is" and the quote
  let fields: string[] = [];

  // Pattern 1: Exported field list is [stuff] "field1, field2, ..."
  // Allow any junk between "is" and opening quote (footer residue, dashes, whitespace)
  const fieldListMatch = body.match(
    /Exported field list is[\s\S]{0,50}?"([\s\S]*?)"/
  );
  if (fieldListMatch) {
    fields = fieldListMatch[1]
      .replace(/\n/g, " ")
      .split(",")
      .map((f) => f.trim())
      .filter((f) => f.length > 0);
  } else {
    // Pattern 2: No quotes, followed by field names starting with uppercase
    const noQuoteMatch = body.match(
      /Exported field list is[\s\-\u2013:]+([A-Z][^"]*?)(?:\n\n|\n\d+\.|$)/s
    );
    if (noQuoteMatch) {
      fields = noQuoteMatch[1]
        .replace(/\n/g, " ")
        .split(",")
        .map((f) => f.trim())
        .filter((f) => f.length > 0);
    }
  }

  // Check for file column
  const hasFileColumn = body.includes('column labeled "File"');
  const fileExampleMatch = body.match(
    /For ex\.?\s*(CHART\d+\/[A-Z_]+\d+\.\w+)/
  );

  // Extract description (everything before "Exported field list")
  let description = body;
  const exportedIdx = body.indexOf("Exported field list");
  if (exportedIdx > 0) {
    description = body.slice(0, exportedIdx).trim();
  }
  // Also trim description at "It contains a specific column"
  const fileColIdx = description.indexOf("It contains a specific column");
  if (fileColIdx > 0) {
    description = description.slice(0, fileColIdx).trim();
  }

  // Collect notes
  const notes: string[] = [];
  const notePatterns = [
    /Only .+? are exported\.?/g,
    /Please note .+/g,
    /We (?:only|do not) .+/g,
    /Void (?:claims|Charges) (?:will )?not be exported\.?/g,
  ];
  for (const np of notePatterns) {
    let nm: RegExpExecArray | null;
    while ((nm = np.exec(body)) !== null) {
      notes.push(nm[0].trim());
    }
  }

  if (fields.length === 0 && !hasFileColumn) {
    parseFailures.push({
      section: `${sec.num}. ${sec.name}`,
      reason: "No field list found (section has minimal detail)",
    });
  }

  elements.push({
    number: sec.num,
    name: sec.name,
    description: description
      .replace(/\n/g, " ")
      .replace(/\s{2,}/g, " ")
      .trim(),
    fields,
    hasFileColumn,
    fileExample: fileExampleMatch ? fileExampleMatch[1] : null,
    notes,
  });
}

// Extract the "Data Elements Types" checklist — skip the TOC entry, use the real one
let checklistItems: string[] = [];
{
  const firstIdx = cleaned.indexOf("Data Elements Types");
  const secondIdx = firstIdx > -1 ? cleaned.indexOf("Data Elements Types", firstIdx + 1) : -1;
  const checklistStart = secondIdx > -1 ? secondIdx : firstIdx;
  const checklistEnd = cleaned.indexOf(
    "Detailed Description of the Data Export Contents",
    checklistStart
  );
  if (checklistStart > -1 && checklistEnd > checklistStart) {
    const checklistSection = cleaned.slice(checklistStart, checklistEnd);
    checklistItems = checklistSection
      .split("\n")
      .map((l) => l.replace(/^[\u2022\s]+/, "").trim())
      .filter(
        (l) =>
          l.length > 0 &&
          !l.startsWith("Data Elements") &&
          !l.startsWith("User can") &&
          !l.startsWith("When Billing") &&
          !l.startsWith("from following") &&
          l !== "•"
      );
  }
}

const billingItems = [
  "Billing Ledger",
  "Billing Claims",
  "Billing Charges",
  "Patient Advance",
  "Statements",
];

const output = {
  source: "b-10-EHI-Export_PrognoCIS-Support.pdf",
  product: "PrognoCIS",
  version: "Denali 3.1",
  document_title:
    "\u00A7170.315(b)(10) Electronic Health Information export_Self Attestation Document",
  document_date: "2023-12-01",
  total_data_elements: elements.length,
  checklist_items: checklistItems,
  billing_conditional_items: billingItems,
  data_elements: elements,
  parse_stats: {
    total_sections_found: sectionPositions.length,
    total_elements_extracted: elements.length,
    elements_with_fields: elements.filter((e) => e.fields.length > 0).length,
    elements_with_file_column: elements.filter((e) => e.hasFileColumn).length,
    total_fields_across_all_elements: elements.reduce(
      (sum, e) => sum + e.fields.length,
      0
    ),
    parse_failures: parseFailures,
  },
};

const outPath = join(__dirname, "data-dictionary.json");
writeFileSync(outPath, JSON.stringify(output, null, 2));

console.log("Extraction complete:");
console.log(`  Sections found: ${sectionPositions.length}`);
console.log(
  `  Elements extracted: ${elements.length} (${elements.filter((e) => e.fields.length > 0).length} with field lists)`
);
console.log(
  `  Total fields: ${elements.reduce((s, e) => s + e.fields.length, 0)}`
);
console.log(
  `  Elements with file attachments: ${elements.filter((e) => e.hasFileColumn).length}`
);
console.log(`  Parse failures: ${parseFailures.length}`);
if (parseFailures.length > 0) {
  for (const pf of parseFailures) {
    console.log(`    - ${pf.section}: ${pf.reason}`);
  }
}
console.log(`Output: ${outPath}`);

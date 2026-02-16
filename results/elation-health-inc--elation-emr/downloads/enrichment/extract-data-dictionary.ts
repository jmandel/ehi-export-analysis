#!/usr/bin/env bun
/**
 * Extracts structured data from Elation's Designated Record Set PDF
 * into queryable JSON.
 *
 * Input: ../elation-designated-record-set-ehi-export.pdf (via pdftotext -layout)
 * Output: ./data-dictionary.json, ./coverage-summary.json
 *
 * Run: bun run extract-data-dictionary.ts
 */

import { $ } from "bun";

const PDF_PATH = new URL(
  "../elation-designated-record-set-ehi-export.pdf",
  import.meta.url
).pathname;

interface DataElement {
  data_element: string;
  data_description: string;
  section: string;
  export_formats: {
    computable_pdf: boolean;
    xml: boolean;
    json: boolean;
    csv: boolean;
  };
}

interface ColumnPositions {
  pdf: number;
  xml: number;
  json: number;
  csv: number;
  line_end: number;
}

interface CoverageSummary {
  total_elements: number;
  by_section: Record<string, number>;
  by_format: {
    computable_pdf: number;
    xml: number;
    json: number;
    csv: number;
  };
  elements_with_no_format: string[];
  parse_info: {
    total_lines: number;
    header_lines: number;
    data_lines: number;
    empty_lines: number;
    section_header_lines: number;
  };
}

function findColumnPositions(headerLine: string): ColumnPositions | null {
  const pdf = headerLine.indexOf("Computable PDF");
  const xml = headerLine.indexOf("XML Export");
  const json = headerLine.indexOf("JSON");
  const csv = headerLine.indexOf("CSV Export");

  if (pdf === -1 || xml === -1 || json === -1 || csv === -1) return null;

  return {
    pdf,
    xml,
    json,
    csv,
    line_end: csv + 10, // "CSV Export" is 10 chars
  };
}

function classifyXPosition(
  xPos: number,
  cols: ColumnPositions
): "pdf" | "xml" | "json" | "csv" | null {
  // Column boundaries: each column extends from its start to just before the
  // next column. "Computable PDF Export" is ~21 chars wide, others are shorter.
  // Use next column start - 2 as the boundary (2 char gap between columns).

  if (xPos >= cols.pdf - 2 && xPos < cols.xml - 2) return "pdf";
  if (xPos >= cols.xml - 2 && xPos < cols.json - 2) return "xml";
  if (xPos >= cols.json - 2 && xPos < cols.csv - 2) return "json";
  if (xPos >= cols.csv - 2 && xPos <= cols.line_end + 5) return "csv";

  return null;
}

function findIsolatedXPositions(line: string): number[] {
  const positions: number[] = [];
  for (let i = 0; i < line.length; i++) {
    if (line[i] === "X") {
      const leftOk = i === 0 || line[i - 1] === " ";
      const rightOk = i === line.length - 1 || line[i + 1] === " ";
      if (leftOk && rightOk) {
        positions.push(i);
      }
    }
  }
  return positions;
}

function inferSection(element: string, description: string, prevSection: string): string {
  // Detect section transitions based on data element names
  if (element === "Imaging Reports") return "Imaging";
  if (element === "Appointment Type") return "Appointments";
  if (element === "Name" && description === "Patient name") return "Patient Demographics";
  if (element === "Race" && description.includes("race")) return "Patient Demographics";
  if (element === "OTC medications") return "Medications";
  if (element === "Providers List") return "Care Team & Documents";
  if (element === "Medical History Report") return "Clinical Records";
  if (element === "Problem List") return "Clinical Records";
  if (element === "Sexual Orientation") return "Additional Demographics";
  if (element === "Guarantor First Name") return "Guarantor Information";
  if (element === "Patient Status") return "Patient Status";
  if (element.includes("Lab Order") || element.includes("Imaging Order")) return "Clinical Orders";
  if (element === "Social history") return "Social History";
  if (element === "Eligibility Check Timestamp") return "Eligibility/Insurance Verification";
  if (element === "Bill" && description.includes("bill object")) return "Billing - Bills";
  if (element === "PatientLiability") return "Billing - Patient Liability";
  if (element === "Amount_refunded_usd") return "Billing - Patient Liability (continued)";
  if (element === "Payment_requests") return "Billing - Payment Requests";

  return prevSection;
}

async function main() {
  const result = await $`pdftotext -layout ${PDF_PATH} -`.text();
  const lines = result.split("\n");

  const elements: DataElement[] = [];
  let currentCols: ColumnPositions | null = null;
  let currentSection = "General";
  let headerCount = 0;
  let dataCount = 0;
  let emptyCount = 0;
  let sectionHeaderCount = 0;

  // Known section header lines (no X markers, standalone text)
  const sectionHeaders = new Set([
    "Elation Billing Specific Data",
  ]);

  for (const line of lines) {
    const trimmed = line.trimEnd();
    const stripped = trimmed.trim();

    // Empty line
    if (!stripped) {
      emptyCount++;
      continue;
    }

    // Header row - update column positions
    if (stripped.startsWith("Data Element") && stripped.includes("Data Description")) {
      const cols = findColumnPositions(trimmed);
      if (cols) {
        currentCols = cols;
        headerCount++;
      }
      continue;
    }

    // Section header
    if (sectionHeaders.has(stripped)) {
      currentSection = stripped;
      sectionHeaderCount++;
      continue;
    }

    // Need column positions to parse data rows
    if (!currentCols) continue;

    // Find isolated X markers
    const xPositions = findIsolatedXPositions(trimmed);

    // Data row with X markers
    if (xPositions.length > 0) {
      // The text portion is everything before the export columns
      // Use the pdf column start minus a small margin as the boundary
      const textEnd = currentCols.pdf - 1;
      const textPortion = trimmed.substring(0, textEnd).trimEnd();

      // Split element name from description by multiple spaces
      const parts = textPortion.split(/\s{2,}/);
      const dataElement = parts[0]?.trim() || "";
      const dataDescription = parts.slice(1).join(" ").trim();

      if (!dataElement) continue;

      // Classify each X marker
      let pdf = false, xml = false, json = false, csv = false;
      for (const xPos of xPositions) {
        const col = classifyXPosition(xPos, currentCols);
        if (col === "pdf") pdf = true;
        else if (col === "xml") xml = true;
        else if (col === "json") json = true;
        else if (col === "csv") csv = true;
      }

      currentSection = inferSection(dataElement, dataDescription, currentSection);

      elements.push({
        data_element: dataElement,
        data_description: dataDescription,
        section: currentSection,
        export_formats: {
          computable_pdf: pdf,
          xml: xml,
          json: json,
          csv: csv,
        },
      });
      dataCount++;
    }
  }

  // Build coverage summary
  const bySection: Record<string, number> = {};
  const byFormat = { computable_pdf: 0, xml: 0, json: 0, csv: 0 };
  const noFormat: string[] = [];

  for (const el of elements) {
    bySection[el.section] = (bySection[el.section] || 0) + 1;
    if (el.export_formats.computable_pdf) byFormat.computable_pdf++;
    if (el.export_formats.xml) byFormat.xml++;
    if (el.export_formats.json) byFormat.json++;
    if (el.export_formats.csv) byFormat.csv++;

    if (
      !el.export_formats.computable_pdf &&
      !el.export_formats.xml &&
      !el.export_formats.json &&
      !el.export_formats.csv
    ) {
      noFormat.push(el.data_element);
    }
  }

  const summary: CoverageSummary = {
    total_elements: elements.length,
    by_section: bySection,
    by_format: byFormat,
    elements_with_no_format: noFormat,
    parse_info: {
      total_lines: lines.length,
      header_lines: headerCount,
      data_lines: dataCount,
      empty_lines: emptyCount,
      section_header_lines: sectionHeaderCount,
    },
  };

  const outDir = new URL(".", import.meta.url).pathname;
  await Bun.write(`${outDir}/data-dictionary.json`, JSON.stringify(elements, null, 2));
  await Bun.write(`${outDir}/coverage-summary.json`, JSON.stringify(summary, null, 2));

  console.log(`Extracted ${elements.length} data elements from ${headerCount} page tables`);
  console.log(`Sections: ${Object.keys(bySection).join(", ")}`);
  console.log(
    `Format coverage: PDF=${byFormat.computable_pdf}, XML=${byFormat.xml}, JSON=${byFormat.json}, CSV=${byFormat.csv}`
  );
  if (noFormat.length > 0) {
    console.log(`Elements with no format specified: ${noFormat.join(", ")}`);
  }
}

main().catch(console.error);

#!/usr/bin/env bun
/**
 * Extracts structured data from the Lunar EHI Export PDF text.
 * Parses C-CDA sections, supplemental data dictionaries, and key elements tables.
 *
 * Usage: bun run extract-sections.ts
 * Input: ../EHI_Export_Jan_2026.pdf (via pdftotext)
 * Output: ./ehi-export-sections.json, ./ehi-export-supplemental.json, ./extraction-stats.json
 */

import { execSync } from "child_process";
import { writeFileSync } from "fs";
import { resolve, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const pdfPath = resolve(scriptDir, "../EHI_Export_Jan_2026.pdf");
const outputSections = resolve(scriptDir, "ehi-export-sections.json");
const outputSupplemental = resolve(scriptDir, "ehi-export-supplemental.json");
const outputStats = resolve(scriptDir, "extraction-stats.json");

// Extract text from PDF
const rawText = execSync(`pdftotext "${pdfPath}" -`, { maxBuffer: 10 * 1024 * 1024 }).toString();

// Split into pages (pdftotext uses form feed \f)
const pages = rawText.split("\f").map((p) => p.trim()).filter(Boolean);

// Remove page footers
const cleanPage = (text: string) =>
  text
    .replace(/© 2026 Lunar Systems, Inc\.\s*​?/g, "")
    .replace(/\n\s*\d+\s*$/g, "")
    .trim();

// Known C-CDA section names from the table of contents
const sectionNames = [
  "Patient Summary",
  "Allergies and Intolerances",
  "Problem List",
  "History of Medication Use",
  "Laboratory/Diagnostic Results",
  "Procedures",
  "Social History",
  "Functional Status",
  "Mental/Cognitive Status",
  "Vital Signs",
  "History of Encounters",
  "History of Immunizations",
  "Care Team",
  "Assessments",
  "Treatment Plan",
  "Clinical Notes",
  "Payers",
  "Participant",
  "Supplemental Data",
];

interface KeyElement {
  element: string;
  description: string;
}

interface CcdaSection {
  name: string;
  description: string;
  templateId: string | null;
  loincCode: string | null;
  loincDisplay: string | null;
  hasExampleXml: boolean;
  keyElements: KeyElement[];
  pageRange: string;
}

interface SupplementalField {
  field: string;
  description: string;
  dataType: string;
}

interface SupplementalCategory {
  category: string;
  fields: SupplementalField[];
}

// Find page boundaries for each section
function findSectionPages(): Array<{ name: string; startPage: number; endPage: number }> {
  const results: Array<{ name: string; startPage: number; endPage: number }> = [];

  for (let i = 0; i < sectionNames.length; i++) {
    const name = sectionNames[i];
    let startPage = -1;

    for (let p = 0; p < pages.length; p++) {
      const cleaned = cleanPage(pages[p]);
      // Look for the section name as a heading (at start of a cleaned page block)
      if (
        cleaned.startsWith(name) ||
        cleaned.includes(`\n${name}\n`) ||
        cleaned.match(new RegExp(`^\\s*${name.replace(/[/()]/g, "\\$&")}\\s*$`, "m"))
      ) {
        // Make sure we're past the table of contents
        if (p > 1) {
          startPage = p;
          break;
        }
      }
    }

    if (startPage !== -1) {
      // End page is the start of next section - 1, or last page
      let endPage = pages.length - 1;
      if (i + 1 < sectionNames.length) {
        const nextName = sectionNames[i + 1];
        for (let p = startPage + 1; p < pages.length; p++) {
          const cleaned = cleanPage(pages[p]);
          if (
            cleaned.startsWith(nextName) ||
            cleaned.includes(`\n${nextName}\n`) ||
            cleaned.match(new RegExp(`^\\s*${nextName.replace(/[/()]/g, "\\$&")}\\s*$`, "m"))
          ) {
            endPage = p - 1;
            break;
          }
        }
      }
      results.push({ name, startPage, endPage });
    }
  }

  return results;
}

// Extract key elements table from section text
function extractKeyElements(text: string): KeyElement[] {
  const elements: KeyElement[] = [];
  // Look for "Key elements" section
  const keyIdx = text.indexOf("Key elements");
  if (keyIdx === -1) return elements;

  const afterKey = text.substring(keyIdx);
  // Match element/description pairs - elements are XML tags in angle brackets
  const lines = afterKey.split("\n").map((l) => l.trim()).filter(Boolean);

  let currentElement = "";
  for (const line of lines) {
    if (line === "Element" || line === "Description" || line.startsWith("Key elements")) continue;
    // Check if this looks like an XML element name
    const elemMatch = line.match(/^<([a-zA-Z]+(?:\s*\(.*?\))?)>$/);
    if (elemMatch) {
      currentElement = line;
    } else if (currentElement && line.length > 5) {
      elements.push({ element: currentElement, description: line });
      currentElement = "";
    }
  }

  return elements;
}

// Extract templateId from section text
function extractTemplateId(text: string): string | null {
  const match = text.match(/<templateId root="([^"]+)"(?:\s+extension="([^"]+)")?/);
  if (match) return match[2] ? `${match[1]} (${match[2]})` : match[1];
  return null;
}

// Extract LOINC code from section metadata
function extractLoincCode(text: string): { code: string | null; display: string | null } {
  const match = text.match(/<code code="([^"]+)".*?codeSystem="2\.16\.840\.1\.113883\.6\.1".*?displayName="([^"]+)"/);
  if (match) return { code: match[1], display: match[2] };
  return { code: null, display: null };
}

// Extract supplemental data tables
function extractSupplemental(text: string): SupplementalCategory[] {
  const categories: SupplementalCategory[] = [];
  const categoryNames = ["Documents", "Orders", "Charges"];

  for (let i = 0; i < categoryNames.length; i++) {
    const catName = categoryNames[i];
    const catIdx = text.indexOf(`\n${catName}\n`);
    if (catIdx === -1) continue;

    const nextCatIdx =
      i + 1 < categoryNames.length
        ? text.indexOf(`\n${categoryNames[i + 1]}\n`, catIdx + 1)
        : text.length;
    const catText = text.substring(catIdx, nextCatIdx);

    const fields: SupplementalField[] = [];
    const lines = catText.split("\n").map((l) => l.trim()).filter(Boolean);

    // Parse field/description/datatype triples
    let idx = 0;
    // Skip header lines
    while (idx < lines.length && !lines[idx].match(/^Field$/)) idx++;
    idx++; // skip "Field"
    while (idx < lines.length && (lines[idx] === "Description" || lines[idx] === "Field Data Type")) idx++;

    while (idx < lines.length) {
      const field = lines[idx];
      if (!field || field === catName || field === "Field" || field === "Description") break;
      const desc = lines[idx + 1] || "";
      const dtype = lines[idx + 2] || "";
      // Validate: data type should be a known type
      if (["string", "boolean", "datetime", "date", "dict", "int", "float", "uuid", "array"].includes(dtype)) {
        fields.push({ field, description: desc, dataType: dtype });
        idx += 3;
      } else {
        // Multi-line description - try to find the data type
        let found = false;
        for (let j = idx + 2; j < Math.min(idx + 5, lines.length); j++) {
          if (["string", "boolean", "datetime", "date", "dict", "int", "float", "uuid", "array"].includes(lines[j])) {
            fields.push({
              field,
              description: lines.slice(idx + 1, j).join(" "),
              dataType: lines[j],
            });
            idx = j + 1;
            found = true;
            break;
          }
        }
        if (!found) idx++;
      }
    }

    categories.push({ category: catName, fields });
  }

  return categories;
}

// Main extraction
const sectionPages = findSectionPages();
const sections: CcdaSection[] = [];

for (const sp of sectionPages) {
  if (sp.name === "Supplemental Data") continue; // handle separately

  const sectionText = pages
    .slice(sp.startPage, sp.endPage + 1)
    .map(cleanPage)
    .join("\n");

  // Extract description - first paragraph after the section title
  const descMatch = sectionText.match(
    new RegExp(`${sp.name.replace(/[/()]/g, "\\$&")}\\s*\\n(.+?)\\n\\n`, "s")
  );
  const description = descMatch ? descMatch[1].replace(/\s+/g, " ").trim() : "";

  const templateId = extractTemplateId(sectionText);
  const loinc = extractLoincCode(sectionText);
  const keyElements = extractKeyElements(sectionText);

  sections.push({
    name: sp.name,
    description,
    templateId,
    loincCode: loinc.code,
    loincDisplay: loinc.display,
    hasExampleXml: sectionText.includes("Example XML"),
    keyElements,
    pageRange: `${sp.startPage + 1}-${sp.endPage + 1}`,
  });
}

// Extract supplemental data
const supplementalStartPage = sectionPages.find((s) => s.name === "Supplemental Data");
let supplementalCategories: SupplementalCategory[] = [];
if (supplementalStartPage) {
  const supplementalText = pages
    .slice(supplementalStartPage.startPage, supplementalStartPage.endPage + 1)
    .map(cleanPage)
    .join("\n");
  supplementalCategories = extractSupplemental(supplementalText);
}

// Write outputs
writeFileSync(
  outputSections,
  JSON.stringify(
    {
      document: {
        title: "Lunar Cloud Platform 2.6 — Electronic Health Information Export",
        date: "January 2026",
        pages: pages.length,
        format: "C-CDA XML with supplemental CSV",
        ccdaVersion: "CDA Release 4.1",
      },
      ccdaSections: sections,
    },
    null,
    2
  )
);

writeFileSync(
  outputSupplemental,
  JSON.stringify(
    {
      description:
        "Supplemental data exported as CSV files for data not captured in C-CDA. Three categories: documents, orders, charges.",
      categories: supplementalCategories,
    },
    null,
    2
  )
);

// Stats
const stats = {
  totalPages: pages.length,
  sectionsFound: sections.length,
  expectedSections: sectionNames.length - 1, // minus Supplemental Data which is separate
  supplementalCategories: supplementalCategories.length,
  totalSupplementalFields: supplementalCategories.reduce((s, c) => s + c.fields.length, 0),
  totalKeyElements: sections.reduce((s, c) => s + c.keyElements.length, 0),
  parseFailures: [] as string[],
};

// Check for missing sections
const foundNames = new Set(sections.map((s) => s.name));
for (const name of sectionNames) {
  if (name === "Supplemental Data") continue;
  if (!foundNames.has(name)) {
    stats.parseFailures.push(`Section not found: ${name}`);
  }
}

writeFileSync(outputStats, JSON.stringify(stats, null, 2));

console.log(`Extracted ${sections.length} C-CDA sections`);
console.log(`Extracted ${supplementalCategories.length} supplemental categories with ${stats.totalSupplementalFields} fields`);
console.log(`Total key elements documented: ${stats.totalKeyElements}`);
if (stats.parseFailures.length > 0) {
  console.log(`Parse failures: ${stats.parseFailures.join(", ")}`);
}

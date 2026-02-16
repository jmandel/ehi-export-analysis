#!/usr/bin/env bun
/**
 * Extract structured field definitions from the MEDENT ASCII Field List HTML page.
 * This page documents 750 financial/billing/scheduling data export fields.
 *
 * Usage: bun run extract-ascii-fields.ts
 *
 * Input: ../asciifieldlistinter.html
 * Output: ./ascii-field-list.json
 */

import { join } from "node:path";

const HTML_FILE = join(import.meta.dir, "..", "asciifieldlistinter.html");
const OUT_FILE = join(import.meta.dir, "ascii-field-list.json");

interface AsciiField {
  format_number: string;
  area: string;
  area_description: string;
  name: string;
  notes: string;
}

const AREA_DESCRIPTIONS: Record<string, string> = {
  A: "Activity file data (financial charges)",
  CC: "Immunization/Injection CPT Codes",
  DI: "Diagnostic Imaging",
  H: "History record",
  HA: "History/Activity financial data",
  I: "Immunization data",
  L: "Lab data",
  O: "Orders",
  OA: "Appointment/Scheduling data",
  P: "Patient data",
  PI: "Practice Information",
  PP: "Primary Patient data",
  R: "Referral",
  RC: "Recall",
  RD: "Referring Doctor",
  SB: "Surgical Booking",
};

async function main() {
  const html = await Bun.file(HTML_FILE).text();

  // Parse table rows using regex since this is a simple table structure
  // Look for <tr> containing <td> elements
  const rowPattern =
    /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
  const cellPattern = /<td[^>]*>([\s\S]*?)<\/td>/gi;
  const tagStrip = /<[^>]*>/g;

  const fields: AsciiField[] = [];
  let match;

  while ((match = rowPattern.exec(html)) !== null) {
    const rowHtml = match[1];
    const cells: string[] = [];
    let cellMatch;

    // Reset lastIndex for cell pattern
    cellPattern.lastIndex = 0;
    while ((cellMatch = cellPattern.exec(rowHtml)) !== null) {
      const text = cellMatch[1].replace(tagStrip, "").replace(/&[^;]+;/g, " ").trim();
      cells.push(text);
    }

    if (cells.length >= 3) {
      const formatNum = cells[0].trim();
      const area = cells[1].trim();
      const name = cells[2].trim();
      const notes = cells[3]?.trim() || "";

      // Skip header row and empty rows
      if (formatNum === "Format Number" || !formatNum || !name) continue;
      // Skip non-numeric format numbers (navigation rows)
      if (!/^\d+$/.test(formatNum)) continue;

      fields.push({
        format_number: formatNum,
        area,
        area_description: AREA_DESCRIPTIONS[area] || area,
        name,
        notes,
      });
    }
  }

  // Group by area for summary
  const byArea: Record<string, number> = {};
  for (const f of fields) {
    byArea[f.area] = (byArea[f.area] || 0) + 1;
  }

  const output = {
    source: "https://www.medent.com/htmlmanual/html/v237/asciifieldlistinter.html",
    description:
      "MEDENT ASCII Field List - fields available for financial/billing data export via the Data Export Module",
    total_fields: fields.length,
    fields_by_area: byArea,
    area_descriptions: AREA_DESCRIPTIONS,
    fields,
  };

  await Bun.write(OUT_FILE, JSON.stringify(output, null, 2));
  console.log(`Extracted ${fields.length} fields`);
  console.log("Fields by area:", byArea);
  console.log(`Wrote ${OUT_FILE}`);
}

main();

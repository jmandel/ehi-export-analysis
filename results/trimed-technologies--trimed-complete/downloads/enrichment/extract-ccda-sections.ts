#!/usr/bin/env bun
/**
 * extract-ccda-sections.ts
 *
 * Parses the C-CDA XML sample responses from the Patient Data API to
 * extract structured information about the sections, templates, and
 * data elements contained in the export format.
 *
 * Input:  ../xml-samples/*.xml
 * Output: ccda-sections.json
 */

import { readFileSync, writeFileSync, readdirSync } from "fs";
import { join, dirname } from "path";

const ROOT = dirname(new URL(import.meta.url).pathname);
const XML_DIR = join(ROOT, "..", "xml-samples");

interface CcdaSection {
  title: string;
  templateIds: string[];
  codeSystem: string;
  code: string;
  displayName: string;
}

interface XmlSample {
  filename: string;
  sizeBytes: number;
  documentTitle: string | null;
  sections: CcdaSection[];
  templateIds: string[];
}

const samples: XmlSample[] = [];
let totalFiles = 0;
let parsedFiles = 0;
const failures: { file: string; error: string }[] = [];

const files = readdirSync(XML_DIR).filter((f) => f.endsWith(".xml"));
totalFiles = files.length;

for (const file of files) {
  try {
    const content = readFileSync(join(XML_DIR, file), "utf-8");
    const sizeBytes = Buffer.byteLength(content);

    // Extract document title
    const titleMatch = content.match(/<title>(.*?)<\/title>/i);
    const docTitle = titleMatch ? titleMatch[1].trim() : null;

    // Extract root template IDs
    const rootTemplates: string[] = [];
    const rootTplMatches = content.match(
      /<templateId[^>]*root="([^"]+)"[^>]*\/?\s*>/gi
    );
    if (rootTplMatches) {
      for (const m of rootTplMatches) {
        const rootMatch = m.match(/root="([^"]+)"/);
        if (rootMatch) rootTemplates.push(rootMatch[1]);
      }
    }

    // Extract sections from component/section elements
    const sections: CcdaSection[] = [];
    const sectionRegex =
      /<component>\s*<section>([\s\S]*?)<\/section>\s*<\/component>/gi;
    let sectionMatch;
    while ((sectionMatch = sectionRegex.exec(content))) {
      const sectionContent = sectionMatch[1];

      const secTitle = sectionContent.match(/<title>(.*?)<\/title>/i);
      const secCode = sectionContent.match(
        /<code\s+([^>]+)\/?>/i
      );

      const templateIds: string[] = [];
      const tplMatches = sectionContent.match(
        /<templateId[^>]*root="([^"]+)"[^>]*\/?>/gi
      );
      if (tplMatches) {
        for (const m of tplMatches) {
          const r = m.match(/root="([^"]+)"/);
          if (r) templateIds.push(r[1]);
        }
      }

      let code = "";
      let displayName = "";
      let codeSystem = "";
      if (secCode) {
        const codeAttr = secCode[1].match(/code="([^"]+)"/);
        const dispAttr = secCode[1].match(/displayName="([^"]+)"/);
        const sysAttr = secCode[1].match(/codeSystem="([^"]+)"/);
        code = codeAttr ? codeAttr[1] : "";
        displayName = dispAttr ? dispAttr[1] : "";
        codeSystem = sysAttr ? sysAttr[1] : "";
      }

      sections.push({
        title: secTitle ? secTitle[1].trim() : "Unknown",
        templateIds,
        code,
        displayName,
        codeSystem,
      });
    }

    samples.push({
      filename: file,
      sizeBytes,
      documentTitle: docTitle,
      sections,
      templateIds: [...new Set(rootTemplates)],
    });
    parsedFiles++;
  } catch (e: any) {
    failures.push({ file, error: e.message });
  }
}

const output = {
  source: "XML sample responses from Patient Data API",
  totalFiles,
  parsedFiles,
  parseFailures: failures,
  samples,
};

writeFileSync(
  join(ROOT, "ccda-sections.json"),
  JSON.stringify(output, null, 2)
);

console.log(`Total files discovered: ${totalFiles}`);
console.log(`Total files parsed: ${parsedFiles}`);
console.log(`Parse failures: ${failures.length}`);
if (failures.length > 0) {
  for (const f of failures) {
    console.log(`  FAIL: ${f.file} — ${f.error}`);
  }
}
for (const s of samples) {
  console.log(`\n${s.filename}: ${s.sections.length} sections`);
  for (const sec of s.sections) {
    console.log(`  - ${sec.title} (${sec.code || "no code"})`);
  }
}

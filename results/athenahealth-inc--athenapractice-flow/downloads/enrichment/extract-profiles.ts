#!/usr/bin/env bun
/**
 * Extract structured data from athenahealth FHIR IG StructureDefinition JSON files.
 * Produces a queryable JSON catalog of all profiles, their elements, extensions,
 * value sets, and relationships.
 *
 * Usage: bun run extract-profiles.ts
 * Input: ../definitions/StructureDefinition-athena-*-profile.json
 * Output: profiles-catalog.json, coverage-accounting.json
 */

import { readdir, readFile, writeFile } from "fs/promises";
import { join } from "path";

const DEFINITIONS_DIR = join(import.meta.dir, "..", "definitions");
const OUTPUT_DIR = import.meta.dir;

interface ElementInfo {
  path: string;
  short: string;
  definition: string;
  types: string[];
  min: number;
  max: string;
  binding?: {
    strength: string;
    valueSet: string;
  };
  extensions: string[];
  isCustom: boolean;
}

interface ProfileInfo {
  id: string;
  name: string;
  title: string;
  description: string;
  kind: string;
  type: string;
  baseDefinition: string;
  isCustomResource: boolean;
  url: string;
  version: string;
  status: string;
  date: string;
  elementCount: number;
  elements: ElementInfo[];
  extensions: string[];
  references: string[];
  category: "system" | "clinical" | "practice-management" | "custom" | "unknown";
}

function categorizeResource(name: string, kind: string, type: string): ProfileInfo["category"] {
  const systemResources = ["Location", "Medication", "Organization", "Practitioner",
    "PractitionerRole", "OperationOutcome", "AuditEvent", "ConceptMap", "Endpoint",
    "List", "NamingSystem", "OperationDefinition", "Subscription", "ValueSet", "Provenance"];
  const pmResources = ["Account", "Appointment", "Coverage", "Patient", "RelatedPerson",
    "Schedule", "Slot", "Posting"];
  const customResources = ["Adjustment", "BillingStatement", "Charge", "Claim",
    "Collection", "Deductible", "Eligibility", "PatientInsurance", "Payment"];

  if (kind === "logical") return "custom";
  const shortType = type.split("/").pop() || "";
  if (customResources.some(c => name.includes(c) || shortType.includes(c))) return "custom";
  if (pmResources.some(c => shortType === c || name.replace("Athena", "") === c)) return "practice-management";
  if (systemResources.some(c => shortType === c || name.replace("Athena", "") === c)) return "system";
  return "clinical";
}

async function extractProfile(filePath: string): Promise<ProfileInfo | null> {
  try {
    const raw = await readFile(filePath, "utf-8");
    const sd = JSON.parse(raw);

    const kind = sd.kind || "unknown";
    const type = sd.type || "unknown";
    const name = sd.name || "";
    const isCustom = kind === "logical";

    const snapshot = sd.snapshot?.element || [];
    const elements: ElementInfo[] = snapshot.map((el: any) => {
      const types = (el.type || []).map((t: any) => t.code);
      const extensions = (el.type || [])
        .filter((t: any) => t.code === "Extension")
        .flatMap((t: any) => t.profile || []);

      return {
        path: el.path,
        short: el.short || "",
        definition: el.definition || "",
        types,
        min: el.min ?? 0,
        max: el.max || "*",
        binding: el.binding ? {
          strength: el.binding.strength,
          valueSet: el.binding.valueSet || "",
        } : undefined,
        extensions,
        isCustom: !el.path.includes(".") ? false : !type.startsWith("http") ? false : true,
      };
    });

    // Collect all referenced resources
    const references: string[] = [];
    for (const el of snapshot) {
      for (const t of el.type || []) {
        if (t.code === "Reference") {
          for (const tp of t.targetProfile || []) {
            references.push(tp);
          }
        }
      }
    }

    // Collect all extensions used
    const allExtensions: string[] = [];
    for (const el of snapshot) {
      if (el.path.endsWith(".extension") && el.sliceName) {
        for (const t of el.type || []) {
          for (const p of t.profile || []) {
            allExtensions.push(p);
          }
        }
      }
    }

    return {
      id: sd.id || "",
      name,
      title: sd.title || "",
      description: sd.description || "",
      kind,
      type: type.split("/").pop() || type,
      baseDefinition: sd.baseDefinition || "",
      isCustomResource: isCustom,
      url: sd.url || "",
      version: sd.version || "",
      status: sd.status || "",
      date: sd.date || "",
      elementCount: elements.length,
      elements,
      extensions: [...new Set(allExtensions)],
      references: [...new Set(references)],
      category: categorizeResource(name, kind, type),
    };
  } catch (e) {
    console.error(`Failed to parse ${filePath}: ${e}`);
    return null;
  }
}

async function main() {
  const files = (await readdir(DEFINITIONS_DIR))
    .filter(f => f.match(/^StructureDefinition-athena-.*-profile\.json$/))
    .sort();

  console.log(`Found ${files.length} profile files`);

  const profiles: ProfileInfo[] = [];
  const failures: { file: string; error: string }[] = [];

  for (const file of files) {
    const result = await extractProfile(join(DEFINITIONS_DIR, file));
    if (result) {
      profiles.push(result);
    } else {
      failures.push({ file, error: "parse failure" });
    }
  }

  // Write profiles catalog
  await writeFile(
    join(OUTPUT_DIR, "profiles-catalog.json"),
    JSON.stringify(profiles, null, 2)
  );

  // Generate coverage accounting
  const accounting = {
    totalFilesDiscovered: files.length,
    totalFilesParsed: profiles.length,
    parseFailures: failures,
    summary: {
      byCategory: {
        system: profiles.filter(p => p.category === "system").map(p => p.name),
        clinical: profiles.filter(p => p.category === "clinical").map(p => p.name),
        practiceManagement: profiles.filter(p => p.category === "practice-management").map(p => p.name),
        custom: profiles.filter(p => p.category === "custom").map(p => p.name),
      },
      totalElements: profiles.reduce((sum, p) => sum + p.elementCount, 0),
      customResourceCount: profiles.filter(p => p.isCustomResource).length,
      standardResourceCount: profiles.filter(p => !p.isCustomResource).length,
      profilesWithBindings: profiles.filter(p =>
        p.elements.some(e => e.binding)
      ).length,
      profilesWithExtensions: profiles.filter(p => p.extensions.length > 0).length,
    },
  };

  await writeFile(
    join(OUTPUT_DIR, "coverage-accounting.json"),
    JSON.stringify(accounting, null, 2)
  );

  console.log(`Extracted ${profiles.length} profiles`);
  console.log(`  System: ${accounting.summary.byCategory.system.length}`);
  console.log(`  Clinical: ${accounting.summary.byCategory.clinical.length}`);
  console.log(`  Practice Management: ${accounting.summary.byCategory.practiceManagement.length}`);
  console.log(`  Custom: ${accounting.summary.byCategory.custom.length}`);
  console.log(`  Total elements: ${accounting.summary.totalElements}`);
  console.log(`  Parse failures: ${failures.length}`);
}

main().catch(console.error);

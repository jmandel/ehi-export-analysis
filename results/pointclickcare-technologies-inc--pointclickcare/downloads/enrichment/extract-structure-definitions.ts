#!/usr/bin/env bun
/**
 * extract-structure-definitions.ts
 *
 * Parses all StructureDefinition JSON files from the PCC EHI Export IG package
 * and produces a single queryable JSON file with:
 *   - All resource profiles and their elements
 *   - All extensions
 *   - All custom (non-FHIR) resources
 *   - Value sets and code systems
 *   - Coverage accounting
 */

import { readdir, readFile, writeFile } from "fs/promises";
import { join } from "path";

const PACKAGE_DIR = join(import.meta.dir, "..", "package", "package");
const OUTPUT_FILE = join(import.meta.dir, "structure-definitions.json");

interface ElementInfo {
  path: string;
  short: string;
  definition: string;
  types: string[];
  min: number;
  max: string;
  binding?: {
    strength: string;
    valueSet?: string;
  };
}

interface ProfileInfo {
  id: string;
  name: string;
  type: string;
  kind: string;
  description: string;
  url: string;
  baseDefinition?: string;
  status: string;
  isCustomResource: boolean;
  elements: ElementInfo[];
  extensions: string[];
}

interface ValueSetInfo {
  id: string;
  name: string;
  url: string;
  concepts: { code: string; display: string }[];
}

interface CodeSystemInfo {
  id: string;
  name: string;
  url: string;
  concepts: { code: string; display: string; definition?: string }[];
}

interface Output {
  extractionDate: string;
  igPackage: string;
  igVersion: string;
  fhirVersion: string;
  profiles: ProfileInfo[];
  valueSets: ValueSetInfo[];
  codeSystems: CodeSystemInfo[];
  accounting: {
    totalFiles: number;
    parsedFiles: number;
    parseFailures: { file: string; error: string }[];
    profileCount: number;
    extensionCount: number;
    customResourceCount: number;
    standardResourceCount: number;
    valueSetCount: number;
    codeSystemCount: number;
  };
}

async function main() {
  const files = await readdir(PACKAGE_DIR);
  const jsonFiles = files.filter((f) => f.endsWith(".json"));

  const profiles: ProfileInfo[] = [];
  const valueSets: ValueSetInfo[] = [];
  const codeSystems: CodeSystemInfo[] = [];
  const failures: { file: string; error: string }[] = [];
  let parsed = 0;

  for (const file of jsonFiles) {
    try {
      const content = await readFile(join(PACKAGE_DIR, file), "utf-8");
      const resource = JSON.parse(content);
      parsed++;

      if (resource.resourceType === "StructureDefinition") {
        const snap = resource.snapshot?.element || [];
        const diff = resource.differential?.element || [];

        const elements: ElementInfo[] = snap
          .filter((el: any) => el.path?.includes("."))
          .map((el: any) => ({
            path: el.path,
            short: el.short || "",
            definition: el.definition || "",
            types: (el.type || []).map((t: any) => t.code),
            min: el.min ?? 0,
            max: el.max || "*",
            ...(el.binding
              ? {
                  binding: {
                    strength: el.binding.strength,
                    valueSet: el.binding.valueSet,
                  },
                }
              : {}),
          }));

        // Detect custom resources: kind=resource but type is not a standard FHIR R4 type
        const standardFhirTypes = new Set([
          "AllergyIntolerance", "CarePlan", "CareTeam", "Condition", "Coverage",
          "DiagnosticReport", "DocumentReference", "Encounter", "FamilyMemberHistory",
          "Goal", "Immunization", "Device", "Location", "Medication",
          "MedicationDispense", "MedicationRequest", "Observation", "Organization",
          "Patient", "Practitioner", "PractitionerRole", "Procedure", "Provenance",
          "RelatedPerson", "ServiceRequest", "Specimen",
        ]);

        const isCustom =
          resource.kind === "resource" &&
          !standardFhirTypes.has(resource.type) &&
          resource.type !== "Extension";

        const extensionUrls = diff
          .filter((el: any) =>
            el.type?.some((t: any) => t.code === "Extension" && t.profile)
          )
          .flatMap((el: any) =>
            el.type
              ?.filter((t: any) => t.code === "Extension")
              .flatMap((t: any) => t.profile || [])
          );

        profiles.push({
          id: resource.id,
          name: resource.name,
          type: resource.type,
          kind: resource.kind,
          description: (resource.description || "").replace(/<[^>]*>/g, "").trim(),
          url: resource.url,
          baseDefinition: resource.baseDefinition,
          status: resource.status,
          isCustomResource: isCustom,
          elements: elements.filter(
            (el) => el.path.split(".").length <= 3
          ),
          extensions: extensionUrls,
        });
      } else if (resource.resourceType === "ValueSet") {
        const concepts: { code: string; display: string }[] = [];
        for (const inc of resource.compose?.include || []) {
          for (const c of inc.concept || []) {
            concepts.push({ code: c.code, display: c.display || "" });
          }
        }
        valueSets.push({
          id: resource.id,
          name: resource.name,
          url: resource.url,
          concepts,
        });
      } else if (resource.resourceType === "CodeSystem") {
        const concepts = (resource.concept || []).map((c: any) => ({
          code: c.code,
          display: c.display || "",
          definition: c.definition,
        }));
        codeSystems.push({
          id: resource.id,
          name: resource.name,
          url: resource.url,
          concepts,
        });
      }
    } catch (e: any) {
      failures.push({ file, error: e.message });
    }
  }

  const extensionProfiles = profiles.filter((p) => p.kind === "complex-type" || p.type === "Extension");
  const customResources = profiles.filter((p) => p.isCustomResource);
  const standardResources = profiles.filter(
    (p) => p.kind === "resource" && !p.isCustomResource && p.type !== "Extension"
  );

  const output: Output = {
    extractionDate: new Date().toISOString().split("T")[0],
    igPackage: "ehi-export.pointclickcare.com#0.1.0",
    igVersion: "0.1.0",
    fhirVersion: "4.0.1",
    profiles,
    valueSets,
    codeSystems,
    accounting: {
      totalFiles: jsonFiles.length,
      parsedFiles: parsed,
      parseFailures: failures,
      profileCount: profiles.length,
      extensionCount: extensionProfiles.length,
      customResourceCount: customResources.length,
      standardResourceCount: standardResources.length,
      valueSetCount: valueSets.length,
      codeSystemCount: codeSystems.length,
    },
  };

  await writeFile(OUTPUT_FILE, JSON.stringify(output, null, 2));
  console.log(`Extracted ${profiles.length} profiles, ${valueSets.length} value sets, ${codeSystems.length} code systems`);
  console.log(`Custom resources: ${customResources.map((p) => p.type).join(", ")}`);
  console.log(`Standard resource profiles: ${standardResources.map((p) => p.type).join(", ")}`);
  console.log(`Extensions: ${extensionProfiles.length}`);
  console.log(`Parse failures: ${failures.length}`);
  if (failures.length > 0) {
    for (const f of failures) {
      console.log(`  FAIL: ${f.file} - ${f.error}`);
    }
  }
}

main().catch(console.error);

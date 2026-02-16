#!/usr/bin/env bun
/**
 * Extract structured data from athenahealth FHIR IG example JSON files.
 * Produces a queryable JSON summary of all example resources, their types,
 * and key characteristics.
 *
 * Usage: bun run extract-examples.ts
 * Input: ../examples/*.json
 * Output: examples-catalog.json
 */

import { readdir, readFile, writeFile } from "fs/promises";
import { join } from "path";

const EXAMPLES_DIR = join(import.meta.dir, "..", "examples");
const OUTPUT_DIR = import.meta.dir;

interface ExampleInfo {
  file: string;
  resourceType: string;
  id: string;
  meta?: {
    profile?: string[];
    lastUpdated?: string;
  };
  topLevelKeys: string[];
  sizeBytes: number;
  isBundle: boolean;
  bundleEntryCount?: number;
  description?: string;
}

async function extractExample(filePath: string, fileName: string): Promise<ExampleInfo | null> {
  try {
    const raw = await readFile(filePath, "utf-8");
    const resource = JSON.parse(raw);

    const info: ExampleInfo = {
      file: fileName,
      resourceType: resource.resourceType || "unknown",
      id: resource.id || "",
      meta: resource.meta ? {
        profile: resource.meta.profile,
        lastUpdated: resource.meta.lastUpdated,
      } : undefined,
      topLevelKeys: Object.keys(resource),
      sizeBytes: raw.length,
      isBundle: resource.resourceType === "Bundle",
    };

    if (info.isBundle && resource.entry) {
      info.bundleEntryCount = resource.entry.length;
    }

    // For CapabilityStatement, summarize resource types
    if (resource.resourceType === "CapabilityStatement") {
      const rest = resource.rest?.[0];
      if (rest?.resource) {
        info.description = `CapabilityStatement with ${rest.resource.length} resource types`;
      }
    }

    return info;
  } catch (e) {
    console.error(`Failed to parse ${filePath}: ${e}`);
    return null;
  }
}

async function main() {
  const files = (await readdir(EXAMPLES_DIR))
    .filter(f => f.endsWith(".json"))
    .sort();

  console.log(`Found ${files.length} example files`);

  const examples: ExampleInfo[] = [];
  const failures: { file: string; error: string }[] = [];

  for (const file of files) {
    const result = await extractExample(join(EXAMPLES_DIR, file), file);
    if (result) {
      examples.push(result);
    } else {
      failures.push({ file, error: "parse failure" });
    }
  }

  // Group by resource type
  const byType: Record<string, number> = {};
  for (const ex of examples) {
    byType[ex.resourceType] = (byType[ex.resourceType] || 0) + 1;
  }

  const output = {
    totalFiles: files.length,
    totalParsed: examples.length,
    parseFailures: failures,
    byResourceType: byType,
    examples,
  };

  await writeFile(
    join(OUTPUT_DIR, "examples-catalog.json"),
    JSON.stringify(output, null, 2)
  );

  console.log(`Extracted ${examples.length} examples`);
  console.log("By resource type:");
  for (const [type, count] of Object.entries(byType).sort()) {
    console.log(`  ${type}: ${count}`);
  }
  console.log(`Parse failures: ${failures.length}`);
}

main().catch(console.error);

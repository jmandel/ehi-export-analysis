#!/usr/bin/env bun
/**
 * Extracts structured information from the MDOps CCD XML Schema files.
 * Parses all 4 XSD files and emits queryable JSON with:
 * - Complex types and their elements
 * - Simple types (value sets/enumerations)
 * - Coverage/accounting stats
 */

import { readFileSync, writeFileSync, readdirSync } from "fs";
import { join, basename } from "path";

const DOWNLOADS_DIR = join(import.meta.dir, "..");
const OUTPUT_DIR = import.meta.dir;

interface SchemaElement {
  name: string;
  type: string | null;
  minOccurs: string | null;
  maxOccurs: string | null;
  fixed: string | null;
}

interface SchemaAttribute {
  name: string;
  type: string | null;
  use: string | null;
  fixed: string | null;
}

interface ComplexType {
  name: string;
  source_file: string;
  elements: SchemaElement[];
  attributes: SchemaAttribute[];
  mixed: boolean;
  documentation: string | null;
}

interface SimpleType {
  name: string;
  source_file: string;
  restriction_base: string | null;
  enumeration_values: string[];
}

interface SchemaInfo {
  file: string;
  target_namespace: string | null;
  includes: string[];
  complex_types: ComplexType[];
  simple_types: SimpleType[];
}

function extractAttr(element: string, attr: string): string | null {
  const re = new RegExp(`${attr}="([^"]*)"`, "i");
  const m = element.match(re);
  return m ? m[1] : null;
}

function parseSchema(filePath: string): SchemaInfo {
  const content = readFileSync(filePath, "utf-8");
  const fileName = basename(filePath);

  const targetNs = extractAttr(content.match(/<xs:schema[^>]*>/)?.[0] || "", "targetNamespace");

  // Extract includes
  const includes: string[] = [];
  for (const m of content.matchAll(/<xs:include\s+schemaLocation="([^"]*)"/g)) {
    includes.push(m[1]);
  }

  // Extract complex types
  const complexTypes: ComplexType[] = [];
  const ctRegex = /<xs:complexType\s+name="([^"]*)"([^>]*)>([\s\S]*?)(?=<xs:complexType\s|<\/xs:schema)/g;
  for (const m of content.matchAll(ctRegex)) {
    const name = m[1];
    const attrs = m[2];
    const body = m[3];
    const mixed = /mixed="true"/.test(attrs);

    const elements: SchemaElement[] = [];
    for (const el of body.matchAll(/<xs:element\s+([^>]*?)\/?>(?:<\/xs:element>)?/g)) {
      const elStr = el[1];
      elements.push({
        name: extractAttr(elStr, "name") || "",
        type: extractAttr(elStr, "type"),
        minOccurs: extractAttr(elStr, "minOccurs"),
        maxOccurs: extractAttr(elStr, "maxOccurs"),
        fixed: extractAttr(elStr, "fixed"),
      });
    }

    const attributes: SchemaAttribute[] = [];
    for (const at of body.matchAll(/<xs:attribute\s+([^>]*?)\/?>(?:<\/xs:attribute>)?/g)) {
      const atStr = at[1];
      attributes.push({
        name: extractAttr(atStr, "name") || "",
        type: extractAttr(atStr, "type"),
        use: extractAttr(atStr, "use"),
        fixed: extractAttr(atStr, "fixed"),
      });
    }

    const docMatch = body.match(/<xs:documentation>([\s\S]*?)<\/xs:documentation>/);
    const documentation = docMatch ? docMatch[1].trim() : null;

    complexTypes.push({
      name,
      source_file: fileName,
      elements,
      attributes,
      mixed,
      documentation,
    });
  }

  // Extract simple types
  const simpleTypes: SimpleType[] = [];
  const stRegex = /<xs:simpleType\s+name="([^"]*)"[^>]*>([\s\S]*?)(?=<xs:simpleType\s|<\/xs:schema)/g;
  for (const m of content.matchAll(stRegex)) {
    const name = m[1];
    const body = m[2];

    const baseMatch = body.match(/<xs:restriction\s+base="([^"]*)"/);
    const restrictionBase = baseMatch ? baseMatch[1] : null;

    const enumValues: string[] = [];
    for (const ev of body.matchAll(/<xs:enumeration\s+value="([^"]*)"/g)) {
      enumValues.push(ev[1]);
    }

    simpleTypes.push({
      name,
      source_file: fileName,
      restriction_base: restrictionBase,
      enumeration_values: enumValues,
    });
  }

  return {
    file: fileName,
    target_namespace: targetNs,
    includes,
    complex_types: complexTypes,
    simple_types: simpleTypes,
  };
}

// Find all XML schema files
const xmlFiles = readdirSync(DOWNLOADS_DIR)
  .filter((f) => f.endsWith("-schema.xml"))
  .map((f) => join(DOWNLOADS_DIR, f));

const results: {
  extraction_date: string;
  schemas: SchemaInfo[];
  summary: {
    total_files: number;
    total_complex_types: number;
    total_simple_types: number;
    total_elements_across_types: number;
    total_enumeration_values: number;
    parse_failures: { file: string; error: string }[];
  };
} = {
  extraction_date: new Date().toISOString(),
  schemas: [],
  summary: {
    total_files: xmlFiles.length,
    total_complex_types: 0,
    total_simple_types: 0,
    total_elements_across_types: 0,
    total_enumeration_values: 0,
    parse_failures: [],
  },
};

for (const file of xmlFiles) {
  try {
    const schema = parseSchema(file);
    results.schemas.push(schema);
    results.summary.total_complex_types += schema.complex_types.length;
    results.summary.total_simple_types += schema.simple_types.length;
    results.summary.total_elements_across_types += schema.complex_types.reduce(
      (sum, ct) => sum + ct.elements.length,
      0
    );
    results.summary.total_enumeration_values += schema.simple_types.reduce(
      (sum, st) => sum + st.enumeration_values.length,
      0
    );
  } catch (e: any) {
    results.summary.parse_failures.push({
      file: basename(file),
      error: e.message,
    });
  }
}

const outputPath = join(OUTPUT_DIR, "schema-extract.json");
writeFileSync(outputPath, JSON.stringify(results, null, 2));

console.log("Extraction complete:");
console.log(`  Files processed: ${results.schemas.length}/${xmlFiles.length}`);
console.log(`  Complex types: ${results.summary.total_complex_types}`);
console.log(`  Simple types: ${results.summary.total_simple_types}`);
console.log(`  Elements across types: ${results.summary.total_elements_across_types}`);
console.log(`  Enumeration values: ${results.summary.total_enumeration_values}`);
console.log(`  Parse failures: ${results.summary.parse_failures.length}`);
console.log(`  Output: ${outputPath}`);

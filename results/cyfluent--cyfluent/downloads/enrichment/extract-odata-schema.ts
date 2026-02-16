#!/usr/bin/env bun
/**
 * Extracts entity types, properties, navigation properties, and relationships
 * from Cyfluent's OData metadata XML (EDMX format) into queryable JSON.
 *
 * Usage: bun run extract-odata-schema.ts
 * Input:  ../OdataMetadata.xml
 * Output: odata-schema.json, odata-schema-summary.json
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";

const scriptDir = dirname(new URL(import.meta.url).pathname);
const inputPath = join(scriptDir, "..", "OdataMetadata.xml");
const outputPath = join(scriptDir, "odata-schema.json");
const summaryPath = join(scriptDir, "odata-schema-summary.json");

const xml = readFileSync(inputPath, "utf-8");

interface Property {
  name: string;
  type: string;
  nullable: boolean;
  maxLength?: string;
  fixedLength?: boolean;
  unicode?: boolean;
  precision?: number;
}

interface NavigationProperty {
  name: string;
  relationship: string;
  toRole: string;
  fromRole: string;
}

interface EntityType {
  name: string;
  keyProperties: string[];
  properties: Property[];
  navigationProperties: NavigationProperty[];
}

interface Association {
  name: string;
  ends: Array<{
    type: string;
    multiplicity: string;
    role: string;
  }>;
  referentialConstraint?: {
    principal: { role: string; propertyRef: string };
    dependent: { role: string; propertyRef: string };
  };
}

// Parse using regex since the XML is on a single line and we need specific elements
function extractEntityTypes(): EntityType[] {
  const entities: EntityType[] = [];
  const entityRegex = /<EntityType Name="([^"]+)">(.*?)<\/EntityType>/gs;
  let match;

  while ((match = entityRegex.exec(xml)) !== null) {
    const name = match[1];
    const body = match[2];

    // Extract key properties
    const keyProps: string[] = [];
    const keyRegex = /<PropertyRef Name="([^"]+)"/g;
    let keyMatch;
    while ((keyMatch = keyRegex.exec(body)) !== null) {
      keyProps.push(keyMatch[1]);
    }

    // Extract properties
    const properties: Property[] = [];
    const propRegex =
      /<Property Name="([^"]+)" Type="([^"]+)"([^/]*?)\/>/g;
    let propMatch;
    while ((propMatch = propRegex.exec(body)) !== null) {
      const attrs = propMatch[3];
      const prop: Property = {
        name: propMatch[1],
        type: propMatch[2],
        nullable: !attrs.includes('Nullable="false"'),
      };
      const maxLenMatch = attrs.match(/MaxLength="([^"]+)"/);
      if (maxLenMatch) prop.maxLength = maxLenMatch[1];
      const fixedMatch = attrs.match(/FixedLength="([^"]+)"/);
      if (fixedMatch) prop.fixedLength = fixedMatch[1] === "true";
      const unicodeMatch = attrs.match(/Unicode="([^"]+)"/);
      if (unicodeMatch) prop.unicode = unicodeMatch[1] === "true";
      const precisionMatch = attrs.match(/Precision="([^"]+)"/);
      if (precisionMatch) prop.precision = parseInt(precisionMatch[1]);
      properties.push(prop);
    }

    // Extract navigation properties
    const navProps: NavigationProperty[] = [];
    const navRegex =
      /<NavigationProperty Name="([^"]+)" Relationship="([^"]+)" ToRole="([^"]+)" FromRole="([^"]+)"[^/]*\/>/g;
    let navMatch;
    while ((navMatch = navRegex.exec(body)) !== null) {
      navProps.push({
        name: navMatch[1],
        relationship: navMatch[2],
        toRole: navMatch[3],
        fromRole: navMatch[4],
      });
    }

    entities.push({
      name,
      keyProperties: keyProps,
      properties,
      navigationProperties: navProps,
    });
  }

  return entities;
}

function extractAssociations(): Association[] {
  const associations: Association[] = [];
  const assocRegex = /<Association Name="([^"]+)">(.*?)<\/Association>/gs;
  let match;

  while ((match = assocRegex.exec(xml)) !== null) {
    const name = match[1];
    const body = match[2];

    const ends: Association["ends"] = [];
    const endRegex =
      /<End Type="([^"]+)" Multiplicity="([^"]+)" Role="([^"]+)"[^/]*\/>/g;
    let endMatch;
    while ((endMatch = endRegex.exec(body)) !== null) {
      ends.push({
        type: endMatch[1],
        multiplicity: endMatch[2],
        role: endMatch[3],
      });
    }

    let refConstraint: Association["referentialConstraint"];
    const principalMatch = body.match(
      /<Principal Role="([^"]+)"[^>]*>.*?<PropertyRef Name="([^"]+)"/s
    );
    const dependentMatch = body.match(
      /<Dependent Role="([^"]+)"[^>]*>.*?<PropertyRef Name="([^"]+)"/s
    );
    if (principalMatch && dependentMatch) {
      refConstraint = {
        principal: {
          role: principalMatch[1],
          propertyRef: principalMatch[2],
        },
        dependent: {
          role: dependentMatch[1],
          propertyRef: dependentMatch[2],
        },
      };
    }

    associations.push({ name, ends, referentialConstraint: refConstraint });
  }

  return associations;
}

function extractEntitySets(): Array<{ name: string; entityType: string }> {
  const sets: Array<{ name: string; entityType: string }> = [];
  const setRegex = /<EntitySet Name="([^"]+)" EntityType="([^"]+)"/g;
  let match;
  while ((match = setRegex.exec(xml)) !== null) {
    sets.push({ name: match[1], entityType: match[2] });
  }
  return sets;
}

// Main extraction
const entities = extractEntityTypes();
const associations = extractAssociations();
const entitySets = extractEntitySets();

const totalProperties = entities.reduce(
  (sum, e) => sum + e.properties.length,
  0
);
const totalNavProps = entities.reduce(
  (sum, e) => sum + e.navigationProperties.length,
  0
);

const fullSchema = {
  source: "OdataMetadata.xml",
  extractedAt: new Date().toISOString(),
  namespace: "CfChartOpModel",
  stats: {
    totalEntityTypes: entities.length,
    totalProperties,
    totalNavigationProperties: totalNavProps,
    totalAssociations: associations.length,
    totalEntitySets: entitySets.length,
  },
  entityTypes: entities,
  associations,
  entitySets,
};

writeFileSync(outputPath, JSON.stringify(fullSchema, null, 2));
console.log(`Full schema written to ${outputPath}`);

// Summary: entity names with property counts and categorization
const categorized = entities.map((e) => {
  let category = "other";
  const n = e.name.toLowerCase();
  if (n.startsWith("patient")) category = "patient";
  else if (n.startsWith("encounter")) category = "encounter";
  else if (n.startsWith("actionitem") || n.startsWith("actionableitem"))
    category = "orders/actions";
  else if (n.startsWith("code") || n.startsWith("codeset"))
    category = "code-sets";
  else if (n.startsWith("facility")) category = "facility-config";
  else if (n.startsWith("application")) category = "application";
  else if (n.startsWith("report")) category = "reporting";
  else if (n.startsWith("scan")) category = "scanning";
  else if (n.startsWith("ddo") || n.startsWith("hpi"))
    category = "clinical-templates";
  else if (n.startsWith("geo")) category = "geography";
  else if (n.startsWith("eligibility")) category = "eligibility";
  else if (n.startsWith("secure")) category = "messaging";
  else if (n.startsWith("human")) category = "human-resources";
  else if (n.startsWith("location")) category = "location";

  return {
    name: e.name,
    category,
    propertyCount: e.properties.length,
    navigationPropertyCount: e.navigationProperties.length,
    keyProperties: e.keyProperties,
  };
});

const categorySummary: Record<string, number> = {};
for (const c of categorized) {
  categorySummary[c.category] = (categorySummary[c.category] || 0) + 1;
}

const summary = {
  source: "OdataMetadata.xml",
  extractedAt: new Date().toISOString(),
  stats: fullSchema.stats,
  categorySummary,
  entities: categorized,
};

writeFileSync(summaryPath, JSON.stringify(summary, null, 2));
console.log(`Summary written to ${summaryPath}`);
console.log(`\nStats:`);
console.log(`  Entity types: ${entities.length}`);
console.log(`  Properties: ${totalProperties}`);
console.log(`  Navigation properties: ${totalNavProps}`);
console.log(`  Associations: ${associations.length}`);
console.log(`  Entity sets: ${entitySets.length}`);
console.log(`\nCategories:`);
for (const [cat, count] of Object.entries(categorySummary).sort(
  (a, b) => b[1] - a[1]
)) {
  console.log(`  ${cat}: ${count}`);
}

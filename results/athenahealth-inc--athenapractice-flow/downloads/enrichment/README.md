# Enrichment: athenahealth athenaPractice/athenaFlow EHI Export

## Run Commands

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/athenahealth-inc--athenapractice/downloads/enrichment
bun run extract-profiles.ts
bun run extract-examples.ts
```

## Input Boundary

- `extract-profiles.ts`: Parses all `../definitions/StructureDefinition-athena-*-profile.json` files (54 files)
- `extract-examples.ts`: Parses all `../examples/*.json` files (220 files)

## Output Files

- **`profiles-catalog.json`**: Complete catalog of all 54 FHIR StructureDefinition profiles, including:
  - Profile metadata (name, kind, type, category, URL, version)
  - All snapshot elements with paths, types, cardinality, short descriptions, and definitions
  - Bindings (strength and value set URL) for coded elements
  - Extensions referenced by each profile
  - Cross-resource references (Reference target profiles)
  - Classification into system/clinical/practice-management/custom categories

- **`coverage-accounting.json`**: Summary statistics:
  - Files discovered vs parsed, parse failures
  - Profiles grouped by category
  - Total element count across all profiles
  - Counts of custom vs standard resources

- **`examples-catalog.json`**: Catalog of all 220 example resources:
  - Resource type, ID, top-level keys, file size
  - Profile references from meta
  - Bundle entry counts where applicable
  - Summary by resource type

## Known Parsing Limitations

- Element definitions are extracted from the `snapshot` view only; `differential` is not separately output
- Extension definitions (StructureDefinition files for extensions, not profiles) are in the definitions directory but are not parsed by these scripts — they are referenced by URL in the profile elements
- Custom resources (kind=logical) use non-standard paths (e.g., `athena-charge-profile.ticketNumber` instead of `Charge.ticketNumber`)
- ValueSet and ConceptMap content is available in the definitions directory as separate JSON files but not cross-linked in the profile catalog

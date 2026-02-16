# Cyfluent OData Schema Enrichment

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/cyfluent--cyfluent/downloads/enrichment
bun run extract-odata-schema.ts
```

## Input

- `../OdataMetadata.xml` — OData EDMX metadata file (796KB) from Cyfluent's Desktop.zip archive, originally hosted at `https://www.cyfluentchart.com/_Files/Desktop.zip`. Describes the full `CfChartOpModel` namespace.

## Output Files

- `odata-schema.json` — Full parsed schema with all entity types, properties (with types, nullability, max length), navigation properties, associations (with referential constraints), and entity sets.
- `odata-schema-summary.json` — Summary with entity counts, property counts, category classifications, and key property listings.

## Schema Statistics

| Metric | Count |
|--------|-------|
| Entity types | 296 |
| Properties | 3,159 |
| Navigation properties | 876 |
| Associations | 438 |
| Entity sets | 296 |

## Entity Categories

| Category | Count | Description |
|----------|-------|-------------|
| facility-config | 64 | Facility-level configuration entities |
| encounter | 43 | Encounter/visit documentation entities |
| code-sets | 36 | Clinical code sets (ICD, CPT, LOINC, SNOMED, etc.) |
| patient | 36 | Patient demographic and clinical data |
| other | 31 | Misc entities (companies, genders, etc.) |
| orders/actions | 25 | Orders, action items, results |
| application | 23 | Application infrastructure (users, roles, files, audit) |
| clinical-templates | 9 | DDO widgets and HPI templates |
| reporting | 9 | Report views |
| geography | 5 | Geographic reference data |
| location | 4 | Practice locations |
| scanning | 4 | Document scanning entities |
| eligibility | 3 | Insurance eligibility |
| human-resources | 2 | Provider/staff records |
| messaging | 2 | Secure messaging |

## Known Limitations

- The OData metadata is from 2017 (Desktop.zip last modified 2017-09-01). The current database schema may have additional entities not reflected here.
- Some entity names are truncated by SQL Server conventions (e.g., `ActionItemResultObservationStatu` for `ActionItemResultObservationStatus`).
- The extraction uses regex parsing rather than a full XML parser for cross-element relationships; all 296 entities and 438 associations are successfully parsed.

# AI SKILL: EHI Export Analysis Repository

## What this repo contains

This repository analyzes **Electronic Health Information (EHI) export
documentation** from ONC-certified EHR products, evaluating how well each vendor
meets the §170.315(b)(10) export requirement. It contains raw collected data,
AI-generated analyses, and structured summaries for ~120 product families.

## Repository layout

```
results/<vendor>--<product>/        # Raw collected data per product family
  chpl-metadata.json                # CHPL certification details, developer info, EHI doc URL
  product-research.md               # AI research on what the product does/stores
  ehi-export-report.md              # AI report on the export documentation found
  sources.json                      # URLs visited during research
  files.json                        # Manifest of downloaded artifacts with descriptions
  downloads/                        # Actual artifacts: PDFs, HTML, JSON, screenshots, etc.

abstraction/<vendor>--<product>/    # AI analysis outputs per product family
  metadata.json                     # Developer info, CHPL IDs, EHI documentation URL
  analysis.md                       # Deep analysis: export mechanics, content, coverage, quality
  summary.json                      # Structured summary: score, zagat blurb, fidelity, comms
  analysis/                         # Intermediate artifacts from analysis
    full-entity-inventory.json      # Complete parse of all entities/fields (when applicable)
    analysis-stats.json             # Derived statistics
    *.py / *.ts                     # Scripts the agent wrote to parse data

abstraction/ehi-summary-schema.ts   # TypeScript schema defining summary.json structure
abstraction/abstraction-prompt.md   # Prompt used to generate analysis.md

chpl-data/                          # CHPL API data: listings, search results, developer maps
dashboard/                          # React dashboard (builds to dashboard/dist/)
scripts/                            # Pipeline scripts (run-analysis.ts, run-summary.ts, etc.)
wiggum/                             # Collection pipeline (browser automation, download agents)
```

## Key data files and what they tell you

### `results/<slug>/chpl-metadata.json`
- `url` — The vendor's official EHI export documentation URL (from CHPL)
- `developer.name` — Vendor/developer name
- `developer.website` — Vendor website
- `developer.contact_email` — Listed contact
- `products[]` — Certified products with CHPL IDs, versions, certification dates, criteria

### `results/<slug>/files.json`
- `files[]` — Every downloaded artifact with `path`, `source_url`, `size_bytes`, `description`
- `access_status` — Whether the documentation URL was accessible

### `abstraction/<slug>/summary.json`
- `holistic_score` — 0-10 quality rating
- `summary` — Zagat-style 2-3 sentence blurb
- `export_fidelity` — One of: `native`, `summary_with_supplements`, `summary_with_thin_supplements`, `summary_only`
- `patient_communications` — One of: `not_applicable`, `included`, `partial`, `excluded`, `unclear`
- `product_name` — Focus product name and version

### `abstraction/<slug>/analysis.md`
Deep analysis with 7 sections:
1. Product Context — what the product stores
2. Artifacts Reviewed — what documentation exists
3. Export Mechanics — format, scope, access
4. Export Content — detailed field/entity inventory
5. Coverage Assessment — bottom-up and top-down domain coverage
6. Documentation Quality — descriptions, schemas, sample data
7. Overall Assessment — classification, key findings, summary stats

### `abstraction/<slug>/analysis/full-entity-inventory.json`
Complete machine-readable parse of the vendor's data dictionary when one exists.
Contains every entity/table/file with all fields, data types, descriptions.

## How to answer questions

### About a specific vendor/product

The directory slug follows the pattern `<vendor>--<product>` in kebab-case.
To find a vendor, search or glob:

```bash
ls results/*epic*        # Find Epic-related dirs
ls abstraction/*athena*  # Find Athena-related dirs
```

**"What is their EHI documentation URL?"**
```bash
jq '.url' results/<slug>/chpl-metadata.json
```

**"How many entities/fields does their export cover?"**
```bash
# Quick stats from summary
jq . abstraction/<slug>/summary.json

# Full entity inventory (if available)
jq '.entities | length' abstraction/<slug>/analysis/full-entity-inventory.json
jq '[.entities[].fields | length] | add' abstraction/<slug>/analysis/full-entity-inventory.json
```

**"What format is their export?"**
Read `abstraction/<slug>/analysis.md` Section 3 (Export Mechanics).

**"Do they include billing data? Patient messages?"**
Read `abstraction/<slug>/analysis.md` Section 5 (Coverage Assessment).
Or check the structured field:
```bash
jq '.patient_communications' abstraction/<slug>/summary.json
```

**"Is this just a C-CDA repackaged as EHI?"**
```bash
jq '.export_fidelity' abstraction/<slug>/summary.json
# "summary_only" = yes, C-CDA/FHIR only
# "native" = no, uses their own data model
```

### Across all vendors

**"How many vendors just repackage C-CDA?"**
```bash
jq -r '.export_fidelity' abstraction/*/summary.json | sort | uniq -c | sort -rn
```

**"Which vendors got the best/worst scores?"**
```bash
jq -r '[.vendor_slug, .holistic_score, .summary] | @tsv' abstraction/*/summary.json | sort -t$'\t' -k2 -rn | head -10
```

**"Which vendors exclude patient communications?"**
```bash
jq -r 'select(.patient_communications == "excluded") | .vendor_slug' abstraction/*/summary.json
```

**"What downloaded artifacts exist for a vendor?"**
```bash
jq '.files[] | .path' results/<slug>/files.json
ls results/<slug>/downloads/
```

## Deep-diving into vendor data

The structured summaries are useful for quick lookups and cross-vendor queries, but
the real depth is in the narrative documents and raw source artifacts. AI tools
should read these when answering detailed questions.

### Narrative documents (per vendor)

Each vendor has up to three AI-generated narrative documents:

**`results/<slug>/product-research.md`** — Background research on the product.
What company makes it, what it does, who uses it, what data domains it manages
(clinical, billing, scheduling, messaging, specialty modules). This establishes
what a *complete* EHI export should cover. Example content:
- Company history, acquisitions, market positioning
- Product capabilities by module (charting, e-prescribing, lab, billing, portal)
- Certified ONC criteria and what they imply about stored data
- Specialty-specific features (OB, behavioral health, dental, etc.)

**`results/<slug>/ehi-export-report.md`** — The collection agent's journal of
finding and downloading the EHI export documentation. Includes:
- Navigation steps taken to find the documentation from the CHPL-registered URL
- What was found (or not found) — broken links, login walls, redirects
- Description of each downloaded artifact
- Initial observations about export format and completeness

**`results/<slug>/downloads/`** — The actual source artifacts. These are the
ground truth. Common types:
- **PDFs** (147 across all vendors) — user guides, data dictionaries, export instructions
- **HTML pages** (135) — web-based documentation, often saved with screenshots
- **Screenshots** (195 PNGs) — visual captures of documentation pages, export UIs
- **JSON/XML** (35+ JSON, 4 XML) — schemas, sample data, API specs
- **Spreadsheets** (9 XLSX) — data dictionaries, field inventories
- **ZIP archives** (4) — sample export packages

**`abstraction/<slug>/analysis.md`** — The deep analysis. This is the most
information-dense document per vendor. Its 7 sections systematically evaluate:
1. What the product stores (context for completeness assessment)
2. What artifacts were reviewed and their informativeness
3. Export mechanics (format, scope, access method, bulk capability)
4. Detailed content inventory (every entity, file, field catalogued)
5. Coverage assessment (bottom-up from export, top-down from known domains)
6. Documentation quality (descriptions, schemas, sample data, relationships)
7. Overall assessment with classification, key findings, and summary stats

### Structured analysis artifacts

The analysis phase produces JSON files that provide a machine-readable starting
point for understanding a vendor's export. **These are best-effort AI-generated
parses** — useful for overview, counts, and cross-vendor comparison, but a deep
analysis should evaluate them closely for quality and completeness against the
raw source documents.

**`abstraction/<slug>/analysis/full-entity-inventory.json`**

A complete parse of every entity, table, file, or data structure the vendor
documents in their EHI export. The schema varies by vendor because it mirrors
the vendor's own data organization, but common patterns include:

*Entity-keyed format* (for database-style exports):
```json
{
  "PatientEntity": {
    "fields": [
      { "name": "account", "type": "String", "description": "Patient Account" },
      { "name": "dob", "type": "Date", "description": "Date of Birth" }
    ]
  },
  "EmrMedicationEntity": {
    "fields": [
      { "name": "drugName", "type": "String", "description": "" }
    ]
  }
}
```

*File-keyed format* (for report/spreadsheet-style exports):
```json
{
  "exportFormat": { "container": "ZIP", ... },
  "exportFiles": [
    {
      "fileName": "Chart Cover Report.xlsx",
      "sections": [
        {
          "sectionName": "Patient Information",
          "fields": [
            { "name": "Patient Name", "dataType": "String" }
          ]
        }
      ]
    }
  ],
  "documentCategories": [ ... ]
}
```

Fields may include `name`, `type`/`dataType`, `description`, `nullable`,
`format`, or other attributes depending on what the source documentation
provides. Empty descriptions are common — many vendors list field names
without explaining them.

**`abstraction/<slug>/analysis/analysis-stats.json`**

Derived aggregate statistics from the entity inventory. Example fields:
- `totalFields`, `totalEntities` or `totalExportFiles`
- `fieldsWithDataType`, `fieldsWithoutDataType`
- `descriptionsProvided`, `percentFieldsWithDescriptions`
- `dataTypeDistribution` — counts per data type (String, Date, Number, etc.)
- `fileBreakdown` — per-file field counts

**`abstraction/<slug>/summary.json`**

The top-level structured summary (see schema in `abstraction/ehi-summary-schema.ts`):
```json
{
  "vendor_slug": "compugroup-medical-us--cgm-emds",
  "product_name": "CGM eMDs v10",
  "summary": "Zagat-style 2-3 sentence quality blurb...",
  "holistic_score": 5,
  "export_fidelity": "native",
  "patient_communications": "excluded"
}
```

**Caveat on all AI-generated artifacts**: These files are produced by automated
agents parsing PDFs, HTML pages, and other source documents. Common failure modes
include: miscounted fields, missed sections in complex PDFs, hallucinated
descriptions, incorrect data type assignments, and incomplete parses of deeply
nested structures. Always cross-check claims against the raw artifacts in
`results/<slug>/downloads/` when accuracy matters. The `analysis.md` narrative
is generally more reliable than the JSON files because it includes verification
steps, but it too should be treated as a starting point rather than ground truth.

### Scripts and intermediate artifacts

During both collection and analysis, agents frequently write scripts to parse
structured data out of raw artifacts. These scripts and their outputs persist
and can be reused or adapted.

**Collection-phase enrichment** (`results/<slug>/downloads/enrichment/`):
Scripts written by the download agent to extract structured data from artifacts
it collected. Example:
```
results/compugroup-medical-us--cgm-emds/downloads/enrichment/
  extract-ehi-data-dictionary.ts    # Bun script to parse PDF tables → JSON
  ehi-data-dictionary.json          # Extracted structured output
  README.md                         # What the script does and how to run it
```

**Analysis-phase scripts** (`abstraction/<slug>/analysis/`):
Scripts written by the analysis agent for deeper parsing. Nearly every vendor
that has parseable documentation gets a custom parser. Examples:
```
abstraction/allegiancemd-software-inc--veracity/analysis/
  parse_entities_v2.py              # Parses HTML entity pages → field inventory
  full-entity-inventory.json        # Complete 715-field inventory (31 entities)
  summary-statistics.json           # Derived counts and percentages

abstraction/compugroup-medical-us--cgm-emds/analysis/
  parse_ehi_guide.py                # Parses PDF data dictionary
  full-entity-inventory.json        # Complete 162-field inventory (5 export files)
  analysis-stats.json               # File breakdown, data type distribution
```

These scripts are typically Python or TypeScript, read from `results/<slug>/downloads/`,
and write JSON to `abstraction/<slug>/analysis/`. They can be re-run, modified,
or used as templates for similar vendors. The `full-entity-inventory.json` files
are particularly valuable — they contain every field the vendor documents, with
names, data types, descriptions, and parent entity/table/file relationships.

### Example: answering a detailed question

**Q: "Does Epic's export include discrete lab results with reference ranges?"**

1. Find the slug: `ls results/*epic*` → `results/epic-systems-corporation--epiccare-ambulatory`
2. Check the analysis: `cat abstraction/epic-systems-corporation--epiccare-ambulatory/analysis.md`
   → Read Section 5 (Coverage Assessment) for the lab results domain row
3. Check the entity inventory:
   ```bash
   jq '.entities[] | select(.name | test("lab|result|observation"; "i")) | {name, fields: [.fields[].name]}' \
     abstraction/epic-systems-corporation--epiccare-ambulatory/analysis/full-entity-inventory.json
   ```
4. If needed, look at the raw source:
   ```bash
   ls results/epic-systems-corporation--epiccare-ambulatory/downloads/
   # Find and read the relevant PDF or data dictionary
   ```

**Q: "How does Athena's export compare to Epic's on billing data?"**

1. Read both analyses' Section 5b coverage tables for the billing/claims domain
2. Compare entity inventories:
   ```bash
   jq '[.entities[] | select(.name | test("billing|claim|charge|payment|invoice"; "i"))] | length' \
     abstraction/*/analysis/full-entity-inventory.json
   ```
3. Cross-reference with the product research to understand what each system stores

## Running the pipeline

The pipeline has three phases per vendor:

1. **Collection** (`wiggum/`) — Browser automation visits the EHI documentation URL,
   researches the product, downloads artifacts
2. **Analysis** (`scripts/run-analysis.ts`) — AI agent reads all collected data and
   produces `analysis.md` + intermediate artifacts
3. **Summary** (`scripts/run-summary.ts`) — AI agent extracts structured `summary.json`
   from analysis.md using the TypeScript schema

Batch scripts: `scripts/run-all-analyses.sh`, `scripts/run-all-summaries.sh`

Dashboard: `cd dashboard && bun install && bun run build` → outputs to `dashboard/dist/`

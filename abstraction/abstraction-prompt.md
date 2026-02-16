# EHI Export Analysis

You are analyzing the EHI (Electronic Health Information) export documentation
for a certified EHR product. Your job is to deeply examine everything collected
in the results folder and produce a rigorous, evidence-backed analysis.

## Your inputs

- **Product**: {{PRODUCT_NAME}}
- **Working directory**: Your current working directory is `{{OUTPUT_DIR}}`

Your working directory contains symlinks to the collected results, so you can
access everything directly:
- `downloads/` — the actual artifacts: PDFs, HTML pages, JSON schemas, sample data, etc.
- `product-research.md` — prior research on what this vendor/product does and stores
- `ehi-export-report.md` — prior agent's narrative about the export documentation
- `sources.json` — URLs visited during research
- `files.json` — manifest of downloaded artifacts
- `chpl-metadata.json` — CHPL certification details
- `metadata.json` — pre-populated with developer info, certified products, and `ehi_documentation_url`

**The `downloads/` folder is your primary source of truth.** The markdown reports
are useful for orientation but may be incomplete or wrong. Do your own work.

**Verify, don't parrot.** The prior reports were written by automated agents at
collection time and may contain errors — websites that were down may be back up,
claims about file contents may be wrong, page counts or field counts may be off.
When a prior report makes a factual claim (e.g., "site returns 403," "PDF has 8
pages," "data dictionary has 50 fields"), verify it yourself before repeating it
in your analysis. If you find a discrepancy, note it. Your analysis should be
independently defensible, not a summary of the prior agent's work. But you don't
have to go back out to the web unless something is missing / failed; you should
generally just rely on what's in downloads if it has what you need and expect.

**Don't surface claims you can't substantiate.** If a prior report says a website
is down or a file was inaccessible, don't repeat that unless you've checked
yourself. Your analysis should only contain claims you can back up with evidence
from the artifacts in `downloads/` or from your own verification. If you wind up
doing your own browsing or research, save anything you find / use. Don't speculate.

## What you're trying to understand

The ONC Cures Act rule 170.315(b)(10) requires certified EHR systems to support
export of **all electronic health information** the product stores — not a clinical
summary, not just the FHIR API data, but everything in the designated record set.

Many vendors do a poor job. Common failure modes:
1. **Repackaged existing export**: vendor points to their existing C-CDA or FHIR
   Bulk Data (g)(10) export and calls it "(b)(10)." This covers USCDI — maybe 20%
   of what the product stores — clinical summaries but no billing, no specialty
   data, no custom forms. The telltale sign: documentation that says "C-CDA" or
   "FHIR Bulk Data" and links to the generic standard spec with no product-specific
   data dictionary.
2. **Empty documentation**: a few sentences saying "we support EHI export" with
   no data dictionary, no schema, no detail about what's actually exported.
3. **Documentation exists but is thin**: field names and types but no descriptions,
   no relationships, no value sets, no sample data.
4. **Good but incomplete**: solid export but missing entire domains (e.g., exports
   clinical data but not billing).

**Important distinction:** the format (FHIR, C-CDA, CSV, TSV, etc.) does NOT
determine whether an export is genuine (b)(10). What matters is whether the
vendor built a purpose-specific EHI export that covers the breadth of what
the product stores, or just relabeled an existing clinical exchange export.
A FHIR-based export that maps 50+ EHR-specific concepts to FHIR resources
(including billing, custom forms, specialty data) is fundamentally different
from a vendor pointing at their existing (g)(10) FHIR API. Similarly, a
native database dump that only exports clinical tables is not comprehensive
just because it uses a proprietary format.

## All EHI vs USCDI

USCDI v3 (mandatory for certified systems as of Jan 2026) defines 22 data classes
with ~94 data elements — the regulatory floor for clinical exchange. In FHIR
terms (US Core 6.1.0), these map to ~26 base resource types via 47+ profiles:

| USCDI Data Class | FHIR Resources |
|---|---|
| Allergies & Intolerances | AllergyIntolerance |
| Assessment & Plan of Treatment | CarePlan, Observation, QuestionnaireResponse |
| Care Team Members | CareTeam, Practitioner, PractitionerRole, RelatedPerson |
| Clinical Notes (8 types: Consult, Discharge Summary, H&P, Imaging Narrative, Procedure, Progress, Operative, ED) | DocumentReference, DiagnosticReport |
| Clinical Tests | Observation, DiagnosticReport |
| Diagnostic Imaging | Observation, DiagnosticReport |
| Encounters | Encounter, Condition |
| Facility Information | Location |
| Family Health History | FamilyMemberHistory |
| Goals & Preferences | Goal, Observation, DocumentReference |
| Health Insurance Information | Coverage, Organization |
| Health Status Assessments (health concerns, functional/disability/mental status, pregnancy, smoking, SDOH) | Observation, Condition, QuestionnaireResponse |
| Immunizations | Immunization |
| Laboratory | Observation, DiagnosticReport, Specimen |
| Medical Devices | Device |
| Medications | Medication, MedicationRequest, MedicationDispense |
| Orders | MedicationRequest, ServiceRequest, DocumentReference |
| Patient Demographics | Patient, RelatedPerson, Observation |
| Problems | Condition |
| Procedures | Procedure, ServiceRequest |
| Provenance | Provenance |
| Vital Signs (13 profiles: BP, height, weight, HR, RR, temp, SpO2, BMI, etc.) | Observation |

A (b)(10) export that covers only these USCDI-scope resources is the vendor's
existing clinical exchange surface rebranded — it represents the regulatory
floor, not the designated record set.

The designated record set exceeds USCDI in two ways. First, **depth within USCDI
domains**: US Core profiles define a small number of Must Support elements per
resource, but EHRs typically store far more data elements internally — a
Condition resource might have 5 Must Support fields in US Core, but the EHR's
problem list table may have 30+ columns tracking onset context, severity history,
verification workflows, linked orders, and audit metadata, all of which are part
of the patient record and must be in a (b)(10) export. Second, **breadth beyond
USCDI domains**: most EHRs store entire categories of patient data that USCDI
doesn't address at all. Examples include: patient-specific billing and revenue
cycle records (charges, claims, superbills, payments, adjustments, EOBs),
insurance and coverage details beyond basic membership, prior authorizations and
eligibility responses, referral workflows and tracking, patient communications
(portal messages, secure messaging threads, phone call logs), scanned/uploaded
documents and media not captured as clinical notes, custom forms and
questionnaires (intake forms, consent forms, specialty-specific assessments),
detailed medication administration records (MAR), detailed surgical/operative
records beyond the procedure note, order sets and order details with linked
results, behavioral health and substance use treatment records, oncology-specific
data (staging, regimens, tumor registries), OB/GYN records (prenatal visits,
labor/delivery, birth records), dental charts and periodontal data, wound care
assessments and healing trajectories, correctional/institutional health records,
durable medical equipment orders, patient-reported outcomes, and
demographic/social history details beyond USCDI fields. The more of these
non-USCDI designated-record-set domains an export includes — and the more
completely it exports fields within USCDI domains — the more credibly the vendor
has engaged with (b)(10).

## How to work

### Phase 1: Orient yourself

Read `product-research.md` to understand what this product is and what data it
stores. This establishes your baseline: what *should* the export cover?

Skim `ehi-export-report.md` and `files.json` for orientation on what was collected.

### Phase 2: Dig into the artifacts

This is the core of the analysis. **Start by reading `files.json`** — it tells
you what's in `downloads/`, where each file came from (source URL), and what
it is. This gives you a map before you start opening artifacts.

Then go through `downloads/` systematically:

**For every artifact**, understand what it is and what it tells you:
- PDFs: use `pdftotext -layout` to extract text; `pdfinfo` for metadata; render
  pages with `pdftoppm` if text extraction is poor
- HTML: parse structure, extract tables, count elements
- JSON/XML schemas: parse and count entities/fields
- Sample data files: inspect structure, count records, check coverage
- ZIP files: list contents, extract, examine
- XLSX: use a script to extract sheet names and row/column counts

**Write scripts when it helps.** If there's a data dictionary in HTML or JSON or
XLSX, don't just eyeball it — write a script to parse it and produce hard numbers.
Save scripts and their outputs to `./analysis/` so the work is
reproducible.

### Scripting setup

Use **Python** or **Bun (TypeScript)** for scripts. Set up dependencies properly:

**Python**: Create a virtual environment in the analysis folder:
```bash
cd ./analysis
uv venv && source .venv/bin/activate
uv pip install openpyxl   # or whatever you need
python parse_dictionary.py
```

**Bun**: Initialize a local package.json in the analysis folder:
```bash
cd ./analysis
bun init -y
bun add xlsx cheerio      # or whatever you need
bun run parse_dictionary.ts
```

This keeps dependencies explicit and reproducible without polluting the
global environment.

### Good scripts to write
- Parse an HTML data dictionary → count tables, fields, fields with descriptions
- Parse a JSON schema → enumerate entities and their properties
- Analyze sample export data → count files, record counts, field coverage
- Extract table structures from a PDF data dictionary (use `pdftotext -layout`
  to extract text first, then parse the text programmatically)
- Inventory a ZIP of sample export files → list files, sizes, formats, record counts
- Compare entities in the export vs domains the product covers

### Phase 3: Assess

With the evidence in hand, assess the export along these dimensions:

**What is the export, structurally?**
- What format? (CSV/TSV, JSON, FHIR, C-CDA, SQL dump, proprietary XML, etc.)
- Is it the vendor's native data model (internal tables) or a projection into
  a standard (FHIR resources, C-CDA sections)?
- How many entities/tables/resources? How many total fields?
- How is it obtained? (UI button, API call, vendor-assisted, unclear)

**How well is it documented?**
- Is there a data dictionary? How detailed?
- Field names? Types? Descriptions? Value sets? Relationships?
- Sample data? Machine-readable schemas?
- Could a developer build an import from this documentation alone?

**What does it cover?**
- Which data domains are represented? (demographics, encounters, meds, labs,
  billing, insurance, notes, images, specialty data, etc.)
- Which domains are missing relative to what the product stores?
- Is this a genuine "all EHI" export or a clinical summary repackaged?

**What are the red flags?**
- Is the export just summary C-CDA or USCDI summary FHIR being called "(b)(10)"?
- Are entire categories of data (billing, specialty) absent?
- Is documentation so thin that you can't even tell what's exported?
- Are there signs this was a compliance checkbox rather than a real effort?

### Phase 4: Write the analysis

Write `./analysis.md` with the structure described below.

## Output: `analysis.md`

The analysis should be structured as follows. Be concrete throughout — cite
specific file names, table names, field counts, page numbers. Hard numbers
over vibes.

```markdown
# EHI Export Analysis: {{Vendor Name}}

**Product**: {{product name(s)}}
**Analysis date**: {{date}}
**CHPL IDs**: {{ids}}

## 1. Product Context

Brief summary of what this product is and what data it stores, drawn from
product-research.md. Focus on what's relevant to assessing export completeness:
what clinical workflows, what billing/PM capabilities, what specialty features,
what patient-facing tools. This sets the baseline for "what should the export cover?"

## 2. Artifacts Reviewed

List every artifact you examined with a one-line description of what it is and
what it told you. Include size/scope where relevant (page count, table count,
field count). Flag which artifacts were most vs least informative.

## 3. Export Mechanics

How the export works:
- Format(s)
- Mechanism (UI, API, vendor-assisted)
- Single-patient vs bulk capability
- Any access constraints or fees

## 4. Export Content: What's In It

This is the meat. Describe what the export actually contains based on your
examination of the artifacts. Be specific:

- If there's a data dictionary: how many entities/tables? How many fields total?
  How many fields have descriptions beyond just a name? Are types documented?
  Are relationships/foreign keys documented? Are value sets/code systems specified?

- If there are sample data files: what do they contain? How many records? What
  fields are populated vs empty?

- If it's FHIR/C-CDA: which resource types / sections? Are there vendor
  extensions beyond the standard? Or is it strictly standard?

### Vendor's own content organization

Present what you found using the **vendor's own language and categories**.
If the vendor organizes their data dictionary into "Demographics", "Clinical",
"Billing and Insurance", "Labs" — use those groupings. If they have entities
named `patient-superbills.tsv` or `claim_procedure.json`, use those names.

This table should reflect exactly what the vendor provides, in their terms:

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| patient_demographics | 50 | 50 | yes | Demographics |
| patient_superbills | 70 | 70 | yes | Billing and Insurance |
| ... | ... | ... | ... | ... |

(Generate this from a script if the data dictionary is large.)

**For large exports (100+ entities):** Don't list every entity in the markdown.
Instead, write a script that produces a complete inventory and saves it to
`analysis/` (`analysis/entity-inventory-full.json`). In the analysis.md,
show:
- Summary statistics (total entities, total fields, fields with descriptions)
- A breakdown by the vendor's own categories (table count + field count per category)
- The 10-20 largest/most important entities as representative examples
- Any notable outliers (entities with 0 descriptions, unexpectedly thin entities,
  entities that seem misplaced)

The full inventory in `analysis/` is the reference; the analysis.md presents
the highlights and patterns.

For exports without a data dictionary (e.g., C-CDA or FHIR with no vendor
documentation), describe what sections/resources are visible and what
evidence you have for each.

## 5. Coverage Assessment

This section has two parts: first describe what you found in the vendor's
terms, then map it to standardized domains for cross-vendor comparison.

### 5a. What the vendor covers (bottom-up)

Summarize the export content using the vendor's own categories and language.
What modules/sections/categories does the vendor describe? How deep is each?
Which are richest (most entities, most fields)? Which are thinnest?

This is where you note things like "the vendor's 'Billing and Insurance'
category has 12 tables and 286 fields — this is genuinely deep" or "the
vendor lists a 'Clinical' section but it's just 3 C-CDA sections with no
field-level detail."

### 5b. Standardized domain coverage (top-down)

Now map the export against a standard set of EHI domains for cross-vendor
comparison. For each domain, assess coverage:

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient_demographics` (50 fields), `patient_contacts` (15 fields) | Thorough |
| Claims / Billing | ❌ Not covered | No billing entities in export | Product does billing (see Section 1); significant gap |
| ... | ... | ... | ... |

Coverage levels:
- ✅ **Covered**: dedicated entities/tables/fields address this domain
- ⚠️ **Partial**: some data present but clearly thin or incomplete
- ❌ **Not covered**: no evidence in the export
- **N/A**: product doesn't store this type of data

Standard domains (include all that apply to this product):
- Demographics
- Encounters / visits
- Problems / conditions / diagnoses
- Medications / prescriptions
- Allergies
- Immunizations
- Vitals
- Lab results
- Imaging / diagnostic reports
- Procedures
- Clinical notes / documents
- Care plans / goals
- Orders / referrals
- Insurance / coverage
- Claims / billing
- Payments
- Consents / directives
- Patient communications / portal messages
- Specialty-specific (name the specialty)

The **Gap Analysis** column is critical. For each domain, connect back to
Section 1 (Product Context): does the product store this data? If yes and
the export doesn't cover it, that's a real gap. If the product doesn't do
billing, then missing billing data is N/A, not a gap.

## 6. Documentation Quality

Assess the quality of the export documentation itself:
- Can a developer actually understand and use the export from these docs?
- What's well-documented vs what requires guesswork?
- Are there machine-readable artifacts (schemas, sample data) or just prose?

## 7. Overall Assessment

### Classification

Classify the export along two independent axes, with comments and notes about
why / how you can tell and calling out any specific details or surprising
aspects of what you saw.

**Axis 1 — Coverage breadth** (relative to what the product stores):

- **Comprehensive**: Export demonstrably covers the breadth of data domains
  the product stores — not just clinical summaries but billing, specialty,
  administrative, and operational data as applicable. "Comprehensive" is
  relative to the product: a simple ambulatory charting tool has fewer
  domains to cover than a full hospital EHR. Assess against the product's
  known capabilities from Section 1, not against an abstract ideal.
  Coverage must go meaningfully beyond USCDI — USCDI is a minimum floor
  for clinical exchange, not a measure of EHI completeness.
- **Partial**: Export covers some domains well but has significant gaps
  relative to what the product stores (e.g., clinical data exported but
  billing omitted despite the product having billing capabilities).
- **Minimal/stub/unclear**: Documentation is too thin to assess, or export
  clearly covers only a tiny fraction of what the product stores.

**Axis 2 — Export approach**:

- **Purpose-built EHI export**: Vendor built an export specifically for
  (b)(10) that goes beyond their existing clinical exchange capabilities.
  This could be a native database dump (Epic's TSV tables, Oracle's SQL
  model) OR a deep standards-based mapping (e.g., FHIR resources mapped
  to 50+ EHR concepts including billing, specialty data, custom forms).
  The key signal is that the export covers data domains not present in the
  vendor's existing (g)(10) or C-CDA exchange.
- **Repackaged existing export**: Vendor points to their existing C-CDA,
  FHIR Bulk Data (g)(10), or other clinical exchange export and relabels
  it as (b)(10). The telltale sign: documentation references USCDI, US Core,
  or the generic C-CDA/FHIR spec with no product-specific data dictionary,
  no mapping beyond standard templates, and no coverage of billing or
  operational data.
- **Unclear/undetermined**: Documentation is too thin to distinguish
  between purpose-built and repackaged.

### Key Findings

Bullet the 3-5 most important findings. Lead with the strongest signal
(positive or negative). Be specific and cite artifacts.

### Summary Stats

A quick-reference block for cross-vendor comparison:

    Coverage:        (Comprehensive / Partial / Minimal-stub-unclear)
    Approach:        (Purpose-built EHI export / Repackaged existing export / Unclear)
    Export format:   (e.g., TSV, JSON, C-CDA, FHIR R4, mixed)
    Entities:        (count, or "N/A" if no data dictionary)
    Fields:          (count, or "N/A")
    Descriptions:    (% of fields with descriptions, or "N/A")
    Sample data:     (yes/no)
    Bulk export:     (yes/no/unclear)
    Domains covered: (X of Y applicable domains)

### Bottom Line

2-3 sentences. Would a patient or provider get a usable, complete copy of
their data from this export? What's the single biggest gap or strength?
```

## Output: `analysis/` directory

Save scripts you wrote and their outputs to `./analysis/`. Include:
- Scripts used to parse artifacts (with comments explaining what they do)
  These should rely on ./downloads/ content, but not directly
  rely on ./downloads/enrichment/ content (read and re-implement where helpful)
- Extracted data (e.g., parsed data dictionary as JSON, field counts as text)
  * includes `entity-inventory-full.json` and `entity-inventory-summary.json`
- Any other intermediate artifacts that make the analysis reproducible

Every hard number in the analysis.md should be traceable to a file in `analysis/`.

### Extraction completeness requirement

Your most valuable output is a **complete, idiomatic JSON parse** of every
structured artifact in `downloads/`. The workflow is:

1. **Parse first, analyze second.** Before writing any summary statistics or
   prose, write a script that reads the raw artifact (HTML data dictionary,
   PDF tables, JSON schema, XLSX, CSV, etc.) and emits a clean, complete
   JSON representation of its full content. This is your intermediate
   representation — everything downstream derives from it.

2. **`entity-inventory-full.json`** (required whenever there's a parseable
   data dictionary or schema or any content we can turn into one, e.g. via PDF, csv, html, etc):
   A complete machine-readable extraction of
   every entity/table and every field. For each field, capture everything
   the source provides: name, type, description, nullability, max length,
   foreign keys, value sets, coded values, default values, example data.
   Don't summarize or truncate — if the source has 715 fields, the JSON
   has 715 field objects. This file IS the parse. You many see similar
   files in the existing download/enrichments but you should build your
   script from raw sources, not enrichments (but read/use code in the
   enrichments to inform your choices, when helpful).

3. **Derive aggregates from the parse.** Summary statistics, category
   breakdowns, coverage tables in analysis.md — all computed from the
   full inventory JSON, not counted separately. If your script counts
   "164 fields with descriptions," there should be exactly 164 field
   objects in the JSON where `description` is non-empty. These should
   all land in `entity-inventory-summary.json`

4. **Parse aggressively.** If a PDF has tabular data, extract the table
   rows — don't just count them. If an HTML page has field definitions
   in a `<dl>` or `<table>`, parse every entry. If a JSON schema has
   nested properties, flatten and enumerate them all. Err on the side
   of extracting too much rather than too little. A messy-but-complete
   parse is better than a tidy summary with the underlying data thrown
   away. Iterate until you are perfect or cannot make progress.

5. **Handle parse failures explicitly.** If `pdftotext` garbles some rows,
   include them with a `"parse_error": true` flag and the raw text. Report
   total parsed vs failed in the output. Don't silently skip unparseable
   content.

The full inventory is the most valuable artifact you produce. Every number
in analysis.md should be reproducible by querying it.

## Important guidance

- **Do the work.** Parse the PDFs. Count the fields. Inspect the sample data.
  Don't just read the markdown summaries and rephrase them.
- **Hard numbers beat adjectives.** "85 tables, 1165 fields, all with
  descriptions" beats "comprehensive documentation."
- **Cite your sources.** Every claim should reference a specific artifact,
  table, field, page number, or file.
- **Be honest about uncertainty.** If you can't tell from the artifacts
  whether billing data is in the export, say so. Don't guess.
- **Use the EHI scope reference.** Don't flag missing audit logs or system
  config as gaps — those aren't EHI. Do flag missing billing, specialty
  clinical data, or custom forms if the product stores them.
- **The classification matters.** Getting the two axes right is the single
  most important output. A vendor whose "(b)(10) export" is just their
  FHIR API repackaged should be classified as "Repackaged existing export,"
  even if it uses a lot of FHIR resources. A vendor who built a deep
  FHIR mapping covering billing, specialty data, and custom forms beyond
  (g)(10) should be classified as "Purpose-built EHI export" — the format
  being FHIR doesn't make it repackaged.

## EHI Scope Reference

{{EHI_SCOPE_REFERENCE}}

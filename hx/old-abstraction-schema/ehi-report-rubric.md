# EHI Grading Rubric (v1.6)

## Scope of use

Apply this rubric to every complete vendor report in `results/*/ehi-export-report.md` for future graders and for any automated scoring pass that writes `abstraction/ehi-grading-results.json`.

Current complete scope: `abstraction/ehi-grading-results.json` should include all complete folders in `results/*`.

Use `1.6` for this refresh.

The rubric now reflects the full complete set and now embeds statutory scope boundaries from `wiggum/prompts/ehi-scope-reference.md`.

Highlights incorporated from the latest full corpus:

- treat XML as two states: explicit CDA (`ccda`) and non-CDA custom XML (`custom_xml`) with overlap handled only in `xmlFlavorChoices`.
- avoid counting operational/admin-only products as EHI unless patient-chart continuity is explicit.
- require explicit `examples.sampleData` signal where sample payloads are observed.
- prioritize `B10_UNDERDOCUMENTED` when schema + examples are incomplete after complete-folder review.

For historical context, the 15 most recently ingested examples remain:

1. `allegiancemd-software-inc`
2. `naphcare-inc`
3. `zoobook-systems-llc`
4. `practice-fusion`
5. `juno-health`
6. `pulse-systems-inc`
7. `carecloud-inc`
8. `enable-healthcare-inc`
9. `micromd-llc`
10. `md-charts-llc`
11. `health-systems-technology-inc`
12. `medaz-net-llc`
13. `aarista-technology-llc`
14. `dox-emr`
15. `american-medical-solutions-inc`

## 0) Objective

Classify each vendor's public EHI export mechanism into one of six buckets:
- `B10_NATIVE_FULL`
- `B10_NATIVE_PARTIAL`
- `B10_NATIVE_HYBRID`
- `B10_G10_REPURPOSED`
- `B10_UNDERDOCUMENTED`
- `B10_UNRESOLVED`

Then score five signals (`scope`, `format`, `dictionary`, `conflationRisk`, `accessibility`) on 0–4 scales and annotate domain coverage in an `EHI`/`non-EHI` aware way.

## 1) First rule: scope comes from product context, then report evidence

Never infer coverage breadth only from export language.  
Start with `product-research.md` and CHPL-supported capabilities:

1. Identify product-supported modules and patient-related capabilities.
2. Build the expected patient-linked decision set from those capabilities.
3. Grade export scope against those expected domains, not against every table in the product docs.

If product context is missing and no clinical rationale exists for a function, mark as `non_applicable` instead of `potentially_missing`.

## 2) What is in scope as EHI (decision framework)

Apply this practical test from the scope reference:

> If there is a problem with this data, could it affect a patient's treatment or the amount a patient/insurer owes?
>
> **Yes** -> EHI.
>
> **No** -> operational/admin only (not EHI).

### Regulatory frame: designated record set

EHI is narrower than “all data in the EHR.” It is electronic PHI that is part of the HIPAA Designated Record Set (45 CFR 164.501) and is defined in 45 CFR 171.102.
Statutory in-scope areas include:
- medical records and billing records
- enrollment, payment, claims adjudication, and case/medical management records
- records used to make decisions about individuals

Two statutory carve-outs are excluded even if present in the broader product data model:
- psychotherapy notes
- litigation compilations

Mark domains as EHI only when they materially affect care/financial continuity for an individual patient.

### Include as EHI
- demographics, encounters, problems, meds, labs, allergies, immunizations, procedures, results, plans, goals, notes
- insurance/coverage + claims/claim workflow artifacts tied to patient care
- consents, referrals, documents, media/image metadata, specialty records stored in patient chart
- per-patient billing and payment traces where tied to care continuity

### Explicitly not EHI
- system settings, role/permission tables, queue/workload dashboards
- audit/security logs, authentication metadata, app config
- utilization KPIs and aggregate reporting unless per-patient per-record continuity is explicit
- provider credentialing/admin records, templates, policy copies
- psychotherapy notes, litigation compilations

## 2b) Quick boundary checks

- If a reported domain is workflow/process-only (e.g., staff schedules, queue state, aggregate dashboards), prefer `operations-only` notes and `nonApplicable` unless explicit per-patient linkage is shown.
- If the same functional area is present in the source but clearly represented only in non-patient aggregate form, treat as a gap in EHI scope rather than missing clinical data.

If a domain is ambiguous, add `scopeBoundaryNotes` with explicit rationale.

Operational exclusions from this rubric are intentionally explicit:
- Staff scheduling, workload dashboards, and queue health are operations-only without explicit patient linkage.
- Templates, credentialing, access control policy, and quality metrics are non-EHI.
- Psychotherapy notes and litigation compilations are out-of-scope even when documented.
- Patient-facing UI affordances should not be read as full export mechanisms unless a reproducible artifact is attached.

## 3) XML is not one thing

### `xmlFlavor` decisions
- `ccda`: explicit Clinical Document Architecture terms, CDA sectioning, explicit C-CDA vocabulary
- `custom_xml`: vendor-owned XML schema, tags unknown/non-CCDA, "custom XML" wording, XML mention without CDA claims
- `unknown_xml`: XML detected with insufficient schema/namespace evidence
- `not_xml`: no XML export path

Do not set both `ccda` and `custom_xml` for one signal.  
Use `xmlFlavorChoices` only for mixed/ambiguous exports with explanation in `formatSignals.notes`.
If both are encountered, retain one canonical choice in `xmlFlavor` and move the ambiguity into `xmlFlavorChoices`.

## 4) Category decision map

Apply these in order:

1. Is the mechanism unreachable or contradictory? → `B10_UNRESOLVED`
2. Is there a native/bulk export mechanism (tabular, JSON, XML files, NDJSON, archive)? → native branches (Full / Partial / Hybrid)
3. Is the only substantive mechanism a standardized USCDI-style (g)(10) representation? → `B10_G10_REPURPOSED`
4. Is export format/dictionary/sample path under-described? → `B10_UNDERDOCUMENTED` unless evidence is clearly enough for a different branch

### A) `B10_NATIVE_FULL`
Use when native format is clear, documented, and broad enough for the product's patient-linked scope.

Examples:
- Natively structured table dumps with complete field-level documentation
- Clear CSV/TSV/JSON tables with PK/FK or equivalent linkage metadata
- Native plus C-CDA/other supplemental documents where non-clinical domains are also recoverable

Subcategories:
- `csv_table_dump`
- `tsv_table_dump`
- `parquet_bulk`
- `json_schema_export`
- `ccda_plus_vendor_structured`
- `native_tabular_plus_ccda`
- `form_export`

### B) `B10_NATIVE_PARTIAL`
Use when there is a native mechanism, but evidence shows major, evidence-backed, patient-linked gaps or structural breaks that prevent full reconstruction.

Subcategories:
- `ndjson_with_schema` (if schema only partially documented)
- `custom_xml` (if schema exists but linkage/coverage is weak)

### C) `B10_NATIVE_HYBRID`
Use when multiple native-style streams are intentionally used and are necessary for breadth.

Subcategories:
- `ccda_plus_tabular`
- `native_tabular_plus_ccda`

### D) `B10_G10_REPURPOSED`
Use when the dominant export path appears designed for g(10)-style interoperability and lacks full EHI breadth.

Subcategories:
- `ccda_summary_only`
- `fhir_bulk_api`
- `fhir_nonstandard_serialization`

### E) `B10_UNDERDOCUMENTED`
Use when product indicates EHI export exists but with missing format/schema/relationship details that materially reduce validation.

Subcategories:
- `ui_only`
- `opaque_claimed`
- `module_selector_unknown_format`
- `xml_bundle_unknown`
- `cbor_bundle`
- `custom_binary`
- `proprietary_binary_bundle`
- `other`

### F) `B10_UNRESOLVED`
Use when key evidence is inaccessible or internally contradictory after full attempt (dead link, blocked authentication, inaccessible paths, mutually irreconcilable artifacts).

### New subcategory guardrails from recent reports
- CBOR exports are a native proprietary stream (`cbor_bundle`) only if ZIP + tooling notes are present and evidence is reproducible.
- Proprietary opaque XML/JSON binaries that are not documented are `proprietary_binary_bundle` or `custom_binary`, not native-full by default.
- Unknown export module selectors with no output format are `module_selector_unknown_format` even if marketing is detailed.

## 5) Score rules

Each score is 0–4; use evidence, not opinion.

`scope`
- 0: no patient-linked domain evidence
- 1: generic claims only
- 2: limited standard clinical only
- 3: includes several non-core/billing/specialty domains
- 4: explicit full-breadth mapping to product-supported patient domains

`format`
- 0: format unverified/opaque
- 1: only format name
- 2: format named
- 3: format + artifact examples/schemas
- 4: format + usable structure + reproducible artifacts

`dictionary`
- 0: none
- 1: superficial labels only
- 2: partial field definitions
- 3: substantive machine-readable schema/docs
- 4: schema + key relationship / linkage details

`conflationRisk`
- 0: clearly separate native path
- 1: native primary with minor clinical API overlap
- 2: mixed API/native artifacts without clear segmentation
- 3: explicit FHIR/C-CDA framing dominates
- 4: repurposed g(10) path as sole practical path

`accessibility`
- 0: inaccessible
- 1: marketing-only
- 2: some docs but no reusable artifacts
- 3: reproducible docs/links
- 4: reproducible artifacts + file-level examples

### Score profile expectation
For each grading batch, compute per-score histograms (0–4 counts) and a total-score profile.  
Use this to detect shifts in grading style and avoid category drift between graders.

## 6) Record-level mandatory fields

Every record must include:
- `vendor`, `reportPath`, `assessedAt`, `category`, `subcategory`, `confidence`
- all five `scores`
- `rationale` with 2–5 evidence-backed bullets
- `decisionRulesApplied`
- `signals.native`, `signals.g10Conflation`, `signals.underdocumented`
- `domainCoverage` buckets (`covered`, `potentiallyMissing`, `nonApplicable`, `unknown`)
  - emit all four buckets for every record, with explicit empty arrays when no values exist
- `productContext` evidence
- `scopeBoundaryNotes` (at least 2 when scope is nuanced)
- `formats`, `dataFiles`
- `formatSignals` (including explicit XML signal when XML is used)
- `examples.includedArtifacts`, `examples.missingArtifacts`
- `examples.sampleData` (structured signal) and top-level `examples.hasSampleData`
- `examples.sampleData.hasSamples` should equal `examples.hasSampleData` when both are present.
- `evidence` array with source anchors

## 7) Recent-pattern calibration (decision guidance from last 15)

- `allegiancemd-software-inc`: proprietary CBOR ZIP with docs; treat format as custom/proprietary unless explicit schema + linkage evidence is present.
- `naphcare-inc`: CSV+CCDA+PDF combination with broad domain breadth ⇒ likely `B10_NATIVE_HYBRID`.
- `zoobook-systems-llc`: UI selector is rich, format not documented ⇒ likely `B10_UNDERDOCUMENTED` / `module_selector_unknown_format`.
- `practice-fusion`: true TSV per-entity dump + linked IDs ⇒ strong native coverage (often `B10_NATIVE_FULL`).
- `juno-health`: large CSV table dump with field-level dictionary and relationships ⇒ `B10_NATIVE_FULL`.
- `pulse-systems-inc`: CDA-centric export for complex non-clinical product modules ⇒ `B10_G10_REPURPOSED`.
- `carecloud-inc`: C-CDA for clinical + PDFs for billing/admin ⇒ native/hybrid with non-native artifact gap.
- `enable-healthcare-inc`: many formats (C-CDA, CSV, EDI, HL7v2, JSON) without join documentation across streams ⇒ often `B10_NATIVE_HYBRID` or `B10_NATIVE_PARTIAL` depending on relationship evidence.
- `micromd-llc`: password-protected ZIP containing proprietary XML schema-export files, with broad domain coverage but missing field semantics/type catalog (often `B10_NATIVE_PARTIAL`, `custom_xml`) unless schema detail is explicitly raised to full documentation confidence.
- `md-charts-llc`: format not determined from guidance page alone ⇒ `module_selector_unknown_format`.
- `health-systems-technology-inc`: C62 proprietary format without public schema ⇒ `proprietary_binary_bundle`.
- `medaz-net-llc`: standard FHIR bulk data with US Core scope only ⇒ `B10_G10_REPURPOSED`.
- `aarista-technology-llc`: "machine-readable" claim with no schema and mixed free-text clinical tables ⇒ underdocumented native stream, likely partial/hybrid uncertainty.
- `dox-emr`: C-CDA-only clinical documents without non-clinical breadth ⇒ `B10_G10_REPURPOSED` + `ccda_summary_only`.
- `american-medical-solutions-inc`: CSV zip with category-level extraction but weak linkage/documentation semantics ⇒ often `B10_NATIVE_PARTIAL`.

## 8) Anti-patterns

- Do not grade a report “full” from high volume alone.
- Do not infer non-clinical module coverage unless product context and export artifacts agree.
- Do not default XML mentions to `ccda` in the absence of CDA evidence.
- Do not ignore patient-linked billing/scheduling/service artifacts as “operations-only” when they drive continuity decisions.
- Do not skip `sampleData` signals; absence of samples should be explicit (`hasSampleData = false`).

## 9) Conflict arbitration

If two patterns conflict, prioritize:

1. Scope integrity (`product-context` agreement)
2. Verifiable primary mechanism evidence (downloadable artifacts and structure)
3. Score consistency across all five dimensions
4. Minimal-risk category (`B10_UNDERDOCUMENTED` over `B10_NATIVE_PARTIAL`) when evidence quality is not enough to support full/partial confidence.

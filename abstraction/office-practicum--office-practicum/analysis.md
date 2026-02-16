# EHI Export Analysis: Office Practicum

**Product**: Office Practicum (Version 21)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3048.Offi.21.02.1.221121

## 1. Product Context

Office Practicum (OP) is a pediatric-specialty EHR, practice management, and revenue cycle management platform developed by Connexin Software, Inc. It serves over 9,000 pediatricians across 48–49 states and is described as the only EHR "built by pediatricians for pediatricians." The product is a complete, integrated platform — not a module — combining:

- **Clinical EHR**: SOAP notes, pediatric-specific templates (175+ school/camp forms, sick visit templates, preventive exam templates), growth charts (including specialty curves), developmental assessments, behavioral health screening (PHQ-9, GAD-7), VacLogic immunization forecasting, allergy tracking, medication management, e-prescribing with EPCS
- **Lab integration**: Electronic lab orders, results, in-house lab device connectivity
- **Practice management**: Scheduling, patient flow tracking, well-visit recalls, insurance eligibility verification
- **Billing & RCM**: Electronic superbills, claims processing, payment posting, denial tracking, clearinghouse integration, revenue analysis
- **Patient engagement**: Patient portal (BridgeInteract-powered), secure messaging, self-registration, telehealth (via RemedyConnect)
- **Document management**: Document scanning, bi-directional eFax, referral workflows

Given this breadth, a complete (b)(10) export should cover demographics (with pediatric family/guardian relationships), clinical documentation, growth data, immunizations, behavioral health screenings, medications, allergies, labs, billing/claims, insurance, documents, referrals, and portal communications — at minimum.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/onc-certification-page.html` (407 KB) | Registered URL page; contains ~129 words of EHI export documentation in 3 paragraphs | **Primary source** — but critically thin |
| `downloads/onc-certification-info-disclosures.html` (414 KB) | Mandatory disclosures page with accordion; identical EHI text | Duplicative — confirms registered URL content |
| `downloads/OP_RWT_Results_Report_2025.pdf` (965 KB, 10 pages) | 2025 Real World Testing results; page 7 covers EHI export (2,861 single exports, 20 bulk exports) | Confirms feature is functional and used; no technical details |
| `downloads/screenshot-registered-url-ehi-section.png` | Screenshot of EHI section on registered URL | Visual confirmation |
| `downloads/screenshot-ehi-export-accordion-expanded.png` | Screenshot of expanded EHI accordion on disclosures page | Visual confirmation |
| `downloads/screenshot-registered-url-onccert.png` | Screenshot of certification section | Context only |
| `downloads/screenshot-disclosures-page-top.png` | Screenshot of disclosures page header | Context only |

**Most informative**: The HTML pages (identical content). **Least informative**: Screenshots (visual confirmation only). **Critical gap**: No data dictionary, schema, sample data, or technical documentation of any kind was found.

## 3. Export Mechanics

- **Format**: CSV
- **Mechanism**: Built-in "Database Viewer stored SQL query" named "Single patient EHI export" — users run a pre-built query through OP's Database Viewer tool
- **Single-patient**: Yes, explicitly described as available "at any time … without developer assistance"
- **Bulk/multi-patient**: Yes, described as exporting "all the data for a patient population"
- **Access constraints**: Not documented. The mention of "Database Viewer" implies the user needs access to OP's query tool, which may require specific permissions
- **Fees**: Not mentioned in the EHI documentation; the disclosures page's price transparency section may address this separately
- **Developer assistance**: Explicitly stated as not required for single-patient export; unclear for bulk

The mechanism — a pre-built SQL query running against the database — suggests the export could be comprehensive (direct database access), but without seeing the query or its output, this is speculative.

## 4. Export Content: What's In It

### Documentation completeness

The entire publicly available EHI export documentation consists of **129 words** across 3 paragraphs (verified via `analysis/extract-ehi-documentation.py`):

1. **"Single Patient Export"** — names the feature and format
2. **"Multi-Patient Export"** — one sentence noting bulk capability
3. **"CSV"** — a generic Wikipedia-style definition of the CSV format

The documentation provides:
- ❌ No data dictionary
- ❌ No table/entity names
- ❌ No field names, types, or descriptions
- ❌ No schema or ERD
- ❌ No sample data
- ❌ No information about what data domains are included
- ❌ No information about file organization (one CSV or many? how related?)
- ❌ No value sets or code systems
- ❌ No export instructions beyond naming the SQL query
- ❌ No machine-readable artifacts

### Vendor's own content organization

There is nothing to present. The vendor provides zero structured information about export content. No entities, no tables, no fields, no categories.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes only the export mechanism (CSV via SQL query) and says nothing about content. The phrases "export electronic health information (EHI) for a single patient" and "export all the data for a patient population" imply comprehensive coverage, but these are bare assertions with no supporting detail.

The 2025 RWT results (page 7 of `OP_RWT_Results_Report_2025.pdf`) confirm the feature is actively used — 2,861 single-patient exports and 20 bulk exports across 5 test practices in Q4 2025 — and that "satisfaction is high" and "functionality is working as expected." This confirms a working feature exists but says nothing about what data it covers.

### 5b. Standardized domain coverage (top-down)

Without any data dictionary or field-level documentation, coverage cannot be assessed from the public documentation alone. Every domain below is rated based solely on what the documentation tells us — which is nothing.

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No documentation | Product stores extensive demographics including family/guardian relationships; cannot verify export |
| Encounters / visits | ❓ Unknown | No documentation | Product stores visit data (SOAP notes, sick visits, preventive exams); cannot verify |
| Problems / conditions | ❓ Unknown | No documentation | Product stores diagnoses; cannot verify |
| Medications / prescriptions | ❓ Unknown | No documentation | Product has e-prescribing with EPCS; cannot verify |
| Allergies | ❓ Unknown | No documentation | Product tracks allergies; cannot verify |
| Immunizations | ❓ Unknown | No documentation | Product has extensive VacLogic immunization engine; cannot verify |
| Vitals / growth data | ❓ Unknown | No documentation | Product stores growth charts, specialty curves; cannot verify |
| Lab results | ❓ Unknown | No documentation | Product has eLabs integration; cannot verify |
| Procedures | ❓ Unknown | No documentation | Cannot verify |
| Clinical notes / documents | ❓ Unknown | No documentation | Product stores SOAP notes, templates; cannot verify |
| Care plans / goals | ❓ Unknown | No documentation | Cannot verify |
| Orders / referrals | ❓ Unknown | No documentation | Product has referral workflows; cannot verify |
| Insurance / coverage | ❓ Unknown | No documentation | Product stores insurance data, eligibility checks; cannot verify |
| Claims / billing | ❓ Unknown | No documentation | Product has full RCM (superbills, claims, payments, denials); cannot verify |
| Payments | ❓ Unknown | No documentation | Product does payment posting; cannot verify |
| Patient communications | ❓ Unknown | No documentation | Product has patient portal messaging; cannot verify |
| Behavioral health data | ❓ Unknown | No documentation | Product tracks PHQ-9, GAD-7 scores longitudinally; cannot verify |
| Scanned documents | ❓ Unknown | No documentation | Product has document scanning, eFax; cannot verify |
| School/camp forms | ❓ Unknown | No documentation | Product has 175+ templates; cannot verify |

**Coverage is entirely unverifiable.** The export *may* be comprehensive — the SQL-query-against-database mechanism is consistent with a thorough export — but the documentation provides zero evidence either way.

## 6. Documentation Quality

Office Practicum's EHI export documentation is among the most minimal possible while still technically existing. Key issues:

- **A developer cannot use this export from the documentation alone.** Upon receiving CSV files, a developer would have no documentation to understand the schema, field semantics, relationships, or value encoding. Every field would require reverse-engineering.
- **No machine-readable artifacts exist** — no schemas, no sample data, no data dictionaries.
- **The CSV definition paragraph is filler** — it literally defines what CSV means rather than documenting the export content. This accounts for roughly a third of the documentation's word count.
- **The documentation satisfies the letter but not the spirit of (b)(10)** — it confirms an export exists but provides none of the technical detail needed for a patient or third party to actually use the exported data.

A generous interpretation: the internal export (the SQL query and its results) may actually be quite good, and the vendor simply failed to document it publicly. But from the public documentation alone, the export is opaque.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess coverage. There is no data dictionary, no schema, no table names, no field names — nothing that reveals what the export contains. The vendor makes generic claims ("export electronic health information," "export all the data") but provides zero evidence. Without seeing the actual SQL query, its output schema, or any sample data, coverage cannot be evaluated. The RWT results prove the feature is functional (2,861 exports) but say nothing about completeness.

**Axis 2 — Export approach: Unclear/undetermined**

The export mechanism — a "Database Viewer stored SQL query" producing CSV — is distinctive and does not match the common pattern of repackaging C-CDA or FHIR (g)(10). This is not a repackaged clinical exchange export; it's clearly a separate feature. However, without knowing what the query selects, it's impossible to determine whether it's a purpose-built comprehensive export or a narrow clinical subset. The mechanism *could* be purpose-built (direct database access suggests comprehensiveness), but the documentation doesn't confirm this.

### Key Findings

1. **Documentation is essentially non-existent**: The entire EHI export documentation is 129 words, of which ~45 are a generic CSV definition. There is no data dictionary, no schema, no sample data, and no description of what data domains are exported. (Source: `downloads/onc-certification-page.html`, verified via `analysis/extract-ehi-documentation.py`)

2. **The export feature is real and actively used**: RWT results from Q4 2025 show 2,861 single-patient exports and 20 bulk exports across 5 test practices, with "satisfaction is high" feedback. This is not a paper-only feature. (Source: `downloads/OP_RWT_Results_Report_2025.pdf`, page 7)

3. **The export mechanism is distinctive**: A pre-built SQL query ("Single patient EHI export") in OP's Database Viewer tool producing CSV is a unique approach — not a repackaged C-CDA or FHIR export. This suggests the vendor built something specific for (b)(10), but the absence of documentation makes it impossible to evaluate.

4. **Coverage is completely unverifiable from public documentation**: Office Practicum stores extensive data across clinical, billing, and specialty domains (pediatric growth data, immunization forecasting, behavioral health screenings, 175+ form templates). Whether any of this beyond basic clinical data appears in the export is unknown.

5. **The documentation gap is the core problem**: The export may be excellent internally; the failure is in public documentation. A patient or third-party developer receiving CSV files from this export would have no reference material to interpret the data.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined
Export format:   CSV
Entities:        N/A (no data dictionary)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes
Domains covered: 0 of 19 verifiable (export may cover more, but documentation provides no evidence)
```

### Bottom Line

Office Practicum has a functional EHI export feature that is actively used in production (2,861 single-patient exports in Q4 2025), but its public documentation is so thin — 129 words with no data dictionary, no schema, and no description of exported content — that it is impossible to assess what data the export actually covers. The single biggest gap is not necessarily in the export itself but in the documentation: without knowing what tables and fields are exported, neither patients nor developers can meaningfully use the data.

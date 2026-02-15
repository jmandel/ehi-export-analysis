# EHI Export Analysis: Office Practicum

**Product**: Office Practicum 21  
**Analysis date**: 2026-02-15  
**CHPL ID**: 15.04.04.3048.Offi.21.02.1.221121 (CHPL listing 11049)

## 1. Product Context

Office Practicum (OP) is a pediatric-specialty EHR and practice management platform developed by Connexin Software, Inc. It serves over 9,000 pediatricians across 48–49 states and is the dominant vendor in the pediatric EHR market. The product is an integrated platform covering:

- **Clinical EHR**: SOAP notes, pediatric-specific templates (175+ school/camp forms, sick visit templates, preventive exam templates aligned with AAP Periodicity Schedule), growth charts (including specialty curves for Down Syndrome, preemie), developmental assessments, VacLogic immunization forecasting engine, behavioral health monitoring (PHQ-9, GAD-7), allergy tracking, medication management with EPCS
- **Practice management**: Scheduling with well-visit recalls, patient flow tracking, real-time insurance eligibility validation
- **Billing & RCM**: Electronic superbill charges auto-generated during documentation, claims processing, payment posting, denial tracking, clearinghouse integration, revenue analysis
- **Lab integration**: Electronic lab orders and results (reference and in-house labs)
- **Patient portal**: Secure messaging, self-registration, online records access, prescription refill requests
- **Document management**: Scanning, bi-directional eFax
- **e-Prescribing**: Full EPCS support via Surescripts
- **Telehealth**: Via RemedyConnect acquisition
- **Interoperability**: C-CDA, FHIR API (g)(10), immunization registry reporting

This is a feature-rich product storing extensive patient data across clinical, billing, scheduling, document, and engagement domains. A complete EHI export should cover all of these.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `onc-certification-page.html` (397 KB) | Registered URL page; contains the entire EHI export documentation — 3 paragraphs (~129 words) under "Electronic Health Information Export" heading | **Primary source** — contains all available EHI export documentation |
| `onc-certification-info-disclosures.html` (404 KB) | Mandatory disclosures page; contains identical EHI export text in an accordion section, plus links to RWT plan/results PDFs | Duplicate of above; links to RWT PDFs are informative |
| `OP_RWT_Results_Report_2025.pdf` (943 KB, 10 pages) | 2025 Real World Testing results; page 7 reports 2,861 single-patient EHI exports and 20 bulk exports across 5 practices in Q4 2025 | Confirms feature is functional and used; **no technical detail** about export content |
| `screenshot-registered-url-ehi-section.png` (351 KB) | Screenshot of the EHI export section on the registered URL page | Visual confirmation of the text content |
| `screenshot-ehi-export-accordion-expanded.png` (311 KB) | Screenshot of the EHI export accordion expanded on the disclosures page | Visual confirmation of the text content |
| `screenshot-registered-url-onccert.png` (416 KB) | Screenshot of the ONC certification section on the registered URL page | Context only |
| `screenshot-disclosures-page-top.png` (770 KB) | Screenshot of the mandatory disclosures page top section | Context only |

**Additionally verified via live web fetch** (2026-02-15): The registered URL page at `https://www.officepracticum.com/op/population-health/onc-certification` was re-fetched live and confirmed to contain the same EHI export text with no updates or additional links.

**Additionally reviewed** (not in downloads/):
- 2024 RWT Results (fetched live): Reports only 5 single-patient and 6 bulk EHI exports in Q4 2024. Notes "EHI Export functionality was newly introduced."
- 2023 RWT Results (fetched live): Notes that a new button and tab were added in December 2023 to improve the EHI export workflow, separating it from CDA generation. No technical detail about export contents.
- 2025 RWT Plan (fetched live): Describes metric as counting single-patient and population exports. Acknowledges "this functionality is outside the daily workflow" and clients may not use it.

## 3. Export Mechanics

- **Format**: CSV (comma-separated values)
- **Mechanism**: Built-in SQL query accessible via the product's "Database Viewer" tool. The single-patient export uses a pre-built stored query named "Single patient EHI export." The multi-patient export is described separately but with no detail on how it is initiated.
- **Single-patient**: Yes — via the named SQL query "Single patient EHI export"
- **Bulk/population**: Yes — described as exporting "all the data for a patient population"
- **UI evolution**: Per the 2023 RWT, a new button and tab were added in December 2023 to streamline the export (previously, EHI export and CDA generation shared the same interface)
- **Access constraints**: No fees mentioned for the export itself. The feature appears available to all OP customers.
- **Developer assistance**: Not required for single-patient export (per documentation). Multi-patient export documentation is ambiguous on this point.

## 4. Export Content: What's In It

### What the documentation tells us

**Nothing.** The entire public EHI export documentation is 129 words (including the heading and a generic definition of CSV). Stripping the CSV definition paragraph (which is filler — it defines what a CSV file is), the substantive content is approximately 75 words across two paragraphs.

The documentation provides:
- The name of the SQL query ("Single patient EHI export")
- The output format (CSV)
- Two export modes (single patient, multi-patient)

The documentation does **not** provide:
- Any list of tables or entities exported
- Any field names, types, or descriptions
- Any data dictionary or schema
- Any sample data or example output
- Any information about how many CSV files are produced
- Any information about relationships between files
- Any information about what clinical domains are covered
- Any value sets, code systems, or coded field documentation
- Any instructions beyond the query name

### Vendor's own content organization

There is no vendor-provided content organization. No tables, entities, fields, or categories are documented anywhere in the publicly available artifacts.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

### What we can infer (but not confirm)

The mention of a "Database Viewer stored SQL query" suggests the export runs directly against OP's underlying database, which *could* mean the export extracts data from the native data model rather than projecting through a standard like C-CDA or FHIR. The 2023 RWT explicitly distinguishes EHI export from CDA generation ("a new button and tab were added" to separate "CDAs and full EHI"), confirming the EHI export is not simply a C-CDA repackaging.

However, without a data dictionary, schema, sample output, or any documentation of the query's scope, it is impossible to determine what tables or fields the query actually returns.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides **zero information** about what data domains the export covers. The documentation uses the phrase "export electronic health information (EHI) for a single patient" and "export all the data for a patient population," implying comprehensive coverage, but provides no evidence to support this claim.

There is no data dictionary, no table listing, no field listing, and no categorization of export content. The vendor's own organization of their export content is nonexistent.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No documentation | Product stores extensive demographics including family/guardian relationships; cannot assess |
| Encounters / visits | ❓ Unknown | No documentation | Product stores encounter data (SOAP notes, visit templates); cannot assess |
| Problems / conditions / diagnoses | ❓ Unknown | No documentation | Product stores diagnoses; cannot assess |
| Medications / prescriptions | ❓ Unknown | No documentation | Product stores medications and EPCS data; cannot assess |
| Allergies | ❓ Unknown | No documentation | Product stores allergy data; cannot assess |
| Immunizations | ❓ Unknown | No documentation | Product stores extensive immunization data (VacLogic); cannot assess |
| Vitals | ❓ Unknown | No documentation | Product stores vitals and growth chart data; cannot assess |
| Lab results | ❓ Unknown | No documentation | Product stores lab orders and results; cannot assess |
| Imaging / diagnostic reports | ❓ Unknown | No documentation | Limited imaging capability in ambulatory pediatric context; cannot assess |
| Procedures | ❓ Unknown | No documentation | Product stores procedure data; cannot assess |
| Clinical notes / documents | ❓ Unknown | No documentation | Product stores extensive clinical notes (SOAP, templates, forms); cannot assess |
| Care plans / goals | ❓ Unknown | No documentation | Product may store care plans; cannot assess |
| Orders / referrals | ❓ Unknown | No documentation | Product stores referral data; cannot assess |
| Insurance / coverage | ❓ Unknown | No documentation | Product stores insurance and eligibility data; cannot assess |
| Claims / billing | ❓ Unknown | No documentation | Product has full billing/RCM module (superbills, claims, payments, denials); cannot assess |
| Payments | ❓ Unknown | No documentation | Product stores payment data; cannot assess |
| Patient communications / portal messages | ❓ Unknown | No documentation | Product has patient portal with secure messaging; cannot assess |
| Specialty-specific (pediatric) | ❓ Unknown | No documentation | Product stores pediatric-specific data (growth charts, developmental assessments, school/camp forms, behavioral health screenings); cannot assess |

**Every domain is "Unknown."** The documentation is so thin that no coverage assessment is possible. This is not a case where we can identify specific gaps — we cannot confirm coverage of *any* domain, despite the product clearly storing data across all of them.

## 6. Documentation Quality

The EHI export documentation is **critically deficient**:

- **Data dictionary**: None
- **Schema**: None
- **Field documentation**: None (zero fields documented)
- **Table/entity documentation**: None (zero entities documented)
- **Sample data**: None
- **Machine-readable artifacts**: None
- **Value sets / code systems**: None
- **Relationships / foreign keys**: None
- **Export instructions**: Minimal — only the name of the SQL query

A developer receiving data from this export would have CSV file(s) with column headers and no documentation explaining what any column means, what values are expected, how files relate to each other, or what data domains are covered. Reverse-engineering would be the only option.

The third paragraph of the documentation — a generic definition of what a CSV file is — is notable as filler. It adds zero information about the export and reads as padding to make the section appear longer.

The 2023 and 2024 RWT results provide slightly more context (the feature was enhanced with a dedicated UI button in December 2023, usage grew from 11 exports in 2024 to 2,881 in 2025), but no RWT document contains any information about export content.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The export documentation is too thin to assess what the export contains. Three paragraphs totaling ~129 words (of which ~50 are a generic CSV definition) constitute the entire public documentation. There is no data dictionary, no schema, no sample data, no field-level documentation, and no information about which data domains are covered.

The export mechanism (a built-in SQL query against the database) and the 2023 RWT's distinction between "CDAs and full EHI" suggest this *may* be a genuine native database export rather than a C-CDA repackaging. However, without any documentation of what the query actually returns, this cannot be confirmed. The classification is "minimal/stub" because the documentation provides insufficient evidence to evaluate the export's completeness.

### Key Findings

1. **Documentation is essentially nonexistent.** The entire EHI export documentation is ~75 substantive words (excluding the generic CSV definition). Zero tables, zero fields, zero data domains are documented. This is among the thinnest EHI export documentation possible while technically existing. (Source: `onc-certification-page.html`, verified via live web fetch 2026-02-15)

2. **The export is not a C-CDA or FHIR repackaging.** The 2023 RWT results confirm that the EHI export was separated from CDA generation with a dedicated button/tab in December 2023. The mechanism — a "Database Viewer stored SQL query" — suggests native database-level extraction. This is a positive signal, but without documentation of what the query returns, it cannot be confirmed. (Source: 2023 RWT Results PDF, fetched live)

3. **The feature is actively used in production.** RWT results show 2,861 single-patient and 20 bulk exports in Q4 2025, up dramatically from 5 single-patient and 6 bulk exports in Q4 2024. This confirms the feature works and is being adopted. (Source: `OP_RWT_Results_Report_2025.pdf`, page 7)

4. **Coverage cannot be assessed at all.** For a product with extensive clinical, billing, scheduling, document management, and pediatric specialty capabilities, the documentation provides zero evidence of what is or isn't included in the export. No domain can be confirmed as covered.

5. **No downloadable artifacts exist.** All documentation is inline HTML text — no PDFs, schemas, sample files, data dictionaries, or any other downloadable documentation beyond RWT reports (which contain no export content detail).

### Summary Stats

```
Classification:  Minimal/stub
Export format:   CSV
Model type:      Likely native database (inferred from "Database Viewer stored SQL query"; unconfirmed)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (per documentation and RWT results: 20 bulk exports in Q4 2025)
Domains covered: 0 of 17 confirmed (all unknown due to absent documentation)
```

### Bottom Line

Office Practicum's EHI export appears to be a functional feature — actively used in production with thousands of exports — but its public documentation is among the worst available. A patient, provider, or developer receiving this export would get CSV files with no explanation of what they contain, how they're structured, or what data domains they cover. The single biggest gap is the complete absence of a data dictionary: without one, the export is a black box.

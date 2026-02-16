# EHI Export Analysis: Patagonia Health

**Product**: Patagonia Health EHR Version 6  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2139.Pata.06.01.1.221227 (CHPL ID 11147)

## 1. Product Context

Patagonia Health is a cloud-based EHR, practice management, and billing platform specifically designed for **public health departments** and **behavioral health agencies**. It serves local/county health departments, statewide public health systems, school-based health clinics, and community behavioral health organizations across 38+ states and 510+ counties. The company reports $622M+ in claims processed.

The product stores data across multiple domains relevant to EHI completeness:

- **Clinical**: Patient demographics, encounter documentation, problem lists, medication lists, allergies, immunizations, lab orders/results, vitals, clinical assessments (including behavioral health assessments, psychiatric evaluations, DSM-5 coded diagnoses, treatment plans, progress notes, group therapy notes), care plans, referrals, clinical documents.
- **Public health program data**: Communicable disease surveillance, contact tracing, immunization registry data, vaccine inventory tracking, community outreach records, program eligibility determinations, state-specific program reporting (HRSA UDS).
- **Billing/financial**: Insurance claims, insurance verification, billing codes (ICD-10, CPT), financial reports, clearinghouse transactions.
- **Practice management**: Appointment scheduling, patient registration, consent forms, case management, referral tracking.
- **Patient portal (MyHealth)**: Secure messages, patient-completed questionnaires, demographic updates, portal notifications.
- **E-prescribing**: Medication orders, pharmacy transmissions, drug interaction checks.
- **Telehealth**: Virtual visit capabilities integrated into clinical workflow.

This is a specialty-focused EHR with significant data beyond standard clinical summaries — behavioral health assessments, public health surveillance, and program compliance data are core to its value proposition. A complete EHI export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Type | Size | Description | Informativeness |
|---|---|---|---|---|
| `ehi-export-section.html` | HTML fragment | 3,139 bytes | Extracted EHI Export section from ONC certification page — ~399 words describing export workflow, formats, access control | **Primary** — contains all EHI export documentation |
| `onc-certified-hit-page.html` | HTML page | 50,851 bytes | Full ONC certification page including EHI section, MU info, API links | Secondary — EHI section is a small portion |
| `PatientHealth-Data-API-Documentation-v1.1.pdf` | PDF, 7 pages | 372 KB | Proprietary REST API (April 2018) returning CCDA XML in JSON wrappers; lists 10 available CCDA sections | Supplementary — not the (b)(10) export, but enumerates available clinical sections |
| `SmartOnFHIR-API-Documentation.pdf` | PDF, 67 pages | 860 KB | SMART on FHIR / (g)(10) API docs covering 20 FHIR R4 resources (Feb 2026) | Supplementary — this is the (g)(10) API, not (b)(10) |
| `FHIRBaseURL.json` | JSON | 4,827 bytes | FHIR Bundle with Endpoint/Organization resources for API discovery | Minimal |
| `PatagoniaHealth-MeaningfulUse-Stage3-CostsandLimitations-May2018.pdf` | PDF, 2 pages | 120 KB | MU Stage 3 supplemental costs (Direct Messaging, lab interfaces, immunization registries) | Minimal — not EHI export related |
| `screenshot-ehi-export-section-1.png` | Screenshot | 256 KB | Visual of EHI section (role access, single patient export) | Supplementary — confirms HTML text |
| `screenshot-ehi-export-section-2.png` | Screenshot | 234 KB | Visual of EHI section (multi-patient export, formats, API links) | Supplementary — confirms HTML text |
| `screenshot-ehi-export-section-3.png` | Screenshot | 265 KB | Bottom of page (FHIR links, footer) | Minimal |
| `screenshot-main-page-top.png` | Screenshot | 851 KB | Top of ONC certification page | Minimal |

**Most informative**: `ehi-export-section.html` — it is the entire (b)(10) EHI export documentation. The Patient Health Data API PDF is secondarily useful for listing available CCDA sections.

**Least informative**: The FHIR API docs, FHIR base URLs, and MU costs PDF are not related to the (b)(10) EHI export.

## 3. Export Mechanics

- **Clinical data format**: CCDA 2.1 Release 2, USCDI v1 (XML)
- **Billing data format**: CSV, XLSX, or PDF
- **Mechanism**: In-product UI
  - **Single patient**: Reports > Medical Practice Reports > Electronic Health Information (EHI) Export → select provider/date range → search patient → select record → click "EHI Export" → download file
  - **Multi-patient**: Same path → "Multi Patients" button → schedule execution date/time → asynchronous processing (Queued → Completed)
  - **Billing (single)**: Dashboard > Billing > Search > Claims → download in CSV/XLSX
  - **Billing (multi)**: Dashboard > Billing > Reports > Claim > Detail → set all date filters to "All" → run report → export
- **Access control**: Role-based. Practice Administrator enables "EHI Export & Schedule Data Export" permission per user. Separate billing role required for financial data.
- **Single-patient**: Yes
- **Bulk export**: Yes (multi-patient with scheduling)
- **Fees/constraints**: None documented for the export itself

## 4. Export Content: What's In It

### No data dictionary, schema, or sample data

The EHI export documentation provides **zero field-level detail**. There is:
- No data dictionary
- No schema or format specification
- No sample export files
- No field names, types, descriptions, value sets, or relationships
- No documentation of what CCDA sections are included in the EHI export specifically

The documentation is purely procedural — ~399 words of step-by-step instructions describing how to click through the UI to trigger an export. It does not describe what data the export contains beyond the format labels "CCDA 2.1 Release 2 USCDI v1" (clinical) and "CSV or XLSX" (billing).

### Clinical export content (inferred)

The clinical export is stated to be CCDA 2.1 USCDI v1 XML. The EHI export page does not enumerate which CCDA sections are included. However, the separately documented Patient Health Data API v1.1 (April 2018) lists 10 CCDA sections available via their proprietary API:

| Section API Name | Section Display Name |
|---|---|
| demographics | Patient Demographics |
| allergies | Allergies and Intolerances |
| assessments | Assessment |
| encounters | Encounters |
| goals | Goals |
| immunizations | Immunizations |
| medications | Medications |
| procedures | Procedures |
| results | Results |
| vitalsigns | Vital Signs |

These are standard CCDA clinical summary sections. The EHI export likely includes these same sections (or a subset), but this is inference — the EHI documentation itself does not confirm which sections are in the export.

### Billing export content (unknown)

The billing data export is described only as "Claim data can then be downloaded in CSV or XLSX formats for computation." No field definitions, no column names, no schema, no sample data. The content is completely undocumented.

### Vendor's own content organization

The vendor does not organize their export by entities, tables, or categories. The entire documentation consists of two categories:

| Category | Format | Documentation Depth | Fields Documented |
|---|---|---|---|
| Clinical data | CCDA 2.1 XML | Format named only — no section or field detail | 0 |
| Billing data | CSV/XLSX/PDF | Format named only — no schema or field detail | 0 |

**Total entities/tables documented: 0**  
**Total fields documented: 0**  
**Fields with descriptions: 0**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's EHI export documentation describes exactly two data categories:

1. **Clinical data** — exported as CCDA 2.1 XML. The CCDA standard constrains this to the standard clinical summary sections (demographics, problems, medications, allergies, immunizations, labs, vitals, procedures, encounters, goals, assessments). This is the same data available via their (g)(10) FHIR API and their older proprietary API. No vendor extensions or custom sections are mentioned.

2. **Billing/claims data** — exported separately via a different UI workflow as CSV/XLSX. No detail on what fields or claim types are included.

The two categories are exported through entirely separate workflows with no documented relationship between them. There is no indication that the vendor's native data model is exposed — the clinical export is a standard C-CDA projection, not a database export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CCDA demographics section (inferred from API doc) | CCDA covers basic demographics but may miss fields specific to public health (race/ethnicity detail, interpreter needs, program enrollment) |
| Encounters / visits | ⚠️ Partial | CCDA encounters section (inferred) | Standard encounter data likely present; telehealth-specific metadata unknown |
| Problems / conditions / diagnoses | ⚠️ Partial | CCDA problems section; DSM-5 coded diagnoses are core to product | CCDA may include ICD-10 problems but behavioral health-specific DSM-5 coded diagnoses may not be fully represented in CCDA structure |
| Medications / prescriptions | ⚠️ Partial | CCDA medications section (inferred) | Standard med list likely present; e-prescribing transmission history unlikely |
| Allergies | ✅ Covered | CCDA allergies section (inferred) | Standard coverage expected |
| Immunizations | ⚠️ Partial | CCDA immunizations section (inferred) | Patient immunization records likely present; vaccine inventory/registry sync data is operational, not EHI |
| Vitals | ✅ Covered | CCDA vital signs section (inferred) | Standard coverage expected |
| Lab results | ⚠️ Partial | CCDA results section (inferred) | Results likely present; lab order details and interface messages unknown |
| Imaging / diagnostic reports | ⚠️ Partial | CCDA may include diagnostic report entries | Product scope unclear — likely limited imaging for public/behavioral health |
| Procedures | ✅ Covered | CCDA procedures section (inferred) | Standard coverage expected |
| Clinical notes / documents | ⚠️ Partial | CCDA may include some notes via DocumentReference/Assessment sections | **Significant concern**: behavioral health progress notes, group therapy notes, psychiatric evaluations, case management notes are core to this product. CCDA has limited support for structured behavioral health documentation. Custom clinical templates likely not represented. |
| Care plans / goals | ⚠️ Partial | CCDA goals section (inferred); CarePlan in FHIR API | Treatment plans for behavioral health patients are core — CCDA care plan sections may not capture the full structured behavioral health treatment plan data |
| Orders / referrals | ❌ Not covered | No mention in EHI export; ServiceRequest in FHIR API only | Product supports case management with referral tracking; not addressed in export documentation |
| Insurance / coverage | ❌ Not covered | No mention in EHI export; Coverage in FHIR API only | Product stores insurance information from registration and automated verification; not addressed in export documentation |
| Claims / billing | ⚠️ Partial | Separate CSV/XLSX export described but completely undocumented | Billing export exists but with zero field-level documentation; impossible to assess completeness |
| Payments | ❌ Not covered | No mention | Product processes $622M+ in claims; payment/remittance data not addressed |
| Consents / directives | ❌ Not covered | No mention | Product supports electronic consent forms; not addressed in export |
| Patient communications / portal messages | ❌ Not covered | No mention | Product has MyHealth patient portal with secure messaging; not addressed |
| Specialty: Behavioral health | ❌ Not covered | No evidence of BH-specific data in CCDA export | **Major gap**: psychiatric evaluations, DSM-5 coded assessments, treatment plans, progress notes, group therapy notes are core to product; CCDA cannot represent most of this structured data |
| Specialty: Public health | ❌ Not covered | No mention | **Major gap**: communicable disease surveillance, contact tracing, program eligibility, community outreach are core to product; none addressed in export |

**Summary**: Of 19 applicable domains, 3 appear adequately covered (allergies, vitals, procedures), 8 are partially covered (via CCDA limitations or undocumented billing export), and 8 are not covered at all. The uncovered domains include several that are core to the product's specialty focus — behavioral health assessments and public health program data.

## 6. Documentation Quality

The EHI export documentation is among the thinnest possible while still technically existing. It consists of ~399 words of procedural UI instructions on an ONC certification page.

**What's present**:
- Export format names (CCDA 2.1, CSV/XLSX)
- UI navigation paths for triggering exports
- Access control setup steps
- Single-patient and multi-patient workflows

**What's absent**:
- Data dictionary (none)
- Field definitions (none)
- Schema or format specification (none)
- Sample data files (none)
- Value set or code system documentation (none)
- Relationship documentation (none)
- Machine-readable artifacts (none for EHI export)
- Documentation of what CCDA sections the export includes
- Documentation of what columns/fields the billing CSV contains

**Could a developer build an import?** For clinical data: a developer would need to parse generic CCDA 2.1 XML using general CCDA knowledge — the vendor provides no custom profile information, no extension documentation, and no indication of what sections are actually populated. For billing data: impossible without reverse-engineering the CSV/XLSX output, as there is zero documentation of the format.

The documentation reads as a compliance checkbox — procedural instructions for internal users, not technical documentation for data portability.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The clinical EHI export is a C-CDA 2.1/USCDI v1 projection — the same standard clinical summary data that the (g)(10) FHIR API and the older proprietary API already provide. The billing export adds CSV/XLSX claims data through a separate workflow, but with no documentation of its contents. There is no evidence that the vendor's native data model (with its behavioral health assessments, public health program data, custom templates, etc.) is exposed through the export.

### Key Findings

1. **The clinical EHI export is a CCDA repackaging, not a native data export.** The export produces CCDA 2.1 USCDI v1 XML — essentially the same clinical summary data available through the (g)(10) FHIR API. This is a textbook case of the (b)(10)/(g)(10) conflation, where the vendor treats their clinical summary document as the "all EHI" export. (`ehi-export-section.html`, line 17)

2. **Behavioral health and public health data — the product's core specialty — appear entirely absent from the export.** Patagonia Health's primary differentiator is its behavioral health (psychiatric assessments, DSM-5 coding, treatment plans, group therapy notes) and public health functionality (disease surveillance, contact tracing, program data). None of this specialty data is addressed in the export documentation, and CCDA 2.1 cannot represent most of it. (`product-research.md`)

3. **The billing export exists but is completely undocumented.** The vendor does acknowledge that billing data needs to be exported separately (a positive distinction from vendors who only export clinical summaries), but provides zero documentation of the billing CSV/XLSX format — no field names, no schema, no sample data. (`ehi-export-section.html`, lines 19-20)

4. **Documentation is near-minimal: ~399 words with no data dictionary.** The entire EHI export documentation is procedural UI instructions. There are no field-level details, no schema, no sample data, and no machine-readable artifacts. Total entities documented: 0. Total fields documented: 0. (`analysis/parse_artifacts.py` output)

5. **The export is split across two disconnected workflows with no correlation mechanism.** Clinical data (CCDA) and billing data (CSV) are exported through entirely different UI paths with no documented way to link records across the two outputs.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   CCDA 2.1 XML (clinical) + CSV/XLSX (billing)
Model type:      Standard projection (C-CDA) + undocumented tabular (billing)
Entities:        0 documented (CCDA sections inferred: ~10; billing: unknown)
Fields:          0 documented
Descriptions:    N/A (0 fields documented)
Sample data:     No
Bulk export:     Yes (multi-patient with scheduling)
Domains covered: 3 of 19 applicable domains adequately covered
```

### Bottom Line

Patagonia Health's EHI export is a C-CDA clinical summary repackaged as a (b)(10) export, supplemented by an undocumented billing CSV export. A patient or provider would receive a standard clinical summary and raw claims data, but would **not** get the behavioral health assessments, public health program data, custom template data, portal messages, or any of the specialty-specific information that makes this product what it is. The single biggest gap is the complete absence of behavioral health and public health specialty data — the core value proposition of this EHR — from the export.

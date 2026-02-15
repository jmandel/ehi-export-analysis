# EHI Export Analysis: Patagonia Health

**Product**: Patagonia Health EHR Version 6
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.2139.Pata.06.01.1.221227 (CHPL #11147)

## 1. Product Context

Patagonia Health EHR is a cloud-based, integrated EHR/practice management/billing platform specifically designed for **public health departments** and **behavioral health agencies**. The company serves 510+ counties across 38+ states and has processed $622M+ in claims. Key customers include county health departments (e.g., Fairfax County VA, Cleveland County NC) and community behavioral health organizations.

The product's data footprint extends well beyond standard ambulatory clinical data:

- **Clinical documentation**: Customizable clinical templates, progress notes, encounter documentation, problem lists, medication lists, allergy lists, immunizations, labs, vitals, care plans
- **Behavioral health**: Psychiatric assessments, DSM-5 coded diagnoses, treatment plans, progress notes, group therapy notes, case management notes
- **Public health programs**: Communicable disease surveillance, contact tracing, immunization registry sync, vaccine inventory, community outreach records, program eligibility
- **Practice management**: Scheduling, patient registration, consent forms, referral tracking, case management
- **Billing/revenue cycle**: Insurance claims, insurance verification, clearinghouse transactions, financial reporting
- **Patient portal (MyHealth)**: Secure messaging, questionnaires, consent forms, demographic updates
- **E-prescribing**: Medication orders transmitted to pharmacies via Surescripts
- **Telehealth**: Embedded audio/video visit capabilities

This breadth is critical context: a complete EHI export should cover clinical, behavioral health, public health, billing, and patient communication data — not just standard ambulatory clinical summaries.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `ehi-export-section.html` | 3.1 KB (399 words) | Extracted HTML of the EHI Export section from the ONC certification page. Contains the complete (b)(10) documentation. | **Most informative** — this is the entirety of the vendor's EHI export documentation |
| `onc-certified-hit-page.html` | 49.7 KB | Full ONC certification page containing the EHI section plus MU and API links | Context for the EHI section |
| `PatientHealth-Data-API-Documentation-v1.1.pdf` | 363.5 KB, 7 pages | Proprietary REST API (April 2018) returning CCDA XML in JSON wrappers. Lists 19 CCDA sections. | Moderately informative — shows what CCDA sections the vendor supports |
| `SmartOnFHIR-API-Documentation.pdf` | 840.2 KB, 67 pages | (g)(10) FHIR R4 API documentation covering 20 FHIR resources with SMART/OAuth2 | Reference only — this is the FHIR API, not the (b)(10) export |
| `FHIRBaseURL.json` | 4.7 KB | FHIR service base URLs for 2 test organizations | Not relevant to (b)(10) |
| `PatagoniaHealth-MeaningfulUse-Stage3-CostsandLimitations-May2018.pdf` | 117.1 KB, 2 pages | MU Stage 3 costs/limitations for Direct Messaging, lab interfaces, immunization registries | Not relevant to (b)(10) |
| `screenshot-ehi-export-section-1.png` | 249.5 KB | Screenshot of EHI export section (role-based access, single patient export) | Corroborates HTML text |
| `screenshot-ehi-export-section-2.png` | 228.1 KB | Screenshot of EHI export section (multi-patient export, file formats) | Corroborates HTML text |
| `screenshot-ehi-export-section-3.png` | 258.8 KB | Screenshot of page bottom (FHIR links, footer) | Minimal |
| `screenshot-main-page-top.png` | 831.1 KB | Screenshot of page top (MU overview) | Minimal |

**No data dictionary, schema, sample data, or field-level documentation exists for the EHI export.** The entire (b)(10) documentation is 399 words of procedural text describing UI navigation steps.

## 3. Export Mechanics

**Clinical data export:**
- **Format**: C-CDA 2.1 Release 2, USCDI v1 (XML)
- **Mechanism**: UI-based. Reports → Medical Practice Reports → Electronic Health Information (EHI) Export
- **Single-patient**: Select provider (or all), optional date range, search for patient, click "EHI Export," download file locally
- **Multi-patient (bulk)**: Same path, click "Multi Patients" button, schedule date/time for asynchronous execution. Status tracked as Queued → Completed.

**Billing data export (separate workflow):**
- **Format**: CSV, XLSX, or PDF
- **Single-patient**: Dashboard → Billing → Search → Claims → download
- **Multi-patient**: Dashboard → Billing → Reports → Claim → Detail, set Claim Receive Date / Claim Service Date / Claim Submitted Date to "All," run report, export

**Access control**: Role-based. Practice Administrator enables "EHI Export & Schedule Data Export" permission for users. A separate billing role is needed for financial data extraction.

**No API-based export**: The Patient Health Data API (v1.1) and FHIR API are mentioned on the same page but are described under separate headings ("Patient Health Data API and FHIR Access") and are not presented as part of the (b)(10) EHI export workflow.

**Fees**: No fees or costs mentioned specifically for EHI export. The costs/limitations document (May 2018) covers Direct Messaging and lab interfaces but does not address EHI export.

## 4. Export Content: What's In It

### Clinical export (C-CDA)

The clinical EHI export produces C-CDA 2.1 Release 2 documents conforming to USCDI v1. No data dictionary or field-level documentation is provided. The vendor's Patient Health Data API documentation (a separate mechanism, not the (b)(10) export itself) lists 19 CCDA sections that the system can produce:

| CCDA Section | Section Name |
|---|---|
| Patient Demographics | demographics |
| Care Team | careteam |
| Allergies and Intolerances | allergies |
| Assessment | assessments |
| Encounters | encounters |
| Functional Status | functionalstatus |
| Goals | goals |
| Health Concerns | healthconcerns |
| Immunizations | immunizations |
| Medical Equipment | medicalequipment |
| Medications | medications |
| Mental Status | mentalstatus |
| Plan of Treatment | planoftreatment |
| Problem | problem |
| Procedures | procedures |
| Reason for Referral | reasonforreferral |
| Results | results |
| Social History | socialhistory |
| Vital Signs | vitalsigns |

These 19 sections represent standard C-CDA content. There is no documentation of vendor extensions, custom sections, or additional data elements beyond what CCDA 2.1 / USCDI v1 specifies. The EHI export documentation itself does not even enumerate these sections — the list above comes from the Patient Health Data API document (a different mechanism entirely).

### Billing export (CSV/XLSX)

The billing export is described in 2 sentences per workflow (single/multi-patient). The documentation states:
- Single-patient: "Claim data can then be downloaded in CSV or XLSX formats for computation."
- Multi-patient: "Export data in CSV or XLSX formats for computation."

**There is no schema, field list, sample data, or any documentation whatsoever about what fields, tables, or data elements the billing export contains.** We do not know if it includes claim line items, diagnosis codes, CPT codes, payer information, payment status, denial reasons, or any other billing detail. The only certainty is that some form of claims data can be downloaded.

### Vendor's own content organization

The vendor does not organize their export into named entities, tables, or categories. The only structural distinction is:
1. **Clinical data** → C-CDA XML (one document per patient)
2. **Billing data** → CSV/XLSX (format and content undocumented)

There is no data dictionary to inventory. No table names, no field counts, no entity-level breakdown exists.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's EHI export documentation describes exactly two data categories:

1. **Clinical data (CCDA)**: Standard C-CDA 2.1 clinical summary content. This is the same data available through the (g)(10) FHIR API and the proprietary Patient Health Data API — a USCDI v1 clinical summary. The vendor has not distinguished the (b)(10) export from their existing clinical interoperability outputs.

2. **Billing data (CSV/XLSX)**: An entirely separate workflow accessible through the Billing module. No schema or content description is provided. This acknowledges that EHI extends beyond clinical summaries, but without any documentation of what the billing export contains, its adequacy cannot be assessed.

Notable absences in the vendor's own terms:
- No mention of behavioral health assessment data (psychiatric evaluations, DSM-5 assessments, treatment plans, group therapy notes)
- No mention of public health program data (disease surveillance, contact tracing, vaccine inventory, community outreach)
- No mention of custom clinical template data
- No mention of patient portal data (secure messages, questionnaires)
- No mention of uploaded documents or images
- No mention of e-prescribing transaction data
- No mention of referral tracking or case management records

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | CCDA demographics section | Standard CCDA demographic fields |
| Encounters / visits | ✅ Covered | CCDA encounters section | Standard encounter data |
| Problems / conditions | ✅ Covered | CCDA problem section | Standard problem list |
| Medications / prescriptions | ✅ Covered | CCDA medications section | Medication list; e-prescribing transaction history unclear |
| Allergies | ✅ Covered | CCDA allergies section | Standard allergy data |
| Immunizations | ✅ Covered | CCDA immunizations section | Standard immunization records |
| Vitals | ✅ Covered | CCDA vital signs section | Standard vital signs |
| Lab results | ✅ Covered | CCDA results section | Lab results; lab order details unclear |
| Imaging / diagnostic reports | ⚠️ Partial | CCDA may include some diagnostic reports; no explicit mention | Product stores documents; no imaging-specific export documented |
| Procedures | ✅ Covered | CCDA procedures section | Standard procedure data |
| Clinical notes / documents | ⚠️ Partial | CCDA assessment/mental status/functional status sections; no mention of uploaded documents | Product supports document uploads and extensive note types (BH progress notes, group notes); CCDA captures structured notes only |
| Care plans / goals | ✅ Covered | CCDA goals and plan of treatment sections | Standard care plan data |
| Orders / referrals | ⚠️ Partial | CCDA "reason for referral" section | Product has full referral tracking and case management; only referral reason appears in CCDA |
| Insurance / coverage | ❌ Not covered | No insurance/coverage data in clinical CCDA; billing export content unknown | Product stores insurance information and automated verification data; significant gap |
| Claims / billing | ⚠️ Partial | Separate billing export in CSV/XLSX; no schema or field documentation | Product processes $622M+ in claims; billing export exists but content is entirely undocumented |
| Payments | ❌ Not covered | No payment data mentioned | Product handles revenue cycle; payment data likely exists but is not addressed |
| Consents / directives | ❌ Not covered | No consent data in export | Product manages electronic consent forms; not exported |
| Patient communications / portal messages | ❌ Not covered | No portal data in export | Product has MyHealth portal with secure messaging; not exported |
| Specialty — Behavioral health | ❌ Not covered | No BH-specific data beyond standard CCDA mental status/assessment sections | **Critical gap.** Product's core market. Stores psychiatric assessments, DSM-5 diagnoses, treatment plans, progress notes, group therapy notes. CCDA cannot represent most of this structured data. |
| Specialty — Public health | ❌ Not covered | No public health program data in export | **Critical gap.** Product's core market. Stores communicable disease surveillance, contact tracing, vaccine inventory, community outreach, program eligibility. None of this appears in the export. |

**Summary**: 10 of 20 applicable domains are covered (all via standard CCDA), 4 are partially covered, and 6 are not covered at all. The two most critical gaps — behavioral health and public health program data — are the product's defining specialties.

## 6. Documentation Quality

The EHI export documentation is **extremely thin**:

- **Total documentation**: 399 words of inline HTML on the ONC certification page
- **No data dictionary**: Zero field-level documentation for either the clinical or billing export
- **No schema**: No machine-readable format specification for the billing CSV/XLSX output
- **No sample data**: No example export files provided
- **No field definitions**: No description of data types, value sets, cardinality, or constraints
- **No relationship documentation**: No description of how clinical and billing exports relate or how to correlate records
- **No CCDA profile documentation**: The vendor does not describe which CCDA sections are included in the EHI export or whether any vendor-specific extensions are used. The 19-section list in this analysis comes from the Patient Health Data API document (a separate mechanism).

The documentation is entirely **procedural** — it describes UI navigation steps ("click here, then here") rather than documenting what data is exported. A developer receiving this export would need to:
1. Parse C-CDA 2.1 XML using generic CCDA knowledge (feasible but no vendor-specific guidance)
2. Reverse-engineer the billing CSV/XLSX format with zero documentation (not feasible without sample data)

The documentation could not serve as a basis for building a data import pipeline. It reads as a compliance checkbox rather than a genuine effort at data portability.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The clinical EHI export is C-CDA 2.1 / USCDI v1 — the same standard clinical summary available through the vendor's FHIR and proprietary APIs. This is a textbook case of repackaging existing clinical interoperability outputs as the (b)(10) export. The billing export in CSV/XLSX is a step beyond pure C-CDA, but with zero documentation of its content, it cannot be credited as a meaningful native export component.

### Key Findings

1. **C-CDA repackaging as (b)(10)**: The clinical EHI export is explicitly described as "CCDA 2.1 Release 2 USCDI v1" — the same standard clinical summary the vendor already provides through its FHIR API and proprietary Patient Health Data API. This covers standard ambulatory clinical data but not the vendor-specific data that distinguishes this product. (Source: `ehi-export-section.html`)

2. **Critical specialty data gaps**: The product's two core markets — behavioral health and public health — generate extensive specialty data (psychiatric assessments, DSM-5 coding, disease surveillance, contact tracing, vaccine inventory) that C-CDA cannot represent. None of this data is addressed in the export documentation. (Source: `product-research.md` vs. `ehi-export-section.html`)

3. **Billing export exists but is entirely undocumented**: The vendor acknowledges billing data as part of EHI and provides a separate workflow to export claims in CSV/XLSX, but provides zero documentation of what fields or data elements are included. This makes the billing export practically unusable for import purposes. (Source: `ehi-export-section.html`)

4. **No data dictionary at all**: The entire (b)(10) documentation is 399 words of procedural UI instructions. There are no table names, field names, data types, value sets, schemas, or sample data for any part of the export. (Source: `ehi-export-section.html`, verified word count)

5. **Multi-patient export supported**: The vendor does offer bulk/multi-patient export with asynchronous scheduling — a positive feature that some vendors lack. However, the exported content is still limited to C-CDA clinical summaries and undocumented billing CSVs. (Source: `ehi-export-section.html`)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA 2.1 XML (clinical) + CSV/XLSX (billing)
Model type:      Standard projection (CCDA), not native database
Entities:        N/A (no data dictionary; CCDA is a single document per patient)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (multi-patient with scheduled execution)
Domains covered: 10 of 20 applicable domains (fully); 4 partial
```

### Bottom Line

A patient or provider receiving this export would get a standard C-CDA clinical summary and an undocumented billing CSV — together covering perhaps 30–40% of the data this product stores. The most critical gaps are the product's defining specialties: behavioral health assessment data (psychiatric evaluations, DSM-5 diagnoses, treatment plans, group therapy notes) and public health program data (disease surveillance, contact tracing, vaccine inventory, community outreach). These specialty domains are the entire reason organizations choose Patagonia Health over a general-purpose EHR, yet they are absent from the export. The vendor has taken its existing clinical interoperability output (C-CDA) and relabeled it as an EHI export, which is the most common (b)(10) compliance failure pattern.

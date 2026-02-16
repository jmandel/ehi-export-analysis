# EHI Export Analysis: Core Solutions Inc

**Product**: Cx360 (Version 7)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2703.Cx36.07.00.1.171226 (CHPL ID 9168)

## 1. Product Context

Cx360 is a **behavioral health and IDD (intellectual/developmental disabilities) EHR and practice management platform** built by Core Solutions Inc. It is not a general-purpose ambulatory EHR — it is purpose-built for community mental health centers, CCBHCs, substance use disorder programs, and IDD agencies. The product serves 35,000+ users and 400,000+ lives.

**Key data domains the product stores:**

- **Clinical (behavioral health)**: Comprehensive psychiatric/addiction/social history assessments, evidence-based screening tools (depression, PTSD, anxiety, substance use), treatment plans with trackable goals and interventions, progress notes linked to treatment goals, medication management and MAR
- **IDD-specific**: Person-centered life plans, valued outcomes tracking, DSP task assignments, behavioral tracking
- **Child & family services**: Foster care management, family engagement, trauma-informed documentation
- **Billing/RCM**: Full revenue cycle — claims submission, claim scrubbing, ledger/bill generation, accounts receivable, authorization management, payment tracking
- **Patient engagement**: Client portal with secure messaging, bill payment, self-surveys
- **Scheduling**: Appointments, clinician availability, telehealth sessions
- **Mobile/field**: EVV records (GPS/timestamps), ambient documentation, mileage tracking (Cx360 GO, DSP Assist)
- **Labs & e-prescribing**: Electronic lab orders/results, e-prescribing via Dr. First integration
- **Standard clinical**: Demographics, encounters, problems, medications, allergies, immunizations, vitals, procedures

This baseline is critical because Cx360's core value is behavioral health-specific data that goes far beyond what standard clinical exchange formats can represent.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Electronic-Health-Information-Export-Doc.pdf` (2.4 MB, 12 pages) | The sole EHI export documentation. Pages 1–2: cover/overview. Pages 3–6: screenshots of the export UI (single patient and bulk export). Pages 7–12: C-CDA data dictionary with 24 sections and 82 data elements. | **Primary source** — this is the entire body of EHI export documentation |
| `Electronic-Health-Information-Export-Doc.txt` (7.6 KB) | Plain text extraction of the PDF via pdftotext. Table columns are garbled due to multi-column layout. | Low — useful for keyword search but unreliable for structured data |
| `enrichment/ccd-sections.json` (20 KB) | Machine-readable JSON extraction of the PDF's data dictionary: 24 C-CDA sections, 82 data elements, template IDs, XPATH paths, code system OIDs. Hand-curated from rendered PDF pages. | **High** — verified against PDF; accurate structured representation |
| `enrichment/coverage-accounting.json` (805 bytes) | Extraction metadata: counts and method notes | Supplementary — confirms extraction methodology |
| `enrichment/extract-ccd-sections.ts` (19 KB) | TypeScript script used to produce the JSON extraction | Supplementary — documents extraction process |
| `enrichment/README.md` (1.3 KB) | Enrichment documentation | Supplementary |

**Verification notes**: I independently confirmed the PDF is 12 pages (via `pdfinfo`), created 2023-12-06 by author "bbala1" using "Microsoft: Print To PDF." The enrichment JSON was verified against the raw PDF text extraction — section names, field names, and code system OIDs match. The prior report's claim of 24 sections and 82 data elements is confirmed.

## 3. Export Mechanics

- **Format**: CCD (Continuity of Care Document) — a C-CDA XML document conforming to §170.205(a)(4) HL7 CDA R2 Consolidated CDA Templates DSTU R2.1, August 2015. A human-readable Adobe PDF rendering is also generated.
- **Mechanism**: UI-based export within the Cx360 application
  - **Single patient**: Via "Patient Summary Report Screen" — users select a patient, choose which C-CDA sections to include (15 checkboxes), click Print/Download
  - **Bulk export**: Via "CCDA Management" utility — users select multiple patients by provider or appointment date, click "Generate CCD"
  - **On-demand**: Images and clinical notes can be downloaded separately as PDF (mentioned in the overview but not detailed)
- **Single-patient**: Yes
- **Bulk capability**: Yes (by provider or appointments)
- **Access constraints**: No fees or special access constraints documented. Appears to be available to authorized clinical users within the application.

## 4. Export Content: What's In It

### Structure

The export is a **standard C-CDA CCD document** — not a native database export. The data dictionary documents **24 C-CDA sections** containing **82 data elements** total.

### Documentation depth

- **Field names**: Yes — 82 data elements named
- **Descriptions**: No — zero fields have descriptions beyond the field name
- **Data types**: Not documented
- **XPATH/Entry paths**: 30 of 82 elements (37%) have XPATH or C-CDA entry template references
- **Code system OIDs**: 27 of 82 elements (33%) reference code systems (SNOMED, ICD-10, LOINC, RxNorm, NDC, CVX, CPT-4, HCPCS, NCI)
- **Relationships/foreign keys**: Not applicable (C-CDA is document-structured, not relational)
- **Value sets**: Code system names referenced but no value set bindings documented
- **Sample data**: None provided
- **Machine-readable schemas**: None beyond the enrichment JSON (which was created by the prior collection agent, not the vendor)

### Vendor's own content organization

The vendor organizes the export as C-CDA sections. The full inventory is in `analysis/full-entity-inventory.json`.

| C-CDA Section | Fields | w/ Code System | w/ XPath |
|---|---|---|---|
| Patient Demographics/Information | 6 | 3 | 6 |
| Provider's name and office contact information | 3 | 0 | 3 |
| Date and Location of visit | 2 | 0 | 2 |
| Chief Complaint and Reason for visit | 1 | 0 | 0 |
| Encounters | 5 | 2 | 1 |
| Immunizations | 9 | 3 | 1 |
| Instructions | 1 | 1 | 1 |
| Treatment Plan | 2 | 1 | 2 |
| Social History | 3 | 2 | 1 |
| Problems | 3 | 1 | 1 |
| Medications | 5 | 1 | 1 |
| Medication Allergies | 4 | 4 | 1 |
| Laboratory Tests | 4 | 1 | 0 |
| Laboratory Information | 5 | 0 | 0 |
| Laboratory value(s)/result(s) | 5 | 1 | 1 |
| Vitals | 2 | 1 | 1 |
| Goal | 3 | 0 | 1 |
| Procedures | 2 | 1 | 1 |
| Care team member(s) | 3 | 0 | 1 |
| Reason for Referral | 1 | 1 | 1 |
| Medical Equipment | 2 | 1 | 1 |
| Mental Status | 4 | 1 | 1 |
| Functional Status | 4 | 1 | 1 |
| Health Concern | 3 | 1 | 1 |
| **TOTAL** | **82** | **27** | **30** |

No field descriptions, data types, or value set bindings exist for any element. The documentation provides element names, occasional XPATH paths, and code system OID references — nothing more.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers exactly what the C-CDA CCD standard defines: a clinical summary with standard sections for demographics, encounters, problems, medications, allergies, immunizations, vitals, labs, procedures, goals, care team, social history, mental/functional status, health concerns, referrals, and medical equipment.

This is the **standard USCDI clinical data set** — the same content that would satisfy the (b)(1) Transitions of Care criterion. The vendor does not document any C-CDA extensions, vendor-specific sections, or supplementary export files that go beyond the standard.

The 15 selectable UI sections map directly to standard C-CDA sections. The 24 sections in the data dictionary are standard C-CDA sections. There is no evidence of any vendor-specific data being exported.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient Demographics/Information` (6 fields: name, sex, DOB, race, ethnicity, language) | Basic demographics only — product stores addresses, contacts, insurance, emergency contacts per UI screenshots; these are absent |
| Encounters / visits | ✅ Covered | `Encounters` (5 fields), `Date and Location of visit` (2 fields), `Chief Complaint` (1 field) | CPT codes, diagnoses, dates, location — basic encounter data present |
| Problems / conditions | ✅ Covered | `Problems` (3 fields: problem, status, active date) | SNOMED/ICD-10 coded; adequate for problem list |
| Medications / prescriptions | ✅ Covered | `Medications` (5 fields: medication, directions, dates, status) | RxNorm/NDC coded; adequate for medication list |
| Allergies | ✅ Covered | `Medication Allergies` (4 fields: substance, reaction, severity, status) | RxNorm/SNOMED coded |
| Immunizations | ✅ Covered | `Immunizations` (9 fields) | CVX/CPT-4 coded; most detailed section |
| Vitals | ✅ Covered | `Vitals` (2 fields: observation, date/time) | LOINC coded; minimal but standard |
| Lab results | ✅ Covered | `Laboratory Tests` + `Laboratory Information` + `Laboratory value(s)/result(s)` (14 fields total across 3 sections) | LOINC coded; reasonable coverage |
| Procedures | ✅ Covered | `Procedures` (2 fields: procedure, date) | CPT-4/SNOMED/HCPCS coded |
| Clinical notes / documents | ❌ Not covered | PDF mentions "ability to download Images / Clinical notes on demand" as separate from CCD export; no structured representation in the export | **Significant gap** — product stores detailed progress notes linked to treatment goals. On-demand PDF download is mentioned but not documented as part of the (b)(10) export |
| Care plans / goals | ⚠️ Partial | `Treatment Plan` (2 fields: planned observation, date), `Goal` (3 fields) | C-CDA Treatment Plan section only covers planned observations — not the rich behavioral health treatment plans with trackable goals, interventions, and progress tracking that Cx360 stores |
| Orders / referrals | ⚠️ Partial | `Reason for Referral` (1 field) | Referral reason only; no order details |
| Insurance / coverage | ❌ Not covered | No insurance section in export; UI screenshot shows Insurance widget on patient home | **Gap** — product manages insurance/enrollment/authorization data for billing |
| Claims / billing | ❌ Not covered | No billing entities in export | **Significant gap** — product has full RCM module: claims, ledger, AR, payment tracking, authorization management |
| Payments | ❌ Not covered | No payment data in export | **Gap** — product processes payments including client portal payments |
| Consents / directives | ❌ Not covered | No consent documentation in export | Unknown whether product stores structured consent data |
| Patient communications / portal messages | ❌ Not covered | No messaging data in export | **Gap** — product has client portal with secure messaging |
| Specialty: Behavioral health assessments | ❌ Not covered | `Mental Status` section (4 fields) provides only a generic SNOMED-coded slot — not the structured multi-question evidence-based instruments (depression, PTSD, anxiety, substance use screenings) that are the product's core clinical value | **Critical gap** — this is the product's primary differentiator; comprehensive behavioral health assessments are the core data type and are not representable in C-CDA |
| Specialty: IDD data | ❌ Not covered | No IDD-specific sections in export | **Critical gap** — person-centered life plans, valued outcomes, DSP tasks, behavioral tracking are entirely absent |
| Specialty: SUD data | ❌ Not covered | No SUD-specific sections beyond what fits in generic Problems/Social History | **Significant gap** — addiction history, SUD-specific assessments, MAT tracking not represented |
| Specialty: Child/family services | ❌ Not covered | No child/family services sections | **Gap** — foster care records, family engagement data absent |

## 6. Documentation Quality

The documentation is a **12-page PDF** of which:
- 2 pages are cover/overview
- 4 pages are UI screenshots
- 6 pages are the C-CDA section data dictionary

**What it does well:**
- Clearly identifies the export format (C-CDA CCD) and standard referenced
- Screenshots show the actual export UI for both single and bulk modes
- Data dictionary lists code system OIDs for coded elements

**What it lacks:**
- **No field descriptions** — zero of 82 elements have descriptions beyond the element name
- **No data types** documented
- **No value sets** — code systems are referenced by OID but no bindings or allowed values
- **No sample data** — no example CCD files
- **No machine-readable schema** — PDF-only documentation
- **No documentation of the on-demand clinical notes download** mentioned in the overview
- **No guidance** on interpreting the export, handling edge cases, or importing the data
- **No documentation of data completeness** — no indication of what Cx360 data maps to which C-CDA section, or what data is excluded from the export

**Could a developer build an import from this?** A developer familiar with C-CDA could import the data using the public C-CDA IG — the vendor's documentation adds minimal value beyond confirming which sections are populated. The vendor documentation alone is insufficient.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is a standard C-CDA CCD clinical summary — the same format used for transitions of care under (b)(1). It is not a native database export and does not expose the vendor's data model. It covers standard clinical data classes but misses the vast majority of behavioral health-specific clinical data, billing records, and specialty data that constitute the product's core value.

### Key Findings

1. **The export is a C-CDA/CCD document repackaged as (b)(10) — a textbook example of conflating transitions of care with EHI export.** The 24 C-CDA sections and 82 data elements are identical to what would satisfy the (b)(1) criterion. No vendor-specific extensions or supplementary exports exist. (Source: `Electronic-Health-Information-Export-Doc.pdf`, pages 7–12; `ccd-sections.json`)

2. **The product's core clinical value — behavioral health assessments, IDD life plans, SUD protocols — is entirely absent from the export.** C-CDA has no sections for structured multi-question psychiatric instruments, person-centered IDD plans, or substance use treatment tracking. The Mental Status section's 4 generic SNOMED fields cannot represent the complex assessment data this product stores. (Source: `ccd-sections.json`, Mental Status section)

3. **All billing and revenue cycle data is missing.** Cx360 has a full RCM module (claims, ledger, AR, authorizations, payments) used to make decisions about patients — this is squarely within the HIPAA designated record set. Zero billing entities appear in the export. (Source: absence from `ccd-sections.json`; product capabilities from `product-research.md`)

4. **Clinical notes are explicitly excluded from the structured export.** The PDF overview mentions "ability to download Images / Clinical notes on demand" separately from the CCD, but this on-demand download is not documented as part of the (b)(10) process, has no data dictionary, and appears to be ad hoc rather than systematic. (Source: `Electronic-Health-Information-Export-Doc.txt`, lines 22–23)

5. **Documentation quality is thin.** 82 data elements with zero descriptions, zero type definitions, zero value set bindings, zero sample data. The documentation adds almost no value beyond what the public C-CDA specification provides. (Source: `analysis/summary-stats.txt`)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA CCD (XML) + PDF rendering
Model type:      Standard projection (C-CDA)
Entities:        24 (C-CDA sections)
Fields:          82
Descriptions:    0% (0 of 82 fields have descriptions)
Sample data:     No
Bulk export:     Yes
Domains covered: 8 of 18 applicable domains (with several only partially covered)
```

### Bottom Line

This export would give a patient a basic clinical summary — demographics, problem list, medications, labs, vitals — but would lose the vast majority of their behavioral health record. For a product whose entire value proposition is behavioral health, IDD, and SUD-specific clinical documentation, exporting only what fits in a standard C-CDA document is a fundamental mismatch. The single biggest gap is the complete absence of structured behavioral health assessments, treatment plans, and specialty clinical data — the very data that makes this EHR different from a general-purpose system.

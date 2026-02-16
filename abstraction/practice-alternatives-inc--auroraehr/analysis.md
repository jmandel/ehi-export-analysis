# EHI Export Analysis: Practice Alternatives, Inc.

**Product**: AuroraEHR v2.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 11128 (15.99.04.2186.Auro.02.01.1.221227)

## 1. Product Context

AuroraEHR is a small, regional ambulatory EHR developed by Practice Alternatives, Inc. (PAI), a New Jersey-based healthcare IT company serving over 500 physicians across 70+ specialties. AuroraEHR is the clinical EHR component of a larger suite that includes Rexpert, PAI's practice management and billing software. The two systems are described as "fully integrated."

**Relevant to export completeness:**
- **Clinical documentation**: Point-and-click templates, progress notes, H&Ps, nursing orders, CPOE for medications/labs/imaging
- **Billing integration**: AuroraEHR captures CPT and ICD-10 codes; billing claims and financial data flow to/reside in Rexpert. The EHR appears to maintain its own charges/payments data
- **Specialty/surgical workflows**: Pre-op/post-op assessments, surgical checklists, vascular access documentation (suggests ambulatory surgery center use)
- **Document management**: Supports PDF, JPG, Word, TIF, GIF, BMP images and documents
- **Patient portal**: Secure messaging, record access, visit summaries
- **Interoperability**: Transitions of care, immunization registry reporting, FHIR APIs
- **Mobile**: iPad app for vitals, photos, consent signing

AuroraEHR is certified under 2015 Edition (2022-12-27) with criteria covering CPOE (a)(1-3), demographics (a)(5), drug interaction checks (a)(4), transitions of care (b)(1-2), CQMs (c)(1-3), immunization registry (h)(1), and FHIR APIs (g)(7-10).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|----------|-------------|-----------------|
| `AuroraEHR_b10_EHI_Export_Documentation.pdf` (719 KB, 39 pages) | The sole and primary artifact. A dedicated (b)(10) EHI export documentation PDF with export instructions, UI screenshots, and field-level data dictionary for all export categories. Created 2023-11-30, last modified 2024-12-22. | **High** — this single document contains the complete export specification |

No additional artifacts were collected (no sample data, no JSON schemas, no HTML documentation). The registered CHPL URL was a direct link to this PDF.

## 3. Export Mechanics

- **Format**: ZIP archive containing CSV files (structured data) and PDF reports (medications, orders), plus original-format files (documents, scans, reports)
- **Mechanism**: Desktop application UI: AuroraEHR > Data Export. Privileged users select patients from a filtered browse list and choose which data categories to include.
- **Single-patient vs bulk**: Single-patient export supports up to 10 patients per run. Population-level export is available by request via email to gvti@practice-alt.com.
- **Access constraints**: Limited to users in Administrator, Billing Manager, Clinical Manager, or Front Office Manager user groups. Each export is individually audited per patient.
- **Output**: ZIP file placed on user's desktop, named `[userid]-dataExport-[practice code]-[datetime].zip`. Per-patient subfolders contain the exported files.
- **Fees**: Not mentioned in the documentation.

## 4. Export Content: What's In It

The export documentation describes **31 distinct entities** (CSV files and PDF reports) across **14 vendor-defined categories**, containing a total of **493 documented fields**. Every field has a description. 33 fields include enumerated possible values.

Data types are implicit from descriptions (e.g., "Formatted MM/dd/yyyy", "Numeric value", "Yes or no") rather than explicitly typed. Relationships between entities are established through `Account#` (patient ID) and `Accession#` (appointment ID) foreign keys present consistently across most CSVs.

### Vendor's own content organization

The vendor organizes the export into 14 selectable categories. Below is a summary with field counts verified against the PDF (full inventory in `analysis/full-entity-inventory.json`):

| Entity | File(s) | Fields | Format | Category (vendor's) |
|--------|---------|--------|--------|---------------------|
| Account Data | AccountData.pdf | 12 | PDF | Account Data |
| Charges | Charges.csv | 30 | CSV | Charges/Payments |
| Payments | Payments.csv | 22 | CSV | Charges/Payments |
| ChargeTransactions | ChargeTransactions.csv | 12 | CSV | Charges/Payments |
| AccountNotes | AccountNotes.csv | 5 | CSV | Notes/Instructions |
| ClinicalInstructions | ClinicalInstructions.csv | 5 | CSV | Notes/Instructions |
| ClinicalProgressNotes | ClinicalProgressNotes.csv | 12 | CSV | Notes/Instructions |
| Appointments | Appointments.csv | 9 | CSV | Appointments |
| Documents | Documents.csv + Documents/ folder | 12 | CSV | Documents/Scans/Reports |
| Scans | Scans.csv + Scans/ folder | 6 | CSV | Documents/Scans/Reports |
| Reports | Reports.csv + Reports/ folder | 14 | CSV | Documents/Scans/Reports |
| ClinicalAlerts | ClinicalAlerts.csv | 7 | CSV | Clinical Alerts |
| Allergies | Allergies.csv | 11 | CSV | Allergies |
| Immunizations | Immunizations.csv | 17 | CSV | Immunizations |
| Medications | Medications.pdf | 6 | PDF | Medications |
| Problems | Problems.csv | 11 | CSV | Problems/Diagnoses |
| ReviewOfSystems | ReviewOfSystems.csv | 5 | CSV | Review of Systems |
| SocialHistory | SocialHistory.csv | 13 | CSV | Social/Family/Surgical History |
| FamilyHistory | FamilyHistory.csv | 10 | CSV | Social/Family/Surgical History |
| SurgicalHistory | SurgicalHistory.csv | 9 | CSV | Social/Family/Surgical History |
| Orders | ImagingOrders.pdf, LabOrders.pdf, PathologyOrders.pdf, TherapyOrders.pdf | 5 | PDF | Orders: Tests and Results |
| VitalSigns | VitalSigns.csv | 25 | CSV | Vital Signs |
| ImplantedDevices | ImplantedDevices.csv | 22 | CSV | Additional Clinical Data |
| PatientEducation | PatientEducation.csv | 9 | CSV | Additional Clinical Data |
| PostAppointment | PostAppointment.csv | 17 | CSV | Additional Clinical Data |
| PostOp | PostOp.csv | 46 | CSV | Additional Clinical Data |
| PreOp | PreOp.csv | 28 | CSV | Additional Clinical Data |
| PreopProcedureNotes | PreopProcedureNotes.csv | 36 | CSV | Additional Clinical Data |
| ProviderOrders | ProviderOrders.csv | 47 | CSV | Additional Clinical Data |
| SurgicalChecklist | SurgicalChecklist.csv | 18 | CSV | Additional Clinical Data |
| SutureInfo | SutureInfo.csv | 12 | CSV | Additional Clinical Data |

**Category totals:**

| Category | Entities | Fields |
|----------|----------|--------|
| Account Data | 1 | 12 |
| Charges/Payments | 3 | 64 |
| Notes/Instructions | 3 | 22 |
| Appointments | 1 | 9 |
| Documents/Scans/Reports | 3 | 32 |
| Clinical Alerts | 1 | 7 |
| Allergies | 1 | 11 |
| Immunizations | 1 | 17 |
| Medications | 1 | 6 |
| Problems/Diagnoses | 1 | 11 |
| Review of Systems | 1 | 5 |
| Social/Family/Surgical History | 3 | 32 |
| Orders: Tests and Results | 1 | 5 |
| Vital Signs | 1 | 25 |
| Additional Clinical Data | 9 | 235 |
| **Total** | **31** | **493** |

**Notable observations:**
- The "Additional Clinical Data" category is by far the largest (235 fields, 9 entities), driven by detailed pre-op/post-op/surgical workflow data — suggesting ambulatory surgery center clientele
- Charges/Payments is the second-richest category (64 fields across 3 CSVs), covering charges with CPT/ICD-10 codes, payments with payor/remit detail, and a charge transaction audit trail
- Medications and Orders are exported as PDF reports rather than structured CSV, reducing machine-readability. Medications has only 6 searchable fields; Orders has only 5.
- The Orders entity shares a single field spec across 4 PDF files (lab, imaging, pathology, therapy)

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers three broad functional areas:

**1. Clinical core (well-covered):** Demographics via Account Data (PDF report with name, DOB, SSN, address, contacts, ethnicity, language, employment). Allergies with SNOMED/RXNORM coding. Problems with dual SNOMED + ICD-10 coding. Immunizations with comprehensive vaccine detail (17 fields including lot, manufacturer, route, site, refusal reasons). Vital signs with 25 fields including O2 sat, BMI, pain scale. Social, family, and surgical history (32 fields across 3 CSVs, with SNOMED-coded smoking status). Review of systems text. Clinical progress notes with amendment tracking and dual-signature support.

**2. Billing and financial (strong):** This is an unusual strength for a small vendor. Three CSVs cover charges (30 fields: CPT codes, 4 diagnosis slots, amounts, balances, modifiers, claim numbers, RVUs), payments (22 fields: deposit dates, financial class, payor detail, remit types), and charge transactions (12 fields: billing audit trail). Account Data PDF also includes balances and statement information. Insurance payors are exported as part of Account Data.

**3. Specialty/surgical workflows (deep):** The "Additional Clinical Data" category contains remarkably detailed pre-op and post-op data. PostOp.csv (46 fields) includes Aldrete-style scoring (activity, respiration, consciousness, O2 saturation at arrival and discharge), vascular assessments (12 pulse/grip/color-temp measurements), fluid intake tracking, transport methods, and suture counts. PreOp.csv (28 fields) captures baseline versions of the same assessments. PreopProcedureNotes.csv (36 fields) documents vascular access, catheter placement, anxiety reduction protocols, declot procedures, and antibiotic administration. ProviderOrders.csv (47 fields) covers puncture sites, catheter locations, heparin dosing, medication administration, discharge disposition, SNOMED-coded discharge diagnoses, functional/cognitive status, and referrals.

**4. Documents and external records (good):** The export includes actual files (PDFs, images) in their original format, not just metadata. Three CSVs provide indexes: Documents.csv for internally generated documents (medical reports, referral documents, patient instructions), Scans.csv for imported images/files, and Reports.csv for external clinical reports and summaries of care. Each includes file path references to link metadata to actual files.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|--------|----------|-----------------|--------------|
| Demographics | ✅ Covered | `AccountData.pdf` — name, DOB, SSN, address, contacts, ethnicity, language, employment | Thorough, though as PDF rather than structured CSV |
| Encounters / visits | ✅ Covered | `Appointments.csv` (9 fields: date, time, duration, reason, provider, location, kept/fail status) | Comprehensive for ambulatory visits |
| Problems / conditions / diagnoses | ✅ Covered | `Problems.csv` (11 fields) with dual SNOMED + ICD-10 coding, onset/resolved dates, status | Well-documented with coded values |
| Medications / prescriptions | ⚠️ Partial | `Medications.pdf` — 6 searchable fields (name, dose, duration, start/stop, refills, last fill). PDF format limits machine readability. No pharmacy or e-prescribing transmission data | Covers medication list but not prescribing workflow or pharmacy detail |
| Allergies | ✅ Covered | `Allergies.csv` (11 fields) with SNOMED reaction codes, RXNORM codes, severity levels | Thorough |
| Immunizations | ✅ Covered | `Immunizations.csv` (17 fields) including vaccine codes, lot numbers, manufacturer, 15 status values, refusal reasons | Comprehensive |
| Vitals | ✅ Covered | `VitalSigns.csv` (25 fields) including BP with site/side, O2 sat, BMI, pain scale, respiratory rate, temperature, blood sugar | Very thorough |
| Lab results | ⚠️ Partial | `LabOrders.pdf` exports order# and test names with LOINC codes, but **no discrete result values, reference ranges, or interpretations**. External lab reports may be captured as files in the Reports folder | Orders documented; result values appear absent from structured export. This is a notable gap if the system stores discrete results |
| Imaging / diagnostic reports | ⚠️ Partial | `ImagingOrders.pdf` exports orders with CPT codes. Actual imaging reports may be in Documents/Reports folders as files | Orders present; results as documents only |
| Procedures | ✅ Covered | `SurgicalHistory.csv` (procedure codes, code system, description). Extensive pre-op/post-op data. `SurgicalChecklist.csv` | Strong for surgical procedures |
| Clinical notes / documents | ✅ Covered | `ClinicalProgressNotes.csv` (12 fields, with amendment tracking), `AccountNotes.csv`, `ClinicalInstructions.csv`, `ReviewOfSystems.csv`. Plus actual document files exported | Thorough with multiple note types |
| Care plans / goals | ❌ Not covered | No care plan entity in the export | Product research mentions "care plans and patient education materials" as a feature. Patient education is exported but care plans are not. Minor gap |
| Orders / referrals | ✅ Covered | 4 order PDFs (lab, imaging, pathology, therapy) with LOINC/CPT codes. `ProviderOrders.csv` includes referral fields (Refer To, Refer To Date, Referral Reason) | Order metadata present; referrals documented |
| Insurance / coverage | ✅ Covered | `AccountData.pdf` includes "All Account Payors" section. `Charges.csv` includes FIRST PAYOR. `Payments.csv` includes PAYOR, FIN CLASS, REPT GRP | Covered across multiple entities |
| Claims / billing | ✅ Covered | `Charges.csv` (30 fields: CPT, ICD-10 diagnoses, amounts, claim numbers, modifiers, RVUs), `Payments.csv` (22 fields), `ChargeTransactions.csv` (12 fields) | **Unusually strong for a small vendor.** Three dedicated CSVs with detailed billing data |
| Payments | ✅ Covered | `Payments.csv` — deposit dates, amounts, interest, payor, remit type, financial class | Thorough |
| Consents / directives | ⚠️ Partial | `PreopProcedureNotes.csv` includes "Verbal Consent Obtained From." No general consent document entity | Surgical consent captured; general advance directives not explicitly addressed |
| Patient communications / portal messages | ❌ Not covered | No portal messaging or patient communication entity in the export | Product has a patient portal with secure messaging; this data is not in the export |
| Specialty-specific (ambulatory surgery) | ✅ Covered | `PostOp.csv` (46 fields), `PreOp.csv` (28 fields), `PreopProcedureNotes.csv` (36 fields), `ProviderOrders.csv` (47 fields), `SurgicalChecklist.csv` (18 fields), `SutureInfo.csv` (12 fields) — totaling 187 fields | **Exceptionally detailed.** Aldrete scoring, vascular assessments, heparin dosing, catheter placement, declot procedures, antibiotic protocols |

## 6. Documentation Quality

**Strengths:**
- **Completeness**: Every CSV column and PDF searchable field is documented with a description (493/493 = 100%)
- **Value sets**: 33 fields include complete enumerated value lists (e.g., 15 immunization statuses, 9 smoking statuses with SNOMED codes, 4 allergy severity levels, 5 transport methods)
- **Format specifications**: Date/time formats explicitly stated (MM/dd/yyyy, hh:mm:ss am)
- **Relationship keys**: Account# and Accession# serve as consistent foreign keys across all CSVs, clearly documented
- **Operational guidance**: Clear instructions on access roles, patient selection, 10-patient limit, population export process, and audit logging
- **Screenshots**: Includes UI screenshots of the export screen and export completion dialog

**Weaknesses:**
- **No sample data**: No example export files are provided. A developer would have to perform an actual export to see real data
- **No machine-readable schema**: Documentation is PDF-only — no JSON schema, XSD, CSV header specs, or DDL
- **Implicit data types**: Fields are described in prose ("Numeric value", "Yes or no", "Formatted MM/dd/yyyy") but there's no explicit type column (string, integer, date, boolean)
- **No cardinality documentation**: It's implied but never stated that a patient can have multiple allergies, immunizations, etc. (one row per record)
- **PDF-based medications and orders**: These categories export as PDF reports rather than structured CSV, reducing machine parsability
- **Placeholder noted**: Page 4 has "[add screenshot of windows explorer showing directories and files of an export]" — the screenshot does appear on page 5, but the placeholder text remains

**Could a developer build an import?** Yes, with reasonable effort. The field descriptions and value sets are detailed enough to map to a target system. The consistent Account#/Accession# relationship model is straightforward. The main challenge would be the PDF-format entities (AccountData, Medications, Orders) which would require PDF parsing rather than simple CSV reading.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

AuroraEHR's (b)(10) export is a genuine, purpose-built native data model export — not a repackaged FHIR API or C-CDA. It exports the vendor's own data structures in CSV/PDF format, covers clinical, billing, and specialty surgical domains, and includes 31 entities with 493 documented fields. The coverage is broad and the documentation quality is above average for a vendor of this size.

### Key Findings

1. **Genuine native export with strong billing coverage.** The export includes 3 dedicated billing CSVs (Charges, Payments, ChargeTransactions) totaling 64 fields — covering CPT codes, diagnosis codes, amounts, balances, claim numbers, modifiers, RVUs, payor details, and billing audit trails. Many larger vendors omit billing entirely from their (b)(10) exports.

2. **Exceptionally detailed surgical/procedural data.** The "Additional Clinical Data" category contains 235 fields across 9 entities, capturing Aldrete-style post-anesthesia scoring, vascular assessments, catheter placement, heparin dosing protocols, antibiotic administration, surgical checklists, and suture tracking. This reflects real ambulatory surgery center workflows.

3. **Lab results gap.** Orders for labs, imaging, pathology, and therapy are exported (with LOINC/CPT codes), but **discrete result values appear absent** from the structured export. If AuroraEHR stores discrete lab results, this is a meaningful gap. External lab reports may be captured as document files in the Reports folder, but without structured result data.

4. **100% field documentation with value sets.** All 493 fields have descriptions, and 33 fields include complete enumerated value lists. Date formats are explicitly specified. This is solid documentation, though it lacks machine-readable schemas and sample data.

5. **Some data exported as PDF rather than structured format.** Medications, Account Data, and Orders are exported as PDF reports rather than structured CSV. This reduces machine readability — a developer would need to parse PDFs to extract structured medication or order data.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV + PDF (in ZIP archive), with original-format documents/images
Model type:      Native database
Entities:        31
Fields:          493
Descriptions:    100%
Sample data:     No
Bulk export:     Yes (by request via email)
Domains covered: 14 of 17 applicable domains (with 3 partial, 2 not covered)
```

### Bottom Line

AuroraEHR delivers a solid (b)(10) export that covers the vast majority of what an ambulatory EHR and ambulatory surgery center workflow would store. The billing data coverage is a particular standout for a small vendor, and the surgical workflow documentation is remarkably detailed. The main gaps are the absence of discrete lab result values in the structured export, patient portal communications, and the use of PDF format for medications and orders rather than structured CSV. A patient or provider would get a comprehensive, usable copy of their clinical and financial data from this export.

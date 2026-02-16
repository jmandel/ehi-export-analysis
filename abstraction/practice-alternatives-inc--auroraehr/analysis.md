# EHI Export Analysis: Practice Alternatives, Inc.

**Product**: AuroraEHR
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.99.04.2186.Auro.02.01.1.221227

## 1. Product Context

AuroraEHR is a small ambulatory EHR built by Practice Alternatives, Inc. (PAI), a regional healthcare IT company based in New Jersey serving ~500 physicians across 70+ specialties. AuroraEHR is the clinical EHR component paired with Rexpert, PAI's practice management and billing system. Together they form an integrated suite covering clinical documentation, CPOE (medications, labs, imaging), vital signs, allergy tracking, immunizations, document management, patient portal, and clinical quality measures.

Key data domains relevant to export completeness:
- **Clinical**: Notes (H&P, progress notes, nursing orders), problems, allergies, medications, immunizations, vitals, review of systems, implanted devices, clinical alerts
- **Orders**: Lab, imaging, pathology, therapy orders with results
- **Documents**: Scanned documents, external reports, transcribed documents
- **Billing/Financial**: Charges, payments, claims — handled by Rexpert but integrated with AuroraEHR. The EHR captures CPT/ICD-10 codes; billing claims and financial data reside in Rexpert
- **Surgical/Procedural**: Pre-op assessments, post-op assessments, surgical checklists, suture tracking, provider orders — indicating ambulatory surgery center (ASC) workflows
- **Patient History**: Social history, family history, surgical history
- **Demographics**: Full patient demographics, contacts, insurance/payors, employers

The product notably includes deep ASC/vascular access center workflows (declot procedures, catheter tracking, heparin dosing, Aldrete-style post-anesthesia scoring) suggesting a significant customer base in procedural specialties.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/AuroraEHR_b10_EHI_Export_Documentation.pdf` (39 pages, 718 KB) | Complete (b)(10) documentation: export instructions, UI screenshots, and field-level data dictionary for all export categories. Created 2023-11-30. | **Most informative** — sole artifact; contains everything needed |

Only one artifact was collected, but it is a thorough, purpose-built document covering the entire EHI export feature with field-level detail and value sets.

## 3. Export Mechanics

- **Format**: Mixed CSV and PDF. Most categories export as CSV spreadsheets; medications and orders (lab, imaging, pathology, therapy) export as searchable PDF reports. Documents, scans, and external reports export as actual files (PDF, JPG, etc.) with CSV metadata indexes.
- **Mechanism**: UI-based export through `AuroraEHR > Data Export` screen. Users select patients by account number or by provider/location/date range filter, then choose categories to export.
- **Single-patient vs bulk**: Supports up to 10 patients at once via the UI. For full patient population exports, users contact PAI at gvti@practice-alt.com.
- **Output**: A ZIP file placed on the user's desktop, organized into per-patient subfolders with named CSV/PDF files and document subfolders.
- **Access**: Available to Administrator, Billing Manager, Clinical Manager, and Front Office Manager user groups.
- **Audit**: Each export is audited per patient, recording who requested it, when, and what categories were selected.
- **Fees**: Not mentioned in the export documentation.

## 4. Export Content: What's In It

The export documentation defines **34 entities** (CSV spreadsheets and PDF reports) containing **508 documented fields**. Every field has a description (100% coverage). 33 fields include enumerated value sets with specific possible values.

The data dictionary is organized into export categories selectable by the user. Each category produces one or more named files per patient.

### Vendor's own content organization

| Entity/Table | File | Format | Fields | Category |
|---|---|---|---|---|
| Account Data | AccountData.pdf | PDF | 12 | Demographics / Account |
| Charges | Charges.csv | CSV | 30 | Billing |
| Payments | Payments.csv | CSV | 22 | Billing |
| Charge Transactions | ChargeTransactions.csv | CSV | 12 | Billing |
| Account Notes | AccountNotes.csv | CSV | 5 | Notes / Instructions |
| Clinical Instructions | ClinicalInstructions.csv | CSV | 5 | Notes / Instructions |
| Clinical Progress Notes | ClinicalProgressNotes.csv | CSV | 12 | Notes / Instructions |
| Appointments | Appointments.csv | CSV | 9 | Encounters |
| Documents | Documents.csv | CSV | 12 | Documents / Scans / Reports |
| Scans | Scans.csv | CSV | 6 | Documents / Scans / Reports |
| Reports | Reports.csv | CSV | 14 | Documents / Scans / Reports |
| Clinical Alerts | ClinicalAlerts.csv | CSV | 7 | Clinical |
| Allergies | Allergies.csv | CSV | 11 | Clinical |
| Immunizations | Immunizations.csv | CSV | 17 | Clinical |
| Medications | Medications.pdf | PDF | 6 | Clinical |
| Problems/Diagnoses | Problems.csv | CSV | 11 | Clinical |
| Review of Systems | ReviewOfSystems.csv | CSV | 5 | Clinical |
| Vital Signs | VitalSigns.csv | CSV | 25 | Clinical |
| Implanted Devices | ImplantedDevices.csv | CSV | 22 | Additional Clinical Data |
| Patient Education | PatientEducation.csv | CSV | 9 | Additional Clinical Data |
| Post Appointment | PostAppointment.csv | CSV | 16 | Additional Clinical Data |
| Social History | SocialHistory.csv | CSV | 13 | History |
| Family History | FamilyHistory.csv | CSV | 10 | History |
| Surgical History | SurgicalHistory.csv | CSV | 9 | History |
| Imaging Orders | ImagingOrders.pdf | PDF | 5 | Orders |
| Lab Orders | LabOrders.pdf | PDF | 5 | Orders |
| Pathology Orders | PathologyOrders.pdf | PDF | 5 | Orders |
| Therapy Orders | TherapyOrders.pdf | PDF | 5 | Orders |
| Post Op | PostOp.csv | CSV | 43 | Surgical / Procedural |
| Pre Op | PreOp.csv | CSV | 28 | Surgical / Procedural |
| Preop Procedure Notes | PreopProcedureNotes.csv | CSV | 35 | Surgical / Procedural |
| Provider Orders | ProviderOrders.csv | CSV | 45 | Surgical / Procedural |
| Surgical Checklist | SurgicalChecklist.csv | CSV | 18 | Surgical / Procedural |
| Suture Info | SutureInfo.csv | CSV | 12 | Surgical / Procedural |

**Category summary:**

| Category | Entities | Fields |
|---|---|---|
| Surgical / Procedural | 6 | 187 |
| Clinical | 7 | 82 |
| Billing | 3 | 64 |
| Additional Clinical Data | 3 | 48 |
| Documents / Scans / Reports | 3 | 32 |
| History | 3 | 32 |
| Notes / Instructions | 3 | 22 |
| Orders | 4 | 20 |
| Demographics / Account | 1 | 12 |
| Encounters | 1 | 9 |

The Surgical/Procedural category is by far the largest (187 fields, 37% of total), reflecting the product's deep ASC/procedural workflows including Aldrete scoring, vascular access assessments, declot procedures, and heparin protocols.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers a genuinely broad set of domains, organized into the vendor's own export categories:

**Billing (3 entities, 64 fields)**: The deepest billing coverage seen in a small vendor EHI export. Charges.csv includes 30 fields with CPT codes, ICD-10 diagnoses (4 slots), charge amounts, RVUs, claim numbers, balances, modifiers, and authorization numbers. Payments.csv captures 22 fields including remittance types, financial classes, payor groups, and interest. ChargeTransactions.csv adds 12 fields of billing audit trail. This is genuine billing data, not just a summary.

**Clinical (7 entities, 82 fields)**: Solid coverage of core clinical data. Allergies include SNOMED reactions and RXNORM codes. Problems use both SNOMED and ICD-10 coding. Vital Signs has 25 fields including specialty-specific items (shoe size for podiatry). Immunizations are particularly thorough with 17 fields covering lot numbers, manufacturers, routes, sites, and refusal reasons with detailed value sets.

**Surgical/Procedural (6 entities, 187 fields)**: Exceptionally deep specialty data for ambulatory surgery workflows. PostOp.csv alone has 43 fields covering Aldrete-style post-anesthesia scoring, bilateral vascular assessments, fluid intake tracking, and suture management. PreopProcedureNotes.csv covers vascular access (fistula/graft), catheter placement, declot procedures, and antibiotic administration. ProviderOrders.csv documents heparin dosing protocols, discharge dispositions, functional/cognitive status, and referrals. This is clearly custom clinical workflow data well beyond USCDI scope.

**Documents/Scans/Reports (3 entities, 32 fields)**: Exports actual document files (PDFs, images) with metadata indexes. Covers internally-generated documents, imported scans, and external reports with review tracking.

**History (3 entities, 32 fields)**: Social, family, and surgical history with coded conditions. Social history includes substance use, smoking status with SNOMED codes, abuse screening, and pregnancy status.

**Notes (3 entities, 22 fields)**: Account notes (by type: billing, medical, surgery), clinical instructions, and progress notes with amendment tracking and dual signature workflows.

**Demographics/Account (1 entity, 12 fields)**: The AccountData.pdf report bundles demographics, payors, employers, contacts, and billing information into a single PDF report. While comprehensive in scope, the PDF format means the granular field structure is less visible than the CSV entities.

**Orders (4 entities, 20 fields)**: Lab, imaging, pathology, and therapy orders exported as searchable PDFs. Each has 5 documented searchable fields. The PDF format limits granularity; order results appear to be embedded in the PDF alongside orders but aren't separately structured as CSV.

**Thinnest areas**: Orders (PDF format limits field-level detail), medications (6 fields in PDF, no prescribing details like pharmacy, SIG, or route), and encounters/appointments (9 fields, basic scheduling data).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `AccountData.pdf` — name, DOB, SSN, address, contacts, ethnicity, language, employment | Thorough; bundled into PDF report |
| Encounters / visits | ✅ Covered | `Appointments.csv` (9 fields) — date, time, duration, reason, provider, location, status | Basic but functional |
| Problems / conditions | ✅ Covered | `Problems.csv` (11 fields) — SNOMED + ICD-10 coded, onset/resolved dates, status tracking | Solid with dual coding |
| Medications / prescriptions | ⚠️ Partial | `Medications.pdf` (6 fields) — name, dose, duration, dates, refills | Missing SIG, route, pharmacy, prescriber, frequency; PDF format |
| Allergies | ✅ Covered | `Allergies.csv` (11 fields) — SNOMED reactions, RXNORM codes, severity, onset | Well documented with coded values |
| Immunizations | ✅ Covered | `Immunizations.csv` (17 fields) — vaccine, lot, manufacturer, route, site, refusal tracking | Very thorough |
| Vitals | ✅ Covered | `VitalSigns.csv` (25 fields) — BP, HR, height, weight, BMI, SpO2, temp, respiratory rate, pain, blood sugar | Comprehensive including supplemental O2 and specialty fields |
| Lab results | ⚠️ Partial | `LabOrders.pdf` — orders with LOINC codes, but results in PDF format | Results not separately structured; PDF limits usability |
| Imaging / diagnostic reports | ⚠️ Partial | `ImagingOrders.pdf` — orders with CPT codes in PDF format | Same limitation as labs |
| Procedures | ✅ Covered | `SurgicalHistory.csv`, `PostOp.csv`, `PreOp.csv`, `SurgicalChecklist.csv` — coded procedures, extensive perioperative data | Exceptionally deep for procedural specialties |
| Clinical notes / documents | ✅ Covered | `ClinicalProgressNotes.csv` (12 fields), `Documents.csv` + actual files, `Reports.csv` + actual files, `Scans.csv` + actual files | Strong — includes note text, documents, scans, external reports |
| Care plans / goals | ❌ Not covered | No care plan entities in export | Product lists "care plans" as a feature; potential gap |
| Orders / referrals | ✅ Covered | `ProviderOrders.csv` (referral fields), 4 order PDFs (lab/imaging/pathology/therapy) | Referrals well-documented; orders limited by PDF format |
| Insurance / coverage | ✅ Covered | `AccountData.pdf` — "All Account Payors" section | Present but in PDF; no separate structured payor CSV |
| Claims / billing | ✅ Covered | `Charges.csv` (30 fields), `Payments.csv` (22 fields), `ChargeTransactions.csv` (12 fields) | **Strong** — 64 fields across 3 CSVs with claim-level detail |
| Payments | ✅ Covered | `Payments.csv` (22 fields) — deposit dates, amounts, remittance types, payor info | Thorough |
| Consents / directives | ⚠️ Partial | `PreopProcedureNotes.csv` — "Verbal Consent Obtained From" field | Only surgical consent; no general advance directives |
| Patient communications | ❌ Not covered | No portal messages or communication entities | Product has patient portal; communications likely exist |
| Specialty-specific (ASC/vascular) | ✅ Covered | `PostOp.csv` (43 fields), `PreOp.csv` (28 fields), `PreopProcedureNotes.csv` (35 fields), `ProviderOrders.csv` (45 fields), `SurgicalChecklist.csv` (18 fields), `SutureInfo.csv` (12 fields) | **Exceptionally deep** — 181 fields of perioperative/vascular access data |

**Gap summary**: 14 of 17 applicable domains are covered. Missing: care plans/goals and patient portal communications. Partial: medications (thin fields, PDF format), lab/imaging results (PDF format limits structured access), consents (surgical only).

## 6. Documentation Quality

**Strengths:**
- Every field (508/508, 100%) has a text description explaining what it contains
- 33 fields include explicit enumerated value sets with all possible values listed
- Date and time formats are consistently specified (e.g., "Formatted MM/dd/yyyy", "Formatted hh:mm:ss am")
- File naming conventions are documented (e.g., `[user id]-dataExport-[practice code]-[date].zip`)
- Export folder structure is described with examples
- Each entity includes clear explanation of what the CSV/PDF represents and how records relate to appointments via Accession#

**Weaknesses:**
- No sample data files included
- No machine-readable schema (no JSON schema, no XSD, no CSV header specification)
- No entity-relationship documentation — relationships between tables rely on shared Account#/Accession# fields but aren't formally documented
- PDF-format exports (Medications, Orders) lose structured field detail
- Data types (string, numeric, date) are implied by descriptions but not formally specified
- The AccountData.pdf entity has only high-level section descriptions, not field-level detail, because the underlying PDF report bundles many fields into prose sections

**Overall**: A developer could build an import from this documentation with moderate effort. The CSV entities are well-specified enough to parse directly. The PDF entities would require more work (OCR/text parsing). The lack of sample data is a gap but the descriptions are detailed enough to understand field semantics.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export goes meaningfully beyond USCDI/clinical exchange. The strongest signal is the billing coverage: 64 fields across 3 CSVs covering charges, payments, and billing transactions at claim-level granularity — this is data that would never appear in a C-CDA or (g)(10) FHIR export. The 187 fields of surgical/procedural data (Aldrete scoring, vascular assessments, declot procedures, heparin protocols) represent deep specialty workflow data that is entirely outside the scope of standard clinical exchange. The product is a small ambulatory EHR, so the applicable domain set is relatively bounded. Within that scope, the export covers demographics, clinical data, billing, notes, documents/scans, orders, history, and specialty surgical workflows. The only notable gaps are care plans and patient portal messages.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged clinical exchange. Key evidence:
1. The document explicitly names itself "§170.315(b)(10) Electronic Health Information export – Documentation"
2. The export uses the vendor's native data model (CSV/PDF from internal tables), not FHIR or C-CDA
3. The billing data (Charges.csv, Payments.csv, ChargeTransactions.csv) would never appear in a clinical exchange export
4. The deep surgical/procedural data (PostOp.csv with 43 fields including heparin dosing and vascular assessments) is entirely product-specific
5. The export UI has a dedicated screen with category selection, patient filtering, and audit logging
6. There is no mention of C-CDA, FHIR, USCDI, or US Core anywhere in the documentation

### Key Findings

1. **Genuinely purpose-built with deep billing coverage.** This small vendor built a dedicated EHI export that includes 64 fields of billing data (charges, payments, billing transactions) — a strong signal of authentic (b)(10) engagement rather than clinical exchange repackaging.

2. **Unusually deep specialty/surgical data.** 187 fields (37% of total) cover ASC/vascular access workflows including Aldrete scoring, vascular assessments, catheter/fistula tracking, declot procedures, and medication administration. This is domain-specific clinical data well beyond USCDI.

3. **100% field-level documentation.** All 508 fields have descriptions, and 33 include enumerated value sets. For a vendor of this size (~20 employees), this is above-average documentation quality.

4. **Medications and lab/imaging results are weak spots.** Medications have only 6 fields in PDF format (missing SIG, route, pharmacy). Orders export as PDFs with only 5 searchable fields each — results are embedded in PDFs rather than structured as CSVs, limiting usability.

5. **No sample data or machine-readable schema.** The documentation is prose-only (a 39-page PDF). No JSON schemas, CSV samples, or relationship diagrams are provided.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV + PDF (mixed)
Entities:        34
Fields:          508
Descriptions:    100%
Sample data:     No
Bulk export:     Yes (via vendor request to gvti@practice-alt.com)
Domains covered: 14 of 17 applicable domains
```

### Bottom Line

AuroraEHR's (b)(10) export is a genuinely purpose-built EHI export that goes well beyond clinical exchange. With 34 entities, 508 fields, and deep coverage of billing (64 fields) and specialty surgical/procedural workflows (187 fields), it represents one of the stronger small-vendor efforts. The main gaps are medications (thin documentation), lab/imaging results (PDF format limits structured access), and missing patient portal communications and care plans.

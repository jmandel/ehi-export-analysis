# EHI Export Analysis: Modernizing Medicine Inc.

**Product**: EMA (Electronic Medical Assistant) v7
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.2002.EMA6.70.18.1.221129 (CHPL #11032)

## 1. Product Context

ModMed EMA is a cloud-based, specialty-specific EHR and practice management platform serving 11 medical specialties (dermatology, ophthalmology, gastroenterology, orthopedics, OB/GYN, ENT, urology, pain management, plastic surgery, podiatry, allergy/immunology). It is an all-in-one system encompassing:

- **Clinical EHR**: Specialty-specific templates, Virtual Exam Room, anatomical atlas, adaptive learning, AI ambient documentation (ModMed Scribe)
- **Practice Management**: Scheduling, billing, claims, remittance, denial management
- **Revenue Cycle Management**: Full billing automation from charge capture through payment posting
- **E-Prescribing**: Integrated with Surescripts
- **Lab Integration**: Electronic lab orders and results
- **Ophthalmology-specific**: DICOM image management, pretesting modules (visual acuity, keratometry, IOP, visual fields, etc.)
- **Patient Engagement**: Patient portal (APPatient), secure messaging, kiosk, telehealth
- **Inventory Management**: Supply tracking, product sales
- **Pathology**: Dermatopathology tracking
- **Cancer Registry**: Oncology staging and tracking
- **OB/GYN**: Prenatal, pregnancy, delivery records

With 40,000+ providers and a $5.3B valuation (Clearlake Capital acquisition, March 2025), this is a substantial mid-market specialty EHR vendor. The product stores extensive clinical, financial, and operational data — setting a high bar for what a complete EHI export should cover.

## 2. Artifacts Reviewed

| Artifact | Size/Scope | Informativeness |
|---|---|---|
| `ModMed-EMA-EHI-Export-Data-Dictionary.pdf` | 96 pages, 420 table entries, 8 appendices with value sets | **High** — comprehensive table inventory with descriptions, relationships, longitudinal tracking metadata, and product/vertical assignments |
| `ModMed-EMA-Detailed-Data-Dictionary.pdf` | 210 pages, 5,250 field entries across 240 tables | **High** — complete field-level data dictionary with column names, descriptions, data types, nullability, field lengths, and coded value references |
| `onc-certification-page.png` | Full-page screenshot of modmed.com/onc-certification/ | **Moderate** — confirms EHI Export Documentation link structure; shows "Data Dictionary for ModMed EMA EHI Export" as the sole EHI documentation artifact |
| `overview-dd-xml.xml` | 666 KB XML from pdftohtml | Intermediate parsing artifact |
| `detailed-dd-xml.xml` | 3.5 MB XML from pdftohtml | Intermediate parsing artifact |

The two PDFs constitute 306 pages of documentation. The overview PDF is dated January 8, 2026 (per PDF metadata: created from Google Docs). The detailed PDF was originally a Google Sheets spreadsheet exported as .xlsx then PDF. Both are recently updated.

## 3. Export Mechanics

- **Format**: Tabular/relational — the export mirrors the vendor's internal database schema. SQL data types (string, int, datetime, boolean, float, double) with explicit field lengths. The documentation does not explicitly state the file format (CSV, TSV, JSON, or database dump), though the relational structure with typed columns suggests per-table flat files.
- **Mechanism**: The title is "EHI Export Data Dictionary for **Single Patient** Export" — this is a single-patient export. The documentation references a "training manual" for usage instructions but does not include export initiation procedures.
- **Single-patient vs bulk**: Single-patient only (per title).
- **Access constraints**: The documentation includes a confidentiality notice: "This Data Dictionary is the sole property of Modernizing Medicine, Inc." Users must agree not to share contents without written authorization.
- **Timestamps**: All date/timestamp fields use UTC unless the field has an "_ld" suffix (local date/time).
- **PM data**: Practice Management tables are included but will be empty for practices not using PM.

## 4. Export Content: What's In It

### Data Dictionary Scope

The export documentation comprises two complementary artifacts:

1. **Overview PDF (96 pages)**: Inventories 420 database tables organized into 19 groupings, with table-level descriptions, inter-table relationships, longitudinal tracking indicators (Y/N/L/S), product/vertical assignments, financial priority flags, and refresh frequencies. Includes 8 appendices with coded value sets for ophthalmology, visual acuity, fax status, patient history, billing, immunization, cancer staging, and HPI follow-up.

2. **Detailed PDF (210 pages)**: Provides field-level documentation for 240 of those tables — 5,250 individual fields with column name, description, data type, nullability, field length, and values/coding schema.

**Key metrics** (from `analysis/entity-inventory-summary.json`):
- **Total entities**: 420 (overview) / 240 with field-level detail (detailed DD)
- **Total fields documented**: 5,250
- **Fields with descriptions**: 5,144 (98.0%)
- **Fields with data types**: 5,237 (99.8%)
- **Fields with nullability**: 4,871 (92.8%)
- **Fields with coded values**: 1,179 (22.5%)

### Vendor's own content organization

The vendor organizes the export into 19 groupings (using their terminology). Below is a breakdown by grouping:

| Grouping | Entities (Overview) | Entities w/ Field Detail | Total Fields | Key Tables |
|---|---|---|---|---|
| PM Financials | 77 | 41 | 1,346 | `bill` (119), `charges` (110), `production_summary` (121), `payments_posted` (100), `payer_adjustments` (98), `accounts_receivable` (83) |
| Ophth Pretesting | 25 | 25 | 1,209 | `wearing_contacts` (110), `binocular` (107), `contacts_trial` (106), `visual_acuity` (93), `color_vision` (89), `refraction` (82) |
| Patient | 53 | 53 | 913 | `patient` (195), `insurance_policy` (139), `patient_flag` (12), `allergy`, `problem_list`, `medication`, `immunization` |
| Prescription | 7 | 7 | 337 | `rgp_contacts_rx` (109), `glasses_rx` (105), `contacts_rx` (74), `rx`, `compound_medication` |
| eLab | 21 | 21 | 252 | `lab_request`, `lab_result`, `elab_order`, `result_log` |
| Appointment | 15 | 15 | 216 | `appointment` (97), `appointment_insurance_policy`, `appointment_log` |
| Visit | 17 | 17 | 198 | `visit`, `vitals`, `ros`, `final_bill_procedure`, `visit_quality_measure` |
| Pathology | 10 | 10 | 123 | `pathology_log`, `cancer_log` (47), `cancer_log_visit` |
| Inventory | 20 | 20 | 120 | `product_sales` (46), `stock`, `package`, `product` |
| CC/HPI | 9 | 9 | 115 | `hpi_response_metadata` (18), `hpi_follow_up`, `hpi_response` |
| Office Flow | 12 | 12 | 102 | `task`, `task_fax_inbound`, `facility_resource` |
| Document | 7 | 7 | 92 | `file_attachment`, `fax_outbound`, `fax_inbound`, `fax_management` |
| Diagnosis | 13 | 13 | 91 | `diagnosis`, `diagnosis_morphology`, `diagnosis_body_location` |
| Practice | 88 | 7 | 64 | `visit_referral`, `consent_form_patient`, `referral_source_link` (mostly config/reference tables) |
| Procedure | 6 | 6 | 45 | `procedure`, `procedure_metadata`, `procedure_body_location` |
| Exam | 4 | 4 | 27 | `exam_element`, `exam_element_metadata` |
| Lookup | 7 | 0 | 0 | `loinc`, `icd9`, `icd10`, `snomed` (reference tables, no field detail) |
| MIPS | 9 | 0 | 0 | `mips_score`, `mips_quality_measure_score` (overview-only) |
| Medical Lookup | 20 | 0 | 0 | `static_diagnosis`, `static_procedure`, etc. (reference tables) |

The full entity inventory with all 420 entities and 5,250 fields is in `analysis/entity-inventory-full.json`.

### Representative largest tables

| Table | Fields | Grouping | Description (truncated) |
|---|---|---|---|
| `patient` | 195 | Patient | Patient demographics, practice data, clipboard info |
| `insurance_policy` | 139 | Patient | Insurance policy details |
| `production_summary` | 121 | PM Financials | Production summary financial data |
| `bill` | 119 | PM Financials | Bills generated at the practice |
| `wearing_contacts` | 110 | Ophth Pretesting | Contact lens wear data |
| `charges` | 110 | PM Financials | Charge detail |
| `rgp_contacts_rx` | 109 | Prescription | RGP contact lens prescriptions |
| `binocular` | 107 | Ophth Pretesting | Binocular vision testing |
| `contacts_trial` | 106 | Ophth Pretesting | Contact lens trial data |
| `glasses_rx` | 105 | Prescription | Eyeglass prescriptions |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized around 19 vendor-defined groupings that map closely to the product's major functional modules:

**Deepest coverage (1,000+ fields each)**:
- **PM Financials** (1,346 fields, 77 entities): Exceptionally detailed billing coverage — bills, charges, payments posted, payer adjustments, accounts receivable, claims, claim submissions, claim scrub rules, production summaries, refunds, transfers, statements, batch processing, billing quotes. This is genuinely deep financial data, not just summary billing.
- **Ophth Pretesting** (1,209 fields, 25 entities): Comprehensive specialty-specific ophthalmic testing data — visual acuity, refraction, keratometry, IOP, pachymetry, visual fields, cover test, motility, duction, color vision, RNFL thickness, endothelial cell counts. Each test type has its own table with dozens of measurement fields.

**Strong coverage (100-900 fields)**:
- **Patient** (913 fields, 53 entities): Extensive demographics, insurance, history (medical, surgical, family, social, gynecological, pregnancy), allergies, medications, problem list, immunizations, chart notes, consent forms.
- **Prescription** (337 fields, 7 entities): Multiple prescription types (general Rx, glasses, contacts, RGP contacts, compound medications).
- **eLab** (252 fields, 21 entities): Lab orders, results, specimens, SNOMED coding.
- **Appointment** (216 fields, 15 entities): Scheduling, authorization, waitlist, reminders, insurance snapshots.
- **Visit** (198 fields, 17 entities): Visit data, vitals, ROS, billing procedures/diagnoses, follow-ups, quality measures.
- **Pathology** (123 fields, 10 entities): Biopsy logs, pathology results, cancer staging/treatment logs.
- **Inventory** (120 fields, 20 entities): Products, packages, stock, sales, cabinets.
- **CC/HPI** (115 fields, 9 entities): Chief complaint/HPI response data.

**Moderate coverage**:
- **Office Flow** (102 fields): Task management, fax routing, facility resources.
- **Document** (92 fields): File attachments, fax management (note: physical attachments excluded).
- **Diagnosis/Procedure/Exam**: Clinical findings from the Virtual Exam Room.
- **Practice**: Mostly configuration/reference (88 entities but only 64 fields with detail — most are structural tables).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient` (195 fields), `patient_race`, `patient_ethnicity`, `patient_language`, `patient_phone_number`, `patient_address`, `patient_email` | Thorough — 195 fields in patient table alone |
| Encounters / visits | ✅ Covered | `visit`, `visit_attendee`, `visit_finalization_phase`, `appointment` (97 fields) | Well-covered with visit finalization workflow |
| Problems / conditions | ✅ Covered | `problem_list`, `diagnosis` + 12 related tables (91 fields), `diagnosis_morphology`, `diagnosis_body_location` | Detailed including DDx, ADx, body location, morphology |
| Medications / prescriptions | ✅ Covered | `medication`, `rx`, `compound_medication`, `glasses_rx`, `contacts_rx`, `rgp_contacts_rx` (337 fields total) | Very thorough including specialty optical Rx |
| Allergies | ✅ Covered | `allergy` table in Patient grouping | Present |
| Immunizations | ✅ Covered | `immunization` table, Appendix F value sets | Present with coded values |
| Vitals | ✅ Covered | `vitals` table in Visit grouping | Present |
| Lab results | ✅ Covered | `lab_request`, `lab_result`, `elab_order`, `elab_order_result`, `result_log` + sub-tables (252 fields) | Thorough — includes SNOMED specimens, result details, attachments |
| Imaging / diagnostic reports | ⚠️ Partial | Document attachments (`file_attachment`, `result_log_attachment`) present but "physical attachments are excluded." No DICOM image tables. | Product stores ophthalmic DICOM images (OCT, visual fields, fundus photos); export explicitly excludes physical files — metadata only |
| Procedures | ✅ Covered | `procedure`, `procedure_body_location`, `procedure_metadata` (45 fields), `final_bill_procedure` | Well-covered including nested metadata |
| Clinical notes / documents | ✅ Covered | `chart_note`, `chart_note_signature`, `chart_segmentation_event`, `file_attachment`, `document_category` | Present |
| Care plans / goals | ⚠️ Partial | `visit_follow_up`, `visit_follow_up_reason`, `outcome_measurement` | Follow-up and outcomes tracked; no explicit care plan entity |
| Orders / referrals | ✅ Covered | `order_log`, `order_log_detail`, `order_log_attachment`, `visit_referral`, `diagnosis_referral`, `referral_contact` | Comprehensive order tracking |
| Insurance / coverage | ✅ Covered | `insurance_policy` (139 fields), `insurance_group`, `insurance_policy_authorization`, `insurance_company`, `payer`, `payer_plan` | Very detailed — authorizations, addresses, phone numbers |
| Claims / billing | ✅ Covered | 77 PM Financials entities, 1,346 fields: `bill`, `charges`, `claim`, `claim_submission`, `bill_item`, `claim_scrub_rule` | Exceptionally deep — includes claim scrubbing rules, denial categories, timely filing |
| Payments | ✅ Covered | `payments_received` (50 fields), `payments_posted` (100 fields), `payer_adjustments` (98 fields), `patient_adjustments`, `refunds`, `transaction_settlement` | Comprehensive payment lifecycle |
| Consents / directives | ✅ Covered | `consent_form`, `consent_form_patient`, `consent_form_facility` | Present |
| Patient communications | ⚠️ Partial | `intra_mail`, `intra_mail_recipient` (internal mail); `fax_inbound`, `fax_outbound` | Internal messaging present; no evidence of patient portal messages (APPatient) or Klara messaging integration |
| Specialty-specific (Ophthalmology) | ✅ Covered | 25 Ophth Pretesting entities, 1,209 fields covering visual acuity, refraction, keratometry, IOP, pachymetry, visual fields, cover test, motility, color vision, RNFL, endothelial counts | Exceptionally thorough specialty data |
| Specialty-specific (Dermatology) | ✅ Covered | `pathology_log`, `cancer_log` (47 fields) + cancer treatment/staging tables; Appendix G cancer log values with TNM staging | Well-covered pathology and cancer registry |
| Specialty-specific (OB/GYN) | ✅ Covered | `gyn_history`, `patient_pregnancy`, `patient_pregnancy_baby`, `pregnancy_chart_patient_vitals`, `pregnancy_chart_baby_vitals`, `patient_menstrual_history`, `patient_reproductive_stage` | Comprehensive pregnancy/OB tracking |
| Specialty-specific (GI) | ⚠️ Partial | No explicit gastroenterology/endoscopy tables visible, though gGastro is a separate product line | May be a separate export for gGastro ASC module |
| Social determinants | ✅ Covered | `patient_sdoh`, `social_history` | Present |
| Family history | ✅ Covered | `family_history`, `specialty_family_history` | Present |
| Inventory / supplies | ✅ Covered | 20 Inventory entities, 120 fields: products, stock, packages, sales, cabinets | Uncommon for EHI exports; present here |

## 6. Documentation Quality

**Overall: Very High.** This is among the most thorough EHI export documentation produced by any vendor.

**Strengths**:
- **Field-level completeness**: 5,250 fields with 98.0% having descriptions, 99.8% having data types, 92.8% having nullability — near-complete documentation
- **Value set appendices**: 8 appendices define coded values for specialty-specific fields (ophthalmology usage, visual acuity scales, cancer staging, HPI follow-up)
- **Relationship documentation**: Inter-table relationships documented in the overview (foreign key references)
- **Longitudinal tracking**: Each table has Y/N/L/S indicators explaining whether change history is maintained
- **Product/vertical assignments**: Tables indicate which specialty modules they apply to
- **Refresh frequency**: Each table states its data refresh cadence
- **Recently updated**: January 2026

**Weaknesses**:
- **No export format specification**: The actual export file format (CSV, TSV, JSON?) is not stated
- **No export initiation procedure**: No instructions on how to request or trigger the export
- **No sample data**: No example export files or test data
- **Physical attachments excluded**: Images and file attachments are metadata-only
- **180 tables overview-only**: 180 of 420 tables lack field-level detail in the detailed DD (mostly Practice/config and lookup tables, but also some PM Financials tables)

**Could a developer build an import?** Mostly yes. The field names, types, descriptions, and relationships provide enough to build a schema and map most data. The lack of explicit file format specification and sample data would require some experimentation, and the 180 tables without field detail would need additional research.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains EMA stores. With 420 entities across 19 groupings, it goes far beyond USCDI clinical summaries to include:
- Extensive PM/billing data (1,346 fields — the single largest grouping)
- Specialty-specific clinical data (1,209 fields for ophthalmology pretesting alone)
- Inventory management (120 fields)
- Document management, fax tracking, internal messaging
- Cancer registry/staging, pathology, OB/GYN-specific records
- Social determinants, consent forms, quality measures

The few gaps (patient portal messages, DICOM image files, Klara messaging) are relatively minor compared to the overall coverage. The export is not a repackaged USCDI subset — it represents a genuine designated record set.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export using the vendor's native relational data model. Key evidence:
1. The export uses internal database table/column names (e.g., `payer_adjustments_rarc`, `hpi_response_metadata_selection`, `appointment_facility_resource_reservation`) — not FHIR resources or C-CDA sections
2. It includes 77 PM Financials entities — data that would never appear in a (g)(10) FHIR API or C-CDA export
3. 25 ophthalmology pretesting tables with 1,209 fields of specialty measurement data
4. Inventory management tables (stock, cabinets, product sales)
5. The documentation is titled "EHI Export Data Dictionary for Single Patient Export" — explicitly built for (b)(10)
6. The FHIR API is documented separately at portal.api.modmed.com for (g)(10) only

### Key Findings

1. **Exceptionally deep financial data**: 1,346 fields across 77 PM Financials entities — claims, billing, payments, adjustments, AR, production summaries, denial management, claim scrubbing. This is the deepest billing coverage observed in EHI exports.

2. **Rich specialty-specific data**: 1,209 fields for ophthalmology pretesting (25 test-type tables), cancer staging/pathology (10 tables), OB/GYN pregnancy tracking, dermatology-specific pathology — all included in the export.

3. **High documentation quality**: 98% of 5,250 fields have descriptions; 99.8% have data types; 8 value set appendices provide coded values. January 2026 date shows active maintenance.

4. **Minor gaps relative to product capabilities**: DICOM images explicitly excluded ("physical attachments are excluded"), patient portal content (APPatient) not visible, Klara messaging integration absent. These are the main gaps versus the product's full feature set.

5. **Native relational model, not standards-based**: Export uses the vendor's internal schema — highly complete but would require significant mapping effort to transform into FHIR or other standard formats.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   Tabular/relational (specific file format not documented)
Entities:        420 (240 with field-level detail)
Fields:          5,250
Descriptions:    98.0% of fields have descriptions
Sample data:     No
Bulk export:     No (single-patient only)
Domains covered: 18 of 20 applicable domains
```

### Bottom Line

ModMed EMA's EHI export is one of the most thorough implementations of (b)(10) encountered. A patient would receive a genuinely comprehensive copy of their data spanning clinical encounters, billing/claims, specialty testing, prescriptions, labs, pathology, and more — 5,250 documented fields across 420 database tables. The biggest limitation is the exclusion of physical file attachments (including diagnostic images) and the absence of patient portal/messaging content; the biggest strength is the exceptional depth of financial and specialty-specific clinical data that most vendors omit entirely.

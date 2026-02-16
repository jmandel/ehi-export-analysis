# EHI Export Analysis: DocToMe, Inc.

**Product**: ethizo EHR v2.0
**Analysis date**: 2026-02-16
**CHPL ID**: 15.05.05.3060.DOTM.01.00.1.200107

## 1. Product Context

Ethizo EHR is a cloud-based, full-stack EHR and practice management platform developed by DocToMe, Inc., a very small vendor (~5–9 employees) based in Gig Harbor, Washington. Despite its small size, ethizo is certified across an unusually broad range of ONC criteria and offers eight distinct modules:

1. **MU-3 Certified EHR** — clinical documentation, CPOE, CDS, lab/radiology orders, referral management, scheduling
2. **Practice Management System (PMS)** — full billing/revenue cycle: claims scrubbing, ERA posting, CPT macros, eligibility verification, PCI-compliant payments, KPI dashboards, patient statements
3. **Patient Portal** — appointment booking, secure messaging, medication tracking, Fitbit/device integration, questionnaires
4. **Vezo (Telemedicine)** — video visits, virtual rooms, transit notes
5. **Hybrid eFax** — fax/email/e-signature document management
6. **IVR** — automated phone triaging and call tracking
7. **CCM (Chronic Care Management)** — care plan creation, activity tracking, automated billing
8. **RPM (Remote Patient Monitoring)** — cellular-connected devices for BP, glucose, CGM, SpO2, weight, temperature, HR, ECG

The product targets ambulatory practices, FQHCs, and PALTC settings across 20+ specialties. The PMS module is a significant part of the product offering, with detailed billing, claims, payments, and revenue cycle features.

**Baseline for export completeness**: The export should cover clinical data across all specialties, billing/claims/payment data from the PMS, secure messages, telemedicine records, RPM data, CCM care plans, and patient-generated data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `EHI-Export-b.10-Documentation-v2.pdf` (311 KB, 9 pages) | Sole documentation artifact. Describes the "Share Data" export mechanism, CDA data dictionary with XPATH paths and code system OIDs for 24 CCD sections/82 data elements, plus mention of CSV and document exports. Created 2025-03-01. | **Primary source** — contains the entire data dictionary |
| `ehi-export-landing-page.png` (64 KB) | Screenshot of the EHI export page at ethizo.com showing just a heading and download link | Low — confirms page structure only |
| EHI export landing page (live verification) | Verified https://www.ethizo.com/electronic-health-information-export/ returns HTTP 200 with the same PDF download link | Confirms accessibility |

**No sample data files, no machine-readable schemas (XSD, JSON Schema), no CSV field documentation, and no FHIR Bulk Data documentation were provided.** The entire EHI export documentation consists of a single 9-page PDF.

## 3. Export Mechanics

- **Format**: ZIP file containing:
  - Clinical data in C-CDA R2.1 (XML)
  - Patient demographics and insurance details (CSV)
  - Appointments (CSV)
  - Scanned documents (PDF, JPG, PNG) in chart-number folders with category subfolders
- **Standard**: HL7 CDA Release 2, Consolidated CDA Templates for Clinical Notes, US Realm, DSTU R2.1, August 2015 (§ 170.205(a)(4))
- **Single patient**: Via "Share Data" menu → select sections → Process → secure link via email/text → download ZIP
- **Bulk/population**: Via Quick Links → Share Data → EHI export for single/bulk → Process → secure link → download ZIP of ZIPs
- **FHIR alternative**: One sentence at the end of the PDF mentions FHIR DocumentReference (single-patient) and FHIR Bulk Data (population) as described in §170.315(b)(10)(ii). No endpoints, authentication details, or resource type listing are documented for this pathway.
- **Access constraints**: Export is delivered via a secure link sent to an email or phone number, with a second-factor token required to access the download. No mention of fees.

## 4. Export Content: What's In It

### CDA Data Dictionary

The PDF documents 24 CCD sections containing 82 data elements. Each element may include:
- **XPATH/Entry path**: 30 of 82 fields (37%) have an XPATH or template entry path documented
- **Code system OID**: 27 of 82 fields (33%) reference a coded terminology
- **Code system name**: 27 fields identify the code system by name (e.g., SNOMED, LOINC, CPT, RxNorm)

No fields have:
- Data type documentation
- Nullability/optionality
- Value set bindings (within code systems)
- Description text beyond the field name
- Foreign key / relationship documentation
- Sample data or examples

### Vendor's own content organization

The CDA dictionary is organized by CCD section. All 24 sections and their field counts:

| CCD Section | Fields | Fields with Code System | Template ID |
|---|---|---|---|
| Patient Demographics/Information | 6 | 3 | — |
| Provider's name and office contact | 3 | 0 | — |
| Date and Location of visit | 2 | 0 | 2.16.840.1.113883.10.20.22.2.22.1 |
| Chief Complaint and Reason for visit | 1 | 0 | 2.16.840.1.113883.10.20.22.2.13 |
| Encounters | 5 | 2 | 2.16.840.1.113883.10.20.22.2.22.1 |
| Immunizations | 9 | 3 | 2.16.840.1.113883.10.20.22.2.2.1 |
| Instructions | 1 | 1 | 2.16.840.1.113883.10.20.22.2.45 |
| Treatment Plan | 2 | 1 | 2.16.840.1.113883.10.20.22.2.10 |
| Social History | 3 | 2 | 2.16.840.1.113883.10.20.22.2.17 |
| Problems | 3 | 1 | 2.16.840.1.113883.10.20.22.2.5.1 |
| Medications | 5 | 1 | 2.16.840.1.113883.10.20.22.2.1.1 |
| Medication Allergies | 4 | 4 | 2.16.840.1.113883.10.20.22.2.6.1 |
| Laboratory Tests | 4 | 1 | — |
| Laboratory Information | 5 | 0 | — |
| Laboratory value(s)/result(s) | 5 | 1 | 2.16.840.1.113883.10.20.22.2.3.1 |
| Vitals | 2 | 1 | 2.16.840.1.113883.10.20.22.2.4.1 |
| Goals | 3 | 0 | 2.16.840.1.113883.10.20.22.2.60 |
| Procedures | 2 | 1 | 2.16.840.1.113883.10.20.22.2.7.1 |
| Care team member(s) | 3 | 0 | 2.16.840.1.113883.10.20.22.2.500 |
| Reason for Referral | 1 | 1 | 1.3.6.1.4.1.19376.1.5.3.1.3.1 |
| Medical Equipment (Implanted Devices) | 2 | 1 | 2.16.840.1.113883.10.20.22.2.23 |
| Mental Status | 4 | 1 | 2.16.840.1.113883.10.20.22.2.56 |
| Functional Status | 4 | 1 | 2.16.840.1.113883.10.20.22.2.14 |
| Health Concerns | 3 | 1 | 2.16.840.1.113883.10.20.22.2.58 |
| **Total** | **82** | **27** | **20 of 24 sections** |

### Non-CDA Components

| Component | Format | Field Documentation |
|---|---|---|
| Patient Demographics and Insurance Details | CSV | **None** — described only as "comprehensive view" |
| Appointments | CSV | **None** — described as "future appointments details" only |
| Documents | PDF/JPG/PNG | **None** — described as signed notes, lab results, radiology reports, scanned uploads; organized in patient chart folders with category subfolders |

The CSV files may contain fields beyond what the CDA covers (e.g., insurance details, appointment scheduling data), but without any field-level documentation, this cannot be assessed. The appointment CSV is explicitly limited to "future appointments" only.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export has three layers:

1. **CDA clinical data** (82 documented fields across 24 sections): This is a standard C-CDA clinical summary covering the usual USCDI domains — demographics, encounters, problems, medications, allergies, labs, vitals, immunizations, procedures, care team, goals, referrals, implantable devices, mental/functional status, health concerns, and social history. The code systems referenced (SNOMED, ICD-10, LOINC, RxNorm, CVX, CPT, NDC, HCPCS, GMDN) are all standard. There are no vendor-specific CDA extensions or custom sections.

2. **CSV supplements** (0 documented fields): Demographics/insurance and appointments in CSV. No field names, types, or examples are provided. The demographics/insurance CSV could potentially contain billing-adjacent data (insurance plan details, subscriber info), but this is speculation.

3. **Document files**: Scanned/uploaded documents organized by chart number and category. This captures the unstructured document layer (signed notes, lab reports, radiology, receipts) but provides no structured data.

The richest sections by field count are Immunizations (9 fields), Demographics (6 fields), and Encounters/Medications/Laboratory (5 fields each). Most sections have 2–4 fields. The overall level of detail is thin — these are CDA section-level element lists, not a database-level data dictionary.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CDA: 6 fields (name, sex, DOB, race, ethnicity, language). CSV "demographics" file mentioned but undocumented | CDA covers basic demographics. CSV may supplement but is undocumented |
| Encounters / visits | ✅ Covered | CDA Encounters section: code, performer, diagnosis, location, date (5 fields, CPT/SNOMED/ICD-10) | Reasonable for a C-CDA |
| Problems / conditions | ✅ Covered | CDA Problems section: problem, status, active date (SNOMED/ICD-10) | Standard coverage |
| Medications / prescriptions | ✅ Covered | CDA Medications section: medication, directions, start/end date, status (RxNorm/NDC) | Standard coverage; no PDMP-specific data |
| Allergies | ✅ Covered | CDA Medication Allergies: substance, reaction, severity, status (RxNorm/SNOMED) | Standard coverage |
| Immunizations | ✅ Covered | CDA Immunizations: vaccine, date, status, route, site, manufacturer, dose, lot, notes (CVX/CPT-4) | Most detailed section (9 fields) |
| Vitals | ⚠️ Partial | CDA Vitals: observation, date/time (LOINC). Only 2 fields documented | Standard CDA vitals; no RPM device-sourced data detail |
| Lab results | ✅ Covered | CDA Labs: 3 sub-sections with 14 total fields covering test info, lab info, and result values (LOINC) | Reasonable coverage |
| Imaging / diagnostic reports | ⚠️ Partial | Only via document exports (radiology reports as scanned files) | No structured imaging/radiology order data |
| Procedures | ✅ Covered | CDA Procedures: procedure, date (CPT-4/SNOMED/HCPCS) | Standard coverage |
| Clinical notes / documents | ✅ Covered | Document export includes signed progress notes and other uploaded documents in PDF/JPG/PNG | Unstructured only; no structured note metadata |
| Care plans / goals | ✅ Covered | CDA Treatment Plan (planned observations, dates) + Goals section (goal, value, date) | Standard coverage; does not specifically address CCM care plans |
| Orders / referrals | ✅ Covered | CDA Reason for Referral section (SNOMED) | Basic referral reason only; no order details |
| Insurance / coverage | ⚠️ Partial | CSV "demographics and insurance details" mentioned but no fields documented | Cannot assess depth; no field-level documentation |
| Claims / billing | ❌ Not covered | No billing entities in the export | **Significant gap.** Product has full PMS with claims scrubbing, ERA posting, CPT macros, eligibility verification, payments, patient statements, and revenue cycle KPIs. None of this appears in the export. |
| Payments | ❌ Not covered | No payment entities in the export | **Significant gap.** Product offers PCI-compliant payment processing and copay collection. |
| Consents / directives | ❌ Not covered | No consent or advance directive data | Product likely stores consents; not addressed |
| Patient communications / portal messages | ❌ Not covered | No secure messaging data in the export | **Gap.** Patient portal supports secure messaging. |
| Specialty-specific (multi-specialty) | ❌ Not covered | No specialty-specific clinical data beyond standard CDA sections | Product targets 20+ specialties and has behavioral medicine, wound care, and other modules. Custom assessments, specialty forms, and questionnaire data are not represented. |
| Remote Patient Monitoring (RPM) | ❌ Not covered | No RPM data entities | **Gap.** RPM module captures BP, glucose, CGM, SpO2, weight, temp, HR, ECG from connected devices. CDA vitals section may capture some manually-entered vitals but not the RPM data stream. |
| Telemedicine records | ❌ Not covered | No telemedicine visit or transit note data | **Gap.** Vezo telemedicine module generates visit records and transit notes. |
| Chronic Care Management (CCM) | ❌ Not covered | No CCM-specific entities (enrollment, activity logs, care plans) | **Gap.** CCM module tracks enrollment, care plans, activity, and automated billing. |

## 6. Documentation Quality

**Overall: Thin and incomplete.**

- **CDA mapping is functional but surface-level.** The XPATH paths and code system OIDs allow a developer to parse C-CDA XML for the documented sections. However, only 37% of fields have XPATH paths and 33% have code system references. No field has a description beyond its name, no data types are specified, no value set bindings are provided, and no relationships between elements are documented.

- **CSV exports are completely undocumented.** The demographics/insurance and appointments CSV files are described in a single sentence each ("comprehensive view of..."). No field names, types, sample rows, or column documentation is provided. A developer would have to reverse-engineer these files from sample exports.

- **No sample data.** No example CDA documents, CSV extracts, or sample ZIP exports are provided anywhere.

- **No machine-readable schemas.** No XSD, JSON Schema, or other parseable artifact. Only the PDF.

- **FHIR Bulk Data pathway is essentially undocumented.** A single sentence mentions it exists with no endpoint URLs, authentication, or resource type listing. Review of the FHIR API documentation at fhir-api.ethizo.com shows only standard US Core resources — no billing, scheduling, or custom resources — confirming this is the (g)(10) API reused for (b)(10).

- **Could a developer build an import from this documentation?** For CDA: partially, since it's a standard format and the section/XPATH mapping provides a roadmap. For CSV: no, not without sample files. For documents: trivially (just file I/O). For billing, messaging, RPM, CCM, telemedicine data: impossible — these are not documented or exported.

## 7. Overall Assessment

### Classification

**Standard-based projection.** The export is primarily a C-CDA clinical summary augmented with undocumented CSV files and document attachments. It uses a recognized standard (C-CDA R2.1) but does not export the vendor's native data model. The 82 CDA data elements represent the standard CCD template — no vendor-specific extensions or custom sections are present. Major data domains stored by the product (billing, PMS, RPM, CCM, telemedicine, secure messaging) are entirely absent.

### Key Findings

1. **The export is a C-CDA clinical summary, not a comprehensive EHI export.** The 24 CCD sections and 82 data elements are the standard clinical summary template. No vendor-specific data, billing, or specialty data is included. This is the classic pattern of a C-CDA/(g)(10) repackaging being called "(b)(10)."

2. **The entire Practice Management System (billing, claims, payments, ERA, eligibility) is missing.** For a product that explicitly markets full revenue cycle management with claims scrubbing, ERA posting, PCI-compliant payments, and KPI dashboards, the complete absence of billing data from the EHI export is the most significant gap.

3. **Multiple product modules generate patient data that is not exported.** RPM (remote patient monitoring with cellular devices), Vezo telemedicine, CCM (chronic care management), secure messaging, and patient-generated data from portal questionnaires and device integrations are all absent.

4. **CSV exports lack any field documentation.** The demographics/insurance and appointments CSVs could potentially contain valuable data, but with zero field names, types, or examples documented, their value cannot be assessed.

5. **Documentation is a single 9-page PDF with no sample data or machine-readable schemas.** The entire EHI export documentation is one Word-generated PDF. While the CDA section mapping is functional, the overall documentation effort is minimal relative to the product's breadth.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA R2.1 (XML) + CSV + document files (PDF/JPG/PNG)
Model type:      Standard projection (C-CDA), not native database
Entities:        24 CCD sections + 2 undocumented CSV files + document export
Fields:          82 CDA data elements (+ unknown CSV fields)
Descriptions:    0% (no fields have descriptions beyond their name)
Sample data:     No
Bulk export:     Yes (ZIP of ZIPs for population export)
Domains covered: 9 of 18 applicable domains (with several only partially)
```

### Bottom Line

Ethizo's EHI export is a C-CDA clinical summary repackaged as a (b)(10) export, supplemented by undocumented CSV files and document attachments. It covers standard clinical domains adequately but entirely omits billing/financial data, RPM, telemedicine, CCM, secure messaging, and specialty-specific data — all significant modules of this product. A patient or provider requesting their complete data would receive a clinical summary and scanned documents, but none of their billing history, RPM readings, telehealth records, or care management data. The single biggest gap is the complete absence of the Practice Management System's billing and financial data.

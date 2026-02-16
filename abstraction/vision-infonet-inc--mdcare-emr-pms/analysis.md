# EHI Export Analysis: Vision Infonet Inc

**Product**: MDCare EMR/PMS  
**Analysis date**: 2026-02-15  
**CHPL ID**: 15.04.04.2872.MDCa.06.02.1.250604 (CHPL listing ID 11650)

## 1. Product Context

MDCare EMR/PMS is a combined Electronic Medical Records and Practice Management System from Vision Infonet Inc, an Illinois-based healthcare IT and services company. The product is web-based, ONC-certified (v6.0, certified June 2025), and serves ambulatory/outpatient practices ranging from solo providers to groups of 400+ physicians. Vision Infonet claims 2,000+ clients and markets specialty-specific versions for cardiology, dermatology, endocrinology, family practice, pulmonary medicine, psychiatry, critical care, geriatric/palliative care, radiology, podiatry, and internal medicine.

The "PMS" in the product name is significant: MDCare integrates full practice management and billing capabilities alongside its clinical EMR. The product handles:

- **Clinical documentation**: Customizable specialty-specific templates, SOAP notes, AI-powered speech-to-text (v6.0), clinical decision support
- **E-prescribing**: Surescripts integration
- **Billing/RCM**: CMS-1500 claims, electronic superbills, accounts receivable, denial management, payment posting, automated CPT/E&M coding
- **Lab/imaging interfaces**: HL7, DICOM
- **Document management**: Scanning, fax integration ("Faxtone")
- **Patient portal**: Exists at app.mdcare.com/mdcareportal
- **Scheduling**: Multi-provider/resource scheduling

Vision Infonet's primary business model combines the EMR/PMS software with managed billing services — many clients use both. This means the billing and RCM data within the product is a core data domain, not a peripheral feature.

For assessing EHI export completeness, the critical question is whether the export covers both the clinical EMR side **and** the practice management/billing side of the product.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `EHIexport.pdf` (5.1 MB, 19 pages) | Primary (b)(10) documentation. Title page, table of contents, overview, single-patient export instructions with UI screenshots, bulk export instructions with UI screenshots, sample C-CDA rendering, and C-CDA data dictionary (pages 12–19). Created Nov 29, 2023; references MDCare V5.1. | **Primary source** — contains all EHI export documentation |
| `APIDocument.pdf` (1.4 MB, 54 pages) | FHIR R4 SMART on FHIR API documentation for (g)(10) certification. OAuth 2.0 auth flows, FHIR resource request examples, Terms of Use. References V5.1. | Low for (b)(10) — this is g(10) API documentation, not the EHI export. Included for completeness. Prior report incorrectly stated 20 pages; actual is 54 pages. |
| `API.json` (4 KB) | FHIR R4 Bundle containing Endpoint and Organization resources for fhir.mdcare.com. | Minimal — g(10) service base URL, not related to b(10) export |

**No sample export data files were provided.** No data dictionary beyond the C-CDA section listing in the PDF. No machine-readable schema. No JSON, CSV, or XML schema files for the export format.

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated CDA) XML, plus PDF and HTML renderings of the same document. Each encounter produces three files named `{MRNo}-{Date}` (e.g., `1004-20231128`) in a ZIP archive. The screenshot on page 6 shows file sizes of 31 KB (HTML), 10 KB (PDF), and 140 KB (XML) for one encounter.
- **Standard**: §170.205(a)(4) HL7 CDA R2 Consolidated CDA Templates DSTU R2.1 (August 2015), referencing USCDI Version 1.
- **Mechanism**: Dedicated UI feature at Home → Records Tab → EHI-Export. Role-based access.
- **Single-patient export**: Search by patient name, select specific encounter(s) or all encounters. Downloads as ZIP.
- **Bulk export**: Select "Multiple Patients," specify date range, resource, and physicians. Downloads one ZIP per patient.
- **Additional content**: Documentation states the ZIP includes "all scanned clinical and administrative documents" alongside the C-CDA. The UI shows checkboxes for "Medical Records," "Patient Demographics," and "All POS Documents."
- **Access constraints/fees**: Not documented. The export requires specific user roles.

## 4. Export Content: What's In It

### Data dictionary structure

The data dictionary occupies pages 12–19 of EHIexport.pdf. It lists C-CDA sections with their XPATHs/template IDs, code system OIDs, and code system names. There are no field-level descriptions, no data types, no cardinality, no optionality, no relationships, no value set bindings, and no sample values.

**Parsed totals from the data dictionary:**
- **24 C-CDA sections** documented
- **82 data elements** across all sections
- **27 fields** (33%) reference a code system OID/name
- **30 fields** (37%) have an XPATH or template ID

The 41 selectable checkboxes visible in the UI (page 4, page 9) include additional categories not individually detailed in the data dictionary text, such as: HPI, ROS, Past Medical History, Physical Exam, General Status, Interventions, Assessment, Medication Administered, Diagnostic Pending Test, Future Appointments, Future Scheduled Tests, Recommended Patient Decision Aids, and Clinical Notes.

### Vendor's own content organization

The vendor organizes content as C-CDA sections. The data dictionary enumerates the following:

| C-CDA Section | Fields | Fields w/ Code System | Template ID |
|---|---|---|---|
| Patient Demographics/Information | 6 | 3 | — |
| Provider's name and office contact information | 3 | 0 | — |
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
| Goal | 3 | 0 | 2.16.840.1.113883.10.20.22.2.60 |
| Procedures | 2 | 1 | 2.16.840.1.113883.10.20.22.2.7.1 |
| Care team member(s) | 3 | 0 | 2.16.840.1.113883.10.20.22.2.500 |
| Reason for Referral | 1 | 1 | 1.3.6.1.4.1.19376.1.5.3.1.3.1 |
| Medical Equipment | 2 | 1 | 2.16.840.1.113883.10.20.22.2.23 |
| Mental Status | 4 | 1 | 2.16.840.1.113883.10.20.22.2.56 |
| Functional Status | 4 | 1 | 2.16.840.1.113883.10.20.22.2.14 |
| Health Concern | 3 | 1 | 2.16.840.1.113883.10.20.22.2.58 |
| **Totals** | **82** | **27** | — |

The full parsed inventory is in `analysis/full-entity-inventory.json`. UI checkbox inventory is in `analysis/ui-checkbox-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export is structured entirely around C-CDA sections — the same standard sections used for clinical summaries and transitions of care. The content maps closely to USCDI v1 data elements:

- **Demographics**: 6 fields (name, sex, DOB, race, ethnicity, preferred language). No insurance, no contacts, no address.
- **Clinical encounters**: Encounter codes (CPT), dates, locations, diagnoses, performers.
- **Problems/medications/allergies**: Standard problem list (SNOMED/ICD-10), medication list (RxNorm/NDC), and allergy list with reactions/severity.
- **Laboratory**: Test codes (LOINC), results, reference ranges, interpretation, specimen source, lab information.
- **Vitals, immunizations, procedures**: Standard C-CDA sections with coded values.
- **Care planning**: Goals, treatment plan (including planned observations, pending tests, future appointments), health concerns, care team members, referrals.
- **Assessments**: Mental status, functional status (both SNOMED-coded), with dates, results, and comments.
- **Social history**: Observations (LOINC), descriptions (SNOMED).
- **Implantable devices**: SNOMED-coded with GMDN descriptions.

The UI also shows checkboxes for HPI, ROS, Physical Exam, General Status, Past Medical History, Clinical Notes, and Interventions — these are mentioned in the UI but not detailed in the data dictionary section of the PDF. They are likely exported as narrative text within the C-CDA.

The vendor also states that "all scanned clinical and administrative documents" are included in the ZIP alongside the C-CDA files. The UI checkbox "All POS Documents" likely refers to documents attached to point-of-service encounters. However, there is no documentation of what document types are included, how they are organized, or what metadata accompanies them.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient Demographics/Information` (6 fields: name, sex, DOB, race, ethnicity, language) | Basic demographics only — no address, no phone, no insurance info, no emergency contacts. Product stores richer registration data. |
| Encounters / visits | ✅ Covered | `Encounters` section (5 fields), `Date and Location of visit` (2 fields) | Encounter codes (CPT), dates, locations, performers, diagnoses documented. |
| Problems / conditions / diagnoses | ✅ Covered | `Problems` section (3 fields: problem code SNOMED/ICD-10, status, active date) | Standard problem list representation. |
| Medications / prescriptions | ✅ Covered | `Medications` section (5 fields: medication RxNorm/NDC, directions, start/end date, status) | Medication list covered; full prescribing transaction history (Surescripts) not mentioned. |
| Allergies | ✅ Covered | `Medication Allergies` section (4 fields: substance, reaction, severity, status) | Well-structured with SNOMED coding for reactions. |
| Immunizations | ✅ Covered | `Immunizations` section (9 fields) | Most detailed section — vaccine (CVX/CPT-4), date, status, route, site, manufacturer, dose, lot, notes. |
| Vitals | ✅ Covered | `Vitals` section (2 fields: observation LOINC, date) | Standard vitals representation. |
| Lab results | ✅ Covered | `Laboratory Tests` + `Laboratory Information` + `Laboratory value(s)/result(s)` (14 fields total across 3 sub-sections) | Comprehensive: test codes, lab info, specimen source, result values, reference ranges, interpretation. |
| Imaging / diagnostic reports | ⚠️ Partial | UI checkbox "Diagnostic Pending Test" visible; no dedicated imaging section in data dictionary. Product has DICOM interface. | Product stores DICOM imaging data; unclear if images or imaging reports beyond the C-CDA are exported. |
| Procedures | ✅ Covered | `Procedures` section (2 fields: procedure CPT-4/SNOMED/HCPCS, date) | Standard procedure list. |
| Clinical notes / documents | ⚠️ Partial | UI checkbox "Clinical Notes" + "all scanned clinical and administrative documents" in ZIP. HPI, ROS, Physical Exam, Past Medical History also selectable. | Notes appear to be included but no documentation of structure or completeness. Scanned documents included but undocumented. |
| Care plans / goals | ✅ Covered | `Treatment Plan` (2 fields), `Goal` (3 fields), `Health Concern` (3 fields) | Planned observations, dates, goals with values. |
| Orders / referrals | ✅ Covered | `Reason for Referral` (1 field), `Instructions` (1 field) | Basic referral reason (SNOMED). No detailed order data. |
| Insurance / coverage | ❌ Not covered | No insurance entities in export documentation | Product stores insurance data (insurance IDs, payer info, coverage details for billing). Significant gap. |
| Claims / billing | ❌ Not covered | No claims, superbills, or billing entities in export | Product has integrated billing module (CMS-1500, electronic superbills, claims processing). Major gap for an EMR/**PMS** product. |
| Payments | ❌ Not covered | No payment entities in export | Product handles payment posting, AR, collections. Major gap. |
| Consents / directives | ⚠️ Partial | UI tab "Advance Directives" visible in page 5 screenshot; no section in data dictionary. Scanned consent forms may be in ZIP. | Advance directives tab exists in the system but not documented as a structured export section. |
| Patient communications / portal | ❌ Not covered | No portal data or messaging entities in export | Product has patient portal (app.mdcare.com/mdcareportal) and clinical messaging. Gap. |
| Specialty-specific data | ❌ Not covered | No specialty-specific sections beyond standard C-CDA | Product markets specialty versions for 10+ specialties with customizable templates. Any specialty-specific structured data beyond standard C-CDA sections is not in the documented export. |

## 6. Documentation Quality

**Strengths:**
- Clear step-by-step instructions with annotated UI screenshots for both single-patient and bulk export workflows
- Dedicated EHI-Export feature (not just pointing to the FHIR API)
- Data dictionary identifies C-CDA sections, XPATHs, and code systems (OIDs)
- Both single-patient and bulk patient export documented

**Weaknesses:**
- **No field-level descriptions**: The data dictionary lists element names and code system OIDs, but provides no descriptions, cardinality, optionality, data types, or value set bindings
- **No sample data**: No sample export files are provided. One screenshot shows a rendered C-CDA, but no raw XML sample
- **No machine-readable schema**: No JSON schema, XSD, or other machine-readable artifact
- **Version mismatch**: Documentation references V5.1 (created November 2023) but current certification is V6.0 (June 2025)
- **Undocumented content**: The "All POS Documents" checkbox and "all scanned clinical and administrative documents" claim are not explained — no list of document types, no file naming conventions, no metadata description
- **Incomplete data dictionary vs. UI**: The UI shows 41 selectable categories, but the data dictionary only documents 24 sections. Categories like HPI, ROS, Physical Exam, General Status, Past Medical History, Clinical Notes, Interventions, Assessment, Medication Administered are selectable in the UI but not individually detailed in the data dictionary

A developer could use the C-CDA standard to parse the XML output, but the vendor's documentation alone would not be sufficient to understand what vendor-specific data or customizations are in the export. The C-CDA standard itself provides more structure than this documentation does.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The EHI export is a C-CDA (Consolidated CDA) clinical summary repackaged as the (b)(10) export. While the vendor has built a dedicated EHI-Export feature (not just reusing the FHIR API), the underlying export format and content scope are constrained to what C-CDA supports — which is clinical summary data aligned with USCDI v1. The export does not expose the vendor's native data model and entirely omits the practice management/billing side of the product.

### Key Findings

1. **The export is C-CDA, not a native data model export.** The entire export is structured around C-CDA sections (24 sections, 82 data elements). This is the same clinical summary format used for transitions of care, not a comprehensive EHI export. No vendor-specific tables or database structures are exposed. (Source: `EHIexport.pdf` pages 12–19)

2. **Billing and practice management data are completely absent.** MDCare EMR/**PMS** integrates billing (CMS-1500 claims, superbills, AR, payment posting, denial management) as a core function — the "PMS" is in the product name. None of this data appears anywhere in the export documentation. For a product whose vendor's primary business is medical billing services, this is a critical omission. (Source: `EHIexport.pdf` — no billing sections; `product-research.md` — billing capabilities)

3. **The vendor did build a dedicated EHI-Export feature.** Unlike vendors that simply point to their FHIR API, MDCare has a purpose-built export UI at Records → EHI-Export with both single-patient and bulk-patient modes, role-based access, and a rich selection interface with 41 checkboxes. This shows genuine effort toward compliance, even if the scope is limited. (Source: `EHIexport.pdf` pages 3–11, UI screenshots)

4. **Documentation is outdated relative to certification.** The PDF was created November 29, 2023 and references V5.1, but the product's current certification is V6.0 (certified June 4, 2025). V6.0 added AI capabilities including AI-based authorization generation and payment posting — none reflected in the export documentation. (Source: `EHIexport.pdf` title page; `chpl-metadata.json`)

5. **Scanned documents are included but undocumented.** The documentation repeatedly states the ZIP includes "all scanned clinical and administrative documents," and the UI has an "All POS Documents" checkbox. This could partially compensate for the lack of structured billing data if POS documents include superbills or encounter forms, but without documentation of what's included, this is impossible to assess. (Source: `EHIexport.pdf` pages 5, 6, 10)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + PDF + HTML (ZIP archive per patient)
Model type:      Standard projection (C-CDA / USCDI v1)
Entities:        24 C-CDA sections
Fields:          82 data elements documented
Descriptions:    0% (names and code systems only, no descriptions)
Sample data:     No (screenshot of rendered C-CDA only)
Bulk export:     Yes (multi-patient with date range filtering)
Domains covered: 9 of 16 applicable domains (✅ or ⚠️)
```

### Bottom Line

MDCare's EHI export is a C-CDA clinical summary with scanned documents — it covers standard clinical data adequately but completely omits the billing and practice management data that is half of what this EMR/PMS product stores. A patient would get a usable clinical record but no billing history, insurance information, payment records, or specialty-specific structured data. The single biggest gap is the total absence of billing/financial data from a product whose name literally includes "PMS" (Practice Management System) and whose vendor's primary business is medical billing services.

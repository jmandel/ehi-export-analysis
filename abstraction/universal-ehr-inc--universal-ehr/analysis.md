# EHI Export Analysis: Universal EHR, Inc.

**Product**: Universal EHR (also known as Physician's Solution)
**Analysis date**: 2025-07-17
**CHPL IDs**: 9333 (15.04.04.2478.Univ.02.00.1.180312)

## 1. Product Context

Universal EHR (Physician's Solution) is a browser-based EHR and practice management system from Universal EHR, Inc., a very small company based in Garden Grove, CA. The product targets ambulatory/outpatient practices and has an extremely small market footprint, concentrated among Vietnamese-American medical practices in Southern California (notably DAO Medical Group, a 30+ physician multi-specialty group).

The product is certified as a Complete EHR (version 2.0.0, certified 2018-03-12) across 35+ ONC criteria. Based on vendor materials and the product UI visible in screenshots, it stores:

- **Clinical data**: Patient demographics, clinical notes/progress notes, conditions/diagnoses, medications/prescriptions (e-prescribing), lab orders and results, radiology/imaging results, referrals, vitals, care teams
- **Billing/practice management**: Superbills, claims, charge capture, collections, insurance information (primary/secondary), appointment scheduling
- **Patient engagement**: Patient portal ("Patient Direct"), provider-to-patient messaging ("Doctor Direct"), provider-to-provider messaging
- **Specialty features**: Customizable templates for OB/GYN, cardiology, pediatrics, internal medicine, and other specialties
- **Documents**: Patient document storage (PDFs, images, lab reports, referral letters, mammograms, etc.)

The patient chart UI (visible on PDF page 1) confirms tabs for: DEMOGRAPHIC, SUPER BILL, PROGRESS NOTES, LAB, RADIOLOGY, REFERRAL, and EHI EXPORT. Insurance fields (PRIMARY INSURANCE, SECONDARY INSURANCE, INSURANCE NOTE) are also visible.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `EHI_Document.pdf` | 2.46 MB, 6 pages | Screenshot-based walkthrough of the export UI; created 2023-11-16 via Chrome print-to-PDF from `universalehr.com/PatientExport/EHIDocument/` | **Most informative** — sole substantive artifact; provides visual evidence of export format (NDJSON), file listing (12 resource types), and Documents subfolder |
| `exportdoc-aspx.html` | 878 bytes | ASP.NET wrapper page that embeds `EHI_Document.pdf` via iframe | Minimal — just the hosting page |
| `EHIDocument-page.html` | 16 KB | HTML source of the EHI documentation page; contains embedded images and a CMS textarea with the full page content; links to `/EMR/index2022.html` for EMR Direct information | Low — mirrors PDF content; the EMR Direct link confirms use of a third-party interoperability engine |

**No data dictionary, schema, sample data, or field-level documentation exists.** The entire export documentation consists of a 6-page PDF with annotated screenshots.

## 3. Export Mechanics

- **Format**: FHIR R4 NDJSON (Newline Delimited JSON), one file per resource type per patient, plus a `Documents/` subfolder with actual patient files (PDFs, images). All packaged as a ZIP file.
- **Mechanism**: Built-in UI within the EHR. Users navigate to the "EHI EXPORT" tab in the patient chart. Requires one of these roles: Admin, SystemAdmin, Ournurses, OurDoctor, or Lead.
- **Single-patient export**: Select patient → click "Start Export" → wait for processing → click "Download all files as a Zip file"
- **Bulk/multi-patient export**: Select multiple patients (or all) from a list → click "Start Export" → download ZIP. Each patient gets a folder named by Patient ID.
- **Access constraints**: Role-restricted to 5 specific roles. No mention of fees.
- **Infrastructure**: Uses EMR Direct Interoperability Engine as the authorization server (per the PDF header text and HTML link to `/EMR/index2022.html`).

## 4. Export Content: What's In It

### What we know from the artifacts

The export contains **12 FHIR R4 resource types** as NDJSON files, plus a **Documents/** subfolder with actual patient files. This is confirmed from the 7-Zip file listing screenshots visible on PDF pages 3-6.

**There is no data dictionary, no schema, and no field-level documentation.** The vendor provides zero information about what fields are populated in each resource type, what value sets are used, what extensions (if any) are applied, or what FHIR profiles the resources conform to. The only documentation is the screenshot walkthrough of how to use the export UI.

A `Readme.txt` file is included in each patient's export folder (visible in the file listing), but its contents are not shown in the documentation.

### Vendor's own content organization

The vendor does not organize the export into named categories. The export is simply a flat list of NDJSON files per patient folder. Based on the file listing visible in screenshots (PDF pages 3-4, 6):

| FHIR Resource Type | File Pattern | US Core? | Domain |
|---|---|---|---|
| Appointment | `Appointment_1.ndjson` | No | Scheduling |
| CareTeam | `CareTeam_1.ndjson` | Yes | Care coordination |
| Condition | `Condition_1.ndjson` | Yes | Problems/diagnoses |
| DocumentReference | `DocumentReference_1.ndjson` | Yes | Document metadata |
| Encounter | `Encounter_1.ndjson` | Yes | Visits |
| Invoice | `Invoice_1.ndjson` | No | Billing |
| MedicationRequest | `MedicationRequest_1.ndjson` | Yes | Medications |
| Observation | `Observation_1.ndjson` | Yes | Vitals/labs/results |
| Organization | `Organization_1.ndjson` | Yes | Organization info |
| Patient | `Patient_1.ndjson` | Yes | Demographics |
| Practitioner | `Practitioner_1.ndjson` | Yes | Provider info |
| Provenance | `Provenance_1.ndjson` | Yes | Data provenance |
| *(Documents/ subfolder)* | Various PDFs/images | N/A | Patient documents |

The full inventory is saved to `analysis/full-entity-inventory.json`.

### Notable observations

- **10 of 12 resource types are standard US Core resources**, closely mirroring what a (g)(10) FHIR API would serve.
- **Invoice and Appointment are NOT US Core resources** — their inclusion suggests the vendor made some effort to extend beyond the standard (g)(10) clinical data API. Invoice in particular is a billing-related resource, which is notable.
- **Documents/ subfolder** includes actual patient files (PDFs, images) — visible on page 6 with filenames like breast screening mammograms, lab results, CXR results, BCBS provider documents, and referral letters. File sizes range from ~4.9 KB to ~313 KB, with dates spanning 2016-2023.
- **Missing common resource types**: AllergyIntolerance, Immunization, Procedure, DiagnosticReport, CarePlan, Goal, Coverage, Claim — all absent from the visible file listing.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no explicit categorization of the export content. The export is a flat set of 12 FHIR R4 NDJSON resource types plus patient documents. It covers:

- **Core clinical data** (7 resource types): Patient demographics, conditions/diagnoses, medications, observations (vitals/labs), encounters, care teams, document references
- **Billing signal** (1 resource type): Invoice — presence is noteworthy but without field documentation it's unclear how much billing detail this captures versus a minimal representation
- **Scheduling** (1 resource type): Appointment
- **Contextual/support** (3 resource types): Organization, Practitioner, Provenance
- **Actual documents** (Documents/ subfolder): Patient files including lab reports, imaging reports, referral letters, insurance documents

The export is thin relative to what the product stores. The product UI shows tabs for SUPER BILL, PROGRESS NOTES, LAB, RADIOLOGY, and REFERRAL — each implying structured data storage that may not be fully captured in the 12 generic FHIR resource types.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient_1.ndjson` | Standard FHIR Patient resource; likely adequate for basic demographics |
| Encounters / visits | ✅ Covered | `Encounter_1.ndjson` | Standard FHIR Encounter; depth unknown without field documentation |
| Problems / conditions / diagnoses | ✅ Covered | `Condition_1.ndjson` | Standard FHIR Condition resource |
| Medications / prescriptions | ✅ Covered | `MedicationRequest_1.ndjson` | NDJSON content partially visible on PDF page 3 (MedicationRequest JSON); appears to include standard fields |
| Allergies | ❌ Not covered | No AllergyIntolerance resource in export | Product likely stores allergy data (certified for (a)(1) CPOE which requires allergy checking); significant gap |
| Immunizations | ❌ Not covered | No Immunization resource in export | Product is certified for (f)(1) immunization registry reporting, confirming it stores immunization data; significant gap |
| Vitals | ⚠️ Partial | `Observation_1.ndjson` may include vitals | Observation is used for vitals in US Core, but without documentation it's unclear if vitals are included |
| Lab results | ⚠️ Partial | `Observation_1.ndjson` may include labs; actual lab PDFs in Documents/ | Product has dedicated LAB tab; structured lab data may be in Observation but no DiagnosticReport resource exists; actual lab documents are included as PDFs |
| Imaging / diagnostic reports | ⚠️ Partial | No DiagnosticReport resource; imaging documents present in Documents/ subfolder | Product has RADIOLOGY tab; structured radiology data not captured in a dedicated resource, but imaging documents (CXR results, mammograms) are included as files |
| Procedures | ❌ Not covered | No Procedure resource in export | Product likely stores procedure data (certified for (a)(14) implantable device list which relates to procedures); gap |
| Clinical notes / documents | ⚠️ Partial | `DocumentReference_1.ndjson` + Documents/ subfolder with actual files | Product has PROGRESS NOTES tab implying structured note data; export includes document references and actual document files but unclear if structured note content is captured in the FHIR resources |
| Care plans / goals | ⚠️ Partial | `CareTeam_1.ndjson` present; no CarePlan or Goal resources | CareTeam is included but CarePlan and Goal are missing; partial at best |
| Orders / referrals | ⚠️ Partial | No ServiceRequest resource; referral documents present in Documents/ | Product has REFERRAL tab; referral letters exported as documents but structured referral data not captured as FHIR resources |
| Insurance / coverage | ❌ Not covered | No Coverage resource; no InsurancePlan resource | Product stores insurance data (PRIMARY INSURANCE / SECONDARY INSURANCE visible on patient chart); significant gap |
| Claims / billing | ⚠️ Partial | `Invoice_1.ndjson` present | Product has SUPER BILL tab and claims/billing functionality; Invoice resource is a billing signal but likely captures only a fraction of superbill/claims data. No Claim, ExplanationOfBenefit, or ChargeItem resources |
| Payments | ❌ Not covered | No PaymentReconciliation or similar resource | Product handles collections; gap if payment data is stored |
| Consents / directives | ❌ Not covered | No Consent resource | Gap only if product stores advance directives |
| Patient communications / portal messages | ❌ Not covered | No Communication resource | Product has "Doctor Direct" messaging and patient portal; significant gap |
| Specialty-specific data | ❌ Not covered | No evidence of specialty-specific resources or extensions | Product has customizable specialty templates (OB/GYN, cardiology, pediatrics, etc.); significant gap — specialty template data almost certainly not captured in generic FHIR resources |

**Summary**: 4 domains fully covered, 6 partially covered, 7 not covered. Several gaps align with data the product demonstrably stores (allergies, immunizations, insurance, messaging, specialty templates).

## 6. Documentation Quality

The export documentation quality is **extremely poor**:

- **No data dictionary exists.** Zero field-level documentation for any of the 12 resource types.
- **No schema or profile documentation.** No information about what FHIR profiles the resources conform to, what extensions are used, or what value sets are applied.
- **No sample data.** The PDF shows a blurred/redacted MedicationRequest JSON snippet on page 3, but no usable sample data is provided.
- **No machine-readable artifacts.** No JSON schemas, no CapabilityStatement, no StructureDefinitions, no sample NDJSON files.
- **The entire documentation is a 6-page screenshot walkthrough** showing how to click through the export UI. It tells users *how to click buttons* but provides zero information about *what data comes out*.
- **A developer could not build an import** from this documentation. The only information available is the list of 12 FHIR resource type names visible in file listings in the screenshots. A developer would need to reverse-engineer the export format from actual exported data.
- **The Readme.txt** included in each patient folder might contain useful information, but its contents are not shown in the documentation.

The documentation references EMR Direct Interoperability Engine as the authorization server, linking to `/EMR/index2022.html`. This suggests the export may leverage EMR Direct's standard FHIR R4 US Core 3.1.1 API infrastructure, but this is not explicitly stated in the (b)(10) documentation.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is a FHIR R4 NDJSON output with 12 resource types, 10 of which are standard US Core resources. This closely mirrors what a (g)(10) Standardized API would produce, extended with Invoice and Appointment resources and supplemented with a Documents/ subfolder. There is no evidence of native database model exposure — no custom tables, no vendor-specific schemas, no raw data model. The export is a projection of the vendor's data into standard FHIR resources, with significant data loss relative to what the product stores.

### Key Findings

1. **The export is essentially a (g)(10) FHIR API repackaged as (b)(10)**, with two notable additions: Invoice (billing signal) and Appointment (scheduling). The 10 other resource types are standard US Core. The Documents/ subfolder with actual patient files is a genuine (b)(10) extension. (Source: 7-Zip file listings on PDF pages 3-6)

2. **Zero field-level documentation exists.** The entire "documentation" is a 6-page screenshot walkthrough of the export UI. No data dictionary, no schema, no sample data, no field descriptions. A developer cannot understand or import the exported data from this documentation alone. (Source: `EHI_Document.pdf`, all 6 pages reviewed)

3. **Significant data domains are missing from the export** relative to what the product stores: allergies, immunizations, insurance/coverage, procedures, patient portal messages, and specialty template data. The product's UI confirms it stores superbill, progress notes, lab, radiology, referral, and insurance data — much of which is not represented in the 12 FHIR resource types. (Source: Product UI tabs visible on PDF page 1; product-research.md)

4. **The Invoice resource is a positive signal** — most (g)(10) repackaging efforts don't include any billing data at all. However, without documentation, it's impossible to assess whether Invoice captures meaningful billing detail or is a minimal stub. (Source: `Invoice_1.ndjson` visible in file listing, PDF page 4)

5. **The Documents/ subfolder is genuinely useful** — it includes actual patient documents (lab reports, mammograms, CXR results, referral letters, insurance documents) as PDFs spanning 2016-2023. This is real patient data that goes beyond what FHIR resources capture. (Source: Detailed file listing on PDF page 6)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR R4 NDJSON + patient document files (ZIP)
Model type:      Standard projection (FHIR R4, mostly US Core)
Entities:        12 FHIR resource types + Documents subfolder
Fields:          N/A (zero field-level documentation)
Descriptions:    N/A (no data dictionary)
Sample data:     No
Bulk export:     Yes (multi-patient export supported via UI)
Domains covered: 4 of 17 applicable domains fully; 6 partially
```

### Bottom Line

Universal EHR's (b)(10) export is a FHIR R4 NDJSON output that closely mirrors its (g)(10) API, extended with Invoice and Appointment resources and supplemented with actual patient document files. While the Documents/ subfolder and Invoice resource show some effort beyond pure (g)(10) repackaging, the export lacks coverage of several data domains the product demonstrably stores (allergies, immunizations, insurance, specialty templates, messaging) and provides absolutely no documentation — no data dictionary, no schema, no sample data. A patient or provider would get a partial copy of their clinical data plus their documents, but would miss billing detail, specialty-specific assessments, and several standard clinical data categories.

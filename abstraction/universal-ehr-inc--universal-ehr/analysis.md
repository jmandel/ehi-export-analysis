# EHI Export Analysis: Universal EHR, Inc.

**Product**: Universal EHR (Physician's Solution) v2.0.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2478.Univ.02.00.1.180312 (CHPL ID 9333)

## 1. Product Context

Universal EHR (also branded as Physician's Solution) is a browser-based, integrated EHR and practice management system targeting ambulatory/outpatient practices. It is developed by Universal EHR, Inc., a very small company (~3–11 employees) based in Garden Grove, CA, with a customer base concentrated among Vietnamese-American medical practices in Southern California (primary customer: DAO Medical Group, a 30+ physician multi-specialty group).

The product is certified as a Complete EHR (35+ ONC criteria) and includes:

- **Clinical/EHR**: Patient charting, clinical documentation, customizable specialty templates (OB/GYN, cardiology, pediatrics, internal medicine, and others), prescription ordering (e-prescribing), lab orders/results, diagnostic device interfacing (EKG), image management, messaging
- **Practice Management**: Appointment scheduling, claims/billing processing, charge capture, collections, superbill generation, reporting
- **Patient Engagement**: Patient portal ("Patient Direct"), physician-patient communication ("Doctor Direct"), provider messaging ("Physician's Portal")
- **Interoperability**: HL7/XML bidirectional interfaces, FHIR API (g)(10), hospital/lab/radiology interfaces

This means a genuine (b)(10) export should cover: clinical records, prescriptions, lab results, diagnostic images, billing/claims/charges/superbills, scheduling, patient-provider messaging, specialty-specific template data, and patient documents.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI_Document.pdf` (2.4 MB, 6 pages) | Print-to-PDF of internal documentation page. Screenshot-based walkthrough of the EHI export UI. Created 2023-11-16 via Chrome Print. Shows export UI, NDJSON file listing, and patient document folder. | **Primary artifact** — only source of export content information |
| `downloads/exportdoc-aspx.html` (878 bytes) | The registered CHPL URL. Minimal ASP.NET page that embeds EHI_Document.pdf via iframe. | Wrapper only — no content |
| `downloads/EHIDocument-page.html` (16 KB) | HTML source of the page that was printed to create the PDF. Contains same content as PDF plus embedded image URLs. | Confirms PDF content; reveals image source URLs |

**No data dictionary, schema, sample data, or field-level documentation exists.** The entire (b)(10) documentation consists of a single 6-page screenshot walkthrough.

## 3. Export Mechanics

- **Format**: FHIR R4 NDJSON files plus a Documents subfolder containing patient clinical documents (PDFs, images)
- **Mechanism**: UI-based. Users log in, click "EHI EXPORT" link, select patients via checkboxes, click "Start Export," then download a ZIP file
- **Single-patient and bulk capability**: Both supported. The UI allows selecting individual patients or "all patients" with checkbox selection. A date/time filter ("Filter by Modification Date/Time") allows filtering to records modified after a specified date
- **Access constraints**: Export is available to users in roles: Admin, SystemAdmin, Ournurses, OurDoctor, or Lead
- **Fees**: Not documented in export documentation; no mention of cost
- **Authorization**: References EMR Direct Interoperability Engine as the authorization server (this is the vendor's (g)(10) FHIR infrastructure)

## 4. Export Content: What's In It

### No Data Dictionary

There is **no data dictionary, no schema, no field-level documentation, and no sample data** provided. The only evidence of what the export contains comes from screenshots in the PDF showing:

1. A 7-Zip window listing NDJSON files in a patient export folder (PDF page 4/6)
2. A Notepad++ window showing MedicationRequest NDJSON content (PDF page 3)
3. A 7-Zip window showing the Documents subfolder with patient clinical documents (PDF page 6)
4. File size information for each NDJSON file (PDF page 6)

### FHIR Resource Types in Export

From the 7-Zip screenshots (pages 4 and 6), the export contains 13 FHIR resource types as NDJSON files:

| Resource Type | Filename | File Size | US Core? | Notes |
|---|---|---|---|---|
| Provenance | Provenance_1.ndjson | 1,204,004 bytes | Yes | Largest file; audit/tracking |
| Practitioner | Practitioner_1.ndjson | 4,100 bytes | Yes | Provider reference data |
| Patient | Patient_1.ndjson | 31,379 bytes | Yes | Demographics |
| Organization | Organization_1.ndjson | 330 bytes | Yes | Organization reference data |
| Observation | Observation_1.ndjson | 675,261 bytes | Yes | Vitals, labs, social history |
| MedicationRequest | MedicationRequest_1.ndjson | 77,098 bytes | Yes | Prescriptions/medication orders |
| Invoice | Invoice_1.ndjson | 232,177 bytes | **No** | Billing data — goes beyond US Core |
| Encounter | Encounter_1.ndjson | 54,648 bytes | Yes | Visit records |
| DocumentReference | DocumentReference_1.ndjson | 163,680 bytes | Yes | References to documents |
| Device | Device_1.ndjson | unknown | Yes | Medical devices |
| Condition | Condition_1.ndjson | 16,663 bytes | Yes | Problems/diagnoses |
| CareTeam | CareTeam_1.ndjson | 31,180 bytes | Yes | Care team members |
| Appointment | Appointment_1.ndjson | 58,905 bytes | **No** | Scheduling — goes beyond US Core |

Additionally, a `Readme.txt` (35 bytes) links to `https://build.fhir.org/nd-json.html`.

### Patient Documents

The Documents subfolder (visible on page 6) contains actual clinical document files. 21+ document files are visible in the screenshot for a single patient, including:

- **Imaging results**: Breast ultrasound PDFs, bilateral screening mammogram PDFs, chest X-ray results
- **Lab reports**: Urinalysis (UA) dipstick results, urinalysis results
- **Clinical records**: OCM (Office Clinical Management) records
- **Referral/insurance documents**: BCBS OB/GYN provider referrals, BCBS GI provider referrals
- **HL7 documents**: Several files with "hl7" in the filename (likely CDA/clinical document exchanges)
- **Other clinical documents**: Multiple "Viewed.pdf" files from various dates (2016–2023)

Document file sizes range from ~5 KB to ~313 KB, with dates spanning 2016–2023.

### MedicationRequest Sample (from screenshot)

The Notepad++ screenshot on page 3 shows ~26 lines of MedicationRequest NDJSON. Visible fields include: `resourceType`, `id`, `status` ("stopped"), `intent` ("order"), `reportedBoolean` (false), `medicationCodeableConcept` with `coding`. This appears to be standard FHIR MedicationRequest structure with no visible vendor-specific extensions.

### Vendor's Own Content Organization

The vendor does not organize its export into categories. There is no data dictionary or content categorization. The export is simply a flat list of NDJSON files plus a Documents folder. The vendor's documentation describes it only as "Data is exported in ndjson format (newline delimited JSON)."

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no content categorization. Based solely on the FHIR resource types visible in screenshots:

- **Clinical data (11 US Core resources)**: The export includes standard FHIR resources for demographics (Patient), conditions (Condition), medications (MedicationRequest), observations (Observation — likely vitals, labs), encounters (Encounter), care teams (CareTeam), clinical documents (DocumentReference), devices (Device), practitioners (Practitioner), organizations (Organization), and provenance (Provenance).
- **Billing (1 non-US-Core resource)**: The presence of `Invoice_1.ndjson` (232 KB) is the single most interesting signal. Invoice is not a US Core resource and indicates some attempt to export billing data. However, without any field documentation, it's impossible to know what billing fields are captured — whether this includes charges, line items, insurance references, CPT codes, payment status, etc.
- **Scheduling (1 non-US-Core resource)**: `Appointment_1.ndjson` (59 KB) captures scheduling data, which is also outside US Core.
- **Patient documents**: The Documents subfolder is a genuine strength, containing actual clinical documents (imaging results, lab reports, referrals) as PDF files — not just metadata references.

**Thinnest areas**: No documentation exists for any resource's field-level content. The Observation resource (675 KB, likely the second-largest data file) could contain vitals, labs, social history, or all three — there's no way to tell from the documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient_1.ndjson` (31 KB) present | Resource exists but no field documentation; can't assess depth |
| Encounters / visits | ⚠️ Partial | `Encounter_1.ndjson` (55 KB) present | Resource exists; no field documentation |
| Problems / conditions | ⚠️ Partial | `Condition_1.ndjson` (17 KB) present | Resource exists; no field documentation |
| Medications / prescriptions | ⚠️ Partial | `MedicationRequest_1.ndjson` (77 KB) present | Resource exists; screenshot shows standard fields. E-prescribing workflow details (pharmacy, refill history) unknown |
| Allergies | ❌ Not covered | No AllergyIntolerance resource in export | Product likely stores allergies; significant gap |
| Immunizations | ❌ Not covered | No Immunization resource in export | Product is certified for immunization reporting (f)(1); gap |
| Vitals | ⚠️ Partial | Likely within `Observation_1.ndjson` | Cannot distinguish vitals from other Observation types |
| Lab results | ⚠️ Partial | Likely within `Observation_1.ndjson`; lab PDFs in Documents folder | Lab PDFs present as documents; structured lab data may be in Observation |
| Imaging / diagnostic reports | ⚠️ Partial | Imaging PDFs in Documents folder (mammograms, CXR, breast US) | Actual imaging reports present as PDFs; no DiagnosticReport FHIR resource |
| Procedures | ❌ Not covered | No Procedure resource in export | Gap if product stores procedure records |
| Clinical notes / documents | ✅ Covered | `DocumentReference_1.ndjson` (164 KB) + Documents folder with 21+ PDFs | Best-covered domain; actual document files included |
| Care plans / goals | ⚠️ Partial | `CareTeam_1.ndjson` (31 KB) present; no CarePlan or Goal | CareTeam present but no care plan or goal resources |
| Orders / referrals | ⚠️ Partial | Referral PDFs visible in Documents folder (BCBS referrals) | Referral documents present as PDFs; no ServiceRequest resource |
| Insurance / coverage | ❌ Not covered | No Coverage resource in export | Product handles insurance/billing; gap |
| Claims / billing | ⚠️ Partial | `Invoice_1.ndjson` (232 KB) present | Invoice resource is a positive signal but completely undocumented. Product handles claims, billing, superbills, charge capture, collections — unclear if Invoice captures all of this |
| Payments | ❌ Not covered | No payment-specific resource visible | Product handles collections; likely gap |
| Patient communications | ❌ Not covered | No Communication resource in export | Product has Doctor Direct (patient messaging) and Physician's Portal; gap |
| Specialty-specific data | ❌ Not covered | No evidence of specialty template data | Product has customizable templates for OB/GYN, cardiology, pediatrics, internal medicine, and 12+ other specialties. Standard FHIR resources cannot capture this structured specialty data. Significant gap |
| Consents / directives | ❌ Not covered | No Consent resource in export | N/A — unclear if product stores advance directives |

**Summary**: Of 19 assessed domains, 1 is covered (clinical documents), 9 are partially covered (resource exists but no field documentation), and 9 are not covered. Several of the gaps (allergies, immunizations, patient communications, specialty templates) correspond to known product capabilities.

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the thinnest possible for a certified product:

- **No data dictionary**: Zero field-level documentation for any of the 13 FHIR resource types
- **No schema**: No JSON Schema, OpenAPI spec, FHIR StructureDefinition, or ImplementationGuide
- **No sample data**: The only data visible is a redacted Notepad++ screenshot showing ~26 lines of MedicationRequest NDJSON
- **No value sets or code systems**: No documentation of what codes or terminologies are used
- **No relationships documented**: No explanation of how FHIR references link resources
- **No mapping documentation**: No description of how the EHR's internal data model maps to FHIR resources
- **No explanation of Invoice or Appointment content**: The two non-US-Core resources that could distinguish this from a (g)(10) repackage are completely undocumented
- **Format**: A 6-page Chrome Print-to-PDF of annotated screenshots showing the UI workflow. Created 2023-11-16 and never updated
- **References**: Links to EMR Direct's (g)(10) API documentation and the generic FHIR NDJSON spec — no product-specific technical documentation

**Could a developer build an import from this documentation?** No. A developer would need to actually request an export and reverse-engineer the NDJSON content. The documentation answers only "how do I click the export button," not "what data will I receive."

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export includes 13 FHIR resource types — 11 US Core resources plus Invoice and Appointment. The Invoice resource is a genuine signal that the vendor went somewhat beyond USCDI clinical data to include billing information, and the Appointment resource adds scheduling data. The Documents subfolder with actual patient clinical documents (imaging reports, lab results, referrals) is a real strength that goes beyond what typical (g)(10) exports provide.

However, significant gaps exist relative to known product capabilities: allergies and immunizations are absent despite being standard clinical data that the product stores and is certified to report. Patient communications (a key product feature via Doctor Direct and Physician's Portal) are missing. Specialty-specific template data — a significant differentiator for this product with 12+ specialty templates — has no export path via standard FHIR resources. Insurance/coverage data is absent despite the product handling billing. The complete absence of field-level documentation means that even for the resources present, we cannot assess whether they contain the full depth of what the EHR stores or just a USCDI-minimum projection.

**Axis 2 — Export approach: Purpose-built EHI export (minimal)**

This is not a pure (g)(10) repackage. The evidence: (1) Invoice_1.ndjson is not a US Core resource and not part of (g)(10) — it was specifically added for billing data; (2) Appointment_1.ndjson is also not in US Core; (3) the Documents subfolder exports actual patient document files alongside FHIR resources, which is not part of the standard FHIR Bulk Data flow; (4) the export has its own dedicated UI ("EHI EXPORT" link) rather than pointing users to the FHIR API.

However, the "purpose-built" effort was minimal. The vendor built a separate export mechanism, but the documentation suggests very little effort was put into mapping the EHR's full internal data model to FHIR. The MedicationRequest sample shows standard FHIR fields with no vendor extensions. Nine US Core resources that EMR Direct supports (AllergyIntolerance, CarePlan, DiagnosticReport, Goal, Immunization, Location, Medication, PractitionerRole, Procedure) are absent from the export, suggesting the vendor didn't even include all available (g)(10) resources. The export appears to be a subset of the EHR's FHIR capability augmented with Invoice, Appointment, and a document dump.

### Key Findings

1. **Invoice resource is the distinguishing signal**: The presence of `Invoice_1.ndjson` (232 KB — a substantial file) is the clearest evidence this goes beyond (g)(10). But it is completely undocumented, making it impossible to assess billing coverage depth.

2. **Patient document export is genuinely useful**: The Documents subfolder contains actual clinical documents (mammograms, X-rays, lab reports, referrals, OCM records) as PDFs spanning 2016–2023. This is more comprehensive than many vendors' document handling.

3. **Zero field-level documentation**: No data dictionary, schema, value sets, or sample data exist. This is among the thinnest documentation encountered for a certified product. The entire (b)(10) documentation is a 6-page screenshot walkthrough.

4. **Missing standard resources**: AllergyIntolerance and Immunization — core clinical data the product stores and is certified to report — are absent from the export, suggesting incomplete resource coverage even within USCDI domains.

5. **Specialty template data is unaddressed**: The product's customizable specialty templates (12+ specialties) represent significant patient-specific clinical data with no export path via standard FHIR resources and no documentation of how (or whether) this data is captured.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export (minimal)
Export format:   FHIR R4 NDJSON + patient document files (PDF/image)
Entities:        13 FHIR resource types
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No (only redacted screenshots)
Bulk export:     Yes (multi-patient selection via UI)
Domains covered: 10 of 19 applicable domains (1 fully, 9 partially)
```

### Bottom Line

Universal EHR built a dedicated EHI export that goes modestly beyond its (g)(10) FHIR API by adding Invoice, Appointment, and patient document files — but the effort was minimal. The complete absence of field-level documentation makes it impossible to assess the depth of any exported resource, and the omission of standard clinical data (allergies, immunizations) alongside specialty template data and patient communications represents real gaps. A patient receiving this export would get structured clinical data and their actual documents, but would have no documentation to understand what's in the structured data, and would likely be missing billing details, messaging history, and specialty-specific clinical assessments.

# EHI Export Analysis: MaxRemind Inc

**Product**: Maximus 1.0  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.05.05.3173.MAXR.01.00.1.231031 (CHPL #11360)

## 1. Product Context

Maximus EHR is a cloud-based, ONC-certified electronic health record system from MaxRemind Inc, a small Texas-based company (est. ~25–200 employees) whose core business is medical billing and revenue cycle management (RCM). The product was certified in October 2023 and is marketed as an "all-in-one" platform for 75+ specialties.

**Key data domains the product should store (based on vendor marketing and certified criteria):**

- **Clinical documentation**: Charting, progress notes, voice recognition, smart templates for 75+ specialties
- **Scheduling & practice management**: Appointments, registration, follow-up workflows, multi-location
- **Billing & revenue cycle**: Claims, billing records, charges, payments, coding (this is MaxRemind's core business; also offered via standalone MaxCoder and Provider Portal products)
- **E-prescribing**: Medication prescribing
- **Lab & referral management**: Lab integration, referrals
- **Patient engagement**: Patient portal with secure messaging, appointment reminders
- **Care coordination**: Transitions of care (C-CDA), Direct messaging
- **Remote patient monitoring**: MaxRPM companion product (blood pressure, weight, pulse, glucose)
- **Public health reporting**: Immunization registries, syndromic surveillance, electronic case reporting

The vendor's core competency is billing/RCM, making the absence of billing data from the EHI export particularly notable.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/B10-Electronic-Health-information-Export.pdf` | 4-page PDF (254 KB) describing 6 export components. Created 2023-10-03 by Nouman Zafar in Microsoft Word. No data dictionary, no field definitions, no schemas. | **Primary source** — but extremely thin |
| `downloads/screenshot-fhir-docs-portal.png` | Screenshot of `documents.maximus.care` — a React SPA documenting the (g)(10) FHIR API with OAuth2 auth flow, FHIR base URL, and standard US Core STU3.1.1 resources | Confirms FHIR component is standard (g)(10) |
| `downloads/screenshot-certification-page-full.png` | Full screenshot of the ONC certification page at `maxremind.com/maximusehr-certification/` showing all criteria, documentation links, third-party software (NewCrop 2.0, MaxMD 3.0), and costs section | Confirms no additional EHI-specific docs exist |
| `downloads/screenshot-certification-page.png` | Cropped screenshot of the certification page documentation section | Redundant with full screenshot |

**Most informative**: The B10 PDF and FHIR docs portal screenshot together constitute the entirety of the export documentation. **Least informative**: The certification page screenshots mainly confirm that no additional documentation exists beyond what was already found.

## 3. Export Mechanics

- **Format**: Hybrid — C-CDA XML, FHIR R4 (via Bulk Data API), Excel spreadsheets, and native document files (PDF/JPG/PNG)
- **Mechanism**: The PDF states the system "allows a user to export electronic health information (EHI) for a single patient at any time without developer assistance." No screenshots or step-by-step instructions are provided for how to initiate the export.
- **Single-patient**: Supported ("using the below mentioned file format")
- **Bulk/multi-patient**: Supported ("Maximus can export all the data for a patient population in our standardized format")
- **Access constraints**: No fees or special access requirements mentioned. The certification page's "Costs" section describes a general subscription model but does not mention EHI export fees.

## 4. Export Content: What's In It

### No data dictionary exists

The entire EHI export documentation is a 4-page PDF with **zero field-level definitions**. There is no data dictionary, no schema, no column headers, no sample data, and no machine-readable artifact of any kind. Each export component gets at most one sentence of description.

### Vendor's own content organization

The PDF describes 5 export components (the 6th item — single vs. multi-patient — is a capability description, not a separate component):

| Export Component | Format | Description (verbatim from PDF) | Fields Documented | Category |
|---|---|---|---|---|
| CCD/C-CDA Documents | HL7 C-CDA XML R2.1 | "Bulk export of HL7 CCDA xml files which comply to USCDI v1 requirements" | 0 | Clinical Exchange Standard |
| FHIR Bulk Data Access | FHIR R4 / US Core 3.1.1 | "HL7 FHIR R4, FHIR US Core STU V3.1.1, HL7 FHIR Bulk Data export" | 0 | Clinical Exchange Standard |
| Patient Demographics & Insurance | Excel | "Comprehensive view of demographics and insurance details" | 0 | Proprietary Export |
| Appointments | Excel | "Comprehensive view of all future appointment details" | 0 | Proprietary Export |
| Documents | PDF, JPG, PNG | "Signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document" | 0 | Proprietary Export |

**Total entities with field-level documentation: 0 of 5**  
**Total fields documented: 0**

### FHIR Resources (via (g)(10) API)

The FHIR documentation portal at `documents.maximus.care` documents 18 standard US Core STU3.1.1 resource types:

AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, MedicationRequest, Observation, Organization, Patient, Practitioner, Procedure, Provenance

These are the standard (g)(10) USCDI resource types. No custom FHIR profiles, extensions, or vendor-specific mappings are documented. The B10 PDF explicitly references "170.315(g)(10) SmartOnFHIR API Documentation" — confirming this is the existing (g)(10) API being cited as part of the (b)(10) export.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export has two tiers:

1. **Standard clinical exchange (C-CDA + FHIR)**: Covers the USCDI v1 clinical data set through two parallel mechanisms — C-CDA XML and FHIR US Core 3.1.1. This is identical to the vendor's existing (g)(10) interoperability surface. 18 FHIR resource types are listed, all standard US Core. No depth beyond what the standard mandates.

2. **Three proprietary supplements**: Demographics/insurance in Excel (one sentence of documentation), appointments in Excel (one sentence; future appointments only), and document files organized by patient folder. These are the only components that go beyond the existing (g)(10) scope — but they have zero field-level documentation.

The proprietary supplements suggest some awareness that (b)(10) should cover more than USCDI, but the execution is minimal. The demographics/insurance Excel is the only component that might export data not already in the FHIR Patient resource. The appointment Excel only covers "future" appointments, explicitly omitting historical visit data. The document export is a reasonable addition but lacks any metadata schema.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR Patient resource + "Demographics & Insurance" Excel (no field detail) | Likely covered between FHIR and Excel, but Excel contents are undocumented |
| Encounters / visits | ⚠️ Partial | FHIR Encounter resource; Appointments Excel covers "future" only | Historical encounter data only via FHIR Encounter (USCDI scope). Past appointment details may be missing |
| Problems / conditions | ⚠️ Partial | FHIR Condition resource (US Core) | Standard USCDI scope only; no evidence of depth beyond US Core Must Support fields |
| Medications / prescriptions | ⚠️ Partial | FHIR MedicationRequest (US Core) | E-prescribing is a product feature; no prescription transmission history or MAR documented |
| Allergies | ⚠️ Partial | FHIR AllergyIntolerance (US Core) | Standard USCDI scope only |
| Immunizations | ⚠️ Partial | FHIR Immunization (US Core) | Standard USCDI scope only |
| Vitals | ⚠️ Partial | FHIR Observation (US Core) | Standard USCDI scope only |
| Lab results | ⚠️ Partial | FHIR Observation, DiagnosticReport (US Core); document file export may include lab reports | Standard USCDI scope; scanned lab results may appear in document export |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport (US Core); document export includes "radiology reports" | Narrative reports via document export; structured data limited to US Core |
| Procedures | ⚠️ Partial | FHIR Procedure (US Core) | Standard USCDI scope only |
| Clinical notes / documents | ✅ Covered | FHIR DocumentReference + document file export (signed progress notes, lab results, radiology, scanned documents) | Best-covered domain — both structured reference and raw files |
| Care plans / goals | ⚠️ Partial | FHIR CarePlan, Goal (US Core) | Standard USCDI scope only |
| Orders / referrals | ❌ Not covered | No order or referral entities beyond what's in MedicationRequest | Product supports CPOE (a)(1)–(a)(3) and referral management; not in export |
| Insurance / coverage | ⚠️ Partial | "Demographics & Insurance" Excel (no field detail) | Excel may contain insurance info but contents are completely undocumented |
| Claims / billing | ❌ Not covered | No billing entities in export | **Critical gap** — MaxRemind's core business is billing/RCM. Product stores claims, charges, payments. None are in the export |
| Payments | ❌ Not covered | No payment entities in export | Product processes payments; not exported |
| Consents / directives | ❌ Not covered | No consent entities documented | No evidence of advance directive export |
| Patient communications | ❌ Not covered | No portal messages or communication data | Product has patient portal with secure messaging; not exported |
| Specialty-specific data | ❌ Not covered | No specialty-specific entities | Product claims 75+ specialties with custom templates; none appear in export |

### Summary

- **Domains with some coverage**: 12 of 19 applicable domains
- **Domains with genuine depth**: 1 (clinical notes/documents)
- **Domains at USCDI-only depth**: 11 (everything via FHIR/C-CDA)
- **Domains completely absent**: 7 (orders/referrals, claims/billing, payments, consents, patient communications, specialty-specific data)
- **Biggest gap**: Billing and claims data — this is MaxRemind's core business, the product stores it, and it's entirely absent from the export

## 6. Documentation Quality

**Very poor.** The documentation fails on every dimension:

- **Field-level detail**: None. Zero fields are defined for any export component.
- **Data types**: Not documented (inherited from C-CDA/FHIR standards for those components; completely absent for Excel exports).
- **Value sets / code systems**: Not documented.
- **Relationships / foreign keys**: Not documented. No explanation of how the Excel demographics relate to FHIR Patient records, or how documents link to encounters.
- **Sample data**: None provided.
- **Machine-readable schemas**: None. No XSD, JSON schema, or Excel template.
- **Export procedure**: No screenshots, no step-by-step instructions, no UI documentation.

**Could a developer build an import from this documentation?** For the C-CDA and FHIR components: yes, using standard parsers (since there's nothing product-specific). For the Excel exports: no — a developer would have to reverse-engineer the column structure from an actual export file. For the document files: partially — the folder structure is described but there's no metadata manifest.

The 4-page PDF reads more like a compliance checklist item than technical documentation. It was created in Microsoft Word on 2023-10-03 — just weeks before the certification date of 2023-10-31 — suggesting it was produced for certification rather than as a genuine developer resource.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export is essentially the vendor's existing (g)(10) clinical exchange surface (C-CDA + FHIR US Core) with three minimally-documented additions: a demographics/insurance Excel, a future-appointments Excel, and a document file dump. The B10 PDF explicitly references "(g)(10) SmartOnFHIR API Documentation" for the FHIR component, confirming the reuse. The three proprietary additions show some awareness that (b)(10) requires more than USCDI, but they are documented with single sentences and no field definitions. Major data domains the product stores — billing/claims (the vendor's core competency), orders, referrals, patient portal messages, specialty-specific data — are entirely absent. The documentation is too thin to assess whether even the Excel components contain meaningful data.

**Axis 2 — Export approach: Repackaged existing export**

The core of the export is the existing (g)(10) FHIR API and C-CDA output relabeled as (b)(10). The PDF says so explicitly by referencing "(g)(10) SmartOnFHIR API Documentation." The FHIR documentation portal at `documents.maximus.care` documents only standard US Core resources with no custom profiles or extensions. The three proprietary additions (two Excel files and a document dump) add marginally beyond (g)(10) scope but are too thin and undocumented to constitute a purpose-built EHI export. There is no evidence the vendor enumerated what their product stores and built an export to cover it.

### Key Findings

1. **The export is a repackaged (g)(10) API with minimal additions.** The B10 PDF explicitly references "(g)(10) SmartOnFHIR API Documentation" for the FHIR bulk data component. The FHIR docs portal documents only standard US Core STU3.1.1 resources with no custom profiles or extensions. The C-CDA component similarly references standard USCDI v1 specifications with no product-specific additions.

2. **Zero field-level documentation exists.** Across 4 pages, the PDF provides zero field definitions for any export component. The Excel exports ("demographics & insurance" and "appointments") get one sentence each. There is no data dictionary, no schema, no sample data, and no machine-readable artifact.

3. **Billing data is entirely absent despite being the vendor's core business.** MaxRemind's primary business is medical billing and RCM services. Maximus EHR stores claims, charges, payments, and billing records. None of this data appears in the export — a significant gap for a billing-focused vendor.

4. **The appointments export covers only future appointments.** The PDF specifies "all future appointment details" — explicitly excluding historical visit/appointment data, which is part of the patient record.

5. **The document file export is the most genuinely (b)(10) component**, covering signed progress notes, lab results, radiology reports, and scanned documents organized by patient chart. However, it lacks any metadata manifest or schema describing how documents are indexed.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML, FHIR R4, Excel, PDF/JPG/PNG
Entities:        5 export components (+ 18 standard FHIR resources)
Fields:          0 (no data dictionary)
Descriptions:    N/A (no fields documented)
Sample data:     No
Bulk export:     Yes
Domains covered: 12 of 19 applicable (but 11 at USCDI-only depth)
```

### Bottom Line

A patient or provider would receive C-CDA and FHIR documents (standard clinical summaries), two undocumented Excel files for demographics/insurance and future appointments, and a folder of scanned documents — but no billing data, no order history, no specialty-specific assessments, no portal messages, and no referral records. The biggest gap is the complete absence of billing and claims data from a vendor whose core business is medical billing. This is a compliance checkbox, not a genuine EHI export effort.

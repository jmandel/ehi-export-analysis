# EHI Export Analysis: Enable Healthcare Inc.

**Product**: MDnet V10  
**Analysis date**: 2026-02-15  
**CHPL IDs**: 15.04.04.2719.MDne.10.01.1.191231 (CHPL ID 10247)

## 1. Product Context

MDnet by Enable Healthcare Inc. is a cloud-based, ONC-certified EHR platform targeting ambulatory practices across multiple specialties (behavioral health, pediatrics, cardiology, internal medicine, urgent care, OBGYN). It is an integrated clinical, administrative, and financial system encompassing:

- **Clinical EHR**: encounter documentation, problem lists, medication lists, allergy tracking, immunizations, family health history, implantable devices, lab results, vitals, AI-powered charting ("Lumina"), clinical decision support
- **E-Prescribing**: electronic prescription transmission to pharmacies
- **Practice Management**: appointment scheduling, patient check-in, multi-physician calendar management
- **Medical Billing & RCM**: insurance eligibility verification, claim submission, denial management, branded "revQ" AI billing platform; Enable Healthcare also operates as a billing services company
- **Patient Portal**: secure messaging, appointment booking, medical record access, co-payment management
- **Telehealth**: integrated video visit capability
- **Care Coordination**: chronic care management (CCM), remote patient monitoring (RPM), population health, annual wellness visits
- **Document Management**: scanned paper records, fax management
- **Interoperability**: C-CDA exchange, Direct messaging, FHIR R4 API

This product stores data across clinical, financial, administrative, and patient engagement domains. A complete (b)(10) export should cover all of these.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `EHI_DATA_EXPort_GUIDE.pdf` | 9-page PDF (904 KB), "Data Interoperability & EHI Data Export Guide." Created 2023-12-28 by Rahul Dewan. Describes scope and 8 export methods. Pages 1–4 cover export methods; pages 5–9 describe an optional C-CDA incremental data exchange service. **Primary artifact.** | Medium — describes capabilities at a high level but provides no field-level documentation |
| `fhir-capability-statement.json` | FHIR R4 CapabilityStatement (25 KB) from `ehifire.ehiconnect.com`. Lists 27 resource types. Standard US Core set. | Low — this is the (g)(10) API, not a (b)(10) export mechanism |
| `fhir-portal-landing.png` | Screenshot of Enable Healthcare FHIR portal. Three cards: Testing Sandbox, Registration, Documentation. | Low — confirms FHIR portal exists |
| `fhir-api-documentation-page.png` | Screenshot of Dynamic FHIR API documentation page. Shows SMART on FHIR authorization, client registration, Bulk Export. Branded "Dynamic FHIR" (third-party platform by Dynamic Health IT). | Low — confirms (g)(10) API documentation; no (b)(10) content |

**Critical missing artifact**: The PDF references a CSV data dictionary at `https://emr.ehiconnect.com/docs/`. This URL returns HTTP 404 (verified 2026-02-15). No alternative URL was found. No Wayback Machine captures exist for this path. This data dictionary — the only artifact that would document the native data export — is inaccessible.

## 3. Export Mechanics

The PDF describes **8 export methods**, though not all are (b)(10) mechanisms:

| Method | Format | Type | Patient/Bulk | Mechanism |
|---|---|---|---|---|
| FHIR R4 API | FHIR JSON | Standard projection | Single + Bulk | API (portal at fhir.ehiconnect.com) |
| C-CDA R2.1 Export | C-CDA XML | Standard projection | Single + Bulk | UI ("CCDA Export Tracker" in MDnet) |
| CSV Full Data Set | CSV | Native data | Single + Bulk | Request from authorized users |
| HL7 2.x ADT | HL7 v2 | Real-time feed | Per-event | Interface engine |
| HL7 2.x SIU | HL7 v2 | Real-time feed | Per-event | Interface engine |
| HL7 2.x DFT | HL7 v2 | Real-time feed | Per-event | Interface engine |
| JSON Document Exchange | JSON + BASE-64 | Proprietary | Per-document | Real-time exchange |
| EDI 837P/835 | EDI X12 | Standard claims | Bulk | Continuous feed |

**Access constraints**: The PDF states exports are available to "authorized users" with "required access" granted. No mention of fees for the export itself, though the "Announce & Deliver" incremental C-CDA service is described as an "add-on additional service," implying a cost.

**Key observation**: The CSV export (method 3) is described as covering "health, activity and financial data" — this is the only method that could constitute a genuine (b)(10) all-EHI export. However, its data dictionary is inaccessible, so the actual content and completeness cannot be verified.

## 4. Export Content: What's In It

### 4.1 What can be verified

**C-CDA R2.1 Sections** (20 sections, per pages 6–7 of PDF):

| # | Section | Standard C-CDA? |
|---|---|---|
| 1 | Allergy | Yes |
| 2 | Assessment | Yes |
| 3 | Encounters | Yes |
| 4 | Family History | Yes |
| 5 | Functional Status | Yes |
| 6 | Cognitive Status | Yes |
| 7 | Immunizations | Yes |
| 8 | Medical Equipment | Yes |
| 9 | Medications | Yes |
| 10 | Lab Results | Yes |
| 11 | Problems | Yes |
| 12 | Procedures | Yes |
| 13 | Reason for Visit | Yes |
| 14 | Referrals | Yes |
| 15 | Social History | Yes |
| 16 | Vitals | Yes |
| 17 | Care Plan | Yes |
| 18 | Goal | Yes |
| 19 | Health Concern | Yes |
| 20 | Clinical Instructions | Yes |

All 20 sections are standard C-CDA R2.1 sections. No vendor-specific extensions are documented.

**FHIR R4 Resources** (27 types from CapabilityStatement):

AllergyIntolerance, Binary, CarePlan, CareTeam, ClinicalImpression, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Group, Immunization, Location, MedicationDispense, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance, RelatedPerson, ServiceRequest, Specimen

This is the standard US Core resource set — no vendor-specific resources or custom extensions.

**EDI Claims**: EDI 837P (professional claims) and 835 (remittance advice) are described as a "continuous feed." No field-level documentation is provided, but EDI 837P/835 formats are industry standards with defined structures.

### 4.2 What cannot be verified

**CSV Full Data Set Export**: The PDF claims this covers "health, activity and financial data" for single or all patients. The referenced data dictionary at `https://emr.ehiconnect.com/docs/` is inaccessible (HTTP 404). Without this data dictionary, the following are unknown:

- How many tables/entities the CSV export contains
- What fields are in each table
- What data types are used
- What relationships exist between tables
- Whether billing, scheduling, portal messages, care coordination data, etc. are included
- Whether fields have descriptions or value set definitions

**No sample data files** of any format are provided or accessible.

### Vendor's own content organization

The PDF organizes export content by **method** rather than by data domain. There is no entity-level data dictionary available to present. The closest the vendor comes to content organization is:

| Export Method | Vendor's Claimed Content | Documented Detail |
|---|---|---|
| C-CDA R2.1 | 20 clinical sections (listed above) | Section names only; relies on C-CDA standard for field definitions |
| CSV Full Data Set | "Health, activity and financial data" | No detail — data dictionary URL is dead |
| FHIR R4 API | 27 resource types (US Core) | Standard FHIR resource definitions |
| HL7 ADT | "Demographics and payer information" | No field-level detail |
| HL7 SIU | "Appointments, edits, cancellations, check-in" | No field-level detail |
| HL7 DFT | Description is copy-paste of SIU (likely an error) | No field-level detail |
| JSON Documents | "Scanned documents, faxes, custom reports" | Described as JSON with BASE-64 encoded content |
| EDI 837P/835 | "Claim and remittance files" | Standard EDI format |

**No entity/field inventory can be produced** because no data dictionary, schema, or sample data is accessible.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes coverage through **methods** rather than **data domains**:

- **Clinical data** is covered via C-CDA R2.1 (20 standard sections) and FHIR R4 (27 US Core resources). These are standard projections, not native data. They cover the standard clinical summary but not vendor-specific clinical data structures.
- **Financial data** is claimed via CSV export (unverifiable) and EDI 837P/835 (claims/remittance only, no charges, payments, or insurance details beyond what EDI carries).
- **Scheduling data** is covered via HL7 SIU messages (real-time feed, not bulk export).
- **Demographics/payer data** is covered via HL7 ADT and FHIR Patient/Coverage resources.
- **Documents** (scanned/faxed) are covered via JSON exchange.

The **richest documented mechanism** is the C-CDA export, with 20 named sections and a detailed use case walkthrough (pages 6–9). The **thinnest** is the CSV export — described in a single paragraph with a dead link for details. Yet the CSV export is the only one that could constitute a true all-EHI export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA (standard demographics), FHIR Patient, HL7 ADT | Standard fields covered; vendor-specific demographics fields unknown |
| Encounters / visits | ⚠️ Partial | C-CDA Encounters section, FHIR Encounter | Standard encounter data; visit-level detail (visit type, duration, facility specifics) unknown |
| Problems / conditions | ✅ Covered | C-CDA Problems section, FHIR Condition | Standard coverage via C-CDA/FHIR |
| Medications / prescriptions | ✅ Covered | C-CDA Medications section, FHIR MedicationRequest/MedicationDispense | Standard coverage; e-prescribing transaction details (pharmacy responses, fill status) unclear |
| Allergies | ✅ Covered | C-CDA Allergy section, FHIR AllergyIntolerance | Standard coverage |
| Immunizations | ✅ Covered | C-CDA Immunizations section, FHIR Immunization | Standard coverage |
| Vitals | ✅ Covered | C-CDA Vitals section, FHIR Observation | Standard coverage |
| Lab results | ✅ Covered | C-CDA Lab Results section, FHIR DiagnosticReport/Observation | Standard coverage |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport; no dedicated C-CDA imaging section listed | Product's imaging capabilities unclear; DiagnosticReport may cover radiology reports |
| Procedures | ✅ Covered | C-CDA Procedures section, FHIR Procedure | Standard coverage |
| Clinical notes / documents | ⚠️ Partial | FHIR DocumentReference, JSON document exchange for scanned docs | Scanned documents covered; structured clinical notes (SOAP notes, H&P) not explicitly addressed beyond C-CDA Assessment/Clinical Instructions |
| Care plans / goals | ✅ Covered | C-CDA Care Plan, Goal, Health Concern sections; FHIR CarePlan, Goal | Standard coverage |
| Orders / referrals | ✅ Covered | C-CDA Referrals section, FHIR ServiceRequest | Standard coverage |
| Insurance / coverage | ⚠️ Partial | HL7 ADT "payer information," FHIR Coverage, CSV export claims | HL7 ADT and FHIR Coverage provide some payer data; depth of insurance details unknown |
| Claims / billing | ⚠️ Partial | EDI 837P/835 for claims/remittance; CSV export claims "financial data" | EDI covers claim submissions and remittances in standard format; but charges, superbills, fee schedules, and full billing detail are unverifiable without the CSV data dictionary. Product has deep billing/RCM capabilities ("revQ"); significant gap if CSV doesn't cover it |
| Payments | ⚠️ Partial | EDI 835 for remittance; CSV "financial data" claimed | EDI 835 covers payer remittance; patient payments, co-pays, adjustments unknown |
| Consents / directives | ❌ Not covered | No mention in any export method | Product likely stores consent forms; gap |
| Patient communications / portal messages | ❌ Not covered | No mention in any export method | Product has patient portal with secure messaging; gap |
| Specialty-specific data | ❌ Not covered | No specialty-specific entities in any export | Product serves behavioral health, cardiology, pediatrics, OBGYN; any specialty-specific templates or assessments would not be captured by standard C-CDA/FHIR |

**Key gaps**: Patient portal messages, consents/directives, and specialty-specific clinical data are not covered by any documented export method. Billing data coverage depends entirely on the unverifiable CSV export.

## 6. Documentation Quality

**Overall quality: Poor.**

- **No data dictionary**: The single most important documentation artifact — the CSV data dictionary — is inaccessible (dead URL, no alternatives found, no Wayback Machine captures). This makes it impossible to evaluate the native data export.
- **No sample data**: No example files of any format are provided.
- **No machine-readable schemas**: No XSD, JSON Schema, OpenAPI spec, or other programmatic format definition.
- **No field-level documentation**: The C-CDA export lists section names but relies entirely on the C-CDA R2.1 standard for field definitions. No vendor-specific fields or extensions are documented.
- **Copy-paste error**: The HL7 DFT description (method 6) repeats the SIU description verbatim — "real time updates on patient appointments, appointment edits, appointments cancelation and check-in" — rather than describing financial transactions.
- **Format**: The 9-page PDF reads as a high-level implementation overview, not technical export documentation. Half of the document (pages 5–9) describes an optional data exchange service rather than the (b)(10) export itself.

**Could a developer build an import?** Not from these artifacts alone. The C-CDA and FHIR exports use recognized standards, so a developer familiar with those could consume them — but that's standard interoperability, not (b)(10). The CSV export, which is the actual "all EHI" mechanism, has zero documentation available. A developer would need to contact Enable Healthcare directly to understand the CSV file structure, relationships, and field definitions.

## 7. Overall Assessment

### Classification

**Partial native export** — with significant caveats.

The vendor *describes* a CSV "full data set export" that would cover health, activity, and financial data — which, if implemented as described, would constitute a native data export. However, the data dictionary documenting this export is inaccessible (HTTP 404), making the claim unverifiable. The verifiable export mechanisms (C-CDA, FHIR, EDI) are standard-based projections that cover clinical data and some billing data but miss vendor-specific data.

Given that the CSV export's existence and scope cannot be verified from available documentation, and the only verifiable export mechanisms are standard projections, the practical reality is closer to a **standard-based projection** supplemented by EDI claims data. The "partial native export" classification gives benefit of the doubt to the vendor's stated CSV capability.

### Key Findings

1. **The critical data dictionary is missing.** The CSV export data dictionary at `https://emr.ehiconnect.com/docs/` returns HTTP 404 with no alternative available. This is the only artifact that could validate the vendor's claim of a "full data set" export covering health, activity, and financial data. Without it, the (b)(10) export is effectively undocumented.

2. **The verifiable exports are standard projections, not native data.** The C-CDA R2.1 (20 sections) and FHIR R4 (27 US Core resources) are standard clinical interoperability formats, not the vendor's native data model. They cover typical clinical summary data but inherently exclude billing detail, specialty-specific data, portal messages, and vendor-specific clinical structures.

3. **Multi-format approach adds complexity without clarity.** Eight different export methods across 5+ formats (FHIR, C-CDA, CSV, HL7 v2, EDI, JSON) means a data consumer would need to integrate multiple disparate formats with no documentation on how they relate to each other or how to correlate records across formats.

4. **Financial data coverage is split and partial.** EDI 837P/835 covers claims and remittances in standard billing format, but the deeper billing data the product stores (charges, superbills, insurance details, patient payments, RCM workflow data) is only claimed via the inaccessible CSV export.

5. **The PDF has quality issues.** The HL7 DFT description is a copy-paste error repeating the SIU text. The document is a Word-to-PDF conversion from December 2023 that appears to be a one-time compliance artifact rather than maintained technical documentation.

### Summary Stats

```
Classification:  Partial native export (unverifiable — data dictionary inaccessible)
Export format:   CSV (claimed), C-CDA R2.1, FHIR R4, EDI 837P/835, HL7 v2, JSON
Model type:      Claimed native (CSV) + standard projections (C-CDA, FHIR)
Entities:        N/A (data dictionary inaccessible)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (C-CDA, CSV, FHIR Bulk, EDI)
Domains covered: 10 of 16 applicable domains (with caveats — most via standard projections only)
```

### Bottom Line

Enable Healthcare describes a CSV "full data set" export that could be a genuine all-EHI export, but the data dictionary documenting it is inaccessible (HTTP 404), making the claim unverifiable. The verifiable export mechanisms are standard C-CDA and FHIR projections covering typical clinical data, supplemented by EDI claims files. A patient or provider requesting their complete data would get clinical summaries via C-CDA/FHIR but likely lack full billing detail, portal messages, specialty-specific assessments, and consent records — unless the undocumented CSV export fills those gaps. The single biggest weakness is the inaccessible data dictionary: without it, neither patients nor developers can understand what the CSV export actually contains.

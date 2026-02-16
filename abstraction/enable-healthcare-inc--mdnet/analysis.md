# EHI Export Analysis: Enable Healthcare Inc.

**Product**: MDnet V10  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 10247 (15.04.04.2719.MDne.10.01.1.191231)

## 1. Product Context

MDnet is a cloud-based, ONC-certified ambulatory EHR and practice management platform from Enable Healthcare Inc. (East Hanover, NJ). It serves small-to-midsize ambulatory practices across multiple specialties including behavioral health, pediatrics, cardiology, internal medicine, and OB/GYN.

The product is an integrated clinical, administrative, and financial platform. Key capabilities relevant to EHI scope:

- **Clinical EHR**: Encounter documentation, problem/medication/allergy lists, immunizations, family health history, implantable device tracking, lab results, clinical notes (including AI-powered SOAP notes via "Lumina"), clinical decision support
- **E-Prescribing**: Electronic prescriptions to pharmacies
- **Practice Management**: Appointment scheduling, online booking, patient check-in
- **Medical Billing & RCM**: Insurance eligibility verification, claim submission, revenue cycle management (branded "revQ"), claims scrubbing, denial management
- **Patient Portal**: Secure messaging, medical record access, appointment scheduling, co-payment management
- **Telehealth**: Integrated telehealth/telemedicine
- **Care Coordination**: Chronic Care Management (CCM), Remote Patient Monitoring (RPM), population health, Annual Wellness Visits
- **Document Management**: Scanning of paper records, fax management
- **Interoperability**: C-CDA exchange, Direct messaging, FHIR API

The breadth of the product — particularly the integrated billing/RCM capabilities — sets a high bar for what a genuine (b)(10) export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI_DATA_EXPort_GUIDE.pdf` | 9-page PDF (904 KB). "Data Interoperability & EHI Data Export Guide" dated Dec 2023. Describes scope and 8 export methods. Created from Word via "Print to PDF." Author: Rahul Dewan. | **Primary artifact** — provides the only substantive documentation of the EHI export. High-level overview only; no field-level detail. |
| `downloads/fhir-capability-statement.json` | FHIR R4 CapabilityStatement (25 KB). Lists 27 resource types with interactions and search parameters. | **Moderately informative** — confirms the FHIR API is a standard US Core (g)(10) API, not a purpose-built EHI export. |
| `downloads/fhir-portal-landing.png` | Screenshot of the FHIR portal landing page at fhir.ehiconnect.com. Shows Testing Sandbox, Registration, and Documentation cards. | **Low informativeness** — confirms portal exists, no content detail. |
| `downloads/fhir-api-documentation-page.png` | Screenshot of the FHIR API documentation page. "Dynamic FHIR" branded page with standard FHIR R4 API docs. | **Low informativeness** — confirms standard (g)(10) API documentation. |

**Critical missing artifact**: The PDF references a CSV data dictionary at `https://emr.ehiconnect.com/docs/` — this URL returns HTTP 404 (verified 2026-02-16). This is the only artifact that could document the field-level content of the claimed "full data set" CSV export. No alternative location was found.

## 3. Export Mechanics

The PDF describes **8 export methods** spanning multiple formats and delivery mechanisms:

| # | Method | Format | Mechanism | Scope |
|---|---|---|---|---|
| 1 | FHIR APIs | FHIR R4 JSON | API (SMART on FHIR) | USCDI clinical data (27 resource types) |
| 2 | C-CDA R2.1 Export | C-CDA XML | Integrated "CCDA Export Tracker" in MDnet UI | Clinical data (20 sections); supports full set, partial, incremental |
| 3 | CSV Full Data Set | CSV | On-demand request by authorized users | "Health, activity and financial data" (claimed) |
| 4 | HL7 2.x/3.x ADT | HL7 v2/v3 | Real-time feed | Demographics and payer info |
| 5 | HL7 2.x SIU | HL7 v2 | Real-time feed | Appointment scheduling |
| 6 | HL7 2.x DFT | HL7 v2 | Real-time feed | Financial transactions (description appears copy-pasted from SIU) |
| 7 | JSON Scanned Documents | JSON + BASE-64 | Real-time feed | Scanned documents, faxes, custom reports |
| 8 | EDI 837P/835 | EDI | Continuous feed | Claims and remittance files |

**Single-patient vs bulk**: The C-CDA export supports both single and bulk. The CSV export supports "a specific patient or all patients." The FHIR API supports both via standard FHIR and Bulk Data Access.

**Access constraints**: Exports require "authorized users" with "required access" granted within MDnet. The optional "Announce & Deliver" C-CDA service (pages 5–9) involves Enable Healthcare configuring data exchange bridges (VPN, SFTP, web services).

**Fees**: Not documented in the PDF, though the "Announce & Deliver" service is described as an "add-on additional service."

## 4. Export Content: What's In It

### No Data Dictionary Available

The most critical finding: **there is no accessible data dictionary for any export method.** The PDF references a CSV data dictionary at `https://emr.ehiconnect.com/docs/` which returns HTTP 404. Without this, the field-level content of the CSV export (the only method claimed to cover financial data) is unknown.

- **Total entities with field-level documentation**: 0
- **Total fields documented with descriptions**: 0
- **Machine-readable schemas**: Only the FHIR CapabilityStatement (standard US Core, not product-specific)
- **Sample data**: None provided

### Vendor's own content organization

The PDF organizes export content by method rather than by data domain. Here is what can be documented:

**FHIR API (27 resource types — standard US Core)**:

| Resource Type | Category | Search Params | Notes |
|---|---|---|---|
| Patient | Demographics | 7 | Standard US Core |
| Condition | Clinical | 3 | Problems/diagnoses |
| Procedure | Clinical | 3 | Procedures |
| Observation | Clinical | 5 | Labs, vitals, assessments |
| DiagnosticReport | Clinical | 5 | Diagnostic reports |
| MedicationRequest | Clinical | 4 | Medication orders |
| MedicationDispense | Clinical | 2 | Medication dispensing |
| AllergyIntolerance | Clinical | 2 | Allergies |
| Immunization | Clinical | 3 | Immunizations |
| CarePlan | Clinical | 3 | Care plans |
| CareTeam | Clinical | 3 | Care team members |
| Goal | Clinical | 2 | Goals |
| Encounter | Clinical | 3 | Encounters |
| DocumentReference | Clinical | 5 | Clinical documents |
| Coverage | Financial | 2 | Insurance coverage |
| ServiceRequest | Clinical | 3 | Orders/referrals |
| Device | Clinical | 2 | Medical devices |
| Provenance | Infrastructure | 2 | Data provenance |
| Specimen | Clinical | 2 | Specimens |
| ClinicalImpression | Clinical | 2 | Clinical assessments |
| Location | Infrastructure | 2 | Facility info |
| Organization | Infrastructure | 2 | Organizations |
| Practitioner | Infrastructure | 2 | Providers |
| PractitionerRole | Infrastructure | 2 | Provider roles |
| RelatedPerson | Demographics | 2 | Related persons |
| Group | Infrastructure | 0 | Bulk data groups |
| Binary | Infrastructure | 0 | Binary content |

**C-CDA R2.1 Export (20 sections)**:

| Section | Category | Notes |
|---|---|---|
| Allergy | Clinical | Standard C-CDA section |
| Assessment | Clinical | |
| Encounters | Clinical | |
| Family History | Clinical | |
| Functional Status | Clinical | |
| Cognitive Status | Clinical | |
| Immunizations | Clinical | |
| Medical Equipment | Clinical | Implantable devices |
| Medications | Clinical | |
| Lab Results | Clinical | |
| Problems | Clinical | |
| Procedures | Clinical | |
| Reason for Visit | Clinical | |
| Referrals | Clinical | |
| Social History | Clinical | |
| Vitals | Clinical | |
| Care Plan | Clinical | |
| Goal | Clinical | |
| Health Concern | Clinical | |
| Clinical Instructions | Clinical | |

All 20 sections are standard C-CDA content — no vendor-specific extensions or non-clinical sections.

**CSV Export**: Claimed to cover "health, activity and financial data" but data dictionary is inaccessible (404). No field-level detail available.

**EDI 837P/835**: Standard claims (837P) and remittance (835) formats. No product-specific documentation beyond one-sentence description.

**HL7 v2 ADT/SIU/DFT**: Standard HL7 message types for demographics, scheduling, and financial transactions. DFT description appears to be a copy-paste error (repeats SIU text verbatim).

**JSON Scanned Documents**: Custom JSON format with patient identifier segments and BASE-64 encoded document content. No schema provided.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes export through **8 methods** spanning 5 formats. The coverage breaks down into:

1. **Clinical data (well-described)**: The FHIR API (27 US Core resources) and C-CDA export (20 sections) cover standard clinical domains comprehensively at the section/resource level. This is the standard clinical exchange surface — what every certified EHR provides for interoperability.

2. **Financial data (claimed but undocumented)**: The scope statement explicitly includes "claim, adjudication and all other related data sets." Financial data is addressed through three mechanisms: CSV export (field-level detail unavailable — 404), EDI 837P/835 (standard claim/remittance files), and HL7 DFT (description is a copy-paste error from SIU). The Coverage FHIR resource provides basic insurance information.

3. **Scanned documents (thin)**: JSON-based exchange for scanned documents and faxes is described in one paragraph. No schema or sample provided.

4. **Scheduling (thin)**: HL7 SIU for appointment updates is described in one sentence.

5. **Demographics/payer (thin)**: HL7 ADT for demographics and payer updates is described in one paragraph.

The richest documentation is for the optional "Announce & Deliver" C-CDA incremental update service (pages 5–9), which includes a detailed use case walkthrough. However, this covers only C-CDA clinical data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR Patient resource; HL7 ADT; C-CDA standard demographics. No field-level detail for what MDnet specifically exports. | Product stores demographics per (a)(5). Coverage likely adequate via standard formats but unverifiable at field level. |
| Encounters / visits | ⚠️ Partial | FHIR Encounter; C-CDA Encounters section. | Standard clinical encounter data only. No detail on visit-specific metadata MDnet may store. |
| Problems / conditions | ⚠️ Partial | FHIR Condition; C-CDA Problems section. | Standard coverage via clinical exchange formats. |
| Medications / prescriptions | ⚠️ Partial | FHIR MedicationRequest, MedicationDispense; C-CDA Medications section. | Prescriptions covered. E-prescribing workflow data (pharmacy responses, fill status) unclear. |
| Allergies | ⚠️ Partial | FHIR AllergyIntolerance; C-CDA Allergy section. | Standard allergy data. |
| Immunizations | ⚠️ Partial | FHIR Immunization; C-CDA Immunizations section. | Standard immunization records. |
| Vitals | ⚠️ Partial | FHIR Observation; C-CDA Vitals section. | Standard vital signs. |
| Lab results | ⚠️ Partial | FHIR Observation, DiagnosticReport, Specimen; C-CDA Lab Results section. | Standard lab data. |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport; C-CDA not explicit for imaging. | Product's imaging capabilities are unclear (not prominently featured). |
| Procedures | ⚠️ Partial | FHIR Procedure; C-CDA Procedures section. | Standard procedure data. |
| Clinical notes / documents | ⚠️ Partial | FHIR DocumentReference, Binary; C-CDA Assessment, Clinical Instructions; JSON scanned docs. | Clinical notes via standard formats. Scanned docs via custom JSON. No field-level documentation for either. |
| Care plans / goals | ⚠️ Partial | FHIR CarePlan, Goal; C-CDA Care Plan, Goal, Health Concern sections. | Standard care planning data. |
| Orders / referrals | ⚠️ Partial | FHIR ServiceRequest; C-CDA Referrals section. | Basic order/referral data. |
| Insurance / coverage | ⚠️ Partial | FHIR Coverage; HL7 ADT payer segments. | Basic insurance info. Depth of eligibility details, prior authorizations unclear. |
| Claims / billing | ⚠️ Partial | EDI 837P/835 described in one sentence; CSV export claimed but undocumented (404). | Product has robust billing/RCM capabilities ("revQ"). EDI files cover claim/remittance but the CSV export that would provide full financial data detail is undocumented. **Significant documentation gap.** |
| Payments | ⚠️ Partial | EDI 835 remittance files; CSV export claimed but undocumented. | Patient payments, adjustments, posting detail unknown. |
| Consents / directives | ❌ Not covered | No mention in any export method. | Product likely stores consent forms; not addressed in export documentation. |
| Patient communications | ❌ Not covered | No mention of portal messages, secure messaging, or communication history. | Product has patient portal with secure messaging; **gap**. |
| Specialty-specific data | ❌ Not covered | No specialty-specific content documented. | Product serves behavioral health, cardiology, pediatrics, OB/GYN. No specialty-specific export content documented. |

**Note on "Partial" ratings**: All clinical domains are rated "Partial" rather than "Covered" because the documentation provides only section/resource names with no field-level detail specific to MDnet. The vendor relies entirely on standard format specifications (FHIR US Core, C-CDA R2.1) without documenting what MDnet-specific data elements are included. There is no way to verify whether MDnet exports all fields it stores for any given clinical domain, or only the minimum required by the standard.

## 6. Documentation Quality

**Overall: Poor.** The documentation fails the basic test of enabling a developer to understand and consume the export.

**What exists**:
- A 9-page high-level overview PDF listing export methods and their scope
- A FHIR CapabilityStatement (standard, not product-specific)
- The PDF scope statement correctly identifies health data AND financial data

**What's missing**:
- **Data dictionary**: The only referenced data dictionary URL returns 404 — the most critical documentation artifact is inaccessible
- **Field-level documentation**: Zero fields are documented with names, types, descriptions, or relationships for any export method
- **Sample data**: No sample exports, example files, or test data provided
- **Schemas**: No machine-readable schemas beyond the standard FHIR CapabilityStatement (no XSD, JSON Schema, OpenAPI, CSV column specs)
- **Value sets**: No coded value documentation
- **Relationship mappings**: No documentation of how data across the 8 export methods relates or can be correlated
- **Error in PDF**: The HL7 DFT section (method 6) repeats the SIU description verbatim — a copy-paste error that was not caught

**Could a developer build an import?** No. A developer receiving these exports would need to:
1. Reverse-engineer the CSV format with no data dictionary
2. Integrate 5+ different formats (C-CDA, CSV, EDI, HL7 v2, JSON) with no documentation of how they relate
3. Contact Enable Healthcare for field-level details on every format
4. Hope that the training videos (behind MDnet authentication) provide what the public documentation doesn't

The PDF reads as a compliance-oriented overview document created once (Dec 2023) from a Word document, not as maintained technical documentation.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to verify what the export actually covers. While the PDF *claims* the CSV export covers "health, activity and financial data," the data dictionary for that export is inaccessible (HTTP 404). The verifiable export components (FHIR API, C-CDA) are standard clinical exchange formats covering only USCDI-scope data. The EDI 837P/835 files would cover claims data, but there is no documentation of what specific claim data is included or how it maps to MDnet's billing model. The HL7 DFT method (financial transactions) has a copy-paste error in its description, making its actual scope unknowable.

The product has deep billing/RCM capabilities, a patient portal with messaging, telehealth, care coordination programs (CCM, RPM), and multi-specialty workflows — none of which are verifiably covered by the documented export.

**Axis 2 — Export approach: Unclear/undetermined**

The vendor describes 8 export methods, which suggests they put thought into coverage breadth rather than simply pointing to a single existing API. The inclusion of EDI 837P/835 for billing data and a CSV "full data set" export alongside the standard FHIR/C-CDA clinical exports is a positive signal — if these methods actually work and are documented. However:

- The FHIR API is clearly the standard (g)(10) API (Dynamic FHIR branded, standard US Core resources)
- The C-CDA export is standard clinical exchange (20 standard sections)
- The CSV export — the only method that could constitute a purpose-built EHI export — has no accessible documentation
- The HL7 and EDI methods are real-time feeds typically used for operational integration, not point-in-time EHI export

Without the CSV data dictionary, it's impossible to determine whether Enable Healthcare built a genuine purpose-built EHI export or assembled a list of their existing integration interfaces and called it (b)(10).

### Key Findings

1. **The CSV data dictionary — the single most important artifact — is inaccessible.** The URL referenced in the PDF (`https://emr.ehiconnect.com/docs/`) returns HTTP 404. This is the only export method claimed to cover "health, activity and financial data," and without its data dictionary, the central claim of the EHI export is unverifiable.

2. **Zero fields are documented at the field level across all 8 export methods.** The documentation provides section/resource names only, relying entirely on external standard specifications (FHIR US Core, C-CDA R2.1, HL7 v2, EDI). No MDnet-specific field mappings, value sets, or data relationships exist in any accessible artifact.

3. **The verifiable export components (FHIR, C-CDA) are standard clinical exchange surfaces.** The 27 FHIR resources match the standard US Core set; the 20 C-CDA sections are standard C-CDA content. These cover USCDI-scope data but not the billing, scheduling, portal messaging, care coordination, or specialty data that MDnet stores.

4. **The multi-format approach creates integration complexity without documentation.** A consumer would need to integrate 5+ formats (C-CDA, CSV, EDI, HL7 v2, JSON) with no documentation of how to correlate records across them (e.g., linking a C-CDA clinical encounter to an EDI 837P claim for the same visit).

5. **The HL7 DFT description is a copy-paste error.** Method 6 (HL7 DFT for financial transactions) repeats the SIU appointment scheduling description verbatim, suggesting the documentation was not carefully reviewed.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined
Export format:   Mixed (FHIR R4, C-CDA R2.1, CSV, HL7 v2, EDI 837P/835, JSON)
Entities:        48 (27 FHIR resources + 20 C-CDA sections + 1 undocumented CSV export)
Fields:          0 (no field-level documentation accessible)
Descriptions:    N/A (0 fields documented)
Sample data:     No
Bulk export:     Yes (C-CDA and CSV support bulk; FHIR supports Bulk Data Access)
Domains covered: 0 of 19 fully verified; ~13 of 19 partially addressed via standard formats
```

### Bottom Line

Enable Healthcare's EHI export documentation makes the right claims — explicitly including financial data alongside clinical data and describing 8 export methods — but fails to deliver the documentation needed to verify or use those exports. The single most important artifact, the CSV data dictionary for the "full data set" export, returns 404. Without it, the export is effectively a collection of standard clinical exchange interfaces (FHIR API, C-CDA) supplemented by undocumented billing feeds (EDI, DFT) and an undocumented CSV export. A patient or provider requesting their data would receive clinical summaries in standard formats but would have no way to verify whether the financial, portal messaging, care coordination, or specialty data that MDnet stores is included.

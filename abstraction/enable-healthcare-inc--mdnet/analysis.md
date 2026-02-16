# EHI Export Analysis: Enable Healthcare Inc.

**Product**: MDnet V10
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2719.MDne.10.01.1.191231 (CHPL ID 10247)

## 1. Product Context

MDnet is a cloud-based, ONC-certified Electronic Health Records platform by Enable Healthcare Inc. (East Hanover, NJ) designed as an integrated clinical, administrative, and financial management system for ambulatory healthcare practices. The product serves multiple specialties including mental/behavioral health, pediatrics, cardiology, internal medicine, urgent care, and OBGYN.

MDnet encompasses:
- **Clinical EHR**: Encounter documentation, problem/medication/allergy lists, immunizations, family history, implantable devices, vitals, lab results, clinical decision support, AI-powered charting ("Lumina"/"enableAssist")
- **E-Prescribing**: Electronic prescription transmission
- **Practice Management**: Appointment scheduling, patient check-in, online booking
- **Medical Billing & RCM**: Insurance eligibility verification, claim submission, denial management, revenue cycle management (branded "revQ")
- **Patient Portal**: Record access, secure messaging, appointment scheduling, co-payment management
- **Telehealth**: Integrated telemedicine
- **Care Coordination**: Chronic Care Management (CCM), Remote Patient Monitoring (RPM), population health, Annual Wellness Visits
- **Document Management**: Scanning of paper records, fax management
- **Interoperability**: C-CDA exchange, Direct messaging, FHIR R4 API

Enable Healthcare also operates as a medical billing services company, making billing/claims data a core part of the product's data holdings. A complete EHI export should cover clinical encounters, demographics, medications, allergies, immunizations, labs, problems, procedures, vitals, care plans, billing/claims, insurance/coverage, prescriptions, scanned documents, patient portal messages, and care coordination data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `EHI_DATA_EXPort_GUIDE.pdf` | 9-page PDF (904 KB). Primary EHI export documentation. Describes scope, 8 export methods, and an optional incremental C-CDA data exchange service. Created 2023-12-28 from Word document by Rahul Dewan. | **Most informative** — the only substantive documentation |
| `fhir-capability-statement.json` | FHIR R4 CapabilityStatement (25 KB). Lists 27 supported resource types with search parameters. Standard US Core set. | **Moderately informative** — confirms FHIR API scope |
| `fhir-portal-landing.png` | Screenshot of FHIR portal at fhir.ehiconnect.com. Shows three cards: Testing Sandbox, Registration, Documentation. "Dynamic FHIR" branding (third-party platform by Dynamic Health IT). | **Low informativeness** — confirms portal exists |
| `fhir-api-documentation-page.png` | Screenshot of FHIR API documentation page. Shows SMART on FHIR authorization, terms of use, client registration details. "Dynamic FHIR Server API works in conjunction with ConnectEHR version FHIR4-B." | **Low informativeness** — standard (g)(10) API docs, not (b)(10) specific |

**Critical missing artifact**: The PDF references a CSV data dictionary at `https://emr.ehiconnect.com/docs/` — this URL returns HTTP 404 (verified 2026-02-16). No alternative location found. The root `emr.ehiconnect.com` returns HTTP 403. Seven alternative paths probed — all 404. This is the single most important artifact for assessing the (b)(10) export and it is inaccessible.

## 3. Export Mechanics

The EHI Data Export Guide describes **8 export methods**:

| # | Method | Format | Mode | Bulk? | Real-time? |
|---|---|---|---|---|---|
| 1 | FHIR APIs | FHIR R4 JSON/XML | SMART on FHIR API | Yes (Bulk Data) | No |
| 2 | C-CDA R2.1 export | C-CDA R2.1 XML | Integrated "CCDA Export Tracker" UI | Yes | No |
| 3 | CSV full data set | CSV | On-demand request | Yes | No |
| 4 | HL7 2.x/3.x ADT | HL7 v2 ADT | Real-time interface | No | Yes |
| 5 | HL7 2.x SIU | HL7 v2 SIU | Real-time interface | No | Yes |
| 6 | HL7 2.x DFT | HL7 v2 DFT | Real-time interface | No | Yes |
| 7 | JSON documents | JSON + BASE-64 | Real-time exchange | No | Yes |
| 8 | EDI 837P/835 | EDI 837P/835 | Continuous feed | Yes | Yes |

**How export is obtained**: The C-CDA export uses an integrated "CCDA Export Tracker" accessible by authorized users within MDnet — options include full set, partial date-based, partial segment-based, or incremental. The CSV export is described as available to "authorized users" who can "request" it. The FHIR API requires SMART on FHIR registration. HL7, JSON, and EDI methods appear to be integration interfaces rather than user-initiated exports.

**Single-patient and bulk**: Both C-CDA and CSV support single-patient or all-patient export. FHIR supports both individual and bulk operations.

**Optional add-on service**: Pages 5–9 describe an "Announce & Deliver" data exchange service using C-CDA R2.1 with incremental updates. This supports VPN P2P tunnels, SFTP (hosted by either party), or HTTPS web services. This appears to be a vendor-assisted integration service, not a self-service export.

**Fees**: Not explicitly stated. The optional incremental C-CDA service is described as an "add-on" which implies additional cost.

**Notable issue**: The HL7 DFT description (method 6) repeats the SIU text verbatim — a copy-paste error. DFT is supposed to handle financial transactions, but the document describes it as handling "patient appointments, appointment edits, appointments cancelation and check-in" (the SIU description).

## 4. Export Content: What's In It

### 4.1 What can be verified

There is **no accessible data dictionary** for the CSV export — the referenced URL (`https://emr.ehiconnect.com/docs/`) returns 404. No sample data, no schemas (apart from the FHIR CapabilityStatement), and no field-level documentation exist in the available artifacts. The analysis below is therefore based on:
1. The 20 C-CDA sections listed in the PDF
2. The 27 FHIR resource types from the CapabilityStatement
3. The descriptions of the 8 export methods in the PDF

### 4.2 C-CDA R2.1 content (20 sections)

The PDF lists these C-CDA sections (vendor's exact terms):

| Section | Standard EHI Domain |
|---|---|
| Allergy | Allergies |
| Assessment | Clinical notes |
| Encounters | Encounters/visits |
| Family History | Demographics (family) |
| Functional Status | Clinical assessments |
| Cognitive Status | Clinical assessments |
| Immunizations | Immunizations |
| Medical Equipment | Implantable devices |
| Medications | Medications/prescriptions |
| Lab Results | Lab results |
| Problems | Problems/conditions |
| Procedures | Procedures |
| Reason for Visit | Encounters |
| Referrals | Orders/referrals |
| Social History | Demographics (social) |
| Vitals | Vitals |
| Care Plan | Care plans/goals |
| Goal | Care plans/goals |
| Health Concern | Problems/conditions |
| Clinical Instructions | Clinical notes |

These are standard C-CDA sections. No vendor-specific extensions or custom sections are described. Field-level detail is not provided — the vendor defers to the C-CDA R2.1 standard specification.

### 4.3 FHIR R4 resources (27 types)

From `fhir-capability-statement.json`:

| Resource Type | Search Params | Profiles | Notes |
|---|---|---|---|
| Patient | 8 | 1 (US Core) | Has `patient-export` bulk operation |
| Observation | 4 | 24 (vitals, labs, smoking, SDOH, etc.) | Broadest profile support |
| DocumentReference | 7 | 1 | C-CDA documents only (LOINC 48764-5) |
| Organization | 7 | 1 | |
| ServiceRequest | 6 | 1 | |
| MedicationRequest | 5 | 1 | |
| Encounter | 5 | 1 | |
| CarePlan | 4 | 1 | |
| Condition | 4 | 3 (problems, encounter dx, health concerns) | |
| DiagnosticReport | 4 | 2 (lab, note) | |
| AllergyIntolerance | 3 | 1 | |
| Goal | 3 | 1 | |
| MedicationDispense | 3 | 1 | |
| Coverage | 1 | 1 | Insurance coverage |
| CareTeam | 2 | 1 | |
| ClinicalImpression | 2 | 1 | |
| Device | 2 | 1 (implantable) | |
| Immunization | 2 | 1 | |
| Location | 2 | 1 | |
| Procedure | 2 | 1 | |
| Practitioner | 2 | 1 | |
| PractitionerRole | 2 | 1 | |
| RelatedPerson | 2 | 1 | |
| Specimen | 2 | 1 | |
| Binary | 2 | 1 | |
| Group | 0 | 0 | Bulk export operation only |
| Provenance | 0 | 1 | |

Total: 27 resource types, 86 search parameters. All US Core profiles — no vendor-specific extensions. Server-level `$export` operation is available (Bulk Data). This is a standard (g)(10) FHIR API, not a (b)(10)-specific mechanism.

### 4.4 Other export methods (no field-level detail)

| Method | What it covers (per PDF) | Documentation level |
|---|---|---|
| CSV full data set | "Health, activity and financial data" | **Undocumented** — data dictionary URL returns 404 |
| HL7 ADT | Demographics and payer information | Standard HL7 v2 — no MDnet-specific documentation |
| HL7 SIU | Appointment scheduling data | Standard HL7 v2 — no MDnet-specific documentation |
| HL7 DFT | Financial transactions (stated) | **Copy-paste error** — description matches SIU |
| JSON documents | Scanned documents, faxes, custom reports | Described briefly — JSON with BASE-64 content |
| EDI 837P/835 | Claims and remittance files | Standard EDI — no MDnet-specific documentation |

### Vendor's own content organization

The vendor does not organize content into categories. The PDF presents export methods, not data domains. The closest to a content inventory is the C-CDA section list (20 items) and the claim that the CSV export covers "health, activity and financial data." Without the CSV data dictionary, there is no entity-level or field-level inventory available from this vendor.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes coverage at three levels of specificity:

1. **C-CDA R2.1** (most specific): 20 clinical sections covering allergies, problems, medications, immunizations, labs, procedures, vitals, encounters, care plans, goals, referrals, social/family history, functional/cognitive status, and clinical instructions. This is standard clinical summary data — well-defined but limited to what C-CDA can represent.

2. **FHIR R4 API** (moderately specific): 27 US Core resource types. This overlaps heavily with C-CDA content. Notable additions: Coverage (insurance), MedicationDispense, Specimen, ClinicalImpression, ServiceRequest. But these are all standard US Core — no vendor-specific extensions that would indicate native data model exposure.

3. **CSV export** (claimed but unverifiable): Described as "detailed export of health, activity and financial data." This is the only export method claimed to cover everything, including financial data. But the data dictionary is inaccessible, so the actual content cannot be verified.

4. **EDI 837P/835** (specific to billing): Claims and remittance data in standard EDI format. This is genuinely financial data, but it's a separate feed — not integrated with the other export methods.

5. **HL7 v2 interfaces** (real-time feeds): ADT for demographics/payer, SIU for scheduling, DFT for financial transactions. These are integration interfaces, not bulk export mechanisms.

6. **JSON exchange** (specific to documents): Scanned documents, faxes, custom reports with BASE-64 encoded content. Narrow but addresses a data type (documents) that other methods don't.

**Strongest area**: Clinical data via C-CDA and FHIR — standard and well-defined.
**Weakest area**: Financial/billing data — claimed to be in CSV export but unverifiable; EDI 837P/835 covers claims but is a separate mechanism. The CSV data dictionary's inaccessibility is the single biggest documentation gap.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA Social History, FHIR Patient (8 search params); HL7 ADT for demographics | C-CDA/FHIR provide standard demographic fields. No evidence of native-model export with full demographic detail (contacts, preferred language, employer, etc.) |
| Encounters / visits | ✅ Covered | C-CDA Encounters + Reason for Visit sections; FHIR Encounter resource | Standard encounter data available via both formats |
| Problems / conditions / diagnoses | ✅ Covered | C-CDA Problems + Health Concern sections; FHIR Condition (3 profiles: problems, encounter dx, health concerns) | Well-covered across both export formats |
| Medications / prescriptions | ✅ Covered | C-CDA Medications section; FHIR MedicationRequest + MedicationDispense | Includes dispense data via FHIR, prescriptions via C-CDA |
| Allergies | ✅ Covered | C-CDA Allergy section; FHIR AllergyIntolerance | Standard allergy data |
| Immunizations | ✅ Covered | C-CDA Immunizations section; FHIR Immunization | Standard immunization records |
| Vitals | ✅ Covered | C-CDA Vitals section; FHIR Observation (multiple vital sign profiles) | FHIR Observation has 24 supported profiles including pediatric measures |
| Lab results | ✅ Covered | C-CDA Lab Results section; FHIR Observation (lab profile) + DiagnosticReport | Standard lab result data |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport (note profile); no imaging-specific export | Product's imaging capabilities are unclear; DiagnosticReport exists but imaging not prominent |
| Procedures | ✅ Covered | C-CDA Procedures section; FHIR Procedure | Standard procedure records |
| Clinical notes / documents | ⚠️ Partial | C-CDA Assessment + Clinical Instructions sections; FHIR DocumentReference (C-CDA only per LOINC 48764-5); JSON export for scanned docs | C-CDA and JSON cover structured notes and scanned documents, but full note content (free-text SOAP notes, AI-generated notes) unclear |
| Care plans / goals | ✅ Covered | C-CDA Care Plan + Goal sections; FHIR CarePlan + Goal + CareTeam | Well-represented across both formats |
| Orders / referrals | ✅ Covered | C-CDA Referrals section; FHIR ServiceRequest | Referral and order data present |
| Insurance / coverage | ⚠️ Partial | FHIR Coverage resource; HL7 ADT includes payer information | Coverage data exists in FHIR but limited (1 search param). Detailed insurance data (policy details, copay structures) likely in CSV export but unverifiable |
| Claims / billing | ⚠️ Partial | EDI 837P/835 provides claims and remittance files; CSV export claims "financial data" but no data dictionary | EDI covers claims in standard format, but this is a separate feed. The product does extensive billing/RCM — the depth of billing data export is unverifiable without the CSV data dictionary |
| Payments | ⚠️ Partial | EDI 835 provides remittance/payment data; CSV export may include more | EDI 835 covers insurer payments; patient payments, co-pays, adjustments unclear |
| Consents / directives | ❌ Not covered | No mention in any export method | Product may store consent data; no export evidence |
| Patient communications / portal messages | ❌ Not covered | No mention in any export method | Product has patient portal with secure messaging; significant gap |
| Specialty-specific data | ❌ Not covered | No specialty-specific export content described | Product serves multiple specialties (behavioral health, cardiology, pediatrics); no evidence of specialty-specific data in any export |

**Key gap analysis findings**:
- **Billing/claims**: MDnet is a billing/RCM platform (Enable Healthcare also offers billing services). The CSV export claims to cover "claim, adjudication and all other related data sets," but this is unverifiable. EDI 837P/835 covers standard claims but is a separate feed, not an integrated export. The gap between what MDnet stores (full RCM data) and what is documented is significant.
- **Patient portal messages**: MDnet has a patient portal with secure messaging — these are EHI (used for care decisions) but not mentioned in any export method.
- **Care coordination**: MDnet offers CCM, RPM, and population health features. Data from these programs (enrollment, monitoring data, care plans) is not specifically addressed in the export documentation, though some may be captured in C-CDA care plan sections.

## 6. Documentation Quality

**Overall**: Poor. The documentation describes *that* exports exist but provides almost no detail about *what* they contain at the field level.

**Strengths**:
- The scope statement is correct — it explicitly includes financial data alongside clinical data, which is the right framing for (b)(10)
- The C-CDA incremental update use case (pages 5–9) is well-written and provides a genuinely helpful walkthrough of how the "Announce & Deliver" service works
- The multi-format approach acknowledges that different data types require different formats
- The FHIR CapabilityStatement is machine-readable and confirms the (g)(10) API scope

**Weaknesses**:
- **No accessible data dictionary**: The single most critical artifact — the CSV data dictionary at `https://emr.ehiconnect.com/docs/` — returns HTTP 404. Without it, the "full data set" claim is entirely unverifiable
- **No sample data**: No example CSVs, C-CDAs, HL7 messages, EDI files, or JSON payloads
- **No field-level documentation**: Beyond the C-CDA section names (which defer to the standard) and FHIR search parameters (also standard), there is zero field-level detail about what MDnet exports
- **No schemas**: No XSD, JSON Schema, OpenAPI specs, or other machine-readable format definitions for non-FHIR exports
- **Copy-paste error**: The DFT section (method 6) repeats the SIU description verbatim
- **No relationship mapping**: No documentation of how records correlate across the 8 different export formats
- **Training videos behind auth**: The PDF references training videos "embedded into MDNet" — inaccessible for documentation review

**Could a developer build an import?** No. A developer receiving this documentation could implement FHIR and C-CDA consumption (since those follow published standards), but would have no basis for consuming the CSV export, JSON document exchange, or HL7 v2 interfaces without extensive back-and-forth with Enable Healthcare. The multi-format approach with 8 different formats and no field-level documentation for most of them makes independent implementation infeasible.

## 7. Overall Assessment

### Classification

**Partial native export** — The vendor claims a CSV export covering "health, activity and financial data" which, if the data dictionary were accessible, could represent a native data model export. However, the data dictionary URL is dead, making this unverifiable. The documented exports (C-CDA, FHIR) are standard-based projections. The overall picture is a product with the right *intent* (explicitly including financial data, offering CSV native export) but critically incomplete *documentation* (the only artifact that would validate the native export claim is inaccessible).

### Key Findings

1. **The CSV data dictionary is inaccessible** — the URL referenced in the PDF (`https://emr.ehiconnect.com/docs/`) returns HTTP 404 (verified 2026-02-16). This is the single most important artifact for evaluating the (b)(10) export and it is missing. Without it, the claimed "full data set" CSV export is entirely undocumented.

2. **The scope statement is correct but unsubstantiated** — the PDF explicitly states the export covers both health data and financial data including "claim, adjudication and all other related data sets." This is the right scope for (b)(10). But no evidence exists to verify this claim — no data dictionary, no sample files, no field lists.

3. **The documented exports are standard-based projections** — C-CDA R2.1 (20 sections) and FHIR R4 (27 US Core resource types) cover standard clinical data but inherently cannot represent billing, custom forms, specialty data, or administrative data. The FHIR API is a standard (g)(10) implementation using Dynamic FHIR (third-party platform), not a (b)(10)-specific mechanism.

4. **Multi-format fragmentation increases complexity** — a complete export requires consuming 5+ different formats (C-CDA, CSV, HL7 v2, EDI, JSON) with no documentation of how to correlate records across them. This is architecturally ambitious but practically difficult.

5. **Patient portal messages and specialty data are absent** — MDnet has a patient portal with secure messaging and serves multiple specialties, but neither portal messages nor specialty-specific data appear in any export method.

### Summary Stats

    Classification:  Partial native export
    Export format:   Multi-format (C-CDA R2.1, CSV, FHIR R4, HL7 v2, EDI 837P/835, JSON)
    Model type:      Hybrid (standard projections documented; native CSV export claimed but undocumented)
    Entities:        27 FHIR resources + 20 C-CDA sections (CSV entity count unknown — data dictionary inaccessible)
    Fields:          N/A (no field-level documentation for native export; 86 FHIR search parameters)
    Descriptions:    N/A (data dictionary inaccessible)
    Sample data:     No
    Bulk export:     Yes (C-CDA bulk, FHIR Bulk Data, CSV all-patients)
    Domains covered: 10 of 17 applicable domains (✅ or ⚠️)

### Bottom Line

Enable Healthcare has the right intent — their scope statement explicitly includes financial data and they describe a CSV export that could cover the full native data model. However, the critical documentation artifact (CSV data dictionary) is inaccessible, leaving the most important export method entirely undocumented. What *is* documented — C-CDA and FHIR — covers standard clinical data but misses billing detail, portal messages, and specialty-specific data that MDnet stores. A patient or provider requesting their data would receive clinical summaries in standard formats but would have no assurance of receiving complete billing, administrative, or specialty data.

# EHI Export Analysis: eDerm Systems LLC

**Product**: eDerm Systems v2.8.0
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2592.eDer.28.00.1.191025 (CHPL Product ID 10149)

## 1. Product Context

eDerm Systems is a cloud-based, dermatology-specific EHR and practice management platform built by eDerm Systems LLC (Boca Raton, FL). It comprises three integrated modules:

- **EHR** (iPad-native): "One-Touch Charting" using 3D anatomical maps, clinical photography (unlimited photos linked to encounters), pathology lifecycle tracking (biopsy orders through results and treatment), cancer patient tracking, structured physical exam templates, and a dermatology knowledge base with disease descriptions, differentials, and treatment plans.
- **Practice Management** (web-based): Patient registration, multi-provider/multi-location scheduling, insurance verification, document management, consent forms, phone messages.
- **Revenue Cycle Management** (web-based): "Smart Coder" for automated CPT/ICD-10 code suggestion, electronic claims filing (primary/secondary/tertiary), automatic payment posting, collections management, financial reporting.

The product was ONC-certified on October 25, 2019, with certified criteria including (b)(10) EHI export. It integrates with Updox for patient portal/messaging and NLM API for clinical terminology. The product appears to have a small installed base (8 App Store ratings, no reviews on major platforms).

**Baseline expectation for a complete EHI export**: Given these three modules, a (b)(10) export should cover clinical encounter documentation (including dermatology-specific charting, clinical photographs, pathology lifecycle data), demographics, medications, allergies, labs, vitals, problems, procedures, immunizations, billing/claims data, insurance information, and any patient portal data stored locally.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `eDerm-API-Documentation-G8-G9.pdf` | 570 KB, 26 pages | Proprietary REST API documentation for (g)(9)/(g)(10). Documents OAuth auth, patient search, encounter listing, and C-CDA export. Contains sample C-CDA response. | **Primary artifact** — only technical documentation available. Covers (g)(9)/(g)(10), NOT (b)(10). |
| `ederm-onc-certified.html` | 60 KB | ONC certification/mandatory disclosures page. Lists certified criteria, links to API docs and RWT plans/results. | **Confirmed absence** — no mention of EHI export, (b)(10), data dictionary, or export documentation anywhere on page. |
| `ValidURLs.json` | 4 KB | FHIR Endpoint Bundle with 2 Organization/Endpoint pairs registering the FHIR service base URL. | Not informative for EHI analysis — (g)(10) registration artifact only. |
| `ederm-onc-certified-page.png` | 467 KB | Full-page screenshot of certification page. | Visual confirmation of page content; no EHI export content visible. |
| `fhir-endpoint-cert-expired.png` | 72 KB | Screenshot of browser SSL error for the FHIR endpoint. | Documents dead endpoint. |

**No EHI-specific documentation was found among any artifact.** The only technical documentation (the API PDF) covers the (g)(9)/(g)(10) clinical summary API.

## 3. Export Mechanics

**There is no documented (b)(10) EHI export mechanism.** The only documented data access is through the proprietary REST API described in the PDF:

- **Format**: C-CDA 2.1 XML (also supports JSON and HTML response formats for the same clinical summary data)
- **Mechanism**: REST API with OAuth token authentication (username/password grant). Four endpoints: Authenticate → SearchPatient → GetPatientEncounters → GetPatientData
- **Scope**: Single-patient only. No bulk export documented.
- **Access**: API documentation references an internal hostname (`remotedev-5`), not a production URL. The registered FHIR endpoint (`fhir.ederm.io:9443`) has an expired SSL certificate (expired Feb 10, 2026) and returns HTTP 404 — the FHIR application has been undeployed from the Tomcat server.
- **Fees**: Not documented. The API PDF's "Terms of Use" section states "TBD: Link will be added here," indicating the documentation was never finalized.

The registered CHPL URL for (b)(10) points to the FHIR CapabilityStatement endpoint — this is a (g)(10) endpoint, not an EHI export mechanism. This appears to be a classic (b)(10)/(g)(10) conflation.

## 4. Export Content: What's In It

### No data dictionary exists

There is no data dictionary, no schema documentation, no field-level definitions, no value sets, no relationship documentation, and no sample export files. The only structural information comes from the GetPatientData API's 21 boolean parameters (of which 6 are demographics identifiers, leaving 15 clinical data toggles) and the embedded C-CDA sample in the PDF.

### API Parameters (GetPatientData)

The API accepts the following boolean flags to select C-CDA sections:

| Parameter | Category | Notes |
|---|---|---|
| `patientname` | Demographics | Patient name |
| `patientgender` | Demographics | Gender |
| `patientdob` | Demographics | Date of birth |
| `patientrace` | Demographics | Race |
| `patientethnicity` | Demographics | Ethnicity |
| `patientpreferredlanguage` | Demographics | Preferred language |
| `medications` | Medications | Medication list |
| `medicationallergies` | Allergies | Medication allergies |
| `labtest` | Lab | Lab test orders |
| `labresults` | Lab | Lab test results |
| `vitalsigns` | Vitals | Vital signs |
| `procedures` | Procedures | Procedure history |
| `careteammembers` | Care team | Care team members |
| `immunizations` | Immunizations | Immunization history |
| `udiforpatientdevices` | Devices | Implantable device UDIs |
| `planoftreatment` | Treatment | Plan of treatment |
| `goals` | Goals | Patient goals |
| `healthconcerns` | Health concerns | Health concerns |
| `assessment` | Assessment | Assessment and plan |
| `problems` | Problems | Problem list |
| `smokingstatus` | Social history | Smoking status |

The PDF states: "All values are options, if you donot give any paratemer it will return complete record." This "complete record" is limited to what C-CDA can represent.

### C-CDA Sections in Sample Response

The embedded C-CDA sample contains 14 sections: Chief Complaint, Allergies, Immunizations, Medications Administered, Problem List, Procedures, Results (Lab), Vital Signs, Goals, Health Concerns, Assessments, Social History, Encounter Diagnosis, and Referrals.

These are standard USCDI/US Core clinical summary sections. There are no vendor extensions, no dermatology-specific sections, no billing sections, and no custom data elements beyond what C-CDA 2.1 natively supports.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides exactly one documented data export mechanism: a C-CDA clinical summary API. It covers 15 clinical data categories corresponding to standard USCDI data classes. The coverage is shallow — each category is a single boolean toggle with no field-level documentation. There is no indication that any data beyond standard C-CDA sections is exportable.

The export covers basic clinical summary data that any ONC-certified EHR must support for (g)(9)/(g)(10). It does not cover any of eDerm's distinctive features: clinical photography, pathology lifecycle tracking, dermatology-specific charting, billing/claims, or practice management data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | 6 API params (name, gender, DOB, race, ethnicity, language) | Minimal demographics — no address, contact info, insurance, or registration details. Product stores full registration data. |
| Encounters / visits | ⚠️ Partial | GetPatientEncounters returns PatientId, VisitBeginDateTime, ProviderFullName | Only 3 fields per encounter. No encounter type, location, disposition, or detailed encounter data. |
| Problems / conditions | ⚠️ Partial | `problems` param → C-CDA Problem List section | Standard C-CDA section; no field-level detail documented. |
| Medications / prescriptions | ⚠️ Partial | `medications` param → C-CDA Medications section | Standard C-CDA section only. E-prescribing data (if stored) not addressed. |
| Allergies | ⚠️ Partial | `medicationallergies` param → C-CDA Allergies section | Limited to medication allergies; environmental/food allergies unclear. |
| Immunizations | ⚠️ Partial | `immunizations` param → C-CDA Immunizations section | Standard C-CDA section. |
| Vitals | ⚠️ Partial | `vitalsigns` param → C-CDA Vital Signs section | Standard C-CDA section. |
| Lab results | ⚠️ Partial | `labtest` + `labresults` params → C-CDA Results section | Standard C-CDA section. No lab interface detail. |
| Imaging / diagnostic reports | ❌ Not covered | No params or C-CDA sections for imaging | Product stores clinical photographs (unlimited, encounter-linked); significant dermatology-specific gap. |
| Procedures | ⚠️ Partial | `procedures` param → C-CDA Procedures section | Standard C-CDA section only. Dermatology-specific procedure detail (Mohs surgery, biopsies) not addressed. |
| Clinical notes / documents | ❌ Not covered | No note/document params in API | Product's "One-Touch Charting" creates structured dermatology notes with 3D anatomical maps. No export mechanism for this core feature. |
| Care plans / goals | ⚠️ Partial | `planoftreatment`, `goals`, `healthconcerns`, `assessment` params | Standard C-CDA sections. |
| Orders / referrals | ⚠️ Partial | C-CDA Referrals section in sample | Only referrals; lab CPOE orders not separately documented. |
| Insurance / coverage | ❌ Not covered | No insurance params or sections | Product stores insurance info and performs real-time verification. Not exportable. |
| Claims / billing | ❌ Not covered | No billing params or sections | Product has full RCM module (Smart Coder, claims, payments, collections). None exported. |
| Payments | ❌ Not covered | No payment data | Product has automatic payment posting. Not exported. |
| Consents / directives | ❌ Not covered | No consent params or sections | Product generates automated consent forms. Not exported. |
| Patient communications | ❌ Not covered | No messaging params | Portal via Updox; phone messages in PM module. Not exported. |
| Specialty-specific (Dermatology) | ❌ Not covered | No dermatology-specific params or sections | **Critical gap**: Pathology lifecycle (biopsy orders → results → treatment), clinical photography, cancer tracking, dermatology knowledge base references, anatomical charting data — none exportable. These are the product's core differentiating features. |

**Summary**: 0 domains fully covered, 10 domains partially covered (standard C-CDA only), 8 domains not covered at all. Every "partial" coverage is limited to what a standard C-CDA document contains, with no field-level documentation.

## 6. Documentation Quality

The documentation quality is very poor:

- **No EHI-specific documentation exists.** There is no acknowledgment of (b)(10) requirements, no description of what "all electronic health information" means in the context of this product, and no export documentation beyond the (g)(9)/(g)(10) API PDF.
- **The API PDF is rudimentary.** It is 26 pages, most of which is an embedded C-CDA sample response. The actual API documentation consists of 4 endpoint descriptions with no field-level definitions, no error handling beyond generic HTTP status codes, and sample URLs referencing an internal hostname (`remotedev-5`).
- **No machine-readable artifacts.** No JSON schema, no FHIR CapabilityStatement (endpoint is dead), no data dictionary in any format.
- **Unfinished documentation.** The "Terms of Use" section reads "TBD: Link will be added here." The link text on the certification page says "G9-G10.pdf" but the file is actually named "G8-G9.pdf."
- **A developer could not build an import from this documentation.** There are no field definitions, no value sets, no data types, no cardinality, and no relationship documentation. Even the C-CDA sections are documented only as boolean on/off toggles with no detail about what each section contains.

## 7. Overall Assessment

### Classification

**Minimal/stub** — There is no (b)(10) EHI export documentation. The vendor's only documented data access is a (g)(9)/(g)(10) C-CDA clinical summary API that covers standard USCDI data classes. There is no data dictionary, no native database export, no bulk export, and no coverage of dermatology-specific clinical data, billing, or practice management data. The registered FHIR endpoint is dead.

### Key Findings

1. **No (b)(10) documentation exists.** The certification page, vendor website, and all downloaded artifacts contain zero references to EHI export, (b)(10), data dictionary, or full record export. The CHPL-registered URL for (b)(10) points to a FHIR CapabilityStatement endpoint that is dead (expired SSL cert, 404).

2. **Classic (b)(10)/(g)(10) conflation.** The only documented export is the (g)(9)/(g)(10) C-CDA API — a clinical summary mechanism being implicitly treated as the (b)(10) export. This covers roughly 15 USCDI data classes but none of the vendor-specific data.

3. **Dermatology-specific data is entirely missing.** The product's core value — clinical photography, pathology lifecycle tracking, anatomical charting, cancer follow-up, dermatology knowledge base references — has no export mechanism documented. This is the most significant gap because it represents data that exists nowhere else.

4. **Billing/RCM data is entirely missing.** The product has a complete revenue cycle management module (claims, payments, collections, Smart Coder) with no documented export.

5. **FHIR endpoint is non-functional.** The registered FHIR server at `fhir.ederm.io:9443` has an expired SSL certificate (expired Feb 10, 2026) and returns 404 for all paths — the FHIR application has been undeployed from Tomcat.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA 2.1 XML (also JSON/HTML via same API)
Model type:      Standard projection (C-CDA clinical summary)
Entities:        N/A (no data dictionary)
Fields:          N/A (21 API parameters, 15 clinical toggles)
Descriptions:    N/A (no field-level documentation)
Sample data:     No (only an embedded C-CDA example in the API PDF)
Bulk export:     No
Domains covered: 0 of 18 fully; 10 of 18 partially (C-CDA standard sections only)
```

### Bottom Line

eDerm Systems has not implemented or documented a (b)(10) EHI export. The only available mechanism is a standard C-CDA clinical summary API that covers basic USCDI data classes while omitting the product's entire dermatology-specific clinical dataset (photography, pathology tracking, anatomical charting), all billing/RCM data, and all practice management data. A patient or provider requesting their complete record from this system would receive a fraction of what is stored, with the most clinically distinctive and valuable data — the dermatology-specific content — entirely absent.

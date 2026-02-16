# EHI Export Analysis: eDerm Systems LLC

**Product**: eDerm Systems v2.8.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2592.eDer.28.00.1.191025 (CHPL #10149)

## 1. Product Context

eDerm Systems is a cloud-based, dermatology-specific EHR, practice management, and revenue cycle management platform built by eDerm Systems LLC (Boca Raton, FL). The EHR runs as a native iPad app with a cloud backend; Practice Management and RCM run as browser-based web applications.

**Key data domains the product stores:**
- **Clinical charting**: "One-Touch Charting" with 3D anatomical body maps, structured dermatology exam templates, clinical photography (unlimited photos linked to encounters)
- **Pathology lifecycle**: Biopsy orders, requisitions, pathology results, status tracking, biopsy logs — a distinctive dermatology-specific workflow
- **Cancer patient tracking**: Follow-up management for cancer diagnoses
- **Demographics, problems, medications, allergies, vitals, labs, immunizations, procedures** — standard clinical data
- **Practice management**: Scheduling, patient registration, insurance verification, phone messages, document scanning, consent forms
- **Revenue cycle management**: Smart Coder (automated CPT/ICD-10 coding), electronic claims filing (primary/secondary/tertiary), automatic payment posting, collections management, financial reporting
- **Patient portal** (via Updox integration): Portal access to medical records, secure messaging

The product was ONC certified October 2019 and is certified for (b)(10) EHI export among other criteria. The product is a small-footprint niche product (8 App Store ratings, no reviews on major EHR comparison sites).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/eDerm-API-Documentation-G8-G9.pdf` (584 KB, 26 pages) | Proprietary REST API documentation covering OAuth authentication, patient search, encounter listing, and C-CDA patient data retrieval. Documents the (g)(9)/(g)(10) API only. Lists 20 boolean parameters for toggling C-CDA sections. Includes embedded C-CDA sample response. | **Most informative** — only technical documentation available |
| `downloads/ValidURLs.json` (4 KB) | FHIR Endpoint Bundle registering the FHIR service base URL with two Organization/Endpoint pairs. Payload type: C-CDA structured body. | **Low** — registration artifact, not documentation |
| `downloads/ederm-onc-certified.html` (61 KB) | ONC certification/mandatory disclosures page. Links to API PDF, ValidURLs.json, and Real World Testing plans/results (2022–2025). Contains Drummond Group letter dated 01/25/2019. | **Moderate** — confirms no EHI export documentation exists on the certification page |
| `downloads/ederm-onc-certified-page.png` (478 KB) | Full-page screenshot of the ONC certification page. | **Low** — visual confirmation of HTML content |
| `downloads/fhir-endpoint-cert-expired.png` (74 KB) | Screenshot showing ERR_CERT_DATE_INVALID for the FHIR metadata URL (expired Let's Encrypt cert, Feb 10 2026). | **Low** — documents the dead endpoint |

**No EHI export documentation, data dictionary, export schema, or (b)(10)-specific documentation was found among any artifacts.** The ONC certification page contains zero mentions of "EHI," "b(10)," "electronic health information," "export," or "data dictionary" (verified by text search of HTML source).

## 3. Export Mechanics

- **Format**: C-CDA 2.1 (XML), with JSON and HTML also available as return formats from the same API
- **Mechanism**: Proprietary REST API (not FHIR). Four endpoints: Authenticate, SearchPatient, GetPatientEncounters, GetPatientData. Accessed via POST requests with OAuth bearer token.
- **Single-patient only**: The API is patient-by-patient — no bulk export capability is documented
- **Access constraints**: Requires OAuth credentials (username/password grant). Sample URLs reference an internal hostname (`remotedev-5`), and the "Terms of Use" section says "TBD: Link will be added here" — suggesting the API was never fully productionized for external use
- **FHIR server**: The registered FHIR endpoint (`fhir.ederm.io:9443`) is dead — SSL certificate expired Feb 10, 2026, and the FHIR application has been undeployed (Tomcat returns 404 for all paths)
- **Fees**: Not documented

**This is not a (b)(10) EHI export mechanism.** It is the (g)(9)/(g)(10) clinical summary API. The CHPL entry lists the FHIR metadata URL as the EHI documentation URL, which is a (g)(10) endpoint registration, not (b)(10) documentation.

## 4. Export Content: What's In It

### No data dictionary exists

There is no data dictionary, no export schema, no field-level documentation, and no description of what data would be included in a (b)(10) export. The only structured documentation is the list of 20 boolean API parameters that toggle C-CDA sections.

### What the API returns

The GetPatientData API returns a standard C-CDA 2.1 document. The sample response embedded in the PDF (pages 7–25) contains these sections:

| C-CDA Section | Template OID | Content in Sample |
|---|---|---|
| Chief Complaint and Reason for Visit | 2.16.840.1.113883.10.20.22.2.13 | Free text |
| Allergies and Adverse Reactions | 2.16.840.1.113883.10.20.22.2.6.1 | SNOMED-coded allergies |
| Immunizations | 2.16.840.1.113883.10.20.22.2.2.1 | CVX-coded immunizations |
| Medications | 2.16.840.1.113883.10.20.22.2.1.1 | RxNorm-coded medications |
| Problems | 2.16.840.1.113883.10.20.22.2.5.1 | SNOMED-coded conditions |
| Procedures | 2.16.840.1.113883.10.20.22.2.7.1 | SNOMED/CPT-coded procedures |
| Results (Laboratory) | 2.16.840.1.113883.10.20.22.2.3.1 | LOINC-coded lab results |
| Plan of Treatment | 2.16.840.1.113883.10.20.22.2.10 | Free text plan |
| Social History | 2.16.840.1.113883.10.20.22.2.17 | Smoking status (SNOMED) |
| Vital Signs | 2.16.840.1.113883.10.20.22.2.4.1 | LOINC-coded vitals |
| Goals | 2.16.840.1.113883.10.20.22.2.60 | Goal observations |
| Health Concerns | 2.16.840.1.113883.10.20.22.2.58 | Coded health concerns |
| Assessment | 2.16.840.1.113883.10.20.22.2.8 | Free text assessment |
| Mental Status | 2.16.840.1.113883.10.20.22.2.14 | Cognitive/functional observations |
| Functional Status | 2.16.840.1.113883.10.20.22.2.14 | Functional condition observations |
| Referrals | 1.3.6.1.4.1.19376.1.5.3.1.3.1 | Free text referral |

These are standard C-CDA sections corresponding to USCDI data classes. There are no vendor extensions, no dermatology-specific sections, and no billing/financial data.

### Vendor's own content organization

The vendor organizes the API into 20 boolean toggle parameters:

| Parameter | C-CDA Element | Category |
|---|---|---|
| patientname | Patient Name | Demographics |
| patientgender | Sex | Demographics |
| patientdob | Date of Birth | Demographics |
| patientrace | Race | Demographics |
| patientethnicity | Ethnicity | Demographics |
| patientpreferredlanguage | Preferred Language | Demographics |
| smokingstatus | Smoking Status | Social History |
| problems | Problems | Clinical |
| medications | Medications | Clinical |
| medicationallergies | Medication Allergies | Clinical |
| labtest | Laboratory Tests | Clinical |
| labresults | Laboratory Values Results | Clinical |
| vitalsigns | Vital Signs | Clinical |
| procedures | Procedures | Clinical |
| careteammembers | Care Team Members | Clinical |
| immunizations | Immunizations | Clinical |
| udiforpatientdevices | Unique Device Identifiers | Clinical |
| assessment | Assessment and Plan | Clinical |
| goals | Goals | Clinical |
| healthconcerns | Health Concerns | Clinical |

**Total: 20 parameters, 0 field-level definitions, 0 value set specifications.** Each parameter is documented only as a boolean toggle with no further detail about the data returned.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides exactly one documented data access mechanism: a proprietary REST API that returns C-CDA 2.1 documents. The content is organized into 20 toggle parameters across three implicit categories:

- **Demographics** (6 parameters): Basic patient identifiers — name, sex, DOB, race, ethnicity, preferred language. No address, contact info, insurance, or emergency contacts.
- **Social History** (1 parameter): Smoking status only.
- **Clinical** (13 parameters): Standard USCDI clinical data — problems, medications, allergies, labs, vitals, procedures, immunizations, devices, care team, assessment/plan, goals, health concerns.

This is exactly the USCDI v1/v2 clinical summary surface. There is zero depth beyond the C-CDA standard — no field-level documentation, no data types, no value sets beyond what C-CDA requires.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | 6 boolean toggles for name/sex/DOB/race/ethnicity/language in C-CDA header | Basic USCDI demographics only. Product stores registration details, contacts, insurance info — none exported. |
| Encounters / visits | ⚠️ Partial | GetPatientEncounters returns PatientId, VisitBeginDateTime, ProviderFullName | Only 3 fields per encounter. No encounter details, location, type, diagnosis codes, or provider notes. |
| Problems / conditions | ⚠️ Partial | C-CDA Problems section with SNOMED codes | Standard C-CDA section; no dermatology-specific condition detail |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medications section with RxNorm codes | Standard C-CDA; no MAR, no prescription detail, no e-prescribing history |
| Allergies | ⚠️ Partial | C-CDA Allergies section | Standard C-CDA section |
| Immunizations | ⚠️ Partial | C-CDA Immunizations section with CVX codes | Standard C-CDA section |
| Vitals | ⚠️ Partial | C-CDA Vital Signs section with LOINC codes | Standard C-CDA section |
| Lab results | ⚠️ Partial | C-CDA Results section with LOINC codes | Standard C-CDA; no lab interface detail |
| Procedures | ⚠️ Partial | C-CDA Procedures section with SNOMED/CPT codes | Standard C-CDA; no Mohs surgery details, no operative notes |
| Clinical notes / documents | ❌ Not covered | No notes section; only Assessment free text | Product has One-Touch Charting, structured derm templates, document scanning — none exported |
| Clinical photography | ❌ Not covered | No image/media export | **Critical gap**: unlimited clinical photos per encounter is a core feature; no export path |
| Pathology / biopsy tracking | ❌ Not covered | No pathology section | **Critical gap**: biopsy lifecycle (order → results → treatment) is a distinguishing feature; no export |
| Cancer patient tracking | ❌ Not covered | No cancer-specific data | Product tracks cancer patients specifically; no export |
| Care plans / goals | ⚠️ Partial | C-CDA Goals and Health Concerns sections | Standard C-CDA sections |
| Orders / referrals | ⚠️ Partial | C-CDA Referrals section (free text only) | Product has CPOE for lab; referral detail not structured |
| Insurance / coverage | ❌ Not covered | No insurance entities | Product does real-time insurance verification; no export |
| Claims / billing | ❌ Not covered | No billing entities | **Significant gap**: full RCM module with Smart Coder, claims, payment posting; none exported |
| Payments | ❌ Not covered | No payment data | Product has automatic payment posting; no export |
| Consents / directives | ❌ Not covered | No consent data | Product generates consent forms; no export |
| Patient communications | ❌ Not covered | No messaging data | Updox integration provides portal/messaging; no export |
| Specialty-specific (Dermatology) | ❌ Not covered | No dermatology-specific data | 3D anatomical maps, dermatology knowledge base, One-Touch Charting — all absent |

**Summary: 0 domains fully covered, 10 partially covered (standard C-CDA level), 11 not covered at all.** All "partial" coverage is at the generic C-CDA level with no vendor-specific depth.

## 6. Documentation Quality

The documentation quality is very poor:

- **No data dictionary**: There is no field-level documentation for any data element. The API parameters are documented only as boolean toggles ("true"/"false").
- **No schema**: No machine-readable schema, no FHIR StructureDefinitions, no C-CDA template customization documentation.
- **No value sets**: No documentation of coded values, code systems, or allowed values beyond what is implicit in the C-CDA standard.
- **No relationships**: No foreign key documentation, no entity relationship descriptions.
- **Sample data**: A single C-CDA sample response is embedded in the PDF (as escaped XML in the response body section). It uses test data ("Bob New," "Alice Newman") that appears generic rather than dermatology-specific.
- **Unfinished documentation**: The "Terms of Use" section says "TBD: Link will be added here." Sample URLs reference an internal hostname (`remotedev-5`). The file is named "G8-G9" but the website link text says "G9-G10."
- **Dead endpoint**: The registered FHIR server is non-functional (expired SSL cert, undeployed application).

**A developer could not build an import from this documentation.** The only information available is the C-CDA standard itself — the vendor-specific documentation adds nothing beyond the API call mechanics.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

No (b)(10) EHI export documentation exists. The only documented data access mechanism is a C-CDA clinical summary API that covers USCDI-scope data — roughly 14 of the 20+ data categories this product stores. The product's most distinctive features (clinical photography, pathology lifecycle tracking, dermatology-specific charting, cancer tracking) and its entire billing/RCM module have no export documentation whatsoever. The registered CHPL URL for (b)(10) documentation points to a dead FHIR metadata endpoint, which is itself a (g)(10) artifact, not (b)(10) documentation.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging. The vendor registered a FHIR metadata endpoint as the EHI documentation URL (a (g)(10) artifact) and provides only a C-CDA clinical summary API as documentation. The API parameters map exactly to USCDI data classes. The C-CDA sample response contains standard sections with no vendor extensions. There is no indication the vendor ever considered what a full EHI export should include or made any effort to build one. The documentation predates the (b)(10) requirement (PDF created August 2022, certification October 2019) and was clearly written for (g)(9)/(g)(10) compliance.

### Key Findings

1. **No (b)(10) documentation exists.** The ONC certification page contains zero mentions of EHI export, (b)(10), or data dictionary. The registered EHI documentation URL (`fhir.ederm.io:9443/fhir-server/api/v4/metadata`) is a FHIR (g)(10) endpoint that is now dead (expired SSL cert, undeployed app). (`ederm-onc-certified.html`, `fhir-endpoint-cert-expired.png`)

2. **The only documentation is a (g)(9)/(g)(10) C-CDA API** with 20 boolean toggles mapping to standard USCDI sections. No field-level documentation, no data dictionary, no export schema. (`eDerm-API-Documentation-G8-G9.pdf`, 26 pages)

3. **The product's most valuable dermatology-specific data has no export path.** Clinical photography, pathology/biopsy lifecycle tracking, cancer patient tracking, 3D anatomical charting, and dermatology knowledge base — all core differentiators — are entirely absent from any export documentation.

4. **The full RCM module (billing, claims, payments, Smart Coder) is not represented at all.** The product has electronic claims filing, automatic payment posting, and collections management — none of this appears in any export documentation.

5. **The documentation appears unfinished.** "Terms of Use: TBD: Link will be added here." Internal hostnames in sample URLs. Filename/link text mismatch ("G8-G9" vs "G9-G10"). This suggests the API documentation was a draft that was never completed.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   C-CDA 2.1 (XML)
    Entities:        N/A (no data dictionary; 3 API endpoints documented)
    Fields:          20 API toggle parameters (no field-level documentation)
    Descriptions:    0% (parameters are labeled but data elements have no descriptions)
    Sample data:     Yes (single C-CDA sample embedded in PDF)
    Bulk export:     No (single-patient API only)
    Domains covered: 0 of 21 applicable domains fully; 10 of 21 at C-CDA summary level

### Bottom Line

eDerm Systems has not implemented a (b)(10) EHI export. A patient or provider requesting their data would receive, at best, a standard C-CDA clinical summary covering basic USCDI data — no dermatology photos, no biopsy tracking, no billing records, no encounter notes, and none of the specialty-specific data that makes this product a dermatology EHR. The single biggest gap is the complete absence of any EHI export documentation or mechanism beyond the relabeled (g)(10) API, compounded by the fact that even that API endpoint is now non-functional.

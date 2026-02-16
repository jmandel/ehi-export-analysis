# EHI Export Analysis: Advanced Data Systems Corporation

**Product**: MedicsCloud, Version 11.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 10786 (15.02.05.1044.AVDC.01.01.1.220111)

## 1. Product Context

MedicsCloud is an integrated cloud-based EHR and practice management (PM) platform from Advanced Data Systems Corporation (ADS), a privately held healthcare IT company founded in 1977 and headquartered in Paramus, NJ. The product serves ambulatory medical practices across 27+ specialties including internal medicine, podiatry, ophthalmology, orthopedics, cardiology, OB-GYN, neurology, behavioral health, pain management, dermatology, ENT, and urgent care.

MedicsCloud is sold as an all-in-one suite combining:

- **Clinical EHR**: Specialty-specific templates, AI-driven charting (MedicsScribe), voice navigation, CPOE, e-prescribing (Surescripts-certified), lab ordering/results, clinical decision support
- **Practice Management (MedicsPremier)**: Scheduling, billing and claims management, claim tracking/denial management, insurance verification, revenue cycle management, inventory management
- **Patient Engagement**: Patient portal, FHIR/SMART patient app (Medics Me), digital kiosk check-in, interactive texting, telemedicine, remote patient monitoring (RPM)
- **Specialty features**: Attorney/legal case management (personal injury/workers' comp), healthcare CRM, bed management

Based on these capabilities, a comprehensive EHI export should cover: patient demographics, clinical encounters and notes, problems/diagnoses, medications/prescriptions, allergies, immunizations, vitals, lab results, procedures, care plans, billing/claims/payments, insurance/coverage, patient portal messages, RPM data, specialty-specific clinical assessments, documents/images, and communication records.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/B10_MedicsCloud.html` | The entire EHI export documentation page — a single static HTML file (2,288 bytes) containing one paragraph and two links to external HL7 standards. No data dictionary, schema, or vendor-specific documentation. | **Primary artifact** — but almost no information content |
| `downloads/B10_MedicsCloud_screenshot.png` | Browser screenshot (129,601 bytes) confirming the rendered page matches the HTML source. | Confirmatory only |

**Live page verification**: The page at `https://apps.medicscloud.com/B10_MedicsCloud.html` was fetched on 2026-02-16 and is identical to the downloaded artifact. No additional content has been added since the initial collection on 2026-02-15.

Only two files exist in the downloads directory. There are no PDFs, no data dictionaries, no JSON schemas, no sample data files, no ZIP archives — nothing beyond the single HTML page and its screenshot.

## 3. Export Mechanics

Based solely on the documentation page:

- **Format(s)**: HL7 C-CDA XML and HL7 FHIR R4 US Core STU3.1.1
- **Standards referenced**: USCDI v1
- **Mechanism**: Unclear. The page states "authorized users can generate the Electronic Health Information Export (EHI)" but provides no details on how — no UI instructions, no screenshots, no API endpoints, no workflow description.
- **Single-patient**: Yes (stated in documentation)
- **Bulk/population**: Yes (documentation says "a single patient and also the patient population")
- **Access constraints/fees**: Not documented
- **Timing/scheduling**: Not documented

There is no information about how a user actually initiates an export, where the output goes, how long it takes, or what format options are available at export time.

## 4. Export Content: What's In It

### What the documentation says

The documentation contains exactly one substantive sentence:

> "MedicsCloud authorized users can generate the Electronic Health Information Export (EHI) for a single patient and also the patient population in both HL7 CCDA xml format that comply with USCDI v1 requirements standards and HL7 FHIR v 4.0.1 US Core v 3.1.1."

It then links to:
1. The HL7 C-CDA implementation guide ([HL7 C-CDA](https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492))
2. The HL7 FHIR US Core STU3.1.1 implementation guide ([US Core STU3.1.1](https://hl7.org/fhir/us/core/STU3.1.1/))

### What can be inferred

Since the vendor explicitly states compliance with USCDI v1 via C-CDA and FHIR US Core STU3.1.1, the export likely covers the USCDI v1 data classes:

- Patient demographics
- Allergies and intolerances
- Assessment and plan of treatment
- Care team members
- Clinical notes (limited: Consultation Note, Discharge Summary, History and Physical, Procedure Note, Progress Note, and others per US Core)
- Goals
- Health concerns
- Immunizations
- Laboratory results
- Medications
- Problems (conditions)
- Procedures
- Provenance
- Smoking status
- Vital signs

However, there is **no vendor-specific documentation** to verify what data actually appears in MedicsCloud's C-CDA documents or FHIR responses. There are no mappings, no custom extensions, no profiles, and no sample data.

### Vendor's own content organization

There is no vendor-provided entity listing, data dictionary, or content organization. The vendor provides zero entities, zero fields, and zero descriptions. The full inventory is recorded in `analysis/full-entity-inventory.json` (which documents this absence).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no vendor-specific content breakdown whatsoever. The only content claim is conformance to USCDI v1 via C-CDA and FHIR US Core STU3.1.1. These are standardized clinical summary formats that cover a defined (and limited) subset of clinical data. The vendor makes no claims about exporting billing, practice management, specialty-specific, or other non-USCDI data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Implied by USCDI v1 / US Core Patient resource; no vendor-specific mapping provided | USCDI v1 demographics are limited; product stores richer registration data (insurance, ID scans, contacts) |
| Encounters / visits | ⚠️ Partial | Implied by USCDI v1 / US Core Encounter resource | Product stores detailed encounter data across 27+ specialties; C-CDA/US Core captures limited encounter metadata |
| Problems / conditions / diagnoses | ⚠️ Partial | Implied by USCDI v1 Condition resource / C-CDA Problem section | Standard clinical data, likely present but unverified |
| Medications / prescriptions | ⚠️ Partial | Implied by USCDI v1 MedicationRequest / C-CDA Medications section | E-prescribing data (Surescripts transaction details, controlled substance records) likely not fully captured in standard formats |
| Allergies | ⚠️ Partial | Implied by USCDI v1 AllergyIntolerance / C-CDA Allergies section | Likely present but unverified |
| Immunizations | ⚠️ Partial | Implied by USCDI v1 Immunization / C-CDA Immunizations section | Likely present but unverified |
| Vitals | ⚠️ Partial | Implied by USCDI v1 Vital Signs / C-CDA Vital Signs section | Standard vitals likely present; RPM-sourced readings (BP, glucose, O2 sat) unclear |
| Lab results | ⚠️ Partial | Implied by USCDI v1 DiagnosticReport/Observation / C-CDA Results section | Likely present but unverified |
| Imaging / diagnostic reports | ⚠️ Partial | Implied by USCDI v1 DiagnosticReport | Product integrates with imaging; depth of export unclear |
| Procedures | ⚠️ Partial | Implied by USCDI v1 Procedure / C-CDA Procedures section | Likely present but unverified |
| Clinical notes / documents | ⚠️ Partial | Implied by USCDI v1 Clinical Notes (limited types) | Product supports AI-generated notes, specialty templates, voice-transcribed documentation — far richer than C-CDA note types |
| Care plans / goals | ⚠️ Partial | Implied by USCDI v1 CarePlan/Goal | Likely present but unverified |
| Orders / referrals | ⚠️ Partial | CPOE orders implied by C-CDA | Product supports lab orders, referrals; export depth unclear |
| Insurance / coverage | ❌ Not covered | No evidence in USCDI v1 / C-CDA / US Core STU3.1.1 | Product stores insurance verification, insurance discovery, coverage details — **significant gap** |
| Claims / billing | ❌ Not covered | No evidence in USCDI v1 / C-CDA / US Core STU3.1.1 | Product has full billing/claims/RCM capabilities — **significant gap** |
| Payments | ❌ Not covered | No evidence in USCDI v1 / C-CDA / US Core STU3.1.1 | Product processes patient payments, portal payments — **significant gap** |
| Consents / directives | ❌ Not covered | Not part of USCDI v1 | Product collects e-signatures, kiosk check-in consents — gap |
| Patient communications / portal messages | ❌ Not covered | Not part of USCDI v1 / C-CDA / US Core STU3.1.1 | Product has patient portal, interactive texting, telemedicine — **gap** |
| Specialty-specific data | ❌ Not covered | C-CDA/FHIR US Core cannot represent custom specialty assessments | Product supports 27+ specialties with user-definable templates — **significant gap** |

**Note**: All "⚠️ Partial" ratings above reflect that the vendor *claims* USCDI v1 conformance but provides no vendor-specific documentation to verify what actually appears in the export. The rating is based on what USCDI v1 / US Core STU3.1.1 / C-CDA *could* contain, not on verified export content.

## 6. Documentation Quality

The documentation is essentially non-existent from a developer usability standpoint:

- **Data dictionary**: None
- **Field-level documentation**: None
- **Types / constraints**: None (deferred entirely to external HL7 standards)
- **Value sets / code systems**: None
- **Relationships / foreign keys**: None
- **Sample data**: None
- **Machine-readable schemas**: None (the external links to HL7 standards do not constitute vendor-specific schemas)
- **User guide / export instructions**: None beyond "authorized users can generate"
- **API documentation**: None
- **Screenshots**: None

A developer could not build an import from this documentation. The only guidance is "it's C-CDA and FHIR US Core" — which identifies the standard but says nothing about how MedicsCloud specifically implements it, what data is included, what extensions are used, or how vendor-specific data is represented (or whether it is at all).

The page was last modified December 5, 2023 (per HTTP headers noted in the prior report), aligning closely with the December 31, 2023 EHI export compliance deadline. This suggests it was created near the deadline as a compliance checkbox.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The EHI export documentation consists of a single paragraph on a single HTML page. There is no data dictionary, no schema, no sample data, and no vendor-specific documentation of any kind. The vendor equates their (b)(10) EHI export with their existing USCDI v1 / C-CDA / FHIR US Core compliance — which is a textbook case of repackaging (g)(10) standardized API capabilities as a (b)(10) comprehensive EHI export.

### Key Findings

1. **The entire EHI export documentation is 2,288 bytes** — a single HTML page with one substantive sentence and two links to external HL7 standards. This is among the most minimal (b)(10) documentation possible. (Source: `downloads/B10_MedicsCloud.html`)

2. **Classic (b)(10) / (g)(10) conflation**: The vendor explicitly states the export "comply with USCDI v1 requirements standards" using C-CDA and FHIR US Core — these are the (g)(10) standardized API formats, not a comprehensive EHI export. USCDI v1 covers a narrow subset of clinical data.

3. **Billing, claims, and PM data are entirely absent**: MedicsCloud includes a full practice management system (MedicsPremier) with billing, claims, payments, insurance verification, and RCM. None of this data — which is core EHI (billing records about individuals per 45 CFR 164.501) — is addressed in the export documentation.

4. **Specialty-specific clinical data is unaddressed**: The product serves 27+ specialties with user-definable templates. Custom clinical assessments, specialty workflows, and templated documentation cannot be represented in standard C-CDA sections or US Core resources without extensions, which are not documented.

5. **No vendor-specific documentation exists at all**: Zero entities, zero fields, zero descriptions. No mapping of MedicsCloud data to C-CDA sections or FHIR resources. No information about what the export actually contains beyond a reference to external standards.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA XML, FHIR R4 US Core STU3.1.1
Model type:      Standard projection (USCDI v1 only)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (claimed)
Domains covered: 0 of 17 verified; up to 12 of 17 implied by USCDI v1 but unverified
```

### Bottom Line

MedicsCloud's EHI export documentation is a minimal compliance stub — a single sentence equating the (b)(10) export with USCDI v1 / C-CDA / FHIR US Core, which by definition covers only a fraction of what this full-featured EHR+PM system stores. Billing, claims, insurance, payments, specialty-specific clinical data, patient portal interactions, and communication records are entirely unaddressed. A patient or provider relying on this export would receive at best a clinical summary, not a complete copy of their electronic health information.

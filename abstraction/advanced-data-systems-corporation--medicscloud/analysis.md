# EHI Export Analysis: Advanced Data Systems Corporation

**Product**: MedicsCloud  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.02.05.1044.AVDC.01.01.1.220111 (CHPL ID 10786)

## 1. Product Context

MedicsCloud is a cloud-based EHR + practice management (PM) platform from Advanced Data Systems Corporation (ADS), a privately held healthcare IT company founded in 1977 and headquartered in Paramus, NJ. The product targets ambulatory practices across 27+ specialties (internal medicine, podiatry, ophthalmology, orthopedics, cardiology, OB-GYN, behavioral health, pain management, dermatology, ENT, urgent care, and more). It can be deployed as an all-in-one EHR+PM suite or with components used independently.

Key data domains the product stores include:

- **Clinical**: Encounter notes (voice-transcribed via MedicsScribe), problem lists, medication lists, allergies, vitals, clinical assessments, specialty-specific templates for 27+ specialties
- **Orders & Results**: Lab orders, lab results, imaging orders/results, CPOE
- **Prescriptions**: E-prescribing (including controlled substances via Surescripts)
- **Billing & Claims**: Claims management, claim tracking, denial management, EDI transactions, payment history, patient balances, insurance verification/discovery, revenue cycle management
- **Patient Engagement**: Patient portal (questionnaires, appointment requests, messages, payments), patient-facing FHIR/SMART app ("Medics Me"), digital check-in kiosk, interactive texting, telemedicine, remote patient monitoring (BP, glucose, SpO2)
- **Communications**: Secure messages, text interactions, fax documents (AI-sorted)
- **Scheduling**: Appointments, multi-modality scheduling
- **Specialty Features**: Attorney/legal case management (PI/workers' comp), healthcare CRM, inventory management
- **Quality/Public Health**: MIPS dashboards, CQMs, immunization registry submissions, syndromic surveillance, electronic case reporting

This is a full-featured ambulatory EHR+PM system with significant billing, patient engagement, and specialty capabilities. The (b)(10) export should cover far more than clinical summaries.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/B10_MedicsCloud.html` (2,346 bytes) | The entire EHI export documentation page. One paragraph stating exports use C-CDA XML and FHIR US Core STU3.1.1, with two links to external HL7 standards. No data dictionary, no schema, no sample data, no user guide. | **Primary source** — but contains almost no substantive information |
| `downloads/B10_MedicsCloud_screenshot.png` (130 KB) | Screenshot of the HTML page confirming it renders as a simple text page with one paragraph and two links. No hidden content, accordions, or interactive elements. | Confirms the HTML page has no hidden content |

**Total documentation artifacts: 2** (1 HTML page + 1 screenshot). No PDFs, no JSON schemas, no sample data files, no data dictionaries of any kind.

## 3. Export Mechanics

- **Format(s)**: HL7 C-CDA XML and FHIR R4 (US Core STU3.1.1)
- **Mechanism**: Documentation states "authorized users can generate" the export — implies a UI-triggered action, but no screenshots, user guide, or instructions are provided
- **Single-patient vs bulk**: Documentation claims support for "a single patient and also the patient population"
- **Access constraints or fees**: Not documented
- **Export trigger details**: Not documented — no API endpoints, no UI workflow description, no instructions

## 4. Export Content: What's In It

### What the documentation says

The entire substantive content of the (b)(10) documentation is this single sentence:

> "MedicsCloud authorized users can generate the Electronic Health Information Export (EHI) for a single patient and also the patient population in both HL7 CCDA xml format that comply with USCDI v1 requirements standards and HL7 FHIR v 4.0.1 US Core v 3.1.1."

This is followed by two links:
1. HL7 C-CDA standard: `https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492`
2. HL7 FHIR US Core STU3.1.1: `https://hl7.org/fhir/us/core/STU3.1.1/`

### What this tells us

There is **no data dictionary**. There are **no vendor-specific entities, tables, fields, or mappings documented**. Zero entities. Zero fields. The documentation points exclusively to external standards (C-CDA and FHIR US Core STU3.1.1) and claims compliance with USCDI v1.

### Vendor's own content organization

There is no vendor-specific content organization. The vendor provides no tables, no entities, no categories, no field definitions — nothing beyond the sentence quoted above.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

### Implied coverage from referenced standards

The referenced standards (USCDI v1 / US Core STU3.1.1) would at most cover the 16 USCDI v1 data classes mapped to ~27 US Core profiles. But without vendor-specific documentation, it is impossible to verify which of these are actually implemented in the export, or whether the vendor's mapping includes any data beyond the minimum required fields per profile.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no category breakdown, no module listing, and no content inventory. The sole claim is that the export complies with "USCDI v1 requirements standards" via C-CDA and FHIR US Core. This implies coverage of the USCDI v1 clinical summary scope at most — demographics, allergies, conditions, medications, labs, vitals, procedures, immunizations, clinical notes, care plans, goals, smoking status, implantable devices, and provenance.

There is no indication that any data beyond the USCDI v1 clinical summary scope is included. The export formats chosen (C-CDA and FHIR US Core STU3.1.1) are by design limited to clinical exchange data and cannot represent billing, claims, scheduling, patient portal interactions, custom specialty assessments, RPM data, CRM data, attorney/case management data, or inventory data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial (implied) | Implied by USCDI v1 / US Core Patient profile; no vendor mapping | USCDI v1 Patient demographics are a small subset of what an EHR stores; no evidence of full demographic export |
| Encounters / visits | ⚠️ Partial (implied) | Implied by US Core Encounter profile | No vendor-specific documentation of encounter data depth |
| Problems / conditions | ⚠️ Partial (implied) | Implied by US Core Condition profile | Standard profile covers minimal fields; product likely stores more |
| Medications / prescriptions | ⚠️ Partial (implied) | Implied by US Core MedicationRequest profile | E-prescribing details, Surescripts transaction history likely not covered |
| Allergies | ⚠️ Partial (implied) | Implied by US Core AllergyIntolerance profile | Likely present but depth unknown |
| Immunizations | ⚠️ Partial (implied) | Implied by US Core Immunization profile | Likely present but depth unknown |
| Vitals | ⚠️ Partial (implied) | Implied by US Core Vital Signs profiles | Likely present but depth unknown |
| Lab results | ⚠️ Partial (implied) | Implied by US Core DiagnosticReport/Observation profiles | Likely present but depth unknown |
| Imaging / diagnostic reports | ⚠️ Partial (implied) | Implied by US Core DiagnosticReport | Product integrates with imaging; depth unknown |
| Procedures | ⚠️ Partial (implied) | Implied by US Core Procedure profile | Likely present but depth unknown |
| Clinical notes / documents | ⚠️ Partial (implied) | Implied by US Core DocumentReference profile | MedicsScribe AI-transcribed notes, specialty templates likely far exceed what's in standard profiles |
| Care plans / goals | ⚠️ Partial (implied) | Implied by US Core CarePlan/Goal profiles | Depth unknown |
| Orders / referrals | ⚠️ Partial (implied) | Implied by US Core DiagnosticReport; no ServiceRequest in US Core 3.1.1 | CPOE order details likely not fully represented |
| Insurance / coverage | ❌ Not covered | No Coverage resource in US Core STU3.1.1; not in C-CDA clinical summary | Product stores insurance verification, discovery, and coverage data; significant gap |
| Claims / billing | ❌ Not covered | No billing/claims resources in US Core or C-CDA | Product has full billing/claims/denial/EDI capabilities; major gap |
| Payments | ❌ Not covered | No payment data in US Core or C-CDA | Product tracks patient balances, payment history; significant gap |
| Patient communications / portal messages | ❌ Not covered | No messaging resources in US Core STU3.1.1 | Product has patient portal, secure messaging, texting; significant gap |
| Remote patient monitoring data | ❌ Not covered | RPM data (BP, glucose, SpO2 from devices) not in US Core STU3.1.1 scope | Product has RPM module; gap |
| Specialty-specific (27+ specialties) | ❌ Not covered | Custom specialty templates/assessments cannot be represented in standard C-CDA/US Core | Product supports 27+ specialties with custom templates; major gap |
| Attorney/legal case management | ❌ Not covered | No representation in C-CDA or FHIR US Core | Product has PI/workers' comp case management; gap |
| Telemedicine records | ❌ Not covered | No telemedicine session data in US Core | Product has telemedicine module; gap |

**All "Partial (implied)" ratings above are generous** — without vendor-specific documentation, we cannot confirm that even the USCDI v1 domains are fully implemented. The ratings assume the vendor actually implemented the standard profiles they reference.

## 6. Documentation Quality

The documentation quality is essentially non-existent:

- **No data dictionary**: Zero entities, zero fields documented
- **No field-level mapping**: No documentation of how MedicsCloud data maps to C-CDA sections or FHIR resources
- **No schema or profile documentation**: No custom profiles, extensions, or constraints described
- **No sample data**: No example export files provided
- **No user guide**: No instructions for performing the export
- **No API documentation**: No endpoints, authentication, or request/response formats
- **No screenshots**: No visual documentation of the export interface
- **Machine-readable artifacts**: None

A developer could not build an import from this documentation. The only actionable guidance is "it's C-CDA and FHIR US Core 3.1.1" — which defines the container format but says nothing about the vendor's specific implementation, data depth, or mapping decisions.

The HTML page is 2,346 bytes — smaller than many email signatures. It was last modified December 5, 2023, just weeks before the December 31, 2023 EHI export compliance deadline, suggesting minimal effort.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. The stated formats (C-CDA + FHIR US Core STU3.1.1) are structurally incapable of representing the majority of data domains MedicsCloud stores — billing, claims, patient portal interactions, RPM data, specialty templates, telemedicine, CRM, attorney case management, and inventory are all absent from these standard formats. At best, the export covers the USCDI v1 clinical summary layer, which represents a fraction of this full-featured EHR+PM product's designated record set.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of the (b)(10)/(g)(10) conflation. The documentation explicitly states compliance with "USCDI v1 requirements standards" using the exact same formats (C-CDA and FHIR US Core STU3.1.1) required for the (g)(10) FHIR API certification criterion. The vendor references no product-specific data dictionary, no custom mapping beyond the standard templates, and no coverage of data domains outside USCDI. The two external links point to the same generic standards specifications any vendor uses for (g)(10). There is zero evidence that any purpose-built EHI export work was done — this appears to be the vendor's existing clinical exchange export relabeled as (b)(10).

### Key Findings

1. **Single-paragraph documentation**: The entire (b)(10) export documentation is one sentence plus two links to external standards — 2,346 bytes of HTML. This is among the thinnest (b)(10) documentation possible while still having a page at the registered URL.

2. **Explicit USCDI v1 / US Core STU3.1.1 scope**: The vendor explicitly states the export complies with "USCDI v1 requirements standards" using C-CDA and FHIR US Core 3.1.1. These are the (g)(10) clinical exchange formats, not a comprehensive EHI export. USCDI v1 has 16 data classes — this product stores data across 20+ domains.

3. **No billing/PM data in export**: MedicsCloud includes full practice management with billing, claims, denial management, EDI, payment tracking, and revenue cycle management. None of this is representable in C-CDA or FHIR US Core STU3.1.1, and no alternative export mechanism is documented.

4. **No vendor-specific mapping**: The documentation provides zero insight into how MedicsCloud's internal data model maps to the referenced standards. There are no entities, no fields, no profiles, no extensions, no sample data — nothing a developer could use.

5. **Multiple product-specific data domains unaddressed**: Patient portal interactions, RPM data, telemedicine sessions, specialty-specific assessments for 27+ specialties, attorney/legal case management, CRM data, and inventory data have no representation in the documented export formats.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   C-CDA XML + FHIR R4 (US Core STU3.1.1)
    Entities:        0 (no data dictionary)
    Fields:          0 (no data dictionary)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Claimed ("patient population") but undocumented
    Domains covered: 0 confirmed; ~12 implied by standards but unverifiable, of 15+ applicable domains

### Bottom Line

MedicsCloud's (b)(10) documentation is a single sentence claiming the export uses C-CDA and FHIR US Core STU3.1.1 — the same clinical exchange formats used for (g)(10) — with zero vendor-specific detail. For a product that includes full practice management, billing, 27+ specialty templates, patient portal, RPM, telemedicine, and CRM, this represents a repackaging of the clinical summary exchange layer as "all EHI," leaving the majority of the designated record set undocumented and almost certainly unexported. A patient requesting their complete record would likely receive only a clinical summary, not the billing, communications, specialty assessments, and operational data that constitute their full record.

# EHI Export Analysis: Pulse Systems, Inc.

**Product**: Pulse EHR v8.02
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2837.Puls.08.03.1.240806 (CHPL listing 11500)

## 1. Product Context

Pulse EHR is an integrated EHR and practice management platform from Pulse Systems, Inc. (part of Harris Ambulatory Care Enterprise, acquired by N. Harris Computer Corporation in 2019). It targets ambulatory practices across multiple specialties — urology, gastroenterology, orthopedics, primary care, FQHCs, behavioral health, cardiology, oncology, and more.

The product is marketed as "Pulse EHR/PM" — the EHR and practice management components are tightly coupled. Key modules include:

- **Clinical Documentation**: customizable flow sheets, "Pulse Note" clinical knowledge engine, patient clinical snapshot, E&M coding
- **CPOE**: medications, labs, diagnostic imaging with drug interaction checking
- **E-Prescribing**: Surescripts Gold Solution Provider
- **Practice Management (PulsePro)**: scheduling, registration, billing, coding, claims, eligibility verification, A/R tracking, payment posting, denial management
- **Revenue Cycle Management (PulseRCM)**: claims management, certified coding, denial analysis
- **Patient Engagement**: patient portal (InteliChart), automated reminders
- **Population Health**: CQM, care gaps, chronic care management, MACRA/MIPS
- **Document Management**: faxes, transcription, scanned documents

This breadth means the product stores data across clinical, billing, scheduling, claims/RCM, quality, and document management domains. A complete (b)(10) export should cover all of these.

## 2. Artifacts Reviewed

| Artifact | Description | Informative Value |
|---|---|---|
| `screenshot-certification-page-full.png` (694 KB) | Full-page screenshot of Pulse Systems' registered mandatory disclosures page. Shows all certified criteria, costs/disclosures text, and the three documentation links at the bottom. | **High** — confirms the EHI export link text and location |
| `screenshot-ehi-export-link-target.png` (222 KB) | Screenshot showing where the "View Electronic Health Information Export Documentation" link leads — the HL7 FHIR US Core USCDI page | **High** — visual proof the EHI link points to an external standard, not vendor documentation |
| `Pulse-EHI-Export-Document-REV-06142024.docx` (164 KB) | 6-page Word document from CHS.net describing Pulse v16.1's EHI export as a CDA XML document. Lists 44 unique CDA sections. | **Medium** — only EHI export documentation found, but for a **different** product (CHS/Pulse v16.1, CHPL 10360), not Pulse Systems Inc. v8.02 |
| `Pulse-8.0-API-FHIR-Documentation.pdf` (597 KB, 41 pages) | FHIR R4 API documentation for §170.315(g)(10). Covers 19 US Core FHIR resources. | **Low for (b)(10)** — this is the (g)(10) API, not EHI export |
| `Pulse_CommonClinicalDataAPI-002.pdf` (430 KB, 10 pages) | Proprietary REST API for retrieving CCD/CCDA documents via POST requests. | **Low for (b)(10)** — this is the (g)(7)/(g)(9) API |
| `screenshot-certification-page-top.png` (246 KB) | Top portion of the certification page | **Low** — supplementary to the full screenshot |

**Verification of the vendor's EHI export link**: I fetched `https://pulseinc.com/terms-conditions-certification-costs-and-limitations/` directly and confirmed the "View Electronic Health Information Export Documentation" link targets `https://www.hl7.org/fhir/us/core/uscdi.html`. I also fetched that HL7 URL and confirmed it is the US Core USCDI standards page — a generic reference about USCDI versions and FHIR profiles. This is not vendor-specific EHI export documentation.

**Verification of the CHS document**: I fetched `https://www.chs.net/pulse-ehr-information/` and confirmed it hosts the DOCX. The page explicitly states: *"This page contains information related to the Pulse certified Health IT product developed and maintained by Community Health Systems for internal hospital use. This is not commercially available technology."* The CHS product is Pulse v16.1 (certificate references CHPL 10360), a different certified product than Pulse Systems Inc.'s v8.02.

## 3. Export Mechanics

**From Pulse Systems Inc. directly**: Essentially undocumented. The only statement on their certification page is:

> "Pulse EHR is certified to data export criteria and can create a set of export summaries in real time. Though the user can create a set of export summaries in real time, this type of mass export is recommended as best practice to be scheduled during off-peak hours to reduce performance stress on the system."

This tells us:
- An export exists and can run "in real time"
- It generates "export summaries" (plural, suggesting per-patient documents)
- Mass export is possible but resource-intensive (off-peak scheduling recommended)
- No information on format, mechanism (UI button? API?), access, or content

**From the CHS document** (Pulse v16.1, different product): The export is described as a CDA XML document generated via "EHI Tables export," viewable with an HL7 CDA.xsl stylesheet. No UI instructions, no API endpoint, no batch/bulk mechanism described.

- **Format**: CDA XML
- **Mechanism**: unclear (described as "EHI Tables export" but no workflow shown)
- **Single-patient vs bulk**: the Pulse Systems page mentions "mass export," suggesting bulk is possible; CHS doc doesn't address this
- **Access constraints**: none stated; no fees for the export itself

## 4. Export Content: What's In It

### Pulse Systems Inc. (v8.02) — the certified product

**There is no EHI export documentation for the certified product.** The "View Electronic Health Information Export Documentation" link on the mandatory disclosures page points to `https://www.hl7.org/fhir/us/core/uscdi.html` — the HL7 FHIR US Core USCDI reference page. This is not a data dictionary, not a schema, not an export guide. It is an external standards page that maps USCDI data classes to FHIR profiles.

The only content-related statement is the phrase "export summaries," which suggests CDA or similar clinical summary documents, consistent with the CHS document's description.

### CHS/CereCore (Pulse v16.1) — different product, for reference only

The CHS-hosted DOCX describes the export as a CDA XML document containing 44 unique CDA sections (46 listed, with "Health Concerns Section" and "Goals Section" each appearing twice). These sections are standard CDA sections, not vendor-specific entities.

**Key characteristics:**
- **No field-level documentation**: the document lists section names only — no fields, no data types, no value sets, no coded entries
- **No data dictionary**: just a one-column table of section names
- **No sample data**: one partial XML snippet showing CDA header structure
- **No relationships or constraints documented**
- **Acknowledged limitations**: "Some electronic health information might not be available in a format, such as rich text documents or images"

### CDA sections listed (from CHS document)

The 44 unique sections, organized by category:

| Category | Sections |
|---|---|
| Clinical Notes (8) | History Of Present Illness, Physical Examination, Review Of Systems, Progress Note, Procedure Note, Hospital Course, Discharge Summary Note, Consultation Note |
| Diagnoses/Problems (5) | Problems, Hospital Discharge Diagnosis, Admission Diagnosis, PreOperative Diagnosis, Postprocedure Diagnosis |
| Procedures/Devices (5) | Procedures, Implants, Planned Procedure, Procedure Indications, Procedure Description |
| Care Planning (6) | Assessments, Plan of Care, Goals Section, Health Concerns Section, Interventions Section, Health Status Evaluations/Outcomes Section |
| Medications (2) | Medications, Discharge Medications |
| Encounters/Visits (4) | Encounters, Reason For Visit/Chief Complaint, Hospital Discharge Instructions, General Status |
| Vitals/Labs (2) | Vital Signs, Results |
| Allergies (1) | Allergies and Adverse Reactions |
| Immunizations (1) | Immunizations |
| Social/Family History (3) | Social History, Family History, Past Medical History |
| Functional/Mental (3) | Functional Status, Mental Status, Reason for Referral |
| Financial/Payer (2) | Payers, Financial Data |
| Security (1) | Security and Privacy Prohibitions |
| Other (1) | Complications |

The "Payers" and "Financial Data" sections are notable — they go beyond the typical clinical-only CDA. However, CDA's capacity to represent detailed billing, claims, RCM, and A/R data is extremely limited. Standard CDA payer sections typically contain insurance coverage information (plan name, subscriber ID), not detailed claims, charge line items, payments, or denial records.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**For Pulse Systems Inc. (v8.02)**: It is impossible to assess what the export covers because no documentation exists. The EHI export link points to an external HL7 standards page with no vendor-specific content.

**For CHS/Pulse v16.1 (reference only)**: The CDA-based export covers 44 sections that span clinical documentation comprehensively — notes, diagnoses, medications, procedures, vitals, labs, allergies, immunizations, care plans, and social/family history. It includes "Payers" and "Financial Data" sections, but the depth of financial coverage in a CDA document is structurally limited. The document explicitly acknowledges that "some electronic health information might not be available in a format, such as rich text documents or images."

The CDA format is fundamentally a clinical document exchange standard. It is designed for sharing narrative clinical documents with some coded data — not for exporting an entire EHR database. A CDA document cannot meaningfully represent scheduling data, claims management records, A/R aging, denial tracking, payment posting, eligibility verification results, quality measure calculations, or patient portal communications.

### 5b. Standardized domain coverage (top-down)

The following assessment is based on the CHS document (the only available evidence), noting that this describes a different product version. For the actual certified product (Pulse Systems v8.02), coverage cannot be assessed due to absent documentation.

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CDA header contains patient demographics by standard; no field-level detail in documentation | CDA headers typically include name, DOB, gender, address, but may not include all registration fields the PM system stores |
| Encounters / visits | ⚠️ Partial | "Encounters" CDA section listed | CDA encounter section is typically a list of visit dates/types; unlikely to capture full encounter detail from PM/scheduling |
| Problems / conditions | ✅ Covered | "Problems," "Hospital Discharge Diagnosis," "Admission Diagnosis," "PreOperative Diagnosis," "Postprocedure Diagnosis" sections | Multiple diagnosis-related sections suggest reasonable coverage |
| Medications / prescriptions | ⚠️ Partial | "Medications," "Discharge Medications" sections | Standard CDA medication lists; unclear if full e-prescribing history (Surescripts transactions) is captured |
| Allergies | ✅ Covered | "Allergies and Adverse Reactions" section | Standard CDA allergy section |
| Immunizations | ✅ Covered | "Immunizations" section | Standard CDA immunization section |
| Vitals | ✅ Covered | "Vital Signs" section | Standard CDA vitals |
| Lab results | ✅ Covered | "Results" section | Standard CDA results section |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated imaging section; may be in "Results" | Product supports CPOE for diagnostic imaging; unclear if reports are in export |
| Procedures | ✅ Covered | "Procedures," "Planned Procedure," "Procedure Indications," "Procedure Description," "Procedure Note" sections | Strong procedural coverage with 5 dedicated sections |
| Clinical notes / documents | ✅ Covered | 8 note-type sections (Progress Note, H&P components, Consultation Note, Discharge Summary, etc.) | Comprehensive note coverage in CDA format |
| Care plans / goals | ✅ Covered | "Plan of Care," "Goals Section," "Health Concerns Section," "Interventions Section," "Assessments" | Multiple care planning sections |
| Orders / referrals | ⚠️ Partial | "Reason for Referral" section listed; no explicit orders section | CPOE orders (labs, meds, imaging) are a core product feature; no dedicated orders section in export |
| Insurance / coverage | ⚠️ Partial | "Payers" section listed | CDA payer sections typically contain plan-level info (name, subscriber ID), not detailed eligibility or coverage details |
| Claims / billing | ❌ Not covered | "Financial Data" section listed, but CDA cannot represent claims, charge line items, payment posting, A/R, or denial data | Product includes PulsePro billing/coding and PulseRCM claims management — **significant gap** |
| Payments | ❌ Not covered | No evidence of payment data in CDA export | Product supports payment posting and reconciliation; not in export |
| Consents / directives | ⚠️ Partial | "Security and Privacy Prohibitions" section | May contain consent/directive data, but section name suggests privacy restrictions rather than advance directives |
| Patient communications / portal messages | ❌ Not covered | No section for portal messages | Product integrates InteliChart patient portal; portal data not in export |
| Specialty-specific data | ⚠️ Partial | No dedicated specialty sections | Product serves urology, GI, orthopedics, oncology, etc. with customizable flow sheets; unclear if custom data is captured in CDA |

**Summary**: Of 18 applicable domains, 7 are covered, 8 are partial, and 3 are not covered. The most significant gaps are in billing/claims/RCM (core product functionality via PulsePro and PulseRCM), payments, and patient portal communications.

## 6. Documentation Quality

**For the certified product (Pulse Systems v8.02)**: Documentation quality is **essentially zero**. The vendor's registered EHI export documentation link points to an external HL7 standards page (`https://www.hl7.org/fhir/us/core/uscdi.html`) that has nothing to do with their product's export. There is no data dictionary, no schema, no user guide, no sample data, and no format specification. A developer would have no basis to understand, import, or process the export.

The single sentence on the certification page ("can create a set of export summaries in real time") is the entirety of what Pulse Systems provides about its (b)(10) export.

**For the CHS document (different product)**: The 6-page DOCX provides a section-name-level inventory (44 CDA section names in a single-column table) and a partial XML snippet. There are no field-level definitions, no data types, no value sets, no relationships, and no import guidance. It provides slightly more than nothing — a developer would know the export is CDA XML and could identify section names, but would need to rely entirely on the CDA standard for parsing.

**Machine-readable artifacts**: None. No JSON schema, no sample export file, no data dictionary in any parseable format.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The certified product (Pulse Systems v8.02) has no EHI export documentation whatsoever. The EHI export link on the mandatory disclosures page points to an irrelevant external standards page. The only substantive export documentation found anywhere is a 6-page Word document from CHS.net describing a different product (Pulse v16.1) by a different developer (Community Health Systems), which reveals a CDA-based export — a clinical document standard being repurposed as a (b)(10) export.

### Key Findings

1. **The vendor's EHI export documentation link is a dead end.** Pulse Systems' "View Electronic Health Information Export Documentation" link points to `https://www.hl7.org/fhir/us/core/uscdi.html` — the HL7 FHIR US Core USCDI page. This is an external standards reference about USCDI data classes and FHIR profiles, not vendor-specific export documentation. Verified by direct web fetch and corroborated by screenshot evidence (`screenshot-ehi-export-link-target.png`).

2. **No EHI export documentation exists on the vendor's website.** I searched the full pulseinc.com sitemap (14 pages) and the harrisambulatory.com domain — no EHI export documentation was found anywhere. The certification page contains a single sentence about "export summaries" with zero technical detail.

3. **The only EHI export documentation found is for a different product.** The CHS-hosted document (`Pulse-EHI-Export-Document-REV-06142024.docx`) describes Pulse v16.1, developed and maintained by Community Health Systems for internal hospital use. CHS's own website says this is "not commercially available technology." This is a separate CHPL listing (10360), not the Pulse Systems Inc. v8.02 product (CHPL 11500).

4. **The CHS document reveals a CDA-based export** with 44 CDA sections — a clinical document standard being used as a (b)(10) mechanism. CDA is structurally incapable of representing billing, claims, RCM, scheduling, quality measures, or patient portal data that Pulse EHR stores. The document acknowledges "some electronic health information might not be available."

5. **The vendor appears to conflate (b)(10) with (g)(10)/USCDI.** Pointing the EHI export link to the USCDI page suggests the vendor equates the (b)(10) "all EHI" export requirement with the (g)(10) USCDI/FHIR API requirement — a fundamentally different and much narrower scope.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Unknown (likely CDA XML based on CHS reference doc)
Model type:      Standard projection (CDA)
Entities:        N/A (no data dictionary for certified product)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear ("mass export" mentioned but undocumented)
Domains covered: Cannot assess — no documentation for certified product
```

### Bottom Line

Pulse Systems Inc. provides no EHI export documentation for its certified product. The "View Electronic Health Information Export Documentation" link on the mandatory disclosures page redirects to an external HL7 standards page, not vendor documentation. The only EHI export documentation that exists anywhere for any Pulse product is a brief CHS-hosted document for a different version by a different developer, describing a CDA-based export that structurally cannot capture the billing, claims, RCM, and practice management data that Pulse EHR stores. This is one of the weakest (b)(10) implementations possible — the vendor has not even provided documentation, let alone a comprehensive export.

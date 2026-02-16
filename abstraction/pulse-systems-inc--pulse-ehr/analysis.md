# EHI Export Analysis: Pulse Systems, Inc

**Product**: Pulse EHR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2837.Puls.08.03.1.240806 (CHPL ID 11500)

## 1. Product Context

Pulse EHR is an integrated ambulatory EHR and practice management platform from Pulse Systems, Inc (now part of Harris Ambulatory Care Enterprise / N. Harris Computer Corporation). The certified product is version 8.02 (certified 2024-08-06).

The product suite includes:
- **Pulse EHR**: Clinical documentation, CPOE, e-prescribing (Surescripts Gold), clinical notes with customizable flow sheets, "Pulse Note" clinical knowledge engine
- **PulsePro (Practice Management)**: Scheduling, patient registration, billing/coding, claims processing, insurance eligibility verification, A/R tracking, payment posting, denial management
- **PulseRCM (Revenue Cycle Management)**: Claims management, certified coding, denial root cause analysis
- **Patient Portal**: Via InteliChart partnership — secure messaging, health records access, lab results
- **Population Health**: CQM module, care gaps, MACRA/MIPS reporting, chronic care management

The product targets ambulatory practices across many specialties (primary care, urology, gastroenterology, orthopedics, cardiology, oncology, behavioral health, pediatrics, etc.) from solo practices to multi-site groups and ASCs.

**Baseline for export assessment**: A complete (b)(10) export should cover clinical documentation, medications, labs, vitals, allergies, immunizations, problems, procedures, encounters, care plans, referrals, insurance/coverage, billing/claims data, scheduling, patient communications, custom forms/flow sheets, and scanned documents/faxes.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Pulse-EHI-Export-Document-REV-06142024.docx` (164 KB) | CHS/CereCore-hosted EHI export document for Pulse v16.1. Lists 44 CDA sections (46 before dedup). Contains a sample CDA XML screenshot. **Only substantive EHI export documentation found.** | **Most informative** — sole source of export content detail |
| `downloads/Pulse-8.0-API-FHIR-Documentation.pdf` (41 pages, 597 KB) | §170.315(g)(10) FHIR R4 API documentation. Covers ~19 US Core resource types. This is the (g)(10) API, not (b)(10). | Useful for comparison — shows what the FHIR API covers |
| `downloads/Pulse_CommonClinicalDataAPI-002.pdf` (10 pages, 430 KB) | Proprietary REST API for CCD/CCDA retrieval. Not related to (b)(10). | Low — unrelated to EHI export |
| `downloads/screenshot-certification-page-full.png` (694 KB) | Full screenshot of pulseinc.com certification page showing three documentation links | **Key evidence** — shows the "View Electronic Health Information Export Documentation" link |
| `downloads/screenshot-ehi-export-link-target.png` (222 KB) | Screenshot proving the EHI export link leads to HL7 FHIR US Core USCDI page (external standard) | **Key evidence** — confirms vendor provides no actual EHI export documentation |
| `downloads/screenshot-certification-page-top.png` (246 KB) | Top portion of certification page | Minor supporting context |

## 3. Export Mechanics

- **Format**: CDA XML (Clinical Document Architecture) — a "Summarization of Episode Note" document (LOINC 34133-9), essentially a C-CDA/CCD document
- **Mechanism**: Per the CHS document, an "EHI Tables export" generates the CDA XML document. The pulseinc.com certification page states: "Pulse EHR is certified to data export criteria and can create a set of export summaries in real time."
- **Single-patient vs bulk**: Described as single-patient export ("a patient's Pulse record"). Bulk export is implied possible but "recommended as best practice to be scheduled during off-peak hours to reduce performance stress on the system."
- **Access constraints**: No specific fees listed for the export itself. The pulseinc.com page lists costs for other features (e-prescribing, patient portal) but not for EHI export.
- **Viewer**: CDA.xsl stylesheet from HL7 GitHub for human-readable rendering

**Critical caveat**: The export documentation is from a CHS/CereCore deployment of Pulse v16.1, which is a different version line than the certified Pulse Systems v8.02 product. The export behavior may differ.

## 4. Export Content: What's In It

### Documentation structure

The only substantive documentation is the CHS-hosted DOCX (3 pages of content after TOC/cover). It provides:
- A brief prose description of the export
- A single-column table listing CDA section names (no field-level detail)
- A screenshot of sample CDA XML showing the document header

There is **no data dictionary**, **no field-level documentation**, **no schema**, and **no description of what data elements appear within each CDA section**. The documentation relies entirely on the CDA standard itself to define content.

### Vendor's own content organization

The vendor organizes content as CDA sections. After deduplication (Health Concerns Section and Goals Section each appeared twice), there are **44 unique CDA sections**:

| CDA Section | Domain Category |
|---|---|
| Security and Privacy Prohibitions | Administrative |
| Allergies and Adverse Reactions | Allergies |
| Medications | Medications |
| Discharge Medications | Medications |
| Problems | Problems/Diagnoses |
| Hospital Discharge Diagnosis | Problems/Diagnoses |
| Admission Diagnosis | Problems/Diagnoses |
| Encounters | Encounters |
| Procedures | Procedures |
| Planned Procedure | Procedures |
| PreOperative Diagnosis | Procedures |
| Postprocedure Diagnosis | Procedures |
| Procedure Indications | Procedures |
| Procedure Description | Procedures |
| Procedure Note | Procedures |
| Implants | Medical Devices |
| Immunizations | Immunizations |
| Vital Signs | Vitals |
| Social History | Social History |
| Results | Lab Results |
| Functional Status | Health Status |
| Mental Status | Health Status |
| Health Status Evaluations/Outcomes Section | Health Status |
| Assessments | Assessments |
| Plan of Care | Care Plans/Goals |
| Goals Section | Care Plans/Goals |
| Health Concerns Section | Care Plans/Goals |
| Interventions Section | Care Plans/Goals |
| Hospital Discharge Instructions | Clinical Notes |
| Reason For Visit/Chief Complaint | Clinical Notes |
| General Status | Clinical Notes |
| Past Medical History | Clinical Notes |
| History Of Present Illness | Clinical Notes |
| Physical Examination | Clinical Notes |
| Review Of Systems | Clinical Notes |
| Progress Note | Clinical Notes |
| Complications | Clinical Notes |
| Hospital Course | Clinical Notes |
| Discharge Summary Note | Clinical Notes |
| Consultation Note | Clinical Notes |
| Reason for Referral | Referrals |
| Family History | Family History |
| Payers | Insurance/Coverage |
| Financial Data | Billing/Financial |

**No field-level detail is available for any section.** The documentation provides section names only — there are zero documented fields, zero field descriptions, zero type definitions, and zero value sets. The entire content specification defers to the CDA standard.

The sample XML screenshot (embedded in the DOCX as image3.png, 114 KB) shows a standard CDA header with:
- Patient demographics (name, address, phone, gender)
- Document metadata (LOINC code 34133-9, effective time, confidentiality code)
- Organization: "COMMUNITY HEALTH HOSPITALS"
- Patient ID with CHS-specific OID

This confirms the export is a standard C-CDA "Summarization of Episode" document — the same format used for clinical document exchange.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export lists 44 CDA sections spanning clinical notes (12 sections), procedures (7 sections), care plans/goals (4 sections), problems/diagnoses (3 sections), health status (3 sections), medications (2 sections), and single sections each for allergies, encounters, devices, immunizations, vitals, social history, lab results, assessments, family history, referrals, insurance/coverage, and financial data.

The clinical note coverage is extensive — progress notes, H&P components, discharge summaries, consultation notes, operative notes, and procedure notes are all represented. This breadth of clinical note sections is the strongest aspect of the export.

The "Payers" and "Financial Data" sections are notable inclusions that go beyond typical C-CDA clinical summaries. However, CDA sections for these domains are extremely limited in what they can represent — CDA was not designed for billing/financial data. The "Payers" section in CDA typically contains basic insurance identification (payer name, ID, policy type), not claims, charges, payments, or A/R data. "Financial Data" is not a standard CDA section at all, and without any documentation of what it contains, its depth is unknown.

The document explicitly acknowledges limitations: "Some electronic health information might not be available in a format, such as rich text documents or images."

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CDA header contains patient name, address, phone, gender (visible in XML sample). No dedicated demographics section. | CDA headers carry basic demographics but likely miss extended fields the PM system stores (emergency contacts, employer, preferred pharmacy, language, race/ethnicity detail). |
| Encounters / visits | ⚠️ Partial | "Encounters" section listed | Single CDA section; unlikely to capture full encounter detail from PM system (scheduling, check-in/out, visit types, billing encounters). |
| Problems / conditions | ✅ Covered | "Problems", "Hospital Discharge Diagnosis", "Admission Diagnosis" sections | Three dedicated sections provide reasonable coverage. |
| Medications / prescriptions | ✅ Covered | "Medications", "Discharge Medications" sections | Clinical medication data likely covered; but e-prescribing transaction history (Surescripts logs) likely not included. |
| Allergies | ✅ Covered | "Allergies and Adverse Reactions" section | Standard CDA coverage. |
| Immunizations | ✅ Covered | "Immunizations" section | Standard CDA coverage. |
| Vitals | ✅ Covered | "Vital Signs" section | Standard CDA coverage. |
| Lab results | ✅ Covered | "Results" section | Standard CDA coverage for results; may miss order details. |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated imaging section; may be within "Results" | Product has diagnostic imaging CPOE; imaging reports not explicitly listed. |
| Procedures | ✅ Covered | 7 procedure-related sections (Procedures, Planned Procedure, PreOp/PostOp Diagnosis, Indications, Description, Note) | Strongest clinical coverage area. |
| Clinical notes / documents | ✅ Covered | 12 clinical note sections (Progress Note, H&P components, Discharge Summary, Consultation Note, etc.) | Extensive clinical note coverage. |
| Care plans / goals | ✅ Covered | "Plan of Care", "Goals Section", "Health Concerns Section", "Interventions Section" | Good coverage. |
| Orders / referrals | ⚠️ Partial | "Reason for Referral" section only | No dedicated orders section. Product has CPOE for meds, labs, imaging — order details beyond what's captured in result/procedure sections are likely missing. |
| Insurance / coverage | ⚠️ Partial | "Payers" section listed | CDA Payers section typically contains basic insurance ID only — payer name, policy number, group. Full coverage details, eligibility responses, prior authorizations from PM system likely not included. |
| Claims / billing | ⚠️ Partial | "Financial Data" section listed | Not a standard CDA section. Unknown depth. CDA cannot meaningfully represent claims, charge detail, CPT/HCPCS line items, claim status, denials, or A/R data. Product has extensive billing/RCM capabilities (PulsePro, PulseRCM) — this is likely a significant gap. |
| Payments | ❌ Not covered | No payment-related section | Product handles payment posting, reconciliation, denial refiling. No evidence in export. |
| Consents / directives | ❌ Not covered | No consent or advance directive section | Not explicitly listed. |
| Patient communications / portal messages | ❌ Not covered | No messaging section | Product has patient portal (InteliChart) with secure messaging. Not in export. |
| Custom forms / flow sheets | ❌ Not covered | No custom form section | "Customizable flow sheets" are a key Pulse feature. CDA cannot represent arbitrary custom form structures. |
| Scanned documents / faxes | ❌ Not covered | No document management section | Product has integrated document, fax, and transcription management. Explicitly acknowledged as potentially missing: "rich text documents or images." |
| Specialty-specific data | ❌ Not covered | No specialty sections | Product serves multiple specialties (urology, GI, orthopedics, oncology, behavioral health). No specialty-specific clinical data sections beyond generic CDA. |

## 6. Documentation Quality

**From Pulse Systems directly: Nonexistent.** The vendor's registered (b)(10) documentation link (`pulseinc.com/terms-conditions-certification-costs-and-limitations/`) has a "View Electronic Health Information Export Documentation" button that links to `https://www.hl7.org/fhir/us/core/uscdi.html` — the HL7 FHIR US Core USCDI page. This is an external standards reference page about USCDI data classes, not vendor-specific EHI export documentation. This was verified via screenshot (`screenshot-ehi-export-link-target.png`). The vendor provides zero proprietary documentation about what their (b)(10) export contains, how to use it, or what data is included.

**From CHS/CereCore (third-party)**: The only actual export documentation is a 3-page DOCX hosted by Community Health Systems for Pulse v16.1 (a different version than the certified v8.02). It provides:
- ✅ A list of CDA section names (44 sections)
- ✅ A sample XML header screenshot
- ✅ A reference to the CDA.xsl stylesheet for rendering
- ❌ No field-level definitions
- ❌ No data types, value sets, or constraints
- ❌ No instructions for performing the export
- ❌ No description of what's in the "Financial Data" section
- ❌ No schema or machine-readable specification
- ❌ No sample data files

**Could a developer build an import?** No. A developer receiving this export would get a CDA XML document and would need to know the CDA standard to parse it. The vendor documentation provides no guidance on Pulse-specific data elements, extensions, or limitations within each section. The "Financial Data" section — potentially the most important for (b)(10) differentiation — has zero documentation about its contents.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers clinical data domains reasonably well through 44 CDA sections — problems, medications, allergies, immunizations, vitals, labs, procedures, and clinical notes are all represented with multiple dedicated sections. The inclusion of "Payers" and "Financial Data" sections suggests an attempt to go beyond pure clinical exchange. However, Pulse is an integrated EHR/PM/RCM platform with extensive billing, scheduling, claims management, and revenue cycle capabilities. CDA as a format fundamentally cannot represent most of this data. The export likely captures the clinical record well but misses the practice management, billing/RCM, custom form, and specialty data that constitute a significant portion of the patient's designated record set in an ambulatory PM/EHR system.

**Axis 2 — Export approach: Repackaged existing export**

Multiple signals indicate this is an existing C-CDA/CCD export relabeled as (b)(10):

1. **The vendor's own EHI export link points to the HL7 US Core USCDI page** — not to any vendor-specific documentation. This conflates the (g)(10) FHIR API / USCDI scope with the (b)(10) EHI export requirement, suggesting the vendor views them as equivalent.

2. **The export format is CDA XML with LOINC code 34133-9 ("Summarization of Episode Note")** — this is the exact same document type used for C-CDA clinical document exchange under (g)(6)/(g)(9). The sample XML header confirms this is a standard Continuity of Care Document.

3. **The CDA sections map almost exactly to C-CDA templates** — the 44 sections are standard C-CDA sections (problems, medications, allergies, results, procedures, etc.) with no vendor-specific extensions documented.

4. **No product-specific data dictionary exists** — the vendor defers entirely to the CDA standard for content specification, which is what you'd expect if they're reusing an existing C-CDA export.

5. **The CHS document calls it "EHI Tables export"** but the output is a single CDA document, not a set of data tables — the naming is contradictory.

The "Financial Data" section is the one element that might suggest purpose-built effort, but without any documentation of its contents and given CDA's fundamental limitations for financial data, this is likely either empty/minimal or contains only basic charge information. It is not sufficient to reclassify the export as purpose-built.

### Key Findings

1. **Vendor provides no actual EHI export documentation.** The registered "View Electronic Health Information Export Documentation" link redirects to the HL7 FHIR US Core USCDI page — an external standard reference, not vendor documentation. This is verified by screenshot evidence (`screenshot-ehi-export-link-target.png`).

2. **The only substantive documentation comes from a third party (CHS/CereCore) for a different product version** (v16.1 vs. certified v8.02). This document was not created by Pulse Systems and may not reflect the certified product's actual export.

3. **The export is a C-CDA document (Summarization of Episode Note)** — the same clinical document exchange format used for (g)(6)/(g)(9) interoperability. The sample XML confirms LOINC code 34133-9 and standard CDA structure.

4. **Zero field-level documentation exists.** The entire export specification is a list of 44 CDA section names with no fields, types, descriptions, value sets, or relationships documented.

5. **Billing, scheduling, custom forms, patient communications, and specialty data are absent or questionable.** The product has extensive PM/RCM capabilities (PulsePro, PulseRCM) but the CDA format cannot meaningfully export claims, A/R, denial management, payment posting, or scheduling data.

### Summary Stats

    Coverage:        Partial
    Approach:        Repackaged existing export
    Export format:   CDA XML (C-CDA Summarization of Episode Note)
    Entities:        44 CDA sections (no field-level breakdown)
    Fields:          N/A (no field-level documentation)
    Descriptions:    N/A
    Sample data:     Partial (one XML header screenshot in DOCX)
    Bulk export:     Unclear (single-patient described; bulk implied possible)
    Domains covered: 10 of 18 applicable domains (with several only partially covered)

### Bottom Line

Pulse Systems provides effectively no (b)(10) documentation — their official link points to an external HL7 standards page. The only evidence of the export's contents comes from a third-party document describing a different version, which reveals a standard C-CDA clinical summary being relabeled as an EHI export. For a product with integrated practice management and revenue cycle management, the absence of billing, claims, scheduling, custom form, and specialty data from the export represents a significant gap between what Pulse stores and what it exports.

# Pulse Systems, Inc — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://pulseinc.com/terms-conditions-certification-costs-and-limitations/
- CHPL IDs: 11500
- Product: Pulse EHR v8.02
- Developer: Pulse Systems, Inc (part of Harris Ambulatory Care Enterprise)

## Navigation Journal

### Step 1: Initial probe
```bash
curl -sI -L "https://pulseinc.com/terms-conditions-certification-costs-and-limitations/" -H 'User-Agent: Mozilla/5.0'
```
HTTP/2 200, Content-Type: text/html; charset=UTF-8. WordPress site on Hostinger/LiteSpeed.

### Step 2: Examine the page
The page is titled "Certification, Costs and Disclosures." It contains:
- ONC certification statement for Pulse EHR v8.0.2 (CHPL ID: 15.04.04.2837.Puls.08.02.1.231206, certified Dec 6, 2023)
- Full list of certified criteria including 170.315 (b)(10): Electronic Health Information Export
- Cost disclosures for various features
- Three documentation links at the bottom

### Step 3: Documentation links found
The page has three yellow-colored links at the bottom:

1. **"View API Documentation"** → `https://pulseinc.com/wp-content/uploads/2024/06/63b433c15bacad3a0c435e8c_Pulse_CommonClinicalDataAPI-002.pdf`
   - A 10-page PDF describing a proprietary REST API for retrieving Common Clinical Data (CCD/CCDA documents). Version 1.0, dated 11/21/2022. Authored by Rob Sprague. This is a custom (non-FHIR) API that uses POST requests, returns base64-encoded XML CCD documents. It requires practice-provided credentials and uses OAuth 2.0.

2. **"View FHIR API Documentation"** → `https://harrisambulatory.com/pulse-api-documentation/`
   - Links to the Harris Ambulatory Care Enterprise page for Pulse's §170.315(g)(10) FHIR API documentation. That page links to a 41-page PDF (`Pulse-8.0-API-FHIR-Documentation.pdf`) describing the FHIR R4 API with US Core profiles. Published endpoint: `https://hag-fhir.amazingcharts.com/pl/endpoints`.

3. **"View Electronic Health Information Export Documentation"** → `https://www.hl7.org/fhir/us/core/uscdi.html`
   - **This link goes to HL7.org's FHIR US Core USCDI page** — an external standards reference, not vendor-specific documentation. This is NOT actual EHI export documentation. Confirmed by navigating in browser and taking a screenshot showing the HL7 FHIR US Core USCDI page.

### Step 4: Checked /certification/ page
```bash
curl -sL "https://pulseinc.com/certification/" -H 'User-Agent: Mozilla/5.0'
```
This page contains version 8.0.1 certification info with the same EHI export link pointing to the HL7 USCDI page. No additional EHI export documentation found here.

### Step 5: Broader site search
- Checked sitemap (`/page-sitemap.xml`): 14 pages total, none related to EHI export documentation.
- Web search for `site:pulseinc.com "EHI export"` found only the certification pages.

### Step 6: External discovery — CHS EHI Export Document
A web search for `"Pulse Systems" OR "Pulse EHR" "EHI export" documentation` revealed that Community Health Systems (CHS), which deploys Pulse EHR internally, has an EHI export documentation page at `https://www.chs.net/pulse-ehr-information/`.

That page hosts a Word document: `Pulse-EHI-Export-Document-REV-06142024.docx` (163 KB). This document is branded as "CHS / CereCore" and describes the EHI export for Pulse version 16.1 (a different version than the Pulse Systems Inc. v8.02 certified product). However, it provides the only substantive description of how Pulse's EHI export actually works.

```bash
curl -sL "https://www.chs.net/_assets/docs/Pulse-EHI-Export-Document-REV-06142024.docx" -H 'User-Agent: Mozilla/5.0' -o Pulse-EHI-Export-Document-REV-06142024.docx
```

## What Was Found

### Pulse Systems' own documentation (at the registered URL)
The registered URL provides **no actual EHI export documentation**. The "View Electronic Health Information Export Documentation" link redirects to the HL7 FHIR US Core USCDI page — an external standard, not vendor-specific export documentation. There is no data dictionary, no export format specification, no user guide, and no schema describing the (b)(10) export.

The only relevant content on the page itself is a single sentence under "Costs and Disclosures":
> "Pulse EHR is certified to data export criteria and can create a set of export summaries in real time. Though the user can create a set of export summaries in real time, this type of mass export is recommended as best practice to be scheduled during off-peak hours to reduce performance stress on the system."

This tells us the export exists and can be run in real time, but provides zero technical detail.

### CHS-hosted EHI Export Document (external, different version)
The CHS-hosted `Pulse-EHI-Export-Document-REV-06142024.docx` (created May 2023, revised Sep 2023) describes the export as:

- **Format**: XML document using Clinical Document Architecture (CDA) standard
- **Mechanism**: "EHI Tables export" that generates a computable XML CDA document containing the electronic health information in a patient's Pulse record
- **Limitations acknowledged**: "Some electronic health information might not be available in a format, such as rich text documents or images"
- **Variability factors**: Content varies based on software applications in use, documentation/use practices, and configuration decisions
- **Viewer**: CDA.xsl stylesheet from HL7 GitHub for human-readable rendering

The document lists CDA sections included in the export:

| Section | Included |
|---------|----------|
| Security and Privacy Prohibitions | ✓ |
| Allergies and Adverse Reactions | ✓ |
| Medications | ✓ |
| Discharge Medications | ✓ |
| Problems | ✓ |
| Hospital Discharge Diagnosis | ✓ |
| Encounters | ✓ |
| Admission Diagnosis | ✓ |
| Procedures | ✓ |
| Implants | ✓ |
| Immunizations | ✓ |
| Vital Signs | ✓ |
| Social History | ✓ |
| Results | ✓ |
| Functional Status | ✓ |
| Mental Status | ✓ |
| Assessments | ✓ |
| Plan of Care | ✓ |
| Goals Section | ✓ |
| Health Concerns Section | ✓ |
| Hospital Discharge Instructions | ✓ |
| Family History | ✓ |
| Reason For Visit/Chief Complaint | ✓ |
| General Status | ✓ |
| Past Medical History | ✓ |
| History Of Present Illness | ✓ |
| Physical Examination | ✓ |
| Review Of Systems | ✓ |
| Progress Note | ✓ |
| PreOperative Diagnosis | ✓ |
| Postprocedure Diagnosis | ✓ |
| Planned Procedure | ✓ |
| Complications | ✓ |
| Procedure Indications | ✓ |
| Procedure Description | ✓ |
| Procedure Note | ✓ |
| Reason for Referral | ✓ |
| Hospital Course | ✓ |
| Health Concerns Section | ✓ |
| Goals Section | ✓ |
| Interventions Section | ✓ |
| Health Status Evaluations/Outcomes Section | ✓ |
| Discharge Summary Note | ✓ |
| Consultation Note | ✓ |
| Payers | ✓ |
| Financial Data | ✓ |

The document includes a sample XML CDA fragment at the end, showing the XML structure of the export.

### FHIR API documentation (g)(10), not (b)(10)
Two API documents were found:
1. **Pulse Common Clinical Data API** (10pp PDF): Proprietary REST API for CCD retrieval, not FHIR-based
2. **Pulse 8.0 API FHIR Documentation** (41pp PDF): Standard FHIR R4/US Core API for (g)(10) compliance. Covers standard US Core resources only (AllergyIntolerance, CarePlan, CareTeam, DocumentReference, Encounter, Goal, Condition, Immunization, DiagnosticReport, Medication, Patient, Procedure, Provenance, Observation, ImplantableDevice, Vital Signs, etc.)

Neither of these constitutes (b)(10) EHI export documentation.

## Export Coverage Assessment

### Data Domain Coverage
Based on the CHS-hosted document (the only substantive export documentation found), the EHI export uses CDA format which covers a broad range of **clinical** data domains. The section list is extensive — approximately 44 CDA sections covering clinical notes, diagnoses, procedures, medications, allergies, immunizations, vitals, and more.

Notably, the export includes "Payers" and "Financial Data" sections, which goes beyond the typical clinical-only export. However, based on what the product research tells us Pulse stores, significant data domains are likely missing or inadequately represented:

**Likely covered (based on CDA sections listed):**
- Patient demographics (implied by CDA header)
- Clinical notes and encounter documentation
- Medication lists and prescriptions
- Laboratory results
- Vital signs
- Problem lists and diagnoses
- Allergies
- Immunizations
- Procedures
- Implantable devices
- Family history
- Social history
- Care plans and goals
- Payer/insurance data
- Financial data (section listed but unclear depth)

**Likely missing or uncertain:**
- **Scheduling and appointment data** — not represented in CDA sections
- **Billing, claims, and detailed financial data** — "Financial Data" section listed but CDA is a clinical document standard; depth of billing/RCM data is highly questionable
- **Practice management data** — A/R tracking, claims management, denial data, payment posting
- **Quality measure data** — CQM module data, MIPS/MACRA submissions
- **Audit logs** — not represented in CDA
- **Patient portal messages** — InteliChart integration data
- **Scanned documents, faxes, transcriptions** — document management content
- **E-prescribing history** — Surescripts transaction logs
- **Clinical decision support rules** — configuration data
- **Custom flow sheet data** — "customizable flow sheets" are a key Pulse feature; unclear if CDA captures the full custom data structures

### Export Format & Standards
The export uses **Clinical Document Architecture (CDA)** — an XML-based HL7 standard for clinical documents. This is a recognized standard, but it's fundamentally a **clinical document exchange format**, not a database export format.

CDA is designed for document exchange between healthcare systems. It excels at representing narrative clinical content with some coded data. However, it is a poor fit for exporting **all** electronic health information from a system that also manages billing, scheduling, practice management, revenue cycle, and population health data. CDA simply cannot represent most of these data domains — there is no CDA section for "claims denials" or "A/R aging" or "appointment schedules."

This approach is essentially using the (g)(6) Consolidated CDA export capability to satisfy (b)(10), which is a common vendor shortcut that fails to capture the full breadth of data the system stores.

The CHS document acknowledges this limitation: "Some electronic health information might not be available in a format, such as rich text documents or images."

### Documentation Quality
**From Pulse Systems Inc. directly: Essentially nonexistent.** The registered URL's "View Electronic Health Information Export Documentation" link points to an external HL7 standards page. There is no vendor-specific data dictionary, no export format specification, no field-level documentation, no user guide, and no sample files hosted by Pulse Systems.

**From CHS (external, different version):** The document is brief (6 pages including cover page and table of contents). It provides a useful list of CDA sections and a sample XML snippet, but lacks:
- Field-level definitions within each section
- Data types, value sets, or constraints
- Instructions for performing the export
- Explanation of how non-clinical data is handled
- Description of completeness relative to what the system stores

A developer receiving this export would know it's a CDA XML document and could identify the sections, but would need to rely entirely on the CDA standard itself for parsing — which is reasonable for a standards-based format. However, the documentation provides no guidance on Pulse-specific extensions, limitations, or data mapping.

### Structure & Completeness
- **Granularity**: Section-level only (lists CDA section names). No field-level documentation.
- **Value sets**: Not documented (defers to CDA standard).
- **Relationships**: Not documented (inherent in CDA structure).
- **Versioning**: Document dated May/Sep 2023; no change history.
- **Sample data**: One partial XML snippet included.

### Overall Assessment
This is one of the weakest (b)(10) implementations encountered. The vendor (Pulse Systems Inc.) has registered a mandatory disclosures URL that contains a "View Electronic Health Information Export Documentation" link pointing to an external HL7 standards page — not their own documentation. This is not a documentation oversight; it fundamentally misrepresents what the link leads to.

The only actual EHI export documentation for Pulse was found on a third-party site (CHS/CereCore) for a different product version (16.1 vs 8.02). That document reveals the export is a CDA XML document — a clinical document standard being used as a (b)(10) export mechanism. While CDA covers clinical data reasonably well, it cannot represent the scheduling, billing, practice management, revenue cycle, quality reporting, and administrative data that Pulse EHR stores and that (b)(10) is intended to capture.

The vendor appears to have conflated (b)(10) with clinical document exchange, pointing to USCDI/US Core (which is the (g)(10) domain) as their EHI export documentation. This suggests a fundamental misunderstanding of the (b)(10) requirement — or a deliberate decision to satisfy it minimally with existing clinical document capabilities rather than building a true comprehensive export.

## Access Summary
- Final URL (after redirects): https://pulseinc.com/terms-conditions-certification-costs-and-limitations/
- Status: found
- Required browser: no (page is static HTML, no JS required for content)
- Navigation complexity: direct_link (links are visible at bottom of page)
- Anti-bot issues: none

## Obstacles & Dead Ends
1. The "View Electronic Health Information Export Documentation" link on both the registered URL and `/certification/` pages points to `https://www.hl7.org/fhir/us/core/uscdi.html` — an external HL7 standards page, not vendor documentation.
2. No EHI export documentation found anywhere on pulseinc.com (checked sitemap, all pages).
3. No EHI export documentation found on harrisambulatory.com (only FHIR API docs).
4. The CHS-hosted document (`Pulse-EHI-Export-Document-REV-06142024.docx`) is for Pulse v16.1, which appears to be a different version line than the Pulse Systems v8.02 certified product. CHS uses Pulse internally and may have a customized deployment, so the export behavior described may not exactly match the Pulse Systems product.

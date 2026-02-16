# EHI Export Analysis: Pulse Systems, Inc

**Product**: Pulse EHR
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2837.Puls.08.03.1.240806 (CHPL ID 11500)

## 1. Product Context

Pulse EHR is an integrated electronic health records and practice management platform ("Pulse EHR/PM") developed by Pulse Systems, Inc., a Kansas City-based company now part of the Harris Ambulatory Care Enterprise (N. Harris Computer Corporation). The certified product (v8.02, certified 2024-08-06) targets ambulatory practices across multiple specialties including primary care, urology, gastroenterology, orthopedics, cardiology, and behavioral health.

The product stores data across several major domains relevant to EHI completeness:

- **Clinical documentation**: Customizable flowsheets, "Pulse Note" clinical intelligence engine, encounter templates, E&M coding
- **CPOE**: Medication, laboratory, and diagnostic imaging orders with drug interaction checking
- **E-prescribing**: Surescripts Gold Solution Provider integration
- **Practice management (PulsePro)**: Scheduling, patient registration, medical billing/coding, claims processing, insurance eligibility verification, A/R tracking, payment posting, denial management
- **Revenue cycle management (PulseRCM)**: Claims management, denial management, certified coding support
- **Patient engagement**: Patient portal via InteliChart, automated appointment reminders
- **Population health**: CQM tracking, care gaps, chronic care management, MIPS/MACRA support
- **Document management**: Fax, transcription, scanned document management

This breadth of functionality — particularly the deeply integrated billing, practice management, and RCM capabilities — sets a high bar for what a complete EHI export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `Pulse-EHI-Export-Document-REV-06142024.docx` (164 KB) | CHS/CereCore-branded EHI export document for Pulse v16.1. Lists 44 unique CDA sections. Contains sample XML as screenshot image. **Most informative artifact for (b)(10) — but from a different organization and version.** | ⭐ Most informative |
| `Pulse-8.0-API-FHIR-Documentation.pdf` (597 KB, 41 pp) | FHIR R4 API documentation for §170.315(g)(10). Documents 21 US Core FHIR resources. **Not EHI export documentation.** | Contextual only |
| `Pulse_CommonClinicalDataAPI-002.pdf` (430 KB, 10 pp) | Proprietary REST API for CCD/CCDA retrieval via POST with OAuth 2.0. **Not EHI export documentation.** | Contextual only |
| `screenshot-certification-page-full.png` (694 KB) | Full-page screenshot of pulseinc.com certification page showing three documentation links at bottom. | Confirms link placement |
| `screenshot-certification-page-top.png` (246 KB) | Top portion of certification page. | Minor |
| `screenshot-ehi-export-link-target.png` (222 KB) | Screenshot proving the "View Electronic Health Information Export Documentation" link leads to HL7.org's FHIR US Core USCDI page, not vendor documentation. | ⭐ Key evidence |

**Verification of prior report claims:**
- ✅ Confirmed: The vendor's "View Electronic Health Information Export Documentation" link at the registered URL points to `https://www.hl7.org/fhir/us/core/uscdi.html` (verified via curl and screenshot). This is an external HL7 standards reference page, not vendor-specific documentation.
- ✅ Confirmed: The certification page (HTTP 200 on 2026-02-16) contains the statement: "Pulse EHR is certified to data export criteria and can create a set of export summaries in real time."
- ✅ Confirmed: The CHS page (`https://www.chs.net/pulse-ehr-information`) is live (HTTP 200 after redirect) and still hosts the DOCX.
- ✅ Confirmed: The DOCX is branded CHS/CereCore (embedded logos: image1.png = CereCore logo, image2.png = CHS logo).
- ⚠️ Corrected: Prior report says "~44 CDA sections." Actual count is 46 raw entries in the table, of which 44 are unique (2 duplicates: "Goals Section" and "Health Concerns Section" each appear twice).
- ⚠️ Corrected: Prior report describes the document as "6 pages." The DOCX has no explicit page count metadata; it contains 38 non-empty paragraphs and 1 table across 2 heading sections plus front matter.
- ✅ Confirmed: The FHIR API PDF is 41 pages and the Common Clinical Data API PDF is 10 pages.

## 3. Export Mechanics

- **Format**: CDA XML (Clinical Document Architecture) — an HL7 standard for clinical document exchange
- **Mechanism**: Called "EHI Tables export" in the CHS document; the vendor's own certification page says "the user can create a set of export summaries in real time." Specific UI steps or API calls are not documented.
- **Single-patient vs bulk**: The vendor's certification page mentions "mass export" that "should be scheduled during off-peak hours to reduce performance stress," implying bulk capability exists but details are not provided.
- **Access constraints**: No fees or access constraints mentioned beyond system performance considerations.
- **Viewer**: CDA.xsl stylesheet from HL7 GitHub for human-readable rendering.

**Critical caveat**: The only documentation of the export mechanism comes from CHS (Community Health Systems) for Pulse v16.1 — a different certified product by a different developer. CHS's page explicitly states "This is not commercially available technology." Pulse Systems, Inc.'s own certification page provides no technical documentation whatsoever about how the (b)(10) export works for v8.02.

## 4. Export Content: What's In It

### Data dictionary assessment

There is **no data dictionary**. The CHS document provides only a single-column table of CDA section names — no fields, no data types, no descriptions, no relationships, no value sets, no constraints. The CDA standard itself defines the structure within each section, but the vendor provides no documentation of how Pulse data maps to CDA elements, what Pulse-specific extensions exist (if any), or which fields within each section are actually populated.

### CDA sections listed

The DOCX lists 44 unique CDA sections (46 raw entries with 2 duplicates). These sections are names only — there is zero field-level documentation within any section.

### Vendor's own content organization

The CHS document does not organize sections into categories. The table below maps each listed CDA section to a clinical domain based on standard CDA semantics:

| CDA Section | Mapped Domain |
|---|---|
| Security and Privacy Prohibitions | Administrative |
| Allergies and Adverse Reactions | Allergies |
| Medications | Medications |
| Discharge Medications | Medications |
| Problems | Problems / Conditions |
| Hospital Discharge Diagnosis | Problems / Conditions |
| Encounters | Encounters |
| Admission Diagnosis | Problems / Conditions |
| Procedures | Procedures |
| Implants | Implantable Devices |
| Immunizations | Immunizations |
| Vital Signs | Vitals |
| Social History | Social History |
| Results | Lab Results |
| Functional Status | Functional Status |
| Mental Status | Mental Status |
| Assessments | Assessments |
| PLAN OF CARE | Care Plans / Goals |
| Goals Section | Care Plans / Goals |
| Health Concerns Section | Problems / Conditions |
| Hospital Discharge Instructions | Clinical Notes |
| Family History | Family History |
| Reason For Visit/Chief Complaint | Clinical Notes |
| General Status | Clinical Notes |
| Past Medical History | Clinical Notes |
| History Of Present Illness | Clinical Notes |
| Physical Examination | Clinical Notes |
| Review Of Systems | Clinical Notes |
| Progress Note | Clinical Notes |
| PreOperative Diagnosis | Procedures |
| Postprocedure Diagnosis | Procedures |
| Planned Procedure | Procedures |
| Complications | Clinical Notes |
| Procedure Indications | Procedures |
| Procedure Description | Procedures |
| Procedure Note | Procedures |
| Reason for Referral | Orders / Referrals |
| Hospital Course | Clinical Notes |
| Interventions Section | Care Plans / Goals |
| Health Status Evaluations/Outcomes Section | Care Plans / Goals |
| Discharge Summary Note | Clinical Notes |
| Consultation Note | Clinical Notes |
| Payers | Insurance / Coverage |
| Financial Data | Claims / Billing |

### Sample data

The DOCX contains one sample XML fragment as a **screenshot image** (image3.png, 1617×836 px). The XML shows a standard CDA `<ClinicalDocument>` header with:
- Title: "Continuity of Care Document"
- Code: LOINC 34133-9 "Summarization of Episode Note"
- Organization: "COMMUNITY HEALTH HOSPITALS"
- Patient demographics: name, address, phone, gender in standard CDA `<recordTarget>` structure

This is a standard C-CDA/CCD header — no Pulse-specific extensions are visible. The sample shows only the document header, not the body sections that would contain clinical data. As an image, it is not machine-readable.

### FHIR API (not EHI export)

For context, the (g)(10) FHIR API documentation covers 21 US Core FHIR resource types. This represents standard USCDI clinical data and is explicitly the (g)(10) API, not the (b)(10) export. The resource types are: AllergyIntolerance, CarePlan, CareTeam, Condition, DocumentReference, DiagnosticReport, Encounter, Goal, Immunization, ImplantableDevice, Location, Medication, MedicationRequest, Observation, Organization, Patient, Practitioner, Procedure, Provenance, and Vital Signs.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The CHS document lists CDA sections covering clinical documentation broadly. The strongest coverage is in:

- **Clinical Notes**: 12 sections covering progress notes, H&P components, discharge summaries, consultation notes, procedure notes — this is the deepest area
- **Procedures**: 7 sections covering procedure descriptions, diagnoses, indications, and notes
- **Problems / Conditions**: 4 sections including problems, diagnoses, and health concerns
- **Care Plans / Goals**: 4 sections including plan of care, goals, interventions, and outcomes

The thinnest areas are:
- **Insurance / Coverage**: 1 section ("Payers") — section name only, no indication of depth
- **Claims / Billing**: 1 section ("Financial Data") — section name only, and CDA is fundamentally unsuited to represent detailed billing data

The document explicitly acknowledges limitations: "Some electronic health information might not be available in a format, such as rich text documents or images."

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CDA header contains patient demographics (visible in sample XML) but no dedicated CDA section listed | CDA header includes name, address, phone, gender. Product stores full registration data (PulsePro) — depth of demographic export unknown |
| Encounters / visits | ⚠️ Partial | "Encounters" section listed | Section name only; product has advanced scheduling and encounter management. No field-level detail on what encounter data is exported |
| Problems / conditions / diagnoses | ✅ Covered | "Problems," "Hospital Discharge Diagnosis," "Admission Diagnosis," "Health Concerns Section" | 4 sections addressing diagnoses and conditions |
| Medications / prescriptions | ⚠️ Partial | "Medications," "Discharge Medications" | Sections listed but product has deep e-prescribing (Surescripts Gold) with transaction history that CDA likely cannot fully represent |
| Allergies | ✅ Covered | "Allergies and Adverse Reactions" | Standard CDA section |
| Immunizations | ✅ Covered | "Immunizations" | Standard CDA section |
| Vitals | ✅ Covered | "Vital Signs" | Standard CDA section |
| Lab results | ✅ Covered | "Results" | Standard CDA section |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated imaging section; "Results" may include some | Product has CPOE for diagnostic imaging; unclear if imaging reports/orders are in export |
| Procedures | ✅ Covered | 7 procedure-related sections | Strong coverage of procedure documentation |
| Clinical notes / documents | ✅ Covered | 12 note-related sections | Strongest area of coverage |
| Care plans / goals | ✅ Covered | "PLAN OF CARE," "Goals Section," "Interventions Section," "Health Status Evaluations/Outcomes Section" | 4 sections with good breadth |
| Orders / referrals | ⚠️ Partial | "Reason for Referral" only | Product has full CPOE (meds, labs, imaging); only referral reason is represented, not order details |
| Insurance / coverage | ⚠️ Partial | "Payers" section listed | Section name only; product does insurance eligibility verification — depth of export unknown |
| Claims / billing | ⚠️ Partial | "Financial Data" section listed | **Significant concern**: Product has deep billing (PulsePro), RCM (PulseRCM), claims management, A/R tracking, payment posting, denial management. CDA is fundamentally unable to represent this data. A single "Financial Data" CDA section cannot capture claims, payments, denials, A/R aging, etc. |
| Payments | ❌ Not covered | No evidence | Product handles payment posting and reconciliation; no evidence in export |
| Consents / directives | ⚠️ Partial | "Security and Privacy Prohibitions" may partially address | Unclear scope |
| Patient communications / portal messages | ❌ Not covered | No evidence | Product integrates InteliChart patient portal; portal messages not in export |
| Specialty-specific data | ❌ Not covered | No evidence of custom flowsheet data | Product's key differentiator is "customizable flow sheets configurable per provider" and specialty-specific templates — these are not representable in standard CDA sections |

**Summary**: Of 17 applicable domains, 7 have clear coverage (all clinical), 8 have partial/uncertain coverage, and 3 have no evidence of coverage. The gaps concentrate in billing/financial data and specialty-specific clinical content — exactly the areas where CDA as a format is weakest.

## 6. Documentation Quality

**From Pulse Systems, Inc. (the certified developer): No documentation exists.** The registered certification URL's "View Electronic Health Information Export Documentation" link navigates to `https://www.hl7.org/fhir/us/core/uscdi.html` — HL7's FHIR US Core USCDI reference page. This is an external standards reference about USCDI data classes, not vendor-specific EHI export documentation. There is no data dictionary, no export format specification, no user guide, and no sample data hosted by Pulse Systems.

**From CHS/CereCore (third party, different version):** The DOCX provides:
- ✅ Export format identification (CDA XML)
- ✅ List of 44 CDA section names
- ✅ One sample XML fragment (as screenshot image)
- ✅ Acknowledgment of limitations
- ❌ No field-level documentation within any section
- ❌ No data types, constraints, or value sets
- ❌ No instructions for performing the export
- ❌ No explanation of data completeness relative to what the system stores
- ❌ No machine-readable schema or sample data

**Could a developer build an import from this documentation?** No. A developer would receive a CDA XML document and would need to rely entirely on the CDA/C-CDA standard specifications for parsing. The vendor documentation provides no guidance on which CDA sections are populated, what coded values are used, what Pulse-specific extensions might exist, or how to handle the acknowledged gaps (rich text, images). The section list tells you what sections *might* appear, but nothing about their content.

## 7. Overall Assessment

### Classification

**Standard-based projection**: The EHI export is a CDA XML document — a clinical document standard being repurposed as a (b)(10) export mechanism. This is essentially the vendor's existing C-CDA/CCD capability (certified under (g)(6) "Consolidated CDA Creation Performance") being called the (b)(10) export. CDA is designed for clinical document exchange between healthcare systems, not for comprehensive data export. It cannot represent billing, practice management, revenue cycle, scheduling, or custom specialty data that the product stores.

### Key Findings

1. **Vendor provides no EHI export documentation at all.** The "View Electronic Health Information Export Documentation" link on pulseinc.com points to HL7.org's FHIR US Core USCDI page — an external standards reference with no connection to Pulse's export. This appears to conflate (b)(10) EHI export with (g)(10) FHIR API/USCDI requirements.

2. **The only substantive documentation is from a different organization for a different version.** The CHS-hosted DOCX describes Pulse v16.1 (CHS's internal deployment), not the Pulse Systems v8.02 certified product. CHS explicitly states their Pulse product is "not commercially available technology."

3. **Export is CDA XML, covering clinical data but structurally unable to represent billing/PM data.** The product has deep billing, RCM, practice management, and scheduling capabilities (PulsePro, PulseRCM). CDA has no sections for claims, payments, denials, A/R, or appointment schedules. The "Financial Data" section name is listed but CDA is not designed for this purpose.

4. **Zero field-level documentation.** The export documentation consists of a list of 44 CDA section names with no fields, types, descriptions, value sets, or relationships. There is no data dictionary of any kind.

5. **Custom specialty data is unaddressed.** The product's differentiating feature is customizable flowsheets for specialty practices. Standard CDA sections cannot represent custom flowsheet data structures, and the documentation makes no mention of how (or whether) this data is exported.

### Summary Stats

    Classification:  Standard-based projection
    Export format:   CDA XML (Clinical Document Architecture)
    Model type:      Standard projection (C-CDA repackaged as b(10))
    Entities:        44 CDA sections (not database entities)
    Fields:          N/A (no field-level documentation)
    Descriptions:    N/A (section names only)
    Sample data:     Yes (XML screenshot in DOCX, not machine-readable)
    Bulk export:     Unclear (vendor mentions "mass export" should be off-peak)
    Domains covered: 7 of 17 applicable domains clearly; 8 partial/uncertain

### Bottom Line

Pulse Systems, Inc. provides no EHI export documentation at its registered URL — the link labeled "View Electronic Health Information Export Documentation" redirects to an external HL7 standards page. The only substantive documentation found is a brief CHS-hosted document for a different version describing a CDA XML export. This is a C-CDA clinical document being called a (b)(10) export, covering clinical data reasonably but structurally unable to represent the billing, practice management, and specialty data that this integrated EHR/PM product stores. The single biggest gap is the complete absence of vendor-authored EHI export documentation.

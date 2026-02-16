# EHI Export Analysis: Netsmart Technologies

**Product**: myUnity (and myUnity Senior Living)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2816.myUn.23.02.0.231218 (CHPL #11409)

## 1. Product Context

myUnity is Netsmart Technologies' unified post-acute care EHR platform spanning home health, hospice, palliative care, skilled nursing facilities (SNF), senior living (assisted living, independent living, memory care), life plan communities/CCRCs, personal care/private duty, adult day care, and state veterans homes. It is a comprehensive platform covering:

- **Clinical workflows**: point-of-care documentation, care plans, orders, medication management (including eMAR), clinical notes, regulatory assessments (OASIS for home health, MDS for SNF, HOPE/HIS for hospice), vitals, allergies, immunizations, lab results, procedures
- **Billing/revenue cycle**: claims submission for Medicare, Medicaid, Medicare Advantage, commercial, and private pay; payment tracking; eligibility verification; prior authorizations; collections
- **Administrative**: scheduling, referral management, EVV, staff assignments, telehealth
- **Patient engagement**: patient/family portal, secure messaging

Given this breadth, a genuine (b)(10) export should cover clinical data, assessments (regulatory and non-regulatory), billing/claims, insurance, orders, medications/administrations, notes/documents, referrals, and attachments.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi_export_all_files_myunity_fall_2024.pdf` | 64-page PDF data dictionary documenting all 23 JSON export files. Contains field-level definitions (name, type, description) for 404 fields. Last updated 08/15/2024. | **Primary source** — most informative artifact |
| `downloads/ehi-all-data-myunity.html` | HTML landing page for the EHI All Data Export documentation hub. Describes export format (JSON files in ZIP), links to the PDF, and includes variability disclaimers. | Moderately informative — confirms export mechanics |
| `downloads/ehi-page-screenshot.png` | Screenshot of the EHI documentation page | Low — visual confirmation only |
| `downloads/enrichment/data-dictionary.json` | Prior agent's structured extraction of the PDF data dictionary (23 files, 404 fields) | Used for cross-validation; my own parse matches exactly |
| `downloads/enrichment/extract-data-dictionary.ts` | Prior agent's extraction script | Reviewed for approach validation |

## 3. Export Mechanics

- **Format**: JSON files, each exported to its own ZIP file with a unique filename. The export is native to myUnity's data model (not FHIR or C-CDA, except for the CCD file which is an embedded C-CDA XML).
- **Mechanism**: Manual one-time export via the myUnity application UI. The HTML page states: "EHI Export functionality allows organizations to do a manual one-time export of health data for one or more patients."
- **Scope**: Single-patient or multi-patient ("one or more patients").
- **Access constraints**: The documentation notes content may vary based on: software applications in use, software version, documentation practices, and configuration/customizations at the organization. No mention of fees.
- **Bulk capability**: Supports exporting for multiple patients but described as a "manual one-time export" — not an automated bulk pipeline.

## 4. Export Content: What's In It

The export consists of **23 JSON files** containing **404 fields** total (excluding the CCD's internal C-CDA structure). Every field (100%) has a name, data type, and human-readable description. No field is undocumented.

The CCD file is a standard C-CDA XML document with 19 sections covering USCDI v1 content. The Attachments file contains raw patient documents (PDF, DOC, images, etc.) without structured field definitions.

### Vendor's own content organization

The vendor organizes export files by functional domain. All 23 files:

| Export File | Fields | Described | Typed | Domain |
|---|---|---|---|---|
| Demographics | 29 | 29 | 29 | Patient identity |
| CCD | 0 (19 sections) | — | — | Clinical summary (C-CDA) |
| FamilyHealthHistory | 8 | 8 | 8 | Clinical |
| HealthInsurance | 15 | 15 | 15 | Insurance/coverage |
| Referrals | 36 | 36 | 36 | Care coordination |
| ResponsibleParties | 21 | 21 | 21 | Patient contacts |
| CensusAdvanceDirectives | 12 | 12 | 12 | Directives/consents |
| AssessmentandPlanOfTreatment | 14 | 14 | 14 | Care planning |
| Consents | 9 | 9 | 9 | Consents |
| Attachments | 0 (raw files) | — | — | Documents/media |
| Documents | 9 | 9 | 9 | Clinical documents |
| PatientNotes | 27 | 27 | 27 | Clinical notes |
| Orders | 37 | 37 | 37 | Orders |
| OrderAdministrations | 41 | 41 | 41 | Medication administration |
| Claims | 29 | 29 | 29 | Billing |
| ClaimCharges | 18 | 18 | 18 | Billing detail |
| ClaimChargeAdjustments | 10 | 10 | 10 | Billing adjustments |
| RegulatoryAssessment | 14 | 14 | 14 | Regulatory assessments (MDS, OASIS, HIS) |
| EventADTs | 5 | 5 | 5 | Admissions/discharges/transfers |
| Appointments | 10 | 10 | 10 | Scheduling |
| Eligibility | 14 | 14 | 14 | Insurance eligibility |
| Authorization | 20 | 20 | 20 | Prior authorizations |
| NonRegulatoryAssessment | 26 | 26 | 26 | Non-regulatory assessments |

**Field type distribution**: Types used include String, Integer, Date, DateTime, Time, Decimal, Boolean, Array, and a few compound types (e.g., `AssessmentDocList` as Array). The most common type is String.

**Largest files by field count**:
1. OrderAdministrations — 41 fields (detailed medication administration records including dose, route, frequency, site, administering staff, etc.)
2. Orders — 37 fields (order details including type, status, physician, start/stop dates, frequency, PRN reason, etc.)
3. Referrals — 36 fields (referral details including source, diagnosis, physician, insurance, status, clinical info)
4. Demographics — 29 fields (comprehensive demographics including race, ethnicity, language, pronouns, gender identity, sexual orientation, military status)
5. Claims — 29 fields (claim/invoice details including payer, dates, amounts, status, facility)

**Notable design decisions**:
- The export includes both a CCD (C-CDA standard document) AND separate JSON files for the same clinical domains (e.g., orders, medications via OrderAdministrations). This means the export goes beyond the C-CDA by providing granular, structured data in addition to the summary document.
- Regulatory assessments (OASIS, MDS, HIS) and non-regulatory assessments are exported separately, with the non-regulatory assessments containing detailed question/answer pairs via nested arrays.
- Billing data is split across three files (Claims, ClaimCharges, ClaimChargeAdjustments) with foreign key relationships via `InvoiceSys`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export organizes around these functional areas:

**Patient Identity & Contacts** (Demographics, ResponsibleParties): 50 fields covering detailed demographics (29 fields) including gender identity, pronouns, sexual orientation, military status, and 21 fields for responsible parties/emergency contacts with relationship types, phone numbers, and addresses.

**Clinical Data** (CCD, FamilyHealthHistory, PatientNotes, Orders, OrderAdministrations, AssessmentandPlanOfTreatment, Documents, Attachments): This is the richest area. The CCD provides a standard C-CDA with 19 sections. Beyond that, PatientNotes (27 fields) covers clinical documentation with note type, category, body text, author, and discipline. Orders (37 fields) captures detailed order information including medications with dose/route/frequency. OrderAdministrations (41 fields) provides granular medication administration records — the deepest single file in the export.

**Assessments** (RegulatoryAssessment, NonRegulatoryAssessment): 40 fields total. RegulatoryAssessment covers federally mandated assessments (MDS, OASIS, HIS) with assessment type, dates, status, and a note that content is "formatted as a key/value pair." NonRegulatoryAssessment (26 fields) captures other clinical assessments with question/answer structures via nested arrays.

**Billing & Insurance** (Claims, ClaimCharges, ClaimChargeAdjustments, HealthInsurance, Eligibility, Authorization): 106 fields across 6 files. This is genuinely substantive — Claims captures claim-level data (payer, dates, amounts, status, facility), ClaimCharges has line-item charges with procedure codes and modifiers, ClaimChargeAdjustments tracks payment adjustments, HealthInsurance covers insurance plans, Eligibility tracks eligibility status, and Authorization handles prior authorizations.

**Care Coordination** (Referrals, CensusAdvanceDirectives, Consents, EventADTs, Appointments): 72 fields. Referrals (36 fields) is notably deep, covering referral source, diagnosis, clinical information, physician details, and insurance. EventADTs (5 fields) tracks admissions/discharges/transfers. Appointments (10 fields) covers visit scheduling.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Demographics` (29 fields) — comprehensive including pronouns, gender identity, sexual orientation, military status, birth order | Thorough |
| Encounters / visits | ⚠️ Partial | `EventADTs` (5 fields — admit/discharge/transfer events only), `Appointments` (10 fields) | Product tracks detailed visit documentation; EventADTs is thin (only 5 fields for type, date, description, status, location) |
| Problems / conditions / diagnoses | ⚠️ Partial | Diagnoses appear in `Referrals` and `CCD` sections but no dedicated Problems/Diagnoses file | Problems likely in CCD only; no structured JSON export of the problem list |
| Medications / prescriptions | ✅ Covered | `Orders` (37 fields) covers medication orders with dose, route, frequency, start/stop dates, PRN reason | Well-covered |
| Allergies | ⚠️ Partial | In CCD (Allergies and Intolerances section) only | No dedicated JSON file for allergies; only in C-CDA summary |
| Immunizations | ⚠️ Partial | In CCD (Immunizations section) only | No dedicated JSON file; only in C-CDA summary |
| Vitals | ⚠️ Partial | In CCD (Vital Signs section) only | No dedicated JSON file; only in C-CDA summary |
| Lab results | ⚠️ Partial | In CCD (Results section) only | No dedicated JSON file; only in C-CDA summary |
| Imaging / diagnostic reports | ⚠️ Partial | May appear in Documents or Attachments | No dedicated structured file |
| Procedures | ⚠️ Partial | In CCD (Procedures section) and possibly via `Orders` | No dedicated Procedures file |
| Clinical notes / documents | ✅ Covered | `PatientNotes` (27 fields), `Documents` (9 fields), `Attachments` (raw files) | Well-covered with structured notes and raw document attachments |
| Care plans / goals | ✅ Covered | `AssessmentandPlanOfTreatment` (14 fields), CCD (Goals Section, Health Concerns, Treatment Plan) | Reasonably covered |
| Orders / referrals | ✅ Covered | `Orders` (37 fields), `Referrals` (36 fields) | Strong — detailed order and referral data |
| Insurance / coverage | ✅ Covered | `HealthInsurance` (15 fields), `Eligibility` (14 fields), `Authorization` (20 fields) | Thorough — includes eligibility verification and prior auth |
| Claims / billing | ✅ Covered | `Claims` (29 fields), `ClaimCharges` (18 fields), `ClaimChargeAdjustments` (10 fields) | Genuinely substantive billing coverage |
| Payments | ⚠️ Partial | `ClaimChargeAdjustments` includes adjustment amounts but no dedicated payment file | Adjustments tracked; direct payment records unclear |
| Consents / directives | ✅ Covered | `Consents` (9 fields), `CensusAdvanceDirectives` (12 fields) | Covered including advance directives |
| Patient communications / portal messages | ❌ Not covered | No evidence of portal messages, secure messaging, or patient communication logs | Product has patient portal (certified (e)(1), (e)(3)); communication data not exported |
| Specialty-specific (post-acute assessments) | ✅ Covered | `RegulatoryAssessment` (14 fields — MDS, OASIS, HIS), `NonRegulatoryAssessment` (26 fields) | Key differentiator — exports federally mandated and custom post-acute assessments |
| Medication administration (eMAR) | ✅ Covered | `OrderAdministrations` (41 fields) — detailed MAR data with dose, route, site, administering staff, time | Strong — most detailed file in the export |
| Family health history | ✅ Covered | `FamilyHealthHistory` (8 fields) | Adequate |
| Responsible parties / contacts | ✅ Covered | `ResponsibleParties` (21 fields) | Thorough |

**Key observation**: Several USCDI domains (allergies, immunizations, vitals, labs, problems, procedures) are only represented in the CCD file (C-CDA XML) and lack dedicated JSON export files. This means the structured, queryable data for these domains is limited to whatever the C-CDA standard captures. The vendor clearly built purpose-specific JSON export files for domains *beyond* USCDI (billing, assessments, medication administration, referrals, insurance eligibility, prior auth) while relying on the CCD for core USCDI clinical domains.

## 6. Documentation Quality

**Strengths**:
- Every field (404/404 = 100%) has a name, type, and description
- Descriptions are genuinely informative (not just restating the field name) — e.g., "Indicates the specific type of the order associated with the administration" rather than just "Order type"
- A glossary defines common fields (PatientSys, PatientID, Patient_DisplayName) for cross-file joining
- File-level descriptions clearly explain what each file contains
- The documentation explicitly states it covers "the electronic health information available in a patient's myUnity record"

**Weaknesses**:
- No foreign key documentation beyond the implicit PatientID/PatientSys linkage and the InvoiceSys link between Claims/ClaimCharges/ClaimChargeAdjustments
- No value sets or code systems documented (e.g., what values does `Patient_InsurancePayerType` accept?)
- No sample data provided
- No machine-readable schema (JSON Schema, etc.) — only the PDF
- The CCD file is described only at the section level, not field level (relying on the C-CDA standard for details)
- Assessment files note content is "formatted as a key/value pair" but don't enumerate the specific assessment items that may appear

**Overall**: A developer could understand the structure and build an import, but would need to inspect actual export data to understand value sets, handle edge cases, and parse the assessment key/value pairs. The documentation is functional but not self-sufficient.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export goes meaningfully beyond USCDI. The strongest signal is the inclusion of dedicated, structured files for billing (Claims, ClaimCharges, ClaimChargeAdjustments — 57 fields), insurance eligibility and prior authorization (34 fields), medication administration records (41 fields), regulatory assessments specific to post-acute care (MDS, OASIS, HIS), non-regulatory assessments, detailed referral data (36 fields), and advance directives. These are domains that a repackaged USCDI export would not cover. The 23-file, 404-field scope spans demographics, clinical data, billing, insurance, care coordination, assessments, and documents — a breadth consistent with the product's post-acute care focus.

The notable gaps — several core clinical domains (allergies, immunizations, vitals, labs, problems, procedures) exported only via the CCD rather than structured JSON — are a limitation in depth but not in coverage breadth. The data is present; it's just in C-CDA format rather than the vendor's richer JSON format. Patient communications/portal messages are the most significant missing domain.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged existing clinical exchange. The telltale signs:
1. The export includes 22 JSON files in the vendor's native data model *alongside* a C-CDA document — this is additive, not relabeled
2. Domains like billing (Claims, ClaimCharges, ClaimChargeAdjustments), medication administration (OrderAdministrations), insurance eligibility, prior authorizations, and regulatory assessments would never appear in a (g)(10) FHIR API or C-CDA exchange
3. The documentation page explicitly distinguishes this from the FHIR API: "If you are working with a Netsmart customer and want to understand different options on integrating with our solutions, please visit our Netsmart Developer Portal for documentation regarding our FHIR API's"
4. The export format is native JSON, not FHIR or C-CDA (the CCD is included as one component of a larger export)

### Key Findings

1. **Purpose-built with real billing depth**: The 3-file billing suite (Claims/ClaimCharges/ClaimChargeAdjustments, 57 fields total) with foreign key linkage via InvoiceSys demonstrates genuine engagement with (b)(10) — this is patient-specific billing data that would never appear in a standard clinical exchange.

2. **Post-acute specialty data exported**: RegulatoryAssessment covers MDS (skilled nursing), OASIS (home health), and HIS/HOPE (hospice) — the federally mandated assessments specific to myUnity's post-acute care market. NonRegulatoryAssessment captures custom clinical assessments with question/answer structures.

3. **Medication administration is the deepest entity**: OrderAdministrations (41 fields) captures granular eMAR data including dose, route, frequency, site, administering staff, and administration time — detailed operational clinical data well beyond what USCDI requires.

4. **Core clinical domains rely on CCD**: Allergies, immunizations, vitals, labs, problems, and procedures lack dedicated JSON export files and are only available through the embedded CCD (C-CDA XML). This means these domains are exported at the C-CDA standard's level of detail rather than the vendor's internal data model depth.

5. **100% field documentation**: All 404 fields across 23 files have names, types, and descriptions — a level of documentation completeness that enables practical use of the export.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   JSON (native) + C-CDA XML (CCD component) + raw file attachments
    Entities:        23 export files
    Fields:          404 (plus 19 CCD sections via C-CDA standard)
    Descriptions:    100% of fields have descriptions
    Sample data:     No
    Bulk export:     Yes (one or more patients)
    Domains covered: 15 of 19 applicable domains (4 partial via CCD only)

### Bottom Line

myUnity's EHI export is a genuine purpose-built effort that covers the breadth of the product's post-acute care data model — demographics, clinical notes, orders, medication administration, billing/claims, insurance, assessments (both regulatory and non-regulatory), referrals, and documents. The biggest limitation is that several core clinical domains (allergies, immunizations, vitals, labs, problems, procedures) are exported only via the embedded CCD (C-CDA) rather than in the vendor's richer native JSON format, meaning those domains are captured at USCDI depth rather than the product's full internal depth. Overall, this is a substantive and well-documented (b)(10) implementation.

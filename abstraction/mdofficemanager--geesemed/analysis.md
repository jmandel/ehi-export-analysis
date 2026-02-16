# EHI Export Analysis: MDOfficeManager (GeeseMed)

**Product**: GeeseMed EHR v7.1 (with MDOfficeManager PMS)
**Analysis date**: 2026-02-15
**CHPL ID**: 11586 (CHPL Product Number: 15.04.09.3013.Gees.07.00.1.250101)

## 1. Product Context

GeeseMed is a cloud-based EHR developed by MDOfficeManager LLC (Clarksville, Indiana), a very small vendor (revenue < $10M, ~80 users per market data). It is marketed alongside **MDOfficeManager PMS** as an integrated EMR + practice management platform targeting small-to-medium ambulatory practices, outpatient surgery centers, and long-term care facilities (SNF, NF, ALF). The vendor claims support for 22+ medical specialties.

Key data domains the product stores, relevant to EHI export completeness:

- **Clinical documentation**: Template-based charting with macros, speech recognition, medical transcription (DRT/CDA/HL7 document types)
- **Orders**: CPOE for medications, labs, and imaging
- **E-prescribing**: SureScripts-certified including EPCS, formulary/eligibility checks
- **Lab interfaces**: Electronic ordering and results from major laboratories
- **Billing/RCM**: Fully integrated billing with claims processing, denial tracking, A/R management, dashboard analytics
- **Patient portal**: Real-time access to records, lab results, histories, appointment requests
- **Telehealth**: Secure video/chat, remote patient monitoring
- **Care plans**: Certified for §170.315(b)(11)
- **Health information exchange**: Direct messaging (EMRDirect), C-CDA transitions of care
- **LTC-specific**: Marketed to skilled nursing/nursing/assisted living facilities (though specific LTC data elements like MDS assessments are not detailed on the website)

This product stores data across clinical, billing, patient engagement, and potentially LTC-specific domains. A complete (b)(10) export should cover all of these.

## 2. Artifacts Reviewed

Only a single artifact was collected:

| Artifact | Description | Informativeness |
|---|---|---|
| `GeeseMed_b10_Health-Info.Export_11202023.pdf` (844 KB, 8 pages) | The sole (b)(10) documentation. Created 2023-11-20 in Microsoft Word 2016 by author "dimple" (developer contact Dimple Shah). Contains: overview (1 page), single-patient export walkthrough with screenshots (1 page), bulk export walkthrough with screenshots (2 pages), data dictionary listing C-CDA sections and fields (3 pages). | **Primary and only source.** The data dictionary on pages 6–8 is the only specification of what the export contains. No sample data, no schemas, no supplementary files. |

No other artifacts (sample exports, JSON schemas, HTML data dictionaries, additional PDFs) were found. The `downloads/` directory contains only this single PDF.

## 3. Export Mechanics

- **Format**: C-CDA XML (HL7 CDA R2, Consolidated CDA Templates for Clinical Notes, US Realm, DSTU Release 2.1, August 2015), delivered as ZIP archives. The ZIP also contains human-readable CCD renderings and supplemental clinical documents as PDFs.
- **Mechanism**: UI-driven export within the GeeseMed EHR application. Two modes:
  - **Single Patient Export**: Select date range → "Create and View CCD" → review rendered CCD → click "Export" → download ZIP containing C-CDA XML + readable CCD.
  - **Bulk Patient Export**: Select date range + provider → search/select patients → choose destination (local path or Direct Mail) → optionally schedule as recurring → "Generate CCD" → download batch ZIP from "CCD Result" tab.
- **Single-patient vs bulk**: Both supported via the UI.
- **Access constraints/fees**: Not mentioned in documentation. The document is marked "intended for the use of MDOfficeManager – GeeseMed clients only."
- **Scheduling**: Bulk export supports recurring scheduled exports (date/time configurable).

### Batch export ZIP structure (from page 5 screenshot)

The batch export ZIP (named like `BatchExport_U0000032_00C111_11202023_013330.zip`) contains:
- Per-patient readable CCD files (e.g., `James Portability_11202023_013329`)
- Per-patient C-CDA XML files (e.g., `James Portability_11202023_013329.xml`)
- Additional clinical PDFs (e.g., `James_11202023_013329_LungReport` — a PDF icon is visible)

The inclusion of supplemental PDFs like "LungReport" is noted in the documentation text ("other clinical data as PDF documents") but there is **no systematic documentation** of which clinical document types are included as PDFs, when they are attached, or what data they contain.

## 4. Export Content: What's In It

The export is a **C-CDA document** — a standardized clinical summary. The "data dictionary" on pages 6–8 is a two-column table listing C-CDA section names/template IDs and their constituent data elements with optional descriptions.

### Parsed data dictionary statistics

From script `analysis/parse_data_dictionary.py` → `analysis/full-entity-inventory.json`:

- **Total C-CDA sections**: 21
- **Total fields across all sections**: 70
- **Fields with any description**: 20 (28.6%)
- **Fields with no description**: 50 (71.4%)
- **Sections with C-CDA template IDs**: 16
- **Sections without template IDs**: 5 (Patient Demographics, Provider Info, Participant, Laboratory Tests, Laboratory Information)
- **No data types documented** for any field
- **No value sets or code systems specified** for any field
- **No cardinality, nullability, or constraints** documented
- **No foreign key relationships** documented (beyond implicit C-CDA structure)

### Vendor's own content organization

The vendor organizes data by C-CDA section. Each section and its fields:

| C-CDA Section | Template ID | Fields | Fields Described | Category |
|---|---|---|---|---|
| Patient Demographics/Information | — | 8 | 0 | Demographics |
| Provider's name and office contact information | — | 5 | 5 | Provider |
| Participant | — | 4 | 4 | Next of Kin |
| Encounter Diagnosis | 2.16.840.1.113883.10.20.22.2.22.1 | 4 | 4 | Diagnoses |
| Immunizations | 2.16.840.1.113883.10.20.22.2.2.1 | 4 | 1 | Immunizations |
| Treatment Plan | 2.16.840.1.113883.10.20.22.2.10 | 2 | 2 | Care Plan |
| Social History | 2.16.840.1.113883.10.20.22.2.17 | 3 | 3 | Social History |
| Problems | 2.16.840.1.113883.10.20.22.2.5.1 | 3 | 0 | Problems |
| Medications | 2.16.840.1.113883.10.20.22.2.1.1 | 4 | 1 | Medications |
| Medication Allergies | 2.16.840.1.113883.10.20.22.2.6.1 | 5 | 0 | Allergies |
| Vitals | 2.16.840.1.113883.10.20.22.2.4.1 | 2 | 0 | Vitals |
| Laboratory Tests | — | 4 | 0 | Labs |
| Laboratory Information | — | 5 | 0 | Labs |
| Laboratory Results | 2.16.840.1.113883.10.20.22.2.3.1 | 4 | 0 | Labs |
| Goal | 2.16.840.1.113883.10.20.22.2.60 | 2 | 0 | Goals |
| Procedures | 2.16.840.1.113883.10.20.22.2.7.1 | 2 | 0 | Procedures |
| Referral | 1.3.6.1.4.1.19376.1.5.3.1.3.1 | 2 | 0 | Referrals |
| Medical Equipment | 2.16.840.1.113883.10.20.22.2.23 | 1 | 0 | Devices |
| Cognitive Status | 2.16.840.1.113883.10.20.22.2.56 | 2 | 0 | Assessments |
| Functional Status | 2.16.840.1.113883.10.20.22.2.14 | 2 | 0 | Assessments |
| Health Concern | 2.16.840.1.113883.10.20.22.2.58 | 2 | 0 | Assessments |
| **TOTAL** | | **70** | **20** | |

Where descriptions exist, they are minimal — mostly restating the field name in slightly different words (e.g., "Encounter Code" → "Diagnosis code", "Associated Person Name" → "Next of kin name", "Direction" → "SIG"). No description provides data type, format, code system, or constraints.

### Supplemental PDF attachments

The batch export screenshot (page 5) shows a `LungReport` PDF included alongside C-CDA files. The document states the ZIP contains "other clinical data as PDF documents," but:
- No list of which clinical document types may be included
- No documentation of what triggers PDF inclusion
- No description of PDF content structure
- This is the only evidence that anything beyond C-CDA is exported

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers exactly one thing: **standard C-CDA clinical summary data**. The 21 sections map directly to standard C-CDA templates — there are no vendor extensions, no custom sections, and no data beyond what the C-CDA specification defines.

The richest areas are:
- **Labs**: 3 separate sections (Tests, Information, Results) with 13 fields total — the most detailed domain
- **Demographics + Provider + Participant**: 17 fields covering patient identity, provider, and next of kin
- **Medication Allergies**: 5 fields (substance, reaction, severity, status, date)

The thinnest areas:
- **Medical Equipment**: 1 field only (implanted device name/ID)
- **Vitals, Goal, Procedures, Referral, Cognitive Status, Functional Status, Health Concern**: Each has only 2 fields with no descriptions

There is no evidence of any data beyond standard C-CDA sections. The export is a **clinical summary**, not a database export. It represents the USCDI/transitions-of-care data subset, not the full designated record set.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient Demographics/Information` (8 fields: name, sex, DOB, race, ethnicity, language, phone, address). No insurance/coverage info, no SSN/MRN identifiers documented. | Basic demographics present but thin — no insurance enrollment data despite product storing it |
| Encounters / visits | ⚠️ Partial | `Encounter Diagnosis` section lists diagnoses with dates, but no encounter-level data (visit type, duration, location, provider seen, reason for visit) | Product stores full encounter records; export only has diagnosis codes attached to encounters |
| Problems / conditions / diagnoses | ✅ Covered | `Problems` (3 fields) and `Encounter Diagnosis` (4 fields) | Adequate for problem list and encounter diagnoses |
| Medications / prescriptions | ⚠️ Partial | `Medications` (4 fields: medication, direction/SIG, start/end date). No NDC/RxNorm codes documented, no dosage details, no prescriber, no pharmacy | Product has SureScripts e-Rx with EPCS; export captures only basic medication list, not Rx transaction history |
| Allergies | ✅ Covered | `Medication Allergies` (5 fields: substance, reaction, severity, status, date) | Standard allergy list coverage |
| Immunizations | ✅ Covered | `Immunizations` (4 fields: vaccine name, date, status, notes) | Standard immunization coverage |
| Vitals | ⚠️ Partial | `Vitals` (2 fields: observation, observation date). No specific vital types enumerated (BP, HR, temp, etc.) | Extremely thin — only 2 undescribed fields for all vital sign types |
| Lab results | ✅ Covered | Three sections: `Laboratory Tests` (4 fields), `Laboratory Information` (5 fields), `Laboratory Results` (4 fields) — 13 fields total | Relatively detailed lab coverage across ordering, performing lab, and results |
| Imaging / diagnostic reports | ❌ Not covered | No imaging section in the CCD data dictionary. The "LungReport" PDF in the batch export may be a diagnostic report, but this is undocumented. | Product supports CPOE for imaging; no systematic imaging data in export |
| Procedures | ⚠️ Partial | `Procedures` (2 fields: procedure, date). No CPT/HCPCS codes, no provider, no details. | Product serves outpatient surgery centers; procedure documentation is minimal |
| Clinical notes / documents | ⚠️ Partial | No dedicated clinical notes section in C-CDA dictionary. The batch export includes "other clinical data as PDF documents" (a LungReport PDF is shown), but this mechanism is undocumented. | Product's core workflow is template-based charting with dictation/transcription; the export provides no systematic way to capture these notes. Ad-hoc PDFs may partially cover this. |
| Care plans / goals | ⚠️ Partial | `Treatment Plan` (2 fields: planned observation, planned date) and `Goal` (2 fields: description, date). Very thin. | Product is certified for (b)(11) care plans; export captures only minimal plan/goal data |
| Orders / referrals | ⚠️ Partial | `Referral` (2 fields: referral, date). Lab/imaging orders partially covered under Treatment Plan. | Extremely thin — no order detail, no ordering provider for referrals |
| Insurance / coverage | ❌ Not covered | No insurance or enrollment entities in the export | Product stores insurance information (integrated billing); significant gap |
| Claims / billing | ❌ Not covered | No billing, claims, charges, or financial entities in the export | Product has fully integrated billing with claims processing, denial tracking, A/R management; **major gap** |
| Payments | ❌ Not covered | No payment entities in the export | Product processes payments through integrated billing; significant gap |
| Consents / directives | ❌ Not covered | No consent or directive entities in the export | Unknown whether product stores consents; cannot confirm gap |
| Patient communications / portal messages | ❌ Not covered | No patient portal messages, appointment requests, or communication data in the export | Product has a patient portal with messaging; significant gap |
| Specialty-specific (LTC) | ❌ Not covered | No LTC-specific data elements (ADL tracking, MDS assessments, care facility documentation) | Product actively markets to SNF/NF/ALF facilities; if LTC-specific data is stored, this is a gap |
| Cognitive / Functional Status | ✅ Covered | `Cognitive Status` (2 fields) and `Functional Status` (2 fields) — relevant to LTC | Present but very thin (assessment + date only) |

**Summary**: Of 19 applicable domains assessed, 4 are adequately covered, 8 are partially covered (present but thin), and 7 are not covered at all. The export is limited to standard C-CDA clinical summary data and entirely omits billing, insurance, patient portal, imaging, and specialty-specific domains.

## 6. Documentation Quality

The documentation quality is **poor**:

- **8 pages total**, of which 3 are the data dictionary, 2 are screenshots/walkthroughs, 1 is the title page, 1 is the table of contents, and 1 is the overview.
- **No data types** for any field — the table has only "Data Elements" and "Description" columns.
- **No value sets or code systems** — coded fields (diagnosis codes, smoking status, medication codes) reference C-CDA template IDs but don't specify which code systems (ICD-10, SNOMED, RxNorm, etc.) are used.
- **No cardinality or constraints** — cannot tell which fields are required, repeatable, or optional.
- **No relationships** beyond implicit C-CDA document structure.
- **No sample data** — screenshots show the export UI with test patient names but no sample C-CDA content.
- **No machine-readable artifacts** — no JSON schema, no XML sample, no XSD.
- **28.6% description coverage** (20 of 70 fields), and even those descriptions are mostly trivial restatements of the field name (e.g., "Encounter Code" described as "Diagnosis code").
- **Supplemental PDFs undocumented** — the batch export includes clinical documents as PDFs, but there is no specification of which document types, when they're included, or what they contain.

A developer could not build an import from this documentation alone. They would need to rely entirely on the external C-CDA specification and would have no guidance on the supplemental PDF attachments or any vendor-specific behaviors.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is a C-CDA clinical summary repackaged as the (b)(10) EHI export. It covers the standard USCDI/transitions-of-care clinical domains but omits the vendor's native data model entirely. Billing, insurance, patient portal, specialty (LTC), and detailed clinical documentation are absent.

### Key Findings

1. **C-CDA repackaging as (b)(10)**: This is a textbook case of a vendor pointing to their existing C-CDA transitions-of-care export and calling it their EHI export. The document explicitly states GeeseMed "meets the certification criterion §170.315(b)(10) ... by implementing the CCD Export." C-CDA is designed for clinical summaries, not comprehensive EHI export. (Source: `GeeseMed_b10_Health-Info.Export_11202023.pdf`, page 3, "Overview" section)

2. **Entire billing/financial domain missing**: GeeseMed is marketed with fully integrated billing (claims processing, denial tracking, A/R management, RCM services). None of this data appears in the export. No claims, charges, payments, insurance, or financial entities exist in the data dictionary. (Source: pages 6–8 data dictionary; `product-research.md` billing section)

3. **Extremely thin data dictionary**: 70 fields across 21 C-CDA sections, with only 20 fields (28.6%) having any description at all. No data types, no value sets, no constraints. Many sections have just 2 fields (name + date). (Source: `analysis/full-entity-inventory.json`)

4. **Undocumented supplemental PDFs**: The batch export includes clinical documents as PDFs (a "LungReport" is visible in the page 5 screenshot), but there is no documentation of what triggers PDF inclusion or what types of documents are exported this way. This may partially address the clinical notes gap, but it's impossible to assess without documentation.

5. **LTC-specific data absent**: Despite marketing to SNF/NF/ALF facilities, no LTC-specific data elements (ADL tracking, MDS assessments, care facility documentation) appear in the export.

### Summary Stats

```
Classification:  Standard-based projection (C-CDA repackaged as b(10))
Export format:   C-CDA XML (HL7 CDA R2 DSTU 2.1) + supplemental PDFs in ZIP
Model type:      Standard projection (C-CDA), not native database
Entities:        21 C-CDA sections
Fields:          70
Descriptions:    28.6% (20/70), all trivial restatements
Sample data:     No
Bulk export:     Yes (with recurring scheduling support)
Domains covered: 4 of 19 adequately; 8 partial; 7 not covered
```

### Bottom Line

GeeseMed's (b)(10) export is a C-CDA clinical summary — functionally identical to a transitions-of-care document — labeled as an EHI export. A patient or provider would receive standard clinical data (diagnoses, meds, allergies, labs, immunizations) but would be missing all billing/financial records, detailed clinical notes, patient portal communications, imaging data, and any LTC-specific information the product stores. The single biggest gap is the complete absence of billing and financial data from a product that offers fully integrated practice management and revenue cycle services.

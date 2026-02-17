# EHI Export Analysis: Medical Information Technology, Inc. (MEDITECH) — Configuration 1

**Product**: MEDITECH Expanse 2.2 Core HCIS, Expanse 2.2 Ambulatory, Expanse 2.2 ED Management, Expanse 2.1 Core HCIS, Expanse 2.1 Ambulatory, Expanse 2.1 ED Management, 6.1 EHR Core HCIS, 6.1 Ambulatory EHR, 6.1 ED Management, 6.0 EHR Core HCIS, 6.0 ED Management, Client/Server EHR Core HCIS, Client/Server ED Management, MAGIC EHR Core HCIS, MAGIC HCA EHR Core HCIS (without PatientKeeper), MAGIC ED Management
**Analysis date**: 2026-02-16
**CHPL IDs**: 10925, 10926, 10927, 10929, 10930, 10931, 10935, 10972, 10973, 10979, 10981, 10982, 10984, 11018, 11742, 11743

## 1. Product Context

MEDITECH is the third-largest U.S. acute care hospital EHR vendor (~14.8% market share), serving 630–690 U.S. hospitals. The company produces a comprehensive, fully integrated hospital information system spanning clinical, diagnostic, administrative, financial, and operational domains — not just a clinical EHR.

This analysis covers **Configuration 1** of MEDITECH's EHI export — the configuration used by sites with Health Information Management (HIM) and Scanning/eChart (SCN) modules. It applies across four platform generations:

- **Expanse 2.2** (current-gen, web-based) — Acute & Ambulatory
- **Expanse 2.1** — Acute & Ambulatory
- **6.15** (prior-gen) — Acute & Ambulatory
- **6.08** (prior-gen) — Acute only
- **Client/Server 5.67** (legacy, thick-client) — Acute only
- **MAGIC 5.67** (legacy, MUMPS-based green-screen) — Acute only

MEDITECH's product portfolio stores an exceptionally broad range of data relevant to the designated record set:

- **Clinical**: demographics, encounters, problem lists, diagnoses, allergies, medications, MARs, vital signs, clinical notes (all specialties), orders, assessments, flowsheets, care plans, immunizations
- **Diagnostic**: lab results, microbiology, pathology, blood bank, radiology, imaging
- **Pharmacy**: dispensing, formulary, e-prescribing
- **Revenue cycle/financial**: registration, insurance, scheduling, charge capture, claims, patient accounts, coding/abstracting
- **Specialty**: oncology, L&D, mental health, surgical services, critical care, home health, hospice, dietary
- **Patient engagement**: portal messages, telehealth, remote monitoring
- **Care coordination**: population health registries, case management, transitions of care
- **Document management**: scanning/archiving, HIM

The key question for Config 1 is whether the eChart-based approach (exporting rendered documents + FHIR + C-CDA) adequately captures all this structured data, or whether it produces a document-centric "print of record" that loses the underlying structured information.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehiexport-main.html` (9 KB) | Main EHI Export landing page. Describes two export configurations and platform applicability. | **High** — establishes the two-config architecture |
| `downloads/ehiexportconfig1.html` (29 KB) | Configuration 1 detail page. Documents export zip structure, 7 product versions, 15 export sections, and NDJSON schema. | **Primary source** — this is the core documentation for Config 1 |
| `downloads/ehiexportold.html` (28 KB) | Older version of Config 1 documentation. Nearly identical to current config1 page except it lacks "Historical Ambulatory Data" section (added for Expanse 2.2/2.1/6.15 in the current version). | **Medium** — useful for version comparison |
| `downloads/screenshot-ehiexportconfig1.png` (1.2 MB) | Full-page screenshot of Config 1 page. | **Low** — confirms HTML content visually |
| `downloads/screenshot-ehiexport-main.png` (239 KB) | Screenshot of main landing page. | **Low** |
| `product-research.md` | Prior research on MEDITECH products and data domains. | **High** — establishes what data the product stores |
| `chpl-metadata.json` | CHPL certification details for all 16 products. All certified for (b)(10). | **Medium** — confirms certification |
| `metadata.json` | Split analysis context for Config 1. | **Low** |

**Not primary for this analysis but reviewed for shared context:**
- `downloads/ehiexportconfig2.html` — Config 2 page (MRI/DR-based export with CSV data dictionaries). Provides contrast: Config 2 has structured tabular exports with 300+ tables; Config 1 does not.
- Three PDF data dictionaries (608ehiexportcsv.pdf, csacuteandambehiexportdrsolutionmerged.pdf, mgehiexportdrsolutionmerged.pdf) — these belong to Config 2, not Config 1.

## 3. Export Mechanics

**Format**: ZIP file containing multiple formats (document images, PDFs, C-CDA XML, FHIR R4 JSON, TXT reports, NDJSON metadata)

**Mechanism**: The export is triggered through the HIM (Health Information Management) module in coordination with SCN (Scanning and Archiving with eChart). The documentation references "Regulatory EHI Export Functionality Guides" behind a customer portal login at `customer.meditech.com`, suggesting the operational workflow details are not publicly documented. The export produces a single ZIP file per patient.

**Single-patient vs bulk**: The documentation describes a single-patient export (the ZIP contains data for one patient with the FHIR bundle using Patient $everything). No bulk/multi-patient export mechanism is described.

**Access constraints**: The implementation guides are behind a SAML-authenticated customer portal (customer.meditech.com). The technical specifications (this Config 1 page) are publicly accessible. No fees are documented.

**Platform variation**: The number of export sections varies by platform version:
- Expanse 2.2 and 2.1: 10 sections (richest)
- 6.15: 9 sections
- 6.08 Acute: 7 sections
- Client/Server 5.67 Acute: 7 sections
- MAGIC 5.67 Acute: 6 sections
- HCA MAGIC 5.67 Acute: 5 sections (most limited)

## 4. Export Content: What's In It

Configuration 1's export is **document-centric with structured data overlays**. The primary data vehicle is the Electronic Chart (scanned/electronic documents from eChart), supplemented by a US Core FHIR R4 bundle, C-CDA documents, and various rendered reports (PDFs, TXT files).

### Critical observation: No data dictionary

Unlike Configuration 2 (which provides PDF data dictionaries with 97–333 tables and 482–1,231 fields per platform), **Configuration 1 has no data dictionary whatsoever**. There is no enumeration of fields, tables, columns, or structured data elements beyond what is implicit in the FHIR US Core and C-CDA specifications. The documentation describes folder structures and file formats at a high level, but provides zero field-level detail for any of the supplemental reports (FinancialEHI.txt, authorization reports, immunization records, etc.).

### Vendor's own content organization

The vendor organizes the export into named "sections," each corresponding to a folder or file in the ZIP. The table below enumerates every section documented for Config 1:

| Section | Format | Structured? | Content Description | Applicable Versions |
|---|---|---|---|---|
| Electronic Chart | PNG, JPG, TIF, BMP, PDF | No | Scanned/electronic documents organized by account > category > subcategory. Three folder types: account-specific, patient-level (Record_Documents), global (Global_Documents). | All 7 versions |
| Structured Clinical Documents (CCDA) | C-CDA XML (R2.1 or R1.1) | Yes | All Consolidated-CDA documents created and possibly sent externally. | All 7 versions |
| FHIR Resource Bundle | FHIR R4 JSON (US Core STU 3.1.1) | Yes | Patient $everything bundle per US Core STU 3.1.1. | All 7 versions |
| Ambulatory Results | PDF | No | Manually entered micro/lab results + outside vendor micro/lab results. | Expanse 2.2, 2.1, 6.15 |
| Authorization & Referral Management Reports | PDF | No | ArmAuthData (authorizations/referrals) + InsEligCopayDeductData (insurance eligibility, copay, deductibles). | Expanse 2.2, 2.1, 6.15 |
| Financial Reports | TXT | No | FinancialEHI.txt (patient accounting transactions), ResidentTrustEHI.txt (Expanse/6.1x), CostEstimation.txt (Expanse only). | Expanse 2.2, 2.1, 6.15, 6.08, C/S, MAGIC |
| Immunization History | PDF | No | Patient's immunization history. | Expanse 2.2, 2.1, 6.15, 6.08 |
| Immunizations | TXT | No | Patient immunization data. | C/S 5.67 only |
| Implantable Devices | TXT | No | Patient medical/implantable devices. | C/S, MAGIC, HCA MAGIC |
| Patient Notices | PDF | No | Patient-physician interactive messages. | 6.08 only |
| Population Health | PDF | No | External aggregated data received from a vendor. | Expanse 2.2, 2.1 only |
| Provider Messages | TXT | No | Patient-physician interactive messages. | C/S, MAGIC, HCA MAGIC |
| Utilization Review | PDF | No | Case management utilization reviews. | Expanse 2.2, 2.1, 6.15 |
| Historical Ambulatory Data | PNG, JPG, TIF, BMP, TXT, PDF | No | Historical ambulatory documentation migrated from previous software version. | Expanse 2.2, 2.1, 6.15 |
| Ambulatory Order Summary | Unknown | Unknown | Referenced in 6.08 Acute product sections but **no section detail provided**. Documentation gap. | 6.08 only |

Additionally, every export includes these metadata files (all product versions):
- **README.txt** — human-readable table of contents
- **EHIEXPORTSCHEMA.txt** — documentation URL and product version
- **ACCOUNTS_INDEX.html/xml** — browser-viewable index
- **Table of Contents.ndjson** — FHIR DocumentReference resources (27 fields documented) conforming to the Argonaut EHI Export API IG (draft)

### Structured data components (only 2 of 15 content sections)

**FHIR Resource Bundle (US Core STU 3.1.1)**: The FHIR bundle is documented only by reference to the US Core STU 3.1.1 specification and fhir.meditech.com. No vendor-specific extensions, custom resources, or mappings beyond the standard US Core profiles are described. This means the FHIR component covers approximately the USCDI v1 data set: Patient, Condition, MedicationRequest, AllergyIntolerance, Observation, Encounter, Procedure, DiagnosticReport, DocumentReference, CarePlan, CareTeam, Goal, Immunization, Device, Organization, Practitioner, Location, and Provenance resources. This is exactly the (g)(10) FHIR API surface — no additional data domains.

**Structured Clinical Documents (C-CDA)**: Standard C-CDA documents (R2.1 or R1.1) that have been created by the system. These are the same clinical summary documents used for transitions of care — not a broader export of the underlying record.

### Unstructured data components (13 of 15 content sections)

Everything beyond FHIR and C-CDA is exported as **rendered documents** — PDFs, TXT files, and document images (PNG, JPG, TIF, BMP). The Electronic Chart section is the largest, containing all scanned and electronic documents from the eChart system organized by category/subcategory. The financial reports, authorization reports, immunization records, utilization reviews, provider messages, and other supplemental data are all exported as pre-rendered files with no documented field structure.

This is the fundamental characteristic of Config 1: it exports the **visual representation** of the patient record (as documents/images) rather than the **structured data** underlying it. A lab result stored as structured data in MEDITECH's database is exported either as a FHIR Observation (if it falls within US Core scope) or as a scanned/rendered document image in the Electronic Chart.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Config 1 organizes content into the following vendor-defined categories:

1. **Electronic Chart (all versions)**: The broadest section — encompasses all documents in the eChart system. This is the "catch-all": whatever clinical documentation, reports, notes, and images have been scanned or electronically generated and filed to the eChart appear here. The categories and subcategories are organization-defined (not standardized), meaning content varies by site. This could include clinical notes, lab reports, radiology reports, pathology reports, consent forms, referral letters, operative notes — essentially anything the organization files to eChart. However, it's all rendered as images/PDFs, not structured data.

2. **FHIR Resource Bundle (all versions)**: US Core STU 3.1.1 Patient $everything. Covers standard USCDI clinical data (conditions, medications, allergies, vitals, encounters, labs, procedures, immunizations, etc.) in structured form.

3. **Structured Clinical Documents (all versions)**: C-CDA XML documents (care summaries, discharge summaries, etc.). Standard transitions-of-care documents.

4. **Financial Reports (6 of 7 versions, not HCA MAGIC)**: Patient accounting transactions (FinancialEHI.txt), resident trust (Expanse/6.1x), cost estimation (Expanse). Rendered as TXT — format and fields unknown.

5. **Authorization & Referral Management Reports (Expanse 2.2, 2.1, 6.15 only)**: Auth/referral data and insurance eligibility. Rendered as PDF.

6. **Ambulatory Results (Expanse 2.2, 2.1, 6.15 only)**: Manual-entry and outside-vendor micro/lab results. Rendered as PDF.

7. **Immunizations (varies by version)**: Immunization history as PDF or TXT.

8. **Provider Messages / Patient Notices (varies by version)**: Patient-physician communications. TXT or PDF.

9. **Implantable Devices (C/S, MAGIC only)**: Medical device data as TXT.

10. **Utilization Review (Expanse 2.2, 2.1, 6.15)**: Case management reviews as PDF.

11. **Population Health (Expanse 2.2, 2.1 only)**: External aggregated data.

12. **Historical Ambulatory Data (Expanse 2.2, 2.1, 6.15)**: Migrated historical records.

The richest version (Expanse 2.2) has 10 content sections. The most limited (HCA MAGIC 5.67) has only 5 sections (Electronic Chart, C-CDA, FHIR, Provider Messages, Implantable Devices — notably missing Financial Reports).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR Patient resource (US Core); possibly in Electronic Chart documents | Structured via FHIR but limited to US Core Patient elements. Full registration data (guarantors, employers, detailed insurance, emergency contacts) not in structured form. |
| Encounters / visits | ⚠️ Partial | FHIR Encounter resource (US Core); encounter-linked eChart documents | Structured encounter metadata via FHIR. Detailed encounter documentation (nursing flowsheets, assessments) only as rendered documents. |
| Problems / conditions / diagnoses | ⚠️ Partial | FHIR Condition resource (US Core); eChart may contain diagnosis documentation | Structured via FHIR US Core. Limited to US Core Condition Must Support fields. |
| Medications / prescriptions | ⚠️ Partial | FHIR MedicationRequest (US Core); pharmacy data likely in eChart documents | Structured prescriptions via FHIR. Detailed MAR, dispensing records, pharmacy workflow data not in structured form. |
| Allergies | ✅ Covered | FHIR AllergyIntolerance (US Core) | Adequate via FHIR. |
| Immunizations | ✅ Covered | FHIR Immunization (US Core) + dedicated Immunization History PDF/TXT section | Covered in both structured (FHIR) and document (PDF/TXT) form. |
| Vitals | ⚠️ Partial | FHIR Observation (US Core vital signs profiles) | Standard vital signs via FHIR. Beyond-USCDI vitals or flowsheet data only in eChart documents. |
| Lab results | ⚠️ Partial | FHIR Observation/DiagnosticReport (US Core); Ambulatory Results PDFs (manual/OV); eChart documents | Structured via FHIR for standard labs. Ambulatory manual/OV results as rendered PDF. Detailed lab result metadata (specimen, comments, delta checks) not in structured form. |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport (US Core); eChart documents likely contain radiology reports | Structured report metadata via FHIR. Full radiology/imaging reports as rendered documents in eChart. |
| Procedures | ⚠️ Partial | FHIR Procedure (US Core); operative notes in eChart | Procedure records via FHIR. Detailed surgical/operative records only as documents. |
| Clinical notes / documents | ✅ Covered | Electronic Chart section (all document types organized by category/subcategory); C-CDA documents | Broad coverage via eChart documents — clinical notes, discharge summaries, H&Ps, consult notes, etc. However, these are all rendered images/PDFs, not structured note content. C-CDA provides structured clinical summaries. |
| Care plans / goals | ⚠️ Partial | FHIR CarePlan/Goal (US Core); Utilization Review PDFs | Standard care plans via FHIR. Case management utilization reviews as PDF. |
| Orders / referrals | ⚠️ Partial | FHIR MedicationRequest/ServiceRequest (US Core); Authorization & Referral Management Reports (PDFs); Ambulatory Order Summary (undocumented, 6.08 only) | Basic order data via FHIR. Auth/referral data as rendered PDFs for Expanse/6.15. Missing structured order details. Ambulatory Order Summary referenced but not documented. |
| Insurance / coverage | ⚠️ Partial | ARMEHI-InsEligCopayDeductData.pdf (Expanse/6.15 only); FHIR may include basic Coverage | Insurance eligibility as rendered PDF for newer versions only. No structured insurance/coverage export for C/S, MAGIC, 6.08. Product stores detailed registration/insurance data. |
| Claims / billing | ⚠️ Partial | FinancialEHI.txt (patient accounting transactions) | Financial transactions exported as TXT for most versions, but format is undocumented. No evidence of detailed claims/charge-level data or structured billing records. Not available for HCA MAGIC. |
| Payments | ⚠️ Partial | FinancialEHI.txt may include payment transactions | Unclear — the FinancialEHI.txt "patient accounting report" may include payments, but format is undocumented. |
| Consents / directives | ⚠️ Partial | eChart may contain scanned consent forms | Likely in Electronic Chart if scanned, but not as a dedicated structured section. |
| Patient communications / portal messages | ⚠️ Partial | Provider Messages (TXT, C/S/MAGIC); Patient Notices (PDF, 6.08) | Patient-provider messages exported for legacy platforms. For Expanse, no dedicated messaging section — portal messages may be in eChart or missing. |
| Specialty-specific (oncology, L&D, mental health, surgical, critical care, home health, dietary) | ⚠️ Partial | eChart may contain specialty documentation as rendered documents | MEDITECH has extensive specialty modules (Oncology, L&D, Mental Health, Surgical Services, Critical Care, Home Health, Hospice, Dietary). No dedicated export sections for any specialty data. Specialty documentation may exist as rendered documents in eChart, but all structured specialty data (e.g., oncology treatment protocols, L&D records, mental health assessments) is lost in the rendering. |

## 6. Documentation Quality

**Can a developer build an import from this documentation?** Partially. A developer could:
- Parse the FHIR bundle using standard FHIR R4/US Core libraries
- Parse C-CDA documents using standard CDA parsers
- Navigate the eChart folder structure and display images/PDFs
- Parse the NDJSON Table of Contents (well-documented with 27 fields)

A developer could **not**:
- Parse the FinancialEHI.txt, ResidentTrustEHI.txt, or CostEstimation.txt files (format undocumented)
- Parse the Provider Messages.txt or Immunization Record.txt files (format undocumented)
- Understand what categories/subcategories to expect in the Electronic Chart (organization-defined)
- Extract structured data from the rendered PDFs (Authorization, Ambulatory Results, Immunization History, Utilization Review, Population Health)
- Know what Ambulatory Order Summary contains (section referenced but not described)

**Machine-readable artifacts**: The NDJSON Table of Contents schema is well-documented with a pseudo-JSON example showing all 27 fields. The FHIR bundle and C-CDA are documented by reference to their respective standards. No sample export files are provided.

**Documentation gaps**:
- No data dictionary for Config 1 (contrast with Config 2's 752 tables / 2,834 fields across three PDF dictionaries)
- No field-level documentation for any non-FHIR/non-C-CDA section
- No sample data or example exports
- No documentation of TXT file formats (FinancialEHI.txt, etc.)
- Implementation guides behind customer portal login
- "Ambulatory Order Summary" section referenced but not described

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

Config 1 attempts to cover multiple data domains beyond USCDI — financial transactions, authorization/referral management, utilization review, population health, provider messages, and implantable devices are all present as dedicated sections supplementing the FHIR/C-CDA core. This represents genuine engagement with (b)(10) requirements; the vendor clearly understood the need to go beyond the (g)(10) FHIR API.

However, the coverage is partial because:
1. **Document-centric export loses structured data.** The Electronic Chart exports rendered images/PDFs. MEDITECH stores enormous amounts of structured data (lab results with discrete values, medication administration records, nursing assessments with coded data, vital signs with timestamps) in its database tables. When this data is exported as rendered documents, the structured information is lost. A scanned lab report image is not equivalent to a structured lab result table.
2. **Significant domain gaps for non-Expanse versions.** HCA MAGIC 5.67 (the most deployed MAGIC variant, serving 190+ hospitals) gets only 5 sections with no Financial Reports, no Authorization/Referral data, no Immunization History, and no Patient Notices. The export degrades substantially for older platforms.
3. **Specialty clinical data not specifically addressed.** Despite MEDITECH having dedicated modules for Oncology, Labor & Delivery, Mental Health, Surgical Services, Critical Care, Home Health, Hospice, and Dietary, no dedicated export sections exist for any specialty. The documentation provides no indication that specialty-specific structured data (oncology protocols, L&D records, mental health assessments) is included beyond what appears in eChart documents.
4. **No structured tabular data export.** Unlike Config 2 (which exports CSV files from 97–333 database tables), Config 1 exports zero structured tabular data beyond FHIR/C-CDA. All the additional sections beyond FHIR and C-CDA are rendered reports.

**Axis 2 — Export approach: Purpose-built EHI export**

Despite the coverage limitations, this is clearly a purpose-built (b)(10) export, not a repackaged (g)(10) FHIR API:

1. The export is explicitly labeled as §170.315(b)(10) and described as a ZIP file (not an API).
2. It includes 15 content sections, only 2 of which (FHIR and C-CDA) overlap with the existing clinical exchange surface.
3. Financial reports, authorization/referral data, utilization review, provider messages, and implantable devices are all non-USCDI data domains added specifically for (b)(10).
4. The Electronic Chart section exports the entire scanned/electronic document archive — a fundamentally different approach from the FHIR API.
5. The NDJSON Table of Contents conforms to the Argonaut EHI Export API IG (draft), showing awareness of emerging EHI export standards.
6. The export varies by platform version, with newer platforms getting richer exports (10 sections for Expanse vs 5 for HCA MAGIC) — indicating ongoing investment.

The vendor has invested in building a distinct (b)(10) capability. The main limitation is the architectural choice to export supplemental data as rendered documents rather than structured data, and the complete absence of a data dictionary for Config 1.

### Key Findings

1. **Document-centric architecture is the defining limitation.** Config 1 exports the patient's Electronic Chart (rendered documents) plus FHIR/C-CDA plus supplemental reports. The supplemental reports (financial, auth/referral, immunization, utilization review, etc.) are all rendered PDFs or TXT files with undocumented formats. Structured data stored in MEDITECH's database tables is lost in this rendering. This is a fundamental architectural difference from Config 2 (which exports 97–333 CSV tables with field-level dictionaries).

2. **No data dictionary for Config 1.** The documentation provides no field-level detail for any export section beyond referencing FHIR US Core and C-CDA standards. The FinancialEHI.txt format is not described. The authorization reports are PDFs with no schema. Compare this to Config 2's three PDF data dictionaries covering 752 tables and 2,834 fields.

3. **FHIR component is standard (g)(10) surface.** The FHIR bundle explicitly references US Core STU 3.1.1 and Patient $everything — this is exactly the (g)(10) API output bundled into a file. No vendor-specific extensions or broader FHIR resource types are documented.

4. **Coverage degrades substantially for legacy platforms.** HCA MAGIC 5.67 (serving 190+ HCA hospitals) gets only 5 sections: Electronic Chart, C-CDA, FHIR, Provider Messages, and Implantable Devices. No financial data, no authorization/referral data, no immunization history.

5. **Genuine (b)(10) effort with the wrong architecture for structured data.** MEDITECH clearly built Config 1 as a purpose-specific (b)(10) export with 15 sections covering financial, administrative, and clinical domains. However, by routing everything through the eChart/HIM document paradigm (rendered images/PDFs), they export the *visual* record rather than the *structured* record. The contrast with Config 2's CSV-based approach makes this limitation especially clear.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   Mixed (ZIP containing FHIR R4 JSON, C-CDA XML, PDF, TXT, PNG/JPG/TIF/BMP images, NDJSON metadata)
Entities:        15 export sections (no structured data dictionary)
Fields:          N/A (no data dictionary; 27 NDJSON schema fields documented)
Descriptions:    N/A (sections described at folder/file level only)
Sample data:     No
Bulk export:     No (single-patient ZIP only)
Domains covered: ~13 of 19 applicable domains (most only partially, via rendered documents)
```

### Bottom Line

MEDITECH's Config 1 is a genuine (b)(10) export effort that goes beyond USCDI by including financial data, authorization/referral reports, utilization review, and other administrative data. However, the document-centric architecture means nearly all data beyond FHIR/C-CDA is exported as rendered images or undocumented text files rather than structured data. A patient would receive their complete document archive (everything scanned or filed to eChart) but would lose the ability to computationally process their structured clinical, financial, and administrative data. The single biggest gap is the absence of any structured tabular data export — the same underlying data that Config 2 exports as CSV from hundreds of database tables is instead rendered as unstructured documents in Config 1.

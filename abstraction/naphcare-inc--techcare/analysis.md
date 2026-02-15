# EHI Export Analysis: NaphCare, Inc.

**Product**: TechCare® Version 5.0
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.2813.Tech.05.00.0.191208 (CHPL Product ID 10207)

## 1. Product Context

TechCare is a corrections-specific EHR built by NaphCare, Inc., a correctional healthcare services company headquartered in Birmingham, Alabama. TechCare is deployed in 220+ local and state correctional facilities, managing over 200,000 active patient records daily. It was the first EHR purpose-built for correctional healthcare.

TechCare is a comprehensive medical operations platform, not just clinical charting. Key data domains relevant to EHI export completeness:

- **Core clinical**: Demographics, encounters, problems, medications, allergies, vitals, immunizations, lab/radiology results, clinical notes
- **Corrections-specific clinical**: Intake screening/receiving assessments, health services requests (sick calls), mental health/behavioral health assessments (substance abuse, detox, suicide prevention, MAT), diet orders
- **Orders & referrals**: Medication orders, lab orders, treatment orders, specialty consult/offsite orders (hospitalization, ER, specialty referrals), admission/discharge orders
- **Medication administration**: Detailed MAR tracking via TechCare GO module
- **Billing/claims**: Claims processing, Medicaid processing integration (per Carahsoft product description — may be handled by separate NaphCare administrative systems rather than TechCare itself)
- **Patient portal**: MyCare patient portal for incarcerated individuals
- **Telehealth**: STATCare 24/7 telehealth sessions
- **Documents**: Scanned records, wound photos, faxed progress notes from outside clinics

The certified criteria include (b)(10) EHI Export, (b)(1) Transitions of Care (C-CDA), (a)(12) Family Health History, (a)(14) Implantable Device List, and (b)(11) Care Plan, establishing baseline expectations for what the export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-page.html` (24 KB) | Full EHI Export documentation page from devportal.techcareehr.com — Word-to-HTML document containing purpose statement, export format description, assumptions, and data dictionary (as embedded images). Last updated 11/28/2023. | **Primary source** — contains all substantive documentation |
| `image003.jpg` through `image020.jpg` (12 images) | Data dictionary screenshots showing database table schemas with columns for Unique Key, Name, Data Type, Description/Attributes, and NULLABLE. One image per CSV export table. | **Primary source** — these ARE the data dictionary |
| `image001.png` (12 KB) | Screenshot of TechCare UI showing export notification with "All Facilities" dropdown and Messages badge | Minor — shows export trigger mechanism |
| `screenshot-ehi-export-full-page.png` (3.7 MB) | Full-page browser screenshot of the rendered EHI Export documentation page | Useful for visual verification of page layout |
| `screenshot-ehi-export-page-top.png` (208 KB) | Top portion of the EHI Export page | Minor |

**Verified**: The live URL (https://devportal.techcareehr.com/EHIExport) was fetched on 2026-02-15 and its content matches the collected HTML exactly — no updates since the 11/28/2023 date indicated on the page. No additional artifacts (sample data, schemas, downloadable files) were found.

## 3. Export Mechanics

- **Format**: Three file types per patient:
  1. **CSV files** — one per data category (12 categories documented), with header rows
  2. **C-CDA documents** — one per patient, covering 8 additional clinical data types
  3. **PDF files** — images (wound photos) and scanned paper records, named for patient identification
- **Mechanism**: UI-driven — administrative users can trigger single-patient export at any time without developer assistance. Notification appears in TechCare Messages when export is ready for download.
- **Single-patient**: Available on-demand, completes in minutes or seconds
- **Bulk/all-patients**: Uses a "side-loaded export engine" that continuously produces files for all patients. Same file types as single-patient.
- **Access constraints**: Limited to users with administrative rights. No third-party software required.
- **Fees**: Not mentioned in documentation. Mandatory disclosures at https://www.techcareehr.com/#costandlimitations (not collected).

## 4. Export Content: What's In It

### CSV Data Dictionary

The data dictionary is presented as 12 screenshot images of database table schemas. Each image shows a table with columns: **Unique Key**, **Name**, **Data type**, **Description / Attributes**, and **NULLABLE**. The primary key linking patients across tables is `INMATES.ID`.

From manual transcription of all 12 images (see `analysis/parse_data_dictionary.py` and `analysis/full-entity-inventory.json`):

- **12 CSV tables**
- **163 total fields**
- **163/163 (100%) fields have descriptions** — every field has a human-readable description explaining what it contains
- **163/163 (100%) fields have SQL Server data types** — e.g., `nvarchar(50)`, `datetime`, `int`, `float`
- **16 foreign key references** to lookup/reference tables (e.g., `dbo.DIET_TYPES`, `dbo.CVX`, `dbo.MEDISPAN`)
- **Lookup table contents are NOT provided** — the dictionary references tables like `dbo.OFF_SITE_SPECIALTY_TYPES` but never lists the actual values

### C-CDA Content

8 additional clinical data types are exported exclusively via C-CDA (not as separate CSVs): Medication Administrations, Vital Signs, Diagnostic Results, Treatment Plans (Plan of Care), Social History, Assessments, Functional Status, Mental Status. No further detail is provided about C-CDA template structure, sections used, or level of detail.

### PDF Content

All images and scanned paper records from the patient's encounter history are exported as PDFs with naming conventions for patient identification.

### Vendor's own content organization

| Entity/Table | Fields | Described | Types | Source Image |
|---|---|---|---|---|
| Demographics | 10 | 10 | Yes | image003.jpg |
| Medications | 21 | 21 | Yes | image005.jpg |
| Allergies | 13 | 13 | Yes | image007.jpg |
| Problem List | 10 | 10 | Yes | image009.jpg |
| Flags | 8 | 8 | Yes | image011.jpg |
| Appointments | 13 | 13 | Yes | image012.png |
| Diet Orders | 12 | 12 | Yes | image014.jpg |
| Lab Orders | 14 | 14 | Yes | image015.png |
| Treatment Orders | 12 | 12 | Yes | image016.png |
| Specialty Consult Orders | 13 | 13 | Yes | image017.png |
| Admission Orders | 12 | 12 | Yes | image018.png |
| Immunizations | 25 | 25 | Yes | image020.jpg |
| **Totals** | **163** | **163** | — | — |

Additionally, 8 C-CDA data types are exported but with no field-level documentation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into three tiers:

1. **CSV exports (12 tables, 163 fields)**: These cover discrete, structured data from TechCare's native database — demographics, medication orders, allergies, problem list, patient flags/alerts, appointments, diet orders, lab orders, treatment orders, specialty consult/offsite orders, admission/discharge orders, and immunizations. This is the best-documented tier, with field-level descriptions, data types, and nullability for every field. The Immunizations table is the richest (25 fields including CVX codes, VIS tracking, refusal reasons), while Flags is the thinnest (8 fields).

2. **C-CDA exports (8 data types)**: These cover clinical data types that the vendor chose to export via C-CDA rather than CSV — vital signs, medication administrations, diagnostic results, treatment plans, social history, assessments, functional status, and mental status. This tier is essentially undocumented beyond naming the 8 categories. No field-level detail, no template specifications, no sample data.

3. **PDF exports**: Images and scanned paper records. Appropriately handled as PDFs given their non-discrete nature.

The CSV tier is genuinely native database data — the field names, SQL Server data types, and `dbo.` table references clearly come from TechCare's internal schema, not from a standard like FHIR or C-CDA. The C-CDA tier appears to be a standard projection for data types the vendor didn't create separate CSV tables for.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Demographics` CSV (10 fields) — ID, booking info, custody status, name, DOB, gender, housing, SSN | Covered but thin for a corrections EHR: missing race/ethnicity, language, emergency contacts, next-of-kin |
| Encounters / visits | ⚠️ Partial | No dedicated encounter table. `Appointments` CSV tracks scheduling. C-CDA "Assessments" may contain encounter data. PDF section mentions "entire encounter history documentation" | Product tracks clinical encounters extensively; no structured encounter export is a significant gap |
| Problems / conditions / diagnoses | ✅ Covered | `Problem List` CSV (10 fields) — ICD-10 codes, date identified/resolved, resolve text | Adequate |
| Medications / prescriptions | ✅ Covered | `Medications` CSV (21 fields) — drug names (MEDISPAN), SIG, GPI, route, order type (PRN/DOT/KOP), quantity, refills, prescriber NPI | Strong — includes pharmacological detail |
| Allergies | ✅ Covered | `Allergies` CSV (13 fields) — allergy name/type, NDC, GPI, allergy class, SNOMED-coded reactions | Good — includes coded reactions |
| Immunizations | ✅ Covered | `Immunizations` CSV (25 fields) — CVX, MVX, lot numbers, VIS tracking, refusal reasons, route, site | Most detailed table in the export |
| Vitals | ⚠️ Partial | C-CDA "Vital Signs" only — no CSV table, no field-level documentation | Product is certified for (a)(5) vitals; C-CDA-only export with no documentation is thin |
| Lab results | ⚠️ Partial | `Lab Orders` CSV (14 fields) covers orders only. C-CDA "Diagnostic Results" presumably covers results, but no field-level documentation | Orders are well-documented; results are C-CDA-only with no detail |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA "Diagnostic Results" may include imaging. No dedicated imaging table. | Product integrates with radiology; unclear if imaging results are in the export |
| Procedures | ⚠️ Partial | `Treatment Orders` CSV (12 fields) covers treatment/procedure orders. No procedure results/outcomes table. | Orders documented but outcomes/results not separately captured |
| Clinical notes / documents | ⚠️ Partial | PDF section exports scanned records and images. No structured clinical note export (no encounter notes, progress notes, H&P). C-CDA sections may contain some note content. | **Significant gap** — clinical encounter notes are core EHI. TechCare captures extensive clinical documentation; its absence from the structured export is notable. |
| Care plans / goals | ⚠️ Partial | C-CDA "Treatment Plans (Plan of Care)" — no field-level documentation. Product is certified for (b)(11) Care Plan. | C-CDA-only, undocumented |
| Orders / referrals | ✅ Covered | `Lab Orders` (14), `Treatment Orders` (12), `Specialty Consult Orders` (13), `Diet Orders` (12), `Admission Orders` (12) — 5 order tables with 63 fields total | Strong — multiple order types with corrections-specific detail (offsite/hospitalization/ER referrals) |
| Insurance / coverage | ❌ Not covered | No insurance or coverage entities in the export | Unclear if TechCare stores insurance data directly vs. NaphCare's separate administrative systems. If stored, it's a gap. |
| Claims / billing | ❌ Not covered | No billing or claims entities in the export | Product documentation mentions claims processing and Medicaid integration, but this may be handled by separate NaphCare systems. If TechCare stores billing data, it's a gap. |
| Payments | ❌ Not covered | No payment entities in the export | Same uncertainty as billing — may not be in TechCare's scope |
| Consents / directives | ❌ Not covered | No consent entities. Immunization "Reason Not Given" and "VIS Given" fields capture some consent-adjacent data. | May be captured in scanned PDFs but no structured export |
| Patient communications / portal messages | ❌ Not covered | MyCare patient portal activity not in export | Product has MyCare portal; portal messages are patient EHI |
| Specialty: Corrections intake screening | ❌ Not covered | No intake/receiving screening table | **Significant gap** — receiving screenings are a core correctional healthcare workflow and a primary data type for this product |
| Specialty: Mental/behavioral health | ⚠️ Partial | C-CDA "Mental Status" and "Assessments" may cover some MH data. No dedicated tables for substance abuse assessments, detox tracking, suicide prevention documentation, or MAT records. | **Significant gap** — behavioral health is core to correctional healthcare. Product has dedicated MH modules (Detox Dashboard, Substance Abuse Level of Care, suicide prevention); none appear in the structured export. |
| Specialty: Health services requests (sick calls) | ❌ Not covered | No HSR/sick call table. Product has dedicated HSR dashboards. | Gap — sick call requests are part of the patient record in correctional settings |
| Family health history | ❌ Not covered | Not mentioned. Product is certified for (a)(12). | Minor gap — certified capability not reflected in export |
| Implantable devices | ❌ Not covered | Not mentioned. Product is certified for (a)(14). | Minor gap — certified capability not reflected in export |

## 6. Documentation Quality

**Strengths:**
- Every field in the CSV data dictionary has a human-readable description, SQL Server data type, and nullability flag — 163/163 fields fully documented
- Descriptions are contextually useful (e.g., "value is pre-populated when an alert is created from an item in a queue or list")
- Foreign key relationships are partially documented — 16 `dbo.*` table references show the underlying relational schema
- Export process is clearly described with both single-patient and bulk capabilities
- Some value sets are documented inline (e.g., CustodyStatus: "ACTIVE or NOT ACTIVE", Gender: "M or F or Male or Female")

**Weaknesses:**
- **Data dictionary is screenshot images, not machine-readable** — the entire dictionary consists of 12 JPEG/PNG screenshots of what appears to be a database design tool or spreadsheet. No CSV, JSON, XML, or other structured format is provided.
- **No sample data** — no example export files or worked examples are provided
- **C-CDA section is essentially undocumented** — 8 data types are listed by name with no detail about template structure, sections, coded entries, or field-level content
- **Lookup table values are not provided** — fields reference 16 lookup tables (e.g., `dbo.DIET_TYPES`, `dbo.OFF_SITE_SPECIALTY_TYPES`) but the actual valid values are never listed
- **No machine-readable schema** — no XSD, JSON Schema, CSV header template, or API specification
- **Stale documentation** — last updated 11/28/2023 (over 2 years ago as of analysis date)
- **Word-to-HTML export artifacts** — the page is a Microsoft Word document pasted into a web template, with VML namespaces and MSO markup artifacts

**Could a developer build an import?** Partially. The CSV tables are well-enough documented to build a parser for the 12 structured tables. However, the developer would need to: (1) reverse-engineer lookup table contents from actual export data, (2) handle the C-CDA portion with no guidance beyond data type names, (3) handle PDF documents with no schema for naming conventions, and (4) accept that significant portions of clinical data (encounter notes, vitals, lab results, MH assessments) are either in the opaque C-CDA or missing entirely.

## 7. Overall Assessment

### Classification

**Partial native export.** The CSV portion represents a genuine native data model export from TechCare's SQL Server database — 12 tables with field-level documentation drawn from the actual schema. However, the export has significant coverage gaps: clinical encounter notes, behavioral health records, intake screenings, health services requests, and potentially billing data are absent from the structured export. The C-CDA component serves as a catch-all for data types without dedicated CSV tables, but is essentially undocumented, making it impossible to assess what those 8 data types actually contain. The result is a hybrid export where perhaps half the clinical data is well-documented native database extract and the other half is an opaque C-CDA blob.

### Key Findings

1. **The CSV data dictionary is well-crafted but narrow**: 12 tables, 163 fields, 100% with descriptions and types — this is real schema documentation, not boilerplate. But 12 tables is thin for a system described as a "complete medical operations system" with extensive modules.

2. **Clinical encounter notes appear absent**: The largest category of clinical documentation — encounter notes, progress notes, H&P — has no dedicated CSV table and isn't explicitly listed in the C-CDA section. The PDF section mentions "encounter history documentation" for scanned records, but structured encounter notes are unaccounted for.

3. **Corrections-specific clinical data is mostly missing**: Despite being the first corrections-specific EHR, the export lacks dedicated tables for intake screenings, health services requests (sick calls), substance abuse assessments, detox tracking, and suicide prevention documentation — the very workflows that differentiate TechCare from a general-purpose EHR.

4. **The C-CDA section is a documentation gap, not a strength**: Listing 8 data types by name without any field-level detail, template specification, or sample data means these categories cannot be independently assessed. Key clinical data (vitals, lab results, assessments, mental status) may be adequately represented in the C-CDA — or may not be.

5. **No sample data or machine-readable artifacts**: The data dictionary exists only as screenshot images. No sample export files, no downloadable schemas, no JSON/CSV version of the dictionary itself.

### Summary Stats

    Classification:  Partial native export
    Export format:   CSV + C-CDA + PDF (mixed)
    Model type:      Hybrid (native database for CSV; standard projection for C-CDA)
    Entities:        12 CSV tables + 8 C-CDA data types
    Fields:          163 (CSV only; C-CDA fields undocumented)
    Descriptions:    100% of CSV fields
    Sample data:     No
    Bulk export:     Yes (side-loaded export engine for all patients)
    Domains covered: 7 of 19 applicable domains fully covered; 7 partial; 5 not covered

### Bottom Line

TechCare's EHI export makes a genuine effort with its CSV component — 12 native database tables with solid field-level documentation. But for a product that runs all healthcare operations in 220+ correctional facilities, 12 tables and 163 fields is thin. The most significant gaps are clinical encounter notes (the core of any patient record), corrections-specific clinical workflows (intake screenings, sick calls, behavioral health assessments), and the complete absence of documentation for the C-CDA component that supposedly covers vitals, lab results, and mental health data. A patient requesting their full record would get medication orders, allergies, problem list, and immunizations in usable form — but their encounter notes, mental health records, and much of their clinical narrative would either be buried in an opaque C-CDA or missing entirely.

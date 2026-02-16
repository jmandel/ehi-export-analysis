# EHI Export Analysis: NaphCare, Inc.

**Product**: TechCare®  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2813.Tech.05.00.0.191208

## 1. Product Context

TechCare® is a corrections-specific EHR built by NaphCare, Inc., a correctional healthcare services company. It is purpose-built for jails, prisons, and detention facilities — not adapted from an ambulatory or hospital EHR. The product operates in 220+ correctional facilities managing 200,000+ active patient records.

TechCare is described as a "complete medical operations system" encompassing:

- **Clinical documentation**: Intake screenings, encounter notes, problem lists, medication lists, allergy lists, vitals, care plans
- **Medication management**: MAR, pharmacy integration (NaphCare Rx), TechCare GO offline medication administration
- **Mental health/behavioral health**: Substance abuse assessments, detox tracking, MAT support, suicide prevention documentation
- **Orders**: Lab, treatment, diet, specialty consult/offsite, admission orders
- **Immunizations**: Full vaccine tracking with CVX codes and registry integration
- **Diagnostics**: Lab results, radiology integration
- **Telehealth**: STATCare 24/7 telehealth encounters
- **Patient portal**: MyCare portal for incarcerated patients
- **Administrative**: Claims processing, Medicaid processing, hospital referral management, scheduling, compliance monitoring (NCCHC standards)
- **Correctional-specific**: Booking/custody status tracking, housing location, intake screening, discharge planning, records across prior incarcerations

The breadth of the product — spanning clinical, pharmacy, behavioral health, diagnostics, claims/billing, and correctional-specific workflows — sets a high bar for what a comprehensive EHI export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.html` | Full EHI Export documentation page (Word-to-HTML), 24 KB. Contains purpose statement, export format description, assumptions, and data dictionary section headings with embedded images. Last updated 11/28/2023. | **High** — primary documentation source |
| `downloads/image003.jpg` | Data dictionary: Demographics table (10 fields) | **High** — field-level detail |
| `downloads/image005.jpg` | Data dictionary: Medications table (21 fields) | **High** |
| `downloads/image007.jpg` | Data dictionary: Allergies table (13 fields) | **High** |
| `downloads/image009.jpg` | Data dictionary: Problem List table (10 fields) | **High** |
| `downloads/image011.jpg` | Data dictionary: Flags/Alerts table (8 fields) | **High** |
| `downloads/image012.png` | Data dictionary: Appointments table (13 fields) | **High** |
| `downloads/image014.jpg` | Data dictionary: Diet Orders table (12 fields) | **High** |
| `downloads/image015.png` | Data dictionary: Lab Orders table (14 fields) | **High** |
| `downloads/image016.png` | Data dictionary: Treatment Orders table (12 fields) | **High** |
| `downloads/image017.png` | Data dictionary: Specialty Consult Orders table (13 fields) | **High** |
| `downloads/image018.png` | Data dictionary: Admission Orders table (12 fields) | **High** |
| `downloads/image020.jpg` | Data dictionary: Immunizations table (25 fields) | **High** |
| `downloads/image001.png` | Screenshot: TechCare UI showing EHI export notification | Low — UI context only |
| `downloads/screenshot-ehi-export-full-page.png` | Full-page browser screenshot of entire EHI Export documentation page (3.6 MB) | Low — confirms page layout |

All data dictionary images are screenshots of database table schemas showing column name, data type, description/attributes, and nullable status. The documentation page itself is a Word document converted to HTML and hosted on the TechCare 5.0 API developer portal.

## 3. Export Mechanics

- **Format**: Three-part export: (1) CSV files for structured data (one per entity, with header row), (2) C-CDA documents for clinical data types not covered by CSV, (3) PDF files for images and scanned paper records
- **Mechanism**: UI-driven — users with administrative rights can trigger a single-patient export at any time "without Developer assistance." A notification message appears when the export is ready for download. Bulk (all-patient) export uses a "side-loaded export engine that scalably produces the files continuously for all patients."
- **Single-patient**: Yes, available on-demand
- **Bulk export**: Yes, all patients supported via the same file types
- **Access constraints**: Limited to users with administrative rights. No fees mentioned. No third-party software required.
- **Documentation link**: Included with every export output per the documentation

## 4. Export Content: What's In It

### CSV Data Dictionary

The data dictionary documents **12 CSV entities** with a total of **163 fields**. Every field (100%) has a description, a data type, and a nullable indicator. The data dictionary is presented as images of database table schemas — not machine-readable, but fully human-readable with complete metadata per field.

Database table references (foreign keys) are documented inline in descriptions (e.g., "References: dbo.INMATES", "References: dbo.USERS", "References: dbo.DIET_TYPES"). Value sets are partially documented (e.g., CustodyStatus: "ACTIVE or NOT ACTIVE"; Gender: "M or F or Male or Female"; Allergy Class: "Drug, Class, or Environmental").

### C-CDA Content

The documentation states that 8 additional data types are provided exclusively via C-CDA because "due to their format and archival structure, they remain the most broadly useful and importable into other certified EHRs via existing C-CDA functionality":

1. Medication Administrations
2. Vital Signs
3. Diagnostic Results
4. Treatment Plans (Plan of Care)
5. Social History
6. Assessments
7. Functional Status
8. Mental Status

No field-level data dictionary is provided for these C-CDA sections — they rely on the standard C-CDA specification.

### PDF Content

Images (e.g., wound pictures) and scanned paper records (e.g., faxed progress notes from outside clinics) are exported as unrestricted PDFs. No discrete data dictionary applies.

### Vendor's own content organization

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| Demographics | 10 | 10 | yes | Demographics |
| Medications | 21 | 21 | yes | Medications |
| Allergies | 13 | 13 | yes | Allergies |
| Problem List | 10 | 10 | yes | Problems |
| Flags | 8 | 8 | yes | Alerts |
| Appointments | 13 | 13 | yes | Scheduling |
| Diet Orders | 12 | 12 | yes | Orders |
| Lab Orders | 14 | 14 | yes | Orders |
| Treatment Orders | 12 | 12 | yes | Orders |
| Specialty Consult Orders | 13 | 13 | yes | Orders |
| Admission Orders | 12 | 12 | yes | Orders |
| Immunizations | 25 | 25 | yes | Immunizations |
| **Totals** | **163** | **163 (100%)** | **yes** | |

Additionally, 8 C-CDA sections provide data for vitals, medication administrations, diagnostic results, plans of care, social history, assessments, functional status, and mental status — but without field-level documentation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The CSV export covers a focused set of correctional healthcare data: **demographics** with correctional-specific fields (booking number, custody status, housing location), **medication orders** with pharmacy detail (GPI, route, quantity, refills, NPI), **allergies** with coded reactions (SNOMED, NDC), **problem list** with ICD-10 codes, **clinical alerts/flags**, **appointments**, and **five order types** (diet, lab, treatment, specialty consult, admission). **Immunizations** is the most detailed entity at 25 fields including CVX codes, VIS tracking, manufacturer (MVX), lot numbers, and refusal reasons.

The C-CDA supplement adds coverage for **vital signs, medication administrations, diagnostic results, care plans, social history, assessments, functional status, and mental status** — all critical clinical domains. However, these rely entirely on the C-CDA standard specification with no product-specific field documentation.

The **Orders** category is the richest in the CSV portion (5 entities, 63 fields), reflecting the correctional healthcare workflow emphasis on tracking multiple order types. The **Specialty Consult Orders** entity is particularly correctional-specific, covering offsite, hospitalization, onsite, and ER referral types.

The thinnest areas: **Demographics** has only 10 fields (no race, ethnicity, language, emergency contacts, next of kin). **Flags** has only 8 fields. There are no separate encounter/visit entities in the CSV — encounters appear to be captured only via the C-CDA.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Demographics` CSV (10 fields): ID, booking number, custody status, name, DOB, gender, housing, SSN | Missing race, ethnicity, language, contact info. Correctional-specific fields (booking, custody, housing) are present but standard demographic detail is thin. |
| Encounters / visits | ⚠️ Partial | No dedicated CSV entity; C-CDA likely contains encounter sections; `Appointments` CSV captures scheduling | Product tracks encounter documentation extensively; no structured encounter export in CSV. C-CDA may partially cover this. |
| Problems / conditions / diagnoses | ✅ Covered | `Problem List` CSV (10 fields): ICD-10 codes, dates identified/resolved, resolve text | Reasonable coverage for problem list functionality. |
| Medications / prescriptions | ✅ Covered | `Medications` CSV (21 fields): drug name, SIG, GPI, route, quantity, refills, prescriber NPI, start/stop dates | Detailed medication order data. Medication Administrations provided via C-CDA only. |
| Allergies | ✅ Covered | `Allergies` CSV (13 fields): allergy name, class (drug/environmental), NDC, GPI, SNOMED reaction | Well-documented with coded values. |
| Immunizations | ✅ Covered | `Immunizations` CSV (25 fields): CVX, manufacturer/MVX, lot, route, site, VIS tracking, refusal reasons | Most detailed entity — comprehensive immunization documentation. |
| Vitals | ⚠️ Partial | Via C-CDA only ("Vital Signs" section) | Product is certified for vitals (a)(5); no CSV entity for vitals, only C-CDA. No field-level documentation. |
| Lab results | ⚠️ Partial | `Lab Orders` CSV (14 fields) captures order metadata only; `Diagnostic Results` via C-CDA | Lab Orders CSV has order info but no result values — results appear only in C-CDA. |
| Imaging / diagnostic reports | ⚠️ Partial | Via C-CDA "Diagnostic Results" section; scanned images via PDF | No structured imaging data dictionary. |
| Procedures | ⚠️ Partial | `Treatment Orders` CSV (12 fields) covers treatment-type orders; C-CDA may contain procedure sections | Treatment orders are documented but no dedicated procedures entity. |
| Clinical notes / documents | ⚠️ Partial | Scanned/faxed records exported as PDF; C-CDA contains assessments, functional/mental status | No structured clinical notes entity in CSV. Encounter notes appear to be in C-CDA or PDF only. |
| Care plans / goals | ⚠️ Partial | Via C-CDA "Treatment Plans (Plan of Care)" section | No CSV entity; relies on C-CDA standard. |
| Orders / referrals | ✅ Covered | 5 CSV order entities: Diet Orders, Lab Orders, Treatment Orders, Specialty Consult Orders, Admission Orders (63 total fields) | Strong order coverage with correctional-specific types (offsite consults, admissions). |
| Insurance / coverage | ❌ Not covered | No insurance entities in export | Product integrates with Medicaid processing; gap depends on whether TechCare stores insurance data or passes through to external systems. |
| Claims / billing | ❌ Not covered | No billing/claims entities in export | Product handles claims processing per vendor materials. Significant gap if TechCare stores patient-level billing records. |
| Payments | ❌ Not covered | No payment entities in export | Unclear if product stores patient-level payment data. |
| Consents / directives | ❌ Not covered | No consent entities in export | Correctional healthcare involves consent documentation; likely stored but not exported. |
| Patient communications / portal messages | ❌ Not covered | No portal/communication entities despite MyCare patient portal existing | Product has MyCare patient portal; portal interactions not exported. |
| Specialty-specific (Correctional) | ⚠️ Partial | Booking/custody data in Demographics; Admission Orders for intake; Specialty Consult Orders for offsite referrals | Correctional-specific intake screenings, behavioral health assessments, detox tracking, substance abuse level of care, and suicide prevention documentation are not exported as structured CSV. Some may appear in C-CDA "Assessments" or "Mental Status" sections. |
| Specialty-specific (Behavioral Health) | ⚠️ Partial | C-CDA sections for "Mental Status," "Assessments," "Social History" | Product has extensive behavioral health features (MAT, detox dashboard, suicide prevention). C-CDA sections are generic; no product-specific behavioral health data dictionary. |

## 6. Documentation Quality

**Strengths:**
- Every CSV field has a name, SQL Server data type (with length), description, and nullable indicator — 100% coverage
- Foreign key references are documented inline (e.g., "References: dbo.INMATES," "References: dbo.DIET_TYPES")
- Some value sets are provided (CustodyStatus values, Gender values, Allergy Class values)
- The `INMATES.ID` primary key and its role as the foundational link across all tables is explicitly documented
- Export process is clearly described (single-patient on-demand, bulk via export engine)

**Weaknesses:**
- Data dictionary is presented as **images** (JPG/PNG screenshots of tables) rather than machine-readable format — cannot be parsed programmatically without OCR
- C-CDA sections have **no product-specific field documentation** — the documentation simply lists 8 data types and says they're in the C-CDA
- No sample data files provided
- No machine-readable schema (no JSON Schema, no XSD, no SQL DDL)
- Documentation was last updated **11/28/2023** — over 2 years old
- No relationship diagrams beyond inline foreign key references
- No guidance on CSV encoding, delimiter handling, date formatting, or null representation

**Could a developer build an import?** Partially. The CSV entities are well-enough documented to build a basic import for those 12 tables. However, the C-CDA content would require trial-and-error to understand TechCare's specific C-CDA template usage, and there's no documentation on how the three export components (CSV, C-CDA, PDF) relate to each other or how files are organized in the export package.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

TechCare's export covers a moderate set of clinical domains through a combination of 12 CSV entities (163 fields) and 8 C-CDA sections. The CSV portion handles demographics, medications, allergies, problems, flags, appointments, five order types, and immunizations — a reasonable clinical core for a correctional EHR. The C-CDA supplement adds vitals, medication administrations, diagnostic results, care plans, social history, and mental health assessments.

However, significant gaps exist relative to what TechCare stores. The product handles claims processing, Medicaid integration, behavioral health workflows (detox tracking, MAT, substance abuse assessments), intake screenings, discharge planning, patient portal (MyCare) interactions, and telehealth encounters — none of which have dedicated export entities. The behavioral health data gap is particularly notable for a corrections-specific EHR where mental health and substance use treatment are core functions, not peripheral features. The C-CDA "Mental Status" and "Assessments" sections may capture some of this, but without product-specific documentation, it's impossible to assess their depth.

The export goes beyond a bare USCDI repackaging — it includes correctional-specific fields (booking number, custody status, housing location), five distinct order types, and detailed immunization tracking — but it falls short of the product's full data footprint.

**Axis 2 — Export approach: Purpose-built EHI export**

This is a purpose-built export, not a repackaged clinical exchange. The evidence:
- The CSV component exports from TechCare's native database tables (field names reference `dbo.INMATES`, `dbo.DRUG_ORDERS_ADDITIONAL_INFO`, `dbo.ADMISSION_MANAGEMENT_TYPE` — these are internal database objects)
- The export includes correctional-specific data not found in any standard clinical exchange (booking numbers, custody status, housing locations, admission management types)
- The three-format approach (CSV + C-CDA + PDF) is specifically designed for (b)(10), combining structured data dumps with clinical documents and scanned records
- The documentation explicitly addresses (b)(10) requirements and describes a purpose-built export engine
- However, the C-CDA component is the standard transitions-of-care document reused, and some data domains rely entirely on it rather than getting their own structured CSV export

### Key Findings

1. **Purpose-built but incomplete**: TechCare built a genuine (b)(10) export with native database CSV files plus C-CDA and PDF supplements, but it covers only a fraction of the product's data domains. The 12 CSV entities represent a clinical core, not the full designated record set.

2. **Strong field-level documentation where it exists**: All 163 CSV fields have descriptions, data types, and nullable indicators — 100% documentation coverage. Foreign key references and some value sets are documented. This is better than many larger vendors' data dictionaries.

3. **C-CDA used as a catch-all**: Eight data types (vitals, medication administrations, diagnostic results, care plans, social history, assessments, functional status, mental status) are exported only via C-CDA with zero product-specific documentation. This effectively delegates these domains to the standard C-CDA template without explaining what TechCare specifically includes.

4. **Major gaps in behavioral health and administrative data**: For a corrections-specific EHR, the absence of structured exports for behavioral health assessments, substance use tracking, detox records, intake screenings, claims/billing, and patient portal data represents significant gaps in the designated record set.

5. **Data dictionary as images is a documentation anti-pattern**: The entire data dictionary is embedded as JPG/PNG screenshots of database tables. This makes it impossible to programmatically parse, search, or validate. While the content is complete, the format is a barrier to usability.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   CSV + C-CDA + PDF
Entities:        12 (CSV) + 8 C-CDA sections + PDF documents
Fields:          163 (CSV only; C-CDA fields undocumented)
Descriptions:    100% (of CSV fields)
Sample data:     No
Bulk export:     Yes
Domains covered: 8 of 17 applicable domains fully or mostly covered
```

### Bottom Line

TechCare built a genuine purpose-built EHI export with well-documented CSV files from its native database, supplemented by C-CDA documents and PDFs — but the export covers only a subset of what this feature-rich correctional EHR stores. The biggest gaps are behavioral health data (a core function for corrections), claims/billing, and the absence of product-specific documentation for the 8 C-CDA data types that serve as a catch-all for everything not in CSV. A patient would get their medication orders, allergies, problem list, immunizations, and clinical notes (via C-CDA/PDF), but would likely miss their behavioral health assessments, substance use treatment records, billing history, and portal communications.

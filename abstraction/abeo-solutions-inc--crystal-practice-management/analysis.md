# EHI Export Analysis: Abeo Solutions, Inc

**Product**: Crystal Practice Management v6.0
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.1030.Crys.06.01.1.221004 (CHPL listing 10996)

## 1. Product Context

Crystal Practice Management (Crystal PM) is an all-in-one practice management and EHR platform purpose-built for optometry and ophthalmology practices. Developed by Abeo Solutions, Inc (Austin, TX; ~12–35 employees), it targets independent and multi-location eye care practices.

The product integrates the following functional modules, all relevant to EHI export completeness:

- **EHR/Clinical**: 300+ customizable exam templates, comprehensive eye exam documentation (refraction, visual acuity, tonometry, slit lamp, fundus, etc.), vision therapy records, specialty contact lens fitting, diagnostic imaging integration with 60+ ophthalmic devices (Zeiss, Marco, Optos, Humphreys), automated ICD-10 coding, clinical notes
- **E-Prescribing**: Integrated electronic prescriptions (optional add-on)
- **Billing & Claims**: Invoice creation, electronic claims via clearinghouses (Apex, Trizetto, Waystar, VSP), CMS-1500 (HCFA) forms, routing slips, medical and vision insurance claims
- **Revenue Cycle Management**: Via related entity Abeo Billing, LLC — claim submission, payment posting, A/R management, appeals
- **Optical & Inventory**: Frame and contact lens inventory (multi-location), RFID support, lab orders, barcode scanning, DME integrations
- **Patient Engagement**: Patient portal (records, prescriptions, invoices, secure messaging), Crystal Communicator (SMS), Crystal Kiosk (check-in), online intake forms, recall management
- **Scheduling**: Multi-doctor/location scheduling, drag-and-drop appointments, waitlists, automated notifications

The product is certified for (b)(10) EHI export along with a broad set of ONC criteria including FHIR API access (g)(7)–(g)(10).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/21stCenturyCuresActB10AllDataExportUserDocumentation2.pdf` | 921-page PDF data dictionary documenting the complete Crystal PM (b)(10) export. 2.6 MB. Created Oct 12, 2023 in Microsoft Word 2021. Authored by "Erik." | **Primary artifact — extremely informative.** Contains field-level documentation for every table in the export. |
| `files.json` | Manifest of downloaded files (1 file). | Orientation only. |
| `product-research.md` | Prior research on Crystal PM's features and data stores. | Useful for establishing baseline of what the product stores. |
| `ehi-export-report.md` | Prior agent's narrative about the export. Claimed 55 distinct tables; actual count is **58**. | Useful for orientation but contains minor inaccuracies. |
| `chpl-metadata.json` | CHPL certification details. | Confirms certification criteria and product version. |

The single PDF is the only artifact, and it is extraordinarily thorough.

## 3. Export Mechanics

- **Format**: CSV files — one file per database table. Serialized blob columns (containing XML-encoded .NET objects) are deserialized during export back to structured form ("CSV + Binary Deserialization").
- **Mechanism**: The documentation describes it as a "feature" of the EHR system, implying a UI-triggered export. No API endpoint is described. No step-by-step instructions or screenshots are included in the documentation — it is purely a data dictionary.
- **Single-patient vs bulk**: The title says "All Patient Data Export," suggesting a bulk export of the entire database, not a per-patient extraction.
- **Access constraints/fees**: Not described in the documentation. The CHPL mandatory disclosures URL (https://crystalpm.com/pricing/) lists FHIR server access as an optional add-on but does not specifically mention EHI export fees.

## 4. Export Content: What's In It

The export documentation is a **complete database data dictionary** covering 58 distinct database tables organized into 80 documented sections (the `ehr_file` table has 23 sub-type-specific sections, each documenting a different clinical record type stored in the same table).

### Key statistics

| Metric | Value |
|---|---|
| Total documented sections | 80 |
| Distinct database tables | 58 |
| Total fields documented | 1,368 |
| Fields with descriptions | 1,368 (100%) |
| Fields with data types | 1,368 (100%) |
| Fields with extraction method | 1,028 (75%) |
| Serialized object types documented | 2 (VisualAcuityFieldDataModel, RefractionMeasurementFieldDataModel) |

Each field entry includes: column name, MySQL data type (int, varchar, char, date, datetime, bigint, longblob, tinyint, etc.), prose description, and extraction method (CSV or CSV + Binary Deserialization / CSV + XML Deserialization).

### Vendor's own content organization

The vendor organizes the export as one CSV file per database table. The `ehr_file` table is polymorphic — a single table stores 23 different clinical record types distinguished by a `type` column. The vendor documents each sub-type as a separate section with its own field listing.

**Category breakdown (vendor's implicit grouping, reconstructed from table names and descriptions):**

| Category | Sections | Distinct Tables | Fields |
|---|---|---|---|
| Clinical / EHR | 26 | 4 | 708 |
| Insurance (VSP) | 10 | 10 | 201 |
| Patient Engagement & Communication | 7 | 7 | 101 |
| Billing & Financial | 7 | 7 | 57 |
| Documents & Images | 10 | 10 | 59 |
| Patient Demographics | 1 | 1 | 51 |
| Optical & Inventory | 7 | 7 | 50 |
| Scheduling & Appointments | 3 | 3 | 41 |
| Prescriptions & Medication | 3 | 3 | 40 |
| Referrals | 1 | 1 | 19 |
| Interoperability | 1 | 1 | 18 |
| Administrative & Compliance | 3 | 3 | 16 |
| Administrative | 1 | 1 | 7 |
| **TOTAL** | **80** | **58** | **1,368** |

### Representative entities (largest and most important)

| Entity/Section | Table | Fields | Category |
|---|---|---|---|
| VSP Claim | `vsp_claims` | 87 | Insurance (VSP) |
| Lab Result CCR | `ehr_file` | 59 | Clinical / EHR |
| Medication Order | `ehr_file` | 54 | Clinical / EHR |
| Patient | `patients` | 51 | Patient Demographics |
| Lab Order | `ehr_file` | 47 | Clinical / EHR |
| Immunization | `ehr_file` | 43 | Clinical / EHR |
| Medication - External | `ehr_file` | 42 | Clinical / EHR |
| VSP Authorization | `vsp_authorizations` | 40 | Insurance (VSP) |
| Medication History | `ehr_file` | 39 | Clinical / EHR |
| Lab Result | `ehr_file` | 36 | Clinical / EHR |
| Kno2 Message | `kno2_message` | 35 | Patient Engagement & Communication |
| Order Group | `order_groups` | 32 | Clinical / EHR |
| Eye Care Data | `ehr_file` | 31 | Clinical / EHR |
| Direct Mail Message | `directmail_message` | 29 | Patient Engagement & Communication |
| Result Group | `result_groups` | 29 | Clinical / EHR |
| Appointment | `appts` | 26 | Scheduling & Appointments |
| Implantable Device | `ehr_file` | 25 | Clinical / EHR |

### Notable details

- **`ehr_file` polymorphic table**: This single table stores 23 different clinical record types (Lab Orders, Lab Results, Immunizations, Medication Orders, Drug Allergies, Problems, Observations, Procedures, Smoking Status, Implantable Devices, Eye Care Data, and more). Each sub-type has its own field documentation section. Total: 637 fields across all 23 sub-type sections.

- **Serialized type documentation**: For the Eye Care Data sub-type, the PDF documents two .NET serialized object models in detail:
  - `VisualAcuityFieldDataModel`: target site (right/left/both eye), measurement type (distance/near/pinhole), status (corrected/uncorrected), data format, unit (FootUSOverFootUS), and method — with full enum value documentation
  - `RefractionMeasurementFieldDataModel`: target site, measurement types (sphere, cylinder, axis, add, horizontal prism, horizontal prism base, vertical prism, vertical prism base, distance visual acuity, near visual acuity, pinhole visual acuity), data format, unit, and method

  This is genuinely specialty-specific ophthalmic data that goes well beyond USCDI/standard EHR exports.

- **Binary data tables**: The export includes actual binary data for medical images (`med_image_data`), patient files (`pat_file_data`), patient photos (`pat_photo_data`), and insurance cards (`ins_card_data`), along with their metadata tables.

- **VSP vision insurance**: 10 tables / 201 fields dedicated to Vision Service Plan (VSP) claims, authorizations, eligibility, and services — reflecting the product's deep integration with vision insurance workflows.

The full entity inventory is saved at `analysis/full-entity-inventory.json` (80 entries with complete field lists).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers virtually every functional domain of the Crystal PM product:

**Deepest coverage (most entities and fields):**
- **Clinical/EHR data** (26 sections, 708 fields): The `ehr_file` table with 23 sub-types covers lab orders/results, medications (orders, history, formulary, external), drug allergies (including history, interactions, external), problems (internal and external), observations, procedures, immunizations, smoking status, implantable devices, interventions, diagnostic studies, devices, and eye care data. The `clinical_note` and `order_groups`/`result_groups` tables add further depth.
- **VSP Insurance** (10 tables, 201 fields): Extremely detailed coverage of vision insurance workflows — claims (87 fields alone), authorizations, eligibility, benefits, services. This level of detail in vision plan billing data is distinctive to an eye care product.

**Solid coverage:**
- **Patient demographics** (1 table, 51 fields): Comprehensive — name, address, SSN, DOB, family linkage, insurance balances, financial balances, communication preferences, death indicator, HL7 opt-in, location, recall type.
- **Billing & Financial** (7 tables, 57 fields): Invoices, transaction line items, payments, transaction data, HCFA/CMS-1500 claims (print and data), routing slips.
- **Documents & Images** (10 tables, 59 fields): Medical images, patient files, patient photos, insurance cards — both metadata and binary data. This is notably complete.
- **Patient Engagement** (7 tables, 101 fields): Recall, reminders (with log), direct mail messages, Kno2 secure messages, marketing records, patient comments.
- **Optical & Inventory** (7 tables, 50 fields): Contact lens logs/orders/RX notes, frame page data/logs, inventory logs, spectacle RX notes.
- **Prescriptions** (3 tables, 40 fields): MedComp RX (prescriptions), MedComp (medication collections with XML serialization), MedComp Log.
- **Scheduling** (3 tables, 41 fields): Appointments (26 fields), waitlist, appointment log.
- **Referrals** (1 table, 19 fields): Professional referrals with detailed fields.
- **Interoperability** (1 table, 18 fields): HL7 message records.

**Thinnest coverage:**
- Some link/bridge tables have very few fields (e.g., `inv_trans_items` with 3 fields, `pat_photos` with 2 fields, binary data tables with 2 fields each), but these are structurally appropriate — they're FK pairs or blob containers.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patients` (51 fields) — name, DOB, SSN, address, phone, sex, family_id, location, death indicator, communication preferences | Thorough |
| Encounters / visits | ⚠️ Partial | `appts` (26 fields) tracks appointments; `rslip` (10 fields) tracks routing slips from check-in to discharge; no explicit "encounter" entity | Appointments and routing slips serve as encounter proxies; clinical data linked via date/acctid rather than encounter ID |
| Problems / conditions / diagnoses | ✅ Covered | `ehr_file` Problem (22 fields), Problem - External (20 fields) | Includes both internal and external problem sources |
| Medications / prescriptions | ✅ Covered | `ehr_file` Medication Order (54 fields), Medication History (39 fields), Medication - External (42 fields), Formulary (20 fields); `mcrx` (13 fields), `mcs` (15 fields), `mcs_log` (12 fields) | Deep — multiple tables covering orders, history, external meds, formulary, and e-prescribing data |
| Allergies | ✅ Covered | `ehr_file` Drug Allergy (21 fields), Drug Allergy - External (21 fields), Drug Allergy History (17 fields), Drug Interaction (17 fields), Drug F9 (16 fields) | Unusually thorough — five sub-type sections covering allergies, history, interactions |
| Immunizations | ✅ Covered | `ehr_file` Immunization (43 fields) | Well-documented with extensive fields |
| Vitals | ⚠️ Partial | `ehr_file` Observation (27 fields) likely includes vitals; Eye Care Data (31 fields) covers visual acuity and refraction | No explicit "vitals" entity; vitals likely stored as observations |
| Lab results | ✅ Covered | `ehr_file` Lab Order (47 fields), Lab Result (36 fields), Lab Result CCR (59 fields) | Three distinct sub-types; CCR variant has the most fields |
| Imaging / diagnostic reports | ✅ Covered | `med_image_info` (10 fields), `med_image_data` (binary), `ehr_file` Diagnostic Study (15 fields) | Includes both metadata and binary image data |
| Procedures | ✅ Covered | `ehr_file` Procedure (18 fields) | Present |
| Clinical notes / documents | ✅ Covered | `clinical_note` (10 fields), `pat_file` (14 fields), `pat_file_data` (binary) | Clinical notes table plus general patient file storage |
| Care plans / goals | ❌ Not covered | No care plan or goal entities | Product is an eye care PM; care plans may not be a core workflow. Minor gap. |
| Orders / referrals | ✅ Covered | `order_groups` (32 fields), `result_groups` (29 fields), `pro_refrl` (19 fields) | Order/result groups plus professional referrals |
| Insurance / coverage | ✅ Covered | `patients` includes insurance balance fields; `pat_ins_card` (4 fields), `ins_card_info` (11 fields), `ins_card_data` (binary); VSP eligibility tables (3 tables, 34 fields) | Insurance card images, eligibility data, and patient-level insurance info |
| Claims / billing | ✅ Covered | `invoice` (12 fields), `inv_trans_items` (3 fields), `trans_data` (9 fields), `hcfa_print` (8 fields), `hcfa_data` (5 fields), `rslip` (10 fields); VSP claims (3 tables, 110 fields) | Strong coverage of both medical (HCFA) and vision (VSP) claims |
| Payments | ✅ Covered | `trans_pay` (10 fields) | Payment records present |
| Consents / directives | ⚠️ Partial | `hippadisc` (7 fields) — HIPAA disclosure log | HIPAA disclosures tracked; no explicit advance directives or consent forms entity |
| Patient communications / portal messages | ✅ Covered | `kno2_message` (35 fields), `directmail_message` (29 fields), `comments` (6 fields), `reminders` (14 fields), `rem_log` (8 fields) | Multiple communication channels covered |
| Specialty-specific (Optometry/Ophthalmology) | ✅ Covered | `ehr_file` Eye Care Data (31 fields) with documented VisualAcuityFieldDataModel and RefractionMeasurementFieldDataModel serialized types; `sprx_notes` (3 fields), `clrx_notes` (3 fields); optical inventory tables | **Standout feature.** Serialized object models for visual acuity and refraction measurements documented to individual enum values. Spectacle and contact lens RX notes. Frame and CL inventory. |

**Summary**: 14 of 18 standard domains are fully covered, 3 are partially covered, and 1 (care plans/goals) is not covered but is arguably N/A for an eye care PM. No significant EHI gaps identified.

## 6. Documentation Quality

**Strengths:**
- **Completeness**: Every field in every exported table has a name, MySQL data type, and prose description. 100% of 1,368 fields are described.
- **Structure**: Consistent four-column format (Column Name, Data Type, Description, Extraction Method) throughout the 921-page document. Easy to parse programmatically.
- **Serialized data models**: The documentation of .NET serialized types for eye care data (VisualAcuityFieldDataModel, RefractionMeasurementFieldDataModel) is genuinely unusual and valuable. Many vendors would export opaque blobs; Crystal PM documents the full object hierarchy including enum values (e.g., TargetSiteType: Right, Left, Both; MeasurementType: Sphere, Cylinder, Axis, Add, HorizontalPrism, etc.).
- **Extraction method documentation**: Each field specifies whether it's extracted as plain CSV or requires binary/XML deserialization, which is critical for consumers to know.

**Weaknesses:**
- **No value sets for coded integer fields**: Many integer columns (e.g., `type` in `ehr_file`, `recall_type` in `patients`) are described as "represents a category" without enumerating the valid values and their meanings. A consumer would need to discover these from the data itself.
- **No entity relationship diagram (ERD)**: Relationships are implied through column descriptions (e.g., "acctid is a unique identifier for a patient in the 'patients' table") but there is no formal FK documentation or visual diagram.
- **No sample data**: No example CSV files, no sample records, no screenshots of the export output.
- **No export instructions**: The document is purely a data dictionary. There are no UI screenshots, step-by-step instructions, or API documentation for how to trigger the export.
- **No machine-readable schema**: The data dictionary is only available as a PDF. No JSON Schema, SQL DDL, or other machine-readable format is provided.

**Developer usability**: A competent developer could build an import system from this documentation. The field descriptions are sufficient to understand most data semantics. The main difficulty would be reverse-engineering coded value meanings for integer type fields and understanding the exact relationships between tables without an ERD. The serialized type documentation for eye care data is particularly useful and would save significant reverse-engineering effort.

## 7. Overall Assessment

### Classification

**Comprehensive native export.** Crystal PM exports its native MySQL database model as CSV files — 58 tables, 1,368 fields, covering clinical, billing, insurance, optical, scheduling, documents/images, communications, and specialty eye care data. This is not a C-CDA wrapper or FHIR projection; it is a genuine database dump with field-level documentation.

### Key Findings

1. **Genuinely comprehensive database export**: 58 distinct tables and 1,368 documented fields covering virtually all data domains the product stores. The export format (one CSV per table, native schema) is exactly the right approach for (b)(10). This is one of the more thorough implementations among small vendors.

2. **Outstanding specialty data documentation**: The serialized .NET object models for visual acuity and refraction measurements are documented down to individual enum values (TargetSiteType, MeasurementType, StatusType, etc.). This eye care-specific data is precisely what generic C-CDA/FHIR exports miss.

3. **Deep VSP vision insurance coverage**: 10 tables and 201 fields dedicated to VSP claims, authorizations, eligibility, and services — reflecting the product's core market in eye care. This billing depth is unusual and appropriate.

4. **100% field-level descriptions**: Every one of 1,368 fields has a prose description and data type. While coded value enumerations are missing, the field descriptions are substantive and useful.

5. **Documentation gaps are real but manageable**: No sample data, no ERD, no value sets for coded fields, no export trigger instructions. These weaknesses are notable but do not undermine the overall quality of the data dictionary. A prior report claimed 55 tables; actual count is 58.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV (one file per table, with binary deserialization for serialized columns)
Model type:      Native database
Entities:        58 distinct tables (80 documented sections including ehr_file sub-types)
Fields:          1,368
Descriptions:    100% of fields have descriptions
Sample data:     No
Bulk export:     Yes (all patient data)
Domains covered: 14 of 18 standard domains fully covered; 3 partial; 1 N/A
```

### Bottom Line

Crystal PM delivers a genuinely comprehensive EHI export — a full native database dump of 58 tables and 1,368 fields with 100% field-level documentation, covering clinical, billing, insurance, optical, and specialty eye care data. For a company of 12–35 employees, the 921-page data dictionary is an outsized effort that exceeds what many larger vendors provide. The main gaps are the absence of value set enumerations for coded fields and no sample data, but these are documentation polish issues rather than coverage failures.

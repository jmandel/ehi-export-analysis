# EHI Export Analysis: eMedPractice LLC

**Product**: eMedicalPractice  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.02.05.2898.EMED.01.01.1.220112 (CHPL ID 10787)

## 1. Product Context

eMedicalPractice is a comprehensive cloud-based ambulatory EHR and practice management platform from eMedPractice LLC (Delray Beach, FL), certified under the 2015 Edition Cures Update. It is marketed as an all-in-one solution covering:

- **Clinical EHR**: Charting, encounter documentation, customizable templates, problem lists, medication lists, allergy lists, vital signs, immunizations, clinical decision support, AI ambient documentation (ScribeSync)
- **E-Prescribing**: EPCS-capable prescribing, drug interaction checking, refill management
- **Lab Integration**: Bidirectional lab orders and results
- **Practice Management**: Scheduling, registration, eligibility verification, prior authorizations
- **Billing & RCM**: Integrated medical billing, claims creation/scrubbing/submission, clearinghouse, EOB auto-posting, patient statements, e-payments, financial dashboards
- **Patient Portal**: Appointment booking, health info viewing, prescription refills, document submission, bill viewing, payments
- **Telemedicine**: Integrated telehealth
- **Communications**: Direct messaging (HISP), fax management, email
- **Quality Reporting**: MIPS registry, CQMs, public health reporting (immunization, syndromic surveillance, cancer)

The product targets 9+ specialties (dermatology, cardiology, pediatrics, behavioral health, allergy/immunology, gastroenterology, chiropractic, ophthalmology, neurology).

**Baseline for export assessment**: A genuine (b)(10) export from this product should cover clinical data, billing/claims/payments, prescribing details, lab orders and results, insurance, scheduling, communications, documents, and specialty-specific clinical data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.html` (361 KB) | Main EHI export documentation page (WordPress/Elementor). Describes C-CDA + CSV dual export. Contains commented-out Section 4 (documents). | **High** — primary documentation |
| `downloads/ehi-export-page-api.json` (14 KB) | WordPress JSON API version of the export page. Cleaner content, same information. Page created 2023-09-19, modified 2025-12-05. | **High** — verified content matches HTML |
| `downloads/ehi-data-dictionary-tables.html` (398 KB) | Data dictionary page with 3 table schemas (Patients, Insurance, Appointments). | **High** — only field-level documentation |
| `downloads/ehi-data-dictionary-tables-api.json` (56 KB) | WordPress JSON API version of data dictionary. Page created 2025-12-05, modified 2025-12-06. | **High** — used for programmatic parsing |
| `downloads/screenshot-ehi-export-page.png` (1.1 MB) | Full-page screenshot of export documentation | Low — confirms rendered layout |
| `downloads/screenshot-ehi-data-dictionary.png` (1.3 MB) | Full-page screenshot of data dictionary tables | Low — confirms rendered layout |
| `downloads/enrichment/data-dictionary.json` (9 KB) | Pre-extracted data dictionary (3 tables, 61 columns) | Medium — verified against my own parse |

**No sample data, no downloadable files (PDF, ZIP, CSV), and no machine-readable schemas** were found on either page.

## 3. Export Mechanics

- **Format**: Dual-format: (1) C-CDA XML documents for clinical data, (2) CSV files for patient demographics, insurance, and appointments
- **Mechanism**: The documentation mentions that CSV exports are available via the application's "Reports" section. The C-CDA documents are organized in directory structures by patient chart number. No API endpoint for export is described. Export appears to be vendor-assisted or initiated through the application UI.
- **Single-patient vs bulk**: The C-CDA component organizes by individual patient chart number. Bulk export capability is not explicitly described.
- **Access constraints**: No mention of fees. Documentation notes exports use "robust encryption standards and secure transmission methods."
- **Documents**: A Section 4 describing export of scanned documents (PDFs, JPGs, PNGs) exists in the HTML source but is **commented out** (`<!-- -->`), suggesting this capability was either removed or is not currently active. The visible page numbering jumps from Section 2 directly to Notes, skipping both Sections 3 and 4.

## 4. Export Content: What's In It

The export has two documented components:

### Component 1: Clinical Data in C-CDA Format

The documentation states:
- Each patient encounter is represented as a CDA document
- A consolidated CDA file aggregates all encounters per patient
- Files organized by chart number in a directory structure
- Claims to include "all data elements defined in USCDI v3, in addition to other EHI the system stores"
- References the C-CDA specification at hl7.org

**No data dictionary, field mapping, template list, or sample C-CDA** is provided. The documentation does not specify which C-CDA templates, sections, or extensions are used. It does not describe what "other EHI" beyond USCDI is included. There is no way to verify the "all EHI" claim from the documentation alone.

### Component 2: Patient Details CSV

A CSV file containing demographics, insurance, and appointment data. The data dictionary page documents 3 tables with 61 total fields:

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| Patients Table Schema | 19 | 0 (names only) | Yes | Demographics |
| Insurance Table Schema | 29 | 0 (names only) | Yes | Insurance |
| Appointments Table Schema | 13 | 0 (names only) | Yes | Appointments |
| **Total** | **61** | **0** | **61** | — |

**Field-level detail**: Column names and SQL data types (int, varchar, date, float) are provided, along with nullability constraints. **Zero fields have descriptions** — only column names are given. No value sets are documented for coded fields (e.g., `Gender`, `Race`, `Ethnicity`, `MaritalStatus`, `status`, `AppointmentType`, `AppointmentStatus`). Several integer columns (`FacilityName`, `SchedulerName`, `AppointmentType`, `AppointmentStatus`) appear to be foreign keys or coded values with no reference tables. One data type has a typo: `InsuredDOB` is typed as "datet" (presumably "date").

**No relationships** are formally documented, though `ChartNo` appears in all three tables as an implicit join key. No foreign key constraints, cardinality, or entity-relationship diagrams are provided.

### Component 3: Documents (Commented Out)

The HTML source contains a commented-out Section 4 describing export of scanned documents (signed progress notes, lab results, radiology reports, other uploaded documents), organized by patient chart number with category subfolders. This section is not visible to users viewing the page.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes two active export components:

1. **C-CDA clinical data**: Described in broad terms with a claim of USCDI v3 completeness "plus other EHI." No specifics beyond the claim. C-CDA is inherently limited to clinical document data — it cannot represent billing, claims, financial transactions, scheduling details, or many operational data types.

2. **Patient Details CSV**: Covers exactly 3 narrow domains — demographics (19 fields), insurance (29 fields, covering primary and secondary insurance), and appointments (13 fields). The insurance table is the deepest, capturing subscriber details, policy numbers, group numbers, copays, and addresses for both primary and secondary insurance. The appointments table is thin (13 fields including redundant patient name/DOB/contact fields).

The CSV component is genuinely small: 61 fields across 3 tables, with no descriptions for any field. For a comprehensive ambulatory EHR with integrated billing, this is strikingly thin.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CSV: `Patients Table Schema` (19 fields — name, gender, DOB, address, phone, fax, email, status, race, ethnicity, marital status, referring physician). C-CDA presumably has demographics. | Basic demographics covered. No emergency contacts, preferred language, sexual orientation, gender identity (USCDI v3 requirements for the latter two are unclear from CSV fields alone; may be in C-CDA). |
| Encounters / visits | ⚠️ Partial | C-CDA claims encounter data. CSV `Appointments` table (13 fields). | Appointment scheduling is covered in CSV; clinical encounter content depends entirely on unverified C-CDA claim. |
| Problems / conditions | ⚠️ Partial | C-CDA claim only. No field-level documentation. | Product stores problem lists; coverage depends on C-CDA content which is unverified. |
| Medications / prescriptions | ⚠️ Partial | C-CDA claim only. | Product has EPCS e-prescribing. C-CDA would cover basic medication lists but not prescribing workflows, pharmacy communications, refill histories, or EPCS audit data. |
| Allergies | ⚠️ Partial | C-CDA claim only. | Standard USCDI domain; likely in C-CDA but unverified. |
| Immunizations | ⚠️ Partial | C-CDA claim only. | Product has immunization tracking and registry reporting; likely in C-CDA but unverified. |
| Vitals | ⚠️ Partial | C-CDA claim only. | Standard USCDI domain; likely in C-CDA but unverified. |
| Lab results | ⚠️ Partial | C-CDA claim only. | Product has bidirectional lab integration. C-CDA would carry results; lab orders and workflow data likely not captured. |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA claim only. Commented-out Section 4 mentions radiology reports as documents. | Unclear whether imaging data is in C-CDA or was only in the now-hidden document export. |
| Procedures | ⚠️ Partial | C-CDA claim only. | Standard USCDI domain; likely in C-CDA but unverified. |
| Clinical notes / documents | ⚠️ Partial | C-CDA claim. Commented-out Section 4 described signed progress notes and scanned documents, but this section is hidden. | Significant uncertainty. If Section 4 was removed, scanned documents and non-C-CDA formatted notes may not be exported. |
| Care plans / goals | ⚠️ Partial | C-CDA claim only. | May be in C-CDA if the product stores them. |
| Orders / referrals | ❌ Not covered | No mention in any documented export component. | Product supports lab orders and referrals. Not documented in export. |
| Insurance / coverage | ✅ Covered | CSV: `Insurance Table Schema` (29 fields) — primary and secondary insurance with subscriber details, policy/group numbers, copays, addresses. | Reasonably thorough for basic insurance coverage data. Missing eligibility verification records, prior authorization data. |
| Claims / billing | ❌ Not covered | No billing entities in any export component. | **Major gap.** Product has integrated billing, RCM, claims creation/submission, clearinghouse, EOB auto-posting, patient statements, e-payments. None of this is in the export. |
| Payments | ❌ Not covered | No payment entities in any export component. | **Major gap.** Product has payment processing, copay tracking, outstanding balance management. |
| Consents / directives | ❌ Not covered | No mention. | Product likely stores consent forms; not in export. |
| Patient communications / portal messages | ❌ Not covered | No mention. | Product has patient portal with messaging, document submission, appointment requests, refill requests. None exported. |
| Specialty-specific data | ❌ Not covered | No mention. | Product markets to 9+ specialties with customizable templates. No specialty-specific clinical data documented in export. |

## 6. Documentation Quality

**Overall**: Poor. The documentation is clean HTML but substantively thin.

- **For the C-CDA component**: No data dictionary, no template list, no field mapping, no sample files. The vendor makes a broad claim ("all data elements defined in USCDI v3, in addition to other EHI") but provides zero evidence. A developer cannot determine what C-CDA sections or templates are used, what extensions exist, or what "other EHI" means in practice.

- **For the CSV component**: A data dictionary exists but is minimal — column names and SQL types only. Zero descriptions for 61 fields. No value sets for coded fields. No relationship documentation. No sample data. A developer could guess at the structure but would need to reverse-engineer coded values (e.g., what integer values does `AppointmentType` use?).

- **Machine-readable artifacts**: None. No JSON schemas, no sample exports, no downloadable files of any kind.

- **Export instructions**: Minimal. One sentence mentions CSV exports are in the "Reports" section. No step-by-step guide, no screenshots, no API documentation.

- **Could a developer build an import?** Not reliably. The C-CDA portion would require following the C-CDA standard and hoping the vendor's output conforms. The CSV portion has enough structure to parse but not enough semantics to interpret coded values.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documented CSV export covers only 3 entities (demographics, insurance, appointments) with 61 fields total — a tiny fraction of what a comprehensive ambulatory EHR stores. The C-CDA component makes a broad "all EHI" claim but provides no evidence to verify it, and C-CDA is inherently limited in what data types it can represent (it cannot carry billing, claims, payments, scheduling details, portal messages, or specialty-specific structured data). Even accepting the C-CDA claim at face value, the export would still miss billing/RCM data (a core product capability), patient portal data, communications, and specialty clinical data. The commented-out document export section (Section 4) further undermines confidence — it appears document export capability may have been removed.

**Axis 2 — Export approach: Repackaged existing export**

The C-CDA component is the vendor's existing clinical document exchange (the same format used for transitions of care under (b)(1)-(b)(3)) relabeled as "(b)(10)." The telltale signs:
- References the generic HL7 C-CDA specification with no product-specific mapping
- Claims USCDI v3 completeness, which is the clinical exchange floor
- No evidence of billing, specialty, or operational data beyond what C-CDA naturally carries
- The CSV component adds 3 administrative tables but nothing approaching a purpose-built EHI export

The CSV addition (demographics, insurance, appointments) shows a minimal effort to go beyond pure C-CDA, but 3 tables with 61 undescribed fields is not a purpose-built EHI export — it is a supplement to cover the most obvious gap (demographics/insurance aren't well-represented in C-CDA). A purpose-built export from this product would need to cover billing/claims tables, prescribing workflows, lab orders, document metadata, portal interactions, and specialty clinical data.

### Key Findings

1. **Billing data is entirely absent** from the export despite the product having integrated billing, RCM, claims, clearinghouse, EOB posting, patient statements, and payment processing. This is the single largest gap — billing records are squarely within the designated record set.

2. **The data dictionary is extremely thin**: 3 tables, 61 fields, 0 descriptions. For a comprehensive ambulatory EHR, this represents a trivial fraction of the data model. The CSV component covers only demographics, insurance, and appointments.

3. **The C-CDA "all EHI" claim is unsubstantiated**: The vendor claims the C-CDA export includes "all data elements defined in USCDI v3, in addition to other EHI" but provides no template list, field mapping, sample data, or any evidence to verify this claim. C-CDA is structurally incapable of representing billing, scheduling, portal messages, and many other data types.

4. **Section 4 (Documents) is commented out**: The HTML source reveals a previously visible section about exporting scanned documents (progress notes, lab results, radiology reports). This section is now hidden, raising questions about whether document export functionality was removed.

5. **No sample data or machine-readable schemas exist**: There are no downloadable artifacts — no sample C-CDA files, no sample CSVs, no JSON schemas. All documentation is inline HTML on two WordPress pages.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA (XML) + CSV
Entities:        3 (in CSV data dictionary; C-CDA content unspecified)
Fields:          61 (CSV only)
Descriptions:    0% (0 of 61 fields have descriptions)
Sample data:     No
Bulk export:     Unclear
Domains covered: 2 of 15 applicable domains with any confidence (Insurance, Demographics via CSV); remainder dependent on unverified C-CDA claims
```

### Bottom Line

A patient or provider would receive a C-CDA clinical summary (standard content, unverified scope) plus a bare-bones CSV with demographics, insurance, and appointments — but no billing records, no payment history, no detailed prescribing data, no portal communications, no scanned documents (section commented out), and no specialty clinical data. The biggest gap is the complete absence of billing/RCM data from a product whose core value proposition includes integrated billing and revenue cycle management.

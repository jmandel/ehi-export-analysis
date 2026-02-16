# EHI Export Analysis: Nextech

**Product**: SRS EHR (SRSPro) and Nextech EHR (IntelleChartPRO/ICP)
**Analysis date**: 2026-02-16
**CHPL IDs**: 11040 (SRS EHR, v12, certified 2022-12-02), 11724 (Nextech EHR ICP, v9, certified 2025-12-02)

## 1. Product Context

Nextech develops specialty-focused EHR and practice management software for ambulatory specialty practices. Two distinct CHPL-certified platforms share a single EHI documentation page:

**SRS EHR (SRSPro)** — Originally developed by SRS Health (acquired by Nextech in 2019), this platform historically dominated the orthopedic EHR market with 5,000+ providers. It also serves ophthalmologists, cardiologists, and other surgical specialists. SRSPro includes EHR with specialty templates, practice management with scheduling, billing/claims, CPOE for medications/labs/imaging, e-prescribing, PACS integration, CDS, immunization/syndromic reporting, and direct secure messaging. It is certified for (b)(10), (a)(1)–(a)(5), (a)(9), (a)(12), (a)(14), (b)(1)–(b)(2), (c)(1)–(c)(3), (e)(3), (f)(1), (f)(5), (g)(2)–(g)(7), (h)(1). Notably, it lacks (e)(1) patient portal and (g)(9)–(g)(10) standardized FHIR API.

**Nextech EHR (IntelleChartPRO/ICP)** — Nextech's cloud-based EHR platform serves dermatology, ophthalmology, plastic surgery, orthopedics, and med spa practices. Features include customizable specialty templates, iPad/mobile apps, integrated e-prescribing, lab management, photo/image management with IntelleDraw, scheduling, billing with claims management and Nextech Payments, patient portal, telehealth, cosmetic business tools (quotes, packages, gift cards), CRM/lead management, and AI-powered Cora Scribe ambient documentation. Won Best in KLAS for Ambulatory Specialty EHR (2024, 2025).

A third platform, **Nextech Select/NexCloud**, is also documented at the same URL but does not have its own CHPL listing in the provided metadata.

**Baseline for export completeness**: Both certified products store clinical data (encounters, problems, medications, labs, vitals, orders/results, immunizations, procedures, allergies), demographic data, insurance/billing data, specialty-specific clinical data (ophthalmology refractions, PACS imaging, glaucoma flowsheets), documents/images, communications, and custom/user-defined fields.

## 2. Artifacts Reviewed

| Artifact | Description | Size/Scope | Informativeness |
|---|---|---|---|
| `srspro-ehi-export-documentation.pdf` | SRSPro EHI export guide — ZIP structure, CSV/XML file descriptions, data handling rules, inter-entity relationships | 8 pages, 451 KB | **High** — detailed folder structure, relationship documentation, handling of edge cases |
| `srspro-ehi-data-dictionary.xlsx` | SRSPro field-level data dictionary | 19 sheets, 868 fields across 19 entities | **High** — complete field inventory with descriptions, including XML schema documentation |
| `nextech-ehr-icp-ehi-export-documentation.pdf` | ICP EHI export guide — ZIP structure, folder layout, JSON/PDF/XML file descriptions, audit logging | 6 pages, 335 KB | **High** — clear folder/file structure with specialty-specific exports |
| `nextech-ehr-icp-ehi-data-dictionary.xlsx` | ICP field-level data dictionary | 19 sheets, 341 fields across 19 entities | **Medium** — all fields described but no data types, fewer fields than SRSPro |
| `nextech-select-nexcloud-ehi-export-documentation.pdf` | Select/NexCloud export guide — ZIP structure, billing CSV exports, EMN PDFs | 8 pages, 729 KB | **High** — notable for including billing data (charges, payments, payment plans) |
| `nextech-select-nexcloud-ehi-data-dictionary.xlsx` | Select/NexCloud field-level data dictionary | 16 sheets, 730 fields across 16 entities | **High** — 100% descriptions, deepest billing documentation |
| `enrichment/data-dictionaries.json` | Prior agent's JSON parse of all three dictionaries | 290 KB | **Medium** — useful for cross-reference but undercounted SRSPro fields (427 vs 868) |
| `ehi-export-page-screenshot.png` | Screenshot of the EHI documentation landing page | 877 KB | **Low** — confirms page layout and download links |

## 3. Export Mechanics

### SRS EHR (SRSPro)

- **Format**: Per-patient ZIP file containing CSV files (15 types), XML files (encounter data, vitals, results), C-CDA XML, and a Documents folder with attached files. ZIP named as `FirstNameInitial_LastName_PersonID_DateTimeStamp.ZIP`.
- **Mechanism**: Single-patient export from within the application UI. Bulk export is initiated via support ticket to Nextech (vendor-assisted).
- **Access constraints**: Requires user permission within SRSPro. Audit logging records requesting user, patient, and timestamp. Bulk requests go through Salesforce ticket workflow.
- **Fees**: Not documented.

### Nextech EHR (ICP)

- **Format**: Per-patient ZIP file containing JSON files (structured clinical data), PDF files (chart notes, consents, letters), XML (C-CDA per encounter), image files (JPG + TXT metadata). ZIP named as `LastName_FirstName_MiddleInitial_MRN.zip`.
- **Mechanism**: Single-patient export from within the EHR. Bulk patient export also supported (with slightly different letter format). Audit logging for both single and bulk exports.
- **Access constraints**: User permission required. Single exports audited per-user; bulk exports tracked via Salesforce support tickets.

### Nextech Select/NexCloud

- **Format**: Per-patient ZIP with CSV files (16 types including billing), EMN PDFs (encounter notes), Documents folder, iPad Documents folder, and C-CDA XML.
- **Mechanism**: Not explicitly described; parallels the other platforms.

## 4. Export Content: What's In It

The three platforms collectively document **54 entities** and **1,939 fields**, with **99.6% of fields having descriptions**. No formal data types, cardinality specifications, or machine-readable schemas (JSON Schema, XSD) are provided for any platform. Value sets are partially documented (SRSPro includes a CodeSystemNames.csv mapping VocabularyIDs to OIDs; ICP occasionally notes enumerations in Notes columns). No sample export data files are provided.

### SRS EHR (SRSPro) — 19 entities, 868 fields

SRSPro's export combines CSV flat files for discrete clinical data with XML files for complex encounter-level and results data, plus C-CDA for standardized clinical summary.

**CSV exports (15 files)**:
- **Orders** (80 fields) — the most detailed CSV, covering CPOE orders with HL7 mapping, order status, ordering/performing providers, specimen data, and linked requisition IDs
- **Smoking Status** (58 fields) — unusually comprehensive, includes screening plans, cessation interventions, and post-screening tracking
- **Diagnoses** (35 fields) — full coding detail (ICD-10, SNOMED), status, onset dates, encounter-agnostic patient problem list
- **Implantable Devices** (35 fields) — UDI data, device status (active/inactive/deleted), manufacturer info
- **Insurance Information** (33 fields) — payer details, subscriber info, group numbers, authorization data
- **GuarantorInformation** (30 fields) — guarantor demographics, relationship to patient, contact details
- **Messages** (28 fields) — chart-attached messages including sticky notes and TOC messages, with DocumentID linkage
- **Injections** (26 fields) — injection records with administration details
- **Family History** (18 fields) + **Family History Codes** (12 fields) + **Family History Statuses** (4 fields) — three linked CSVs connected via ConceptPath
- **Medication** (13 fields) — documented as CCDA-sourced medication data
- **Custom Alerts** (4 fields) — practice-configurable alert criteria
- **Appointment List** (3 fields) — basic appointment export
- **UDFs** (3 fields) — user-defined fields from demographic data
- **CodeSystemNames** (4 fields) — reference table mapping VocabularyIDs to OIDs

**XML exports (3 types)**:
- **Encounter Data Capture** (363 fields across 30 XML sections) — per-encounter XML with procedures (21 fields), problems (16), social history (16), lab results (19), vital signs (12), plan of care with goals/procedures/health concerns (41), physical exams (10), chief complaints (5), clinical notes (16), HPI (19), review of systems (119), assessments (7), visual activities (13), gender identity/sexual orientation/sex (11), tribal affiliation (4), occupation (12), and more
- **Results** (95 fields) — lab/radiology/procedure results with header, grid data, and footer sections covering account numbers, performing labs, specimen data, and result values
- **Vitals** (24 fields) — full vitals data including fields not in C-CDA

**Relationship documentation** is a notable strength:
- Orders → Results linked via RequisitionId (RequisitionId = OrderID)
- Messages → Documents linked via DocumentID
- FamilyHistory → FamilyHistoryCodes linked via ConceptPath
- Orders → Documents linked via UnstructuredDocumentId

**Documents folder** contains all chart-attached documents (images, forms, CPOE results, TOC attachments). Deleted documents are excluded. Messages are explicitly separated from documents.

### Nextech EHR (ICP) — 19 entities, 341 fields

ICP's export uses JSON for structured data, PDFs for narrative clinical content, and C-CDA for standardized summary.

| Entity | Fields | Format | Category |
|---|---|---|---|
| Patient Demographics | 71 | JSON | Demographics |
| ChartNote | 49 | PDF | Clinical documentation |
| Tasking_Microservice | 47 | JSON/CSV | Workflow/tasks |
| Refractions | 31 | JSON | Ophthalmology specialty |
| Insurance & Auth | 22 | JSON | Insurance |
| Glaucoma Flowsheet | 20 | JSON | Ophthalmology specialty |
| Communications | 14 | PDF | Patient communications |
| Laboratory | 13 | JSON | Lab studies and results |
| Referrals | 13 | JSON | Referral management |
| Procedures | 11 | JSON | Procedures |
| Patient Tasks | 10 | — | Workflow/tasks |
| Specialty Medications | 10 | JSON | Medications |
| Appointments | 7 | JSON | Scheduling |
| Internal Communication | 6 | JSON | Internal messaging |
| Secure Messages | 5 | JSON | Portal messages |
| Retina Injection Log | 4 | JSON | Ophthalmology specialty |
| Documents | 3 | TXT metadata | Document metadata |
| Images | 3 | TXT metadata | Image metadata |
| Shared Care Comments | 2 | JSON | Care coordination |

**Specialty-specific exports** distinguish ICP: Glaucoma Flowsheet (20 fields), Refractions (31 fields), Retina Injection Log (4 fields), Shared Care Comments (incoming/outgoing), and Surgery Planner Comments. These reflect ophthalmology-focused workflows.

**Document/Image handling**: Files exported as JPG with accompanying TXT metadata files, organized by document type and date.

**C-CDA coverage**: 26 data classes including allergies, clinical notes, demographics, encounters, immunizations, implantable devices, insurance coverage, lab results, medications, problem list, procedures, social status, vitals, health concerns, goals, plan of care, reason for referral/visit, and specialty medications.

### Nextech Select/NexCloud — 16 entities, 730 fields

This platform's export is the only one with explicit billing data:

| Entity | Fields | Category |
|---|---|---|
| Patient Demographics | 212 | Demographics |
| Charges | 140 | Billing |
| Insurances | 85 | Insurance |
| Appointments | 52 | Scheduling |
| Payments | 50 | Billing |
| EMN | 43 | Encounter notes |
| Recalls | 27 | Patient recalls |
| Notes | 23 | Clinical notes |
| Recalls Steps | 17 | Recall management |
| Follow up | 16 | Follow-up tasks |
| iPad Tasks | 15 | iPad workflow |
| Payment Plans | 13 | Billing |
| DSI feedback | 11 | Decision support |
| PracYakker | 10 | Internal messaging |
| iPad Notes | 9 | iPad notes |
| Custom | 7 | Custom fields |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**SRSPro** organizes its export around clinical discrete data (CSV + XML) plus C-CDA and documents. The strongest areas are:
- **Orders** (80 fields) — genuinely detailed CPOE export with HL7 mapping
- **Encounter Data Capture** (363 fields across 30 XML sections) — comprehensive per-encounter clinical capture covering procedures, problems, vitals, labs, physical exams, review of systems (119 fields alone), assessments, HPI, chief complaints, clinical notes, social determinants, care plans, and specialty visual activities
- **Smoking Status** (58 fields) — unusually thorough with screening plans
- **Diagnoses/Implantable Devices** (35 fields each) — full coding and status detail
- **Insurance/Guarantor** (63 fields combined) — thorough insurance coverage

The thinnest areas are Appointments (3 fields — just basic info), UDFs (3 fields), and Custom Alerts (4 fields).

**ICP** organizes around data folders (Appointments, Encounters, Demographics, etc.) with specialty subfolders. The ophthalmology-specific data (Refractions 31 fields, Glaucoma Flowsheet 20 fields) is a genuine strength. Demographics (71 fields) and Tasking (47 fields) are deep. But the overall field count (341) is notably lower than SRSPro's 868.

**Select/NexCloud** is the only platform exporting billing: Charges (140 fields), Payments (50 fields), and Payment Plans (13 fields) — 203 billing fields total. Patient Demographics is exceptionally detailed at 212 fields.

### 5b. Standardized domain coverage (top-down)

**SRS EHR (SRSPro)** — the primary certified product:

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | C-CDA demographics; Insurance Information CSV (33 fields); GuarantorInformation CSV (30 fields) | Demographics in C-CDA only (no separate CSV for non-insurance demographics), but PDF docs note this is intentional as C-CDA covers full demographics |
| Encounters / visits | ✅ Covered | Encounter Data Capture XML (363 fields across 30 sections per encounter); Appointment List CSV (3 fields) | Thorough — per-encounter XML captures comprehensive clinical content |
| Problems / conditions / diagnoses | ✅ Covered | Diagnoses CSV (35 fields) with ICD-10/SNOMED coding; also in Encounter XML and C-CDA | Deep — encounter-agnostic problem list plus encounter-level diagnoses |
| Medications / prescriptions | ⚠️ Partial | Medication entity (13 fields, CCDA-sourced); Injections CSV (26 fields) | Medications come from C-CDA with limited field depth (13 fields). No dedicated e-prescribing data (pharmacy selections, fill history, prior authorizations) |
| Allergies | ✅ Covered | C-CDA allergies section | Via C-CDA only; no separate structured export |
| Immunizations | ✅ Covered | C-CDA immunizations section | Via C-CDA only; no separate structured export |
| Vitals | ✅ Covered | Vitals XML (24 fields); also in C-CDA (subset) | Dedicated XML export goes beyond C-CDA |
| Lab results | ✅ Covered | Results XML (95 fields); linked to Orders CSV via RequisitionId | Thorough — full lab result detail with header/grid/footer |
| Imaging / diagnostic reports | ⚠️ Partial | Documents folder includes imaging results as attached files; no structured imaging data | Product has PACS integration; no structured PACS/DICOM metadata export |
| Procedures | ✅ Covered | Encounter Data Capture XML procedures section (21 fields); C-CDA procedures | Covered in encounter XML |
| Clinical notes / documents | ✅ Covered | Documents folder (all chart-attached documents); Encounter Data Capture XML (clinical notes, HPI, ROS sections); C-CDA clinical notes | Comprehensive — both structured note data and original document files |
| Care plans / goals | ✅ Covered | Encounter Data Capture XML Plan of Care section (goals, procedures, health concerns — 41 fields); C-CDA plan of treatment | Thorough |
| Orders / referrals | ✅ Covered | Orders CSV (80 fields) with detailed CPOE data | Strong — one of the most detailed entities |
| Insurance / coverage | ✅ Covered | Insurance Information CSV (33 fields); GuarantorInformation CSV (30 fields); C-CDA insurance section | Thorough — 63 fields across two dedicated CSVs |
| Claims / billing | ❌ Not covered | No billing/charges/payments entities in SRSPro export | Product has integrated PM with billing — **significant gap** |
| Payments | ❌ Not covered | No payment data in export | Product handles payments — **significant gap** |
| Consents / directives | ⚠️ Partial | Not explicitly in CSV/XML exports; may be in Documents folder as attached files | No structured consent data |
| Patient communications / portal messages | ✅ Covered | Messages CSV (28 fields) covering chart messages, sticky notes, TOC messages | Good coverage; messages explicitly separated from documents |
| Specialty-specific (orthopedics) | ⚠️ Partial | Encounter Data Capture XML includes procedures, physical exams, visual activities; UDFs for custom fields | No dedicated orthopedic-specific entities despite product's orthopedic heritage |

**SRSPro coverage**: ✅ 12 domains covered, ⚠️ 4 partial, ❌ 2 not covered (of 18 applicable)

**Nextech EHR (ICP)**:

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient Demographics JSON (71 fields) | Thorough |
| Encounters / visits | ✅ Covered | ChartNote PDF (49 fields documented); C-CDA per encounter | Encounter content as customizable PDFs — preserves layout but less computable |
| Problems / conditions / diagnoses | ✅ Covered | C-CDA problem list | Via C-CDA only |
| Medications / prescriptions | ✅ Covered | Specialty Medications JSON (10 fields); C-CDA medications | Specialty medications as dedicated JSON; general meds via C-CDA |
| Allergies | ✅ Covered | C-CDA allergies | Via C-CDA only |
| Immunizations | ✅ Covered | C-CDA immunizations | Via C-CDA only |
| Vitals | ✅ Covered | C-CDA vitals | Via C-CDA only |
| Lab results | ✅ Covered | Laboratory JSON (13 fields) with study/test/result hierarchy | Dedicated structured export |
| Imaging / diagnostic reports | ⚠️ Partial | Documents/Images folders with metadata; no structured imaging data | Images exported as JPG + metadata |
| Procedures | ✅ Covered | Procedures JSON (11 fields); C-CDA procedures | Dedicated structured export |
| Clinical notes / documents | ✅ Covered | ChartNote PDF; Documents folder; Images folder; Letters; Consents | Multiple document types captured |
| Care plans / goals | ✅ Covered | C-CDA plan of care, health concerns, goals | Via C-CDA |
| Orders / referrals | ✅ Covered | Referrals JSON (13 fields); Laboratory JSON (studies/results) | Referrals well-documented; labs cover ordered studies |
| Insurance / coverage | ✅ Covered | Insurance & Auth JSON (22 fields); C-CDA insurance coverage | Dedicated JSON + C-CDA |
| Claims / billing | ❌ Not covered | No billing/charges/payments entities | Product has integrated billing (EM coding, claims, POS, Nextech Payments) — **significant gap** |
| Payments | ❌ Not covered | No payment data | **Significant gap** |
| Consents / directives | ✅ Covered | Consents folder with signed consent PDFs | Exported as signed PDF documents |
| Patient communications / portal messages | ✅ Covered | Communications PDF (14 fields), Internal Communication JSON (6 fields), Secure Messages JSON (5 fields) | Three separate communication channels captured |
| Specialty-specific (ophthalmology) | ✅ Covered | Glaucoma Flowsheet (20 fields), Refractions (31 fields), Retina Injection Log (4 fields), Shared Care Comments (2 entities), Surgery Planner Comments | **Strong** — genuine specialty data exported |

**ICP coverage**: ✅ 15 domains covered, ⚠️ 1 partial, ❌ 2 not covered (of 18 applicable)

## 6. Documentation Quality

**Strengths:**
- Every field across all three platforms has a name, and 99.6% have descriptions (1,932 of 1,939 fields)
- SRSPro's relationship documentation is excellent — explicit cross-entity linking instructions (Orders↔Results via RequisitionId, Messages↔Documents via DocumentID, FamilyHistory↔FamilyHistoryCodes via ConceptPath, Orders↔Documents via UnstructuredDocumentId)
- Each platform has both a structural guide (PDF) and a field-level dictionary (XLSX) — well-organized
- Edge case handling is documented: empty data behavior (empty CSVs created, empty XML files or no file), deleted record handling (included with status flags), "No Known Diagnoses" special case
- The documentation explicitly notes where data overlaps between CSV/XML and C-CDA (vitals, diagnoses, smoking status appear in both with the structured export having more fields)

**Weaknesses:**
- **No formal data types**: No column for data type (string, integer, date, boolean) in any dictionary. Types must be inferred from descriptions (e.g., "Date when the ROS is created in format ex. 8/22/2022 3:51:52 PM")
- **No machine-readable schemas**: No JSON Schema, XSD, OpenAPI, or similar. Only human-readable XLSX and PDF
- **No sample data files**: No example exports to validate against the dictionary
- **No cardinality/nullability**: Required vs optional fields not specified
- **No version control**: Dictionaries have no version numbers or change history. PDF filenames include dates (10.30.25, 2025) but no formal versioning
- **Cross-platform inconsistency**: ICP uses JSON, SRSPro uses CSV/XML, Select uses CSV — different formats, field names, and entity structures for equivalent data. No unified data model

**Developer implementability**: A developer could build a basic import from these docs through trial and error. The folder structures are clear, field names are descriptive, and relationship documentation (especially SRSPro) is actionable. However, the lack of types, schemas, and sample data means significant guesswork around parsing, date formats, null handling, and encoded values.

## 7. Overall Assessment

### Classification

**Partial native export** — Both certified platforms export structured data from their native data models (not just FHIR/C-CDA repackaging), with genuine specialty-specific content and well-documented inter-entity relationships. However, the complete absence of billing/charges/payments data from both SRS EHR and Nextech EHR (ICP) exports represents a significant coverage gap, especially since both products have integrated billing capabilities. The sister platform (Select/NexCloud) demonstrates Nextech's ability to export billing data (Charges: 140 fields, Payments: 50 fields, Payment Plans: 13 fields), making the gap in the two certified products conspicuous.

### Key Findings

1. **Billing data absent from both certified products**: SRS EHR and Nextech EHR (ICP) both have integrated practice management with billing, but neither export includes charges, payments, or claims data. The Select/NexCloud platform (not separately CHPL-certified) exports 203 billing fields across 3 entities, proving Nextech can do this. This is the most significant compliance gap. *(Source: absence in `srspro-ehi-data-dictionary.xlsx` and `nextech-ehr-icp-ehi-data-dictionary.xlsx`; presence in `nextech-select-nexcloud-ehi-data-dictionary.xlsx`)*

2. **SRSPro Encounter Data Capture is exceptionally detailed**: At 363 fields across 30 XML sections per encounter, SRSPro captures comprehensive encounter-level clinical data including procedures, problems, vitals, labs, physical exams, review of systems (119 sub-fields), assessments, HPI, chief complaints, care plans, social determinants, and even visual activity data. This goes well beyond typical EHI exports. *(Source: `srspro-ehi-data-dictionary.xlsx`, Encounter Data Capture sheet)*

3. **ICP exports genuine ophthalmology specialty data**: Glaucoma Flowsheet (20 fields), Refractions (31 fields), Retina Injection Log, Shared Care Comments, and Surgery Planner Comments are specialty-specific entities not found in standard clinical summaries. This demonstrates export of data "beyond USCDI." *(Source: `nextech-ehr-icp-ehi-data-dictionary.xlsx`)*

4. **Strong relationship documentation in SRSPro**: Four explicit cross-entity relationships documented with field-level join keys. This is rare and essential for reconstructing a complete patient record from the export files. *(Source: `srspro-ehi-export-documentation.pdf`, pp. 5-7)*

5. **No data types or schemas across any platform**: Despite near-complete field descriptions (99.6%), no dictionary specifies data types, and no machine-readable schema exists. Developers must infer date formats, numeric types, and encoded values from description text. *(Source: all three XLSX data dictionaries)*

### Summary Stats

```
Classification:  Partial native export
Export format:   CSV + XML + C-CDA + PDF (SRSPro); JSON + PDF + C-CDA (ICP)
Model type:      Native database (hybrid with C-CDA for standardized clinical data)
Entities:        54 across 3 platforms (SRSPro: 19, ICP: 19, Select: 16)
Fields:          1,939 total (SRSPro: 868, ICP: 341, Select: 730)
Descriptions:    99.6% of fields have descriptions
Sample data:     No
Bulk export:     Yes (vendor-assisted for SRSPro and ICP; single-patient via UI)
Domains covered: 14 of 18 applicable domains (for SRSPro); 15 of 18 (for ICP)
```

### Bottom Line

Nextech's EHI export is a genuine effort that goes well beyond C-CDA/FHIR repackaging — both certified products export native structured data with specialty-specific content (ophthalmology data in ICP, comprehensive encounter XML in SRSPro) and near-complete field-level documentation across 1,939 fields. The single biggest gap is the absence of billing/charges/payments data from both SRS EHR and Nextech EHR (ICP) exports, despite both products having integrated billing capabilities — a gap Nextech demonstrably knows how to fill, since their Select/NexCloud platform exports 203 billing fields.

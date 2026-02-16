# EHI Export Analysis: AdvancedMD

**Product**: AdvancedMD (v25), AdvancedMD Mobile (v8)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2666.Adva.25.07.1.251215 (AdvancedMD), 15.04.04.2666.AdvM.08.03.1.251218 (Mobile)

## 1. Product Context

AdvancedMD is a cloud-based ambulatory EHR and practice management platform serving 65,000+ practitioners across 14,000+ practices. It is a comprehensive all-in-one system encompassing:

- **EHR**: Clinical charting with customizable templates, problem lists, medication lists, allergy lists, vitals, immunizations, lab orders/results, clinical notes, clinical decision support, order entry
- **E-Prescribing**: EPCS-certified electronic prescriptions including controlled substances
- **Practice Management**: Scheduling, patient demographics, registration, insurance eligibility verification
- **Medical Billing & RCM**: Charge capture, ClaimInspector claims scrubbing, electronic claims submission, ERA processing, denial management, patient billing, online payment processing, financial analytics
- **Patient Engagement**: Patient portal with messaging, telehealth, appointment reminders, self-scheduling
- **Document Management**: Scanning, faxing, e-signatures, chart file management
- **Specialty Support**: Mental/behavioral health, physical therapy, pediatrics (Bright Futures), and 20+ specialties

The product stores extensive clinical, billing/financial, scheduling, document, and patient communication data. A complete (b)(10) export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `advancedmd-ehrExport-dataDictionary.pdf` (13 pages, 826 KB) | EHR Bulk Data Export data dictionary documenting 12 SQL tables with column-level descriptions. The most detailed artifact. | **High** |
| `advancedmd-dataExport-dataDictionary.pdf` (6 pages, 453 KB) | C-CDA/HTML single-patient export implementation guide mapping USCDIv1 sections to EHR fields with vocabulary codes. | Medium |
| `advancedmd-bulkDataExport-scannedDocsImages.pdf` (9 pages, 2.1 MB) | Scanned documents/images export guidance with annotated screenshots of folder hierarchy and index files. | Medium |
| `advancedmd-flyer-dataExport.pdf` (2 pages, 36 KB) | Desk guide summarizing all 7 export mechanisms (4 single-patient, 3 bulk). | **High** (overview) |
| `data-export-page.html` (279 KB) | Full HTML of registered EHI documentation page with structured descriptions of all export options and field lists. | **High** |
| `screenshot-data-export-page.png` (866 KB) | Screenshot of documentation page. | Low (redundant with HTML) |

## 3. Export Mechanics

AdvancedMD provides **7 distinct export mechanisms** divided into single-patient and bulk categories:

### Single-Patient Exports (no developer assistance needed)
1. **Patient Transaction Report** — CSV from PM Report Center (35 fields: demographics + billing transactions)
2. **Patient Visit Summary Report** — CSV from PM Report Center (27 fields: visit/charge/appointment data)
3. **EHR Data Portability Export Tool** — C-CDA XML + HTML file via Tools > Data Portability Export Tool (USCDIv1 scope)
4. **EHR Patient Chart Print Tool** — PDF export of selectable chart sections (20 selectable categories)

### Bulk Patient Exports (developer assistance required)
5. **Practice Management Data Export** — Microsoft Access (.mdb) file via Utilities > Data Export (demographics, transactions, appointments)
6. **Scanned Documents & Images** — File system export with index files for PM and EHR documents
7. **EHR Bulk Data Export** — SQL Server backup (.bak) file with 12 EHR tables (313 fields)

**Access**: Single-patient exports are self-service through the UI. Bulk exports require contacting Client Support Services (developer assistance). No fees are mentioned.

**Format**: Mixed — CSV, C-CDA XML, PDF, Microsoft Access (.mdb), SQL Server backup (.bak), file system hierarchy.

## 4. Export Content: What's In It

### EHR Bulk Data Export (SQL .bak) — Primary data dictionary

The most documented export is the EHR Bulk Data Export, a SQL Server backup file containing 12 tables with 313 total fields. Column descriptions are provided for 267 of 313 fields (85%). Types are not documented (the columns are described as column names + descriptions only; SQL data types are not specified). No foreign key documentation exists beyond JOIN examples for lab results.

| Entity | Fields | Described | Category |
|---|---|---|---|
| EHR_Allergies | 14 | 14/14 | Clinical |
| EHR_Immunizations | 39 | 39/39 | Clinical |
| EHR_Messages | 23 | 12/23 | Communications |
| EHR_PatientNoteDiagnosis | 5 | 5/5 | Clinical |
| EHR_Problems | 18 | 12/18 | Clinical |
| EHR_Prescriptions | 78 | 68/78 | Medications |
| EHR_LabResults | 47 | 43/47 | Labs |
| EHR_ResultItems | 11 | 11/11 | Labs |
| EHR_ResultSets | 24 | 9/24 | Labs |
| EHR_ResultValues | 21 | 21/21 | Labs |
| EHR_PatientNotes | 30 | 30/30 | Clinical Notes |
| EHR_WordMerge | 3 | 3/3 | Templates |

**Notable**: EHR_Prescriptions is the richest table (78 fields), including Surescripts e-prescribing metadata, DEA class codes, formulary plan names, and discontinuation reasons. EHR_PatientNotes includes positional data (Left_Loc, Top_Loc) for reconstructing custom note templates. The EHR_WordMerge table provides template blob data for rendering notes.

### Single-Patient CSV Exports (PM)

The Patient Transaction Report and Patient Visit Summary provide billing/financial data at the single-patient level:
- Transaction types, charges, payments (patient & insurance), adjustments, write-offs
- Visit data with CPT codes, diagnosis codes, modifiers, place of service
- Insurance carrier info, copay, current balance

### Practice Management Bulk Export (Microsoft Access .mdb)

Described at a high level only: "demographics data, and the user might also choose to export transactions and appointment data. The exported file includes charges, payments, and write-offs, as well as patient demographics, provider, appointments, and carrier information." No field-level data dictionary is provided for this export.

### C-CDA Export (Single Patient)

Standard USCDIv1 C-CDA with 28 data sections including allergies, medications, problems, encounters, procedures, immunizations, vital signs, lab results, clinical notes (8 types), care team, assessments, goals, health concerns, plan of treatment, social history, medical equipment, and advance directives. This is a standard C-CDA implementation, not a custom export.

### Scanned Documents & Images

Both PM and EHR documents/images exported as files organized in date-based folder hierarchies with CSV index files mapping documents to patients. Retains native file format.

### Vendor's own content organization

The vendor organizes exports into two major systems — Practice Management (PM) and EHR — with the following categories:

**EHR Bulk Export (SQL .bak)**:
- Clinical: Allergies (14 fields), Immunizations (39 fields), Problems (18 fields), PatientNoteDiagnosis (5 fields)
- Medications: Prescriptions (78 fields)
- Labs: LabResults (47 fields), ResultItems (11 fields), ResultSets (24 fields), ResultValues (21 fields)
- Clinical Notes: PatientNotes (30 fields), WordMerge templates (3 fields)
- Communications: Messages (23 fields)

**PM Exports (CSV + Access)**:
- Demographics/Registration (header fields in CSV reports)
- Financial/Billing (transaction, charge, payment, adjustment fields)
- Appointments/Scheduling (visit data, appointment status/type)
- Insurance/Carrier information

**Documents**: Scanned documents and images (PM and EHR)

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor separates clinical data (EHR system) from administrative/financial data (PM system) and provides distinct export mechanisms for each.

**EHR side (strongest)**: The SQL .bak export covers core clinical domains deeply — prescriptions alone have 78 fields capturing drug details, e-prescribing workflow, formulary information, and discontinuation tracking. Lab results span 4 related tables (103 fields total) with detailed result values, sets, and items. Clinical notes use a custom template system captured with positional data for reconstruction. Allergies and immunizations are well-covered with full audit trails (CreatedBy/ChangedBy/CreatedAt/ChangedAt on most tables).

**PM side (thinner documentation)**: The PM Data Export (Access .mdb) is described only at a high level — demographics, transactions, appointments, charges, payments, write-offs, carriers — but no field-level data dictionary exists. The CSV single-patient reports provide field names (35 and 27 fields respectively) but no field descriptions.

**Major gap**: The PM side contains the billing and financial data that AdvancedMD is known for (claims scrubbing, ERA processing, denial management, A/R worklists, financial analytics), but this data has minimal documentation. The Access export presumably contains this data but without a data dictionary, there's no way to confirm what's actually included vs. excluded.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CSV header fields (patient, address, DOB, sex, SSN, phone, email); PM Access export includes "demographics data"; EHR tables contain PatientID but no demographics table | No dedicated demographics table in EHR export; PM Access export likely covers this but undocumented at field level |
| Encounters / visits | ⚠️ Partial | CSV exports include visit number, date of service, facility, appointment data; C-CDA includes Encounters section; no dedicated encounters table in EHR .bak | Product tracks encounters; export coverage depends on undocumented PM Access export |
| Problems / conditions | ✅ Covered | EHR_Problems (18 fields) + EHR_PatientNoteDiagnosis (5 fields) with diagnosis codes, status, onset dates | Solid coverage with ICD codes and status tracking |
| Medications / prescriptions | ✅ Covered | EHR_Prescriptions (78 fields) — very deep: drug details, e-prescribing, DEA class, formulary, Surescripts integration, discontinuation | Strongest table in the export |
| Allergies | ✅ Covered | EHR_Allergies (14 fields) with name, reaction, treatment, status, NKDA flag | Complete |
| Immunizations | ✅ Covered | EHR_Immunizations (39 fields) with CVX/MVX codes, lot, manufacturer, VFC eligibility, route, site | Very thorough |
| Vitals | ⚠️ Partial | C-CDA includes vital signs section with LOINC codes; no vitals table in EHR .bak export | Vitals only available via single-patient C-CDA, not in bulk SQL export |
| Lab results | ✅ Covered | 4 tables (EHR_LabResults, EHR_ResultItems, EHR_ResultSets, EHR_ResultValues) with 103 total fields, JOIN examples | Deep coverage with structured result values |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA includes Imaging Narrative section; no imaging table in EHR .bak | Only via C-CDA single-patient export |
| Procedures | ⚠️ Partial | C-CDA includes Procedures section from signed charge slips (CPT codes); CSV exports include charge/CPT codes; no procedures table in EHR .bak | No dedicated bulk procedures table |
| Clinical notes / documents | ✅ Covered | EHR_PatientNotes (30 fields) with custom template system + EHR_WordMerge (3 fields) for template rendering | Notes are complex (positional layout system) but fully exported |
| Care plans / goals | ⚠️ Partial | C-CDA includes Plan of Treatment, Goals, Health Concerns, Assessments sections | Only via single-patient C-CDA |
| Orders / referrals | ❌ Not covered | No orders or referrals table in any export. Lab orders are referenced (LabOrderID in EHR_LabResults) but order details are not in a separate table | Product supports order entry for labs, imaging, referrals — gap |
| Insurance / coverage | ⚠️ Partial | CSV header includes Insurance (Primary, Secondary, Tertiary); CSV body includes Carrier, Transaction Carrier; PM Access export includes "carrier information" | No detailed insurance/eligibility data in documented exports |
| Claims / billing | ⚠️ Partial | CSV exports include charges, payments, adjustments, modifiers, CPT codes; PM Access export includes "charges, payments, and write-offs" | Product has extensive claims management (ClaimInspector, denial management) — claims data likely in undocumented Access export |
| Payments | ⚠️ Partial | CSV exports include Patient Payments, Insurance Payments, Total Payments, Payment Method, Check Number; PM Access export mentions "payments" | Transaction-level payments present in CSV but no detailed payment/ERA data |
| Consents / directives | ✅ Covered | C-CDA includes Advanced Directives section; EHR Chart Print includes Advanced Directives | Available via C-CDA and chart print |
| Patient communications | ✅ Covered | EHR_Messages (23 fields) with message content, sender/recipient patient IDs, priority, timestamps; EHR Chart Print includes Portal and Staff Messages | Messages exported in bulk SQL |
| Specialty-specific data | ⚠️ Partial | Custom note templates (EHR_PatientNotes) capture specialty-specific assessments via the template system; Pediatric vital signs in C-CDA | Specialty data captured through generic template system rather than structured specialty tables |

## 6. Documentation Quality

**Strengths**:
- The EHR Bulk Export data dictionary provides column-level descriptions for most fields (267/313 = 85%)
- SQL JOIN examples for lab results tables help with data reconstruction
- Detailed explanation of the clinical notes template system with visual examples
- The documentation webpage clearly describes all 7 export options with UI navigation paths
- The 2-page desk guide provides a concise overview

**Weaknesses**:
- **No data types**: Column types (varchar, int, datetime, etc.) are never specified for any table
- **No value sets**: Enumerated values (e.g., what values AllergyStatus can take) are not documented
- **No foreign keys**: Relationships between tables are not formally documented (only the lab result JOIN is shown)
- **No schema for PM exports**: The Practice Management Access database export — which contains all billing/financial data — has zero field-level documentation
- **No sample data**: No sample export files are provided for any format
- **Could a developer build an import?** Partially. The EHR clinical data dictionary is usable but incomplete (missing types and value sets). The PM billing data is essentially undocumented at the field level — a developer would need to reverse-engineer the Access database schema.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

AdvancedMD provides a purpose-built export that covers clinical EHR data reasonably well (12 SQL tables with 313 fields), but the billing/financial/PM side — which is half of what makes AdvancedMD a comprehensive practice management platform — is only partially documented. The PM Data Export exists as a Microsoft Access file and presumably contains billing data (charges, payments, write-offs, carriers), but the complete absence of a field-level data dictionary for this export means we cannot verify what's actually included. Key product capabilities like claims management, denial tracking, ERA processing, eligibility verification, and detailed financial analytics have no documented export coverage. Vitals, procedures, care plans, goals, and orders are only available through the single-patient C-CDA export, not in the bulk export. The export demonstrates real effort on the clinical side but significant gaps on the administrative/financial side and some clinical domains.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly not a repackaged C-CDA or FHIR export. AdvancedMD built a multi-format export system with 7 distinct mechanisms covering different data domains and use cases. The EHR Bulk Data Export uses the vendor's internal SQL data model (12 tables from their native database), which is fundamentally different from a standardized clinical exchange format. The PM export uses Microsoft Access with the vendor's own schema. The C-CDA export exists as one option among many, not as the sole (b)(10) mechanism. The documentation, data dictionaries, and multi-modal approach all indicate genuine purpose-built work for (b)(10) compliance.

### Key Findings

1. **Split architecture creates documentation asymmetry**: The EHR clinical side has a 13-page data dictionary with 313 fields documented at the column level. The PM billing/financial side has zero field-level documentation — just a high-level description saying it includes "demographics, transactions, appointments, charges, payments, and write-offs."

2. **Prescriptions are exceptionally well-documented**: The EHR_Prescriptions table has 78 fields covering drug details, e-prescribing workflow, Surescripts integration, formulary data, and discontinuation tracking — far exceeding USCDI requirements.

3. **Clinical notes use a unique template system**: Rather than exporting structured note types, AdvancedMD exports raw template field data with positional coordinates (Left_Loc, Top_Loc) for visual reconstruction, plus WordMerge blob templates. This is thorough but requires significant effort to consume.

4. **No dedicated vitals, procedures, or orders tables in bulk export**: These are only available through the single-patient C-CDA export, creating a gap for bulk data portability.

5. **No sample data or machine-readable schemas**: All documentation is in PDFs and HTML prose. No sample export files, no JSON/XML schemas, no database schema DDL is provided.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   Mixed (SQL Server .bak, Microsoft Access .mdb, CSV, C-CDA XML, PDF, file system)
    Entities:        19 across all export mechanisms (12 SQL tables in EHR bulk export)
    Fields:          434 total (313 in EHR bulk export)
    Descriptions:    68% of fields have descriptions (85% in EHR bulk export)
    Sample data:     No
    Bulk export:     Yes (3 bulk mechanisms: PM Access, EHR SQL .bak, Scanned docs)
    Domains covered: 7 of 18 fully covered, 9 partially covered, 2 not covered

### Bottom Line

AdvancedMD built a genuine multi-format EHI export system that goes well beyond repackaging a C-CDA, particularly strong on clinical data (prescriptions, lab results, notes, allergies, immunizations). However, the export has a significant documentation gap: the billing/financial side — half of what the product does — lacks any field-level data dictionary, making it impossible to verify what's actually exported. A patient would get their clinical data comprehensively but would need to trust the undocumented PM Access export for billing data, and would miss vitals, procedures, orders, and care plans unless they also ran the single-patient C-CDA export separately.

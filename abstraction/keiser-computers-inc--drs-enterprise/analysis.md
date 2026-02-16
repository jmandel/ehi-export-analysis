# EHI Export Analysis: Keiser Computers, Inc.

**Product**: Drs Enterprise 12
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1764.DrsE.12.01.1.221213 (CHPL #11072)

## 1. Product Context

Drs Enterprise is a certified Complete Ambulatory EHR developed by Keiser Computers, Inc. (Fort Lauderdale, FL), a small vendor operating since 1985. The product targets small to medium-sized medical practices across multiple specialties including orthopedics, ophthalmology, sports medicine, and OB/GYN.

**Key data domains the product stores:**
- **Clinical documentation**: Chart-centric clinical narratives ("Clicktation"), customizable WYSIWYG templates, progress notes
- **Documents & images**: Scanned documents, PDFs, Word files, photographs, RTF files, faxes — organized in customizable folder/category structures with QR-code-based automated filing
- **E-prescribing**: Via SureScripts/GoldRx/SafeRx integration with drug interaction checking
- **Lab results**: Received via HL7 interface, stored in both discrete and scanned formats
- **Charge capture**: Charges posted during visits, exported to external billing systems (MicroMD, Medisoft, Medical Manager, MedFX, PCN)
- **EOB Manager**: Explanation of Benefits processing
- **Tasks & messages**: Internal workflow tasks, phone messages, secure instant messaging
- **Forms**: Auto-populated clinical and administrative forms (Medicaid, hospital forms)
- **Patient portal data**: View/Download/Transmit certified
- **Fax communications**: Integrated fax system

**Critical distinction**: Drs Enterprise does **not** include a full practice management or billing system. It integrates with third-party PM systems and exports charge data to them. Core billing, claims submission, and accounts receivable reside in external systems.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Export_data.pdf` | 10-page PDF (1,001,575 bytes), created 2023-11-07 with Microsoft Word 2010. Primary export documentation describing C-CDA + proprietary XML sidecar format. Documents 7 XML entities with 71 fields, 2 enumerators (32 values), directory structure, and XML examples. | **Primary source** — contains all technical detail |
| `downloads/DataExport.html` | HTML landing page (8,300 bytes) at `drsdoc.com/DataExport`. Brief introduction paragraph and link to the PDF. | Low — just a landing page |
| `downloads/screenshot-DataExport-page.png` | Screenshot of the landing page (119,279 bytes). | Low — visual confirmation only |
| `downloads/enrichment/export-schema.json` | Machine-readable JSON extraction (20,080 bytes) of the PDF's full export schema: all 7 entities, 71 fields, 2 enumerators, file types, directory structure, and examples. | **High** — verified accurate against PDF text extraction |
| `downloads/enrichment/extract-export-schema.ts` | Bun TypeScript script (17,762 bytes) used to produce the schema JSON. | Reference — shows extraction methodology |
| `downloads/enrichment/README.md` | Documentation for the enrichment script. | Low — meta-documentation |

The PDF is the sole substantive artifact. There are no sample data files, no separate data dictionary, no JSON schemas, and no additional documentation beyond the PDF and its landing page. Both the EHI documentation URL (`drsdoc.com/DataExport`) and the PDF (`drsdoc.com/Export_data.pdf`) return HTTP 200 as of analysis date.

## 3. Export Mechanics

- **Format**: Hybrid — C-CDA 2.1 XML (`account_ccda.xml`) for standard clinical data, plus proprietary XML sidecar files and raw document files for non-C-CDA data
- **Mechanism**: Not explicitly documented. The PDF describes the export output structure but provides no user-facing instructions, screenshots, or UI workflow for initiating an export. The HTML landing page states the system "provides the capability to export" but doesn't explain how.
- **Single-patient vs bulk**: Both. The introduction states: "export Electronic Health Information (EHI) for a single patient as well as for multiple patients."
- **Access constraints**: None documented. No mention of fees, permissions, or restrictions.
- **Directory structure**: Patient data organized by Account ID converted to hexadecimal, using 4 levels of 2-hex-digit folders (e.g., Account ID 9999 → hex `270F` → path `00\00\27\0F`). Faxes organized into Year/Month subdirectories.
- **Error handling**: Documented — an `export_xml` folder is created with `errors_<Session_ID>.xml` if errors occur.

## 4. Export Content: What's In It

The export consists of two components:

### 4a. C-CDA Component (`account_ccda.xml`)

The C-CDA XML file contains the patient's core clinical data "in compliance with the USCDv1 standard." The documentation describes this as including "demographics, problems, medications, allergies, etc." but provides **no vendor-specific field mapping**. The documentation simply references the HL7 C-CDA 2.1 standard and links to HL7.org resources. There is no detail on:
- Which C-CDA sections Drs Enterprise populates
- How vendor-specific data maps to C-CDA elements
- What data is included beyond the "etc."
- Whether any vendor extensions are used

### 4b. Proprietary XML Sidecar Files

The non-C-CDA data is well-documented with 7 XML entities totaling 71 fields, all with names, types, and descriptions (100% coverage on both).

### Vendor's own content organization

The vendor organizes the export documentation around file types and XML entities. There are no explicit domain categories; the organization follows the file structure:

| Entity/Table | Fields | Described | Types | Context |
|---|---|---|---|---|
| Document | 15 | 15 (100%) | Yes | `<Document_ID>_info.xml` — document metadata (folder, dates, user-defined fields) |
| office_notes | 13 | 13 (100%) | Yes | `<Document_ID>_info.xml` — office notes linked to documents |
| tasks | 14 | 14 (100%) | Yes | `account_tasks.xml` and `<Document_ID>_info.xml` — workflow tasks |
| doc_data | 8 | 8 (100%) | Yes | `<Document_ID>_info.xml` — discrete clinical observations with LOINC codes |
| loinc_code | 1 | 1 (100%) | Yes | Nested within `doc_data` — LOINC code descriptions |
| fax_inbox | 10 | 10 (100%) | Yes | `Fax_inbox.xml` — incoming fax metadata |
| fax_outbox | 10 | 10 (100%) | Yes | `Fax_outbox.xml` — outgoing fax metadata |

**Additional export files (not XML entities):**
- `account_ccda.xml` — C-CDA clinical data (undocumented field-level detail)
- `Account_U.img` — Patient photo
- `<Document_ID>.<ext>` — Raw document files (PDF, TIF, RTF, XML, etc.)
- `Readme.txt` — Link to export documentation

**Enumerators documented:**
- `convert_type`: 12 unit conversion types (cv_none, cv_inches, cv_pounds, cv_Centimeters, cv_Celsius, cv_Fahrenheit, cv_Celsius_Fahrenheit, cv_snomed_enum, cv_Milimeters, cv_microns, cv_question_enum, cv_Kilogram)
- `TFieldType`: 20 Delphi-native field types (ftString, ftInteger, ftBoolean, ftFloat, ftDateTime, etc.) — reveals the product is built on Delphi/Object Pascal

**Notable observations:**
- The `doc_data` entity is the mechanism for exporting discrete clinical observations (vitals, etc.) with LOINC coding. The example shows a BMI value with LOINC code 39156-5.
- The `tasks` entity uses a Delphi null date (`1899-12-30 00:00:00`) for unset datetime fields, visible in the XML examples.
- All fax entity fields are optional; all office_notes and tasks fields are required.
- No value sets are documented for text-typed categorical fields (e.g., `task_priority_desc`, `task_type_desc`, `receive_status`, `sent_status`).
- No foreign key relationships are formally documented, though implicit links exist via `account_id`, `doc_id`, and `Document_id`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export has two tiers of documentation quality:

**Well-documented tier (proprietary XML sidecar):**
- **Document management**: 15 fields for document metadata (folder location, dates, user-defined fields) plus raw document files in original format. This is the strongest part — consistent with the product's document-centric design.
- **Office notes**: 13 fields capturing internal office notes linked to documents.
- **Tasks/workflow**: 14 fields for account- and document-linked tasks with priority, type, user assignment, and timestamps.
- **Discrete clinical data (Drs Data Lookup)**: 8 fields for LOINC-coded observations with unit conversion support.
- **Fax communications**: 20 fields across inbox/outbox fax metadata with TIF file exports.
- **Patient photo**: Exported as `Account_U.img`.

**Undocumented tier (C-CDA):**
- **Core clinical data**: Demographics, problems, medications, allergies are mentioned as being in the C-CDA file but have zero vendor-specific documentation. The vendor delegates entirely to the HL7 C-CDA 2.1 standard.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Mentioned in C-CDA description ("demographics") but no field-level detail | Product stores demographics; C-CDA would include standard demographic fields but vendor-specific fields unknown |
| Encounters / visits | ⚠️ Partial | Not explicitly mentioned; may be in C-CDA sections | Product documents visits via progress notes; likely in C-CDA but undocumented |
| Problems / conditions | ⚠️ Partial | Mentioned in C-CDA description ("problems") | Likely in C-CDA but no vendor-specific detail |
| Medications / prescriptions | ⚠️ Partial | Mentioned in C-CDA description ("medications"); e-prescribing integration data coverage unclear | Product integrates with SureScripts; prescription history detail in export unknown |
| Allergies | ⚠️ Partial | Mentioned in C-CDA description ("allergies") | Likely in C-CDA but no vendor-specific detail |
| Immunizations | ⚠️ Partial | Not mentioned; product is certified for (f)(1) immunization registry | May be in C-CDA but not confirmed in documentation |
| Vitals | ✅ Covered | `doc_data` entity with LOINC-coded observations (BMI example shown), plus conversion types for units (inches, pounds, Celsius, etc.) | Well-documented via Drs Data Lookup mechanism |
| Lab results | ⚠️ Partial | Not explicitly addressed in sidecar format; may be in C-CDA or exported as scanned document files | Product receives HL7 lab data; discrete results coverage unclear |
| Imaging / diagnostic reports | ⚠️ Partial | Documents exported in original format (TIF, PDF, etc.) — imaging results stored as documents would be included | Document-centric approach covers scanned images |
| Procedures | ⚠️ Partial | Not explicitly mentioned; may be in C-CDA | Coverage unknown |
| Clinical notes / documents | ✅ Covered | All chart documents exported as original files with metadata (15 fields per document), office notes (13 fields), and document-linked discrete data | Strong — core strength of the product |
| Care plans / goals | ❌ Not covered | No mention in export documentation | May not be a core product feature; unclear |
| Orders / referrals | ❌ Not covered | No mention in export documentation | Product may generate referrals; not confirmed in export |
| Insurance / coverage | ❌ Not covered | Not in sidecar format; may be in C-CDA (unlikely — C-CDA doesn't typically include insurance) | Product imports insurance data from PM systems; may be a gap if stored locally |
| Claims / billing | ❌ Not covered | No billing entities in export | Product has charge capture and EOB Manager; charges and EOBs are EHI. **However**, core billing resides in external PM systems, so the gap is limited to charge capture data and EOBs within Drs Enterprise |
| Payments | N/A | N/A | Full billing/payments handled by external PM systems |
| Consents / directives | ❌ Not covered | Not mentioned | If stored as documents, they'd be exported as files; discrete consent data not addressed |
| Patient communications / portal messages | ❌ Not covered | Secure messaging not mentioned in export; fax communications are covered | Internal instant messages and phone messages not in export |
| Specialty-specific data | ⚠️ Partial | Custom templates and forms would be exported as documents, but discrete specialty data coverage depends on how the product stores it | Product emphasizes customizable templates; if forms are stored as documents they'd be included as files |

### Summary of coverage

- **6 domains** are clearly or partially covered by the proprietary XML sidecar documentation (documents, office notes, tasks, vitals/observations, faxes, patient photos)
- **6+ domains** are nominally covered by the C-CDA but lack vendor-specific documentation (demographics, problems, medications, allergies, encounters, possibly labs/immunizations/procedures)
- **5 domains** appear absent from the export (billing/charges, insurance, care plans, orders/referrals, patient communications beyond fax)
- The C-CDA component makes exact coverage assessment difficult — the vendor claims it covers clinical data but provides no mapping

## 6. Documentation Quality

**Strengths:**
- The proprietary XML sidecar format is well-documented: every field has a name, type, and description (71/71 = 100% coverage). XML examples are provided for 5 of 7 entities.
- The document is structured clearly with tables for each entity.
- The directory structure is explained with examples.
- Error handling is documented (export_xml folder with errors XML).
- Two enumerators are fully documented with 32 total values.
- Optionality (required vs. optional) is specified for every field.

**Weaknesses:**
- **The C-CDA component is entirely undocumented** at the vendor level. This is the core clinical data export, but the vendor provides only a reference to the HL7 standard and the word "etc." A developer receiving this export would have to parse the C-CDA blindly with no guidance on which sections are populated or how vendor data maps to C-CDA elements.
- **No sample data files** are provided. No test export, no example C-CDA, no example sidecar files beyond the inline XML snippets.
- **No user guide** for performing the export. The documentation describes the output but not how to produce it.
- **No machine-readable schema** (e.g., XSD) for the proprietary XML format. The schema is documented only in the PDF tables.
- **Value sets are missing** for several text-typed fields: `task_priority_desc`, `task_type_desc`, `type_name` (office note types), `receive_status`, `sent_status`, `document_folder_desc`. Only the `convert_type` and `TFieldType` enumerators are documented.
- **No relationships or foreign keys** are formally documented, though cross-references via `account_id`, `doc_id`, and `Document_id` are apparent from context.

**Could a developer build an import?** For the proprietary XML sidecar files — yes, with reasonable effort. The field definitions, types, and examples are sufficient. For the C-CDA — a developer experienced with C-CDA 2.1 could parse it using standard libraries, but without knowing which sections Drs Enterprise populates, they'd need to inspect actual exports to understand coverage.

## 7. Overall Assessment

### Classification

**Partial native export**

The export is a hybrid: C-CDA for standard clinical data plus a proprietary XML sidecar format for data that doesn't fit in C-CDA (documents, tasks, office notes, vitals with LOINC codes, faxes). This goes beyond a pure "standard-based projection" because the sidecar files export vendor-native data structures. However, the C-CDA portion is documented only by reference to the external standard, and several data domains the product stores — notably charge capture data, EOBs, and internal messaging — are absent from the export documentation. The overall coverage is incomplete for a "(b)(10) all EHI" export.

### Key Findings

1. **Genuine (b)(10) effort, not a FHIR/C-CDA repackaging**: The vendor built a custom export that goes beyond standard C-CDA by including proprietary XML sidecar files for documents, tasks, office notes, discrete observations with LOINC codes, and fax communications. This demonstrates awareness of the requirement to export *all* EHI, not just what fits in a clinical summary.

2. **C-CDA clinical data is documented by reference only**: The core clinical data component (`account_ccda.xml`) has zero vendor-specific documentation. The vendor simply points to the HL7 C-CDA 2.1 standard and says the data "is in compliance with USCDv1." No field mapping, no section inventory, no sample file. This is the largest data component and the least documented.

3. **Proprietary sidecar format is well-documented**: The 7 XML entities (71 fields) in the sidecar files have 100% description and type coverage with XML examples. For a 10-page document from a small vendor, this is above average.

4. **Charge capture and EOB data are missing from the export**: The product stores charge capture data and Explanation of Benefits records (per the product research and feature list). These are billing records about patients — part of the designated record set under HIPAA. The export documentation makes no mention of charges, CPT/ICD codes, or financial data.

5. **No sample data or export instructions**: There are no test exports, sample files, or user-facing documentation on how to perform the export within the application. A practice administrator would need to contact the vendor to learn how to run it.

### Summary Stats

```
Classification:  Partial native export
Export format:   C-CDA 2.1 XML + proprietary XML + raw document files
Model type:      Hybrid (standard projection for clinical data, native for sidecar data)
Entities:        7 (proprietary sidecar only; C-CDA entities undocumented)
Fields:          71 (proprietary sidecar only; C-CDA fields undocumented)
Descriptions:    100% (of the 71 proprietary fields)
Sample data:     No
Bulk export:     Yes (single-patient and multi-patient)
Domains covered: ~8 of 15 applicable domains (with many only via undocumented C-CDA)
```

### Bottom Line

Drs Enterprise's EHI export is a genuine but incomplete effort. The proprietary XML sidecar files for documents, tasks, notes, vitals, and faxes are well-documented and represent real native data the product stores. However, the core clinical data is delegated entirely to an undocumented C-CDA file, and charge capture/EOB data — which are part of the patient's designated record set — are absent from the export. A patient would receive their documents and clinical summary, but the completeness and interpretability of the clinical data depends on an opaque C-CDA with no vendor-specific guidance.

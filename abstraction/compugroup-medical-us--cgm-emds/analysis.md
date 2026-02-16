# EHI Export Analysis: CompuGroup Medical US

**Product**: CGM eMDs v10
**Analysis date**: 2026-02-16
**CHPL IDs**: 11133 (15.04.04.2700.eMDs.10.02.1.221227)

## 1. Product Context

CGM eMDs is an **integrated EHR and practice management suite** for ambulatory/outpatient practices, originally created in 1996 and now owned by CompuGroup Medical (acquired via eMDs in 2020 for $240M). It is a single certified module encompassing clinical charting, e-prescribing, scheduling, practice management, billing, and patient engagement. The product supports 70+ specialties and serves small-to-medium practices including CHCs, FQHCs, and RHCs.

**Key data domains the product stores** (relevant for export completeness assessment):
- **Clinical**: encounter notes (point-and-click + templates for 70+ specialties), problem lists, medication lists, allergies, immunizations, vitals, lab orders/results, procedures, social history, family history, SDOH, care plans, clinical decision support alerts
- **E-Prescribing** (CGM PRESCRIBE): prescriptions including EPCS, prior authorizations, PDMP integration, medication benefit info
- **Billing/PM**: full integrated practice management — claims, charges, payments, adjustments, ERA posting, eligibility verification, denial management (via eMEDIX clearinghouse)
- **Document management** (DocMan): scanned documents, imported files/images, external source documents
- **Patient engagement**: patient portal (secure messaging, intake forms, health records), CGM CONNECTION (automated communications)
- **Internal messaging** (TaskMan): messages and task assignments between staff
- **Referrals/authorizations**: inbound/outbound referral tracking
- **Quality reporting** (CGM MEASURES): eCQM/MIPS tracking
- **Specialty modules**: includes dedicated OB module, templates for 70+ specialties

This is a broadly-featured ambulatory EHR with integrated billing — the (b)(10) export should cover clinical data, billing/financial records, documents, and specialty-specific data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/cgm-emds-electronic-health-information-export-user-guide.pdf` | **Primary EHI export documentation.** 14-page PDF (December 2023). Contains file inventory, 27 document categories, and field-level data dictionary for 5 export files. | **High** — sole source of export content details |
| `downloads/fhir-api-documentation-guide.pdf` | FHIR R4 API documentation (76 pages, April 2024). This is the (g)(10) standardized API — separate from the (b)(10) export. Covers US Core resources. | **Medium** — useful for confirming (b)(10) is distinct from (g)(10) |
| `downloads/screenshot-certifications-links.png` | Screenshot of the CGM eMDs product page certifications accordion showing EHI Export Documentation link. | **Low** — confirms navigation only |
| `downloads/enrichment/ehi-data-dictionary.json` | Prior agent's structured extraction of the PDF data dictionary. 28,725 bytes. | **Medium** — used to cross-check my own parse; confirmed consistent |
| `product-research.md` | Product research on CGM eMDs capabilities, modules, and data types. | **High** — establishes baseline for coverage assessment |

## 3. Export Mechanics

- **Format**: Password-protected ZIP file containing 5 structured files (4 XLSX spreadsheets + 1 RTF text file) plus a DocMan Files folder with unstructured documents/images
- **Naming convention**: `Patient(lastname, firstname[AccountNumber]) YYYY-MM-DD HH-MM-SS.zip`
- **Mechanism**: Generated within the CGM eMDs application (UI-based). The PDF describes this as "exported Electronic Health Information (EHI) zip file generated using CGM eMDs"
- **Scope**: Single-patient export only
- **Bulk capability**: Not documented; no evidence of bulk/multi-patient export
- **Access constraints**: The ZIP file is password-protected; password is provided separately to the patient
- **Fees**: Not mentioned in the export documentation (a separate "Costs" document is linked from the certifications page but was not collected)
- **Distinct from (g)(10)**: CGM eMDs has a separate FHIR R4 API for (g)(10). The EHI export is entirely separate — different format (XLSX/RTF vs FHIR), different mechanism (file download vs API), different scope (broader than US Core)

## 4. Export Content: What's In It

The export is documented via a single 14-page PDF. It defines:
- **27 document categories** (types of data that may appear in the export)
- **5 structured export files** with field-level data dictionaries
- **1 document collection** (DocMan Files folder) for unstructured content

### Field-level documentation

All 162 fields across the 5 structured files have **field names and data types** specified. **No fields have descriptions** beyond the field name itself. Data types used: String, Date, Time, Number, Image, String List. No value sets, format specifications, foreign keys, or relationships are documented.

### Vendor's own content organization

The vendor organizes the export into 5 structured files plus a document folder. Each file maps to a functional domain:

| Entity/File | Fields | Sections | Types | Category |
|---|---|---|---|---|
| Chart Cover Report.xlsx | 53 | 7 | yes | Demographics / Insurance |
| Entire Patient Chart Report.xlsx | 14 | 1 | yes | Clinical Documentation |
| Health Summary Report.xlsx | 27 | 8 | yes | Clinical Summary |
| Referral Authorization Report.xlsx | 19 | 4 | yes | Referrals / Authorizations |
| Trial Balance Report.rtf | 49 | 9 | yes | Billing / Financial |
| DocMan Files (folder) | 0 (unstructured) | — | — | Documents / Images |

**Notable details by file:**

**Chart Cover Report.xlsx** (53 fields): The richest structured file. Covers patient demographics (16 fields: name, address, DOB, SSN, gender, marital status, DL#, multiple phone numbers, provider, first visit date, financial group), employment info (6 fields), guarantor demographics (10 fields), insurance info (10 fields including card images), and a health summary section with string-list fields for problems, medications, and histories.

**Entire Patient Chart Report.xlsx** (14 fields): The most important clinical file but the **least well-documented**. Its single section lists 14 high-level content categories (e.g., "All clinical visit notes", "Allergies", "Problem list", "Immunizations", "SDOH responses") each typed as "String" — meaning the actual column-level structure within the spreadsheet is not specified. This file likely contains hundreds of data points per patient but is described only at a category level.

**Health Summary Report.xlsx** (27 fields): Current clinical summary — problems, medications (with dosage, form, instructions), allergies, past medical/surgical/family/social history, tobacco/alcohol/substance status, mental health history, communicable diseases, health maintenance items, and a "Tests and Procedures" section (listed but with **zero fields documented**).

**Trial Balance Report.rtf** (49 fields): Detailed billing data organized per invoice. Includes invoice headers (ICD/CPT codes, superbill reference, fees), itemized CPT line items (codes, dates, units, fees), insurance data per invoice (company, policy, filing status), payment details (patient vs insurance payments, adjustments, check/credit card info), payment totals, and invoice balances. This is genuinely deep billing documentation.

**DocMan Files**: Unstructured folder containing 10 document categories: C-CCD (CDA XML), Care Plans (CDA XML), Consents (TIF/PDF), Images, Lab Images (HL7/TIF), Letters, Patient Documents, Pregnancy History (RTF/PDF), Procedure Images, and Radiology Images. No field-level structure — these are raw document files.

### 27 Document Categories

The PDF defines 27 categories of data that may appear in the export. These span across the structured files and DocMan folder:

- **In structured files (17 categories)**: Authorizations, Claim Payments, Claim Charges, Insurance, Past Medical History, Patient Allergies, Patient Demographics, Patient Visit Notes, Patient Education, Patient Immunizations, Patient Medications, Patient Messages, Patient Problems, Orders, Referrals, SDOH, Social History
- **In DocMan Files (10 categories)**: C-CCD, Care Plan, Consents, Images, Lab Images, Letters, Patient Documents, Pregnancy History, Procedure Images, Radiology Images

Full inventory available in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export covers four broad areas:

1. **Demographics/Insurance** (Chart Cover Report): Deep — 53 fields covering patient demographics, employment, guarantor info, and insurance details including card images. This exceeds what USCDI requires for patient demographics.

2. **Clinical Documentation** (Entire Patient Chart + Health Summary + DocMan): Broad but shallowly documented — the Entire Patient Chart Report captures visit notes, allergies, medications, problems, immunizations, messages, histories, education, and SDOH, but at a category level rather than field level. Health Summary adds structured medication fields (name, dosage, form, instructions) and health maintenance tracking. DocMan captures care plans, images, and unstructured documents.

3. **Billing/Financial** (Trial Balance Report): Genuinely detailed — 49 fields organized around invoices with ICD/CPT codes, charges, fees, insurance and patient payments, adjustments, and balances. This is the strongest signal that this is a purpose-built EHI export, not a repackaged clinical exchange.

4. **Referrals/Authorizations** (Referral Authorization Report): Moderate — 19 fields covering referral tracking, authorization numbers, status, and dates.

**Thinnest areas**: The Entire Patient Chart Report (the most important clinical file) is described with only 14 category-level fields, making it impossible to assess the actual granularity of clinical data export. The "Tests and Procedures" section in Health Summary Report has **zero fields documented**.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Chart Cover Report (16 patient fields + 6 employment fields) | Thorough; includes SSN, DL#, marital status, employer |
| Encounters / visits | ✅ Covered | Entire Patient Chart Report ("All clinical visit notes") | Visit notes exported but field-level detail unknown |
| Problems / conditions | ✅ Covered | Health Summary Report (Current Problems), Entire Patient Chart (Problem list) | Present in two files |
| Medications / prescriptions | ✅ Covered | Health Summary Report (4 medication fields: name, dosage, form, instructions), Chart Cover Report (current medication list) | Medication lists covered; prescription transmission records (e-Rx, EPCS details) not mentioned |
| Allergies | ✅ Covered | Health Summary Report (Allergy/Reaction), Entire Patient Chart (Allergies) | Present |
| Immunizations | ✅ Covered | Entire Patient Chart Report (Immunizations) | Present but field-level detail not documented |
| Vitals | ⚠️ Partial | Not explicitly listed as a category; likely embedded in clinical visit notes | Product stores vitals; no dedicated export section or fields documented |
| Lab results | ⚠️ Partial | Health Summary "Tests and Procedures" section (0 fields documented); Lab Images in DocMan (HL7 format) | Lab images (HL7) exported; unclear if discrete result values are structured |
| Imaging / diagnostic reports | ✅ Covered | DocMan Files: Radiology Images, Procedure Images, Lab Images | Images exported; narrative reports likely in visit notes |
| Procedures | ⚠️ Partial | "Tests and Procedures" section (0 fields); CPT codes in Trial Balance; Procedure Images in DocMan | Billing codes captured; clinical procedure details unclear |
| Clinical notes / documents | ✅ Covered | Entire Patient Chart Report (all visit notes), DocMan Files (letters, patient documents) | Core strength of the export |
| Care plans / goals | ✅ Covered | DocMan Files (Care Plan as CDA XML) | Present as CDA documents |
| Orders / referrals | ✅ Covered | Health Summary Report (Orders), Referral Authorization Report (19 fields) | Referrals well-documented; order field detail thin |
| Insurance / coverage | ✅ Covered | Chart Cover Report (10 insurance fields including card images), Trial Balance (insurance data per invoice) | Thorough |
| Claims / billing | ✅ Covered | Trial Balance Report (49 fields: ICD/CPT codes, charges, fees) | **Strong** — genuinely detailed billing export |
| Payments | ✅ Covered | Trial Balance Report (payment data, adjustments, totals, balances) | Detailed patient and insurance payment tracking |
| Consents / directives | ✅ Covered | DocMan Files (Consents as TIF/PDF) | Present as scanned/uploaded documents |
| Patient communications | ✅ Covered | Entire Patient Chart Report (Patient Messages), DocMan Files (Letters) | Messages included; portal message detail unclear |
| Specialty-specific (OB) | ✅ Covered | DocMan Files (Pregnancy History as RTF/PDF) | OB module data exported |
| Family health history | ✅ Covered | Entire Patient Chart Report, Health Summary Report (Family History List) | Present in two files |
| Social history / SDOH | ✅ Covered | Entire Patient Chart Report (SDOH responses), Health Summary Report (Social History, Tobacco/Alcohol/Substance status) | Well-represented |
| Mental health history | ✅ Covered | Entire Patient Chart Report, Health Summary Report (Mental Health History list) | Present |
| Patient education | ✅ Covered | Entire Patient Chart Report (Patient Education) | Present |

**Key gaps relative to product capabilities:**

1. **Vital signs**: Product stores vitals; no explicit export category or fields for vital sign data. Likely embedded in visit notes but not confirmed.
2. **Discrete lab results**: Lab images in HL7 format are exported, but structured discrete results (values, reference ranges, units) are not clearly documented. The "Tests and Procedures" section has 0 documented fields.
3. **E-Prescribing details**: Medication lists are exported, but prescription transmission records (Surescripts transactions, EPCS details, PDMP queries, prior authorization specifics from CGM PRESCRIBE module) are not mentioned.
4. **Internal messaging/tasks**: The TaskMan internal messaging system is not referenced in the export.

## 6. Documentation Quality

**Strengths:**
- Clear, organized 14-page document with table of contents
- Field names and data types for all 162 structured fields
- Comprehensive table of 27 document categories with descriptions, locations, and file types
- Practical user-facing instructions (ZIP extraction for Windows/Mac)
- Export file naming convention documented with example

**Weaknesses:**
- **No field descriptions**: All 162 fields have names and types but zero have descriptions explaining what the field contains or how it's populated (0% description rate)
- **No value sets**: Coded fields (Patient Gender, Marital Status, payment Type, Status) have no documented valid values
- **No format specifications**: Date format, string encoding, number precision are unspecified
- **No relationships/foreign keys**: No documentation of how records in different files relate (e.g., how an invoice in Trial Balance links to a visit in Entire Patient Chart)
- **No sample data**: No example exports or sample records provided
- **No machine-readable schema**: The XLSX structure is documented only in the PDF; no XSD, JSON Schema, or programmatic specification
- **Entire Patient Chart Report is under-documented**: The most important clinical file has only 14 category-level "fields" — the actual column structure within the XLSX is not specified
- **"Tests and Procedures" section is empty**: Listed as a section in Health Summary Report but has zero fields documented
- **No versioning/change history**: Document is dated December 2023 with no revision tracking

A developer could understand the general structure of the export from these docs but would need sample data to build a reliable import. The lack of field descriptions, value sets, and inter-file relationships means significant guesswork would be required for semantic interpretation.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers a meaningful breadth of domains: demographics, clinical notes, problems, medications, allergies, immunizations, referrals/authorizations, patient messages, social history, SDOH, documents/images, and — critically — detailed billing data. The inclusion of the Trial Balance Report with 49 fields of billing detail (ICD/CPT codes, charges, insurance and patient payments, adjustments, balances) demonstrates genuine engagement with (b)(10) beyond clinical exchange. However, there are notable gaps: vitals are not explicitly addressed, discrete lab results lack structured documentation, e-prescribing details (EPCS, PDMP, prior auth records) from the CGM PRESCRIBE module are absent, and the internal TaskMan messaging system is not included. The Entire Patient Chart Report likely contains much of this data within visit notes, but the documentation is too thin to confirm. The export merits "Partial" rather than "Comprehensive" because several product capabilities (discrete lab values, e-prescribing workflow data, vitals) have unclear or absent export coverage.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged (g)(10) or C-CDA. The evidence:
1. **Separate mechanism**: The export is a ZIP of XLSX/RTF files generated in-app, entirely distinct from the FHIR R4 API documented in the separate 76-page FHIR guide
2. **Billing data**: The Trial Balance Report contains detailed billing/payment data (49 fields) that would never appear in a (g)(10) FHIR API or C-CDA exchange
3. **DocMan Files**: The export includes the full document management repository (scanned documents, images, CDA files, HL7 lab data) — broader than any clinical exchange format
4. **Custom file structure**: The XLSX/RTF format is CGM eMDs' own export design, not a standard template
5. **27 document categories**: The vendor defined a specific taxonomy of exportable content that goes well beyond USCDI

The format is proprietary (XLSX/RTF rather than FHIR or C-CDA) but this is appropriate for an ambulatory EHR export and demonstrates that the vendor built something specifically for (b)(10) compliance.

### Key Findings

1. **Purpose-built export with real billing data**: The Trial Balance Report (49 fields) with detailed charge/payment/adjustment data per invoice is the strongest evidence this is a genuine (b)(10) effort, not a repackaged clinical exchange.

2. **Entire Patient Chart Report is critically under-documented**: The most important clinical file — containing all visit notes, allergies, medications, problems, immunizations, messages, and histories — is documented with only 14 category-level labels, not actual column specifications. This makes it impossible to assess the true granularity of clinical data export.

3. **162 fields documented but with zero descriptions**: Every field has a name and data type, but none have explanatory descriptions, value sets, or format specifications. This is a usable but thin data dictionary.

4. **27 document categories provide broad coverage**: The export spans clinical, billing, administrative, and document domains — demographics, insurance, visit notes, medications, problems, immunizations, orders, referrals, billing charges/payments, and 10 types of DocMan documents.

5. **Vitals and discrete lab results are unclear gaps**: Despite the product storing both, neither has explicit export documentation. They may be embedded in visit notes or the undocumented "Tests and Procedures" section, but this cannot be confirmed from the documentation alone.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   XLSX + RTF + mixed documents (in password-protected ZIP)
    Entities:        6 (5 structured files + 1 document collection)
    Fields:          162
    Descriptions:    0% (0 of 162 fields have descriptions)
    Sample data:     No
    Bulk export:     No (single-patient only)
    Domains covered: 18 of 21 applicable domains (vitals unclear, discrete labs unclear, e-prescribing details absent)

### Bottom Line

CGM eMDs built a genuine purpose-specific EHI export that goes beyond clinical exchange to include detailed billing data, document management contents, and 27 categories of patient information. The export's main weakness is documentation quality: the most important clinical file (Entire Patient Chart Report) is documented at a category level rather than field level, and no fields anywhere have descriptions, value sets, or format specifications. A patient would receive a broadly complete record, but a developer trying to programmatically import the data would face significant ambiguity.

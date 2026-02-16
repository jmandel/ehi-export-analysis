# EHI Export Analysis: Health Information Management Systems, LLC

**Product**: Axiom EHR (Version 7)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1590.Axio.02.01.1.201229

## 1. Product Context

Axiom is a **cloud-based, integrated EHR platform purpose-built for behavioral health and integrated healthcare providers**, developed by Health Information Management Systems, LLC (HiMS), a small specialty vendor based in Arizona. The product is a full-platform solution — not a narrow clinical module — encompassing:

- **Clinical documentation**: AI-powered note-taking, customizable clinical templates, drag-and-drop form builder, e-signatures
- **Practice management & scheduling**: appointment scheduling across teams and locations
- **Billing & RCM**: full built-in revenue cycle management — claims submission, eligibility verification, payment posting, HCPCS/CPT/ICD-10 coding, contract management, claims appeals
- **E-prescribing & labs**: full e-prescribing, lab integration and results management
- **Telehealth**: built-in HIPAA-compliant virtual sessions
- **Patient portal (Axiom Connect)**: health record access, appointment scheduling, secure messaging
- **Mobile (AxiomMobile)**: clinician mobile app
- **Specialty modules**: Electronic Visit Verification (EVV), developmental disability (DD), foster care support, inpatient services

Target market includes behavioral health clinics, addiction treatment centers, integrated health providers, FQHCs, and DD/foster care facilities. Notable customers include COPE Community Services (15,000+ clients) and Service Access & Management (SAM).

**For (b)(10) purposes**, the export should cover: clinical documentation (behavioral health assessments, encounter notes, treatment plans), demographics, medications, labs, diagnoses, billing/claims data, insurance/eligibility, EVV records, DD/foster care records, patient portal communications, custom forms, and e-prescribing data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Axiom-EHI-Export-Instructions.pdf` | 4-page PDF (187 KB) with procedural instructions and screenshots for performing EHI exports. Created 2026-01-30 by Khalid Maskari. No data dictionary, no format specification, no schema. | **Primary artifact** — but extremely thin. Only tells us an export button exists and shows a form-selection interface. |
| `downloads/screenshot-ehi-export-page.png` | Screenshot of the axiomehr.com/ehiexport/ web page. Shows a purple hero banner with "EHI Export Instructions" heading and a single "Download PDF" button. | **Minimal** — confirms the web page is just a download link. |

**That is all.** No data dictionary, no schema file, no sample export data, no format specification, no additional documentation artifacts exist in the downloads. The entire (b)(10) EHI export documentation is a single 4-page PDF.

## 3. Export Mechanics

- **Format**: Unknown. The export produces a password-encrypted compressed ZIP file (filename is a GUID, e.g., `1BA97693-8CC0-4C82-A96F-FF42748F15AA.zip`). What's inside the ZIP is never documented — could be PDFs, CSVs, JSON, or anything else.
- **Mechanism**: UI-based. Users navigate to the Report page in Axiom EHR, enter patient name and date range parameters, select from a "Form Types" dropdown, click "BUILD REPORT," then select documents to export and choose "EHI Export" from an action dropdown.
- **Single-patient**: Supported. The user selects a patient, filters by date range and form types, selects specific documents, and triggers export.
- **Bulk export**: Claimed. The PDF states: "The request for patient population export will include all population data. The export file(s) will be compressed to reduce file size." No further details — no screenshot, no instructions for how to initiate it, no definition of "all population data."
- **Delivery**: The encrypted ZIP file and its password are emailed to both the employee and the patient.
- **Access constraints**: Requires authorized user login to Axiom EHR. No mention of fees.

## 4. Export Content: What's In It

### What the documentation reveals

The documentation provides **zero information** about what data fields, tables, or structured content the export contains. There is:

- **No data dictionary** — not a single field name, type, or description is documented
- **No schema** — no JSON schema, XML schema, database schema, or any structural documentation
- **No format specification** — the internal format of the exported ZIP is never stated
- **No sample data** — no example exports are provided
- **No entity/table listing** — no enumeration of what data categories are included

### What can be inferred from screenshots

The PDF screenshots (pages 2–4) reveal the export operates as a **document/form-level selection mechanism**:

1. **Page 2**: Shows a "Form Types" dropdown with ~12 visible entries, all prefixed with "Dynamic Form:" — these appear to be behavioral health assessment forms configured in the system:
   - Dynamic Form: AccountLogin
   - Dynamic Form: Active Meds Test
   - Dynamic Form: ADAD Test Form
   - Dynamic Form: Adult ADHD Self-Report Scale (ASRS-v1...)
   - Dynamic Form: Adult Brief Pscyhosocial Assessment - Dra... (appears twice)
   - Dynamic Form: Advance Directive Form
   - Dynamic Form: Agency - Encounter Form Signature
   - Dynamic Form: AKDA
   - Dynamic Form: All Tools Form
   - Dynamic Form: allow fax 1

2. **Page 3**: Shows the export selection list for patient "KING, TERRY" with 16 forms. Visible entries:
   - Dynamic Form: 13-17 EPSDT
   - Dynamic Form: NPP Weekly Progress Report (×2)
   - Encounter: CPT Note

3. **Page 4**: Shows the "EHI Export History" table with one completed export record of type "Encounter - CM 3.0"

The form types visible are overwhelmingly **behavioral health clinical assessments and encounter notes**. There is no evidence of billing data, medication lists, lab results, demographics tables, insurance records, or any structured clinical data being part of this export.

### Vendor's own content organization

No content organization exists — the vendor provides no categorization, no table listing, no entity enumeration. The only structure visible is the "Form Types" dropdown which lists dynamic forms and encounter types.

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| *(none documented)* | N/A | N/A | N/A | N/A |

The export appears to be a **document-level export** — users select individual clinical forms/encounters and export them, likely as rendered documents rather than structured data. This is fundamentally different from a structured data export with defined tables and fields.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation provides **no information about data domain coverage**. The only content organization is the "Form Types" dropdown in a screenshot, which shows behavioral health assessment forms (ASAM, ADHD scales, psychosocial assessments, EPSDT, progress reports) and encounter notes (CPT Notes, CM 3.0 encounters).

The bulk export section claims to "include all population data" but does not define what "all population data" means — there is no enumeration of included data categories, no list of form types, and no indication of whether non-form data (demographics, medications, billing) is included.

The export mechanism appears to be form/document-centric: users select specific clinical forms and encounter documents to export. This architecture suggests the export covers **clinical documentation** (assessments, progress notes, encounter notes) but may not cover **structured data** (discrete demographics, medication lists, lab results, billing records) at all.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❌ Not covered | No demographics entity or fields documented. Export history shows patient name/ID but that's metadata, not exported demographic content. | Product stores demographics (per product research). Significant gap. |
| Encounters / visits | ⚠️ Partial | "Encounter: CPT Note" and "Encounter - CM 3.0" visible in screenshots, but no field-level detail about what's exported for an encounter. | Product stores encounters. Coverage is implied but unverifiable. |
| Problems / conditions / diagnoses | ❌ Not covered | No problem list, diagnosis, or condition entity documented or visible. | Product stores diagnoses (ICD-10 coding, problem lists). Gap. |
| Medications / prescriptions | ❌ Not covered | "Dynamic Form: Active Meds Test" visible in dropdown, but this appears to be a test form, not a medication list export. No e-prescribing data mentioned. | Product has full e-prescribing. Significant gap. |
| Allergies | ❌ Not covered | No allergy entity visible or documented. | Product likely stores allergies (certified for (a)(1) CPOE). Gap. |
| Immunizations | ❌ Not covered | No immunization entity visible or documented. | Product may store immunizations. Gap if applicable. |
| Vitals | ❌ Not covered | No vitals entity visible or documented. | Product likely stores vitals. Gap. |
| Lab results | ❌ Not covered | No lab entity visible or documented. | Product has lab integration. Gap. |
| Imaging / diagnostic reports | N/A | Not documented. | Behavioral health product — imaging not a core function. |
| Procedures | ❌ Not covered | No procedure entity visible or documented. | Product stores procedures (certified for (a)(14)). Gap. |
| Clinical notes / documents | ⚠️ Partial | Form-based export shows behavioral health assessment forms and encounter notes. This appears to be the primary content of the export. | Appears to be the export's main strength, but no field-level detail available to confirm completeness. |
| Care plans / goals | ❌ Not covered | No care plan entity visible or documented. | Product stores treatment plans/service plans. Gap. |
| Orders / referrals | ❌ Not covered | No order or referral entity documented. | Product likely handles orders (certified for CPOE). Gap. |
| Insurance / coverage | ❌ Not covered | No insurance entity documented. | Product does eligibility verification and insurance management. Gap. |
| Claims / billing | ❌ Not covered | No billing, claims, or RCM entity documented. | Product has full RCM — claims, payments, coding. **Major gap**. |
| Payments | ❌ Not covered | No payment entity documented. | Product handles payment posting. Gap. |
| Consents / directives | ⚠️ Partial | "Dynamic Form: Advance Directive Form" visible in Form Types dropdown. | At least one form type exists; coverage depth unknown. |
| Patient communications / portal messages | ❌ Not covered | No portal message or communication entity documented. | Product has Axiom Connect patient portal with secure messaging. Gap. |
| Behavioral health assessments (specialty) | ⚠️ Partial | Multiple behavioral health forms visible: ASAM, ADHD Self-Report Scale, Psychosocial Assessment, EPSDT, NPP Weekly Progress Report, ADAD Test Form. | This is the strongest area of evidence, but only form names are visible — no field-level content is documented. |
| EVV records (specialty) | ❌ Not covered | No EVV entity documented. | Product has EVV module. Gap. |
| DD / foster care (specialty) | ❌ Not covered | No DD or foster care entity documented. | Product has DD/foster care modules. Gap. |

## 6. Documentation Quality

The export documentation is **critically inadequate**:

- **No data dictionary exists.** Not a single field name, data type, or description is provided anywhere.
- **No format specification.** The internal structure of the exported ZIP file is never documented. A developer receiving an export file would not know what to expect inside.
- **No schema.** No machine-readable or human-readable schema of any kind.
- **No sample data.** No example exports are provided.
- **No entity listing.** No enumeration of what data categories are included in the export.
- **The entire documentation is 4 pages**, of which 1 is a cover page and ~2 are screenshots. The substantive prose content amounts to approximately 8 sentences.
- **Typos** in the documentation ("informaiton", "cllick", "compresses" for "compressed") suggest minimal review.
- **The bulk export section** is 2 sentences with no detail whatsoever.

A developer **could not build an import** from this documentation. They would not know:
1. What format the files inside the ZIP are in
2. What fields or data structures exist
3. How to interpret coded values
4. What relationships exist between exported items
5. What "all population data" means

This documentation reads as a **minimal compliance checkbox** — it demonstrates that an "EHI Export" button exists in the software, but provides no usable technical specification.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. The export *appears* to be a form/document-level export of clinical assessments and encounter notes, which would cover only a fraction of what Axiom stores. The product has full RCM/billing, e-prescribing, lab integration, patient portal, EVV, DD/foster care modules, and scheduling — none of which appear in the export documentation. The bulk export section claims "all population data" but this claim is unsupported by any specifics. Even for the clinical forms that are visible in screenshots, there is no field-level documentation to assess depth of coverage. The most generous reading is that the form-based export captures behavioral health assessment documents (the product's core clinical content), but even that is unverifiable without knowing what's inside the exported ZIP files.

**Axis 2 — Export approach: Unclear/undetermined**

The documentation is too thin to determine whether this is a purpose-built EHI export or a repackaged existing capability. The export mechanism (selecting forms from a Report page and exporting as encrypted ZIPs) could be either a new (b)(10)-specific feature or a pre-existing report/document export relabeled for compliance. The "EHI Export" action dropdown and the "EHI Export History" table suggest some purpose-built UI was created, but without knowing what data is actually exported (format, fields, scope), it's impossible to determine whether this genuinely exports all EHI or is just a clinical document download mechanism. The architecture — selecting individual form types rather than exporting all patient data automatically — raises concerns that this may be a clinical document export rather than a comprehensive structured data export.

### Key Findings

1. **The entire (b)(10) documentation is a 4-page PDF with zero data content specification.** No data dictionary, no schema, no format description, no sample data, no entity listing. This is the thinnest EHI export documentation possible while still having a document to point to. (`downloads/Axiom-EHI-Export-Instructions.pdf`)

2. **The export appears to be document/form-centric, not structured-data-centric.** The UI shows users selecting individual "Dynamic Form" types (behavioral health assessments, encounter notes) for export, rather than exporting structured data tables. This suggests the export may produce rendered documents rather than machine-readable structured data.

3. **No evidence of billing, medication, lab, or demographic data in the export.** Despite Axiom having full RCM, e-prescribing, lab integration, and demographic management, none of these data domains appear in the export documentation or screenshots. The visible form types are exclusively behavioral health clinical assessments and encounter notes.

4. **Bulk export is claimed but undocumented.** The PDF states bulk export "will include all population data" in two sentences with no further detail — no instructions, no screenshots, no definition of scope.

5. **Export format is completely unknown.** The output is a password-encrypted ZIP, but the contents (PDF? CSV? JSON? proprietary format?) are never specified. This makes independent import/use of the data impossible without reverse engineering.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined
Export format:   Unknown (encrypted ZIP; internal format undocumented)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Claimed but undocumented
Domains covered: 0 of 17 confirmed; 4 of 17 partially implied by screenshots
```

### Bottom Line

Axiom's (b)(10) EHI export documentation is a **minimal compliance stub** — a 4-page PDF demonstrating that an "EHI Export" button exists, with no specification of what data is actually exported, in what format, or at what level of completeness. For a product with full RCM, e-prescribing, lab integration, EVV, and behavioral health specialty modules, the absence of any data dictionary, schema, or format specification means it is impossible to verify whether patients or providers would receive a usable or complete copy of their data. The single biggest gap is the complete absence of documentation: without knowing what's in the export, the export is functionally opaque.

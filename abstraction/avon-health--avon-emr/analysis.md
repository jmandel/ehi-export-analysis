# EHI Export Analysis: Avon Health

**Product**: Avon EMR 1.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 11636 (15.04.04.3227.Avon.01.00.1.250514)

## 1. Product Context

Avon EMR is a cloud-based, all-in-one ambulatory EMR and practice management platform built by Avon Health, a startup founded in 2021 and ONC-certified in May 2025. The product targets ambulatory practices across multiple specialties (primary care, behavioral health, women's health, pediatrics, hospice, geriatrics) and virtual care companies.

The platform is modular, with toggleable features spanning:

- **Clinical documentation**: Visit notes, care plans, documents, AI Scribe (auto-generated note drafts)
- **Prescriptions**: E-prescribing, fulfillment tracking
- **Lab & imaging**: Lab orders to 1,000+ labs, imaging orders, parsed results
- **Scheduling**: Virtual/in-person appointments, patient self-scheduling, group sessions
- **Patient engagement**: Patient portal, messaging (in-app, 2-way SMS), intake forms, courses (patient education)
- **Billing & RCM**: Insurance eligibility checks, invoices, superbills, payment collection, revenue cycle management
- **Administration**: Custom fields, custom objects, custom pages, automations, tasks, fax

The sidebar navigation of the vendor's guides site (`guides.avonhealth.com`) confirms 20+ distinct functional modules including Messaging, Tasks, Invoices, Superbills, Revenue Cycle Management, Eligibility Checks, Fax, Courses, Custom Fields, Custom Objects, and AI Scribe — all of which represent data that could be part of the designated record set.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export.html` (52,873 bytes) | Full HTML of the EHI export documentation page at `guides.avonhealth.com/docs/ehi-export`. Single page with 388 words of substantive content. Lists 4 data categories and 24 data items at category level. No data dictionary, no schema, no sample data. | **Primary artifact** — contains all available export documentation |
| `downloads/ehi-export-page-screenshot.png` (466 KB) | Full-page screenshot of the EHI export documentation page. Visually confirms the HTML content: heading structure, bulleted data category lists, and sidebar navigation showing product modules. | Corroborative — confirms HTML content matches rendered page |
| `downloads/certification-page-screenshot.png` (664 KB) | Full-page screenshot of the ONC certification page at `avonhealth.com/meaningful-use`. Lists all certified criteria, certification date (May 14, 2025), product name (Avon EMR 1.0), CHPL number, costs section, MFA details, SVAP notice (WCAG 2.1 AA), and links to EHI Export Documentation and API Documentation. | Corroborative — confirms (b)(10) certification and links |

**Verification**: The live page at `https://guides.avonhealth.com/docs/ehi-export` was fetched during this analysis and matches the collected HTML artifact exactly — same content, same structure, no changes since collection on 2026-02-15.

**Notable absence**: No downloadable artifacts (PDFs, ZIPs, CSVs, JSON schemas, XLSX data dictionaries) were found on either the certification page or the EHI export documentation page. The entire (b)(10) documentation consists of a single web page.

## 3. Export Mechanics

- **Format**: ZIP file containing CSV files, PDF documents, and PNG images
- **Single-patient export**: Admin navigates to a patient's profile and clicks "Export EHI" button (self-service)
- **Population export**: Must email `support@avonhealth.com` with subject line "Patient Population b10 Export Request" — handled manually by support team "as it depends on size of data, time and efforts required to manage the server resources"
- **Access constraints**: Requires admin role. Population export is vendor-assisted, not self-service.
- **Fees**: Not mentioned in the export documentation. The certification page states users pay a monthly fee for the EMR; no separate export fee is documented.
- **Relationship to FHIR/API**: The export is clearly distinct from the vendor's REST/FHIR API (documented separately at `docs.avonhealth.com`). This is a native export mechanism, not a repackaged API.

## 4. Export Content: What's In It

### Documentation level

The documentation provides **category-level descriptions only**. There is:

- ❌ No data dictionary (no field/column names, no data types)
- ❌ No schema (no XSD, JSON Schema, DDL, or OpenAPI spec)
- ❌ No sample export files or example CSVs
- ❌ No documentation of CSV file structure (which CSVs are generated, what columns each contains)
- ❌ No documentation of relationships between entities
- ❌ No documentation of coded values or value sets
- ❌ No documentation of how many CSV files compose an export

The export documentation consists of 24 named data items organized into 4 categories. Each item is a single phrase (e.g., "Lab results," "Insurance claims") with no further elaboration.

### Vendor's own content organization

The vendor organizes data into 4 categories. Since no field-level detail exists, the table below reflects the entirety of what is documented:

| Category | Items Listed | Field-Level Detail | Types | Descriptions |
|---|---|---|---|---|
| Demographics | 6 | None | No | No |
| Clinical Information | 12 | None | No | No |
| Administrative and Billing Information | 4 | None | No | No |
| Other Documents | 2 | None | No | No |
| **Total** | **24** | **None** | **No** | **No** |

**Demographics** (6 items): Name, Date of birth, Sex, Race and ethnicity, Language preferences, Addresses

**Clinical Information** (12 items): Allergies and adverse reactions; Medications, including prescription history and active medications; Problem list (diagnoses); Immunizations; Family history; Vital signs; Procedures; Surgical history; Lab results; Imaging results; Clinical notes (e.g., progress notes, history and physical, discharge summaries); Care plans

**Administrative and Billing Information** (4 items): Appointments, Insurance details, Insurance claims, Payment history

**Other Documents** (2 items): Forms; Uploaded documents (PDFs) and images (PNGs)

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor claims the export "includes all electronic health information (EHI) that is part of the designated record set." The 4 categories span demographics, clinical data, billing/administrative data, and documents — a reasonable scope statement.

However, the documentation is at such a high level that coverage claims cannot be verified. "Insurance claims" could mean full claim detail with CPT/ICD codes, amounts, and adjudication data — or it could mean a simple list of claim IDs. Without field-level documentation or sample data, it's impossible to assess depth.

**Comparison to product modules**: The product's guides sidebar lists 20+ functional modules. Several modules that store patient-facing data are **not mentioned** in the export documentation:

- **Messaging** (in-app messaging, 2-way SMS, internal notes) — not listed
- **Superbills** (procedure codes, diagnosis codes) — not listed
- **Invoices** — not listed
- **Eligibility checks** (insurance verification data) — not listed
- **Revenue cycle management** (detailed RCM data beyond "insurance claims") — not listed
- **Courses** (patient education content and progress) — not listed
- **Tasks** (clinical task assignments) — not listed
- **Custom fields / Custom objects** (user-defined patient data) — not listed
- **AI Scribe** (transcriptions, AI-generated note drafts) — not listed
- **Implantable device list** (certified under (a)(14)) — not listed
- **Smoking status** — not listed

The vendor's broad claim may cover these via the CSV export, but the documentation does not confirm it.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | 6 items listed (name, DOB, sex, race/ethnicity, language, addresses) | Items listed but no field detail. Missing: contact info (phone, email), emergency contacts, marital status, identifiers (MRN listed in folder naming only). Product stores these (patient portal requires contact info). |
| Encounters / visits | ⚠️ Partial | "Appointments" listed under Administrative | Appointments mentioned, but visit/encounter records (with providers, reasons, durations) are not explicitly described. Product has visit notes and scheduling modules. |
| Problems / conditions / diagnoses | ⚠️ Partial | "Problem list (diagnoses)" listed | Mentioned but no detail on coding system (SNOMED, ICD-10), status, onset dates, etc. |
| Medications / prescriptions | ⚠️ Partial | "Medications, including prescription history and active medications" listed | Mentioned but unclear if full e-prescribing data (pharmacy, fill status, SIG) is included. Product has prescriptions module. |
| Allergies | ⚠️ Partial | "Allergies and adverse reactions" listed | Named but no field detail. |
| Immunizations | ⚠️ Partial | "Immunizations" listed | Named but no field detail. Certified under (h)(1) for registry reporting. |
| Vitals | ⚠️ Partial | "Vital signs" listed | Named but no field detail. |
| Lab results | ⚠️ Partial | "Lab results" listed | Named but no detail on structure (panels, reference ranges, ordering info). Product integrates with 1,000+ labs. |
| Imaging / diagnostic reports | ⚠️ Partial | "Imaging results" listed | Named but no field detail. |
| Procedures | ⚠️ Partial | "Procedures" and "Surgical history" listed | Two separate items named but no field detail. |
| Clinical notes / documents | ⚠️ Partial | "Clinical notes (e.g., progress notes, history and physical, discharge summaries)" listed; PDFs exported | Likely exported as PDF documents rather than structured data. No detail on note types or structure. |
| Care plans / goals | ⚠️ Partial | "Care plans" listed | Named but no field detail. Product has care plan templates module. |
| Orders / referrals | ❌ Not covered | Not mentioned in export documentation | Product supports lab orders, imaging orders, and referring providers. Absence from documentation is a gap. |
| Insurance / coverage | ⚠️ Partial | "Insurance details" listed | Named but no field detail. |
| Claims / billing | ⚠️ Partial | "Insurance claims" listed | Named but unclear scope. Superbills, invoices, eligibility checks, and RCM data are product features not mentioned in export. |
| Payments | ⚠️ Partial | "Payment history" listed | Named but no field detail. Product has patient payments integration. |
| Consents / directives | ❌ Not covered | Not mentioned | Product may store consent via forms module, but not explicitly listed. |
| Patient communications / portal messages | ❌ Not covered | Not mentioned | Product has messaging module (in-app, 2-way SMS) — significant gap if not exported. |
| Family history | ⚠️ Partial | "Family history" listed | Named but no field detail. |

**Summary**: Every listed domain is rated ⚠️ Partial rather than ✅ Covered because the documentation provides only category names with zero field-level detail. It is impossible to confirm actual coverage depth. Three domains with product evidence (orders/referrals, consents, patient communications) are not mentioned at all.

## 6. Documentation Quality

The EHI export documentation is a **single web page with 388 words** of substantive content. It is the thinnest documentation possible that still acknowledges what EHI is and what the export contains.

**What's present**:
- Correct definition of EHI scope (references HIPAA designated record set, excludes psychotherapy notes and litigation materials)
- Clear description of two export mechanisms (single patient and population)
- Export format description (ZIP with CSVs, PDFs, PNGs)
- High-level data category listing (24 items in 4 groups)

**What's absent**:
- No data dictionary or field-level documentation of any kind
- No sample export files or worked examples
- No schema or machine-readable format specification
- No documentation of CSV file names, column headers, or data types
- No relationship documentation (how entities link to each other)
- No value set or code system documentation
- No versioning or changelog

**Could a developer build an import from this documentation?** No. A developer receiving an export ZIP would have to reverse-engineer every CSV file's structure, guess at data types and relationships, and interpret coded values without documentation. The documentation tells you *what topics* are covered but nothing about *how the data is structured*.

**Machine-readable artifacts**: None. The only artifact is an HTML page with prose and bullet lists.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The documentation is too thin to assess actual export content or quality. While the vendor describes a genuine native export mechanism (ZIP with CSVs — not a repackaged FHIR/C-CDA export), the documentation provides only 24 category-level item names with no field-level detail, no schema, and no sample data. It is impossible to determine from the documentation alone what the CSV files actually contain, how many there are, or how they are structured.

### Key Findings

1. **The export mechanism is genuinely native** — a ZIP file with CSV, PDF, and PNG files, separate from the vendor's FHIR/REST API. This is the right approach for (b)(10), but the documentation does not support evaluation of its completeness.

2. **Documentation consists of 388 words on a single web page** — 24 data items listed as bullet points across 4 categories, with zero field-level detail. No data dictionary, no schema, no sample data, no CSV structure documentation.

3. **Population export requires manual vendor involvement** — users must email support@avonhealth.com rather than triggering it through the UI. This suggests the export infrastructure is not fully automated.

4. **Multiple product modules storing patient data are absent from the export documentation** — Messaging, Superbills, Invoices, Eligibility Checks, Custom Fields/Objects, AI Scribe, and Implantable Device List are product features with patient data that are not mentioned in the export categories. The vendor's claim that the export includes "all EHI" may cover these, but the documentation does not confirm it.

5. **The product is early-stage** (certified May 2025, startup founded 2021) — the thin documentation is consistent with a recently certified product that has not yet invested in comprehensive export documentation.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   CSV, PDF, PNG in ZIP archive
Model type:      Appears to be native database export (not standard projection)
Entities:        N/A (no data dictionary; 24 data items listed at category level)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (vendor-assisted via email request)
Domains covered: 0 of 16 confirmed covered; 13 of 16 listed at category level without detail
```

### Bottom Line

Avon Health has built what appears to be a genuine native EHI export (ZIP of CSVs, not a FHIR/C-CDA repackaging), but the documentation is too thin to evaluate. A patient or provider would receive a ZIP file with no schema, no data dictionary, and no documentation of the CSV structure — they would have to reverse-engineer the export to use it. The biggest gap is the complete absence of field-level documentation: 24 bullet points is not a data dictionary.

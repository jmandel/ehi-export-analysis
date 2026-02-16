# EHI Export Analysis: Avon Health

**Product**: Avon EMR 1.0
**Analysis date**: 2026-02-15
**CHPL IDs**: 11636 (15.04.04.3227.Avon.01.00.1.250514)

## 1. Product Context

Avon Health is an early-stage startup (founded 2021, ONC-certified May 2025) building a cloud-based, "AI-first" all-in-one EMR and practice management platform for ambulatory care. The product targets primary care, behavioral health, women's health, pediatrics, geriatrics, hospice, and virtual care practices.

Based on the vendor's own documentation site (guides.avonhealth.com), the product has **18 functional modules** visible in the sidebar navigation: Patient registration, Organization member registration, Scheduling, Messaging, Forms, Tasks, Care plans, Documents, Visit notes, Prescriptions, Labs, Eligibility checks, Invoices, Superbills, Revenue cycle management, Fax, Courses, and Automations.

For assessing export completeness, the key data domains the product stores include:
- **Clinical**: Visit notes, care plans, prescriptions/medications, lab orders and results, allergies, immunizations, vital signs, procedures, clinical documents, imaging orders
- **Patient engagement**: Messaging (in-app, 2-way SMS), forms/intake, patient education courses, patient portal
- **Financial/billing**: Invoices, superbills, insurance eligibility, revenue cycle management, payment collection
- **Administrative**: Scheduling, tasks, fax records, custom fields/objects

The product is also certified for (a)(14) Implantable Device List, (a)(12) Family Health History, and (h)(1) Immunization Registry Reporting, confirming it stores these data types.

## 2. Artifacts Reviewed

| Artifact | Description | Informational Value |
|---|---|---|
| `downloads/ehi-export.html` (52,873 bytes) | Primary EHI export documentation page from guides.avonhealth.com/docs/ehi-export. Contains export mechanism, format description, and data categories. Embedded Next.js markdoc JSON confirms text content. | **Primary artifact** — sole source of export documentation |
| `downloads/ehi-export-page-screenshot.png` (466 KB) | Full-page screenshot of the EHI export documentation page | Confirms HTML content matches rendered page; shows sidebar with all product modules |
| `downloads/certification-page-screenshot.png` (664 KB) | Screenshot of avonhealth.com/meaningful-use ONC certification page | Confirms certification criteria list, links to EHI Export Documentation and API Documentation |
| Live verification: guides.avonhealth.com/docs/ehi-export | Fetched live page on 2026-02-15 | Content identical to collected HTML artifact — no updates since collection |
| Live verification: docs.avonhealth.com/patient | REST API documentation for Patient resource | Shows 24 patient fields with types and descriptions — demonstrates the vendor *has* field-level data model detail but did not include it in EHI export documentation |

**Most informative**: The EHI export HTML page and the sidebar navigation (which inventories all product modules, establishing the baseline for coverage assessment).

**Least informative**: The screenshots confirm but don't add information beyond the HTML.

**Notable absence**: No data dictionary, no sample export files, no schema, no CSV column documentation. The entire EHI export documentation is a single web page with approximately 300 words of substantive content.

## 3. Export Mechanics

- **Format**: ZIP file containing CSV files, PDF documents, and PNG images
- **Mechanism**:
  - *Single patient*: Admin navigates to patient profile → clicks "Export EHI" button (self-service via UI)
  - *Patient population*: Must email support@avonhealth.com with subject "Patient Population b10 Export Request" — handled manually by Avon Support team
- **Single-patient**: Yes, self-service
- **Bulk export**: Yes, but vendor-assisted (manual request via email)
- **Access constraints**: Population export depends on "size of data, time and efforts required to manage the server resources" per documentation. No fees mentioned for the export itself (product is subscription-based).

## 4. Export Content: What's In It

### What the documentation tells us

The export documentation lists **4 data categories** containing **24 named data items**. These are described at a category level only — there are no field names, no data types, no column definitions, no CSV file names, no relationships, and no sample data.

There is **no data dictionary**. The documentation provides zero field-level detail. For example, "Lab results" is listed as an item but there is no information about what columns a lab result CSV would contain, what coding systems are used, or how results link to orders.

### What we can infer about the export format

The export produces CSVs (for structured data), PDFs (for documents), and PNGs (for images). The population export organizes files into per-patient folders named `<FirstName><LastName>_<MRN>`. Beyond this, the documentation provides no information about:
- How many CSV files are generated
- What each CSV file contains
- Column names, data types, or formats
- Relationships between CSV files
- Coded values or value sets

### Vendor's own content organization

The documentation organizes export content into 4 categories with the following items:

| Category (vendor's) | Data Item | Field Count | Types Documented |
|---|---|---|---|
| Demographics | Name | N/A | No |
| Demographics | Date of birth | N/A | No |
| Demographics | Sex | N/A | No |
| Demographics | Race and ethnicity | N/A | No |
| Demographics | Language preferences | N/A | No |
| Demographics | Addresses | N/A | No |
| Clinical Information | Allergies and adverse reactions | N/A | No |
| Clinical Information | Medications, including prescription history and active medications | N/A | No |
| Clinical Information | Problem list (diagnoses) | N/A | No |
| Clinical Information | Immunizations | N/A | No |
| Clinical Information | Family history | N/A | No |
| Clinical Information | Vital signs | N/A | No |
| Clinical Information | Procedures | N/A | No |
| Clinical Information | Surgical history | N/A | No |
| Clinical Information | Lab results | N/A | No |
| Clinical Information | Imaging results | N/A | No |
| Clinical Information | Clinical notes (progress notes, H&P, discharge summaries) | N/A | No |
| Clinical Information | Care plans | N/A | No |
| Administrative and Billing Information | Appointments | N/A | No |
| Administrative and Billing Information | Insurance details | N/A | No |
| Administrative and Billing Information | Insurance claims | N/A | No |
| Administrative and Billing Information | Payment history | N/A | No |
| Other Documents | Forms | N/A | No |
| Other Documents | Uploaded documents (PDFs) and images (PNGs) | N/A | No |

**No field counts are available** — the documentation lists data items at a category level (e.g., "Lab results") without any indication of what fields each item contains. The full inventory is saved to `analysis/export-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into 4 categories:

1. **Demographics** (6 items): Basic patient identity — name, DOB, sex, race/ethnicity, language, addresses. These are category-level labels, not fields, but they align with standard USCDI demographic data elements.

2. **Clinical Information** (12 items): The largest category, covering core clinical data — allergies, medications, problems, immunizations, family history, vitals, procedures, surgical history, labs, imaging, clinical notes, and care plans. This is a reasonable clinical checklist that maps well to USCDI v1 data classes.

3. **Administrative and Billing Information** (4 items): Appointments, insurance details, insurance claims, and payment history. This is the thinnest category relative to the product's billing capabilities.

4. **Other Documents** (2 items): Forms and uploaded documents/images.

**Key observations**:
- The clinical category is relatively complete for a general ambulatory EMR.
- The billing category is thin — the product has dedicated modules for Invoices, Superbills, Eligibility checks, and Revenue cycle management (visible in the sidebar), but the export documentation only mentions "Insurance details," "Insurance claims," and "Payment history." Superbills, invoices, and eligibility data are not mentioned.
- Several product modules have no representation in the export documentation (see gap analysis below).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Listed: Name, DOB, Sex, Race/ethnicity, Language, Addresses | Items listed but no field-level detail. API docs show the patient model has 24+ fields (MRN, SSN, pronouns, gender, sexual orientation, phone, email, status, custom_data, etc.) — unclear if these are all in the export. |
| Encounters / visits | ⚠️ Partial | "Appointments" listed under Administrative; "Clinical notes" listed under Clinical | Appointments are listed but visit/encounter records as a clinical entity are not explicitly mentioned. It's unclear whether encounter-level metadata (providers, diagnoses linked to visit, etc.) is exported. |
| Problems / conditions / diagnoses | ✅ Covered | "Problem list (diagnoses)" listed under Clinical Information | Listed at category level. No detail on coding systems (SNOMED CT is used per product research). |
| Medications / prescriptions | ✅ Covered | "Medications, including prescription history and active medications" listed under Clinical Information | Listed at category level. The product has a dedicated Prescriptions module with e-prescribing integration — unclear if full Rx transaction data (pharmacy, fill status, sig) is included or just a medication list. |
| Allergies | ✅ Covered | "Allergies and adverse reactions" listed under Clinical Information | Listed at category level. |
| Immunizations | ✅ Covered | "Immunizations" listed under Clinical Information | Listed at category level. Product is certified for (h)(1) Immunization Registry Reporting. |
| Vitals | ✅ Covered | "Vital signs" listed under Clinical Information | Listed at category level. |
| Lab results | ✅ Covered | "Lab results" listed under Clinical Information | Listed at category level. Product integrates with 1000+ labs per product research. |
| Imaging / diagnostic reports | ✅ Covered | "Imaging results" listed under Clinical Information | Listed at category level. |
| Procedures | ✅ Covered | "Procedures" and "Surgical history" listed under Clinical Information | Two separate items cover this domain. |
| Clinical notes / documents | ✅ Covered | "Clinical notes (e.g., progress notes, history and physical, discharge summaries)" and "Uploaded documents (PDFs) and images (PNGs)" | Notes and documents both listed. Visit notes are a major product module. |
| Care plans / goals | ✅ Covered | "Care plans" listed under Clinical Information | Product has a dedicated Care plans module and is certified for (b)(11). |
| Orders / referrals | ❌ Not covered | No mention of orders or referrals in export | Product supports lab orders and imaging orders. Order data is not explicitly listed in the export. Potential gap. |
| Insurance / coverage | ✅ Covered | "Insurance details" listed under Administrative and Billing | Listed at category level. |
| Claims / billing | ⚠️ Partial | "Insurance claims" and "Payment history" listed | Product has Invoices, Superbills, Eligibility checks, and Revenue cycle management modules — none explicitly mentioned in export. "Insurance claims" may partially cover this, but superbill-level detail (CPT/ICD codes, modifiers) and invoice data are not mentioned. |
| Payments | ✅ Covered | "Payment history" listed under Administrative and Billing | Listed at category level. |
| Consents / directives | ❌ Not covered | No mention in export | Unclear if the product stores advance directives. Not a confirmed gap since the product doesn't appear to have a dedicated consents module. |
| Patient communications / portal messages | ❌ Not covered | No mention of messages in export | Product has a dedicated Messaging module (in-app, 2-way SMS, internal notes). This is a **significant gap** — patient messages are part of the designated record set. |
| Specialty-specific data | N/A | No specialty-specific items in export | Product claims to serve behavioral health, women's health, pediatrics, etc. but does not appear to have specialty-specific clinical templates or assessments documented in the guides. Custom fields may serve this purpose but are not mentioned in export. |
| Family history | ✅ Covered | "Family history" listed under Clinical Information | Product is certified for (a)(12) Family Health History. |
| Implantable devices | ❌ Not covered | No mention in export | Product is certified for (a)(14) Implantable Device List. This data type should be in the export. Gap. |
| Custom fields/objects | ❌ Not covered | No mention in export | Product supports custom fields and custom objects (visible in guides sidebar under "Extensions"). API docs confirm `custom_data` field on patients. If used clinically, this is EHI. |

## 6. Documentation Quality

The EHI export documentation is **minimal**. It consists of a single web page (~300 words of substantive content) that provides:

**What it does well**:
- Correctly defines EHI scope (cites designated record set, HIPAA, exclusions)
- Clearly describes two export types (single patient, population)
- Specifies the export format (ZIP with CSVs, PDFs, PNGs)
- Lists data categories at a high level

**What it lacks**:
- **No data dictionary**: Zero field-level documentation. No column names, no data types, no descriptions.
- **No sample data**: No example CSV files, no sample export output.
- **No schema**: No machine-readable format specification (no JSON Schema, XSD, DDL, etc.).
- **No CSV documentation**: No information about how many CSV files are generated, what each contains, or how they relate.
- **No value sets**: No coded value documentation despite the product using SNOMED CT and CDC code sets (per API docs).
- **No relationship documentation**: No description of how entities link together.
- **No screenshots**: No visual documentation of the export interface or output.

**Could a developer build an import?** No. A developer receiving this export would get a ZIP file with CSV files and would need to reverse-engineer the column structure, data types, relationships, and coded values entirely from the data itself. The documentation provides no technical guidance.

**Contrast with API documentation**: The vendor's REST API docs at docs.avonhealth.com include field-level detail for at least the Patient resource (24+ fields with names, types, descriptions, and value sets). This demonstrates the vendor has the capability to document their data model but chose not to for the (b)(10) export.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The documentation is too thin to assess what is actually exported. The vendor lists 24 data items across 4 categories at a category level only, with no field-level detail, no sample data, no schema, and no CSV column documentation. While the export mechanism itself (ZIP with CSVs) suggests a potentially genuine native data export rather than a C-CDA/FHIR repackaging, the documentation provides insufficient detail to verify what the export actually contains or how complete it is.

### Key Findings

1. **No data dictionary or field-level documentation exists.** The entire EHI export documentation is a single web page listing 24 data items by name (e.g., "Lab results," "Medications") with zero field-level detail. This is among the thinnest documentation possible while still being a documentation page. (Source: `downloads/ehi-export.html`)

2. **The export format is genuinely native, not a C-CDA/FHIR repackaging.** The export produces a ZIP with CSV files, PDFs, and PNGs — this is clearly distinct from the vendor's (g)(10) FHIR API and C-CDA endpoint (available at `/v2/patients/:id/ccda`). This is a positive signal that the vendor has built a separate (b)(10) mechanism. (Source: `downloads/ehi-export.html`, `downloads/certification-page-screenshot.png`)

3. **Patient messaging data is absent from the export despite being a core product module.** The product has a dedicated Messaging module supporting in-app, 2-way SMS, and internal notes — all visible in the sidebar navigation. Messages between patients and care teams are EHI (part of the designated record set). None are mentioned in the export. (Source: `downloads/ehi-export-page-screenshot.png` sidebar, `downloads/ehi-export.html`)

4. **Billing coverage is thin relative to the product's financial capabilities.** The product has 5 billing/financial modules (Invoices, Superbills, Eligibility checks, Revenue cycle management, Payment collection) but the export lists only 3 generic items: "Insurance details," "Insurance claims," and "Payment history." Superbills, invoices, and eligibility data are not mentioned. (Source: `downloads/ehi-export.html`, `downloads/ehi-export-page-screenshot.png` sidebar)

5. **Population export requires manual vendor assistance.** Bulk export is not self-service — it requires emailing support@avonhealth.com and is described as depending on "size of data, time and efforts required to manage the server resources." This suggests incomplete automation of the export infrastructure. (Source: `downloads/ehi-export.html`)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   ZIP containing CSV, PDF, PNG
Model type:      Appears native (CSV-based), but undocumented
Entities:        N/A (no data dictionary; 24 data items listed at category level)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A (no fields documented)
Sample data:     No
Bulk export:     Yes (vendor-assisted via email request)
Domains covered: 11 of 17 applicable domains listed, but without field-level detail
                 to verify actual coverage
```

### Bottom Line

Avon Health has built a separate (b)(10) export mechanism (ZIP with CSVs) rather than repackaging their FHIR/C-CDA output, which is a positive design choice. However, the documentation is a single page listing data categories with no field-level detail, no sample data, and no schema — making it impossible to verify what is actually exported or to programmatically consume the export. The biggest gaps are the complete absence of a data dictionary and the omission of patient messaging data and detailed billing data from the documented export categories.

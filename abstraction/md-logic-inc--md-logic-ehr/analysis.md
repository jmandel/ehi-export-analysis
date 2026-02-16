# EHI Export Analysis: MD Logic, Inc.

**Product**: MD Logic EHR
**Analysis date**: 2026-02-16
**CHPL IDs**: 11056 (v7.2, certified 2022-12-07), 11403 (v8.0, certified 2023-12-06)

## 1. Product Context

MD Logic EHR is a comprehensive ambulatory EHR with tightly integrated Practice Management (PM) and Revenue Cycle Management (RCM), targeting physician-owned independent practices across 25+ medical and surgical specialties. The product suite stores:

- **Clinical data**: Patient charts, clinical progress notes, customizable specialty-specific documentation, medical histories, problem lists, allergies, immunizations (implied by (a)(1)–(a)(3) certification)
- **Medication data**: Electronic prescriptions (47M generated per vendor statistics), refill requests, drug-allergy and drug-drug interaction data
- **Lab data**: Bi-directional lab interfaces, electronic lab results with trending/graphing
- **Imaging**: PACS module for image storage; clinical/surgical photo capture via smartphone app
- **Billing/financial data**: CPT/DX codes automatically generated from clinical documentation, insurance claims, EOB payments, claim status, patient statements, clearinghouse integration, insurance eligibility verification
- **Patient-entered data**: Medical histories, consent forms via patient kiosk and eForms
- **Communication data**: Provider-to-staff electronic messaging, orders sent remotely

This is a product that stores extensive structured clinical *and* billing data across its integrated EHR/PM/RCM suite. The export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | File | Size | What It Tells You |
|---|---|---|---|
| B10 Export Documentation page | `downloads/b10-export-documentation.html` | 66,222 bytes | **Primary artifact.** The entire EHI export documentation: 8 paragraphs of prose (~180 words) and 2 embedded JSON schemas. No data dictionary, no sample data, no downloadable files. |
| Per-patient manifest schema | `downloads/patient-manifest-schema.json` | 1,309 bytes | JSON Schema describing the `manifest.json` inside each patient's ZIP export. 4 fields: document description, filename, file type, date created. |
| Bulk export manifest schema | `downloads/bulk-export-manifest-schema.json` | 2,196 bytes | JSON Schema describing the top-level manifest for bulk (all-patient) exports. 11 defined fields (12 required — schema has bugs): patient demographics + ZIP file reference. |
| Page screenshot | `downloads/b10-page-screenshot.png` | 413,886 bytes | Visual confirmation of page layout. Shows header, prose, two dark-themed scrollable code blocks with schemas, and sidebar navigation. |

**Most informative**: The HTML page itself — it is the only source of information about how the export works. **Least informative**: The screenshot, which simply confirms the page layout already visible in the HTML source.

**Verified against live site**: The page at `https://www.mdlogic.com/solutions/b10-export-documentation` was fetched live on 2026-02-16 and confirmed to be identical to the downloaded artifact. No changes since collection.

## 3. Export Mechanics

- **Format**: ZIP file(s) containing individual document files (PDF, Word, JPEG, C-CDA XML) plus a `manifest.json` index file.
- **Mechanism**: User requests data for a patient; MD Logic sends an email with a direct download link to a page where the ZIP can be downloaded. For bulk export of all patients, the user must "contact mdlogic support" because "this can be an extremely large amount of data, special arrangements will need to be made to deliver the data."
- **Single-patient**: Yes — email-based download link.
- **Bulk**: Vendor-assisted only — requires contacting support.
- **Access constraints**: The mandatory disclosures page (`/solutions/meaningful-use`) states: *"Data Export: MD Logic will charge a fee to export health data out of the MD Logic EHR software in the event the customer requires data to transfer to another EHR."* No fee amount is specified.

## 4. Export Content: What's In It

### What the export actually contains

The export is a **document dump**, not a structured data export. Each patient receives a ZIP file containing the documents stored in their chart as individual files. The manifest describes the container, not the clinical data:

**Per-patient manifest**: 4 fields describing each document file:

| Field | Type | Examples | Purpose |
|---|---|---|---|
| `Descripton` [sic] | string | "MRI Spine", "MRI Hip", "Registration Form", "Progress Notes" | Free-text document description |
| `FileName` | string | "testFile_51.pdf", "testFile_3305.xml" | File name within the ZIP |
| `FileType` | string | "Word", "PDF", "CCDA", "JPEG" | Document format label |
| `DateCreated` | string | "8/25/2020" | Date in M/D/YYYY format |

**Bulk export manifest**: 11 defined fields (demographics + ZIP reference):

| Field | Type | Examples | Purpose |
|---|---|---|---|
| `FirstName` | string | "John", "Jane" | Patient first name |
| `LastName` | string | "Doe" | Patient last name |
| `MiddleName` | string | "Q", "James" | Patient middle name |
| `Suffix` | string | "Jr", "Sr", "III" | Name suffix |
| `Address1` | string | "143 Main Street" | Street address |
| `Address2` | string | "Suite 100" | Address line 2 |
| `City` | string | "Atlanta", "Houston" | City |
| `State` | string | "GA", "TX", "NY" | State code |
| `Zip` | string | "30097" | ZIP code |
| `DOB` | string | "01/01/1980" | Date of birth (MM/DD/YYYY) |
| `PatientFileName` | string | "5125.zip" | Reference to patient's ZIP file |

**Note**: `Gender` is listed as required in the schema but has no property definition (schema bug). `Address` is listed as required but the property is named `Address1` (name mismatch).

### What's NOT in the export

There is **no structured clinical data export**. The export contains documents (PDFs, Word files, images, C-CDA XML files) — not the discrete, structured data stored in the EHR's database. Specifically absent:

- No data dictionary of any kind
- No structured tables for medications, lab results, diagnoses, vitals, allergies, immunizations, or any other clinical domain
- No billing or claims data
- No insurance/coverage data
- No structured encounter records
- No orders, referrals, or care plans
- No patient communications or portal messages

The C-CDA XML files mentioned as a possible `FileType` would contain some structured clinical data (problems, medications, allergies, etc.) in standard C-CDA format, but these would be clinical summaries — not the full breadth of data stored in the EHR database.

### Vendor's own content organization

The vendor does not organize the export into data categories. The entire documentation describes only two schemas — a document index (4 fields) and a patient index (11 fields). There is no categorization of clinical, billing, or other data domains.

| Entity/Schema | Fields Defined | Fields with Descriptions | Types Documented | Category |
|---|---|---|---|---|
| Per-patient manifest | 4 | 0 (auto-generated titles only) | Yes (all string) | Document index |
| Bulk export manifest | 11 | 0 (auto-generated titles only) | Yes (all string) | Patient index |
| **Total** | **15** | **0** | **15** | — |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export covers exactly two things:

1. **A collection of document files** stored in each patient's chart (PDFs, Word docs, images, C-CDA XML). The types of documents that might be included can be inferred from the `Descripton` examples ("MRI Spine", "MRI Hip", "Registration Form", "Progress Notes") and `FileType` examples ("Word", "PDF", "CCDA", "JPEG"), but there is no exhaustive list or any documentation of which document types are generated.

2. **Basic patient demographics** in the bulk export manifest only (name, address, DOB). This is index-level data to match patients to their ZIP files — not a structured demographics export.

The export documentation says nothing about what clinical data is captured in the documents. A "Progress Notes" PDF likely contains clinical observations, but the structure, completeness, and fidelity of that rendering are undocumented. There is no indication that discrete lab values, medication lists, problem lists, vital signs, or billing records are exported in any structured form.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Bulk manifest has name, address, DOB, gender (bugged). No phone, email, race, ethnicity, language, SSN, or other demographic fields. | Product stores full demographics (patient kiosk intake); only basic name/address in export index. |
| Encounters / visits | ❌ Not covered | No encounter data in export schemas | Product tracks visits (Command Center, scheduling); not in export. |
| Problems / conditions / diagnoses | ❌ Not covered | No structured problem list. May exist in C-CDA documents if included. | Product certified for (a)(1) CPOE diagnoses; structured data not exported. |
| Medications / prescriptions | ❌ Not covered | No structured medication data. May exist in C-CDA documents if included. | Product has generated 47M prescriptions; major gap. |
| Allergies | ❌ Not covered | No structured allergy data. May exist in C-CDA if included. | Certified for (a)(3); not in export. |
| Immunizations | ❌ Not covered | No structured immunization data. | Certified for (a)(3); not in export. |
| Vitals | ❌ Not covered | No structured vital signs. | Product stores vitals (implied by clinical charting); not in export. |
| Lab results | ❌ Not covered | No structured lab data. | eLabs module has bi-directional interfaces, trending, graphing; major gap. |
| Imaging / diagnostic reports | ⚠️ Partial | JPEG files and "MRI Spine"/"MRI Hip" descriptions suggest imaging documents are exported as files. | PACS module stores images; some may be included as document files but no structured metadata. |
| Procedures | ❌ Not covered | No procedure data in export. | Product likely stores procedures (surgical specialties); not in export. |
| Clinical notes / documents | ⚠️ Partial | "Progress Notes" in manifest examples; PDF/Word documents exported. | Notes likely exported as rendered documents (PDFs), losing structured data within them. |
| Care plans / goals | ❌ Not covered | No care plan data in export. | No evidence product stores these extensively; likely N/A or minor gap. |
| Orders / referrals | ❌ Not covered | No order data in export. | Command Center handles ancillary orders (x-rays, EKGs, labs); not in export. |
| Insurance / coverage | ❌ Not covered | No insurance data in export. | PM module handles insurance eligibility verification; gap. |
| Claims / billing | ❌ Not covered | No billing data in export at all. | PM module handles claims, EOBs, charge entry, clearinghouse integration; **major gap**. |
| Payments | ❌ Not covered | No payment data in export. | PM handles EOB payment posting, patient statements; gap. |
| Consents / directives | ⚠️ Partial | "Registration Form" in manifest examples suggests consent/intake forms may be exported as document files. | Patient kiosk captures consent forms; may be included as PDFs. |
| Patient communications | ❌ Not covered | No messaging data in export. | Smartphone app supports provider-team messaging; gap if patient-facing messages exist. |
| Specialty-specific data | ❌ Not covered | No specialty clinical data structures. | Product supports 25+ specialties with customizable documentation; significant gap. |

**Summary**: Of 18 applicable domains, 0 are fully covered, 4 are partially covered (via document files only), and 14 are not covered at all.

## 6. Documentation Quality

The export documentation is **extremely thin** — among the thinnest possible while still being non-empty.

- **Total prose**: 8 paragraphs, approximately 180 words (verified by script: `analysis/compute_prose_stats.py`)
- **Data dictionary**: None. The two JSON schemas describe the manifest/index format, not the clinical data being exported.
- **Field descriptions**: Zero. The JSON schema "titles" are auto-generated (e.g., "The Descripton Schema") and provide no semantic information.
- **Value sets / code systems**: None. The `FileType` and `Descripton` fields have a few examples but no exhaustive enumeration.
- **Relationships / foreign keys**: The only relationship is `PatientFileName` linking a patient to their ZIP file.
- **Sample data**: None provided.
- **Machine-readable schemas**: The two JSON schemas are machine-readable but describe only the manifest container, not the clinical content.
- **Spelling errors**: 3 found — "Descripton" (field name), "recive" (prose), "Allong" (prose) — suggesting minimal review.
- **Schema bugs**: `Gender` is required but undefined; `Address` vs `Address1` name mismatch; trailing comma in `FirstName` examples (invalid JSON).

**Could a developer build an import from this documentation?** A developer could parse the manifest JSON and extract individual files from the ZIP. However, they would have no programmatic way to interpret the heterogeneous document collection — each PDF, Word doc, or image would require format-specific handling with no documentation of what clinical content appears in which document type. The export is essentially an opaque file dump with a minimal file index.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation describes a document-file dump with a simple manifest index. There is no data dictionary, no structured data export, no coverage of billing or discrete clinical data. The export covers only documents stored in the patient's chart — not the structured clinical, medication, lab, or billing data that the product stores in its database. The 15 total fields across both schemas are manifest metadata, not clinical data fields.

### Key Findings

1. **The export is a document dump, not a data export.** Patients receive ZIP files of their chart documents (PDFs, Word docs, images, C-CDA files) indexed by a 4-field JSON manifest. No structured clinical data — lab values, medication lists, coded diagnoses, vitals — is exported in discrete form. (Source: `downloads/patient-manifest-schema.json`, `downloads/b10-export-documentation.html`)

2. **Billing and practice management data is entirely absent.** Despite MD Logic's tightly integrated PM/RCM suite handling claims, EOBs, charge entry, insurance verification, and patient statements, zero billing or financial data appears in the export documentation. (Source: absence from `downloads/b10-export-documentation.html`; PM capabilities confirmed on vendor website)

3. **Documentation is among the thinnest reviewed.** The entire (b)(10) documentation is ~180 words of prose and two JSON schemas totaling 15 fields — all describing the manifest container, none describing clinical content. No data dictionary, no sample data, no field definitions. (Source: `analysis/compute_prose_stats.py`, `analysis/full-entity-inventory.json`)

4. **Bulk export requires contacting vendor support and incurs a fee.** The mandatory disclosures page states MD Logic "will charge a fee to export health data." Bulk export requires special arrangements. (Source: `https://www.mdlogic.com/solutions/meaningful-use`, verified live 2026-02-16)

5. **The JSON schemas contain multiple bugs suggesting minimal maintenance.** Field name typo ("Descripton"), required/property name mismatch ("Address" vs "Address1"), missing property definition (Gender), invalid JSON (trailing comma). (Source: `downloads/bulk-export-manifest-schema.json`, `downloads/patient-manifest-schema.json`)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   ZIP of document files (PDF, Word, JPEG, C-CDA XML) + JSON manifest
Model type:      Document dump (not a data model)
Entities:        2 (manifest schemas only — no clinical data entities)
Fields:          15 (manifest metadata only — 4 per-patient + 11 bulk index)
Descriptions:    0% (0 of 15 fields have meaningful descriptions)
Sample data:     No
Bulk export:     Vendor-assisted only (contact support; fee charged)
Domains covered: 0 of 18 fully; 4 of 18 partially (via document files)
```

### Bottom Line

A patient or provider requesting their data from MD Logic EHR would receive a ZIP of chart documents (PDFs, images, possibly C-CDA summaries) — but not the structured clinical data (medications, lab results, diagnoses, vitals) or billing data that the product stores in its database. This is a document-file dump dressed as an EHI export, with no data dictionary and no evidence that the full designated record set — particularly billing/claims data from the integrated PM/RCM system — is included. The single biggest gap is the complete absence of structured data export for a product that stores extensive discrete clinical and financial data.

# EHI Export Analysis: MD Logic, Inc.

**Product**: MD Logic EHR
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2785.MDLo.07.02.1.221207 (v7.2), 15.04.04.2785.MDLo.08.03.1.231206 (v8.0)

## 1. Product Context

MD Logic EHR is an ambulatory electronic health record system from MD Logic, Inc. (Lawrenceville, GA), targeting independent physician practices across 25+ medical and surgical specialties. The product is sold as an integrated suite comprising:

- **EHR**: Clinical charting, progress notes, specialty-specific documentation, problem lists, medications, allergies, immunizations, vitals, lab integration (eLabs), imaging (PACS), e-prescribing (eRx), patient kiosk, eForms, patient portal, barcode document scanning
- **Practice Management (PM)**: Scheduling, insurance eligibility, automated charge entry (CPT/DX from EHR), electronic claims, EOB posting, patient statements, collections
- **Revenue Cycle Management (RCM)**: Managed billing services

The vendor reports 20 million patient visits, 47 million prescriptions, and 125 million clinical documents managed. The product stores structured clinical data (diagnoses, meds, labs, vitals, allergies, immunizations), billing/financial data (claims, charges, EOBs, payments), patient-entered forms, scanned documents, clinical photos, and provider communications. This is a feature-rich ambulatory EHR+PM platform, so a genuine (b)(10) export should cover all of these data domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/b10-export-documentation.html` (66,222 bytes) | Full HTML source of the vendor's sole (b)(10) documentation page. Contains ~150 words of prose and two embedded JSON schemas. | **Primary source** — this is the entire documentation |
| `downloads/patient-manifest-schema.json` (1,309 bytes) | Extracted JSON Schema for the per-patient manifest.json file. 4 fields: Descripton, FileName, FileType, DateCreated | Moderately informative — shows export is document-centric |
| `downloads/bulk-export-manifest-schema.json` (2,196 bytes) | Extracted JSON Schema for the bulk export manifest. 11 demographic fields + PatientFileName reference | Moderately informative — confirms only demographics in manifest |
| `downloads/b10-page-screenshot.png` (414 KB) | Full-page screenshot of the documentation page | Confirms page layout; no hidden content |

**No data dictionary, no sample export data, no additional documentation files exist.** The entire (b)(10) documentation is a single HTML page.

## 3. Export Mechanics

- **Format**: ZIP file per patient containing documents (PDF, Word, JPEG, C-CDA XML) plus a `manifest.json` index file
- **Mechanism**: Email-based delivery. User requests patient data; vendor emails a download link. For bulk (all-patient) export, user must "contact mdlogic support" for "special arrangements."
- **Single-patient**: Yes, via email link
- **Bulk**: Available but requires vendor assistance; described as potentially "an extremely large amount of data"
- **Access constraints**: Bulk export requires contacting vendor support. The vendor's mandatory disclosures page states: "MD Logic will charge a fee to export health data out of the MD Logic EHR software in the event the customer requires data to transfer to another EHR."

## 4. Export Content: What's In It

The export is a **document dump**, not a structured data export. Each patient's ZIP file contains the documents stored in their chart (PDFs, Word files, JPEGs, C-CDA XML files) plus a `manifest.json` that indexes them.

### What the manifest schemas tell us

**Per-patient manifest** (4 fields):

| Field | Type | Description | Examples |
|---|---|---|---|
| `Descripton` [sic] | string | Document description | "MRI Spine", "MRI Hip", "Registration Form", "Progress Notes" |
| `FileName` | string | File name | "testFile_51.pdf", "testFile_3305.doc", "testFile_3305.xml" |
| `FileType` | string | File format | "Word", "PDF", "CCDA", "JPEG" |
| `DateCreated` | string | Creation date (M/D/YYYY) | "8/25/2020" |

**Bulk export manifest** (12 fields):

| Field | Type | Required | Examples |
|---|---|---|---|
| `FirstName` | string | Yes | "John", "Jane" |
| `LastName` | string | Yes | "Doe" |
| `MiddleName` | string | Yes | "Q", "James" |
| `Suffix` | string | Yes | "Jr", "Sr", "III" |
| `Address1` | string | Yes* | "143 Main Street" |
| `Address2` | string | Yes | "Suite 100" |
| `City` | string | Yes | "Atlanta", "Houston" |
| `State` | string | Yes | "GA", "TX", "NY" |
| `Zip` | string | Yes | "30097" |
| `Gender` | — | Yes* | (no property definition) |
| `DOB` | string | Yes | "01/01/1980" |
| `PatientFileName` | string | Yes | "5125.zip" |

\* Schema bugs: `required` lists "Address" but property is "Address1"; `Gender` is required but has no property definition.

### Vendor's own content organization

The vendor does not organize content into categories. The entire export consists of two schema objects:

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| per_patient_manifest | 4 | 4 | Yes | Export Manifest |
| bulk_export_manifest | 11 | 10 (Gender missing) | Yes | Export Manifest |
| **Total** | **15** | **14** | | |

There is **no data dictionary** for the exported documents themselves. The manifest describes metadata *about* the documents (name, type, date) but nothing about the clinical or structured content within them.

### What's actually in the ZIP files

Based on the schema examples and file type list, the patient ZIP contains:
- **PDF files**: Likely clinical documents, imaging reports, forms
- **Word documents**: Possibly letter templates, reports
- **JPEG images**: Possibly clinical photos, scanned documents
- **C-CDA XML files**: Clinical summary documents in standard format

The C-CDA files would contain structured USCDI-equivalent data (demographics, problems, medications, allergies, vitals, labs, procedures, immunizations) in C-CDA format. However, the export does not document which C-CDA templates are used, what sections are included, or whether the C-CDA covers the full breadth of structured data in the EHR.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export documentation describes a single mechanism: exporting the documents stored in a patient's chart as files in a ZIP. The manifest provides only document-level metadata (description, filename, filetype, date). The bulk manifest adds basic demographics for patient identification.

There is **no evidence of structured data export** for any clinical domain. The export relies entirely on whatever documents happen to be in the patient's chart — if a progress note was saved as a PDF, it's in the ZIP. If a C-CDA was generated, it's in the ZIP. But the underlying structured data (discrete medication records, lab result values, allergy codes, vital sign measurements, billing records, insurance information) is not exported in any queryable or structured form.

The documentation is extraordinarily thin: approximately 150 words of prose describing the process, plus two JSON schemas totaling 15 fields. No data dictionary. No sample data. No description of what document types are guaranteed to be included.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Bulk manifest has 11 demographic fields (name, address, gender, DOB). No phone, email, race, ethnicity, language, marital status, or emergency contacts. | Product stores full demographics; only basic identifiers exported in manifest |
| Encounters / visits | ❌ Not covered | No encounter data in export | Product tracks visits (Command Center); gap |
| Problems / conditions | ❌ Not covered | No structured problem list export | Product certified for (a)(1) CPOE/problem list; significant gap |
| Medications / prescriptions | ❌ Not covered | No structured medication data | Product has eRx module (47M prescriptions); significant gap |
| Allergies | ❌ Not covered | No structured allergy data | Product certified for (a)(3); gap |
| Immunizations | ❌ Not covered | No structured immunization data | Implied by certification criteria; gap |
| Vitals | ❌ Not covered | No structured vital signs | Standard EHR feature; gap |
| Lab results | ❌ Not covered | No structured lab data | Product has eLabs with bi-directional interfaces; significant gap |
| Imaging / diagnostic reports | ⚠️ Partial | Manifest examples include "MRI Spine", "MRI Hip" as document descriptions; JPEG file type listed | Images may be exported as files but no structured report data |
| Procedures | ❌ Not covered | No structured procedure data | Implied by surgical specialties served; gap |
| Clinical notes / documents | ⚠️ Partial | "Progress Notes" listed as manifest example; PDF/Word files exported | Document files exported but no guarantee of completeness; no structured note data |
| Care plans / goals | ❌ Not covered | No mention | May not be a major feature; uncertain |
| Orders / referrals | ❌ Not covered | No structured order data | Command Center describes ancillary orders; gap |
| Insurance / coverage | ❌ Not covered | No insurance data in export | PM module handles eligibility verification; gap |
| Claims / billing | ❌ Not covered | No billing data | PM module handles claims, charges, EOBs, payments; significant gap |
| Payments | ❌ Not covered | No payment data | PM module handles payments, patient statements; gap |
| Consents / directives | ⚠️ Partial | "Registration Form" in manifest examples; eForms module implies consent forms | May be exported as document files if stored as PDFs |
| Patient communications | ❌ Not covered | No messaging or communication data | Smartphone app describes provider messaging; gap |
| Specialty-specific data | ❌ Not covered | No specialty clinical data | Product serves 25+ specialties with specialty knowledgebases; gap |

**Summary**: Of 19 applicable domains, 0 are fully covered, 4 are partially covered (only as document files, not structured data), and 15 are not covered at all.

## 6. Documentation Quality

The documentation is among the thinnest possible for a certified (b)(10) export:

- **Total documentation**: A single HTML page with ~150 words of prose and two JSON schemas (15 fields total)
- **No data dictionary**: There is no description of what data is actually exported — no field definitions, no entity lists, no schema for the clinical content
- **No sample data**: No example exports provided
- **No machine-readable artifacts**: The two JSON schemas describe only manifest metadata, not clinical content
- **Schema quality issues**: The schemas contain bugs (field name mismatches in `required` vs `properties`, missing `Gender` property definition, typo in `Descripton`)
- **No import guidance**: A developer receiving this export would have no documentation to work from beyond the manifest structure

A developer could not build an import system from this documentation. They would receive a ZIP of heterogeneous document files (PDF, Word, JPEG, C-CDA) with a 4-field manifest, and would have to reverse-engineer the content of each file type.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export documentation describes only a document file dump with no structured data export. MD Logic EHR is a comprehensive ambulatory EHR+PM platform storing structured clinical data across numerous domains (medications, labs, vitals, allergies, billing, insurance, orders, etc.), yet the documented export contains none of this structured data. The only structured elements are a 4-field document manifest and an 11-field demographic index. Even the document export is undocumented — there's no specification of which document types are included or guaranteed. The possible inclusion of C-CDA files (listed as a FileType) would provide some USCDI-scope clinical data, but this is not documented or described.

**Axis 2 — Export approach: Unclear/undetermined**

The export mechanism (ZIP of document files delivered via email link) is unique to (b)(10) — it's not a repackaging of the g(10) FHIR API or C-CDA exchange. However, it's not a purpose-built structured EHI export either. It appears to be a simple file dump of whatever documents are stored in the patient's chart, with no effort to export the structured clinical and billing data that constitutes the majority of the EHR's designated record set. The inclusion of C-CDA as a file type suggests some C-CDA documents may be generated and included, but this is not documented. The approach is best characterized as a minimal document export that may or may not include clinical summaries.

### Key Findings

1. **Entire (b)(10) documentation is ~150 words of prose and 15 manifest fields.** There is no data dictionary, no sample data, no schema for clinical content. This is one of the thinnest (b)(10) documentation sets possible for a certified product. (Source: `downloads/b10-export-documentation.html`)

2. **Export is document-centric, not data-centric.** The export delivers files (PDFs, Word docs, JPEGs, possibly C-CDAs) stored in the patient chart, not structured clinical data. Discrete data elements (lab values, medication records, vital measurements, allergy codes, billing records) are not exported in any queryable form. (Source: `downloads/patient-manifest-schema.json`)

3. **No billing or financial data in the export.** Despite MD Logic offering a full Practice Management module with claims, charges, EOBs, payments, and patient statements, none of this data appears in the (b)(10) export. (Source: comparison of `product-research.md` capabilities vs. export documentation)

4. **Bulk export requires vendor contact and may incur fees.** The documentation states users must "contact mdlogic support" for bulk export, and the mandatory disclosures page indicates a fee may be charged for data export. (Source: `downloads/b10-export-documentation.html`)

5. **JSON schemas contain bugs.** The bulk manifest schema has a field name mismatch (`required` lists "Address" but property is "Address1"), a missing `Gender` property definition, and placeholder `$id` values. The per-patient manifest has a typo (`Descripton`). These suggest minimal QA effort. (Source: `downloads/bulk-export-manifest-schema.json`, `downloads/patient-manifest-schema.json`)

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined
Export format:   ZIP (document files: PDF, Word, JPEG, C-CDA) + JSON manifest
Entities:        2 (manifest schemas only; no clinical data dictionary)
Fields:          15 (4 per-patient manifest + 11 bulk manifest)
Descriptions:    93% of manifest fields (14/15) — but no clinical content documented
Sample data:     No
Bulk export:     Yes (vendor-assisted, potentially fee-based)
Domains covered: 0 of 19 fully; 4 of 19 partially (as document files only)
```

### Bottom Line

MD Logic's (b)(10) export is a document file dump with no structured data export and no data dictionary. A patient or provider would receive a ZIP of whatever PDFs, Word documents, and images happen to be in the chart — but none of the discrete clinical data (medications, lab results, vitals, allergies, diagnoses) or billing data that constitutes the bulk of the EHR's designated record set. The single biggest gap is the complete absence of structured data export from a product that stores extensive structured clinical and billing information.

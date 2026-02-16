# EHI Export Analysis: Sequel Systems, Inc.

**Product**: SequelMed EHR V12
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2846.Sequ.12.01.1.221227

## 1. Product Context

SequelMed EHR is an integrated EHR + Practice Management platform from Sequel Systems, Inc. (Melville, NY), targeting ambulatory physician practices across 24+ specialties. The product combines clinical EHR, practice management, document management, and medical billing into a single platform. It is a small-vendor product (pricing from ~$148/month, minimal market footprint based on 7–9 third-party reviews).

Key data domains the product stores, per vendor materials:
- **Clinical**: Demographics, problem lists, medications, allergies, immunizations, vital signs, clinical notes via specialty-specific templates, lab/imaging orders and results, e-prescribing (SureScripts), clinical decision support
- **Financial/billing**: Claims, charges, payments, patient A/R, collections, denials management, eligibility verification, claim scrubbing, revenue cycle management
- **Administrative**: Scheduling, document management (scanning/archiving), multi-office coordination, enterprise reporting
- **Patient engagement**: Patient portal (via Data Motion), online registration, secure messaging
- **Interoperability**: HL7 interfaces, DICOM imaging, C-CDA transitions of care, FHIR APIs

The product is certified for 170.315(b)(10) (EHI export) along with a broad set of clinical and interoperability criteria. The combined EHR+PM nature means a genuine (b)(10) export should cover both clinical and financial data domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/SequelMed-EHR-B10-Electronic-Health-Information-Export.pdf` | 4-page PDF (96,891 bytes, created 2023-11-22). The entire EHI export documentation. ~1.5 pages of actual content after cover page. Describes export as ZIP per patient containing C-CDA XML, document files, and an undocumented XLS file. | **Primary source** — but extremely thin |
| `downloads/data-export-page-screenshot.png` | Screenshot of vendor's data export landing page at `sequelmed.com/data-export/`. Shows a single link to the PDF. | Confirms no additional documentation exists on the site |
| `files.json` | Manifest of collected artifacts. Confirms only 2 files were available. | Orientation |
| `metadata.json` | CHPL certification details. Confirms (b)(10) certification and broad certified criteria. | Context |
| `product-research.md` | Research on product capabilities. Establishes baseline of what the product stores. | Critical for gap analysis |

No data dictionary, schema, sample export, or additional documentation exists. The PDF is the sole artifact describing the (b)(10) export.

## 3. Export Mechanics

- **Format**: ZIP archive per patient containing:
  1. A C-CDA XML file (in a "Clinical" folder)
  2. Document files in original upload format (in a "Documents" folder)
  3. A `Patient Documents Detail.xls` file (undocumented)
- **Mechanism**: UI-based export within SequelMed EHR. The documentation states users can export "at any time without developer assistance."
- **Single-patient**: Yes
- **Bulk/multi-patient**: Yes — documentation explicitly describes a multi-patient export mode
- **Access constraints/fees**: Not mentioned in the documentation

## 4. Export Content: What's In It

### Overview

The export documentation provides **zero field-level detail**. There is no data dictionary, no schema, no sample data, and no product-specific mapping. The entire description of export content consists of:

1. **C-CDA XML**: One file per patient. The vendor states it complies with "US Core Data for Interoperability (USCD) [sic], Version 1 requirements" and references three HL7 C-CDA specifications. No vendor-specific extensions, profiles, or constraints are documented. No indication of which C-CDA sections or templates are populated.

2. **Document files**: Exported in original upload/scan format. Six document types listed: signed progress notes, available lab results, radiology reports, scanned documents, imported documents, and "Iploaded" [sic] documents. Supported formats: .jpg, .gif, .bmp, .png, .pdf, .txt.

3. **Patient Documents Detail.xls**: Listed by name only — no description of contents, columns, or purpose provided anywhere.

### Vendor's own content organization

The vendor organizes export content into two categories plus an undocumented file:

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| C-CDA Clinical Document | 0 (defers to external spec) | 0 | N/A | Clinical Data |
| Patient Documents (files) | 0 | 0 | N/A | Patient Documents |
| Patient Documents Detail.xls | 0 (undocumented) | 0 | N/A | Patient Documents |

**Total documented entities**: 3 file-level components
**Total documented fields**: 0
**Fields with descriptions**: 0

The vendor provides no product-specific documentation whatsoever. The clinical data component is described solely by reference to the external C-CDA R2.1 specification.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes two categories of export content:

1. **Clinical Data** (1 component): A standard C-CDA XML file. This is a transitions-of-care document format that, per the C-CDA R2.1 specification, can include sections for allergies, encounters, immunizations, medications, problems, procedures, results, vital signs, plan of treatment, goals, health concerns, assessment, and social history. However, the vendor does not specify which sections are populated, which templates are used, or how product-specific data maps to C-CDA elements. The vendor claims USCDI V1 compliance, which covers core clinical summary data.

2. **Patient Documents** (2 components): Document files in original format plus an undocumented XLS file. This covers attached/scanned documents but with zero structured metadata documentation.

Both categories are extremely thin — the "Clinical Data" section is entirely defined by reference to an external standard, and the "Patient Documents" section has no field-level documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Presumably in C-CDA (standard section), but no confirmation | C-CDA typically includes basic demographics; depth unknown |
| Encounters / visits | ⚠️ Partial | Presumably in C-CDA encounters section, but no confirmation | C-CDA encounters section is typically summary-level, not full visit detail |
| Problems / conditions | ⚠️ Partial | Presumably in C-CDA problem list, but no confirmation | Standard C-CDA coverage; product-specific fields (severity tracking, verification workflows) unlikely |
| Medications / prescriptions | ⚠️ Partial | Presumably in C-CDA medications section, but no confirmation | C-CDA captures medication list; full e-prescribing history (SureScripts transactions) unlikely |
| Allergies | ⚠️ Partial | Presumably in C-CDA allergies section, but no confirmation | Standard C-CDA coverage |
| Immunizations | ⚠️ Partial | Presumably in C-CDA immunizations section, but no confirmation | Standard C-CDA coverage |
| Vitals | ⚠️ Partial | Presumably in C-CDA vital signs section, but no confirmation | Standard C-CDA coverage |
| Lab results | ⚠️ Partial | Presumably in C-CDA results section; also "available lab results" in Documents folder | C-CDA results section plus document files; structured lab data depth unknown |
| Imaging / diagnostic reports | ⚠️ Partial | "Radiology reports" listed in Documents folder; C-CDA may include diagnostic imaging section | Document files in original format; no structured imaging data |
| Procedures | ⚠️ Partial | Presumably in C-CDA procedures section, but no confirmation | Standard C-CDA coverage |
| Clinical notes / documents | ⚠️ Partial | "Signed progress notes" in Documents folder; C-CDA may include notes sections | Document files exported; but specialty-specific template data likely lost (exported as flat documents, not structured data) |
| Care plans / goals | ⚠️ Partial | Presumably in C-CDA plan of treatment/goals sections, but no confirmation | Standard C-CDA coverage if populated |
| Orders / referrals | ❌ Not covered | No mention in export documentation | Product stores lab, pharmacy, and imaging orders. Significant gap. |
| Insurance / coverage | ❌ Not covered | No mention in export documentation | Product stores insurance/eligibility data as part of PM. Significant gap. |
| Claims / billing | ❌ Not covered | No mention in export documentation | Product has full billing/RCM capabilities. **Major gap.** |
| Payments | ❌ Not covered | No mention in export documentation | Product tracks payments, A/R, collections. Significant gap. |
| Consents / directives | ❌ Not covered | No mention in export documentation | Uncertain if product stores these |
| Patient communications / portal messages | ❌ Not covered | No mention in export documentation | Product has patient portal (via Data Motion). Gap if messages are stored in SequelMed. |
| Specialty-specific data | ❌ Not covered | No mention in export documentation | Product claims 24+ specialty-specific templates. **Major gap** — custom template data likely cannot be represented in standard C-CDA. |

**Covered (with caveats)**: ~11 domains via C-CDA, but all are marked "partial" because the vendor provides zero confirmation of which C-CDA sections are actually populated. Coverage is assumed from the C-CDA standard, not documented by the vendor.

**Not covered**: 7+ domains, including billing/claims, payments, insurance, orders, specialty-specific data, and patient communications — all of which the product stores.

**Applicable domains with gaps**: At least 7 of 18 assessed domains are completely absent from the export despite the product storing that data.

## 6. Documentation Quality

The documentation quality is extremely poor:

- **Total content**: ~1.5 pages of actual text in a 4-page PDF (including cover page and whitespace)
- **Data dictionary**: None
- **Field-level documentation**: None — zero fields documented
- **Schema**: None provided; vendor defers entirely to external C-CDA specifications
- **Sample data**: None
- **Machine-readable artifacts**: None
- **Screenshots of export UI**: None
- **Error handling / edge cases**: Not discussed
- **Scope statement**: The document never explicitly states what data is or isn't included
- **Quality indicators**: Contains a typo ("Iploaded" for "Uploaded") and references "USCD" instead of "USCDI," suggesting minimal review
- **Usability**: A developer could not build an import system from this documentation alone. They would need to rely entirely on the external C-CDA specification for the clinical data, and would have no guidance whatsoever for the document files or the undocumented XLS file.

The documentation version is 1.0 (dated 2023-11-22) with no change history, suggesting it has not been updated since initial creation.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export is a C-CDA clinical summary plus document file attachments. Even assuming the C-CDA populates all standard sections, this covers only the USCDI V1 clinical summary — roughly the same scope as a transitions-of-care document. The entire practice management side of the product (billing, claims, payments, collections, A/R, eligibility, insurance) is absent. Specialty-specific clinical data from 24+ specialty templates — which is the product's key differentiator — is also absent, since standard C-CDA cannot represent arbitrary custom clinical forms. The documentation is too thin to confirm even the clinical domains are fully covered; coverage is inferred from the C-CDA standard, not documented by the vendor.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging the existing C-CDA transitions-of-care export as (b)(10). The telltale signs are all present:
- The export format is C-CDA, the same format used for (b)(1)–(b)(3) transitions of care
- The vendor references USCDI V1 and the standard C-CDA specifications — no product-specific data dictionary
- There is no coverage of data domains outside C-CDA's scope (billing, scheduling, specialty forms)
- There are no vendor-specific extensions, profiles, or custom mappings documented
- The documentation is version 1.0, minimal, and appears to have been created as a compliance artifact (November 2022 certification, November 2023 documentation)

The document attachments (progress notes, lab results, radiology reports, scanned documents) add marginal value beyond the C-CDA but are simply the product's existing document management export. The undocumented XLS file is the only potentially novel element, but its contents are unknown.

### Key Findings

1. **No data dictionary whatsoever**: Zero fields documented across the entire export. The vendor provides no product-specific field mapping, relying entirely on external C-CDA specifications. This is among the least documented (b)(10) exports possible. (`SequelMed-EHR-B10-Electronic-Health-Information-Export.pdf`, 4 pages)

2. **Entire practice management domain excluded**: SequelMed is marketed and sold as an integrated EHR + Practice Management platform with billing, claims, payments, A/R, collections, and revenue cycle management. None of this data is mentioned in the export documentation. (`product-research.md` vs. PDF content)

3. **Specialty template data unaddressed**: The product's distinguishing feature — customizable specialty-specific clinical templates for 24+ specialties — cannot be represented in standard C-CDA and is not mentioned in the export documentation. (`product-research.md` — "customizable specialty-specific clinical templates for 24+ specialties")

4. **C-CDA is the entire structured export**: The clinical data component is a single C-CDA file — the same format and scope as transitions-of-care exports under (b)(1)–(b)(3). This is a clinical summary, not a comprehensive EHI export. (`PDF`, page 2)

5. **Documentation created well after certification**: The PDF was created November 2023, nearly a year after certification in December 2022, suggesting documentation was an afterthought rather than part of the export design process. (`pdfinfo` metadata: CreationDate Wed Nov 22 12:11:29 2023)

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML + document files + undocumented XLS, in ZIP per patient
Entities:        3 file-level components (0 with field-level documentation)
Fields:          0 (no data dictionary)
Descriptions:    N/A (no fields documented)
Sample data:     No
Bulk export:     Yes (multi-patient mode documented)
Domains covered: ~11 of 18 applicable domains partially (via assumed C-CDA sections); 0 confirmed; 7 completely absent
```

### Bottom Line

SequelMed's (b)(10) export is a repackaged C-CDA transitions-of-care document with attached files — it covers at most the USCDI clinical summary scope and entirely omits the practice management, billing, and specialty-specific clinical data that constitute a large portion of the product's designated record set. A patient or provider receiving this export would get a clinical summary and scanned documents but would lose all billing history, specialty-specific clinical assessments, and any structured data that doesn't fit the C-CDA format. The documentation is among the thinnest possible: 4 pages, zero fields documented, no data dictionary, no sample data.

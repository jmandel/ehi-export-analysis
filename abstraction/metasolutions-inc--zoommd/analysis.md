# EHI Export Analysis: Metasolutions Inc

**Product**: ZoomMD v4.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1979.Zoom.41.01.1.221230 (CHPL #11182)

## 1. Product Context

ZoomMD is a cloud-based, integrated EHR and Practice Management system from Metasolutions Inc, targeting small to mid-sized ambulatory practices (~100 practices). Priced at $395/month, it bundles EHR, practice management, e-prescribing (via Surescripts/NewCropRx), lab integration, scheduling, billing, patient portal, document management, and medical transcription services. The product is broadly certified across 33 ONC criteria including clinical CPOE, e-prescribing, transitions of care, patient portal, CQMs, public health reporting, and FHIR API (g)(10).

**Data domains the product stores** (relevant to export completeness):
- **Clinical**: Demographics, problems/diagnoses, medications/prescriptions (including EPCS), allergies, labs (with national lab connectivity), vitals, immunizations, procedures, clinical notes (via templates, macros, and dictation/transcription), implantable devices, care plans, family health history
- **Billing/PM**: Superbills, claims, charges, insurance eligibility verification, patient balances, collections data, scheduling/appointments
- **Documents**: Scanned/faxed documents, clinical images
- **Patient portal**: Messages, treatment plan access
- **Reporting**: 25 CMS clinical quality measures

This is a full-spectrum ambulatory EHR+PM product. A genuine (b)(10) export should cover clinical data *and* billing, insurance, scheduling, and portal communication data.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `ZoomMD_EHI_Export_Format_Specification.pdf` (1.7 MB, 4 pages) | The sole EHI export documentation. A Word-to-PDF document dated Nov 2023, authored by "CS Sekhar." Contains 403 words of text and ~8 screenshots of the export UI workflow. Describes export format as ZIP containing C-CDA R2.1 + PDFs + HTML notes + images. **No data dictionary, no field-level spec, no schema, no sample data.** | Primary source; very thin |
| `certifications-page-screenshot.png` (533 KB) | Screenshot of the ZoomMD certifications page showing ONC/Drummond logos | Minimal — confirms page layout |
| `ehi-export-link-visible-screenshot.png` (246 KB) | Screenshot showing the "Electronic Health Information Export: Click Here" link on the certifications page | Confirms navigation path |
| `ehi-export-link-section-screenshot.png` (269 KB) | Additional screenshot of the EHI link section | Redundant with above |
| `ehi-export-section-screenshot.png` (269 KB) | Additional screenshot of the certifications page | Redundant with above |

The PDF is the only substantive artifact. The four screenshots are browser captures of the certifications page and add no technical content.

## 3. Export Mechanics

- **Format**: ZIP file containing per-patient folders with sub-folders of C-CDA R2.1 documents, PDF/scanned documents, HTML clinical notes, and image files (JPEG/JPG/PNG)
- **Mechanism**: Application UI — Settings > Interoperability > Data Export > Generate Summaries
- **Single-patient**: Yes — select one patient checkbox and click "Export"
- **Bulk/multi-patient**: Yes — select multiple patient checkboxes; also supports scheduled exports via "Configure Schedule" (frequency, date range, time settings)
- **Access constraints**: Role-controlled; ineligible users see disabled export functionality
- **Fees**: Not mentioned in documentation
- **Re-download**: Exported files available from "Data Export Summaries List" portlet on user dashboard
- **Developer assistance**: Explicitly states export can be performed "without subsequent developer assistance"

## 4. Export Content: What's In It

### Documentation gap

The PDF provides **zero** field-level, table-level, or section-level documentation. The only content specification is the format listing on page 1:

1. C-CDA R2.1 documents (referencing the generic HL7 C-CDA R2.1 Companion Guide)
2. PDF documents, scanned paper, and digital records of faxes
3. Clinical notes in HTML
4. Image files (JPEG, JPG, PNG)

There is no:
- Data dictionary
- Field listing or field descriptions
- Schema definition (XSD, JSON Schema, etc.)
- Sample export data
- Mapping from ZoomMD's internal data model to export format
- Description of which C-CDA sections/templates are populated
- Description of any vendor-specific extensions to C-CDA
- Any mention of billing, insurance, scheduling, or portal message data in the export

### Vendor's own content organization

The vendor does not organize content into categories. The only structured information is the format list. Since no data dictionary exists, no entity/field inventory can be constructed from the documentation:

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| C-CDA R2.1 Document | 0 | N/A | N/A | "Document Reference" |
| PDF Document | 0 | N/A | N/A | "Document Reference" |
| HTML Clinical Note | 0 | N/A | N/A | "Document Reference" |
| Image File | 0 | N/A | N/A | "Document Reference" |

**Total documented entities**: 4 file types (not database entities)
**Total documented fields**: 0
**Fields with descriptions**: 0

The vendor's "Standards Information" section uses the term "Document Reference" as metadata describing a document "such as" the four types listed. This is a format specification, not a data dictionary.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes exactly one category of export content: **documents**. The export is framed as a collection of document files organized into per-patient folders. The only structured data format mentioned is C-CDA R2.1, which by the standard's specification would cover a subset of clinical data (demographics, problems, medications, allergies, labs, vitals, immunizations, procedures, encounters, and care plans). However, the vendor provides no indication of which C-CDA sections they actually populate, whether they use any extensions, or how deeply their internal data maps to C-CDA templates.

The phrase "all accessible EHI information" appears once in the general description but is not substantiated with any specifics about what "all" includes. The documentation does not mention billing data, insurance information, scheduling data, portal messages, prescribing details beyond standard C-CDA, or any other non-clinical data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Implied via C-CDA R2.1 standard demographics section; no field-level confirmation | Product stores demographics (a)(5); C-CDA would include basic demographics but depth is unknown |
| Encounters / visits | ⚠️ Partial | Implied via C-CDA R2.1 encounters section | Product has encounter-based charting; C-CDA coverage likely limited to summary |
| Problems / conditions | ⚠️ Partial | Implied via C-CDA R2.1 problem list section | Product certified for (a)(4); C-CDA would include standard problem list |
| Medications / prescriptions | ⚠️ Partial | Implied via C-CDA R2.1 medications section | Product has full e-prescribing with EPCS; C-CDA likely captures medication list but not Rx routing, pharmacy details, formulary data |
| Allergies | ⚠️ Partial | Implied via C-CDA R2.1 allergies section | Product has allergy checking; standard C-CDA section |
| Immunizations | ⚠️ Partial | Implied via C-CDA R2.1 immunizations section | Product certified for (f)(1) immunization registries |
| Vitals | ⚠️ Partial | Implied via C-CDA R2.1 vital signs section | Standard C-CDA section |
| Lab results | ⚠️ Partial | Implied via C-CDA R2.1 results section | Product has integrated lab module; C-CDA likely captures results but not order details |
| Imaging / diagnostic reports | ⚠️ Partial | Implied via C-CDA R2.1; images exported as files | Product certified for (a)(3) CPOE for imaging |
| Procedures | ⚠️ Partial | Implied via C-CDA R2.1 procedures section | Standard C-CDA section |
| Clinical notes / documents | ⚠️ Partial | HTML clinical notes and PDF/scanned documents exported as files | Product has charting, templates, dictation/transcription; HTML notes and PDFs would capture document content but not structured template data |
| Care plans / goals | ⚠️ Partial | Implied via C-CDA R2.1 plan of care section | Standard C-CDA section |
| Orders / referrals | ❌ Not covered | No evidence; C-CDA R2.1 has limited order support | Product has CPOE for labs/imaging; order details likely missing |
| Insurance / coverage | ❌ Not covered | No mention in documentation | Product has eligibility verification and insurance data; significant gap |
| Claims / billing | ❌ Not covered | No mention in documentation | Product has superbills, claims, charges, collections; significant gap |
| Payments | ❌ Not covered | No mention in documentation | Product tracks patient balances and collections; significant gap |
| Patient communications / portal messages | ❌ Not covered | No mention in documentation | Product has patient portal with messaging; gap |
| Consents / directives | ❌ Not covered | No evidence | Unknown if product stores these |
| Family health history | ⚠️ Partial | Implied via C-CDA R2.1 family history section | Product certified for (a)(12) |

All "Partial" ratings are based solely on the assumption that C-CDA R2.1 standard sections would be populated — the vendor provides no confirmation of which sections they actually include. Without sample data or a data dictionary, even the clinical domain coverage cannot be verified.

**Billing/PM gap**: ZoomMD is an integrated EHR+PM product with superbills, claims tracking, insurance eligibility, and patient balance features. The export documentation makes zero mention of any billing, insurance, or financial data. This is the most significant gap.

## 6. Documentation Quality

**Rating: Very poor — among the weakest possible.**

The 4-page PDF is a screenshot-driven user guide showing how to navigate the export UI. It contains 403 total words. It provides:

- ✅ Export format name (C-CDA R2.1 + documents)
- ✅ Export mechanism (UI path, single/multi-patient, scheduling)
- ✅ Access control mention
- ❌ No data dictionary
- ❌ No field-level documentation of any kind
- ❌ No schema files
- ❌ No sample export data
- ❌ No C-CDA section/template mapping
- ❌ No description of what "all accessible EHI" actually includes
- ❌ No mention of non-clinical data domains
- ❌ No vendor extensions or product-specific mapping
- ❌ No relationship documentation
- ❌ No value sets or code systems

A developer receiving this export would know they're getting a ZIP with C-CDA files and document attachments. They would have zero vendor-specific guidance on what data to expect in the C-CDA, what sections are populated, what level of detail is included, or whether non-clinical data is present. They would need to reverse-engineer the export by examining actual exported files.

The documentation references the generic HL7 C-CDA R2.1 Companion Guide spec — this is the standard itself, not a product-specific data dictionary. This is the hallmark of a vendor pointing at a generic standard rather than documenting their own export.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to verify what the export actually contains. The only concrete format information is "C-CDA R2.1 + documents in a ZIP." Even assuming the C-CDA sections are fully populated (which is unverified), this would cover only clinical summary data — roughly the USCDI surface. The product's billing/PM capabilities (superbills, claims, insurance eligibility, patient balances) have zero representation in the export documentation. The phrase "all accessible EHI information" is used once but never substantiated. With no data dictionary, no sample data, and no field-level documentation, it's impossible to assess actual coverage beyond what C-CDA R2.1 standard sections would provide by default.

**Axis 2 — Export approach: Repackaged existing export**

Every indicator points to this being the vendor's existing C-CDA clinical summary export repackaged as (b)(10):
1. The export format is C-CDA R2.1 — the same standard used for transitions of care (b)(1)-(b)(3), which ZoomMD is also certified for
2. The only standards reference is the generic HL7 C-CDA R2.1 Companion Guide — no product-specific data dictionary or mapping
3. There is no mention of billing, insurance, scheduling, or any non-clinical data domain
4. The documentation title calls it "Generate Summaries" — language consistent with clinical summary generation, not full EHI export
5. The UI navigation path visible in the screenshots shows the export under "Interoperability > Data Export > Generate Summaries" — the same pattern used for clinical document exchange
6. No evidence of any vendor-specific extensions, custom fields, or data beyond what standard C-CDA templates provide

### Key Findings

1. **No data dictionary exists.** The entire export documentation is a 4-page, 403-word PDF consisting primarily of UI screenshots. Zero fields are documented. This is one of the thinnest EHI export documentation sets possible.

2. **Export appears to be repackaged C-CDA clinical summaries.** The format, standards reference, UI labeling ("Generate Summaries"), and navigation path all indicate this is the vendor's existing clinical document exchange repurposed as (b)(10). The generic HL7 C-CDA R2.1 spec is referenced with no product-specific mapping.

3. **Billing/PM data is entirely absent from documentation.** ZoomMD is an integrated EHR+PM product with superbills, claims, insurance eligibility, and collections features. The export documentation makes no mention of any billing or financial data — a significant gap for a product that markets billing as a core capability.

4. **Even clinical coverage is unverifiable.** Without sample data or a data dictionary, it's impossible to confirm which C-CDA sections are actually populated, how deeply internal data maps to C-CDA templates, or whether any product-specific data survives the export.

5. **Scheduled export is a positive feature.** The "Configure Schedule" capability allowing automated recurring exports with frequency, date range, and time parameters is a useful operational feature, though it doesn't address the content completeness issues.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   C-CDA R2.1 + PDF/HTML/images in ZIP
    Entities:        N/A (no data dictionary)
    Fields:          N/A (0 fields documented)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Yes (multi-patient selection + scheduled exports)
    Domains covered: 0 confirmed, ~12 implied via C-CDA standard (unverified) of 15+ applicable domains

### Bottom Line

ZoomMD's EHI export documentation is a 4-page screenshot guide with no data dictionary, no field-level specification, and no evidence of coverage beyond standard C-CDA clinical summaries. For a product that includes integrated billing and practice management, the complete absence of billing, insurance, and scheduling data from the export — combined with the reuse of C-CDA clinical exchange format and generic HL7 spec references — indicates this is a compliance checkbox rather than a genuine effort to export all electronic health information. A patient or provider receiving this export would get a clinical summary document, not a complete copy of their designated record set.

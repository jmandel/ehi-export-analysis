# EHI Export Analysis: Metasolutions Inc

**Product**: ZoomMD v4.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1979.Zoom.41.01.1.221230 (CHPL ID 11182)

## 1. Product Context

ZoomMD is a cloud-based, ONC-certified integrated Electronic Health Record (EHR) and Practice Management (PM) system developed by Metasolutions Inc, a small healthcare IT company based in Irvine, California. The product targets small to mid-sized ambulatory medical practices (approximately 100 practices), starting at $395/month. It is broadly certified across 33 ONC criteria.

ZoomMD stores and manages data across the following domains relevant to EHI completeness:

- **Clinical documentation**: Charting via templates, macros, dictation/transcription; encounter notes; problem lists; vitals
- **E-prescribing**: Medications, controlled substances (EPCS), allergy/interaction checks via Surescripts/NewCropRx
- **Lab integration**: Lab orders and results via national lab connectivity
- **Imaging orders**: CPOE for diagnostic imaging
- **Billing / Practice Management**: Superbills, claims tracking, electronic claims submission, real-time eligibility verification, collections
- **Scheduling**: Appointment scheduler with patient balance display at check-in
- **Insurance**: Eligibility verification, coverage details
- **Patient portal**: Patient profiles, treatment plans, messaging/communication
- **Document management**: Scanned/faxed documents, "Zoom viewer"
- **Telehealth**: Marketed as part of the platform
- **Quality measures**: 25 CMS clinical quality measures
- **Public health reporting**: Immunizations, syndromic surveillance, electronic case reporting

The breadth of this product—particularly its integrated billing/PM module—sets a high bar for what a complete EHI export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ZoomMD_EHI_Export_Format_Specification.pdf` (1.7 MB, 4 pages) | The sole EHI export documentation. Page 1: header, product info, and brief format description. Pages 2–4: 11 numbered steps with screenshots showing the export UI workflow. Authored by "CS Sekhar," dated November 2023. | **Primary artifact** — but contains almost no technical detail |
| `certifications-page-screenshot.png` (533 KB) | Screenshot of the ZoomMD certifications page showing ONC/Drummond logos, vendor info, and certified criteria listing. | Low — confirms website is live and accessible |
| `ehi-export-link-visible-screenshot.png` (246 KB) | Screenshot showing the "Electronic Health Information Export: Click Here" link on the certifications page, alongside Real World Test plans/results. | Low — confirms the PDF is directly linked |
| `ehi-export-link-section-screenshot.png` (269 KB) | Additional screenshot of the EHI export link section. | Redundant with above |
| `ehi-export-section-screenshot.png` (269 KB) | Additional screenshot of the certifications page export section. | Redundant with above |

**Verification**: The certifications page at `https://www.zoommd.com/company-certifications-awards/` returns HTTP 200 and the EHI Export Format Specification PDF is directly downloadable. No additional EHI documentation artifacts (data dictionaries, schemas, sample data, XLSX files) were found on the page — only Real World Test plans/results and a mandatory disclosure statement.

## 3. Export Mechanics

- **Format**: ZIP file containing per-patient folders with C-CDA R2.1 documents, PDF documents (scanned paper, faxes), clinical notes in HTML, and image files (JPEG, JPG, PNG)
- **Mechanism**: Application UI — Settings > Interoperability > Data Export > Generate Summaries
- **Single-patient**: Yes — select one patient checkbox and click "Export"
- **Bulk/multi-patient**: Yes — select multiple patient checkboxes; a single ZIP containing multiple patient folders is downloaded
- **Scheduled export**: Yes — "Configure Schedule" allows setting frequency (year/month), start/end dates, and time
- **Re-download**: Exported files are available from a "Data Export Summaries List" portlet on the user dashboard
- **Access control**: Role-based — ineligible users cannot access export functionality (demonstrated in PDF page 4 screenshot)
- **Developer assistance**: Not required — "A user can export the patient(s) EHI at any time without subsequent developer assistance"
- **Fees**: Not mentioned in export documentation

## 4. Export Content: What's In It

### What the documentation tells us

The PDF states the export contains "all accessible EHI information" in a ZIP file with:

1. **C-CDA R2.1 documents** — referenced standard: "C-CDA Templates for Clinical Notes R2.1 Companion Guide, Release 2"
2. **PDF documents** — scanned paper and digital records of faxes
3. **Clinical notes in HTML**
4. **Image files** — JPEG, JPG, PNG

That is the entirety of the format specification. There is:

- **No data dictionary** — zero entities, zero fields documented
- **No schema files** — no XSD, JSON Schema, or other machine-readable artifacts
- **No sample data** — no example exports provided
- **No C-CDA section/template specification** — no indication of which C-CDA sections are populated
- **No field-level documentation** — no field names, types, descriptions, value sets, or relationships
- **No mapping** from ZoomMD's internal data model to the export format
- **No description** of how billing, scheduling, insurance, or portal data is handled

### Vendor's own content organization

The vendor does not organize the export into categories, entities, or tables. The entire "format specification" describes only the container format (ZIP → patient folders → document types). No entity-level or field-level inventory exists to present.

| Content Type | Fields | Described | Types | Category |
|---|---|---|---|---|
| C-CDA R2.1 documents | N/A | N/A | N/A | Clinical documents |
| PDF documents | N/A | N/A | N/A | Scanned/faxed records |
| HTML clinical notes | N/A | N/A | N/A | Clinical notes |
| Image files | N/A | N/A | N/A | Clinical images |

**There are zero enumerated entities or fields.** The documentation describes file formats, not data content.

### What we can infer (but not verify)

C-CDA R2.1 typically includes sections for demographics, problems, medications, allergies, immunizations, vitals, lab results, procedures, and clinical notes. However, without a data dictionary, sample export, or section list, we cannot confirm which C-CDA sections ZoomMD actually populates, whether they include vendor extensions, or how complete the data mapping is.

### Observable UI modules (from PDF screenshots)

The PDF screenshots reveal the ZoomMD application navigation menu, which includes tabs for: Settings, Demographics, Charting, Scheduler, Billing, Reports, Messages. The patient list view shows columns: Acc No#, First Name, Last Name, DOB, Gender, Practice Physician, Referring Physician. The "Superbills Status" indicator is visible in the toolbar. None of this data is described in the export format specification.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes exactly one category of export content: **clinical documents packaged in C-CDA R2.1 format, supplemented by raw documents (PDFs, HTML notes, images)**. There are no categories, no modules, no sections — just a flat statement that the ZIP contains these file types.

The C-CDA standard *could* cover core clinical data (demographics, problems, medications, allergies, vitals, labs, immunizations, procedures, notes), but the vendor provides no evidence about which sections are populated or how complete the mapping is. The PDF/HTML/image components cover scanned documents and clinical notes in their original format.

There is no mention whatsoever of billing data, scheduling data, insurance data, patient portal data, or any practice management content in the export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Likely in C-CDA, but no confirmation of which fields | Product stores demographics (visible in patient list screenshots); C-CDA typically includes basic demographics but completeness is unverifiable |
| Encounters / visits | ⚠️ Partial | Likely in C-CDA encounter sections | Product manages encounters; C-CDA may include encounter data but no specifics documented |
| Problems / conditions | ⚠️ Partial | Likely in C-CDA problem list section | Product certified for (a)(4) drug-diagnosis interaction; C-CDA typically includes problems |
| Medications / prescriptions | ⚠️ Partial | Likely in C-CDA medications section | Product has full e-prescribing module (Surescripts/EPCS); C-CDA covers basic med lists but likely not full Rx routing/pharmacy/formulary detail |
| Allergies | ⚠️ Partial | Likely in C-CDA allergies section | Product has allergy checking; C-CDA typically includes allergies |
| Immunizations | ⚠️ Partial | Likely in C-CDA immunizations section | Product certified for (f)(1) immunization registries |
| Vitals | ⚠️ Partial | Likely in C-CDA vital signs section | Standard EHR data |
| Lab results | ⚠️ Partial | Likely in C-CDA results section | Product has lab module with national lab connectivity |
| Imaging / diagnostic reports | ⚠️ Partial | Likely in C-CDA if populated | Product certified for (a)(3) CPOE imaging |
| Procedures | ⚠️ Partial | Likely in C-CDA procedures section | Standard clinical data |
| Clinical notes / documents | ⚠️ Partial | HTML notes and C-CDA document sections; PDFs of scanned records | Product has charting, templates, dictation/transcription. HTML notes and scanned PDFs are exported, but completeness is unknown |
| Care plans / goals | ⚠️ Partial | May be in C-CDA if populated | Patient portal mentions "treatment plans" |
| Orders / referrals | ⚠️ Partial | May be in C-CDA if populated | Product has ordering portlets visible in UI |
| Insurance / coverage | ❌ Not covered | No mention in export documentation | Product has insurance eligibility verification and coverage data — **significant gap** |
| Claims / billing | ❌ Not covered | No mention in export documentation | Product has integrated billing, superbills, claims tracking, electronic claims submission — **significant gap** |
| Payments | ❌ Not covered | No mention in export documentation | Product tracks patient balances and collections — **significant gap** |
| Consents / directives | ⚠️ Partial | May be in C-CDA advance directives section | Unknown if product stores these |
| Patient communications / portal messages | ❌ Not covered | No mention in export documentation | Product has patient portal with messaging — **gap** |
| Family health history | ⚠️ Partial | May be in C-CDA if populated | Product certified for (a)(12) family health history |

**Note on "Partial" ratings**: All clinical domains are rated "Partial" rather than "Covered" because the vendor provides zero evidence about which C-CDA sections are actually populated. C-CDA R2.1 *can* contain these data types, but without a section list, sample data, or data dictionary, we are inferring coverage from the standard's capabilities rather than verifying from the vendor's documentation. The vendor has done nothing to demonstrate what data is actually in the export.

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the lowest possible while still having a document at all.

**What exists**: A 4-page PDF that functions as a basic user guide for triggering an export. It shows how to log in, navigate to the export function, select patients, and download the ZIP. It mentions the file types in the ZIP (C-CDA, PDF, HTML, images).

**What's missing**: Everything a developer would need to actually use the exported data:
- No data dictionary or entity inventory
- No field names, types, or descriptions
- No C-CDA section/template specification
- No schema files (XSD, JSON Schema)
- No sample data or example exports
- No mapping from internal data model to export format
- No description of what "all accessible EHI information" actually includes
- No value sets or coded values
- No relationship documentation

**Could a developer build an import?** No. A developer receiving this export would get a ZIP of C-CDA XML files with no vendor-specific guidance on what to expect. They would need to parse generic C-CDA documents and hope the relevant sections are populated. There is no way to know in advance what data domains are covered, what fields are present, or what coding systems are used.

**Machine-readable artifacts**: None. The only artifact is a PDF with embedded screenshot images. No schemas, no structured documentation, no sample data.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is built entirely on C-CDA R2.1, a clinical document standard, supplemented by raw document attachments (PDFs, HTML, images). There is no native database export and no evidence that the vendor's internal data model is exposed. The export covers, at best, the clinical summary data that C-CDA supports — likely missing billing, insurance, scheduling, patient portal, and practice management data that ZoomMD stores.

### Key Findings

1. **C-CDA repackaging with zero documentation**: The export is a ZIP of C-CDA R2.1 documents plus document attachments. No data dictionary, no schema, no sample data, no field-level specification exists. This is one of the thinnest EHI export documentation sets possible — it describes the container but not the contents. (Source: `ZoomMD_EHI_Export_Format_Specification.pdf`, 4 pages, 46 lines of extractable text)

2. **Billing and practice management data are almost certainly missing**: ZoomMD has an integrated billing module (superbills, claims, eligibility verification, collections) and practice management features (scheduling, patient balances). C-CDA R2.1 has no standard templates for billing records, claims, or practice management data. The export documentation makes no mention of these domains. (Source: product-research.md; `ZoomMD_EHI_Export_Format_Specification.pdf` — no billing/PM data types listed)

3. **All clinical domain coverage is unverifiable**: While C-CDA can carry clinical data (demographics, problems, meds, labs, etc.), the vendor provides no specification of which sections are populated. Every clinical domain is "likely covered" based on the standard's capabilities, but zero domains can be confirmed as covered based on the vendor's documentation. (Source: absence of any section/template list in the PDF)

4. **Export mechanics are reasonable**: Despite the documentation gap, the export mechanism itself is functional: UI-driven, supports single and multi-patient export, offers scheduled exports, provides role-based access control, and allows re-download. The UI screenshots show a working export workflow. (Source: `ZoomMD_EHI_Export_Format_Specification.pdf`, steps 1–11)

5. **Compliance checkbox, not a real effort**: The 4-page PDF reads as a minimal compliance artifact — a screenshot walkthrough of the export button with a brief mention of C-CDA as the format. There is no evidence that Metasolutions invested in documenting what data their export actually contains, which is the core requirement of a format specification.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA R2.1 + PDF + HTML + images (in ZIP)
Model type:      Standard projection (C-CDA clinical documents)
Entities:        N/A (no data dictionary)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (multi-patient selection + scheduled export)
Domains covered: 0 of 15 confirmed; ~10 of 15 likely via C-CDA (unverifiable)
```

### Bottom Line

ZoomMD's EHI export is a C-CDA R2.1 document package with no data dictionary, no schema, and no field-level documentation. A patient or provider would likely receive clinical summary data in C-CDA format plus scanned documents, but billing records, insurance data, patient portal messages, and practice management data from ZoomMD's integrated PM module are almost certainly absent. The single biggest gap is the complete absence of any specification for what data is actually exported — making it impossible to verify compliance with the "all EHI" requirement.

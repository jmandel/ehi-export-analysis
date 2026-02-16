# EHI Export Analysis: Practice EHR LLC

**Product**: Practice EHR V12
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2997.Prac.12.01.1.220628

## 1. Product Context

Practice EHR is a cloud-based, all-in-one ambulatory EHR and practice management platform targeting small to mid-sized multi-specialty practices. It covers a wide range of clinical and administrative workflows:

- **Clinical**: Charting with specialty-specific templates (23 specialties), e-prescribing (including EPCS), lab ordering/results (Quest, Labcorp, regional labs), vitals, problem lists, medication lists, allergies, immunizations, implantable device tracking, clinical decision support, AI Scribe transcription
- **Practice management**: Multi-provider/multi-location scheduling, appointment reminders, patient check-in kiosk with customizable intake forms
- **Billing & RCM**: Superbill/encounter forms, claim scrubbing and submission to 16,000+ payers (professional, institutional, workers' comp, no-fault, dental), ERA processing, payment posting, denial management, patient statements, eligibility verification
- **Patient engagement**: Patient portal (messages, refill requests, appointment requests, statement viewing), telehealth (TeleVisit)
- **Document management**: Scanning, importing, uploading documents
- **Reporting**: Practice dashboards, financial analytics, MIPS/CQM quality reporting

This is a full-featured ambulatory EHR+PM product. A genuine (b)(10) export should cover clinical data, billing/claims, patient communications, intake forms, scheduling history, and document management — far more than a clinical summary.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Practice-EHR-B10-Electronic-Health-Information-Export.pdf` | 4-page PDF (cover + 3 pages content). Version 1.0, dated November 2023. The sole documentation artifact. Describes the ZIP export structure at a high level: C-CDA XML, documents folder, and XLS index. No data dictionary, no schema, no sample data. | **Primary but extremely thin** |
| `downloads/data-export-page.png` | Screenshot of the vendor's data export landing page. Shows a single heading ("Data Export") and one link to the PDF. | Confirms there is no additional documentation |

Only two artifacts exist. The PDF is the entirety of the vendor's (b)(10) export documentation.

## 3. Export Mechanics

- **Format**: ZIP file per patient containing: (1) a C-CDA XML file, (2) a folder of document files in original formats, (3) a `Patient Documents Detail.xls` index file
- **Mechanism**: UI-initiated; the PDF states users can export "at any time without developer assistance" but provides no screenshots or step-by-step instructions
- **Single-patient**: Yes
- **Bulk/multi-patient**: Yes ("multi patients" mode described)
- **Access constraints**: None mentioned; no fees documented
- **Developer assistance**: Not required per the documentation

## 4. Export Content: What's In It

The export contains three components, none of which have field-level documentation:

### 4.1 C-CDA XML (Clinical folder)

A single C-CDA file per patient, described as complying with "US Core Data for Interoperability (USCD), Version 1" (note: "USCD" is a typo for "USCDI"). Three HL7 C-CDA specifications are referenced. No vendor-specific template IDs, extensions, or section mappings are documented. The C-CDA standard covers approximately 13 USCDI v1 data classes: demographics, problems, medications, allergies, lab results, vitals, procedures, immunizations, care team, goals, health concerns, smoking status, and assessment/plan.

**No data dictionary is provided.** The vendor simply points to the HL7 C-CDA specification. There are zero vendor-specific field definitions, zero descriptions of how Practice EHR maps its internal data to C-CDA sections, and zero documentation of any vendor extensions.

### 4.2 Patient Documents (Documents folder)

Unstructured document files exported in their original upload/scan formats (.jpg, .gif, .bmp, .png, .pdf, .txt). The PDF lists six document types:
1. Signed progress notes
2. Available lab results
3. Radiology reports
4. Scanned documents
5. Imported documents
6. Uploaded documents (listed as "Iploaded" — typo)

This is essentially a file dump with no structured metadata.

### 4.3 Patient Documents Detail.xls

An XLS index file included in the ZIP. **Its structure, columns, and content are completely undocumented.** The PDF mentions it exists but does not describe what it contains.

### Vendor's own content organization

The vendor does not organize content into categories or provide an entity-level breakdown. The entire documentation is at the component level:

| Component | Fields | Described | Types | Category |
|---|---|---|---|---|
| C-CDA XML file | N/A (refers to HL7 standard) | No | No | Clinical |
| Documents folder | N/A (unstructured files) | No | No | Documents |
| Patient Documents Detail.xls | Unknown | No | No | Index |

**Total documented entities: 3 components. Total documented fields: 0. No data dictionary exists.**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export documentation describes exactly two data categories:

1. **Clinical summary data** via C-CDA: Standard USCDI v1 clinical data classes. No depth beyond what the C-CDA standard requires. No vendor-specific fields, extensions, or additional sections are documented.

2. **Document files**: A dump of uploaded/scanned documents in original formats. This provides some coverage of clinical documents (progress notes, lab results, radiology reports) but only as unstructured files, not as parsed/structured data.

The documentation is extraordinarily thin. There is no billing category, no administrative category, no patient engagement category, no scheduling category — nothing beyond the two items above.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA recordTarget section (per standard) | C-CDA covers basic demographics; product collects richer data via kiosk intake forms — likely not fully exported |
| Encounters / visits | ⚠️ Partial | C-CDA Encounters section (per standard) | C-CDA may include basic encounter info; product stores detailed encounter/superbill data — unlikely fully captured |
| Problems / conditions | ⚠️ Partial | C-CDA Problems section (per standard) | Covered at USCDI level; depth of internal problem list fields unknown |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medications section (per standard) | USCDI-level coverage; EPCS history, Surescripts medication history, formulary data likely missing |
| Allergies | ⚠️ Partial | C-CDA Allergies section (per standard) | Covered at USCDI level |
| Immunizations | ⚠️ Partial | C-CDA Immunizations section (per standard) | Covered at USCDI level |
| Vitals | ⚠️ Partial | C-CDA Vital Signs section (per standard) | Covered at USCDI level |
| Lab results | ⚠️ Partial | C-CDA Results section + document files | Structured results in C-CDA; lab PDFs in documents folder. Lab ordering details likely missing |
| Imaging / diagnostic reports | ⚠️ Partial | Document files (radiology reports) | Radiology reports included as unstructured documents only; no structured imaging data |
| Procedures | ⚠️ Partial | C-CDA Procedures section (per standard) | Covered at USCDI level |
| Clinical notes / documents | ⚠️ Partial | Document files (signed progress notes, scanned docs) | Progress notes exported as files; structured note data from charting templates likely not exported |
| Care plans / goals | ⚠️ Partial | C-CDA Goals/Health Concerns sections (per standard) | Covered at USCDI level |
| Orders / referrals | ❌ Not covered | No evidence in export | Product supports lab ordering; no order data in export |
| Insurance / coverage | ❌ Not covered | No evidence in export | Product stores insurance/eligibility data; significant gap |
| Claims / billing | ❌ Not covered | No evidence in export | Product has full billing/claims (16,000+ payers); **major gap** |
| Payments | ❌ Not covered | No evidence in export | Product handles payment posting, ERA, patient statements; significant gap |
| Consents / directives | ❌ Not covered | No evidence in export | Product collects consent forms via kiosk; not exported |
| Patient communications / portal messages | ❌ Not covered | No evidence in export | Product has patient portal with secure messaging; significant gap |
| Specialty-specific (23 specialties) | ❌ Not covered | No evidence in export | Product has specialty templates for 23 specialties; none exported as structured data |

**Summary**: 0 of 19 domains fully covered. ~11 domains have partial coverage via C-CDA standard sections (USCDI-level only). 8 domains have no coverage at all, including billing/claims, insurance, payments, patient communications, and specialty-specific data — all of which the product actively stores.

## 6. Documentation Quality

The documentation quality is **extremely poor**:

- **No data dictionary**: Zero field-level documentation anywhere
- **No schema**: No machine-readable artifact of any kind
- **No sample data**: No example exports provided
- **No vendor-specific mappings**: The C-CDA is described only by reference to the HL7 standard; no information about which sections Practice EHR populates, which template IDs are used, or whether any vendor extensions exist
- **No description of XLS index**: The `Patient Documents Detail.xls` file is mentioned but its structure is completely undocumented
- **No user instructions**: No screenshots, no menu paths, no step-by-step guide for performing the export
- **Typos**: "USCD" for "USCDI", "Iploaded" for "Uploaded" — suggesting minimal review
- **3 pages of content** (plus a cover page) for what should be comprehensive export documentation

A developer could not build an import from this documentation. They would need to parse C-CDA per the HL7 standard (not vendor-specific) and guess at the XLS index file structure. No information exists about how Practice EHR's internal data model maps to C-CDA sections.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub**

The export covers only USCDI v1 clinical summary data via C-CDA plus an unstructured document dump. For a product that is a full EHR + practice management + billing + RCM platform serving 23 specialties, this represents a small fraction of stored patient data. Entire major domains — billing/claims, insurance, payments, patient portal messages, consent forms, specialty templates, encounter/superbill data, e-prescribing history — are completely absent. The documentation is 3 pages with no data dictionary, making it impossible to verify even what the C-CDA export contains beyond standard sections.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging. The clinical data component is a C-CDA — the same format used for transitions of care under (b)(1)–(b)(3). The documentation explicitly references USCDI v1 and the standard C-CDA specifications with no vendor-specific additions. The document folder is a simple file dump that likely already existed as part of the product's document management. Adding these two existing capabilities together and labeling them "(b)(10)" does not constitute a purpose-built EHI export. The telltale signs are all present: no product-specific data dictionary, no mapping beyond standard C-CDA templates, and no coverage of billing or operational data.

### Key Findings

1. **The export is a repackaged C-CDA + document dump.** The clinical data is a standard C-CDA per USCDI v1 — the same format used for care transitions. No vendor-specific fields, extensions, or additional data beyond the standard are documented. (Source: `Practice-EHR-B10-Electronic-Health-Information-Export.pdf`, pages 2–3)

2. **Zero field-level documentation exists.** There is no data dictionary, no schema, no sample data, and no description of how Practice EHR's internal data maps to C-CDA sections. The entire documentation is 3 pages of content. (Source: `Practice-EHR-B10-Electronic-Health-Information-Export.pdf`, 4 pages total)

3. **Billing, claims, and RCM data are entirely absent.** Practice EHR is a full billing and practice management platform handling claims to 16,000+ payers, ERA processing, payment posting, and denial management. None of this data is included in the export. (Source: product-research.md vs. PDF documentation)

4. **Patient engagement data is absent.** Portal messages, appointment requests, prescription refill requests, kiosk intake forms, and consent forms — all stored by the product — are not exported. (Source: product-research.md vs. PDF documentation)

5. **The XLS index file is undocumented.** The `Patient Documents Detail.xls` file is mentioned but its columns and structure are not described at all. (Source: `Practice-EHR-B10-Electronic-Health-Information-Export.pdf`, page 3)

### Summary Stats

```
Coverage:        Minimal/stub
Approach:        Repackaged existing export
Export format:   C-CDA XML + document files (.jpg/.png/.pdf/.txt) + XLS index, in ZIP
Entities:        N/A (no data dictionary)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (multi-patient mode described)
Domains covered: 0 of 19 fully; ~11 of 19 partially (USCDI-level only via C-CDA)
```

### Bottom Line

Practice EHR's (b)(10) export is a standard C-CDA clinical summary plus a folder of scanned/uploaded documents — the same data a patient could get through a transitions-of-care document. For a product that stores billing, claims, insurance, patient portal messages, specialty-specific clinical data, and practice management information, this export covers a small fraction of the designated record set. The single biggest gap is the complete absence of billing and RCM data from a product whose core value proposition includes integrated billing and claims processing.

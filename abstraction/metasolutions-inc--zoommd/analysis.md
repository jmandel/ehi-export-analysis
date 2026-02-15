# EHI Export Analysis: Metasolutions Inc

**Product**: ZoomMD v4.1
**Analysis date**: 2026-02-15
**CHPL IDs**: 11182 (15.04.04.1979.Zoom.41.01.1.221230)

## 1. Product Context

ZoomMD is a cloud-based, ONC-certified integrated EHR and Practice Management (PM) system developed by Metasolutions Inc (Irvine, CA). It targets small to mid-sized ambulatory practices across 40+ specialties, priced at $395/month. The product is broadly certified across 33 ONC criteria including (b)(10) EHI export.

ZoomMD stores the following data relevant to EHI completeness assessment:

- **Clinical data**: patient demographics, problem lists, medications (including EPCS via NewCropRx/Surescripts), allergies, lab orders and results, vitals, immunizations, procedures, implantable device identifiers, clinical notes (via charting templates, macros, and dictation/transcription), care plans, and family health history
- **Billing/PM data**: superbills, claims, charges, insurance eligibility verification, collections, and payment tracking — the vendor also offers professional billing *services* alongside the software
- **Practice management**: appointment scheduling, referrals, document management (scanned/faxed documents)
- **Patient engagement**: patient portal with messaging, view/download/transmit capabilities, and (reportedly) telehealth
- **Public health reporting**: immunization registry submissions, syndromic surveillance, electronic case reporting

This is a full-featured ambulatory EHR+PM system. A complete EHI export should cover clinical documentation, billing records, insurance information, and specialty-specific data — not just a clinical summary.

## 2. Artifacts Reviewed

| Artifact | Type | Size | Informativeness | What It Told Me |
|---|---|---|---|---|
| `ZoomMD_EHI_Export_Format_Specification.pdf` | PDF, 4 pages | 1.63 MB | **Primary (but low value)** | The only documentation of the (b)(10) export. Contains ~300 words of specification text plus 11 UI screenshots. States export is a ZIP of C-CDA R2.1 + PDF/HTML/image attachments. No data dictionary, no field-level detail, no schema. |
| `certifications-page-screenshot.png` | Screenshot | 521 KB | Minimal | Confirms ZoomMD v4.1 certification as "Certified EHR Ambulatory" with Drummond/ONC logos. |
| `ehi-export-link-visible-screenshot.png` | Screenshot | 240 KB | Minimal | Shows the "Electronic Health Information Export: Click Here" link on the certifications page linking to the PDF. |
| `ehi-export-link-section-screenshot.png` | Screenshot | 263 KB | Minimal | Shows certified criteria list and CQM measures. Confirms use of NewCropRx and Surescripts for clinical interoperability. |
| `ehi-export-section-screenshot.png` | Screenshot | 262 KB | Minimal | Shows full certified criteria list including (b)(10). |

**Summary**: The entire EHI export documentation consists of a single 4-page PDF. There are no supplementary artifacts — no data dictionary, no schema, no sample export files, no field-level documentation of any kind. The 4 screenshots of the certifications page add no substantive information beyond confirming the PDF link exists.

## 3. Export Mechanics

- **Format**: ZIP file containing per-patient folders with sub-folders of C-CDA R2.1 XML documents, PDF documents (scanned paper, faxes), HTML clinical notes, and image files (JPEG/JPG/PNG)
- **Mechanism**: Application UI at Settings > Interoperability > Data Export > Generate Summaries
- **Single-patient**: Yes — select one patient via checkbox and click "Export"
- **Bulk/multi-patient**: Yes — select multiple patients via checkboxes; also supports scheduled/automated exports via "Configure Schedule" with frequency, date range, and time parameters
- **Access constraints**: Role-based access control — ineligible users are blocked from the export UI. The PDF states "A user can export the patient(s) EHI at any time without subsequent developer assistance."
- **Fees**: Not documented in the export specification; no mention of additional costs

The export produces a downloadable ZIP file with a date/time stamp. Previously generated exports can be re-downloaded from a "Data Export Summaries List" portlet on the user dashboard.

## 4. Export Content: What's In It

### What the documentation tells us

The specification states the export contains "all accessible EHI information" but provides **zero field-level detail**. The only concrete format information is:

1. **C-CDA R2.1 documents** — referenced standard: "C-CDA Templates for Clinical Notes R2.1 Companion Guide, Release 2." No indication of which C-CDA templates/sections are populated, whether vendor extensions are used, or how ZoomMD's internal data maps to C-CDA elements.

2. **PDF documents** — scanned paper and digital records of faxes from the document management system.

3. **HTML clinical notes** — clinical notes "in various forms."

4. **Image files** — JPEG, JPG, PNG files attached to patient records.

### What's absent from the documentation

There is:
- **No data dictionary** — zero tables, zero fields documented
- **No schema definition** — no XSD, JSON Schema, or structural specification
- **No sample export data** — no example C-CDA documents or sample ZIPs
- **No C-CDA section/template mapping** — impossible to know which of the ~30+ C-CDA R2.1 document templates are used
- **No entity or field inventory** — the word "field" does not appear in the document
- **No value set or terminology documentation**
- **No relationship/foreign key documentation**

### Vendor's own content organization

The vendor does not organize or categorize the export content. The documentation presents the export as an undifferentiated "ZIP file" of documents. There is no table-level, entity-level, or domain-level breakdown. The following is the entirety of what can be enumerated:

| Content Type | Format | Detail Level | Notes |
|---|---|---|---|
| Clinical documents | C-CDA R2.1 XML | None — sections/templates unspecified | Standard reference provided but no mapping |
| Scanned documents / faxes | PDF | None | From document management system |
| Clinical notes | HTML | None — note types unspecified | "Various forms" |
| Clinical images | JPEG/JPG/PNG | None | Attached to patient records |

**Entity/field count: 0 entities, 0 fields documented.** The export relies entirely on the C-CDA R2.1 standard for its structured data specification, with no vendor-specific documentation of what data populates the C-CDA or how.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no categorization of export content. The entire specification is "C-CDA documents plus document attachments." If we assume the C-CDA R2.1 export follows standard clinical document templates, it would *at minimum* cover the USCDI v1 data elements (demographics, problems, medications, allergies, lab results, vitals, immunizations, procedures, clinical notes, care team, goals, health concerns). However, there is no vendor-specific confirmation of which C-CDA sections are populated or how complete they are.

The inclusion of PDF/scanned documents and HTML clinical notes suggests the export goes somewhat beyond pure C-CDA by including the document management system content and rendered clinical notes. This addresses document-level completeness but not structured data completeness.

Critically, there is **no mention** of billing, insurance, scheduling, superbills, claims, referrals, patient portal messages, or any practice management data in the export. Given that ZoomMD is an integrated EHR+PM system with billing as a core module, this is a significant omission.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Presumed present in C-CDA header; no field-level confirmation | C-CDA typically includes basic demographics; likely present but depth unknown |
| Encounters / visits | ⚠️ Partial | Presumed present if C-CDA includes encounter documents; no confirmation | ZoomMD stores encounters; unknown if export captures encounter-level data vs. summary documents |
| Problems / conditions | ⚠️ Partial | Presumed present in C-CDA Problem section; no confirmation | Standard C-CDA section; likely present but completeness unknown |
| Medications / prescriptions | ⚠️ Partial | Presumed present in C-CDA Medications section; no confirmation | ZoomMD has robust e-prescribing (EPCS, NewCropRx); unclear if full Rx history vs. active meds |
| Allergies | ⚠️ Partial | Presumed present in C-CDA Allergies section; no confirmation | Standard C-CDA section; likely present |
| Immunizations | ⚠️ Partial | Presumed present in C-CDA Immunizations section; no confirmation | ZoomMD certified for immunization registry reporting; likely present |
| Vitals | ⚠️ Partial | Presumed present in C-CDA Vital Signs section; no confirmation | Standard C-CDA section; likely present |
| Lab results | ⚠️ Partial | Presumed present in C-CDA Results section; no confirmation | ZoomMD has lab module with national lab connectivity; depth in export unknown |
| Imaging / diagnostic reports | ⚠️ Partial | Image files (JPEG/JPG/PNG) included; structured imaging orders unclear | Images exported as attachments; radiology report structure unknown |
| Procedures | ⚠️ Partial | Presumed present in C-CDA Procedures section; no confirmation | Standard C-CDA section; likely present |
| Clinical notes / documents | ✅ Covered | C-CDA documents + HTML clinical notes + PDF scanned documents | Most explicitly addressed domain; multiple format types included |
| Care plans / goals | ⚠️ Partial | Presumed present if C-CDA includes Plan of Treatment; no confirmation | C-CDA R2.1 supports this; presence in ZoomMD's export unknown |
| Orders / referrals | ❌ Not covered | No mention of orders or referrals in export documentation | ZoomMD UI shows Referrals panel (visible in PDF screenshots); not addressed in export |
| Insurance / coverage | ❌ Not covered | No mention of insurance data in export | ZoomMD verifies insurance eligibility at check-in; significant gap |
| Claims / billing | ❌ Not covered | No mention of billing, claims, superbills, or charges | ZoomMD has integrated billing module with superbills, claims tracking; **major gap** |
| Payments | ❌ Not covered | No mention of payment data | ZoomMD tracks patient balances and collections; significant gap |
| Consents / directives | ❌ Not covered | No mention of advance directives or consent documents | May be in scanned PDFs if captured on paper; no structured data |
| Patient communications / portal messages | ❌ Not covered | No mention of patient portal data or messages | ZoomMD has patient portal with messaging; gap |
| Specialty-specific data | ❌ Not covered | No mention of specialty assessments or custom forms | ZoomMD serves 40+ specialties with custom charting; gap if specialty templates store structured data beyond C-CDA |

**Summary**: 1 domain (clinical notes/documents) has confirmed coverage. 10 domains have presumed partial coverage via C-CDA but zero vendor confirmation. 7 domains that ZoomMD stores data for have no evidence of coverage in the export.

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the worst possible while still technically existing.

- **Usability for a developer**: A developer receiving this export would know only that they're getting a ZIP with C-CDA XML files and some document attachments. They would need to reverse-engineer the C-CDA structure from the files themselves. There is no vendor-specific guidance on data mapping, custom extensions, or content expectations.

- **What's documented**: The UI workflow for initiating an export (which patients can select, where to click). This is user documentation, not a format specification.

- **What requires guesswork**: Everything about the actual data content — which C-CDA sections are populated, what fields they contain, whether the C-CDA follows standard templates or includes vendor-specific data, what types of HTML clinical notes are included, how document attachments relate to clinical records.

- **Machine-readable artifacts**: None. No schemas, no sample data, no structured metadata.

- **Could a developer build an import?**: Only by treating the export as generic C-CDA R2.1 + document attachments. Any ZoomMD-specific data or structure would be lost because it's undocumented.

The 4-page PDF is primarily a set of screenshots showing how to click buttons in the UI. The "Format Specification" title is misleading — this is a user guide for initiating exports, not a specification of what data is exported or how it's structured.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is explicitly C-CDA R2.1 plus document attachments. This is a projection of the vendor's internal data into a clinical document standard. C-CDA covers a defined subset of clinical data (demographics, problems, medications, allergies, labs, vitals, immunizations, procedures, notes) but does not cover billing, insurance, practice management, custom specialty data, or patient portal communications — all of which ZoomMD stores. There is no evidence of any native data model export or vendor-specific data beyond what C-CDA provides.

### Key Findings

1. **The export is C-CDA R2.1 repackaged as "(b)(10)"**: The format specification explicitly names C-CDA R2.1 as the structured data format. This covers only the clinical summary portion of what ZoomMD stores — a classic failure mode where the existing Transitions of Care / (b)(1) export is repurposed as the EHI export. The product's billing module, insurance verification, superbills, claims, referrals, patient portal messages, and specialty-specific structured data are not addressed.

2. **Zero field-level documentation**: The entire "format specification" is 4 pages with ~300 words of actual specification text and 11 UI screenshots. There is no data dictionary, no schema, no entity list, no field inventory — the word "field" does not appear in the document. This makes it impossible to verify what data is actually exported without obtaining a sample export file.

3. **Billing and PM data appear entirely absent**: ZoomMD is an integrated EHR+PM system with billing as a core feature (superbills, claims tracking, insurance eligibility, collections). The PDF screenshots even show a "Superbills Status" indicator in the UI. Yet the export documentation makes zero mention of any billing, insurance, or practice management data. This is a significant gap for a product whose value proposition includes integrated billing.

4. **The documentation is a UI walkthrough, not a format specification**: Despite being titled "EHI Export Format Specification," the document describes *how to click buttons* to initiate an export, not *what data is in the export*. It reads as a minimal compliance artifact rather than a genuine technical specification.

5. **Document attachments are a positive signal**: The inclusion of PDF scanned documents, HTML clinical notes, and image files alongside C-CDA suggests the export goes slightly beyond a pure clinical summary by incorporating the document management system content. However, these are unstructured attachments, not queryable data.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA R2.1 XML + PDF + HTML + images in ZIP
Model type:      Standard projection (C-CDA)
Entities:        0 (no data dictionary)
Fields:          0 (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (multi-patient + scheduled)
Domains covered: 1 confirmed + 10 presumed of 18 applicable domains
```

### Bottom Line

ZoomMD's EHI export is a C-CDA R2.1 clinical document export repackaged as its (b)(10) offering, accompanied by a 4-page PDF that documents how to click the export button but not what data is exported. A patient would likely receive their clinical summary (problems, meds, allergies, labs, notes) but would almost certainly be missing their billing records, insurance information, claims history, and any specialty-specific structured data — all of which ZoomMD stores. The single biggest gap is the complete absence of billing/PM data from an integrated EHR+PM system.

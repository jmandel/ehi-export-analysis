# EHI Export Analysis: Infor-Med Medical Information Systems Inc.

**Product**: Praxis EMR Version 9
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.2766.INFO.01.02.1.220310

## 1. Product Context

Praxis EMR is a full ambulatory EHR system targeting solo practitioners and small independent practices across 90+ specialties. Its core differentiator is a "template-free" AI-driven documentation approach (the "Concept Processor") where the system learns from each physician's natural language charting patterns rather than using pre-built templates. It runs on Oracle or Microsoft Access databases.

Key data domains the product stores:

- **Clinical documentation**: Free-text narrative encounter notes with embedded discrete data via the "Datum+" engine, problem lists, assessments, treatment plans
- **Medications/prescriptions**: Full e-prescribing via Surescripts including EPCS, refill workflows, PDMP integration
- **Lab data**: Orders and results via HL7 interfaces with 20+ lab systems
- **Documents/images**: Scanned documents and attachments via PraxDocs
- **Patient demographics**: Bidirectionally synced with external practice management systems
- **Patient portal**: Messages, intake forms, self-scheduling, secure messaging
- **Billing/coding**: PraxCoder for E&M coding optimization; interfaces with 34+ billing/PM systems for superbill/charge transmission (billing itself is external)
- **Quality reporting**: Datum+ discrete parameters for CQM/MIPS reporting
- **Clinical decision support**: Practice guidelines, clinical advisories
- **Scheduling**: Appointments, AI-driven self-scheduling
- **Messaging**: Secure Direct messaging, Smart Agent automated communications

Notably, billing and practice management are handled by external systems — Praxis is an EHR, not a PM system. However, it does store coding data (PraxCoder) and transmits charges to external billing systems.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Infor-Med-Medical-Information-Systems-DataExportDocumentation.pdf` | 10-page PDF (effectively ~7 pages of content). The sole EHI export documentation. Procedural guide with screenshots showing how to use the Praxis Data Export Utility. Describes output file types and folder structure. Revision date Nov 14, 2023. Created from Google Docs (Skia/PDF m125 renderer). | **Primary artifact** — only source of export documentation |
| `downloads/certifications-page-screenshot.png` | Screenshot of the certification disclosures page showing the EHI export download link. | Low — confirms access path only |
| `downloads/onc-cert-doc.pdf` | 3-page CHPL CMS EHR ID certificate listing Praxis EMR v8 and EMR Direct Interoperability Engine as compound certification. | Low — confirms certification scope |
| `downloads/praxis-cert.pdf` | 2-page SLI Compliance ONC certification certificate for Praxis EMR v9. Lists 34 certified criteria including (b)(10). Updated June 5, 2025. | Low — confirms (b)(10) certification |

The only substantive artifact is the export documentation PDF. There are **no data dictionaries, schemas, sample data files, or technical specifications** among the artifacts.

## 3. Export Mechanics

- **Format**: Hybrid — C-CDA XML for clinical summaries + Microsoft Word .doc files for narrative text + original-format attachments (PDF, XLSX, PNG, etc.) + HTML index page for demographics
- **Mechanism**: Desktop utility ("Praxis Data Export Utility") accessible from the Praxis Control Panel. Manual operation only — no API or programmatic access.
- **Single-patient**: Yes — "Only Selected" option exports one patient by chart number
- **Bulk**: Yes — "Export All" exports all patients. Supports resume via "Continue from selected" after interruption.
- **Access constraints**: No fees documented. The utility appears to be available to any user with access to the Praxis Control Panel.
- **Output**: Folder hierarchy with `index.html` (patient index) and per-patient subfolders containing CDA Files and doc/attachment files.

Three export options (checkboxes, can be combined):
1. **Export Patient Summary** — CDA XML + HTML rendering per patient
2. **Export Documents** — All visit text (.doc), inserted note text (.doc), and attachments in original format
3. **Export Visit Summaries** — Per-visit CDA XML + HTML rendering

## 4. Export Content: What's In It

The documentation provides **no data dictionary**. There are no field-level specifications for the CDA documents, no enumeration of CDA sections populated, no template IDs, no value sets, and no sample data. The only field-level information is the description of the `index.html` demographics page.

### Vendor's own content organization

The export produces 8 distinct output file types across 5 categories:

| Entity/File Type | Documented Fields | Format | Category (vendor's) |
|---|---|---|---|
| `index.html` | 12 | HTML | Demographics / Patient Index |
| `PatientSummary.xml` | 0 (undocumented) | CDA XML | Clinical Summary |
| `PatientSummary.xml.html` | 0 (undocumented) | HTML | Clinical Summary (readable) |
| `VisitSummary.xml` | 0 (undocumented) | CDA XML | Visit Summary |
| `VisitSummary.xml.html` | 0 (undocumented) | HTML | Visit Summary (readable) |
| `Visit.doc` | 0 (unstructured) | DOC | Visit Narrative |
| `InsertedNote.doc` | 0 (unstructured) | DOC | Inserted Notes |
| `InsertedNote_attachments` | 0 (binary) | Original format | Attachments |

**Total documented fields: 12** (all in `index.html` demographics).

The 12 demographics fields explicitly documented in `index.html` are: Patient Name, Chart Number, Date of Birth, Date of Death, Status (Active/Inactive), Gender, SSN, Last Attending Physician, Primary Physician, Referring Physician, Address, Phone Numbers.

The CDA documents would contain structured clinical data per the C-CDA standard (problems, medications, allergies, vitals, labs, procedures, immunizations, etc.), but the documentation does not specify which sections are populated, which templates are used, or what coded values appear. Without sample data, the actual CDA content is unknowable from the documentation alone.

The .doc files contain the physician's unstructured narrative text — the core of Praxis's Concept Processor output. This captures the full clinical narrative but loses all discrete/structured data (Datum+ parameters).

Full inventory saved to `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes three categories of export output:

1. **CDA summaries** (patient-level and visit-level): These would contain whatever C-CDA sections Praxis populates, presumably the standard clinical summary sections. The documentation calls these "complete patient summary" and "suitable for importing into another EMR compliant with the standard certified by ONC," suggesting standard C-CDA Continuity of Care Document content. However, the documentation provides zero detail about which sections, what data depth, or what coded values.

2. **Document/narrative files** (.doc): These capture the full text of every visit and every inserted note. For a narrative-driven EMR like Praxis where the Concept Processor is the core documentation method, this is the most complete clinical record component. However, it exports as unstructured text — the discrete Datum+ parameters embedded in the narrative are lost as structured data.

3. **Attachments**: Files attached to inserted notes are exported in original format. This covers scanned documents, imported PDFs, images, etc. from PraxDocs.

The demographic index.html provides basic patient identification data but is shallow (12 fields — no insurance, no emergency contacts, no language/ethnicity/race, no consent status).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `index.html` with 12 fields (name, DOB, gender, SSN, address, phone, physician assignments) | Present but thin — no race, ethnicity, language, insurance, emergency contacts. Product syncs demographics bidirectionally with PM systems, so more fields likely exist internally. |
| Encounters / visits | ⚠️ Partial | `Visit.doc` files (one per visit) + `VisitSummary.xml` (CDA per visit) | Visit text is exported as unstructured narrative. Visit metadata (date/time in filename) is minimal. No structured encounter data documented (visit type, duration, disposition, billing codes). |
| Problems / conditions / diagnoses | ⚠️ Partial | Presumably in CDA `PatientSummary.xml` | Undocumented — would depend on CDA section content. Problem lists likely in CDA but depth unknown. |
| Medications / prescriptions | ⚠️ Partial | Presumably in CDA `PatientSummary.xml` | CDA may contain current medication list, but full prescription history, refill workflows, EPCS records, PDMP queries are unlikely to be in a CDA summary. Product has deep Surescripts/EPCS integration — significant potential gap. |
| Allergies | ⚠️ Partial | Presumably in CDA `PatientSummary.xml` | Likely present in CDA but depth undocumented. |
| Immunizations | ⚠️ Partial | Presumably in CDA `PatientSummary.xml` | Likely present in CDA but depth undocumented. |
| Vitals | ⚠️ Partial | Presumably in CDA `PatientSummary.xml` or `VisitSummary.xml` | Likely present in CDA but depth undocumented. |
| Lab results | ⚠️ Partial | Presumably in CDA summaries | CDA may contain lab results but unclear if full history from 20+ lab integrations is captured vs. latest values only. Lab orders likely not included. |
| Imaging / diagnostic reports | ⚠️ Partial | May appear as inserted notes/attachments | No structured imaging data documented. Reports may exist as scanned attachments. |
| Procedures | ⚠️ Partial | Presumably in CDA `PatientSummary.xml` | Likely present in CDA but depth undocumented. |
| Clinical notes / documents | ✅ Covered | `Visit.doc` + `InsertedNote.doc` + attachments | This is the strongest domain — full visit narrative text and all inserted notes with attachments are exported. However, they are unstructured .doc files, not structured data. |
| Care plans / goals | ⚠️ Partial | May be in CDA summaries or visit narratives | Undocumented. May appear in narrative text. |
| Orders / referrals | ❌ Not covered | No evidence in export documentation | Product supports lab orders and referrals; no export mechanism documented for order data. |
| Insurance / coverage | ❌ Not covered | Not mentioned in export documentation | Product stores insurance data (synced with PM systems). Not in export. |
| Claims / billing | N/A | N/A | Billing is handled by external PM systems, not stored in Praxis itself. PraxCoder coding data (see below) is internal. |
| Payments | N/A | N/A | Payments handled by external PM systems. |
| Coding (PraxCoder) | ❌ Not covered | Not mentioned in export documentation | PraxCoder E&M coding suggestions and superbill data generated within Praxis are not documented as part of the export. |
| Patient communications / portal messages | ❌ Not covered | Not mentioned in export documentation | Product has patient portal with messaging, intake forms, reminders. None included in export. |
| Consents / directives | ❌ Not covered | Not mentioned in export documentation | Consent forms from patient portal intake not included. |
| Quality measures (Datum+) | ❌ Not covered | Not mentioned in export documentation | Datum+ discrete parameters embedded in narrative are exported only as unstructured text in .doc files — the structured quality data is lost. |
| Scheduling | N/A | N/A | Appointment data is operational/administrative, not EHI per scope reference. |

**Summary**: Of 16 applicable EHI domains, 1 is well covered (clinical notes/documents), 9 are partially covered (likely present in CDA but undocumented), and 6 are not covered (orders, insurance, coding, portal data, consents, quality measures).

## 6. Documentation Quality

The documentation is a **procedural user guide** — it tells users how to click buttons in the export utility. It does not tell developers, patients, or recipients what data the export contains.

**What's well-documented:**
- How to launch and use the export utility (clear screenshots, step-by-step)
- File naming conventions and folder structure
- The three export option categories

**What requires guesswork:**
- Which CDA sections are populated (completely undocumented)
- What structured data fields exist in the CDA documents
- What template IDs or CDA conformance level is used
- Whether the CDA captures full history or just current/summary data
- What Datum+ discrete parameters look like in the export
- The completeness of any clinical domain

**Machine-readable artifacts**: None. No schemas, no sample CDA files, no template definitions, no value sets.

**Could a developer build an import from this documentation?** No. A developer would need to receive an actual export and reverse-engineer the CDA structure. The .doc files are unstructured text with no documented format. The only parseable specification is the file naming convention.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to determine actual export coverage. What is documented suggests the export captures: (a) C-CDA clinical summaries of unspecified depth, (b) full visit narrative text, and (c) document attachments. This likely captures the core clinical documentation — which is the heart of Praxis's value proposition — but the complete absence of field-level documentation makes it impossible to assess CDA content depth. Meanwhile, several data domains the product stores (e-prescribing history, patient portal data, PraxCoder coding data, orders, insurance information) have no documented export mechanism. The 12-field demographics in `index.html` is notably shallow for a product that stores full patient demographics synchronized with PM systems.

**Axis 2 — Export approach: Repackaged existing export**

The export is built from existing capabilities rather than a purpose-built EHI mechanism:
- The CDA patient summaries and visit summaries are the same C-CDA documents used for transitions of care [(b)(1)/(b)(2) certification criteria] — the documentation explicitly says they are "suitable for importing into another EMR compliant with the standard certified by ONC."
- The .doc visit text files are essentially the same content a user would print from the chart.
- No billing, coding, portal, or operational data is exported — only the clinical exchange surface.
- There is no product-specific data dictionary; the CDA output is described generically with no indication of vendor-specific extensions or additional data beyond standard C-CDA.
- The documentation makes no mention of exporting data beyond what's in the standard clinical summary, strongly suggesting this is the existing C-CDA export repackaged as (b)(10).

The combination of C-CDA summaries + narrative .doc files is somewhat more than a pure C-CDA repackage (the .doc visit text does add the full narrative beyond what C-CDA captures), but the overall approach is clearly to assemble existing export capabilities rather than build a comprehensive EHI extraction.

### Key Findings

1. **No data dictionary exists.** The entire EHI export documentation is a 10-page procedural guide with screenshots. There is zero field-level documentation for the CDA documents, no schema, no sample data, and no specification of which CDA sections are populated. Only the 12 demographic fields in `index.html` are explicitly named (PDF page 7).

2. **The CDA export appears to be the existing transitions-of-care C-CDA repackaged.** The documentation describes CDA summaries "suitable for importing into another EMR compliant with the standard certified by ONC" — language that points directly to the (b)(1)/(b)(2) transitions of care CDA, not a purpose-built EHI export.

3. **Clinical narrative is the export's strongest component.** Visit text exported as .doc files captures the full Concept Processor narrative for every visit and inserted note, plus attachments in original format. For a narrative-focused EMR, this is meaningful — but it's unstructured text, not discrete data.

4. **Multiple EHI domains the product stores are absent from the export.** E-prescribing history (Surescripts/EPCS), patient portal data (messages, intake forms), PraxCoder coding data, orders, and insurance information are all stored by Praxis but not mentioned anywhere in the export documentation.

5. **Structured discrete data (Datum+) is lost.** The Datum+ engine embeds discrete clinical parameters in narrative text for quality reporting. The .doc export preserves the text but loses the structured parameter values, meaning CQM/MIPS data cannot be extracted from the export in discrete form.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML + DOC + HTML + original-format attachments
Entities:        8 output file types (no data dictionary)
Fields:          12 documented (demographics in index.html only)
Descriptions:    100% of the 12 documented fields; 0% of CDA content
Sample data:     No
Bulk export:     Yes (all patients with resume capability)
Domains covered: 1 of 16 well covered; 9 of 16 partially (undocumented CDA)
```

### Bottom Line

A patient or provider receiving this export would get their full clinical narrative text (the core of Praxis's documentation) plus C-CDA clinical summaries and document attachments — enough to read the clinical record but insufficient for structured data migration or complete EHI transfer. The single biggest gap is the complete absence of documentation: without a data dictionary, schema, or sample data, it is impossible to verify what the CDA documents actually contain, and several data domains the product stores (prescribing history, portal data, coding data, orders, insurance) appear to be entirely missing from the export.

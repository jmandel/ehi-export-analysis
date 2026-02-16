# Infor-Med Medical Information Systems Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.praxisemr.com/certifications-and-costs.html
- CHPL IDs: 10853
- Product: Praxis EMR Version 9
- Certification Date: 2022-03-10

## Navigation Journal

1. **Initial probe** — HTTP HEAD request confirmed the page is live (HTTP 200, `text/html`, 62KB, served through Sucuri/Cloudproxy WAF):
   ```bash
   curl -sI -L "https://www.praxisemr.com/certifications-and-costs.html" \
     -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'
   ```

2. **Fetched the page** and searched for download links:
   ```bash
   curl -sL "https://www.praxisemr.com/certifications-and-costs.html" \
     -H 'User-Agent: Mozilla/5.0' -o /tmp/praxis-page.html
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|csv|json)[^"]*"' /tmp/praxis-page.html
   ```
   Found these PDF links:
   - `downloads/press_releases_downloads/Infor-Med-Praxis-EMR-v9-5-ONC-Certified-Health-IT.pdf` (press release)
   - `downloads/press_releases_downloads/Infor-Med-Praxis-EMR-v9-ONC-Certified-Health-IT.pdf` (press release)
   - `downloads/clients_downloads/Infor-Med-Medical-Information-Systems-DataExportDocumentation.pdf` — **EHI Export documentation**
   - `downloads/clients_downloads/ONC-Certification-Document.pdf` (certification document)

3. **Downloaded the EHI export PDF** — the only EHI-specific document on the page:
   ```bash
   curl -sL "https://www.praxisemr.com/downloads/clients_downloads/Infor-Med-Medical-Information-Systems-DataExportDocumentation.pdf" \
     -H 'User-Agent: Mozilla/5.0' \
     -o downloads/Infor-Med-Medical-Information-Systems-DataExportDocumentation.pdf
   ```
   Verified: `file` command confirms PDF document, version 1.4, 10 pages, 690KB. Produced by "Skia/PDF m125 Google Docs Renderer" (created from Google Docs). Titled "Infor-Med Medical Information Systems_DataExportDocumentation."

4. **Examined the page in a browser** — the "Certification Disclosures and Costs" page has a prominent blue button labeled "Electronic Health Information Export" that links directly to the PDF. The page also lists all certified criteria (including b(10)) in a table, plus clinical quality measures. No additional EHI-related content, accordions, or hidden sections.

5. **Checked the costs-and-limitations page** for any additional EHI content — none found.

6. **Checked the PDF for embedded URLs** — only `https://www.praxisemr.com/` (the vendor homepage). No embedded attachments.

## What Was Found

The entire EHI export documentation consists of a single 10-page PDF: **"Infor-Med Medical Information Systems_DataExportDocumentation"** (revision date November 14, 2023).

### Export Mechanism

Praxis EMR provides a **"Praxis Data Export Utility"** — a desktop application accessible from the Praxis Control Panel. The utility is a Windows application (screenshots show a standard Windows form). Key features:

1. **Patient selection**: Export all patients, continue from a selected patient (useful for resuming interrupted exports), or export a single selected patient by chart number.

2. **Output folder**: User selects a local filesystem directory for export output.

3. **Three export options** (checkboxes, all can be selected simultaneously):
   - **Export Patient Summary**: Complete patient summary in CDA (C-CDA) XML format + human-readable HTML
   - **Export Documents**: All patient documentation including:
     - Text from all visits (as .doc files)
     - Text from all inserted notes (as .doc files)
     - Attachments from inserted notes in original format (PDF, XLSX, PNG, etc.)
   - **Export Visit Summaries**: Per-visit summary in CDA format + human-readable HTML

4. **Progress tracking**: The utility shows total patients found, processed count, and per-patient status. It can be stopped and resumed.

### Export Output Structure

The export produces a folder structure:
```
[Export Folder]/
├── index.html                    # Patient index with demographics
├── [Patient Folder Name]/        # One folder per patient
│   ├── CDA Files/
│   │   ├── ..._PatientSummary.xml
│   │   ├── ..._PatientSummary.xml.html
│   │   ├── YYYY-MM-DD-HH-MM_..._VisitSummary.xml
│   │   └── YYYY-MM-DD-HH-MM_..._VisitSummary.xml.html
│   ├── YYYY-MM-DD-HH-MM_..._Visit.doc
│   ├── YYYY-MM-DD-HH-MM_..._InsertedNote.doc
│   └── YYYY-MM-DD-HH-MM_..._InsertedNote_file0.png
└── [error logs if any]
```

Patient folder naming convention: `LASTNAME_[LASTNAME]_[MIDDLENAME]_FIRSTNAME_GENDER_(REG_NO)_MM-DD-YYYY`

The **index.html** file serves as a master index listing all exported patients with: name, chart number, DOB, date of death (if applicable), Active/Inactive status, gender, SSN, last attending physician, primary physician, referring physician, and full demographic information (address, phone numbers).

### Export Formats

- **CDA XML** (.xml) — C-CDA format for patient summaries and visit summaries, described as "suitable for importing into another EMR compliant with the standard certified by ONC"
- **HTML** (.xml.html) — Human-readable renderings of the CDA documents
- **DOC** (.doc) — Microsoft Word format for visit text and inserted note text
- **Original format** — Attachments exported in their original format (PDF, XLSX, PNG, etc.)

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, Praxis EMR stores the following data categories. Here is what the export covers:

**Clearly covered:**
- **Clinical encounter notes/visit text** — All visit text exported as .doc files. This is the core of Praxis's data, and the export captures the full narrative text from every visit.
- **Inserted notes** — All note text and attachments exported in original formats.
- **Patient summaries** — CDA format captures structured clinical data (problems, medications, allergies, labs, vitals, etc.) as defined by C-CDA.
- **Documents and images** — Attachments from inserted notes exported in original format (PDF, XLSX, PNG, etc.) via the PraxDocs integration.
- **Demographics** — The index.html includes comprehensive demographics: name, DOB, gender, SSN, status, physicians, address, phone numbers.

**Partially covered / ambiguous:**
- **Medications and prescriptions** — Likely included in the CDA patient summary (which would contain a medication list per the C-CDA standard), but the documentation does not specifically enumerate which CDA sections are populated. The full prescription history, refill requests, and EPCS records may not be fully captured in a summary CDA.
- **Lab results** — Similarly likely in the CDA summaries, but unclear if the full history of all lab results (from 20+ lab integrations) is included versus just the latest values.
- **Quality reporting data (Datum+)** — The Datum+ discrete data parameters embedded in narrative notes would be exported as part of the visit text (.doc files), but only as free text — the discrete, structured parameter values that drive quality measure reporting may not be preserved in a machine-readable way.

**Likely missing / not mentioned:**
- **E-prescribing history** — Full Surescripts prescription transmission history, PDMP queries, refill request workflows. Not mentioned in the export documentation.
- **Patient portal data** — Portal messages, intake forms, self-scheduled appointments, patient-facing content. Not mentioned.
- **Scheduling data** — Appointment history and scheduling records. Not mentioned.
- **Billing/coding data** — PraxCoder coding suggestions, superbill/charge data, billing interface transmission records. Not mentioned.
- **Clinical decision support data** — Practice guidelines, clinical advisories, protocol configurations. Not mentioned.
- **Knowledge bases** — Per-physician Concept Processor learned patterns, shared knowledge bases from Knowledge Exchanger. Not mentioned (though these are arguably physician tools rather than patient records).
- **Messaging/communications** — Secure Direct messages, Smart Agent automated communications. Not mentioned.
- **Lab orders** — Outbound lab order history. Not mentioned separately from CDA summaries.

### Export Format & Standards

The export uses a **hybrid approach**:
- **C-CDA XML** for structured clinical summaries (patient summary and per-visit summaries)
- **Microsoft Word .doc files** for unstructured clinical narrative (visit text, inserted notes)
- **Original format preservation** for attachments

This is a pragmatic approach for a template-free, narrative-driven EMR. The CDA documents provide standardized structured data, while the .doc files preserve the full clinical narrative that is Praxis's core differentiator (the "Concept Processor" AI-driven documentation). A third party could reconstruct much of the clinical record from these files, though the separation between structured CDA and unstructured .doc means some data reconciliation would be needed.

The format is **not a database dump** — it does not export the underlying Oracle/Access database tables. This means the relational structure of the data, including the Datum+ discrete parameters, is lost in the export. The export is document-oriented rather than data-oriented.

### Documentation Quality

The documentation is a **brief user guide** (10 pages including cover, table of contents, and contact page — effectively ~7 pages of content). It includes:
- Clear screenshots of the export utility interface with numbered annotations
- Step-by-step instructions for performing the export
- File naming conventions and folder structure documentation
- Description of each export option and what it produces

**Strengths:**
- Clear, readable, well-organized
- Good screenshots showing the actual UI
- Practical: a user could follow these instructions and perform the export

**Weaknesses:**
- **No data dictionary** — there is no documentation of what fields are in the CDA documents, what sections are populated, what coded values are used, or what the .doc file content structure looks like.
- **No schema documentation** — no CDA template constraints, no field definitions, no value sets.
- **No sample data** — no example export files or sample records.
- **No information about data completeness** — the document does not state whether the export captures all electronic health information in the system or acknowledge what might be excluded.
- **No API or programmatic access** — the export is manual only, through the desktop application.

### Structure & Completeness

The documentation is purely procedural (how to run the export utility) rather than technical (what data the export contains). There is:
- No field-level documentation
- No data types, value sets, or constraints
- No entity-relationship documentation
- No versioning or change history beyond the revision date
- No discussion of CDA profile conformance or template IDs

A developer receiving an export from this system would have the C-CDA files (which are self-describing to some degree) and .doc files, but would need to reverse-engineer the actual data content. The index.html provides demographic data in an HTML table, but there is no documentation of its structure either.

### Overall Assessment

Praxis EMR has taken a **minimally compliant approach** to EHI export documentation. They have a functional export utility that produces a reasonable set of output files (CDA summaries + full narrative text + attachments), but the documentation only describes how to use the tool — not what data it exports in detail.

The export appears to cover the clinical core of the system well (visit narratives, clinical summaries, documents), but significant data domains are unaddressed: e-prescribing history, patient portal data, billing/coding data, lab orders, and messaging. The absence of a data dictionary or schema documentation makes it impossible to assess the completeness of the CDA documents without actually running the export and examining the output.

For a small, physician-centric EMR focused on clinical documentation, the narrative-heavy export approach makes sense. But the lack of technical documentation means a third party would need to do significant reverse engineering to understand and import the exported data.

## Access Summary
- Final URL (after redirects): https://www.praxisemr.com/certifications-and-costs.html
- Status: found
- Required browser: no (direct PDF link accessible via curl)
- Navigation complexity: one_click (button on certification page → PDF download)
- Anti-bot issues: none (Sucuri WAF present but did not block requests)

## Obstacles & Dead Ends
- No obstacles encountered. The page loaded cleanly, the PDF downloaded without issues.
- The costs-and-limitations.html page was checked for additional EHI content — none found.
- The PDF contained no embedded URLs to follow-on documentation and no embedded attachments.
- The page has no accordions, hidden sections, or JavaScript-dependent content related to EHI export.

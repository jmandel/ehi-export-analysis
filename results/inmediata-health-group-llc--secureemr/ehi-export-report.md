# Inmediata Health Group LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://portal.inmediata.com/2023/(b)%20(10)%20EHI%20Export_PrognoCIS%20Support_Self%20Attestation%20Document_final_Inmediata_Rev.pdf
- CHPL IDs: 11753
- Product: SecureEMR+ v4.0
- Certification date: 2026-01-16

## Navigation Journal

1. **Probed the registered URL with curl:**
   ```bash
   curl -sI -L 'https://portal.inmediata.com/2023/(b)%20(10)%20EHI%20Export_PrognoCIS%20Support_Self%20Attestation%20Document_final_Inmediata_Rev.pdf' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
   ```
   Result: HTTP 200, Content-Type: application/pdf, Content-Length: 1182354 bytes. Direct PDF download — no redirects.

2. **Downloaded the PDF:**
   ```bash
   curl -sL 'https://portal.inmediata.com/2023/(b)%20(10)%20EHI%20Export_PrognoCIS%20Support_Self%20Attestation%20Document_final_Inmediata_Rev.pdf' -H 'User-Agent: Mozilla/5.0' -o downloads/ehi-export-prognocis-self-attestation.pdf
   ```
   Verified with `file` command: "PDF document, version 1.7 (zip deflate encoded)". 16 pages.

3. **Checked mandatory disclosures page** at https://portal.inmediata.com/secureemr-plus/ for additional EHI documentation. The page is a WordPress/Elementor site with an accordion section labeled "Data Export 170.315(b)(10)" that links to the same PDF. No additional EHI export documents were found. A separate FHIR API document exists (SecureEMR-Denali-3.1_2015-Edition-Cures-Update-FHIR-API-Document-rev-12-2024.pdf) but is for (g)(10), not (b)(10).

4. **Extracted text from PDF** with `pdftotext` — clean extraction, text-based PDF (not scanned). Rendered key pages as images to view screenshots embedded in the document.

5. **Checked for embedded URLs and attachments** in the PDF — none found. No embedded files.

## What Was Found

The registered URL is a single 16-page PDF titled **"Electronic Health Information Data Export and User Guide"** for SecureEMR+ (Version: Denali 3.1). The document was authored by Neha Parmar (PrognoCIS/Bizmatics) and created November 16, 2023, consistent with the ONC compliance date of December 31, 2023. The PDF filename itself references "PrognoCIS Support" and "Self Attestation Document," confirming the product is built on the PrognoCIS platform.

### Export Mechanism

The document describes two export modes:

**1. Single Patient Data Export** — Available to any user with the `CuresEHIExport` role (under "Role (No Access Rights)" section of User Role Master). The user navigates to the Data Export link, selects "Single Patient," searches for and selects a patient, chooses data categories via checkboxes, and clicks EXPORT. The export is generated in background, with email notification on completion. The exported zip file appears under Settings > Configuration > Clinic > Download Files, in a "Cures EHI Export" category. The zip contains data in **.txt, .xls, and .pdf formats**.

**2. All/Multiple Patient Data Export** — Available to admin users but requires Inmediata Data Migration Team involvement ("depends on size of data, time and efforts required to manage server resources"). Users contact servicioalcliente@inmediata.com or techsupport@inmediata.com. The admin can filter by: all patients, selected patients, patients of primary/attending doctor, encounters of attending provider, patient last name range, or export to SQL file. An encounter date range can be specified. Export generates in background with email notification.

### Export Format

Data is exported as a **ZIP file** containing:
- **.xls files** (one per worksheet/data category) with tabular data
- **.txt files** (parallel text format for non-document data)
- **.pdf files** for attached documents (progress notes, letters, lab results, etc.)
- **CCD export** includes HTML and XML files (C-CDA documents)
- **SQL file option** available for admin exports (exports data as .SQL)

The exported folder structure uses patient chart folders (e.g., `APC02734/`, `CHART01/`) containing associated document files, with the .xls files referencing document paths in a `FILE` column.

### Data Categories (Worksheets)

The "Configure Export Fields" feature shows all exportable worksheets. Each worksheet has configurable fields with Field name, Name, Title, Hide, and Sequence Number options. The full list of 43+ worksheets:

**Clinical:**
- Patient Demographics, Patient Insurance
- Allergy, Current Medication, Prescriptions
- Vaccination, Health Maintenance
- Family History, Past Medical Hist, Surgery
- Social History, Vitals, All Vitals
- Lab Results, Lab Test Result Values, Rad Results
- Diagnosis Codes, CPT Codes, HCPC Codes
- Procedure Orders, Consults
- Enc Progress Notes, Procedure Notes, Old Progress Notes
- Letters, Messages
- Patient Cases, Patient Notes, Patient Alert
- CCD (Consolidated Clinical Document)

**Documents:**
- Legal Documents, Other Documents, Enc Attach Docs

**Administrative/Reference:**
- Insurance Master, Medics, Referring Provider
- Adjusters, Attorneys, Employers, Guarantor
- Future Appointments, Past Appointments

**Billing (when billing is enabled):**
- Billing Ledger, Billing Claims, Billing Charges
- Patient Advance, Statements

### Field-Level Detail

The document shows one example of the Configure Export Fields interface (for Insurance Master), displaying field names like `IM_ID`, `IM_NAME`, `IM_PAYER_ID`, `IM_ADDRESS_LINE1`, etc. For data exports, the document provides two field-list examples:
- **Allergy:** Last name, First name, Middle name, Chart no, Account no, Birth date, Allergy, Reaction, Type, Int Name, Status, Rxnorm
- **Letters:** Last name, First name, Middle name, Chart no, Account no, Birth date, Letter Date, Outward (O) Inward (I), To Name, Subject, List of To Names, List of Cc Names, List of To and Cc Names, Status Code, Status Name, FILE

No comprehensive data dictionary is provided — only these two examples and one screenshot.

### Audit Trail

The document describes an audit trail for both single-patient and multi-patient exports, accessible via Audit Trail Report with Action "Export/Download" or Menu Option "Export Data" / Action "Approve."

## Export Coverage Assessment

### Data Domain Coverage

The export's worksheet list covers a **remarkably broad set of data categories** — this is one of the more complete (b)(10) implementations in terms of declared data domains. Mapping against the product research:

**Clearly covered:**
- Patient demographics and contacts
- Insurance/enrollment information (Insurance Master, Patient Insurance)
- Diagnoses (Diagnosis Codes)
- Medications (Current Medication, Prescriptions)
- Lab results and values (Lab Results, Lab Test Result Values)
- Radiology results (Rad Results)
- Vital signs (Vitals, All Vitals)
- Allergies (Allergy)
- Immunizations (Vaccination)
- Procedures and orders (Procedure Orders, CPT Codes, HCPC Codes)
- Clinical notes (Enc Progress Notes, Procedure Notes, Old Progress Notes)
- Surgery history
- Family history, Past medical history, Social history
- Health maintenance/preventive care
- Letters and messages (correspondence)
- Documents and attachments (Legal Documents, Other Documents, Enc Attach Docs)
- Referrals/consults (Consults, Referring Provider)
- CCD/C-CDA documents
- Patient cases, notes, and alerts
- **Billing data** (Billing Ledger, Billing Claims, Billing Charges, Patient Advance, Statements) — critically, this is conditional on billing being "turned on for the clinic"

**Potentially covered but unclear:**
- E-prescribing transmission records (Prescriptions worksheet exists but unclear if EPCS/Surescripts metadata is included)
- Telemedicine session records — not explicitly listed as a worksheet
- Patient portal interactions/messages — "Messages" worksheet exists but unclear if this covers portal-specific messages
- Clinical decision support alerts/interventions — not listed
- Public health reporting submissions — not listed
- Quality measure data — not listed
- Implantable device data (certified (a)(14)) — not listed as a dedicated worksheet

**Likely missing:**
- **Scheduling data** — "Future Appointments" and "Past Appointments" are listed, so this is actually covered
- **Telemedicine records** — no dedicated worksheet
- **Provider/medics reference data** — "Medics" is listed, though this is reference data not patient-specific EHI
- **Guarantor/employer/attorney** — reference/administrative data, listed

### Key observation on billing
The billing worksheets (Billing Ledger, Claims, Charges, Patient Advance, Statements) are only available "when Billing is turned on for the clinic." Given that Inmediata processes ~85% of all medical claims in Puerto Rico and SecureClaim is deeply integrated, billing would presumably be enabled for most customers. However, the conditional nature means billing data export coverage depends on the clinic's configuration.

### Export Format & Standards

**Format:** Proprietary tabular format — XLS spreadsheets, TXT files, and associated document files (PDF, HTML, XML for CCDs) in a ZIP archive. An SQL export option also exists.

**Assessment:** This is a pragmatic, if unsophisticated, approach. XLS/TXT tabular exports are computable and can be processed by standard tools. The format is appropriate for an ambulatory EHR — it captures structured data as flat tables and preserves document attachments as files. The CCD export includes both HTML and XML (C-CDA), which is the most standardized component.

The export is **not FHIR-based** and makes no pretense of being standards-based beyond CCD. This is actually a positive signal for (b)(10) compliance — the vendor has built a dedicated bulk data export rather than repackaging their (g)(10) FHIR API. The worksheet-per-domain approach covers data that doesn't map to standard FHIR resources (billing ledger, statements, legal documents, adjusters, attorneys, etc.).

**Reconstructibility:** A third party could reconstruct the patient record from this export with moderate effort. The XLS files contain structured data with patient identifiers (chart no, account no) that serve as linking keys. Document attachments are referenced by file path in the XLS. However, relationships between entities (e.g., which billing charge relates to which encounter) would need to be inferred from overlapping fields.

### Documentation Quality

**Readability:** The 16-page document is well-organized with clear sections, screenshots of the actual UI, and step-by-step instructions. It covers both single-patient and population-level exports.

**Data dictionary:** **Very weak.** The document lists all 43+ worksheet names and shows one screenshot of the Insurance Master field configuration (with database-style field names like `IM_ID`, `IM_NAME`, `IM_PAYER_ID`). Only two export examples are given with field lists (Allergy and Letters). There is no comprehensive data dictionary documenting:
- All fields for all worksheets
- Data types
- Value sets or coded field definitions
- Cardinality or null handling
- Relationships between worksheets

The Configure Export Fields UI screenshot suggests the system stores detailed field metadata internally (Field, Name, Title, Hide, Seqn columns), but this information is not documented in the PDF.

**Developer usability:** A developer could understand the high-level export process and data categories from this document, but could not implement a reliable import without significant reverse engineering. The field names visible in the UI (e.g., `IM_PAYER_ID`, `IM_ADDRESS_WORKTEL1`) are database column names, not human-readable definitions. Without a full data dictionary, interpreting exported data would require trial and error.

**Maintenance:** The document is dated November 2023 (matching the ONC compliance deadline). Version is "Denali 3.1." No change history or versioning mechanism is evident.

### Structure & Completeness

**Granularity:** Worksheet-level documentation is comprehensive (43+ categories listed). Field-level documentation is minimal — only 2 of 43+ worksheets have their fields listed, and only in the context of export examples rather than formal definitions.

**Coded fields:** Diagnosis Codes, CPT Codes, and HCPC Codes are listed as worksheets, suggesting coded data is exported, but no documentation of code systems, value sets, or how codes are represented in the export files.

**Relationships:** No documentation of how entities relate across worksheets. Patient linking appears to be via Last name, First name, Middle name, Chart no, and Account no fields (common across export examples), but this is not formally specified.

**Versioning:** None beyond the document version (Denali 3.1).

### Overall Assessment

Inmediata/PrognoCIS has implemented a **genuine (b)(10) export** that goes well beyond the USCDI/US Core data set. The export covers 43+ data domains including billing data, legal documents, correspondence, and administrative reference data — far more than a repurposed FHIR API would provide. The export format (XLS/TXT with document attachments in ZIP) is pragmatic and computable.

The main weakness is the **near-complete absence of a data dictionary**. The documentation tells you *what categories* of data are exported but not *what the fields mean* within each category. The Configure Export Fields feature clearly contains field-level metadata (it's visible in the UI screenshot), but this metadata is not published in the documentation. This makes the export a "data dump" that requires insider knowledge or reverse engineering to fully interpret.

The population-level export requiring vendor involvement (Data Migration Team) is also a concern for the (b)(10) requirement that exports be available "without subsequent developer assistance" — though this may be a practical server-resource consideration rather than a technical limitation, and single-patient export is self-service.

## Access Summary
- Final URL (after redirects): https://portal.inmediata.com/2023/(b)%20(10)%20EHI%20Export_PrognoCIS%20Support_Self%20Attestation%20Document_final_Inmediata_Rev.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The URL was a direct, clean PDF download with no redirects, no authentication, no anti-bot measures. The mandatory disclosures page at https://portal.inmediata.com/secureemr-plus/ confirmed this is the sole EHI export documentation artifact.

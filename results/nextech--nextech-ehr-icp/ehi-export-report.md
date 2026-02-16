# Nextech — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.nextech.com/compliance/ehi-export-documentation
- CHPL IDs: 11724 (Nextech EHR / IntelleChartPRO, certified 2025-12-02), 11040 (SRS EHR / SRSPro, certified 2022-12-02)
- Developer: Nextech

## Navigation Journal

1. **Initial probe**: `curl -sI -L "https://www.nextech.com/compliance/ehi-export-documentation"` returned HTTP 200, Content-Type: text/html, hosted on HubSpot CMS via Cloudflare CDN. No redirects.

2. **Page fetch**: `curl -sL "https://www.nextech.com/compliance/ehi-export-documentation" -o /tmp/nextech-ehi-page.html` — 92KB static HTML page. No JavaScript rendering required to see content.

3. **Content examination**: The page is a simple compliance hub titled "Cures Update 170.315(b)(10) — Electronic Health Information (EHI) Export Documentation." It states: "Documentation on the §170.315(b)(10) Electronic Health Information export format for each Nextech ONC-certified solution is listed below or will be provided soon."

4. **Documentation links found**: Six direct download links organized by platform:
   - **IntelleChartPro**: PDF export doc + XLSX data dictionary
   - **Nextech Select/NexCloud**: PDF export doc + XLSX data dictionary
   - **SRSPro**: PDF export doc + XLSX data dictionary

5. **Downloads**: All six files downloaded successfully via direct curl with User-Agent header. All verified as correct file types (`file` command confirmed PDF documents and Excel 2007+ files).

6. **URL extraction from PDFs**: Only external link found was `http://www.hl7.org/ccdasearch/pdfs/Companion_Guide.pdf` (HL7 standard — not downloaded per instructions). No embedded attachments in any PDF.

7. **Full-page screenshot** captured via Chrome DevTools for visual reference.

## What Was Found

Nextech provides **genuine (b)(10) EHI export documentation** for three distinct platforms, each with its own export format, folder structure, and data dictionary. This is notably one of the better-documented EHI export implementations encountered.

### Platform 1: IntelleChartPRO (ICP) — CHPL 11724

**Export format**: Per-patient ZIP file containing:
- **JSON files** for structured clinical data (appointments, demographics, insurance, labs, procedures, referrals, refractions, specialty medications, etc.)
- **XML (C-CDA)** for standardized clinical summary per encounter
- **PDF files** for chart notes, consent forms, letters, surgery planner comments
- **JPG + TXT metadata** for documents and images
- A ReadMe file with public documentation link

**Folder structure**: Well-organized by data domain — `Patient Data/Appointments/`, `Patient Data/Encounters/YYYY-MM-DD-Time/`, `Patient Data/Documents/DocumentType/Date/`, `Patient Data/Images/FileType/Date/`, etc.

**Data dictionary**: 19 entities, 341 fields. Notable entities include Patient Demographics (71 fields), ChartNote (49 fields), Tasking_Microservice (46 fields), Refractions (31 fields), Insurance & Auth (22 fields).

**Specialty-specific content**: Glaucoma Flow Sheet Comments, Refractions, Intravitreal Injection Log Comments, Surgery Planner Comments — these reflect Nextech's ophthalmology focus and demonstrate export of specialty clinical data beyond standard USCDI.

**Export scope**: Single patient and bulk patient exports are supported. Bulk exports include Letters in a different format. Only signed encounters are exported. Empty JSON files are created for domains with no data, ensuring consistent structure.

### Platform 2: SRSPro — CHPL 11040

**Export format**: Per-patient ZIP file containing:
- **CSV files** for structured clinical data (15 CSV types: appointments, custom alerts, diagnoses, family history × 3, guarantor info, implantable devices, injections, insurance, orders, smoking status, UDFs, messages, code system names)
- **XML files** for encounter data capture (per encounter), vitals, and results
- **C-CDA XML** for standardized clinical summary
- **Documents folder** with all chart-attached documents
- A ReadMe file

**Data dictionary**: 19 entities, 427 fields. Notable entities include Orders (86 fields with detailed CPOE/HL7 mapping), Smoking Status (58 fields including screening plans), Insurance Information (38 fields), Implantable Devices (35 fields), Injections (36 fields), Diagnoses (35 fields).

**Relationship documentation**: SRSPro's docs go further than most in documenting inter-entity relationships — Orders link to Results via RequisitionId, Messages link to Documents via DocumentID, FamilyHistory links to FamilyHistoryCodes via ConceptPath, Orders link to Documents via UnstructuredDocumentId. This is critical for reconstructing a patient record from the export.

**Data handling notes**: Includes deleted records with status flags, handles "No Known Diagnoses" correctly, includes GUID-based encounter identifiers, and documents which data is duplicated between CSV/XML and CCDA (vitals, smoking status, diagnoses are in both but with different field sets).

### Platform 3: Nextech Select/NexCloud

**Export format**: Per-patient ZIP file containing:
- **CSV files** for clinical and financial data (16 CSV types: appointments, demographics, charges, payments, custom data, follow-ups, notes, insurances, recalls × 2, payment plans, PracYakker internal messages, iPad tasks, iPad notes)
- **EMN (Electronic Medical Note) PDFs** — one per encounter
- **Documents folder** — all chart-attached documents
- **iPad Documents folder** — documents from iPad application
- **C-CDA XML**
- A ReadMe file

**Data dictionary**: 16 entities, 730 fields — the most detailed of the three. Notable entities include Patient Demographics (212 fields!), Charges (140 fields), Insurances (85 fields), Appointments (52 fields), Payments (50 fields).

**Billing coverage**: The Select/NexCloud export stands out for explicit billing data inclusion — Charges, Payments, and Payment Plans are separate CSV exports with documented relationships (linked via Bill ID and Payment Plan ID). The documentation explicitly notes that practices with iPad-only PM don't include billing data since it's stored in the non-certified PM module.

**Custom data**: Exports practice-configurable custom fields (date, free text, list item, checkbox types) with actual field names as configured by the practice.

## Export Coverage Assessment

### Data Domain Coverage

Nextech's EHI export documentation represents a **serious and thorough approach to (b)(10) compliance**. This is clearly not a repackaged FHIR API — it's purpose-built export functionality that goes well beyond USCDI.

**Clearly covered domains across platforms:**
- Patient demographics (extensive — 71-212 fields depending on platform)
- Clinical encounters/chart notes (as PDFs or XML, per encounter)
- Problem lists/diagnoses (with full coding detail)
- Medications (specialty medications in ICP, CCDA medications across all)
- Allergies (via CCDA)
- Lab results (JSON in ICP, XML in SRSPro, via CCDA in Select)
- Orders (extremely detailed in SRSPro — 86 fields)
- Immunizations (via CCDA)
- Vital signs (JSON/XML + CCDA)
- Procedures (separate exports + CCDA)
- Insurance information (comprehensive — 22-85 fields)
- Referrals (detailed in ICP)
- Documents/images (exported as files with metadata)
- Patient communications (secure messages, internal messages, PracYakker)
- Implantable devices (CSV + CCDA)
- Family history (detailed in SRSPro with linked code tables)
- Consents (signed PDF forms in ICP)
- Care plans/goals (via CCDA)
- Social history / SDOH (via CCDA, including SDOH Assessment in SRSPro, SDOH Problems/Goals/Interventions in Select)
- Clinical notes by type (progress notes, H&P, discharge summaries via CCDA)
- Smoking status (extensive — 58 fields in SRSPro)
- Custom/user-defined fields (UDFs in SRSPro, Custom Data in Select)
- Billing: Charges, Payments, Payment Plans (Select/NexCloud)

**Specialty-specific data covered (ICP):**
- Glaucoma Flow Sheet Comments
- Refractions (31 fields)
- Intravitreal Injection Log Comments
- Surgery Planner Comments
- Specialty Medications

**Domains with potential gaps or ambiguity:**
- **Billing in ICP and SRSPro**: The Select/NexCloud platform explicitly exports charges, payments, and payment plans. However, the ICP and SRSPro export documentation makes no mention of billing/charges/payments data. Given that ICP has integrated billing features (EM coding, claims management, POS, payment processing, etc.), the absence of billing data from ICP's export is a notable gap. SRSPro also has PM billing but no billing CSV.
- **Inventory data**: ICP is described as having inventory management (automated planning, purchasing, tracking) — this is not mentioned in any export.
- **Lead/CRM data**: ICP includes lead management, marketing campaign tracking, and CRM tools. None of this appears in the export. While CRM/lead data may not be part of the designated record set in most cases, patient-linked communications could be.
- **Cosmetic/aesthetic data**: ICP supports quotes, packages, gift cards — none exported. Cosmetic quotes and packages linked to patients could arguably be part of the billing record.
- **TouchMD visual consultation content**: Not mentioned in exports. If TouchMD images/consultation data is integrated into the patient chart, it should be exported.
- **Telehealth session data**: No mention of telehealth-specific data in any export (session records, virtual visit metadata).
- **E-prescribing data**: While medications appear in CCDA, there's no mention of detailed prescription/e-prescribing records (pharmacy selections, fill history, prior authorizations).
- **Clinical images in SRSPro**: SRSPro's PACS integration suggests image-heavy workflows, but the export documentation doesn't specifically address PACS images vs. chart-attached documents.

### Export Format & Standards

The export uses a **hybrid approach** that is well-suited to the (b)(10) requirement:

- **C-CDA XML** provides standardized representation of core clinical data (allergies, medications, problems, labs, vitals, immunizations, procedures, etc.) — this covers the USCDI slice in a standard format.
- **Platform-specific structured data** (JSON for ICP, CSV for SRSPro and Select) captures data that doesn't fit in C-CDA — appointments, insurance, specialty clinical data, communications, billing, custom fields.
- **PDFs** for chart notes/encounters — these preserve the visual layout that clinicians created, though they are less computable.
- **Document/image files** with metadata — the actual attachments.

This is a thoughtful design. The C-CDA handles standardized clinical data, while the JSON/CSV files handle everything else. The documentation explicitly notes where data overlaps between C-CDA and structured files (e.g., vitals, diagnoses, smoking status appear in both, with the structured export having more fields).

**Relationship documentation** is a strength, particularly in SRSPro — the docs explain how to join Orders to Results (via RequisitionId), Messages to Documents (via DocumentID), and Family History to Codes (via ConceptPath). This is essential for a third party to reconstruct the patient record.

**Format appropriateness**: Good. JSON/CSV/XML are computable and parseable. PDFs for encounters are less ideal but reflect the reality that encounter notes are highly customizable and layout-dependent. The ZIP structure with consistent folder naming makes the export self-describing.

### Documentation Quality

**Readable and navigable**: Yes. Each platform has a clear PDF explaining the export structure, followed by an XLSX data dictionary with per-entity sheets. The documentation is well-organized.

**Field-level definitions**: Present across all three dictionaries but vary in depth:
- Select/NexCloud is the most detailed (730 fields, with notes on data types, relationships, and edge cases)
- SRSPro has good field-level detail especially for complex entities (orders, encounter XML)
- ICP is the least detailed of the three (341 fields) but still provides field names, descriptions, and notes

**Data types**: Not formally specified (no column for data type in any dictionary). You can infer types from descriptions and notes, but there are no explicit type declarations (string, integer, date, boolean, etc.).

**Value sets / coded fields**: Partially documented. SRSPro includes a CodeSystemNames.csv mapping VocabularyIDs to OIDs. The ICP dictionary occasionally notes enumerated values in the "Note" column (e.g., "Routine, High, Urgent" for priority). But systematic value set documentation is lacking across all three platforms.

**Worked examples / sample data**: The ICP PDF includes a screenshot of an example ZIP folder structure. No sample export files or example data records are provided for any platform.

**Developer implementability**: A developer could implement a basic import from these exports using the documentation — the folder structures are clear, the field names are descriptive, and the relationships are documented (especially in SRSPro). However, the lack of formal schemas (JSON Schema, XSD, OpenAPI), data type specifications, and sample data means there would be significant trial-and-error required.

### Structure & Completeness

**Field-level granularity**: Field names and descriptions for every exported field across all three platforms. This is above average for EHI export documentation.

**Cardinality**: Not documented. Whether a field is required, optional, or repeating is not specified.

**Versioning**: No version numbers on the data dictionaries. The PDFs have dates in filenames (10.30.25, 2025). No change history.

**Cross-platform consistency**: The three platforms use different export formats (JSON vs CSV vs XML for the same data types), different field naming conventions, and different entity structures. This reflects the reality that they are distinct software systems with separate databases, but it means there is no unified "Nextech EHI export format" — each platform must be understood independently.

## Summary Assessment

Nextech's EHI export documentation is **well above average** for the (b)(10) requirement. Key strengths:

1. **Genuine (b)(10) scope**: This is clearly not a (g)(10) FHIR API relabeled. The exports include data far beyond USCDI — insurance details, specialty clinical data (glaucoma, refractions, injections), communications, custom fields, and (for Select) billing data.

2. **Three-platform coverage**: Documentation covers all three certified platforms (ICP, SRSPro, Select/NexCloud) with platform-specific detail, acknowledging their distinct architectures.

3. **Structured + standard hybrid**: The C-CDA plus JSON/CSV/XML approach is smart — it gives you standardized data where standards exist and raw structured data where they don't.

4. **Relationship documentation**: Especially in SRSPro, the documentation explains how to join related data across files — this is rare and valuable.

5. **Realistic scope notes**: The documentation acknowledges that encounter note formats are customizable and practice-dependent, that iPad practices have different data boundaries, and that PM-only data isn't in the EHR export. This honesty helps consumers understand what they're working with.

The main weakness is the **absence of billing data from ICP and SRSPro exports**, despite both platforms having integrated billing. The Select/NexCloud platform shows Nextech knows how to export billing (Charges: 140 fields, Payments: 50 fields), so the gap in ICP and SRSPro appears to be an implementation gap rather than a design decision. There are also no formal schemas, no sample data files, and no data type specifications — the documentation tells you what fields exist but not precisely how to parse them programmatically.

## Access Summary
- Final URL (after redirects): https://www.nextech.com/compliance/ehi-export-documentation
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: direct_link (all 6 files linked from single page)
- Anti-bot issues: none (standard User-Agent sufficient)

## Obstacles & Dead Ends
None. The documentation page was straightforward — a single compliance page with six direct download links to HubSpot-hosted files. No JavaScript rendering needed, no accordion expansion, no login walls, no Cloudflare challenges. This is an exemplary approach to making compliance documentation accessible.

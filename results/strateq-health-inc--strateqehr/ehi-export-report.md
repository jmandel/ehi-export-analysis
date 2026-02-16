# Strateq Health, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://strateqhealth.com/wp-content/uploads/2023/12/Strateq-Export.pdf
- CHPL ID: 10778 (15.05.05.3097.STRQ.01.00.1.220105)
- Mandatory Disclosures: https://strateqhealth.com/resources/product-certification/

## Navigation Journal

1. **Initial probe**: HTTP HEAD request to the registered URL returned `200 OK`, `Content-Type: application/pdf`, `Content-Length: 282110` bytes. The URL is a direct PDF download — no redirects, no login, no JavaScript required.

```bash
curl -sI -L "https://strateqhealth.com/wp-content/uploads/2023/12/Strateq-Export.pdf" -H 'User-Agent: Mozilla/5.0'
```

2. **Downloaded the PDF**:
```bash
curl -sL "https://strateqhealth.com/wp-content/uploads/2023/12/Strateq-Export.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/Strateq-Export.pdf
```

3. **Verified the file**: `file` confirms it is a PDF document. `pdfinfo` reports 1 page, A4, created 2023-12-06 from "Microsoft Word - Export.docx" via "Microsoft: Print To PDF". No embedded files, no embedded URLs.

4. **Checked the certification/mandatory disclosures page** at `https://strateqhealth.com/resources/product-certification/` for additional EHI export documentation. The page lists certification criteria and has a section "API and EHI EXPORT" that reads: "In accordance with 170.315(b)(10) EHR certification criteria, please click below for our full EHI Export documentation." The link points to the same `Strateq-Export.pdf` already downloaded. No additional export-related documents were found.

5. **Checked other files on the certification page**: The page links to several other PDFs (Real-World Testing plans/results for 2023–2025 and a Smart on FHIR API document). The API document (`Strateq-SmartOnFHIR-API.pdf`, 66 pages, updated 2026-02-10) covers the (g)(10) FHIR API — it documents standard US Core FHIR resources via SMART on FHIR and is not related to the (b)(10) EHI export mechanism.

6. **Checked ValidURLs.json**: The FHIR endpoint listing (`https://testauth.strateqhealth.com/SmartOnFHIR/ValidURLs.json`) contains FHIR Endpoint and Organization resources for the SMART on FHIR API. Not related to EHI export.

## What Was Found

The entire EHI export documentation consists of **a single A4 page with 6 sentences**. Here is the full text:

> **Product Name and Version: StrateqEHR, Version 5**
>
> The patient EHI export contains data from the patient's chart. Multiple file formats are used to store this information.
>
> ZIP is an archive file format.
>
> PDF or Portable Document Format is a file format that is used to present text or image based documents.
>
> C-CDA or Consolidated Clinical Document Architecture is a file format used for health information exchange.
>
> The export file itself is a zip file. It contains zip files of C-CDAs and other files attached to the patient's chart (e.g. PDF and images)
>
> Information for each patient encounter is available C-CDA format in zip archive.

That's it. The document describes the export as a ZIP file containing:
- C-CDA documents (one per patient encounter), themselves in ZIP archives
- Other files attached to the patient's chart (PDFs, images)

There is no data dictionary, no field definitions, no schema documentation, no sample data, no export instructions, no screenshots, and no information about how to initiate the export or what specific data elements are included.

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, StrateqEHR is a comprehensive hospital information system storing:
- Patient demographics and registration data
- Clinical documentation (H&P, assessments, care plans, nursing notes, dictation notes, operative notes)
- Orders (medications, labs, radiology, nursing, procedures via CPOE)
- Medication data (prescriptions, medication lists, home medications, medication reconciliation, eMAR)
- Lab results (via Aspyra CyberLAB integration)
- Vital signs and clinical observations
- ED tracking data
- Scanned documents and images
- Medical record deficiency tracking
- Billing and claims data (charges, claims, remittance, eligibility, denials, GL journal entries)
- Scheduling data
- C-CDA documents
- Immunization records
- Clinical quality measure data
- Implantable device data

The export documentation says the export contains "data from the patient's chart" in C-CDA format plus attached files (PDFs, images). This is deeply inadequate for the following reasons:

**C-CDA covers only a subset of clinical data.** C-CDA (Consolidated Clinical Document Architecture) is standardized for clinical summaries — it handles problems, medications, allergies, labs, vitals, immunizations, procedures, and clinical notes reasonably well. However, it does not naturally represent:

- **Billing and revenue cycle data**: Charges, claims, remittance, eligibility, denial management, GL journal entries, patient account balances. This is a major gap — StrateqEHR has an extensive revenue cycle module with Waystar integration. None of this data fits in C-CDA.
- **Order details**: While C-CDA can capture medication orders and some procedure orders, the close-loop CPOE data (lab orders, radiology orders, nursing orders, complaint-specific order sets) with their full lifecycle would not be preserved in a C-CDA clinical summary.
- **eMAR administration records**: Medication administration records with timestamps, administering nurse, held/refused status, etc. are richer than what a C-CDA medication section typically carries.
- **ED tracking data**: ESI levels, arrival times, dispositions, length of stay, turnaround times — operational ED data that doesn't map to C-CDA sections.
- **Dynamic Form Engine content**: StrateqEHR's patent-pending Dynamic Form Engine renders custom clinical forms. Whether the full structured data from these forms survives C-CDA serialization is unknown and undocumented.
- **Perioperative data**: Operative checklists, resource scheduling, perioperative documentation — the level of detail preserved in C-CDA is unclear.
- **HIM data**: Document scanning metadata, deficiency tracking, release of information records.
- **Implantable device data**: While C-CDA can carry UDI information, the documentation doesn't confirm this is included.

**The documentation provides no specifics.** We cannot determine:
- Which C-CDA document types are generated (CCD, Discharge Summary, Progress Note, etc.)
- Which C-CDA sections are populated
- Whether custom or non-standard data is exported at all
- Whether billing data is included in any form
- What "other files attached to the patient's chart" encompasses beyond PDFs and images

### Export Format & Standards

- **Format**: ZIP archive containing per-encounter C-CDA documents (also zipped) and attached files (PDF, images)
- **Standard**: C-CDA is a recognized HL7 standard (good), but it's designed for clinical summaries and transitions of care, not comprehensive EHI export
- **Appropriateness**: C-CDA is a reasonable format for clinical data but is fundamentally a summary format. Using it as the sole export mechanism for a full HIS that includes revenue cycle, ED operations, and custom form data means significant data domains are likely excluded or lossy. A proper (b)(10) export for this product would need supplementary formats (CSV, database dump, etc.) for the data that doesn't fit in C-CDA.
- **Reconstructability**: Without a data dictionary or field mapping, a third party cannot determine what data is present or missing in the export. They would need to parse the C-CDAs and hope the standard sections cover what they need.

### Documentation Quality

This is among the weakest EHI export documentation possible while still technically existing. Specific failures:

- **No data dictionary**: No listing of tables, fields, data types, or value sets
- **No field-level definitions**: No information about what specific data elements are exported
- **No export instructions**: No information about how a user initiates the export, what parameters are available, or what the workflow looks like
- **No sample data**: No example C-CDA documents, no sample export files
- **No schema documentation**: No reference to which C-CDA templates or sections are used
- **No format specification**: Beyond naming C-CDA, ZIP, and PDF, no details about file naming conventions, directory structure within the ZIP, encoding, or version information
- **Definitional padding**: Three of the six sentences are generic definitions of file formats (what ZIP is, what PDF is, what C-CDA is) that add no value
- **A developer could not implement an import** based on this documentation. They would know to expect a ZIP with C-CDAs inside, but nothing about the content, structure, or completeness of those C-CDAs.

### Structure & Completeness

- **Granularity**: None. There are no tables, no fields, no data types, no descriptions, no cardinality information.
- **Coded fields**: Not documented
- **Relationships**: Not documented
- **Versioning**: The PDF was created 2023-12-06 and has not been updated since. The filename and creation metadata suggest it was a quick Word document printed to PDF.

## Access Summary
- Final URL (after redirects): https://strateqhealth.com/wp-content/uploads/2023/12/Strateq-Export.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none (Cloudflare present but no challenge served)

## Obstacles & Dead Ends

None — the PDF was immediately accessible. The obstacle is the content, not the access. The entire EHI export documentation for a comprehensive hospital information system is 6 sentences on a single page, three of which are definitions of common file formats.

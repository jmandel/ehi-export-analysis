# Braintree Health — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.braintreehealth.com/braintree-onc-certification-btree/
- CHPL ID: 10727
- Product: BRAINTREE v10.5.1.1
- Certification Date: 2021-11-19
- Developer: Braintree Health (Corpus Christi, TX)

## Navigation Journal

The registered URL is a WordPress page serving as the product's ONC certification disclosure page.

```bash
curl -sI -L "https://www.braintreehealth.com/braintree-onc-certification-btree/" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
# Returns HTTP 200, Content-Type: text/html; charset=UTF-8
```

The page is a single long HTML page with no accordions, tabs, or JavaScript-dependent content. All content is statically rendered. The page structure is:

1. **Certification disclosures** — product name, version, certification number, full criteria list
2. **FHIR g(10) section** — two links:
   - "FHIR API DOCUMENTATION" → `Braintree-FHIR-API-Documentation-1.pdf` (76 pages, uploaded Jan 2026)
   - "FHIR BASE URL" → `Braintree-fhir-doc.pdf` (1 page, uploaded Nov 2022) — lists test and production FHIR endpoints
3. **Electronic Health Information export b(10) section** — a short paragraph with a bullet list describing export formats. No linked documents, no data dictionary, no downloadable artifacts.
4. **CQMs table**, additional software, costs, accessibility, RWT plans/results

The b(10) EHI export section contains only inline text — there are no linked PDFs, data dictionaries, schemas, or downloadable files specific to the EHI export. The entire b(10) documentation is six bullet points on the page.

```bash
# Extracted all downloadable file links from the page:
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|csv|json|doc)[^"]*"' /tmp/braintree-page.html
# Found 11 PDFs — 2 FHIR-related, 1 API TOU, 1 Access Application, 6 RWT plans/results, 1 transparency spreadsheet
# No EHI-export-specific downloadable files exist.
```

Downloaded:
- `Braintree-FHIR-API-Documentation-1.pdf` — the g(10) FHIR API documentation
- `Braintree-fhir-doc.pdf` — FHIR server endpoint URLs
- `transparency.htm` — cost disclosure (Excel-exported HTML spreadsheet)
- `certification-page.html` — saved copy of the full certification page
- Screenshots of the full page and the b(10) section

## What Was Found

### EHI Export b(10) Documentation

The entire b(10) EHI export documentation consists of a brief paragraph and six bullet points on the certification page, under the heading "Electronic Health Information export b(10)":

> Braintree understands the importance of ensuring patients have timely, secure and easy access to electronic health information ("EHI") to empower them in managing their own health and well-being.
>
> Key Information About the Exported Data:
> - While certain EHI, such as images, documents, reports are exported in human-readable html/pdf format where applicable.
> - The patient demographics are exported in CCDA xml format.
> - The consents form of the patient are exported in HTML format.
> - The clinical and billing report and encounter documentation of the patient is exported in PDF format. The PDF provided are in computable format.
> - The patient attachments are exported in the original format as uploaded into EMR.
> - The patient images are exported into DICOM format.

That is the complete documentation. There is no linked data dictionary, no schema, no sample export, no user guide, and no detailed description of what data is included in the export.

### FHIR g(10) API Documentation

The 76-page FHIR API documentation PDF (uploaded January 2026) is a standard SMART on FHIR API document covering:
- SMART app launch flow (OAuth2 authorization/authentication)
- FHIR endpoints (production and test server URLs)
- Supported FHIR resources: Patient, AllergyIntolerance, CarePlan, CareTeam, Condition (Problems/Health Concerns), Device (Implantable), DiagnosticReport/Clinical Notes/DocumentReference, Observation (Lab Results), Goal, Immunization, Medication/MedicationRequest, Observation (Smoking Status), Procedure, Provenance, Observation (Vital Signs)
- Sample request/response JSON for each resource
- Terms of Use

This is purely g(10) FHIR API documentation — it covers only US Core / USCDI v1 data classes. It does not mention the b(10) EHI export at all.

### FHIR Base URL Document

A single-page PDF listing four endpoints:
- Test FHIR Server: `https://fhirserver.braintreemd.com:9443/fhir-server/api/v4/`
- Test Auth Server: `https://fhiroaserver.braintreemd.com`
- Production FHIR Server: `https://btfhir.braintreemd.com:9443/fhir-server/api/v4/`
- Production Auth Server: `https://btoaserver.braintreemd.com`

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, Braintree's BMW Platform stores a wide range of data: clinical documentation (pre-op, intra-op, post-op), medical imaging (PACS/DICOM), radiology information (RIS), billing with auto-CPT encoding, inventory/supply chain, scheduling, and specialty data for vascular access, interventional radiology, and ambulatory surgery centers.

The b(10) export documentation describes these output formats:
- **Demographics** — CCDA XML (covers basic patient demographics)
- **Consent forms** — HTML format
- **Clinical and billing reports, encounter documentation** — PDF format (described as "computable format")
- **Attachments** — original upload format
- **Medical images** — DICOM format

**Domains that appear covered (at least partially):**
- Patient demographics (via CCDA)
- Clinical notes and encounter documentation (via PDF)
- Billing reports (via PDF — though scope unclear)
- Medical images (via DICOM — appropriate for this imaging-heavy product)
- Patient attachments (original format)
- Consent forms (HTML)

**Domains with no mention or unclear coverage:**
- **Procedure-specific documentation** (pre-op, intra-op, post-op workflows) — may be included in "encounter documentation" PDFs but not specified
- **Medications and prescriptions** — not mentioned in b(10) export
- **Lab results and diagnostic reports** — not mentioned
- **Allergies** — not mentioned
- **Problem lists / diagnoses** — not mentioned
- **Vital signs** — not mentioned
- **Immunization records** — not mentioned
- **Radiology reports** (RIS data) — unclear if included in PDFs or separate
- **Scheduling/appointment data** — not mentioned
- **Inventory/supply consumption per procedure** — not EHI (operational), so correctly absent
- **Detailed billing data** (CPT codes, charges, payment details) — "billing report" is mentioned but no detail on granularity
- **Referral data** — not mentioned
- **Care plans** — not mentioned

The export claims to include "clinical and billing report and encounter documentation" in PDF format, which could conceivably be comprehensive — but without a data dictionary or detailed description, it's impossible to verify what data fields are actually included. The claim that PDFs are in "computable format" is notable but unexplained.

### The b(10) vs g(10) Question

Notably, Braintree does **not** conflate their b(10) and g(10) exports — they are presented as distinct sections on the page. The b(10) export uses CCDA, HTML, PDF, and DICOM formats rather than the FHIR API. This suggests the vendor has made some effort to distinguish the two requirements.

However, the b(10) documentation is so sparse that it's impossible to assess whether the export actually covers "all electronic health information" or just a subset. The g(10) FHIR API covers only standard US Core resources, and the b(10) section doesn't reference FHIR at all — which is actually appropriate for a procedure-center product with imaging, billing, and specialty data that doesn't map neatly to FHIR US Core.

### Export Format & Standards

The export uses a mix of formats:
- **CCDA XML** for demographics — a recognized standard, though using CCDA just for demographics seems like an odd choice when the rest of the export is non-FHIR
- **PDF** for clinical and billing documentation — described as "computable format," which likely means structured/tagged PDFs rather than scanned images. However, PDF is inherently limited for data portability compared to structured formats like CSV, JSON, or XML
- **HTML** for consent forms — readable but not ideal for data interchange
- **DICOM** for medical images — the correct standard for imaging data
- **Original format** for attachments — preserves fidelity but depends on what was uploaded

The format choices are reasonable for human readability but raise concerns about machine-processability. PDFs — even "computable" ones — make it difficult for a receiving system to import and reconstruct structured data. A third party would be able to view the records but would struggle to programmatically ingest them.

### Documentation Quality

The b(10) export documentation quality is **very poor**:
- No data dictionary whatsoever — no tables, fields, schemas, or column definitions
- No sample export files or examples
- No user guide or instructions for performing the export
- No description of the export process (how it's triggered, who can request it, what parameters exist)
- No enumeration of what specific data elements are included
- No versioning or change history
- The six bullet points read more like a compliance checkbox than genuine technical documentation

The claim that "PDFs are in computable format" is the only semi-technical detail provided, and it's not explained. Does this mean PDF/A? Tagged PDFs? PDF with embedded structured data?

A developer tasked with importing data from this export would have almost nothing to work with. They would need to receive an actual export file to reverse-engineer the structure.

### Structure & Completeness

- **Granularity**: Extremely low. No field-level documentation exists. The documentation operates at the level of "demographics are in CCDA" and "billing is in PDF" — there is no description of which demographic fields, which billing elements, or what constitutes an "encounter documentation" PDF.
- **Coded fields**: Not documented. No value sets, no code systems referenced.
- **Relationships**: Not documented. No description of how the various exported files relate to each other or how a receiving system would correlate them.
- **Completeness signal**: The absence of any mention of medications, allergies, labs, vitals, immunizations, problem lists, or care plans in the b(10) section is concerning — these are core clinical data domains that the product stores (and that are available via the g(10) FHIR API). It's unclear whether they're included in the PDF "encounter documentation" or genuinely missing from the export.

### Overall Assessment

Braintree Health has done the minimum to acknowledge the b(10) requirement — they have a labeled section on their certification page that describes export formats at a very high level. The fact that the b(10) export uses non-FHIR formats (CCDA, PDF, DICOM) and is presented separately from the g(10) API suggests some genuine effort to distinguish the requirements.

However, the documentation is far too sparse to assess whether the export actually covers all EHI. For a product that stores procedure-specific clinical workflows, medical imaging, radiology information, billing with auto-CPT encoding, and inventory data, six bullet points is inadequate documentation. The most critical missing piece is a data dictionary or detailed listing of what data elements the export includes across the product's various modules (BT Scheduler, BT RIS, BT PACS, BT Inventory, EMR, Billing).

The use of PDF as the primary format for clinical and billing data, while described as "computable," is a significant limitation for data portability. The DICOM export for images is appropriate and is actually a strength — this is the correct format for the imaging data that is central to this product's use case.

## Access Summary
- Final URL: https://www.braintreehealth.com/braintree-onc-certification-btree/ (no redirects)
- Status: found
- Required browser: no (static HTML, all content visible without JavaScript)
- Navigation complexity: direct_link (b(10) section is inline on the page, no clicks needed)
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles encountered. The page loaded cleanly with curl.
- The transparency.htm file is an Excel-exported HTML frameset for cost disclosures — not relevant to the EHI export.
- No EHI-export-specific downloadable artifacts exist on the page; the b(10) documentation is entirely inline text.

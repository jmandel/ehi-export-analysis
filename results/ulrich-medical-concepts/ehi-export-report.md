# Ulrich Medical Concepts — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://ulrichmedicalconcepts.com/home/the-ehr/meaningful-use/cost-disclosure-and-transparency/
- CHPL ID: 10227
- Product: Team Chart Concept (TCC) v7.1
- Certification date: 2019-12-26

## Navigation Journal

**Step 1: Probed the registered URL.**
```bash
curl -sI -L "https://ulrichmedicalconcepts.com/home/the-ehr/meaningful-use/cost-disclosure-and-transparency/" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
```
HTTP/2 200. Content-Type: text/html. WordPress site behind Sucuri/Cloudproxy WAF. No redirects.

**Step 2: Downloaded and examined the page.**
```bash
curl -sL "https://ulrichmedicalconcepts.com/home/the-ehr/meaningful-use/cost-disclosure-and-transparency/" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' \
  -o cost-disclosure-and-transparency.html
```
104,270 bytes. The page is UMC's mandatory cost disclosure and transparency page. It contains:
- ONC compliance disclosure statement
- Vendor/product info (UMC / TCC 7.1, certified 2019-12-26)
- Clinical quality measures list
- Full certification criteria table including §170.315(b)(10) marked with an asterisk
- A single-sentence EHI export footnote (the asterisk)
- Cost transparency section with fee disclosures
- Application Access API section pointing to InteropEngine (their g(10) FHIR API provider)

**Step 3: Searched for downloadable files on the page.**
```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/umc-page.html
```
Only one file link found: `https://appstudio.interopengine.com/partner/fhirR4endpoints-umc.json` — this is the FHIR R4 endpoint list for UMC's g(10) API customers.

**Step 4: Searched for EHI-specific links.**
```bash
grep -oiE 'href="[^"]*"' /tmp/umc-page.html | grep -iE 'ehi|export|data.dictionary|b.10|bulk|fhir|api|interop'
```
Found links to:
- InteropEngine FHIR R4 endpoints JSON (downloaded; nearly empty — just a Bundle wrapper with no entries)
- UMC interoperability page
- InteropEngine Open API documentation
- InteropEngine API terms of use

None of these are EHI (b)(10) export documentation. They all relate to the (g)(10) FHIR API.

**Step 5: Checked the interoperability page.**
```bash
curl -sL "https://ulrichmedicalconcepts.com/home/the-ehr/interoperability/" -H 'User-Agent: ...' -o /tmp/umc-interop.html
```
This page is about UMC's interoperability achievements (cancer registry reporting, KHIE connectivity, HL7/CDA capabilities). No EHI export documentation, no data dictionary, no downloadable files relevant to b(10).

**Step 6: Checked the InteropEngine Open API Documentation page.**
```bash
curl -sL "https://www.interopengine.com/2021/open-api-documentation.html" -H 'User-Agent: ...' -o /tmp/umc-api-docs.html
```
This is EMR Direct's generic FHIR R4 API documentation for third-party developers. It describes the g(10) standardized API, not the b(10) EHI export. Updated Feb 5, 2026.

**Step 7: Downloaded the FHIR endpoints JSON.**
```bash
curl -sL "https://appstudio.interopengine.com/partner/fhirR4endpoints-umc.json" -o fhirR4endpoints-umc.json
```
The file contains only a FHIR Bundle shell with no entries:
```json
{"resourceType":"Bundle","type":"collection","timestamp":"2026-02-07T14:37:24-08:00"}
```
This suggests either no UMC customers have active FHIR API endpoints, or the list is not publicly populated.

**Step 8: Checked adjacent pages for EHI content.**
- Meaningful Use parent page (`/home/the-ehr/meaningful-use/`): discusses EHR incentives — no EHI export content.
- Capabilities page (`/home/the-ehr/capabilities/`): marketing overview of TCC features — no EHI export content.

**Step 9: Took a full-page browser screenshot** of the cost disclosure page to capture the rendered layout.

## What Was Found

The entire EHI export documentation for Ulrich Medical Concepts' Team Chart Concept consists of a **single sentence** on the cost disclosure and transparency page, presented as a footnote to the §170.315(b)(10) certification criterion:

> *EHI can be exported in PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the user.

That is the complete documentation. There is:
- **No data dictionary** — no listing of what data fields or tables are included in the export
- **No format specification** — no description of the PDF structure or which C-CDA template is used
- **No schema or machine-readable artifact** — no XSD, JSON Schema, or sample files
- **No user guide** — no instructions on how to initiate the export, what options are available, or what the output looks like
- **No sample data or examples**
- **No API documentation** specific to the EHI export (the linked API docs are for the g(10) FHIR API)

The page also links to EMR Direct's InteropEngine Open API Documentation and a FHIR R4 endpoints JSON file, but these are exclusively for the §170.315(g)(10) standardized FHIR API — a completely separate certification criterion. The FHIR endpoints JSON is effectively empty (no customer endpoints listed).

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, Team Chart Concept stores the following data categories:

| Data Domain | Covered by Export? | Assessment |
|---|---|---|
| Demographics & contacts | Unknown | Not documented |
| Encounter notes / clinical documentation | Possibly (C-CDA) | C-CDA would include some clinical narrative, but scope not specified |
| Problem lists / diagnoses | Possibly (C-CDA) | Standard C-CDA content, but not confirmed |
| Medications / e-prescribing records | Possibly (C-CDA) | Standard C-CDA content, but not confirmed |
| Allergies | Possibly (C-CDA) | Standard C-CDA content, but not confirmed |
| Lab results / diagnostic data | Possibly (C-CDA) | Standard C-CDA content, but not confirmed |
| Vital signs | Possibly (C-CDA) | Standard C-CDA content, but not confirmed |
| Immunizations | Possibly (C-CDA) | Standard C-CDA content, but not confirmed |
| Health maintenance / clinical alerts | Unknown | Likely not in standard C-CDA |
| Risk factor analysis data | Unknown | Likely not in standard C-CDA |
| Clinical quality measures data | Unknown | Likely not in standard C-CDA |
| **Billing / claims / payments** | **Unknown — likely missing** | Not a standard C-CDA section; PDFs could contain billing info but this is not documented |
| **Scheduling / appointments** | **Not EHI** | Operational data, not part of designated record set |
| **Scanned documents / document management** | **Unknown** | PDFs could include scanned docs, but this is not documented |
| **Patient portal messages** | **Unknown** | Portal is third-party (Medfusion/Bridge); unclear if these are in the export |
| **Interoperability records** (CDAs, Direct messages) | **Unknown** | Not documented |
| Custom templates / specialty forms | **Unknown** | Not documented |
| Implantable device data | Possibly (C-CDA) | Standard C-CDA content given a(14) certification |

The fundamental problem is that the documentation tells us **nothing** about what is actually in the export. The formats are stated (PDF or C-CDA), but there is zero information about which data domains are included, how they map to these formats, or what completeness looks like.

If the export is a standard Consolidated CDA, it would likely cover the core USCDI clinical data (problems, medications, allergies, labs, vitals, procedures, immunizations, demographics). But that would be essentially identical to what the g(10) FHIR API provides — a narrow clinical summary, not "all electronic health information." The billing, financial, scheduling, document management, and specialty-specific clinical data that TCC stores would almost certainly **not** be in a standard C-CDA.

The mention of PDF export is interesting — PDFs could theoretically contain anything, including billing summaries and scanned documents. But without documentation, it's impossible to assess what they actually contain.

### Export Format & Standards

- **Formats**: PDF and C-CDA (Consolidated Clinical Document Architecture)
- **Standards**: C-CDA is a recognized HL7 standard; PDF is a universal document format
- **Concerns**:
  - C-CDA is designed for clinical summaries, not comprehensive data export. It does not natively accommodate billing records, custom form data, or administrative content. Using C-CDA as the sole structured export format strongly suggests only USCDI-equivalent clinical data is exported.
  - PDF is not a computable format. Exporting data as PDF makes it readable but not machine-processable. A third party could not reconstruct a patient's structured record from PDFs.
  - There is no mention of which C-CDA template is used (e.g., CCD, Discharge Summary, Referral Note), what sections are populated, or what coded values are included.
  - The combination of "PDF or C-CDA" may indicate a choice — the user selects one or the other — or it may mean different data types go to different formats. This is undocumented.

### Documentation Quality

This is among the most minimal EHI export documentation possible. One sentence, no data dictionary, no user guide, no examples, no schema. A developer tasked with importing this data would have literally no specification to work from beyond "it's a PDF or C-CDA."

- No field-level definitions
- No data types or value sets
- No export procedure instructions
- No sample files
- No worked examples
- No versioning or change history

The documentation reads as a compliance checkbox — the absolute minimum text to acknowledge that an EHI export capability exists, without providing any actionable detail about what it does or how it works.

### Structure & Completeness

- **Granularity**: Zero. The documentation specifies only the output format names and the save-to-folder mechanism.
- **Field-level documentation**: None.
- **Coded fields / value sets**: None documented.
- **Relationships between entities**: Not applicable — no entities are documented.
- **Versioning**: None.

### Overall Assessment

Ulrich Medical Concepts has provided the bare minimum acknowledgment that an EHI export function exists, without meaningful documentation of what it exports, how to use it, or what the output looks like. The use of C-CDA as one of the two export formats strongly suggests the structured export covers only standard clinical summary data (the USCDI subset), not the full breadth of electronic health information that TCC stores — particularly billing/financial data, document management content, and specialty-specific clinical forms.

This is a very small vendor (~22 employees, ~$1.4M revenue) with a certification from late 2019. The lack of documentation is consistent with a vendor that implemented the minimum to achieve certification without investing in comprehensive export documentation. The product was certified for (b)(10), confirming the capability exists, but the public documentation provides no basis for evaluating its scope or quality.

## Access Summary
- Final URL: https://ulrichmedicalconcepts.com/home/the-ehr/meaningful-use/cost-disclosure-and-transparency/
- Status: found
- Required browser: no (static WordPress page, fully rendered by curl)
- Navigation complexity: direct_link
- Anti-bot issues: none (Sucuri WAF present but did not block; User-Agent header used as precaution)

## Obstacles & Dead Ends
- No obstacles encountered. The page loaded cleanly and all content was accessible.
- The interoperability page, Meaningful Use parent page, and Capabilities page were checked for additional EHI export content — none was found.
- The InteropEngine API documentation and FHIR endpoints JSON are for the g(10) API, not the b(10) export.
- The FHIR endpoints JSON was essentially empty (no customer endpoints listed).

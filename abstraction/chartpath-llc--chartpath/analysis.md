# EHI Export Analysis: ChartPath, LLC

**Product**: ChartPath v1.29
**Analysis date**: 2026-02-16
**CHPL IDs**: 10258 (15.04.04.2996.Char.12.01.1.191227)

## 1. Product Context

ChartPath is a cloud-based EHR purpose-built for **physician practices that round on patients in long-term and post-acute care (LTPAC) facilities** — primarily skilled nursing facilities (SNFs) and assisted living facilities (ALFs). It is not the facility's own EHR; it is the physician group's EHR for documenting encounters during facility visits. ChartPath was developed by Afoundria (rebranded to ChartPath, LLC in 2021) and is now part of LivTech. It serves 250+ practices and 4,000+ users.

**Relevant to export completeness**, ChartPath stores:
- **Clinical encounter documentation**: The core data — notes from physician rounding encounters with assessment findings, diagnoses, treatment plans. Single-page encounter templates with structured and semi-structured fields.
- **Patient demographics**: Managed natively and pulled from facility EHRs (e.g., PointClickCare).
- **Medications/e-prescribing**: Certified for (a)(2) CPOE for medications. Drug-drug and drug-allergy checking implies allergy data.
- **Problem/diagnosis lists**: ICD-10 diagnoses, active problem lists (implied by CQM reporting certification).
- **Screening/assessment scores**: Scored tools for anxiety, dementia staging, depression, caregiver burden (GUIDE Model features).
- **Implantable device data**: Certified for (a)(14).
- **Billing/claims data**: CPT code suggestion, RVU tracking, claims, and reimbursement. ChartPath RCM and RCM Pro modules launched in 2021.
- **Census/facility management**: Multi-facility census management is a core workflow.
- **Care coordination**: Patient flagging, GUIDE Model care navigator features.
- **Orders**: Integration with PointClickCare and HIEs for orders.
- **C-CDA documents**: Certified for (b)(1) and (b)(2) transitions of care.

The product is **not** known to manage lab ordering, imaging/radiology, or a patient portal.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehiexport-page.html` (15,298 bytes) | The entire EHI export documentation — a single HubSpot landing page with 7 paragraphs (10 sentences, ~140 words) describing the export format. Verified live page matches downloaded artifact. | **Primary artifact** — but extremely thin |
| `downloads/ehiexport-page-screenshot.png` (293,816 bytes) | Full-page screenshot confirming page layout: ChartPath logo, heading, 7 paragraphs, copyright footer. | Confirmatory |
| `downloads/2015-cehrt-page.html` (148,788 bytes) | 2015 CEHRT mandatory disclosures page listing certification details, testing plans/results (2022–2025), FHIR API/OAuth PDFs, and an "EHI Export" button that links back to the same `info.chartpath.com/ehiexport` page. | Useful for context; confirms no additional EHI documentation exists on the CEHRT page |
| `downloads/2015-cehrt-screenshot.png` (555,179 bytes) | Screenshot of CEHRT page. | Confirmatory |

**No data dictionary, schema, sample export, field listing, or user guide was found in any artifact.** The CEHRT page's "EHI Export" button redirects (via HubSpot CTA `d41a24e0-72fd-451a-b702-8f38590631f7`) to the same `info.chartpath.com/ehiexport` page. The FHIR API PDF (55 pages, per prior report) covers (g)(10) standardized API access and is not (b)(10) EHI export documentation.

## 3. Export Mechanics

- **Format**: ZIP archive containing nested ZIP files of PDFs, C-CDA documents, and file attachments.
- **Structure** (per documentation):
  - A top-level ZIP file
  - Sub-ZIP of per-encounter PDFs
  - Sub-ZIP of per-encounter C-CDA documents
  - Sub-ZIP of files attached to the patient's chart (in original format)
  - A "face sheet" document with patient demographics
- **Mechanism**: Not documented. No instructions on how to initiate the export (UI button, API call, vendor-assisted). The prior report could not find a user guide or screenshots.
- **Single-patient vs bulk**: Not documented. The page says "the patient EHI export" (singular), suggesting single-patient export. No mention of bulk capability.
- **Access constraints or fees**: Not documented.

## 4. Export Content: What's In It

### What the documentation says

The entire EHI export documentation is 7 sentences. Here is the complete substantive content, verbatim from `ehiexport-page.html`:

> "The patient EHI export contains data from the patient's chart. Multiple file formats are used to store this information."
>
> "ZIP is an archive file format."
>
> "PDF or Portable Document Format is a file format that is used to present text or image based documents."
>
> "C-CDA or Consolidated Clinical Document Architecture is a file format used for health information exchange."
>
> "The export file itself is a zip file. It contains zip files of PDFs, C-CDAs, and other files attached to the patient's chart."
>
> "Patient demographic information can be found in the face sheet document as well as in the PDF and C-CDA documents for each encounter."
>
> "Information for each patient encounter is available in both PDF and C-CDA format in their respective zip archive."
>
> "Files attached to the patient's chart are also included in their original format in a zip archive."

Three of the seven sentences are definitions of file formats (ZIP, PDF, C-CDA) rather than descriptions of export content.

### What's actually documented as being in the export

Based on the documentation, the export contains exactly three categories of content:

1. **Per-encounter clinical documents** — each encounter is represented as both a PDF and a C-CDA document. No specification of what C-CDA sections or templates are used, what fields are populated, or what clinical data elements are included.

2. **Patient demographics** — described as being in a "face sheet document" and also in each encounter's PDF and C-CDA. No specification of what demographic fields are included.

3. **File attachments** — files attached to the patient's chart are included in their original format. No specification of what types of files these might be.

### Vendor's own content organization

There is no data dictionary, no entity listing, no field listing, and no structured content documentation. The vendor does not organize the export content into categories, tables, or entities. The only organizational structure described is:

| Component | Format | Description |
|---|---|---|
| Face sheet | Document (format unspecified) | Patient demographic information |
| Per-encounter documents | PDF | Encounter information in printable format |
| Per-encounter documents | C-CDA | Encounter information in health information exchange format |
| Attached files | Original format | Files attached to the patient's chart |

**No entity/table/field inventory is possible** because no structured documentation exists. See `analysis/full-entity-inventory.json` (which documents this absence) and `analysis/parsed_ehi_documentation.json` (complete parse of the HTML page).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes only three content types: encounter documents (PDF + C-CDA), a demographic face sheet, and file attachments. There is no categorization into data domains, no enumeration of data elements, and no indication of what specific clinical, billing, or specialty data is included.

The C-CDA documents likely contain standard C-CDA sections (problems, medications, allergies, vitals, etc.) for each encounter, but the documentation does not specify which C-CDA templates or sections are used. The PDFs are presumably rendered encounter notes, which would contain whatever the clinician documented during the visit.

**Critical limitation**: Without a data dictionary, sample export, or C-CDA template specification, it is impossible to determine exactly what data is included in the export. The analysis below reflects what can reasonably be inferred from the format choices (PDF + C-CDA per encounter) and what is known about C-CDA's capabilities and limitations.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | "Face sheet document" and C-CDA documents mention demographics, but no field listing | Likely present but undocumented in detail |
| Encounters / visits | ⚠️ Partial | Per-encounter PDF + C-CDA described | Encounter documents exist; unclear what structured data is captured vs. narrative text |
| Problems / conditions / diagnoses | ⚠️ Partial | Likely in C-CDA sections | C-CDA typically includes problems; no confirmation of completeness |
| Medications / prescriptions | ⚠️ Partial | Likely in C-CDA sections | C-CDA typically includes medications; product is certified for e-prescribing (a)(2), but unclear if full Rx history is in export |
| Allergies | ⚠️ Partial | Likely in C-CDA sections | C-CDA typically includes allergies; no explicit confirmation |
| Immunizations | ⚠️ Partial | May be in C-CDA if documented | Not a core LTPAC workflow; may be N/A for most patients |
| Vitals | ⚠️ Partial | Likely in C-CDA sections | C-CDA typically includes vitals; no explicit confirmation |
| Lab results | ❌ Not covered | No mention; product may not manage labs natively | Product doesn't appear to have lab ordering (no (a)(3) certification); likely N/A |
| Imaging / diagnostic reports | N/A | No mention; product doesn't manage imaging | Not a ChartPath function |
| Procedures | ⚠️ Partial | May be in C-CDA if documented during encounters | No explicit mention |
| Clinical notes / documents | ⚠️ Partial | Per-encounter PDFs are essentially clinical notes; C-CDAs provide structured version | Core content, but PDF format is not computationally useful; C-CDA provides some structure |
| Care plans / goals | ⚠️ Partial | May be in C-CDA if documented | No explicit mention |
| Orders / referrals | ❌ Not covered | No mention in export documentation | Product integrates with facilities for orders; this data may not be in the export |
| Insurance / coverage | ❌ Not covered | No mention in export documentation | Product stores insurance data (billing module); significant gap if absent |
| Claims / billing | ❌ Not covered | No mention of CPT codes, RVU data, claims, charges, or payments | Product has RCM modules with CPT suggestion, RVU tracking, claims management; **significant gap** |
| Payments | ❌ Not covered | No mention | Product manages reimbursement data; gap if absent |
| Consents / directives | ❌ Not covered | No mention | May be in attached files if scanned; not structured |
| Patient communications | N/A | No patient portal | Product does not have a patient portal |
| Specialty-specific (LTPAC assessments) | ❌ Not covered | No mention of structured screening scores, dementia staging, caregiver burden assessments | Product stores structured LTPAC-specific screening data (anxiety, dementia, depression, caregiver burden); **significant gap** — these scores are unlikely to be fully captured in C-CDA format |
| Census / facility assignments | ❌ Not covered | No mention | Core operational data; multi-facility census management is a key workflow. May not qualify as EHI if purely operational, but facility assignment data linked to patient care decisions could be EHI |

**Summary**: Of the applicable domains, the export documentation provides evidence of coverage for only demographics and encounter documentation (via PDF + C-CDA). Even those are only "partial" because there is no specification of what's included. Several domains that ChartPath clearly stores — particularly **billing/claims**, **specialty screening scores**, and **medications beyond C-CDA** — are not mentioned in the export documentation.

## 6. Documentation Quality

The EHI export documentation is **among the most minimal possible**. Specific deficiencies:

- **No data dictionary**: Zero field-level definitions, zero table/column listings.
- **No schema**: No C-CDA template specification, no description of which C-CDA sections are populated or which templates are used.
- **No value sets**: No coded field documentation, no code system references.
- **No sample data**: No example export file for a developer to reference.
- **No user guide**: No instructions on how to initiate the export, what permissions are needed, or what options are available.
- **No screenshots**: No visual documentation of the export interface.
- **No API specification**: Export appears to be document-based; no programmatic access documented.
- **No relationships**: The only structural information is the ZIP nesting (top ZIP → sub-ZIPs for PDFs, C-CDAs, attachments).

Three of the seven sentences are definitions of common file formats (ZIP, PDF, C-CDA) rather than descriptions of ChartPath-specific export content. The page was last updated in 2023 (copyright footer) with no version information or change history.

**Could a developer build an import from this documentation?** No. A developer would know only that the export is a ZIP containing PDFs, C-CDAs, and attachments. They would have no information about:
- What C-CDA sections/entries to expect
- What fields are in the face sheet
- What naming conventions are used for files within the ZIPs
- What data elements are in the encounter PDFs
- What types of files might be attached

They would need to obtain an actual export and reverse-engineer the structure.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to assess export completeness. The export itself is a document-based approach (PDF + C-CDA per encounter) that, even if well-implemented, would cover only clinical encounter data in standardized format and miss native data model elements like billing records, structured screening scores, and specialty assessments. The documentation provides no evidence of covering "all electronic health information" the product stores.

### Key Findings

1. **Entire EHI export documentation is 7 paragraphs (10 sentences, ~140 words)**, three of which are generic definitions of file formats (ZIP, PDF, C-CDA). This is on the far minimal end of vendor (b)(10) documentation. (Source: `ehiexport-page.html`, verified via `analysis/parsed_ehi_documentation.json`)

2. **Export is document-based (PDF + C-CDA per encounter), not a native data model export.** This approach inherently limits what can be exported to what fits in clinical document standards. Billing data, structured screening scores, and specialty-specific assessments are unlikely to be captured in C-CDA format. (Source: EHI export page description)

3. **No data dictionary, schema, sample data, or field-level documentation exists.** The CEHRT page's "EHI Export" button links to the same sparse page — no additional documentation is available. (Source: `2015-cehrt-page.html`, verified via CTA button `alt="EHI Export"`)

4. **Billing/RCM data is conspicuously absent from export documentation.** ChartPath has billing modules (ChartPath RCM, RCM Pro) with CPT code suggestion, RVU tracking, and claims management. None of this data is mentioned in the export. (Source: `product-research.md` vs. `ehiexport-page.html`)

5. **LTPAC-specific structured assessments (dementia staging, anxiety/depression scores, caregiver burden) are not mentioned in the export.** These are a differentiating feature of ChartPath and represent specialty clinical data that a patient should have access to. C-CDA has limited ability to represent these structured scores. (Source: `product-research.md` GUIDE Model features vs. `ehiexport-page.html`)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   ZIP containing PDFs, C-CDAs, and file attachments
Model type:      Standard projection (C-CDA) + document export (PDF)
Entities:        N/A (no data dictionary)
Fields:          N/A (no field documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear (documentation says "the patient EHI export" — singular)
Domains covered: 0 of 14 confirmed; 6 of 14 partial (inferred from C-CDA format, not documented)
```

### Bottom Line

ChartPath's EHI export documentation is a stub — 7 paragraphs (~140 words) on a landing page describing a ZIP of PDFs and C-CDAs with no data dictionary, no schema, and no field-level detail. A patient receiving this export would get printable encounter notes and standard clinical documents, but would likely be missing billing records, structured LTPAC screening scores (dementia staging, depression, caregiver burden), and other specialty data that ChartPath stores. The single biggest gap is the complete absence of documentation: it is impossible to determine what's actually in the export without obtaining one and examining it directly.

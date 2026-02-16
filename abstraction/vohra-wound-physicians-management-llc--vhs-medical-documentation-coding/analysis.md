# EHI Export Analysis: Vohra Wound Physicians Management, LLC

**Product**: VHS Medical Documentation & Coding v3.5
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2875.VHSM.35.00.1.181221 (CHPL ID 9887)

## 1. Product Context

VHS Medical Documentation & Coding is a proprietary, specialty wound care EMR built by Vohra Wound Physicians Management, LLC — the largest physician-led wound care specialty practice in the US (~300+ physicians, ~3,000 skilled nursing facilities, 1.4M annual patient visits). This is **not a general-purpose EHR** sold to external customers; it is an internal tool supporting Vohra's employed wound care physicians who visit post-acute care facilities (SNFs, ALFs, LTACHs) for bedside wound care.

The product name itself — "Medical Documentation **& Coding**" — signals that the system captures both clinical documentation and billing/coding data. Key data domains the product stores:

- **Wound care specialty data**: Wound assessments (etiology, staging, measurements), treatment plans, procedure documentation (debridement, Doppler/ABI studies, skin substitute grafts, negative pressure therapy), dressing orders, MDS-compliant wound documentation, wound healing trajectories
- **Core clinical data**: Demographics, vital signs, problem lists, medications/CPOE, allergies, implantable device lists, family health history
- **Coding/billing data**: Diagnosis codes, procedure codes, billing-supportive documentation; the product "assists with billing, coding and documentation"
- **Clinical notes**: Encounter/progress notes generated at bedside visits
- **Outcomes/analytics**: Healing timelines, re-hospitalization rates, dressing change frequency, per-patient metrics
- **AI/ML predictions**: Wound healing predictions from 6M historical wound cases
- **Portal content**: Facility-facing and patient-facing documents
- **Interoperability data**: C-CDA transitions of care, integrations with PointClickCare, MatrixCare

This baseline establishes a rich data footprint against which to assess export completeness.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/CompleteExport.html` (11,592 bytes) | The **entire** EHI export documentation — a single static HTML page titled "Export data format and location" describing two output file types and the export procedure. No data dictionary, no schema, no sample data. | **Primary source** — but extremely thin |
| `downloads/CompleteExport-screenshot.png` (169 KB) | Full-page screenshot of the documentation page as rendered in Chrome | Confirms the HTML renders as a simple single-page document with Vohra branding |
| `downloads/emr-redirect-page.html` (3,772 bytes) | Redirect notice at the registered CHPL URL (`emr.vohrawoundteam.com`), which uses JavaScript to redirect to `facilityportal.vohrawoundteam.com` | Documents the redirect chain; no substantive content |

**Total documentation surface**: One static HTML page. No supplementary files of any kind — no PDFs, no schemas, no sample exports, no downloadable data dictionaries.

## 3. Export Mechanics

- **Format**: PDF (encounter notes, one per patient) + XML (C-CDA, one per encounter)
- **Mechanism**: Admin portal UI (Advanced → Data Portability). The admin portal URL (`https://med.vohrawoundteam.com/LogIn.aspx`) resolves to NXDOMAIN — the subdomain no longer exists in DNS.
- **Single-patient only**: Documentation describes only a single-patient export procedure (enter first name, last name, DOB → "Export Patients"). No bulk export procedure is documented.
- **Retrieval**: Exported files are written to a server-side directory (`C:\inetpub\webapp\ExportedPatientData` on `IIS-PROD-02`). Retrieval requires logging into the production server — an unusual and operationally challenging delivery mechanism.
- **Access constraints**: Requires authenticated admin portal access with export permissions, plus server login to retrieve files.

## 4. Export Content: What's In It

### Documentation detail

There is **no data dictionary**. The documentation provides zero field-level information. The entire content specification is:

1. **PDF files**: "Encounter notes." No further detail on what encounter notes contain — no section list, no field definitions, no indication of whether wound-specific data (measurements, staging, photographs) is included.
2. **XML files**: "Data in this file conforms to the CCDA standard." No further detail — no C-CDA document type (CCD, Referral Summary, etc.), no template OIDs, no section list, no indication of which data elements are included or excluded.

### Vendor's own content organization

The vendor provides no entity-level or field-level organization. There are no tables, no categories, no data domains described.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | 0 | 0 | N/A | N/A |

**Total entities**: 0
**Total fields**: 0
**Fields with descriptions**: 0

The export documentation is strictly at the file-type level: "you get PDFs and XMLs." What those files contain is unspecified.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor does not describe what data the export covers. The documentation names two output file types — PDF encounter notes and C-CDA XML — but provides no specification of their content.

If the C-CDA uses standard sections, it would plausibly cover basic USCDI clinical domains (problems, medications, allergies, vital signs, demographics). However, this is speculative — the documentation does not confirm which C-CDA sections or template types are used.

The PDF encounter notes presumably contain the narrative text of wound care visit notes, but whether they include structured wound assessment data (measurements, staging), procedure details, photographs, or treatment plans is unknown from the documentation.

**Critically absent from even the file-type descriptions**: Any mention of billing/coding data, wound-specific structured data, outcomes data, MDS documentation, patient portal content, or facility integration data — despite these being core product capabilities.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Likely in C-CDA if standard sections used; unconfirmed | Product stores demographics (certified for (a)(5)); gap cannot be confirmed or denied |
| Encounters / visits | ⚠️ Partial | PDF encounter notes + C-CDA per encounter; but content unspecified | Product stores wound care encounters; format exists but content depth unknown |
| Problems / conditions | ⚠️ Partial | Likely in C-CDA if standard sections used; unconfirmed | Product stores problem lists; speculative coverage |
| Medications / prescriptions | ⚠️ Partial | Likely in C-CDA if standard sections used; unconfirmed | Product has CPOE (certified for (a)(2)); speculative coverage |
| Allergies | ⚠️ Partial | Likely in C-CDA if standard sections used; unconfirmed | Speculative coverage |
| Immunizations | ⚠️ Partial | Likely in C-CDA if standard sections used; unconfirmed | CQM data includes vaccination status; speculative coverage |
| Vitals | ⚠️ Partial | Likely in C-CDA if standard sections used; unconfirmed | Certified for (a)(12); speculative coverage |
| Lab results | ❌ Not covered | No evidence | Unclear if product stores labs (wound care physicians may order Dopplers/ABI but these are procedures, not labs) |
| Imaging / diagnostic reports | ❌ Not covered | No evidence | Wound photographs likely stored; Doppler/ABI results documented; no export evidence |
| Procedures | ❌ Not covered | No evidence in structured form | Product documents debridement, Doppler, skin substitutes, negative pressure therapy; **significant gap** |
| Clinical notes / documents | ⚠️ Partial | PDF encounter notes exist but content unspecified | Notes are the core product output; PDF format loses structure |
| Care plans / goals | ❌ Not covered | No evidence | Treatment plans are core to wound care; no export evidence |
| Orders / referrals | ❌ Not covered | No evidence | Dressing orders, supply orders likely in system; no export evidence |
| Insurance / coverage | ❌ Not covered | No evidence | Medicare/Medicaid billing implies insurance data; no export evidence |
| Claims / billing | ❌ Not covered | No evidence | Product name includes "Coding"; billing is core; **significant gap** |
| Payments | ❌ Not covered | No evidence | Separate billing department exists; no export evidence |
| Consents / directives | ❌ Not covered | No evidence | N/A — unclear if product stores consents |
| Patient communications | ❌ Not covered | No evidence | Patient portal exists; no export evidence |
| Wound care specialty data | ❌ Not covered | No structured evidence | Wound assessments, staging, measurements, healing trajectories, MDS documentation — the **core specialty data** of this product has no documented export coverage. **Most significant gap.** |

**Summary**: Of 19 assessed domains, 0 are confirmed covered, 6 are speculatively partially covered (assuming standard C-CDA sections), and 13 show no export evidence. The most critical gaps are the specialty wound care data and billing/coding data — the two domains that define this product.

## 6. Documentation Quality

The documentation quality is among the lowest possible while still technically existing:

- **No data dictionary**: Zero field-level documentation of any kind
- **No schema**: No machine-readable artifact (XSD, JSON Schema, C-CDA template OIDs)
- **No sample data**: No example export files
- **No C-CDA specification**: Impossible to know what data elements the XML contains
- **No PDF content specification**: Impossible to know what the encounter note PDFs contain
- **Dead admin portal link**: The only outbound link (`med.vohrawoundteam.com`) is NXDOMAIN
- **Server-side retrieval**: Export requires production server login — no API, no download link
- **Single-patient only**: No bulk export procedure documented

**Could a developer build an import from this documentation?** No. A developer would know only that they'll receive PDFs and XMLs. They would need to obtain actual export files, reverse-engineer the C-CDA template structure, and use OCR/NLP on the PDFs to extract structured data. The documentation provides zero guidance on data content, structure, or semantics.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. There are zero entities and zero fields documented. The export description — "PDFs of encounter notes and C-CDA XMLs" — is a file-type description, not a data specification. Even if the C-CDA includes standard clinical sections, that would only cover basic USCDI domains and would entirely miss the product's core specialty data (wound assessments, staging, measurements, treatment plans, procedure details, MDS documentation) and billing/coding data (the product's name literally includes "Coding"). The documentation gives no indication that any non-USCDI data is exported.

**Axis 2 — Export approach: Repackaged existing export**

The export produces C-CDA XML files — the same standard used for the product's certified (b)(1) transitions of care criterion. The documentation provides no evidence of any purpose-built export beyond C-CDA. The telltale signs are all present: reference to "the CCDA standard" with no product-specific data dictionary, no mention of wound care-specific data elements, no custom extensions, and no coverage of billing or specialty operational data. The PDF encounter notes are a document-level export (rendered notes), not a structured data export. This is the vendor's existing clinical exchange surface (C-CDA for transitions of care) plus rendered PDFs, relabeled as (b)(10).

### Key Findings

1. **The entire EHI export documentation is a single HTML page with zero field-level detail** (`CompleteExport.html`, 11,592 bytes). No data dictionary, no schema, no sample data exist. This is among the most minimal (b)(10) documentation encountered.

2. **The export format (C-CDA + PDF) is the vendor's existing clinical exchange surface**, not a purpose-built EHI export. C-CDA is certified for (b)(1) transitions of care; adding rendered PDF encounter notes does not constitute a comprehensive EHI export.

3. **The product's core specialty data — wound care assessments, staging, measurements, treatment plans, healing trajectories, MDS documentation — has no documented export coverage.** This is the most significant gap: a wound care EMR that doesn't document exporting wound care data.

4. **Billing and coding data has no documented export coverage**, despite "Coding" being in the product name and billing documentation being a core product function.

5. **The admin portal link is dead** (NXDOMAIN), and export retrieval requires production server login — raising questions about operational accessibility of the export itself.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   PDF + C-CDA XML
    Entities:        0 (no data dictionary)
    Fields:          0 (no field-level documentation)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     No (single-patient only documented)
    Domains covered: 0 confirmed; 6 speculative (assuming standard C-CDA) of 19 applicable

### Bottom Line

A patient or provider would receive PDF encounter notes and C-CDA XML files, but with no documentation of what those files contain, no ability to verify completeness, and no evidence that the product's most important data — wound care specialty assessments, procedure details, healing trajectories, and billing/coding records — is included. The export appears to be the vendor's existing C-CDA transitions-of-care capability repackaged as (b)(10), with rendered PDFs as a supplementary document-level output. The single biggest gap is the complete absence of documented wound care specialty data export from a product whose sole purpose is wound care documentation.

# EHI Export Analysis: Vohra Wound Physicians Management, LLC

**Product**: VHS Medical Documentation & Coding v3.5
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.2875.VHSM.35.00.1.181221 (ID 9887)

## 1. Product Context

VHS Medical Documentation & Coding is a proprietary, specialty wound care EMR built and used internally by Vohra Wound Physicians, the largest physician-led wound care practice in the US (~300+ physicians, ~3,000 skilled nursing facilities, 28–30 states, 1.4M annual visits). The system is purpose-built for post-acute wound care and is not sold to external customers.

**Core data domains the product stores:**
- **Wound care clinical data**: wound assessments (etiology, staging, measurements), treatment plans, dressing orders, procedure documentation (debridement, Doppler/ABI studies, skin substitutes, negative pressure therapy), wound healing trajectories
- **Standard clinical data**: demographics, vital signs, medications (CPOE), problem lists, implantable devices, family health history, allergies (implied by CDS certification)
- **Coding and billing**: the product name itself includes "Coding" — it assists physicians with diagnosis codes, procedure codes, and billing-compliant documentation. Medicare/Medicaid compliant documentation and MDS-compliant wound documentation are core features
- **Transitions of care**: C-CDA documents for care transitions
- **Clinical quality measures**: BMI screening, tobacco use, medication documentation, diabetes management, vaccination status
- **Integration data**: interoperates with PointClickCare, MatrixCare, and other post-acute EHR systems
- **Portal content**: facility portal (clinician notes, wound outcomes) and patient portal (wound care documents, telemedicine)
- **AI/ML data**: 6M historical wound cases powering predictive algorithms
- **Outcomes data**: healing timelines, re-hospitalization rates, dressing change frequency, nursing time metrics

This is a data-rich specialty system. The (b)(10) export should cover wound care clinical data, standard clinical data, and coding/billing data at minimum.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `CompleteExport.html` | 11,592 bytes | The vendor's entire EHI export documentation — a single static HTML page titled "Export data format and location." Describes export format (PDF + C-CDA XML) and single-patient export procedure. Contains no data dictionary, no schema, no field definitions. | **Primary artifact** — but extremely thin |
| `CompleteExport-screenshot.png` | 169,315 bytes | Full-page screenshot of the export documentation page as rendered in Chrome. Confirms the page renders as a single short document with Vohra branding. | Confirmatory only |
| `emr-redirect-page.html` | 3,772 bytes | Redirect notice page at the CHPL-registered URL (`emr.vohrawoundteam.com`). Uses JavaScript to redirect visitors to `facilityportal.vohrawoundteam.com`. | Documents the redirect chain |

**Total artifacts**: 3 files. No downloadable data dictionaries, schemas, sample data, or supplementary documentation were found. The export documentation page itself contains no links to any downloadable files — its only outbound link is to the administrative portal login page, which no longer exists in DNS.

## 3. Export Mechanics

- **Format**: PDF (encounter notes, one file per patient) + XML (C-CDA standard, one file per encounter)
- **Mechanism**: UI-driven via administrative portal at `https://med.vohrawoundteam.com/LogIn.aspx`. Users navigate to Advanced > Data Portability, set "Export Option" to Patient, enter patient's name and DOB, and press "Export Patients." **Note**: This admin portal domain (`med.vohrawoundteam.com`) returns NXDOMAIN — the subdomain no longer exists in DNS as of 2026-02-16, raising questions about whether the export mechanism itself is currently functional.
- **Single-patient vs bulk**: Only a single-patient export procedure is documented. The heading says "Bulk-exported records are generated into a protected place on the server," but the only procedure described is for exporting one patient at a time by name and DOB.
- **File retrieval**: Exported files are deposited on the production server (`IIS-PROD-02`) at `C:\inetpub\webapp\ExportedPatientData`. Retrieval requires logging into the server directly — there is no download mechanism through the web interface.
- **Access constraints**: Requires authenticated user with export permissions. Server-side file retrieval adds an additional access barrier.

## 4. Export Content: What's In It

The documentation provides no data dictionary, no schema, no field definitions, and no sample data. The entirety of what is documented about the export content is:

1. **PDF files**: Described only as "Encounter notes." No specification of what data elements the encounter notes contain, what sections they include, whether they contain wound measurements, photographs, or procedure details, or how they are structured.

2. **XML files**: Described only as "Data in this file conforms to the CCDA standard." No specification of:
   - Which C-CDA document type (CCD, Referral Summary, Progress Note, etc.)
   - Which C-CDA sections are included
   - Which data elements are populated
   - Whether any vendor extensions exist for wound care data
   - Which C-CDA template OIDs are used

### Vendor's own content organization

The vendor provides no content organization. There are no entities, tables, fields, categories, or any other structural description of the export content. The only information is two file types:

| File Type | Description (vendor's words) | Fields Documented | Types | Categories |
|---|---|---|---|---|
| PDF | "Encounter notes" | 0 | N/A | N/A |
| XML (C-CDA) | "Data conforms to the CCDA standard" | 0 | N/A | N/A |

**Total documented entities: 0. Total documented fields: 0.**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation covers nothing at the field level. The export produces two file types — PDFs and C-CDA XML — but provides zero detail about their contents. Based on the C-CDA standard alone, the XML files likely contain some subset of standard clinical domains (demographics, medications, allergies, problems, vitals, procedures, immunizations), but the vendor does not confirm which sections are present or how complete they are.

The PDF encounter notes likely contain wound care clinical narratives, but as rendered documents they are not computable data — a recipient cannot query, import, or transform PDF content without OCR/NLP processing.

Critically, there is no indication that the export captures the product's specialty wound care data (wound assessments, measurements, staging, healing trajectories, dressing protocols, procedure details) or coding/billing data in any structured form. C-CDA is a clinical document standard designed for care transitions and is not well-suited for specialty wound care data or billing data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Likely in C-CDA if standard sections used; undocumented | Product stores demographics (certified (a)(5)); coverage presumed but unverified |
| Encounters / visits | ⚠️ Partial | PDF encounter notes exist; C-CDA may include encounter sections | Product manages encounters; PDFs are non-computable |
| Problems / conditions | ⚠️ Partial | Likely in C-CDA if standard sections used; undocumented | Product stores problem lists; coverage presumed but unverified |
| Medications / prescriptions | ⚠️ Partial | Likely in C-CDA if standard sections used; undocumented | Product has CPOE for medications (certified (a)(2)); coverage presumed but unverified |
| Allergies | ⚠️ Partial | Likely in C-CDA if standard sections used; undocumented | Not explicitly mentioned in product docs but implied by CDS |
| Immunizations | ⚠️ Partial | Likely in C-CDA if standard sections used; undocumented | Product tracks vaccination status per CQM certification |
| Vitals | ⚠️ Partial | Likely in C-CDA if standard sections used; undocumented | Product stores vital signs (certified (a)(12)); coverage presumed but unverified |
| Lab results | ⚠️ Partial | Likely in C-CDA if standard sections used; undocumented | Unclear if product stores lab results directly |
| Procedures | ⚠️ Partial | Likely in C-CDA if standard sections used; undocumented | Product documents procedures (debridement, Doppler, etc.); wound care procedure detail unlikely in standard C-CDA |
| Clinical notes / documents | ⚠️ Partial | PDF encounter notes | Notes exported as non-computable PDFs only |
| Care plans / goals | ⚠️ Partial | Possibly in C-CDA; undocumented | Product creates treatment plans; coverage unknown |
| Insurance / coverage | ❌ Not covered | No evidence in export documentation | Product handles Medicare/Medicaid documentation; significant gap |
| Claims / billing | ❌ Not covered | No evidence in export documentation | Product name includes "Coding" — coding/billing is a core function; **major gap** |
| Specialty: Wound care | ❌ Not covered | No evidence of structured wound care data in export | Wound assessments, measurements, staging, healing trajectories, dressing protocols, procedure details are the product's core data; **most significant gap** |
| Imaging / wound photographs | ❌ Not covered | No mention of image/photo export | Wound photography is implied in product use; gap |
| Patient communications / portal | ❌ Not covered | No evidence in export | Product has patient portal and facility portal |
| Orders / referrals | ❌ Not covered | No evidence in export | Unclear if product manages referrals |
| Consents / directives | N/A | Not applicable | No evidence product stores consents |
| Payments | ❌ Not covered | No evidence in export | Product has billing department; unclear if EMR stores payment data directly |

**Coverage summary**: 0 domains are confirmed covered. At best, 8 domains may be partially covered through C-CDA (if standard sections are used), but this cannot be verified from the documentation. At least 5 domains with clear product evidence (billing/coding, wound care specialty data, wound photographs, insurance, portal content) are not covered at all. The single most important gap is the absence of structured wound care data — the entire raison d'être of this product.

## 6. Documentation Quality

The documentation quality is among the lowest possible while technically existing:

- **No data dictionary**: Zero field-level documentation of any kind
- **No schema**: No machine-readable artifact (XSD, JSON Schema, C-CDA template OIDs)
- **No sample data**: No example export files to understand what the export actually produces
- **No C-CDA specification**: Impossible to know which document type, sections, or data elements are included
- **No PDF content description**: Impossible to know what the encounter note PDFs contain
- **Dead administrative portal**: The only link in the documentation (`med.vohrawoundteam.com`) returns NXDOMAIN
- **Server-side retrieval**: Export files require logging into the production server, an unusual and operationally challenging delivery mechanism
- **No bulk procedure**: Despite the heading mentioning "bulk-exported records," only a single-patient-at-a-time procedure is documented
- **No versioning**: No version history or change tracking
- **Page last modified**: 2023-12-14 (per HTTP `Last-Modified` header) — over 2 years old

A developer could not build an import from this documentation. They would need to obtain actual export files and reverse-engineer the C-CDA structure and PDF content. Even then, the PDF encounter notes would require OCR/NLP to extract structured data.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to meaningfully assess what is exported. What is documented — PDF encounter notes plus unspecified C-CDA XML — clearly covers only a fraction of what this specialty wound care EMR stores. There is no data dictionary, no schema, no sample data, and no field-level documentation of any kind. The export mechanism's admin portal URL no longer resolves.

### Key Findings

1. **The entire EHI export documentation is a single HTML page (11,592 bytes) with zero field-level detail.** It describes two file types (PDF and C-CDA XML) without specifying what data elements either contains. (Source: `CompleteExport.html`)

2. **The product's core specialty data — wound care assessments, measurements, staging, healing trajectories, dressing protocols — has no documented path to export.** C-CDA is not designed for specialty wound care data, and the documentation gives no indication of custom extensions. This is the most significant gap: the product's primary clinical value is absent from the documented export. (Source: product-research.md vs. `CompleteExport.html`)

3. **Coding and billing data is entirely absent from the export.** The product's name is literally "Medical Documentation & Coding," and coding/billing assistance is a core function. No billing entities appear in the export documentation. (Source: `CompleteExport.html`)

4. **The administrative portal URL for triggering exports (`med.vohrawoundteam.com`) returns NXDOMAIN**, meaning the export mechanism described in the documentation may not be currently functional. (Verified: DNS lookup 2026-02-16)

5. **PDF encounter notes are non-computable.** Even if the PDFs contain clinical detail, they cannot be imported, queried, or transformed by downstream systems without OCR/NLP processing. This is a significant limitation for data portability.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   PDF + C-CDA XML
Model type:      Standard projection (C-CDA) + rendered documents (PDF)
Entities:        0 (no data dictionary)
Fields:          0 (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear (heading mentions "bulk" but only single-patient procedure documented)
Domains covered: 0 confirmed; ~8 presumed partial via C-CDA (unverifiable)
```

### Bottom Line

This is a compliance stub, not a genuine EHI export. A patient or provider would receive PDF encounter notes (non-computable) and C-CDA XML files (content unspecified), with no access to the product's core wound care specialty data, coding/billing data, or any structured native data. The single biggest gap is the complete absence of wound care clinical data — the product's entire purpose — from the documented export.

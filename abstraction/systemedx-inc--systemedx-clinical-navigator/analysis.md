# EHI Export Analysis: Systemedx Inc

**Product**: Systemedx Clinical Navigator v2024.12
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2857.Syst.24.02.1.241126 (CHPL ID 11536)

## 1. Product Context

Systemedx Clinical Navigator is an all-in-one ambulatory EHR and practice management system from a small vendor (~11–50 employees) headquartered in Cullman, Alabama. It targets ambulatory practices with a notable specialty presence in orthopedic and sports medicine.

The product is a single integrated platform encompassing:

- **EHR / Clinical Documentation**: Office visit notes with AI assistance, medication management (including EPCS/PDMP), orders (labs, imaging, meds via "Touch Orders"), drug interaction checking, patient tracking, customizable forms and templates
- **Practice Management**: Scheduling, patient registration, AI-assisted CPT/ICD coding, claims submission, claim scrubbing, remittance auto-posting, eligibility verification, batched statement generation, financial dashboards
- **Patient Portal**: Self-registration, appointment requests, medication refill requests, secure messaging, online bill pay, clinical summary access
- **Surgical Pathways**: Surgical case tracking, AI-driven billing with "rogue surgery detection," automated CPT suggestion, pre/post-op task lists, patient text reminders, surgical performance dashboards
- **MIPS/Quality Reporting**: Measure calculation dashboards, QPP submission
- **Interfaces**: HL7 2.x lab interfaces (LabCorp, Quest, hospital labs), physical therapy, DME, dictation, imaging system integrations

The product is certified for 37 ONC criteria including (b)(10) EHI export. Given its breadth as a combined EHR + PM + surgical pathways system, a complete EHI export should cover clinical data (encounters, meds, problems, labs, allergies, vitals, immunizations, notes), billing/financial data (claims, charges, payments, remittances), surgical pathway data, and patient portal communications.

## 2. Artifacts Reviewed

| Artifact | Description | Informative Value |
|---|---|---|
| `dataExport.html` (19,629 bytes) | The EHI export documentation page at the CHPL-registered URL. A static HTML page containing 232 words of substantive EHI export documentation. Describes export modes and output formats. No data dictionary, schema, field-level detail, or downloadable artifacts. | **Primary source** — the only artifact containing EHI export information |
| `Mandatory-Disclosures-2022.pdf` (771,734 bytes, 2 pages) | ONC mandatory cost transparency disclosures listing fees for 9 certified capabilities. Does not mention (b)(10) data export or any associated costs. | Low — confirms no fee disclosure for EHI export |
| `dataExport-screenshot.png` (751,930 bytes) | Full-page screenshot of the dataExport.html page. | Minimal — visual confirmation of the HTML page content |

**Total artifacts**: 3 files. Only one (the HTML page) contains any EHI export documentation, and it provides no field-level, schema, or structural detail whatsoever.

## 3. Export Mechanics

- **Format**: CDA XML files (template/profile not specified), human-readable CDA HTML copies, and PDF chart documents
- **Mechanism**: UI-based — accessed through a job stream called "CDAEXPORT" that appears as "Data Export" in the application interface
- **Single-patient**: Yes — "Single Patient" mode explicitly supported
- **Bulk capability**: Yes — "All Patients" mode with configurable date range, and "Select Patients" mode (manual selection or by appointment date range)
- **Configuration options**: Output directory, date range, checkbox to include chart documents, checkbox to include human-readable CDA HTML copy
- **Folder structure**: Patient files organized into folders named `LastName_FirstName_DOB_PatientID`
- **Access constraints or fees**: None documented. The Mandatory Disclosures PDF lists fees for 9 other capabilities but does not mention any cost for the (b)(10) data export.

## 4. Export Content: What's In It

### What the documentation says

The entire description of export content is a single bullet-point list (verbatim from `dataExport.html`):

> • Patient demographics and distinct chart data (medications, problems, etc.) are exported as CDA XML files
> • CDA files are also exported as human-readable HTML files named "CDA.html"
> • Patient chart documents are exported as PDF documents and stored in a main "Documents" folder with each document type separated into their own folder
> • CDA files and other documents and images are placed into folders named [by patient identifiers]

### What's documented vs. what's missing

- **No data dictionary**: Zero entities, zero fields documented
- **No schema**: No XSD, JSON Schema, or any machine-readable specification
- **No sample data**: No example CDA files, HTML files, or export folder structures
- **No CDA template specification**: Does not state whether this is C-CDA R2.1, C-CDA R2.0, raw CDA R2, or a custom CDA template. Without this, the CDA sections and data elements included are entirely unknown.
- **No section inventory**: Does not list which CDA sections are included (allergies? immunizations? vital signs? results? procedures?)
- **No value sets or terminology documentation**
- **No relationship documentation**
- **"etc." as documentation**: The phrase "medications, problems, etc." uses "etc." to hand-wave the remainder of the clinical data content. This is the only hint at what clinical data is included.

### Vendor's own content organization

There is no data dictionary or entity inventory to present. The vendor provides no structured information about export content. The only data elements explicitly named are:

| Data Element | Source Format | Evidence |
|---|---|---|
| Patient demographics | CDA XML | Explicitly stated in documentation |
| Medications | CDA XML | Explicitly stated ("medications") |
| Problems | CDA XML | Explicitly stated ("problems") |
| "distinct chart data" (undefined) | CDA XML | Mentioned but undefined; qualified only with "etc." |
| Chart documents | PDF | Explicitly stated; organized by document type in subfolders |
| "documents and images" | PDF/image files | Mentioned in folder structure description |

**Entity count: 0** documented entities/tables. **Field count: 0** documented fields. There is no data dictionary to parse.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes two categories of export output:

1. **CDA XML files**: Contain "patient demographics and distinct chart data (medications, problems, etc.)." The scope of "distinct chart data" is entirely undefined. If this is a standard C-CDA document, it would typically include allergies, medications, problems, procedures, results, vital signs, immunizations, encounters, and care plan sections — but this is speculation, not documentation. The CDA template is not specified.

2. **PDF/image chart documents**: Patient chart documents exported as PDFs, organized by document type in subfolders. This likely includes scanned documents, clinical notes, and possibly lab reports stored as documents — but the documentation does not enumerate what document types exist.

The documentation is too thin to characterize depth in any domain. No field-level information exists for any category.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Mentioned explicitly ("patient demographics") but no field-level detail | Product stores demographics; mentioned in export but no way to verify completeness |
| Encounters / visits | ❌ Not covered | Not mentioned in documentation | Product documents encounters; absence from documentation is a gap |
| Problems / conditions | ⚠️ Partial | Mentioned explicitly ("problems") but no detail | Mentioned but undefined scope |
| Medications / prescriptions | ⚠️ Partial | Mentioned explicitly ("medications") but no detail | Product has extensive Rx features (EPCS, PDMP); mentioned but unknown depth |
| Allergies | ❌ Not covered | Not mentioned (may be in CDA if standard template) | Likely stored by product; not documented in export |
| Immunizations | ❌ Not covered | Not mentioned (may be in CDA if standard template) | Product is certified for immunization registry reporting (f)(1); likely stored but not documented in export |
| Vitals | ❌ Not covered | Not mentioned (may be in CDA if standard template) | Likely stored; not documented |
| Lab results | ❌ Not covered | Not mentioned; product has lab interfaces | Product receives lab results via HL7 interfaces (LabCorp, Quest, etc.); significant gap if absent |
| Imaging / diagnostic reports | ❌ Not covered | Not mentioned; product has imaging interfaces | Product integrates with imaging systems; not documented in export |
| Procedures | ❌ Not covered | Not mentioned | Product tracks surgical procedures extensively; significant gap |
| Clinical notes / documents | ⚠️ Partial | PDF chart documents included but not enumerated | PDF export of chart documents likely captures clinical notes; no detail on types |
| Care plans / goals | ❌ Not covered | Not mentioned | Unknown if product stores structured care plans |
| Orders / referrals | ❌ Not covered | Not mentioned | Product has "Touch Orders" for labs/imaging/meds; not documented in export |
| Insurance / coverage | ❌ Not covered | Not mentioned | Product stores insurance data (patient registration, eligibility verification); significant gap |
| Claims / billing | ❌ Not covered | Not mentioned; CDA format does not carry billing data | Product has full PM with claims submission, AI-assisted coding, remittance posting; **major gap** |
| Payments | ❌ Not covered | Not mentioned | Product handles payments and statement generation; significant gap |
| Consents / directives | ❌ Not covered | Not mentioned | Unknown if product stores advance directives |
| Patient communications | ❌ Not covered | Not mentioned | Product has patient portal with secure messaging; gap if messages are stored |
| Specialty-specific (surgical pathways) | ❌ Not covered | Not mentioned | Product's surgical pathways module with case tracking, billing recovery, and task management is a key differentiator; **major gap** |

**Summary**: Of 19 standard domains assessed, the documentation explicitly mentions content for only 3 (demographics, medications, problems) — all at a superficial "mentioned but not detailed" level. The remaining 16 domains are entirely absent from the documentation. Even if the CDA export includes standard C-CDA sections (allergies, vitals, immunizations, etc.), the vendor has not documented this, and CDA structurally cannot carry billing, surgical pathway, or practice management data.

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the worst possible for a certified product:

- **232 words** of substantive EHI export documentation on the entire page
- **Zero** entities, tables, or fields documented
- **Zero** machine-readable artifacts (no schema, no sample data, no downloadable files)
- **No CDA template specified** — a developer cannot even determine which CDA profile to parse
- **"etc." used as documentation** — the phrase "medications, problems, etc." is the entirety of the clinical data description
- **Stale**: The page's `Last-Modified` HTTP header shows May 5, 2022 — over 2.5 years before the product's November 2024 certification date. The documentation was not updated for the certification cycle.
- **No developer guidance**: A developer receiving this export would need to reverse-engineer the CDA XML files with zero documentation support. Without knowing the CDA template, even basic parsing decisions (which sections to expect, what coded values to look for) cannot be made from the documentation alone.
- **No import feasibility**: It would be impossible to build an import/migration tool from this documentation. A developer would need sample export files and would have to reverse-engineer every aspect of the data structure.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The documentation is too thin to assess the actual scope of the export. What can be determined is:
1. The export is CDA-based, which structurally limits it to clinical document content — CDA cannot carry billing, claims, surgical pathway, or practice management data.
2. The documentation provides zero field-level detail, zero schema information, and zero sample data.
3. Even within clinical data, the scope is undefined — "medications, problems, etc." with "etc." doing all the work.

This is a compliance checkbox — the minimum required to have a URL registered with CHPL. It describes *how to trigger* the export but not *what the export contains*.

### Key Findings

1. **Documentation is 232 words with zero structural detail.** The entire EHI export documentation consists of a single HTML page describing three export modes and four bullet points about output formats. There is no data dictionary, no schema, no sample data, and no field-level documentation of any kind. (`dataExport.html`)

2. **Export is CDA-based, structurally excluding billing and PM data.** The export produces CDA XML files and PDF documents. CDA is a clinical document standard that does not accommodate billing records, claims, surgical case tracking, practice management data, or payment information — all of which are core product capabilities. (`dataExport.html`, bullet 1)

3. **Product has extensive PM and surgical pathway capabilities with no export coverage.** Systemedx Clinical Navigator is a combined EHR + PM + surgical pathways system with AI-assisted coding, claims submission, remittance auto-posting, rogue surgery detection, and surgical billing recovery. None of this data is documented as part of the export, and CDA format cannot carry it.

4. **Documentation predates current certification by 2.5 years.** The `Last-Modified` header shows May 5, 2022; the product was certified November 26, 2024. The documentation was not reviewed or updated during the certification process. (HTTP headers verified 2026-02-16)

5. **No cost disclosure for EHI export.** The Mandatory Disclosures PDF lists fees for 9 other capabilities (including $10,000/year for API access) but does not mention the (b)(10) data export, leaving cost transparency unclear. (`Mandatory-Disclosures-2022.pdf`)

### Summary Stats

    Classification:  Minimal/stub
    Export format:   CDA XML + CDA HTML + PDF
    Model type:      Standard-based projection (CDA)
    Entities:        N/A (no data dictionary)
    Fields:          N/A (no data dictionary)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Yes (All Patients and Select Patients modes)
    Domains covered: 3 of 19 applicable domains partially mentioned; 0 substantively documented

### Bottom Line

Systemedx Clinical Navigator's EHI export documentation is a 232-word page describing how to trigger a CDA-based export with no detail about what data is actually exported. For a product that combines EHR, practice management, and surgical pathways, a CDA export structurally cannot cover billing, claims, surgical case data, or practice management records — all of which are EHI. The single biggest gap is the complete absence of any documentation: not just missing billing data, but the inability to determine from the documentation alone what *any* part of the export actually contains.

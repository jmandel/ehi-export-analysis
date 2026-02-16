# EHI Export Analysis: Prime Clinical Systems, Inc.

**Product**: Patient Chart Manager
**Analysis date**: 2026-02-16
**CHPL ID**: 15.02.05.2206.PRIC.01.03.1.220114 (CHPL listing 10791)

## 1. Product Context

Patient Chart Manager (PCM) is an ambulatory EHR from Prime Clinical Systems, a small vendor founded in 1983 in Pasadena, CA. The product serves solo practitioners through mid-sized multi-specialty groups (up to ~100 providers) across 14+ specialties including Family Practice, Internal Medicine, OB/GYN, Pediatrics, Cardiology, Dermatology, Orthopedics, and Psychiatry.

PCM is tightly integrated with Prime Clinical's practice management platform (branded variously as OnSTAFF, Intellect, and WebSTAFF), sharing a common database. Together they cover:

- **Clinical documentation**: Electronic charting with templated, dictated, and scanned inputs; DICOM imaging; care plans
- **E-prescribing**: Electronic prescription routing, renewal handling, prescription history
- **Lab & orders**: Lab report integration, allergy tracking
- **Patient portal**: View/download/transmit health information (certified under (e)(1))
- **Practice management**: Appointment scheduling, patient registration, insurance eligibility verification, medical billing/claims (1,300+ insurers), CMS-1500 forms, ICD-10 coding, CPT tracking, payment posting, aging reports, charge posting
- **Interoperability**: C-CDA, Direct messaging, FHIR APIs (certified for (g)(7)-(g)(10))
- **Public health**: Immunization, syndromic surveillance, and cancer registry reporting

This is a combined EHR + PM system. A comprehensive (b)(10) export should cover clinical data (demographics, allergies, medications, labs, vitals, notes, immunizations, problems, procedures) **and** administrative/billing data (insurance, claims, charges, payments).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI_Export_170.315_b10.pdf` | 3-page PDF titled "Export Format & Naming Conventions," dated 12/23/2025, PCM Ver. 7.1.1877. The entire EHI export documentation. | **Primary artifact** — but very thin |
| `downloads/EHI_Export_page1.png` | Rendered page 1: general format notes, default export location, XMLDATAExport contents (5 XML files visible in screenshot), CDAXMLExport description | Helpful — screenshot shows actual file listing |
| `downloads/EHI_Export_page2.png` | Rendered page 2: chart document naming conventions, patient data table naming conventions, CDASUMDATA.Zip screenshot (1 file visible), beginning of Section C (migration) | Moderately helpful — reveals CDAFULSUM entity and naming patterns |
| `downloads/EHI_Export_page3.png` | Rendered page 3: VB6 code examples for saving/reloading ADO XML recordsets, next steps, support contact | Low — only code examples |
| `chpl-metadata.json` | CHPL certification details: 37 certified criteria including (b)(10), version 7.1, certified 2022-01-14 | Context only |
| `metadata.json` | Developer contact info (Cindy McMichael, cindym@primeclinical.com, 626.449.1705) | Context only |

**No data dictionary, schema, sample data, or field-level documentation exists.** The entire EHI export documentation is a single 3-page PDF focused on file naming and directory structure.

## 3. Export Mechanics

- **Format**: Microsoft ADO XML recordsets (VB6 `adPersistXML` format) for structured data, plus C-CDA R2.1 for clinical documents
- **Mechanism**: UI-driven export with checkbox options controlling what's included. When no checkboxes are selected, only "Patient Data" is exported. Default export location is a network share (`\\SERVERNAME\BarcodeScans\HL7ExportFiles\CDAexports_#`).
- **Single-patient and bulk**: The documentation states "CDA for both single-patient and patient population" EHI is supported
- **Output structure**: Multiple ZIP files per export session:
  1. `XMLDATAExport_#.zip` — core data tables as ADO XML
  2. `CDAXMLExport_#.zip` — C-CDA documents (only with Bulk CCDA Export)
  3. `CDAXMLDOC.Zip` — chart documents as embedded PDFs in C-CDA format
  4. `CDASUMDATA.Zip` — CDA summary data (visible in screenshot, not described in text)
- **Access constraints**: No fees mentioned. A "HIDE" option allows excluding certain data tables, but the companion document ("Including and Excluding Data") was not found online.

## 4. Export Content: What's In It

### No data dictionary exists

The 3-page PDF provides **zero field-level documentation**. There is no listing of database columns, data types, value sets, foreign keys, or field descriptions for any table. The only structured information is:

- **6 table/entity names** visible across text and screenshots
- **5 field names** referenced incidentally in file naming convention examples
- **0 field definitions** — no types, descriptions, or value sets

The ADO XML format is self-describing (each file embeds its schema), so a recipient of actual export data could discover field names and types from the files themselves. However, no sample data or schema documentation is provided.

### Vendor's own content organization

The PDF does not organize content by domain. It organizes by export component (ZIP file). The entities visible are:

| Entity/Table | Fields | Described | Types | Source in PDF |
|---|---|---|---|---|
| CHART_DOCS | 0 | N/A | N/A | XMLDATAExport screenshot + text (10 KB uncompressed) |
| CHART_STORE | 0 | N/A | N/A | XMLDATAExport screenshot + text (7 KB uncompressed) |
| PATIENT | 0 | N/A | N/A | XMLDATAExport screenshot + text (39 KB uncompressed, largest) |
| PT_ALLERGIES | 0 | N/A | N/A | XMLDATAExport screenshot (11 KB uncompressed) |
| PT_COMPLAINTS | 0 | N/A | N/A | XMLDATAExport screenshot (6 KB uncompressed) |
| CDAFULSUM | 0 | N/A | N/A | CDASUMDATA.Zip screenshot on page 2 |

Additionally, `PT_CHART_DOCS` is referenced as a data table in the naming convention section (field `cdview_cddocid` / `cd_doc_id`), but is not visible in the export screenshot — it may be a view rather than a separate exported table.

The 5 incidentally referenced fields are:
- `pa_clinic` (PATIENT table)
- `pa_account` (PATIENT table)
- `cs_mr_num` (CHART_STORE table)
- `cs_cl_key` (CHART_STORE table)
- `cd_doc_id` / `cdview_cddocid` (PT_CHART_DOCS)

### Critical ambiguity

The PDF states: *"All patient data tables included (except those hidden via HIDE option)."* This could mean the actual export contains many more tables than the 5 shown in the screenshot — medications, labs, vitals, problems, immunizations, etc. — but the documentation provides no enumeration. The screenshot shows only 5 files in `XMLDATAExport_9.Zip`, and it is unclear whether this is a representative sample or the complete set. The file sizes are small (6–39 KB), consistent with either a small patient sample or limited data scope.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation reveals only five named data tables plus C-CDA documents and chart document exports. The documentation is organized around export file structure rather than data domains:

1. **Patient data** (PATIENT table, 39 KB): The largest table; presumably demographics and registration data. No fields listed.
2. **Allergies** (PT_ALLERGIES, 11 KB): Patient allergy data. No fields listed.
3. **Complaints** (PT_COMPLAINTS, 6 KB): Likely chief complaint / reason for visit. No fields listed.
4. **Chart documents** (CHART_DOCS + CHART_STORE + CDAXMLDOC.Zip): Document metadata and the documents themselves as embedded PDFs in C-CDA format. This is the richest documented component — the naming conventions show cross-referencing between patient, chart store, and document tables via MRN, clinic, account, and document IDs.
5. **Clinical summaries** (CDAXMLExport + CDAFULSUM): C-CDA R2.1 clinical summaries, available with bulk export.

The strongest assertion in the documentation is that "all patient data tables" are included. But without enumeration, this is unverifiable. The documentation does not mention any billing, insurance, medication, lab, immunization, vital sign, procedure, or care plan tables by name.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | PATIENT table exists (39 KB) but no fields documented | Table name suggests coverage; no verification possible without field list |
| Encounters / visits | ❌ Not covered | No encounter table mentioned | Product manages visits/appointments; gap if not in "all patient data tables" |
| Problems / conditions | ⚠️ Partial | PT_COMPLAINTS table; may cover chief complaints but unclear if full problem list | Product manages problem lists per (a)(5) certification |
| Medications / prescriptions | ❌ Not covered | No medication table mentioned | Product has e-prescribing; significant gap if absent |
| Allergies | ⚠️ Partial | PT_ALLERGIES table exists but no fields documented | Table exists but content unknown |
| Immunizations | ❌ Not covered | No immunization table mentioned | Product reports to immunization registries ((f)(1)); gap if absent |
| Vitals | ❌ Not covered | No vitals table mentioned | Standard EHR data; gap if absent |
| Lab results | ❌ Not covered | No lab table mentioned | Product integrates lab results; gap if absent |
| Imaging / diagnostic reports | ❌ Not covered | No imaging table mentioned | Product is DICOM-compatible; gap if absent |
| Procedures | ❌ Not covered | No procedure table mentioned | Standard ambulatory EHR data; gap if absent |
| Clinical notes / documents | ✅ Covered | CHART_DOCS, CHART_STORE, CDAXMLDOC.Zip with embedded PDFs in C-CDA | Most thoroughly documented component |
| Care plans / goals | ❌ Not covered | No care plan table mentioned | Listed as product feature; gap if absent |
| Orders / referrals | ❌ Not covered | No orders table mentioned | Standard EHR data |
| Insurance / coverage | ❌ Not covered | No insurance table mentioned | Product manages insurance verification; gap if absent |
| Claims / billing | ❌ Not covered | No billing table mentioned | Product has extensive billing (CMS-1500, claims, charge posting); **major gap** if absent |
| Payments | ❌ Not covered | No payment table mentioned | Product manages payment posting, aging reports; gap if absent |
| Consents / directives | ❌ Not covered | No consent table mentioned | N/A — unclear if product stores these |
| Patient communications | ❌ Not covered | No communications table mentioned | Product has patient portal; gap if absent |

**Important caveat**: The vendor claims "all patient data tables included." If taken at face value, many of the ❌ domains above may actually be present in the export but simply undocumented. The documentation failure is that it provides no way to verify this claim. The 5 visible tables in the screenshot represent only a tiny fraction of what an integrated EHR+PM system would be expected to store.

## 6. Documentation Quality

The documentation is **extremely minimal** — among the thinnest (b)(10) documentation possible:

- **No data dictionary**: Zero fields, types, or descriptions documented for any table
- **No schema**: No machine-readable schema files (XSD, JSON Schema, etc.)
- **No sample data**: No example export files or test datasets
- **No value sets**: No coded value documentation
- **No relationships**: No foreign key or entity relationship documentation (though naming conventions hint at linkages via MRN, clinic, account IDs)
- **No import guide beyond VB6**: The migration section provides VB6 code examples for ADO XML deserialization but no guidance on interpreting the data

A developer receiving this export would need to:
1. Understand Microsoft ADO XML recordset format (legacy VB6 technology)
2. Parse embedded schema from each XML file to discover field names and types
3. Reverse-engineer relationships between tables from field naming conventions
4. Guess at the meaning of coded fields without value set documentation

The documentation answers "where are the files and how do I open them?" but not "what data is in them?" or "how does it all relate?" It would be very difficult to build a reliable import from this documentation alone.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to make a reliable coverage assessment. Only 5 data tables are visibly confirmed in the export, and zero fields are documented. The vendor's claim that "all patient data tables" are included *could* mean comprehensive coverage, but the documentation provides absolutely no evidence to support this. Given that the product is an integrated EHR + practice management system with billing, scheduling, e-prescribing, lab integration, immunization reporting, and more, the 5 visible tables (PATIENT, PT_ALLERGIES, PT_COMPLAINTS, CHART_DOCS, CHART_STORE) would represent only a small fraction of the expected data model. No billing, medication, lab, immunization, vital sign, or procedure data is mentioned anywhere. The C-CDA component adds clinical summary coverage but is the existing (g)(10) clinical exchange format, not purpose-built EHI content.

**Axis 2 — Export approach: Purpose-built EHI export**

Despite the documentation deficiencies, the export approach itself is purpose-built for (b)(10) — it is a native database dump using ADO XML recordsets, not a repackaged C-CDA or FHIR export. The vendor built a mechanism to export internal database tables (PATIENT, PT_ALLERGIES, PT_COMPLAINTS, CHART_DOCS, CHART_STORE) in their native format, supplemented by C-CDA documents. This is clearly distinct from their (g)(10) FHIR API or C-CDA exchange. The ADO XML format preserves the internal database schema and data types, which is the right approach for a (b)(10) export. The problem is not the approach but the documentation and potentially the scope.

### Key Findings

1. **Documentation is a 3-page stub with zero field-level detail.** The entire EHI export documentation is a single PDF that describes file naming conventions and directory structure. No data dictionary, no field definitions, no sample data, no schema. This is among the thinnest (b)(10) documentation reviewed. (`EHI_Export_170.315_b10.pdf`, 3 pages)

2. **Only 5 data tables are visibly confirmed.** The XMLDATAExport screenshot shows CHART_DOCS, CHART_STORE, PATIENT, PT_ALLERGIES, and PT_COMPLAINTS. A 6th entity (CDAFULSUM) appears in a separate screenshot. No billing, medication, lab, immunization, vital, or procedure tables are mentioned. (Page 1 screenshot)

3. **The vendor claims "all patient data tables included" but provides no enumeration.** This is the central ambiguity — the export may be comprehensive but the documentation makes it impossible to verify. The referenced "Including and Excluding Data" companion document was not found online. (Page 1 text)

4. **The export approach is legitimate but the technology is dated.** ADO XML recordsets (VB6 `adPersistXML`) are a functional but legacy format from the late 1990s. The VB6 code examples for reading the export are from a bygone era of Windows development. This is consistent with the product's 40+ year development history.

5. **Billing/PM data is the most significant potential gap.** The product has extensive practice management capabilities (claims, CMS-1500, payment posting, insurance verification, charge posting), but no billing-related tables appear in the export documentation. For an integrated EHR+PM system, omitting billing data would be a major (b)(10) compliance gap.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Purpose-built EHI export
    Export format:   Microsoft ADO XML recordsets + C-CDA R2.1
    Entities:        6 (visible in documentation; actual count unknown)
    Fields:          0 documented (actual fields undiscoverable without sample data)
    Descriptions:    N/A (0 fields documented)
    Sample data:     No
    Bulk export:     Yes (single-patient and population)
    Domains covered: 3 of 18 applicable domains confirmed (demographics, allergies, clinical notes); others unverifiable

### Bottom Line

The export mechanism (ADO XML database dump + C-CDA documents) is a legitimate purpose-built approach, but the documentation is a near-total failure — 3 pages with zero field definitions, no data dictionary, and no way to verify what's actually exported. A patient or developer receiving this export would get files they could technically parse (ADO XML is self-describing) but would have no documentation to interpret the data. The biggest risk is that the export may omit billing, medications, labs, and other critical domains from this integrated EHR+PM system — but the documentation is too thin to confirm or deny this.

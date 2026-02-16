# EHI Export Analysis: MDLAND

**Product**: iClinic v12.3
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1828.iCli.12.00.1.181221

## 1. Product Context

iClinic is a comprehensive cloud-based ambulatory EHR and practice management system developed by MDLand International Corp. It serves outpatient physician practices of all sizes, from solo providers to large organizations like Northwell Health and NYC Health + Hospitals. The product integrates clinical documentation, e-prescribing (including EPCS), lab/imaging interfacing, billing/claims management, scheduling, a patient portal (iClinicHealth), telehealth, and care management (CCM, RPM, TCM, CoCM, PCM) into a single platform.

Key data domains the product stores that a (b)(10) export should cover:
- **Patient demographics** — registration, photos, ID scans, insurance info
- **Clinical records** — encounter notes via customizable templates, problem lists, vitals
- **Medications** — active lists, prescription history, controlled substance e-prescribing
- **Allergies** — allergy and intolerance lists
- **Lab results** — orders, results, trending data
- **Imaging** — orders and results
- **Immunizations** — vaccination history
- **Documents** — scanned/uploaded files, consultation letters, forms
- **Billing/claims** — electronic claims, claim statuses, payments, eligibility checks
- **Patient portal messages** — secure messaging
- **Telehealth** — video visit records
- **Care management** — CCM/RPM/TCM enrollment, care plans, time tracking, remote monitoring data
- **Scheduling** — appointments

The integrated billing module is particularly notable — the product handles electronic claim submission, payment posting, and eligibility checking, meaning substantial billing data exists that should appear in a comprehensive export.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehiexport.pdf` | 2-page PDF (250 KB) describing the EHI export workflow. Created 2023-12-01 by Catherine Cai via Microsoft Word. Documents the UI trigger process and states the export format is XML in a password-protected ZIP. Contains two screenshots of the export UI. **No data dictionary, schema, field definitions, or sample data.** | Low — answers "how to trigger" but not "what's in it" |
| `downloads/ehiexport-page1.png` | PNG render of PDF page 1 (231 KB) — regulatory text and workflow description | Low — same content as PDF text |
| `downloads/ehiexport-page2.png` | PNG render of PDF page 2 (275 KB) — screenshots of the export UI showing batch editor and download list | Low — confirms UI mechanism only |

The single PDF is the only artifact. No data dictionary, XML schema (XSD/DTD), sample XML file, or any other technical documentation was found. The entirety of the EHI export documentation fits on two pages.

## 3. Export Mechanics

- **Format**: XML files inside a password-protected ZIP archive
- **Format reference**: Generic W3C XML specification (https://www.w3.org/TR/xml/) — no vendor-specific schema
- **Mechanism**: UI-driven. Authorized users navigate to Settings → Advanced → Patient Data Export, select scope, and click Submit. MDLand IT processes the request server-side (10 minutes to several hours). The user receives an iClinic Inbox message with the ZIP password, then downloads the file.
- **Single-patient vs bulk**: Both supported. Scope options include: All Patients, All Active Patients, Patients with Encounters, Patients with DOB, or Specify Patient (single)
- **Access constraints**: Restricted to users with "Advanced Settings" privileges
- **Fees**: Not documented
- **Notable**: The export requires MDLand IT to process the request — users cannot generate exports independently despite the regulation requiring operation "without subsequent developer assistance." Step 3 of the documented workflow explicitly states "After MDLand IT completes the processing."

## 4. Export Content: What's In It

### What the documentation says

The PDF claims the export includes "all of a single patient's electronic health information stored at the time of certification." It provides no further detail about what data is included.

### What can be verified

**Nothing.** The documentation provides:
- 0 entities/tables documented
- 0 fields documented
- 0 field descriptions
- 0 data type definitions
- 0 value sets or code systems
- 0 relationship/foreign key definitions
- No XML schema, DTD, or XSD
- No sample XML output
- No list of data domains included

### Vendor's own content organization

There is no vendor-provided content organization. The PDF does not categorize, enumerate, or describe any data elements. The only content-related statement is the generic claim that "all" EHI is exported.

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation makes a single blanket claim: the export contains "all of a single patient's electronic health information." No categories, modules, sections, tables, or fields are enumerated. There is no way to assess depth or breadth from the documentation alone.

The export format is described as proprietary XML (not C-CDA, not FHIR), which suggests a purpose-built export rather than a repackaged clinical exchange. However, without a schema or sample data, this cannot be confirmed.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No documentation | Product stores demographics; cannot assess |
| Encounters / visits | ❓ Unknown | No documentation | Product stores encounter notes; cannot assess |
| Problems / conditions | ❓ Unknown | No documentation | Product stores problem lists; cannot assess |
| Medications / prescriptions | ❓ Unknown | No documentation | Product stores medications and e-prescribing data; cannot assess |
| Allergies | ❓ Unknown | No documentation | Product stores allergies; cannot assess |
| Immunizations | ❓ Unknown | No documentation | Product stores immunization records; cannot assess |
| Vitals | ❓ Unknown | No documentation | Product stores vitals; cannot assess |
| Lab results | ❓ Unknown | No documentation | Product stores lab orders and results; cannot assess |
| Imaging / diagnostic reports | ❓ Unknown | No documentation | Product interfaces with imaging centers; cannot assess |
| Procedures | ❓ Unknown | No documentation | Cannot assess |
| Clinical notes / documents | ❓ Unknown | No documentation | Product stores clinical documentation and scanned documents; cannot assess |
| Care plans / goals | ❓ Unknown | No documentation | Product has CCM/RPM care management with care plans; cannot assess |
| Orders / referrals | ❓ Unknown | No documentation | Product supports lab/imaging ordering; cannot assess |
| Insurance / coverage | ❓ Unknown | No documentation | Product stores insurance info and eligibility data; cannot assess |
| Claims / billing | ❓ Unknown | No documentation | Product has integrated billing with claims, payments, eligibility; cannot assess |
| Payments | ❓ Unknown | No documentation | Product posts electronic payments; cannot assess |
| Patient communications | ❓ Unknown | No documentation | Product has patient portal with secure messaging; cannot assess |
| Telehealth records | ❓ Unknown | No documentation | Product supports telehealth visits; cannot assess |

**Every domain is unknown.** The documentation provides zero evidence for or against coverage of any data domain. The vendor claims "all" EHI is exported, but provides no substantiation.

## 6. Documentation Quality

The documentation is insufficient for any practical purpose beyond triggering the export:

- **Can a developer understand the export?** No. The XML structure is completely undocumented. A developer receiving this export would need to reverse-engineer the XML to understand its structure.
- **What's well-documented?** Only the UI workflow for triggering the export (4 steps with screenshots).
- **What requires guesswork?** Everything about the content and structure of the exported data.
- **Machine-readable artifacts?** None. No schema, no sample data, no data dictionary in any format.
- **Could you build an import?** Not from this documentation. You would need an actual export file to reverse-engineer.

This is among the thinnest EHI export documentation possible — it tells you how to push the button but nothing about what comes out.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess coverage. The vendor makes a blanket "all EHI" claim but provides zero evidence: no data dictionary, no entity list, no field definitions, no sample data, no schema. iClinic is a feature-rich product with clinical, billing, care management, and patient engagement capabilities — there should be substantial data to document. The complete absence of content documentation means we cannot determine whether the export covers 10% or 100% of the product's data.

**Axis 2 — Export approach: Unclear/undetermined**

The export appears to be a purpose-built mechanism (proprietary XML in ZIP, separate from FHIR/C-CDA), which is a positive signal. The vendor did not simply point to their (g)(10) FHIR API or C-CDA exchange. However, without a schema or sample data, it's impossible to confirm whether this is a genuine comprehensive database export or a minimal XML wrapper around limited data. The requirement for "MDLand IT" to process the export suggests server-side database extraction, which could indicate a comprehensive dump — but this is speculation.

### Key Findings

1. **Zero content documentation**: The entire EHI export documentation is a 2-page PDF that describes only the export trigger workflow. No data dictionary, XML schema, field definitions, or sample data exist. This is one of the thinnest documentations reviewed. (Source: `ehiexport.pdf`, 2 pages, 250 KB)

2. **Vendor-assisted processing raises (b)(10) compliance concerns**: Step 3 of the workflow requires "MDLand IT" to process the export, which appears to conflict with the (b)(10) requirement that users operate "without subsequent developer assistance." (Source: `ehiexport.pdf`, page 1, Step 3)

3. **Proprietary XML format with no schema**: The export uses a proprietary XML format with only a reference to the generic W3C XML specification. Without an XSD, DTD, or sample file, a recipient cannot programmatically parse the data without reverse engineering. (Source: `ehiexport.pdf`, "Export File Format" section)

4. **Product has substantial data breadth**: iClinic stores clinical, billing, care management, telehealth, and patient portal data — at least 15+ data domains that should be covered. The complete absence of documentation makes it impossible to verify whether this comprehensive product has a comprehensive export. (Source: `product-research.md`)

5. **Not a repackaged standard**: The export is clearly not a relabeled C-CDA or FHIR export — it uses proprietary XML and a distinct UI workflow. This is a positive signal that the vendor attempted a purpose-built export, even though the documentation fails to describe it.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined
Export format:   Proprietary XML in password-protected ZIP
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (patient population export supported)
Domains covered: 0 of 18 verifiable (vendor claims "all" but provides no evidence)
```

### Bottom Line

A patient or provider receiving this export would get an XML file in an undocumented proprietary format with no schema, no data dictionary, and no way to understand its contents without reverse engineering. The vendor claims to export "all" EHI and appears to have built a purpose-specific mechanism (not a repackaged FHIR/C-CDA export), but the complete absence of content documentation — zero entities, zero fields, zero structural definitions — makes it impossible to verify this claim. The single biggest gap is the total lack of a data dictionary or schema: the documentation answers "how to push the button" but says nothing about what comes out.

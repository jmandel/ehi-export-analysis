# EHI Export Analysis: WRS Health

**Product**: WRS Health Web EHR and Practice Management System v7.0
**Analysis date**: 2026-02-16
**CHPL ID**: 15.02.05.2527.WRSH.01.01.1.211214

## 1. Product Context

WRS Health is a cloud-based, all-in-one ambulatory EHR and practice management platform serving 32+ medical specialties. The certified product integrates clinical documentation (specialty-specific templates for HPI, PE, ROS, A&P across 32+ specialties), e-prescribing (Surescripts Gold Solution Provider, EPCS), bidirectional lab orders and results, patient scheduling and registration, health maintenance/recalls, a patient portal (secure messaging, online scheduling, refill requests, bill pay), integrated telehealth, billing and revenue cycle management (superbills, claim scrubbing, charge capture, denial management, electronic claims), document management with eFax, referral management, and quality reporting (MIPS, CQMs).

This is a feature-rich ambulatory platform. A complete EHI export should cover: demographics, insurance, encounters/scheduling, clinical notes (across specialties), problems, medications/prescriptions, allergies, immunizations, vitals, lab orders and results, procedures, referrals, care plans, billing/claims/charges/payments, patient portal communications, documents/attachments, and telehealth records.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/170.315-b10-EHI-Export.pdf` | 8-page PDF (v1.0, Oct 14 2023). Describes single- and multi-patient export workflows, ZIP file structure with CSV files, C-CDA XML, HTML encounter notes, and document attachments. **No data dictionary, no field-level documentation.** | **Primary and only substantive artifact** |
| `downloads/screenshot-certification-page-full.png` | Full-page screenshot of WRS Health ONC certification page | Low — confirms single PDF link for EHI export |
| `downloads/screenshot-ehi-section-viewport.png` | Viewport screenshot of EHI export section on certification page | Low — shows single link to PDF |
| `files.json` | Manifest of collected artifacts | Orientation only |
| `product-research.md` | Product research on WRS Health capabilities | Context for coverage assessment |

Only one substantive artifact exists: the 8-page PDF. There are no data dictionaries, schemas, sample data files, or API documentation.

## 3. Export Mechanics

- **Format**: ZIP file containing CSV files, one C-CDA XML, HTML encounter notes, and raw document attachments
- **Mechanism**: UI-based. Users log into EHR Admin → search for patient → right-click → select "EHI Export" → click "Request Electronic Health Information" → wait for processing → download ZIP
- **Single-patient**: Self-service via EHR Admin UI (requires Clinical Admin/Admin permissions)
- **Multi-patient/bulk**: Available but NOT self-service — requires emailing `accountmanagement@wrshealth.com`
- **Access constraints**: Requires Clinical Admin or Admin user permissions
- **Fees**: Not documented

## 4. Export Content: What's In It

The export ZIP contains 9 documented components across 4 categories. **No field-level data dictionary exists for any component.** The PDF describes file formats and general content at a prose level only — no column names, no data types, no value sets, no relationships, no schemas, no sample data.

### Vendor's own content organization

| Entity/File | Format | Category (vendor's) | Description (from PDF) | Fields Documented |
|---|---|---|---|---|
| `BillingReport.csv` | CSV | Billing | Financial transactions: patient info, transaction dates, charges, claims, descriptions, status | 0 (no columns listed) |
| `CCDA.xml` | C-CDA XML | Clinical | Patient clinical data per HL7 C-CDA / USCDI v1 | 0 (defers to HL7 spec) |
| `demographics.csv` | CSV | Demographics | Patient key info, identification, contacts, insurance | 0 (no columns listed) |
| `schedule.csv` | CSV | Scheduling | Appointment date, provider, location, type, workflow, notes, note dates | 0 (no columns listed; ~7 data points mentioned in prose) |
| `PatientDocumentFiles.csv` | CSV | Documents | Mapping file listing document attachments | 0 (no columns listed) |
| `Documents/` | Various (PDF, DOCX, XLS, JPG, etc.) | Documents | Raw attachments, lab results, uploaded documents | N/A (raw files) |
| `Notes/` (HTML files) | HTML + CSS/JS | Clinical Notes | Encounter notes, one HTML per visit | N/A (rendered narrative) |
| `Notes/PatientNoteFiles.csv` | CSV | Clinical Notes | Mapping file listing exported notes | 0 (no columns listed) |
| `Notes/NOTES.LOG` | Text | Clinical Notes | Export process log | N/A (process log) |

**Key observation**: The CSV files have **zero documented fields**. The PDF mentions conceptual data points in prose (e.g., "transaction dates, charges, claims" for BillingReport) but provides no column headers, data types, or schemas. The clinical data is entirely delegated to the C-CDA standard with no vendor-specific documentation of what sections or templates are included.

The full inventory is available in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes 4 conceptual categories of export data:

1. **Billing** (1 CSV file): `BillingReport.csv` covers "financial transactions" with charges, claims, and status. This is a single file for all billing data — depth is unknown since no columns are documented. It's unclear whether this includes CPT/ICD codes, superbills, payment details, claim adjudication history, or denial records.

2. **Demographics** (1 CSV file): `demographics.csv` covers patient identification, contacts, and insurance. Again, depth is unknown — it could be 10 fields or 50 fields.

3. **Clinical** (1 C-CDA XML + HTML notes): The C-CDA provides USCDI v1 clinical data (problems, medications, allergies, immunizations, vitals, labs, procedures — the standard C-CDA sections). Encounter notes are exported as individual HTML files — narrative content, not computable structured data.

4. **Scheduling / Documents** (CSV mapping files + raw files): Schedule data in a CSV, plus raw document attachments (lab results, uploaded files, etc.).

The thinnest aspect is the complete absence of field-level documentation. It is impossible to assess the actual depth of any CSV file from the available documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `demographics.csv` mentioned; no columns documented | Product stores rich demographics. CSV exists but content depth unknown. |
| Encounters / visits | ⚠️ Partial | `schedule.csv` with ~7 mentioned data points; HTML notes per visit | Schedule CSV has encounter metadata; notes are narrative HTML. No structured encounter data beyond scheduling. |
| Problems / conditions | ⚠️ Partial | Presumably in `CCDA.xml` (USCDI v1) | Standard C-CDA problems section; depth beyond USCDI unknown. |
| Medications / prescriptions | ⚠️ Partial | Presumably in `CCDA.xml` (USCDI v1) | Product has deep e-prescribing (EPCS, Surescripts, formulary). C-CDA likely covers current meds only — not Rx history, pharmacy details, EPCS records. |
| Allergies | ⚠️ Partial | Presumably in `CCDA.xml` (USCDI v1) | Standard C-CDA section only. |
| Immunizations | ⚠️ Partial | Presumably in `CCDA.xml` (USCDI v1) | Standard C-CDA section only. |
| Vitals | ⚠️ Partial | Presumably in `CCDA.xml` (USCDI v1) | Standard C-CDA section only. |
| Lab results | ⚠️ Partial | Presumably in `CCDA.xml` + raw files in `Documents/` | Product has bidirectional lab connectivity with order tracking. C-CDA has results; order tracking/status/communications not documented. |
| Imaging / diagnostic reports | ⚠️ Partial | May be in `Documents/` as raw files | No structured imaging data documented. |
| Procedures | ⚠️ Partial | Presumably in `CCDA.xml` (USCDI v1) | Standard C-CDA section only. |
| Clinical notes / documents | ✅ Covered | `Notes/` folder with individual HTML files per encounter + `Documents/` folder with attachments | Strong: individual encounter notes exported as readable HTML. But narrative only — no structured note data. |
| Care plans / goals | ❌ Not covered | Not mentioned in export documentation | Product likely stores care plans; not in export. |
| Orders / referrals | ❌ Not covered | Not mentioned in export documentation | Product has referral management and order tracking; not in export. |
| Insurance / coverage | ⚠️ Partial | Mentioned as part of `demographics.csv` | Product stores insurance, eligibility verification. Likely only basic coverage in demographics CSV. |
| Claims / billing | ⚠️ Partial | `BillingReport.csv` | CSV exists, but no field documentation. Unknown depth — could be a summary or detailed claim records. |
| Payments | ⚠️ Partial | May be in `BillingReport.csv` | Mentioned as "financial transactions" — unclear if patient payments, ERA/EOB data included. |
| Consents / directives | ❌ Not covered | Not mentioned | May be in `Documents/` as scanned forms, but no structured consent data. |
| Patient communications / portal messages | ❌ Not covered | Not mentioned in export documentation | Product has patient portal with secure messaging; not in export. |
| Telehealth records | ❌ Not covered | Not mentioned in export documentation | Product has integrated telehealth; not in export. |
| Health maintenance / recalls | ❌ Not covered | Not mentioned in export documentation | Product has automated recall system; not in export. |

**Summary**: Of 19 applicable domains, 1 is solidly covered (clinical notes/documents), 11 are partially covered (mostly through C-CDA or undocumented CSVs), and 7 are not covered at all. The partial coverage ratings are generous — most are "partial" only because we assume the C-CDA includes standard USCDI sections, but this is not verified in the documentation.

## 6. Documentation Quality

The documentation is **minimal and inadequate** for independent use:

- **No data dictionary**: The most critical gap. None of the CSV files have documented column names, data types, or value sets. A developer receiving this export would have to reverse-engineer every CSV's structure.
- **No sample data**: No example files are provided. There's no way to understand the actual format without performing an export.
- **No schema**: No XSD for the C-CDA profile, no JSON Schema, no DDL, no OpenAPI spec.
- **No C-CDA profile detail**: The PDF states the C-CDA follows "USCDI Version 1" and points to the HL7 website. No information about which C-CDA templates are used, what sections are populated, or whether any vendor-specific extensions exist.
- **Process documentation only**: The 8 pages are almost entirely about *how to click buttons to trigger an export* (with 6 screenshots of the UI workflow). Only 3 pages describe the actual export content, and those at the highest level.
- **Stale**: Version 1.0 from October 2023 with no subsequent updates. USCDI v1 reference is outdated (USCDI v3 is current as of Jan 2026).

A developer could not build an import from this documentation. They would need access to a real export to understand the data structure.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export makes a credible attempt to go beyond pure C-CDA by including separate CSV files for billing, demographics, and scheduling, plus raw document attachments and individual encounter notes. This is more than simply handing over a C-CDA. However, multiple significant data domains that WRS Health stores are absent from the documented export: patient portal communications, telehealth records, referrals, care plans, health maintenance/recalls, and prescription history beyond what's in the C-CDA. The billing CSV may add depth, but without field documentation, this cannot be verified. The clinical data beyond notes relies entirely on a standard USCDI v1 C-CDA, which covers only the regulatory minimum for clinical exchange.

**Axis 2 — Export approach: Purpose-built EHI export (lightweight)**

WRS Health did build a specific export mechanism for (b)(10) — it is not simply their existing C-CDA or FHIR API rebranded. The dedicated "EHI Export" UI, the ZIP packaging, and the inclusion of billing CSVs and encounter note HTML files alongside the C-CDA demonstrate that this was built for the (b)(10) requirement. However, the effort was minimal: the documentation is thin (no data dictionary), the C-CDA component is standard USCDI, and multiple data domains the product stores are not addressed. This is a purpose-built export, but a shallow one.

### Key Findings

1. **No data dictionary exists.** The single most significant documentation gap: none of the 4+ CSV files have documented columns, types, or value sets. The C-CDA is referenced by standard only. A user cannot assess what data they're getting without performing an export and inspecting the files. (Source: `170.315-b10-EHI-Export.pdf`, pages 5-7)

2. **Hybrid approach adds some depth beyond C-CDA.** The inclusion of `BillingReport.csv`, `demographics.csv`, `schedule.csv`, and individual HTML encounter notes alongside the C-CDA shows an effort to export data beyond what a standard clinical exchange provides. (Source: `170.315-b10-EHI-Export.pdf`, pages 5-6)

3. **Multiple product domains are absent from the export.** Patient portal messages, telehealth data, referral tracking, health maintenance/recall data, prescription history, and care plans are not mentioned in the export documentation, despite being core features of the product. (Source: comparison of `product-research.md` capabilities vs. `170.315-b10-EHI-Export.pdf` export content)

4. **Bulk export is not self-service.** Multi-patient export requires emailing `accountmanagement@wrshealth.com`, creating an operational barrier for large-scale data requests. (Source: `170.315-b10-EHI-Export.pdf`, page 5)

5. **Documentation is stale and minimal.** Version 1.0 from October 2023 with no updates. 8 pages total, of which only 3 describe export content. References USCDI v1 (now superseded by v3). (Source: `170.315-b10-EHI-Export.pdf`)

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   Mixed (CSV + C-CDA XML + HTML + raw attachments in ZIP)
Entities:        9 export components (4 CSV files, 1 C-CDA XML, 2 folders, 2 mapping/log files)
Fields:          N/A (no data dictionary — zero fields documented)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (vendor-assisted, not self-service)
Domains covered: 12 of 19 applicable domains (1 solid, 11 partial, 7 missing)
```

### Bottom Line

WRS Health built a purpose-specific (b)(10) export that goes beyond a bare C-CDA by including billing, scheduling, and demographic CSVs alongside encounter notes and documents. However, the complete absence of a data dictionary makes it impossible to verify the depth of any component, and multiple significant product domains (portal messages, telehealth, referrals, prescriptions, care plans) are not documented as exported. A patient would receive a ZIP with some useful files, but neither they nor a developer could fully understand the contents without reverse-engineering the CSVs, and important data categories may be missing entirely.

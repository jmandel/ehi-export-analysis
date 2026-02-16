# EHI Export Analysis: VIPA Health Solutions, LLC

**Product**: 24/7 smartEMR v7.2
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.2916.smar.07.02.1.221216

## 1. Product Context

24/7 smartEMR is a cloud-hosted, web-based EMR and practice management system developed by VIPA Health Solutions, LLC (Miami, FL, ~11 employees). It targets physician offices and ambulatory clinics across many specialties (internal medicine, cardiology, dermatology, pediatrics, orthopedics, family medicine, etc.) and is marketed as a combined EMR + billing platform.

Key capabilities relevant to EHI scope:
- **Clinical documentation**: Encounter recording, customizable templates, specialty-specific workflows, voice recognition
- **e-Prescribing**: Surescripts integration, drug interaction checking
- **Lab integration**: LabCorp and Quest Diagnostics results
- **Billing/RCM**: CMS-compliant Superbill generation, electronic claims submission, insurance eligibility verification, E/M coding — this is described as the product's "best-known feature" and a separate SmartEBS billing module exists
- **Patient portal**: Certified for (e)(1) view/download/transmit
- **Scheduling**: Appointment management
- **Telehealth**: Integrated telehealth
- **CQM/Public health**: 14 CQMs, immunization registry reporting, syndromic surveillance
- **FHIR API**: Certified for (g)(10) with 16 FHIR R4 resource types

The product stores clinical encounters, medications, allergies, immunizations, problems, vitals, labs, documents, billing/claims, insurance data, appointments, and provider information. An EHI export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `electronic-health-information-export-b10.html` (92 KB) | **Core EHI export documentation page.** ~200 words describing CDA export + document repository export. No data dictionary, no sample files, no schema. | **Most important** — the only export-specific documentation |
| `screenshot-ehi-export-page-full.png` (279 KB) | Full-page screenshot of the EHI export documentation | Confirms the page content matches the HTML |
| `patient-demographics.html` (123 KB) | Import spec for patient demographics — 30 fields with types, lengths, validation | Import spec — reveals data model, not export |
| `patient-allergies.html` (114 KB) | Import spec for allergies — 11 fields with RxNorm/SNOMED mappings | Import spec |
| `document-upload.html` (110 KB) | Import spec for document uploads — 12 fields | Import spec |
| `insurance-information.html` (106 KB) | Import spec for insurance payer directory — 6 fields | Import spec |
| `problem-list.html` (105 KB) | Import spec for problems — 5 fields with ICD-10-CM | Import spec |
| `service-location.html` (104 KB) | Import spec for service locations — 10 fields | Import spec |
| `scheduler-appointments.html` (103 KB) | Import spec for appointments — 6 fields | Import spec |
| `cpt-and-fee-schedule.html` (100 KB) | Import spec for CPT/fee schedule — 2 fields | Import spec |
| `referring-physician.html` (100 KB) | Import spec for referring physicians — 3 fields | Import spec |
| `immunization-records.html` (84 KB) | Empty page — no content | **Least informative** |
| `enrichment/smartemr-data-models.json` (34 KB) | Parsed field specs from all import pages — 85 fields across 9 entities | Useful structured summary |
| `enrichment/smartemr-ehi-export.json` (2 KB) | Parsed EHI export page structure | Useful structured summary |

**Key observation**: The site has detailed import specifications (85 fields with types, descriptions, validation rules across 9 data models) but **zero** field-level documentation for the export. The asymmetry is striking — the vendor demonstrably knows how to document data models but chose not to do so for the export.

## 3. Export Mechanics

- **Format**: CDA (Clinical Document Architecture) for clinical data; PDF/JPG/PNG files for document repository
- **Mechanism**: UI-based via Admin Panel
  - Clinical data: Admin Panel → Export Options → Patient Data → Create a backup/export
  - Documents: Admin Panel → Export Options → Patient Document Data (b10)
- **Single-patient**: Yes — select individual patient(s)
- **Bulk/all-patients**: Yes — "Select All" option available
- **Scheduling**: One-time or recurring backup/export; date of service filter
- **API access**: None documented for EHI export
- **Fees**: Not documented
- **CDA standard**: References HL7 CDA but does not specify which CDA template, implementation guide, or sections are used (C-CDA R2.1? Generic CDA? Custom sections?)

## 4. Export Content: What's In It

### EHI Export Documentation (what the vendor provides)

The entire EHI export documentation consists of approximately 200 words on a single page. It describes two export components:

1. **CDA Clinical Data Export**: Per-encounter CDA files plus a consolidated CDA file per patient. No specification of CDA sections, templates, or data elements.
2. **Document Repository Export**: Scanned/uploaded documents (PDFs, JPGs, PNGs) organized by patient chart ID folders with category subfolders (Lab Reports, Radiology, Scanned Receipts, etc.).

**There is no data dictionary for the export.** Zero fields are documented for the CDA output. No sample CDA files are provided. No CDA template OIDs or implementation guide references are given.

### Import Specifications (indirect evidence of data model)

The vendor's data import specifications reveal part of the data model, but these document what can be *imported*, not what is *exported*. They cover 9 entities with 85 total fields:

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| Patient Demographic (PM) | 30 | 30 | yes | Data Import |
| Insurance Import (PM) | 6 | 6 | yes | Data Import |
| CPT and Fee Schedule | 2 | 2 | yes | Data Import |
| Service Location (PM) | 10 | 10 | yes | Data Import |
| Referring Physician | 3 | 3 | yes | Data Import |
| Appointments | 6 | 6 | yes | Data Import |
| Document Upload | 12 | 12 | yes | Clinical Data Import |
| Problem List | 5 | 5 | yes | Clinical Data Import |
| Allergy & Intolerance | 11 | 11 | yes | Clinical Data Import |
| Immunization Records | 0 | 0 | — | Clinical Data Import (empty) |
| **Total** | **85** | **85** | — | — |

All 85 fields across the import specs have descriptions, data types, max lengths, and required/optional flags. This demonstrates the vendor's capability to produce detailed data documentation.

### FHIR API (separate from EHI export)

The vendor's (g)(10) FHIR R4 API (documented separately at smartemr.readme.io/reference) exposes 16 resource types: Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, MedicationRequest, Observation, Organization, Practitioner, Procedure. This is the standard USCDI clinical data surface and is explicitly separate from the CDA-based (b)(10) export.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes two export components:

1. **CDA Clinical Data**: Covers patient encounters in CDA format. Without any section inventory or data dictionary, the actual content is unknowable from documentation alone. CDA *can* contain comprehensive clinical data (demographics, problems, medications, allergies, vitals, labs, procedures, notes) but the vendor does not specify what sections are included.

2. **Document Repository**: Covers scanned/uploaded documents organized in patient folders. Categories mentioned include Lab Reports, Radiology, Scanned Receipts. This is useful but only captures document-format records, not structured data.

**What is almost certainly missing** (based on what the product stores per Section 1):
- **Billing data**: The product's "best-known feature" is Superbill generation and electronic claims. The EHI export documentation mentions nothing about billing records, claims, charges, payments, or financial data. CDA format has no standard sections for billing data.
- **Insurance/coverage details**: The import spec shows 30 demographic fields including primary and secondary insurance. Whether insurance data appears in the CDA is undocumented.
- **Medication/prescription data**: The product integrates with Surescripts for e-prescribing. Whether medication lists appear in CDA sections is undocumented.
- **Structured lab results**: Lab results may be in the CDA or only as scanned documents in the document repository.
- **Specialty-specific clinical data**: The product markets specialty-specific templates — this data likely doesn't map to standard CDA sections.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Likely in CDA but undocumented; import spec shows 30 fields | Product stores extensive demographics; export may include but is unverifiable |
| Encounters / visits | ⚠️ Partial | CDA is per-encounter, so encounters are the organizing unit | Encounter structure exists but field-level content unknown |
| Problems / conditions | ⚠️ Partial | Likely a CDA section; import spec shows 5 fields (ICD-10-CM) | Probably present in CDA but undocumented |
| Medications / prescriptions | ⚠️ Partial | Likely a CDA section; e-prescribing is a core feature | Product has Surescripts integration; CDA may include but undocumented |
| Allergies | ⚠️ Partial | Likely a CDA section; import spec shows 11 fields with RxNorm/SNOMED | Probably present in CDA but undocumented |
| Immunizations | ⚠️ Partial | Likely a CDA section; product certified for immunization registry reporting | Probably present but undocumented; import page is empty |
| Vitals | ⚠️ Partial | Likely a CDA section | Probably present but undocumented |
| Lab results | ⚠️ Partial | May be in CDA sections and/or document repository (Lab Reports folder) | Product integrates with LabCorp/Quest; structured results may or may not be in CDA |
| Imaging / diagnostic reports | ⚠️ Partial | Document repository includes Radiology folder; may have CDA section | Likely document-only, not structured |
| Procedures | ⚠️ Partial | Likely a CDA section | Probably present but undocumented |
| Clinical notes / documents | ⚠️ Partial | Document repository exports signed encounter notes | Document export covers this; CDA may also include narrative |
| Care plans / goals | ⚠️ Partial | Product's FHIR API has CarePlan and Goal resources | May be in CDA but undocumented |
| Orders / referrals | ❌ Not covered | No mention in export documentation | Product has order management; not documented in export |
| Insurance / coverage | ❌ Not covered | No mention in export; import spec has some insurance fields | Product stores insurance data; not documented in export |
| Claims / billing | ❌ Not covered | No mention in export documentation | **Major gap** — billing/Superbills are the product's signature feature; completely absent from export |
| Payments | ❌ Not covered | No mention in export documentation | Product processes claims/payments; not in export |
| Consents / directives | ❌ Not covered | No mention | Unknown if product stores these |
| Patient communications | ❌ Not covered | No mention | Product has patient portal; messages not in export |
| Specialty-specific data | ❌ Not covered | No mention of specialty templates | Product marketed as "specialty-specific" with custom templates; not in export |

**Note**: Many clinical domains are rated ⚠️ Partial rather than ✅ Covered because while a CDA export likely *contains* these sections, the vendor provides zero documentation confirming this. The coverage is assumed based on CDA conventions, not evidenced.

## 6. Documentation Quality

**Rating: Very poor.**

- **Data dictionary**: None for the export. The vendor has demonstrated they can write detailed field specs (85 fields across import pages, all with descriptions, types, and validation rules) but provides nothing for the export.
- **Sample data**: None. No sample CDA files, no example directory listings.
- **Schema/machine-readable artifacts**: None. No CDA template OIDs, no XSD references, no implementation guide citations.
- **CDA specification**: The documentation says "CDA" and links to the HL7 CDA product page but does not specify C-CDA version, template identifiers, or which sections are included.
- **Technical guidance**: Navigation paths are provided (Admin Panel → Export Options → ...) but no screenshots, no troubleshooting, no format details.

**Could a developer build an import from this documentation?** No. A developer would need to obtain a sample CDA export and reverse-engineer its structure. The documentation provides no information about what data elements appear in the CDA, what coding systems are used, or how the data is organized. The document repository export is slightly better documented (folder organization by patient ID with category subfolders) but still lacks field-level detail.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. The EHI export page is ~200 words with no data dictionary, no field specifications, and no sample data. While the CDA format likely carries standard clinical data, the complete absence of billing data documentation is a glaring gap for a product whose signature feature is Superbill generation and electronic claims. The vendor makes no claims about exporting billing, insurance, specialty-specific, or administrative patient data — all of which the product stores.

**Axis 2 — Export approach: Unclear/undetermined**

The CDA-based export is technically distinct from the FHIR (g)(10) API, so this isn't a simple repackaging of the FHIR endpoint. However, CDA is fundamentally a clinical document standard — it's well-suited for encounter summaries and USCDI-scope clinical data, but it has no standard sections for billing, claims, or specialty-specific structured data. The choice of CDA as the export format, combined with the complete absence of any billing data mentions, strongly suggests this export covers only the clinical encounter data that would be representable in a standard C-CDA — essentially the same data scope as the (g)(10) API, just in a different format. The document repository export adds value by including scanned documents, but this is a file dump rather than structured EHI. Without a data dictionary or sample data, it is impossible to confirm whether the CDA export goes beyond standard clinical exchange content.

### Key Findings

1. **No export data dictionary exists.** The entire (b)(10) documentation is ~200 words. The vendor documents 85 fields for data *import* but zero fields for data *export*. This is the most significant finding — the vendor demonstrably knows how to document data models but chose not to do so for the EHI export.

2. **Billing data — the product's signature feature — appears absent from the export.** SmartEMR markets Superbill generation and electronic claims as core capabilities, yet the EHI export documentation makes no mention of billing records, claims, charges, or payments. CDA format has no standard sections for this data.

3. **CDA format limits breadth.** CDA is a clinical document standard. Using it as the sole structured export format inherently constrains what can be exported to clinical encounter data, leaving out billing, specialty-specific structured data, and administrative records that are part of the designated record set.

4. **The document repository export is a useful supplement** — it captures signed notes, lab results, radiology reports, and scanned documents in their original formats. However, it is a file dump with folder organization, not a structured data export.

5. **All clinical domain coverage is assumed, not demonstrated.** Because no CDA section inventory or data dictionary is provided, every clinical domain (medications, allergies, vitals, labs, etc.) is assessed as "likely present" based on CDA conventions rather than documented evidence.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Unclear/undetermined
    Export format:   CDA + PDF/JPG/PNG (document repository)
    Entities:        0 (no export data dictionary; 9 import specs exist with 85 fields)
    Fields:          N/A (no export field documentation)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Yes (all patients option available)
    Domains covered: 0 of 15 confirmed; ~10 of 15 probable but undocumented

### Bottom Line

A patient or provider requesting their EHI from smartEMR would receive CDA clinical files and a folder of scanned documents, but with no documentation explaining what's in the CDA output. Billing and claims data — the product's core differentiator — appears to be entirely absent from the export. The vendor's failure to provide any data dictionary for the export, despite demonstrating that capability on their import specification pages, suggests this was a compliance checkbox rather than a genuine effort to provide complete EHI access.

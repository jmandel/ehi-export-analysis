# EHI Export Analysis: Sargas Pharmaceutical Adherence and Compliance International

**Product**: Sargas International's Chronic Care Management Cloud dba hru2day  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.05.05.2306.SPAC.01.00.0.211014

## 1. Product Context

Sargas International (SPAC International) operates a cloud-based chronic care management (CCM) platform branded "hru2day." It is **not a full EHR** — it holds ONC Modular EHR certification (version 21.9, certified 2021-10-14) and focuses exclusively on Medicare CCM, Principal Care Management (PCM), Remote Patient Monitoring (RPM), and Medication Therapy Monitoring (MTM). The company also operates a 24/7 clinical call center that performs care management services on behalf of physician practices.

Per vendor materials and the hru2day website, the platform serves 200+ practices and 20,000+ patients with 200,000+ recorded interactions. The product stores:

- **Patient demographics** and chronic condition problem lists
- **Comprehensive care plans** (physical, mental, cognitive, psychosocial, functional, environmental domains)
- **Medication lists and allergies**, medication adherence tracking, and side effect reporting (the company's founding use case, originally for oncology)
- **RPM device data**: glucose, blood pressure, heart rate, oxygen saturation, weight from FDA-approved home monitoring devices
- **Care coordination logs**: the 20+ minutes/month of CCM service documentation
- **Secure messages** between patients, care teams, and providers
- **Time tracking** for CCM/PCM/RPM services (linked to CPT codes 99490, 99491, 99487, 99489, 99439, 99424–99427)
- **Patient consent records** (required for CCM billing)
- **Clinical summaries** and reconciliation data

The certified criteria are narrow: CPOE for medications/labs/imaging (a)(1)–(a)(3), demographics (a)(5), clinical information reconciliation (e)(2), EHI export (b)(10), FHIR API (g)(10), and security criteria. Notably absent: e-prescribing, transitions of care, patient portal view/download/transmit, and public health reporting.

This product's data footprint is **deep on care management and medication adherence but narrow compared to a full EHR**. The relevant question for (b)(10) assessment is whether the export captures the CCM-specific data (care plans, coordination logs, RPM readings, adherence tracking) — not whether it captures traditional EHR data the product doesn't store.

## 2. Artifacts Reviewed

| # | Artifact | Type | Size | What It Tells Us |
|---|----------|------|------|-----------------|
| 1 | `downloads/SPAC-Export.pdf` | PDF, 1 page | 379,759 bytes | **Primary (and only) EHI export documentation.** 6 sentences describing the export format: a ZIP containing C-CDA XML documents (per encounter) and PDF attachments. No data dictionary, no field-level detail, no sample data, no schema, no instructions for performing the export. Created 2023-12-19, last modified 2025-11-25. 109 words of substantive content. |
| 2 | `downloads/screenshot-certification-page.png` | PNG screenshot | 235,885 bytes | Screenshot of vendor's Certified EHR Technology page. Contains certification boilerplate and a link to mandatory disclosures. No EHI export documentation. |

**Additionally verified** (not in downloads but checked independently):
- `ONC-HIT-CERTIFICATE-DISCLOSURE_ver_21_9_Revised-25.pdf` (2 pages, from vendor website): Lists certified criteria and pricing. Confirms (b)(10) certification. No additional EHI export technical detail.
- The vendor's certification page at `spacinternational.com/certified-ehr-technology.php`: Links to mandatory disclosures and a capabilities statement. No EHI export documentation beyond the SPAC-Export.pdf.

**Most informative artifact**: `SPAC-Export.pdf` — though it is extremely minimal.  
**Least informative**: The screenshot, which adds nothing beyond what the PDF provides.

## 3. Export Mechanics

Based on the SPAC-Export.pdf (the sole documentation):

- **Format**: ZIP archive containing:
  - C-CDA XML documents (one per patient encounter), nested in ZIP archives within the outer ZIP
  - PDF files attached to the patient's chart (described as "machine readable PDF")
- **Mechanism**: Not documented. No instructions for how to initiate the export, from which screen, by which user role, or through what workflow.
- **Single-patient vs bulk**: Not documented. The language says "patient EHI export" (singular), suggesting single-patient scope.
- **Access constraints or fees**: Not documented in the EHI export materials. The mandatory disclosures PDF mentions "one time implementation fee and yearly maintenance charge" for the ONC certified portals generally, but no fees specific to EHI export.

## 4. Export Content: What's In It

The documentation provides **no field-level, section-level, or entity-level detail** about what the export contains. The entirety of the content description is:

> "The patient EHI export contains data from the patient's chart."

The export format is C-CDA XML per encounter plus PDF attachments. There is:

- **No data dictionary**: zero entities, zero fields documented
- **No schema or profile**: no indication of which C-CDA template(s), which sections are populated, or which optional sections are included
- **No sample data**: no example C-CDA documents or PDFs
- **No value sets or code systems**: not documented
- **No relationships**: not documented
- **No machine-readable artifacts**: only a 1-page PDF with prose

### Vendor's own content organization

The vendor provides no content organization. No tables, categories, or entity groupings are described. The only structure conveyed is:

| Component | Format | Description (vendor's words) |
|-----------|--------|------------------------------|
| Patient encounter data | C-CDA XML | "Information for each patient encounter is available C-CDA format in zip archive" |
| Chart attachments | PDF | "PDF files attached to the patient's chart (machine readable PDF)" |

No further breakdown is provided. There are **0 entities and 0 fields** documented.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes only that the export includes C-CDA documents per encounter and PDF attachments from the chart. Without a data dictionary or sample data, it is impossible to determine which C-CDA sections are populated or how comprehensively. At best, a C-CDA export would include standard sections (demographics, problems, medications, allergies, encounters). At worst, the C-CDAs could be minimal templates with sparse population.

The PDF attachments could theoretically contain additional clinical documents, but their nature and scope are completely undocumented.

The vendor's documentation provides **zero visibility** into whether the export includes the product's core data: care plans, care coordination logs, RPM device readings, medication adherence records, time tracking, or secure messages.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|--------|----------|-----------------|--------------|
| Demographics | ⚠️ Partial | C-CDA typically includes demographics, but no confirmation of which fields | Product stores demographics (certified for (a)(5)); likely present in C-CDA but undocumented |
| Encounters / visits | ⚠️ Partial | Documentation says "each patient encounter" gets a C-CDA | Encounter structure likely present but content unknown |
| Problems / conditions | ⚠️ Partial | C-CDA standard section; product certified for (a)(5) problem list | Likely present in C-CDA but undocumented |
| Medications / prescriptions | ⚠️ Partial | C-CDA standard section; product certified for (a)(1) CPOE-meds | Likely present but medication adherence tracking (core product feature) almost certainly not captured in C-CDA |
| Allergies | ⚠️ Partial | C-CDA standard section | Likely present but undocumented |
| Immunizations | N/A | Not documented | Product does not appear to store immunization data |
| Vitals | ⚠️ Partial | C-CDA has a vitals section | RPM device readings (glucose, BP, HR, SpO2, weight) are the product's core data; C-CDA vitals section cannot represent continuous time-series device telemetry. **Significant potential gap.** |
| Lab results | ❌ Not covered | No evidence | Product has CPOE for labs but unclear if results are stored; no evidence in export |
| Imaging / diagnostic reports | ❌ Not covered | No evidence | Product has CPOE for imaging but unclear if results are stored |
| Procedures | N/A | Not documented | Product is not a procedure-documentation system |
| Clinical notes / documents | ⚠️ Partial | PDF attachments from chart included | Some documents may be captured as PDFs, but scope is unknown |
| Care plans / goals | ❌ Not covered | No evidence | **Critical gap.** Care plans are the core product feature (comprehensive plans covering physical, mental, cognitive, psychosocial, functional, environmental domains). C-CDA has a care plan section but no evidence the vendor populates it, and the structured richness of their care plans likely exceeds what C-CDA can represent. |
| Orders / referrals | ❌ Not covered | No evidence | Product has CPOE; unclear if orders are in the export |
| Insurance / coverage | ❌ Not covered | No evidence | Product likely stores some insurance info for Medicare CCM billing |
| Claims / billing | ❌ Not covered | No evidence | CCM/PCM/RPM time tracking and billing documentation are core to the product but have no C-CDA analog |
| Payments | N/A | Not documented | Medicare billing appears to be done by the physician practice, not through this system |
| Consents / directives | ❌ Not covered | No evidence | Patient consent records are required for CCM and stored in the system; not evidenced in export |
| Patient communications | ❌ Not covered | No evidence | Secure messaging is a product feature; no evidence in export |
| Specialty: Medication adherence tracking | ❌ Not covered | No evidence | **Critical gap.** This is the company's founding specialty (Drug Adherence® for oncology). Adherence records, side effect reports, and adherence monitoring data have no C-CDA representation. |
| Specialty: RPM device telemetry | ❌ Not covered | No evidence | **Critical gap.** Continuous device readings (glucose, BP, HR, SpO2, weight) are a core product feature. C-CDA cannot represent time-series device data. |
| Specialty: Care coordination logs | ❌ Not covered | No evidence | **Critical gap.** 200,000+ logged care coordination interactions are core to CCM services and billing support. No C-CDA representation exists. |

**Summary**: Of 15 applicable domains, 0 are confirmed covered, 5 are partially/presumably covered (based on C-CDA being a standard format), and 10 show no evidence of coverage. The product's three most distinctive data types — care plans, RPM device telemetry, and care coordination logs — all appear to be absent from the export.

## 6. Documentation Quality

The export documentation is **among the thinnest possible** while still existing:

- **1 page, 109 words, 6 sentences** — describes only the container format (ZIP with C-CDAs and PDFs)
- **No data dictionary**: zero tables, zero fields, zero descriptions
- **No schema or profile**: no indication of which C-CDA template, which sections, or which extensions
- **No sample data**: no example export files
- **No instructions**: no guidance on how to perform the export (what screen, what role, what workflow)
- **No machine-readable artifacts**: no JSON schema, no FHIR CapabilityStatement, no C-CDA template OIDs
- **No API documentation**: the export mechanism is completely undescribed

A developer given this documentation could determine only that the export produces a ZIP file containing C-CDA XML and PDF files. They could not:
- Determine which data elements are included
- Build an import process
- Validate the completeness of an export
- Understand the relationship between documents
- Know how to request or trigger an export

The documentation quality is insufficient for any practical use beyond knowing the file format.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The documentation is too thin to confirm what is actually exported, but the described format (C-CDA per encounter + PDF attachments) is structurally incapable of capturing this product's core data domains (care coordination logs, RPM device telemetry, medication adherence tracking, comprehensive care plans, CCM time tracking). Even if the C-CDAs are well-populated, a C-CDA-only export for a chronic care management platform represents a fundamental mismatch between export format and product data model. The documentation is a 109-word compliance artifact, not a genuine export specification.

### Key Findings

1. **The entire EHI export documentation is a single 1-page PDF with 109 words** (`SPAC-Export.pdf`). It describes only the container format — no data dictionary, no field definitions, no sample data, no schema, and no export instructions.

2. **The export format (C-CDA + PDF) is fundamentally mismatched with the product's core data.** hru2day is a chronic care management platform whose most important data — care coordination logs (200,000+ interactions), RPM device telemetry (glucose, BP, HR, SpO2, weight), medication adherence tracking, and CCM time-based billing records — cannot be represented in C-CDA documents. This appears to be a clinical summary export being repurposed as (b)(10).

3. **Zero entities and zero fields are documented.** There is no data dictionary of any kind. It is impossible to determine from the documentation what specific data elements are included in or excluded from the export.

4. **The product's three most distinctive capabilities are likely unrepresented**: (a) comprehensive care plans across physical/mental/cognitive/psychosocial/functional/environmental domains, (b) RPM device data from FDA-approved monitors, and (c) care coordination activity logs supporting Medicare CCM billing. None of these have standard C-CDA representations.

5. **No export mechanism is described.** The documentation does not explain how to initiate an export, who can perform it, or any parameters involved.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   ZIP (C-CDA XML + PDF)
Model type:      Standard projection (C-CDA)
Entities:        0 (no data dictionary)
Fields:          0 (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 of 15 confirmed; 5 of 15 presumed partial (based on C-CDA standard sections)
```

### Bottom Line

A patient or provider requesting their data from hru2day would receive C-CDA clinical summaries and PDF chart attachments — likely capturing basic demographics, problems, medications, and allergies, but almost certainly missing the product's core data: care coordination logs, RPM device readings, medication adherence records, and comprehensive care plans. The 109-word documentation provides no visibility into what is actually exported. This is a compliance checkbox, not a genuine EHI export capability. The single biggest gap is the structural mismatch between the C-CDA export format and the product's specialized care management data model.

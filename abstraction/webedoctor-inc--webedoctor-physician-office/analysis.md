# EHI Export Analysis: WEBeDoctor, Inc.

**Product**: WEBeDoctor Physician Office v6.0
**Analysis date**: 2026-02-15
**CHPL ID**: 15.99.05.2526.WEBe.06.02.1.260113

## 1. Product Context

WEBeDoctor Physician Office is a cloud-based, fully integrated EHR and practice management platform developed by WEBeDoctor, Inc. (Brea, CA; ~11 employees). It is marketed to ambulatory physician practices across multiple specialties including cardiology, ophthalmology, podiatry, pediatrics, family practice, dermatology, psychiatry, and others. The product has been certified by SLI Compliance (January 13, 2026) across 30+ ONC criteria.

The product is a comprehensive platform combining:

- **Clinical documentation (EMR)**: Point-and-click templates, dictation, handwriting recognition, voice recognition, AI-generated notes (WEBeNote.AI), clinical images with annotations, customizable specialty templates
- **Practice management**: Multi-provider/multi-location scheduling, patient demographics, insurance verification, appointment reminders
- **Billing and revenue cycle**: Electronic claims submission via Change Healthcare clearinghouse, claims tracking, payment posting, coding assistance, EDI, financial reporting
- **E-prescribing (WEBeRx)**: Surescripts-connected, controlled substance e-prescribing, drug interaction/allergy checking
- **Lab integration (eLabs)**: Orders and results via LabCorp and Quest Diagnostics
- **Patient portal**: Secure messaging, lab results viewing, billing information, appointment/refill requests
- **Telehealth**: HIPAA-compliant virtual visits
- **Remote patient monitoring (RPM)**: Blood pressure, weight, glucose monitoring syncing to EMR
- **Chronic care management (CCM) and remote therapeutic monitoring (RTM)**

This product stores data across clinical, financial, communication, and monitoring domains. A complete EHI export should cover all of these.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `WEBeDoctor_EHI_Export.pdf` | 860 KB, 3 pages | The sole EHI export documentation. Describes C-CDA 2.1 export mechanism with screenshots. Created 2023-10-27 by Microsoft Word 2007. Contains 1 paragraph of intro, 4 UI screenshots, and brief navigation instructions. | **Primary artifact** — but extremely thin |
| `WEBeDoctor_Mandatory_Disclosures_SLI_01192026_Signed.pdf` | 157 KB, 5 pages | Mandatory disclosures confirming certification of 170.315(b)(10) and all other criteria. Lists costs (per-provider licensing, monthly SAAS fee). Signed January 16, 2026 by CEO Anwer Siddiqi. | Confirms (b)(10) certification; no EHI technical detail |
| `certification-page-full.png` | 490 KB | Screenshot of the certification page at `new.webedoctor.com/certification/`. Shows the EHI Export card at bottom-left linking to the PDF. No other EHI-related documentation visible. | Confirms no additional EHI documentation exists on the page |

**Verification of certification page (2026-02-15)**: The page at `https://new.webedoctor.com/certification/` returns HTTP 200 and lists 9 PDF downloads: mandatory disclosures, RWT plans/results for 2022–2025, and the single EHI Export PDF. No additional data dictionary, schema, FHIR documentation, or sample export files exist on the site.

## 3. Export Mechanics

- **Format**: C-CDA 2.1 (XML), one document per patient
- **Mechanism**: UI-based export within WEBeDoctor EMR
  - **Access control**: Facility admin must enable EHI Export per user via Administration > User Configuration > "Enable EHI Export" button
  - **Single patient**: Hub > EHI Export > One Time > Select Patient > Save → C-CDA file generated → download from Hub > EHI Export > CCDA List > Download
  - **All patients**: Hub > EHI Export > One Time > check "All Patients" → ZIP file of all C-CDA files generated → download from CCDA List
- **Single-patient**: Yes
- **Bulk/population export**: Yes (all patients as ZIP)
- **Date range filtering**: The UI shows Start Date/End Date fields and a "No Date Range" checkbox, suggesting date-based filtering is available
- **Provider filtering**: The UI shows a "Provider: All" dropdown, suggesting exports can be filtered by provider
- **Access constraints**: Requires facility admin to grant EHI Export rights per user
- **Fees**: Not explicitly stated for EHI export; general costs are per-provider license + monthly SAAS fee

## 4. Export Content: What's In It

### What we know

WEBeDoctor's EHI export produces **C-CDA 2.1 XML documents**. The documentation states:

> "WEBeDoctor is compliant with §170.315(b)(10) Electronic Health Information Export by generating C-CDA 2.1 electronic documents."

The documentation provides **zero field-level detail** about what data is included in the C-CDA. It links to the HL7 C-CDA specification (https://www.hl7.org/implement/standards/product_brief.cfm?product_id=447) as the format reference and says nothing more about content.

### What we don't know

- Which C-CDA document type(s) are generated (CCD, Discharge Summary, Referral Note, etc.)
- Which C-CDA sections are populated
- Whether any vendor extensions or custom sections are included
- What coded value sets are used
- How specialty-specific data maps to C-CDA templates
- Whether clinical notes are included and in what format

### No data dictionary provided

There is **no data dictionary, no field mapping, no schema, no sample data, and no description of exported data elements** beyond the C-CDA standard reference. The vendor provides exactly zero information about what specific data appears in their C-CDA exports.

### Vendor's own content organization

The vendor provides no content organization. The entire documentation is a 3-page how-to guide with screenshots. There are no entities, tables, fields, categories, or data domains described.

### Standard C-CDA 2.1 sections (inferred, not confirmed)

Based on the C-CDA 2.1 standard, the following sections would *typically* be present in a CCD document, but we **cannot confirm** which ones WEBeDoctor actually populates:

| C-CDA Section | OID | Likely Included? | Notes |
|---|---|---|---|
| Patient Demographics | N/A (header) | Likely | Always in C-CDA header |
| Allergies and Intolerances | 2.16.840.1.113883.10.20.22.2.6.1 | Likely | Required in CCD |
| Medications | 2.16.840.1.113883.10.20.22.2.1.1 | Likely | Required in CCD |
| Problem List | 2.16.840.1.113883.10.20.22.2.5.1 | Likely | Required in CCD |
| Procedures | 2.16.840.1.113883.10.20.22.2.7.1 | Likely | Standard CCD section |
| Results (Labs) | 2.16.840.1.113883.10.20.22.2.3.1 | Likely | Standard CCD section |
| Vital Signs | 2.16.840.1.113883.10.20.22.2.4.1 | Likely | Standard CCD section |
| Immunizations | 2.16.840.1.113883.10.20.22.2.2.1 | Likely | Standard CCD section |
| Encounters | 2.16.840.1.113883.10.20.22.2.22.1 | Likely | Standard CCD section |
| Plan of Treatment | 2.16.840.1.113883.10.20.22.2.10 | Unknown | Optional |
| Social History | 2.16.840.1.113883.10.20.22.2.17 | Unknown | Optional but common |
| Family History | 2.16.840.1.113883.10.20.22.2.15 | Unknown | Product has (a)(12) cert |
| Medical Equipment | 2.16.840.1.113883.10.20.22.2.23 | Unknown | Product has (a)(14) cert |
| Clinical Notes | Various | Unknown | Implementation varies |
| Goals | 2.16.840.1.113883.10.20.22.2.60 | Unknown | Optional |
| Health Concerns | 2.16.840.1.113883.10.20.22.2.58 | Unknown | Optional |
| Functional Status | 2.16.840.1.113883.10.20.22.2.14 | Unknown | Optional |
| Advance Directives | 2.16.840.1.113883.10.20.22.2.21.1 | Unknown | Optional |

**Key limitation**: "Likely" designations are based on the C-CDA standard requirements, not on verified WEBeDoctor implementation. Without sample data, we cannot confirm any of these.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides **no content-level documentation whatsoever**. The sole artifact is a 3-page PDF that:
1. States the export uses C-CDA 2.1
2. Shows screenshots of the export UI
3. Links to the HL7 C-CDA specification

There are no categories, modules, sections, or data domains described. There is no acknowledgment of what data falls outside the C-CDA format, and no mention of supplementary export mechanisms for non-clinical data.

The screenshots (verified via PDF rendering) show:
- Page 1: User Configuration screen with "Enable EHI Export" buttons per user
- Page 2: One Time Export screen showing patient selection (name, gender, DOB, SSN fields visible), date range filtering, and the CCDA List showing generated exports with "View" and "Download" buttons. Status column shows "Generated" for all entries. Process type is "Single" and "OneTime."
- Page 3: All Patients export with "All Patients" checkbox checked

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header carries basic demographics | Product stores richer PM data (insurance verification, pre-visit checklists) not in C-CDA |
| Encounters / visits | ⚠️ Partial | C-CDA Encounters section likely present | Telehealth visit metadata, scheduling context likely absent |
| Problems / conditions / diagnoses | ✅ Covered | Required C-CDA section; product certified (a)(1)-(a)(5) | Standard coverage expected |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medications section likely present | Full e-prescribing workflow (pharmacy routing, EPCS, refill mgmt) not in C-CDA |
| Allergies | ✅ Covered | Required C-CDA section | Standard coverage expected |
| Immunizations | ✅ Covered | Standard C-CDA section; product certified (f)(1) | Standard coverage expected |
| Vitals | ✅ Covered | Standard C-CDA section | In-office vitals likely; RPM vitals unknown |
| Lab results | ✅ Covered | Standard C-CDA section; LabCorp/Quest integration | Structured results expected |
| Imaging / diagnostic reports | ❌ Not covered | C-CDA XML cannot carry clinical images with annotations; no DICOM/image export mentioned | Product supports clinical images, annotations, possibly PACS — significant gap |
| Procedures | ✅ Covered | Standard C-CDA section | Standard coverage expected |
| Clinical notes / documents | ⚠️ Partial | C-CDA supports some note types | Product uses specialty templates, dictation, AI notes, handwriting — custom content may not map to C-CDA |
| Care plans / goals | N/A | Optional C-CDA sections; unknown if populated | Cannot assess without sample data |
| Orders / referrals | ❌ Not covered | C-CDA has limited order support | Product has CPOE, referral management — likely not fully represented |
| Insurance / coverage | ❌ Not covered | No insurance sections in C-CDA | Product stores insurance data, verification records — entirely absent |
| Claims / billing | ❌ Not covered | No billing sections in C-CDA | Product has full billing/claims/EDI via Change Healthcare — significant gap |
| Payments | ❌ Not covered | No payment sections in C-CDA | Product tracks payments, adjustments — entirely absent |
| Patient communications / portal messages | ❌ Not covered | No messaging sections in C-CDA | Product has portal with secure messaging, appointment/refill requests — entirely absent |
| Remote patient monitoring | ❌ Not covered | No RPM sections in C-CDA | Product supports BP, weight, glucose monitoring — RPM workflow data absent |
| Consents / directives | N/A | Optional C-CDA Advance Directives section; unknown if populated | Cannot assess |

**Summary**: Of 19 domains assessed, 6 are likely covered by standard C-CDA sections, 4 are partially covered, 7 are not covered at all, and 2 cannot be assessed. The product stores significant data in billing, communications, RPM, and imaging domains that C-CDA structurally cannot represent.

## 6. Documentation Quality

The documentation quality is **minimal to the point of being functionally useless** for understanding what data is exported.

**What exists:**
- A 3-page PDF with navigation instructions and screenshots
- Four screenshots showing the export UI workflow
- A link to the external HL7 C-CDA specification

**What's missing:**
- No data dictionary or field mapping
- No description of which C-CDA sections are populated
- No C-CDA template IDs or profile constraints
- No sample export file
- No data type specifications
- No value set documentation
- No description of how WEBeDoctor-specific data maps to C-CDA elements
- No acknowledgment of data that falls outside C-CDA scope
- No error handling or troubleshooting guidance
- No versioning — the PDF was created October 2023 but the product was re-certified January 2026 (v6.0)

**Could a developer build an import from this documentation?** No. A developer would need to: (1) obtain an actual C-CDA export file, (2) reverse-engineer its structure, (3) determine which sections and entries are populated, and (4) handle whatever encoding choices WEBeDoctor made. The documentation tells you only how to click the buttons in the UI, not what data you'll receive.

**Machine-readable artifacts:** None. No schemas, no sample data, no JSON/XML specifications.

## 7. Overall Assessment

### Classification

**Standard-based projection**

WEBeDoctor's EHI export is a C-CDA 2.1 clinical document generation feature repackaged as a (b)(10) export. C-CDA is a transitions-of-care standard designed for clinical summaries exchanged between providers — not a comprehensive database export format. It covers USCDI-level clinical data but structurally cannot represent billing, claims, insurance, patient communications, remote monitoring data, clinical images, or specialty-specific data that doesn't map to standard C-CDA templates.

This is the classic failure mode described in the task: a vendor pointing to their existing C-CDA/transitions-of-care capability and calling it "(b)(10)."

### Key Findings

1. **C-CDA repackaged as EHI export**: The entire (b)(10) compliance consists of generating C-CDA 2.1 documents — the same format used for transitions of care (b)(1). This covers roughly the USCDI clinical summary data (~20-30% of what the product stores). The vendor explicitly states compliance is achieved "by generating C-CDA 2.1 electronic documents" with no supplementary mechanisms.

2. **Billing and financial data entirely absent**: WEBeDoctor is a fully integrated EHR+PM platform with claims submission, payment posting, EDI, and financial reporting via Change Healthcare. None of this data is representable in C-CDA and is therefore excluded from the export. This is the single largest gap.

3. **Documentation is a 3-page how-to guide with no data content description**: The PDF (created October 2023, 860 KB, author: Syed Imran Ali) contains only navigation instructions and UI screenshots. There is zero field-level documentation, no sample data, no schema, and no acknowledgment that data exists beyond what C-CDA covers.

4. **Patient communications, RPM data, and clinical images excluded**: The product's patient portal messaging, remote patient monitoring readings (BP, weight, glucose), and clinical image annotations have no representation in C-CDA XML and are entirely absent from the export.

5. **No evidence of vendor awareness of the gap**: The documentation does not acknowledge that C-CDA is a subset of the product's data. There is no mention of plans to expand the export, no supplementary mechanisms, and no discussion of data that falls outside C-CDA scope.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA 2.1 (XML)
Model type:      Standard projection (HL7 C-CDA)
Entities:        N/A (no data dictionary; ~9-18 C-CDA sections inferred)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (ZIP of all patient C-CDAs)
Domains covered: 6 of 17 applicable domains (fully); 4 partial; 7 not covered
```

### Bottom Line

WEBeDoctor's EHI export is a C-CDA clinical summary repackaged as a (b)(10) compliance artifact. A patient or provider would receive a standard clinical document covering diagnoses, medications, allergies, labs, vitals, and immunizations — but would get **none** of their billing records, insurance information, portal messages, e-prescribing workflow data, remote monitoring readings, or clinical images. For a product that markets itself as a fully integrated EHR and practice management platform, this export covers at most a quarter of the data the system stores about patients.

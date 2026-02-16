# EHI Export Analysis: PracticeSuite, Inc.

**Product**: PracticeSuite (EHR-18.0.0), FreeChiro (EHR-18.0.0) — same underlying platform
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.2198.PRAS.01.01.1.220113 (PracticeSuite), 15.02.05.2198.FREC.01.02.1.220113 (FreeChiro)

## 1. Product Context

PracticeSuite is a cloud-based, integrated practice management and EHR platform serving independent physician practices across 61+ clinical specialties. The company claims 92,000+ medical professionals and processes over $10 billion in claims annually. FreeChiro is a chiropractic-branded version of the same platform.

**Key data domains the product stores:**

- **Clinical/EHR**: Patient demographics, encounter notes (30+ customizable templates), diagnoses/problem lists, medications, allergies, lab orders/results (integrated with Labcorp/Quest), imaging orders, vital signs, immunizations, procedures, clinical decision support alerts, implantable device tracking, care plans, family health history, social history
- **E-Prescribing**: Electronic prescriptions via NewCropRx integration, including controlled substances, prior authorizations, PDMP data
- **Billing/Revenue Cycle**: Charge entry, claims submission and tracking, denied claims management, payment posting, collections, credit card processing, insurance eligibility verification, financial reporting (140+ reports), AI-powered claim processing
- **Scheduling**: Multi-provider appointment scheduling, patient check-in, patient flow management
- **Patient Portal**: Portal messages, appointment requests, prescription refill requests, patient-completed forms, satisfaction surveys, ePayments, e-Statements (powered by HelloHealth)
- **Telehealth**: HIPAA-compliant video/phone consultations
- **Documents**: e-Faxes, referral documents, scanned documents, uploaded files
- **Interoperability**: C-CDA transitions of care, Direct messaging, FHIR APIs, immunization registry reporting

This is a comprehensive ambulatory platform with deep billing/PM capabilities — the export should cover both clinical and financial data domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.html` (159 KB) | Main EHI (b)(10) documentation page. Contains export workflow instructions, file naming conventions, and embedded screenshots. **No data dictionary, no field mapping, no schema.** | Primary source — but contains only procedural instructions |
| `downloads/k3-report-page.html` (161 KB) | K3 Patient Clinical Analysis Report documentation. Describes the report used for EHI export, search filters, and output options. | Supplementary — adds context on search capabilities |
| `downloads/page-screenshot-full.png` (1.3 MB) | Full-page screenshot of the EHI export documentation page | Confirms HTML content; no additional information |
| `downloads/singlepatsearch.png` (158 KB) | Single patient search interface screenshot | Shows search by name/MR# plus filter sections |
| `downloads/patpopulationsrch.png` (132 KB) | Population search interface screenshot | Shows filter categories: Diagnosis, Medication, Facesheet, CPT Code, Lab Order, Lab Result, Radiology, vitals |
| `downloads/ccdadownloadzip.png` (85 KB) | C-CDA ZIP contents screenshot | Shows one XML file (~253 KB) + cda.xsl stylesheet (~128 KB) per patient |
| `downloads/docdownloadzip.png` (148 KB) | Documents ZIP contents screenshot | Shows per-patient subfolder with multiple document files in original formats |
| `downloads/k3-images/K3OutputList.png` (36 KB) | K3 report search results | Shows patient list columns: MR#, PC Ref#, name, gender, DOB, age, address, phone, work phone, preferred contact, race, ethnicity, language spoken, last seen, provider, insurance, DOS, time. Three export buttons: Visit Summary, C-CDA, Documents |
| `downloads/k3-images/K3CustomVisitSummary.png` (81 KB) | Sample Custom Visit Summary Report | **Most informative artifact.** Shows actual data sections: Patient Demographics, Documentation Demographics, Encounter Demographics, Chief Complaint, Past Medical History, Allergies, Med List, Vital Signs, Assessment/Diagnosis, Plan/Recommended Action, Special Situation, Escalation/Emergency, Provider Signatures, Care Coordinator, CareTeam Communication |
| `downloads/k3-images/k3search.png`, `k3searchDetail.png`, other PNGs | Additional UI screenshots | Minor supplementary value |

**Most informative**: The K3CustomVisitSummary.png screenshot, which reveals the actual clinical data structure. **Least informative**: The icon images and duplicate screenshots.

**Critical absence**: No data dictionary, no sample C-CDA XML file, no schema, no field mapping document, no value set documentation.

## 3. Export Mechanics

- **Format**: C-CDA (HL7 CDA R2) XML files + original-format document files, each delivered as separate ZIP archives
- **Mechanism**: UI-driven via Report Central > K3 Patient Clinical Analysis Report. No API, no command-line, no automated/scheduled export documented.
- **Single-patient**: Search by patient name or MR#, then click "Download C-CDA" or "Download Documents"
- **Bulk/population**: Search by health parameters (vitals, diagnoses, medications, CPT codes, lab orders/results, radiology, facesheet), then bulk download for all matching patients. Note: this is a filtered population export, not an "all patients" export — requires search criteria.
- **Access control**: Restricted to users with Report Central privileges
- **Fees**: Not mentioned in documentation
- **Third export option**: "Download Visit Summary" also available (Custom Visit Summary Report as PDF), but this appears to be a formatted clinical summary rather than a structured data export

## 4. Export Content: What's In It

### No data dictionary exists

PracticeSuite provides **zero field-level documentation** for the EHI export. There is no data dictionary, no schema file, no sample C-CDA, no field mapping, no value set documentation, and no machine-readable artifact of any kind. The entire documentation consists of workflow instructions ("how to click buttons") and screenshots.

### What we can infer about C-CDA content

The documentation states the export produces a "full CCDA Summary" but never specifies which C-CDA sections are populated. Based on the C-CDA standard and the Custom Visit Summary screenshot, the export likely includes standard C-CDA sections:

| Inferred C-CDA Section | Evidence | Confidence |
|---|---|---|
| Patient Demographics | Visit Summary screenshot shows name, DOB, age, gender, location | High |
| Allergies | Visit Summary shows allergy categories (Medications, Food, Environmental, Animals & Insects) | High |
| Medications | Visit Summary shows "Med List" section | High |
| Vital Signs | Visit Summary shows Temperature, Heart Rate, Respiratory Rate, BP, Pain, Pulse Ox, Height | High |
| Assessment/Diagnosis | Visit Summary shows ICD codes (G43.909, R11.0) | High |
| Plan of Treatment | Visit Summary shows Plan/Recommended Action with multiple sub-fields | High |
| Chief Complaint | Visit Summary shows chief complaint field | High |
| Past Medical History | Visit Summary shows medical history notes and significant conditions | High |
| Problems | Standard C-CDA section; likely populated | Medium |
| Procedures | Standard C-CDA section; likely populated | Medium |
| Results (Labs) | K3 search filters include Lab Order/Lab Result; likely in C-CDA | Medium |
| Immunizations | Certified for immunization reporting (f)(1); likely in C-CDA | Medium |
| Encounters | Standard C-CDA section | Medium |
| Social History | Standard C-CDA section | Low-Medium |
| Family History | Certified for (a)(12); may be in C-CDA | Low-Medium |
| Medical Equipment | Certified for (a)(14) implantable devices; may be in C-CDA | Low |

### Document export content

The separate Documents ZIP contains all documents associated with the patient in their original file formats (PDFs, images, scanned documents, etc.), organized into per-patient subfolders. File naming convention: `<FileName>_<Category>[file]`. No further documentation on what document categories exist or what metadata is preserved.

### Vendor's own content organization

The vendor does not organize their export into categories or entities. The entirety of what they describe is:

| Component | Description | Documented Fields | Source |
|---|---|---|---|
| C-CDA XML | "Full CCDA Summary" per patient | 0 (no field documentation) | `ehi-export-page.html` |
| Documents ZIP | All patient documents in original format | 2 (filename, category in naming convention) | `ehi-export-page.html` |
| Visit Summary (PDF) | Custom visit summary report (optional) | 0 (not documented as structured export) | `k3-report-page.html` |

**Total vendor-documented fields: 2** (the file naming convention components). No data dictionary exists — see `analysis/entity-inventory-full.json` for the complete inferred inventory and `analysis/entity-inventory-summary.json` for summary statistics.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes exactly two export components:

1. **C-CDA XML export**: A standard C-CDA clinical document covering whatever sections PracticeSuite populates (undocumented). C-CDA is a clinical summary standard designed for care transitions — it covers demographics, allergies, medications, problems, procedures, results, vitals, immunizations, encounters, and care plans. It does **not** have sections for billing records, claims, payments, scheduling, portal messages, or operational data.

2. **Documents export**: Raw files (PDFs, images, scanned documents) associated with the patient, exported in original format. This is a useful supplement for unstructured content but does not address structured data stored in database fields.

The vendor provides no indication of any product-specific data mapping, extensions, or customizations beyond the standard C-CDA template. There is no evidence that the export includes anything beyond what a generic C-CDA generator would produce.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header demographics; Visit Summary shows name, DOB, age, gender, location | C-CDA covers basic demographics but product stores much more (contacts, insurance cards, intake forms, preferred contact method, multiple addresses/phones) — depth unclear without sample data |
| Encounters / visits | ⚠️ Partial | C-CDA Encounters section (inferred); Visit Summary shows encounter demographics with encounter type, telehealth type, start time | Likely present but depth unknown; product has rich encounter data (templates, workflows) |
| Problems / conditions / diagnoses | ⚠️ Partial | Visit Summary shows ICD codes (G43.909, R11.0); C-CDA Problem List section inferred | Standard C-CDA problem list; product likely stores more detail (onset context, verification, linked orders) |
| Medications / prescriptions | ⚠️ Partial | Visit Summary shows "Med List"; C-CDA Medications section inferred | C-CDA covers basic medication list. Product integrates with NewCropRx for e-prescribing — detailed prescription data (prior auths, PDMP, refill history, controlled substance tracking) almost certainly not in C-CDA |
| Allergies | ⚠️ Partial | Visit Summary shows allergy categories; C-CDA Allergies section inferred | Basic allergy data likely present; depth within C-CDA uncertain |
| Immunizations | ⚠️ Partial | Certified for (f)(1) immunization reporting; C-CDA Immunizations section inferred | Likely present but undocumented |
| Vitals | ✅ Covered | Visit Summary shows 7+ vital sign types; C-CDA Vital Signs section inferred | Reasonably covered through C-CDA |
| Lab results | ⚠️ Partial | K3 search filters include Lab Order/Lab Result; C-CDA Results section inferred | Basic lab results likely in C-CDA. Product integrates with Labcorp/Quest — full order detail and result history depth uncertain |
| Imaging / diagnostic reports | ⚠️ Partial | K3 search filters include Radiology; may appear in C-CDA | Uncertain depth |
| Procedures | ⚠️ Partial | C-CDA Procedures section inferred | Standard coverage likely; depth unknown |
| Clinical notes / documents | ⚠️ Partial | Documents ZIP contains raw document files; C-CDA may include note text | Documents export covers attached files. Structured note content from 30+ EHR templates — unclear how much maps into C-CDA vs. remains only in template-specific database fields |
| Care plans / goals | ⚠️ Partial | Visit Summary shows Plan/Recommended Action; C-CDA Plan of Treatment inferred | Basic plan data likely present |
| Orders / referrals | ❌ Not covered | No evidence of orders in export beyond what appears in C-CDA | Product has CPOE for meds, labs, imaging; referral module exists. Order detail, order sets, order tracking not in standard C-CDA |
| Insurance / coverage | ❌ Not covered | C-CDA has no insurance section. K3 output list shows "Insurance" column but this is display only | Product stores detailed insurance/coverage data, eligibility verification results. **Major gap** — not exportable via C-CDA |
| Claims / billing | ❌ Not covered | No billing data in C-CDA format. No separate billing export | Product processes $10B+ in claims annually. Charge entry, claims, denials, corrections, collections — **none exported**. This is the largest gap. |
| Payments | ❌ Not covered | No payment data in export | Product has payment posting, credit card processing, patient statements. Not in C-CDA |
| Consents / directives | ❌ Not covered | No evidence in export | Product likely stores consent forms; may be in Documents ZIP if scanned |
| Patient communications / portal messages | ❌ Not covered | No portal data in export | Product has patient portal (HelloHealth) with messaging, appointment requests, refill requests, surveys. None exported |
| Specialty-specific (chiropractic, multi-specialty) | ❌ Not covered | C-CDA has no specialty-specific sections | Product supports 61+ specialties with customizable templates. Specialty-specific data fields stored in proprietary templates are almost certainly not mapped to C-CDA |

## 6. Documentation Quality

**Overall: Extremely poor.** The documentation is a compliance checkbox, not a technical specification.

- **No data dictionary**: Zero field-level documentation exists
- **No sample data**: No sample C-CDA XML files are provided
- **No schema**: No XSD, JSON Schema, or machine-readable specification
- **No field mapping**: No documentation of how PracticeSuite data maps to C-CDA elements
- **No value sets**: No vocabulary or code system documentation
- **No C-CDA section inventory**: The vendor never specifies which C-CDA sections are populated
- **No version info**: No mention of which C-CDA version/template is used
- **What IS documented**: How to navigate to the K3 report, how to click search and download buttons, and file naming conventions. This is user-facing workflow documentation, not technical export documentation.
- **Could a developer build an import?** A developer receiving this export would have standard C-CDA XML and could parse it with any C-CDA library. But they would have no PracticeSuite-specific guidance — they couldn't tell which sections are populated, what coded vocabularies are used, or what data is missing without trial and error against actual export files.
- **The "publicly accessible hyperlink of the export's format"** (required by (b)(10)) links back to the same documentation page — it does not link to the C-CDA specification or any format definition.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export is a standard C-CDA clinical summary plus raw document files. C-CDA covers basic clinical data (demographics, allergies, medications, problems, vitals, labs, immunizations, encounters) — this is the USCDI clinical exchange surface, not a comprehensive EHI export. The vendor's documentation never even specifies which C-CDA sections are populated, making it impossible to confirm even USCDI-level coverage.

Critically, PracticeSuite is as much a billing/PM platform as it is an EHR — it processes $10B+ in claims annually with robust revenue cycle management features. **Zero billing, claims, payment, or insurance data appears in the export.** Patient portal communications, scheduling, specialty-specific template data, and operational records are also absent. The export covers perhaps 20-30% of the designated record set.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of a vendor relabeling their existing C-CDA clinical exchange capability as (b)(10). The telltale signs are all present:
- Export format is standard C-CDA with no vendor-specific extensions documented
- Documentation says "full CCDA Summary" — the same term used for care transitions, not EHI export
- No product-specific data dictionary or field mapping
- The K3 report's C-CDA download predates the (b)(10) documentation (the K3 report page describes the feature as "already in place" for population export)
- The single-patient C-CDA download is described as "a new feature to comply with 170.315(b)(10)" — suggesting they merely added a single-patient button to their existing population C-CDA generator
- No coverage of billing, portal, scheduling, or any data domain beyond what C-CDA naturally supports
- The "publicly accessible hyperlink of the export's format" just points back to their own documentation page rather than to the C-CDA specification

The Documents ZIP is a minor addition (exported raw files), but this only captures unstructured attachments, not the structured billing, portal, and specialty data that constitutes the majority of the designated record set.

### Key Findings

1. **No data dictionary or schema exists.** The entire (b)(10) documentation is 2 HTML pages of workflow screenshots showing how to click buttons. There is zero field-level documentation, no sample data, and no technical specification. A developer cannot determine what is in the export without generating one.

2. **Export is standard C-CDA rebranded as (b)(10).** The C-CDA download existed before (b)(10) compliance; PracticeSuite added a single-patient download button and wrote a documentation page. The population export is described as "already in place."

3. **Billing and financial data — the product's core strength — is completely absent.** PracticeSuite processes $10B+ in claims annually with comprehensive revenue cycle management. None of this data (charges, claims, payments, denials, collections, insurance details) appears in the export. C-CDA has no mechanism for billing data.

4. **Patient portal, scheduling, and specialty data are absent.** Portal messages (HelloHealth), appointment history, prescription refill requests, patient surveys, and specialty-specific template data are not in the export.

5. **The "publicly accessible hyperlink" requirement is arguably unmet.** The link points to PracticeSuite's own documentation page rather than to the C-CDA standard specification, and that page contains no format specification whatsoever.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   C-CDA XML + raw document files (ZIP)
    Entities:        N/A (no data dictionary; ~17 C-CDA sections inferred)
    Fields:          N/A (no field documentation)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Yes (population export via K3 report search)
    Domains covered: ~5-7 of 17 applicable domains (partial clinical coverage only)

### Bottom Line

PracticeSuite's (b)(10) export is their existing C-CDA clinical summary download relabeled for compliance, with a raw documents ZIP added. A patient would receive a standard clinical summary (demographics, meds, allergies, vitals, diagnoses) and their attached documents — but would get **none** of their billing history, claims, payments, insurance details, portal messages, or specialty-specific clinical data. For a platform whose primary value proposition includes revenue cycle management processing billions in claims, the complete absence of financial data from the "all EHI" export is the most significant gap.

# EHI Export Analysis: Adaptamed, LLC

**Product**: EHR Your Way  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.02.05.1042.ADAP.01.01.0.211220 (CHPL #10757)

## 1. Product Context

EHR Your Way is a cloud-based EHR built specifically for **behavioral health** — serving psychiatrists, therapists, counselors, substance abuse clinicians, and community behavioral health centers. It is marketed as an integrated platform combining clinical documentation, billing/practice management, and patient engagement in one system.

Key capabilities relevant to EHI scope:

- **Behavioral health assessments**: 50+ validated instruments (PHQ-9, GAD-7, etc.) with automated scoring and trending — a core product differentiator.
- **Treatment planning**: Outcome tracking, goals, objectives, interventions, progress measurement.
- **Substance abuse treatment**: IOP schedules, group therapy documentation, PDMP integration.
- **Custom forms**: Electronic replication of paper forms for state compliance (intake forms, consent forms, specialty assessments).
- **Billing & revenue cycle**: Integrated CMS 1500/UB-04 billing, claims submission, ERA/835 processing, payment posting, denial management, chargemaster.
- **Patient portal**: Intake forms, messaging, appointment scheduling, payment processing.
- **Clinical notes**: Customizable templates, voice dictation, AI documentation assistant.
- **E-prescribing**: Full EPCS certification with PDMP checking.
- **Lab integration**: Lab orders and results (depth unclear).
- **Telehealth**: Integrated Zoom/Teams/Meet sessions.
- **Document management**: AI-powered document indexing to patient charts.

The product serves both inpatient and outpatient behavioral health settings, including community behavioral health centers (CCBHC), residential treatment, IOP, autism/IDD services, eating disorders, correctional health, and homeless shelters.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.html` (214,711 bytes) | Single HTML page containing all EHI export documentation — narrative text describing export workflows plus a 69-row C-CDA data dictionary table. Source of truth for the entire analysis. | **Primary** |
| `downloads/screenshot-full-page.png` (1.4 MB) | Full-page screenshot of the EHI export documentation. Used to verify rendered layout matches HTML parse. | Confirmatory |
| `downloads/screenshot-top.png` (214 KB) | Screenshot of page header and compliance statement section. | Confirmatory |
| `downloads/screenshot-middle.png` (248 KB) | Screenshot of export workflows and beginning of data dictionary table. | Confirmatory |
| `downloads/enrichment/ccda-data-dictionary.json` (13 KB) | Prior agent's structured extraction of the C-CDA data dictionary — 69 elements across 28 sections. Verified against my independent parse; results match. | Confirmatory |
| `product-research.md` | Background research on EHR Your Way's capabilities and data domains. Used to establish the baseline of what the product stores. | Context |

No downloadable PDFs, ZIP files, sample exports, JSON schemas, or machine-readable artifacts were provided by the vendor. The entire documentation consists of a single HTML page.

## 3. Export Mechanics

- **Format**: C-CDA Release 2.1 (August 2015) XML documents, packaged in ZIP archives with human-readable PDF versions and any selected attachment PDFs.
- **Mechanism**: UI-based — accessible from within the patient chart (single patient) or from a dashboard export folder (bulk).
- **Single-patient export**: Navigate to patient chart → CCDA folder → Data Export. Users select date range, choose clinical sections to include, and optionally select scanned document attachments. Produces a ZIP file.
- **Bulk export**: Navigate to Dashboard → CCDA Export folder → Data Export. Filter by date range and provider, select patients from a list, queue for export. Produces individual ZIP files per patient.
- **Access constraints**: Limited to users with export privileges granted by a practice administrator.
- **Fees**: Not mentioned.
- **Developer assistance**: Explicitly stated as not required — "Users can execute exports at any time without developer assistance."

## 4. Export Content: What's In It

The export produces standard C-CDA 2.1 documents. The vendor provides a data dictionary table with 69 data elements organized across 28 C-CDA sections. Each row contains:

- **Section Name**: The C-CDA section (e.g., "Demographics," "Medication Allergies")
- **Data Element**: The element within the section (e.g., "Patient Name," "Substance")
- **Entry/XPath**: C-CDA template ID or XPath reference
- **Code System**: OID for the code system (e.g., SNOMED, RxNorm, LOINC, CVX)

**What's missing from the documentation:**
- No field descriptions or business definitions (0% of fields have descriptions)
- No data types or cardinality
- No value set bindings (OIDs listed but specific values not enumerated)
- No foreign key / relationship documentation
- No sample export files or example C-CDA XML
- No schema or machine-readable artifact beyond the HTML table

### Vendor's own content organization

The vendor organizes data by C-CDA section. All 28 sections and their field counts:

| Entity/Table (C-CDA Section) | Fields | Described | Types | Code Systems | Category |
|---|---|---|---|---|---|
| Demographics | 13 | 0 | No | 2 of 13 | Demographics |
| Reason for Visit | 1 | 0 | No | 0 of 1 | Encounters |
| Encounter | 2 | 0 | No | 2 of 2 | Encounters |
| Medication Allergies | 6 | 0 | No | 3 of 6 | Allergies |
| Medication Information | 2 | 0 | No | 1 of 2 | Medications |
| Problem or Conditions | 2 | 0 | No | 1 of 2 | Problems |
| Results | 1 | 0 | No | 0 of 1 | Lab Results |
| Social History | 3 | 0 | No | 2 of 3 | Social History |
| Vitals | 2 | 0 | No | 1 of 2 | Vitals |
| Immunizations | 4 | 0 | No | 2 of 4 | Immunizations |
| Procedures | 2 | 0 | No | 1 of 2 | Procedures |
| Assessment | 1 | 0 | No | 0 of 1 | Assessment & Plan |
| Reason for Referral | 1 | 0 | No | 0 of 1 | Assessment & Plan |
| Plan of Treatment | 2 | 0 | No | 1 of 2 | Assessment & Plan |
| Functional Status | 2 | 0 | No | 0 of 2 | Health Status |
| Mental Status | 2 | 0 | No | 0 of 2 | Health Status |
| Medical Equipment | 2 | 0 | No | 1 of 2 | Medical Devices |
| Goals | 2 | 0 | No | 0 of 2 | Goals & Concerns |
| Health Concerns | 2 | 0 | No | 1 of 2 | Goals & Concerns |
| Care Team | 1 | 0 | No | 0 of 1 | Care Team |
| History and Physical Exam Note | 2 | 0 | No | 1 of 2 | Clinical Notes |
| Progress Notes | 2 | 0 | No | 1 of 2 | Clinical Notes |
| Procedure Notes | 2 | 0 | No | 1 of 2 | Clinical Notes |
| Laboratory Notes | 2 | 0 | No | 1 of 2 | Clinical Notes |
| Consultation Notes | 2 | 0 | No | 1 of 2 | Clinical Notes |
| Discharge Summary | 2 | 0 | No | 1 of 2 | Clinical Notes |
| Imaging Narrative | 2 | 0 | No | 1 of 2 | Clinical Notes |
| Pathology Report | 2 | 0 | No | 1 of 2 | Clinical Notes |

**Summary**: 28 sections, 69 fields total. 0 fields have descriptions. 0 fields have data types. 28 of 69 fields (40.6%) reference a code system OID.

The complete inventory is in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export is organized as a standard C-CDA document with 28 sections. The sections map directly to standard C-CDA 2.1 template IDs — there are no vendor-specific extensions, no custom sections, and no data beyond what the C-CDA standard defines.

The richest section is **Demographics** (13 fields including patient name, DOB, race, ethnicity, sex, language, author info, custodian, and encompassing encounter). **Clinical Notes** is the broadest category with 8 note types (H&P, progress, procedure, lab, consultation, discharge summary, imaging narrative, pathology report) — each documented with just a section template ID and a notes entry template ID (2 fields each).

The export is essentially a standard C-CDA clinical summary. There is no evidence of any vendor-specific extension or supplementary export mechanism for data that falls outside C-CDA's scope.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Demographics section (13 fields: name, DOB, race, ethnicity, sex, language, author, custodian, encounter) | Adequate for basic demographics per C-CDA standard |
| Encounters / visits | ⚠️ Partial | Encounter section (2 fields: code + diagnosis); Reason for Visit (1 field) | Only encounter code and diagnosis — no visit details, duration, location, provider notes, or visit-level metadata |
| Problems / conditions | ⚠️ Partial | Problem or Conditions section (2 fields: section + problem value) | Section-level template ID and coded problem value only — minimal detail |
| Medications / prescriptions | ⚠️ Partial | Medication Information section (2 fields: section + consumable with RxNorm) | Only medication identity — no dosage, frequency, route, prescriber, start/stop dates, refills, pharmacy details documented |
| Allergies | ✅ Covered | Medication Allergies section (6 fields: substance, reaction, severity, status) | Reasonable allergy coverage per C-CDA standard |
| Immunizations | ✅ Covered | Immunizations section (4 fields: vaccine, route, dose) | Adequate per C-CDA standard |
| Vitals | ⚠️ Partial | Vitals section (2 fields: section + observation) | Only section-level template — no individual vital sign types documented |
| Lab results | ⚠️ Partial | Results section (1 field: section template ID only) | Minimal — just a section template reference, no documentation of result structure |
| Imaging / diagnostic reports | ⚠️ Partial | Imaging Narrative section (2 fields) | Narrative notes only, not structured imaging data |
| Procedures | ⚠️ Partial | Procedures section (2 fields: section + observation with SNOMED) | Basic procedure coding only |
| Clinical notes / documents | ✅ Covered | 8 note types documented (H&P, progress, procedure, lab, consultation, discharge summary, imaging, pathology) | Good breadth of note types per C-CDA standard. Scanned attachments can be included as PDFs. |
| Care plans / goals | ⚠️ Partial | Plan of Treatment (2 fields), Goals (2 fields), Assessment (1 field) | Section-level template references only — no structured treatment plan data |
| Orders / referrals | ⚠️ Partial | Reason for Referral section (1 field) | Only a referral narrative section — no structured order data |
| Insurance / coverage | ❌ Not covered | No insurance or coverage sections in the C-CDA export | Product stores insurance/eligibility data for billing; significant gap |
| Claims / billing | ❌ Not covered | No billing entities in export | Product has integrated billing (CMS 1500, UB-04, claims, ERA/835, denial management); **major gap** |
| Payments | ❌ Not covered | No payment data in export | Product processes payments and payment posting; gap |
| Consents / directives | ❌ Not covered | No consent or advance directive sections documented | Custom forms include consent forms; gap |
| Patient communications / portal messages | ❌ Not covered | No messaging or portal data in export | Product has patient portal with messaging; gap |
| Behavioral health assessments (specialty) | ❌ Not covered | No structured assessment data (PHQ-9, GAD-7, etc.) in export | Product's **core differentiator** — 50+ validated assessments with scoring and trending — is entirely absent from the export. Mental Status section (2 fields) cannot represent discrete scored assessment data. **Critical gap.** |
| Substance abuse treatment data (specialty) | ❌ Not covered | No substance use treatment protocols, IOP data, group therapy records, or PDMP data | Product is designed for substance abuse treatment; significant gap |
| Custom forms / intake forms | ❌ Not covered | No custom form data in export | Product allows electronic replication of paper forms; gap |
| Treatment plan outcome tracking (specialty) | ❌ Not covered | Plan of Treatment section is a basic C-CDA template — no outcome measurement data | Product emphasizes treatment outcome measurement; gap |

**Summary**: Of 21 assessed domains, 3 are adequately covered (Demographics, Allergies, Immunizations), 9 are partially covered (basic C-CDA template-level representation), and 9 are entirely absent. The absent domains include the product's most distinctive capabilities: behavioral health assessments, substance abuse treatment data, billing, and custom forms.

## 6. Documentation Quality

- **Workflow documentation**: Clear and usable — step-by-step instructions for both single-patient and bulk export, with enough detail to perform the export.
- **Data dictionary**: Thin. The 69-element table provides section names, data element names, C-CDA template IDs, and code system OIDs. No field has a description, data type, cardinality indicator, or value set enumeration. The dictionary essentially restates the C-CDA 2.1 standard rather than documenting vendor-specific implementation details.
- **Machine-readable artifacts**: None. No sample export files, no schema, no JSON/XML definition. The only artifact is the HTML page itself.
- **Developer usability**: A developer familiar with C-CDA could produce a conformant document from the template IDs listed, but they would get no product-specific guidance — the documentation tells you nothing about EHR Your Way's data model, field mappings, or extensions beyond what the C-CDA standard already defines.
- **Contact**: `support@ehryourway.com` provided for questions.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers standard clinical domains via C-CDA sections (demographics, medications, problems, notes, vitals, immunizations, etc.) but entirely omits the product's most important and distinctive data domains:

1. **Behavioral health assessments** — 50+ validated instruments with discrete scored results are the product's core differentiator. None of this appears in the export. The Mental Status section (a standard C-CDA section with 2 template-level fields) cannot represent individual PHQ-9 question responses, total scores, or score trending.

2. **Billing and revenue cycle** — The product has deep integrated billing (CMS 1500, UB-04, claims, ERA/835, payment posting, denial management). Zero billing data is in the export. C-CDA has no billing sections.

3. **Substance abuse treatment data** — For an EHR designed for substance abuse treatment, the absence of substance use treatment protocols, IOP records, group therapy data, and PDMP query results is a significant gap.

4. **Custom forms and intake data** — The product's ability to replicate paper forms electronically generates structured data that is not represented in C-CDA.

The export covers approximately the USCDI clinical summary surface — the regulatory floor for clinical exchange — but not the designated record set.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging an existing C-CDA clinical exchange capability as a (b)(10) export. The evidence:

- The export format is standard C-CDA 2.1 — the same format used for transitions of care ((b)(1)–(b)(3) certification).
- The data dictionary lists only standard C-CDA template IDs with no vendor-specific extensions.
- The 28 sections map 1:1 to standard C-CDA sections; there is no evidence of custom sections or supplementary data files.
- The export workflow is accessed via a "CCDA folder" in the patient chart — the same infrastructure used for clinical document exchange.
- No billing, behavioral health assessment, custom form, or substance abuse treatment data is included — all data domains that would require a purpose-built export mechanism beyond C-CDA.
- The documentation references the HL7 CDA implementation guide without any product-specific mapping documentation.

### Key Findings

1. **The export is a standard C-CDA clinical summary, not a purpose-built EHI export.** The 28 C-CDA sections and 69 data elements map directly to the C-CDA 2.1 standard with zero vendor extensions. This is the same clinical exchange format the product would use for transitions of care.

2. **The product's core behavioral health data is entirely absent.** EHR Your Way's primary differentiator — 50+ validated behavioral health assessments (PHQ-9, GAD-7, etc.) with automated scoring and trending — has no representation in the export. For a behavioral health EHR, this is the most clinically significant gap possible.

3. **Billing and revenue cycle data is completely missing.** Despite integrated CMS 1500/UB-04 billing, claims processing, ERA/835 remittance, and payment management, zero financial data appears in the export.

4. **Documentation is thin.** No field descriptions, no data types, no sample data, no machine-readable schemas. The data dictionary restates C-CDA standard template IDs without product-specific detail.

5. **Export mechanics are functional.** The two export workflows (single-patient and bulk) are clearly documented, require no developer assistance, and allow date-range filtering and section selection. The inclusion of scanned attachments as PDFs is a partial mitigation for unstructured documents.

### Summary Stats

```
Coverage:        Partial
Approach:        Repackaged existing export
Export format:   C-CDA 2.1 XML + PDF (ZIP archive)
Entities:        28 (C-CDA sections)
Fields:          69
Descriptions:    0%
Sample data:     No
Bulk export:     Yes
Domains covered: 3 fully + 9 partially of 21 applicable domains
```

### Bottom Line

EHR Your Way's (b)(10) export is a standard C-CDA clinical summary repackaged as an EHI export. A patient or provider would receive basic clinical data (demographics, medications, problems, notes, immunizations) but would **not** receive the behavioral health assessments, substance abuse treatment records, billing data, custom forms, or treatment outcome tracking that constitute the product's core value and the bulk of the designated record set. For a behavioral health EHR, the gap between what the product stores and what the export provides is especially wide — the most clinically important data (validated assessment scores, treatment progress) is exactly what's missing.

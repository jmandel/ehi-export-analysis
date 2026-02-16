# EHI Export Analysis: Adaptamed, LLC

**Product**: EHR Your Way  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.02.05.1042.ADAP.01.01.0.211220 (CHPL ID 10757)

## 1. Product Context

EHR Your Way is a cloud-based EHR developed by Adaptamed, LLC (San Diego, CA), designed specifically for **behavioral health** — psychiatrists, therapists, counselors, substance abuse clinicians, and social workers. The product serves both outpatient and inpatient behavioral health settings, including intensive outpatient programs (IOP), community behavioral health centers (CCBHC), autism/IDD services, eating disorder treatment, and correctional health.

The product is marketed as an all-in-one platform combining:

- **Clinical documentation**: Customizable notes, 50+ validated behavioral health assessments (PHQ-9, GAD-7, etc.) with automated scoring and trending, treatment planning with outcome tracking, group therapy documentation, voice dictation, custom forms that replicate paper forms for state compliance
- **Medication management**: e-Prescribing (including EPCS for controlled substances), integrated PDMP checking
- **Billing / practice management**: Integrated billing (CMS 1500, UB-04), claims submission, ERA/835 processing, denial management, payment posting, chargemaster, financial reporting
- **Patient portal**: Digital intake forms, messaging, appointment scheduling, payment processing
- **Lab integration**: Lab orders and results (details unclear)
- **Telehealth**: Zoom/Teams/Meet integration

This is a feature-rich product. A complete EHI export should cover clinical notes, behavioral health assessments, substance abuse treatment data, medications/prescriptions, billing records, insurance information, and custom form data — not just the standard clinical summary data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.html` (214,711 bytes) | Raw HTML of the vendor's EHI export documentation page at `ehryourway.com/electronic-health-information-export/`. Contains all export documentation and the C-CDA data dictionary table. | **Primary source** — all documentation is on this single page |
| `downloads/screenshot-top.png` (214 KB) | Screenshot of the top of the EHI export page showing compliance statement, export capabilities, formats, and access controls | Confirms rendered content matches HTML extraction |
| `downloads/screenshot-middle.png` (248 KB) | Screenshot showing export workflows and the beginning of the data dictionary table | Confirms table structure and rendering |
| `downloads/screenshot-full-page.png` (1.39 MB) | Full-page screenshot of the entire documentation page | Confirms completeness of content extraction |
| `downloads/enrichment/ccda-data-dictionary.json` (13,276 bytes) | Prior agent's structured JSON extraction of the C-CDA data dictionary table — 69 elements across 28 sections | Verified accurate against my own independent parse |
| `downloads/enrichment/extract-ccda-dictionary.ts` (3,122 bytes) | Bun TypeScript script used to produce the JSON extraction | Reproducibility artifact |
| `downloads/enrichment/README.md` (1,091 bytes) | Documentation for the enrichment pipeline | Minor |

**No downloadable files** (PDFs, ZIPs, CSVs, schemas, sample data) are linked from the page. All documentation is inline HTML. There are no sample export files, no machine-readable schemas, and no additional data dictionaries.

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture) XML, based on HL7 CDA Release 2, DSTU 2.1 (August 2015). Human-readable PDF versions are also included.
- **Packaging**: ZIP archive containing C-CDA XML, human-readable version, and any selected PDF attachments.
- **Mechanism**: UI-driven. Two workflows:
  - *Single Patient Export*: Navigate to patient chart → CCDA folder → Data Export. Users select date range, clinical sections, and optionally attach scanned documents (via Attachments tab). Click Export to download ZIP.
  - *Bulk Export*: Navigate to Dashboard → CCDA Export folder → Data Export. Filter by date range and provider, select patients, queue them, generate, and download. Produces individual ZIP files per patient.
- **Access constraints**: Limited to users with export privileges granted by a practice administrator.
- **Bulk capability**: Yes — supports multi-patient export from the dashboard.
- **Fees**: Not mentioned.

## 4. Export Content: What's In It

The export is a **standard C-CDA document** — not the vendor's native data model. The documentation provides a data dictionary table with 69 data elements across 28 C-CDA sections. Each row specifies a section name, data element name, C-CDA entry/XPath reference, and code system OID.

### Documentation characteristics

- **69 data elements** across **28 sections**
- **0 field descriptions**: Only element names are provided (e.g., "Patient Name", "Reaction", "Observation") — no business definitions, no explanations of what data populates each element
- **0 data types**: No type information (string, date, coded, etc.)
- **28 code system references** out of 69 elements (41% have a code system OID; the rest are blank or "NA")
- **0 value sets**: Code system OIDs are listed (SNOMED, RxNorm, LOINC, CVX, ICD-10) but no value set bindings are enumerated
- **0 cardinality indicators**: No required/optional/repeating documentation
- **0 relationship documentation**: No foreign keys or cross-references between sections
- **No sample data**: No example C-CDA XML or sample export files are provided

### Vendor's own content organization

The vendor organizes the export into 28 C-CDA sections. These are standard C-CDA section names, not vendor-specific categories:

| Section | Elements | With Code System | Notes |
|---|---|---|---|
| Demographics | 13 | 3 | Includes patient name, DOB, race, ethnicity, sex, language, author info, custodian, encompassing encounter |
| Reason for Visit | 1 | 0 | Free text |
| Encounter | 2 | 2 | Encounter code (CPT) and diagnosis (SNOMED/ICD-10) |
| Medication Allergies | 6 | 4 | Substance (RxNorm), reaction, severity, status (SNOMED) |
| Medication Information | 2 | 1 | Section + consumable (RxNorm) |
| Problem or Conditions | 2 | 1 | SNOMED + ICD-10 translation |
| Results | 1 | 0 | Section-level only, no individual result elements |
| Social History | 3 | 2 | Smoking status observation (LOINC/SNOMED) |
| Vitals | 2 | 1 | Vital sign observations (SNOMED/LOINC) |
| Immunizations | 4 | 2 | Vaccine (CVX), route (NCI), dose |
| Procedures | 2 | 1 | Procedure observations (SNOMED) |
| Assessment | 1 | 0 | Section-level only |
| Reason for Referral | 1 | 0 | Section-level only |
| Plan of Treatment | 2 | 1 | Planned observations (LOINC) |
| Functional Status | 2 | 0 | Section + observation (no code system specified) |
| Mental Status | 2 | 0 | Section + observation (no code system specified) |
| Medical Equipment | 2 | 1 | SNOMED |
| Goals | 2 | 0 | Section + goal entries |
| Health Concerns | 2 | 1 | SNOMED observations |
| Care Team | 1 | 0 | Section-level only |
| History and Physical Exam Note | 2 | 1 | Notes entry (LOINC: 34117-2) |
| Progress Notes | 2 | 1 | Notes entry (LOINC: 11506-3) |
| Procedure Notes | 2 | 1 | Notes entry (LOINC: 28570-0) |
| Laboratory Notes | 2 | 1 | Notes entry (LOINC: 11502-2) |
| Consultation Notes | 2 | 1 | Notes entry (LOINC: 11488-4) |
| Discharge Summary | 2 | 1 | Notes entry (LOINC: 18842-5) |
| Imaging Narrative | 2 | 1 | Notes entry (LOINC: 18748-4) |
| Pathology Report | 2 | 1 | Notes entry (LOINC: 60570-9) |

The 8 clinical note types all use the same C-CDA Notes Activity template (2.16.840.1.113883.10.20.22.4.202: 2016-11-01) differentiated by LOINC codes.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers standard C-CDA clinical summary content. Organized by domain grouping:

- **Demographics** (1 section, 13 elements): Patient identifiers, race, ethnicity, sex, language, author, custodian, encompassing encounter. This is reasonably thorough for C-CDA header content.
- **Clinical data** (19 sections, 40 elements): Standard USCDI-aligned clinical data — encounters, allergies, medications, problems, results, social history, vitals, immunizations, procedures, assessment, treatment plan, functional/mental status, medical equipment, goals, health concerns, care team, referrals. Each section has 1–6 elements, mostly at a section-level granularity rather than field-level detail.
- **Clinical notes** (8 sections, 16 elements): H&P, progress notes, procedure notes, lab notes, consultation notes, discharge summaries, imaging narratives, pathology reports. These are note-type references, not discrete data — the notes are likely included as narrative text blocks.

**Missing entirely**: Billing, insurance, claims, payments, behavioral health assessments, custom forms, substance abuse treatment protocols, PDMP data, patient portal messages, intake forms.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Demographics` section (13 elements): name, DOB, race, ethnicity, sex, language | Standard C-CDA demographics; address and phone not explicitly listed but may be in header |
| Encounters / visits | ⚠️ Partial | `Encounter` section (2 elements): encounter code and diagnosis | Encounter codes and diagnoses present, but encounter-level detail (provider, location, duration, visit type) is thin |
| Problems / conditions / diagnoses | ✅ Covered | `Problem or Conditions` section (2 elements) with SNOMED + ICD-10 | Standard problem list representation |
| Medications / prescriptions | ⚠️ Partial | `Medication Information` section (2 elements): section + consumable (RxNorm) | Medication name/code present, but dosage, frequency, prescriber, start/stop dates, and EPCS-specific controlled substance data not explicitly documented |
| Allergies | ✅ Covered | `Medication Allergies` section (6 elements): substance, reaction, severity, status | Most detailed section in the export |
| Immunizations | ✅ Covered | `Immunizations` section (4 elements): vaccine (CVX), route, dose | Reasonable coverage |
| Vitals | ✅ Covered | `Vitals` section (2 elements) with SNOMED/LOINC | Section-level; individual vital sign types not enumerated |
| Lab results | ⚠️ Partial | `Results` section (1 element, section-level only) + `Laboratory Notes` | Only section-level reference; no discrete result values, units, or reference ranges documented |
| Imaging / diagnostic reports | ⚠️ Partial | `Imaging Narrative` + `Pathology Report` sections | Notes-based (narrative text), not discrete structured data |
| Procedures | ✅ Covered | `Procedures` section (2 elements) with SNOMED | Standard representation |
| Clinical notes / documents | ✅ Covered | 8 note types (H&P, progress, procedure, lab, consultation, discharge, imaging, pathology) | Good breadth of note types; also mentions scanned document attachments as PDFs |
| Care plans / goals | ✅ Covered | `Plan of Treatment`, `Goals`, `Health Concerns` sections | Standard C-CDA coverage |
| Orders / referrals | ⚠️ Partial | `Reason for Referral` section (1 element) | Referral reason only; no order details |
| Insurance / coverage | ❌ Not covered | No insurance entities in export | Product stores insurance/eligibility data; **significant gap** |
| Claims / billing | ❌ Not covered | No billing entities in export | Product has full billing (CMS 1500, UB-04, claims, ERA/835); **major gap** |
| Payments | ❌ Not covered | No payment entities in export | Product processes payments and patient payments via portal; **significant gap** |
| Consents / directives | ❌ Not covered | No consent entities in export | May be captured in scanned attachments but not as structured data |
| Patient communications / portal messages | ❌ Not covered | No messaging or portal data in export | Product has patient portal with messaging; **gap** |
| Specialty-specific: Behavioral health assessments | ❌ Not covered | No assessment score data in export | Product's core differentiator: 50+ validated assessments (PHQ-9, GAD-7, etc.) with automated scoring and trending. `Mental Status` section is a generic C-CDA section, not discrete assessment scores. **Critical gap** |
| Specialty-specific: Substance abuse treatment | ❌ Not covered | No substance abuse-specific data in export | Product serves substance abuse treatment centers; treatment protocols, PDMP results, program-specific data absent. **Critical gap** |
| Specialty-specific: Treatment outcome tracking | ❌ Not covered | No outcome measurement data in export | Product emphasizes treatment planning with outcome tracking; not in C-CDA. **Significant gap** |
| Specialty-specific: Custom forms | ❌ Not covered | No custom form data in export | Product allows replication of paper forms as electronic versions for state compliance; data from these forms is absent. **Significant gap** |

**Summary**: 8 of 21 applicable domains are covered (✅), 5 are partially covered (⚠️), and 8 are not covered at all (❌). The uncovered domains include the product's most distinctive and clinically important data: behavioral health assessments, substance abuse treatment data, billing, and custom forms.

## 6. Documentation Quality

The documentation is **clear but minimal**. It successfully explains *how* to perform the export (step-by-step UI workflows for single and bulk export) and provides a data dictionary table. The page is well-organized and readable.

However, the documentation has serious gaps:

- **No field-level descriptions**: The data dictionary lists element names (e.g., "Observation", "Consumable") but never explains what data populates them or what they mean in the context of this EHR
- **No data types, cardinality, or constraints**: A developer couldn't build an import without referring to the C-CDA specification itself
- **No value set documentation**: Only OIDs are listed, not enumerated value sets
- **No sample data**: No example C-CDA XML files are provided
- **No machine-readable schema**: The only structured artifact is the HTML table itself
- **No acknowledgment of limitations**: The documentation does not mention that C-CDA cannot express all the data the product stores

A developer receiving this documentation would know they're getting C-CDA XML and could parse it using standard C-CDA libraries, but would have no vendor-specific guidance on how EHR Your Way populates the C-CDA beyond what the template IDs imply. The documentation essentially says "we produce standard C-CDA" without adding vendor-specific detail.

Contact email (support@ehryourway.com) is provided for questions.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is a C-CDA document — a standard clinical summary format designed for transitions of care, not comprehensive data export. The vendor has repackaged their existing C-CDA generation capability (certified under (b)(1)–(b)(3) for transitions of care) as their (b)(10) EHI export. This is a textbook case of C-CDA/FHIR repackaging being called "(b)(10)."

### Key Findings

1. **The export is C-CDA, not a native data export.** The 69 data elements across 28 sections map directly to standard C-CDA sections — these are the same sections any C-CDA-compliant EHR would produce for a transitions-of-care summary. There is no evidence of vendor-specific extensions or additional data beyond the standard.

2. **The product's most clinically important data is absent from the export.** EHR Your Way's core value proposition — 50+ validated behavioral health assessments with automated scoring and trending, substance abuse treatment protocols, treatment outcome tracking, and custom state-compliance forms — falls entirely outside what C-CDA can express. For a behavioral health EHR, this is the most significant possible gap.

3. **All billing and financial data is excluded.** The product has full revenue cycle management (CMS 1500, UB-04, claims, ERA/835, payment posting, denial management), but C-CDA has no billing sections. Insurance, claims, and payment data are absent.

4. **Documentation is thin.** 69 data elements with no descriptions, no types, no value sets, no sample data. The data dictionary is essentially a list of C-CDA template IDs — useful only to someone already familiar with the C-CDA specification.

5. **Export mechanics are reasonable.** The product does support both single-patient and bulk export via a UI, export is user-initiated without developer assistance, and scanned document attachments can be included as PDFs. The *mechanism* is compliant even though the *content* falls short.

### Summary Stats

```
Classification:  Standard-based projection (C-CDA repackaging)
Export format:   C-CDA XML (HL7 CDA R2.1) + PDF, packaged as ZIP
Model type:      Standard projection (C-CDA)
Entities:        28 C-CDA sections
Fields:          69 data elements
Descriptions:    0% (element names only, no descriptions)
Sample data:     No
Bulk export:     Yes
Domains covered: 8 of 21 applicable domains fully covered; 5 partial; 8 missing
```

### Bottom Line

EHR Your Way's EHI export is a standard C-CDA clinical summary repackaged as a (b)(10) export. A patient or provider receiving this export would get a basic clinical summary (demographics, medications, allergies, problems, notes, vitals) but would **miss the product's most important data**: behavioral health assessment scores, substance abuse treatment records, treatment outcome measurements, custom form data, and all billing/financial information. For a behavioral health EHR, these are the very data elements that drive treatment decisions — making this gap especially consequential.

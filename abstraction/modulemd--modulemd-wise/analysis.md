# EHI Export Analysis: ModuleMD, Inc.

**Product**: ModuleMD WISE™
**Analysis date**: 2025-07-15
**CHPL IDs**: 15.04.04.3123.WISE.10.00.1.221219 (CHPL #11092)

## 1. Product Context

ModuleMD WISE™ is a specialty-focused EHR platform primarily serving allergy and immunology practices, with over 300 practices and 10 million patient records. The product integrates clinical EMR, practice management (PM), and revenue cycle management (RCM) into a single platform. Key data domains relevant to EHI export completeness:

**Specialty clinical data (allergy/immunology)**:
- Skin prick testing and intradermal testing with wheal/flare measurements
- Immunotherapy management: vial mixing/compounding, injection tracking, dosing schedules, reaction monitoring
- USP 797 compliance: compounding logs, sterility testing, environmental monitoring
- Spirometry/PFT data with trend analysis
- Infusion center management: IV scheduling, drug administration, monitoring
- SkinSight AI diagnostic imaging for dermatological conditions
- JOSH AI-powered clinical dictation

**General clinical data**: Demographics, encounters, diagnoses, medications, allergies, vitals, lab results, clinical notes, care plans, referrals, immunizations, patient portal communications.

**Practice management / billing / RCM**: Appointment scheduling, charge capture, claims submission and tracking, ERA/EOB processing, patient statements, insurance verification, A/R management, denial management, financial reporting.

**Patient engagement**: Patient portal, secure messaging, appointment reminders, educational materials, telehealth.

This breadth — especially the deep specialty clinical data and integrated billing — establishes a high bar for what a complete EHI export should cover.

## 2. Artifacts Reviewed

Only **one artifact** was collected:

| Artifact | Description | Informative? |
|---|---|---|
| `B10-Data-Export-Process-Flow-Document_compressed.pdf` | 9-page process flow document (448 KB). Author: Rajesh Dandu. Created: 2023-11-20. Shows step-by-step UI screenshots for initiating a data export. | **Low** — documents only the UI workflow, not the content or structure of what is exported. No data dictionary, schema, sample data, or field-level documentation of any kind. |

No other artifacts were available: no HTML data dictionary, no JSON/XML schema, no sample export files, no supplementary documentation.

## 3. Export Mechanics

- **Format**: C-CDA XML (ClinicalSummary). All screenshots and file examples in the PDF show XML files named `*_ClinicalSummary`. Page 1 mentions CSV as a possible format ("data dictionary for comma separated values (csv) file(s)"), but no CSV output, documentation, or examples are provided anywhere in the document. A "File Type" dropdown is visible on page 4 but its value is blank/undocumented.
- **Mechanism**: UI-driven. Navigate to Administration >> Practice Setup >> Data Export >> +New Export. Select patient(s), name the archive, optionally set an encryption key, and submit.
- **Processing**: A backend batch program runs daily to process export requests. Status progresses: New → InProgress → Completed. Not real-time.
- **Single-patient vs bulk**: Supports both. Can select a single patient, multiple patients, or "Select All Patients" via checkbox (pages 2–3).
- **Access constraints**: Download link is visible only to the requestor. Downloads have expiry dates. Optional encryption key/password protection. Single patients can also download their C-CDA from the Patient Portal under Documents (page 8).
- **Fees**: Not documented.

## 4. Export Content: What's In It

### What the documentation tells us

The documentation provides **zero information** about the content or structure of the exported data. There is:

- No data dictionary
- No schema or field listing
- No description of which C-CDA sections are populated
- No sample data files
- No entity/table listing
- No relationship documentation
- No value set definitions

The only evidence of export content comes from file naming patterns visible in screenshots:

- **Page 7**: ZIP files (`QAT_1.zip`, `QAT_2.zip`, `QAT_3.zip`) containing per-patient folders
- **Page 8**: File named `QAT-1-11142023_ClinicalSummary` (XML Document) within a patient folder
- **Page 8**: Patient Portal showing `DevAsthma7-6-11172023_ClinicalSummary.xml`

The `_ClinicalSummary` naming pattern indicates standard C-CDA Clinical Summary documents.

### Vendor's own content organization

The vendor provides no content organization. There is no breakdown by category, no entity listing, no field inventory. The entire documentation is a process guide.

### Inferred content (from C-CDA standard)

Since the export produces C-CDA ClinicalSummary documents, standard sections would typically include:

| C-CDA Section (inferred) | Fields | Described | Types | Category |
|---|---|---|---|---|
| Demographics (recordTarget) | N/A | N/A | N/A | Standard C-CDA |
| Allergies and Intolerances | N/A | N/A | N/A | Standard C-CDA |
| Medications | N/A | N/A | N/A | Standard C-CDA |
| Problem List | N/A | N/A | N/A | Standard C-CDA |
| Procedures | N/A | N/A | N/A | Standard C-CDA |
| Results (Laboratory) | N/A | N/A | N/A | Standard C-CDA |
| Vital Signs | N/A | N/A | N/A | Standard C-CDA |
| Immunizations | N/A | N/A | N/A | Standard C-CDA |
| Encounters | N/A | N/A | N/A | Standard C-CDA |
| Plan of Treatment | N/A | N/A | N/A | Standard C-CDA |
| Goals | N/A | N/A | N/A | Standard C-CDA |
| Social History | N/A | N/A | N/A | Standard C-CDA |

**Critical caveat**: These sections are inferred from the C-CDA standard, not verified from the vendor's documentation or sample data. The vendor provides no information about which sections are actually populated, what fields are included, or whether any vendor-specific extensions exist.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor does not organize or describe their export content in any way. The entire documentation is a UI process guide. Based on the C-CDA ClinicalSummary format, the export likely covers basic clinical summary data — the same data typically exported under § 170.315(b)(1) Transitions of Care.

C-CDA Clinical Summary is a **constrained clinical document format** designed for care transitions, not for comprehensive data export. It is structurally incapable of representing:
- Specialty-specific clinical data (allergy skin tests, immunotherapy protocols, vial compounding)
- Billing records, claims, and revenue cycle data
- Practice management data
- Custom forms and assessments
- Infusion center operational data
- USP 797 compliance records
- Spirometry/PFT raw data and trends
- AI-generated diagnostic imaging results

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA recordTarget (inferred — not verified) | C-CDA carries basic demographics; product likely stores richer contact, insurance, and preference data |
| Encounters / visits | ⚠️ Partial | C-CDA Encounters section (inferred) | C-CDA carries encounter summaries, but not full encounter documentation with specialty workflow data |
| Problems / conditions / diagnoses | ⚠️ Partial | C-CDA Problem List (inferred) | Likely present as standard problem list; may miss specialty-specific condition tracking |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medications section (inferred) | Standard medication list; likely misses immunotherapy dosing schedules and compounding details |
| Allergies | ⚠️ Partial | C-CDA Allergies section (inferred) | Standard allergy list only; **critical gap** — skin test results (wheal/flare measurements), intradermal testing data, and detailed allergy workup data are the product's core specialty and cannot be represented in C-CDA |
| Immunizations | ⚠️ Partial | C-CDA Immunizations section (inferred) | Standard immunization records; immunotherapy injection tracking and reaction monitoring are distinct from standard immunizations |
| Vitals | ⚠️ Partial | C-CDA Vital Signs section (inferred) | Basic vitals likely covered; spirometry/PFT data unlikely to fit standard C-CDA vitals |
| Lab results | ⚠️ Partial | C-CDA Results section (inferred) | Standard lab results; specialty lab panels may not be fully represented |
| Imaging / diagnostic reports | ❌ Not covered | No evidence | Product includes SkinSight AI diagnostic imaging; C-CDA does not carry image data or AI analysis results |
| Procedures | ⚠️ Partial | C-CDA Procedures section (inferred) | Standard procedure list; infusion administration details, compounding procedures unlikely to be included |
| Clinical notes / documents | ⚠️ Partial | C-CDA may contain note sections (inferred) | Some notes may be in C-CDA; AI-dictated notes, specialty templates unlikely to be fully represented |
| Care plans / goals | ⚠️ Partial | C-CDA Plan of Treatment / Goals (inferred) | Basic care plan data; immunotherapy treatment protocols and escalation schedules unlikely |
| Orders / referrals | ⚠️ Partial | C-CDA may contain referral data (inferred) | Basic referral info possible; detailed order workflows unlikely |
| Insurance / coverage | ❌ Not covered | No evidence in C-CDA export | Product has insurance verification and management; C-CDA does not carry this data. **Significant gap.** |
| Claims / billing | ❌ Not covered | No evidence in C-CDA export | Product has full RCM with claims submission, ERA/EOB, denial management. **Major gap.** |
| Payments | ❌ Not covered | No evidence in C-CDA export | Product manages patient payments, statements, A/R. **Significant gap.** |
| Consents / directives | ❌ Not covered | No evidence | No documentation of consent data in export |
| Patient communications / portal messages | ❌ Not covered | No evidence | Product has patient portal with messaging; not in C-CDA |
| Specialty: Allergy skin testing | ❌ Not covered | No evidence | **Critical gap** — this is the product's core specialty. Skin prick/intradermal test results, wheal/flare measurements, testing panels are not representable in C-CDA |
| Specialty: Immunotherapy management | ❌ Not covered | No evidence | **Critical gap** — vial mixing, injection tracking, dose escalation, reaction monitoring are core product features with no C-CDA equivalent |
| Specialty: USP 797 compliance | ❌ Not covered | No evidence | Compounding logs, sterility testing, environmental monitoring — N/A for standard EHI but related clinical compounding data may qualify |
| Specialty: Spirometry/PFT | ❌ Not covered | No evidence | Raw PFT data and trends not representable in C-CDA |
| Specialty: Infusion center | ❌ Not covered | No evidence | IV drug administration records, monitoring data not in C-CDA |

**Summary**: Of ~20 applicable EHI domains, 0 are fully covered, ~10 are partially covered (inferred from C-CDA standard, not verified), and ~10 are not covered at all. Every "partial" rating is generous — it assumes the C-CDA includes the relevant sections, which cannot be confirmed from the documentation.

## 6. Documentation Quality

The documentation quality is **extremely poor** for the purposes of (b)(10) compliance:

- **No data dictionary**: Zero information about what data elements are in the export.
- **No schema**: No machine-readable or human-readable description of the export structure.
- **No sample data**: No example files to inspect.
- **No field documentation**: Not a single field name, type, or description is provided.
- **No content description**: The document never states what clinical data is included — only how to click through the UI to request an export.
- **Process-only documentation**: The 9-page PDF is entirely devoted to screenshots of the export UI workflow (how to select patients, submit a request, check status, download files).
- **File Type dropdown undocumented**: Page 4 shows a "File Type" dropdown but its value is blank and options are never listed. This is the only hint that formats other than C-CDA might exist.
- **CSV mentioned but undocumented**: Page 1 references CSV as a possible format, but no CSV-related documentation, schema, or examples appear anywhere.

**Could a developer build an import from this documentation?** No. The documentation provides no information about the structure or content of the exported data. A developer would need to request an actual export, examine the files, and reverse-engineer the format — which is possible for C-CDA XML (since it's a standard) but defeats the purpose of (b)(10) documentation.

## 7. Overall Assessment

### Classification

**Standard-based projection**: The export is C-CDA ClinicalSummary XML — the same clinical summary format used for Transitions of Care under § 170.315(b)(1). This covers a small fraction of the data ModuleMD WISE stores, particularly missing all specialty allergy/immunology data, all billing/RCM data, and all practice management data. The documentation is so thin it borders on "minimal/stub," but the export itself does appear to function (ZIP files with per-patient C-CDA documents), so "standard-based projection" is the more accurate classification.

### Key Findings

1. **C-CDA repackaging as (b)(10)**: The export produces ClinicalSummary XML files — effectively the same output as Transitions of Care. This is a textbook case of repackaging an existing C-CDA export as the (b)(10) EHI export, covering perhaps 15–20% of the data the product stores. (Evidence: PDF pages 7–8, file naming pattern `*_ClinicalSummary`.)

2. **Complete absence of specialty data**: ModuleMD WISE's core value proposition — allergy skin testing, immunotherapy management, vial compounding, spirometry, infusion center management — produces rich structured data that has no C-CDA equivalent. None of this data appears in the export. (Evidence: no mention of specialty data anywhere in the 9-page PDF; C-CDA standard has no sections for these data types.)

3. **No billing/RCM data**: The product includes full revenue cycle management (claims, ERA/EOB, denial management, A/R), but C-CDA carries no billing data. The export omits this entire domain. (Evidence: absence from C-CDA format; product capabilities documented in `product-research.md`.)

4. **No data dictionary or content documentation whatsoever**: The vendor's entire (b)(10) documentation is a 9-page UI walkthrough. There is zero information about what data elements are exported — no field names, no types, no descriptions, no schema. (Evidence: full text extraction and page-by-page visual review of the PDF.)

5. **CSV format mentioned but not documented**: Page 1 references CSV as a possible export format and a File Type dropdown exists (page 4), but no CSV-related documentation is provided. If CSV export exists and provides native data model access, it is entirely undocumented. (Evidence: PDF page 1 text, page 4 screenshot.)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML (ClinicalSummary)
Model type:      Standard projection (C-CDA)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (select all patients)
Domains covered: 0 of ~20 fully covered; ~10 of ~20 partially covered (inferred, not verified)
```

### Bottom Line

ModuleMD WISE's (b)(10) export is a C-CDA Clinical Summary repackaging with no data dictionary and no documentation of export content. For a specialty allergy/immunology EHR with integrated billing and deep specialty workflows, this export misses the vast majority of stored EHI — including all allergy skin testing data, immunotherapy records, billing/RCM data, and practice management data. The single biggest gap is the complete absence of the specialty clinical data that is the product's core differentiator.

# EHI Export Analysis: eHana

**Product**: eHana EHR  
**Analysis date**: 2025-07-17  
**CHPL ID**: 15.04.04.2594.eHan.19.00.1.191206 (CHPL #10200)  
**Version**: v2019-MU  
**Certification date**: 2019-12-06

## 1. Product Context

eHana EHR is a behavioral health electronic health record system purpose-built for Massachusetts nonprofit community behavioral health organizations. It serves 10,000+ users and processes 600,000+ clinical documents per month. Key capabilities relevant to EHI completeness include:

- **Clinical documentation**: Progress notes, treatment plans, assessments, psychiatric evaluations — the core of behavioral health charting
- **Billing and claims**: Full revenue cycle management including 837/835 electronic claims submission and processing
- **E-prescribing**: Integrated electronic prescribing (EPCS-certified)
- **Scheduling**: Appointment scheduling and management
- **CANS assessments**: Child and Adolescent Needs and Strengths — a Massachusetts-mandated behavioral health assessment tool
- **Program enrollment**: Multi-program client tracking across behavioral health programs
- **Scanned documents**: Document management for uploaded/scanned records
- **Secure messaging**: Patient and provider communication
- **Care coordination**: Referral management and inter-agency coordination
- **Incident reporting**: Safety and incident tracking
- **Outcomes tracking**: Program outcomes and reporting

This product stores significantly more data than a typical ambulatory EHR — the behavioral health documentation, billing/claims, CANS assessments, program enrollment, and care coordination workflows represent substantial data domains beyond what USCDI covers.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI_Export.pdf` (1.4 MB, 15 pages) | The sole (b)(10) EHI export documentation. Image-based PDF (no extractable text) showing 18 C-CDA sections with UI screenshots and XML element examples using sample patient "Alice Newman." Created 2023-05-10. | **Primary artifact** — defines the entire export |
| `downloads/SmartOnFHIR-API-Doc.pdf` (703 KB, 68 pages) | SMART on FHIR API documentation for (g)(10) — OAuth2/SMART App Launch and FHIR R4 US Core resource access. Separate from (b)(10). | Context only — shows the (g)(10) API is also standard/minimal |
| `downloads/fhir-base-urls.csv` (282 bytes) | FHIR server endpoint URLs (test and production). | Not relevant to (b)(10) |
| `downloads/screenshot-certification-page.png` (517 KB) | Screenshot of the certification documentation page at ehana.com. | Confirms the EHI Export PDF is the only (b)(10) artifact published |

The EHI_Export.pdf is the only artifact relevant to (b)(10). It is image-based — `pdftotext` returns empty output — so all content was extracted by rendering pages as PNGs (`pdftoppm -png -r 200`) and visually inspecting each page.

## 3. Export Mechanics

- **Format**: C-CDA (CDA R2) XML — standard clinical document architecture
- **Mechanism**: Unclear from documentation; the PDF shows UI screenshots suggesting a patient-level export from the EHR interface, but no step-by-step process is described
- **Single-patient vs bulk**: Appears to be single-patient based on the documentation structure (one sample patient "Alice Newman"), though not explicitly stated
- **Access constraints or fees**: Not documented

The PDF provides no operational guidance on how to initiate or receive an export — it only shows what the output document contains.

## 4. Export Content: What's In It

The export is a standard C-CDA document with 18 sections. There is no data dictionary — the PDF shows XML snippets with sample data for each section but does not provide field-level documentation with types, cardinality, value sets, or relationships.

### Quantitative summary

- **Sections**: 18 C-CDA sections
- **Fields cataloged**: 91 XML elements across all sections (derived from visible XML snippets)
- **Fields with descriptions**: 91 (100%) — descriptions are inferred from XML element names and context, not provided by the vendor
- **Fields with code systems**: 35 (38%) — standard terminologies (SNOMED-CT, LOINC, RxNorm, CVX, UCUM)
- **Documentation type**: XML examples with UI screenshots — not a field-level data dictionary

### Vendor's own content organization

The vendor organizes the export into 18 "Resource Types and Elements" listed in the PDF's table of contents. All fall under a single implicit category: clinical C-CDA data. There is no vendor-defined category system.

| Section | Fields | Code Systems | PDF Page |
|---|---|---|---|
| Electronic Chart / Patient Data | 13 | HL7 AdministrativeGender, CDC Race/Ethnicity | 3 |
| Vital Signs | 6 | LOINC, UCUM, HL7 ObservationInterpretation | 4 |
| Immunization | 6 | CVX, NCI Thesaurus | 4 |
| Allergies, Adverse Reactions, Alerts | 6 | RxNorm, SNOMED-CT | 5 |
| History of Medication Use | 7 | RxNorm, NCI Thesaurus | 6 |
| Instructions | 2 | SNOMED-CT | 7 |
| Functional and Cognitive Status | 4 | SNOMED-CT | 7 |
| Chief Complaint / Reason For Visit | 1 | — | 8 |
| Problem List | 5 | SNOMED-CT | 8 |
| Social History | 5 | SNOMED-CT, LOINC, HL7 | 9 |
| Encounters | 5 | CPT | 10 |
| Results | 7 | LOINC, UCUM, HL7 ObservationInterpretation | 11 |
| Procedures | 5 | SNOMED-CT | 12 |
| Reason for Referral | 1 | — | 12 |
| Implantable Devices | 6 | SNOMED-CT | 13 |
| Health Concerns | 4 | SNOMED-CT | 14 |
| Assessment and Plan | 4 | — | 14 |
| Goals | 4 | SNOMED-CT | 15 |

These 18 sections map directly to standard CCD/C-CDA template sections. There are no vendor-specific extensions, custom sections, or behavioral-health-specific content visible in the XML examples.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers exactly the standard C-CDA CCD template sections — the same content that would be exchanged via transitions of care (ToC) or patient health summary documents. All 18 sections are clinical in nature and use standard terminologies.

The documentation is entirely one-dimensional: every section falls under "clinical C-CDA." There are no billing sections, no behavioral health sections, no administrative sections, no program-specific sections. The export is the thinnest possible C-CDA implementation — each section shows a single example entry with standard coded data.

Notably absent is any behavioral health-specific content, which is the product's primary domain. There are no sections for:
- Service notes / progress notes (the 600K+ monthly documents)
- Behavioral health assessments (CANS, PHQ-9, etc.)
- Treatment plans with behavioral health goals
- Program enrollment and tracking
- Substance use treatment records
- Crisis intervention records

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Electronic Chart / Patient Data` — 13 fields (name, DOB, sex, race, ethnicity, language, address, phone) | Basic demographics only; no emergency contacts, no program enrollment info, no insurance details |
| Encounters / visits | ⚠️ Partial | `Encounters` — 5 fields (type, date, provider, location, diagnosis) | Standard encounter shell; no visit notes, no behavioral health service details, no duration, no session type |
| Problems / conditions | ✅ Covered | `Problem List` — 5 fields with SNOMED codes, onset dates, status | Standard C-CDA problem list |
| Medications / prescriptions | ✅ Covered | `History of Medication Use` — 7 fields with RxNorm codes, dosing | Standard medication list; no e-prescribing workflow details, no MAR |
| Allergies | ✅ Covered | `Allergies, Adverse Reactions, Alerts` — 6 fields | Standard allergy documentation |
| Immunizations | ✅ Covered | `Immunization` — 6 fields with CVX codes | Standard immunization records |
| Vitals | ✅ Covered | `Vital Signs` — 6 fields with LOINC codes | Standard vital signs |
| Lab results | ✅ Covered | `Results` — 7 fields with LOINC codes, values, ranges | Standard lab results |
| Procedures | ✅ Covered | `Procedures` — 5 fields with SNOMED codes | Standard procedure list |
| Clinical notes / documents | ❌ Not covered | No clinical note content beyond `Assessment and Plan` (4 fields) and `Chief Complaint` (1 field) | **Critical gap**: Product generates 600K+ clinical documents monthly — behavioral health progress notes, psychiatric evaluations, intake assessments, discharge summaries. None are in the export. |
| Care plans / goals | ⚠️ Partial | `Goals` (4 fields), `Assessment and Plan` (4 fields) | Bare-minimum structured entries; no behavioral health treatment plans |
| Orders / referrals | ⚠️ Partial | `Reason for Referral` — 1 free-text field | Referral reason only; no order details, no referral tracking, no prior authorizations |
| Insurance / coverage | ❌ Not covered | No insurance entities | Product manages insurance for billing; significant gap |
| Claims / billing | ❌ Not covered | No billing entities | **Critical gap**: Product handles full 837/835 claims cycle — charges, claims, payments, adjustments. None exported. |
| Payments | ❌ Not covered | No payment entities | Product processes payments; gap |
| Consents / directives | ❌ Not covered | No consent documentation | Behavioral health requires informed consent tracking |
| Patient communications | ❌ Not covered | No messaging entities | Product has secure messaging; gap |
| Specialty: Behavioral health assessments | ❌ Not covered | No CANS, PHQ-9, or other assessment instruments | **Critical gap**: CANS is a core MA behavioral health requirement; product is built around these assessments |
| Specialty: Program enrollment | ❌ Not covered | No program tracking entities | **Critical gap**: Multi-program enrollment tracking is a key eHana feature |
| Scanned documents | ❌ Not covered | No document attachment entities | Product stores scanned documents |
| Imaging / diagnostic reports | ⚠️ Partial | Implantable Devices section only | Minimal — not a primary domain for behavioral health EHR |

**Summary**: 7 of 21 applicable domains are covered (all standard USCDI clinical domains). 10 domains are not covered at all, including the product's most critical data: behavioral health documentation, billing/claims, and specialty assessments. 4 domains have partial coverage.

## 6. Documentation Quality

The documentation quality is poor:

- **No data dictionary**: The PDF shows XML snippets but does not provide a field-level data dictionary with element names, types, cardinality, optionality, or value set bindings.
- **No machine-readable artifacts**: No JSON schema, no XML schema reference, no sample C-CDA file. Only screenshots of XML fragments in a non-text-extractable PDF.
- **No operational guidance**: No instructions on how to request, initiate, or receive an export. No information about file naming, delivery mechanism, or timing.
- **No completeness documentation**: No statement about what data is or is not included relative to the full patient record.
- **Image-based PDF**: The documentation itself is a Google Doc printed to PDF via "Microsoft: Print To PDF," resulting in an image-based file that cannot be searched, indexed, or programmatically parsed.

A developer could not build an import tool from this documentation. The XML snippets are illustrative fragments, not complete schemas. There are no field descriptions beyond what can be inferred from standard C-CDA template definitions. The documentation adds nothing beyond what the C-CDA Implementation Guide already specifies.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub**

The export covers only standard C-CDA CCD sections — the same clinical summary content available via transitions of care. This maps to USCDI-scope data, which is the regulatory floor for clinical exchange, not a comprehensive EHI export. The product's core value proposition — behavioral health documentation (600K+ documents/month), CANS assessments, program enrollment tracking, billing/claims processing (837/835) — is entirely absent from the export. The gap between what eHana stores and what this export provides is enormous.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging a clinical summary as (b)(10). The telltale signs:
1. The 18 sections map exactly to standard CCD template sections with no extensions
2. No vendor-specific data dictionary — the documentation just shows C-CDA XML examples
3. No coverage of billing, behavioral health-specific data, or any non-USCDI domain
4. The PDF title references "CDA R2" and "§170.315(b)(10)" but the content is indistinguishable from a standard patient summary document
5. No evidence of any purpose-built export engineering — this appears to be the existing C-CDA generation capability relabeled

### Key Findings

1. **The export is a standard C-CDA clinical summary relabeled as (b)(10).** All 18 sections are standard CCD template sections with no vendor extensions. The documentation adds nothing beyond what the C-CDA IG already specifies. (Source: `EHI_Export.pdf`, all 15 pages)

2. **The product's core behavioral health data is entirely missing.** eHana processes 600K+ clinical documents monthly and is purpose-built for behavioral health — progress notes, psychiatric evaluations, CANS assessments, treatment plans, program enrollment. None of this data has an export path. (Source: `product-research.md` vs. `EHI_Export.pdf`)

3. **Billing and revenue cycle data is absent.** eHana handles full 837/835 claims processing, yet the export contains no billing, claims, charge, or payment data. (Source: `product-research.md` vs. `EHI_Export.pdf`)

4. **The documentation is unusable for implementation.** The PDF is image-based (no text extraction), shows XML fragments rather than complete schemas, and provides no operational guidance on how to actually obtain an export. (Source: `EHI_Export.pdf` — `pdftotext` returns empty output)

5. **No sample data or machine-readable artifacts exist.** The only artifact is a 15-page image PDF with screenshots. No sample C-CDA files, no schemas, no field-level documentation. (Source: `files.json` — only 4 artifacts, 3 unrelated to (b)(10))

### Summary Stats

```
Coverage:        Minimal/stub
Approach:        Repackaged existing export
Export format:   C-CDA (CDA R2) XML
Entities:        18 C-CDA sections
Fields:          91 (cataloged from XML snippets; no formal data dictionary)
Descriptions:    N/A (no vendor-provided field descriptions)
Sample data:     No (only XML fragment screenshots in PDF)
Bulk export:     Unclear
Domains covered: 7 of 21 applicable domains (all standard USCDI clinical)
```

### Bottom Line

A patient or provider would receive a standard clinical summary — demographics, medications, allergies, labs, problems — but would be missing the vast majority of their behavioral health record. The core of what eHana stores — service notes, behavioral health assessments, treatment plans, program enrollment, billing/claims — has no export path. This is a compliance checkbox, not a genuine EHI export effort.

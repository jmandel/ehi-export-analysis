# EHI Export Analysis: Core Solutions Inc

**Product**: Cx360 V7
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2703.Cx36.07.00.1.171226

## 1. Product Context

Cx360 is a **behavioral health, substance use disorder (SUD), and intellectual/developmental disabilities (IDD)** EHR and practice management platform from Core Solutions Inc. It is purpose-built for community mental health centers, CCBHCs, SUD treatment programs, IDD agencies, and child/family services organizations — not a general-purpose ambulatory EHR.

Key data domains the product stores:

- **Clinical**: Comprehensive behavioral health assessments (depression, PTSD, anxiety, substance use screenings), psychiatric/medical/social/addiction history, treatment plans with trackable goals and interventions, progress notes linked to goals, medication management and MAR, lab orders/results, vitals, diagnoses, immunizations
- **Behavioral health-specific**: Evidence-based screening instruments, measurement-based care outcomes, risk assessment/stratification, custom configurable clinical forms
- **IDD-specific**: Person-centered life plans, valued outcomes tracking, DSP task assignments, behavioral tracking
- **Child & family services**: Foster care records, family engagement, Title IV-E/CAPTA/COA compliance
- **Billing/RCM**: Claims submission and scrubbing, ledger/bill generation, authorization management, accounts receivable, payment tracking
- **Patient engagement**: Client portal with secure messaging, bill payment, self-surveys
- **Mobile/field**: EVV records (GPS/timestamps), mileage logs, ambient documentation (Cx360 GO), DSP Assist
- **Scheduling**: Appointments, clinician availability, telehealth sessions
- **E-prescribing**: Via Dr. First integration
- **Health information exchange**: HL7 connections, Direct Secure Messaging, FHIR API

This product's core value proposition — behavioral health assessments, treatment planning, IDD life plans, SUD protocols, custom forms — is what distinguishes it from generic EHRs and what a genuine (b)(10) export must cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Electronic-Health-Information-Export-Doc.pdf` | 12-page PDF (2.4 MB). The sole EHI export documentation. Contains cover page, overview, 5 screenshots of the export UI, and a data dictionary of 24 C-CDA sections with 82 data elements (pages 7–12). Created 2023-12-06. | **Primary source** — only artifact available |
| `downloads/Electronic-Health-Information-Export-Doc.txt` | Plain-text extraction of the PDF (7.6 KB). Table content is garbled due to multi-column layout. | Low — verified against PDF rendering |
| `downloads/enrichment/ccd-sections.json` | Structured JSON extraction of the PDF data dictionary: 24 sections, 82 elements, with template IDs, XPATHs, and code system OIDs. Hand-curated from rendered PDF pages. | **High** — machine-readable version of the data dictionary |
| `downloads/enrichment/extract-ccd-sections.ts` | TypeScript script that produced the enrichment JSON. | Reference only |
| `downloads/enrichment/coverage-accounting.json` | Extraction metadata and counts. | Reference only |
| `product-research.md` | Prior research on Cx360 capabilities and data domains. | High — establishes baseline for coverage assessment |

**No sample data files, no machine-readable schemas (XSD, JSON Schema), no FHIR CapabilityStatement, no additional documentation** were found. The entire (b)(10) documentation is a single 12-page PDF.

## 3. Export Mechanics

- **Format**: C-CDA (CCD — Continuity of Care Document) XML, plus human-readable Adobe PDF rendering
- **Standard**: HL7 Implementation Guide for CDA Release 2, Consolidated CDA Templates (DSTU R2.1, August 2015) — per §170.205(a)(4)
- **Mechanism**: UI-driven
  - **Single patient**: Via "Patient Summary Report Screen" — select patient, choose sections via 15 checkboxes, click Print/Download
  - **Bulk patients**: Via "CCDA Management" utility — select patients by provider or appointment date, click "Generate CCD"
  - **On-demand**: Images and clinical notes can be downloaded separately as PDF (mentioned but not documented in detail)
- **Single-patient**: Yes
- **Bulk capability**: Yes (by provider or appointment date)
- **Access constraints/fees**: Not documented

## 4. Export Content: What's In It

The export is a standard C-CDA/CCD document containing **24 sections with 82 data elements**.

### Data dictionary quality

- **82 data elements** across 24 C-CDA sections
- **0 fields (0%)** have descriptions beyond the element name
- **0 fields (0%)** have documented data types
- **27 fields (32.9%)** have code system OID references
- **30 fields (36.6%)** have XPATH/Entry path references
- **No relationships**, cardinality, optionality, or value set details documented
- **No sample data** provided
- **No vendor-specific extensions** documented — strictly standard C-CDA sections

### Vendor's own content organization

The vendor organizes the export as standard C-CDA sections. All 24 sections are listed below (from `analysis/entity-inventory-full.json`):

| C-CDA Section | Fields | With Code System | With XPATH |
|---|---|---|---|
| Patient Demographics/Information | 6 | 3 | 6 |
| Provider's name and office contact information | 3 | 0 | 3 |
| Date and Location of visit | 2 | 0 | 2 |
| Chief Complaint and Reason for visit | 1 | 0 | 0 |
| Encounters | 5 | 2 | 1 |
| Immunizations | 9 | 3 | 1 |
| Instructions | 1 | 1 | 1 |
| Treatment Plan | 2 | 1 | 2 |
| Social History | 3 | 2 | 1 |
| Problems | 3 | 1 | 1 |
| Medications | 5 | 1 | 1 |
| Medication Allergies | 4 | 4 | 1 |
| Laboratory Tests | 4 | 1 | 0 |
| Laboratory Information | 5 | 0 | 0 |
| Laboratory value(s)/result(s) | 5 | 1 | 1 |
| Vitals | 2 | 1 | 1 |
| Goal | 3 | 0 | 1 |
| Procedures | 2 | 1 | 1 |
| Care team member(s) | 3 | 0 | 1 |
| Reason for Referral | 1 | 1 | 1 |
| Medical Equipment | 2 | 1 | 1 |
| Mental Status | 4 | 1 | 1 |
| Functional Status | 4 | 1 | 1 |
| Health Concern | 3 | 1 | 1 |
| **TOTAL** | **82** | **27** | **30** |

This is a standard set of C-CDA sections — identical to what would be produced for a (b)(1) Transitions of Care export. There are no vendor-specific extensions, no behavioral health-specific sections, and no custom data elements beyond what the C-CDA standard defines.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export is organized entirely around standard C-CDA sections. There is no vendor-specific categorization — the sections map 1:1 to the Consolidated CDA Implementation Guide template IDs. The export covers the standard clinical summary data classes:

- **Demographics**: 6 elements (name, sex, DOB, race, ethnicity, language)
- **Encounters**: 7 elements across 2 sections (encounters + date/location)
- **Problems/Medications/Allergies**: 12 elements across 3 sections
- **Labs**: 14 elements across 3 sections (tests, info, results)
- **Other clinical**: Vitals (2), immunizations (9), procedures (2), goals (3)
- **Assessment**: Mental status (4), functional status (4), health concern (3)
- **Care coordination**: Care team (3), referral (1), instructions (1), treatment plan (2)
- **Social history**: 3 elements
- **Devices**: Medical equipment (2)

There is **no depth beyond standard C-CDA**. Each section has only the elements defined by the C-CDA template — no additional vendor-specific fields, no behavioral health extensions, no IDD-specific content. The Mental Status section, for example, has 4 generic elements (Assessment, Assessment Date, Results, Comments) — it cannot represent the structured multi-question psychiatric screening instruments (PHQ-9, GAD-7, AUDIT-C, etc.) that are the product's core clinical content.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | 6 standard C-CDA elements (name, sex, DOB, race, ethnicity, language) | Basic demographics only; no address, phone, contacts, emergency contacts, insurance identifiers |
| Encounters / visits | ⚠️ Partial | Encounter Code (CPT), Performer, Diagnosis, Location, Date | Standard encounter summary; no session duration, service type, billing modifiers, place of service detail |
| Problems / conditions / diagnoses | ✅ Covered | Problem (SNOMED/ICD-10), Status, Active date | Standard representation adequate for diagnosis list |
| Medications / prescriptions | ✅ Covered | Medication (RxNorm/NDC), Directions, Start/End Date, Status | Standard medication list; no prescriber detail, quantity, refills, pharmacy |
| Allergies | ✅ Covered | Substance (RxNorm), Reaction, Severity, Status (all SNOMED-coded) | Well-coded allergy section |
| Immunizations | ✅ Covered | Vaccine (CVX/CPT-4), Date, Status, Route, Site, Manufacturer, Dose, Lot Number, Notes | Reasonably detailed for a behavioral health EHR |
| Vitals | ⚠️ Partial | Observation (LOINC), Observation Date/Time — only 2 elements | Generic; no specific vital sign types enumerated |
| Lab results | ✅ Covered | 14 elements across 3 lab sections (tests, information, results) with LOINC coding | Adequate for lab result representation |
| Procedures | ⚠️ Partial | Procedure (CPT-4/SNOMED/HCPCS), Date — only 2 elements | Minimal procedure data |
| Clinical notes / documents | ❌ Not covered | PDF mentions "ability to download Images/Clinical notes on demand" as separate from CCD export | Product stores detailed progress notes linked to treatment goals; these are NOT in the structured export. On-demand download is separate and undocumented |
| Care plans / goals | ⚠️ Partial | Treatment Plan section (Planned Observation, Planned Date); Goal section (Goal, Value, Date) | C-CDA treatment plan section is a thin placeholder — cannot represent Cx360's structured behavioral health treatment plans with trackable goals, interventions, and progress tracking |
| Orders / referrals | ⚠️ Partial | Reason for Referral (1 element) | Only referral reason; no referral tracking, status, receiving provider, or order details |
| Insurance / coverage | ❌ Not covered | No insurance/coverage sections in export | Product stores insurance/enrollment information (visible in UI screenshot); significant gap |
| Claims / billing | ❌ Not covered | No billing entities in export | Product has full RCM module (claims, charges, payments, AR, authorization management); **major gap** |
| Payments | ❌ Not covered | No payment data in export | Product supports payment tracking and client portal payments; gap |
| Consents / directives | ❌ Not covered | No consent/directive sections | Product likely stores consent forms for behavioral health treatment |
| Patient communications / portal messages | ❌ Not covered | No messaging data in export | Product has client portal with secure messaging; gap |
| Specialty: Behavioral health assessments | ❌ Not covered | Mental Status section has 4 generic elements; no structured instrument data | Product's **core value proposition** — PHQ-9, GAD-7, AUDIT-C, psychiatric history, comprehensive BH assessments, measurement-based care data — has no representation in the export. **Critical gap** |
| Specialty: IDD data | ❌ Not covered | No IDD-specific sections | Product stores person-centered life plans, valued outcomes, DSP task data, behavioral tracking; **critical gap** |
| Specialty: SUD treatment | ❌ Not covered | No SUD-specific sections beyond generic Social History | Product stores addiction history, SUD assessments, MAT tracking; **significant gap** |
| Specialty: Child & family services | ❌ Not covered | No child welfare sections | Product has foster care management, family engagement modules; gap |
| Custom forms / configurable assessments | ❌ Not covered | No mechanism for exporting custom form data | Product supports configurable clinical forms; gap |
| Medical devices | ✅ Covered | Medical Equipment section with Implanted Device (SNOMED) and GMDN PT Description | Adequate |
| Social history | ⚠️ Partial | Social History Observation (LOINC), Description (SNOMED), Dates — 3 elements | Standard USCDI smoking status level; cannot represent the rich social/psychiatric/addiction history Cx360 stores |

**Summary**: Of 22 assessed domains, 6 are covered, 7 are partially covered, and 9 are not covered at all. The most critical gaps are in behavioral health assessments, IDD data, SUD treatment data, billing/claims, clinical notes, and custom forms — which collectively represent the majority of what makes this a behavioral health EHR rather than a generic clinical summary tool.

## 6. Documentation Quality

- **12 pages total**, of which ~5 are screenshots/cover page and ~5 are data dictionary tables
- **No descriptions** for any of the 82 data elements — only element names
- **No data types** documented
- **No cardinality or optionality** information
- **No value sets** documented beyond code system OID references
- **No sample CCD/XML files** provided
- **No machine-readable schema** (no XSD, no Schematron, no JSON schema)
- **No error handling** or edge case documentation
- **No documentation** of the "on-demand download" for images/clinical notes
- **No vendor-specific mapping** — the documentation simply references the C-CDA standard

A developer could import this data using the public C-CDA IG — the vendor documentation adds almost nothing beyond confirming which sections are populated. The documentation is a compliance checkbox, not a useful technical resource.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub**

The export covers only standard C-CDA clinical summary data — the USCDI floor. For a behavioral health/IDD EHR, this represents a small fraction of the designated record set. The product's core clinical value — structured behavioral health assessments, IDD life plans, SUD treatment protocols, measurement-based care data, custom clinical forms — is entirely absent from the export. Billing, insurance, client communications, and specialty data are all missing. The 82 data elements across 24 standard C-CDA sections cover what any generic EHR would export for transitions of care.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging an existing C-CDA clinical summary export as (b)(10). The evidence is unambiguous:

1. The format is C-CDA CCD — the same format used for (b)(1) Transitions of Care
2. The 24 sections map exactly to standard C-CDA templates with no vendor extensions
3. The documentation explicitly references the C-CDA IG standard (§170.205(a)(4)) — the same standard used for (b)(1)
4. There is no product-specific data dictionary — just standard C-CDA element names
5. The UI for single-patient export appears to be the same "Patient Summary Report" used for clinical summaries
6. No behavioral health, IDD, SUD, billing, or custom form data is included — domains that have no natural C-CDA representation
7. The 15 selectable sections in the UI exactly match standard C-CDA clinical summary sections

The vendor appears to have pointed their existing transitions-of-care C-CDA export at the (b)(10) requirement and written 12 pages of documentation around it.

### Key Findings

1. **The export is a standard C-CDA clinical summary, not a comprehensive EHI export.** 24 sections, 82 elements — all standard C-CDA with zero vendor extensions. This is functionally identical to a (b)(1) transitions of care export. (`Electronic-Health-Information-Export-Doc.pdf`, pages 7–12)

2. **The product's core behavioral health data is entirely absent.** Structured psychiatric assessments, evidence-based screening instruments (PHQ-9, GAD-7, etc.), measurement-based care outcomes, IDD life plans, SUD treatment protocols, and custom clinical forms — the data that defines this product — cannot be represented in C-CDA and are not exported. This is the single most critical gap.

3. **Billing and revenue cycle data is absent despite the product having a full RCM module.** Claims, charges, payments, authorization management, accounts receivable — none appear in the export. (`product-research.md`, "Revenue Cycle Management / Billing" section)

4. **Clinical notes are not in the structured export.** The PDF mentions "ability to download Images / Clinical notes on demand" as a separate capability, but this is not part of the CCD export and is not documented. Progress notes linked to treatment goals — a core Cx360 feature — are effectively inaccessible. (`Electronic-Health-Information-Export-Doc.pdf`, page 2)

5. **Documentation is minimal.** 0% of data elements have descriptions or type information. No sample data, no schemas, no import guidance. The documentation adds almost nothing beyond confirming which standard C-CDA sections are populated.

### Summary Stats

```
Coverage:        Minimal/stub
Approach:        Repackaged existing export
Export format:   C-CDA (CCD) XML + PDF rendering
Entities:        24 (C-CDA sections)
Fields:          82
Descriptions:    0% (0 of 82)
Sample data:     No
Bulk export:     Yes (by provider or appointment date)
Domains covered: 6 of 22 applicable domains (7 partial)
```

### Bottom Line

A patient or provider requesting their complete behavioral health record from Cx360 via this export would receive a standard clinical summary — diagnoses, medications, allergies, labs — but would lose the vast majority of their behavioral health-specific data: psychiatric assessments, treatment plans with goal tracking, IDD life plans, SUD treatment history, custom clinical forms, progress notes, billing records, and communications. This is a C-CDA transitions-of-care export relabeled as (b)(10), covering roughly the USCDI floor while the product stores extensive specialty data that has no representation in the export.

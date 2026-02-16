# EHI Export Analysis: MDOfficeManager

**Product**: GeeseMed v7.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.09.3013.Gees.07.00.1.250101 (CHPL #11586)

## 1. Product Context

GeeseMed is a cloud-based EHR from MDOfficeManager LLC (Clarksville, IN), a small vendor targeting ambulatory practices, outpatient surgery centers, and long-term care (LTC) facilities (SNF, NF, ALF). The product is marketed alongside MDOfficeManager PMS (Practice Management System) as an integrated platform. It claims support for 22+ medical specialties.

Key data domains the product stores, relevant to export completeness:

- **Clinical charting**: Template-based notes, dictation/transcription, macros, specialty patient cards
- **Problems, medications, allergies, immunizations, vitals, labs** (standard clinical data)
- **E-prescribing**: SureScripts-certified including EPCS
- **Lab orders and results**: Interfaces with "all major laboratories"
- **Billing/RCM**: Fully integrated billing with claims processing, denial tracking, revenue cycle management
- **Care plans**: Certified for (b)(11) care plan criteria
- **Patient portal**: Lab results, medical records, appointment requests, messaging
- **Telehealth**: Secure video and chat, remote patient monitoring
- **Referrals, orders, implantable devices**
- **LTC-specific features**: Marketed to SNF/NF/ALF; integration with PointClickCare mentioned

This product stores significantly more data than what a C-CDA clinical summary can represent — notably billing/claims data, clinical notes in their native structure, portal messages, telehealth sessions, and LTC-specific assessments.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/GeeseMed_b10_Health-Info.Export_11202023.pdf` | 8-page PDF (844 KB). The sole artifact — contains export overview, step-by-step UI screenshots for single and bulk export, standard reference, and a data dictionary table listing C-CDA sections and fields. Created Nov 20, 2023 in Microsoft Word 2016 by author "dimple" (Dimple Shah, developer contact). | **Primary source**; thin but the only documentation available. |

Only one artifact was collected. No sample data files, no machine-readable schemas, no additional documentation pages were available.

## 3. Export Mechanics

- **Format**: C-CDA XML (HL7 CDA R2, Consolidated CDA Templates DSTU 2.1, August 2015), delivered as ZIP archives containing per-patient C-CDA XML files, human-readable CCD renderings, and supplemental clinical PDFs
- **Mechanism**: UI-based export within GeeseMed EHR
  - **Single patient**: Select date range → "Create and View CCD" → review → "Export" button → downloads ZIP
  - **Bulk export**: Select date range + provider → search patients → select patients → choose destination (local path or Direct Mail) → optionally schedule as recurring → "Generate CCD" → download batch ZIP
- **Single-patient**: Yes
- **Bulk capability**: Yes, with scheduling/recurring options
- **Access constraints/fees**: Not documented; the PDF states it is "intended for the use of MDOfficeManager – GeeseMed clients only"

The batch export ZIP shown in the documentation contains per-patient XML files, readable CCD files, and at least one supplemental PDF ("LungReport"), suggesting some clinical documents are bundled as PDFs. However, which document types are included and under what conditions is not documented.

## 4. Export Content: What's In It

The entire data dictionary spans pages 6–8 of the PDF. It consists of a two-column table ("Data Elements" / "Description") organized by C-CDA section headers with template IDs.

**Quantitative summary** (from `analysis/entity-inventory-full.json`):
- **21 C-CDA sections** documented
- **68 total fields** across all sections
- **19 fields (27.9%)** have descriptions beyond just restating the field name
- **49 fields (72.1%)** have no description at all
- **No data types** documented for any field
- **No value sets, cardinality, or constraints** documented
- **No relationships/foreign keys** — the only structure is the C-CDA document hierarchy
- **No sample data files** provided

### Vendor's own content organization

The vendor organizes content by C-CDA section. All sections are in the "C-CDA Section" category — there is no vendor-defined categorization beyond the CDA template structure.

| Section | Template ID | Fields | Fields Described |
|---|---|---|---|
| Patient Demographics/Information | — | 8 | 0 |
| Provider's name and office contact information | — | 5 | 5 |
| Participant (Next of Kin) | — | 4 | 4 |
| Encounter Diagnosis | 2.16.840.1.113883.10.20.22.2.22.1 | 4 | 4 |
| Immunizations | 2.16.840.1.113883.10.20.22.2.2.1 | 4 | 1 |
| Treatment Plan | 2.16.840.1.113883.10.20.22.2.10 | 2 | 2 |
| Social History | 2.16.840.1.113883.10.20.22.2.17 | 2 | 2 |
| Problems | 2.16.840.1.113883.10.20.22.2.5.1 | 3 | 0 |
| Medications | 2.16.840.1.113883.10.20.22.2.1.1 | 4 | 1 |
| Medication Allergies | 2.16.840.1.113883.10.20.22.2.6.1 | 5 | 0 |
| Vitals | 2.16.840.1.113883.10.20.22.2.4.1 | 2 | 0 |
| Laboratory Tests | — | 4 | 0 |
| Laboratory Information | — | 5 | 0 |
| Laboratory Results | 2.16.840.1.113883.10.20.22.2.3.1 | 4 | 0 |
| Goal | 2.16.840.1.113883.10.20.22.2.60 | 1 | 0 |
| Procedures | 2.16.840.1.113883.10.20.22.2.7.1 | 2 | 0 |
| Referral | 1.3.6.1.4.1.19376.1.5.3.1.3.1 | 2 | 0 |
| Medical Equipment | 2.16.840.1.113883.10.20.22.2.23 | 1 | 0 |
| Cognitive Status | 2.16.840.1.113883.10.20.22.2.56 | 2 | 0 |
| Functional Status | 2.16.840.1.113883.10.20.22.2.14 | 2 | 0 |
| Health Concern | 2.16.840.1.113883.10.20.22.2.58 | 2 | 0 |
| **Total** | | **68** | **19** |

Where descriptions exist, they are brief restatements (e.g., "Encounter Code" → "Diagnosis code," "Associated Person Name" → "Next of kin name"). No description provides data type, format, or value set information.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is a standard C-CDA clinical summary document. The 21 sections correspond directly to standard C-CDA templates — there is no evidence of vendor-specific extensions, custom sections, or non-clinical data inclusion. The sections cover:

- **Patient identification**: Demographics (8 fields), provider info (5 fields), next of kin (4 fields)
- **Clinical core**: Encounter diagnoses, problems, medications, allergies, immunizations, vitals, lab results, procedures
- **Care planning**: Treatment plan (future appointments/orders), goals, referrals
- **Assessments**: Cognitive status, functional status, health concerns
- **Devices**: Medical equipment / implantable devices

The richest sections are demographics (8 fields), medication allergies (5 fields), and provider info (5 fields). Many sections are extremely thin — Goals has 1 field ("Goal Description"), Medical Equipment has 1 field ("Implanted Device name / ID"), and most clinical sections have 2–4 fields each.

The batch export screenshot shows supplemental PDFs can be included (a "LungReport" PDF is visible), but this mechanism is entirely undocumented — there is no list of what clinical document types trigger PDF inclusion.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | 8 fields (name, sex, DOB, race, ethnicity, language, phone, address) + next of kin (4 fields) | Basic USCDI demographics only; no insurance/coverage IDs, no emergency contacts beyond next of kin |
| Encounters / visits | ⚠️ Partial | Encounter Diagnosis section (4 fields: code, name, date, status) | Encounter diagnoses only — no encounter metadata (visit type, date/time, location, provider, disposition, reason for visit) |
| Problems / conditions | ⚠️ Partial | Problems section (3 fields: problem, status, date onset) | Minimal — no resolution date, no severity, no verification status, no linked orders |
| Medications / prescriptions | ⚠️ Partial | Medications section (4 fields: medication, direction/SIG, start date, end date) | Basic medication list only; no prescription details (pharmacy, prescriber, dosage form, quantity, refills, EPCS data) despite SureScripts e-Rx integration |
| Allergies | ⚠️ Partial | Medication Allergies section (5 fields: substance, reaction, severity, status, date) | Reasonable for C-CDA; limited to medication allergies (no food/environmental allergies documented) |
| Immunizations | ✅ Covered | Immunizations section (4 fields: vaccine name, date, status, notes) | Adequate for basic immunization records |
| Vitals | ⚠️ Partial | Vitals section (2 fields: observation, observation date) | Only 2 fields — no individual vital sign breakdown (BP, HR, temp, etc.) documented; relies on C-CDA structure |
| Lab results | ✅ Covered | Three lab sections (13 fields total): Laboratory Tests, Laboratory Information, Laboratory Results | Relatively detailed for C-CDA — covers ordering, lab facility info, and results with reference ranges |
| Imaging / diagnostic reports | ❌ Not covered | No imaging section in export | Product supports CPOE for imaging orders; imaging results/reports are not documented in export |
| Procedures | ⚠️ Partial | Procedures section (2 fields: procedure, date) | Minimal — just procedure name and date; no provider, no status, no coded procedure details |
| Clinical notes / documents | ⚠️ Partial | Not in data dictionary; batch export screenshot shows supplemental PDFs (e.g., "LungReport") can be included | Product's core is template-based charting with dictation/transcription; the export's handling of clinical notes is undocumented. The PDF attachment mechanism is not described. |
| Care plans / goals | ⚠️ Partial | Treatment Plan (2 fields) + Goal (1 field — just "Goal Description") | Very thin; product is certified for (b)(11) care plans but export captures minimal care plan data |
| Orders / referrals | ⚠️ Partial | Treatment Plan mentions "Future Appointments, lab orders, medication orders and diagnostic orders"; Referral section (2 fields) | Only future/planned orders, not historical orders. Referrals have just name and date. |
| Insurance / coverage | ❌ Not covered | No insurance entities in export | Product has integrated billing with insurance/claims processing; significant gap |
| Claims / billing | ❌ Not covered | No billing entities in export | Product has full billing/RCM capabilities (claims, denial tracking, revenue cycle); **major gap** |
| Payments | ❌ Not covered | No payment entities in export | Product tracks payments as part of RCM; gap |
| Consents / directives | ❌ Not covered | No consent entities in export | N/A — not clearly a product capability based on available info |
| Patient communications / portal | ❌ Not covered | No portal message entities in export | Product has patient portal with messaging, appointment requests, record access; gap |
| Telehealth data | ❌ Not covered | No telehealth entities in export | Product offers telehealth with video/chat and remote patient monitoring; gap |
| LTC-specific data | ❌ Not covered | No LTC-specific entities in export | Product markets to SNF/NF/ALF and integrates with PointClickCare; if LTC-specific data is stored, this is a gap |

**Summary**: Of 19 applicable domains, 2 are adequately covered, 9 are partially covered (C-CDA minimum), and 8 are entirely absent. The absent domains include billing, insurance, payments, clinical notes (beyond ad-hoc PDFs), imaging, patient portal, telehealth, and LTC-specific data — all of which are product capabilities per vendor marketing.

## 6. Documentation Quality

- **Usability**: The PDF provides clear step-by-step screenshots of the export process. A user could follow the instructions to generate an export. However, a developer could not build an import from this documentation — there are no data types, no value sets, no schemas, and no sample data.
- **Data dictionary**: Present but superficial. The two-column table lists field names and brief descriptions for 68 fields. 72% of fields lack any description. No field has a documented type, format, constraint, or value set.
- **Machine-readable artifacts**: None. No JSON schema, no XSD, no sample C-CDA files.
- **Standard reliance**: The documentation references the C-CDA DSTU 2.1 standard and provides template IDs for most sections, effectively delegating data structure documentation to the HL7 standard. A developer would need the C-CDA specification to interpret the export.
- **Supplemental PDFs**: The batch export apparently includes clinical documents as PDFs, but this is mentioned in a single sentence and screenshot — there is no documentation of which document types are included, how they map to the clinical record, or what triggers their inclusion.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub**

The export is a standard C-CDA clinical summary with 21 sections and 68 fields. This maps directly to the USCDI clinical exchange surface — the same data available via (b)(1)/(b)(2) transitions of care. There is no coverage of billing, insurance, claims, payments, patient portal data, telehealth records, or LTC-specific data, all of which are capabilities GeeseMed advertises. The documentation is an 8-page PDF with a 3-page data dictionary that provides no field types, value sets, or sample data. Even within covered clinical domains, coverage is thin (e.g., Goals has 1 field, Procedures has 2 fields, Vitals has 2 fields).

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook example of repackaging an existing C-CDA transitions-of-care export as a (b)(10) EHI export. The evidence is clear:
1. The export format is C-CDA XML — the standard clinical exchange format used for (b)(1)/(b)(2) transitions of care
2. The data dictionary lists only standard C-CDA template sections with no vendor extensions
3. The documentation explicitly references the C-CDA DSTU 2.1 standard as the basis
4. There is no coverage of non-clinical data (billing, portal, telehealth) that would indicate a purpose-built EHI effort
5. The data elements map exactly to what a standard CCD would contain — nothing more

The one slightly positive signal is the bulk export's inclusion of supplemental clinical PDFs (e.g., "LungReport"), which goes marginally beyond a pure C-CDA export. However, this mechanism is undocumented and appears to be an ad-hoc addition rather than a systematic attempt to export all EHI.

### Key Findings

1. **Repackaged C-CDA export**: The (b)(10) export is GeeseMed's existing C-CDA clinical summary mechanism relabeled. The 21 C-CDA sections with 68 fields represent standard USCDI clinical exchange data — nothing beyond what's available via transitions of care. (`GeeseMed_b10_Health-Info.Export_11202023.pdf`, pages 6–8)

2. **Major billing/financial data gap**: GeeseMed is marketed with fully integrated billing, claims processing, denial tracking, and revenue cycle management — yet zero billing, insurance, claims, or payment data appears in the export. (`product-research.md`; absence confirmed in PDF data dictionary)

3. **Extremely thin documentation**: 68 fields total across 21 sections, with only 19 (27.9%) having any description beyond the field name. No data types, value sets, cardinality, sample data, or machine-readable schemas. (`analysis/entity-inventory-summary.json`)

4. **Undocumented PDF attachment mechanism**: The batch export apparently bundles clinical documents as PDFs (a "LungReport" is shown in a screenshot), but there is no documentation of what this covers, making it impossible to assess how much clinical note content is actually exported. (`GeeseMed_b10_Health-Info.Export_11202023.pdf`, page 5)

5. **Multiple product capabilities unaddressed**: Patient portal messages, telehealth sessions, remote patient monitoring data, e-prescribing transaction history, and LTC-specific data (despite marketing to SNF/NF/ALF) are entirely absent from the export documentation.

### Summary Stats

```
Coverage:        Minimal/stub
Approach:        Repackaged existing export
Export format:   C-CDA XML (HL7 CDA R2, Consolidated CDA Templates DSTU 2.1)
Entities:        21 (C-CDA sections)
Fields:          68
Descriptions:    27.9% of fields have descriptions
Sample data:     No
Bulk export:     Yes
Domains covered: 2 of 19 applicable domains adequately; 9 partially (C-CDA minimum)
```

### Bottom Line

GeeseMed's (b)(10) export is a repackaged C-CDA clinical summary — the same format and content used for transitions of care — relabeled as an EHI export. A patient or provider requesting their complete health information would receive a clinical summary covering basic demographics, diagnoses, medications, allergies, labs, and vitals, but would be missing all billing/financial records, detailed clinical notes, e-prescribing history, patient portal communications, telehealth data, and any LTC-specific assessments. The single biggest gap is the complete absence of billing and financial data from a product whose integrated billing capabilities are a core selling point.

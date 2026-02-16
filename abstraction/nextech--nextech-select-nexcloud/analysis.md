# EHI Export Analysis: Nextech

**Product**: Nextech Select and NexCloud
**Analysis date**: 2026-02-16
**CHPL IDs**: 11722 (Nextech Select and NexCloud), 11723 (Nextech Select and NexCloud with NewCropRx)

## 1. Product Context

Nextech Select/NexCloud is a specialty-focused integrated EHR and practice management platform serving dermatology, ophthalmology, plastic surgery, orthopedics, and med spa practices. "Select" is the on-premise deployment; "NexCloud" is the cloud SaaS version — both share the same core functionality and are jointly certified.

The product is **not just an EHR** — it encompasses:
- **Clinical documentation/EHR**: Specialty-specific customizable charting templates, problem lists, medication lists, allergy lists, vitals, lab orders/results, referral management, CCDA support, clinical decision support
- **E-Prescribing** (NewCropRx variant): Via DrFirst/NewCrop integration with EPCS support
- **Photo/Image management**: Integrated clinical photography, before-and-after comparison, image markup
- **Practice management**: Scheduling, patient intake, digital check-in, insurance eligibility verification
- **Billing & RCM**: Insurance billing, cosmetic/elective procedure billing, claims submission/tracking, payment posting, payment processing, ASC billing
- **Patient portal & engagement**: Portal, mobile app, two-way texting, telehealth
- **CRM & Marketing**: Lead tracking, campaign management, communication logs
- **Analytics**: KPI dashboards, revenue tracking, operational analytics
- **Inventory management**: Supply tracking, POS, injectable inventory

This breadth means a genuine (b)(10) export should cover clinical, billing, insurance, scheduling, messaging, custom forms, and documents at minimum. CRM, inventory, and marketing may be separately licensed modules whose EHI status is ambiguous.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Nextech_Select_NexCloud_EHI_Export_Documentation_2025.pdf` | 8-page PDF (729 KB), created 2025-10-30. Describes export structure, folder hierarchy, file naming, data relationships, CCDA data classes, and configuration notes. | **High** — primary procedural documentation |
| `Nextech_Select_NexCloud_EHI_Export_Documentation.pdf` | 7-page PDF (266 KB), created 2023-11-16. Original version registered at CHPL. Superseded by 2025 version. | **Low** — superseded |
| `Nextech_Select_NexCloud_EHI_Export_Data_Dictionary_2025.xlsx` | Excel workbook (56 KB), 16 sheets, 730 field definitions. Each field has name, description, and optional note. | **High** — primary data dictionary |
| `compliance-ehi-export-documentation.html` | Nextech compliance hub page (92 KB). Lists EHI export docs for all Nextech products with download links. | **Low** — navigation reference only |

The XLSX data dictionary and 2025 PDF were the most informative artifacts. Both are well-structured and complementary: the PDF explains the export mechanics and CCDA coverage, while the XLSX provides field-level detail for all CSV entities and the EMN format.

## 3. Export Mechanics

- **Format**: Multi-format ZIP archive per patient containing:
  - **14 CSV files** for structured data (billing, demographics, appointments, insurance, notes, etc.)
  - **EMN PDFs** — one PDF per encounter (Electronic Medical Note)
  - **CCDA XML** — standard C-CDA document
  - **Documents folder** — all attached documents, images, photos, eCR responses, direct message attachments
  - **iPad Documents folder** — documents from iPad Select application
  - **ReadMe** — link to public documentation
- **Mechanism**: UI-initiated per-patient export (based on documentation; no API mechanism described)
- **Scope**: Single-patient export. No bulk/multi-patient export mechanism described.
- **Access constraints**: No fees mentioned. Documentation is publicly accessible. Export is PHI and requires encryption/secure storage.
- **ZIP naming**: `FirstNameInitial_LastName_PersonID_DateTimeStamp.ZIP`

**Configuration notes** (2025 version):
- Practices using a third-party PM system will not get PM data in the export; they should contact their PM administrator separately.
- Practices using the iPad application will see limited PM data.
- Billing data (Charges, Payments, Payment Plans) is excluded for iPad-only practices since that data is stored in the non-certified PM module.

## 4. Export Content: What's In It

### Data Dictionary Overview

The XLSX data dictionary contains **16 entities** with **730 total fields**. Every field (100%) has a text description. 84 fields (11.5%) have additional explanatory notes. No explicit data types are documented. No value sets or coded value enumerations are provided. No foreign key or relationship documentation exists in the XLSX itself (relationships are described in the PDF narrative).

### Vendor's own content organization

| Entity/Table | Format | Fields | Described | Notes | Category |
|---|---|---|---|---|---|
| Patient Demographics | CSV | 212 | 212 | 18 | Demographics |
| Charges | CSV | 140 | 140 | 4 | Billing |
| Insurances | CSV | 85 | 85 | 2 | Insurance |
| Appointments | CSV | 52 | 52 | 4 | Scheduling |
| Payments | CSV | 50 | 50 | 8 | Billing |
| EMN | PDF | 43 | 43 | 2 | Clinical Encounters |
| Recalls | CSV | 27 | 27 | 2 | Patient Outreach |
| Notes | CSV | 23 | 23 | 16 | Clinical Notes |
| Recalls Steps | CSV | 17 | 17 | 3 | Patient Outreach |
| Follow up | CSV | 16 | 16 | 9 | Patient Outreach |
| iPad Tasks | CSV | 15 | 15 | 4 | iPad Application |
| Payment Plans | CSV | 13 | 13 | 1 | Billing |
| DSI feedback | Unknown | 11 | 11 | 5 | Clinical Decision Support |
| PracYakker | CSV | 10 | 10 | 2 | Internal Messaging |
| iPad Notes | CSV | 9 | 9 | 2 | Clinical Notes |
| Custom | CSV | 7 | 7 | 2 | Custom Data |

### Category breakdown

| Category | Entities | Fields |
|---|---|---|
| Demographics | 1 | 212 |
| Billing | 3 | 203 |
| Insurance | 1 | 85 |
| Patient Outreach | 3 | 60 |
| Scheduling | 1 | 52 |
| Clinical Encounters | 1 | 43 |
| Clinical Notes | 2 | 32 |
| iPad Application | 1 | 15 |
| Clinical Decision Support | 1 | 11 |
| Internal Messaging | 1 | 10 |
| Custom Data | 1 | 7 |

### Key entity details

**Patient Demographics (212 fields)**: Extremely comprehensive. Covers patient identifiers, name, address, contacts, race/ethnicity/language (USCDI), insurance identifiers, guarantor info, employer, emergency contacts, referral sources, consent flags, marketing preferences, portal access status, provider assignments, custom fields. This is one of the most thorough demographics exports seen.

**Charges (140 fields)**: Deep billing data including CPT codes, ICD codes (up to 12 diagnosis pointers), modifiers (4 positions), quantities, fees, adjustments, bill status, provider info, facility, referring provider, insurance details, authorization data, claim tracking, ERA posting info. This is genuine billing data — not a summary.

**Insurances (85 fields)**: Covers primary/secondary/tertiary tiers, subscriber details, group numbers, copays, deductibles, authorization info, eligibility, insured party information.

**Payments (50 fields)**: Payment method, amount, adjustments, check/CC info, insurance payments, copay tracking, ERA details. Linked to Charges via Bill ID.

**EMN (43 fields)**: Describes the structure of encounter PDFs — encounter title, topic/section titles, items/questions, header/footer merge fields, patient identifiers, vitals (height, weight, temp, pulse, BP systolic/diastolic, respiration, BMI, SpO2, pain, head circumference), assessment and plan items, and signature information. The documentation explicitly states that EMN content is highly customizable per practice and the 43 fields listed are "best practice" examples — actual encounters may have more or fewer fields.

### CCDA coverage (from PDF documentation)

The CCDA export covers these data classes:
- Patient Demographics, Health Insurance
- Allergies, Medications, Medications administered
- Problems (including SDOH Problems), Problem list
- Procedures (including SDOH Intervention, Reason for Referral)
- Clinical Test, Lab orders, Lab results, Diagnostic Imaging
- Immunizations, Medical equipment (implantable devices)
- Assessment and Plan of Treatment (including SDOH Assessment)
- Social history, Vital signs
- Goals (including SDOH Goals), Assessments, Health concerns
- Mental/Cognitive status, Disability Status, Pregnancy Status
- Care team members, Diagnoses/encounter diagnoses
- Referring Provider, Discharge summary
- History & Physical note, Reason for Visit

### Cross-entity relationships (from PDF)

- **Charges ↔ Payments**: Linked by Bill ID
- **Payments ↔ Payment Plans**: Linked by Payment Plan ID / Payment ID
- **Recalls ↔ Appointments**: Linked by Appointment ID
- **Recalls ↔ Recall Steps**: Linked by Recall Step ID
- All entities linked to patient via Patient ID

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized into structured CSV files for discrete data, EMN PDFs for clinical encounters, CCDA for standardized clinical data, and document attachments. The vendor's coverage is strongest in:

1. **Demographics** (212 fields): The deepest entity in the export. Covers patient identifiers, contacts, guarantor, employer, emergency contacts, insurance IDs, preferences, consent, portal access, and custom fields.

2. **Billing** (203 fields across 3 entities): Genuinely deep. Charges (140 fields) includes CPT, ICD-10, modifiers, fees, adjustments, claim status, authorization data, and ERA posting. Payments (50 fields) covers payment methods, amounts, insurance payments, and copay tracking. Payment Plans (13 fields) tracks installment arrangements. This is not summary billing — it's the full billing record.

3. **Insurance** (85 fields): Thorough coverage of multi-tier coverage, subscriber info, copays, deductibles, and authorization details.

4. **Scheduling** (52 fields): Comprehensive appointment data including status, provider, location, confirmation, linked recalls.

5. **Clinical encounters**: Via EMN PDFs (rendering of encounter documentation) plus CCDA (structured clinical data). The EMN captures specialty-specific content that doesn't map to structured standards. The CCDA covers USCDI data classes plus SDOH.

6. **Patient outreach** (60 fields): Recalls and follow-ups with step tracking.

7. **Internal messaging** (10 fields): PracYakker captures internal messages mentioning the patient, including deleted messages.

8. **Clinical notes** (32 fields): Notes from across the system — clinical, billing, labs, appointments, reminders, history.

The thinnest areas are Custom Data (7 generic fields — by design, as these are practice-configured) and DSI feedback (11 fields — a compliance tracking entity for decision support interventions).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics.csv` (212 fields) — name, DOB, address, contacts, race/ethnicity, language, guarantor, employer, emergency contacts, consent, portal access | Thorough; one of the deepest demographics exports seen |
| Encounters / visits | ✅ Covered | EMN PDFs (one per encounter, 43 documented fields); CCDA encounter data; `Appointments.csv` (52 fields) | Clinical encounters captured as PDFs (not structured); appointment scheduling data in CSV |
| Problems / conditions / diagnoses | ✅ Covered | CCDA Problems, Problem list, SDOH Problems; diagnoses in EMN PDFs; ICD codes in `Charges.csv` | CCDA provides structured problems; EMN provides full encounter context; billing has coded diagnoses |
| Medications / prescriptions | ⚠️ Partial | CCDA Medications and Medications administered; EMN encounter data | No dedicated CSV for prescription details. E-prescribing data (NewCropRx variant) via DrFirst integration may reside externally. Medication data is in CCDA and EMN but not as structured discrete fields in CSV |
| Allergies | ✅ Covered | CCDA Allergies section | Standard CCDA coverage |
| Immunizations | ✅ Covered | CCDA Immunizations section | Standard CCDA coverage |
| Vitals | ✅ Covered | EMN PDFs (height, weight, temp, pulse, BP, respiration, BMI, SpO2, pain, head circumference); CCDA Vital signs | Vitals in EMN (as PDF) and CCDA (structured). Good vital sign range |
| Lab results | ✅ Covered | CCDA Lab orders, Lab results; Clinical Tests | Standard CCDA coverage; no dedicated CSV for lab discrete data |
| Imaging / diagnostic reports | ✅ Covered | CCDA Diagnostic Imaging section; clinical photos in Documents folder | CCDA provides imaging data; clinical images/photos exported as attachments |
| Procedures | ✅ Covered | CCDA Procedures (including SDOH Intervention); CPT codes in `Charges.csv` | Both CCDA and billing provide procedure data |
| Clinical notes / documents | ✅ Covered | EMN PDFs (all encounters); `Notes.csv` (23 fields — notes from across system); Documents folder (all attachments, images, photos) | Comprehensive: every encounter as PDF, all attached documents, and cross-system notes |
| Care plans / goals | ✅ Covered | CCDA Assessment and Plan of Treatment, Goals (including SDOH Goals), Health concerns | Standard CCDA coverage |
| Orders / referrals | ⚠️ Partial | CCDA Reason for Referral, Referring Provider; `Charges.csv` has authorization fields | No dedicated referral tracking export. Referral management is a product feature but only referral reasons/providers appear in CCDA. No order tracking CSV |
| Insurance / coverage | ✅ Covered | `Insurances.csv` (85 fields) — multi-tier coverage, subscriber info, copays, deductibles, authorization | Very thorough |
| Claims / billing | ✅ Covered | `Charges.csv` (140 fields), `Payments.csv` (50 fields), `Payment Plans.csv` (13 fields) | Genuinely deep billing export — CPT, ICD, modifiers, fees, adjustments, ERA data, authorization |
| Payments | ✅ Covered | `Payments.csv` (50 fields) — payment methods, amounts, insurance payments, copay tracking | Comprehensive payment records |
| Consents / directives | ⚠️ Partial | `Patient Demographics.csv` has consent flags; CCDA may include advance directives | Consent flags present in demographics but no dedicated consent document export beyond what's in Documents folder |
| Patient communications / portal messages | ⚠️ Partial | `PracYakker.csv` (10 fields) — internal messaging; online visit attachments in Documents folder | PracYakker is internal staff messaging, not patient-facing portal messages. Product has patient portal, two-way texting — no dedicated export for patient communications |
| Specialty-specific (dermatology, ophthalmology, plastic surgery) | ⚠️ Partial | EMN PDFs capture specialty encounter content; clinical photos in Documents folder | Specialty-specific clinical data (ophthalmic exams, dermatology findings, etc.) is in EMN PDFs but not as structured/queryable data. Product has layered drawings, subspecialty flowsheets, and specialty templates — these are rendered in PDFs but not exported as discrete data |

## 6. Documentation Quality

**Strengths:**
- Clear, well-organized 8-page PDF describing the complete export structure, folder hierarchy, file naming conventions, and data relationships
- Field-level data dictionary in XLSX with 730 fields — 100% have descriptions
- Documentation explains edge cases: empty CSVs for missing data, deleted records included with status flags, inactive patients included
- Billing data relationships explicitly documented (Charges → Payments → Payment Plans)
- Configuration-dependent notes (third-party PM, iPad limitations) are disclosed
- Two versions available (2023, 2025) showing active maintenance

**Weaknesses:**
- No explicit data types — all fields described by name and text description only. A developer would need sample data to determine date formats, number formats, string lengths
- No value set documentation for coded fields (e.g., possible values for "Appointment Status," "Charge Status," "Payment Method")
- No sample export files or worked examples
- No machine-readable schema (no CSV header templates, no XSD)
- EMN documentation explicitly states fields are "best practice" and may vary per practice — the actual clinical encounter schema is unknowable without seeing specific practice configurations
- No foreign key documentation in the XLSX itself; relationships described only in PDF prose

**Overall**: A developer could understand the general structure and build a basic import from these docs, but would need sample data to handle data types, coded values, and edge cases. The documentation is well above average for EHI exports but stops short of being fully machine-actionable.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains Nextech Select/NexCloud stores for patient care and billing. The combination of 14 CSV files (730 documented fields), EMN encounter PDFs, CCDA, and document attachments covers demographics, billing (140 fields of charges data), payments, insurance, appointments, clinical notes, encounters, and documents. The billing coverage alone — with CPT codes, ICD-10 diagnoses, modifiers, fees, adjustments, ERA posting, and authorization data across 203 fields — goes far beyond what any USCDI/FHIR clinical exchange would include. The custom data export, internal messaging (including deleted messages), recalls, follow-ups, and iPad-specific data show attention to the full data footprint.

The main gaps are in structured specialty clinical data (which is captured in EMN PDFs but not as queryable discrete fields), referral tracking, and patient-facing communications. These are real but modest gaps for a specialty ambulatory EHR. The product's CRM, inventory, and analytics modules may store patient-adjacent data, but these are potentially separate licensed modules and their EHI status is ambiguous.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged clinical exchange. The telltale signs:
1. **14 custom CSV files** with a dedicated data dictionary — this is the vendor's native data model exported to flat files, not a standard format repackaged
2. **Billing data** (Charges, Payments, Payment Plans) with 203 fields — this data would never appear in a (g)(10) FHIR API or C-CDA exchange
3. **Insurance data** (85 fields) at a depth far exceeding USCDI Health Insurance Information
4. **Internal messaging** (PracYakker) and **recalls/follow-ups** — operational data beyond any clinical exchange standard
5. **Custom data export** for practice-specific fields
6. The CCDA is included as a supplement, not as the primary export mechanism
7. The documentation is product-specific with a dedicated data dictionary, not a pointer to a generic standard specification

### Key Findings

1. **Genuine billing depth**: The Charges entity (140 fields) is one of the deepest billing exports seen in EHI documentation. It includes CPT, ICD-10, modifiers, fee schedules, adjustments, ERA data, authorization tracking, and provider information — this is real billing data, not a summary.

2. **Purpose-built multi-format approach**: The CSV + EMN PDF + CCDA + Documents combination is pragmatic and well-suited for a specialty EHR with highly customizable encounter templates. Each format serves its purpose.

3. **100% field descriptions**: All 730 fields in the data dictionary have text descriptions. While no data types or value sets are provided, this is still above-average documentation.

4. **Specialty clinical data is PDF-only**: The richest clinical content (ophthalmic exams, dermatology findings, surgical notes) lives in EMN PDFs and is not exported as structured/queryable data. This is the product's most significant limitation — a recipient could read but not computationally process encounter details.

5. **No dedicated medication/prescription CSV**: Despite e-prescribing being a product feature (NewCropRx variant), there is no structured medication export beyond what's in the CCDA. Prescription details may reside in the DrFirst/NewCrop external system.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   CSV + PDF + C-CDA + native documents (ZIP per patient)
    Entities:        16
    Fields:          730
    Descriptions:    100% (730/730)
    Sample data:     No
    Bulk export:     No (single-patient)
    Domains covered: 13 of 17 applicable domains (4 partial)

### Bottom Line

Nextech has built a genuine (b)(10) EHI export that goes meaningfully beyond USCDI clinical exchange. The 730-field data dictionary across 16 entities — anchored by 203 fields of billing data, 212 fields of demographics, and 85 fields of insurance data — demonstrates real investment in exporting the designated record set. The main limitation is that specialty clinical encounter data (the most valuable content for dermatology, ophthalmology, and plastic surgery practices) is exported only as rendered PDFs rather than structured data, making downstream computational use difficult. A patient or provider would get a comprehensive, readable copy of their data, though computational reuse of encounter details would require manual extraction from PDFs.

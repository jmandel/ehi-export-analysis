# EHI Export Analysis: Nextech

**Product**: Nextech Select and NexCloud
**Analysis date**: 2026-02-16
**CHPL IDs**: 11722 (Nextech Select and NexCloud), 11723 (Nextech Select and NexCloud with NewCropRx)

## 1. Product Context

Nextech Select/NexCloud is an integrated EHR and practice management platform serving specialty practices in dermatology, ophthalmology, plastic surgery, orthopedics, and med spas. "Select" is the on-premise deployment; "NexCloud" is the cloud-based SaaS version. Both share the same core product and are certified jointly. The "with NewCropRx" variant (CHPL 11723) adds e-prescribing via DrFirst/NewCrop integration.

The product is **not just an EHR** — it encompasses:

- **Clinical documentation**: Specialty-specific customizable charting templates, encounter notes (EMN), problem/medication/allergy lists, lab orders/results, referrals, care plans, clinical photos/images, drawing tools, specialty flowsheets (e.g., glaucoma, cataract planning)
- **Practice management**: Scheduling, patient intake, digital check-in, appointment management
- **Billing & RCM**: Insurance billing, cosmetic/elective procedure billing, claims submission/tracking, payment processing, payment plans, accounts receivable
- **Insurance management**: Eligibility verification, multi-tier insurance tracking, copay/deductible management
- **Patient engagement**: Patient portal, online scheduling, telehealth, two-way texting
- **CRM & marketing**: Lead tracking, campaign management, communication logs
- **Analytics**: Dashboards, KPIs, revenue tracking, operational metrics
- **Inventory**: Product/supply tracking, POS, injectable tracking
- **E-prescribing** (NewCropRx variant): Rx history, EPCS, drug interaction checking

This establishes a broad baseline: a complete EHI export should cover clinical documentation, billing, payments, insurance, demographics, appointments, medications, and custom/specialty data at minimum. CRM, inventory, and analytics data may also qualify as EHI if patient-linked.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Nextech_Select_NexCloud_EHI_Export_Documentation_2025.pdf` | 8-page PDF (729,375 bytes, dated 2025-10-30) describing export structure, folder hierarchy, CSV files, EMN PDFs, CCDA content, and data relationships. Author: Simmie McCarty. | **Most informative** — primary documentation of what the export contains and how it's structured |
| `Nextech_Select_NexCloud_EHI_Export_Documentation.pdf` | 7-page PDF (265,621 bytes, dated 2023-11-16) — original version registered at CHPL. Author: Hristina Arsovska. | Useful for version comparison; superseded by 2025 version |
| `Nextech_Select_NexCloud_EHI_Export_Data_Dictionary_2025.xlsx` | Excel data dictionary (56,430 bytes) with 16 sheets and 730 field definitions. Each field has name, description, and optional note. | **Most informative** — the primary computable artifact for understanding export schema |
| `compliance-ehi-export-documentation.html` | Nextech compliance hub page (92,339 bytes) listing EHI documentation for all Nextech products with download links. | Contextual — confirms documentation is publicly accessible |
| `enrichment/data-dictionary.json` | Prior agent's JSON extraction of the XLSX (133,548 bytes). | Verified against independent extraction — field counts match |
| `enrichment/extraction-summary.json` | Prior agent's extraction accounting. | Confirmed: 16 sheets, 730 fields, 0 parse failures |

## 3. Export Mechanics

- **Format**: Per-patient ZIP file containing CSV files (structured data), EMN PDFs (encounter notes), C-CDA XML (standardized clinical data), and native documents/images
- **ZIP naming**: `FirstNameInitial_LastName_PersonID_DateTimeStamp.ZIP`
- **Mechanism**: UI-based single-patient export (documentation describes per-patient ZIP generation)
- **Bulk capability**: Not documented — appears to be single-patient only
- **Access constraints**: No fees or access restrictions mentioned. Documentation is publicly accessible at the compliance hub (`nextech.com/compliance/ehi-export-documentation`)
- **Configuration notes**: Practices using a third-party PM system will not have PM data in the export. iPad-configured practices will have limited PM/billing data. These caveats are documented in the 2025 version.

## 4. Export Content: What's In It

The export contains 4 distinct data types within each patient ZIP:

### 4a. CSV Files (14 files, structured tabular data)

Independently parsed from the XLSX data dictionary (script: `analysis/analyze_dictionary.py`; output: `analysis/full-entity-inventory.json`).

**Totals**: 16 entities (14 CSV + 1 EMN PDF + 1 DSI feedback), 730 fields total. 100% of fields have descriptions. 84 fields (11.5%) have additional notes providing value set hints or behavioral explanations.

| Entity | Format | Fields | Fields w/ Note | Category |
|---|---|---|---|---|
| Charges | CSV | 140 | 3 | Billing |
| Patient Demographics | CSV | 212 | 18 | Demographics |
| Insurances | CSV | 85 | 0 | Insurance |
| Appointments | CSV | 52 | 0 | Scheduling |
| Payments | CSV | 50 | 0 | Billing |
| EMN | PDF | 43 | 2 | Clinical Encounters |
| Recalls | CSV | 27 | 0 | Patient Outreach |
| Notes | CSV | 23 | 0 | Clinical Notes |
| Recalls Steps | CSV | 17 | 0 | Patient Outreach |
| Follow up | CSV | 16 | 0 | Patient Outreach |
| iPad Tasks | CSV | 15 | 0 | iPad Application |
| Payment Plans | CSV | 13 | 0 | Billing |
| DSI feedback | — | 11 | 3 | Clinical Decision Support |
| PracYakker | CSV | 10 | 0 | Internal Messaging |
| iPad Notes | CSV | 9 | 0 | iPad Application |
| Custom | CSV | 7 | 0 | Custom Data |

### Category breakdown

| Category | Entities | Total Fields |
|---|---|---|
| Billing | 3 | 203 |
| Demographics | 1 | 212 |
| Insurance | 1 | 85 |
| Scheduling | 1 | 52 |
| Clinical Encounters | 1 | 43 |
| Clinical Notes | 2 | 32 |
| Patient Outreach | 3 | 60 |
| Custom Data | 1 | 7 |
| Internal Messaging | 1 | 10 |
| Clinical Decision Support | 1 | 11 |
| iPad Application | 1 | 15 |

### Key entity details

**Charges (140 fields)**: The most granular billing entity. Includes patient identifiers, full provider details (26 fields including name, address, identifiers like NPI/DEA/EIN/Medicare/Medicaid numbers), charge amounts (unit price, quantity, pretax, tax rates, discounts, patient/insurance responsibility splits), CPT codes with modifiers and diagnosis pointers, bill details (12 ICD-9 + 12 ICD-10 diagnosis code fields, dates of illness/hospitalization, prior auth numbers, claim sent dates), and Place of Service (POS) and Location details (address, phone, EIN for each). This is genuine billing data, not a summary.

**Patient Demographics (212 fields)**: Extremely comprehensive. Beyond standard demographics (name, address, contact, DOB, SSN, race/ethnicity/language/tribal affiliation, sex/gender identity/sexual orientation), includes: allergy list, current medications list, serial numbers, occupation/industry (ODH), marital status, related persons, patient type/groups, custom fields (4 name/value pairs), provider details (26 fields), patient coordinator (14 fields), referral source with counts, referring patient details, emergency contact, employer, primary care physician (13 fields), referring physician (16 fields), location details (14 fields), global period tracking, and default ICD-9/ICD-10 codes (4 of each with descriptions).

**Insurances (85 fields)**: Covers primary and secondary insurance comprehensively — subscriber demographics, group numbers, copay amounts/percentages, effective dates, company details, plus responsible party (guarantor) information and insurance referral authorization.

**Payments (50 fields)**: Payment details including method, check/bank/account numbers, credit card details (type, number, name, exp date, auth number), prepayment flag, insurance payment flag, and links to bills and payment plans.

### 4b. EMN (Electronic Medical Note) PDFs

One PDF per encounter, placed in the `EMN/` folder. The data dictionary describes 43 "best practice" fields including encounter title, patient demographics, current medications (name, start/discontinue dates), allergies (name, notes, dates), procedures, admission/discharge times, discharge status, providers, diagnosis codes, charges (CPT codes), and prescriptions. However, the documentation explicitly states these fields are **not static** and are **completely customizable** per practice — the actual content of any given EMN PDF depends on the practice's template configuration.

This means specialty-specific clinical data (ophthalmology exams, dermatology findings, plastic surgery notes) is captured in EMN PDFs but is not in a machine-readable structured format.

### 4c. C-CDA XML

Standard C-CDA file per patient. The 2025 documentation lists the following data classes:

- Patient Demographics (partial — full set in CSV)
- Health Insurance (some data complementary to CSV)
- Allergies, Medications, Medications administered
- Problems (including SDOH Problems), Problem list
- Procedures (including SDOH Interventions, Reason for Referral)
- Clinical Tests, Lab orders, Lab results, Diagnostic Imaging
- Immunizations, Medical equipment
- Assessment and Plan of Treatment (including SDOH Assessment)
- Social history, Vital signs (partial — full set in EMN)
- Reason for Referral, Reason for Visit
- History & Physical note
- Goals (including SDOH Goals), Assessments, Health concerns
- Mental/Cognitive status, Disability Status, Pregnancy Status
- Care team members, Diagnoses/encounter diagnoses
- Implantable Devices, Referring Provider, Discharge summary

The 2025 version expanded SDOH coverage compared to the 2023 version (which lacked SDOH problems/interventions/assessments/goals, clinical tests, diagnostic imaging, disability status, and pregnancy status).

### 4d. Documents folder

All documents attached to the patient chart: images/photos, eCR reportability responses, direct message attachments, online visit ("Iagnosis") attachments, user-attached documents, clinical and summary of care documents. iPad documents are in a separate `iPad Documents/` folder.

### Relationships between entities

The documentation explicitly describes linking keys:
- Charges ↔ Payments: linked by **Bill ID**
- Payments ↔ Payment Plans: linked by **Payment Plan ID / Payment ID**
- Recalls ↔ Appointments: linked by **Appointment ID**
- Recalls ↔ Recalls Steps: linked by **Recall Step ID**
- Notes: linked to originating context via Bill ID, Payment ID, Charges ID, Mail ID, Lab ID, Lab Result ID, Recall ID, Appointment ID, Schedule Payment ID, Patient Implantable Device ID, or Message Thread ID
- All entities: linked by **Patient ID**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export's strength is its **billing and financial data depth**. The Billing category (Charges + Payments + Payment Plans) has 203 fields — more than many vendors' entire exports. The Charges entity alone (140 fields) includes CPT codes, 24 diagnosis code fields (ICD-9 and ICD-10), modifiers, fee breakdowns, patient/insurance responsibility splits, prior authorization, place of service, and billing location. This is genuine practice management data, not a clinical summary.

Demographics (212 fields) is similarly deep, going well beyond USCDI requirements to include referral source tracking, patient coordinator details, custom fields, employer information, and default diagnosis codes.

Insurance (85 fields) covers primary and secondary tiers with subscriber details, copay structures, company information, and responsible party/guarantor data.

The **clinical data strategy is split**: structured discrete data (medications, allergies, problems, labs, vitals, immunizations, procedures) is in the C-CDA, while the full encounter documentation (including specialty-specific content) is in EMN PDFs. This means specialty clinical data is exported but not in a machine-readable format.

The **thinnest areas** are:
- Custom Data (7 fields): Generic key-value export for practice-specific fields
- PracYakker (10 fields): Simple internal messaging
- iPad Notes/Tasks (9 and 15 fields): iPad-specific variants of notes and tasks

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (212 fields) — identifiers, contacts, race/ethnicity/language, gender identity, sexual orientation, tribal affiliation, occupation, employer, emergency contact, related persons | Thorough — exceeds USCDI requirements |
| Encounters / visits | ✅ Covered | EMN PDFs (one per encounter, 43 documented fields); `Appointments` (52 fields) | Encounter content is comprehensive via PDFs but not machine-readable |
| Problems / conditions / diagnoses | ✅ Covered | C-CDA (Problems, Problem List, SDOH Problems); `Charges` has diagnosis codes; `Demographics` has default ICD codes; EMN PDFs contain encounter diagnoses | Multi-source coverage |
| Medications / prescriptions | ⚠️ Partial | C-CDA (Medications, Medications administered); EMN PDFs (current medications, prescriptions given) | Medications present but no dedicated structured prescription CSV. For practices with NewCropRx, e-prescribing data (Rx details, pharmacy routing, controlled substance tracking) appears to reside in the DrFirst/NewCrop integration, not in Nextech's database |
| Allergies | ✅ Covered | C-CDA (Allergies); `Demographics` (Allergy List field); EMN PDFs (allergy section with name, notes, dates) | Adequate |
| Immunizations | ✅ Covered | C-CDA (Immunizations) | Standard coverage via C-CDA |
| Vitals | ✅ Covered | C-CDA (Vital signs — partial); EMN PDFs (full vitals) | C-CDA has standard vitals; EMN PDFs have full detail but not machine-readable |
| Lab results | ✅ Covered | C-CDA (Lab orders, Lab results, Clinical Tests); `Notes` links to Lab ID/Lab Result ID | Standard coverage |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA (Diagnostic Imaging — added in 2025); clinical photos in Documents folder | Diagnostic imaging metadata in C-CDA; clinical photos exported as files. Specialty imaging data (e.g., ophthalmology device integrations like Topcon Harmony) may not be fully captured |
| Procedures | ✅ Covered | C-CDA (Procedures, SDOH Interventions); EMN PDFs; `Charges` (CPT codes) | Well-covered across multiple sources |
| Clinical notes / documents | ✅ Covered | EMN PDFs (full encounter notes); `Notes` CSV (23 fields); Documents folder (all attachments); `iPad Notes` (9 fields) | Comprehensive — encounter notes plus free-text notes from multiple system modules |
| Care plans / goals | ✅ Covered | C-CDA (Assessment and Plan of Treatment, Goals, SDOH Goals, SDOH Assessment, Health concerns) | Standard coverage via C-CDA |
| Orders / referrals | ⚠️ Partial | C-CDA (Reason for Referral, Referring Provider); `Appointments` has referring physician; `Demographics` has referring physician fields; `Recalls` tracks follow-up scheduling | Referral status/tracking is not explicitly exported as a separate entity. Lab orders are in C-CDA. No dedicated referral management export despite the product having referral letter generation features |
| Insurance / coverage | ✅ Covered | `Insurances` (85 fields) — primary/secondary subscriber details, copays, deductibles, company info, responsible party | Thorough |
| Claims / billing | ✅ Covered | `Charges` (140 fields) — CPT codes, diagnosis pointers, fees, adjustments, claim dates, prior auth, place of service | Exceptionally thorough — this is genuine claims/billing data |
| Payments | ✅ Covered | `Payments` (50 fields) — method, amounts, credit card details, insurance payments; `Payment Plans` (13 fields) | Well-covered |
| Consents / directives | ❌ Not covered | No consent or advance directive entities in CSV export. C-CDA does not list directives | Product likely manages consent preferences (portal access, communication preferences are in Demographics), but no dedicated consent tracking export |
| Patient communications / portal messages | ⚠️ Partial | `PracYakker` (10 fields) covers internal staff messaging about patients. Documents folder includes direct message attachments. `Notes` includes message threads (Thread ID, Status, Subject fields). | Internal messaging exported; patient portal messages not explicitly covered as a separate export |
| Specialty-specific (dermatology, ophthalmology, plastic surgery) | ⚠️ Partial | EMN PDFs capture specialty clinical data (customized per practice template) but in PDF format only, not structured | Specialty exam data (IOP readings, visual acuity, skin lesion mapping, surgical planning) is exported but not machine-readable. `Custom Data` (7 fields) exports practice-specific custom fields |

**Summary**: 12 of 18 domains are covered (✅), 4 are partially covered (⚠️), and 2 are not covered (❌ or N/A). The partial ratings for medications, imaging, referrals, and patient communications reflect real data that is present but either not fully structured or potentially incomplete due to third-party integration boundaries.

## 6. Documentation Quality

**Strengths:**
- **Field-level data dictionary**: 730 fields across 16 entities, each with a description (100% coverage). 84 fields have additional notes explaining values or behavior
- **Clear export structure documentation**: The 2025 PDF clearly explains ZIP folder structure, file naming conventions, data relationships, and edge cases (empty CSVs, deleted records, inactive patients)
- **Relationship documentation**: Key linking fields between entities are explicitly described (Bill ID, Payment Plan ID, Appointment ID, Recall Step ID)
- **Configuration-aware**: Documentation notes that practices with third-party PM systems or iPad configurations will see different export content
- **Publicly accessible**: All documentation available without login at the compliance hub

**Weaknesses:**
- **No data types**: Fields have names and descriptions but no explicit data types (string, integer, date, boolean, etc.)
- **No value sets**: Coded fields (Appointment Status, Payment Method, Note Category, etc.) are described but possible values are not enumerated. Only 3 entities have any fields with value hints in notes (e.g., "Possible values are 'Yes' 'No'" for Patient Deceased)
- **No sample data**: No sample export files or worked examples provided
- **No machine-readable schema**: No CSV header templates, no JSON schema, no XSD. The XLSX data dictionary is the only machine-readable artifact
- **EMN schema unknowable**: The EMN documentation explicitly states the 43 documented fields are "best practice" examples and "can differ" per practice configuration. A developer cannot predict EMN PDF content without seeing a specific practice's templates
- **No foreign key formalization**: Relationships are described in prose but not formally documented (no ERD, no foreign key annotations in the data dictionary)

**Developer usability**: A developer could understand the CSV export structure and build a basic import from this documentation. However, they would need sample data to determine data types, date formats, and coded value sets. The EMN PDFs would require OCR or manual review. The C-CDA portion follows HL7 standards and is self-documenting.

## 7. Overall Assessment

### Classification

**Partial native export**

This is a genuine (b)(10) effort — not a C-CDA or FHIR repackaging. The export uses the vendor's native data model for structured data (CSV files mapped to internal tables) supplemented by C-CDA for standardized clinical data and PDFs for encounter documentation. The billing/financial coverage is exceptionally deep (203 fields across Charges, Payments, Payment Plans), and demographics (212 fields) goes well beyond what any standard projection would include.

However, it falls short of "comprehensive native export" because:
1. Clinical encounter data (the richest clinical content for specialty practices) is only available as PDFs — not as structured, queryable data
2. E-prescribing data from the NewCropRx integration does not appear to have a dedicated structured export
3. No sample data is provided to validate the documentation
4. Several product features (CRM, inventory, telehealth metadata) have no corresponding export entities

### Key Findings

1. **Genuine billing/financial export is the standout strength.** The Charges entity (140 fields with CPT codes, 24 diagnosis code fields, fee breakdowns, insurance responsibility splits) plus Payments (50 fields) and Insurances (85 fields) represent real practice management data rarely seen in EHI exports. This alone distinguishes the export from vendors who repackage C-CDA or FHIR.

2. **730 fields across 16 entities, all with descriptions.** The data dictionary provides meaningful text descriptions for every field — not just field names. This is above-average documentation quality for EHI exports.

3. **Clinical encounter data is not machine-readable.** EMN PDFs capture the full specialty-specific encounter documentation but in a format that cannot be queried, imported, or processed without OCR. For specialty practices where the richest data lives in custom encounter templates (ophthalmology exams, dermatology assessments), this is a significant limitation.

4. **Multi-format approach is pragmatic.** The combination of CSV (structured tabular data), C-CDA (standardized clinical data), PDF (customized encounter notes), and native documents/images covers more ground than any single format would for a specialty EHR with highly configurable documentation.

5. **No sample data or data types.** The absence of sample exports and explicit data types means a developer cannot build a reliable import without trial and error. Value sets for coded fields are almost entirely undocumented.

### Summary Stats

    Classification:  Partial native export
    Export format:   CSV + C-CDA XML + PDF + native documents (per-patient ZIP)
    Model type:      Hybrid (native database tables as CSV + standard C-CDA + PDF encounters)
    Entities:        16
    Fields:          730
    Descriptions:    100% (730/730 fields have descriptions)
    Sample data:     No
    Bulk export:     No (single-patient only per documentation)
    Domains covered: 12 of 18 applicable domains (4 partial, 2 not covered)

### Bottom Line

Nextech has done genuine (b)(10) work that goes well beyond compliance theater. The export provides real billing data (140-field Charges entity with CPT codes and diagnosis pointers), comprehensive demographics (212 fields), and insurance detail (85 fields) — data that a C-CDA/FHIR repackaging would never include. The single biggest limitation is that specialty clinical encounter data — the core of what makes this a specialty EHR — is exported only as PDFs, not as structured data. A patient would get a substantially complete copy of their record, but a developer trying to import or analyze the clinical content would face significant challenges with the PDF encounter notes.

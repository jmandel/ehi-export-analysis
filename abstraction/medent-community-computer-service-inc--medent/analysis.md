# EHI Export Analysis: Community Computer Service, Inc. (MEDENT)

**Product**: medent v23.7
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.1840.MEDE.23.02.1.230918 (listing #11347)

## 1. Product Context

MEDENT is an integrated All-In-One ambulatory EHR, Practice Management, and Patient Engagement system developed by Community Computer Service, Inc. (Auburn, NY). It serves 11,000+ providers across 1,700+ client sites in 37 states, primarily independent practices, multi-specialty groups, and FQHCs across 30+ specialties.

**Data domains the product stores (baseline for completeness assessment):**
- **Clinical**: Chart Central dashboard with problem lists, allergies, medications, vitals, immunizations, lab results (260+ lab interfaces), clinical notes (voice, Dragon, point-and-click), procedures, care plans/goals, screenings/assessments, medical/surgical/social history
- **Billing/PM**: Scheduling, CPT/HCPCS fee schedules, claims, ERA processing, A/R, patient payments (RevSpring), e-statements, collections, MIPS/UDS reporting
- **Patient engagement**: Portal (messaging, scheduling, results, payments, proxy access, refill requests), telehealth/e-visits
- **Interoperability**: C-CDA exchange, Direct messaging, Community Chart (Carequality/CommonWell), FHIR API
- **Specialty**: Ophthalmology/optometry prescriptions, OB/GYN antepartum/delivery records, and templates for 30+ specialties
- **Documents**: Scanned documents, faxes, incoming external records
- **Public health**: Immunization registry, syndromic surveillance, cancer case reporting, eCR

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `EHI_Setup_and_File_Format_Specification.pdf` (3 pp) | Master document: export architecture (Setup/Create/Send/Control File), patient filters, format options, document/triage/todo handling | **High** — defines export mechanism |
| 31 field specification PDFs (1–12 pp each) | One per data domain; each lists field names, descriptions, and example output | **High** — primary data dictionary |
| `asciifieldlistinter.html` (370 KB) | MEDENT HTML manual page: 750 configurable financial/billing export fields across 17 data areas | **High** — covers financial export breadth |
| `enrichment/ehi-specs.json` (90 KB) | Prior agent's parsed extraction of all 33 PDFs: 648 fields total | **Medium** — useful starting point, verified against PDFs |
| `enrichment/ascii-field-list.json` (135 KB) | Prior agent's parsed extraction of all 750 ASCII fields | **Medium** — verified against HTML source |
| `enrichment/extraction-report.json` | Extraction coverage: 33/33 files parsed, 648 fields, 0 failures | **Low** — summary only |
| `screenshots/onc-page-ehi-section.png` | Screenshot of MEDENT ONC page showing 33 PDF download links | **Low** — confirms documentation availability |
| `screenshots/ascii-field-list-full.png` | Screenshot of ASCII Field List page | **Low** — confirms HTML source |

All 33 PDFs were verified as genuine PDF documents via `pdftotext`. Field counts were independently verified against the prior extraction (see `analysis/build_inventory.py`). The prior extraction was accurate for all specs except the Financial File Specification, which was garbled — the PDF actually contains 4 clearly defined header fields (practice_id, patient_id, MEDENT_id, Financial_id) plus a reference to the 750-field ASCII Field List.

## 3. Export Mechanics

- **Format**: Delimited text files (CSV or pipe-delimited, with or without quotes — user-configurable). Documents, triages, and todos are exported as HL7 C-CDA 2.1 Unstructured Documents containing Base64-encoded PDFs, zipped together.
- **Mechanism**: Built-in EHR feature accessed via **Medical Records > Data Export/Import/Connection Table > Electronic Health Information Export**. Four operational areas: Setup (configure population/data feeds), Create (generate export for date range), Send (queue for transmission), Control File (format/destination).
- **Single-patient vs bulk**: Supports both. Population can be narrowed to specific patients or filtered by provider, location, age, insurance, race, ethnicity, sex, status. Supports scheduled autorun for overnight batch processing.
- **Access constraints**: Requires security clearance for "Data Export/Import/Connection Table" and "Electronic Health Information Export." No mention of fees. Export can be sent to configured external destinations or downloaded to local PC.
- **ZIP compression**: Optional.
- **Filename format**: Configurable with create date, practice ID, process ID, date ranges.

This is a **purpose-built EHI export module** — clearly distinct from the FHIR API (g)(10) and C-CDA transitions of care (b)(1)–(b)(3).

## 4. Export Content: What's In It

### Data Dictionary Scope

The EHI export documentation consists of:
1. **31 data file specifications** (excluding 2 metadata documents) covering 651 fields total
2. **750 configurable financial/billing fields** in the ASCII Field List (referenced by the Financial File Specification)
3. **Combined total: 1,401 documented fields**

**Field documentation quality:**
- 650 of 651 EHI spec fields (99.8%) have descriptions — plain English explanations of what the field contains and where in MEDENT it comes from
- Every field specification includes example output showing realistic data formats
- Standard terminologies are referenced throughout: SNOMED CT, LOINC, RxNorm, CVX, NDC, CPT/HCPCS, ICD-10, UNII
- UUIDs serve as record identifiers
- Data types are not formally declared (no "string", "date", "integer"), but are inferable from examples
- Value sets are partially documented inline (e.g., verification_status: "Confirmed, Unconfirmed, Refuted"; patient_status: "Active, Inactive, Deceased, Transfer Care, Hospital")
- Foreign keys are implicit through shared field names (patient_mrn, MEDENT_id, encounter_id, provider_id, location_id, plan_id)

For the ASCII Field List: 178 of 750 fields (23.7%) have notes/descriptions. The remainder have descriptive names only.

### Vendor's own content organization

The export is organized as one file per data domain. Each row in the table below is a separate export file with its own specification PDF:

| Entity/File | Fields | Descriptions | Category |
|---|---|---|---|
| Patient File | 80 | 80 (100%) | Demographics |
| Eye/Contact Script File | 56 | 56 (100%) | Specialty - Ophthalmology/Optometry |
| Medication File | 43 | 43 (100%) | Medications / Prescriptions |
| Screenings and Assessments File | 43 | 43 (100%) | Screenings / Assessments |
| Result File | 39 | 39 (100%) | Lab Results |
| Order File | 31 | 31 (100%) | Orders |
| Procedures File | 30 | 30 (100%) | Procedures |
| Immunization File | 29 | 29 (100%) | Immunizations |
| Referral File | 26 | 26 (100%) | Referrals |
| Allergy File | 21 | 21 (100%) | Allergies |
| HIPAA File | 21 | 21 (100%) | Consents / Communication Preferences |
| Goals File | 19 | 19 (100%) | Care Plans / Goals |
| Provider File | 18 | 18 (100%) | Reference Data |
| Appointment File | 15 | 15 (100%) | Encounters / Visits |
| Vital File | 15 | 15 (100%) | Vitals |
| ProblemList File | 14 | 14 (100%) | Problems / Conditions |
| Encounter File | 14 | 14 (100%) | Encounters / Visits |
| Diagnosis File | 13 | 13 (100%) | Diagnoses |
| Exchanged Patient Level Files | 13 | 13 (100%) | Data Exchange Records |
| Progress Note Listing File | 13 | 13 (100%) | Clinical Notes / Documents |
| Document Listing File | 12 | 12 (100%) | Clinical Notes / Documents |
| OBEpisode File | 12 | 12 (100%) | Specialty - OB/GYN |
| OBOutcome File | 11 | 11 (100%) | Specialty - OB/GYN |
| Location File | 9 | 9 (100%) | Reference Data |
| MedicalHistory File | 9 | 9 (100%) | Medical History |
| SocialHistory File | 9 | 9 (100%) | Social History |
| SurgicalHistory File | 9 | 9 (100%) | Surgical History |
| PatientPlan File | 9 | 9 (100%) | Insurance / Coverage |
| CareTeam and Resources File | 8 | 8 (100%) | Care Team |
| InsurancePlan File | 6 | 6 (100%) | Insurance / Coverage |
| Financial File | 4 + 750 configurable | 4 (100%) + 178 notes | Claims / Billing |

Additionally, the **ASCII Field List** provides 750 configurable fields for financial export, organized into 17 data areas:

| Area | Code | Fields | Description |
|---|---|---|---|
| Patient data | P | 260 | Patient demographics (overlaps with Patient File) |
| History/Activity | HA | 143 | Financial transaction data (charges, payments, adjustments) |
| Primary Patient | PP | 55 | Primary/guarantor patient data |
| Referral | R | 42 | Referral tracking fields |
| Surgical Booking | SB | 40 | Surgical scheduling/booking |
| Referring Doctor | RD | 39 | Referring provider demographics |
| Appointment/Scheduling | OA | 34 | Scheduling data |
| Lab data | L | 29 | Lab order/result fields |
| Orders | O | 25 | General order fields |
| Diagnostic Imaging | DI | 25 | DI order fields |
| Immunization | I | 19 | Immunization detail fields |
| Activity (charges) | A | 18 | Charge-level financial data |
| Recall | RC | 7 | Patient recall/reminder data |
| Immunization CPT | CC | 6 | CPT codes for immunizations |
| Practice Information | PI | 6 | Practice-level reference data |
| History record | H | 1 | History pointer |

The Financial File Specification explicitly states that "The setup should only include fields from History and Activity (HA) in the ASCII Field List" — meaning the 143 HA fields plus the 18 A fields (161 total) are the primary financial export content, alongside the 4 header fields.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

MEDENT's EHI export covers an unusually broad set of clinical and administrative domains through 31 dedicated data files. Key strengths:

- **Demographics** (Patient File, 80 fields): Exceptionally thorough — includes SDOH fields (homelessness, migrant status, veteran status), gender identity, sexual orientation, pronouns, education level, employment, income, birth location/time, multiple birth, provider-by-location, portal status, advance directive indicator, and previous addresses.

- **Clinical data**: 12 dedicated files covering allergies (21 fields with coded reactions/severity), medications (43 fields with NDC/RxNorm/SIG/refills/administration), problems (14 fields with SNOMED), diagnoses (13 fields with ICD codes), vitals (15 fields with LOINC), results (39 fields with reference ranges), orders (31 fields), procedures (30 fields with CPT/SNOMED/body site/complications), medical/surgical/social history (9 fields each), and immunizations (29 fields with CVX/lot/manufacturer/VIS).

- **Screenings and Assessments** (43 fields, 12-page spec): Notably detailed — covers tobacco use, alcohol screening (AUDIT, AUDIT-C, CAGE, SBIRT), depression (PHQ-2/9, Edinburgh), anxiety (GAD-7), fall risk, SDOH, substance abuse (DAST), developmental screening (ASQ-3, M-CHAT-R), and many more. Includes a comprehensive mapping table showing which document codes, component names, SNOMED/LOINC codes, and assessment ID prefixes correspond to each screening type.

- **Financial/Billing** (4 header fields + up to 750 configurable ASCII fields): The financial export delegates to MEDENT's pre-existing Data Export Module, which provides 143 History/Activity fields covering charges, payments, adjustments, denial codes, diagnosis codes, insurance info, and 18 Activity fields for charge-level detail. This is genuinely deep financial data — not a token inclusion.

- **Specialty data**: Ophthalmology/optometry prescriptions (56 fields with keratometry, sphere, cylinder, axis, prism, add power, DVA/NVA for both eyes); OB/GYN antepartum records (12 fields with EDD, gestational age, risk factors) and delivery outcomes (11 fields with birthweight, delivery type, multiple birth support). These specialty data types would never appear in a standard FHIR or C-CDA export.

- **Documents and Notes**: Document metadata (12 fields with LOINC codes) and progress note metadata (13 fields with signature status) are exported as structured data. The actual document/note content is exported as C-CDA 2.1 Unstructured Documents wrapping Base64-encoded PDFs — preserving original formatting while providing interoperable metadata.

- **Care coordination**: Referrals (26 fields with comprehensive date tracking), care team/community resources (8 fields), goals (19 fields with short-term/long-term tracking and status), and data exchange records (13 fields tracking disclosures).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient File (80 fields), SocialHistory File (9 fields) | Exceptionally thorough; includes SDOH, gender identity, pronouns, education, income |
| Encounters / visits | ✅ Covered | Encounter File (14 fields, E-Superbill based), Appointment File (15 fields) | Solid; encounters linked via encounter_id across files |
| Problems / conditions / diagnoses | ✅ Covered | ProblemList File (14 fields), Diagnosis File (13 fields), MedicalHistory File (9 fields) | Complete; problem list + encounter-level diagnoses + past medical history |
| Medications / prescriptions | ✅ Covered | Medication File (43 fields) | Deep; includes NDC, RxNorm, SIG, refills, D/C reason, DEA schedule, administration records, pharmacy sent |
| Allergies | ✅ Covered | Allergy File (21 fields) | Thorough; SNOMED, RxNorm, UNII codes; reactions, severity, criticality, verification status |
| Immunizations | ✅ Covered | Immunization File (29 fields) | Complete; CVX, CPT, lot numbers, manufacturer, diluent, VIS dates, route, site |
| Vitals | ✅ Covered | Vital File (15 fields) | Good; includes LOINC codes, remote monitoring flag, units |
| Lab results | ✅ Covered | Result File (39 fields) | Thorough; LOINC, reference ranges, high/low flags, priority, status, multiple dates, accession ID |
| Imaging / diagnostic reports | ⚠️ Partial | Order File includes DI orders (type="Diagnostic Image"); ASCII DI area (25 fields) | Orders are covered but no dedicated imaging result/report file beyond the document export |
| Procedures | ✅ Covered | Procedures File (30 fields), SurgicalHistory File (9 fields) | CPT, SNOMED, modifiers, body site, status, outcome, complications, notes |
| Clinical notes / documents | ✅ Covered | Progress Note Listing (13 fields metadata), Document Listing (12 fields metadata), actual content as C-CDA wrapped PDFs | Metadata is structured; full content preserved as PDF |
| Care plans / goals | ✅ Covered | Goals File (19 fields), CareTeam File (8 fields) | Short-term and long-term goals with status tracking |
| Orders / referrals | ✅ Covered | Order File (31 fields), Referral File (26 fields) | Lab, DI, and general orders; referrals with comprehensive date tracking |
| Insurance / coverage | ✅ Covered | PatientPlan File (9 fields), InsurancePlan File (6 fields) | Policy numbers, effective/expired dates, billing order, payer ID, plan type |
| Claims / billing | ✅ Covered | Financial File (4 header + configurable ASCII fields), HA area (143 fields), A area (18 fields) | Genuine financial data: charges, payments, adjustments, denial codes, insurance co detail |
| Payments | ✅ Covered | Included in Financial File ASCII fields (HA area includes payment-related fields) | Covered within financial export |
| Consents / directives | ✅ Covered | HIPAA File (21 fields), advance_directive_ind in Patient File | Communication preferences (appointment/medical info by channel), consent status, signature |
| Patient communications / portal messages | ⚠️ Partial | Exchanged Patient Level Files (13 fields) tracks data disclosures; triages exported as C-CDA PDFs | Triages (which include messages) are exported but as unstructured PDFs, not structured data. Portal message content is not explicitly specified. |
| Specialty - Ophthalmology/Optometry | ✅ Covered | Eye/Contact Script File (56 fields) | Keratometry, sphere, cylinder, axis, prism, add power, DVA/NVA for both eyes |
| Specialty - OB/GYN | ✅ Covered | OBEpisode File (12 fields), OBOutcome File (11 fields) | Antepartum records, delivery outcomes, multiple birth support |
| Screenings / assessments | ✅ Covered | Screening and Assessment File (43 fields, 12-page spec) | Extensive: tobacco, alcohol, depression, anxiety, fall risk, SDOH, developmental, and many more |

**Summary**: 17 of 19 applicable domains are fully covered. 2 domains (imaging reports, patient portal messages) are partially covered. No domains are entirely missing. The partial gaps are minor: imaging orders exist but dedicated imaging results are handled through the document export; portal messages/triages are exported as PDFs rather than structured data.

## 6. Documentation Quality

**Strengths:**
- Every data file has its own PDF specification with field names, descriptions, and example output — a consistent, well-structured data dictionary
- Field descriptions reference specific MEDENT UI screens and data sources (e.g., "Provider number from the Patient info for the RDr field. Provider ID begins with an R to indicate data is from the referring dr master files"), making the mapping traceable
- Standard code systems (SNOMED, LOINC, RxNorm, CVX, NDC, CPT, ICD-10, UNII) are explicitly identified for coded fields
- The Screening and Assessment specification (12 pages) includes a detailed mapping table of 40+ assessment types to document codes, component names, and SNOMED/LOINC codes
- The master Setup document (3 pages) provides clear workflow instructions with navigation paths
- The Info File provides export metadata including criteria used and record counts per file — enabling audit/verification

**Weaknesses:**
- **No formal schema files** (no XSD, JSON Schema, or DDL) — specs are only in PDF format
- **Data types not formally declared** — there is no "varchar(50)", "date", "integer" specification, though types are inferable from example output
- **Value sets not systematically enumerated** — some are documented inline (e.g., appointment status, verification status) but most are not
- **Cardinality not specified** — no indication of required vs. optional fields
- **Relationships are implicit** — shared field names (patient_mrn, encounter_id, provider_id, location_id) imply foreign keys but no ERD or formal relationship documentation exists
- **No sample export data** provided — only example output values within the specifications
- **Financial export documentation is indirect** — requires navigating to a separate HTML manual page for the 750-field ASCII Field List

**Could a developer build an import?** Yes, with moderate effort. The field specs are clear enough to map data. The lack of formal schemas, explicit data types, and enumerated value sets would require some trial-and-error, but the descriptions and examples provide sufficient context to work from.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a purpose-built EHI export system that exports MEDENT's native data model across clinical, billing, and specialty domains. It is not a repurposed FHIR API or C-CDA export — it has its own dedicated module, its own documentation corpus, and its own configurable export pipeline.

### Key Findings

1. **Genuinely comprehensive scope**: 31 data files covering 651 structured fields plus 750 configurable financial fields (1,401 total) — spanning demographics, clinical, billing, specialty (ophthalmology, OB/GYN), screenings/assessments, care coordination, insurance, and consents. This is one of the broadest (b)(10) implementations reviewed.

2. **Purpose-built, not repurposed**: The EHI export is a dedicated module (Medical Records > Data Export/Import > Electronic Health Information Export) with its own Setup/Create/Send/Control File workflow. It is explicitly separate from the FHIR API and C-CDA transitions of care. Documents/triages/todos are handled via C-CDA 2.1 Unstructured Documents wrapping PDFs — a pragmatic hybrid approach.

3. **Near-complete field documentation**: 99.8% of EHI spec fields have descriptions (650 of 651). Every spec includes example output. Standard terminologies are systematically referenced. This is well above average documentation quality.

4. **Specialty clinical data included**: The Eye/Contact Script File (56 fields for ophthalmology/optometry) and OBEpisode/OBOutcome Files (23 fields for OB/GYN) demonstrate genuine (b)(10) thinking — exporting specialty data that would never appear in USCDI or FHIR US Core.

5. **Minor gaps**: Patient portal messages and triages are exported as unstructured PDFs rather than structured data. The financial export documentation requires navigating to a separate HTML manual page. No formal schema files, no sample data files, and no ERD are provided.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV/pipe-delimited text + C-CDA 2.1 Unstructured Documents (PDFs)
Model type:      Native database model
Entities:        31 data files (+ 2 metadata)
Fields:          651 (EHI specs) + 750 (ASCII financial fields) = 1,401 total
Descriptions:    99.8% of EHI spec fields; 23.7% of ASCII fields have notes
Sample data:     No (example values in specs only)
Bulk export:     Yes (scheduled autorun, population filters, date ranges)
Domains covered: 17 of 19 fully, 2 partially
```

### Bottom Line

MEDENT's EHI export is one of the stronger (b)(10) implementations: a purpose-built export module with 31 data files, 1,401 documented fields, and coverage across clinical, billing, specialty, and administrative domains. A patient or provider would get a genuinely comprehensive copy of their data. The biggest gap is minor — portal messages/triages are exported as PDFs rather than structured data — and the documentation, while thorough in descriptions, lacks formal schemas and sample data files.

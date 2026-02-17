# EHI Export Analysis: Veradigm

**Product**: Veradigm EHR (version 26)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2891.Vera.26.14.1.251231 (CHPL 11763)

## 1. Product Context

Veradigm EHR (formerly Allscripts Professional EHR) is a full-featured ambulatory EHR for small-to-mid-size independent physician practices and multi-specialty organizations. It is the flagship clinical product of Veradigm Inc. (formerly Allscripts Healthcare Solutions), with ~180,000 physician users and approximately 3.6% of the U.S. ambulatory EHR market.

The product ecosystem includes several separately sold but integrated products:

- **Veradigm EHR** — the ONC-certified clinical EHR (the subject of this analysis, CHPL 11763)
- **Veradigm Practice Management** — billing, claims, scheduling (separately sold, non-ONC-certified)
- **Veradigm ePrescribe** — standalone electronic prescribing (also available as a module within the EHR)
- **FollowMyHealth** — patient portal and personal health record (separately ONC-certified)
- **Veradigm View** — rebranded Practice Fusion EHR, a simpler cloud-native EHR for small practices

**What the product stores (relevant to export completeness):**
- Full clinical documentation including one-click templates, specialty-specific protocols, ambient AI-generated notes
- ePrescribing with EPCS, PDMP integration, prior authorization (eAUTH), medication pricing
- Lab and imaging orders/results via the DORN network (500+ labs/radiology centers)
- Clinical decision support, HCC alerts, risk scores
- Immunization records and public health reporting data
- Care plans, goals, health concerns, questionnaires
- Patient communications and secure messaging
- Scanned documents, transcriptions, chart attachments
- Billing/claims data (via Practice Management), insurance, superbills
- Patient portal data (via FollowMyHealth) including patient-entered data, appointment scheduling, billing

The ONC certification spans 40+ criteria including clinical (a)(1)-(a)(15), care coordination (b)(1)-(b)(11), quality measures (c)(1)-(c)(3), public health reporting (f)(1)-(f)(7), and FHIR APIs (g)(10).

## 2. Artifacts Reviewed

Veradigm publishes EHI export documentation for **five separate products** from a single compliance page at `veradigm.com/legal/onc-reg-compliance/`. All artifacts were publicly accessible.

| # | Artifact | Size | Description | Informative |
|---|---------|------|-------------|-------------|
| 1 | `VeradigmEHR_EHI_Export_output_format_documentation_v1.pdf` | 89 pages, 761 KB | **Core EHR data dictionary** — 51 database tables across 15 clinical domains, 997 fields with names, descriptions, and SQL types. Published Nov 9, 2023. | **Highest** |
| 2 | `veradigm-view-v6/*.html` (88 files) | ~20 MB total | **Veradigm View (Practice Fusion) data dictionary** — 87 TSV entity definitions, 1,194 fields. Version 6, published Jan 12, 2026. Most recently updated documentation. | **High** |
| 3 | `EHIDataExportFile_ReferenceGuide_VeradigmPM_V2.pdf` | 20 pages, 324 KB | **Practice Management billing export** — hierarchical JSON schema for voucher/claims data with 75 core fields plus appendices listing 317 additional claim, ailment, ambulance, drug, anesthesia, and dental fields. Published May 7, 2024. | **High** |
| 4 | `VeradigmePrescribe_EHI_Export_Documentation_v1.pdf` | 22 pages, 684 KB | **ePrescribe export** — 6 TSV files (Allergies, Demographics, Diagnosis, Historical Medications, Insurance, Prescriptions) with 263 fields. Published Nov 27, 2023. | **Medium** |
| 5 | `VeradigmFMH_EHI_Export_Data_Guide_v2.pdf` | 20 pages, 539 KB | **FollowMyHealth export** — FHIR R4 Bundle with 18 resource types, custom extensions, not US Core/Bulk Data. Published Feb 28, 2024. | **Medium** |
| 6 | `fmh-fhir-extensions/*.json` (9 files) | ~8 KB total | **FMH FHIR extension definitions** — 3 StructureDefinitions, 3 CodeSystems, 3 ValueSets for allergy status, procedure status, and health condition status. | **Low** |
| 7 | `EHIDataExportFile_ReferenceGuide_VeradigmPM.pdf` | 17 pages, 467 KB | PM export v1 (Dec 2023) — superseded by v2 above. | **Low** |
| 8 | `VeradigmFMH_EHI_Export_Data_Guide_v1.pdf` | 18 pages, 530 KB | FMH export v1 (Nov 2023) — superseded by v2 above. | **Low** |

## 3. Export Mechanics

Veradigm provides separate export mechanisms for each product component:

**Veradigm EHR (core clinical data):**
- **Format**: JSON files organized in clinical domain folders, plus raw attachments/documents/transcriptions
- **Packaging**: Password-protected ZIP containing per-patient sub-ZIPs
- **Mechanism**: EHI Export tool within the EHR application (UI-driven)
- **Scope**: Single-patient or multi-patient export
- **Access**: Practice initiates export; patient receives ZIP + password

**Veradigm Practice Management (billing data):**
- **Format**: Hierarchical JSON (single file per patient)
- **Mechanism**: Not explicitly documented; described as "EHI data export file"
- **Scope**: Per-patient financial/billing data
- **Note**: PM is "non ONC certified" per the compliance page but provides separate EHI documentation

**Veradigm ePrescribe (prescribing data):**
- **Format**: TSV files in ZIP
- **Mechanism**: Health Information Export tool within ePrescribe
- **Scope**: Per-patient; supports single or multi-patient selection

**FollowMyHealth (patient portal data):**
- **Format**: FHIR R4 Bundle in JSON + raw documents/images in ZIP
- **Mechanism**: Export from FMH Dashboard (by practice) or by patient from their PHR account
- **Scope**: Per-patient; practice-initiated exports limited to data from that practice's EHR; patient-initiated exports include all sources
- **Note**: Explicitly states "This is not an implementation of SMART/HL7 Bulk Data Access (Flat FHIR)"

**Veradigm View / Practice Fusion (separate EHR):**
- **Format**: TSV files
- **Mechanism**: Not documented in the artifacts reviewed
- **Scope**: 87 entity types across demographics, clinical, labs, billing, messaging, administrative domains

**Bulk export capability**: Not explicitly documented as a single "bulk export all patients" mechanism. The EHR export supports multi-patient selection. No mention of fees or access constraints.

## 4. Export Content: What's In It

### Combined scope across all products

Across all five products, the Veradigm suite documents **169 entities** with **2,938 total fields**. Documentation quality is exceptional: 99.9% of fields have descriptions and 100% have data types.

### 4a. Veradigm EHR (the certified product)

The EHR export produces 51 JSON files organized into 15 clinical domains, mapping directly to named database tables with primary keys. Total: **997 fields**, all with descriptions and SQL data types.

| Category | Entities | Fields | Key tables |
|----------|----------|--------|-----------|
| Demographics | 4 | 124 | DEMOGRAPHICS (81 fields), PATIENT_CONSENT (6), PATIENT_CONTACTS (21), PATIENT_PHYSICIANS (16) |
| History | 3 | 87 | HX_DIAGNOSIS (29), HX_IMPLANTABLE_DEVICE (27), HX_MEDICATION (31) |
| Vitals | 1 | 50 | VITALS_DATA (50) — exceptionally detailed including pre-pregnancy weight, electronically-acquired flags, LMP |
| Diagnosis | 1 | 35 | DX (35) — includes SNOMED, ICD-10, severity, acuity, stability, intensity, barrier flags |
| Medications | 3 | 100 | MEDICATIONS (58), MEDADMIN_RECORD (34), HTML_DOCUMENT (8 — Rx output summary) |
| Procedures | 2 | 58 | PROCEDURES (30), PROCEDURE_RESULT (28) |
| Lab Orders | 2 | 51 | LABORDERS (22), LAB_RESULT (29) |
| Referrals | 1 | 43 | REFERRALS (43) — comprehensive with authorization numbers, insurance info |
| Flowsheet | 2 | 30 | FLOWSHEET_DEFINITION (10), PATIENT_RISK_SCORE (20) |
| Contact | 3 | 30 | CONTACTCHUNKS (9), CONTACT (10), CONTACT_DATA (11) |
| Encounter | 7 | 94 | ENCOUNTER (38), ENCOUNTER_ASSESSMENT (8), ENCOUNTER_PLAN (9), CHART_ADDENDUM (7), HpiData (17), HpiDataNotes (7), ENCOUNTER_ACCOMPANIEDBY (8) |
| Immunization | 4 | 59 | IMMUNIZATION_RECORD (37), IMMUNIZATION_RECORD_VIS (4), IMMUNIZATIONS_FORECAST (8), IMMREC_ADDENDUM (10) |
| Message | 3 | 72 | MESSAGE_SAVED (45), WEBMESSAGE_SAVED (20), MESSAGE_RESULT_SAVED (7) |
| Questionnaire | 3 | 18 | QNS_RECORD (8), QNS_RECORD_RESULT (6), QNS_RECORD_QUES_ANS (4) |
| Care Plans | 8 | 102 | CP_PATIENT_CAREPLAN (8), CP_PATIENT_HC_DETAILS (14), PATIENT_GOAL (18), PATIENT_ACHIEVE_GOAL (11), PATIENT_GOAL_BARRIER (5), PATIENT_GOAL_PLAN (13), PATIENT_GOAL_PLAN_BARRIER (5), PATIENT_CAREPLAN_ENCOUNTER (5) |
| Additional Files | 4 | 67 | NOTES_RAWDATA (5), SCAN_DOCUMENT (21), TRANSCRIPTION (24), CHARTATTACHMENT (17) |

The export also includes the actual binary files (images, scanned documents, transcriptions) in separate folders, not just metadata references.

### 4b. Veradigm Practice Management

The PM export documents a hierarchical JSON structure for patient billing/financial data with **75 core fields** covering:
- Practice and patient identification
- Voucher-level billing data (charges, payments, adjustments, balances)
- Provider, referring provider, responsible party, billing provider details
- Service-level details (procedure codes, descriptions, units, fees, modifiers, diagnoses)
- Payment transactions (date, insurance, transaction type, amount, transfers)

Plus **317 appendix fields** covering possible values for:
- **Claim information** (218 fields): prior authorization, condition codes 1-7, occurrence codes 1-8, value codes 1-12, diagnosis codes, procedure codes, employer info, scan regions, outgoing referrals, EPSDT fields, and more
- **Ailment information** (51 fields): case type, disability dates, hospitalization dates, pregnancy-related, EPSDT referral codes
- **Ambulance information** (21 fields): transport codes, pick-up addresses, stretcher/emergency indicators
- **Drug information** (13 fields): NDC codes, lot numbers, unit pricing, lab results
- **Anesthesia information** (12 fields): start/stop times, base units, CRNA details, related procedures
- **Dental information** (2 fields): tooth/quadrant, surface

### 4c. Veradigm ePrescribe

The ePrescribe export documents 6 TSV files with **263 fields** total:
- **Demographics.tsv** (46 fields): patient info, pharmacy preferences (retail, mail order, other), clinical flags
- **Allergies.tsv** (12 fields): medication and medication class allergies with RxNorm codes
- **Diagnosis.tsv** (9 fields): ICD-9, ICD-10, SNOMED codes
- **Historical Medications.tsv** (78 fields): comprehensive prescription details with drug checking flags, PBM card info, pharmacy details, provider credentials
- **Insurance.tsv** (40 fields): PBM data, card holder information, formulary IDs, coverage details
- **Prescriptions.tsv** (78 fields): active prescriptions with same level of detail as historical

### 4d. FollowMyHealth

The FMH export uses **18 FHIR R4 resource types** with custom extensions (explicitly not US Core or Bulk Data):

| Resource | Category | FMH PHR Location |
|----------|----------|-----------------|
| Account | Billing | Billing section |
| AllergyIntolerance | Clinical | My Health > Allergies |
| Appointment | Administrative | Appointments widget |
| Bundle | Infrastructure | Container |
| Communication | Messaging | Messages |
| Condition | Clinical | Health Conditions |
| DiagnosticReport | Clinical | Results |
| DocumentReference | Documents | Documents (scanned, CCDAs, forms) |
| Encounter | Clinical | Not visible in PHR |
| FamilyMemberHistory | Clinical | Family Health Conditions |
| Immunization | Clinical | Immunizations |
| Invoice | Billing | Billing section |
| Medication | Clinical | Medications |
| MedicationRequest | Clinical | Medications |
| Observation | Clinical | Results, Vitals, Wellness Measurements |
| Patient | Demographics | Patient demographics |
| Practitioner | Administrative | Connections |
| Procedure | Clinical | Surgical History |

Notable: FMH includes **Account** and **Invoice** FHIR resources for billing data, plus **Communication** for secure messaging. Uses 3 custom extensions (AllergyStatus, ProcedureStatus, HealthConditionStatus) to handle FMH-specific status values not representable in standard FHIR.

### 4e. Veradigm View (Practice Fusion)

The most extensively documented product with **87 TSV entities** and **1,194 fields** across 8 categories:

| Category | Entities | Fields |
|----------|----------|--------|
| Clinical | 32 | 376 |
| Billing and insurance | 12 | 286 |
| Labs | 15 | 187 |
| Demographics | 10 | 143 |
| Medications and prescriptions | 11 | 124 |
| Messaging | 3 | 27 |
| Patient | 2 | 27 |
| Referrals | 2 | 24 |

The View documentation is the most recently updated (v6, Jan 12, 2026 — 6 versions in ~9 months) and the most comprehensive in entity count. It is a separate product from Veradigm EHR (Practice Fusion rebranded), but its inclusion on the same compliance page reflects the integrated suite approach.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Veradigm EHR** covers the core clinical data comprehensively:
- **Demographics** (124 fields across 4 tables): exceptionally detailed including multiple name variants (preferred, former, birth), multiple sex/gender fields (birth sex, medical sex, administrative sex, gender identity, sexual orientation, preferred pronouns), organ donor status, employment, VIP indicator, confidentiality codes.
- **Medications** (100 fields across 3 tables): active prescriptions with 58 fields including local vs. mail-order pharmacy details, sample drug tracking, MAR records with injection sites and lot numbers.
- **Encounter** (94 fields across 7 tables): encounters, assessments, plans, HPI data, addenda, accompanied-by records.
- **History** (87 fields across 3 tables): historical diagnoses, historical medications, implantable devices with UDI/DI codes.
- **Messages** (72 fields across 3 tables): saved messages, web messages, and message results.
- **Immunization** (59 fields across 4 tables): immunization records, VIS editions, forecast, and addenda.
- **Additional Files** (67 fields across 4 tables plus actual files): scanned documents, transcriptions, chart attachments with metadata.

**Practice Management** adds deep billing coverage:
- 75 core fields covering the full voucher-to-payment lifecycle
- 218 claim information fields covering institutional, professional, and specialty billing
- Specialty appendices for ambulance, anesthesia, dental, and drug billing

**Combined across the suite**, the strongest areas are:
1. **Billing/insurance** — PM provides extensive claim-level detail; View has 12 billing entities with 286 fields; ePrescribe adds 40 insurance fields
2. **Medications/prescriptions** — Three products cover active prescriptions, historical medications, administered medications, and prescription transactions
3. **Demographics** — All products include patient demographics at varying depths
4. **Clinical notes/documents** — EHR exports actual files (images, scanned docs, transcriptions, voice notes) plus metadata

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|--------|----------|----------------|-------------|
| Demographics | ✅ Covered | EHR: DEMOGRAPHICS (81 fields), PATIENT_CONTACTS (21), PATIENT_PHYSICIANS (16); ePrescribe: Demographics.tsv (46); View: 10 entities (143 fields) | Exceptionally thorough — includes sex/gender identity, birth details, employment, multiple name variants |
| Encounters / visits | ✅ Covered | EHR: ENCOUNTER (38), ENCOUNTER_ASSESSMENT (8), ENCOUNTER_PLAN (9), HpiData (17), CHART_ADDENDUM (7), ENCOUNTER_ACCOMPANIEDBY (8); View: patient-encounters, encounter-related entities | Solid coverage with assessment plans, HPI, addenda |
| Problems / conditions / diagnoses | ✅ Covered | EHR: DX (35), HX_DIAGNOSIS (29); ePrescribe: Diagnosis.tsv (9); View: patient-diagnoses, patient-conditions | Active and historical; ICD-10, SNOMED; severity/acuity/stability/intensity |
| Medications / prescriptions | ✅ Covered | EHR: MEDICATIONS (58), HX_MEDICATION (31), MEDADMIN_RECORD (34), HTML_DOCUMENT (8); ePrescribe: Historical Medications (78), Prescriptions (78); View: 11 entities (124 fields) | Deep coverage including MAR, prescription output history, drug checking flags |
| Allergies | ✅ Covered | EHR: HX_DIAGNOSIS contains allergy data; ePrescribe: Allergies.tsv (12); View: patient-allergy, patient-allergy-reactions | Present across multiple products |
| Immunizations | ✅ Covered | EHR: IMMUNIZATION_RECORD (37), IMMUNIZATION_RECORD_VIS (4), IMMUNIZATIONS_FORECAST (8), IMMREC_ADDENDUM (10); View: patient-immunizations, immunization-vis-editions, etc. | Excellent — includes VIS editions, forecast, addenda |
| Vitals | ✅ Covered | EHR: VITALS_DATA (50 fields); View: patient encounters with observations | Exceptionally detailed — 50 fields with electronic acquisition flags, pre-pregnancy weight, LMP |
| Lab results | ✅ Covered | EHR: LABORDERS (22), LAB_RESULT (29); View: 15 lab entities (187 fields) | Solid; View is especially deep with separate entities for order items, specimens, result notes |
| Imaging / diagnostic reports | ⚠️ Partial | EHR: Attachments folder includes images; ProceduresResult (28 fields) may contain imaging results; View: patient-documents | No dedicated radiology/DICOM entities; imaging data likely comes through as attachments or procedure results |
| Procedures | ✅ Covered | EHR: PROCEDURES (30), PROCEDURE_RESULT (28); View: patient-encounter-procedures | Includes procedure results with specimen and result details |
| Clinical notes / documents | ✅ Covered | EHR: Transcriptions folder (RTF), CHART_ADDENDUM, CONTACTCHUNKS, NOTES_RAWDATA, SCAN_DOCUMENT, CHARTATTACHMENT + actual binary files; View: patient-documents, patient-encounter-documents | Comprehensive — actual files exported, not just metadata |
| Care plans / goals | ✅ Covered | EHR: 8 care plan entities (102 fields) — care plans, health concerns, goals, goal barriers, goal plans; View: patient-goals, patient-health-concerns | Deep care plan model with barriers and goal plans |
| Orders / referrals | ✅ Covered | EHR: REFERRALS (43 fields) with authorization and insurance info; View: patient-referrals, patient-referral-recipients | Referrals well-covered; lab orders covered under Labs |
| Insurance / coverage | ✅ Covered | ePrescribe: Insurance.tsv (40 fields) with PBM details, formulary IDs; View: patient-insurances (65 fields), patient-insurance-eligibilities; PM: claim-level payer information | Strong — includes PBM data, formulary info, eligibility |
| Claims / billing | ✅ Covered | PM: 392 fields covering vouchers, charges, payments, adjustments, claim information, specialty billing; View: patient-superbills (70 fields), superbill-procedures, superbill-diagnoses, superbill-insurances, superbill-events | **Notably comprehensive** — dedicated PM export with extensive claim field appendices |
| Payments | ✅ Covered | PM: payment transactions within voucher structure (payment date, insurance, transaction type, amount, transfers) | Covered within the PM billing export |
| Consents / directives | ✅ Covered | EHR: PATIENT_CONSENT (6 fields); View: patient-advance-directives | Consent types, answers, expiration dates; advance directives |
| Patient communications / portal messages | ✅ Covered | EHR: MESSAGE_SAVED (45), WEBMESSAGE_SAVED (20), MESSAGE_RESULT_SAVED (7); FMH: Communication resource; View: patient-messages (3 entities, 27 fields) | Strong — includes web messages, secure messages, message attachments |
| Questionnaires / custom forms | ✅ Covered | EHR: QNS_RECORD (8), QNS_RECORD_RESULT (6), QNS_RECORD_QUES_ANS (4); View: patient-questionnaire | Question-answer level detail; flowsheet definitions for custom worksheets |
| Risk scores | ✅ Covered | EHR: PATIENT_RISK_SCORE (20 fields); View: patient-risk-scores | HCC/RAF risk score tracking |
| Family history | ✅ Covered | FMH: FamilyMemberHistory; View: patient-family-medical-history, patient-family-history-diagnoses | Present in portal and View exports |
| Specialty-specific data | ⚠️ Partial | EHR: FlowsheetDefinitions captures custom worksheets; PM: dental, ambulance, anesthesia appendices | Generic container (flowsheets/questionnaires) rather than specialty-specific entities. PM appendices do cover specialty billing (dental, anesthesia) |

### Coverage gaps

**Minimal gaps relative to what the product stores:**

1. **Specialty clinical data**: The EHR supports "nearly every medical specialty" with preloaded templates, but the export uses generic containers (FlowsheetDefinitions, QuestionnaireRecords) rather than specialty-specific entities. The data should still be exported, but without specialty-specific documentation, it's hard to verify coverage.

2. **Prior authorization records**: The ePrescribe product has eAUTH for electronic prior authorization, but no dedicated prior authorization entity appears in the EHR export. The PM export includes "Prior Authorization Number" as a claim field.

3. **Structured imaging data**: No dedicated radiology or DICOM entities. Imaging data appears to come through as attachments and procedure results.

4. **Patient-generated data from FollowMyHealth**: Remote monitoring device data is mentioned in product features but not specifically documented as an exported data type beyond FMH's Observation resource.

These are relatively minor gaps for an ambulatory EHR. The core clinical, billing, messaging, and document data are well-covered.

## 6. Documentation Quality

**Strengths:**
- **Field-level documentation is excellent**: 99.9% of fields across all products have human-readable descriptions (2,935 of 2,938 fields). 100% have data types.
- **Database-level transparency**: EHR export documentation names the actual database table and primary key for each JSON file, enabling developers to understand the data model
- **SQL types provided**: VARCHAR(255), Integer, DateTime, etc. — not just "string" or "text"
- **Multiple format options**: JSON (EHR, PM), TSV (ePrescribe, View), FHIR R4 (FMH) — all documented
- **Versioning**: View documentation has been updated 6 times (v1 Apr 2025 through v6 Jan 2026); PM and FMH each have v2 revisions
- **FHIR extension definitions**: FMH provides machine-readable StructureDefinitions, CodeSystems, and ValueSets for custom extensions

**Weaknesses:**
- **EHR documentation is dated**: Only v1 from November 2023 despite the product being certified at version 26 in December 2025. The documentation references "Veradigm EHR 23.4 and higher" — 2+ years of product updates are undocumented.
- **No sample data**: None of the products provide sample export files or example records
- **No machine-readable schema**: No JSON Schema, XSD, or other parseable schema definition — just PDF and HTML documentation
- **No explicit relationship documentation**: Foreign keys between tables (PatientID, EncounterId, ContactId) are implied by field descriptions but not formally specified
- **No value set definitions**: Coded fields like PatientMaritalStatus, Race, Ethnicity are documented as VARCHAR(255) with no enumeration of allowed values. The asterisk convention "(*) means Other" appears in some fields but many coded fields have no value sets.
- **Five separate export mechanisms**: A receiving system must implement five different format parsers (JSON, TSV, FHIR R4) to consume the full patient record across all products

**Could a developer build an import?** Yes, with significant effort. The field-level documentation is sufficient to understand the data model. The main challenges would be: (1) handling five different formats, (2) discovering value sets empirically, and (3) resolving relationships between tables across products.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This is one of the most comprehensive EHI export documentation suites among ambulatory EHR vendors. The combined documentation covers:
- 169 entities with 2,938 fields across 5 products
- All major clinical domains (demographics, problems, medications, labs, vitals, immunizations, procedures, encounters, care plans)
- Billing and claims data at a deep level (PM export with 392 fields including specialty billing appendices)
- Insurance with PBM detail (ePrescribe Insurance.tsv with 40 fields)
- Patient communications (45-field message table, web messages, FMH Communication resource)
- Actual binary files (images, scanned documents, transcriptions) — not just metadata
- Patient portal data (FMH FHIR export with 18 resource types)
- Questionnaires and flowsheets (generic containers that capture specialty data)
- Risk scores, advance directives, consents

The coverage goes well beyond USCDI. The 218-field claim information appendix alone demonstrates a level of billing data detail that most vendors don't approach. The View product's 87 entities with 12 dedicated billing/insurance tables (286 fields) further reinforce the breadth. The only meaningful gaps are in structured imaging data and specialty-specific clinical entities (which are likely captured generically through flowsheets and questionnaires).

**Axis 2 — Export approach: Purpose-built EHI export**

Clear signals this is purpose-built for (b)(10):

1. **Native database model**: The EHR export uses internal database table names (DEMOGRAPHICS, HX_DIAGNOSIS, MEDICATIONS, MEDADMIN_RECORD, etc.) and SQL types — this is a direct database-level export, not a standards projection.
2. **EHI-specific data**: Includes data that would never appear in (g)(10) or C-CDA: internal patient IDs, revision numbers, flowsheet definitions, risk scores, contact chunks, chart attachments, VIP indicators, organ donor flags, electronically-acquired-vital flags.
3. **Separate from FHIR API**: The FMH guide explicitly states "This is not an implementation of SMART/HL7 Bulk Data Access (Flat FHIR). FollowMyHealth is not currently using any FHIR Profile, such as US Core in this implementation."
4. **Dedicated billing export**: The PM product has a separate, purpose-built billing data export that doesn't exist in any standard clinical exchange.
5. **Five-product coverage**: Rather than pointing at a single FHIR API, Veradigm documents separate exports for each product component, each in its native format.
6. **Active development**: The View documentation has been updated 6 times since April 2025.

### Key Findings

1. **Breadth across the suite is exceptional**: 169 entities and 2,938 fields spanning clinical, billing, messaging, documents, and portal data across 5 product components. This is among the most comprehensive EHI export documentation in the ambulatory EHR market.

2. **Billing data is genuinely deep**: The Practice Management export documents 392 billing-related fields including specialty appendices for dental, ambulance, anesthesia, and drug billing. The View product adds 12 billing/insurance entities with 286 fields including 70-field superbill and 65-field insurance tables. This goes well beyond typical "we export billing" claims.

3. **Database-level export, not a clinical summary repackaging**: The EHR export maps directly to 51 internal database tables with SQL types and primary keys. Fields like `RevisionNumber`, `ContactId`, `ActiveStatusFlag`, `VIPIndicator`, and `ElectronicallyAcquiredWeightFlag` are clearly from the native database, not a standards projection.

4. **Documentation quality is high but aging for the core EHR**: The EHR PDF (v1, Nov 2023) hasn't been updated despite 2+ years of product development and a new version certification. The View documentation (v6, Jan 2026) is actively maintained. There are no sample data files or machine-readable schemas.

5. **The five-product architecture creates fragmentation**: A recipient must handle JSON, TSV, and FHIR R4 formats, and there's no single export that covers the full patient record. The EHR export is clinical-focused; billing requires the PM export; insurance detail requires ePrescribe; portal data requires FMH. There's overlap (demographics appear in all products) but also gaps between products that aren't documented.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   JSON (EHR, PM), TSV (ePrescribe, View), FHIR R4 (FMH)
Entities:        169 (51 EHR + 6 ePrescribe + 7 PM + 18 FMH + 87 View)
Fields:          2,938
Descriptions:    99.9% of fields have descriptions
Sample data:     No
Bulk export:     Unclear (multi-patient supported; no documented bulk API)
Domains covered: 18 of 19 applicable domains (imaging is partial)
```

### Bottom Line

A patient or provider using the full Veradigm suite would get a detailed, database-level copy of their clinical, billing, messaging, and portal data across 169 documented entities and 2,938 fields. The export is genuinely purpose-built for (b)(10) — it exposes internal database tables, billing claims, and EHR-specific metadata far beyond what any FHIR API or C-CDA exchange would cover. The biggest practical challenge is the fragmented five-product architecture requiring multiple export mechanisms and formats. The biggest documentation gap is the core EHR's stale v1 PDF (Nov 2023) that hasn't been updated to reflect 2+ years of product changes.

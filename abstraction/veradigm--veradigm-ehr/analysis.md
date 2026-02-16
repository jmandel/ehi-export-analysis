# EHI Export Analysis: Veradigm

**Product**: Veradigm EHR (version 26)
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.2891.Vera.26.14.1.251231 (listing ID 11763)

## 1. Product Context

Veradigm EHR (formerly Allscripts Professional EHR) is a full-featured ambulatory EHR targeting small-to-mid-size independent physician practices and multi-specialty organizations. It claims support for "nearly every medical specialty" with preloaded templates. The product has ~180,000 physician users and ~3.6% U.S. ambulatory EHR market share.

The certified EHR is one component of a broader suite:
- **Veradigm Practice Management** (PM) — scheduling, billing, claims processing, revenue cycle
- **Veradigm ePrescribe** — standalone electronic prescribing (also available separately)
- **FollowMyHealth** (FMH) — patient portal/PHR, separately ONC-certified
- **Veradigm View** — rebranded Practice Fusion EHR (cloud-native, small practices)
- **DORN** — diagnostic ordering/results network (500+ lab/radiology centers)

Key data the product stores: demographics, problem lists, medications, allergies, vitals, lab orders/results, procedures, immunizations, encounters with clinical notes, care plans/goals, referrals, flowsheets/custom worksheets, questionnaires, risk scores, scanned documents, transcriptions, attachments, and messaging. Via companion products: billing/claims, insurance, prescriptions, and patient portal data.

This is critical for export completeness assessment: the EHR itself stores clinical data; billing and scheduling live in Practice Management; the patient portal is FollowMyHealth. Veradigm documents EHI exports for all five products from a single compliance page.

## 2. Artifacts Reviewed

| Artifact | Description | Size/Scope | Usefulness |
|---|---|---|---|
| `VeradigmEHR_EHI_Export_output_format_documentation_v1.pdf` | EHR EHI export data dictionary | 89 pages, 51 JSON entities, 1,011 fields | **Most informative** for EHR |
| `VeradigmePrescribe_EHI_Export_Documentation_v1.pdf` | ePrescribe EHI export data dictionary | 22 pages, 6 TSV files, 266 fields | Informative |
| `EHIDataExportFile_ReferenceGuide_VeradigmPM_V2.pdf` | Practice Management billing export docs | 20 pages, 72 main fields + 317 appendix fields | Informative for billing coverage |
| `EHIDataExportFile_ReferenceGuide_VeradigmPM.pdf` | PM v1 (Dec 2023, superseded by V2) | 17 pages | Superseded |
| `VeradigmFMH_EHI_Export_Data_Guide_v2.pdf` | FollowMyHealth FHIR R4 export docs | 20 pages, 18 FHIR resources | Informative |
| `VeradigmFMH_EHI_Export_Data_Guide_v1.pdf` | FMH v1 (Nov 2023, superseded by v2) | 18 pages | Superseded |
| `veradigm-view-v6/index.html` + 87 entity pages | Veradigm View (Practice Fusion) TSV data dictionary | 88 HTML pages, 87 entities, 1,194 fields | **Most informative** for View |
| `fmh-fhir-extensions/` (9 JSON files) | FHIR StructureDefinitions, CodeSystems, ValueSets for FMH custom extensions | 3 StructureDefinitions + 3 CodeSystems + 3 ValueSets | Supplementary |
| `enrichment/view-entities-catalog.json` | Pre-extracted View entity catalog (machine-readable) | 87 entities, 1,194 fields | Highly useful |

## 3. Export Mechanics

Veradigm documents EHI exports across five products, each with distinct mechanisms:

### Veradigm EHR (the certified product)
- **Format**: Password-protected ZIP containing per-patient sub-ZIPs. Each patient ZIP has four folders: Attachments (images/documents/voice notes), Scanned Documents (TIF files), Transcriptions (RTF files), and Discrete Data (JSON files — 51 files across clinical domains).
- **Mechanism**: Built-in "EHI Export tool" within the EHR
- **Scope**: Single-patient export (ZIP per patient, multiple patients packaged together)
- **Access**: Password provided by practice; third-party archiver required (WinZip/WinRAR/7zip; Windows Explorer extraction does not work)
- **Fees**: Not documented

### Veradigm ePrescribe
- **Format**: ZIP containing TSV files (6 files per patient + a ReadMe.txt)
- **Scope**: Single-patient

### Veradigm Practice Management
- **Format**: JSON file with hierarchical billing/claims data
- **Scope**: Per-patient billing records
- **Note**: Explicitly labeled "non ONC certified" on the compliance page

### FollowMyHealth
- **Format**: FHIR R4 Bundle in JSON format + raw documents/images in a ZIP
- **Scope**: Per-patient; can be initiated by patient from PHR or by organization from Dashboard/API
- **Note**: "This is not an implementation of SMART/HL7 Bulk Data Access (Flat FHIR)" — explicitly not US Core

### Veradigm View (Practice Fusion)
- **Format**: TSV files (87 entity types)
- **Scope**: Per-patient
- **Note**: This is a separate product (Practice Fusion, acquired 2018, rebranded)

## 4. Export Content: What's In It

### Veradigm EHR Export (the certified product)

The 89-page PDF (Nov 9, 2023) documents **51 JSON files** mapping to EHR database tables, with **1,011 total fields**. Of these, **1,006 fields (99.5%) have descriptions** beyond just a name. All 1,011 fields have SQL data types documented (e.g., `VARCHAR(255)`, `Integer`, `DateTime`). Each entity lists its internal database table name and primary key.

**Correction to prior report**: The prior agent's report stated "43 JSON files." The PDF actually documents **51** — 43 have filenames starting at column 0 in the extracted text, but 8 additional entities are documented at indented positions within sub-sections (e.g., `ImplantableDevice.json`, `ContactInformation.json`, `ImmunizationForecast.json`, `EncounterAccompaniedBy.json`, `PatientGoalPlans.json`, `PatientGoalPlanBarriers.json`).

In addition to the 51 JSON discrete data files, the export includes three non-structured folders:
- **Attachments**: Images, documents, and voice notes (jpg, gif, tif, png, wav, mp3, pdf, doc, xls, ppt, etc.)
- **Scanned Documents**: TIF files from the EHR's Input Manager scanning system
- **Transcriptions**: RTF files of clinical transcriptions

### Veradigm ePrescribe Export

6 TSV files with **266 total fields**, all with descriptions and SQL data types:

| File | Fields | Key Content |
|---|---|---|
| Allergies.tsv | 10 | Allergy records with reactions, severity, onset |
| Demographics.tsv | 47 | Patient demographics, addresses, contacts |
| Diagnosis.tsv | 10 | Diagnosis codes and descriptions |
| Historical Medications.tsv | 79 | Medication history with dosing, NDC codes, prior auth |
| Insurance.tsv | 41 | Insurance coverage details |
| Prescriptions.tsv | 79 | Prescription details including EPCS, pharmacy routing |

### Veradigm Practice Management Export

Hierarchical JSON with **72 documented main fields** covering voucher-level billing data plus **317 appendix fields** across 6 specialty categories:

| Appendix Section | Fields |
|---|---|
| Claim information | 218 |
| Ailment information | 51 |
| Ambulance information | 21 |
| Drug information | 13 |
| Anesthesia information | 12 |
| Dental information | 2 |

Main structure covers: patient identification, voucher-level billing (charges, payments, adjustments, balances), provider info, claim info fields, service-level details (procedure codes, fees, modifiers, diagnoses linked per line), and payment transactions.

### FollowMyHealth Export

FHIR R4 Bundle with **18 resource types** (no field-level documentation beyond standard FHIR):
Account, AllergyIntolerance, Appointment, Bundle, Communication, Condition, DiagnosticReport, DocumentReference, Encounter, FamilyMemberHistory, Immunization, Invoice, Medication, MedicationRequest, Observation, Patient, Practitioner, Procedure.

Uses custom FHIR extensions (3 StructureDefinitions) for allergy status, procedure status, and family member history status. Also uses US Core Race/Ethnicity extensions for Patient.

### Veradigm View (Practice Fusion) Export

**87 TSV entity types** with **1,194 fields**, all with descriptions and data types. This is the most recently updated documentation (v6, January 12, 2026 — 6 versions since April 2025). Entity descriptions reference "Practice Fusion EHR" confirming this is a separate product.

### Vendor's own content organization

#### Veradigm EHR (by domain in PDF)

| Domain (vendor's) | Entities | Fields | Key Tables |
|---|---|---|---|
| Demographics | 4 | 124 | Demographics.json (81), PatientConsent.json (6), PatientContacts.json (21), PatientPhysicians.json (16) |
| History | 3 | 87 | HistoryDiagnosis.json (29), ImplantableDevice.json (27), HistoryMedication.json (31) |
| Vitals | 1 | 51 | Vitals.json (51) |
| Diagnosis | 1 | 35 | Diagnosis.json (35) |
| Medications | 3 | 101 | Medications.json (58), AdminMedications.json (35), RxOutputSummary.json (8) |
| Procedures | 2 | 60 | Procedures.json (32), ProceduresResult.json (28) |
| Lab Orders | 2 | 52 | LabOrders.json (22), LabResults.json (30) |
| Referrals | 1 | 43 | Referrals.json (43) |
| Flowsheet | 1 | 10 | FlowsheetDefinitions.json (10) |
| Risk Management | 1 | 20 | PatientRiskScore.json (20) |
| Contact | 3 | 31 | ContactNotes.json (9), ContactInformation.json (10), ContactData.json (12) |
| Encounter | 5 | 72 | Encounter.json (39), EncounterAssessment.json (8), EncounterPlan.json (9), EncounterAccompaniedBy.json (8), ChartAddendum.json (8) |
| ReasonForVisit | 2 | 25 | HpiDataNotes.json (7), HpiData.json (18) |
| Immunization | 4 | 61 | ImmunizationRecord.json (37), ImmunizationVIS.json (4), ImmunizationForecast.json (8), ImmunizationAddendum.json (12) |
| Message | 3 | 72 | SavedMessageResults.json (7), SavedMessages.json (45), SavedWebMessages.json (20) |
| Questionnaire | 3 | 18 | QuestionnaireRecords.json (8), QuestionnaireRecordResult.json (6), QuestionnaireRecordQuestionAnswer.json (4) |
| Care Plans | 8 | 79 | PatientCarePlans.json (8), PatientHealthConcerns.json (14), PatientCarePlanEncounters.json (5), PatientGoals.json (18), PatientAchieveGoals.json (11), PatientGoalBarriers.json (5), PatientGoalPlans.json (13), PatientGoalPlanBarriers.json (5) |
| Additional Files | 4 | 70 | NoteAndAttachmentDetails.json (6), ScannedDocuments.json (22), Transcriptions.json (25), ChartAttachments.json (17) |

#### Veradigm View (by vendor's index page categories)

| Category (vendor's) | Entities | Fields |
|---|---|---|
| Demographics | 10 | 143 |
| Patient | 2 | 27 |
| Clinical | 32 | 376 |
| Billing and Insurance | 12 | 286 |
| Medications and Prescriptions | 11 | 124 |
| Labs | 15 | 187 |
| Referrals | 2 | 24 |
| Messaging | 3 | 27 |

The full entity inventory is in `analysis/full-entity-inventory.json` (163 entities total across all products).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Veradigm EHR** (the certified product) provides a genuine native database export across 18 clinical domains with 51 entities and 1,011 fields. The richest areas are:
- **Demographics** (124 fields across 4 entities): Exceptionally detailed — includes 81 fields in Demographics.json covering names, addresses, employment, pharmacies, privacy status, organ donor flag, preferred pronouns, sexual orientation, race, ethnicity, language, and more.
- **Medications** (101 fields across 3 entities): Active medications (58 fields), administered medications (35 fields), and Rx output summaries (8 fields). Covers NDC codes, SIG information, dosing, administration routes.
- **History** (87 fields across 3 entities): Historical diagnoses (29 fields), implantable devices with UDI data (27 fields), and historical medications (31 fields).
- **Message** (72 fields across 3 entities): Saved messages (45 fields each), web messages, and message results — detailed internal messaging.
- **Encounter** (72 fields across 5 entities): Encounter metadata, assessment plans, HPI data, addenda.

The thinnest areas are:
- **Flowsheet** (10 fields, 1 entity): Only flowsheet definitions — not the actual flowsheet data values. This is a gap since flowsheets contain specialty-specific clinical assessments.
- **Questionnaire** (18 fields across 3 entities): Captures question/answer data but with minimal metadata per entry.

In addition to discrete data, the export includes actual files: attachments (images, documents, voice notes), scanned documents (TIF), and transcriptions (RTF). This is important — many vendors omit non-structured data.

**Veradigm Practice Management** adds billing coverage with 72 main fields documenting the voucher/claim/service/payment hierarchy, plus 317 appendix fields covering specialty claim types (ambulance, anesthesia, dental, drug). This is genuinely deep billing documentation.

**Veradigm ePrescribe** adds 266 fields across 6 files covering allergies, demographics, diagnoses, medications history (79 fields), insurance (41 fields), and prescriptions (79 fields).

**FollowMyHealth** adds 18 FHIR R4 resource types covering the patient portal perspective — account/billing, appointments, communications/messaging, conditions, results, medications, and more. Documentation is resource-type level (no field-level documentation beyond standard FHIR), but it explicitly states they use custom extensions where internal data doesn't map to FHIR.

**Veradigm View** (Practice Fusion, a separate product) has the most detailed and recently updated documentation: 87 entities, 1,194 fields, 100% with descriptions. Organized into 8 vendor categories with deep billing/insurance coverage (12 entities, 286 fields) including superbills.

### 5b. Standardized domain coverage (top-down)

This assessment focuses on **Veradigm EHR** (the certified product, CHPL 11763). Companion product exports are noted where they fill gaps.

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Demographics.json` (81 fields), `PatientContacts.json` (21), `PatientPhysicians.json` (16) | Thorough — addresses, phones, email, race, ethnicity, language, sexual orientation, gender identity, employment |
| Encounters / visits | ✅ Covered | `Encounter.json` (39 fields), `EncounterAssessment.json` (8), `EncounterPlan.json` (9), `EncounterAccompaniedBy.json` (8), `ChartAddendum.json` (8), `ContactData.json` (12) | Solid — encounter metadata, assessments, plans, addenda |
| Problems / conditions / diagnoses | ✅ Covered | `Diagnosis.json` (35 fields), `HistoryDiagnosis.json` (29 fields) | Thorough — active and historical, ICD/SNOMED coding |
| Medications / prescriptions | ✅ Covered | `Medications.json` (58), `AdminMedications.json` (35), `HistoryMedication.json` (31), `RxOutputSummary.json` (8); also ePrescribe: `Prescriptions.tsv` (79), `Historical Medications.tsv` (79) | Thorough — active, historical, administered, prescriptions |
| Allergies | ✅ Covered | Allergies are stored in `HistoryDiagnosis.json` (history domain); ePrescribe: `Allergies.tsv` (10 fields) | Covered but not as a separate EHR entity — lives within history tables |
| Immunizations | ✅ Covered | `ImmunizationRecord.json` (37), `ImmunizationVIS.json` (4), `ImmunizationForecast.json` (8), `ImmunizationAddendum.json` (12) | Thorough — 4 entities, 61 fields, includes VIS records and forecasting |
| Vitals | ✅ Covered | `Vitals.json` (51 fields) | Thorough — detailed with weight, height, BP, BMI, head circumference, and more |
| Lab results | ✅ Covered | `LabOrders.json` (22), `LabResults.json` (30) | Solid — orders and results with discrete data |
| Imaging / diagnostic reports | ⚠️ Partial | Imaging files present in Attachments folder; `ChartAttachments.json` (17 fields) references source (ENCOUNTER, PROCEDURE, etc.); no structured radiology report entity | The product integrates with DORN for imaging orders/results, but the export has no dedicated radiology results entity. Images are in Attachments but without structured interpretation data |
| Procedures | ✅ Covered | `Procedures.json` (32), `ProceduresResult.json` (28) | Solid — procedures with results |
| Clinical notes / documents | ✅ Covered | Transcriptions folder (RTF files), `Transcriptions.json` (25 fields), `ChartAttachments.json` (17), `NoteAndAttachmentDetails.json` (6), `ChartAddendum.json` (8), `ContactNotes.json` (9), Scanned Documents folder (TIF) | Thorough — multiple note types including transcriptions, addenda, scanned documents, attachments |
| Care plans / goals | ✅ Covered | `PatientCarePlans.json` (8), `PatientHealthConcerns.json` (14), `PatientGoals.json` (18), `PatientAchieveGoals.json` (11), `PatientGoalBarriers.json` (5), `PatientGoalPlans.json` (13), `PatientGoalPlanBarriers.json` (5), `PatientCarePlanEncounters.json` (5) | Thorough — 8 entities, 79 fields |
| Orders / referrals | ✅ Covered | `Referrals.json` (43 fields), `LabOrders.json` (22) | Solid |
| Insurance / coverage | ⚠️ Partial | No dedicated insurance entity in EHR export; ePrescribe: `Insurance.tsv` (41 fields); PM export: insurance fields in claims | The EHR export itself lacks insurance entities. Insurance data lives in the companion ePrescribe and PM products. If a customer uses only the EHR, insurance data appears to be missing from the EHR export |
| Claims / billing | ❌ Not in EHR export | PM export: vouchers, claims, services, payments (72 + 317 fields) | Billing is in the separate Practice Management product (explicitly labeled "non ONC certified"). The EHR export itself contains no billing data. For customers using the full suite, billing is covered by the PM export; for EHR-only customers, billing is not exported |
| Payments | ❌ Not in EHR export | PM export: payment transactions per service | Same as claims — only in PM export |
| Consents / directives | ✅ Covered | `PatientConsent.json` (6 fields) | Basic — consent title, format, answer, expiration |
| Patient communications / portal messages | ✅ Covered | `SavedMessages.json` (45), `SavedWebMessages.json` (20), `SavedMessageResults.json` (7); FMH export: Communication resource | Thorough — internal messages and web (portal) messages |
| Specialty-specific data | ⚠️ Partial | `FlowsheetDefinitions.json` (10 fields — definitions only, not data values), `QuestionnaireRecordQuestionAnswer.json` (4 fields), `PatientRiskScore.json` (20 fields) | The product claims to support "nearly every medical specialty" with templates, but specialty data appears to live in flowsheets and questionnaires as generic containers. FlowsheetDefinitions exports only the definitions (10 fields), not the actual patient flowsheet data. This is a potential gap for specialty-specific assessments |

## 6. Documentation Quality

**Strengths:**
- **Field-level documentation is excellent for the EHR export.** 1,006 of 1,011 fields (99.5%) have descriptions. All fields have SQL data types. Each entity documents its internal database table name and primary key, making it clear this is a genuine database-level export.
- **The EHR PDF is 89 pages of structured data dictionary.** This is not a summary or marketing document — it's a real technical reference.
- **Multiple export formats are documented separately** for each product in the suite, with clear structural documentation.
- **Veradigm View's documentation is actively maintained** — 6 versions between April 2025 and January 2026, with 100% field descriptions and data types across 87 entities and 1,194 fields.
- **FMH's FHIR extensions are published as machine-readable StructureDefinitions** at `fhir.followmyhealth.com/api/`, with accompanying CodeSystems and ValueSets.

**Weaknesses:**
- **No sample data or example JSON/TSV files.** A developer would have to guess at actual data formats.
- **No machine-readable schemas** (no JSON Schema, no XSD) for the EHR or PM exports.
- **No value set documentation.** Fields like `PatientMaritalStatus`, `Race`, `Ethnicity`, `PatientPrivacyStatus` are typed as `VARCHAR(255)` with no enumeration of allowed values.
- **No explicit relationship/foreign key documentation.** Relationships between entities are implied by shared field names (e.g., `PatientID`, `EncounterId`) but not formally documented.
- **The EHR export documentation (v1, Nov 2023) has not been updated in over 2 years.** The certified version is 26, but the documentation references "Veradigm EHR 23.4 and higher." Changes in versions 24–26 are undocumented.
- **FlowsheetDefinitions.json documents only 10 fields** — just the definition metadata (name, type, units) — raising questions about whether actual flowsheet data values are exported.
- **The PM export documentation uses a hierarchical structure** that's harder to parse than flat tables, and appendix fields are listed as names only without descriptions or types.

**Could a developer build an import?** Partially. The field descriptions and types are good enough to understand most data semantics. However, the lack of value sets, sample data, explicit relationships, and schemas would require significant discovery work. A developer would need to request an actual export to understand real data patterns.

## 7. Overall Assessment

### Classification

**Comprehensive native export** — with caveats.

The Veradigm EHR export is a genuine native database dump (JSON files mapping to named internal tables), not a repackaged C-CDA or FHIR API. It covers most clinical data domains with 51 entities and 1,011 well-documented fields. The documentation is a real data dictionary with field descriptions, types, table names, and primary keys.

When the full suite is considered (EHR + PM + ePrescribe + FMH), the combined exports cover clinical data, billing/claims, prescriptions, insurance, and patient portal data — a breadth that few vendors match. However, the EHR export alone has gaps in billing, insurance, and potentially in specialty/flowsheet data values.

### Key Findings

1. **Genuine native database export with excellent field documentation.** The EHR export maps 51 JSON files to named database tables (e.g., `DEMOGRAPHICS`, `MEDICATIONS`, `DX`) with 99.5% of fields having descriptions and all having SQL types. This is not a C-CDA or FHIR repackaging. (`VeradigmEHR_EHI_Export_output_format_documentation_v1.pdf`, 89 pages)

2. **Suite-level export covers clinical + billing + prescriptions + portal.** Veradigm documents exports for 5 products from one compliance page. Combined, these provide 163 entities and ~2,860 fields across clinical, billing, prescribing, and patient portal domains. The PM export adds 72 main fields + 317 appendix fields of billing/claims data.

3. **EHR export documentation is stale.** Version 1 (Nov 2023) has not been updated despite the product advancing from version 23.4 to version 26. Contrast with Veradigm View, which published 6 documentation versions in 9 months (Apr 2025 – Jan 2026). It's unclear what export changes accompanied versions 24–26 of the EHR.

4. **Flowsheet data values may be missing.** `FlowsheetDefinitions.json` exports only 10 fields of definition metadata (the template structure), not the actual patient-specific flowsheet data. Since specialty workflows (cardiology templates, orthopedic assessments, etc.) likely use flowsheets, this could represent a significant gap in specialty-specific clinical data.

5. **No value sets, sample data, or machine-readable schemas.** Despite strong field-level documentation, the export lacks the metadata needed for a developer to fully automate an import without requesting actual export files for discovery.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   JSON (EHR), TSV (ePrescribe, View), JSON (PM), FHIR R4 JSON (FMH)
Model type:      Native database (EHR, ePrescribe, PM, View); standard projection (FMH)
Entities:        163 across all products (51 EHR + 6 ePrescribe + 1 PM + 18 FMH + 87 View)
Fields:          ~2,860 across all products (1,011 EHR + 266 ePrescribe + 389 PM + 1,194 View)
Descriptions:    99.5% (EHR), 100% (View), 98.5% (ePrescribe); PM appendix fields lack descriptions
Sample data:     No
Bulk export:     Unclear — documentation describes per-patient ZIP files
Domains covered: 14 of 16 applicable (billing/payments only via companion PM product)
```

### Bottom Line

Veradigm provides one of the more thorough EHI export efforts in the market. The certified EHR product exports its native database model across 51 entities with genuinely useful field-level documentation, plus actual documents, images, and transcriptions. When the full suite is included (PM for billing, ePrescribe for prescriptions, FMH for portal data), the combined exports cover nearly all patient data domains. The biggest concerns are the stale EHR documentation (2+ years without updates) and the potential gap in specialty-specific flowsheet data values. A patient or provider would get a substantively complete copy of their clinical data, though billing data requires the separate Practice Management export.

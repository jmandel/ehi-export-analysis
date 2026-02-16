# EHI Export Analysis: Greenway Health, LLC

**Product**: Greenway Prime Suite  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 11352 (v21, certified 2023-10-03), 11681 (v22, certified 2025-08-14)

## 1. Product Context

Greenway Prime Suite is an integrated ambulatory EHR and practice management system serving approximately 55,000+ providers across 40+ specialties. It combines clinical documentation, practice management, billing/revenue cycle, patient engagement, and e-prescribing in a single platform. The product is available as both cloud-hosted (AWS) and on-premise deployments.

Key functional areas relevant to EHI scope:

- **Clinical documentation**: 4,000+ customizable templates across 40+ specialties, problem lists, diagnoses, medications, allergies, vitals, clinical notes, care plans
- **E-prescribing**: Electronic prescriptions, medication history, formulary checks, drug interaction alerts, EPCS
- **Practice management**: Appointment scheduling, patient registration, multi-site management
- **Billing & revenue cycle**: Claims management, payment processing, denial management, clearinghouse integration, ERA/EOB processing
- **Lab integration**: Bi-directional lab interfaces, lab ordering and results
- **Patient portal**: Secure messaging, lab results access, health history forms
- **Interoperability**: FHIR R4 API, C-CDA exchange, Direct messaging, public health reporting
- **Specialty**: Community Health Center / FQHC workflows (sliding fee scales, UDS reporting), OB/GYN, immunization tracking

The product is reportedly being sunset in favor of Greenway's other platform (Intergy), but remains actively certified and deployed.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `PrimeSuiteEHIExport.html` | 8 KB | Main EHI export landing page; describes export format, two export modes, links to sub-pages | **Medium** — key orientation document |
| `PrimeSuiteEHIExport_Data_Dictionary.html` | 1.7 MB | Complete data dictionary with 1,026 tables and 11,868 columns | **Critical** — primary evidence for export content |
| `PrimeSuiteEHIExport_Document_Reference.html` | 2.5 MB | XML reference for Greenway proprietary document formats (clinical notes, lab flowsheets, allergy tests) | **High** — explains proprietary formats |
| `SinglePatientExport_Structure_Schema.html` | 21 KB | Single-patient export directory structure, file naming, XML schema | **High** — explains export mechanics |
| `PatientPopulationExport_Structure_Schema.html` | 167 KB | Population export structure; initiated via My Greenway portal, fulfilled by Professional Services | **High** — explains bulk export process |
| `enrichment/data-dictionary.json` | 2.4 MB | Pre-extracted JSON parse of the data dictionary (1,026 tables, 11,868 columns, 0 parse failures) | **Critical** — machine-readable inventory |
| `enrichment/xml-reference.json` | 33 KB | Pre-extracted JSON parse of the XML reference (19 document type sections) | **Medium** — supplements document format understanding |
| `default.htm` | 3.5 KB | Greenway EHI documentation home page (covers both Prime Suite and Intergy) | **Low** — navigation only |
| Screenshots (7 files) | 2.5–221 KB | Directory structure screenshots for both export modes | **Low** — visual supplements to HTML docs |

## 3. Export Mechanics

**Format**: XML database dump — one XML file per database table, using a simple `<TableName><row><Column>value</Column></row></TableName>` schema. Documents (PDFs, C-CDAs, images, proprietary XML notes) are exported alongside as separate files in their native format.

**Two export modes**:

1. **Single Patient Export**: Exports all EHI for one patient. Produces a directory structure with:
   - `DataExport/` — XML files (one per table)
   - `DocumentExport/` — three subfolders: `AdamImage` (sketchpad annotations), `ClinicalBin` (clinical documents in PDF/C-CDA/TIF/JPG/GIF/BMP/TXT), `ImgLibGroupItem` (sketchpad images)
   - `Logs/` — error and process logs

2. **Patient Population Export**: Exports all EHI for all patients at a site. Initiated through the My Greenway support portal and fulfilled by Greenway Professional Services. Uses batch file naming (`PatientPopulation_DataExport_SiteID<id>_<Tablename>_Batch1.xml`) with batching at 1 million documents per file.

**Access constraints**:
- Population export requires contacting Greenway Professional Services via the My Greenway portal
- Some exported files require processing through the proprietary "Prime Suite Conversion Tool" (available only through authenticated My Greenway portal) to decrypt
- Minimum supported version: Prime Suite v21.23.00.00

**Fees**: Not mentioned in documentation.

## 4. Export Content: What's In It

The export contains the vendor's native database model — 1,026 relational database tables exported as XML files, plus associated clinical documents in their native formats.

### Data Dictionary Statistics

| Metric | Value |
|---|---|
| Total tables | 1,026 |
| Total columns | 11,868 |
| Tables with descriptions | 1,026 (100%) |
| Columns with descriptions | 11,864 (99.97%) |
| Columns with meaningful descriptions (>20 chars) | 11,386 (96%) |
| Columns with data types | 11,868 (100%) |
| Columns with foreign key references | 578 |
| Unique FK reference targets | 217 |
| Average columns per table | 11.6 |

Every table has a description, and virtually every column has a data type, nullability flag, and description. Column descriptions frequently include foreign key references (e.g., "References: dbo.ABNDocumentStatus"), making relationships navigable. Only 4 columns across the entire dictionary lack descriptions. 13 tables have generic descriptions (e.g., "Stores X description") but their column-level documentation is still complete.

### Vendor's own content organization

The data dictionary does not use explicit vendor-defined categories. Tables are presented alphabetically. I categorized them by name prefixes and descriptions into functional domains. The full inventory is in `analysis/full-entity-inventory.json` (1,026 entries).

**Category breakdown** (sorted by table count):

| Category | Tables | Columns | Representative Tables |
|---|---|---|---|
| Clinical Documents | 112 | 1,032 | ClinicalPatMeds (77 cols), ClinicalDocuments (28 cols), ClinicalVitalHistory (26 cols) |
| Billing & Finance | 97 | 2,012 | CFBClaimInfo (435 cols), br_ServiceDetail (92 cols), ServiceDetailHistory (96 cols) |
| Community Health Center (CHC/FQHC) | 87 | 1,517 | CHCClaim (177 cols), CHCClaim_Lines (95 cols), CHCClaim_Codes (92 cols) |
| Immunization / Vaccines | 80 | 690 | VacPatient (30 cols), VacAntigen (23 cols), InjectionPatientDose (20 cols) |
| Lab Results & Observations | 67 | 478 | OBXAdmin (14 cols), FlowSheetPatient (12 cols), OBXManual (12 cols) |
| Orders | 64 | 408 | OrdReqTransaction (22 cols), _oldOrdersTracking (22 cols), OrdAdmin (13 cols) |
| Patient History | 54 | 520 | PatHistMenstrualHistory (26 cols), fctPatientHistory (22 cols), PatHistBehavior (17 cols) |
| Medications / Prescriptions | 38 | 592 | ClinicalPatMeds (via FK), RxHistory (24 cols), MedicationList (18 cols) |
| Patient Records | 38 | 328 | PatientAllergyTestBattery (11 cols), PatientImplantedDevice (11 cols) |
| Claims Processing | 37 | 1,077 | ClaimHeaderHistory (272 cols), Claim (85 cols), ClaimHistory (84 cols) |
| Insurance & Eligibility | 35 | 685 | fctPatientInsurance (110 cols), InsurancePlan (106 cols), eligRequestTransaction (82 cols) |
| Patient Demographics | 29 | 464 | Person (19 cols), PersonDetails (22 cols), AddressHistory (20 cols) |
| Interoperability / Exchange | 27 | 161 | CDAImportData (11 cols), DSAvailableDocument (7 cols) |
| Scheduling | 26 | 177 | ScheduleAppointment (27 cols), ScheduleResource (7 cols) |
| Vocabulary / Coding Systems | 23 | 116 | VocabQuestionAdmin (10 cols), CodingSystemVersion (6 cols) |
| Demographics Reference Data | 21 | 125 | Race (5 cols), Ethnicity (5 cols), Gender (5 cols) |
| Practice Administration | 20 | 230 | PracticeInformation (53 cols), DataSourceFacility (11 cols) |
| Allergy | 19 | 79 | AllergyTestBattery (6 cols), AllergyTestDetail (9 cols) |
| Care Plans / Goals | 16 | 87 | CarePlanGoal (12 cols), CarePlanAssessment (4 cols) |
| Referrals / Authorizations | 16 | 71 | Referral (8 cols), ReferralDiagnosis (7 cols) |
| Providers & Organizations | 15 | 186 | CareProvider (37 cols), ExternalOrganization (21 cols) |
| Procedures | 13 | 79 | ProcedureMasterInfo (11 cols), CPT (6 cols) |
| Billing & Claims (EDI/X12) | 11 | 300 | ASCX12_835D_Claim (90 cols), ASCX12_837P_Claim (58 cols) |
| OB/GYN & Pregnancy | 8 | 47 | EDCInformation (16 cols), PregnancyIntent (4 cols) |
| Messaging / Communications | 8 | 35 | Messages (10 cols), MessageRecipient (7 cols) |
| Encounters / Visits | 7 | 114 | Visit (34 cols), VisitHistory (33 cols), VisitTypes (17 cols) |
| Advanced Beneficiary Notice (ABN) | 6 | 15 | ABNDocument (5 cols), ABNDocumentReason (3 cols) |
| Quality Measures / Reporting | 6 | 27 | PQRIPatientLog (6 cols), ResearchRequest (5 cols) |
| Vitals / Growth | 4 | 32 | WHOPediatricWeightForLength (15 cols), OldClinicalVitalGroup (6 cols) |
| Diagnoses / Problems | 3 | 13 | SDOHProblem (6 cols), SDOHGoal (4 cols), ProblemListStatus (3 cols) |
| Other / Uncategorized | 11 | 69 | AlcoholAmountUsed, UOMAdmin, FormAddQuestionData |
| Clinical Decision Support | 1 | 2 | AlertsHub (2 cols) |
| Lookup / Reference Tables | 27 | 100 | Various *LU, *Type, *Status tables |

**Note on diagnosis/problem coverage**: While only 3 tables are named "Diagnoses / Problems," diagnosis data is extensively represented across 39+ tables spanning Clinical Documents (`ClinicalDiagnosisExport`, `CTBDiagnosis`, `ClinicalProblemList`), Patient History (`PatHistProblemList`, `PatHistProblemListHistory`), Billing (`br_ServiceDetailToDiagnosis`), Orders (`OrdReqDiagnosis`), and other categories. Similarly, vitals data appears in `ClinicalVital` (22 cols) and `ClinicalVitalHistory` (26 cols) under Clinical Documents.

### Top 20 largest tables by column count

| Table | Columns | Category |
|---|---|---|
| CFBClaimInfo | 435 | Billing & Finance |
| ClaimHeaderHistory | 272 | Claims Processing |
| ClaimHeaderHistoryOLD | 226 | Claims Processing |
| CHCClaim | 177 | Community Health Center |
| CFBUBInfo | 135 | Billing & Finance |
| fctPatientInsurance | 110 | Insurance & Eligibility |
| fctAccount | 107 | Billing & Finance |
| InsurancePlan | 106 | Insurance & Eligibility |
| ServiceDetailHistory | 96 | Billing & Finance |
| CHCClaim_Lines | 95 | Community Health Center |
| br_ServiceDetail | 92 | Billing & Finance |
| CHCClaim_Codes | 92 | Community Health Center |
| ASCX12_835D_Claim | 90 | Billing & Claims (EDI/X12) |
| br_ServiceDetailHistory | 87 | Billing & Finance |
| OldPreRegServiceDetail | 87 | Billing & Finance |
| br_ClaimHistory | 86 | Billing & Finance |
| Claim | 85 | Claims Processing |
| ClaimHistory | 84 | Claims Processing |
| eligRequestTransaction | 82 | Insurance & Eligibility |
| ClinicalPatMeds | 77 | Clinical Documents |

The largest tables are overwhelmingly billing/claims-related, confirming deep financial data coverage.

### Proprietary document formats

The XML Reference document (19 sections) describes how Greenway-proprietary clinical documents are encoded:

- **Clinical Notes (filetype 1005)**: Progress notes, procedure notes, history & physical — stored in Greenway XML format with element-by-element documentation
- **Custom Notes (filetype 1016)**: Custom clinical notes, correspondence notes, consultation notes
- **Health Risk Assessments (HRA)**: Structured assessment documents
- **Lab Results (filetype 1000 BinType, 1016)**: Lab result documents in proprietary format
- **Lab Flowsheets**: XML-like JSON format with instructions for converting to SVG visualization
- **Prenatal Flowsheets (1005)**: OB/GYN-specific flowsheet documentation
- **Allergy Tests (1005)**: Allergy testing documentation
- **Allergy Education (1005)**: Allergy patient education documents
- **Medical Drawings**: Sketchpad annotations with instructions for reconstructing as SVG

Generic document types (PDF, C-CDA, TIF, JPG, GIF, BMP, TXT) are exported in their native format without transformation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is exceptionally broad, covering the full breadth of Prime Suite's database model. The strongest areas:

- **Billing & claims**: 145 tables with 3,389 columns across Billing & Finance (97 tables), Claims Processing (37 tables), and EDI/X12 (11 tables). This includes claim headers, service details, payment allocations, ERA/EOB processing, and full ANSI X12 EDI transaction data. The single largest table (`CFBClaimInfo`, 435 columns) is a billing entity.
- **Clinical documents**: 112 tables with 1,032 columns covering clinical notes, medications (77 cols in `ClinicalPatMeds`), vitals, document metadata, and encounter-level clinical data.
- **Community Health Center / FQHC**: 87 tables with 1,517 columns — a standout for specialty-specific data, covering FQHC claims, UDS reporting, sliding fee scales, and CHC-specific workflows.
- **Immunization / Vaccines**: 80 tables with 690 columns — unusually deep, covering antigen tracking, VFC codes, series management, lot numbers, injection sites, and patient dosing.
- **Lab results**: 67 tables with 478 columns (OBR/OBX-based HL7 segments, flowsheets, specimen instructions).
- **Patient history**: 54 tables with 520 columns covering medical, family, social, surgical, behavioral, genetic, pregnancy, and menstrual history — each with corresponding history-tracking tables.
- **Insurance**: 35 tables with 685 columns including insurance plans (106 cols), patient insurance (110 cols), eligibility transactions (82 cols).

The thinnest areas:
- **Clinical Decision Support**: Only 1 table (AlertsHub, 2 columns) — likely because CDS rules are system configuration, not patient data.
- **Diagnoses / Problems as standalone category**: Only 3 tables, but this is misleading as diagnosis data is distributed across 39+ tables in other categories.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Person` (19 cols), `PersonDetails` (22 cols), `AddressHistory` (20 cols), 29 Patient Demographics tables total, 21 Demographics Reference Data tables (Race, Ethnicity, Gender, Language, etc.) | Thorough — includes historical tracking |
| Encounters / visits | ✅ Covered | `Visit` (34 cols), `VisitHistory` (33 cols), `VisitTypes` (17 cols), `Encounter` (10 cols); 22 visit-related tables across categories | Thorough |
| Problems / conditions / diagnoses | ✅ Covered | `PatHistProblemList` (16 cols), `ClinicalDiagnosisExport` (20 cols), `CTBDiagnosis` (10 cols), `SDOHProblem` (6 cols); 39+ diagnosis/problem tables across categories | Thorough — distributed but comprehensive |
| Medications / prescriptions | ✅ Covered | `ClinicalPatMeds` (77 cols), `RxHistory` (24 cols), `MedicationList` (18 cols); 38 medication/prescription tables + eRx transaction tables | Thorough — includes eRx/EPCS |
| Allergies | ✅ Covered | 19 Allergy tables, `PatHistAllergy` (13 cols), `PatHistAllergyReaction` (9 cols); allergy test batteries, severity tracking, coding systems | Thorough |
| Immunizations | ✅ Covered | 80 tables covering vaccines, antigens, VFC codes, injection tracking, lot numbers, patient doses, series management | Exceptionally thorough |
| Vitals | ✅ Covered | `ClinicalVital` (22 cols), `ClinicalVitalHistory` (26 cols), `ClinicalVitalGroup`, `WHOPediatricWeightForLength` (15 cols) | Thorough — includes pediatric growth charts |
| Lab results | ✅ Covered | 67 Lab/OBR/OBX tables, `FlowSheetPatient` (12 cols), `OBXAdmin` (14 cols); proprietary lab flowsheet format documented | Thorough |
| Imaging / diagnostic reports | ⚠️ Partial | `PrimeImageWorkList` (12 cols), `PrimeImageWorkListHistory` (12 cols); image documents in `ClinicalBin`; `ImgLibGroupItem` for sketchpad images | Orders/worklists present; actual DICOM images not stored in Prime Suite per product research |
| Procedures | ✅ Covered | `ProcedureMasterInfo` (11 cols), `CPT` (6 cols), 13 Procedures tables; `CTBProcedure` (22 cols); procedure-diagnosis links | Covered |
| Clinical notes / documents | ✅ Covered | 112 Clinical Documents tables; proprietary XML formats documented for progress notes (1005), custom notes (1016), correspondence, consultation notes | Thorough — includes proprietary format specs |
| Care plans / goals | ✅ Covered | 16 Care Plans/Goals tables; `CarePlanGoal` (12 cols), `CarePlanAssessment` (4 cols), `SDOHGoal` (4 cols) | Covered |
| Orders / referrals | ✅ Covered | 64 Orders tables; 16 Referrals/Authorizations tables; `OrdReqTransaction` (22 cols), `Referral` (8 cols) | Thorough |
| Insurance / coverage | ✅ Covered | 35 Insurance/Eligibility tables; `InsurancePlan` (106 cols), `fctPatientInsurance` (110 cols), `eligRequestTransaction` (82 cols) | Exceptionally thorough |
| Claims / billing | ✅ Covered | 145 tables across billing/claims/EDI categories; `CFBClaimInfo` (435 cols), `Claim` (85 cols), full X12 835/837 EDI transaction data | Exceptionally thorough |
| Payments | ✅ Covered | Payment tables within billing (payment allocations, check details, deposit tracking, statement history) | Covered |
| Consents / directives | ⚠️ Partial | No dedicated consent tables visible; `ABNDocument` tables cover ABN consent but general advance directives not explicitly present | Product likely stores consents; no dedicated tables visible |
| Patient communications / portal messages | ✅ Covered | 8 Messaging tables (`Messages`, `MessageRecipient`, `MessageFolder`); Patient Portal tables; `PatientPortal*` tables | Covered |
| Specialty-specific: FQHC/CHC | ✅ Covered | 87 CHC tables with 1,517 columns covering FQHC claims, UDS reporting, sliding fee scales, visit types | Exceptionally thorough |
| Specialty-specific: OB/GYN | ✅ Covered | 8 OB/GYN tables + `PatHistPregnancy` (9 cols), `PatHistMenstrual` (22 cols), prenatal flowsheets documented | Covered |
| Specialty-specific: Behavioral health | ✅ Covered | `PatHistBehavior` (17 cols), behavioral assessment questions/answers (8+ tables), substance use coding systems | Covered |

## 6. Documentation Quality

**Strengths**:
- The data dictionary is exceptionally complete: 1,026 tables, 11,868 columns, 100% of tables and 99.97% of columns with descriptions
- Column descriptions are meaningful — 96% exceed 20 characters and include semantic information about what the field stores
- Foreign key references are documented in 578 column descriptions, making table relationships navigable
- Data types and nullability flags are specified for every column
- The XML Reference provides detailed element-level specifications for interpreting proprietary clinical document formats
- Export directory structure is well-documented with naming conventions and screenshots
- Both single-patient and population-level export modes are documented separately with clear instructions

**Weaknesses**:
- No sample data or example export files are provided
- No formal XSD or JSON Schema — the XML schema is described in prose/examples only
- Value sets for coded fields are not enumerated; lookup tables (e.g., `ABNDocumentStatus`, `ProblemListStatus`) are described but their actual values are not listed
- No entity-relationship diagram; relationships must be inferred from FK references in column descriptions
- 13 table descriptions are generic (e.g., "Stores X description") though column-level documentation remains complete
- The documentation is a single monolithic HTML page (1.7 MB for the data dictionary) with no downloadable CSV/JSON/PDF alternative
- The encryption/conversion tool is behind a login wall, creating a barrier to independent data access
- Documentation last-modified date (2023-11-27) predates the v22 certification (2025-08-14)

**Could a developer build an import?** Yes, with significant effort. The XML schema is simple and well-documented. Column-level descriptions provide enough context to understand most fields. Foreign key references allow reconstruction of relationships. However, the lack of sample data, value set enumerations, and formal schema means a developer would need to work from the XML data itself to understand actual data patterns. The proprietary document format decryption requirement adds friction.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

### Key Findings

1. **Genuine native database export covering 1,026 tables and 11,868 columns.** This is one of the most comprehensive EHI export data dictionaries reviewed. The vendor exports their actual relational database model in XML format — not a FHIR or C-CDA projection. (Source: `PrimeSuiteEHIExport_Data_Dictionary.html`, verified via `enrichment/data-dictionary.json`)

2. **Billing and claims coverage is exceptionally deep.** 145 tables with 3,389 columns cover claims, payments, EDI X12 transactions (835/837), service details, and financial records. The single largest table (`CFBClaimInfo`) has 435 columns. This is far beyond what a FHIR-based export would capture. (Source: `analysis/analysis-stats.json`)

3. **Specialty-specific data is included.** 87 CHC/FQHC tables (1,517 columns) for community health center workflows, 80 immunization tables (690 columns), OB/GYN and behavioral health tables, and 54 patient history tables covering medical, family, social, surgical, genetic, and pregnancy history. (Source: `analysis/full-entity-inventory.json`)

4. **Documentation quality is high but not perfect.** 100% of tables and 96% of columns have meaningful descriptions. Foreign key references are documented. However, no sample data, no formal schema, no value set enumerations, and a proprietary conversion tool requirement create barriers. (Source: `analysis/analysis-stats.json`)

5. **Population export requires vendor involvement.** The patient population (bulk) export must be requested through the My Greenway portal and is fulfilled by Greenway Professional Services, introducing a manual step and potential delay. (Source: `PatientPopulationExport_Structure_Schema.html`)

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   XML (one file per database table) + native document formats (PDF, C-CDA, TIF, JPG, etc.)
Model type:      Native database
Entities:        1,026 tables
Fields:          11,868 columns
Descriptions:    100% of tables, 99.97% of columns (96% with >20-char descriptions)
Sample data:     No
Bulk export:     Yes (vendor-assisted via My Greenway portal)
Domains covered: 17 of 19 applicable domains (consents partial, imaging partial)
```

### Bottom Line

Greenway Prime Suite's EHI export is one of the strongest implementations of the (b)(10) requirement. Exporting 1,026 native database tables with 11,868 fully documented columns — spanning clinical, billing, insurance, scheduling, and specialty-specific data — demonstrates a genuine effort to provide the complete designated record set. The main limitations are the lack of sample data, the proprietary conversion tool requirement for some document types, and the need for vendor assistance for population-level exports.

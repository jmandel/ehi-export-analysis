# EHI Export Analysis: Medical Information Technology, Inc. (MEDITECH)

**Product**: MEDITECH 6.0 Electronic Health Record Core HCIS, MEDITECH 6.0 Emergency Department Management, MEDITECH Client/Server Electronic Health Record Core HCIS, MEDITECH Client/Server Emergency Department Management, MEDITECH MAGIC Electronic Health Record Core HCIS, MEDITECH MAGIC HCA Electronic Health Record Core HCIS (without PatientKeeper), MEDITECH MAGIC Emergency Department Management
**Analysis date**: 2026-02-16
**CHPL IDs**: 10972, 10973, 10979, 10981, 10982, 10984, 11018

## 1. Product Context

This analysis covers MEDITECH's **Configuration 2** EHI export, applicable to three legacy platform generations:

- **MEDITECH 6.0 (MPM 6.08)** — ambulatory only
- **MEDITECH Client/Server** — acute and ambulatory
- **MEDITECH MAGIC** — acute and ambulatory

All three are legacy platforms within MEDITECH's integrated hospital information system. MEDITECH is the third-largest U.S. acute-care EHR vendor (~15% market share), and these older platforms remain in active use at hospitals that have not yet migrated to Expanse. Notably, HCA Healthcare (190+ hospitals) historically ran MAGIC and is actively migrating to Expanse.

Configuration 2 is used at sites running the **Medical Records (MRI)** and **Data Repository (DR)** modules, as opposed to Configuration 1 which uses HIM and Scanning & Archiving modules.

MEDITECH is a comprehensive, fully integrated hospital information system — not just an EHR module. The full platform includes modules for:
- **Clinical**: inpatient/outpatient EHR, emergency department, nursing, order entry, clinical decision support
- **Diagnostics**: laboratory, microbiology, pathology, blood bank, radiology, phlebotomy
- **Pharmacy**: pharmacy orders, dispensing, medication administration, e-prescribing
- **Revenue cycle**: registration, scheduling, billing, claims, practice management, coding/abstracting
- **Care coordination**: care plans, referral management, immunizations, population health
- **Specialty**: oncology, mental health, labor & delivery, surgical services, critical care, dietary, home health, hospice
- **Patient engagement**: MyHealth portal, patient messaging
- **Business operations**: general ledger, AP, HR, payroll, materials management

Under (b)(10), the export should cover all electronic health information stored by the product — the designated record set — which for these platforms encompasses clinical, financial, and administrative patient data across all integrated modules.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehiexport-main.html` (9 KB) | Main EHI Export overview page. Documents two export configurations with platform applicability matrix. | Medium — structural overview |
| `ehiexportconfig2.html` (23 KB) | Configuration 2 specification. Documents export zip structure: 8 sections (CSV data, FHIR bundle, clinical reports, messages, financial, C-CDA, external docs, POC scans). Platform-specific folder/file details. JSONTOC schema. | **High** — primary specification |
| `csacuteandambehiexportdrsolutionmerged.pdf` (263 KB, 30 pages) | CSV data dictionary for Client/Server Acute & Ambulatory. Lists 333 tables and 1,231 fields. | **High** — structured data dictionary |
| `mgehiexportdrsolutionmerged.pdf` (363 KB, 48 pages) | CSV data dictionary for MAGIC Acute & Ambulatory. Lists 322 tables and 1,121 fields. | **High** — structured data dictionary |
| `608ehiexportcsv.pdf` (251 KB, 19 pages) | CSV data dictionary for MPM 6.08 Ambulatory. Lists 97 tables and 482 fields. | **High** — structured data dictionary |
| `ehiexportold.html` (28 KB) | Older version of the EHI Export homepage. Essentially same content as Config 1 page. | Low — not primary for Config 2 |
| `screenshot-ehiexport-main.png` (226 KB) | Screenshot of main overview page. | Low — visual confirmation |
| `screenshot-ehiexportconfig2.png` (1.0 MB) | Screenshot of Config 2 spec page. | Low — visual confirmation |

**Note on prior report discrepancies**: The prior report (files.json) stated the C/S PDF was "20 pages" — it is actually 30 pages (verified via `pdfinfo`). The MAGIC PDF is 48 pages and the 6.08 PDF is 19 pages (both correct). The prior report also stated "331 tables" for C/S — it is 333 tables. It stated "323 tables" for MAGIC — it is 322 tables. These are minor discrepancies, likely from slightly different parsing approaches.

## 3. Export Mechanics

**Format**: Multi-format zip file containing:
1. **CSV files** — structured tabular data from the Data Repository, one file per namespace (table)
2. **FHIR R4 JSON** — Patient $everything bundle (US Core STU 3.1.1)
3. **C-CDA XML** — Consolidated-CDA documents (R2.1 or R1.1)
4. **Clinical reports/documents** — physician documentation, radiology, pathology, nursing images (PDF/DOC/TXT)
5. **Provider and patient messages** — PDF or TXT with embedded images
6. **Financial reports** — FinancialEHI.txt (patient accounting transactions)
7. **External documents/images** — scanned/imported documents (multiple formats)
8. **Point of contact scanned documents** — from MPM POC module

**Mechanism**: Export produces a zip file. The exact trigger (UI button, admin tool, vendor-assisted) is not detailed on the public documentation — the "Regulatory EHI Export Functionality Guides" at customer.meditech.com require authenticated access and are not publicly available.

**Single-patient vs bulk**: The export appears to be single-patient (zip per patient, folder named by medical record identifier).

**Access constraints**: The customer-facing implementation guides require MEDITECH customer portal login (SAML authentication at accounts.meditech.com). The public documentation covers the format specification only.

**Metadata**: Each export zip includes:
- `README.txt` — table of contents with folder/file descriptions
- `SCHEMA.txt` — documentation URL and product version
- `JSONTOC.txt` — NDJSON file of FHIR DocumentReference resources indexing every file in the zip, conforming to the Argonaut EHI Export API IG (draft)

## 4. Export Content: What's In It

### CSV Data Dictionaries

The primary structured data export for Config 2 is a set of CSV files from the Data Repository. Three platform-specific PDF data dictionaries document the tables and columns:

| Platform | PDF | Pages | Tables | Fields |
|---|---|---|---|---|
| Client/Server Acute & Ambulatory | `csacuteandambehiexportdrsolutionmerged.pdf` | 30 | 333 | 1,231 |
| MAGIC Acute & Ambulatory | `mgehiexportdrsolutionmerged.pdf` | 48 | 322 | 1,121 |
| MPM 6.08 Ambulatory | `608ehiexportcsv.pdf` | 19 | 97 | 482 |
| **Total** | | **97** | **752** | **2,834** |

Across all three platforms, there are **497 unique table names**, with **29 tables shared across all three platforms**. Client/Server has 108 platform-exclusive tables, MAGIC has 117, and MPM 6.08 has 46.

**Documentation depth per field**: Each field entry contains exactly three pieces of information:
1. **Field** — human-readable label (e.g., "Discharge Disposition", "Policy Num")
2. **Table** — internal table name (e.g., "AdmDischargeInfo", "AdmInsuredInfo")
3. **Column** — internal column name (e.g., "DispositionID", "PolicyNumber")

**What's NOT documented**: data types, value sets, cardinality, nullability, foreign keys/relationships, field descriptions, max lengths, default values, or example data. A developer consuming this export would know that `AdmVisits.RaceID` exists but not its type, possible values, or what it references.

### Vendor's own content organization

The CSV tables are organized by MEDITECH module prefixes. Below is a breakdown by category for each platform, derived from table name prefixes:

**Client/Server Acute & Ambulatory** (333 tables, 1,231 fields):

| Category | Tables | Fields | Representative Tables |
|---|---|---|---|
| Scheduling / Care (Sch) | 65 | 247 | SchAppointments (26 fields), SchOrPatCaseMain, SchPatVitalSigns* |
| Medical Records / Imaging (Mri) | 39 | 190 | MriPatients, MriAllergies, MriImmunVaccineEvents, MriImplDev* |
| Pharmacy (Pha) | 39 | 115 | PhaRx (22 fields), PhaRxAdministrations, PhaRxMedications |
| Nursing (Nur) | 28 | 128 | NurPatientPoc*, NurPlanOfCare*, NurQueryResults |
| Prescriptions / Medications (Rxm) | 22 | 73 | RxmRxs (21 fields), RxmRxDetails*, RxmOrd* |
| Order Entry (Oe) | 17 | 36 | OeOrders (6 variants), OeOrderEdits, OeOrderPhas |
| Ambulatory / Practice (Apr) | 16 | 88 | AprEnc, AprEncVitalsSets (24 fields), AprPatHmItems |
| Interoperability Hub (Hub) | 16 | 46 | HubPatientProblems, HubPatientRelatives, HubPatientProblemCodes |
| Pathology (Pth) | 16 | 25 | PthSpecimens, PthSpecimenHistologies, PthSpecimenTissues |
| Interface Transaction Services (Its) | 12 | 53 | ItsOrder, ItsOrderExams (18 fields), ItsOrderFindings |
| Admissions / Demographics (Adm) | 10 | 61 | AdmVisits, AdmInsuredInfo (14 fields), AdmEmployers |
| Blood Bank (Bbk) | 10 | 27 | BbkSpecimens, BbkHistoryTransfusions, BbkUnits |
| Patient Billing / Records (Pbr) | 8 | 38 | PbrAccountClaims, PbrAccountTransactions, PbrAccountStatements |
| Microbiology (Mic) | 8 | 9 | MicSpecimens, MicSpecimenOrganisms, MicSpecimenOrgSensitivities |
| Emergency Department (Edm) | 7 | 17 | EdmReminders, EdmPatientNotes, EdmPatientCallMngmnt |
| Authorization / Referral (Arm) | 6 | 62 | ArmAuths (33 fields), ArmAuthServices, ArmAuthServiceScheduledUnits |

**MAGIC Acute & Ambulatory** (322 tables, 1,121 fields):

Similar structure to C/S with notable differences:
- **Radiology (Rad)**: 17 tables, 48 fields (dedicated module; C/S uses ItsOrder for radiology instead)
- **E-Prescribing (Eps)**: 18 tables, 48 fields (includes problem lists and family history)
- **Patient Billing (Pbr)**: 27 tables, 139 fields — significantly more billing/ambulatory data than C/S (8 tables, 38 fields), including PbrMpiVisVisitsVitals (27 fields), PbrMpiVisProblems, PbrMpiVisHlthMntItemsDt
- **Nursing (Nur)**: 11 tables, 31 fields — smaller than C/S (28 tables, 128 fields); MAGIC uses text-based notes (NurNotes, NurNoteText) vs. structured plan of care tables in C/S
- No Hub (interoperability) or Apr (ambulatory practice) prefix tables; ambulatory data is under Pbr and Eps instead

**MPM 6.08 Ambulatory** (97 tables, 482 fields):

Ambulatory-only platform with focus on:
- **Ambulatory / Practice (Apr)**: 36 tables, 138 fields — richest category, covering encounters, vitals, health maintenance, problems, family history, questionnaires
- **Medical Records (Mri)**: 21 tables, 110 fields — allergies, immunizations, implantable devices, patient demographics
- **Prescriptions (Rxm)**: 19 tables, 89 fields — prescription management
- **Patient Billing (Pbr)**: 11 tables, 57 fields — billing/claims, insurance
- No inpatient modules (no Sch/surgical, Nur, Bbk, Lab, Mic, Pth, Edm, Oe, Pha)

The full entity inventory is in `analysis/entity-inventory-full.json` (2,834 field objects across 752 tables). Summary statistics are in `analysis/entity-inventory-summary.json`.

### Non-CSV Export Components

Beyond the CSV data files, the Config 2 export includes:

1. **FHIR Resources.json** — US Core STU 3.1.1 Patient $everything bundle. Covers standard USCDI clinical data (conditions, medications, allergies, observations, procedures, etc.). Documented by reference to the US Core spec and fhir.meditech.com.

2. **C-CDA documents** — Consolidated-CDA R2.1 or R1.1 documents. Standard clinical summaries. The 6.08 data dictionary explicitly notes one item as "n/a - found in the CCD" (for a comment field), indicating some data is only available via C-CDA rather than CSV.

3. **Clinical Reports/Documents** — Platform-specific:
   - C/S: Physician documentation and radiology reports (DOC/PDF), pathology reports (DOC/PDF), nursing image documentation (PDF)
   - MAGIC: Physician documentation, departmental reports, radiology reports (TXT), pathology reports with images and manifests (TXT/JPG/BMP), ambulatory physician/nurse documents (TXT/PNG)
   - 6.08: Physician documentation and nurse notes (PDF)

4. **Provider and Patient Messages** — C/S: PDF; MAGIC: TXT with embedded images

5. **Financial Reports** — `FinancialEHI.txt` containing patient accounting transactions

6. **External Documents/Images** — Scanned/imported documents in ambulatory settings (AmbScans folder). Supports PDF, DOCX, DOC, TXT, MTDD, HTML, RTF, ODT, TIF, PNG, JPG, BMP, GIF.

7. **Point of Contact Scanned Documents** — From MPM POC module

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

MEDITECH's Config 2 export demonstrates genuine breadth across the data domains these platforms store. The CSV data dictionaries alone cover 18 distinct module prefixes spanning clinical, diagnostic, financial, and administrative data.

**Richest categories** (by field count):
- Scheduling/Care (Sch): surgical services data with detailed operative records, vital signs across multiple care phases (pre-op, anesthesia, hold, PACU, post-PACU), complications, implants, equipment, devices, medications
- Medical Records/Imaging (Mri): patient demographics, allergies (coded and uncoded), immunizations with vaccine lot details, implantable device tracking, care teams, preferred pharmacies
- Pharmacy (Pha): medication orders, administration records with barcode scanning data, IV details, dose calculations, adverse drug reactions, interventions, refill data
- Nursing (Nur): plans of care with diagnoses/goals/interventions, image documentation with annotations, query results (C/S); text-based notes with amendments (MAGIC)
- Patient Billing (Pbr): account claims, claim details, transactions, statements, finance charges, payment distribution, diagnoses; MAGIC adds ambulatory visit data, health maintenance items, problems

**Notable platform differences**:
- MAGIC has a dedicated Radiology module (17 tables) that C/S handles via Interface Transaction Services
- MAGIC has a richer E-Prescribing module (18 tables) including family history and problem list management
- MAGIC's Patient Billing category is much larger (27 tables vs. C/S's 8), because it includes ambulatory clinical data under the Pbr prefix
- C/S has a unique Interoperability Hub module (16 tables) for problem list and family history management
- 6.08 is ambulatory-only and lacks all inpatient modules

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `AdmVisits` (name, address, phone, email, sex, DOB, race); `MriPatients` (demographics); `MriDrcPatients` | Thorough across all platforms |
| Encounters / visits | ✅ Covered | `AprEnc` (ambulatory encounters); `SchAppointments`; `AdmVisits` (location, status); `PbrMpiVisVisits` (MAGIC) | Multiple encounter types covered |
| Problems / conditions / diagnoses | ✅ Covered | `AdmVisitDiagnoses` (C/S); `AdmVisitOtherApplDiagnoses` (MAGIC); `HubPatientProblems` (C/S); `EpsProblems` (MAGIC); `AprPatProbMainProb` (6.08); `OeOrderProblemList` | Covered across platforms via different module paths |
| Medications / prescriptions | ✅ Covered | `RxmRxs` (18-28 fields), `RxmRxDetails*` (5 detail tables), `PhaRx` (19-22 fields), `PhaRxMedications`, `PhaRxAdministrations`; 22-24 Rxm tables + 39-44 Pha tables per platform | Very deep — covers prescriptions, pharmacy orders, administrations, IV details, dose calculations, refills |
| Allergies | ✅ Covered | `MriAllergies`, `MriAllergyCoded`, `MriAllergyUncoded`, `MriAllergyText`, `MriAllergyViews`, `PhaRxAllergies` | Thorough — coded and uncoded allergies with text and views |
| Immunizations | ✅ Covered | `MriImmunVaccineEvents`, `MriImmunVaccineEventComponents`, `MriImmunVaccineDoseLotDetails`, `MriImmunVacEvtPhaData` | Detailed vaccine event tracking |
| Vitals | ✅ Covered | `AprEncVitalsSets` (24 fields: height, weight, BMI, temp, pulse, resp, BP, SpO2, O2 delivery); `SchOrPatCaseVitalSigns*`; `PbrMpiVisVisitsVitals` (MAGIC, 27 fields) | Very detailed across ambulatory and surgical settings |
| Lab results | ✅ Covered | `LabSpecimens`, `LabSpecimenTests`, `LabSpecimenResultCommentsText`; `AprResLabTests` (C/S ambulatory); `PbrMpiResResults` (MAGIC ambulatory) | Covered, though Lab prefix has only 3 tables — additional lab data appears under Apr (C/S) and Pbr (MAGIC) |
| Imaging / diagnostic reports | ✅ Covered | `RadExams` + 16 related tables (MAGIC); `ItsOrder` + `ItsOrderExams` (C/S); Clinical Reports folder with radiology PDFs/TXT | Covered via different module paths per platform |
| Procedures | ✅ Covered | `SchOrPatCaseActualOps`, `SchOrPatCaseInvasiveProcs`, `SchOrPatCaseImplants`; `OeOrders`; C-CDA procedures | Detailed surgical/operative records |
| Clinical notes / documents | ✅ Covered | Clinical Reports/Documents section (physician documentation, departmental reports, nursing images); `NurNotes`/`NurNoteText` (MAGIC); `EdmPatientDocuments` (MAGIC); plus C-CDA | Multi-format: structured CSV tables + rendered documents |
| Care plans / goals | ✅ Covered | `NurPatientPoc` (C/S — diagnoses, goals, interventions); `NurPocGoalModifier*`, `NurPocWorkActivity` (C/S) | C/S has 28 nursing tables with structured care plans; MAGIC has fewer (11 Nur tables) |
| Orders / referrals | ✅ Covered | `OeOrders` (multiple variants), `OeOrderEdits`, `OeOrderQueries`; `ArmAuths` (33 fields), `ArmAuthServices` | Detailed order entry + authorization/referral management |
| Insurance / coverage | ✅ Covered | `AdmInsuredInfo`/`AdmInsuredData` (policy, group, effective/expiration dates, copay, deductible); `AdmInsurances`/`AdmInsuranceOtherType`; `MriPatientInsurances` (25-27 fields); `PbrAccountInsurance` (6.08) | Thorough — insurance plans, insured info, benefit plans |
| Claims / billing | ✅ Covered | `PbrAccountClaims`, `PbrAccountClaimsDetail`, `PbrAccountTransactions`, `PbrAccountStatements`, `PbrAccountStatementDetail`, `PbrAccountTxnFinanceCharges`, `PbrAccountTxnPymntDistribution`, `PbrAcctTxnDxs`; `FinancialEHI.txt` | Genuine billing data — claims, transactions, statements, payment distribution, finance charges |
| Payments | ✅ Covered | `PbrAccountTxnPymntDistribution`; `PbrAccountTransactions`; `FinancialEHI.txt` | Payment distribution tracked at transaction level |
| Consents / directives | ⚠️ Partial | `OeOrdResuscitation` / `OeOrderResuscitations` (advance directive/resuscitation orders) | Resuscitation status captured; no dedicated consent form tables |
| Patient communications / portal messages | ✅ Covered | Provider and Patient Messages section (PDF/TXT); `AprEncMessages`/`AprEncMessagesLines` (ambulatory); `EdmPatientCallMngmnt` (ED) | Provider-to-provider and provider-to-patient messaging; ambulatory encounter messages |
| Surgical / operative data | ✅ Covered | 50+ SchOrPatCase* tables covering: actual operations, complications (by phase), devices, dressings, equipment, implants, invasive procedures with ICD codes, IVs, medications, vital signs (by phase), untoward events | Exceptionally detailed surgical services data |
| Blood bank / transfusions | ✅ Covered | `BbkSpecimens`, `BbkSpecimenTests`, `BbkSpecimenCrossmatches`, `BbkSpecimenIssuedUnits`, `BbkHistoryTransfusions`, `BbkHistoryTransReactions`, `BbkUnits` | C/S: 10 tables; MAGIC: 8 tables; not applicable for 6.08 ambulatory |
| Pathology | ✅ Covered | 16 tables in both C/S and MAGIC: `PthSpecimens`, `PthSpecimenHistologies*`, `PthSpecimenTissues`, `PthSpecimenPictures`, `PthSpecimenAddendumText` | Detailed: specimens, histologies, blocks, levels, findings, pictures, sign-out audits |
| Microbiology | ✅ Covered | `MicSpecimens`, `MicSpecimenOrganisms`, `MicSpecimenOrgSensitivities`, `MicSpecimenOrgSensAntibiotics`, `MicSpecimenProcResults`, `MicSpecimenInterpretations` | Cultures, sensitivities, organisms, antibiotic susceptibility |
| Emergency Department | ✅ Covered | `EdmReminders`, `EdmPatientNotes`, `EdmPatientCallMngmnt`, `EdmPatientDepartRefers`; MAGIC adds `EdmPatientDocuments` (3 tables) | ED-specific notes, referrals, reminders, call management |
| Family health history | ✅ Covered | `HubPatientRelatives`, `HubPatientRelativeCondData`, `HubPatientRelativeCondNames`, `HubPatientRelativeDeceasedData` (C/S); `EpsFamilyHistoryRelations`, `EpsFamilyHistoryProblems*` (MAGIC); `AprPatientPfshFamilyRels*` (6.08) | All platforms cover family history via different modules |
| Implantable devices | ✅ Covered | `MriImplDevImplants`, `MriImplDevExplants`, related comment/provider/production ID tables | Implant and explant tracking with lot numbers, manufacturers |
| Specialty – oncology, mental health, L&D, dietary | ❌ Not covered | No tables with Onc/MH/OB/Diet prefixes | MEDITECH has dedicated Oncology, Mental Health, L&D, Dietary modules. No evidence these are in the CSV export. Some data may be captured in clinical notes or C-CDA documents, but not as structured data. |
| Scanned/external documents | ✅ Covered | External Documents/Images section (AmbScans folder); POC Scanned Documents | Multi-format support (PDF through GIF) |

## 6. Documentation Quality

**Strengths**:
- **Structured data dictionary exists**: All three platforms have a PDF data dictionary mapping every CSV table and column — this is more than many vendors provide
- **Clear export structure**: The Config 2 HTML page clearly documents the zip folder hierarchy, file naming conventions, and platform-specific variations
- **Machine-readable metadata**: JSONTOC provides FHIR DocumentReference resources for every file in the export, conforming to the Argonaut EHI Export API IG draft
- **Multi-format approach**: Using CSV for structured data, FHIR for standard clinical data, C-CDA for clinical documents, and native formats for reports/images is a reasonable strategy

**Weaknesses**:
- **No data types**: The data dictionaries list only field label, table name, and column name. There are no types (string, integer, date, boolean, etc.) for any of the 2,834 fields
- **No descriptions**: Beyond the human-readable field label (e.g., "Discharge Disposition"), there are no field descriptions explaining what a field contains or how it should be interpreted
- **No value sets**: Fields ending in "ID" (e.g., `RaceID`, `RelationshipID`, `DispositionID`, `StatusID`) clearly reference coded values, but the valid code sets are never documented
- **No relationships**: Tables obviously have foreign key relationships (shared IDs, naming conventions), but these are not documented. A consumer would need to infer that `BbkSpecimenCrossmatches` relates to `BbkSpecimens` via naming convention
- **No sample data**: No example CSV files or example export zips are provided
- **No schema files**: No machine-readable schema (JSON Schema, XSD, etc.) — only PDF
- **PDF format**: The data dictionaries are PDFs with fixed-width layout, making programmatic extraction necessary. No CSV, JSON, or machine-readable version is provided
- **Implementation guides locked**: The "Regulatory EHI Export Functionality Guides" at customer.meditech.com require authentication and are not publicly accessible

**Usability assessment**: A developer receiving this export would have CSV files with column headers matching the documented column names and could identify tables by filename. They would know from the field labels roughly what each column contains. However, interpreting coded values (all the `*ID` fields), understanding relationships between tables, and validating data types would require reverse-engineering from the actual data. Building a reliable import pipeline from this documentation alone would be challenging.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

MEDITECH's Config 2 export covers an impressive breadth of data domains for these legacy platforms. The CSV data dictionaries span 18 distinct module areas including clinical care, diagnostics (lab, microbiology, pathology, blood bank, radiology), pharmacy, nursing, emergency department, order entry, scheduling/surgical services, billing/claims, insurance, authorization/referral management, immunizations, and medical records. For the C/S and MAGIC platforms specifically, the export covers essentially all major patient-facing data domains these products store, plus the FinancialEHI.txt report and C-CDA/FHIR layers.

The one notable gap is the absence of specialty-specific clinical modules (oncology, mental health, L&D, dietary) — MEDITECH has certified Oncology modules for both C/S and MAGIC platforms, and the broader platform supports mental health, L&D, and dietary. However, these may be separately licensed modules not present at all installations, and some specialty data may be captured in clinical notes rather than discrete tables. Overall, the export far exceeds USCDI scope and covers billing, referrals, surgical detail, and diagnostic data that USCDI does not require.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged (g)(10) API. The evidence is unambiguous:

1. The export produces a **zip file** (not an API endpoint), explicitly labeled as §170.315(b)(10)
2. The **CSV data files** from the Data Repository export 300+ internal tables that have no counterpart in the FHIR or C-CDA layers — blood bank specimens, surgical case details, pathology histologies, nursing plans of care, pharmacy IV calculations, etc.
3. The FHIR bundle and C-CDA are included as **supplemental components** alongside the CSV data, not as the sole export mechanism
4. The export includes **financial reports** (FinancialEHI.txt), **provider/patient messages**, **scanned documents**, and other non-USCDI data
5. Three **platform-specific data dictionaries** document the CSV tables — these are product-specific artifacts, not generic FHIR/C-CDA specifications
6. The JSONTOC metadata conforms to the **Argonaut EHI Export API IG**, a (b)(10)-specific specification

### Key Findings

1. **Genuinely deep structured data export**: 752 tables and 2,834 fields across three platforms, covering clinical, diagnostic, pharmaceutical, surgical, financial, and administrative data. The surgical services data alone spans 50+ tables with per-phase detail (pre-op, anesthesia, hold, PACU). This is not a summary — it's a Data Repository dump.

2. **Documentation is wide but shallow**: The data dictionaries provide field names and column mappings but zero data types, descriptions, value sets, or relationships. A developer can tell that `AdmInsuredInfo.PolicyNumber` exists but not its type, max length, or format. The 2,834 fields have 0% with descriptions beyond field labels.

3. **Significant platform variation**: C/S and MAGIC have 300+ tables each but organize data differently (e.g., C/S uses Hub* for problems/family history, MAGIC uses Eps*; C/S has Nur* plan of care, MAGIC has Nur* text notes). 6.08 is ambulatory-only with 97 tables. Only 29 tables are shared across all three. A consumer would need to understand three different data models.

4. **Specialty modules absent**: Despite MEDITECH's Oncology, Mental Health, L&D, and Dietary modules being part of the platform, no specialty-specific tables appear in the CSV data dictionaries. This is a real gap for sites using these modules.

5. **Multi-format approach is well-designed**: CSV for structured data, FHIR for standard clinical data, C-CDA for clinical documents, native formats for reports/images, and FHIR DocumentReference metadata for the table of contents. Each data type is exported in its most natural format.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   CSV + FHIR R4 JSON + C-CDA XML + PDF/TXT reports + images
    Entities:        752 (333 C/S + 322 MAGIC + 97 6.08); 497 unique
    Fields:          2,834 (1,231 C/S + 1,121 MAGIC + 482 6.08)
    Descriptions:    0% (field labels only, no actual descriptions)
    Sample data:     No
    Bulk export:     Unclear (appears single-patient)
    Domains covered: 20 of 22 applicable domains

### Bottom Line

MEDITECH's Configuration 2 EHI export is one of the more comprehensive (b)(10) implementations among EHR vendors — the CSV data dictionaries document hundreds of internal database tables spanning clinical, diagnostic, pharmaceutical, surgical, financial, and administrative domains, far exceeding what USCDI or C-CDA covers. A patient would receive structured data from virtually every major module in the system. The biggest weakness is documentation quality: with no data types, value sets, relationships, or field descriptions, a receiving system would need significant effort to interpret the 2,834+ fields, and the absence of specialty clinical modules (oncology, mental health, L&D) represents a gap for sites that use those capabilities.

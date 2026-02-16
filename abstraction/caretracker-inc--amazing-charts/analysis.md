# EHI Export Analysis: CareTracker, Inc. (Amazing Charts)

**Product**: Amazing Charts
**Analysis date**: 2026-02-16
**CHPL IDs**: 11492 (v12.0), 11608 (v12.2), 11646 (v12.3), 11720 (v12.4)

## 1. Product Context

Amazing Charts is an ONC-certified ambulatory EHR with integrated practice management, targeting small to medium independent medical practices (1–10 clinicians). Developed by CareTracker, Inc. (a Harris Healthcare / Constellation Software subsidiary), it serves primary care, family medicine, pediatrics, internal medicine, dermatology, urgent care, and surgery practices.

**Key capabilities relevant to export completeness:**

- **Clinical EHR**: Charting with customizable templates, problem lists, medication lists, allergy lists, vital signs, lab integration (HL7), clinical notes, immunization records, clinical decision support, care plans, referrals
- **E-Prescribing**: Via NewCrop/DrFirst/Surescripts, including EPCS for controlled substances
- **Practice Management**: Appointment scheduling, insurance eligibility verification, claims management, payment posting, financial reporting
- **Patient Engagement ("AC Patient Connect")**: Patient portal (via Updox), secure messaging, online scheduling, digital intake forms, consent forms, appointment reminders, telemedicine
- **Public Health Reporting**: Immunization registry submissions, electronic case reporting
- **Quality Measures**: 50+ CQMs for MIPS reporting

The product stores clinical data, billing/claims data, insurance information, patient communications, scheduling, and custom/specialty clinical data. A complete (b)(10) export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Amazing-Charts-EHI-Export-Documentation-V1_0-1-1.pdf` | 8-page PDF (195 KB). EHI Export specification v1.0, dated October 2023. Contains export mechanism overview and a 2-column data dictionary listing 44 data classes and their column headings. **Primary artifact.** | **High** — sole source of export specification |
| `downloads/enrichment/data-dictionary.json` | Prior agent's JSON extraction of the data dictionary (43/44 classes, 1,101 columns). Used for cross-reference only. | Medium — useful for validation |
| `downloads/enrichment/extract-data-dictionary.ts` | Prior agent's TypeScript parser script. Read for approach reference. | Low |
| `product-research.md` | Detailed product research establishing baseline capabilities. | High — essential for gap analysis |
| `ehi-export-report.md` | Prior agent's narrative analysis. | Medium — used for orientation, independently verified |

**No sample data files, schemas (XSD/JSON Schema), or additional documentation exist.** The PDF is the entire EHI export documentation.

## 3. Export Mechanics

- **Format**: CSV, JSON, or XML — user-selectable per export
- **Mechanism**: UI-driven export within the Amazing Charts application
- **Scope**: Supports both single-patient and population-level export
- **Population filters**: By Provider, All Active Patients, All Patients, or Encounter Range
- **Structure**: Per-patient folder (timestamped), one file per data class named `[DataClassName].[format]`. A "Documents" subfolder preserves imported items, images, and documents in original format.
- **Access constraints**: No fees or special access requirements mentioned in the documentation
- **Standards**: Not FHIR, not C-CDA — vendor-native flat file format with raw database column names

## 4. Export Content: What's In It

The export documentation is an 8-page PDF containing a two-column table listing 44 data classes and their column headings. This is the complete data dictionary.

**Key documentation characteristics:**
- **44 data classes** with **1,102 total fields** (column names)
- **0 fields with descriptions** (0%) — only column names are provided, no definitions
- **0 fields with types** (0%) — no data types documented
- **No value sets** — coded fields (e.g., `ERXstatus`, `MaritalStatus`, `InsuranceType`) have no enumeration of valid values
- **No relationships** — no foreign keys or entity-relationship documentation; PatientID is the implicit join key
- **No sample data** — no example records or test exports
- **No machine-readable schemas** — no XSD, JSON Schema, or similar

### Vendor's own content organization

The vendor does not organize data classes into categories. The following table uses the vendor's data class names as-is, with analyst-assigned categories based on content:

| Data Class | Fields | Category (analyst-assigned) |
|---|---|---|
| Addendum | 6 | Clinical Notes |
| Advance Directives | 14 | Care Planning |
| Alerts | 14 | Communication |
| Allergies and Intolerances | 25 | Allergies |
| Allergies and Intolerances Pending | 26 | Allergies |
| Assesments | 5 | Clinical Notes |
| Billing History | 74 | Billing |
| Care Team Members | 13 | Care Planning |
| Clinical Notes | 89 | Clinical Notes |
| Demographic Immunization | 8 | Immunizations |
| Email | 11 | Communication |
| FamilyHistory | 20 | History |
| FunctionalStatus | 6 | Care Planning |
| Goals | 5 | Care Planning |
| Health Concerns | 5 | Care Planning |
| Health Insurance | 39 | Insurance |
| HM Rules | 86 | Immunizations / Health Maintenance |
| HM Rules Ignored | 40 | Immunizations / Health Maintenance |
| Immunizations | 37 | Immunizations |
| Implantable device | 19 | Devices |
| Imported Items | 16 | Documents |
| Injections | 14 | Medications |
| Lab Tests | 126 | Labs |
| List Problem | 17 | Problems |
| List Problem Pending | 18 | Problems |
| Medications | 50 | Medications |
| Medications Pending | 38 | Medications |
| Next Of Kin | 17 | Demographics |
| Occupation and Industry History | 14 | History |
| Orders | 24 | Orders |
| Patient Demographics | 62 | Demographics |
| Patient Generated Data | 14 | Documents |
| Patient Health Information Capture | 17 | Documents |
| Patient Record Release | 26 | Administrative |
| Plan of Treatment | 5 | Clinical Notes |
| Procedures | 15 | Procedures |
| Referrals | 12 | Orders |
| Risk Factors | 5 | History |
| Scheduling | 14 | Administrative |
| Smoking Statuses | 12 | History |
| Tracked Data | 5 | Clinical Data |
| Travel History | 7 | History |
| User Defined Fields | 4 | Administrative |
| Vital Signs | 28 | Vitals |

**Category summary:**

| Category | Entities | Fields |
|---|---|---|
| Administrative | 3 | 44 |
| Allergies | 2 | 51 |
| Billing | 1 | 74 |
| Care Planning | 5 | 43 |
| Clinical Data | 1 | 5 |
| Clinical Notes | 4 | 105 |
| Communication | 2 | 25 |
| Demographics | 2 | 79 |
| Devices | 1 | 19 |
| Documents | 3 | 47 |
| History | 5 | 58 |
| Immunizations | 2 | 45 |
| Immunizations / Health Maintenance | 2 | 126 |
| Insurance | 1 | 39 |
| Labs | 1 | 126 |
| Medications | 3 | 102 |
| Orders | 2 | 36 |
| Problems | 2 | 35 |
| Procedures | 1 | 15 |
| Vitals | 1 | 28 |

**Notable entities by depth:**

- **Lab Tests** (126 fields): Most detailed entity. Covers test creation/ordering, specimen data, result details, reference ranges, LOINC codes, abnormal flags, lab facility info, notes, and multiple result detail sub-sections. Column names like `ResultDetailLoincTestCode`, `ResultDetailAbnormalFlag`, `ResultDetailRefenceRanges` indicate rich structured lab data.
- **Clinical Notes** (89 fields): Very thorough encounter documentation including chief complaint, HPI, ROS, physical exam, assessment, plan, vitals (embedded), tobacco use details (pipe, cigar, chewing, e-cig with date ranges), pregnancy data (LMP, EDD), vision/hearing, images/illustrations, and transition of care indicators.
- **HM Rules** (86 fields): Health maintenance rules with vaccine administration details, immunization registry data, VIS info, plus the full rule definition (recommended ages, intervals, risk categories, funding sources, etc.) and vaccine product details.
- **Billing History** (74 fields): CPT codes, up to 12 ICD pointers, modifiers, fees/charges, NDC codes, facility information (address, NPI), billing provider details (DEA, state license, UPIN, NPI), referring provider details, and prior authorization numbers.
- **Patient Demographics** (62 fields): Comprehensive including race, ethnicity, language, sexual orientation, gender identity, previous addresses, employer, marital status, mother's maiden name, birth order, and custom fields.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers a genuine breadth of data domains from the Amazing Charts database — this is not a C-CDA or FHIR repackaging. The column names are raw database field names (including typos like "FristName", "Signetur", "BillingProvideerState"), confirming this is a native data model export.

**Strongest areas:**
- **Clinical documentation**: 4 entities (Clinical Notes, Addendum, Assesments, Plan of Treatment) with 105 total fields. Clinical Notes alone has 89 fields covering the full encounter — far exceeding what C-CDA or USCDI would require.
- **Lab results**: 126 fields in a single entity, including ordering details, specimen tracking, multi-level result data, lab facility information, and notes.
- **Medications**: 3 entities (active, pending, injections) with 102 fields including e-prescribing details (ERXstatus, SentBySureScripts, PharmacyTransactionID), dispensing info, and controlled substance tracking.
- **Billing**: 74 fields covering CPT/ICD coding, charges, modifiers, NDC codes, provider credentialing details, facility info, and prior authorization.
- **Insurance**: 39 fields with payer details, subscriber/guarantor demographics, coverage dates.
- **Immunizations / Health Maintenance**: 3 entities with 171 combined fields — extremely detailed vaccine administration records and health maintenance rule tracking.
- **Demographics**: 79 fields across 2 entities with extensive demographic detail including USCDI v3 requirements (sexual orientation, gender identity) and administrative data.

**Thinnest areas:**
- **Tracked Data** (5 fields), **Risk Factors** (5 fields), **Goals** (5 fields), **Assesments** (5 fields), **Health Concerns** (5 fields), **Plan of Treatment** (5 fields) — minimal field counts, though these may reflect genuinely simple data structures.
- **User Defined Fields** (4 fields: PatientId, FieldValue, Template, DateEntered) — captures custom data but with a generic key-value structure rather than expanded fields.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (62 fields), `Next Of Kin` (17 fields) | Thorough — includes race, ethnicity, language, sexual orientation, gender identity, previous addresses |
| Encounters / visits | ⚠️ Partial | `Clinical Notes` includes `EncounterDate` and `EncounterTypeName`; `Scheduling` has appointment data | No dedicated encounter entity — encounter context is embedded within Clinical Notes. Visit history is reconstructable from scheduling and notes but not explicitly modeled. |
| Problems / conditions | ✅ Covered | `List Problem` (17 fields), `List Problem Pending` (18 fields) | Includes ICD, SNOMED, chronicity, date tracking, provider attribution |
| Medications / prescriptions | ✅ Covered | `Medications` (50 fields), `Medications Pending` (38 fields), `Injections` (14 fields) | Strong — includes e-prescribing status, pharmacy details, dispensing, controlled substance tracking |
| Allergies | ✅ Covered | `Allergies and Intolerances` (25 fields), `Allergies and Intolerances Pending` (26 fields) | Includes severity, reaction, SNOMED adverse reaction IDs, date ranges |
| Immunizations | ✅ Covered | `Immunizations` (37 fields), `HM Rules` (86 fields), `HM Rules Ignored` (40 fields), `Demographic Immunization` (8 fields) | Very detailed — vaccine admin, VIS, manufacturer, lot, registry submissions, VFC status |
| Vitals | ✅ Covered | `Vital Signs` (28 fields) | Thorough — includes BP, temp, pulse, RR, O2 sat, weight, height, BMI, head circumference, pain, peak flow, vision, hearing, pregnancy vitals |
| Lab results | ✅ Covered | `Lab Tests` (126 fields) | Exceptionally detailed — ordering, specimen, results, LOINC, reference ranges, abnormal flags, lab facility info |
| Imaging / diagnostic reports | ⚠️ Partial | `Imported Items` includes `TypeOfItem` which may contain imaging; `Clinical Notes` has `Image1Description`/`Image1Location` | No dedicated imaging/radiology entity. Imaging results likely captured as imported documents but not as structured data. |
| Procedures | ✅ Covered | `Procedures` (15 fields) | CPT codes, descriptions, fees, NDC codes, status tracking |
| Clinical notes / documents | ✅ Covered | `Clinical Notes` (89 fields), `Addendum` (6 fields), `Imported Items` (16 fields) | Rich encounter notes; Documents subfolder preserves original files |
| Care plans / goals | ✅ Covered | `Goals` (5 fields), `Health Concerns` (5 fields), `Plan of Treatment` (5 fields), `Care Team Members` (13 fields), `Advance Directives` (14 fields), `FunctionalStatus` (6 fields) | Present but thin — Goals and Health Concerns have only 5 fields each (PatientID, EncounterDate, Provider, Goals/HealthConcerns text) |
| Orders / referrals | ✅ Covered | `Orders` (24 fields), `Referrals` (12 fields) | Order type, status, tracking, assignment, results |
| Insurance / coverage | ✅ Covered | `Health Insurance` (39 fields) | Payer, plan, subscriber/guarantor demographics, coverage dates, copay |
| Claims / billing | ✅ Covered | `Billing History` (74 fields) | Detailed — CPT/ICD coding, charges, modifiers, NDC, provider/facility details, prior auth |
| Payments | ❌ Not covered | No payment posting, remittance, or accounts receivable entities | Product has payment posting and remittance processing (per PM module description); significant gap |
| Consents / directives | ✅ Covered | `Advance Directives` (14 fields), `Patient Health Information Capture` (17 fields), `Patient Record Release` (26 fields) | Includes consent forms and record release tracking |
| Patient communications | ⚠️ Partial | `Email` (11 fields), `Alerts` (14 fields) | Email entity may capture internal/portal messages. No explicit patient portal message entity despite Updox portal integration. Portal messages may reside in Updox, not Amazing Charts. |
| Specialty-specific data | ⚠️ Partial | `Clinical Notes` has some specialty fields (vision, hearing, pregnancy), but no dedicated specialty entities | Product supports multiple specialties via templates; template-specific data may be captured within Clinical Notes free-text fields or User Defined Fields rather than structured entities |
| Family history | ✅ Covered | `FamilyHistory` (20 fields) | Relationship, SNOMED/ICD coding, diagnosis details |
| Social history | ✅ Covered | `Smoking Statuses` (12 fields), `Risk Factors` (5 fields), `Travel History` (7 fields), `Occupation and Industry History` (14 fields) | Unusually thorough — occupational data with NAICS/SOC codes, travel history, multiple tobacco type tracking |
| Devices | ✅ Covered | `Implantable device` (19 fields) | UDI, manufacturer, MRI safety, lot/serial, implant/explant dates |
| Custom forms | ⚠️ Partial | `User Defined Fields` (4 fields), `Patient Generated Data` (14 fields), `Tracked Data` (5 fields) | User Defined Fields uses a key-value structure (FieldValue, Template, DateEntered) that captures custom data but with minimal metadata. Digital intake forms from AC Patient Connect are not clearly represented. |

## 6. Documentation Quality

**Strengths:**
- Complete listing of all 44 data classes and their column headings
- Clear description of the export mechanism (per-patient folders, format options, population filters)
- Covers both individual and bulk export scenarios

**Weaknesses:**
- **No field descriptions**: None of the 1,102 columns have definitions. A developer would need to guess that "COSTAR" is a classification system, "HowMigrated" refers to data migration source, or "PendingFlag" means the record is pending clinical review.
- **No data types**: No indication whether a field is text, integer, date, boolean, or binary.
- **No value sets**: Fields like `ERXstatus`, `MaritalStatus`, `InsuranceType`, `OrderStatus`, `LabTestStatus` have no enumerated values.
- **No relationships**: No foreign keys or cross-references between data classes. Cannot determine which medications relate to which encounters, which orders generated which lab results, etc.
- **No sample data**: No example exports to illustrate actual content.
- **No machine-readable schemas**: No XSD, JSON Schema, or similar. The only documentation is this PDF.

**Developer usability**: A developer could parse the exported files using column names as headers, but understanding the semantics of many fields would require access to a sample export and domain knowledge. Fields like `NP001Description`, `NP001FriendlyName`, `CcdaGuidLabTestId`, `XLinkProviderID`, `VisitIdExternal` are opaque without definitions. The typos in column names (`FristName`, `Signetur`, `BillingProvideerState`, `OrderTypeDescriptin`) confirm these are raw database column names, not a polished API.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export covers the genuine breadth of what an ambulatory EHR stores. It includes 44 data classes spanning clinical documentation, medications, labs, billing, insurance, immunizations, orders, referrals, demographics, family/social history, devices, care planning, scheduling, custom fields, and documents. The inclusion of Billing History (74 fields with CPT/ICD/modifier/NDC/provider details) and Health Insurance (39 fields) is a strong signal — these are not USCDI domains and demonstrate the vendor went beyond clinical summary exchange. The export covers data domains that would never appear in a C-CDA or FHIR (g)(10) export: billing charges, insurance subscriber details, health maintenance rules, patient record releases, scheduling, and custom tracked data.

The main gap is **payment data** — the product has payment posting and remittance processing capabilities, but no payment or accounts receivable entity appears in the export. Patient portal messages may also be incomplete if they reside in the third-party Updox system rather than Amazing Charts' database. These are real but bounded gaps in an otherwise broad export.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export of the vendor's native database tables, not a repackaged clinical exchange format. Evidence:
1. Raw database column names with typos (`FristName`, `Signetur`, `BillingProvideerState`)
2. Format is CSV/JSON/XML flat files, not C-CDA or FHIR
3. Includes billing, insurance, scheduling, health maintenance rules, and administrative data — none of which would be in a (g)(10) FHIR API or C-CDA export
4. 1,102 total fields far exceed what any standard clinical exchange format covers
5. Separate pending/active states for allergies, problems, and medications show database-level data exposure

### Key Findings

1. **Purpose-built (b)(10) with genuine breadth**: 44 data classes with 1,102 fields covering clinical, billing, insurance, administrative, and custom data domains. This is not a repackaged clinical exchange — it's a native database export that significantly exceeds USCDI scope.

2. **Documentation is minimal — names only, no definitions**: Zero of 1,102 fields have descriptions, types, or value sets. The documentation provides column names as the sole metadata, making data interpretation dependent on domain expertise and sample data access.

3. **Billing and insurance data are included**: Billing History (74 fields) and Health Insurance (39 fields) are substantive data classes with CPT/ICD coding, charges, provider credentialing, and payer details — a strong signal of genuine (b)(10) compliance.

4. **Payment data is absent**: Despite the product having payment posting and remittance capabilities, no payment, accounts receivable, or patient statement entities appear in the export.

5. **Lab Tests is exceptionally detailed**: 126 fields covering the full lifecycle from ordering through specimen handling, result details (with LOINC, reference ranges, abnormal flags), and lab facility information.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   CSV, JSON, or XML (user-selectable)
    Entities:        44
    Fields:          1,102
    Descriptions:    0% (0 of 1,102 fields have descriptions)
    Sample data:     No
    Bulk export:     Yes (population-level with filters)
    Domains covered: 16 of 19 applicable domains (3 partial, 1 not covered)

### Bottom Line

Amazing Charts provides a genuine, purpose-built EHI export that covers the breadth of its ambulatory EHR data — clinical, billing, insurance, immunizations, orders, and administrative data across 44 data classes and 1,102 fields. The export's primary weakness is documentation quality: every field is a bare column name with no type, description, or value set, making downstream use challenging without sample data. The single biggest gap is the absence of payment/remittance data despite the product's payment posting capabilities.

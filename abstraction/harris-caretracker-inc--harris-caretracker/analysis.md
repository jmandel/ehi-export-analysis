# EHI Export Analysis: Harris CareTracker, Inc

**Product**: Harris CareTracker, Version 9  
**Analysis date**: 2026-02-15  
**CHPL ID**: 15.04.04.1569.Harr.09.00.1.180701 (CHPL #9589)

## 1. Product Context

Harris CareTracker is a cloud-based, unified EHR and practice management (PM) platform for ambulatory medical practices. Originally founded in 1995 as Lighthouse Medical Management (focused on revenue cycle management), the CareTracker EMR launched in 2007. The company was acquired by N. Harris Computer Corporation (a Constellation Software subsidiary) in 2014.

The product combines three core modules in a single integrated system:

- **EHR/Clinical**: Demographics, vital signs, allergies, medications, problem lists, diagnoses, prescriptions (including EPCS), clinical notes with specialty templates, lab orders/results, immunizations, clinical decision support, e-prescribing via Surescripts/DrFirst.
- **Practice Management/Billing/RCM**: Scheduling, charge capture, electronic claims submission with scrubbing, eligibility verification, ERA posting, denial management, collections, patient statements, and A/R reporting. The billing capabilities are a particular strength — the product serves over 1,600 medical billing companies.
- **Patient Portal/Engagement**: Portal for records viewing, messaging, prescription renewals, appointment requests, bill viewing/payment, and digital intake forms (via InteliChart partnership).

The product supports a broad range of ambulatory specialties including orthopedics, podiatry, pain management, psychiatry, internal medicine, family practice, gastroenterology, pulmonology, chiropractic, physical therapy, and mental health.

For EHI export assessment, the baseline expectation is that the export should cover clinical data, billing/claims data, insurance information, medications, labs, and patient communications — all of which the product stores natively.

## 2. Artifacts Reviewed

| Artifact | Description | Informational Value |
|---|---|---|
| `CareTracker-EHI-Export-Documentation-V1_0-1-1.pdf` | 8-page PDF (177,610 bytes). "CareTracker EHI Export: Folder Organization and Data Format Specification — v1.0." Created 2023-11-15 by Kathiresan Palanisamy using Acrobat PDFMaker 15 for Word. Lists 44 data classes with column headings. | **Primary artifact** — the only export documentation available. Contains all export structure and field information. |

This is a single-artifact analysis. The vendor provides one PDF document at the CHPL-registered URL. No sample data, no machine-readable schema, no supplemental documentation.

## 3. Export Mechanics

- **Format**: Three options — CSV, JSON, or XML (user-selectable)
- **Mechanism**: Purpose-built EHI export feature within the application (UI-driven). The PDF describes a "feature" for data export, not an API.
- **Single-patient**: Supported — creates a timestamped folder for one patient
- **Bulk export**: Supported — patient population export with selection by Provider, All Active Patients, All Patients, or Patients within an Encounter Range
- **Folder structure**: One folder per patient (timestamped), with one file per data class named `[Data Class Name].[format]` plus a "Documents" subfolder for imported items, images, and documents in their original format
- **Access constraints/fees**: Not documented in the specification

## 4. Export Content: What's In It

The export documentation defines **44 data classes** containing a total of **1,102 column headings** (fields). No field has a description, data type, value set, or relationship/foreign key documentation. The document is exclusively a column-heading inventory.

### Documentation depth

| Metric | Value |
|---|---|
| Total data classes | 44 |
| Total fields | 1,102 |
| Fields with descriptions | 0 (0%) |
| Fields with data types | 0 (0%) |
| Fields with value sets | 0 (0%) |
| Relationships/foreign keys documented | None |
| Sample data provided | No |
| Machine-readable schema | No |

### Vendor's own content organization

The vendor does not organize data classes into categories — they are listed alphabetically in the PDF. The following categorization is analyst-assigned based on content:

**Top 10 largest data classes (by field count):**

| Data Class | Fields | Category |
|---|---|---|
| Lab Tests | 126 | Lab Results |
| Clinical Notes | 89 | Clinical Documentation |
| HM Rules | 86 | Health Maintenance |
| Billing History | 74 | Billing |
| Patient Demographics | 62 | Demographics |
| Medications | 50 | Medications |
| HM Rules Ignored | 40 | Health Maintenance |
| Health Insurance | 39 | Insurance |
| Medications Pending | 38 | Medications |
| Immunizations | 37 | Immunizations |

**All 44 data classes:**

| Data Class | Fields | Category (analyst-assigned) |
|---|---|---|
| Addendum | 6 | Clinical Documentation |
| Advance Directives | 14 | Clinical Documentation |
| Alerts | 14 | Clinical Documentation |
| Allergies and Intolerances Pending | 26 | Clinical |
| Allergies and Intolerances | 25 | Clinical |
| Assesments [sic] | 5 | Clinical Documentation |
| Billing History | 74 | Billing |
| Care Team Members | 13 | Care Coordination |
| Clinical Notes | 89 | Clinical Documentation |
| Demographic Immunization | 8 | Immunizations |
| Email | 11 | Communications |
| FamilyHistory | 20 | Clinical |
| FunctionalStatus | 6 | Clinical |
| Goals | 5 | Care Planning |
| Health Concerns | 5 | Care Planning |
| Health Insurance | 39 | Insurance |
| HM Rules Ignored | 40 | Health Maintenance |
| HM Rules | 86 | Health Maintenance |
| Immunizations | 37 | Immunizations |
| Implantable device | 19 | Clinical |
| Imported Items | 16 | Documents |
| Injections | 14 | Clinical |
| Lab Tests | 126 | Lab Results |
| List Problem Pending | 18 | Clinical |
| List Problem | 17 | Clinical |
| Medications Pending | 38 | Medications |
| Medications | 50 | Medications |
| Next Of Kin | 17 | Demographics |
| Occupation and Industry History | 14 | Demographics |
| Orders | 24 | Orders |
| Patient Demographics | 62 | Demographics |
| Patient Generated Data | 14 | Patient Data |
| Patient Health Information Capture | 17 | Clinical Documentation |
| Patient Record Release | 26 | Administrative |
| Plan of Treatment | 5 | Care Planning |
| Procedures | 15 | Billing |
| Referrals | 12 | Orders |
| Risk Factors | 5 | Clinical |
| Scheduling | 14 | Administrative |
| Smoking Statuses | 12 | Clinical |
| Tracked Data | 5 | Clinical |
| Travel History | 7 | Public Health |
| User Defined Fields | 4 | Custom Data |
| Vital Signs | 28 | Clinical |

Full field inventory is in `analysis/full-entity-inventory.json`.

**Category breakdown:**

| Category | Data Classes | Total Fields |
|---|---|---|
| Clinical | 12 | 195 |
| Clinical Documentation | 6 | 145 |
| Health Maintenance | 2 | 126 |
| Lab Results | 1 | 126 |
| Demographics | 3 | 93 |
| Billing | 2 | 89 |
| Medications | 2 | 88 |
| Immunizations | 2 | 45 |
| Administrative | 2 | 40 |
| Insurance | 1 | 39 |
| Orders | 2 | 36 |
| Care Planning | 3 | 15 |
| Documents | 1 | 16 |
| Patient Data | 1 | 14 |
| Care Coordination | 1 | 13 |
| Communications | 1 | 11 |
| Public Health | 1 | 7 |
| Custom Data | 1 | 4 |

### Notable data class details

**Billing History** (74 fields): Remarkably detailed for an EHI export. Includes PlaceOfService, CPT codes with descriptions, fees, charges, units, pricing, NDC codes, up to 12 ICD diagnosis codes (ICD1–ICD12), modifiers, prior authorization numbers, and full provider details for both billing and referring providers (name, DEA, state license, UPIN, NPI, email). Also includes facility information (name, address, NPI, type).

**Clinical Notes** (89 fields): Comprehensive encounter documentation including chief complaint, HPI, review of systems, past medical history, medications, allergies, social history, family history, physical exam, assessment, plan, vitals (BP, temp, respiration, pulse, weight, height, BMI, head circumference, O2 saturation), tobacco use details, pregnancy data, vision/hearing, SNOMED codes, and image/illustration locations.

**Lab Tests** (126 fields): The largest data class. Three-level structure covering order-level, result-level, and result-detail-level data. Includes LOINC codes, specimen information, abnormal flags, reference ranges, performing lab details (name, address, director), and attached notes. Multiple date/timestamp fields for creation, updates, specimen collection, and result receipt.

**Patient Demographics** (62 fields): Full demographics including SSN, employer, emergency contact, marital status, race/ethnicity, language preference, sexual orientation, gender identity, maiden name, aliases, previous addresses, and occupation.

**Notable typos in field names** (likely reflecting actual export column headers): "Assesments" (sic), "Signetur" (sic), "OrderTypeDescriptin" (sic), "BillingProvideerState" (sic), "ReferProvideerState" (sic), "TestSigedOffDate" (sic), "RestultLastUpdatedDate" (sic), "FristName" (sic in Patient Demographics), "SubscriberFrist" (sic in Health Insurance).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers a genuinely broad range of patient data. The strongest areas are:

1. **Clinical data** (12 data classes, 195 fields): Deep coverage across allergies (with pending items), problems, vital signs, implantable devices, injections, smoking status, risk factors, functional status, and family history. The inclusion of "pending" variants (Allergies Pending, Medications Pending, List Problem Pending) is unusual and valuable — it captures in-progress clinical workflow state, not just finalized records.

2. **Clinical documentation** (6 data classes, 145 fields): Clinical Notes alone has 89 fields covering the full SOAP note structure. Addenda, advance directives, alerts, assessments, and patient health information capture add further depth.

3. **Lab results** (1 data class, 126 fields): Exceptionally detailed with three-level data (order → result → result detail), LOINC codes, performing lab info, specimen details, and notes.

4. **Billing** (2 data classes, 89 fields): The Billing History class is unusually comprehensive for an EHI export. Most vendors omit billing entirely; CareTracker exports CPT codes, ICD codes, fees, charges, NDC codes, modifiers, and full billing/referring provider details.

5. **Health maintenance/immunizations** (4 data classes, 171 fields): Very detailed vaccine administration records including VIS information, manufacturer, lot numbers, routes, sites, and registry submission dates. The HM Rules Ignored class tracks declined preventive care — useful clinical context.

6. **Demographics** (3 data classes, 93 fields): Comprehensive including occupation/industry history with NAICS/SOC codes.

**Thinner areas:**
- Care Planning (Goals, Health Concerns, Plan of Treatment): 3 data classes with only 5 fields each — essentially encounter-linked text blobs.
- Custom Data (User Defined Fields): Only 4 fields (PatientId, FieldValue, Template, DateEntered). Captures custom field data but with minimal structure.
- Tracked Data: 5 generic fields (PatientId, Item, Date, Value, Comments) — a key-value store for arbitrary tracked items.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (62 fields), `Next Of Kin` (17 fields), `Occupation and Industry History` (14 fields) | Thorough — includes SSN, employer, race/ethnicity, language, SOGI, aliases, previous addresses |
| Encounters / visits | ⚠️ Partial | Encounter dates embedded in `Clinical Notes`, `Billing History`, and other data classes; no dedicated encounter entity | No standalone encounter/visit record — encounter context is distributed across data classes via date fields |
| Problems / conditions / diagnoses | ✅ Covered | `List Problem` (17 fields), `List Problem Pending` (18 fields) | Both active and pending problems with ICD/SNOMED/COSTAR codes |
| Medications / prescriptions | ✅ Covered | `Medications` (50 fields), `Medications Pending` (38 fields) | Detailed: pharmacy info, e-prescribing status, DAW, NDC, compound meds, days supply, problem linkage |
| Allergies | ✅ Covered | `Allergies and Intolerances` (25 fields), `Allergies and Intolerances Pending` (26 fields) | Comprehensive with severity, reactions, dates, confirmation tracking |
| Immunizations | ✅ Covered | `Immunizations` (37 fields), `HM Rules` (86 fields), `Demographic Immunization` (8 fields) | Very detailed: VIS, manufacturer, lot, route, site, registry submission |
| Vitals | ✅ Covered | `Vital Signs` (28 fields), also embedded in `Clinical Notes` (89 fields) | Full vital panel including O2 saturation, pain scale, peak flow, vision, hearing |
| Lab results | ✅ Covered | `Lab Tests` (126 fields) | Exceptionally detailed — order/result/result-detail levels with LOINC, specimen info, performing lab |
| Imaging / diagnostic reports | ⚠️ Partial | `Imported Items` (16 fields) stores external documents including images; `Clinical Notes` references image/illustration locations | No dedicated radiology/imaging results entity — images appear to be handled as imported documents |
| Procedures | ✅ Covered | `Procedures` (15 fields), `Billing History` (74 fields) includes CPT-coded procedures | CPT codes, fees, charges, NDC codes documented |
| Clinical notes / documents | ✅ Covered | `Clinical Notes` (89 fields), `Addendum` (6 fields), `Imported Items` (16 fields) | Very detailed note structure; imported items preserved in original format |
| Care plans / goals | ✅ Covered | `Plan of Treatment` (5 fields), `Goals` (5 fields), `Health Concerns` (5 fields) | Present but thin — each has only 5 fields (essentially encounter-linked text) |
| Orders / referrals | ✅ Covered | `Orders` (24 fields), `Referrals` (12 fields) | Order tracking with CPT/ICD codes, status, and assignment info |
| Insurance / coverage | ✅ Covered | `Health Insurance` (39 fields) | Policy/group numbers, payer/plan info, subscriber and guarantor demographics |
| Claims / billing | ✅ Covered | `Billing History` (74 fields) | Unusually comprehensive — CPT, ICD (×12), fees, charges, NDC, modifiers, prior auth, billing/referring provider details |
| Payments | ❌ Not covered | No payment, ERA/remittance, or collections data class in export | Product processes ERA/remittance and tracks payments (see Section 1); this is a gap |
| Consents / directives | ✅ Covered | `Advance Directives` (14 fields), `Patient Record Release` (26 fields) | Includes directive text, codes, dates, and document paths |
| Patient communications / portal messages | ⚠️ Partial | `Email` (11 fields) covers provider-patient messages | Portal-specific interactions (appointment requests, prescription renewals, intake forms, online payments) not exported as discrete data classes |
| Specialty-specific data | ⚠️ Partial | `User Defined Fields` (4 fields), `Tracked Data` (5 fields), customizable `Clinical Notes` templates | Custom/specialty data captured via generic key-value structures rather than specialty-specific entities |

**Key gaps relative to product capabilities:**

1. **Payments/ERA/remittance/collections**: The product has robust ERA posting (95% accuracy claimed), denial management, collections module, and A/R tracking. None of this appears in the export. The Billing History captures charges and claims but not the payment/adjudication side.

2. **Encounter entity**: No dedicated encounter/visit data class. Encounters are implicitly represented via date fields across Clinical Notes, Billing History, etc., but there's no central encounter record with status, visit type, duration, etc.

3. **Patient portal activity**: Only email messages are exported. Portal-specific data (appointment requests, prescription renewal requests, document views, online payment records) is absent.

## 6. Documentation Quality

**What works:**
- The column headings are complete for all 44 data classes. A developer could use them to parse export files and map fields.
- Field names are mostly self-explanatory and follow consistent naming patterns (e.g., `FirstName`/`LastName` pairs, `Date*` prefixes, `Is*` for booleans).
- The folder structure explanation is clear: one folder per patient, one file per data class, documents subfolder for originals.
- Three format options (CSV, JSON, XML) provide flexibility.

**What's missing:**
- **No data types**: A developer cannot know without trial-and-error whether `DateOfService` is ISO 8601, MM/DD/YYYY, or epoch time; whether `Fee` is a decimal or string; whether `IsOpen` is true/false, 0/1, or Y/N.
- **No value sets**: Coded fields like `Chronicity`, `ERXstatus`, `DispenseAsWritten`, `TobaccoUseName`, `VisitType`, `OrderStatus`, `MedSource` have no documentation of allowed values.
- **No descriptions**: Some field names are opaque — `COSTAR`, `NP001Description`, `NP001FriendlyName`, `XLinkProviderID`, `Miscellaneous1`–`Miscellaneous4`, `QuickAddWhoPrescribed` — and have no explanation.
- **No relationships/foreign keys**: Data classes share `PatientID` and sometimes encounter dates, but the document does not specify how entities relate (e.g., how Billing History links to Clinical Notes for the same visit).
- **No sample data or examples**: No worked examples of actual export output.
- **No machine-readable schema**: No XSD, JSON Schema, or CSV header specification file.
- **Multiple typos in field names** that likely reflect actual column headers in the export: `Assesments`, `Signetur`, `OrderTypeDescriptin`, `BillingProvideerState`, `ReferProvideerState`, `TestSigedOffDate`, `RestultLastUpdatedDate`, `FristName`, `SubscriberFrist`.

**Could a developer build an import from this documentation alone?** Partially. The field names provide enough structure to parse and roughly map data, but a production-quality import would require significant reverse-engineering of data types, value sets, and inter-entity relationships.

## 7. Overall Assessment

### Classification

**Partial native export** — Native data model export with broad coverage across clinical and billing domains, but with thin documentation (column names only, no types/descriptions/value sets) and notable gaps in payment/ERA/collections data despite the product's strong billing capabilities.

### Key Findings

1. **Genuinely broad native export with 44 data classes and 1,102 fields.** This is clearly a purpose-built (b)(10) export, not a C-CDA or FHIR repackaging. The data classes reflect vendor-internal model names (e.g., `COSTAR` codes, `QuickAddWhoPrescribed`, `NP001Description`), and the inclusion of in-progress workflow states (Pending allergies, medications, problems) goes beyond what any standard projection would provide.

2. **Billing data is unusually comprehensive.** The `Billing History` data class (74 fields) includes CPT codes, up to 12 ICD diagnosis codes, fees, charges, NDC codes, modifiers, prior authorization numbers, and full billing/referring provider details. Most EHI exports omit billing entirely; CareTracker's inclusion is a notable strength.

3. **Documentation is thin — column headings only.** Zero of the 1,102 fields have descriptions, data types, or value sets documented. The 8-page PDF is essentially a field inventory, not a data dictionary. This limits the practical usability of the export for downstream systems.

4. **Payment/ERA/remittance/collections data is absent.** Despite the product's strong billing and revenue cycle management capabilities (ERA posting, denial management, collections module), the export captures charges/claims but not the payment/adjudication side. This is the most significant content gap.

5. **Typos in field names suggest limited QA review.** At least 9 typographical errors in column headings (`BillingProvideerState`, `FristName`, `Signetur`, etc.) suggest the specification may have been produced quickly without thorough review. These likely reflect actual column names in the export output.

### Summary Stats

```
Classification:  Partial native export
Export format:   CSV, JSON, or XML (user-selectable)
Model type:      Native database (vendor-specific data classes)
Entities:        44
Fields:          1,102
Descriptions:    0% (no field descriptions)
Sample data:     No
Bulk export:     Yes (population-level with flexible patient selection)
Domains covered: 14 of 18 applicable domains (fully or partially)
```

### Bottom Line

Harris CareTracker provides a genuinely substantive EHI export that goes well beyond a clinical summary — 44 native data classes covering clinical, billing, insurance, lab, immunization, and administrative data. However, the documentation is thin (field names only, no types or descriptions), and there is a notable gap in payment/ERA/remittance data despite the product's strong billing capabilities. A patient would get a broad copy of their clinical and billing records, but the missing payment/collections data means the financial picture is incomplete.

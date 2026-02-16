# EHI Export Analysis: PointClickCare Technologies Inc.

**Product**: PointClickCare (CHPL 10246), EHR for Practice Groups (CHPL 11729)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2181.Poin.04.00.1.191231, 15.04.04.2181.Poin.03.01.1.251208

## 1. Product Context

PointClickCare is the dominant cloud-based EHR for long-term and post-acute care (LTPAC), serving 27,000+ providers across skilled nursing facilities (SNFs), assisted living, memory care, and continuing care retirement communities. It is rated #1 in LTC software by KLAS Research for six consecutive years.

The platform encompasses:

- **Core EHR/Clinical**: Point-of-care charting (vitals, assessments, wound care, infection control), care plans, progress notes, physician orders (CPOE), diagnosis management, MDS 3.0 assessments with iQIES submission, and nursing documentation.
- **Medication Management**: Electronic MAR (QuickMAR), bar-coded medication administration, ePrescribing (including EPCS), pharmacy integration, drug interaction alerts.
- **Revenue Cycle Management**: Claims processing (Medicare, Medicaid, private), PDPM scoring, accounts receivable, census management, trust fund management, billing statements, collections.
- **Care Coordination**: Secure messaging, hospital admission/readmission alerts, electronic discharge summaries, insurance coverage validation.
- **Assessments**: MDS 3.0 (federally mandated for SNFs), plus non-MDS assessments including SDOH and health status screenings.
- **Documents**: Progress notes, advanced directives, consent documents, radiology reports, skin/wound documentation, therapy files.
- **Patient/Family Engagement**: Patient portal, clinician/family portals, automated care messaging.

The "EHR for Practice Groups" (CHPL 11729) shares the same underlying data platform and the same EHI export documentation URL. It provides a practitioner-facing interface for physicians and NPs serving LTPAC populations.

**Baseline for completeness**: A genuine EHI export should cover clinical documentation, medications/eMAR, orders, assessments (MDS and non-MDS), billing/claims, payments, census/ADT, care coordination, documents/attachments, and specialty data relevant to long-term care (wound care, care profiles, diet orders).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/package.tgz` | FHIR IG NPM package (479 KB): 67 StructureDefinitions, 2 ValueSets, 2 CodeSystems in machine-readable JSON | **Primary source** — full computable schema |
| `downloads/site/index.html` | IG home page: export mechanics, format description, sample NDJSON, directory structure | **High** — export format and mechanics |
| `downloads/site/MDS.html` | MDS 3.0 assessment CSV schema: 7 CSV files, 166 columns, all with descriptions | **High** — assessment export detail |
| `downloads/site/NonMDS.html` | Non-MDS assessment CSV schema: 5 CSV files, 59 columns including SDOH | **High** — assessment breadth |
| `downloads/site/artifacts.html` | IG artifacts summary listing all profiles, extensions, terminologies | **Medium** — navigation/overview |
| `downloads/site/toc.html` | Table of contents for the IG | **Low** — structure only |
| `downloads/site/StructureDefinition-*.html` (67 files) | HTML rendering of each StructureDefinition with snapshot tables | **Medium** — human-readable versions of package JSON |
| `downloads/site/CodeSystem-*.html` (2 files) | Immunization status and order status code systems | **Medium** — terminology detail |
| `downloads/site/ValueSet-*.html` (2 files) | Value sets for immunization and order status | **Medium** — terminology detail |
| `downloads/enrichment/structure-definitions.json` | Pre-extracted structured data from StructureDefinitions | Reference only (verified independently) |
| `downloads/enrichment/csv-schemas.json` | Pre-extracted CSV schema data | Reference only (verified independently) |

## 3. Export Mechanics

- **Format**: Mixed — FHIR R4 NDJSON for clinical/billing/administrative data; CSV for MDS and non-MDS assessments; raw files for documents and attachments.
- **Delivery**: Encrypted compressed files. Encryption keys obtained through PointClickCare documentation (not publicly specified).
- **Scope**: Single-patient export generates one artifact per patient; population export generates artifacts containing multiple patients.
- **Structure**: Per-patient directory containing:
  - FHIR NDJSON files (patient resource, clinical data, billing data, index files for referenced entities)
  - `mds_assessments/` — per-assessment CSV files (7 files per assessment)
  - `non_mds_assessments/` — per-assessment CSV files (5 files per assessment)
  - `Files/` — consent and advance directive documents
  - `radiology-attachments/` — radiology images
  - `lab-attachments/` — lab result attachments
- **Access**: Export appears to be initiated within the PointClickCare application (UI-based). Both single-patient and bulk export capabilities exist.
- **Custom resources**: EHI is output as "both standard FHIR R4 and non-FHIR custom resources." Custom resources conform to FHIR Base Resource requirements (id and meta elements) but define vendor-specific structure.

## 4. Export Content: What's In It

The export is documented through a formal FHIR R4 Implementation Guide (v0.1.0, built 2026-02-04) with machine-readable StructureDefinitions for every exported entity.

### Summary Statistics

| Metric | Count |
|---|---|
| FHIR Resource Profiles (USCDI-aligned) | 25 |
| Custom FHIR Resources (beyond USCDI) | 8 |
| Other FHIR Resource Profiles | 3 |
| FHIR Extensions | 31 (24 vendor-specific + 7 US Core) |
| CSV Schema Entities (MDS) | 7 files, 166 columns |
| CSV Schema Entities (Non-MDS) | 5 files, 59 columns |
| **Total Entities** | **48** |
| **Total Fields** | **1,679** |
| Fields with Description | 1,679 (100.0%) |
| Fields with Type | 1,677 (99.9%) |
| Code Systems | 2 (immunization-status, order-status) |
| Value Sets | 2 |

### Vendor's Content Organization

#### Custom Resources (Beyond USCDI) — 8 entities, 173 fields

These are the strongest signal that this is a purpose-built export. Each is a vendor-defined FHIR-like resource with no standard FHIR equivalent:

| Entity | Direct Fields | Category | Description |
|---|---|---|---|
| EHIOrder | 36 | Orders | Non-pharmacy orders: diet, lab, diagnostic, immunization. Includes diet texture, fluid consistency, diet supplements, LOINC codes, POCT device info. |
| EHIClaim | 29 | Billing | Insurance claims with revenue codes, HIPPS codes, service dates/units, charges, non-covered charges, payer, NPI, insured info, federal tax number, care level, daily rate. |
| EHICensus | 27 | ADT/Census | Patient census/admission tracking: ADT actions, payer setup, status (active/hospital leave/therapeutic leave), room/rate, admission type/source, discharge status, HIPPS, qualifying hospital stay. |
| EHIPayment | 19 | Billing | Payment records: receipt amount, trust fund amount, AR amount, payer description/type, cash receipt type. |
| EHIAuthorization | 18 | Insurance | Prior authorization: payer, insurance, start/end dates, review date, request status/type, exclusions, comments. |
| EHIBillingStatement | 18 | Billing | Patient billing statements: statement date, invoice transactions, balance due, previous balance, payments, current charges, total due. |
| EHICareProfile | 13 | Clinical | Care profile questionnaire data: category name, question text, answer value. Categories include auxiliary devices, services, dietary needs. |
| EHIInvoiceTransaction | 13 | Billing | Billing line items: effective date, description, units, unit amount, total amount. |

#### FHIR Resource Profiles (USCDI-aligned) — 25 entities, 1,194 fields

Standard FHIR R4 resources with PointClickCare-specific constraints and 24 vendor extensions:

| Entity | Elements | Direct Fields | Notable Extensions/Features |
|---|---|---|---|
| EHIMedicationRequest | 134 | 48 | RouteOfAdministration, ScheduleStartDate, TimeCode, AdministeredBy extensions; dose quantity, frequency, timing, pharmacy details |
| EHIAllergyIntolerance | 74 | 29 | RecordedBy, ResolvedDate, RevisionBy, RevisionDate extensions — audit trail for allergy records |
| EHIEncounter | 72 | 31 | Standard encounter profiling |
| EHICoverage | 65 | 31 | PayerDescription, PayerType, MedicareAdvantagePlan, CompanyName, ProviderNumber extensions |
| EHIImmunization | 63 | 37 | ImmunizationStatus extension with vendor code system |
| EHIMedication | 60 | 16 | RxNorm coding, form, strength, unit of measure |
| EHICarePlan | 59 | 31 | Standard care plan profiling |
| EHIPatient | 54 | 34 | PreviousName, Occupation extensions + US Core race/ethnicity/sex/gender/tribal/pronouns |
| EHIObservation | 49 | 32 | Vitals, occupation, smoking status, pregnancy status/intent |
| EHIProcedure | 49 | 38 | Standard procedure profiling |
| EHISpecimen | 47 | 21 | Lab specimen details |
| EHIDocumentReference | 44 | 24 | Progress Notes, Advanced Directives, Consent, Radiology Report, Skin Wound, Therapy Files |
| EHIMedicationDispense | 44 | 32 | Medication dispensing records |
| EHIServiceRequest | 41 | 41 | Service/referral requests |
| EHILocation | 38 | 25 | Facility location details |
| EHICondition | 36 | 25 | Context extension |
| EHIFamilyMemberHistory | 34 | 26 | Family health history |
| EHIPractitionerRole | 34 | 22 | Provider roles |
| EHIDiagnosticReport | 31 | 26 | Lab and diagnostic results |
| EHIProvenance | 31 | 18 | Data provenance tracking |
| EHIGoal | 30 | 24 | Patient goals |
| EHICareTeam | 28 | 21 | Care team membership |
| EHIPractitioner | 27 | 20 | Provider demographics |
| EHIOrganization | 25 | 18 | Organization details |
| EHIRelatedPerson | 25 | 20 | Patient contacts/relations |

#### Other Resource Profiles — 3 entities, 87 fields

| Entity | Elements | Description |
|---|---|---|
| EHIImplantableDevice | 65 | Implantable device tracking |
| EHIMedicalDevice | 11 | Medical device records |
| EHISingleDevice | 11 | Individual device instances |

#### CSV Assessment Export (MDS) — 7 files, 166 columns

All columns have descriptions, types, and nullability documented:

| CSV File | Columns | Description |
|---|---|---|
| assessment.csv | 90 | Core MDS assessment metadata: assessment type, dates, status, ADL scores, RUG/PDPM classifications, CMI weights, therapy minutes, clinical indicators |
| pdpmScores.csv | 35 | PDPM (Patient-Driven Payment Model) scoring: CMI weights by category (PT, OT, SLP, nursing, NTA), case mix groups, therapy days |
| responses.csv | 15 | Individual MDS item responses: section code, question number, response value, skip patterns |
| sections.csv | 9 | MDS section metadata: section code, name, status, completion dates |
| sectionV.csv | 9 | Section V (CAA) data: care area triggers, assessment results |
| sectionVRapProfile.csv | 6 | Section V RAP/CAA profiles: trigger status, care planning decisions |
| score.csv | 2 | RUG/PDPM calculation score summaries |

#### CSV Assessment Export (Non-MDS) — 5 files, 59 columns

| CSV File | Columns | Description |
|---|---|---|
| assessment.csv | 25 | Non-MDS assessment metadata and scoring |
| sdoh_and_health_status_responses.csv | 14 | SDOH screening and health status responses: question keys, coded answers, LOINC codes, score calculations |
| responses.csv | 9 | Assessment item responses |
| sections.csv | 9 | Assessment section metadata |
| score.csv | 2 | Score summaries |

### Vendor-Specific Extensions (24)

Beyond US Core standard extensions, PointClickCare defines 24 vendor-specific extensions that enrich the standard FHIR resources:

- **Medication management**: AdministeredBy, RouteOfAdministration, ScheduleStartDate, TimeCode
- **Audit/provenance**: RecordedBy, RevisionBy, RevisionDate, ResolvedDate
- **Insurance/billing**: PayerDescription, PayerType, MedicareAdvantagePlan, CompanyName, ProviderNumber
- **Orders**: OrderCategory, OrderType, OrderedBy, LoincOrderCode, LoincOrderCodes
- **Communication**: CommunicationMethod, Context, Custodian
- **Demographics**: Occupation, PreviousName, ImmunizationStatus

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

PointClickCare organizes its EHI export into three streams:

1. **FHIR R4 NDJSON** (36 resource types): Covers clinical, billing, insurance, and administrative data. The 8 custom resources (Authorization, BillingStatement, CareProfile, Census, Claim, InvoiceTransaction, Order, Payment) are the most distinctive — they represent data domains with no standard FHIR mapping, demonstrating purpose-built export work. The 25 USCDI-aligned profiles go beyond bare US Core with 24 vendor-specific extensions adding audit trails, medication administration details, and insurance specifics.

2. **MDS Assessment CSVs** (7 files, 166 columns): Deep export of MDS 3.0 assessment data — the cornerstone of SNF clinical and reimbursement workflows. Includes assessment metadata, section responses, PDPM scoring, RUG calculations, and CAA triggers. This is highly specific to the LTPAC domain and not available through standard FHIR.

3. **Non-MDS Assessment CSVs** (5 files, 59 columns): Broader assessment export including SDOH screenings and health status assessments with LOINC-coded responses.

4. **File attachments**: Consent/advance directive documents, radiology images, lab attachments exported as raw files.

**Richest areas**: Billing (4 custom resources: Claim, BillingStatement, InvoiceTransaction, Payment), medications (MedicationRequest at 134 elements is the largest profile), assessments (225 CSV columns across MDS and non-MDS), and orders (custom Order resource with 36 fields covering diet, lab, diagnostic, and immunization orders).

**Thinnest areas**: CareProfile (13 elements — a simple category/question/answer structure) and InvoiceTransaction (13 elements — basic line item data).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `EHIPatient` (54 elements), Occupation/PreviousName extensions, `EHIRelatedPerson` (25 elements) | Thorough — includes US Core race/ethnicity/sex/gender/tribal/pronouns plus vendor extensions |
| Encounters / visits | ✅ Covered | `EHIEncounter` (72 elements) | Solid |
| Problems / conditions | ✅ Covered | `EHICondition` (36 elements) with Context extension | Solid |
| Medications / prescriptions | ✅ Covered | `EHIMedicationRequest` (134 elements), `EHIMedication` (60), `EHIMedicationDispense` (44) — RouteOfAdministration, ScheduleStartDate, TimeCode, AdministeredBy extensions | Very deep — strongest single domain |
| Allergies | ✅ Covered | `EHIAllergyIntolerance` (74 elements) with RecordedBy, ResolvedDate, RevisionBy, RevisionDate audit extensions | Deep — includes full audit trail |
| Immunizations | ✅ Covered | `EHIImmunization` (63 elements) with ImmunizationStatus extension and vendor code system | Solid |
| Vitals | ✅ Covered | `EHIObservation` (49 elements) — vitals, smoking status, pregnancy status/intent | Solid |
| Lab results | ✅ Covered | `EHIDiagnosticReport` (31), `EHISpecimen` (47), `EHIObservation`, plus `lab-attachments/` folder | Solid — includes attachments |
| Imaging / diagnostic reports | ✅ Covered | `EHIDiagnosticReport` (31), `EHIOrder` (diagnostic type), `radiology-attachments/` folder | Solid — includes image attachments |
| Procedures | ✅ Covered | `EHIProcedure` (49 elements) | Solid |
| Clinical notes / documents | ✅ Covered | `EHIDocumentReference` (44 elements) — progress notes, advanced directives, consent, radiology reports, skin/wound docs, therapy files, plus `Files/` folder | Good breadth of document types |
| Care plans / goals | ✅ Covered | `EHICarePlan` (59), `EHIGoal` (30), `EHICareProfile` (13) | Solid |
| Orders / referrals | ✅ Covered | `EHIOrder` (36) — diet, lab, diagnostic, immunization orders; `EHIServiceRequest` (41) | Deep — custom Order resource covers non-pharmacy orders with diet-specific fields |
| Insurance / coverage | ✅ Covered | `EHICoverage` (65 elements) with MedicareAdvantagePlan, PayerDescription, PayerType, CompanyName, ProviderNumber extensions; `EHIAuthorization` (18) for prior auths | Deep — purpose-built prior authorization resource |
| Claims / billing | ✅ Covered | `EHIClaim` (29), `EHIBillingStatement` (18), `EHIInvoiceTransaction` (13) — revenue codes, HIPPS, charges, service units, daily rates | Genuine billing export — 4 dedicated billing entities |
| Payments | ✅ Covered | `EHIPayment` (19) — receipt amount, trust fund amount, AR amount, payer details, cash receipt type | Dedicated payment resource |
| MDS Assessments | ✅ Covered | 7 CSV files, 166 columns — assessment metadata, section responses, PDPM scores, RUG calculations, CAA triggers | Very deep — specialty-specific |
| Non-MDS Assessments / SDOH | ✅ Covered | 5 CSV files, 59 columns — includes SDOH screenings with LOINC-coded responses | Includes SDOH, a growing focus area |
| Census / ADT | ✅ Covered | `EHICensus` (27) — admission, discharge, transfers, hospital/therapeutic leave, payer setup, room/rate, qualifying hospital stay | Deep — specialty-specific to LTPAC |
| Consents / directives | ✅ Covered | `EHIDocumentReference` for consent/advance directive docs, `Files/` folder for attachments | Covered |
| Devices | ✅ Covered | `EHIImplantableDevice` (65), `EHIMedicalDevice` (11), `EHISingleDevice` (11) | Solid |
| Family health history | ✅ Covered | `EHIFamilyMemberHistory` (34) | Solid |
| Care team | ✅ Covered | `EHICareTeam` (28), `EHIPractitioner` (27), `EHIPractitionerRole` (34) | Solid |
| Provenance | ✅ Covered | `EHIProvenance` (31) | Solid |
| Specialty: Wound care | ⚠️ Partial | `EHIDocumentReference` includes "Skin Wound" files, but no dedicated wound assessment resource | Product has a wound care module; only document-level export, no structured wound data |
| Specialty: Infection control | ❌ Not covered | No infection control entities | Product has an infection prevention module; not represented in export |
| Patient communications | ❌ Not covered | No secure messaging/communication entities | Product has Secure Conversations module; not in export |
| Medication administration records (MAR) | ⚠️ Partial | `EHIMedicationDispense` covers dispensing; `EHIMedicationRequest` has AdministeredBy/TimeCode extensions | No dedicated MAR entity despite eMAR being a core module; administration details captured via extensions on requests |

## 6. Documentation Quality

**Excellent.** PointClickCare has produced one of the strongest EHI export documentation sets:

- **Machine-readable**: Full FHIR R4 Implementation Guide with a downloadable NPM package (`package.tgz`) containing all 67 StructureDefinitions as parseable JSON. This is the gold standard for documentation — a developer can programmatically consume the schema.
- **100% description coverage**: Every field across all 48 entities (1,679 fields) has a description. Every field has a type. This is rare.
- **Structured CSV schemas**: MDS and non-MDS CSV files are documented with column name, data type, nullability, and description for all 225 columns.
- **Vendor-defined code systems**: Custom code systems for immunization status and order status with enumerated values.
- **Sample data**: The index page includes inline NDJSON examples showing actual resource structure with realistic (synthetic) data.
- **Export structure documentation**: Clear description of the per-patient directory layout including FHIR files, assessment folders, and attachment folders.

**Minor gaps**:
- Foreign key relationships between resources are described narratively (on the index page) rather than formally in the StructureDefinitions.
- The 24 vendor extensions are defined as FHIR extensions but some have minimal descriptions (e.g., "Context", "Custodian" — single-word descriptions).
- No separate sample export package is provided for download.
- Encryption key distribution is referenced but not documented in the IG.

**Could a developer build an import?** Yes. The combination of machine-readable StructureDefinitions, described fields, sample data, and clear format specification (NDJSON + CSV) makes this actionable. A developer would need to handle the custom resources (non-standard FHIR types) and the CSV assessment format, but the documentation supports this.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

PointClickCare's export demonstrably covers the breadth of data domains relevant to long-term and post-acute care EHR systems. It goes well beyond USCDI:

- **Billing**: 4 dedicated custom resources (Claim, BillingStatement, InvoiceTransaction, Payment) covering claims, statements, line items, and payments — this is the clearest signal of a genuine EHI export.
- **Insurance**: Coverage profile with 5 vendor extensions plus a dedicated Authorization resource for prior authorizations.
- **Census/ADT**: Custom Census resource with 27 fields covering the full SNF census lifecycle (admission types, hospital/therapeutic leave, payer setup, qualifying hospital stays).
- **Assessments**: Deep MDS 3.0 export (166 CSV columns) and non-MDS assessments (59 columns including SDOH) — these are specialty-specific to LTPAC and not available through any standard clinical exchange.
- **Orders**: Custom Order resource covering diet orders (texture, fluid consistency, supplements), lab orders, diagnostic orders, and immunization orders — LTPAC-specific order types not in standard FHIR.

The few gaps (wound care structured data, infection control, secure messaging, dedicated MAR) are relatively minor compared to the overall coverage. The product stores wound care and infection data, but the export covers these partially through DocumentReference. For a long-term care EHR, covering billing, MDS assessments, census, and diet orders is far more significant than missing structured wound assessments.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged (g)(10) API:

1. **8 custom FHIR-like resources** (Authorization, BillingStatement, CareProfile, Census, Claim, InvoiceTransaction, Order, Payment) that have no equivalent in the FHIR standard or US Core. These were created specifically for EHI export.
2. **24 vendor-specific extensions** added to standard FHIR resources to capture EHR-specific data (audit trails, medication administration details, insurance specifics, LTPAC-specific fields).
3. **CSV assessment export** — a parallel format for MDS 3.0 and non-MDS assessments, recognizing that FHIR is not the right fit for CMS-mandated assessment instruments.
4. **A formal FHIR Implementation Guide** built with the HL7 IG Publisher toolchain — this required significant engineering investment.
5. **File attachment export** — consent documents, radiology images, and lab attachments are exported alongside structured data.

The (g)(10) API (US Core) would provide approximately 26 standard FHIR resource types covering USCDI. This export adds 8 custom resource types, 24 vendor extensions, and 12 CSV schema entities covering billing, payments, census, prior authorizations, MDS/non-MDS assessments, and LTPAC-specific order types. The distinction is clear.

### Key Findings

1. **Genuine purpose-built EHI export with billing coverage**: The 4 billing/payment custom resources (Claim, BillingStatement, InvoiceTransaction, Payment) are the strongest evidence this is a real (b)(10) effort. Most vendors omit billing entirely.

2. **Deep LTPAC-specific content**: The MDS 3.0 assessment export (166 CSV columns), Census resource (27 fields for SNF ADT lifecycle), and Order resource (diet orders with texture/fluid consistency/supplements) reflect genuine engagement with what long-term care facilities actually need exported.

3. **Machine-readable IG with 100% field documentation**: Every one of 1,679 fields across 48 entities has a description and type. The FHIR IG NPM package (`package.tgz`) is a rare example of fully computable EHI export documentation.

4. **Mixed format strategy is appropriate**: Using FHIR R4 NDJSON for clinical/billing data and CSV for CMS assessment instruments (MDS 3.0) is a pragmatic choice that leverages each format's strengths.

5. **Minor gaps in specialty modules**: Wound care (documented only as files, not structured data), infection control, and secure messaging are not explicitly represented despite being product features. The eMAR is covered through MedicationRequest extensions rather than a dedicated resource.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   FHIR R4 NDJSON + CSV + file attachments
    Entities:        48 (36 FHIR resources + 12 CSV schemas)
    Fields:          1,679
    Descriptions:    100.0% of fields
    Sample data:     Yes (inline examples in IG)
    Bulk export:     Yes (population export supported)
    Domains covered: 21 of 24 applicable domains

### Bottom Line

PointClickCare has built one of the strongest (b)(10) EHI exports reviewed. A patient or provider would receive a comprehensive, well-documented export covering clinical data, billing records, insurance claims, payments, MDS assessments, census history, and care profiles — delivered in machine-readable FHIR R4 and CSV formats with 100% field-level documentation. The biggest strength is the genuine inclusion of billing/financial data (4 custom resources) and LTPAC-specific content (MDS assessments, census, diet orders) that go far beyond what a repackaged (g)(10) API would provide.

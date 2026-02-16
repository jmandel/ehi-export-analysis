# EHI Export Analysis: Elation Health, Inc.

**Product**: Elation EMR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2717.Elat.03.00.1.181231 (CHPL #9876)

## 1. Product Context

Elation EMR is a cloud-based, all-in-one EHR, billing, and practice management platform purpose-built for ambulatory primary care. It serves 46,000+ clinical users and 24M+ patients, primarily in small-to-medium independent practices (1–10 physicians), including a strong Direct Primary Care (DPC) niche. Won Best in KLAS 2025–2026 for Small Practice Ambulatory EHR/PM.

Key data domains the product stores:
- **Clinical charting**: demographics, problem lists, medications, allergies, vitals, clinical notes (including AI-generated via "Note Assist"), lab results, imaging reports, procedures, immunizations, care team, referrals, social history, family health history
- **ePrescribing**: Rx/OTC/controlled substances via Surescripts, including EPCS
- **Orders**: Lab, imaging, pulmonary, cardiac, sleep orders
- **Billing (Elation Billing)**: charge capture, claim submission, ERA posting, copay collection, accounts receivable, patient liability, payment processing, eligibility verification
- **Patient portal (Patient Passport)**: secure messaging, appointment scheduling, prescription refills, intake forms, online bill pay
- **Referral management**: provider directory, electronic chart sharing, close-the-loop tracking
- **Documents**: uploaded files, scanned/faxed documents, letters
- **Scheduling**: appointments, visit types, reminders
- **Telehealth**: integrated Zoom-based visits
- **DPC/Membership**: recurring membership fee management

This sets the baseline: a genuine (b)(10) export should cover clinical, billing, patient communication, documents, scheduling, and insurance data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/elation-designated-record-set-ehi-export.pdf` (87 KB, 7 pages) | Primary data dictionary: "Elation's Designated Record Set for EHI Export." Lists 200 data elements organized by category, with descriptions and export format indicators (Computable PDF, XML, JSON, CSV). Created from Google Sheets, dated 2/6/2024. | **Most informative** — sole data dictionary |
| `downloads/ehi-export-criteria-page.html` (6 KB) | Help center article explaining the EHI export requirement, how to trigger single-patient and bulk exports, confidential notes policy, and FAQs. Last updated Sep 18, 2024. | **Informative** — explains export mechanics |
| `downloads/ehi-export-criteria-snapshot.txt` (17 KB) | Accessibility tree text snapshot of the help center article | Redundant with HTML |
| `downloads/ehi-export-criteria-page.png` (840 KB) | Full-page screenshot of the help center article | Redundant with HTML |
| `downloads/pdf-pages/page-[1-7].png` | Rendered page images of the PDF data dictionary (200 DPI) | **Useful** for verifying PDF parsing accuracy |
| `downloads/enrichment/data-dictionary.json` (53 KB) | Structured JSON extraction of 199 data elements from the PDF (prior enrichment pipeline). Missing 1 multi-line entry. | **Useful** as parsing baseline |
| `downloads/enrichment/coverage-summary.json` (790 B) | Aggregate statistics from enrichment extraction | Useful cross-check |

No sample data files, no machine-readable schemas (JSON Schema, XSD), and no FHIR/C-CDA artifacts were provided.

## 3. Export Mechanics

- **Format(s)**: Mixed — data is exported in four formats depending on the data element: Computable PDF, XML, JSON, and CSV. Each data element is tagged with the format(s) it exports in. Of 200 elements: 63 export as Computable PDF, 11 as XML, 106 as JSON, 64 as CSV. Many elements export in multiple formats.
- **Mechanism**: Single-patient export is UI-driven: navigate to patient chart → More → Data Exchange → Export Entire Health Information (EHI). Requires Admin privileges. Export is delivered via two emails (download link + password), with a 6-day download window.
- **Single-patient**: Yes, supported via UI.
- **Bulk capability**: Yes — providers can request a full patient panel export from Elation. Bulk exports may incur additional costs ("expedited exports and customized exports which may include a cost").
- **Access constraints**: Admin-level privileges required for single-patient exports. Confidential Notes (items tagged "Keep this Confidential" or "Mark Confidential") are excluded by default for patient-requested exports; bulk exports offer an option to include/exclude them.
- **Fees**: Customized/expedited exports may include a cost (per help center article).

## 4. Export Content: What's In It

The export is documented via a 7-page PDF data dictionary ("Elation's Designated Record Set for EHI Export") listing 200 data elements across 14 logical categories. Each element has a name, description, and one or more export format flags.

**Documentation quality**:
- **200 data elements** across 14 categories
- **199 of 200** (99.5%) have descriptions — only "Medical History Report" lacks one
- **No data types** are documented (no field-level types like string, integer, date)
- **No foreign keys or relationships** documented
- **No value sets or code systems** specified (e.g., no enumeration of valid values for billing status, appointment status, etc.)
- **No sample data** provided
- **No machine-readable schema** (no JSON Schema, XSD, or FHIR StructureDefinition)

### Vendor's own content organization

The data dictionary organizes content into these categories:

| Entity/Category | Fields | Described | Primary Format | Notes |
|---|---|---|---|---|
| Imaging Reports | 1 | 1 | Computable PDF | Single element for imaging results/documents |
| Appointments | 6 | 6 | CSV | Type, date/time, status, description, provider, duration |
| Patient Demographics | 57 | 57 | CSV/PDF | Name, DOB, gender, race, address, phone, email, insurance (primary+secondary), emergency contacts, pharmacy info, notes |
| Medications | 5 | 5 | Computable PDF | OTC, temporary, discontinued, permanent Rx, immunizations |
| Care Team & Documents | 3 | 3 | Computable PDF | Providers list, uploaded files, messages |
| Clinical Records | 10 | 9 | Computable PDF/XML | Problem list, procedures, vitals, allergies, visit notes, lab results, referrals, letters, medical history report, orders (lab/imaging/pulmonary/cardiac/sleep) |
| Additional Demographics | 2 | 2 | CSV | Sexual orientation, deceased date |
| Guarantor Information | 9 | 9 | CSV | First/last/middle name, address, phone, relationship, city, state, zip |
| Patient Status | 1 | 1 | CSV | Living/deceased |
| Social History | 1 | 1 | Computable PDF | Substance use |
| Eligibility/Insurance Verification | 14 | 14 | JSON | Timestamps, patient/insurance IDs, service type codes, subscriber, plan details, benefits, copay, coinsurance, deductible, out-of-pocket, limitations |
| Billing - Bills | 53 | 53 | JSON | Bill objects with IDs, service dates, billing status/errors, CPT codes, modifiers, DX codes (ICD-9/10), charges, units, payments, provider references (billing/rendering/supervising/ordering/referring), service locations (with CMS place-of-service codes), visit note associations, prior authorization, metadata |
| Billing - Patient Liability | 29 | 29 | JSON | Liability objects with payment status, amounts, patient/practice IDs, invoice numbers, payment charges (status, completion, refund timestamps, processor info), billing addresses |
| Billing - Payment Requests | 9 | 9 | JSON | Payment request objects with status, collection timestamps, reminder timestamps, amounts, date of service, external memos |

**Notable structural observations**:
- Clinical records are exported primarily as Computable PDF and XML — these are document-level exports, not granular field-level data. "Visit Note," "Lab Results," "Referrals," and "Letters" each appear as a single data element, not decomposed into component fields.
- Billing data is the most granular section (91 total fields across Bills, Patient Liability, and Payment Requests), all exported as JSON with detailed field-level structure including nested objects (CPT lines, provider objects, location objects, payment charges).
- Demographics (57 fields) and billing (91 fields) account for 74% of all data elements.
- The 4 clinical record elements exported as XML (Problem List, Procedures, Vitals, Allergies) suggest structured data — but no XML schema is documented.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Using the vendor's own categories:

**Richest sections**:
- **Billing - Bills** (53 fields): Genuinely deep — includes CPT codes with modifiers, ICD-9/10 diagnosis codes, charge amounts, multiple provider roles (billing, rendering, supervising, ordering, referring) with NPI numbers, service locations with CMS place-of-service codes, prior authorization numbers, and timestamps. This is real billing data, not a summary.
- **Patient Demographics** (57 fields): Thorough — includes primary and secondary insurance, pharmacy preferences, emergency contacts, race/ethnicity, contact methods.
- **Billing - Patient Liability** (29 fields): Detailed payment tracking with processor codes, refund timestamps, and billing addresses.
- **Eligibility/Insurance Verification** (14 fields): Structured coverage details including plan benefits, copay/coinsurance/deductible amounts.

**Thinnest sections**:
- **Imaging Reports** (1 field): Just "Imaging results and documents" as a single Computable PDF element — no granular fields.
- **Social History** (1 field): Just "Substance use" — no detail on what's captured.
- **Patient Status** (1 field): Living/deceased flag only.
- **Clinical Records** (10 fields): Each clinical domain (visit notes, lab results, referrals, etc.) is treated as a single data element rather than decomposed into constituent fields. The depth of clinical data within each element is unknown from this documentation.

**Key pattern**: The billing data is documented at field-level granularity (individual JSON properties), while clinical data is documented at document-level granularity (whole clinical artifacts). This asymmetry may reflect the export's actual structure (billing as JSON objects, clinical as rendered PDFs/XML documents) rather than an oversight in documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (57 fields), `Additional Demographics` (2 fields), `Guarantor Information` (9 fields), `Patient Status` (1 field) | Thorough — name, DOB, gender, race, ethnicity, address, phone, email, emergency contacts, insurance, pharmacy |
| Encounters / visits | ✅ Covered | `Appointments` (6 fields: type, date/time, status, description, provider, duration) | Basic appointment data covered; visit encounter details likely embedded in Visit Notes |
| Problems / conditions | ✅ Covered | `Problem List` (Computable PDF + XML) | Present but as single document-level element; no field-level decomposition |
| Medications / prescriptions | ✅ Covered | `OTC medications`, `Temporary medications`, `Discontinued Medications`, `Permanent Rx`, `Current Prescriptions` (5 elements as Computable PDF) | Five medication categories covered; field-level structure within each not documented |
| Allergies | ✅ Covered | `Allergies` (Computable PDF + XML) | Present as single element |
| Immunizations | ✅ Covered | `Patient Immunization history` (Computable PDF) | Present as single element |
| Vitals | ✅ Covered | `Vitals` (Computable PDF + XML) | Present as single element |
| Lab results | ✅ Covered | `Lab Results` (Computable PDF) | Present as single element; no field-level detail |
| Imaging / diagnostic reports | ✅ Covered | `Imaging Reports` (Computable PDF) | Present as single element |
| Procedures | ✅ Covered | `Procedures` (Computable PDF + XML) | Present as single element |
| Clinical notes / documents | ✅ Covered | `Visit Note` (Computable PDF), `Letters` (Computable PDF), `Medical History Report` (Computable PDF), `Files uploaded to the patient chart` (Computable PDF) | Multiple document types included; documents exported as PDFs |
| Care plans / goals | ❌ Not covered | No care plan elements in export | Product research does not indicate strong care plan functionality; may be minor gap |
| Orders / referrals | ✅ Covered | `Lab Order, Imaging Order, Pulmonary Order, Cardiac Order, Sleep Order` (Computable PDF + JSON), `Referrals` (Computable PDF) | Orders across 5 modalities included; referrals present |
| Insurance / coverage | ✅ Covered | `Primary/Secondary Carrier Name`, `Subscriber ID`, `Group No`, `Plan Name` in Demographics (8 fields) + `Eligibility/Insurance Verification` (14 fields) | Thorough — both static insurance info and dynamic eligibility/benefits data |
| Claims / billing | ✅ Covered | `Billing - Bills` (53 fields) including CPT codes, modifiers, ICD-9/10 DX codes, charges, provider roles, service locations | Genuinely deep billing coverage with field-level JSON data |
| Payments | ✅ Covered | `Billing - Patient Liability` (29 fields), `Billing - Payment Requests` (9 fields) | Detailed — payment charges, refunds, processor codes, amounts |
| Consents / directives | ❌ Not covered | No consent or advance directive elements | Product likely stores some consent data (intake forms); minor gap |
| Patient communications | ⚠️ Partial | `Messages` (Computable PDF: "Messages between patient and provider") | Present as single element; no detail on structure. Internal staff messages/tasks not mentioned |
| Social history | ⚠️ Partial | `Social history` (Computable PDF: "Substance use") | Only substance use mentioned; product likely captures more social history data |
| Family health history | ⚠️ Partial | `Personal Relationship` ("Non clinical care team members ie family, or support caregivers") | Personal relationships included, but no explicit family medical history element despite product supporting it (certified for (a)(12)) |
| Referral tracking | ⚠️ Partial | `Referrals` (Computable PDF) | Referrals present but no evidence of close-the-loop tracking data that the product supports |

## 6. Documentation Quality

**Strengths**:
- Every data element (199/200) has a human-readable description
- Clear categorization into logical sections
- Export format tagged per element — users know whether to expect PDF, XML, JSON, or CSV
- Billing section has field-level JSON documentation with meaningful descriptions (e.g., "Ordered list of dx codes ICD 10 if service date is after 2010-10-01, otherwise ICD9")
- Help center article provides clear step-by-step export instructions
- Confidential notes handling is well-documented with explicit inclusion/exclusion policies

**Weaknesses**:
- **No data types**: None of the 200 elements specify a type (string, integer, date, boolean, etc.)
- **No relationships/foreign keys**: No documentation of how entities relate to each other (e.g., how a bill connects to a visit note beyond `visit_note_id`)
- **No value sets**: No enumeration of valid values for coded fields (billing status values, appointment statuses, etc.)
- **No sample data**: No example export files provided
- **No machine-readable schema**: No JSON Schema, XSD, or other programmatic spec
- **Clinical data is opaque**: Clinical elements (visit notes, lab results, etc.) are listed as single items exported as "Computable PDF" — the internal structure of these documents is not described. A developer receiving a "Computable PDF" of visit notes would not know what fields or structure to expect without examining actual exports.
- **Could a developer build an import?** For billing data (JSON), partially — the field names and descriptions would help, but missing types, enumerations, and sample data would require significant trial-and-error. For clinical data (Computable PDF/XML), no — the structure is entirely undocumented.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

Elation has built an export that covers the breadth of what their product stores. It goes well beyond USCDI/clinical summaries to include:
- **Billing**: 91 fields across bills, patient liability, and payment requests — with CPT codes, modifiers, ICD-9/10 diagnosis codes, charge amounts, multiple provider roles, service locations, and payment processing details. This is not available through FHIR (g)(10) or C-CDA.
- **Eligibility/Insurance verification**: 14 fields of structured benefits data (copay, coinsurance, deductible, limitations).
- **Appointments**: 6 fields of scheduling data.
- **Patient communications**: Messages between patient and provider.
- **Documents**: Uploaded files, letters, imaging reports.
- **Orders**: Five order types (lab, imaging, pulmonary, cardiac, sleep).

The clinical side is thinner in documentation granularity (9 elements as document-level items vs. 91 billing fields), but this reflects the export format choice (clinical data as rendered PDFs/XML documents rather than decomposed JSON). The actual data content within those documents may be comprehensive. Since this is a primary care EHR without inpatient, surgical, or specialty workflows, the domains covered align well with what the product stores.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged clinical exchange:
- The data dictionary is titled "Elation's Designated Record Set for EHI Export" — purpose-specific language.
- It includes billing data (91 fields), eligibility verification (14 fields), payment requests, guarantor information, and appointment data — none of which would appear in a C-CDA or FHIR (g)(10) export.
- The mixed-format approach (PDF + XML + JSON + CSV) indicates a custom export pipeline, not a repurposed standard.
- The help center article explicitly describes a dedicated EHI export UI flow (More → Data Exchange → Export Entire Health Information), separate from any clinical exchange pathway.
- The export is specifically designed per (b)(10) with a link to the data dictionary as required by the criterion.

### Key Findings

1. **Billing coverage is genuinely deep**: 91 fields of billing data (bills, patient liability, payment requests) exported as structured JSON, including CPT codes, ICD-9/10 DX codes, modifiers, charge amounts, and payment processing — this is real designated-record-set billing data, far beyond USCDI scope.

2. **Clinical data lacks granularity in documentation**: While 10 clinical record types are included, they're each listed as single data elements (e.g., "Visit Note → Visit notes, Computable PDF"). The internal structure of these PDFs is not documented, making it impossible to assess field-level completeness from the documentation alone.

3. **Mixed export format is unusual but functional**: Four different formats (PDF, XML, JSON, CSV) are used across different data types. Billing uses JSON (granular), demographics use CSV/PDF (tabular), clinical records use PDF/XML (document-level). This reflects practical choices but increases import complexity for downstream systems.

4. **Documentation is moderate quality**: 99.5% of elements have descriptions, but no types, no value sets, no sample data, and no machine-readable schemas. A developer could work with the billing JSON but would struggle with the clinical PDF/XML without actual samples.

5. **Some data domains are present but thin**: Patient communications (1 element), social history (1 element), family health history (indirect only via "Personal Relationship"), and care plans are absent or minimally represented. These are relatively minor gaps for a primary care EHR.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   Mixed (Computable PDF, XML, JSON, CSV)
Entities:        14 categories
Fields:          200
Descriptions:    99.5% (199/200 fields with descriptions)
Sample data:     No
Bulk export:     Yes (vendor-assisted, may incur cost)
Domains covered: 15 of 18 applicable domains (✅ or ⚠️)
```

### Bottom Line

Elation EMR has built a genuine purpose-built EHI export that covers both clinical and billing data, with particularly deep billing coverage (91 structured JSON fields). The main limitation is documentation granularity for clinical data — clinical records are exported as document-level PDFs/XML rather than decomposed into fields, making it hard to assess exactly what's in them from the documentation alone. For a primary care EHR, this export covers the expected breadth of the designated record set, and the inclusion of billing, payments, eligibility, and appointment data clearly distinguishes it from a repackaged clinical exchange.

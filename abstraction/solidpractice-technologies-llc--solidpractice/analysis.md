# EHI Export Analysis: SolidPractice Technologies, LLC

**Product**: SolidPractice v2.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.3095.SOLP.01.00.1.211227 (CHPL ID 10763)

## 1. Product Context

SolidPractice is a small-vendor, desktop-based ambulatory EHR/EMR targeted at small private medical practices. It is a Complete EHR certified across 33 ONC 2015 Edition Cures Update criteria. The product's signature feature is real-time voice dictation/transcription for clinical documentation — the company (Innovative Medical Practice Solutions / IMPS) has roots in voice-enabled medical software dating to 1994.

**Key capabilities relevant to export completeness:**
- **Clinical charting & voice dictation** — the core feature; clinical encounter notes are the product's primary data type
- **E-prescribing** — via NewCrop/SureScripts integration
- **Lab & imaging integration** — electronic lab orders and results
- **Patient demographics** — standard registration data
- **Immunizations** — certified for immunization registry reporting (f)(1)
- **Referral letter generation** — automated referral letters
- **Patient portal** — certified for view/download/transmit (e)(1)
- **Billing integration** — E/M coding support and billing system integration are listed on the feature page, though it's unclear whether billing is built-in or handled through an external system
- **Appointment scheduling** — appointment management
- **Custom data fields** — custom field creation capability
- **Telehealth** — listed in third-party feature comparisons
- **FHIR API and Direct messaging** — certified for (g)(10) and (h)(1)

The install base appears very small (micro-vendor, no published customer counts, zero third-party reviews). This is a general ambulatory EHR with no identified specialty focus.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/SolidPractice-b10-exportable-data-content.pdf` (29 KB, 3 pages) | Core (b)(10) documentation: a landscape Excel-to-PDF spreadsheet listing 87 exportable data elements with columns for element number, name, description, and format support (Computable PDF Export, CCD XML Export, JSON). Created 2024-03-27. | **Most informative** — the definitive data element list for the (b)(10) export |
| `downloads/SolidPractice-Data-Access-API.pdf` (14.5 KB, 6 pages) | Data Access API documentation describing the HTTP endpoint for exporting patient CCD XML data. Includes endpoint URL, token authentication, 16 selectable clinical data sections, JSON response format, and error examples. Dated 2022-12-06. | **Supplementary** — describes the CCD XML export mechanism but covers only clinical sections |

No sample data files, no JSON schemas, no XSD schemas, no FHIR documentation, and no machine-readable artifacts were provided. The entire (b)(10) documentation consists of these two PDFs.

## 3. Export Mechanics

- **Formats**: Three formats are listed in the data element spreadsheet: "Computable PDF Export," "CCD XML Export," and "JSON." The CCD XML export is the only format with documented API mechanics. The "Computable PDF Export" format is completely undocumented beyond its name. The "JSON" format is not described.
- **Mechanism**: The Data Access API provides an HTTP endpoint (`/CCD/ExportPatientData`) that returns CCD (C-CDA) XML wrapped in a JSON response. It uses token-based authentication (API key from EMR Setup). How the Computable PDF export is accessed is not documented.
- **Single-patient**: The API is per-patient (requires `patientId` parameter). No bulk export capability is documented.
- **Section selection**: The API supports exporting all data (`all=true`) or individual clinical sections (16 toggleable sections). An optional date range filter (`from`, `to`) is available.
- **Access constraints**: Requires an API token obtained from the EMR Setup section. No fees are mentioned in the documentation.

The API's 16 selectable sections are all standard C-CDA clinical sections: allergiesAndIntolerances, medications, problem, procedures, immunizations, vitalSigns, socialHistory, results, medicalEquipment, assessment, planOfTreatment, reasonForReferral, goals, healthConcerns, functionalStatus, cognitiveStatus. These sections do not include billing, appointments, insurance, uploaded documents, or guarantor data — suggesting the CCD XML API covers only the clinical subset.

## 4. Export Content: What's In It

The (b)(10) data element list contains **87 data elements**, each with a sequential number, name, brief description, and format indicator(s). All 87 elements (100%) have descriptions, though descriptions are brief (typically one phrase restating the element name). **No data types, value sets, cardinality, relationships, or foreign keys are documented for any field.**

### Vendor's own content organization

The 87 data elements fall into these categories (vendor does not explicitly label categories, but groups elements sequentially by domain):

| Category | Elements | Field Count | Described | Types | Notes |
|---|---|---|---|---|---|
| Patient Demographics | #1–29 | 29 | 29 (100%) | No | Includes emergency contact (8 fields) |
| Medications & Pharmacy | #30–35 | 6 | 6 (100%) | No | Current/past meds + preferred pharmacy address |
| Clinical Data | #36–44 | 9 | 9 (100%) | No | Smoking, social hx, immunizations, problems, procedures, vitals, allergies, providers |
| Labs & Imaging | #45–47 | 3 | 3 (100%) | No | Lab results, lab/imaging orders, imaging reports |
| Uploaded Documents | #48 | 1 | 1 (100%) | No | Insurance cards, consent forms, etc. |
| Insurance | #49–56 | 8 | 8 (100%) | No | Primary + secondary carrier info |
| Guarantor | #57–65 | 9 | 9 (100%) | No | Name, address, phone, relationship |
| Appointments | #66–71 | 6 | 6 (100%) | No | Type, date/time, status, description, provider, duration |
| Billing / Receipts | #72–87 | 16 | 16 (100%) | No | Receipt fields: service date, copay, deductible, balances, payment method, facility info |
| **Total** | | **87** | **87 (100%)** | **No** | |

**Format column analysis**: The PDF's format columns indicate which export format supports each data element. From rendering the PDF pages as images:
- Items 1–46 (demographics + clinical + labs): marked under "CCD XML Export"
- Items 47–48 (imaging reports, uploaded documents): marked under "Computable PDF Export"
- Items 49–87 (insurance, guarantor, appointments, billing): column position is ambiguous across pages (headers not repeated on pages 2–3), but these non-clinical items are marked in one of the rightward format columns

**Key observation about granularity**: Many "data elements" in this list are aggregate/composite items rather than atomic fields. For example:
- #30 "Prescriptions" = "Patient's current and past Medications" — this is an entire clinical domain in one line item
- #39 "Problem List" = "Patient problems" — similarly an entire domain
- #41 "Vitals" = "Patient Vitals" — encompasses all vital sign types
- #45 "Lab Results" — all lab results in one element

These composite items are documented at the domain level without specifying the individual fields within each domain (e.g., what specific medication fields — drug name, dose, frequency, start date, prescriber, NDC code — are exported within "Prescriptions"). The 87-element count therefore overstates the documentation's precision: many of these elements are really section headers for structured clinical data whose internal structure is defined only by the C-CDA standard (if using CCD XML export) or entirely unspecified (if using Computable PDF export).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export spans six functional domains in the vendor's implicit organization:

1. **Patient Demographics** (29 fields) — the largest and most granular section. Individual fields for name components, DOB, gender, race, ethnicity, language, contact info, and full emergency contact details. This is the only section with true field-level granularity.

2. **Clinical Data** (9 items + 3 labs/imaging + 6 medications/pharmacy = 18 items total) — covers the standard ambulatory clinical domains: medications, allergies, problems, procedures, vitals, immunizations, social history, smoking status, lab results, lab/imaging orders, imaging reports, and care team/providers. However, each of these is a single line item representing an entire clinical domain, with no field-level detail.

3. **Insurance** (8 fields) — primary and secondary carrier name, subscriber ID, group number, plan name. Basic coverage information but no policy dates, copay structures, or eligibility details.

4. **Guarantor** (9 fields) — name, address, phone, relationship. Straightforward.

5. **Appointments** (6 fields) — type, date/time, status, description, provider, duration. Basic scheduling data.

6. **Billing / Receipts** (16 fields) — the second-most granular section. Receipt-oriented: service dates, copay/deductible amounts, outstanding balances, credit amounts, payment methods, transaction numbers, billing facility info. Notably, this covers **payment/receipt data only** — there are no CPT codes, ICD codes, E/M levels, claim submission data, or charge details. The billing export is a receipt ledger, not a billing/claims record.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | 29 fields (#1–29) including emergency contact | Thorough at field level |
| Encounters / visits | ❌ Not covered | No encounter/visit data elements | **Critical gap**: product is encounter-based; voice-dictated encounter notes are its core feature |
| Problems / conditions | ⚠️ Partial | #39 "Problem List" (1 aggregate item) | Domain listed but no field-level detail |
| Medications / prescriptions | ⚠️ Partial | #30 "Prescriptions" (1 aggregate item) + pharmacy (#31–35) | Domain listed but no field-level detail for med records |
| Allergies | ⚠️ Partial | #42 "Allergies" (1 aggregate item) | Domain listed, no field-level detail |
| Immunizations | ⚠️ Partial | #38 "Patient Immunization history" (1 aggregate item) | Domain listed, no field-level detail |
| Vitals | ⚠️ Partial | #41 "Vitals" (1 aggregate item) | Domain listed, no field-level detail |
| Lab results | ⚠️ Partial | #45 "Lab Results" (1 aggregate item) | Domain listed, no field-level detail |
| Imaging / diagnostic reports | ⚠️ Partial | #46 "Lab Order, Imaging Order" + #47 "Imaging Reports" | Two aggregate items, no field-level detail |
| Procedures | ⚠️ Partial | #40 "Procedures" (1 aggregate item) | Domain listed, no field-level detail |
| Clinical notes / documents | ❌ Not covered | No data element for encounter notes, progress notes, dictated text, or clinical documents | **Critical gap**: voice-dictated clinical notes are the product's signature feature and primary clinical data type |
| Care plans / goals | ❌ Not covered | Not in b(10) list; "goals" and "planOfTreatment" exist in API sections | API has sections but b(10) data element list omits them |
| Orders / referrals | ⚠️ Partial | #46 covers orders; "reasonForReferral" in API but not in b(10) list | Referral letters (a product feature) not in export |
| Insurance / coverage | ✅ Covered | 8 fields (#49–56) for primary + secondary | Basic but present; no policy dates or eligibility details |
| Claims / billing | ⚠️ Partial | 16 receipt fields (#72–87) | Receipt/payment data only; no CPT/ICD codes, no claim submissions, no charge details |
| Payments | ✅ Covered | Receipt fields include copay, deductible, amounts, payment method, transaction # | Payment receipt data is the strongest billing element |
| Consents / directives | ❌ Not covered | No consent data elements (though #48 mentions consent forms as uploaded documents) | Consent forms may exist as uploaded files but not structured data |
| Patient communications / portal | ❌ Not covered | No portal messages, patient communications, or secure messaging data | Product has patient portal (certified (e)(1)); portal data absent |
| Specialty-specific | N/A | No specialty features identified | Product is general ambulatory; no specialty gaps expected |
| Uploaded documents | ✅ Covered | #48 "Files uploaded to the patient chart" | Single aggregate item; includes insurance cards, consent forms |
| Appointments | ✅ Covered | 6 fields (#66–71) | Basic scheduling data with reasonable granularity |
| Guarantor | ✅ Covered | 9 fields (#57–65) | Standard guarantor information |

## 6. Documentation Quality

**Strengths:**
- The b(10) data element list is enumerated and complete for its scope — 87 elements, all with descriptions
- The Data Access API has sufficient detail for a developer to make API calls (endpoint URL, authentication, parameters, response format, error examples)
- Export scope explicitly goes beyond clinical data to include insurance, guarantor, appointments, and billing receipts

**Weaknesses:**
- **No data types** for any field (what format is Date of Birth? what values for Gender?)
- **No value sets or code systems** for coded fields (Gender, Race, Ethnicity, Marital Status, Appointment Status, Payment Method)
- **No cardinality or nullability** documentation
- **No relationships** between entities (how receipts link to appointments, how orders link to results)
- **No sample data** in any format
- **No machine-readable schemas** (no JSON schema, XSD, OpenAPI spec)
- **"Computable PDF Export" format is entirely undefined** — it is unclear whether this is a structured/tagged PDF, a form-filled PDF, or a rendered printout. The word "computable" is unexplained.
- **Clinical domains are documented at the section level only** — "Prescriptions," "Problem List," "Vitals" are each single line items with no specification of internal fields. For the CCD XML format, the C-CDA standard implicitly defines the fields; for the Computable PDF format, the field structure is unknown.
- A developer could use the CCD XML API for clinical data extraction, but could not build a reliable import system from the Computable PDF export without reverse-engineering the format.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers demographics (well), basic clinical domains (at section level), insurance, guarantor, appointments, and billing receipts — a broader scope than a pure USCDI/C-CDA repackage. However, there are two critical gaps relative to what the product stores:

1. **Clinical encounter notes are entirely absent.** Voice-dictated clinical notes are SolidPractice's signature feature and the primary clinical data type in any ambulatory EHR. There is no data element for encounter notes, progress notes, H&P notes, or dictated text. This is a glaring omission — it's as if the product's most important data category was overlooked.

2. **Billing data is receipts-only.** The 16 billing fields cover payment receipts (amounts, methods, transaction numbers) but not the underlying clinical billing data: no CPT procedure codes, no ICD diagnosis codes, no E/M levels, no claim details, no superbills. If the product stores billing/coding data (as suggested by "E/M coding support" on the feature page), that data is absent from the export.

Additional missing areas: patient portal data, referral letters, custom data fields, care plans/goals (present in the API sections but absent from the b(10) data element list).

**Axis 2 — Export approach: Purpose-built EHI export**

Despite its limitations, this is not a simple repackage of an existing clinical exchange export. Evidence:
- The b(10) data element list explicitly includes non-USCDI domains (insurance, guarantor, appointments, billing receipts, uploaded documents) that would not appear in a standard C-CDA or FHIR (g)(10) export.
- The vendor created a dedicated document (`SolidPractice-b10-exportable-data-content.pdf`) separate from their Data Access API documentation, with 87 data elements organized across clinical and administrative domains.
- The "Computable PDF Export" format (whatever it may be) appears to be a purpose-built mechanism to export data beyond what C-CDA covers.
- The Data Access API (CCD XML) alone would cover only clinical data; the b(10) list goes beyond it.

The export was designed with (b)(10) intent, but the execution is thin and has significant gaps, particularly the missing clinical notes.

### Key Findings

1. **Clinical encounter notes — the product's core feature — are completely absent from the export.** SolidPractice's signature capability is voice-dictated clinical documentation, yet there is no data element for encounter notes, progress notes, or dictated text in the 87-element list. This is the single most significant gap. (`SolidPractice-b10-exportable-data-content.pdf`, items #1–87 reviewed; no clinical note element present)

2. **The export goes beyond USCDI with administrative/financial data.** Unlike many vendors that simply repackage C-CDA, SolidPractice includes insurance (8 fields), guarantor (9 fields), appointments (6 fields), billing receipts (16 fields), and uploaded documents — demonstrating awareness that (b)(10) requires more than clinical summaries.

3. **Clinical domains are documented as aggregate items, not individual fields.** "Prescriptions," "Problem List," "Vitals," "Allergies," and "Lab Results" are each single line items in the data element list. The actual field-level structure within these domains is defined only implicitly by the CCD XML standard, not by the vendor. This means the 87-element count significantly overstates the documentation's specificity.

4. **Billing data covers only payment receipts, not clinical billing codes.** The 16 billing fields are receipt-oriented (copay, deductible, amount paid, payment method). No CPT codes, ICD codes, E/M levels, or claim details are included — only the financial transaction side of billing.

5. **Documentation lacks basic technical specifications.** No data types, no value sets, no sample data, no machine-readable schemas. The "Computable PDF Export" format is entirely undefined. A developer could not build a reliable data import from these documents alone.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   CCD XML (clinical data), "Computable PDF" (non-clinical), JSON (undocumented)
Entities:        87 data elements (flat list, not normalized entities)
Fields:          87 (many are aggregate domain-level items, not atomic fields)
Descriptions:    100% (all 87 have brief descriptions)
Types:           0% (no data types documented)
Value sets:      0% (no coded value sets documented)
Sample data:     No
Bulk export:     No (single-patient API only)
Domains covered: 10 of 16 applicable domains (with caveats on depth)
```

### Bottom Line

SolidPractice made a genuine attempt at (b)(10) by including administrative and financial data beyond USCDI clinical domains, but the export has a critical gap: **clinical encounter notes — the product's signature voice-dictated documentation — are completely absent** from the 87-element export list. This means a patient requesting their EHI would receive demographics, medication lists, billing receipts, and insurance information, but not their actual clinical visit notes. The documentation is also thin, with no data types, no value sets, and an undefined "Computable PDF" format, making the export difficult to use even for the domains it does cover.

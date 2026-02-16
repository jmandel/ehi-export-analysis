# EHI Export Analysis: Medical Information Technology, Inc. (MEDITECH)

**Product**: MEDITECH Expanse 2.2 Ambulatory
**Analysis date**: 2026-02-16
**CHPL IDs**: 10925 (Expanse 2.2 Ambulatory), plus 13 additional certified listings across Expanse, 6.1, 6.0, MAGIC, and Client/Server platforms

## 1. Product Context

MEDITECH Expanse is MEDITECH's current-generation, web-based, cloud-ready EHR platform. MEDITECH is the third-largest U.S. hospital EHR vendor (~14.8% acute care market share, ~900 hospitals). The **Ambulatory** module is a component of the larger Expanse HCIS platform, covering outpatient/clinic workflows within a comprehensive hospital information system.

The full Expanse platform encompasses 60+ modules spanning:
- **Clinical**: EHR, ambulatory, ED, order management, pharmacy, e-prescribing, nursing, therapies
- **Diagnostic**: laboratory, microbiology, blood bank, pathology, radiology/imaging
- **Revenue Cycle**: billing, claims, charge capture, registration, scheduling, practice management, HIM
- **Specialty**: oncology, surgical services, L&D, mental health, long-term care, home health, hospice
- **Patient Engagement**: MyHealth portal, telehealth, patient connect messaging
- **Care Coordination**: care compass registries, case management, referral management

For a product of this breadth, the designated record set includes clinical documentation, lab/imaging results, medications, orders, encounters, referrals, billing records, authorization data, scanned documents, patient portal communications, and specialty-specific clinical data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehiexport-main.html` (9 KB) | Main EHI Export overview page describing two export configurations and platform applicability | **High** — defines which config applies to which product |
| `ehiexportconfig1.html` (29 KB) | Configuration 1 specification — applies to Expanse 2.2 Ambulatory. Documents export ZIP structure with 10 sections | **High** — primary documentation for this product |
| `ehiexportconfig2.html` (23 KB) | Configuration 2 specification — CSV-based export for legacy platforms (NOT applicable to Expanse 2.2 Ambulatory) | **Medium** — shows MEDITECH's approach for other platforms |
| `ehiexportold.html` (28 KB) | Older version of EHI export page, similar to Config 1 | Low — superseded by Config 1 page |
| `608ehiexportcsv.pdf` (251 KB, 19 pages) | CSV data dictionary for MPM 6.08 Ambulatory: 95 tables, 482 fields | **Medium** — not for Expanse, but shows field-level capability on legacy platforms |
| `csacuteandambehiexportdrsolutionmerged.pdf` (263 KB, 30 pages) | CSV data dictionary for Client/Server: 331 tables, 1,231 fields | **Medium** — same caveat as above |
| `mgehiexportdrsolutionmerged.pdf` (363 KB, 48 pages) | CSV data dictionary for MAGIC: 323 tables, 1,121 fields | **Medium** — same caveat as above |
| `screenshot-*.png` (3 files) | Full-page screenshots of the three HTML documentation pages | Low — visual confirmation of HTML content |

**Key observation**: The three PDF data dictionaries document field-level CSV exports, but these apply only to **Configuration 2** (legacy platforms). Configuration 1 — which applies to **Expanse 2.2 Ambulatory** — has **no field-level data dictionary**.

## 3. Export Mechanics

- **Format**: Multi-format ZIP archive containing:
  - Electronic Chart documents (scanned images, PDFs)
  - C-CDA XML documents
  - FHIR R4 JSON bundle (US Core STU 3.1.1 via Patient `$everything`)
  - Supplemental PDF/TXT reports for financial, immunization, authorization, utilization, and ambulatory data
- **Mechanism**: MEDITECH-initiated export; requires configuration of HIM (Health Information Management) and SCN (Scanning and Archiving with eChart) modules. Patient Portal (PHM) is optional.
- **Single-patient vs bulk**: Documentation describes single-patient export (per-account structure). No explicit mention of bulk export capability.
- **Access constraints**: Requires specific MEDITECH modules to be configured (HIM, SCN). No mention of fees in documentation.
- **Machine readability**: Export includes a `Table of Contents.ndjson` file containing FHIR DocumentReference resources for machine-readable metadata of all files in the ZIP.

## 4. Export Content: What's In It

### Configuration 1 (Expanse 2.2 Ambulatory) — Applicable to this product

The export for Expanse 2.2 is **document/report-based with standard clinical exchange components**. There is **no structured data dictionary** — no field-level documentation of what data elements are exported. The export contains 10 sections:

| Section | Format | Content Description |
|---|---|---|
| Electronic Chart | PDF, PNG/JPG/TIF/BMP images | Scanned/stored documents organized by account → category → subcategory. Includes account-level, patient-level ("Record Documents"), and global documents. |
| Structured Clinical Documents | C-CDA XML | All C-CDA documents created and possibly sent externally. Formats: C-CDA R2.1 or R1.1. |
| FHIR Resource Bundle | FHIR R4 JSON | US Core FHIR resources via Patient `$everything`. US Core STU 3.1.1. References fhir.meditech.com. |
| Ambulatory Results | PDF | Manually entered micro/lab results + outside vendor micro/lab results (2 PDF files). |
| Authorization & Referral Management Reports | PDF | Authorization/referral data (ARMEHI-ArmAuthData.pdf) + insurance eligibility/copay/deductible data (ARMEHI-InsEligCopayDeductData.pdf). |
| Financial Reports | TXT | Patient Accounting report with financial transactions (FinancialEHI.txt), Resident Trust report (ResidentTrustEHI.txt, Expanse/6.1x), Cost Estimation (CostEstimation.txt, Expanse only). |
| Immunization History | PDF | Patient immunization history list. |
| Population Health | PDF | External population health aggregated data. |
| Utilization Review | PDF | Case management utilization reviews. |
| Historical Ambulatory Data | Mixed (PDF, images, text) | Legacy ambulatory documentation migrated from previous software versions. |

### Vendor's own content organization

The vendor organizes content into the 10 sections above. There is **no entity/table/field-level data dictionary** for Configuration 1. The data dictionary is only available for Configuration 2 (legacy platforms).

For reference, the Configuration 2 CSV data dictionaries (legacy platforms only) contain:

| Platform | Tables | Fields | Source PDF |
|---|---|---|---|
| Client/Server Acute & Ambulatory | 331 | 1,231 | `csacuteandambehiexportdrsolutionmerged.pdf` (30 pages) |
| MAGIC Acute & Ambulatory | 323 | 1,121 | `mgehiexportdrsolutionmerged.pdf` (48 pages) |
| MPM 6.08 Ambulatory | 95 | 482 | `608ehiexportcsv.pdf` (19 pages) |

The Config 2 CSV data dictionary fields provide only **Field name**, **Table name**, and **Column name** — no descriptions, data types, value sets, or relationships are documented. For the legacy platforms, the CSV tables span these domain categories (aggregated across all 3 platforms):

| Domain Category | Tables | Fields |
|---|---|---|
| Scheduling | 120 | 490 |
| Medical Records/HIM | 89 | 428 |
| Provider/Physician | 46 | 234 |
| Pharmacy | 80 | 232 |
| Pharmacy/Medication Mgmt | 64 | 230 |
| Ambulatory/Practice | 52 | 226 |
| Authorization/Referral Mgmt | 15 | 168 |
| Nursing | 39 | 159 |
| Registration/Demographics | 26 | 153 |
| Interfaces/Transactions | 25 | 106 |
| Order Entry/CPOE | 29 | 72 |
| Blood Bank | 17 | 52 |
| Pathology | 32 | 50 |
| E-Prescribing | 19 | 48 |
| Radiology | 17 | 48 |
| Interoperability/Hub | 16 | 46 |
| ED Management | 17 | 36 |
| Laboratory | 6 | 26 |
| Microbiology | 15 | 18 |
| Other | 23 | 12 |

This demonstrates that MEDITECH *can* export structured data at scale (749 tables, 2,834 fields for legacy platforms), but chose a fundamentally different, less structured approach for Expanse.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

For Expanse 2.2 Ambulatory (Configuration 1), the export combines:

1. **Standard clinical exchange** — C-CDA and US Core FHIR via Patient `$everything`. This covers USCDI-scope data: demographics, problems, medications, allergies, immunizations, vitals, lab results, procedures, encounters, clinical notes, and care plans — but only to the depth defined by US Core STU 3.1.1, not the full depth of MEDITECH's internal data model.

2. **Electronic Chart** — a proprietary document archive containing scanned/stored documents organized by categories and subcategories. This is essentially a document dump of all images and PDFs in the patient's chart. The content depends entirely on what the organization has configured to scan/store — it could include consent forms, external records, printed reports, etc.

3. **Supplemental reports** — purpose-built sections that go beyond C-CDA/FHIR:
   - **Financial Reports**: Patient accounting transactions, resident trust records, cost estimates — this is genuine billing/financial EHI not available through C-CDA or FHIR.
   - **Authorization & Referral Management**: Auth/referral data plus insurance eligibility — administrative EHI beyond USCDI.
   - **Ambulatory Results**: Lab/micro results entered manually or from outside vendors — potentially filling gaps where discrete results aren't in the FHIR bundle.
   - **Population Health**: Aggregated external data.
   - **Utilization Review**: Case management data.
   - **Immunization History**: Dedicated immunization report.

The strongest non-USCDI content is in the Financial Reports (billing transactions, cost estimates) and Authorization & Referral Management sections. However, these are **text/PDF reports**, not structured data — they cannot be programmatically consumed without parsing.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR Patient resource via `$everything`; C-CDA header | FHIR/C-CDA carry standard demographics. No evidence of extended demographics (employer, guarantor, next of kin details) beyond what US Core provides. Product stores much richer demographic data (see Config 2 CSV: 26 registration tables, 153 fields). |
| Encounters / visits | ⚠️ Partial | FHIR Encounter via `$everything`; C-CDA encompassing encounter | Standard encounter data via FHIR/C-CDA. No dedicated structured encounter export. Product has extensive encounter data. |
| Problems / conditions | ⚠️ Partial | FHIR Condition; C-CDA Problem section | US Core depth only. Product stores richer problem data (comments, descriptions, linked items). |
| Medications / prescriptions | ⚠️ Partial | FHIR MedicationRequest; C-CDA Medications section | US Core depth only. Product has extensive pharmacy/medication management (144 tables in Config 2 CSV for Pharmacy + Rx Mgmt). |
| Allergies | ⚠️ Partial | FHIR AllergyIntolerance; C-CDA Allergies section | US Core coverage. |
| Immunizations | ✅ Covered | FHIR Immunization; C-CDA Immunizations; dedicated Immunization History PDF | Good — multiple overlapping sources. |
| Vitals | ⚠️ Partial | FHIR Observation; C-CDA Vital Signs section | US Core profiles for vitals. Config 2 shows ambulatory vitals with 20+ specific fields per set (e.g., O2 delivery method, FiO2, BP position/location). |
| Lab results | ⚠️ Partial | FHIR Observation/DiagnosticReport; C-CDA Results section; Ambulatory Results PDF | FHIR/C-CDA for structured results; PDF for manual/outside vendor results. No structured export of full lab detail. |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport; C-CDA sections; Electronic Chart (if reports stored as documents) | Standard clinical exchange depth. Product has dedicated radiology module (17 tables in Config 2). |
| Procedures | ⚠️ Partial | FHIR Procedure; C-CDA Procedures section | US Core depth. Product has surgical services module. |
| Clinical notes / documents | ✅ Covered | C-CDA clinical documents; Electronic Chart (scanned/stored documents) | Strong — C-CDA provides structured notes, Electronic Chart provides all scanned/stored documents. |
| Care plans / goals | ⚠️ Partial | FHIR CarePlan/Goal via `$everything`; Utilization Review PDF | US Core depth for FHIR. Utilization review adds case management data. |
| Orders / referrals | ⚠️ Partial | FHIR ServiceRequest/MedicationRequest; Authorization & Referral Management Reports (PDF) | FHIR carries standard orders. Auth/referral PDF adds administrative detail but as unstructured report. Config 2 shows 29 order entry tables. |
| Insurance / coverage | ⚠️ Partial | Authorization & Referral Management Reports (insurance eligibility PDF); FHIR Coverage if in US Core | Insurance eligibility in PDF report. No dedicated structured insurance export. Config 2 has dedicated insurance tables. |
| Claims / billing | ⚠️ Partial | Financial Reports (FinancialEHI.txt — patient accounting transactions) | Financial transactions in text file — goes beyond USCDI. But format is a text report, not structured data. No claims detail, charge breakdown, or remittance data evident. |
| Payments | ⚠️ Partial | Financial Reports (FinancialEHI.txt) | Included within financial transaction report as text. |
| Consents / directives | ⚠️ Partial | Electronic Chart may contain scanned consent documents | Depends on organization's scanning practices. No dedicated consent export. |
| Patient communications / portal messages | ❌ Not covered | No dedicated section for portal messages in Config 1 for Expanse 2.2 | Product has MyHealth patient portal; no export of portal messages/communications for Expanse Config 1. (Config 2 has "Provider and Patient Messages" section.) |
| Specialty-specific (surgical, OB, oncology, mental health) | ❌ Not covered | No dedicated specialty data sections | Product has modules for oncology, surgical services, L&D, mental health, etc. No specialty-specific structured export. Electronic Chart may contain specialty documents if scanned. |

## 6. Documentation Quality

**Significant weakness: No field-level data dictionary for Expanse.** While the Configuration 2 legacy platforms have PDF data dictionaries documenting CSV table/column structures (749 tables, 2,834 fields across 3 platforms), the Configuration 1 documentation for Expanse provides only:

- Section-level descriptions of what each folder/file contains
- File format specifications (PDF, TXT, FHIR JSON, C-CDA XML)
- Folder naming conventions
- A FHIR DocumentReference-based NDJSON schema for the table of contents

**What's well-documented**:
- Export ZIP structure and file organization
- Which sections apply to which product version (clear comparison table)
- Table of Contents NDJSON schema (FHIR DocumentReference)
- C-CDA and FHIR version references

**What requires guesswork**:
- The actual content and structure of Financial Reports (FinancialEHI.txt) — no field documentation
- The content of Authorization & Referral Management PDFs — no schema
- What FHIR resources are included in the `$everything` bundle — documentation just references US Core STU 3.1.1 and fhir.meditech.com
- What constitutes the "Electronic Chart" categories and subcategories
- Whether any vendor extensions or custom FHIR resources are included beyond US Core

**Machine-readable artifacts**: The NDJSON table of contents uses FHIR DocumentReference resources, which is a reasonable machine-readable index. The FHIR bundle is inherently machine-readable. However, the core supplemental content (financial reports, auth/referral reports, ambulatory results) is in PDF/TXT format — human-readable but not machine-parseable.

**Could a developer build an import?** Partially. A developer could consume the FHIR bundle and C-CDA documents programmatically. The Electronic Chart documents could be stored as attachments. However, the financial reports, authorization data, and other supplemental PDFs/text files would require custom parsing with no schema documentation to guide it.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export goes meaningfully beyond a pure USCDI/US Core repackaging by including Financial Reports (patient accounting transactions, cost estimates, resident trust data), Authorization & Referral Management data (auth/referral records, insurance eligibility), Utilization Review, Population Health data, and the Electronic Chart (scanned document archive). These sections represent genuine EHI beyond what C-CDA and FHIR US Core provide.

However, significant gaps remain relative to what Expanse stores:
- No structured export of the product's rich pharmacy/medication management data (Config 2 shows 144 tables for pharmacy on legacy platforms)
- No patient portal message export for Expanse (present in Config 2 for legacy platforms)
- No specialty-specific data (oncology, surgical, L&D, mental health) despite the product having dedicated modules
- No structured scheduling, registration, or order data beyond FHIR US Core
- Financial data is provided as a text report rather than structured data with field-level documentation

The supplemental sections represent genuine effort, but the bulk of the export's clinical data comes through C-CDA and FHIR US Core — standard clinical exchange formats with standard depth.

**Axis 2 — Export approach: Purpose-built EHI export (with significant repackaged components)**

This is a hybrid approach. MEDITECH clearly built purpose-specific export functionality:
- The multi-section ZIP structure with NDJSON table of contents is custom-built for (b)(10)
- Financial Reports, Authorization & Referral Management, Utilization Review, Population Health, and Immunization History sections are purpose-built additions not part of standard clinical exchange
- The Electronic Chart export (scanned document archive) appears to be a purpose-built bulk document extraction
- The export conforms to the draft EHI Export API Implementation Guide (FHIR DocumentReference profiles)

However, the clinical data core relies on existing standard exchange:
- C-CDA documents that were "created and possibly sent outside of the organization" — these are existing transitions-of-care documents, not newly generated for EHI
- FHIR Resource Bundle explicitly uses "Patient $everything" with "US Core STU 3.1.1" — this is the existing (g)(10) FHIR API surface

The overall classification is **purpose-built EHI export** because the vendor demonstrably created new export components (financial, auth/referral, document archive, utilization review) beyond existing clinical exchange. However, the clinical data layer is substantially repackaged from existing (g)(10)/C-CDA capabilities.

Notably, MEDITECH built a much more comprehensive structured export for its legacy platforms (Config 2 with 749 CSV tables across 3 platforms and PDF data dictionaries), but chose a less structured, document-heavy approach for Expanse. This contrast is striking — the legacy platforms get field-level CSV data with data dictionaries, while the modern Expanse platform gets reports and standard clinical exchange with no data dictionary.

### Key Findings

1. **Two-tier approach creates a gap for Expanse users.** Legacy platforms (MAGIC, Client/Server, 6.08) get Configuration 2 with structured CSV exports (331 tables, 1,231 fields for C/S) and field-level data dictionaries. Expanse 2.2 gets Configuration 1 with document/report-based exports and standard clinical exchange — paradoxically, the legacy platforms have a more transparent, structured EHI export. (Source: `ehiexport-main.html`, `ehiexportconfig1.html`, `ehiexportconfig2.html`, CSV data dictionary PDFs)

2. **No field-level data dictionary for Expanse.** The three PDF data dictionaries (97 pages total, 749 tables, 2,834 fields) apply only to Configuration 2 legacy platforms. Configuration 1 documentation describes 10 export sections at a conceptual level with no field/column/table documentation. (Source: `ehiexportconfig1.html`, verified against all three PDF data dictionaries)

3. **Financial and administrative data goes beyond USCDI.** The Financial Reports section (FinancialEHI.txt, ResidentTrustEHI.txt, CostEstimation.txt) and Authorization & Referral Management section (insurance eligibility, authorization/referral data) represent genuine EHI beyond standard clinical exchange. (Source: `ehiexportconfig1.html`, Section Information table)

4. **Patient portal messages missing for Expanse.** Configuration 2 includes "Provider and Patient Messages" as a dedicated section for legacy platforms, but Configuration 1 (Expanse) has no equivalent section — a notable omission for a product with an active patient portal (MyHealth). (Source: comparison of `ehiexportconfig1.html` vs `ehiexportconfig2.html` section tables)

5. **FHIR component is explicitly (g)(10) repackaged.** The FHIR Resource Bundle documentation states it "Contains all available FHIR resources for the exported patient leveraging Patient $everything" using "US Core STU 3.1.1 Implementation Guide" — this is the standard FHIR API surface, not a custom mapping. (Source: `ehiexportconfig1.html`)

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export (hybrid — purpose-built supplemental sections + repackaged C-CDA/FHIR core)
    Export format:   Mixed (ZIP containing FHIR R4 JSON, C-CDA XML, PDF reports, TXT reports, scanned images)
    Entities:        10 sections (no entity/table-level granularity for Expanse; Config 2 legacy has 749 tables)
    Fields:          N/A for Expanse Config 1 (no field-level data dictionary; Config 2 legacy has 2,834)
    Descriptions:    N/A (no field-level documentation for Expanse)
    Sample data:     No
    Bulk export:     Unclear (documentation describes single-patient export structure)
    Domains covered: 10 of 17 applicable domains at partial or better coverage

### Bottom Line

MEDITECH's EHI export for Expanse 2.2 Ambulatory is a genuine hybrid that combines standard clinical exchange (C-CDA + FHIR US Core) with purpose-built supplemental sections for financial, administrative, and document data. It goes meaningfully beyond a pure USCDI repackaging but falls well short of comprehensive EHI export — notably lacking structured data export, a field-level data dictionary, patient portal messages, and specialty-specific data. The irony is that MEDITECH's legacy platforms have a more structured and better-documented export (CSV with data dictionaries) than the modern Expanse platform.

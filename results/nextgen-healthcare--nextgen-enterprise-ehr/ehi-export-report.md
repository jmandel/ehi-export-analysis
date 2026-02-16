# NextGen Healthcare — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.nextgen.com/sldkjljieo0935jljsrnfkl
- CHPL IDs: 11645 (Enterprise 8, certified 2025-06-02), 10861 (v6.2021.1 Cures, certified 2022-03-18)
- Developer: NextGen Healthcare

## Navigation Journal

1. **Probed the registered URL:**
   ```bash
   curl -sI -L "https://www.nextgen.com/sldkjljieo0935jljsrnfkl" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, Content-Type: text/html, 175,648 bytes. The URL (despite its random-looking path slug) resolves to a live page titled "ELECTRONIC HEALTH INFORMATION DATA DICTIONARY HYPERLINKS."

2. **Fetched and examined the page content:**
   ```bash
   curl -sL "https://www.nextgen.com/sldkjljieo0935jljsrnfkl" -H 'User-Agent: Mozilla/5.0' -o ehi-landing-page.html
   ```
   The page is a Sitecore-based HTML page with NextGen's standard site chrome (nav, footer). The EHI-relevant content is in the main body under the heading "EHI Data Export." It describes the EHI export program for four products: NextGen Enterprise EHR, NextGen Office, NextGen Direct Messaging, and Mirth Connect.

3. **Identified the Enterprise EHR data dictionary link:**
   ```bash
   grep -oiE 'href="[^"]*"' ehi-landing-page.html | grep -iE 'media/files'
   ```
   Found: `href="/-/media/files/legal/2025/DD_Complete_EHI_20250627"` — linked from the "NextGen® Enterprise EHR" section under "Database dictionary."

4. **Downloaded the data dictionary PDF:**
   ```bash
   curl -sL "https://www.nextgen.com/-/media/files/legal/2025/DD_Complete_EHI_20250627" \
     -H 'User-Agent: Mozilla/5.0' \
     -o DD_Complete_EHI_20250627.pdf
   ```
   Result: PDF document, 29,204,519 bytes (27.8 MB), 10,875 pages. Confirmed with `file` and `pdfinfo`.

5. **Took a full-page screenshot** of the landing page in the browser for archival.

6. **No other Enterprise EHR downloads found.** The page links to dictionaries for other products (NextGen Office, Direct Messaging, Mirth Connect) but those are separate certified products, not NextGen Enterprise EHR. There is only one download link for Enterprise EHR.

## What Was Found

### Landing Page Content

The page at the registered URL is a well-structured EHI export documentation page. Key statements:

- **"On this page, you will find database dictionaries that define the schema of the EHI data exports for each of NextGen Healthcare's certified health IT products."**
- The exported data is described as "machine-readable format."
- "The database dictionaries on this page outline the structure of each exported table and its corresponding data elements."
- "While certain EHI, such as images, documents, reports, and audio files are referenced in the tables, they are located in the corresponding file folders in the extract."
- Users needing human-readable format are directed to request a CCDA from their provider as an alternative.
- Enterprise EHR export is available in v6.2021.1 Cures and higher; the data dictionary "describes the EHI schema as of June 27, 2025."

### Data Dictionary PDF (DD_Complete_EHI_20250627.pdf)

This is a massive 10,875-page PDF containing a comprehensive SQL Server database schema dump for the NextGen Enterprise EHR EHI export. Key characteristics:

- **5,290 unique database tables** documented
- **283,279 total columns** across all tables
- Each table entry lists: Table Name, Column Name, Data Type (SQL Server types: char, varchar, int, datetime, uniqueidentifier, etc.), Default value, and Not Null constraint
- Tables are organized alphabetically
- No field descriptions, value set documentation, or relationship/FK documentation
- No table-level descriptions explaining what each table represents

### Export Format

The EHI export is a **direct database extract** — tables exported in machine-readable format with accompanying file folders for binary content (images, documents, reports, audio). This is a genuine (b)(10) approach: a full database dump of all patient-facing data, not a FHIR or C-CDA wrapper.

The schema uses SQL Server data types (char, varchar, nvarchar, int, datetime, uniqueidentifier, bit, float, money, image, xml, etc.), indicating the export reflects the underlying SQL Server database structure directly.

### Table Name Analysis

The table naming reveals the product's specialty-specific clinical depth. Sample categories observed:

- **Abortion/Reproductive health:** AB_Cervical_Dilator_hist_, AB_Intake_, AB_Procedure_, AB_Recovery_
- **ADHD:** ADHD_, ADHD_Parent_, ADHD_Teachr_, ADHD_Par_Score_
- **Behavioral health:** bh_aims_, bh_ansa_, bh_asam_, bh_contact_note_, bh_crisis_contact_note_, bh_group_progress_note_, bh_medication_data_, bh_psychopharm_
- **Cardiology:** CARD_patient_, CARD_DiagnosesAssessPlan_, card_device_charges_, CARD_PatientResults_
- **Ophthalmology:** oph_info_vfbilling_, eyeGlassesRx_, eyedischargeinstruct_
- **Orthopedics/PT:** AINF_PT_Note_edit_pop_, AINF_PT_single_visit_, work_status_report_
- **OB/GYN:** womens_family_hx_, womens_med_history_, well_woman_subjective_
- **Pediatrics:** well_child_soap_, ACEs_Pearls_Child_, ACEs_Pearls_Teen_
- **Vital signs:** VS_Adult_, vs_charts_adult_, vs_charts_peds_, WelchAllynVitals_
- **Billing:** info_procedure_billing_, card_device_charges_, claim_based_reporting_
- **Clinical orders/labs:** ainf_orders_, ainf_ord_labs_, diagnostics_all_orders_
- **Medications:** allergy_prescribe_, Associate_Medications_, clinical_pharmacist_
- **Insurance:** IORTSinsurance_forms_xpo2_, IORTSPR_Billing_preauth_
- **Demographics:** ainf_patient_enc_info_, CARD_patient_, CARD_PatientContact_
- **Assessments:** Asthma_Step_4c_, audiogram_, barriers_to_care_, chronic_condition_status_
- **Zika screening:** zika_preg_screening_, zika_preg_screening_ext_

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered (evidenced by table names in the data dictionary):**
- ✅ Clinical documentation / encounter notes (extensive specialty-specific tables)
- ✅ Demographics and patient identity (CARD_patient_, ainf_patient_enc_info_)
- ✅ Diagnoses / problem lists (diagnoses_sort_, Diagnostics_, chronic_condition_status_)
- ✅ Medications and allergies (allergy_prescribe_, Associate_Medications_, bh_medication_data_)
- ✅ Lab orders and results (ainf_ord_labs_, ainf_orders_findings_, CARD_PatientResults_)
- ✅ Vital signs (VS_Adult_, vs_charts_adult_, WelchAllynVitals_)
- ✅ Behavioral health assessments (bh_aims_, bh_ansa_, bh_asam_, bh_psychopharm_, ADHD_ tables)
- ✅ Specialty clinical data — cardiology, ophthalmology, orthopedics, OB/GYN, pediatrics, dermatology, and 20+ other specialties
- ✅ Procedure billing (info_procedure_billing_, card_device_charges_, IORTS_surg_billing_)
- ✅ Insurance/authorization (IORTSinsurance_forms_xpo2_, IORTSPR_Billing_preauth_)
- ✅ Care coordination (additional_plans_, additional_personnel_)
- ✅ Patient education (AINF_aud_education_)
- ✅ Images/documents/audio (referenced in tables, exported as files per landing page)
- ✅ Custom assessments / screening tools (ACEs_Pearls_, barriers_to_care_, zika_preg_screening_)

**Potentially missing or unclear:**
- ❓ **Immunization records** — no obviously named immunization table found in the sample, though could be under encounter data
- ❓ **Claims/billing detail** — while billing tables exist (info_procedure_billing_, claim_based_reporting_), the depth of financial data (AR, payments, denials) is unclear from table names alone
- ❓ **Patient portal messages** — secure messaging data not clearly identifiable
- ❓ **Referrals** — no obviously named referral tables found
- ❓ **Care plans / goals** — while additional_plans_ exists, dedicated care plan tables not clearly identified

**Not expected in EHI export (correctly excluded if absent):**
- Audit logs, system configuration, provider credentialing, scheduling infrastructure

### Export Format & Standards

- **Format:** SQL Server database extract in machine-readable format. The data dictionary documents SQL Server table/column schemas. Binary files (images, documents, reports, audio) are exported as separate files in folders.
- **Standard:** This is a proprietary database dump, not FHIR, C-CDA, or any external standard. This is entirely appropriate for (b)(10) — a direct database extract covers far more data than any standardized clinical document format could.
- **Reconstructability:** A third party could reconstruct the patient record from this export given the data dictionary, but it would require significant effort due to the lack of relationship documentation, field descriptions, and value set definitions. The schema is self-evident for many fields (e.g., `person_id`, `practice_id`, `encounter_id`) but domain-specific columns need contextual knowledge.

### Documentation Quality

- **Strengths:**
  - Comprehensive coverage: 5,290 tables, 283,279 columns — this is a full database schema
  - Every column has a data type specified
  - Machine-readable format for the export itself
  - Clear landing page explaining the export format and what to expect
  - Updated as of June 27, 2025 — actively maintained
  - Honest acknowledgment that binary content is in separate folders

- **Weaknesses:**
  - **No field descriptions** — column names are the only documentation. `chk_pt_edu_session` vs `chk_pt_multi_gest` requires domain knowledge to interpret.
  - **No value set documentation** — coded fields (int, varchar values that represent coded categories) have no enumeration of valid values
  - **No relationship/FK documentation** — how tables join is not documented. `person_id` and `enc_id` serve as implicit FKs but there's no ERD or relationship diagram.
  - **No table descriptions** — what each table represents must be inferred from naming conventions
  - **No sample data** — no example export files or worked examples
  - **PDF-only** — the 10,875-page PDF is not searchable in a practical way and there's no structured (CSV, JSON, SQL DDL) alternative provided
  - **No export procedure documentation** — no user guide for how to request or perform the export

### Structure & Completeness

- **Granularity:** Column-level with data types. This is more granular than many vendors (who only list table names) but less than ideal (missing descriptions, value sets, relationships).
- **Coded fields:** Not documented with value sets. A column like `insertion_type (varchar)` has no enumeration of valid values.
- **Relationships:** Not documented. The common pattern of `enterprise_id`, `practice_id`, `person_id`, `enc_id` as key columns across tables implies a hierarchical structure but it's never stated.
- **Versioning:** The document is dated June 27, 2025. No change history or versioning between releases.

### Overall Assessment

NextGen Healthcare has taken a **genuine and comprehensive approach to (b)(10) EHI export**. Rather than repackaging their FHIR (g)(10) API as their EHI export (a common pattern), they have built a full database extract mechanism that exports all patient-facing tables from their SQL Server database, plus binary files. With 5,290 tables covering 26+ medical specialties, this is one of the most comprehensive EHI export schemas in the industry.

The documentation, however, is a **bare-minimum data dictionary** — it tells you what columns exist and their SQL Server data types, but nothing about what the data means, how tables relate, or what values coded fields can take. A developer trying to import this data into another system would need significant reverse-engineering effort. The 10,875-page PDF format makes the dictionary nearly unusable without automated extraction (which we performed in the enrichment step).

The landing page is clear and well-written, properly distinguishing between machine-readable and human-readable formats and directing users to alternatives (CCDA) if needed. The vendor clearly understands the (b)(10) requirement and has built appropriate infrastructure — the documentation quality just hasn't kept pace with the export's breadth.

## Access Summary
- Final URL (after redirects): https://www.nextgen.com/sldkjljieo0935jljsrnfkl
- Status: found
- Required browser: no (curl works fine)
- Navigation complexity: direct_link (single page with one download link for Enterprise EHR)
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The registered URL worked directly, the page is well-structured, and the PDF downloaded without issues. No authentication, no Cloudflare, no JavaScript requirements. This is an exemplary URL registration.

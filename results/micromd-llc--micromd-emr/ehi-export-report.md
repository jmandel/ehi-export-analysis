# MicroMD, LLC — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.micromd.com/micromd-emr-certified/
- CHPL IDs: 11281
- Product: MicroMD EMR Version 20.0
- Certification date: 2023-04-27

## Navigation Journal

1. **Initial probe**: `curl -sI -L "https://www.micromd.com/micromd-emr-certified/" -H 'User-Agent: Mozilla/5.0'` returned HTTP 200, Content-Type: text/html. WordPress site.

2. **Fetched page**: `curl -sL "https://www.micromd.com/micromd-emr-certified/" -H 'User-Agent: Mozilla/5.0' -o /tmp/micromd-page.html` — 130,670 bytes. Static WordPress page with certification information.

3. **Found downloadable files**: Searched HTML for file links. Found one EHI-specific PDF:
   - `/docs/MicroMD-EMR-170.315b10-Electronic-Health-Information-export-EHI.pdf`
   - Also found: Real World Test Plans/Results (2022–2025), costs PDF, and a FHIR API documentation link (`https://micromd.dynamicfhir.com/micromd/basepractice/r4/Home/ApiDocumentation` — this is the (g)(10) API, not the (b)(10) export).

4. **Downloaded PDF**: `curl -sL "https://www.micromd.com/docs/MicroMD-EMR-170.315b10-Electronic-Health-Information-export-EHI.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/MicroMD-EMR-170.315b10-Electronic-Health-Information-export-EHI.pdf` — confirmed as PDF document, 17 pages, 326,238 bytes.

5. **Examined page in browser**: Navigated to URL, took screenshot. Page is a single certification information page with the EHI PDF link prominently listed alongside other certification materials. The EHI link text reads "170.315 (b) (10) Electronic Health Information export (EHI)" and links directly to the PDF.

6. **Verified no additional content**: The page contains no accordion sections, embedded documentation, or additional EHI-specific content beyond the PDF link. The FHIR API link is a separate (g)(10) concern.

## What Was Found

The EHI export documentation is a single 17-page PDF dated February 6, 2026 (recently updated), authored by "Creative Group" in Microsoft Word. It describes MicroMD EMR's (b)(10) EHI export mechanism and provides a complete XML schema for the export output.

### Export Format

The export produces a **compressed (ZIP) file** that is:
- Named with the convention `{practiceId}.{patientChartId}.0`
- Password-protected using the patient's date of birth (mmddyyyy format)
- Contains multiple **XML files** following a proprietary schema

The documentation refers to a "user manual for instruction" on how to perform the export, but this user manual is not publicly available on the page.

### XML File Schema

The export consists of **10 XML files** plus additional DMS (Document Management System) files:

1. **Billing.xml** — Superbills with CPT codes, diagnoses (ICD/SNOMED), procedures, modifiers, referring physicians, and insurance information per transaction.

2. **Encounters.xml** — The most detailed file. Contains encounter metadata plus nested elements for:
   - Reasons for visit (with SNOMED codes)
   - Assessments (ICD codes, SNOMED codes, with detail descriptors)
   - Subjective findings (SOAP S-section)
   - Objective findings (SOAP O-section)
   - Review of problems
   - Medications (with NDC, RxNorm, GCN seq numbers, sig details, multi-sig support)
   - Plans (orders, lab orders, referrals, vaccinations, procedure codes)
   - Face time records
   - Medical info links
   - Encounter notes (text and audio recordings, graphics)

3. **HealthScreening.xml** — Contains:
   - Goal monitoring with progress tracking
   - Health concerns with related concerns, risks, and care teams
   - Health screenings (questionnaires with questions, answers, follow-ups, results, sections — LOINC-coded)
   - Immunizations (CVX codes, NDC, VIS sheets, lot numbers, administration details, side effects)
   - Risk factors
   - Prevention programs with details and associated programs

4. **Histories.xml** — Family, medical, social, surgical history, plus:
   - Birth history (Apgar scores, delivery details)
   - Sexual history
   - Asthma history (detailed trigger and symptom tracking)
   - Habit tracking
   - Hospitalization records (with procedures, diagnoses, reports)
   - Consent history

5. **MedicalInfo.xml** — Core clinical data:
   - Allergies (with coded types, severity, reactions)
   - Problems/conditions (ICD-10, SNOMED codes, with cancer staging data)
   - Vitals (BP, HR, RR, temp, BMI, O2 sat, pain, head circumference, OB-specific vitals)
   - Medications (comprehensive: NDC, RxNorm, GCN, dispensing details, refill info)
   - Test results (LOINC-coded, with normal ranges, abnormal flags)
   - Behavioral health screenings (questionnaire format)
   - Clinical decision support alerts, actions, references, recommendations, treatments
   - Ultrasound/PIMD data (detailed fetal measurements)
   - Operations (procedures, diagnoses, medications, flow records, personnel)
   - Treatment plans (objectives, problems, medications, interventions, progress, care teams)

6. **Miscellaneous.xml** — Attachments, letters, advance directives, patient education, referrals in, and transitions of care.

7. **Orders.xml** — Orders with category, priority, sender/receiver, status, and associated work-to-do items.

8. **Patient.xml** — Demographics (including SOGI data, race/ethnicity, multiple addresses), family members, contacts, insurance policies (with detailed plan and policyholder information), providers (practice and referring), and consent records (including CCM consent details).

9. **Schedule.xml** — Appointment records with status, provider, times, department, and specialty.

10. **Specialty.xml** — Specialty-specific data modules:
    - Vision (detailed ophthalmic tests including acuity, tonometry, confrontation, color vision)
    - Hearing (audiometric levels, thresholds, reports)
    - Diabetes (insulin tracking, dose management, pump basal rates)
    - Pediatric developmental assessments
    - Genetic screenings with family relationships
    - Geriatric assessments (questionnaire format)
    - Allergy testing (skin test results)

11. **WomenHealth.xml** — Obstetric and gynecologic data:
    - Obstetric care episodes (comprehensive prenatal data)
    - Initial physical exams
    - Detailed OB medical history (40+ condition fields)
    - Genetic screenings
    - Deliveries (with fetal data, labor events, complications)
    - Prenatal visits (fundal height, cervical status, fetal monitoring)
    - Estimated date of delivery calculations
    - Progress of labor records
    - Pregnancy history (with fetal outcomes)
    - Gynecology history
    - Menstrual history
    - Family planning

12. **Additional DMS files** — "Additional files will be included from the document management system. These will have the file name and format as saved in the DMS system. They may include pdf, doc, rtf, ccd, xml, image formats, etc."

## Export Coverage Assessment

### Data Domain Coverage

This is a genuinely comprehensive (b)(10) export that covers data well beyond the USCDI/US Core subset. Comparing against the product research:

**Clearly covered:**
- Clinical encounters and SOAP documentation
- Billing/superbill data (CPT codes, diagnoses, modifiers, insurance)
- Problem lists, medication lists, allergy lists
- Immunization records (detailed, CVX/NDC coded)
- Lab/test results (LOINC coded)
- Vital signs
- Patient demographics (including SOGI, race/ethnicity)
- Insurance information (detailed plan data)
- Family/medical/social/surgical history
- Health screening questionnaires
- Clinical decision support alerts
- Advance directives
- Patient education records
- Referrals (in and out via transitions of care)
- Orders
- Appointment scheduling
- Specialty-specific data (vision, hearing, diabetes, pediatric, geriatric, allergy testing)
- Women's health/OB-GYN (extremely detailed)
- Attachments and documents (from DMS integration)
- Care plans/treatment plans with goals and progress
- Consent records
- Operations/surgical procedures

**Partially covered or ambiguous:**
- **Practice management financial data**: Billing.xml includes superbill-level data (CPT codes, insurance references, payment methods), but it's unclear whether full accounts receivable, payment posting, ERA/EOB data, claims adjudication status, and collections data are included. The billing data appears to capture the clinical billing events but may not capture the full financial lifecycle.
- **Patient portal content**: Secure messages between patient and practice are not explicitly mentioned in the schema. The portal interaction data may not be in the export.
- **Audit trails**: No explicit audit log or access history export is documented. While individual records have `recordedby` and `recordedon` fields (basic provenance), there's no dedicated audit log export.
- **E-prescribing transaction logs**: Medications include prescription IDs and pharmacy instructions, but the Surescripts transaction history itself is not explicitly represented.

**Appears missing:**
- **Full practice management accounting**: Payment posting, ERA processing, patient statement history, collections account data — the PM module data appears absent beyond superbill-level billing.
- **Document content**: DMS files are included as attachments but the DMS indexing/metadata (filing categories, annotation data) is only partially captured in the Attachment element.
- **Communication logs**: Patient-practice secure messages, appointment reminders sent, post-visit surveys.
- **User/provider management data**: Provider credentials, privileges, staff records (beyond what's in encounter contexts).

### Export Format & Standards

The export uses a **proprietary XML format** — not FHIR, not C-CDA, not any external standard. This is entirely appropriate for a (b)(10) export that needs to capture everything the product stores. Key observations:

- **Well-structured XML**: The schema is hierarchical, with logical grouping of related data (encounters contain their assessments, medications, plans; patients contain their addresses, contacts, insurance).
- **Standard code systems referenced**: Fields reference ICD-10 (`icdcode`), SNOMED (`snocode`), CPT (`cptcode`), CVX (`cvxcode`), NDC (`ndc`), RxNorm (`rxnorm`), LOINC (`loinc`), and NPI (`npi`). This means the data is coded, not just free text.
- **Relationships via IDs**: Records are linked via IDs (`patientid`, `encounterid`, `transactionid`, `medicationid`, etc.), allowing reconstruction of relationships.
- **Per-patient export**: The export is patient-scoped — each export file is for a single patient chart.
- **Password protection**: The ZIP uses the patient DOB as password, which is a minimal security measure.

A third party could reconstruct the clinical record from this export, though they would need to understand MicroMD's data model to interpret all the fields — many field names are self-explanatory (e.g., `firstname`, `icdcode`, `doseamount`) but some require domain knowledge (e.g., `gcnseqno`, `ADPType`, `bdagetype`).

### Documentation Quality

**Strengths:**
- The document provides the **complete XML schema** for every export file, listing every element and attribute
- The hierarchical nesting is clear
- The format is self-documenting in that most attribute names are descriptive
- The document is well-organized by file, with each XML file getting its own section
- Recently updated (February 2026), suggesting active maintenance

**Weaknesses:**
- **No field-level descriptions**: Attributes are listed but never defined. What does `confidentiality` mean? What values can `billingstatus` take? What's the format of date fields?
- **No data type specifications**: No indication of which fields are dates, integers, strings, coded values, etc.
- **No value sets**: Coded fields like `maritalstatus`, `billingstatus`, `encountertype` lack enumeration of valid values
- **No cardinality**: No indication of which elements can repeat or are required vs. optional
- **No sample data**: No example export files or records showing what populated data looks like
- **No import instructions**: A developer receiving this export would have to reverse-engineer the data types and value sets
- **User manual referenced but not provided**: The document says "see user manual for instruction" on how to perform the export, but the manual is not publicly available
- **No versioning information**: No indication of schema version or change history

### Structure & Completeness

The documentation operates at the **attribute-name level** — it tells you exactly what fields exist in each XML element, which is more granular than just listing table names, but less granular than a full data dictionary with types, constraints, and descriptions. It is essentially an XML Schema rendered as prose, but without the formal type information that an actual XSD would provide.

The export is clearly the result of genuine (b)(10) work, not a repackaged (g)(10) FHIR API. It exports the full breadth of MicroMD's data model — billing, specialty workflows, OB/GYN, scheduling, DMS attachments — well beyond what any FHIR US Core API would cover. The proprietary XML format is appropriate for this purpose.

The critical gap is the lack of field-level documentation. A recipient of this export would know the structure but would need to guess at data types, valid values, and the meaning of ambiguous field names. Adding an actual XSD and a field glossary would significantly improve the documentation.

## Access Summary
- Final URL (after redirects): https://www.micromd.com/micromd-emr-certified/
- Status: found
- Required browser: no
- Navigation complexity: one_click (single PDF link on certification page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles encountered. The page loaded cleanly via curl and in the browser.
- The FHIR API documentation link (`https://micromd.dynamicfhir.com/micromd/basepractice/r4/Home/ApiDocumentation`) was noted but not downloaded — it documents the (g)(10) Standardized API, not the (b)(10) EHI export. The EHI export uses a completely separate proprietary XML format, so the FHIR API docs are irrelevant to the export.
- The "user manual for instruction" on performing the export is referenced in the PDF but not publicly available on the certification page.

# ChartPath, LLC — Product Research

Researched: 2026-02-16
Developer website: https://www.chartpath.com

## Overview

ChartPath, LLC is an Austin, Texas-based healthcare technology company that develops a cloud-based EHR system purpose-built for long-term and post-acute care (LTPAC) physician practices. The company was founded in 2012 by Buzz White under the name **Afoundria** and rebranded to **ChartPath** in March 2021 to align with its flagship product name. ChartPath was subsequently acquired by **LivTech**, a Tennessee-based private equity-backed portfolio company (PSG Equity) that operates multiple healthcare SaaS businesses, including PUREDI (billing) and Sertus. Within LivTech, ChartPath sits under the Physician Division.

ChartPath is a small-to-mid-size niche vendor focused exclusively on the LTPAC space. As of its 10-year anniversary in late 2022, the company reported serving **250+ practices** and **4,000+ users**, having processed over **7 million patient encounters**. It is not publicly traded. Pricing is approximately $329/clinician/month for the EHR and $199/clinician/month for RCM services. The company employs a direct sales model and appears to serve primarily small-to-mid-sized physician groups that round on patients in skilled nursing facilities (SNFs), assisted living facilities (ALFs), and other LTPAC environments.

## Product: ChartPath

CHPL IDs: 10258

### What It Is

ChartPath is a cloud-based EHR system designed specifically for **physician practices that provide rounding-based care in post-acute and long-term care facilities** — primarily skilled nursing facilities (SNFs) and assisted living facilities (ALFs). This is a distinct niche: ChartPath is not the facility's own EHR (that's typically PointClickCare, MatrixCare, or similar), but rather the **physician group's EHR** used by clinicians who visit and round on patients across multiple facilities.

The certified module (ChartPath EHR v1.29) appears to be the core and entirety of the product — there's no indication of separate certified components or a larger platform umbrella. However, the product has expanded over time to include revenue cycle management (RCM) services alongside the clinical EHR.

The SED intended user description — "Clinicians, Assistants, and Scribes, PALTC" — accurately reflects the product's focus on physician-led care teams in post-acute and long-term care settings.

### Users & Market

**Primary users**: Physicians (MDs/DOs), nurse practitioners (NPs), physician assistants (PAs), medical assistants, and scribes who round on patients in SNFs, ALFs, and other LTPAC settings. These clinicians typically manage patients across multiple facilities, visiting each facility on a regular rounding schedule.

**Clinical settings**: Skilled nursing facilities, assisted living facilities, and other sub-acute/long-term care environments. ChartPath is not used in hospitals, ambulatory clinics, or outpatient offices — its entire design is oriented around the facility-rounding workflow.

**Scale**: 250+ practices, 4,000+ users as of late 2022 (per 10-year anniversary press release). This is a small niche vendor — user reviews on third-party sites number only 5-10 across all platforms.

**GUIDE Model participation**: ChartPath has positioned itself as a CMS GUIDE (Guiding an Improved Dementia Experience) Model-ready EHR. The GUIDE Model is a CMS initiative launched in 2024 for dementia care that requires participants to use a certified EHR. ChartPath markets specific features aligned with GUIDE requirements, including dementia staging and caregiver burden assessments.

**Third Eye Health partnership**: In 2024, ChartPath partnered with Third Eye Health, a virtual care company, to integrate telehealth services for after-hours coverage, indicating the product supports telehealth-enabled encounters.

### Modules & Functionality

Based on vendor website, press releases, third-party reviews, and feature descriptions:

**Clinical Documentation & Charting**
- Single-page encounter template designed for speed during facility rounding (per vendor site and reviews)
- Clinical decision support suggesting relevant codes and documentation elements (per vendor)
- One-click "pull forward" of prior charts for continuity across visits (per vendor)
- Customizable templates for various visit types: annual wellness visits, behavioral health, primary care, physical medicine and rehabilitation (per FindEMR)
- Scored screening tools for anxiety, dementia, depression, and other common conditions (per vendor GUIDE program page)
- Dementia staging and caregiver burden assessments (per vendor GUIDE program description)
- Mobile-friendly interface for phone/tablet use during facility rounds (per vendor and reviews)

**Census Management**
- Multi-facility census management — clinicians can view and manage patient panels across all their facilities from a single system (per vendor)
- Patient flagging for prioritization and care coordination (per FindEMR)
- No need to log into multiple systems for different facilities (per vendor)

**E-Prescribing**
- Integrated electronic prescribing with ability to send prescriptions to the patient's preferred pharmacy (per vendor; certified for (a)(2) — CPOE for medications)
- Certified for (a)(14) — implantable device list, suggesting device data is tracked

**Billing & Revenue Cycle Management**
- Smart coding that automatically suggests CPT codes based on clinical note content (per vendor)
- RVU (Relative Value Unit) tracking for provider productivity monitoring (per FindEMR)
- Two RCM products launched in 2021: **ChartPath RCM** (self-service billing SaaS) and **ChartPath RCM Pro** (outsourced white-glove billing service) (per 2021 rebrand press release)
- Claims tracking, reimbursement management (per vendor)
- Automatic note transmission to facility and billing service upon completion (per vendor)
- **Note**: Some user reviews on Software Finder reported that billing functionality was limited and not always suitable as a standalone billing solution. One review noted incompatibility with being used as the "source of truth" for insurance data, suggesting some practices use external billing systems.

**Integrations & Interoperability**
- **PointClickCare integration**: Bidirectional — pulls patient demographics from PointClickCare into ChartPath and publishes completed notes back to the PointClickCare patient record (per 2024 blog post)
- **MatrixCare integration**: Listed as an interoperable partner (per web search results)
- **HIE interoperability**: Interoperable with health information exchange platforms for sending/receiving patient notes, intake forms, medication records, orders, and other clinical information (per vendor)
- **FHIR API**: Certified for (g)(10) — standardized FHIR API access
- Certified for (b)(1) and (b)(2) — transitions of care, C-CDA document exchange
- Certified for (h)(1) — Direct messaging

**Reporting & Analytics**
- Built-in reporting tools for operational and clinical insights (per FindEMR)
- RVU and productivity tracking (per vendor)
- Certified for (c)(1), (c)(2), (c)(3) — clinical quality measures (CQMs)

**Automation Marketplace** (announced 2024)
- Third-party integration marketplace offering vetted tools including AI scribing, auditing, reporting, and handwritten note transcription to structured clinical encounters (per 2024 press release)
- Positions ChartPath as a platform with an extensible ecosystem rather than a monolithic product

**Telehealth**
- Integrated video consultation capability (per vendor marketing)
- Third Eye Health partnership for after-hours virtual care coverage (per 2024 press release)

**Public Health Reporting**
- Certified for (f)(5) — cancer case reporting and (f)(7) — health care surveys

### Data & Content

Based on certified criteria, vendor descriptions, integration details, and user reviews, ChartPath stores and manages the following types of data:

**Clinical encounter data**: The core data type — clinical notes from physician rounding encounters in LTPAC facilities. Includes assessment findings, diagnoses, treatment plans, and follow-up plans. The single-page encounter template and one-click pull-forward features indicate structured and semi-structured encounter documentation.

**Patient demographics**: Patient identifying information, managed both natively and pulled from facility EHRs like PointClickCare. Census management across multiple facilities implies facility-patient assignment data.

**Medication data**: E-prescribing certification (a)(2) confirms the system stores medication lists, prescriptions, and pharmacy information. Drug-drug and drug-allergy checking ((a)(5)) implies allergy data is stored.

**Problem/diagnosis lists**: Clinical documentation and CQM reporting capabilities imply active problem lists and diagnosis codes (ICD-10).

**Screening/assessment scores**: Scored tools for anxiety, dementia staging, depression, caregiver burden, and other conditions — this is structured data specific to the LTPAC population.

**Implantable device data**: Certified for (a)(14), indicating the system maintains an implantable device list.

**Billing/claims data**: CPT codes, RVU data, claims, and reimbursement tracking. The depth of billing data stored likely varies by whether the practice uses ChartPath RCM vs. an external billing service.

**Orders**: The PointClickCare integration and HIE interoperability mention sending/receiving "orders," suggesting order data is stored.

**Care coordination data**: Patient flagging, multi-facility census management, and GUIDE Model care navigator features suggest care coordination metadata.

**C-CDA documents**: Certified for (b)(1) and (b)(2), indicating the system can generate and consume Consolidated Clinical Document Architecture documents for transitions of care.

**Audit data**: Certified for (d)(2) through (d)(9), indicating comprehensive audit logging, integrity checking, and access control data.

**What's less clear**:
- **Lab results**: No explicit mention of lab ordering or results management in any source reviewed. The product doesn't appear to be certified for (a)(3) — CPOE for labs — so it may not natively manage lab data, though it could receive lab results via C-CDA or FHIR.
- **Imaging/radiology**: No mention of imaging data or PACS integration.
- **Patient portal / patient-facing access**: The product is certified for (e)(3) — patient health information export on request — but not (e)(1) (view/download/transmit via patient portal). This suggests the product does not have a patient-facing portal; patient data access is likely handled via FHIR API or on-request export.
- **Scheduling**: Some search results mention scheduling, but user reviews noted limitations in scheduling features. It's unclear how robust appointment/scheduling data management is.
- **Document management**: The Automation Marketplace includes handwritten note transcription, suggesting some document/file storage capability, but the extent is unclear.
- **Social determinants / HRSN data**: GUIDE Model requires Health-Related Social Needs screenings, suggesting ChartPath may store HRSN data, but this wasn't explicitly confirmed in sources reviewed.

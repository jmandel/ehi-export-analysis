# Practice Fusion — Product Research

Researched: 2026-02-14
Developer website: https://www.practicefusion.com

## Overview

Practice Fusion is a cloud-based electronic health record (EHR) platform designed for small, independent ambulatory medical practices. Founded in 2005 by Ryan Howard in San Francisco, it grew rapidly as one of the first free, ad-supported EHRs and became the fastest-growing EHR in the US by 2014, when it facilitated over 56 million patient visits (approximately 6% of all US ambulatory visits).

Practice Fusion was acquired by Allscripts in January 2018 for $100 million, a significant markdown from its earlier private valuation. In January 2020, the DOJ announced a $145 million settlement with Practice Fusion for criminal and civil violations of the Anti-Kickback Statute — the first-ever criminal action against an EHR vendor. Practice Fusion had accepted kickbacks from a pharmaceutical company to implement clinical decision support alerts that steered physicians toward prescribing opioid medications. In January 2023, Allscripts renamed itself Veradigm Inc., and Practice Fusion now operates as a Veradigm Network solution, maintaining its own brand identity within the Veradigm portfolio.

The developer contact email (jennifer.distefano@veradigm.com) confirms the Veradigm ownership. Practice Fusion has transitioned from its earlier free/ad-supported model to a paid subscription starting at $199/month per provider with a required annual commitment.

## Product: Practice Fusion EHR

CHPL ID: 11507 (15.04.04.2924.Prac.37.01.1.240826)

### What It Is

Practice Fusion EHR v3.7 is a 100% cloud-based EHR that requires no software downloads or local hardware. It runs in a web browser and supports charting from laptops, tablets, and mobile phones. The platform is ONC-certified (certification date August 26, 2024) and is broadly certified across clinical, care coordination, patient portal, quality reporting, public health, and API criteria.

Practice Fusion is offered in four packaging tiers:
1. **EHR with Billing Services** — full EHR plus end-to-end managed billing (white-glove RCM)
2. **EHR with Billing Software** — full EHR plus self-service billing tools
3. **Standalone EHR** — clinical EHR only, focused on patient care
4. **ePrescribe** — certified e-prescribing as a standalone capability

Additional required software noted on the mandatory disclosures page includes Updox, Veradigm FollowMyHealth (patient portal), and MedAllies — indicating that the patient portal and some health information exchange capabilities are delivered through partner/sibling products within the Veradigm ecosystem rather than being built natively into Practice Fusion.

### Users & Market

Practice Fusion serves approximately 30,000 medical practices, over 112,000 healthcare professionals, and 5 million patients per month. It is positioned as the #1 cloud-based ambulatory EHR in the US. Among solo and small practices (1-3 clinicians), Practice Fusion holds the largest market share at 12%, with 40% more market share than its nearest competitor (eClinicalWorks) in the solo provider segment. In the broader overall ambulatory EHR market, its share is approximately 0.89%.

The platform supports 53+ medical specialties, including:
- Primary care, family medicine, internal medicine, general practice
- Cardiology (disease and interventional), clinical cardiac electrophysiology
- Dermatology, endocrinology, gastroenterology, hepatology
- Neurology, neurosurgery, psychiatry, child/adolescent psychiatry, psychology
- Obstetrics/gynecology, pediatrics, geriatric medicine
- Orthopedic surgery, general surgery, colon/rectal surgery, thoracic surgery, plastic surgery, transplant surgery
- Allergy/immunology, infectious disease, pulmonary disease, rheumatology, nephrology, hematology, oncology
- Ophthalmology, optometry, otolaryngology/ENT
- Emergency medicine, hospitalist, pain medicine
- Anesthesiology, diagnostic radiology, nuclear medicine, pathology
- Chiropractic, naturopathy, nutritionist, osteopathic medicine, podiatry
- Occupational medicine, physical medicine and rehabilitation, facial plastic surgery, urology, medical genetics

The product provides 130+ built-in customizable clinical templates. It also serves over 300 free and charitable clinics.

Day-to-day users include physicians (charting, ordering, prescribing), clinical staff (patient intake, documentation support), billing staff (superbills, claims), practice managers (scheduling, reporting), and patients (via the FollowMyHealth portal).

### Modules & Functionality

Based on vendor website, Veradigm product page, mandatory disclosures, and EHI export documentation:

**Clinical Documentation & Charting**
- Intuitive charting interface accessible from any device
- 130+ free, customizable clinical templates
- Clinical worksheet summaries and detail documentation
- Encounter-based documentation with addendums
- Encounter observations and procedures tracking
- Pinned notes for important patient information
- Family medical history and family history diagnoses
- Patient education resources
- Health concerns and patient goals
- Advance directives
- Smoking status tracking
- Patient risk scores
- Healthcare device tracking

**Clinical Decision Support**
- Drug-drug interaction alerts
- Drug-allergy interaction alerts
- Drug alert overrides tracking (per EHI export: patient-drug-alert-overrides.tsv)
- Evidence-based clinical recommendations at point of care

**Computerized Provider Order Entry (CPOE)**
- Medication orders (certified (a)(1))
- Lab orders (certified (a)(2))
- Imaging/radiology orders (certified (a)(3))

**Electronic Prescribing**
- Certified e-prescribing including controlled substances (EPCS)
- Drug interaction checking and formulary support
- Prescription history and transaction tracking
- Pharmacy network integration (preferred pharmacy management)
- Medication history with patient consent tracking
- Immunization VIS editions management

**Lab & Imaging Integration**
- Integration with 500+ lab and imaging centers
- Lab order management (items, diagnoses, specimens, documents)
- Lab result management (results, tests, observations, notes, specimen data)
- Direct ordering from within the EHR
- Results delivered into patient records for sharing

**Appointment Scheduling**
- Multi-facility, multi-provider side-by-side scheduling views
- Customizable event types
- Automated appointment reminders (reducing no-shows)
- Patient self-scheduling via portal
- Insurance eligibility checking at scheduling

**Patient Portal & Engagement (via Veradigm FollowMyHealth)**
- Patient access to health records, lab results, appointment schedules
- Secure messaging between patients and providers (messages, attachments, recipients tracked)
- Paperless patient intake forms
- Patient questionnaires
- Communication settings and preferences management
- Free patient portal access

**Billing & Revenue Cycle**
- Superbill generation with diagnoses, procedures, modifiers, and insurance linkage
- Superbill event tracking
- Insurance management (policies, eligibility verification)
- Patient guarantor management
- Patient restrictions tracking
- Contact profiles for billing
- Encounter document management
- Integrated clearinghouse for claims processing
- **Billing Services option**: payer enrollment, compliance, claims scrubbing, claims submission, denial management, refund processing, insurance A/R, credit balance monitoring, payment posting, reconciliation, financial reporting — with dedicated billing team and patient call center
- **Billing Software option**: self-service billing tools with flexible payment options
- Per-visit pricing model for billing services; average 30-day go-live

**Referral Management**
- Referral records with recipient tracking
- Paperless faxing for referral documentation

**Reporting & Analytics**
- Quality metrics: eCQM dashboard, Meaningful Use / Promoting Interoperability tracking, MIPS performance category management
- Clinical intelligence: chart note searchability, diagnosis registry by condition, medication/prescription history reporting, patient lists by clinical/demographic criteria, referral tracking
- Practice management: appointment and eligibility reporting, billing/superbill management, payer and prior authorization tracking, activity/audit reporting with filtering
- CQM updates delivered automatically
- ICD-10 and healthcare policy compliance updates

**Care Team & Provider Management**
- Care team assignment and profiles
- Provider profiles and user management
- Multi-facility management

**Public Health Reporting**
- Immunization registry reporting (f)(1) — with transmission history tracking
- Electronic case reporting (f)(5)

**Interoperability & Data Exchange**
- FHIR R4 APIs (g)(7), (g)(10)
- Transitions of care via C-CDA (b)(1)-(b)(3)
- Electronic notifications (b)(10), (b)(11) — ADT-type event notifications
- 600+ third-party developer marketplace
- Integration with Updox, MedAllies for health information exchange

### Data & Content

The EHI export documentation (v9) reveals 89 TSV files across 8 categories, providing a comprehensive view of all data stored in the system:

**Demographics & Patient Identity (10 files)**
- Patient demographics, race, ethnicity, gender identity, sexual orientation
- Tribal affiliation, occupation/industry, financial resources
- Communication settings and preferences
- Patient contacts (emergency contacts, guarantors, etc.)
- Appointment records

**Patient Documents & Questionnaires (2 files)**
- Uploaded/attached documents
- Patient questionnaire responses

**Clinical Data (33 files)** — the largest category:
- Encounters (with addendums, events, observations, procedures, diagnoses, medications)
- Conditions and diagnoses (current problem list)
- Allergies and allergy reactions
- Clinical worksheet summaries and detail
- Family medical history and family history diagnoses
- Immunizations and immunization registry records
- Advance directives
- Patient goals and health concerns
- Patient education records
- Healthcare devices
- Smoking status
- Patient risk scores
- Pinned notes
- Care team assignments and profiles
- Provider profiles, providers, users, facilities

**Billing & Insurance (12 files)**
- Patient insurances and insurance eligibilities
- Patient guarantors
- Patient restrictions
- Superbills with linked diagnoses, procedures, procedure modifiers, insurances, and events
- Encounter documents
- Contact profiles

**Medications & Prescriptions (11 files)**
- Patient medications (current list)
- Patient medication history
- Medication history consent records
- Prescriptions and prescription transactions
- Encounter-level medications
- Drug alert overrides
- Pharmacies and preferred pharmacy designations
- Immunization VIS editions
- Immunization transmission history

**Labs (16 files)** — notably detailed:
- Lab orders (with items, item diagnoses, item specimens, item answers, documents)
- Lab results (with tests/observations, observation notes, observation diagnoses, notes, documents, item specimen data, item notes)
- Labs reference data

**Referrals (2 files)**
- Patient referrals
- Referral recipients

**Messaging (3 files)**
- Patient messages
- Message recipients
- Message attachments

The FHIR API supports standard USCDI data elements for third-party application access and bulk data export.

Billing data is present but notably structured around superbills (the clinical-to-billing handoff document) rather than full claims lifecycle data, which aligns with Practice Fusion's model where deep billing/RCM is either handled by their managed billing service team or by the practice using external billing software. The EHR captures the clinical and superbill layer; full claims processing appears to happen in the clearinghouse/billing layer.

The mandatory disclosures page references separate cost documentation and API fee schedules as downloadable Excel/PDF files, but does not display their contents inline.

## Research Notes

- The EHI export documentation page (v9) was briefly reviewed during research to understand the data model; detailed analysis is deferred to Phase 2.
- The patient portal (FollowMyHealth) is a separate Veradigm product, not native to Practice Fusion — this is important for understanding data boundaries.
- Billing capabilities are superbill-centric within the EHR; full claims lifecycle processing happens in external billing services/software.
- Full source list available in sources.json.

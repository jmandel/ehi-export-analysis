# Carepaths Inc — Product Research

Researched: 2026-02-15
Developer website: https://www.carepaths.com

## Overview

Carepaths Inc is a small, private behavioral health technology company based in Florida (Jupiter/Vero Beach), founded around 2000. The company was started by two psychologists who saw a role for technology in behavioral health practice; they initially developed an outcomes tracking system and then expanded into a full EHR. Barrett Griffith serves as CEO/CTO, having been named to the role after three years as CTO. The company has over two decades of experience in behavioral health software.

CarePaths is a niche vendor focused exclusively on behavioral health — psychiatrists, psychologists, marriage and family therapists, counselors, addiction specialists, social workers, nurse practitioners, and training clinics. Their website reports processing over 8 million claims and 14 million patient appointments, with 805,000 assessments completed. The product is priced at $49/month per primary clinician, positioning it as an affordable option for solo practitioners and small-to-mid-size behavioral health practices. The company appears to be small (likely under 50 employees based on available signals), competing on affordability and behavioral-health-specific features rather than broad enterprise capabilities.

## Product: CarePaths EHR

CHPL IDs: 10607
Version: 19.11
Certification date: 2021-04-08
SED intended users: Behavioral Practitioners

### What It Is

CarePaths EHR is an all-in-one, cloud-based behavioral health EHR and practice management platform. It is not a component of a larger system — the certified module *is* the full product. The platform combines clinical documentation, practice management (scheduling, billing, claims), measurement-based care (outcomes tracking), teletherapy, a patient portal, and a patient-facing mobile app (CarePaths Connect) into a single integrated system.

The product is certified for 20+ ONC criteria including clinical capabilities (CPOE for labs, demographics, family health history), transitions of care, patient portal (view/download/transmit), FHIR API access, and EHI export. It is *not* certified for public health reporting criteria or standalone e-prescribing criteria, though e-prescribing is offered through a DrFirst/Rcopia integration (at additional cost of $75 setup + $40/month per prescriber).

### Users & Market

**Target users**: Behavioral health practitioners — psychiatrists, psychologists, therapists (MFT, LPC), social workers, addiction specialists, nurse practitioners, and training clinics/supervisees.

**Clinical settings**: Primarily solo practitioners and small-to-mid-size group practices in outpatient behavioral health. The supervisor/supervisee workflow support suggests use by training programs and practices with licensed/unlicensed clinician pairs.

**Market position**: Small niche vendor in the behavioral health EHR space, competing on price ($49/month) and behavioral-health-specific functionality. Rated 4.3 stars across 46 reviews (per vendor website). Reviews on FindEMR indicate users from practices with 1-50 employees. Not a major enterprise vendor.

**No notable large-scale deployments** were found in the research. The product appears oriented toward individual practitioners and small groups rather than large behavioral health organizations or health systems.

### Modules & Functionality

Based on vendor website, feature pages, and third-party review sites:

**Clinical Documentation**
- Extensive library of clinical templates for intakes, progress notes, treatment plans, case management assessments, and outcomes assessments (vendor website, practice management page)
- Forms maker enabling users to edit templates or create custom clinical documents (vendor website)
- Smart note prepopulation: new progress notes auto-populated from previous patient entries (clinical documentation feature page)
- Batch document generation for group and family sessions (clinical documentation feature page)
- Supervisor review and co-signing workflow (clinical documentation feature page)
- AI-powered session summaries for generating clinical notes from teletherapy sessions (product page)

**Measurement-Based Care (MBC) / Outcomes Monitoring**
- Automated weekly patient assessments delivered via patient portal or CarePaths Connect app (MBC product page)
- Library of standardized instruments across three categories (MBC product page):
  - Adult: GAD-7, PHQ-9, OQ-45, HAM-A, and 20+ others (anxiety, depression, PTSD, OCD, substance use)
  - Child: ADHD, autism spectrum screening, anxiety, behavioral assessments (YOQ, SCARED)
  - Special populations: postpartum depression (EPDS), eating disorders, geriatric depression, quality of life
- Results displayed as graphs at top of patient chart showing progress over time (MBC product page)
- Customizable assessment batteries with clinician-defined schedules and automatic reminders
- Aggregate reporting at clinician, program, clinic, and PRN level for quality improvement and benchmarking (vendor website)
- Tracks anxiety, depression, wellbeing, loneliness, medication adherence, patient confidence in therapist/treatment (mobile app page)

**Practice Management / Scheduling**
- Calendar management for individual clinicians and group practices (practice management page)
- Patient self-scheduling via patient portal and mobile app (practice management page)
- Appointment reminders via email/text (product page)
- Support for multiple office locations and unlimited users (practice management page)

**Billing, Claims & Accounting**
- Automated charge posting: completing a progress note or intake automatically posts charges and generates claims (clinical documentation page, vendor website)
- Claims generated in X12 format for electronic submission to payers (vendor website)
- Built-in claim validation rules to ensure clean claims (vendor website)
- Electronic remittance processing with auto-posting of insurance payments (vendor website)
- Credit card payment processing with auto-posting (vendor website)
- Patient accounting: posting of payments and adjustments, invoice/statement generation in customizable styles (vendor website)
- Integrated CPT coding with compliance updates (CPT billing feature page)
- Free insurance eligibility lookups (home page)

**E-Prescribing**
- Integrated via DrFirst/Rcopia platform (mandatory disclosures page)
- Separate per-prescriber fee ($75 setup + $40/month) (product page)
- Medication monitoring capabilities (FindEMR)

**Teletherapy**
- Built-in HIPAA-compliant video sessions supporting up to six participants (product page)
- Launched directly from patient chart (teletherapy feature page)
- Available on desktop, iOS, and Android (teletherapy feature page)
- No separate login or third-party tool required

**Patient Portal**
- View and sign documents (patient portal page)
- Pay invoices online (patient portal page)
- Schedule appointments (patient portal page)
- Secure messaging with therapist (patient portal page)
- Complete assessments / MBC instruments (patient portal page, MBC page)
- Access teletherapy sessions (patient portal page)

**CarePaths Connect (Mobile App)**
- Patient-facing mobile app (iOS/Android) released ~2022 (press release)
- "Digital front door" for self-referrals and appointment booking (product page)
- Patients can search CarePaths network for nearby clinicians, verify insurance, and book appointments (web search results)
- Integrates secure messaging, teletherapy, scheduling, assessments, and payment
- Replaces the earlier "CarePaths Online Therapy" app (web search results)

**Reporting & Analytics**
- Reporting on clinical, financial, demographic, and quality data (practice management page)
- eCQM / MIPS / MACRA quality measure reporting (product page)
- Aggregate outcomes reporting for quality improvement

**Other**
- Fax capability for sending saved clinical documents from the EHR (practice management page)
- Data migration / integration tools for connecting with other EHRs (practice management page)
- Direct messaging (provided in-house, no additional fees) (mandatory disclosures page)
- Multi-factor authentication, encryption, audit controls, emergency access (mandatory disclosures page)

### Data & Content

Based on the features and functionality documented above, CarePaths EHR stores and manages:

**Clinical data** (directly evidenced):
- Patient demographics (certified for criterion (a)(5))
- Family health history (certified for (a)(12))
- Clinical documents: intake assessments, progress notes, treatment plans, case management assessments (clinical documentation page, vendor website)
- Custom clinical forms created via forms maker
- Diagnoses (reviews mention "add diagnosis")
- Treatment goals (reviews mention treatment plans)
- Medication data via DrFirst e-prescribing integration (mandatory disclosures page)
- Lab/imaging orders (certified for CPOE (a)(2)/(a)(3), though behavioral health context means these are likely less central)

**Outcomes / assessment data** (directly evidenced):
- Standardized assessment responses (PHQ-9, GAD-7, OQ-45, etc.) collected over time
- MBC tracking data: anxiety, depression, wellbeing, loneliness, medication adherence, therapeutic alliance metrics (mobile app page)
- Longitudinal outcomes graphs per patient

**Administrative / financial data** (directly evidenced):
- Appointment/scheduling data and calendar records
- Insurance information and eligibility verification results
- Claims data in X12 format
- Electronic remittance records
- Patient accounting: charges, payments, adjustments, invoices, statements
- Credit card payment records
- CPT codes associated with services

**Communication data** (directly evidenced):
- Secure messages between patient and therapist (patient portal, messaging features)
- Appointment reminder records (email/text)
- Faxed documents
- Direct messages (transitions of care)

**Teletherapy data** (partially evidenced):
- Session records exist (sessions launched from patient chart), but it is **unclear whether video session recordings are stored** — the vendor does not explicitly describe recording/storing teletherapy video. AI session summaries suggest at minimum some session content is processed.

**Patient portal / engagement data** (directly evidenced):
- Document viewing and signature records
- Online payment records
- Self-scheduled appointments
- Assessment completions via portal/app

**Audit / system data** (directly evidenced):
- Audit logs (certified for (d)(2))
- Authentication records (MFA support)
- Emergency access logs

**Gaps / uncertainties**:
- The vendor website does not mention lab results storage (as opposed to lab ordering), which is typical for behavioral health where lab work is less common
- No mention of imaging/radiology results storage
- No mention of allergy lists specifically, though this may be captured in intake forms
- No mention of immunization records
- No public health reporting data (not certified for (f) criteria)
- Whether teletherapy sessions are recorded and stored is unclear

---

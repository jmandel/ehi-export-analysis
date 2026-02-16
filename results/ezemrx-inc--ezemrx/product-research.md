# ezEMRx Inc — Product Research

Researched: 2026-02-15
Developer website: https://www.ezemrx.com

## Overview

ezEMRx Inc is a small EHR vendor founded in 2002, headquartered in Elgin, Illinois. The company has approximately 50–86 employees (sources vary) and estimated revenue of ~$22.8M. ezEMRx builds a certified electronic health record and practice management platform serving two primary markets: **public health departments** and **private ambulatory clinics**. The product tagline describes it as "EHR, PM, Inventory designed for all types of Clinics."

The company has a key strategic partnership with **Custom Data Processing, Inc. (CDP)**, an Illinois-based health IT company founded in 1979 that serves public health organizations. CDP is the exclusive reseller/provider of ezEMRx to public health clients and has been implemented in over 1,000 locations throughout the United States. CDP's broader portfolio includes environmental health inspection software (CDPims), WIC management information systems, and WIC EBT processing — ezEMRx is the EHR component of this public health technology ecosystem.

Siri Kumar serves as Chief Technology Officer / Chief Executive Officer at ezEMRx. The company appears to be privately held with no evidence of venture funding or acquisition activity.

## Product: ezEMRx

CHPL ID: 10779

### What It Is

ezEMRx is an ONC-ACB certified complete electronic health record (EHR) with integrated practice management, inventory management, patient portal, intake management, and revenue cycle management. It is a single unified product (not a modular platform with separately sold components), certified under CHPL product number 15.02.05.2886.EZEM.01.01.1.220105, version 10.01, certified 2022-01-05.

The product has a very broad certification profile — 40+ criteria spanning clinical data (a)(1)-(a)(5), (a)(12), (a)(14)-(a)(15); transitions of care (b)(1)-(b)(3); clinical information reconciliation (b)(7)-(b)(9); patient portal (e)(1), (e)(3); public health reporting (f)(1)-(f)(2), (f)(5); FHIR APIs (g)(7), (g)(9)-(g)(10); and direct messaging (h)(1). This indicates it is a full-featured ambulatory EHR, not a narrow specialty module.

The CHPL `sed_intended_user_description` says: "Healthcare providers in a clinic and specialty setting."

### Users & Market

**Primary market segments:**
1. **Public health departments** — local and state government health agencies, community health clinics serving vulnerable populations. This is the core market, served exclusively through the CDP partnership. CDP has deployed its solutions in 1,000+ locations across the US.
2. **Private ambulatory clinics** — physician practices across multiple specialties.

**Specialties supported** (from vendor marketing):
- Primary Care, Family Practice
- OB/GYN
- Neurology, Cardiology
- Urgent Care Centers
- Behavioral Health / Mental Health
- Substance Abuse treatment
- Immunization clinics
- Family Planning
- TB/STD/HIV clinics
- Case Management
- Home Health

**End users:** Physicians, nurses, clinical staff, billing staff, practice managers, and patients (via portal). The system is designed for both clinical documentation and administrative/financial workflows.

**Deployment:** Cloud-hosted, with data hosting described as being in "state-of-the-art data centers." Mobile access available via iOS native apps.

### Modules & Functionality

Based on vendor website, CDP partner site, and press releases, ezEMRx includes:

**Clinical/EHR:**
- Patient charting and clinical documentation
- Complete medical, social, behavioral, and substance abuse history
- Clinical decision support with drug interaction checking
- Treatment plan documentation
- E-prescribing (implied by certification criteria (a)(1) CPOE for medications)
- Immunization registry integration
- Chronic disease reporting
- Ready-to-use clinical workflow templates for multiple specialties (Immunization, Family Planning, Case Management, TB/STD/HIV, Home Health, Behavioral Health)
- Customizable templates, questionnaires, and task lists
- Remote patient care / telehealth mobility

**Practice Management & Scheduling:**
- Appointment scheduling and patient registration
- Patient household management (relevant for public health sliding fee schedules)
- Time tracking and staff management
- Real-time dashboards

**Billing & Revenue Cycle:**
- Integrated billing with claims scrubbing
- Electronic claims submission
- Real-time eligibility and benefits verification
- Sliding fee schedule support (critical for public health / FQHC-like settings)
- Floor pricing and discounts
- Auto-adjudication and automated payment posting
- Denial tracking with timely filing alerts
- Patient statement processing, mailing, viewing, and reporting
- Integrated merchant services (credit card and check processing)
- Optional Revenue Cycle Management (RCM) service — an outsourced service layer on top of the billing engine, including receivables management, coding audits, payment recovery, and write-off management
- BillFlash integration for patient billing: pre-visit billing via email/text, electronic bill notices, mailed statements, payment reminders, automated payments (StoredPay, AutoPay, PlanPay), and patient financing (FlexPay)

**Inventory Management:**
- Inventory tracking with bar code scanning
- Vaccine batch association with events (added for COVID-19 response)
- Distribution and inventory management for administered doses

**Patient Engagement:**
- Patient portal for viewing health information
- Appointment reminders via text and email
- Patient self-registration with QR code tracking (mass vaccination feature)

**Interoperability & Data Exchange:**
- Health Information Exchange (HIE) with a custom HIE portal
- HL7 messaging, CCD/CDA document exchange
- DIRECT messaging (criterion (h)(1))
- FHIR-compliant APIs with OAuth authentication (criteria (g)(7)-(g)(10))
- Code set support: ICD, CPT, LOINC, SNOMED CT, RxNorm

**Public Health Reporting:**
- Immunization registry submission (f)(1)
- Syndromic surveillance (f)(2)
- Cancer case reporting (f)(5)
- Performance measure reporting aligned with AMA, CMS, NCQA
- Meaningful Use, MIPS/MACRA, PQRI, and CQM compliance reporting

**Mass Vaccination / COVID-19 Features** (added December 2020):
- Community vaccination drive setup with demographic-based grouping
- Patient self-registration with unique QR codes
- Attendance and event flow monitoring
- Vaccine batch tracking and distribution management

**Security & Compliance:**
- SOC 1 Type 2 and SOC 2 Type 2 certified
- HIPAA-compliant
- Complete audit trails

**Support:**
- In-application live chat for providers to reach support staff

### Data & Content

Based on the features described above, ezEMRx stores and manages the following categories of data:

**Clinical data** — Patient medical records including medical history, social history, behavioral health and substance abuse records, immunization histories, treatment plans, clinical notes, drug interaction data, lab orders/results (implied by certification criteria), medication lists, problem lists, allergies, vital signs, and clinical decision support alerts.

**Administrative data** — Patient demographics, registration information, household/family relationships, appointment scheduling data, staff time tracking records, and audit logs.

**Billing and financial data** — Insurance eligibility records, claims data (electronic claims with scrubbing), payment posting records, denial tracking, sliding fee schedules, patient statements, merchant services transactions (credit card/check processing), and revenue cycle management records (coding audits, receivables, write-offs).

**Inventory data** — Medication and supply inventory with barcode tracking, vaccine batch records, distribution logs.

**Patient engagement data** — Patient portal access records, appointment reminder records (text/email), patient self-registration data, QR code tracking data.

**Interoperability data** — CCD/CDA documents exchanged, DIRECT messages sent/received, HIE exchange records, FHIR API access logs.

**Public health reporting data** — Immunization registry submissions, syndromic surveillance data, cancer case reports, quality measure data (MIPS/MACRA, CQM, PQRI).

**Notably absent or unclear:**
- The vendor website is built on Wix and renders client-side, making much of its content inaccessible via direct web fetch. The CDP partner site was far more informative.
- No third-party reviews were found on G2, Capterra, or similar sites — the product has very low visibility in the EHR review ecosystem, consistent with its niche focus on public health departments.
- No mention of document management/scanning, faxing, or letter generation — unclear if these are supported.
- No mention of lab interfaces specifically (though lab-related certification criteria are present).
- No mention of referral management as a named feature.
- The product serves both public health and private practice markets but marketing materials lean heavily toward public health. The private practice feature set may differ but this is not clearly documented.

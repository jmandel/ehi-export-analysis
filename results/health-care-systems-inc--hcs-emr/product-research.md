# Health Care Systems, Inc. — Product Research

Researched: 2026-02-14
Developer website: http://www.hcsinc.net

## Overview

Health Care Systems, Inc. (HCS) is a privately held behavioral health software company headquartered in Montgomery, Alabama. Founded in 1983 by a pharmacist and software engineer, HCS has over 40 years of experience delivering clinical software for healthcare facilities. The company specializes exclusively in **behavioral health** — serving psychiatric hospitals, residential treatment centers (RTCs), substance use disorder (SUD) programs, outpatient behavioral health organizations, and correctional healthcare facilities.

HCS positions itself as a unified platform covering clinical, financial, operational, and compliance workflows. The company claims its software is used by "thousands of clinicians and financial analysts" nationwide. Their partner/customer list is notable — it includes major behavioral health hospital chains such as **Universal Health Services (UHS)**, **Acadia Healthcare**, **HCA Healthcare**, **LifePoint Behavioral Health**, **Haven Behavioral Healthcare**, **Summit BHC**, **National HealthCare Corporation**, **US Healthvest**, and **Malvern Health**. These are some of the largest operators of psychiatric hospitals and behavioral health facilities in the U.S., suggesting HCS has significant market penetration in the inpatient behavioral health segment. Technology/data exchange partners include **Surescripts** (e-prescribing), **Merative** (formerly IBM Watson Health / Truven — likely for analytics or data exchange), and **Hawaii Health Information Exchange**.

The company is staffed in part by clinicians ("We're Clinicians Too") and emphasizes quick deployments ("in weeks instead of months"). HCS Cloud hosting is available. There is no indication of recent acquisitions or rebranding — the company appears to have operated under the same name since founding.

## Product: HCS eMR (and broader HCS Behavioral Health Software Suite)

CHPL ID: 11416

### What It Is

HCS eMR is a **comprehensive behavioral health electronic medical record system** designed for inpatient and residential behavioral health settings. The CHPL certification identifies the product as "HCS eMR" version 10 (certified December 2023), but in practice the certified module is part of a broader integrated suite that HCS markets as their "Behavioral Health Software" platform. The SED intended user description confirms this is for **"Physicians, Nurses, Pharmacists and other Clinical Disciplines in an Inpatient Setting"** with HIM (Health Information Management) users also included for the EHI export criterion (b)(11).

The certification is very broad — 40+ criteria spanning clinical data (a)(1)–(a)(15), transitions of care (b)(1)–(b)(2), clinical information exchange (b)(7)–(b)(9), patient portal (e)(1), public health reporting (f)(1)–(f)(7), FHIR API (g)(10), and immunization/syndromic/reportable conditions exchange. This indicates a full-featured clinical EHR with pharmacy, CPOE, patient portal, and public health reporting capabilities.

### Users & Market

**Primary users**: Psychiatrists, nurses, pharmacists, therapists/counselors, HIM staff, billing/financial analysts, compliance officers, call center/intake coordinators, and practice administrators at behavioral health facilities.

**Clinical settings**:
- Psychiatric hospitals (acute inpatient)
- Residential treatment centers (RTCs)
- Substance use disorder (SUD) treatment programs
- Partial hospitalization programs (PHP)
- Intensive outpatient programs (IOP)
- Outpatient behavioral health organizations
- Correctional healthcare facilities
- Crisis centers

**Notable customers/partners**: Summit BHC (39+ locations nationwide, including Northern Path Recovery Center in Fort Wayne, IN as a documented deployment), Algani Consulting (multi-state behavioral health organization implementing the full HCS suite across all facilities), and the major chains listed above (UHS, Acadia, HCA, LifePoint, Haven, NHC, US Healthvest, Malvern).

### Modules & Functionality

HCS markets seven primary product areas, all integrated within the single platform. Based on vendor materials, press releases, and product pages:

**1. Behavioral Record (Core Clinical EMR)**
- Patient intake and evaluation: collects personal details, medical history, assessments, symptoms, eligibility information
- Treatment planning: patient goals, objectives, interventions, expected outcomes; supports multiple diagnoses across behavioral and medical conditions
- Over 50 peer-reviewed behavioral health assessment tools including ASAM 4 (addiction severity), PHQ-9 (depression screening), and C-SSRS (suicide risk screening)
- Group therapy notes documentation
- Administrative and clinical bed board: real-time visibility into patient flow, bed availability, caseload, exam results, insurance status, risk management rules
- AIDA (Artificial Intelligence Dictation Assistant): ambient conversational listening with real-time speech-to-text, OpenAI-powered transcription, structured form fill, multi-language support
- Scheduling module for clinician, therapist, and patient appointments, therapy sessions, and activities
- Rules-based workflow engine monitoring time-restricted tasks with notifications
- Community Portal: patient-facing portal for scheduling, documentation completion, care record access, and provider communication (aligns with (e)(1) certification)

**2. Call Center CRM**
- Pre-admission screening and expedited onboarding
- Referral management with quality documentation
- Patient engagement and alumni tracking
- Treatment coordination and follow-up reminders
- Reporting and analytics

**3. Revenue Cycle Management (Billing/Financial)**
- Electronic eligibility/insurance verification
- Automated charge capture from intake through discharge
- Claim workflow management (every claim tracked to zero balance)
- Denial prevention with proactive alerts before claim submission
- Electronic Remittance Advice (ERA) processing
- Billing reports integrated with HCS Analytics
- Insurance verification, charge documentation, claim processing, payment tracking, denial management

**4. Order Management (CPOE)**
- Computerized provider order entry for medications, labs, radiology, and tasks
- Integration with automated dispensing devices, pharmacy, laboratory, and radiology systems

**5. Medication Management (eMAR, ePharmacy, MEDICS, MAT)**
- eMAR: Electronic Medication Administration Record with barcode scanning for unit dose labels; documented 33% reduction in medication errors and 45% reduction in documentation time
- Medication reconciliation with 12-month prescription history query (via Surescripts)
- Home-to-admission and discharge medication reconciliation
- ePrescribing for both controlled and non-controlled substances (EPCS)
- Medication Assisted Treatment (MAT) — specific module for SUD programs (e.g., buprenorphine, methadone protocols)
- HCS MEDICS: Pharmacy information system built on 30+ years of clinical experience, designed by pharmacists
- HCS ePharmacy: Medication order entry, verification, and clinical alerts documentation
- Clinical alerts, therapeutic substitution recommendations
- Visual alerts for medication due dates and overdue statuses
- Clinical status board for group medication monitoring

**6. Patient Safety**
- Safety Checks (patented, US Patent #US11869638): Electronic observation rounding tool replacing paper-based processes; captures patient location, clinical status, and clinician location at configurable intervals (every 5, 15, 30, or 60 minutes)
- Quality minute rounding with proximity beacons
- Clinical decision support with intelligently derived problem lists and template-driven treatment planning
- Patient education documentation tracking comprehension of medications and treatments
- Safe patient hand-off protocols

**7. Compliance Toolkit**
- Compliance Monitor tracking: unsigned orders/documents, time-based form compliance, Z code and ASAM analysis, readmission tracking, antibiotic stewardship, medication administration analysis, C-SSRS completion rates, discharge disposition, opioid administration oversight
- IPFQR (Inpatient Psychiatric Facility Quality Reporting) publication to CMS
- Credentialing Manager: primary source verification, license tracking, automated recertification reminders, provider/payor enrollment, network inclusion, privileging authorization
- Automated chart review
- Critical task notifications with intelligent escalation
- Metabolic screening measures
- Graphical reporting for HIPAA, billing/coding, regulatory, quality, security, and privacy

**Cross-cutting capabilities**:
- Multi-factor authentication (barcode badge, Active Directory, tokenized verification for EPCS)
- Real-time data analytics (HCS Analytics)
- Cloud hosting (HCS Cloud)
- Telehealth video conferencing for remote therapy sessions
- Public health reporting: immunizations, syndromic surveillance, electronic case reporting, cancer registry, antimicrobial use/resistance (certified for (f)(1)–(f)(7))
- FHIR API access (certified for (g)(10))
- Transitions of care / C-CDA exchange (certified for (b)(1), (b)(2))

### Data & Content

Based on the certified criteria and vendor materials, HCS eMR stores/manages the following data categories:

**Clinical data** (from (a) criteria and product descriptions):
- Patient demographics and registration information
- Problem lists (including intelligently derived)
- Medication lists and medication history (12-month Surescripts history)
- Medication administration records (MAR) with barcode verification
- Allergy and intolerance lists
- Clinical notes (progress notes, group therapy notes, discharge summaries)
- Vital signs
- Laboratory orders and results
- Radiology orders and results
- Behavioral health assessments (50+ standardized tools: ASAM, PHQ-9, C-SSRS, etc.)
- Treatment plans (goals, objectives, interventions, outcomes)
- CPOE orders (medications, labs, radiology, tasks)
- Prescription data (controlled and non-controlled, via Surescripts)
- Patient education records
- Implantable device data (certified for (a)(14))
- Social/psychological history

**Operational/administrative data**:
- Patient safety rounds/observations (location, status, clinician location, timestamps at 5–60 minute intervals)
- Bed board / census data (patient flow, bed availability, caseload)
- Scheduling data (appointments, therapy sessions, activities)
- Referral records
- Intake/pre-admission screening data
- Discharge disposition
- Credentialing data (provider licenses, certifications, privileges)

**Financial data** (from RCM module):
- Insurance eligibility and verification records
- Charge capture records
- Claims data (submission, tracking, zero-balance resolution)
- Denial management records
- Electronic remittance advice (ERA)
- Billing reports
- Patient payment records

**Patient engagement data**:
- Community Portal interactions (appointments, documentation, care records, messages)
- Call center CRM records (referrals, patient engagement, alumni tracking, follow-up reminders)
- Text appointment reminders

**Compliance data**:
- Compliance monitoring records (unsigned orders, form compliance, readmission tracking, etc.)
- IPFQR quality reporting data
- Chart review records
- HIPAA/security/privacy audit data

**Public health data** (from (f) criteria):
- Immunization records
- Syndromic surveillance data
- Electronic case reporting
- Cancer registry reporting
- Antimicrobial use and resistance data

**Exchange data**:
- C-CDA documents (transitions of care)
- FHIR resources (via g(10) API)
- Health information exchange data (Hawaii HIE partnership noted)

The EHI export, per the mandatory disclosures page, is delivered as "a compressed (ZIP) format containing CSV files with the actual EHI and a readme file" and can be done for single patients or patient populations "in real time" and "without HCS assistance and at no charge." An EHI Data Dictionary (CSV) is also available and updated with each new version.

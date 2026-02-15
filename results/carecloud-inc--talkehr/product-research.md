# CareCloud, Inc. — Product Research

Researched: 2026-02-15
Developer website: https://www.carecloud.com

## Overview

CareCloud, Inc. (NASDAQ: CCLD) is a publicly traded healthcare IT company headquartered in Somerset, New Jersey, with approximately 4,000 employees worldwide. The company originated as Medical Transcription Billing Corporation (MTBC), founded in 1999 by Mahmud Haq, initially focused on transcription and manual medical billing for New Jersey-based providers. In 2004, MTBC began developing proprietary practice management and EHR software. In 2017, MTBC launched talkEHR as its next-generation, voice-enabled EHR solution. The company changed its name from Medical Transcription Billing Corp. to MTBC, Inc. in 2019. In January 2020, MTBC acquired the separate company CareCloud Corporation (a Miami-based practice management and EHR vendor founded in 2009) for approximately $36 million, and in 2021 rebranded the entire company as CareCloud, Inc.

Today, CareCloud offers a broad portfolio of healthcare IT solutions: multiple EHR platforms (CareCloud Charts, talkEHR, and VertexDR), practice management, revenue cycle management (RCM), patient experience management (Breeze), telehealth, and newer AI-powered tools (cirrusAI for clinical documentation, stratusAI for front desk automation). The company states it serves "over 40,000+ providers" across practices of varying sizes and specialties. CareCloud operates three distinct EHR products under one corporate umbrella: CareCloud Charts (acquired via the CareCloud Corporation acquisition), talkEHR (MTBC's homegrown product), and VertexDR (designed specifically for anesthesiology).

## Product: talkEHR

CHPL IDs: 9799

### What It Is

talkEHR is a cloud-based electronic health records and practice management platform developed originally by MTBC (now CareCloud). Launched in 2017, it was one of the industry's first voice-enabled EHR solutions and is positioned as "an EHR simply built for your nimble practice." It is an integrated platform combining clinical EHR, practice management, medical billing, patient engagement, telehealth, and mobile health apps. The CHPL certification (dated December 2018) covers talkEHR as a Health IT Module, and based on the mandatory disclosures page, there is "no additional fee" associated with the certified module. The SED intended user description listed in the CHPL metadata is "Pediatric Nephrology," suggesting the usability testing was done with pediatric nephrology users, though the product itself is marketed broadly across specialties.

The certified criteria are extensive — 45+ criteria spanning clinical data (a)(1)-(a)(5), (a)(12), (a)(14)-(a)(15); transitions of care/care coordination (b)(1)-(b)(3), (b)(7)-(b)(9), (b)(10)-(b)(11); clinical quality measures (c)(1)-(c)(4); privacy/security (d)(1)-(d)(9), (d)(11)-(d)(13); patient portal/VDT (e)(1), (e)(3); public health reporting (f)(1)-(f)(2), (f)(4), (f)(6)-(f)(7); API/FHIR access (g)(2)-(g)(7), (g)(9)-(g)(10); and direct messaging (h)(1). This breadth indicates a full-featured ambulatory EHR with clinical documentation, e-prescribing, lab ordering, CPOE, CDS, patient portal, FHIR APIs, and public health reporting capabilities.

### Users & Market

talkEHR targets small to mid-sized independent medical practices and ambulatory clinics. The vendor describes serving practices across multiple specialties with "70+ customizable specialty-specific practice templates" including cardiology, dermatology, and pediatrics. According to a press release, within the first month of its 2017 rollout, MTBC signed new talkEHR customers in 42 states. The broader CareCloud entity claims 40,000+ providers, though it is unclear what share uses talkEHR specifically versus CareCloud Charts or VertexDR.

Pricing starts at $249 per provider per month for the EHR, with medical billing services available separately at 5% of claim reimbursements and PrecisionBI Lite (financial analytics) at $20/provider/month. The primary end users are physicians, nurse practitioners, and clinical staff in ambulatory settings. Practice managers and billing staff also interact with the practice management and billing modules. Patients interact through the talkPHR patient portal app.

### Modules & Functionality

Based on vendor materials, the talkEHR overview page, the detailed offerings page, and third-party reviews, the product includes the following modules and capabilities:

**Electronic Health Records (EHR)**
- Patient charting with 70+ customizable specialty-specific templates
- Clinical documentation with integrated voice dictation (talkDictate app)
- Medical history, medications, immunizations, diagnoses, treatment plans, radiology images, and test results management
- Automatic diagnosis predictions via AI-powered clinical reasoning engine
- Clinical decision support

**Computerized Provider Order Entry (CPOE)**
- Lab ordering with connectivity to major labs and imaging centers
- Lab results integration and viewing
- Medication ordering

**E-Prescribing**
- E-prescribing through Surescripts (v10.6), including controlled substances
- Refill request management
- Drug interaction alerts
- Dedicated talkRX mobile app for e-prescribing on the go

**Practice Management**
- Appointment scheduling with color-coded, filterable calendar (daily/weekly/monthly views)
- Staff scheduling and resource management
- Patient check-in via talkCheckin tablet app
- Reporting and business analytics

**Medical Billing & Revenue Cycle Management**
- Insurance claim submission (described as unlimited)
- Payment posting and denial management
- Claims processing and revenue cycle tools
- Billing services offered as both software and managed service

**Patient Engagement**
- Patient portal (talkPHR) providing round-the-clock access to health records, treatment plans, prescriptions
- Self-service appointment scheduling
- Secure messaging between patients and providers
- Lab results viewing for patients
- Claims and statements review
- Demographic information self-service updates
- Telehealth/video visits integrated with scheduling and charting

**Financial Analytics**
- PrecisionBI Lite dashboards, KPIs, data visualization
- Revenue cycle reporting
- Customizable reports exportable in PDF/XLS/CSV

**Mobile Health Apps**
- talkPHR (patient health records portal)
- talkCheckin (tablet patient intake/check-in)
- talkRX (e-prescribing)
- talkDictate (voice-to-text clinical documentation)
- Anesthesia App (iOS-only, for anesthesia workflows — surgery schedules, clearinghouse integration, document imaging, RCM)

**Telehealth**
- HIPAA-compliant video visits
- Integrated with EMR for charting during visits
- Automated appointment reminders

**Interoperability**
- Surescripts integration for e-prescribing
- EMR Direct for interoperability/Direct messaging
- FHIR APIs (certified for (g)(10) standardized API)
- Public health reporting capabilities (immunization registries, syndromic surveillance, cancer/electronic case reporting)

**Clinical Quality Measures**
- Support for 27 CMS quality measures
- MACRA/MIPS compliance support

### Data & Content

Based on the certified criteria and vendor-described features, talkEHR stores and manages the following categories of data:

**Clinical data** (per vendor feature pages and certification criteria): Patient demographics, medical history, medications/prescriptions, immunizations, allergies (implied by (a)(1) CPOE and CDS criteria), problem lists, diagnoses, treatment plans, clinical notes/encounter documentation, vital signs (implied by clinical charting), lab orders and results, radiology images and results, clinical quality measure data.

**E-prescribing data** (per Surescripts integration and talkRX app): Prescription records, refill requests, drug interaction alerts, pharmacy information, controlled substance prescriptions.

**Practice management data** (per scheduling and PM features): Appointment schedules, patient check-in records, staff schedules, practice configuration data, provider information.

**Billing/financial data** (per billing module descriptions): Insurance claims, payment records, denial management records, revenue cycle data, payer information, billing statements. The vendor explicitly describes "end-to-end Revenue Cycle Management" and "unlimited claim submissions."

**Patient engagement data** (per talkPHR and portal features): Patient portal accounts, secure messages between patients and providers, patient-entered demographic updates, telehealth visit records, appointment requests.

**Public health reporting data** (per certification criteria (f)(1)-(f)(7)): Immunization registry submissions, syndromic surveillance data, cancer case reporting, electronic case reporting.

**Document/imaging data**: The Anesthesia App references "document imaging" and the EHR stores "radiology images." Clinical document exchange is supported via C-CDA (certified for (b)(1)-(b)(3) transitions of care).

**Audit/security data** (per (d) criteria): Audit logs, authentication records, access controls.

**What's less clear**: The vendor website doesn't explicitly detail how referral management data, prior authorization data, or patient consent/advance directive data are handled, though some of these are implied by the certification criteria (e.g., (b)(7) data segmentation for privacy). The Medesk review notes CareCloud also offers Breeze for patient experience management, but it's unclear whether Breeze data integrates with or is separate from talkEHR specifically — Breeze appears to be associated with CareCloud Charts rather than talkEHR.

---

## Notes on CareCloud's Product Portfolio

CareCloud operates three distinct EHR platforms, each with separate ONC certifications:
1. **talkEHR** — the MTBC-originated product researched here, targeting independent ambulatory practices
2. **CareCloud Charts** — the EHR from the acquired CareCloud Corporation, with its own certification
3. **VertexDR** — a specialized anesthesiology EMR

These are separate products sharing the CareCloud corporate umbrella and some shared services (billing, analytics, Breeze patient engagement). The Capterra and Medesk reviews discuss them as distinct offerings. For the purpose of EHI export assessment, only talkEHR (CHPL ID 9799) is in scope.

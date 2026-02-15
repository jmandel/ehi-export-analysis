# Qualifacts Systems, LLC — Product Research

Researched: 2026-02-15
Developer website: https://www.qualifacts.com

## Overview

Qualifacts Systems, LLC is a Nashville-headquartered behavioral health technology company that describes itself as "one of the largest Behavioral Health and Rehabilitative EHR platforms in the U.S." with over 25 years of experience. The company operates three independent EHR platforms — **CareLogic** (enterprise/multi-site), **Credible** (large enterprise, #1 in KLAS for Behavioral Health), and **InSync** (small to mid-size practices). Qualifacts was acquired by Warburg Pincus in September 2019. Qualifacts and Credible Behavioral Health merged in August 2020. InSync Healthcare Solutions was acquired by the combined entity in December 2021, which then rebranded simply as "Qualifacts." The old InSync website (insynchcs.com) now redirects to qualifacts.com.

The combined company serves over 2,500 customers representing 75,000 providers and more than 10 million patients across all 50 states. The InSync acquisition reportedly doubled the organization's customer count. InSync was originally an independent company providing EHR and practice management software plus revenue cycle management services, targeting smaller behavioral health, medical, and rehabilitative practices — a market segment where approximately 40% of behavioral health providers work in organizations with fewer than 50 full-time employees.

## Product: Insync EMR/PM

CHPL ID: 10858

### What It Is

InSync EMR/PM is a cloud-based, fully integrated electronic health record and practice management platform. The product name ("EMR/PM") reflects that it combines clinical EHR functionality with practice management (scheduling, billing, revenue cycle) in a single system. It is hosted on Amazon Web Services (AWS) with redundant Level 1 data warehouse servers and claims 99% uptime. The platform uses Model-View-Controller (MVC) technology for cross-device browser-based access.

The certified module encompasses the full product — InSync EMR/PM is not a component of a larger suite but rather is itself the complete integrated platform. The CHPL certification covers version 10 and includes a broad set of criteria: clinical data (a)(1)-(a)(5), (a)(12), (a)(14)-(a)(15); transitions of care (b)(1)-(b)(3); patient portal (e)(1); public health reporting (f)(1)-(f)(2), (f)(7); and FHIR APIs (g)(10). The SED intended user description is "Medical/Clinical Providers."

### Users & Market

InSync targets **small to mid-size behavioral health, rehabilitative therapy, and medical practices**. Core user types include:

- **Behavioral health providers**: Mental health therapists, psychiatrists, substance use disorder (SUD) counselors, addiction treatment professionals
- **Rehabilitative therapy**: Physical therapists, occupational therapists, speech-language pathologists
- **Medical/primary care**: Family medicine, internal medicine, pediatrics, OB/GYN, orthopedics, occupational medicine, cardiology, dermatology, and other specialties
- **IDD providers**: Intellectual and developmental disability service organizations
- **Practice staff**: Billing staff, front desk/schedulers, practice managers, administrators

The platform serves solo practitioners, small group practices, and mid-size agencies. Qualifacts markets it to Certified Community Behavioral Health Clinics (CCBHCs) as well. A case study references a Michigan mental health practice (KindMind) that scaled using InSync's mental health EMR capabilities.

G2 rating: 4.2/5 based on 45 reviews. TechRadar gave it 2/5, though that review focused more on the vendor's website transparency than on product capabilities.

### Modules & Functionality

Based on vendor materials, product pages, and third-party review sites, InSync includes the following integrated modules and features:

**Clinical Documentation & Charting**
- AI-powered clinical documentation (Qualifacts iQ) that converts session transcripts into compliant clinical notes (DAP, BIRP, Progress Notes, Treatment Plans)
- Therapy progress notes with specialized templates for individual therapy, group therapy, and telehealth sessions
- Treatment planning with progress/outcomes tracking
- Clinical workflow customization with dynamic forms (drag-and-drop form builder)
- Customizable macros, frequently used notes, and personalized workflows
- Voice recognition support
- EM coding tools

**Assessment & Measurement-Based Care**
- Library of evidence-based assessments
- Pre-appointment assessments (completed via patient portal)
- ASAM criteria support (for addiction/SUD severity assessment)
- Measurement-based care tracking
- Mental health assessment tools

**ePrescribing & Medication Management**
- Integrated ePrescribing with EPCS (Electronic Prescribing of Controlled Substances)
- eMAR (electronic medication administration records)
- Drug-drug and drug-allergy interaction/contraindication checks
- PDMP (Prescription Drug Monitoring Program) integration
- Refill management
- Medication history viewing
- Pharmacy search and interface
- Eligibility checking for prescriptions

**Scheduling & Patient Intake**
- Multi-provider, multi-room scheduling view
- Appointment reminders via text, phone, and email
- Patient self-scheduling via portal
- Telehealth appointment scheduling
- API-based patient intake and website registration
- Digital intake forms with eSignature
- Check-in kiosk support (tablet-based)

**Patient/Client Portal**
- HIPAA-compliant secure messaging between patients and providers
- Appointment requests and scheduling
- Pre-visit assessment and intake form completion
- View treatment plans
- View and pay account balances (with real-time balance updates and receipts)
- Access to clinical and financial information
- Telehealth session access from portal
- Broadcast messaging for mass client communications
- Branded portal with organizational customization
- Mobile-friendly

**Billing & Revenue Cycle Management**
- Integrated billing engine with automated claims management
- Rules engine that auto-applies ICD codes to appointments and carries them through the billing workflow
- Claims queue management and submission
- Insurance/claims processing
- Revenue cycle management services (also offered as a separate managed service)
- Links between scheduling, clinical, and billing modules to reduce duplicate work

**Telehealth**
- Integrated video telehealth (no separate system login required)
- Group video sessions (up to 50 participants)
- Telepsychiatry support
- Documentation during live sessions
- ePrescribing from telehealth sessions

**Lab Integration & Referrals**
- Lab interfacing (listed as an add-on)
- Lab orders and results
- Referral management
- E-faxing (add-on)

**Reporting & Analytics**
- 100+ built-in reports covering patient appointments, financial summaries, utilization, lab results, productivity, referrals
- Healthcare analytics and reporting dashboards
- Customizable dashboards with role-based access
- Data-driven decision support

**Administrative & Other**
- Patient demographics management
- Medical history tracking
- Document management
- Task management
- OCR card scanning (add-on)
- eSignature pad support (add-on)
- Notifications and alerts for care teams
- Caseload management tools
- HL7 interoperability support
- ICD-10 coding support
- HIPAA compliance

### Data & Content

Based on the features described above, InSync stores and manages the following categories of data:

**Clinical data**: Patient demographics, medical/behavioral health history, clinical encounter notes (therapy notes, progress notes, treatment plans, group notes), assessments (including ASAM, evidence-based behavioral health instruments), vitals, diagnoses (ICD-10), problem lists, medication lists, allergy lists, immunization records (implied by public health reporting criteria (f)(1)-(f)(2)), lab orders and results, referral records.

**Medication data**: ePrescription records, medication administration records (eMAR), controlled substance prescriptions (EPCS), PDMP query data, drug interaction check logs, prescription history, refill records.

**Scheduling & appointment data**: Appointment schedules across providers and rooms, appointment reminders (text/phone/email), no-show tracking, telehealth session records.

**Billing & financial data**: Claims data, ICD codes linked to encounters, insurance information, payment records, account balances, receipts, revenue cycle data. The billing module's rules engine and automated code application mean the system stores detailed claim lifecycle data.

**Patient portal data**: Secure messages between patients and providers, patient-completed intake forms and assessments, eSignatures, payment transactions, portal activity logs, broadcast messages.

**Telehealth data**: Video session records/metadata, in-session documentation, group therapy session data.

**Documents & forms**: Custom dynamic forms, uploaded documents, scanned documents (OCR), e-faxes, eSignatures.

**Administrative data**: User/provider profiles, role-based access configurations, task assignments, notification/alert logs, audit trails (implied by certification criteria (d)(1)-(d)(9)), system configuration and workflow customization settings.

**Reporting data**: Built-in report outputs spanning clinical, financial, utilization, productivity, and referral analytics.

**Public health reporting data**: Immunization data for registries (f)(1), syndromic surveillance data (f)(2), and clinical data registry reporting (f)(7) — all required by certification.

The vendor website does not discuss imaging storage, radiology, or surgical documentation — consistent with InSync's focus on behavioral health, rehabilitative therapy, and ambulatory medical practices rather than hospital or surgical settings. Lab integration is described as an add-on rather than core, suggesting lab data breadth may vary by customer configuration.

---

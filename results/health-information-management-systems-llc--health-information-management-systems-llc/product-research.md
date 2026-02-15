# Health Information Management Systems, LLC — Product Research

Researched: 2026-02-14
Developer website: https://axiomehr.com/

## Overview

Health Information Management Systems, LLC (commonly known as **HiMS**) is a privately held health IT company headquartered in Tucson and Phoenix, Arizona. Founded in 2014 by CEO Khalid Al-Maskari — a former IT consultant for a behavioral health organization — HiMS builds cloud-based EHR software specifically for behavioral and integrated healthcare providers. The company's flagship product is **Axiom EHR** (also styled "AxiomEHR").

HiMS is a small, specialty-focused vendor. The company reported 100% customer retention in 2019 and operates on a subscription model with bi-monthly product updates included at no extra cost. Notable customers include COPE Community Services (a nonprofit behavioral and physical healthcare organization serving 15,000+ clients in Pima County, Arizona) and Service Access & Management (SAM), which implemented Axiom in 2022. The company has also been recognized with the 2024 Merit Award for Healthcare and a MedTech Breakthrough Award for EHR Innovation.

HiMS positions Axiom as an alternative to legacy EHR platforms, emphasizing customizability without coding, AI-driven automation, and rapid deployment. During COVID-19, HiMS deployed telehealth capabilities within 48 hours for customers, compared to competitors' reported 9+ month timelines.

## Product: Axiom

CHPL IDs: 10512

### What It Is

Axiom is a **cloud-based, integrated EHR platform purpose-built for behavioral health and integrated healthcare providers**. It is not a narrow clinical module — it encompasses clinical documentation, practice management, billing/RCM, e-prescribing, labs, scheduling, telehealth, patient portal, mobile apps, and AI-driven analytics in a single platform. The certified module (Axiom Version 7) appears to represent the full product rather than a subset.

The broader Axiom product ecosystem includes:
- **AxiomEHR** — the core EHR/practice management platform
- **AxiomMobile** — a HIPAA-compliant mobile clinician care app
- **Axiom Connect** — the patient portal (originally launched in 2017 as "MyHealtheHome Patient Portal"), used by patients to access health records, schedule appointments, and communicate with care teams
- **Axiom Services** — training and revenue cycle management services

### Users & Market

**Target users:** Psychiatrists, psychologists, clinicians, nurses, billing clerks, social workers, and practice managers at behavioral health organizations. The product is designed so each employee role can customize the interface for their responsibilities.

**Target settings:**
- Behavioral health clinics and organizations
- Addiction treatment centers
- Integrated health (behavioral + physical health) providers
- Developmental disability and foster care facilities
- Federally Qualified Health Centers (FQHCs)
- Mental health units
- Practices with 11+ physicians (per ehrinpractice.com listing)

**Notable customers:**
- **COPE Community Services** (Tucson, AZ) — nonprofit behavioral and physical healthcare serving 15,000+ clients. Used Axiom's cloud-based architecture to rapidly update telehealth and billing during COVID-19.
- **ChangePoint Integrated Health** — cited in HiMS press release as praising the product.
- **Service Access & Management (SAM)** — implemented Axiom in 2022 with role-based customization.

**Market position:** HiMS is a small, niche vendor focused exclusively on behavioral/integrated health. It competes against larger behavioral health EHR vendors (e.g., Netsmart, Qualifacts/Credible, Exym) but differentiates on AI features and ease of customization. Customer count is not publicly disclosed but appears to be modest.

### Modules & Functionality

Based on vendor materials, press releases, third-party listings, and case studies, Axiom includes the following modules and capabilities:

**Clinical Documentation:**
- AI-powered note-taking and dictation — transcribes office visit conversations using NLP
- AI note comprehensive summary generation
- Auto-population of clinical data fields from conversations (diagnoses, treatment options, social determinants of health)
- Patient sentiment measurement during visits
- Clinical decision support tools
- Customizable clinical templates (PCP/nursing templates)
- Drag-and-drop form and report builder (custom forms without coding)
- e-Signatures

**Practice Management & Scheduling:**
- Appointment scheduling with drag-and-drop tools, synchronized across teams and locations
- Automated appointment creation from clinical encounters
- Text/voice appointment reminders

**Billing & Revenue Cycle Management (RCM):**
- Full built-in RCM
- Claims submission and processing
- Eligibility verification
- Payment posting
- HCPCS and CPT code management
- ICD-10 coding support
- AI-driven coding recommendations (reported 23% more accurate and 33% more comprehensive than market leader in pilot testing)
- Contract management
- Claims appeal management
- Financial analysis and reporting
- Support for all insurance providers

**Prescribing & Labs:**
- Full e-prescribing (RX) capabilities
- Lab integration and lab results management

**Telehealth:**
- Built-in HIPAA-compliant telehealth (virtual sessions integrated into the EHR dashboard)
- Zoom integration capability (as deployed at COPE)

**Patient & Employee Portals:**
- **Axiom Connect** patient portal — health record access, appointment scheduling, secure messaging with care team
- Employee portal

**Mobile:**
- **AxiomMobile** — clinician mobile app for iOS and Android

**Reporting & Analytics:**
- AI-powered report builder
- AI "Ask Axiom" — ChatGPT-style chatbot for querying organizational data (diagnosis prevalence, progress-note completion rates, comparative claim volumes, patient cancellation likelihood)
- Predictive analytics (forecasting patient outcomes, identifying at-risk individuals)
- Monthly stats monitoring
- Practice performance KPIs

**Specialty Features:**
- Electronic Visit Verification (EVV) — critical for Medicaid-funded home and community-based services
- Developmental disability (DD) and foster care support modules
- Inpatient services support

**Integrations & Interoperability:**
- API access and HIE integrations
- Data warehouse capabilities
- FHIR API (certified for g(7)-g(10))
- HL7 support
- CRM capabilities — tracks client engagement from inquiry through admission

### Data & Content

Based on the features and modules described above, Axiom stores and manages the following categories of data:

**Clinical data** (strongly supported by (a)(1)-(a)(5), (a)(12), (a)(14) certifications and vendor materials):
- Patient demographics and history
- Clinical encounter notes (including AI-transcribed and summarized notes)
- Diagnoses and problem lists
- Medications and e-prescriptions
- Lab orders and results
- Allergies
- Immunizations (implied by clinical criteria)
- Treatment plans / service plans
- Clinical decision support alerts
- Social determinants of health data
- Patient sentiment data from visits

**Administrative & scheduling data:**
- Appointment schedules across teams/locations
- Appointment reminders (text/voice)
- Employee information

**Billing & financial data:**
- Insurance eligibility and payer information
- Claims (HCPCS, CPT, ICD-10 codes)
- Payment postings
- Contract terms
- Revenue cycle metrics
- Financial analysis data

**Patient portal data:**
- Patient-accessible health records
- Secure messages between patients and care teams
- Patient-initiated appointment requests

**Behavioral health-specific data:**
- EVV (Electronic Visit Verification) records
- DD (developmental disability) service records
- Foster care records
- CRM/intake tracking (inquiry through admission)

**Reporting & analytics data:**
- Custom forms and reports
- Organizational analytics (diagnosis prevalence, note completion rates, claim volumes)
- Predictive analytics outputs
- Practice performance KPIs

**Notably, the vendor website does not mention:** Imaging/radiology (this is primarily behavioral health, so this absence is expected), surgical/operative notes, or pharmacy dispensing. The product is behavioral health-focused, so the absence of hospital-centric features is consistent with its market positioning.

---

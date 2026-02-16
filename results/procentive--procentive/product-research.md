# Procentive (Ensora Health) — Product Research

Researched: 2026-02-15
Developer website: https://ensorahealth.com/product/procentive/

## Overview

Procentive is a cloud-based EHR and practice management platform built specifically for behavioral health, mental health, and substance use recovery providers. It is now owned by Ensora Health, the rebranded identity of Therapy Brands, a Birmingham, Alabama–based company founded in 2013 by Shegun Otulana. Therapy Brands grew through acquisition, assembling a portfolio of therapy-focused software products including TheraNest, Fusion, WebABA, MyClientsPlus, Catalyst, AccuPoint, TenEleven, and Procentive. In May 2021, KKR acquired a majority stake in Therapy Brands for $1.2 billion. The company subsequently rebranded to Ensora Health.

Procentive appears to have been an independent product (likely Minnesota-based, given the NUWAY Alliance case study and early customer base) that was acquired by Therapy Brands at an unspecified date. The therapybrands.com domain now redirects to ensorahealth.com, and Procentive is marketed as one of Ensora Health's core platforms. Ensora Health reports serving over 28,000–30,000 therapy practices with 200,000+ providers across its entire product portfolio.

Within the Ensora Health portfolio, Procentive serves the "mental health with substance use recovery" market segment, distinguishing it from TheraNest (smaller mental health practices) and Fusion (physical/occupational/speech therapy). Procentive targets mid-size to larger behavioral health organizations, including residential/inpatient facilities, outpatient clinics, and substance abuse treatment centers.

## Product: Procentive

CHPL ID: 11155

### What It Is

Procentive is described as a "full-featured, simple EHR solution for behavioral health practices" and a "complete behavioral health EHR, including clients, documentation, reporting and billing." It is a single integrated platform — the certified module appears to encompass the full product. It is cloud-based (SaaS). The SED intended user description is "Mental and Behavioral Healthcare."

The product is certified for a broad set of ONC criteria (25+), including clinical data capture (a)(2), (a)(3), (a)(5), clinical decision support (a)(12), (a)(14), (a)(15), transitions of care (b)(1), (b)(2), patient portal (e)(1), public health reporting (f)(1), (f)(2), clinical quality measures (c)(1)–(c)(3), and FHIR APIs (g)(10). This is a comprehensive clinical certification, not a narrow billing-only product.

### Users & Market

**Target users:** Behavioral health clinicians (therapists, counselors, psychiatrists), substance use recovery treatment staff, clinical and nursing staff at residential facilities, billing departments, practice administrators, and front-office staff. The NUWAY case study mentions that even staff "with minimal technology experience" can use the clinical charting.

**Settings served:**
- Outpatient mental health clinics
- Substance use/addiction treatment centers (residential and outpatient)
- Chemical health providers
- ABA (Applied Behavioral Analysis) practices (per one source)
- Medium-intensity residential treatment facilities (per NUWAY case study)
- Nonprofit behavioral health organizations

**Notable deployment:** NUWAY Alliance, a nonprofit substance use recovery organization in Minneapolis founded in 1996 with multiple facilities, uses Procentive for the full spectrum from intake through discharge, including bed management, billing, e-prescribing with EPCS, and state reporting. They generate approximately 3,400 reports daily.

**Market position:** Mid-tier behavioral health EHR. Procentive competes with products like Behave Health, Qualifacts (Credible), and Valant in the behavioral health EHR space. As part of Ensora Health / KKR's $1.2B investment, it has corporate backing but serves a niche market.

### Modules & Functionality

Based on vendor materials, the Ensora Health knowledge base, case studies, reviews, and third-party comparisons, Procentive includes the following modules and features:

**Scheduling & Appointments**
- Daily, weekly, monthly appointment views
- Customizable appointment durations
- Automated appointment reminders
- Video session / virtual waiting room support (telehealth)

**Client/Patient Management**
- Complete demographics and medical history
- Insurance details and eligibility verification
- Client authorization management
- Intake and discharge workflows

**Clinical Documentation**
- Customizable clinical notes and templates (individual and group)
- Initial assessments, treatment plans, progress notes, discharge summaries
- Practice Planners for evidence-based treatment plan creation (vendor claims under 20 minutes)
- DSM-5–ready documentation
- CCDA section mapping for CURES compliance
- Clinical document uploads
- Flags for missing CPT codes on appointments/documents

**E-Prescribing**
- Electronic prescriptions with digital signatures
- EPCS (Electronic Prescribing for Controlled Substances)
- Integration with DrFirst for e-prescribing

**Bed Management**
- Launched in 2022 as a dedicated module
- Track client stays, bed status, attendance
- Status tags for special needs or medications
- Capacity visibility by room, building, or unit
- Waitlist creation based on patient needs
- Syncs with scheduling and billing

**Billing & Revenue Cycle Management**
- Automatic claim compilation from clinical documentation
- Claim scrubbing and submission
- Charge submission and payment tracking
- Denials and appeals management
- Integrated RCM services (outsourced billing option)
- Clearinghouse services
- Support for Medicare/Medicaid billing

**Client Portal**
- Client self-service scheduling
- Secure messaging with staff
- Access to treatment information
- Bill pay
- Custom branding (agency logo)
- Integrated telehealth via portal

**Payments**
- Payment processing features (separate from insurance billing)

**Communication**
- Fax
- Messaging (internal messaging between staff reportedly limited per one review)
- Ticket/chat system for support cases

**Reporting & Analytics**
- Over 120 pre-built report templates
- Clinical process, financial, resource utilization, and outcome reports
- Census tracking (e.g., NUWAY's 3,400 daily reports)
- Customizable reports
- Service time tracking

**Staff Management**
- User/staff administration
- Permission management
- Workflow engine with task automation, customizable alerts, event-triggered notifications

**Interoperability**
- FHIR R4 server (Dynamic FHIR Server 4.0.1 / ConnectEHR v4 + BulkFHIR4) at fhir.procentive.com
- CCDA generation for transitions of care
- Integration with DrFirst (e-prescribing)
- Integration with Inpriva (secure health information exchange)
- Integration with Dynamic Health IT
- Integration with Sisense (analytics)
- Integration with thera-LINK (telehealth, though likely legacy given built-in telehealth)

**Public Health Reporting**
- Immunization registry (f)(1)
- Syndromic surveillance (f)(2)
- State compliance reporting (per NUWAY case study)

### Data & Content

Based on the features described above, Procentive stores and manages the following data categories:

- **Patient demographics:** Names, contact info, identifiers, insurance information
- **Clinical records:** Assessments, treatment plans, progress notes, discharge summaries, group notes
- **Medication data:** Prescriptions (including controlled substances via EPCS), medication lists, allergies
- **Scheduling data:** Appointments, attendance, automated reminders
- **Billing/claims data:** Insurance claims, charges, payments, denials, appeals, EOBs
- **Bed management data:** Bed assignments, stays, capacity, waitlists, attendance tracking
- **Clinical documents:** Uploaded documents, CCDAs
- **Portal data:** Secure messages between clients and staff, appointment requests, bill payments
- **Reporting data:** Census data, clinical outcomes, financial metrics, utilization data
- **Staff/admin data:** User accounts, permissions, audit trails
- **Communication records:** Faxes, internal messages, support tickets
- **Compliance data:** CPT code validation, authorization tracking, state reporting submissions

The vendor's website doesn't explicitly mention lab results or imaging as stored data types — this is consistent with behavioral health settings where those are less central. The product clearly emphasizes behavioral health–specific workflows: treatment planning with DSM-5 codes, group therapy notes, bed management for residential facilities, and substance use recovery workflows.

One notable gap: the Behave Health comparison article noted that secure messaging between staff members "appears to not be possible" in Procentive, suggesting internal staff communication data may be limited compared to client-facing messaging.

---

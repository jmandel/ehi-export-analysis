# Office Practicum — Product Research

Researched: 2026-02-15
Developer website: https://www.officepracticum.com/

## Overview

Office Practicum (OP) is a pediatric-specialty EHR, practice management, and revenue cycle management platform developed by Connexin Software, Inc., based in Fort Washington, Pennsylvania. The product was originally created in 1992 by Visual Data, LLC, a collaboration between programmers and pediatricians. In 2007, Visual Data merged with Anderson Financial Systems (AFS) to form Connexin Software, the current corporate home of Office Practicum. The company has been building pediatric-focused technology for over 35 years and describes itself as the only EHR "built by pediatricians for pediatricians."

Office Practicum serves over 9,000 pediatricians across 48–49 states. Its SED intended user description lists "Pediatricians, Physicians, and Practice Managers." According to KLAS Research, 97% of practices that start with OP stay with OP. The company made two significant acquisitions in 2022: **NextStep Solutions** (a behavioral health EHR) and **RemedyConnect** (a pediatric digital healthcare delivery company offering telehealth, after-hours answering service, website development, and marketing services). These acquisitions formed what OP calls the market's first "Whole Child" digital healthcare platform. In 2014, OP also acquired the assets of Workflow.com, a web-based multi-specialty EHR and practice management system.

## Product: Office Practicum

CHPL IDs: 11049

### What It Is

Office Practicum is an end-to-end, cloud-based EHR and practice management platform dedicated to pediatric clinics. It is a complete EHR — not a module or component of a larger system — that combines electronic health records, practice management, revenue cycle management, patient engagement, and (through acquisitions) behavioral health and telehealth services into a single integrated platform. It is Drummond-certified and marketed as a dual-certified EHR (both ambulatory and the Cures Act criteria). The certified product version is 21.

The platform runs as both a desktop and browser-based application compatible with Windows and Mac. It is cloud-hosted.

### Users & Market

**Primary users**: Pediatricians, nurses, clinical staff, administrative/front desk staff, billing staff, and practice managers. The platform is designed specifically for pediatric practices, though it has some family medicine usage.

**Customer base**: Over 9,000 pediatricians across 48–49 states. As of 2014 (post-Workflow.com acquisition), the company reported serving more than 3,000 providers and 750 practices. These numbers have grown since.

**Clinical settings**: Primarily ambulatory pediatric practices — from small/solo pediatric offices to multi-provider pediatric groups. The product is not targeted at hospitals, long-term care, or academic medical centers.

**Market position**: OP is a mid-size, niche-focused vendor — the dominant player in the pediatric EHR space. It has been ranked #1 in the Pediatric Software category on SelectHub. KLAS Research has profiled it specifically in the pediatric EHR/PM category.

### Modules & Functionality

Based on vendor website, third-party reviews, and press releases, Office Practicum includes the following modules and features:

**Clinical / EHR**
- SOAP note-based clinical documentation with pediatric-specific templates
- Growth charts, including specialty curves (Down Syndrome, preemie)
- VacLogic immunization forecasting engine — automatic vaccine tracking, reminders, and interaction with state immunization registries
- Over 175 pre-designed school and camp form templates
- Pediatric developmental assessments and disease-specific action plans
- Hundreds of "sick visit" templates
- Preventive exam templates aligned with AAP Periodicity Schedule
- Integrated AAP resources
- Clinical decision support tools
- Behavioral health monitoring tools — Mental Health Monitor with dashboards for PHQ-9, GAD-7, and other behavioral health surveys, tracking scores over time (sources: vendor website, search results)
- Allergy and immunization tracking
- Medication management

**e-Prescribing**
- Electronic prescribing with EPCS (Electronic Prescribing of Controlled Substances) support
- DEA-compliant workflows for controlled substances
- Surescripts integration (received Surescripts White Coat of Quality Award in 2011 and 2013)

**Lab Integration**
- OP eLabs — connections to hundreds of labs for electronic order sending and result receiving
- In-house lab device connectivity with discrete data flowing into patient charts
- Lab results viewable in patient chart and through patient portal

**Practice Management / Scheduling**
- Appointment scheduling with built-in well-visit recalls based on AAP Periodicity Schedule
- Patient flow tracking by calendar or room, tracking location and time at each visit stage
- One-touch family demographics update
- Provider productivity tracking
- Real-time insurance eligibility validation
- Automated well-visit recall management

**Billing & Revenue Cycle Management**
- Electronic superbill charges automatically generated in real-time during provider documentation
- Claims processing and electronic claim submissions
- Automated charge adjustments
- Payment posting
- Denial tracking
- Clearinghouse integration (in-house billing and clearinghouse services)
- Revenue analysis and reporting
- Detailed charge summaries for visits, immunizations, and ancillary services
- OP also offers outsourced RCM services

**Patient Portal & Engagement**
- Patient portal (relaunched in September 2024, powered by BridgeInteract)
- Self-registration and live scheduling (including flu clinic self-scheduling)
- Secure messaging with providers, with message routing to designated staff
- Bilingual support (English/Spanish)
- Online access to medical records and lab results
- Prescription refill requests
- Appointment reminders

**Telehealth**
- Remedy Telehealth — HIPAA-compliant virtual care platform with video conferencing and speech dictation (via RemedyConnect acquisition)
- Integrated telemedicine for remote pediatric check-ups, diagnoses, and treatment

**Document Management & Fax**
- Document scanning — insurance forms and other documents scanned directly into patient charts
- Bi-directional eFax — HIPAA-compliant inbound and outbound fax management within OP
- Digitized referral workflows, new patient intakes, and record releases

**Interoperability & Data Exchange**
- Integration with labs, pharmacies, immunization registries, and diagnostic devices
- ClearTriage integration (telephone triage protocols)
- Transitions of care / C-CDA support (certified for (b)(1)–(b)(3))
- FHIR API access (certified for (g)(10))
- Public health reporting (certified for (f)(1) — immunization registry reporting)
- GoCheck Kids partnership (pediatric vision screening)

**Reporting & Analytics**
- Practice analytics and pediatric benchmarking
- Comprehensive patient and practice-level reporting
- Provider productivity reports

**Additional Services (via acquisitions)**
- NextStep Solutions behavioral health EHR (for child and adult behavioral health specialists)
- RemedyConnect portfolio: website design, SEO, online reputation management, 24/7 after-hours answering service

### Data & Content

Based on the features described above, Office Practicum stores and manages the following categories of data:

- **Patient demographics** — including family demographics with one-touch update across related patients (pediatric-specific: parents/guardians linked to child patients)
- **Clinical documentation** — SOAP notes, visit notes, sick visit documentation, preventive exam records
- **Growth and development data** — growth chart measurements, developmental assessment scores, developmental milestones
- **Immunization records** — vaccine administration history, VacLogic forecasting data, state registry submissions
- **Behavioral health data** — PHQ-9, GAD-7, and other behavioral health screening scores with longitudinal tracking
- **Medication and prescription data** — active medications, prescription history, EPCS records for controlled substances
- **Allergy data** — allergy and intolerance records
- **Lab orders and results** — electronic lab orders and discrete lab result data (both reference lab and in-house device results)
- **Billing and claims data** — superbill charges, claims, payment records, denial tracking, insurance eligibility data, charge summaries
- **Scheduling data** — appointments, well-visit recall schedules, patient flow/room tracking data
- **Scanned documents** — insurance forms, faxes, other documents scanned into patient charts
- **Referral data** — specialty physician referral workflows
- **Patient portal data** — secure messages between patients/families and providers, self-registration data, portal activity
- **Telehealth encounter data** — virtual visit records (via Remedy Telehealth)
- **School and camp forms** — completed forms from 175+ templates
- **Insurance and eligibility data** — real-time eligibility verification data, insurance card scans
- **Reporting/analytics data** — practice benchmarking, provider productivity metrics

**Notable**: The vendor website does not provide detailed technical documentation about the internal data model. The data categories above are inferred from described features and workflows. It is unclear how much of the RemedyConnect (telehealth, answering service) and NextStep Solutions (behavioral health EHR) data is stored within the core OP system vs. in separate systems — the "Whole Child" platform may involve multiple underlying databases. The EHI export documentation will need to clarify what scope of data is included.

---

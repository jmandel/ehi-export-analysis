# Advanced Data Systems Corporation — Product Research

Researched: 2026-02-15
Developer website: https://www.adsc.com

## Overview

Advanced Data Systems Corporation (ADS/ADSC) is a privately-owned healthcare IT company founded in 1977 by David Barzillai, who originally built patient demographics software for radiology practices in New York City. The company has never changed its name, never been acquired, and describes itself as "debt-free and self-contained." It is headquartered in Paramus, New Jersey, with approximately 200–300 employees (sources vary). ADS handles all development, implementation, training, and support internally.

ADS serves ambulatory medical practices across a wide range of specialties — the vendor lists 27+ specialties including internal medicine, podiatry, ophthalmology, orthopedics, cardiology, OB-GYN, neurology, behavioral health, pain management, dermatology, ENT, urgent care, and more. They also serve imaging centers (via their MedicsRIS product), laboratories, medical billing companies, and rural hospitals. The company claims 45+ years of continuous operation and processes millions of EDI transactions annually with a 95%+ clean claims rate on first submission.

ADS positions itself as a mid-market vendor for small-to-enterprise practices. They appear in Medical Economics' Top 50 EHRs and have Gartner reviews but do not appear to have a significant KLAS presence. They sell direct and also offer outsourced RCM services through their ADS RCM division.

## Product: MedicsCloud

CHPL IDs: 10786

### What It Is

MedicsCloud is ADS's current-generation cloud-based platform that encompasses both EHR and practice management capabilities. The certified product is "MedicsCloud" version 11.0, certified January 2022. It holds a broad set of ONC certifications across clinical data (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15), transitions of care (b)(1)–(b)(3), patient portal (e)(1), clinical quality measures (c)(1)–(c)(3), public health reporting (f)(1)–(f)(5), and FHIR APIs (g)(7)–(g)(10). The SED testing description identifies the intended users as "Internal Medicine and Other Specialties Providers and office staff."

MedicsCloud can be deployed as an all-in-one EHR + PM suite, or the EHR and PM components (MedicsCloud EHR and MedicsPremier) can be used independently or with third-party systems. The "Medics Suite" is the integrated product combining both. The certified module is part of this broader product ecosystem.

### Users & Market

Day-to-day users include physicians, clinical staff, billing staff, and practice managers across ambulatory settings. The product targets small practices through multi-site enterprise groups. ADS lists 27+ supported medical specialties. The vendor's About Us page emphasizes long-term client relationships and describes the company as "highly accessible" to customers.

No specific customer count is publicly disclosed, though ADS's history page mentions growing from 500 clients in the 1980s to over 1,000 clients subsequently. The current customer count is not stated. A Capterra review noted that the product is "the best and highest quality product for your money" but also flagged that there can be a "disjointed onboarding process" due to separation between billing and EHR implementation staff. TechRadar rated MedicsCloud EHR 3/5 stars, praising its patient portal and support options but criticizing opaque pricing and mobile app limitations.

### Modules & Functionality

Based on vendor website materials and feature pages, MedicsCloud includes the following modules and capabilities:

**Clinical Documentation & EHR:**
- User-definable templates for specialty-specific clinical workflows
- AI-driven charting via "MedicsScribe" — real-time dictation, transcription, and automated summaries
- Voice navigation ("Medics FlowText") for hands-free encounter documentation
- Clinical decision support (ezCDS integration)
- Problem lists, medication lists, allergy documentation (per certification criteria)
- CPOE (computerized provider order entry)

**E-Prescribing:**
- Electronic prescribing for controlled and non-controlled substances
- Surescripts-certified for e-prescribing

**Lab & Orders:**
- Lab order transmission to external labs with results flowing back into the EHR
- Embeddable lab icons for in-workflow ordering

**Practice Management (MedicsPremier):**
- Scheduling (including multi-modality scheduling)
- Billing and claims management
- Claim tracking and claim denial management
- Insurance verification and insurance discovery
- Patient due estimator
- Out-of-network payment handling
- After-insurance balance management
- Revenue cycle management
- Dynamic reporting and healthcare analytics
- Support for multiple tax IDs
- Inventory management for purchasable products

**Patient Engagement:**
- Patient portal (24/7 self-service for appointment requests, questionnaires, payments)
- "Medics Me" FHIR/SMART patient-facing app (iOS/Android)
- MedicsKiosk — digital self-service check-in on patients' own devices, with e-signatures and ID scanning
- Interactive texting — appointment reminders with one-tap confirmation, balance-due notifications
- Telemedicine — virtual visits with picture-in-picture, no app download required
- Remote Patient Monitoring (RPM) — blood pressure, glucose, oxygen saturation tracking

**Interoperability & Data Exchange:**
- HL7 and FHIR compatible
- Surescripts Direct Messaging (N2N) for care transitions
- FHIR/SMART API access
- 21st Century Cures Act compliance

**Reporting & Quality:**
- MIPS reporting dashboards
- Clinical Quality Measures (certified for 25 CQMs including depression screening, diabetes management, cancer screening, immunization tracking)
- Public health reporting (immunization registries, syndromic surveillance, electronic case reporting, cancer registry)

**Additional Features:**
- Healthcare CRM software
- Attorney management (legal case management — likely for personal injury/workers' comp workflows)
- Bed management (suggests some inpatient or observation use)
- MedicsMobile app for clinician access to patient data
- Fax automation with AI-driven sorting

**Radiology Information System (MedicsRIS):**
ADS also offers MedicsRIS as a separate product for imaging centers, handling scheduling, orders, reporting, billing, clinical decision support, and prior authorization. This is a distinct product but shares the ADS ecosystem.

### Data & Content

Based on the features described above, MedicsCloud stores and manages:

- **Clinical records**: encounter notes, clinical documentation (voice-transcribed and templated), problem lists, medication lists, allergy lists, vital signs, clinical assessments
- **Orders and results**: lab orders, lab results, imaging orders/results (at minimum via integration)
- **Prescriptions**: medication prescriptions including controlled substances, prescription history, Surescripts transaction data
- **Demographics and registration**: patient demographics, insurance information, ID scans
- **Scheduling data**: appointments, multi-modality scheduling, appointment reminders
- **Billing and claims**: claims data, claim status/tracking, denial records, insurance verification results, patient balances, payment history, EDI transactions
- **Patient portal data**: patient-entered questionnaires, appointment requests, portal messages, payment transactions
- **Telemedicine**: virtual visit sessions
- **Remote monitoring data**: blood pressure, glucose, oxygen saturation readings from RPM devices
- **Communication records**: secure messages, text message interactions, fax documents (with AI categorization)
- **Quality measures**: CQM data, MIPS reporting data
- **Public health reports**: immunization registry submissions, syndromic surveillance data, electronic case reports, cancer registry data
- **Documents**: clinical documents, consult letters (AI-generated), CDA/CCDA documents for transitions of care
- **Inventory**: purchasable product inventory data
- **CRM data**: healthcare CRM records
- **Attorney/legal case management**: case data for personal injury or similar workflows

The mandatory disclosures page confirms costs include "MedicsCloud software itself, user licenses, monthly subscriptions" plus implementation and service fees, and lists integration with "Surescripts for eRx, Surescripts N2N Direct Messaging, Meinberg NTP Daemon for NTP" as additional software components.

One notable gap: the vendor website does not prominently describe document management or scanning capabilities beyond the AI-driven fax automation feature. It's unclear how much unstructured document storage (scanned records, imported PDFs) the system handles, though fax automation implies at least incoming document management.

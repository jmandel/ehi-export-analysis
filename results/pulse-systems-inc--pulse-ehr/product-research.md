# Pulse Systems, Inc — Product Research

Researched: 2026-02-14
Developer website: https://pulseinc.com

## Overview

Pulse Systems, Inc. is a Kansas City-based provider of integrated EHR, practice management, and revenue cycle management solutions for ambulatory healthcare practices. Founded in 1997, the company was previously owned by Cegedim (a global healthcare technology company) before being acquired by N. Harris Computer Corporation in September 2019. Pulse now operates within the **Harris Ambulatory Care Enterprise** family alongside several other ambulatory EHR products including Amazing Charts, PrognoCIS, CareTracker, GEMMS, digiChart, and Picasso EHR. The developer contact email (@harriscomputer.com) confirms this corporate relationship.

Pulse claims to have "worked with thousands of providers" across a variety of specialties. The product targets ambulatory practices of all sizes, including solo practices, multi-site groups, ambulatory surgical centers, integrated delivery networks (IDNs), and management services organizations (MSOs). The vendor emphasizes customizable workflows tailored to individual practice needs. Pulse is a Surescripts Gold Solution Provider (awarded five consecutive years per their press materials), indicating strong e-prescribing integration.

## Product: Pulse EHR

CHPL ID: 11500

### What It Is

Pulse EHR is an integrated electronic health records and practice management platform marketed as "Pulse EHR/PM." The certified product (version 8.02, certified 2024-08-06) carries a broad set of ONC certifications spanning clinical data management (a)(1)–(a)(5), (a)(12), (a)(14), transitions of care (b)(1)–(b)(3), clinical quality measures (c)(1), public health reporting (f)(1),(f)(3),(f)(5), FHIR APIs (g)(7),(g)(10), and direct messaging (h)(1). This breadth indicates a full-featured clinical EHR, not a narrow specialty module.

The certified module appears to be the core of the product — the vendor markets Pulse EHR, PulsePro (practice management), PulseRCM (revenue cycle management), and Population Health as an integrated suite, but the EHR/PM components are tightly coupled. The SED intended user description is "Providers, clinical users, support staff," confirming ambulatory clinical and administrative users.

### Users & Market

- **Settings**: Ambulatory practices across multiple specialties. The vendor website highlights case studies in urology, gastroenterology, and orthopedics. Third-party review sites list supported specialties as primary care, FQHCs, community health, rural clinics, behavioral health, pediatrics, cardiology, neurology, oncology, and orthopedics.
- **Practice sizes**: Solo practices to multi-site groups, ASCs, IDNs, and MSOs.
- **Scale**: "Thousands of providers" — exact numbers not disclosed. The product appears to be a small-to-mid-market ambulatory EHR, not a large enterprise system.
- **Deployment**: Cloud-based or server-based options available.
- **Reviews**: Very limited review presence — Software Advice and FindEMR list the product but with only ~2 user reviews. One user praised ease of navigation and seamless PM/EHR integration; another noted "too many clicks or duplicate modules" during training. A 95% satisfaction rating is claimed but based on a very small sample.

### Modules & Functionality

Based on vendor website descriptions, review sites, and certification criteria:

**Clinical Documentation (EHR)**
- Customizable flow sheets configurable per provider
- "Pulse Note" — described as an "Advanced Clinical Knowledge Engine" for clinical intelligence
- Patient Clinical Snapshot (PCS) — consolidated patient overview
- Multiple problem visit templates for various encounter types
- Point-of-care charting with E&M code checking
- Evaluation & Management (E&M) coder for documentation accuracy

**Computerized Provider Order Entry (CPOE)**
- Medication ordering with drug interaction checking
- Laboratory order entry
- Diagnostic imaging order entry

**E-Prescribing**
- Surescripts Gold Solution Provider
- Electronic prescribing functionality (costs listed as one-time and ongoing fees on mandatory disclosures page)
- EPCS capability implied by Surescripts integration but not explicitly confirmed on vendor site

**Practice Management (PulsePro)**
- Advanced scheduling and patient registration
- Medical billing, coding, and claims processing
- Insurance eligibility verification (individual or batch mode)
- Automated workflow lists for task management
- A/R tracking and management
- Payment posting, claim appeals, payment reconciliation, denial refiling
- Proprietary analytics and reporting

**Revenue Cycle Management (PulseRCM)**
- Claims management with 98% first-pass clean claims rate (per vendor)
- Certified coding support
- Denial management and root cause analysis
- Can be technology-only or bundled with managed services

**Patient Engagement**
- Patient portal via InteliChart partnership — provides 24/7 secure access to health records, lab/diagnostic results, educational materials, and discharge instructions (monthly fees apply per mandatory disclosures)
- Pulse Engage — automated, integrated patient reminder system for appointments

**Population Health**
- Clinical Quality Measures (CQM) module — tracks and submits quality data to CMS
- Care gaps identification and remediation
- Patient View feature for pre-visit review
- Chronic Care Management module
- Practice-wide analytics (risk stratification, quality measurement, performance tracking)
- MACRA/MIPS qualification support
- Qualified CMS Registry for PQRS incentives

**Document Management**
- Integrated document, fax, and transcription management
- Voice-to-text transcription capabilities

**Public Health Reporting**
- Immunization registry reporting — certified (f)(1)
- Electronic case reporting — certified (f)(3)
- Electronic reportable lab results — certified (f)(5)

**Interoperability**
- Transitions of care / C-CDA exchange — certified (b)(1)–(b)(3)
- Direct secure messaging — certified (h)(1)
- FHIR-based APIs for patient and population services — certified (g)(7),(g)(10)
- EHI export — certified (b)(10)
- Lab integration (results automatically attached to patient records)

### Data & Content

Based on the features and certifications described above, the product manages:

- **Patient demographics and registration data** — core PM function
- **Clinical notes and encounter documentation** — flow sheets, templates, Pulse Note engine
- **Medication lists and prescription history** — CPOE and e-prescribing via Surescripts
- **Laboratory orders and results** — CPOE and lab integration
- **Diagnostic imaging orders** — CPOE certified
- **Vital signs and clinical measurements** — documented in review sites
- **Problem lists and diagnoses** — multiple problem visit templates
- **Family health history** — listed in mandatory disclosures certification criteria
- **Implantable device data** — listed in mandatory disclosures
- **Allergies/drug interactions** — drug interaction checking is a certified feature
- **Scheduling and appointment data** — PulsePro scheduling module
- **Billing, claims, and financial data** — PulsePro billing/coding, PulseRCM claims management
- **Insurance eligibility and payer data** — eligibility verification feature
- **Quality measure data** — CQM module, MIPS/MACRA reporting
- **Patient portal messages and shared records** — InteliChart integration
- **Faxes, transcriptions, and scanned documents** — integrated document management
- **Care plan and care gap data** — population health module
- **Audit logs and access records** — certified (d) criteria for security
- **Immunization records** — public health reporting certified
- **Clinical decision support rules** — certified (a)(14)

**Data gaps / uncertainties:**
- The vendor website does not explicitly mention **referral management** as a distinct module, though transitions of care certification implies some referral tracking capability.
- No mention of **telehealth/virtual visit** capabilities on the Pulse website, though the broader Harris Ambulatory group offers "virtual care solutions."
- **Secure messaging between providers** (beyond Direct) is not explicitly described — unclear whether the system supports internal messaging workflows.
- The distinction between data stored in Pulse EHR vs. data managed solely within the InteliChart patient portal is unclear — the portal is a third-party integration, so portal-specific data (patient-entered information, message threads) may reside partially outside the Pulse system.

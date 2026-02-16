# Epic Systems Corporation — Product Research

Researched: 2026-02-16
Developer website: https://www.epic.com

## Overview

Epic Systems Corporation is the dominant electronic health record (EHR) vendor in the United States, founded in 1979 by Judy Faulkner and headquartered in Verona, Wisconsin. Epic is privately held and employs approximately 13,000 people. As of 2025, Epic's systems hold records for over 325 million patients (~79% of the US population) and are used in approximately 3,300+ hospitals and 73,000+ clinics. The company reported ~$5.7 billion in revenue for 2024. Epic holds 42.3% of the acute-care hospital market (54.9% of hospital beds), with Oracle Health (Cerner) a distant second at ~23%. All 20 U.S. News & World Report Best Hospitals run on Epic.

Epic builds a single, comprehensive, integrated health record platform — not a collection of loosely coupled products. The company develops everything in-house with no acquisitions, no mergers, and no rebranding history. They sell directly to health systems (no channel partners or white-label). The platform is primarily on-premise with Epic hosting options available. Epic has near-100% customer retention and captured ~70% of all hospital EHR transitions in 2024.

## Product: EpicCare Inpatient Base

CHPL IDs: 11603 (Feb 2025), 11653 (May 2025), 11686 (Aug 2025), 11730 (Nov 2025)

### What It Is

EpicCare Inpatient (internally known as "ClinDoc") is the inpatient/hospital clinical documentation module of Epic's integrated EHR platform. It is **not** a standalone product — it is one certified module within a much larger platform. The "product" in regulatory terms is the entire Epic EHR system, which includes dozens of tightly integrated modules spanning clinical care, revenue cycle, patient engagement, analytics, and more. EpicCare Inpatient Base is certified across 35 ONC criteria covering clinical data ((a)(1)–(a)(5), (a)(12), (a)(14)), transitions of care ((b)(1)–(b)(3)), EHI export ((b)(10)–(b)(11)), clinical quality measures ((c)(1)–(c)(3)), patient portal ((e)(1), (e)(3)), public health reporting ((f)(1)–(f)(2), (f)(5), (f)(7)), and FHIR APIs ((g)(2)–(g)(10)).

### Users & Market

EpicCare Inpatient is used by physicians, nurses, pharmacists, case managers, infection preventionists, and other hospital-based clinical staff. It is deployed in settings ranging from community hospitals to major academic medical centers, including all 20 U.S. News Best Hospitals. Notable customers include Mayo Clinic, Cleveland Clinic, Johns Hopkins, Kaiser Permanente, Mass General Brigham, NYU Langone, UC Health systems, and many others. Epic also extends its platform to smaller hospitals through its Community Connect program, where large health systems host Epic for affiliated community hospitals and practices.

### Modules & Functionality

The certified EpicCare Inpatient module is part of a much larger Epic EHR product. Based on Epic's own website (epic.com/software/acute-and-inpatient-care/) and third-party descriptions, the inpatient-facing portions of Epic include:

**Core Inpatient Clinical (ClinDoc):**
- Progress notes, assessments, care plans, and discharge documentation
- Customizable flowsheets for vitals, intake/output, and clinical data tracking
- Medication administration records (MAR) and medication reconciliation
- Clinical decision support with alerts and guidelines
- AI-powered features: ambient listening for charting, AI-generated shift notes, smart insights for patient catch-up
- Nursing documentation including shift handoff tools
- Bedside charting via Rover mobile app

**Hospital Medicine:**
- Single patient record with clinical pathways and embedded AI
- Care transition support between units and care teams

**Critical Care:**
- Specialized views for ICU/intensivist workflows
- Early warning and deterioration detection tools

**Inpatient Pharmacy (Willow):**
- Medication ordering, verification, preparation, dispensing, and administration
- Automated pharmacy communication and inventory management
- Financial support suggestions embedded in decision support

**Infection Control (Bugsy):**
- Infection surveillance and trend analysis
- Regulatory reporting for healthcare-associated infections

**Case Management:**
- Utilization review with AI assistance
- Payer communication tools
- Post-acute placement coordination

**Surgical/Perioperative (OpTime):**
- Operating room scheduling and management
- Surgical documentation and perioperative care
- Anesthesia documentation

**Emergency Department (ASAP):**
- ED-specific workflows and tracking boards
- Triage and patient flow management

**Laboratory (Beaker):**
- Clinical and anatomic pathology
- Lab order management and results reporting

**Radiology (Radiant):**
- Imaging workflows, order tracking, results

**Patient Experience:**
- Inpatient MyChart Bedside for patient engagement
- Smart TV integration for patient education and clinical data access
- Secure communication between patients and care teams

**Unified Communications:**
- Secure chat, push notifications, nurse call integration, VoIP
- Integrated into the same devices used for clinical documentation

**Specialty Modules (all integrated):**
- Oncology (Beacon): chemotherapy protocols, cancer care management
- Cardiology (Cupid): invasive and non-invasive cardiology workflows
- Obstetrics (Stork): labor and delivery, perinatal documentation
- Transplant (Phoenix): transplant program management
- Ophthalmology (Kaleidoscope)
- Endoscopy (Lumens)
- Orthopedics (Bones)
- Dentistry (Wisdom)
- Genetics, Dermatology, and others

**Revenue Cycle (Resolute):**
- Hospital billing (Resolute HB): coding, claims submission, denial management, payment reconciliation
- Professional billing (Resolute PB)
- Patient registration (Prelude) and insurance verification
- Charge capture automation (integrated into clinical workflow — per Royal Marsden case study showing 550% increase in charge capture)

**Scheduling & Patient Flow:**
- Cadence: appointment scheduling across ambulatory and specialty
- Grand Central: ADT (admission/discharge/transfer) and bed management

**Patient Portal (MyChart):**
- Over 180 million active US users
- Health record access, secure messaging, appointment scheduling, bill payment, telehealth
- Proxy access for caregivers

**Interoperability:**
- Care Everywhere: health information exchange within and outside Epic network
- Bridges: HL7 and FHIR interface engine for external system integration
- EpicCare Link: portal for community-connected providers

**Population Health (Healthy Planet):**
- Risk stratification, care gap identification
- Value-based care analytics, ACO management
- Population-wide outcomes tracking

**Analytics & Data Warehouse:**
- Caboodle: enterprise data warehouse
- Reporting Workbench: ad-hoc operational and clinical reporting
- Cosmos: de-identified research database across Epic community

**Care at Home:**
- Home health documentation and workflows
- Telehealth and remote patient monitoring integration

**Payer Platform:**
- Tools for payer-provider collaboration, prior authorization, claims status

**Mobile Applications:**
- Haiku: physician smartphone app
- Canto: physician/provider tablet app
- Rover: nursing/ancillary bedside mobile app

### Data & Content

Given the breadth of the integrated Epic platform, the data stored encompasses essentially all aspects of patient care and health system operations:

- **Clinical data:** Diagnoses, problems, medications, allergies, immunizations, vital signs, lab results, imaging results, pathology results, clinical notes (progress notes, H&Ps, discharge summaries, operative notes, consultation notes), nursing assessments, care plans, flowsheet data, growth charts
- **Medication data:** Prescriptions (inpatient and outpatient), medication administration records, pharmacy dispensing records, e-prescribing via Surescripts integration
- **Order data:** All CPOE orders for labs, imaging, medications, procedures, referrals, consults
- **Surgical/procedural data:** Operative reports, anesthesia records, perioperative documentation, surgical scheduling
- **Specialty data:** Oncology treatment plans/chemotherapy regimens (Beacon), cardiac catheterization data (Cupid), OB/perinatal records (Stork), endoscopy reports (Lumens), transplant records (Phoenix)
- **Billing/financial data:** Claims, charges, payments, insurance information, patient financial responsibility, authorization data (Resolute HB/PB)
- **Scheduling data:** Appointments, bed assignments, OR scheduling, ADT events (Cadence, Grand Central)
- **Patient-generated data:** MyChart messages, patient-reported outcomes, proxy/caregiver records, self-scheduled appointments, telehealth encounters
- **Documents and media:** Scanned documents, uploaded images, external records received via Care Everywhere
- **Public health data:** Immunization registry submissions, syndromic surveillance data, cancer registry reports, electronic case reporting
- **Population health data:** Risk scores, care gap lists, quality measure data, attributed patient panels (Healthy Planet)
- **Infection control data:** Surveillance records, infection trends, regulatory reports (Bugsy)
- **Communication data:** Secure messages (provider-to-provider, provider-to-patient), pager/VoIP records
- **Audit and access data:** User access logs, record access auditing
- **Research data:** Clinical trial management data, de-identified data in Cosmos

The mandatory disclosures PDF at epic.com/docs/mucertification.pdf was not renderable in text form, but the URL is confirmed active. The certification numbers align with CHPL listings.

---

## Product: EpicCare Ambulatory Base

CHPL IDs: 11604 (Feb 2025), 11654 (May 2025), 11687 (Aug 2025), 11731 (Nov 2025)

### What It Is

EpicCare Ambulatory is the outpatient/clinic clinical documentation module of Epic's integrated EHR platform. Like EpicCare Inpatient, it is a certified component of the same comprehensive Epic EHR product — not a separate standalone system. It shares the same database, the same patient record, and the same integrated module ecosystem. It is certified across the identical 35 ONC criteria as EpicCare Inpatient.

### Users & Market

EpicCare Ambulatory is used by outpatient physicians, advanced practice providers, nurses, medical assistants, and practice staff in ambulatory settings including primary care, specialty clinics, urgent care, and multi-site group practices. It serves the same customer base as EpicCare Inpatient — the outpatient arms of health systems running Epic. Epic reports being used in 73,000+ clinics. The Community Connect program extends ambulatory Epic to affiliated independent practices and physician groups.

### Modules & Functionality

EpicCare Ambulatory shares the vast majority of its platform and modules with EpicCare Inpatient. The key difference is the user interface and workflows optimized for outpatient visit-based care rather than inpatient admission-based care:

**Core Ambulatory Clinical:**
- Visit-based clinical documentation using SmartTools (SmartText, SmartPhrases, SmartLinks)
- Specialty-specific templates for primary care, pediatrics, cardiology, dermatology, OB/GYN, and many others
- Problem list, medication list, allergy management
- Clinical decision support and best practice alerts
- AI-powered ambient documentation and note drafting

**Order Management:**
- Outpatient orders for labs, imaging, referrals, procedures
- E-prescribing (integrated with Surescripts)
- Order sets and preference lists

**Chart Management:**
- Comprehensive longitudinal patient record shared with inpatient
- Results review, trend analysis
- Document management and scanning

**Scheduling & Registration:**
- Cadence for ambulatory appointment scheduling
- Prelude for patient registration and check-in
- Welcome kiosks for self-service check-in

**Billing:**
- Resolute Professional Billing (PB) for professional/physician billing
- Charge capture embedded in visit workflows
- Insurance verification and eligibility checking (Benefits Engine, Tapestry)

**All shared modules** listed under EpicCare Inpatient above also apply: MyChart, Healthy Planet, Beaker, Willow (outpatient pharmacy), Care Everywhere, Caboodle, Cosmos, Bridges, mobile apps (Haiku, Canto), etc.

### Data & Content

EpicCare Ambulatory stores data in the same unified Epic database as EpicCare Inpatient. The data categories are identical (see above). The distinction is primarily in what workflows generate which data — ambulatory encounters produce office visit notes, outpatient orders, referrals, and ambulatory-specific scheduling data, while inpatient encounters produce admission records, inpatient orders, nursing flowsheets, and discharge documentation. Both flow into the same patient record.

Key ambulatory-specific data includes:
- Office visit notes with specialty-specific templates
- Outpatient prescriptions and e-prescribing records
- Referral orders and tracking
- Preventive care reminders and health maintenance protocols
- After-visit summaries
- Patient instructions and handouts
- Ambulatory procedure documentation

---

## Key Observations for EHI Export Assessment

1. **Single platform, two certified modules:** EpicCare Inpatient and EpicCare Ambulatory are not separate products — they are two certified views into the same comprehensive Epic EHR. An EHI export from this "product" would need to cover data from the entire Epic platform, not just the clinical documentation modules.

2. **Massive data footprint:** Epic's integrated platform stores data from clinical care, revenue cycle, patient engagement, population health, analytics, scheduling, registration, pharmacy, lab, radiology, surgery, specialty care, infection control, case management, communications, and more. This is one of the broadest data footprints of any EHR.

3. **Revenue cycle is built-in:** Unlike some EHRs, Epic's billing (Resolute) is fully integrated — not a separate third-party product. Claims, charges, payments, and insurance data are part of the product.

4. **MyChart data is part of the product:** Patient messages, patient-reported data, self-scheduling activity, proxy access, and telehealth records all live within the Epic platform.

5. **Population health and analytics data:** Healthy Planet's risk scores, care gaps, quality measures, and attributed patient panels are stored within Epic.

6. **Research data:** Cosmos (the de-identified research database) and clinical trial management data are part of the Epic ecosystem.

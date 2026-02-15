# CareCloud, Inc. — Product Research

Researched: 2026-02-14
Developer website: https://www.carecloud.com

## Overview

CareCloud, Inc. (NASDAQ: CCLD) is a publicly traded, cloud-based healthcare IT company headquartered in Somerset, New Jersey, with approximately 4,000 employees worldwide. The company was originally founded in 1999 as Medical Transcription Billing Corporation (MTBC), focused on transcription and medical billing for New Jersey healthcare providers. It went public on NASDAQ in 2014.

In January 2020, MTBC acquired the original CareCloud Corporation — a Miami-based practice management and EHR company founded in 2009 that served over 7,000 providers — for up to $40M. MTBC also acquired Meridian Medical Management that year for $24.8M. In 2021, MTBC renamed itself CareCloud, Inc., adopting the acquired company's brand. Over its history, the company has made 16+ acquisitions in healthcare IT and revenue cycle management.

Most recently, in August 2025, CareCloud acquired Medsphere Systems Corporation, expanding into the hospital IT market with inpatient EHR (CareVue), emergency department (Wellsoft), supply chain (HealthLine), and ambulatory EHR (ChartLogic) products across 600+ hospital clients in 50 states. CareCloud's core market prior to this was ambulatory practices — from solo physicians to multi-site groups — across a wide range of specialties.

CareCloud offers an integrated suite: EHR, practice management, revenue cycle management (RCM), patient engagement, telehealth, medical coding/transcription, and AI-powered clinical and administrative tools. Their go-to-market serves over 40,000 providers according to their website.

## Product: CareCloud Prime

CHPL IDs: 11504

### What It Is

CareCloud Prime is the company's flagship EHR platform, described as "the pinnacle of electronic health records platforms." It is a cloud-based, ONC-certified EHR system priced at $249/provider/month. The CHPL product number (15.04.04.2790.Clou.02.02.1.240821) indicates certification date of August 21, 2024.

CareCloud Prime appears to be the current marketing name for the integrated EHR offering that encompasses what was previously (or in parallel) known as "CareCloud Charts." The vendor website's EHR login section presents three separate access portals — CareCloud (Charts), talkEHR, and Archivus — suggesting these are distinct platforms with separate codebases, though all fall under the CareCloud umbrella. CareCloud Prime, Charts, and talkEHR all appear in the vendor's materials as separate but related EHR products.

The SED intended user description in CHPL metadata lists "Pediatric Nephrology," but this reflects the usability testing setting, not the product's target market. The product serves a broad range of ambulatory specialties.

The certification is very broad, with 40+ criteria spanning clinical data (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); care coordination (b)(1)–(b)(3), (b)(7)–(b)(11); patient portal (e)(1), (e)(3); clinical quality measures (c)(1)–(c)(4); public health reporting (f)(1), (f)(2), (f)(4), (f)(6), (f)(7); FHIR API (g)(7), (g)(9), (g)(10); and more. This breadth indicates a comprehensive clinical system with capabilities spanning CPOE, CDS, care plans, patient portal, immunization/syndromic/cancer reporting, and electronic prescribing.

### Users & Market

CareCloud's customer base spans ambulatory practices of all sizes, from solo practitioners to large multi-site groups and academic institutions. The vendor website mentions over 40,000 providers on the platform. Case studies reference urology practices, urgent care centers, orthopedic groups, and the University of Tennessee Health Science Center. The EHR page specifically lists Internal Medicine, Family Practice, Urgent Care, and General Surgery with a "View All Specialties" option.

talkEHR, a separate product under the CareCloud umbrella, comes with 70+ customizable specialty-specific workflows and templates covering cardiology, dermatology, pediatrics, and more. It's unclear whether CareCloud Prime/Charts has an equivalent breadth of specialty templates, though the marketing suggests broad specialty support.

Day-to-day users include physicians (charting, ordering, prescribing), clinical staff (patient flow, documentation), billing staff (claims, RCM), practice managers (scheduling, analytics, reporting), and patients (via the Breeze portal).

### Modules & Functionality

Based on vendor materials and product pages, CareCloud Prime / the integrated CareCloud platform includes:

**Clinical Documentation & Charting (CareCloud Charts)**
- Flexible charting with customizable templates and order sets (per carecloud.com/ehr/features/)
- AI-powered encounter summaries and clinical note generation via cirrusAI Notes (ambient listening + generative AI)
- Real-time clinical documentation via voice capture
- Predefined specialty-specific clinical templates
- Pre-configured treatment protocols and integrated order sets
- Unified patient summary showing medications, problems, allergies, vitals, labs, immunizations

**Clinical Decision Support**
- Real-time CDS at point of care — drug-drug interactions, drug-allergy alerts
- Evidence-based clinical recommendations (cirrusAI Assist)
- Intelligent task prioritization

**Computerized Provider Order Entry (CPOE)**
- Medication orders (certified (a)(1))
- Lab orders (certified (a)(2))
- Imaging/radiology orders (certified (a)(3))

**Electronic Prescribing**
- ePrescribing including controlled substances (EPCS)
- Integration with Surescripts (per mandatory disclosures page)
- Drug interaction checking

**Patient Portal & Engagement (Breeze + Community)**
- Breeze: patient-facing platform for appointment scheduling, check-in, intake forms, prescription refill requests, secure messaging, consent forms, online bill pay, telehealth
- Community: provider-facing suite with secure patient portal, real-time staff chat, patient acquisition tools, community manager for targeting patient populations
- Automated appointment reminders via text, email, and phone
- Patient access to medical records, test results, treatment plans
- Multiple payment options with saved methods and automated billing

**Practice Management (CareCloud Central)**
- Multi-view calendar scheduling with drag-and-drop
- Patient registration and demographics management
- Insurance eligibility verification
- Claims submission and tracking — electronic submission
- CollectiveIQ: advanced claim scrubbing with millions of Medicare and commercial payer edits
- Contract management for payment accuracy — underpayment/overpayment detection
- Real-time analytics dashboards and KPI tracking
- Automated billing and coding

**Revenue Cycle Management (RCM)**
- End-to-end billing services
- Denial management and appeals (cirrusAI Appeals generates customized appeal letters)
- Payment processing and patient statements

**Telehealth**
- Integrated virtual care platform
- Cross-platform (computer, Android, iOS)
- Integrated with Breeze patient engagement flow

**Reporting & Analytics**
- Advanced reporting for clinical insights
- Population health management analysis
- Quality initiative tracking (CQMs — certified for (c)(1)–(c)(4))
- Dynamic data visualization dashboards
- Practice performance metrics
- Meaningful Use / Promoting Interoperability reporting

**Public Health Reporting**
- Immunization registry reporting (f)(1)
- Syndromic surveillance (f)(2)
- Cancer case reporting (f)(4)
- Electronic reportable lab results (f)(6)
- Health care surveys (f)(7)

**Interoperability & Data Exchange**
- FHIR-based APIs (g)(7), (g)(9), (g)(10)
- C-CDA document exchange (b)(1)–(b)(3)
- Integration with labs, pharmacies, imaging centers
- Direct messaging (EMR Direct integration per disclosures page)
- MedlinePlus patient education integration

**AI-Powered Tools (cirrusAI + stratusAI)**
- cirrusAI Notes: ambient clinical documentation
- cirrusAI Chat: AI chatbot for EHR workflow navigation
- cirrusAI Guide: automates clinical data input, real-time recommendations
- cirrusAI Appeals: generates claim appeal letters
- stratusAI Desk Agent: automated front desk call handling and scheduling

**Additional Services**
- Medical coding and transcription services
- Physician credentialing services
- Chronic Care Management (CCM) — $62/Medicare patient
- Remote Patient Monitoring (RPM) — $120/Medicare patient, with real-time device monitoring and staff alerts
- Data migration services and personalized onboarding

### Data & Content

Based on the features and certifications described above, CareCloud Prime stores and manages:

**Clinical Data** (evidence: certified criteria (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); Charts feature page describing patient summaries):
- Patient demographics and registration information
- Problem lists, medication lists, allergy lists
- Vital signs
- Lab results and orders
- Imaging/radiology orders
- Clinical notes and encounter documentation (including AI-generated summaries)
- Immunization records
- Care plans
- Clinical decision support alerts/interactions

**Medication & Prescribing Data** (evidence: ePrescribing feature, Surescripts integration, EPCS certification):
- Prescription history
- Drug interaction records
- Controlled substance prescribing records

**Scheduling & Workflow Data** (evidence: Central practice management features):
- Appointment schedules and calendars
- Patient check-in status and flow
- Task assignments and unified inbox notifications
- Staff communications (real-time chat)

**Billing & Financial Data** (evidence: Central/CollectiveIQ features, RCM services):
- Insurance information and eligibility verification records
- Claims data — submission, tracking, scrubbing results
- Payment records — insurance and patient payments
- Denial and appeal records
- Contract rates and underpayment/overpayment analysis
- Patient statements and balances

**Patient-Generated & Portal Data** (evidence: Breeze and Community features):
- Patient intake forms
- Secure messages between patients and providers
- Appointment requests
- Prescription refill requests
- Consent forms (e-signatures)
- Patient payment information (saved payment methods)
- Telehealth session data

**Reporting & Quality Data** (evidence: certified (c)(1)–(c)(4), (f)(1)–(f)(7)):
- Clinical quality measure calculations
- Public health reports (immunization, syndromic, cancer, lab, survey)
- Population health analytics
- Practice performance metrics

**Document & Integration Data** (evidence: (b)(1)–(b)(3), interoperability features):
- C-CDA clinical documents (sent and received)
- Direct messages
- Lab interface results
- Scanned/uploaded documents

The mandatory disclosures page also references integration with Surescripts (e-prescribing), EMR Direct (health information exchange), and MedlinePlus (patient education), confirming data flows through these channels.

One area of uncertainty: the relationship between CareCloud Prime, CareCloud Charts, and talkEHR is not entirely clear. They appear as separate login portals on the vendor's site, suggesting potentially separate databases or product architectures. The CHPL certification is specifically for "CareCloud Prime" version 2.0, but the marketing materials often reference "Charts" and "Prime" somewhat interchangeably. It is possible that "CareCloud Prime" is the certified product name for what is marketed as "CareCloud Charts" or an integrated offering built on top of Charts.

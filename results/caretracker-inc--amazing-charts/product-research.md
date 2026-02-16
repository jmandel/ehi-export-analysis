# CareTracker, Inc. — Product Research

Researched: 2026-02-16
Developer website: https://www.amazingcharts.com

## Overview

CareTracker, Inc. is the corporate entity that develops and markets Amazing Charts, an ambulatory EHR and practice management platform targeted at small to medium-sized independent medical practices (1–10 clinicians). The product was founded in 2001 by a practicing family physician and acquired in 2017 by Harris Healthcare, a division of N. Harris Computer Corporation, which is itself a subsidiary of Constellation Software Inc. (TSX: CSU). Harris Healthcare practices a "Family is Forever" policy (no reselling of acquired companies) and a "Software for Life" philosophy.

Under Harris Healthcare, Amazing Charts sits alongside several sibling products including Harris CareTracker (a cloud-based RCM/PM platform oriented toward billing companies), digiChart, Clinix, MEDfx, and Pulse. Despite the CHPL developer being listed as "CareTracker, Inc.," the certified product is Amazing Charts — Harris CareTracker is a distinct product. The contact email in CHPL metadata (kgaglio@harriscomputer.com) confirms the Harris corporate parent.

At the time of Harris's 2017 acquisition, Amazing Charts reported nearly 4,000 practices and 20,000 clinicians/staff (per Constellation Software press release). A subsequent EMR Industry listing cites 6,300+ unique practices and 25,000+ clinicians and office staff, with growth of 75+ new practices per month. The practice management page on the current website states "over 2,000 practices." These numbers likely reflect different points in time or different product scopes.

Amazing Charts is known for affordability and ease of use, consistently rated as a top EHR for small practices. It holds a ~3.6/5 rating on Capterra (99 reviews) and 4.1/5 on G2 (7 reviews). Common praise centers on the simple one-screen charting interface and low cost; common complaints include technical instability (crashes, cloud version slowness), inconsistent customer support, and limited specialty depth compared to enterprise EHRs.

## Product: Amazing Charts

CHPL IDs: 11492 (v12.0), 11608 (v12.2), 11646 (v12.3), 11720 (v12.4)

### What It Is

Amazing Charts is an ONC-certified ambulatory EHR with integrated practice management, medical billing services, and patient engagement capabilities. It is designed by and for physicians in independent outpatient practices. The product offers both local server installation and cloud-based deployment options.

The certified Health IT Module (versions 12.0 through 12.4) covers a broad set of ONC criteria: clinical documentation (a)(1)–(a)(5), (a)(9)/(a)(12)/(a)(14); transitions of care and EHI export (b)(1)–(b)(3), (b)(10)–(b)(11); clinical quality measures (c)(1)–(c)(3); privacy/security (d)(1)–(d)(9), (d)(12)–(d)(13); patient access (e)(3); public health reporting (f)(1), (f)(5); and API/FHIR access (g)(2)–(g)(7), (g)(9)–(g)(10). This is a comprehensive clinical certification profile indicating the EHR stores and manages a wide range of patient clinical data.

The product relies on several third-party components listed as "Additional Software Used":
- **NewCrop** (by DrFirst) — for e-prescribing, including EPCS (electronic prescribing of controlled substances), drug-drug/drug-allergy interaction checking, and drug-formulary checks via the Surescripts network
- **Updox** — for the patient portal, secure messaging, and Direct messaging (care coordination)
- **Unis** — appears in newer certifications (12.3, 12.4) but its specific role is not described on the website
- **eCR FHIR Now App** — for electronic case reporting to public health agencies under (f)(5)
- **Merck Manuals / Medline Plus** — for clinical decision support and patient education (referenced in v12.0/12.2 additional software)

### Users & Market

Amazing Charts primarily serves independent, physician-owned ambulatory practices with 1–10 clinicians. The SED intended user description in CHPL is "Ambulatory Medical Practices."

**Specialties supported** (per vendor website): Family Medicine, Pediatrics, Dermatology, Internal Medicine, Urgent Care, Surgery (including plastic surgery), and others. The product uses customizable templates to adapt to different specialties, though its roots are in primary care/family medicine.

**User base**: The 2017 Constellation Software acquisition press release cited nearly 4,000 practices and 20,000 clinicians/staff. An EMR Industry listing (likely somewhat dated) cites 6,300+ practices and 25,000+ users. The current website's practice management page claims "over 2,000 practices" — the discrepancy is unexplained but may reflect different product scopes or post-acquisition customer dynamics.

**End users**: Physicians, clinical staff (charting, orders, prescriptions), front-office staff (scheduling, intake), billing staff (claims, payment posting), and patients (via portal). The product is used in solo practices, small group practices, and some multi-site settings.

**Go-to-market**: Direct sales via the amazingcharts.com website with demo requests and consultations. Part of the broader Harris Healthcare portfolio but marketed independently.

### Modules & Functionality

The Amazing Charts product suite comprises several components, some tightly integrated and some sold separately:

#### 1. Electronic Health Record (EHR)
The core clinical module. Key features described on the vendor website and mandatory disclosures:
- **Clinical Documentation / Charting**: One-screen patient record display, customizable templates (specialty-specific), progress notes, problem lists, medication lists, allergy lists. Designed by a physician to minimize clicks. (amazingcharts.com/ehr)
- **E-Prescribing**: Built-in prescription management powered by NewCrop/Surescripts. Supports EPCS (controlled substances). Drug-drug interaction checking, drug-allergy interaction checking, drug-formulary checks. When e-prescribing fails, falls back to e-fax. (mandatory disclosures page)
- **Lab Integration**: Electronic lab ordering and results receipt. Supports HL7 interfaces with major labs. Results parsed into the chart. (vendor website FAQ, third-party reviews)
- **Immunization Records**: Records immunizations and transmits to state immunization registries via HL7 2.5.1 standard. Provider-based annual subscription for registry connectivity. (mandatory disclosures)
- **Clinical Decision Support**: Diagnostic reference information via Merck Manuals and Medline Plus integration. (mandatory disclosures, listed as additional software)
- **Clinical Quality Measures (CQMs)**: Supports 50+ CQMs for MIPS/quality reporting. Requires additional subscription enrollment. (mandatory disclosures)
- **Transitions of Care**: C-CDA document generation and consumption. Direct messaging via Updox for care coordination with Direct Trust members. (mandatory disclosures, (b)(1)–(b)(3) criteria)
- **Electronic Case Reporting**: Via eCR FHIR Now App integration for public health reporting under (f)(5). Annual subscription fee. (mandatory disclosures)
- **FHIR API Access**: Certified for (g)(7)–(g)(10), providing standardized API access to patient data via FHIR.
- **Secure Internal Messaging**: Staff-to-staff messaging within the EHR. (amazingcharts.com/ehr)
- **Reporting**: Preset reports and custom query builder for practice metrics. (amazingcharts.com/ehr)

#### 2. Practice Management (PM)
Described as a separate but integrated system that "shares patient data" with the EHR (per the FAQ on the PM page). Key features:
- **Appointment Scheduling**: Multi-provider calendars, resource management. Patient self-scheduling available through the patient engagement module. (amazingcharts.com/practice-management)
- **Insurance Eligibility Verification**: Pre-appointment coverage verification to reduce denials. (PM page)
- **Claims Management**: Claim creation, electronic submission via integrated Secure Connect Clearinghouse. Claim status tracking, denial management. (PM page)
- **Payment Posting**: Electronic remittance processing, patient payment posting. Credit card processing supported. (PM page, FAQ)
- **Financial Reporting**: Revenue cycle reports, unpaid claims tracking, reimbursement delay identification. (PM page)

#### 3. Medical Billing Services (RCM)
Amazing Charts also offers outsourced medical billing/RCM services (not just software). This is a managed service where billing specialists handle:
- Automated claims processing with claim scrubbing
- Denial management and appeals
- Payment posting (payer remittance and patient payments)
- Patient statement management and follow-up
- Claims analysis and optimization
- Targets 95% first-pass payment rate
(amazingcharts.com/medical-billing)

#### 4. Patient Engagement — "AC Patient Connect"
A digital patient engagement platform. Features described on the vendor website:
- **Patient Portal**: 24/7 access to health information, lab results, visit summaries. Powered by Updox partnership. (patient engagement page, mandatory disclosures)
- **Online Scheduling**: Patient self-scheduling with decision trees.
- **Appointment Reminders**: SMS text reminders to reduce no-shows.
- **Digital Patient Intake**: Electronic forms sent based on appointment type, replacing paper forms.
- **Secure Digital Consents**: Electronic consent form signing.
- **Secure Messaging**: Two-way patient-provider messaging via the portal.
- **Telemedicine Integration**: Virtual visit capability.
- **Customizable Alerts**: Automated reminders for medications, preventive care, appointments.
(amazingcharts.com/patient-engagement)

### Data & Content

Based on the certified criteria, vendor website, and mandatory disclosures, Amazing Charts stores and manages the following categories of data:

**Clinical Data** (inferred from certified criteria and described features):
- Patient demographics
- Problem lists / diagnoses (ICD-10, SNOMED)
- Medication lists and prescription history (including controlled substances via EPCS)
- Allergy lists (drug allergies at minimum)
- Vital signs
- Lab orders and results (discrete data from electronic lab interfaces)
- Immunization records
- Clinical notes / progress notes (via customizable templates)
- Clinical decision support interventions and responses
- Care plans
- Referral documentation
- Smoking status and social history (implied by CQM reporting)
- Growth charts and developmental milestones (implied by pediatric specialty support)

**Prescription/Medication Data**:
- E-prescribing records via NewCrop/Surescripts
- Drug interaction check results
- Formulary check results
- Controlled substance prescribing records (EPCS)

**Transitions of Care Data**:
- C-CDA documents (sent and received)
- Direct messages (via Updox / Direct Trust)

**Practice Management / Administrative Data**:
- Appointment schedules and history
- Insurance information and eligibility verification records
- Claims data (submitted, rejected, paid, appealed)
- Payment records (insurance remittance, patient payments, credit card transactions)
- Patient statements
- Financial/revenue cycle reports

**Patient Engagement Data**:
- Patient portal messages and communications
- Digital intake form submissions
- Digital consent forms
- Appointment reminder records
- Telemedicine visit records

**Public Health Reporting Data**:
- Immunization registry submissions (HL7 2.5.1)
- Electronic case reports (via eCR FHIR Now App)

**Quality Measures Data**:
- CQM calculation data for 50+ measures (for MIPS reporting)

**Document Management**:
- The product likely supports document scanning/attachment to patient charts (referenced in reviews and typical for the product class), though the vendor website doesn't prominently feature this. PDF viewing software is listed as additional software in v12.0/12.2 certifications, suggesting document management capability.

**What's less clear**:
- The boundary between what data lives in Amazing Charts vs. in third-party systems (NewCrop, Updox, Surescripts) is not fully transparent. E-prescribing data flows through NewCrop and Surescripts — it's unclear how much prescription detail is stored locally in Amazing Charts vs. only in those external systems.
- The vendor website doesn't prominently mention fax management, document scanning, or referral tracking as standalone features, though these are typical for products in this class and mentioned in third-party reviews.
- Whether the practice management module and EHR share a single database or have separate data stores is unclear — the PM FAQ says they "share patient data" but are "separate systems."

---

## Product Ecosystem & Business Context

**Corporate Structure**: Amazing Charts → CareTracker, Inc. → Harris Healthcare → N. Harris Computer Corporation → Constellation Software Inc. (TSX: CSU). Constellation is a large publicly-traded Canadian software conglomerate.

**Sibling Products**: Under Harris Healthcare, the "Amazing Charts family" includes Harris CareTracker (cloud-based PM/RCM, separately branded at harriscaretracker.com), digiChart, Clinix, MEDfx, and Pulse. These are related but distinct products. Harris CareTracker appears oriented more toward billing companies and larger multi-practice operations, while Amazing Charts targets independent physician practices directly.

**Deployment**: Available as locally installed (on-premise server) or cloud-hosted. The cloud version has received criticism in reviews for performance issues. The local installation option is a distinguishing feature for practices that prefer on-premise control.

**Pricing Model**: The base EHR has a purchase/license cost. Additional annual subscriptions required for: Guardian Angel Support & Maintenance (required for e-prescribing and lab/registry interfaces), CEHRT Edition (compliance features), CQM access, immunization registry connectivity, patient portal/Direct messaging, and electronic case reporting. The pricing model involves multiple add-on subscriptions beyond the base EHR.

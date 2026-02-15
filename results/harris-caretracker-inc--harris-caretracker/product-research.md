# Harris CareTracker, Inc — Product Research

Researched: 2026-02-14
Developer website: https://harriscaretracker.com/

## Overview

Harris CareTracker is a cloud-based EHR and practice management platform serving ambulatory medical practices. The company was originally founded in 1995 as Lighthouse Medical Management in Providence, Rhode Island, initially focused on revenue cycle management for physician practices. They launched the CareTracker EMR in 2007 as a web-based system. CareTracker was later a subsidiary of OptumInsight before being acquired in December 2014 by N. Harris Computer Corporation ("Harris"), itself a wholly-owned subsidiary of Constellation Software Inc. (TSX: CSU), a large publicly traded Canadian software conglomerate. The acquisition expanded Harris's existing U.S. healthcare business (which included QuadraMed for hospitals) into the ambulatory market.

The company is now headquartered in Niagara Falls, NY and claims to serve "thousands of providers" over 20+ years. They also serve over 1,600 medical billing companies as partners. The product targets independent physician practices, solo practitioners, multi-location groups, ambulatory surgery centers, and medical billing companies managing multiple client portfolios. Supported specialties include orthopedics, podiatry, pain management, psychiatry, internal medicine, family practice, gastroenterology, pulmonology, chiropractic, physical therapy, and mental health. Pricing starts at $245/month per provider for EHR/EMR and $399/month per provider for practice management.

## Product: Harris CareTracker

CHPL ID: 9589 (Version 9, certified 2018-07-01)

### What It Is

Harris CareTracker is a unified, cloud-based (SaaS) platform that combines Electronic Health Records (EHR), Practice Management (PM), and Revenue Cycle Management (RCM) in a single integrated system. The certified module appears to be the full product — there is no indication of separate components or sub-products. The platform is browser-based, requiring current Windows with Microsoft Edge or Google Chrome.

The product has broad ONC certification covering clinical data criteria (a)(1)–(a)(5), (a)(12), (a)(14); transitions of care (b)(1)–(b)(3); EHI export (b)(10)–(b)(11); clinical quality measures (c)(1)–(c)(3); patient portal (e)(1), (e)(3); public health reporting (f)(1)–(f)(2), (f)(5); FHIR APIs (g)(7), (g)(10); and direct messaging (h)(1). It supports 69 clinical quality measures (CQMs).

### Users & Market

Day-to-day users include physicians, clinical staff, billing staff, and practice managers. The platform is designed for ambulatory/outpatient settings — primarily independent practices and small-to-mid-size groups across multiple specialties. Over 1,600 medical billing companies also use the platform to manage billing for their physician clients.

The vendor positions itself as a long-term infrastructure provider, noting that some practices have used the platform for 20-30 years (including predecessors). They emphasize stability and avoiding disruptive migrations. Being part of the Constellation Software portfolio (a serial acquirer of vertical market software companies), the company has backing from a large corporate parent but operates as a niche ambulatory EHR/PM vendor.

Third-party reviews on Capterra and Software Finder describe the product positively for billing/revenue cycle management (55% positive sentiment) and reporting (60% positive). Weaknesses noted include a clunky interface (55% negative), customer support responsiveness (65% negative), and system reliability/downtime (65% negative). Users praise the billing and claims processing capabilities in particular, with one reviewer noting front-end denials reduced to below 1%.

### Modules & Functionality

Based on vendor website and third-party descriptions, Harris CareTracker encompasses the following functional areas:

**Clinical / EHR:**
- Patient demographics, medical histories, vital signs, allergies, medications, diagnoses, and prescriptions
- Problem lists and medication histories that auto-populate
- Customizable specialty-specific clinical templates (mental health, chiropractic, PT, primary care, multi-specialty)
- Ambient listening/voice dictation for clinical documentation
- Quick text macros for common phrases
- Clinical decision support alerts, drug interaction notifications, and preventive care reminders
- Lab orders and results integration (electronic transmission of orders and results — ETOR)
- E-prescribing (eRx) including Electronic Prescribing of Controlled Substances (EPCS), via Surescripts and DrFirst
- Immunization record management and state immunization registry interface
- Encounter notes with structured documentation
- Patient summary dashboards

**Practice Management / Scheduling:**
- Appointment scheduling with online patient self-scheduling
- Automated appointment reminders (text, email, voice)
- Real-time availability synchronization
- No-show tracking and confirmation systems
- Resource allocation tools

**Billing & Revenue Cycle Management:**
- Integrated charge capture generated from clinical documentation
- Electronic claim submission with automated scrubbing
- Eligibility verification before appointments
- Benefits and copay verification
- Patient responsibility calculation
- Payer-specific claim formatting and rule validation
- Electronic Remittance Advice (ERA) posting (95% accuracy claimed)
- Automated patient statements (mail or email with payment links)
- Denial management with reason code tracking and resolution workflows
- Collections module with integrated clearinghouse
- Days in A/R, net collection rates, aging reports

**Patient Portal & Engagement:**
- Patient portal (included at no extra charge) for viewing health records, lab results, medication lists
- Online appointment requests with clinic approval workflow
- Prescription renewal requests
- Demographic/profile updates by patients
- Bill viewing, outstanding balances, and online payment
- Secure messaging between providers and patients
- Patient intake forms (digital, via InteliChart partnership — "CareTracker Connect")
- Automated patient communications (reminders, follow-ups, custom messages via SMS/email/voice — "CareTracker Connect Pro")
- Patient satisfaction surveys (via InteliChart — "CareTracker Connect Pro")

**Telehealth:**
- Virtual consultation/telehealth capability (mentioned on multiple pages but details are sparse)

**Reporting & Analytics:**
- Practice analytics dashboards (daily collections vs charges, denial rates by payer, days in A/R, revenue trends)
- Customizable reporting tools (Crystal Reporting bundled)
- MIPS/MVP regulatory incentive program support
- Population health dashboards
- eCQM (electronic Clinical Quality Measures) reporting

**Interoperability & Integrations:**
- 600+ integrations claimed (labs, pharmacies, EMR systems, healthcare networks)
- Surescripts (e-prescribing network)
- DrFirst (medication-related services)
- Iron Bridge (connectivity/interoperability)
- EMR Direct (Direct messaging/interoperability)
- State immunization registry interfaces
- Continuity of Care Document exchange
- FHIR API access (g)(7), (g)(10)
- Direct messaging (h)(1)
- Public health reporting: immunization registries (f)(1), syndromic surveillance (f)(2), cancer registry (f)(5)

**Bundled Third-Party Content (no extra cost):**
- Krames (patient education materials)
- IMO (clinical terminology/problem list content)
- Crystal Reporting (report generation)
- Medicomp Medcin (clinical content engine)
- Medi-Span (drug database)

**Add-on Services (additional fees):**
- ePrescribing and controlled substance prescribing (monthly per-provider fee)
- External laboratory interfaces (enrollment and ongoing fees)
- Registry interfaces (enrollment and ongoing fees)

### Data & Content

Based on the features described above, Harris CareTracker stores and manages a broad range of data types:

**Clinical data:** Patient demographics, medical histories, vital signs, allergies, medication lists, problem lists, diagnoses (ICD codes), prescriptions (including controlled substances), encounter/visit notes with structured templates, lab orders and results, immunization records, clinical decision support alerts, and patient summary information. The ambient listening feature generates structured clinical notes from voice recordings.

**Practice management data:** Appointment schedules, provider availability, patient appointment history, no-show records, and resource allocation data.

**Billing/financial data:** Insurance information, eligibility verification records, claims (submitted and tracked), charge capture records, ERA/remittance data, patient statements, payment records, denial records with reason codes, A/R aging data, and collections records. The integrated clearinghouse means claim data flows through the system.

**Patient engagement data:** Patient portal messages, prescription renewal requests, demographic updates submitted by patients, online appointment requests, patient intake forms, patient satisfaction survey responses (via InteliChart integration), and automated communication logs (text, email, voice reminders).

**Interoperability data:** Continuity of Care Documents (sent/received), Direct messages, immunization registry submissions, syndromic surveillance reports, cancer registry submissions, and FHIR API transaction data.

**Content/reference data:** Drug databases (Medi-Span), clinical terminology (IMO), clinical content (Medicomp Medcin), and patient education materials (Krames).

**Reporting data:** eCQM measure results, MIPS/MVP submission data, population health analytics, and practice performance metrics.

The product is genuinely integrated — billing flows from clinical documentation, the patient portal connects to the core EHR/PM, and lab/pharmacy interfaces bring external data into the same system. This means the EHI export should cover a broad data footprint spanning clinical, financial, and administrative domains.

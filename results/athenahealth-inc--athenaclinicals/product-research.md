# athenahealth, Inc. — Product Research

Researched: 2026-02-16
Developer website: https://www.athenahealth.com

## Overview

athenahealth, Inc. is one of the largest ambulatory EHR vendors in the United States, serving 170,000+ providers across approximately 6,700–6,900 customer organizations. The company was founded in 1997 by Jonathan Bush and Todd Park, went public on NASDAQ in 2007, was taken private in 2018 by Veritas Capital and Evergreen Coast Capital (Elliott Management subsidiary) for $5.7B, and was subsequently acquired by Bain Capital and Hellman & Friedman in 2022 for $17B. It is currently privately held, headquartered in Boston, Massachusetts, with approximately 6,300 employees.

athenahealth's flagship platform is **athenaOne**, a fully integrated, cloud-based SaaS platform combining EHR, practice management/billing, and patient engagement. The company's go-to-market is primarily ambulatory/outpatient practices, ranging from solo practitioners to large multi-site health systems and FQHCs, though they also serve hospitals (particularly critical access and community hospitals under ~100 beds). They support 60+ medical specialties. Per KLAS Research, athenahealth has won 47 lifetime Best in KLAS awards and is positioned alongside Epic as a "clear market leader" in ambulatory care, with particular strength in the 11–75 physician independent practice segment.

Key corporate history: In 2013, athenahealth acquired Epocrates (clinical decision support / drug reference app) for $293M. In 2015, they acquired RazorInsights (cloud EHR for small hospitals) and webOMR from Beth Israel Deaconess Medical Center (inpatient EHR). In 2019, after the Veritas acquisition, athenahealth merged with Virence Health (formerly GE Healthcare's Clinical Business Solutions division), which brought in the Centricity product line — later rebranded as athenaPractice, athenaFlow, and athenaIDX. These legacy Centricity products remain separately ONC-certified.

## Product: athenaClinicals (Ambulatory)

CHPL ID: 11714

### What It Is

athenaClinicals is the EHR/EMR module within the athenaOne platform. It is the clinical documentation and clinical workflow component — but it does not stand alone; it is tightly integrated with athenaCollector (billing/practice management) and athenaCommunicator (patient engagement) as parts of the unified athenaOne platform. The certified module is athenaClinicals, but the product that practices actually purchase and use is athenaOne, which includes all three modules plus ancillary capabilities like telehealth, Epocrates, the Marketplace, and analytics.

athenaOne is fully cloud-based SaaS, running on athenahealth's "athenaNet" infrastructure. There is no on-premise deployment option for athenaOne. The platform is browser-based with mobile apps for patients (athenaPatient on iOS/Android).

### Users & Market

**Who uses it:** Ambulatory/outpatient clinicians and support staff — physicians, nurses, medical assistants, billing staff, practice managers, and patients (via the portal). Supports 60+ specialties including primary care, cardiology, dermatology, pediatrics, orthopedics, OB-GYN, behavioral health, gastroenterology, and many others. Specialty-specific workflow packages (e.g., athenaOne for Women's Health, athenaOne for Urgent Care) launched in 2025.

**Scale:** 170,000+ providers on the network; serves over 20% of the U.S. population; submits 315M+ claims per year. Approximately 6,700–6,900 customer organizations. Per Enlyft, 64% of customers are small organizations (<50 employees), 24% medium, 12% large (>1,000 employees) — but 13% have revenue over $1B, indicating a mix of small practices and large health systems. 95% of customers are in the United States.

**Market position:** Third-largest ambulatory EHR vendor by installation count (5,801 per Definitive Healthcare, October 2025), behind Epic (16,295) and eClinicalWorks (9,966). Rated #1 by KLAS for Independent Physician Practice Suite (3 consecutive years), Ambulatory EHR 11–75 physicians (5 consecutive years), and Practice Management 11–75 physicians (4 consecutive years). In 2026, won first-time recognition for Ambulatory EHR 75+ physicians, signaling enterprise expansion. G2 rating: 3.5/5; Capterra: 3.8/5 across 835+ reviews.

**Notable user feedback (from Capterra/G2/KLAS):** Users praise integrated scheduling/charting/billing workflow, customizable chart templates, reporting capabilities, and first-pass claim resolution rates. Top complaints are customer support responsiveness, implementation difficulties (cost overruns, extended timelines), system performance/freezing, and gaps between sales promises and delivered functionality. Mobile capabilities and telehealth rated below competitors.

### Modules & Functionality

The athenaOne platform consists of three core modules plus ancillary capabilities:

**athenaClinicals (EHR):**
- Clinical documentation — SOAP notes, encounter documentation, specialty-specific templates, voice recognition/dictation
- Computerized Provider Order Entry (CPOE) for medications, labs, and diagnostic imaging
- Electronic prescribing (e-prescribing) including EPCS for controlled substances, with PDMP integration and drug-drug/drug-allergy interaction checking
- Lab and imaging order management with results review
- Problem list, medication list, medication allergy list management
- Patient history (past medical, surgical, family, OB history)
- Vital signs and clinical observations
- Immunization tracking
- Implantable device tracking
- Social, psychological, and behavioral data capture
- Care plans and care team management
- Clinical decision support (via embedded Epocrates — drug reference, interaction checking)
- Quality measure support (MIPS, MACRA, CQMs) — note: CQM certification (c)(1)–(c)(3) is ambulatory-only
- Document management (scanned, faxed, digital documents)
- Referral management (via athenaCoordinator module)
- Population health / care gap tracking
- AI features (2025): ambient-sourced diagnosis suggestions, clinically inferred diagnoses, Chart Assist (GenAI for chart review and summarization), AI document labeling

**athenaCollector (Billing / Practice Management / RCM):**
- Appointment scheduling (daily/weekly/monthly calendar views, patient status tracking, self-scheduling)
- Patient registration and demographics
- Insurance eligibility verification
- Claims submission with 30,000+ automated scrubbing rules (94% first-pass resolution rate)
- Charge entry and medical coding (with AI-assisted coding in 2025)
- Electronic remittance advice (ERA) processing
- Payment posting
- Denial management with root-cause analysis
- Patient billing and collections / statements
- Authorization management
- Provider enrollment
- Days in Accounts Receivable (DAR) tracking
- Copay collection at time of service
- Reporting and analytics
- **Business model note:** athenahealth charges a percentage of client collections rather than licensing fees

**athenaCommunicator (Patient Engagement):**
- Patient portal (web-based + athenaPatient mobile app on iOS/Android)
- Secure HIPAA-compliant messaging between patients and care team
- Appointment reminders ("ReminderCall") — reduces no-show rate by 8%
- Self-scheduling
- Digital intake forms (medical history, consent, demographics that pre-populate charts)
- Online check-in
- Bill pay / payment management
- Population health outreach campaigns (wellness visits, vaccination reminders, cancer screening, chronic disease management)
- Mass messaging capabilities
- Lab result notifications
- Care plan access for patients

**athenaTelehealth:**
- HIPAA-compliant video visits from any browser/device with camera
- Up to 4 participants per session
- Live closed captions and transcripts
- Two-way messaging during visits
- Fully integrated with scheduling and billing workflow
- 3,000+ active customers
- Patients can join from athenaPatient app or web portal

**Epocrates (Clinical Decision Support):**
- Drug reference and dosing information
- Drug-drug and drug-allergy interaction checking
- Clinical decision support at the point of prescribing
- Acquired by athenahealth in 2013; integrated into athenaClinicals

**athenaCoordinator (Care Coordination):**
- Referral management
- Order transmission between providers
- Referral-related denial tracking

**Marketplace (Third-Party Integrations):**
- 500+ vetted third-party applications across 50 digital health capabilities and 60 specialties
- Direct integration with athenaOne via APIs
- Categories include: clinical workflow, patient engagement, billing optimization, AI tools, specialty-specific solutions

**Interoperability / Data Exchange:**
- CommonWell Health Alliance (90% of customers connected; 84,000+ care sites)
- Carequality participation
- TEFCA connectivity
- Direct messaging (h)(1)
- FHIR R4 APIs with SMART on FHIR support
- 800+ REST API endpoints
- HL7 v2 interfaces
- C-CDA document exchange
- Bulk FHIR export
- EHI export
- Public health reporting: immunization registries, syndromic surveillance, cancer registries

**Reporting & Analytics:**
- On-demand SQL access to backend data store via browser-based editor
- BI tool connectivity (connect backend data store to external data warehouses)
- Custom report creation
- Insights dashboards
- Quality measure reporting

### Data & Content

Based on vendor documentation, API specifications, FHIR resource listings from the EHI export documentation, and user reviews, athenaOne stores and manages the following categories of data:

**Clinical Data:** Patient demographics, medical/surgical/family/OB history, problem lists (conditions/diagnoses), medication lists (active/completed/historical), medication allergy lists, allergies and intolerances, encounters/visits, clinical notes and documentation (SOAP notes, encounter summaries), lab orders and results, imaging orders and results, vital signs and clinical observations, immunization records, procedures, care plans, care team assignments, clinical impressions/assessments, goals, family member history, consent records, implantable device information, social/psychological/behavioral data, referral records, prescriptions/e-prescribing records (including controlled substance prescriptions), clinical decision support alerts, scanned/faxed/digital documents, binary attachments, clinical images.

**Billing/Financial Data:** Insurance coverage and eligibility records, claims (submitted/tracked/adjudicated), charges, payments, adjustments, billing statements, collections records, deductibles, patient insurance information, accounts, coding data, ERA/remittance data, denial tracking, authorization records, provider enrollment data. (Sources: athenaCollector features page; FHIR EHI export resource list includes custom resources: Adjustment, BillingStatement, Charge, Claim, Collection, Deductible, Eligibility, PatientInsurance, Payment.)

**Scheduling/Administrative Data:** Appointments, schedules, time slots, patient check-in/check-out records, no-show tracking, provider/practitioner information, organization/location data, account information.

**Patient Engagement Data:** Secure messages between patients and providers, appointment reminder logs, patient portal activity, digital intake form submissions (demographics, medical history, consent), population health campaign/outreach records, telehealth visit records and transcripts.

**Audit/System Data:** Provenance records, audit logs.

The EHI export documentation references FHIR R4 resources in three categories: system resources (Location, Medication, Organization, Practitioner, PractitionerRole), clinical resources (AllergyIntolerance, Binary, CarePlan, CareTeam, ClinicalImpression, Condition, Consent, Device, DiagnosticReport, DocumentReference, Encounter, FamilyMemberHistory, Goal, Immunization, MedicationAdministration, MedicationRequest, MedicationStatement, Observation, Procedure, Provenance, ServiceRequest), and practice management resources (Account, Appointment, Coverage, Patient, RelatedPerson, Schedule, Slot) — plus custom billing resources.

---

## Product: athenaClinicals for Hospitals and Health Systems

CHPL ID: 11613

### What It Is

athenaClinicals for Hospitals and Health Systems is a **separate ONC-certified product** from the ambulatory athenaClinicals, designed for inpatient/hospital settings. It is part of **athenaOne for Hospitals & Health Systems**, which integrates hospital EHR capabilities with the ambulatory athenaOne platform.

Critically, the hospital product was **assembled from multiple acquisitions** and is **not the same codebase** as the ambulatory product:
- **RazorInsights** (acquired January 2015) — cloud-based EHR for rural, critical access, and community hospitals (50 beds and under). Came with ancillary lab, pharmacy, and radiology modules.
- **webOMR from Beth Israel Deaconess Medical Center** (acquired February 2015) — one of the first hospital-built inpatient/outpatient EHR systems, developed over 30 years. Intended to accelerate entry into 100+ bed hospitals.
- **University of Toledo Medical Center co-development** (announced 2016) — partnership to build the inpatient product into a "disruptive alternative to legacy health IT."

The certification criteria are nearly identical to the ambulatory version, with one key difference: the hospital version does **not** include (c)(1)–(c)(3) clinical quality measure criteria. Both versions share the same v25 version number. The hospital version was certified March 21, 2025.

### Users & Market

**Target users:** Inpatient clinicians and support staff — physicians, nurses, hospital administrators, discharge planners, and ancillary staff (lab, pharmacy, radiology).

**Target settings:** Critical access hospitals, community hospitals, small hospitals (originally ~50 beds and under via the RazorInsights heritage, expanding to 100+ beds via the webOMR acquisition). The product integrates with the ambulatory athenaOne platform to provide a unified inpatient + outpatient experience for health systems.

**Market position:** athenahealth is primarily known as an ambulatory vendor. The hospital product is a newer, smaller part of their portfolio. The 2015 acquisitions and 2016 co-development partnership were described as athenahealth's strategy to "accelerate growth in hospital IT" and create a "disruptive alternative to legacy health IT." The product targets hospitals that find Epic or Oracle Health (Cerner) too expensive or complex.

### Modules & Functionality

The hospital product adds inpatient-specific capabilities on top of the athenaOne platform:

- Inpatient clinical documentation / nursing documentation
- Hospital CPOE for medications, laboratory, and diagnostic imaging
- Drug-drug and drug-allergy interaction checks in the inpatient context
- Inpatient medication orders
- Patient floor management
- Discharge planning with automatic generation of discharge instructions and summaries
- Flow of discharge summaries and hospital encounters directly into ambulatory workflows
- Ancillary modules: lab, pharmacy, radiology (from RazorInsights heritage)
- Medical-Surgical department workflows
- Integration with ambulatory athenaClinicals for continuity across settings

The hospital product is offered as part of a comprehensive suite alongside the ambulatory billing, scheduling, and patient engagement modules (athenaCollector, athenaCommunicator).

### Data & Content

The hospital product stores the same categories of clinical data as the ambulatory version (demographics, conditions, medications, allergies, encounters, orders, results, notes, documents, etc.) plus hospital-specific data:

- Inpatient encounter records and nursing documentation
- Inpatient medication administration records
- Discharge summaries and discharge instructions
- Hospital floor/bed management data
- Ancillary department data (lab, pharmacy, radiology)
- Hospital-specific orders and results

The certification criteria overlap significantly with ambulatory, including transitions of care (b)(1)–(b)(3), patient portal access (e)(1), public health reporting (f)(1),(f)(2),(f)(5),(f)(7), FHIR APIs (g)(10), and EHI export (b)(10)–(b)(11). The EHI export documentation (https://docs.athenahealth.com/athenaone-dataexports/) appears to cover both products.

---

## Other Products in the athenahealth Ecosystem

**athenaIDX** — A separate enterprise-scale revenue cycle management product, distinct from athenaCollector. Originally IDX Systems Corporation → GE Centricity Business → rebranded athenaIDX in July 2020. Targets large practices, health systems, hospitals, and billing services. Available on-premise or cloud (unlike athenaOne which is cloud-only). Separately certified and marketed.

**athenaPractice** — A legacy EHR product, formerly GE Centricity EMR/Practice Solution. Came through the Virence Health/GE Healthcare acquisition. Separately ONC-certified with its own Real World Testing plans. Legacy product being maintained alongside athenaOne.

**athenaFlow** — Another legacy product from the GE Centricity family. Separately ONC-certified. Listed together with athenaPractice for ONC cost disclosures.

These products are relevant context because they share the athenahealth brand and infrastructure but are distinct systems with different codebases, certifications, and customer bases. The EHI export obligations for athenaClinicals and athenaClinicals for Hospitals should cover data stored by the athenaOne platform (including athenaCollector and athenaCommunicator data), not just the clinical module in isolation.

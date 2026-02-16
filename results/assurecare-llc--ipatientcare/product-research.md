# AssureCare LLC — Product Research

Researched: 2026-02-16
Developer website: https://ipatientcare.com/

## Overview

AssureCare LLC is a healthcare technology company headquartered in Cincinnati, Ohio, operating since 1993 (originally as CH Mack). The company's flagship product is **MedCompass**, a population health management (PHM) platform serving payors, providers, and pharmacies, supporting over 50 million members. In **2019**, AssureCare acquired **iPatientCare**, a separately developed ambulatory EHR product, to add clinical EHR capabilities to its broader care continuum portfolio. iPatientCare was originally built "by physicians, for physicians" and has served providers across the U.S. and globally for over 20 years.

AssureCare is a mid-size, privately held health IT company — large enough to operate nationally with enterprise PHM contracts, but iPatientCare itself occupies a niche position in the ambulatory EHR market, estimated at below 2% market share (outside the top 10 ambulatory EHR vendors per Definitive Healthcare). The company serves small to mid-size practices, community health centers, rural health clinics, specialty practices, and pharmacies. AssureCare also markets a full Hospital Information Management System (HIMS) through the iPatientCare brand, which appears targeted more at international markets (references to NMC/NABH/NABL/JCI compliance standards suggest India and other global markets).

## Product: iPatientCare

CHPL IDs: 8970 (v18.0, certified 2017-12-01), 11103 (v22.5, certified 2022-12-21), 11286 (v23.0, certified 2023-05-22)

### What It Is

iPatientCare is an **integrated ambulatory EHR, practice management, and billing platform** designed for outpatient physician practices. It is available as both cloud-hosted and on-premise. The product is the entirety of what is ONC-certified — it is not a module of something larger (though the parent company AssureCare has a separate MedCompass PHM platform that can integrate with it). The certification is broad, covering 35+ ONC criteria including clinical data capture (a)(1)–(a)(5), (a)(12), (a)(14), (a)(15); transitions of care (b)(1)–(b)(3); patient portal (e)(1); e-prescribing; public health reporting (f)(1)–(f)(4) in earlier versions; FHIR APIs (g)(7)–(g)(10); and direct messaging (h)(1). The SED intended users are described as "Physicians and Mid-level providers."

### Users & Market

**Target users:** Physicians, mid-level providers (NPs, PAs), front office/scheduling staff, billing staff, clinical support staff, pharmacists and pharmacy technicians. Patients access a patient portal and mobile app.

**Clinical settings served (per vendor website):**
- Primary care practices of all sizes
- Specialty practices: Mental & Behavioral Health, Cardiology, Pain Management, Orthopedics, Pediatrics, Internal Medicine, Women's Health
- Community Health Centers (CHCs) and Rural Health Clinics (RHCs)
- Pharmacies (using the EHR to document billable patient encounters)

**Market position:** iPatientCare is a small vendor in the ambulatory EHR market, outside the top 10 by install count. Exact customer counts are not publicly disclosed. Reviews on Capterra (4.4/5, 66 reviews) and G2 (3.8/5, 2 reviews) suggest a modest but satisfied user base, primarily small and mid-size practices. Users describe it as "great for charting," "easy to use," and "gets the job done" but "not innovative" and "nothing fancy." Multiple reviewers praise the integrated billing and customer support. Some note performance can be sluggish and that it may not be robust enough for large, complex operations.

**Geographic reach:** U.S. and global (international HIMS product appears targeted at India/Middle East based on NMC integration and NABH/NABL/JCI compliance references).

### Modules & Functionality

Based on vendor website, product pages, and third-party review sites, iPatientCare includes the following integrated modules:

**Electronic Health Record (EHR):**
- Clinical charting with customizable, specialty-specific templates
- Problem lists, medication lists, allergy lists
- Patient demographics and history
- Family health history
- Social, psychological, and behavioral data
- Implantable device tracking (certified for (a)(14))
- Clinical decision support (drug-drug and drug-allergy interaction checks)
- Growth charts (for pediatrics), vital signs, clinical notes
- Handwriting and voice recognition support for documentation
- Clinical information reconciliation (problems, meds, allergies — certified (b)(2))

**E-Prescribing:**
- Electronic prescribing including EPCS (electronic prescribing of controlled substances)
- Drug reference database integration
- Drug-drug and drug-allergy checks
- Integrated with Surescripts (implied by pharmacy integration and EPCS capability)

**Lab & Imaging Orders:**
- Electronic lab ordering and results retrieval directly into patient chart
- Integration with lab information systems
- Integration with diagnostic imaging systems (radiology)
- Integration with in-office clinical devices

**Practice Management / Front Office:**
- Patient registration
- Multi-location and multi-provider appointment scheduling
- Wait list and recall list management
- Insurance eligibility verification (real-time and advance)
- Referral management (submission and tracking)
- Automated appointment reminders (SMS)
- Demographic and insurance information management

**Billing & Revenue Cycle Management:**
- Integrated billing system for claim production
- Claims entry, editing, and resubmission
- Electronic claims submission to CMS and commercial payers
- Integrated clearinghouse for electronic claims processing
- Payment posting (electronic remittance)
- Accounts receivable management and follow-up
- Denial management and appeals
- Patient fee estimation
- Payer credentialing and enrollment
- Robust financial dashboards and billing reports
- Optional full RCM outsourcing service (AssureCare team manages billing on behalf of practice)

**Patient Portal & Engagement:**
- Patient portal (web-based and mobile app, Apple & Android)
- View health records, lab results, prescriptions, visit summaries
- Appointment scheduling/requests
- Prescription refill requests
- Secure messaging with providers
- Demographics updates by patients
- Educational materials
- Automated patient reminders and messaging

**Telehealth:**
- Integrated audio, video, and chat functionality
- Built into EHR workflow (no separate platform needed)

**Quality Reporting & Compliance:**
- Meaningful Use certified (63 eCQMs)
- MIPS and MACRA eCQM support and reporting
- Real-time quality dashboards and MIPS financial calculator
- ICD-10 compliant
- HIPAA compliant
- Attestation management (self-service or managed by iPatientCare team)

**Interoperability:**
- Health Information Exchange (HIE) membership
- Integration with state immunization registries
- Integration with pharmacies, labs, imaging systems
- Direct messaging (h)(1)
- FHIR API support (g)(7)–(g)(10)
- C-CDA document exchange for transitions of care
- Public health reporting: immunization registries (f)(1)), syndromic surveillance (f)(2) in v18), cancer registries (f)(3) in v18), electronic lab reporting (f)(4) in v18; later versions only f(1))

**Document Management:**
- Scanned records, referrals, consent forms, clinical notes storage
- Document annotation and search
- Document sharing via patient portal

**Reporting & Analytics:**
- Customizable dashboards for performance metrics
- Financial reports (claims status, payments, AR, revenue)
- Clinical and compliance reporting

### Data & Content

Based on the features described above, iPatientCare stores the following categories of data:

- **Clinical records:** Patient demographics, problem lists, medication lists, allergy lists, vital signs, clinical notes/encounter documentation, family health history, social/psychological/behavioral data, implantable device lists, growth charts
- **Orders & results:** E-prescriptions (including controlled substances), lab orders and results, imaging orders and reports
- **Documents:** Scanned documents, referral letters, consent forms, clinical attachments
- **Scheduling data:** Appointments, wait lists, recall lists, provider schedules
- **Billing & financial data:** Insurance information, eligibility verification results, claims (submitted and tracked), payment postings, electronic remittances, denials, appeals, patient balances, fee schedules
- **Patient portal data:** Secure messages between patients and providers, prescription refill requests, appointment requests, patient-submitted demographic updates
- **Telehealth data:** Virtual visit records (integrated into encounter documentation)
- **Quality measure data:** eCQM calculations, MIPS scores, attestation data
- **Public health submissions:** Immunization registry submissions, syndromic surveillance data (v18), cancer registry data (v18), electronic lab reports (v18)
- **Interoperability data:** C-CDA documents (sent/received), Direct messages, care plans
- **Audit data:** Access logs, user authentication records (certified for multiple (d) criteria)

**What's unclear or absent from vendor materials:**
- The HIMS (Hospital Information Management System) product on the website includes many additional modules (blood bank, OR management, CSSD, diet/kitchen, linen/laundry, asset management, HR, etc.) but this appears to be a separate product line, likely not part of the ONC-certified ambulatory iPatientCare product. The ONC certification is clearly scoped to ambulatory settings ("Physicians and Mid-level providers").
- No mention of behavioral health-specific data structures (e.g., treatment plans, group therapy notes) beyond listing "Mental & Behavioral Health" as a served specialty — it's unclear how deep the behavioral health functionality goes vs. generic templates.
- The relationship between iPatientCare's data and AssureCare's MedCompass PHM platform is not well documented publicly — data may flow between them for care management, but specifics are unclear.
- Exact prescription formulary or drug database vendor is not stated (likely Surescripts/First Databank but not confirmed).

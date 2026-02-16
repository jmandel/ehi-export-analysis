# MedPharm Services LLC / Meditab — Product Research

Researched: 2026-02-15
Developer website: https://www.meditab.com

## Overview

MedPharm Services LLC is an affiliate of Meditab Software, Inc., a family-founded EHR company established in 1998 in Sacramento, CA by the Patel family. The origin story involves the family's frustration with inadequate software at their own pharmacy. MedPharm Services LLC was created by co-founder Kalpesh Patel and is the entity listed on ONC CHPL as the developer of IMS. Meditab itself has approximately 600 employees across offices in 10 countries (US, India, Philippines, UK, Australia, Canada, and others).

Meditab is a small-to-mid-tier ambulatory EHR vendor. They claim 41,000 healthcare professionals and 1,600+ clinics using IMS. Per Enlyft, their market share is approximately 0.01% in healthcare IT. They are bootstrapped (no VC or PE funding). The company is primarily known for deep specialty customization across 40+ medical specialties, and consistently wins Black Book Research awards in niche specialty categories. They also make a separate pharmacy software product called IPS (Intelligent Pharmacy Software).

In September 2024, Meditab and affiliated company DrCatalyst jointly acquired Fox Meadows Software, a practice software and RCM vendor founded in 1994. MICA Information Systems (founded 1979) is their top Value-Added Reseller in the US.

## Product: Intelligent Medical Software (IMS)

CHPL ID: 9739

### What It Is

IMS is a **Complete EHR** (classified as such on ONC certification) for ambulatory/outpatient settings. It is an all-in-one practice automation system encompassing EHR, practice management, medical billing/RCM, e-prescribing, patient portal, telemedicine, and reporting — all within a single platform and single database. The certified product is the whole IMS platform, not a component of something larger.

The product is certified for 50 ONC criteria spanning clinical data (a), care coordination (b), clinical quality measures (c), security (d), patient access (e), public health reporting (f), API/FHIR (g), and direct messaging (h). This is a broad certification indicating the product handles the full range of ambulatory clinical, billing, and interoperability functions.

IMS supports both cloud/SaaS and on-premise deployment. It runs on Windows, Mac, and Linux. The underlying database is Sybase SQL Anywhere. Average implementation time is reported as 22 days.

### Users & Market

**Target users:** Physicians, nurses, billing staff, practice managers, and patients (via portal). The SED intended user description lists "General Medicine, Allergy, Pediatrics, Fertility, Internal Medicine."

**Settings:** Primarily small-to-medium ambulatory practices (2-5 physicians is described as a sweet spot) and FQHCs. Per Enlyft, 54% of users are in practices with fewer than 50 employees, and 92% are in the United States. Not a hospital/inpatient system.

**Specialties:** 40+ specialties with dedicated specialty-specific modules and templates. Key specialties (per Black Book awards and product pages): Allergy & Immunology, Cardiology, Chiropractic, Cosmetic (CosmetiSuite), Dental, Dermatology, Endocrinology, ENT, Family Practice, Fertility (FertilityEHR), FQHC, Gastroenterology, General Surgery, Internal Medicine, Mental Health/Psychiatry, Nephrology, Neurology, OB/GYN, Oncology, Ophthalmology, Optometry, Orthopedics, Pain Management, Pediatrics, Plastic Surgery, Podiatry, Primary Care, Pulmonology, Radiology, Rheumatology, Sleep Medicine, Urgent Care, Urology, and Vascular Surgery.

**Notable deployments:**
- Children's Medical Centers of Fresno (reported 28% revenue increase)
- McKinney Allergy and Asthma Center (reported 80% efficiency boost)
- Safadi and Associates Inc. (reported 30% patient visit increase)
- An FQHC user reported using IMS across multiple service lines (podiatry, medical, dental, optometry, behavioral health, obstetrics) with a single login.

**Pricing:** Starting at approximately $150-199/month per user.

### Modules & Functionality

Based on vendor website, product pages, mandatory disclosures, and reviews:

**EHR / Clinical:**
- Patient charting with specialty-specific modules and templates for 40+ specialties
- Clinical Decision Support ("CareProtocol")
- Clinical flow charts
- Problem lists, medication lists, medication allergy lists
- Vital signs tracking
- Health maintenance schedules
- Chronic care management
- Referral and authorization management and tracking
- Patient education (built-in, specialty-categorized, via Merative integration)
- E&M Coding Assistance
- Data entry via tablet, voice, stylus, mouse, or keyboard

**E-Prescribing:**
- Full e-prescribing via Surescripts integration
- EPCS (Electronic Prescribing of Controlled Substances) via Exostar identity
- IMS Hub-Rx for prescription flow management
- CoverMyMeds integration for prior authorizations
- Drug interaction checking via First Databank (FDB)
- Drug reference via MicroMedex and PDR

**Lab & Diagnostics:**
- Electronic lab ordering and results (bi-directional)
- 90+ lab interfaces including Labcorp, Quest Diagnostics, BioReference Health, Natera, Clinical Pathology Laboratories, PathGroup, and many regional/specialty labs
- Medical device integrations: Clinii, HIMSA (hearing), Morgan Scientific, ndd (pulmonary function)

**Billing & Revenue Cycle Management:**
- Integrated billing (not a separate product)
- Claims creation, scrubbing, submission, denial/rejection management
- Clearinghouse integration via Availity and Data Dimensions
- Automatic superbill creation
- Insurance posting and payment posting
- Managed care claim write-offs
- Electronic claim attachments
- Patient statements via BillFlash and POS
- Payment processing via Global Payments Integrated and Exact Payments
- Monthly billing reports
- ICD-10 compliant

**Patient Portal & Engagement:**
- IMS Care: combined patient portal and mobile app (iOS and Android)
- Patient capabilities: manage payments, request medication refills, schedule appointments, upload documents, view records
- Secure messaging
- OTP login, "portless" access (enhanced security)
- IMS InTouch: automated SMS/email messaging for patient reminders and alerts
- IMS OnArrival: patient self-check-in kiosk system
- Televisit: built-in HIPAA-compliant telemedicine with screen sharing
- Additional patient engagement integrations: Artera, Brevium, EngagedMD, Solutionreach

**Scheduling & Practice Management:**
- Patient Scheduler: centralized appointment booking
- My Tasks: daily task reminders and workflow management
- EMO (Electronic Medical Office): office and staff management suite
- Practice analytics and KPI dashboards
- Lead management
- IVR (Interactive Voice Response) via TelTech

**Communication & Documents:**
- Surescripts Clinical Direct Messaging
- IMS Chat for internal communication
- FaxCloud for fax communications
- Document management with imaging capabilities
- Direct mail via Lob

**Reporting & Quality:**
- MIPS/MACRA quality reporting
- HEDIS reporting (NCQA compliant)
- UDS reporting (for FQHCs)
- HCC (Hierarchical Condition Categories) coding
- Clinical Quality Measures (CMS62, CMS68, CMS74, CMS75, CMS77, CMS124, CMS126, CMS146, CMS148)
- Population health management
- Governance reporting via DHIT and FigMD

**Public Health Reporting:**
- Immunization registry submissions — bi-directional with AZ (ASIIS), CA (CAIR/RIDE), FL (SHOTS), GA (GRITS), TX (IMMTRAC); uni-directional with AL, AR, CA, FL, IL, IN, MA, MI, NC, ND, NJ, NY, UT, WV
- Syndromic surveillance reporting
- Cancer registry reporting

**Interoperability & APIs:**
- FHIR R4 APIs (including Bulk Data export)
- HL7 v2 interfaces
- HL7 C-CDA XML documents
- Health Information Exchange (HIE)
- Surescripts e-prescribing and clinical messaging
- Bamboo Health (prescription drug monitoring)
- Zocdoc, Klara, Luma, Phreesia integrations

**Mobile:**
- IMSGo: mobile EHR app for providers (iOS/Android, additional per-provider fee)
- IMS Care: mobile patient app

**AI:**
- Nabla integration for AI clinical documentation

### Data & Content

Based on the evidence gathered, IMS stores and manages the following data:

**Clinical records:** Patient demographics, medical history, problem lists, medication lists, allergy lists, vital signs, clinical notes (specialty-specific templates for 40+ specialties), clinical flow charts, health maintenance records, chronic care management records, referral and authorization records, patient education delivery records.

**Orders and results:** E-prescriptions (including controlled substances), lab orders and results (bi-directional with 90+ labs), diagnostic orders, prior authorizations.

**Billing and financial data:** Claims (creation through denial management), superbills, patient statements, insurance information, payment records (credit card, online, phone, in-person), managed care write-offs, revenue cycle management data, fee schedules.

**Patient engagement data:** Patient portal activity, secure messages, medication refill requests, appointment scheduling requests, uploaded documents, telemedicine/televisit session records, SMS/email communication logs (InTouch), patient check-in records (OnArrival kiosk).

**Administrative data:** Scheduling and appointment records, staff management data (EMO), practice analytics, lead management data, fax communications, internal chat messages, task management records.

**Quality and reporting data:** MIPS/MACRA quality measure data, HEDIS reports, UDS reports (FQHCs), HCC coding data, CQM data, population health data.

**Public health data:** Immunization records (submitted to state registries), syndromic surveillance data, cancer registry data.

**Interoperability artifacts:** C-CDA documents, FHIR resources, Direct messages, HIE exchange records.

**Mandatory disclosures confirm additional-cost modules** (which are part of the product but require separate fees): Patient portal (Careportal), HIE, e-prescribing, patient education, InTouch messaging, patient API access, immunization interface, syndromic surveillance interface, cancer registry interface, FHIR API, lab integration, device integration, IMSGo mobile app, and custom features/integrations/reports. These are all IMS modules, not third-party products.

**Database:** Sybase SQL Anywhere — a single database for both EHR and practice management, meaning all clinical and administrative data resides in one system.

**User reviews confirm** the product stores billing data (users describe it as "a biller's dream"), scheduling data, and multi-specialty clinical data (an FQHC user described using it across podiatry, medical, dental, optometry, behavioral health, and obstetrics in a single system).

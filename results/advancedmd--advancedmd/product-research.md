# AdvancedMD — Product Research

Researched: 2026-02-16
Developer website: https://www.advancedmd.com/

## Overview

AdvancedMD is a cloud-based medical office software company headquartered in South Jordan, Utah. Founded in 1999, it provides an integrated platform combining electronic health records (EHR), practice management (PM), medical billing, patient engagement, and revenue cycle management (RCM) for ambulatory physician practices. The company targets independent and small-to-mid-sized physician practices across a broad range of specialties.

AdvancedMD has changed ownership multiple times: acquired by Marlin Equity Partners in 2015, then by Global Payments in 2018 for $700 million, and most recently by Francisco Partners in late 2024 for $1.125 billion. As of early 2025, AdvancedMD operates as a standalone company under Francisco Partners, with Amanda Sharp as CEO. The company reported record-breaking revenue and customer growth in 2024, with approximately $250 million in revenue.

The customer base has grown substantially: from 17,500 practitioners in 2015 to over 65,000 practitioners across 14,000 practices and 900 independent billing service companies as of 2025. AdvancedMD positions itself as an all-in-one cloud platform for ambulatory practices, competing with vendors like athenahealth, eClinicalWorks, and NextGen in the ambulatory EHR/PM market.

## Product: AdvancedMD

CHPL IDs: 11732

### What It Is

AdvancedMD is a comprehensive, cloud-based ambulatory EHR and practice management platform. It is the vendor's flagship product — a unified solution that bundles clinical, financial, and patient engagement tools into a single cloud-hosted system. The CHPL-certified product "AdvancedMD" (v25) carries a very broad set of certifications — 32 criteria spanning clinical data management ((a)(1)–(a)(5), (a)(12), (a)(14)), transitions of care ((b)(1)–(b)(3), (b)(10), (b)(11)), clinical quality measures ((c)(1)–(c)(4)), patient portal/VDT ((e)(1), (e)(3)), public health reporting ((f)(1), (f)(5)), and FHIR API access ((g)(7), (g)(9), (g)(10)). This indicates a fully-featured EHR with clinical documentation, e-prescribing, care coordination, patient access, quality reporting, and interoperability capabilities.

The certified module appears to be the core EHR component, but the product as a whole — the thing practices buy and use daily — encompasses significantly more than clinical documentation. The platform includes integrated billing, scheduling, revenue cycle management, patient engagement, and analytics. The SED intended user description is "Ambulatory clinical and practice staff," confirming it serves both clinical and administrative users.

### Users & Market

AdvancedMD serves independent ambulatory practices of varying sizes, from solo providers to multi-location groups. It is recommended particularly for larger practices and multi-location operations requiring robust automation (per third-party review sites). The platform supports a broad range of medical specialties including:

- Primary care / Family medicine / Internal medicine
- Cardiology, Dermatology, Gastroenterology, Orthopedics
- Mental/Behavioral health (a special edition was launched in 2017)
- Physical therapy (special edition launched in 2017)
- Pediatrics (with Bright Futures AAP-partnered content)
- Ophthalmology, Neurology, Endocrinology, Nephrology, Urology
- Allergy & Immunology, Anesthesiology, Chiropractic, Addiction Medicine

There are 65,000+ practitioners across 14,000+ practices using AdvancedMD. The system also serves 900+ independent billing service companies who use the billing/RCM features on behalf of practices.

AdvancedMD also offers a streamlined sub-product called **AdvancedMD NOW**, which is described as "cloud software built for small mental health practices with teletherapy, billing automation and intuitive practice workflows." This appears to be a simplified, specialty-specific packaging of the core platform.

### Modules & Functionality

Based on vendor website materials, search results, and third-party review sites, AdvancedMD's platform includes the following major modules and capabilities:

**Electronic Health Records (EHR)**
- Clinical charting and documentation with customizable, specialty-specific templates
- Problem lists, medication lists, allergy lists
- Patient Cards — customizable clinical summaries showing medications, allergies, problems, and encounter history
- Clinical Notes AutoSave (2025 Winter Release) — real-time automatic saving of notes
- Clinical decision support alerts
- Order entry (labs, imaging, referrals)
- Custom medical plans based on patient age, diagnosis, and lab results
- Alerts for appointment recalls, lab orders, prescription refills
- Task Donut Dashboard — real-time workflow overview with prioritized tasks

**E-Prescribing**
- Electronic prescription creation and transmission directly from EHR
- EPCS (Electronic Prescribing for Controlled Substances) — Schedule II-IV narcotics
- Drug interaction checking
- Prescription tracking

**Telemedicine / Telehealth**
- Integrated video visits (launched 2016 as part of AdvancedPatient suite)
- Charting and billing within the same telehealth session
- Teletherapy for mental health practices (AdvancedMD NOW)

**Practice Management & Scheduling**
- Appointment scheduling with calendar management
- Patient self-scheduling via online portal
- Appointment reminders
- Patient demographics and registration
- Insurance eligibility verification (eEligibility) — batch or on-demand
- AI-assisted extraction of insurance data from uploaded card images
- Patient merge functionality (combining duplicate records across PM and EHR)

**Medical Billing & Revenue Cycle Management**
- Charge capture (real-time)
- ClaimInspector — automated claims scrubbing against CCI, HIPAA, LCD coding rules
- Electronic claims submission
- Electronic remittance advice (ERA) processing
- Denial management with integrated A/R worklists
- Patient billing and statement generation
- Online patient payment processing (credit card via portal)
- Financial analytics and reporting dashboards (MTD, YTD, period comparisons)
- Outsourced RCM/billing services option (AdvancedBiller marketplace with third-party billing companies)

**Patient Engagement (AdvancedPatient)**
- Patient portal — view medical records, send messages, request appointments, request prescription renewals
- Secure online messaging between patients and providers
- Online bill pay
- Reputation management tools
- Patient satisfaction/engagement workflows

**Document Management**
- Document scanning module — scan and import documents, photos, insurance cards, consent forms
- TWAIN-compatible scanning (webcams, traditional scanners)
- Integrated fax (inbound and outbound) with digital document management
- Unsolicited claim attachments — send clinical notes, images, labs, diagnostics with claims
- E-signature capabilities
- Chart file management

**Reporting & Analytics**
- Financial reporting and analytics dashboards
- Population health reporting for MIPS (2025 Winter Release)
- Custom and standard report generation
- KPI tracking, billing trends, A/R monitoring, payer data analysis

**Public Health Reporting**
- Certified for immunization registry reporting ((f)(1))
- Certified for cancer case reporting ((f)(5))

**Interoperability & Integrations**
- FHIR API access ((g)(7), (g)(9), (g)(10))
- Transitions of care / C-CDA exchange ((b)(1)–(b)(3))
- Direct messaging ((b)(11), (h)(1))
- Third-party integrations: Swell, HIPAA One, Vital Interaction, Allegiance Group, PatientTrak, Healthjump
- Surescripts integration (implied by e-prescribing)
- Clearinghouse integration for claims

### Data & Content

Based on the features described across vendor materials and review sites, AdvancedMD stores and manages the following categories of data:

**Clinical data**: Patient charts, clinical notes, encounter documentation, problem lists, medication lists, allergy lists, vital signs, immunization records, lab orders and results, imaging orders, referrals, clinical decision support alerts, custom medical plans. Specialty-specific template content (e.g., Bright Futures pediatric templates from AAP partnership).

**Prescription data**: E-prescribing records including controlled substance prescriptions (Schedule II-IV), drug interaction data, prescription history, pharmacy information, refill requests.

**Scheduling data**: Appointment schedules, patient self-scheduling records, appointment reminders, recall lists, provider calendars.

**Billing and financial data**: Charges, claims (submitted and history), ERA/remittance data, denial records, A/R data, patient balances, payment records (including online credit card payments), insurance eligibility verification results, insurance card images (AI-extracted data), payer information, financial reports.

**Patient demographics and registration**: Patient demographics, insurance information, contact details. Patient merge history.

**Documents and images**: Scanned documents (consent forms, insurance cards, photos, etc.), faxes (inbound and outbound), clinical note attachments, claim attachments, chart files.

**Patient portal/engagement data**: Portal messages between patients and providers, prescription renewal requests via portal, appointment requests, patient-accessible medical records, online bill pay records.

**Telehealth data**: Virtual visit session records, associated charting and billing.

**Public health reporting data**: Immunization registry submissions, cancer case reports.

**Population health and quality data**: MIPS reporting data, quality measure calculations, population health metrics.

**Administrative and system data**: User accounts, audit logs, task assignments (Task Donut), workflow configurations, template libraries, report configurations.

---

## Product: AdvancedMD Mobile

CHPL IDs: 11734

### What It Is

AdvancedMD Mobile (v8) is a companion mobile application for the AdvancedMD platform. It allows clinicians to access and manage their electronic health records from mobile devices while away from the office. It is not a standalone product — it extends the core AdvancedMD EHR to mobile devices (iOS/Android), providing on-the-go access to patient charts and clinical workflows.

The mobile app has a more limited set of certifications — 20 criteria focused on core clinical functions ((a)(1)–(a)(5), (a)(12)), EHI export ((b)(10)), electronic prescribing ((b)(3)), and security/infrastructure criteria ((d) and (g) series). Notably absent compared to the main product: transitions of care ((b)(1)–(b)(2), (b)(11)), patient portal ((e)(1), (e)(3)), public health reporting ((f)(1), (f)(5)), FHIR APIs ((g)(7), (g)(9), (g)(10)), and clinical quality measures ((c)(1)–(c)(4)). This is consistent with a mobile companion app focused on clinical documentation and chart access rather than full administrative functionality.

### Users & Market

The same ambulatory physicians and clinicians who use the main AdvancedMD EHR. The mobile app targets providers who:
- Are on call and need remote access to patient records
- Work across multiple locations
- Need to review and document while away from their primary workstation

### Modules & Functionality

Based on the vendor's mobile app page and the certified criteria, the mobile app provides:
- Patient chart access and review
- Clinical documentation and charting (CPOE, demographics, problem lists, medications, allergies — per (a)(1)–(a)(5))
- E-prescribing including controlled substances ((b)(3))
- Clinical decision support ((a)(12))
- EHI data export ((b)(10))

The mobile app connects to the same backend as the main AdvancedMD platform, so data entered or viewed on mobile is the same data available on the desktop web application.

### Data & Content

The mobile app accesses the same underlying data store as the main AdvancedMD product. It does not maintain a separate data repository. All clinical data created or accessed through the mobile app (patient charts, notes, prescriptions, orders) is stored in the central AdvancedMD cloud platform.

# MEDHOST — Product Research

Researched: 2026-02-16
Developer website: https://www.medhost.com

## Overview

MEDHOST (legally MEDHOST Cloud Services, Inc.) is a healthcare IT company founded in 1984 and headquartered in Franklin, Tennessee. The company provides clinical and financial software solutions primarily for community and rural hospitals across the United States. In January 2024, MEDHOST was acquired by Harris Computer Corporation, a subsidiary of Constellation Software, and continues to operate as a standalone business. The company employs roughly 600–650 staff and reports annual revenues of approximately $126 million.

MEDHOST serves several hundred community and rural hospitals nationwide. Their core value proposition is providing a fully integrated EHR and financial management platform tailored to smaller facilities that don't need (or can't afford) enterprise-scale systems like Epic or Cerner. The company is a partner of the National Rural Health Association (NRHA). Customer testimonials on the website come from facilities like Mt. San Rafael Hospital, Claiborne Memorial Medical Center, Springhill Medical Center, Mille Lacs Health System, and Boone Memorial Hospital — all community/rural hospitals.

## Product: MEDHOST Enterprise - Clinicals

CHPL IDs: 11678

### What It Is

MEDHOST Enterprise - Clinicals is the clinical component of MEDHOST's integrated Enterprise EHR/HIS (Health Information System). It is designed as a comprehensive inpatient clinical information system for hospital settings. The certified module covers clinical functionality; there is a separate certified product — "MEDHOST Enterprise - Financials" (CHPL# 15.04.04.2788.MEDH.FI.09.0.250606) — for the financial/revenue cycle side. Together, these two products plus EDIS (Emergency Department Information System, separately certified) and the YourCare suite form the complete MEDHOST Enterprise platform.

The product has broad ONC certification covering clinical data (a)(1)–(a)(5), (a)(12), (a)(14), transitions of care (b)(1)–(b)(3), EHI export (b)(10)–(b)(11), patient request for data (e)(3), public health reporting (f)(1)–(f)(3), (f)(5), and FHIR APIs (g)(7), (g)(9)–(g)(10). Additional software dependencies listed in the certification include Wolters Kluwer Health Language Data Interoperability Solution, NLM AccessGUDI API, Secure Exchange Services, MEDHOST Cloud Services, Medispan Drug Formulary, Microsoft SQL Server, MEDHOST Cures 2023, and an Interoperability Package.

### Users & Market

**Primary users:** Physicians, nurses, pharmacists, anesthesiologists, perioperative staff, HIM coders, and other clinical staff at community and rural hospitals. The product targets inpatient settings — general acute care hospitals, critical access hospitals, and rural emergency hospitals.

**Market position:** MEDHOST is a mid-tier vendor competing below Epic/Oracle Health but serving a loyal niche of community hospitals. Reviews are mixed — Capterra rates EDIS at 4.1/5 (12 reviews), G2 gives MEDHOST 3.5/5 (6 reviews), and TrustRadius 6.1/10 (2 reviews). Users praise the ED functionality, ease of use in patient tracking, and strong customer support. Criticisms include an occasionally dated-feeling UI, loading delays, and limited template customization compared to enterprise products.

**Notable deployments:** Mt. San Rafael Hospital, Claiborne Memorial Medical Center, Springhill Medical Center, Mille Lacs Health System, Boone Memorial Hospital.

### Modules & Functionality

Based on vendor website descriptions, the MEDHOST Enterprise - Clinicals product encompasses the following modules and features:

**Clinical Suite:**
- **EDIS (Emergency Department Information System):** Separately certified but deeply integrated. Includes patient tracking, CPOE, nurse charting, physician documentation, Toolkit (admin utility), comprehensive reporting, graphical floor plans, touch-screen design, risk alerts, barcode scanning for medication administration, closed-loop medicine administration, automatic charge capture, wait time posting, and ED Online Check-In (QR code self-check-in). (Source: medhost.com/edis-emergency-department/)
- **Perioperative Experience:** Full surgical workflow management from initial consult through scheduling, nurse charting, and post-surgery discharge. Digital displays replace whiteboards for patient tracking and surgical resource management. (Source: medhost.com/ehr/clinical-suite/perioperative-experience/)
- **Anesthesia Experience:** Medication documentation, vitals graphing, anesthesia charting, and orders within the perioperative workflow. (Source: medhost.com/ehr/clinical-suite/medhost-anesthesia-experience/)
- **Clinician Experience:** Patient Care Documentation (multi-disciplinary clinical data management), eMAR (electronic medication administration record with Five Rights enforcement and real-time charge capture), and Care Plan modules. Pre-built and customizable designs. (Source: medhost.com/ehr/clinical-suite/clinical-solutions/)
- **Physician Experience:** Documentation viewing across the continuum of care. CPOE for medications, labs, and radiology orders. (Source: medhost.com/ehr/clinical-suite/physician-experience/)
- **Pharmacy Experience:** Prioritized unverified order review, quick access to patient charts, streamlined medication therapy management. (Source: medhost.com/ehr/clinical-suite/pharmacy-experience/)
- **Laboratory, Radiology, and Pharmacy Information Systems:** Integrated ancillary systems for diagnostic turnaround, order processing, and clinical information accessibility. (Source: medhost.com/ehr/clinical-suite/clinical-solutions/)
- **Documentation Management System (DMS):** Central control and routing hub for documentation. Manages security rules, user access, audit logs, automatic transmission, search, and extraction of documents. (Source: medhost.com/ehr/clinical-suite/clinical-solutions/)

**Interoperability:**
- CCDA 2.1 exchange, Direct Messaging, Automated Transition of Care, Query and Retrieve
- Surescripts integration (e-prescribing)
- FHIR APIs and patient/provider portals
- Public health reporting (immunizations, syndromic surveillance, electronic case reporting, cancer registry)
- Managed Integration Services (cloud-based interfaces)
- Clinical Gateway and YourCare Continuum for care coordination between clinics and hospitals

**YourCare / Continuity of Care Suite (MEDHOST Cloud Services):**
- **YourCare Continuum:** Care coordination portal — scheduling follow-up appointments, sharing electronic orders and results across platforms, referral intake via YourCareReferral. (Source: medhost.com/yourcare/yourcare-continuum-suite/)
- **YourCare Management:** Condition management (e.g., diabetic care) with patient-clinician communication, education, and virtual support groups. (Source: medhost.com/yourcare/yourcare-continuum-suite/yourcare-management/)
- **YourCare Everywhere:** Patient engagement app — wellness dashboard, health content, device consolidation, mobile app. (Source: medhost.com/yourcare/patient-engagement/)
- **Price Transparency Solution:** Web-based search for shoppable procedure prices. (Source: medhost.com/yourcare/patient-engagement/price-transparency/)

**Mobile Solutions:** Clinical mobile apps for medication administration, patient engagement, and clinical workflows away from workstations. (Source: medhost.com/ehr/mobile-solutions/)

### Data & Content

Based on the modules and features described above, the MEDHOST Enterprise - Clinicals product manages the following types of data:

**Clinical data (directly evidenced by vendor materials):**
- Patient demographics and registration data (patient tracking, EDIS)
- Clinical documentation — physician notes, nurse charting, care plans, multi-disciplinary documentation
- Medication data — orders, pharmacy records, medication administration records (eMAR), e-prescribing via Surescripts
- Lab orders and results (Lab Information System, CPOE)
- Radiology orders and results (Radiology Information System, CPOE)
- Vital signs and clinical assessments
- Anesthesia records — vitals graphing, medication documentation, anesthesia charting
- Perioperative/surgical records — scheduling, pre-op, intra-op, post-op documentation, post-surgery surveys
- Emergency department records — triage data, patient tracking, ED visit documentation, risk alerts
- Allergy and problem list data (implied by (a)(1)–(a)(5) certification criteria)
- Clinical decision support rules and alerts
- Care coordination data — referrals, follow-up scheduling, transitions of care (CCD/CCDA documents)

**Administrative/operational data:**
- Document management (DMS) — routing, access controls, audit logs
- Charge capture data (automatic in EDIS and eMAR)
- Scheduling data (perioperative scheduling, YourCare Continuum scheduling)
- Wait time data (EDIS posts to website)

**Patient engagement data:**
- Patient portal messages and interactions (YourCare Everywhere)
- Condition management data (YourCare Management — e.g., diabetic care records, education, virtual support groups)
- Patient self-check-in data (ED Online Check-In)

**Public health reporting data:**
- Immunization registry submissions (f)(1)
- Syndromic surveillance data (f)(2)
- Electronic case reporting (f)(3)
- Cancer registry data (f)(5)

**Note on financial data:** The financial/revenue cycle functionality — including billing, claims, accounts payable, general ledger, materials management, time and attendance, contract management, HIM coding — is part of the separately certified "MEDHOST Enterprise - Financials" product. While it integrates with Clinicals as part of the same Enterprise platform, it has its own CHPL certification. The Clinicals module does capture charge data (automatic charge capture in EDIS and eMAR), which flows to the Financials system.

**Architecture note:** The system runs on Microsoft SQL Server and can be cloud-hosted or on-premise. MEDHOST offers hosting and managed services.

---

## Research Gaps

- Exact customer count is not publicly disclosed; "several hundred" community/rural hospitals is the best available estimate.
- The vendor website is marketing-oriented and does not provide detailed technical documentation about data models or storage.
- The boundary between what data lives in Clinicals vs. Financials vs. EDIS (which has separate certification) is not precisely delineated — they are all part of the same integrated Enterprise platform.
- Limited information on whether imaging/PACS data is stored natively or only interfaced.
- The MEDHOST Cloud Services / YourCare products appear to be cloud-based extensions; it's unclear whether their data is in the same database as the core Enterprise system or separate.

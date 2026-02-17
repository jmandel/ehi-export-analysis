# Medical Information Technology, Inc. (MEDITECH) — Product Research

Researched: 2026-02-17
Developer website: https://www.meditech.com

## Overview

Medical Information Technology, Inc. (MEDITECH) is one of the largest and longest-established EHR vendors in the United States. Founded in 1969 by A. Neil Pappalardo and colleagues, the company is privately held and headquartered in Westwood, Massachusetts. MEDITECH reported approximately $494 million in revenue (2019) and employs around 3,000–3,500 people. It is the third-largest U.S. acute care hospital EHR vendor with approximately 14.8% market share as of 2024 (behind Epic at ~42% and Oracle Health at ~23%), serving an estimated 630–690 U.S. hospitals and over 1,000 organizations worldwide. MEDITECH has won Best in KLAS for 11+ consecutive years, especially dominant in the small hospital (1–150 bed) category.

MEDITECH has gone through several major technology platform generations over its history: MAGIC (1979, MUMPS-based green-screen), Client/Server (1990s, thick-client architecture), 6.x (2000s-2010s), and Expanse (current generation, web-based). All four platform generations have active ONC certifications, though MAGIC and Client/Server are legacy systems receiving only minimal compliance updates. The company's most prominent customer is HCA Healthcare, which operates 190+ hospitals and has historically run MEDITECH MAGIC but is now migrating to Expanse. MEDITECH also serves community hospitals, critical access hospitals, academic medical centers, long-term care facilities, and international health systems (e.g., UPMC Ireland, Fraser Health Authority in British Columbia, Aga Khan University Hospital in Kenya).

MEDITECH is notable for being a comprehensive, fully integrated hospital information system — not just an EHR. Its product list spans clinical, diagnostic, administrative, financial, and operational domains, all within a single integrated platform. This is important context for EHI export evaluation: the certified modules (Core HCIS, Ambulatory, ED Management) are components of a much larger integrated system that also includes billing, lab, pharmacy, imaging, dietary, HR/payroll, materials management, and more.

---

## Product: MEDITECH Expanse

CHPL IDs: 10925 (Expanse 2.2 Ambulatory), 10926 (Expanse 2.2 Core HCIS), 10927 (Expanse 2.2 ED Management), 10929 (Expanse 2.1 Core HCIS), 10930 (Expanse ED Management v2.1), 11742 (Expanse 2.1 Ambulatory)

### What It Is

MEDITECH Expanse is the company's current-generation, web-based EHR platform. It is a comprehensive, fully integrated hospital and health system information platform — not merely a clinical EHR, but an enterprise-wide system covering clinical care, revenue cycle, patient engagement, analytics, and business operations. The certified modules (Core HCIS, Ambulatory, ED Management) are components of this much larger platform.

Expanse is available as a traditional licensed implementation (on-premises or private cloud) or as MEDITECH as a Service (MaaS), a cloud-hosted subscription model. MaaS saw 21% growth in 2024 and is particularly popular with smaller and rural hospitals. Expanse supports FHIR R4 APIs and interoperability through its Traverse Exchange network and Greenfield Workspace developer environment.

### Users & Market

Expanse serves health systems of all sizes, from small critical access hospitals to large integrated delivery networks. Key deployments include:
- **HCA Healthcare** — 190+ hospitals, 2,300+ sites of care across 20 states and the UK (large-scale Expanse migration from MAGIC)
- **Emanate Health** — largest nonprofit in California's San Gabriel Valley
- **Frederick Health** — independent community healthcare organization with precision medicine program
- **Hebrew SeniorLife** — largest nonprofit senior care provider in New England
- **Fraser Health Authority** (British Columbia) — one of the first to deploy generative AI clinical documentation in Expanse
- **UPMC Ireland** — 4 hospitals, 2 cancer centres, 6 sports medicine clinics
- **Aga Khan University Hospital, Nairobi** — academic medical center going fully paperless across 7 hospitals and 340+ outreach centres
- **Centre for Neuro Skills** — specialty brain injury rehabilitation (7 locations, via MaaS)
- **Bethany Children's Health Center** — 160-bed pediatric rehabilitation hospital (via MaaS)

Day-to-day users include physicians, nurses, pharmacists, therapists, social workers, lab technicians, radiologists, billing staff, coders, registration clerks, case managers, practice managers, and administrative/executive staff. Patients interact via the MyHealth patient portal, MHealth mobile app, and Health Records on iPhone.

Expanse is KLAS #1 for Acute Care EHR (Small 1–150 Bed) for 6 consecutive years and ranks in the top 2 for Overall Health System Suite. KLAS customer feedback highlights flexibility, partnership, value, and comprehensive integration as key strengths.

### Modules & Functionality

MEDITECH's official product list (from ehr.meditech.com/meditech-product-list) describes an extensive set of integrated modules:

**Clinical Solutions:**
- Ambulatory (outpatient EHR)
- Electronic Health Record (inpatient)
- Emergency Department Management
- Expanse Now (mobile physician app, includes Expanse Cam)
- Expanse Patient Care (nursing workflows on tablets)
- Expanse Point of Care (mobile app for common nursing interventions)
- Expanse Navigator (AI-powered search and summarization of the patient record, built on Google Cloud)
- Genomics/Precision Medicine
- Order Management (CPOE, medication reconciliation)
- Outpatient Services
- Pharmacy
- Physician Care Manager
- Therapies

**Diagnostic Services:**
- Blood Bank
- Imaging and Documentation Management
- Laboratory
- Microbiology
- Outreach Lab
- Pathology
- Phlebotomy

**Care Coordination and Patient Engagement:**
- Care Compass (population health patient registries)
- Case Management
- Community Care Transitions Portal
- Expanse Patient Connect (cloud-based two-way patient texting)
- MyHealth (patient portal)
- Telehealth
- Traverse Exchange (interoperability network for cross-organization data exchange)
- Virtual Care (including Virtual On Demand Care)

**Specialty Care:**
- Critical Care
- Dietary
- Home Health
- Hospice
- Labor and Delivery
- Long Term Care (Continuing Care)
- Mental Health
- Oncology
- Surgical Services

**Patient Access and Revenue Cycle:**
- Abstracting
- Health Information Management (HIM)
- Practice Management
- Quality and Risk Management
- Registration
- Revenue Cycle / Electronic Claims
- Scanning and Archiving
- Scheduling and Referral Management
- Expanse Transport

**Business Operations:**
- Accounts Payable
- Budgeting and Forecasting
- Business and Clinical Analytics (BCA)
- Corporate Management Software
- Data Repository
- Executive Support System
- Fixed Assets
- General Ledger
- Human Resources
- Materials Management
- Payroll/Personnel
- Staff Gateway
- Staffing and Scheduling

MEDITECH also delivers standard evidence-based content across 50+ medical specialties, including order sets, documentation templates, flowsheets, widgets, protocols, and surveillance profiles (e.g., Cardiology, Pediatrics, Neurology).

Additional capabilities described in MEDITECH marketing and the Tegria guide: ambient listening for clinical documentation, auto-generation of discharge summaries (hospital course narrative), predictive analytics (Surveillance module identifying high-risk patients), Apple Health Records on iPhone integration, Google Workspace for Healthcare integration, and Expanse Virtual Assistant for touchless voice search.

### Data & Content

Based on the modules and features described above, MEDITECH Expanse stores an exceptionally broad range of healthcare data:

**Clinical data** (per EHR, Ambulatory, ED, specialty modules): Patient demographics, encounter/visit records, problem lists, diagnoses, allergies, medications, medication administration records, vital signs, clinical notes (physician, nursing, therapy, social work), orders (lab, radiology, medications, procedures), clinical decision support alerts, care plans, flowsheets, assessments, immunizations, growth charts, surgical/procedure records, anesthesia records, labor & delivery records, critical care flowsheets, oncology treatment plans/infusion records, mental health assessments, home health/hospice documentation, dietary orders and assessments.

**Diagnostic data** (per Lab, Microbiology, Pathology, Blood Bank, Imaging, Phlebotomy modules): Lab orders and results, microbiology cultures and sensitivities, pathology reports, blood bank/transfusion records, radiology orders and reports, imaging documentation, phlebotomy collection records.

**Pharmacy data** (per Pharmacy module): Medication dispensing records, pharmacy orders, formulary data, e-prescribing transactions (Surescripts integration implied by CPOE/e-prescribing certification criteria).

**Revenue cycle and financial data** (per Revenue Cycle, Practice Management, Registration, Abstracting, Electronic Claims, Scheduling): Patient registration and insurance information, scheduling data, referral tracking, charge capture, claims/billing data, electronic claims submissions, patient accounts, collections, coding/abstracting data, HIM records.

**Patient engagement data** (per MyHealth portal, Patient Connect, Telehealth, Virtual Care): Patient portal messages, appointment requests, telehealth visit records, patient-generated health data, remote monitoring data, patient satisfaction/feedback data, two-way text messages.

**Care coordination data** (per Care Compass, Case Management, Community Care Transitions, Traverse Exchange): Population health registries, care coordination records, case management notes, transition of care documents (C-CDAs), community care referral data, interoperability exchange records.

**Business/administrative data** (per full Business Operations suite): General ledger entries, accounts payable, payroll/personnel records, human resources data, materials management/supply chain data, fixed assets, budgeting/forecasting data, staffing schedules.

**Analytics/reporting data** (per BCA, Data Repository, Surveillance): Clinical and business analytics datasets, quality measures, risk management records, surveillance alerts, executive dashboards.

**Document management** (per Scanning and Archiving, HIM): Scanned documents, archived records, release of information records.

The certification page also lists separately certified modules that interact with these platforms: Continuity of Care Interface (CCD) for clinical document exchange, MyHealth Portal for patient access, and multiple Public Health Interface modules (immunization registry, syndromic surveillance, reportable lab results, electronic case reporting, cancer case reporting). These imply structured data for immunizations, reportable conditions, syndromic surveillance, and cancer registry data.

---

## Product: MEDITECH 6.x (6.0 and 6.1)

CHPL IDs: 10931 (6.1 Core HCIS), 10935 (6.1 ED Management), 10972 (6.0 Core HCIS), 10973 (6.0 ED Management), 11743 (6.1 Ambulatory)

### What It Is

MEDITECH 6.x is the prior-generation platform preceding Expanse. It represents two sub-versions: 6.0 (v6.08c) and 6.1 (v6.15c). Like Expanse, it is a comprehensive integrated hospital information system, not just a clinical EHR module. The 6.x platform was the bridge between MEDITECH's older Client/Server architecture and the modern web-based Expanse. It introduced improved graphical interfaces and some web capabilities but is not fully web-based like Expanse.

The certified modules (Core HCIS, ED Management, Ambulatory) are components of the full 6.x platform, which includes the same broad range of clinical, financial, and administrative modules described under Expanse (though with older user interfaces and fewer modern features like AI, mobile apps, and cloud hosting).

### Users & Market

MEDITECH 6.x is still in active use at many hospitals that have not yet migrated to Expanse. According to KLAS data, 63% of legacy MEDITECH customers making a new EHR decision in 2024 chose to migrate to Expanse, meaning a significant portion remain on 6.x or are in the process of transitioning. The user base includes community hospitals, regional health systems, and some larger organizations that adopted 6.x before Expanse was available. The same range of clinical and administrative staff use 6.x as use Expanse.

### Modules & Functionality

The 6.x platform includes functionally similar modules to Expanse — clinical EHR, lab, pharmacy, imaging, revenue cycle, practice management, business operations, etc. — but without Expanse's modern features (web-based UI, AI/ambient listening, mobile-first apps, cloud-native MaaS, advanced interoperability via Traverse Exchange). The certification page shows that 6.x deployments also use the same shared modules: Continuity of Care Interface (CCD), MyHealth Portal, and Public Health Interfaces for immunization registries, syndromic surveillance, reportable lab results, electronic case reporting, and cancer case reporting.

The 6.1 platform also has a separately certified Oncology module (MEDITECH 6.1 Oncology v6.15c), indicating integrated cancer care management.

### Data & Content

The data stored by MEDITECH 6.x is essentially the same categories as Expanse (clinical records, lab results, pharmacy data, billing/claims, scheduling, patient portal messages, care coordination documents, business operations data, etc.), since it runs the same integrated suite of modules. The primary differences from Expanse are in the user interface, technology architecture, and modern feature set — not in the fundamental data domains.

---

## Product: MEDITECH MAGIC

CHPL IDs: 10979 (MAGIC Core HCIS), 10981 (MAGIC ED Management), 11018 (MAGIC HCA Core HCIS without PatientKeeper)

### What It Is

MEDITECH MAGIC is the company's legacy platform, originally launched in 1979. It is built on the MUMPS programming language (also known as M/MIIS) and features a character-based "green-screen" user interface. Despite its age, MAGIC remains in active use at some hospitals, particularly those that have not yet migrated to newer MEDITECH platforms. MAGIC is an on-premises system and does not support web-based or mobile workflows.

The "MAGIC HCA" variant (CHPL 11018) is a special certification for HCA Healthcare's deployment of MAGIC without the PatientKeeper mobile overlay. This variant has notably different certified criteria from the standard MAGIC product, including (b)(1) Transitions of Care — Send, (b)(2) Transitions of Care — Receive, (e)(1) View/Download/Transmit (patient portal), and (f)(1)–(f)(3), (f)(5) for public health reporting (immunization registries, syndromic surveillance, reportable lab results, cancer case reporting). This suggests HCA's MAGIC deployment includes additional interoperability and patient-facing capabilities not present in the standard MAGIC certification.

PatientKeeper is a third-party clinician-facing mobile application that integrates with MEDITECH systems (both MAGIC and Expanse) to provide physicians with smartphone/tablet access to patient data, lab results, notes, and workflow tools. HCA has historically used PatientKeeper as a mobile overlay on top of MAGIC's text-based interface.

### Users & Market

MAGIC's primary remaining user base consists of hospitals that have not yet migrated to newer MEDITECH platforms. The most notable MAGIC user is HCA Healthcare, which operated 190+ hospitals on MAGIC and is actively migrating to Expanse. As of 2024, HCA had completed Expanse rollout to 43+ hospitals. MAGIC is only receiving minimal updates for compliance and patient safety; it is no longer the focus of MEDITECH's development. The system is on a sunset trajectory.

### Modules & Functionality

MAGIC, like all MEDITECH platforms, is a comprehensive integrated hospital information system. The certification page lists MAGIC-specific certifications for: Core HCIS, ED Management, Medical and Practice Management (MPM) — an ambulatory/practice management module, Oncology, and the shared CCD, MyHealth Portal, and Public Health Interface modules. MAGIC supports the full range of hospital operations — clinical documentation, lab, pharmacy, imaging, billing, scheduling, etc. — but through its legacy green-screen interface.

The MAGIC platform also includes the same Business Operations modules (GL, AP, HR, Payroll, Materials Management, etc.) as the broader MEDITECH suite, as these are part of the integrated HCIS platform.

### Data & Content

MAGIC stores the same fundamental categories of healthcare data as the newer platforms: clinical records, lab results, pharmacy data, orders, billing/claims, scheduling, patient registration, supply chain, HR/payroll, etc. The data model is rooted in MUMPS/M databases rather than modern relational or cloud databases, but the functional data domains are comparable. The HCA variant's additional certifications for (e)(1) patient portal access and (b)(1)/(b)(2) transitions of care confirm that patient portal data and clinical document exchange data are also stored.

---

## Product: MEDITECH Client/Server

CHPL IDs: 10982 (C/S Core HCIS), 10984 (C/S ED Management)

### What It Is

MEDITECH Client/Server (C/S) is the platform generation that succeeded MAGIC in the 1990s. It introduced a graphical thick-client architecture replacing MAGIC's green-screen interface, but it is still a legacy platform that predates the web-based 6.x and Expanse systems. Like MAGIC, Client/Server is on-premises only and is receiving only minimal compliance updates. It shares the v5.67c software version with MAGIC, suggesting convergence in the codebase at this point.

The certification page lists Client/Server certifications for: Core HCIS, ED Management, Medical and Practice Management (MPM), Oncology, and the shared CCD, MyHealth Portal, and Public Health Interface modules.

### Users & Market

Client/Server's user base consists of hospitals that adopted MEDITECH after MAGIC but before 6.x. Like MAGIC users, many are migrating to Expanse. The system is on a sunset trajectory with minimal development investment.

### Modules & Functionality

Client/Server includes the same comprehensive suite of integrated hospital modules as other MEDITECH platforms — clinical EHR, lab, pharmacy, imaging, revenue cycle, practice management, business operations, etc. — through a graphical thick-client interface. The certification page confirms C/S also has separately certified Oncology, MPM, CCD, MyHealth Portal, and Public Health Interface modules.

### Data & Content

Data domains are comparable to the other MEDITECH platforms: clinical records, diagnostic results, pharmacy data, billing/revenue cycle, scheduling, administrative/business data. The data architecture is legacy but the functional scope is the same integrated HCIS.

---

## Cross-Platform Observations

### Shared Components
All four platforms share certain separately certified modules that are cross-compatible:
- **MEDITECH Continuity of Care Interface (CCD)** — handles clinical document exchange (C-CDAs)
- **MEDITECH MyHealth Portal** (v2.0c) — patient portal for all platforms
- **Public Health Interfaces** — immunization registry transmission, syndromic surveillance, reportable lab results, electronic case reporting, cancer case reporting

### Certification Criteria Analysis
All products have nearly identical certified criteria, including:
- **(a)(1)–(a)(5), (a)(12), (a)(14)**: Core clinical capabilities (CPOE, demographics, problem list, medication list, medication allergy list, family health history, implantable device list)
- **(b)(3), (b)(10), (b)(11)**: Electronic prescribing, EHI export, care plan interoperability
- **(c)(1)–(c)(3)**: Clinical quality measures
- **(d) series**: Privacy, security, auditing
- **(e)(3)**: Patient health information capture
- **(g)(7), (g)(9), (g)(10)**: API access, FHIR

The MAGIC HCA variant (11018) uniquely includes (b)(1), (b)(2) transitions of care, (e)(1) patient portal access, and (f)(1)–(f)(3), (f)(5) public health reporting — suggesting HCA's deployment has enhanced interoperability capabilities.

### Key Takeaway for EHI Export Assessment
The certified modules (Core HCIS, Ambulatory, ED Management) are just three components of an enormous integrated hospital information system. The full MEDITECH platform includes dozens of modules spanning clinical care, diagnostics, pharmacy, revenue cycle, patient engagement, care coordination, specialty care (oncology, L&D, mental health, home health, hospice, surgical services, critical care, dietary), and business operations (GL, AP, HR, payroll, materials management, staffing). Under §170.315(b)(10), the EHI export should cover all electronic health information stored by the product "of which the Health IT Module is a part" — meaning the entire integrated MEDITECH system, not just the certified module.

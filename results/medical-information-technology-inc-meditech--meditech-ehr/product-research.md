# Medical Information Technology, Inc. (MEDITECH) — Product Research

Researched: 2026-02-16
Developer website: https://www.meditech.com

## Overview

Medical Information Technology, Inc. (MEDITECH) is a privately held healthcare IT company founded in 1969, headquartered in Westwood, Massachusetts. It is the third-largest hospital EHR vendor in the United States, behind Epic and Oracle Health (Cerner), with approximately 14.8% of the U.S. acute care hospital EHR market share by number of hospitals (~900 hospitals) as of 2024 (KLAS data). Globally, MEDITECH serves over 1,000 organizations. Revenue was $493.8 million as of 2019 (the most recent publicly reported figure). The company is led by CEO Michelle O'Connor (since 2021) and has offices in Massachusetts, Georgia, Minnesota, the UK, South Africa, and Australia.

MEDITECH has evolved through five distinct platform generations over its 55+ year history: **MAGIC** (1982), **Client/Server** (1994), **6.0** (2006), **6.1** (incremental upgrade to 6.0), and **Expanse** (2018, current strategic platform). Each generation represents a fundamentally different technology architecture — not just version upgrades — and the older platforms (MAGIC, Client/Server) are in maintenance-only mode. MEDITECH's primary market is small-to-midsize community hospitals, though it also serves large health systems (most notably HCA Healthcare with 190+ hospitals), academic centers, critical access hospitals, long-term care, home health, and ambulatory clinics. The company has been recognized as "Best in KLAS" for 11 consecutive years (through 2025), particularly strong in small acute care (1-150 beds). MEDITECH's customer base is gradually declining as some hospitals migrate to Epic, but over 60% of legacy MEDITECH users choosing a new EHR in 2024 selected Expanse.

Acquisitions include Patient Care Technologies (2007, home care software), LSS Data Systems (2011, long-standing partner), and Centennial Computer Corporation (2018, UK-based, enabling UK/Ireland expansion). MEDITECH is **not** a white-label or resold product — it is a primary developer.

---

## Product: MEDITECH Expanse

CHPL IDs: 10925 (Expanse 2.2 Ambulatory), 10926 (Expanse 2.2 Core HCIS), 10927 (Expanse 2.2 ED Management), 10929 (Expanse 2.1 Core HCIS), 10930 (Expanse ED Management v2.1), 11742 (Expanse 2.1 Ambulatory)

### What It Is

MEDITECH Expanse is MEDITECH's current-generation, fully web-based, cloud-ready EHR platform launched in 2018. It is a comprehensive, fully integrated hospital information system (HCIS) — not just an EHR module but an entire enterprise platform covering clinical, administrative, financial, and operational functions. The certified modules (Core HCIS, Ambulatory, Emergency Department Management) are components of the larger Expanse platform. "Core HCIS" refers to the inpatient/hospital-wide EHR; "Ambulatory" covers outpatient/clinic workflows; "ED Management" is the emergency department module. All share the same underlying platform and database.

Expanse is architecturally distinct from all prior MEDITECH platforms — it is HTML5/web-based, mobile-first, and designed for cloud hosting. MEDITECH offers "MEDITECH as a Service" (MaaS), a subscription-based cloud-hosted deployment. The platform supports both on-premise and cloud deployments.

### Users & Market

Expanse targets healthcare organizations of all sizes:
- **Small/community hospitals** (strongest market segment, consistently #1 in KLAS for 1-150 bed hospitals)
- **Large health systems** — most notably **HCA Healthcare** (190 hospitals, 2,300+ sites of care, 20 U.S. states + UK), which signed a large-scale agreement for Expanse and has gone live at 43+ hospitals as of early 2026
- **Specialty organizations** — including Hebrew SeniorLife (elderly care), Bethany Children's Health Center (pediatric rehab), Centre for Neuro Skills (brain injury rehab)
- **International deployments** — UPMC Ireland, Aga Khan University Hospital (Kenya/Pakistan), Fraser Health Authority (British Columbia), Blackrock Health Group (Ireland), Chris O'Brien Lifehouse (Australia)
- **Ambulatory/clinics** — community health systems with both hospital and clinic settings

Day-to-day users include physicians, nurses, therapists, pharmacists, lab technicians, radiology staff, billing/coding staff, schedulers, case managers, administrators, executives, and patients (via the MyHealth patient portal).

### Modules & Functionality

Based on MEDITECH's published product list (ehr.meditech.com/meditech-product-list) and Expanse marketing materials, Expanse includes the following modules and capabilities:

**Clinical Solutions:**
- **Electronic Health Record** — inpatient clinical documentation, problem lists, clinical notes, orders
- **Ambulatory** — outpatient visit workflows, ambulatory documentation
- **Emergency Department Management** — ED tracking, triage, documentation, disposition
- **Order Management** — CPOE (computerized physician order entry), order sets
- **Pharmacy** — medication management, e-prescribing (integrates with Surescripts per certified criteria (b)(3))
- **Expanse Now** (mobile app with camera — "Expanse Cam") — smartphone/tablet access for physicians
- **Expanse Patient Care** — nursing and therapist workflows on mobile devices
- **Expanse Point of Care** — bedside mobile app for nursing interventions
- **Physician Care Manager** — physician-centric workflow management
- **Expanse Navigator** — AI-powered search and summarization using Google Cloud, NLP, ambient listening for clinical documentation
- **Genomics/Precision Medicine** — integrated DNA data and precision medicine decision support
- **Therapies** — therapy orders and documentation
- **Outpatient Services** — outpatient procedure and visit management
- **High Availability Snapshot** — system availability/disaster recovery

**Diagnostic Services:**
- **Laboratory** — lab orders, results, workflows
- **Microbiology** — microbiology-specific lab module
- **Blood Bank** — transfusion medicine
- **Pathology** — pathology results and reporting
- **Phlebotomy** — specimen collection management
- **Outreach Lab** — reference lab workflows
- **Imaging and Documentation Management** — radiology/imaging orders, results, document management

**Care Coordination & Patient Engagement:**
- **MyHealth** — patient portal for viewing records, messaging, etc.
- **Expanse Patient Connect** — automated patient texting, appointment reminders, Google review prompts
- **Telehealth** — virtual visit capabilities
- **Virtual Care** (includes Virtual On Demand Care) — on-demand telehealth
- **Care Compass** (includes Patient Registries) — population health management, chronic disease registries
- **Case Management** — care coordination, discharge planning
- **Community Care Transitions Portal** — data sharing for transitions of care
- **Traverse Exchange** — MEDITECH's proprietary interoperability network for data exchange across organizations

**Specialty Care:**
- **Oncology** — chemotherapy management, cancer-specific workflows (separately certified)
- **Surgical Services** — OR scheduling, surgical documentation, anesthesia
- **Labor and Delivery** — obstetric workflows
- **Critical Care** — ICU-specific documentation and monitoring
- **Mental Health** — behavioral health workflows
- **Long Term Care (Continuing Care)** — nursing home/SNF documentation
- **Home Health** — home-based care documentation and billing
- **Hospice** — hospice-specific workflows
- **Dietary** — nutrition and dietary management

**Revenue Cycle & Patient Access:**
- **Revenue Cycle / Electronic Claims** — billing, claims submission, denial management, claim scrubbing
- **Registration** — patient registration and ADT
- **Scheduling and Referral Management** — appointment scheduling, referral tracking
- **Practice Management** — ambulatory practice operations
- **Health Information Management (HIM)** — medical records management, coding
- **Abstracting** — clinical data abstraction for quality reporting
- **Quality and Risk Management** — quality metrics, risk tracking
- **Scanning and Archiving** — document scanning and storage
- **Expanse Transport** — patient transport management

**Business Operations:**
- **Business and Clinical Analytics (BCA)** — reporting, dashboards, business intelligence
- **Data Repository** — enterprise data warehouse
- **Executive Support System** — executive-level reporting
- **General Ledger** — financial accounting
- **Accounts Payable** — AP processing
- **Budgeting and Forecasting** — financial planning
- **Fixed Assets** — asset tracking
- **Materials Management** — supply chain/inventory
- **Human Resources** — HR management
- **Payroll/Personnel** — payroll processing
- **Staffing and Scheduling** — workforce scheduling
- **Staff Gateway** — employee self-service portal
- **Corporate Management Software** — multi-facility corporate operations

This is an extremely comprehensive product — effectively a full hospital operating system covering clinical care, diagnostics, patient engagement, revenue cycle, financial/accounting, HR/payroll, supply chain, and analytics.

### Data & Content

Based on the module inventory and certified criteria, Expanse stores and manages:

**Clinical Data:**
- Patient demographics, encounters, admissions/discharges/transfers (Registration, ADT)
- Clinical notes and documentation (structured and unstructured) — physician notes, nursing assessments, therapy documentation
- Problem lists, diagnoses (criteria (a)(1))
- Medication lists, prescriptions, e-prescriptions (criteria (a)(2), (b)(3) — e-prescribing via Surescripts)
- Allergies and adverse reactions
- Lab orders and results (Laboratory, Microbiology, Pathology modules)
- Radiology/imaging orders and results (Imaging module)
- Vital signs, flowsheets, clinical measurements
- Order entry data — CPOE orders, order sets (criteria (a)(3))
- Surgical documentation — OR records, anesthesia records
- Emergency department records — triage, ED notes, dispositions
- Ambulatory visit records — outpatient encounters, follow-ups
- Oncology data — chemotherapy regimens, cancer staging
- Mental health/behavioral health records
- Home health and hospice documentation
- Long-term care / continuing care records
- Labor and delivery records
- Critical care/ICU documentation
- Dietary/nutrition records
- Blood bank / transfusion records
- Genomics/precision medicine data — DNA/genetic test results
- Patient-reported data via MyHealth portal

**Care Coordination Data:**
- Care plans, case management notes
- Referral information
- Continuity of Care Documents (CCDs) — generated and consumed per certification
- Health information exchange data (Traverse Exchange)
- Telehealth/virtual visit records
- Patient portal messages and communications
- Population health registries (Care Compass)

**Revenue Cycle / Financial Data:**
- Insurance/payer information
- Billing codes (ICD, CPT, HCPCS)
- Claims data — submitted claims, remittances, denials
- Charge capture data
- Patient statements and balances
- Practice management / scheduling data

**Administrative/Operational Data:**
- Scheduling data — appointments, referrals, OR schedules
- Scanned documents and archived records
- Quality metrics and risk management data
- Public health reporting data — immunization registry submissions (criteria (f)(6)), syndromic surveillance, electronic case reporting, cancer case reporting
- Audit trails (criteria (d)(2))

**Business/Financial Data:**
- General ledger, AP, fixed assets, budgeting data
- Payroll and HR records
- Materials management / supply chain data
- Staffing schedules
- Analytics and data repository content
- Executive dashboards and reports

The breadth of data is enormous — MEDITECH Expanse is essentially the sole information system for many hospitals, storing virtually all electronic health information, financial data, and operational data for the organization.

---

## Product: MEDITECH 6.1

CHPL IDs: 10931 (6.1 Electronic Health Record Core HCIS), 10935 (6.1 Emergency Department Management), 11743 (6.1 Ambulatory Electronic Health Record)

### What It Is

MEDITECH 6.1 is an incremental improvement over the 6.0 platform, which was launched in 2006 as a complete architectural rewrite of MEDITECH's older platforms. Version 6.1 features improved modularity, database structures, audit trails, disaster recovery, and enhanced clinical modules. The architecture is more modern than MAGIC/Client/Server but still relies on Windows infrastructure for client access — it is not web-based like Expanse. The certified modules (Core HCIS, Ambulatory, ED Management) cover the same functional areas as their Expanse counterparts.

MEDITECH 6.1 is functionally similar to Expanse in terms of available modules (the full product list applies to 6.x as well as Expanse), but the user interface and underlying architecture differ. Migration from 6.1 to Expanse is a substantial project often treated as a re-implementation.

### Users & Market

MEDITECH 6.1 is deployed at hospitals that adopted MEDITECH's 6.x platform and have not yet migrated to Expanse. This is typically community hospitals and mid-size health systems. The user profile is the same as Expanse — physicians, nurses, pharmacists, lab staff, billing staff, administrators. MEDITECH is actively encouraging migration to Expanse; 6.1 continues to receive regulatory and safety updates but is not MEDITECH's strategic future platform.

### Modules & Functionality

The same comprehensive module set described for Expanse applies to MEDITECH 6.1. The Core HCIS, Ambulatory, and ED Management modules provide the same core clinical functionality — CPOE, clinical documentation, e-prescribing, lab/imaging ordering, etc. The difference is in the architecture (not web-based) and user interface rather than functional scope. The regulatory certification page shows that 6.1 also has separately certified modules for Continuity of Care (CCD), MyHealth Portal, public health interfaces (immunization, syndromic surveillance, reportable lab, electronic case reporting, cancer case reporting), and Oncology.

### Data & Content

The data stored by MEDITECH 6.1 is functionally equivalent to Expanse — the same types of clinical, financial, administrative, and operational data. The underlying database structure differs from Expanse but the scope of data capture is the same across the full product suite.

---

## Product: MEDITECH 6.0

CHPL IDs: 10972 (6.0 Electronic Health Record Core HCIS), 10973 (6.0 Emergency Department Management)

### What It Is

MEDITECH 6.0 is the initial release of MEDITECH's "6.x" generation, launched in 2006. It was a complete rewrite of the older MAGIC and Client/Server platforms with focus on modularity, improved database structures, and enhanced clinical capabilities. Version 6.0 is older than 6.1 and would be considered more of a legacy platform at this point, though still certified and actively maintained for regulatory compliance.

Note that unlike 6.1, there is no separately certified Ambulatory module for 6.0 — only Core HCIS and ED Management are certified. The certification page does show separately certified CCD, MyHealth Portal, public health interfaces, and cancer case reporting modules for 6.0.

### Users & Market

Organizations still on MEDITECH 6.0 are typically those that have not yet migrated to 6.1 or Expanse. These are increasingly rare as MEDITECH pushes migration. The user base is the same type of community hospital and health system as described above.

### Modules & Functionality

The full MEDITECH module suite is available on 6.0, though with older interface and capabilities compared to 6.1 and Expanse. The same clinical, financial, administrative, and diagnostic modules apply.

### Data & Content

Same scope as 6.1 and Expanse — all clinical, financial, and operational data stored by the full hospital information system.

---

## Product: MEDITECH MAGIC

CHPL IDs: 10979 (MAGIC Electronic Health Record Core HCIS), 10981 (MAGIC Emergency Department Management), 11018 (MAGIC HCA Electronic Health Record Core HCIS, without PatientKeeper)

### What It Is

MEDITECH MAGIC is the oldest active MEDITECH platform, introduced in 1982. It is a text-based, centralized server system where clients function as dumb terminals. MAGIC is both an operating system and a programming language, built on MEDITECH's proprietary MIIS language (derived from MUMPS). The user interface is character-based — no graphical UI. MAGIC is in maintenance-only mode, receiving only regulatory and safety updates.

The **HCA variant** (CHPL ID 11018 — "MEDITECH MAGIC HCA Electronic Health Record Core HCIS, without PatientKeeper") is a notable special case. HCA Healthcare, the largest U.S. hospital chain (190 hospitals, 2,300+ sites of care), used MAGIC extensively and created a specialized configuration. The "(without PatientKeeper)" designation indicates that HCA supplemented MAGIC with PatientKeeper, a third-party mobile clinical application providing physician-facing mobile workflows (orders, chart review, etc.). This certification covers the MAGIC platform specifically without the PatientKeeper overlay. HCA is actively migrating from MAGIC to Expanse, with 43+ hospitals already live on Expanse as of early 2026.

The HCA MAGIC variant has a notably different certification profile than the standard MAGIC certification:
- Includes (b)(1) and (b)(2) — transitions of care (send/receive)
- Includes (e)(1) — patient portal view/download/transmit
- Includes (f)(1), (f)(2), (f)(3), (f)(5) — immunization registries, syndromic surveillance, electronic case reporting, cancer case reporting
- Lacks (c)(1)-(c)(3) clinical quality measures and (g)(2) automated measure calculation

The regulatory certification page also shows separately certified MAGIC modules for: Medical and Practice Management (MPM) Electronic Health Record (ambulatory/practice management), CCD, MyHealth Portal, public health interfaces, and Oncology.

### Users & Market

MAGIC is used by hospitals that adopted MEDITECH decades ago and have not yet migrated to newer platforms. These are typically smaller community hospitals with limited IT budgets, though HCA was the most prominent MAGIC user. The user experience is very different from modern EHRs — text-based screens, keyboard-driven navigation. The same types of clinical and administrative staff use MAGIC, but the workflows reflect the limitations of a 1980s-era architecture.

### Modules & Functionality

Despite its age, MAGIC provides the full MEDITECH module suite — clinical documentation, orders, pharmacy, lab, radiology, billing, scheduling, etc. — but with a text-based interface. The functional scope is similar to newer platforms, though many modern features (mobile access, AI, genomics, web-based workflows) are not available on MAGIC.

### Data & Content

MAGIC stores the same fundamental types of hospital data — patient demographics, clinical notes, orders, lab results, medications, billing/claims, scheduling, etc. The data architecture uses MEDITECH's proprietary MIIS/MUMPS-derived data structures. All clinical, financial, and operational data generated across the hospital information system is stored in the MAGIC database.

---

## Product: MEDITECH Client/Server

CHPL IDs: 10982 (Client/Server Electronic Health Record Core HCIS), 10984 (Client/Server Emergency Department Management)

### What It Is

MEDITECH Client/Server (C/S), introduced in 1994, is the second-generation MEDITECH platform. It uses the same core programming language as MAGIC but was designed for Microsoft Windows networks. Unlike MAGIC's centralized model, C/S distributes code execution to user PCs, providing a Windows GUI rather than text-based terminals. Client/Server is also in maintenance-only mode and considered a legacy platform.

The regulatory certification page also shows separately certified C/S modules for: Medical and Practice Management (MPM) Electronic Health Record (ambulatory/practice management), CCD, MyHealth Portal, public health interfaces, and Oncology — paralleling the MAGIC and 6.x module structure.

### Users & Market

Client/Server users are hospitals that adopted MEDITECH in the mid-1990s through early 2000s and have not yet migrated. Like MAGIC, these are shrinking populations being encouraged to move to Expanse.

### Modules & Functionality

The full MEDITECH module suite is available on Client/Server with a Windows-based graphical interface. Functionally equivalent in scope to MAGIC but with improved GUI and third-party integration capabilities. The same clinical, financial, administrative, and diagnostic modules apply.

### Data & Content

Same scope as other MEDITECH platforms — all clinical, financial, and operational data for the hospital. The data architecture is similar to MAGIC (MIIS/MUMPS-derived) but adapted for the Client/Server model.

---

## Cross-Cutting Observations

### Platform vs. Module Certification Structure

MEDITECH certifies its products as modular components — **Core HCIS** (the inpatient/hospital-wide EHR backbone), **Ambulatory** (outpatient), and **Emergency Department Management** — but each of these is a component of a much larger integrated HCIS platform. The full product includes 60+ modules spanning clinical, diagnostic, financial, administrative, and operational functions. This is critical for EHI export assessment: the "product of which the Health IT Module is a part" encompasses the entire MEDITECH platform, not just the narrowly certified module.

### Shared Modules Across Platforms

The mandatory disclosures page reveals several separately certified modules that are shared across platform generations:
- **Continuity of Care Interface (CCD)** — certified for each platform (v6.1c for Expanse/6.1, v6.0c for 6.0, v5.67c for MAGIC/C/S)
- **MyHealth Portal v2.0c** — same portal certification used across all platforms
- **Public health interfaces** — immunization registries, syndromic surveillance, reportable lab, electronic case reporting, cancer case reporting — each certified per platform version
- **Oncology** — separately certified for each platform (Expanse 2.2, 2.1, 6.1, MAGIC, C/S)

### Data Implications for EHI Export

Given that MEDITECH is a comprehensive HCIS, the EHI export should potentially cover data from all modules — not just clinical data but also:
- Revenue cycle / billing data (claims, charges, payer information)
- Scheduling data
- Patient portal messages and communications
- Document scans and archives
- Lab, imaging, pathology, blood bank results
- Pharmacy/medication data
- Case management and care coordination data
- Public health reporting data
- Quality metrics and risk management data
- Oncology-specific data (chemotherapy, cancer staging)
- Mental health records
- Home health and hospice records
- Long-term care records
- Surgical/anesthesia records
- Dietary data
- And potentially even financial/HR/supply chain data if considered part of the "product"

### Research Gaps

- **Pricing**: Not publicly disclosed; no free trial available
- **Exact customer counts by platform**: Unclear how many hospitals are on each platform generation (MAGIC vs. C/S vs. 6.0 vs. 6.1 vs. Expanse)
- **Data architecture details**: The specific database schema and data model for each platform generation are not publicly documented
- **Functional differences between platforms**: While I found high-level architectural differences, the specific module-by-module feature parity (or gaps) between platforms is not clearly documented in public sources
- **MEDITECH South Africa / international variants**: The company has international operations but it's unclear if these use the same product or have localized variants

# NaphCare, Inc. — Product Research

Researched: 2026-02-14
Developer website: https://www.naphcare.com

## Overview

NaphCare, Inc. is a privately held, family-owned provider of correctional healthcare services headquartered in Birmingham, Alabama. Founded in 1989, the company provides comprehensive healthcare services — medical, mental health, pharmacy, dialysis, telehealth, and forensic services — to jails, prisons, and reentry centers across the United States. NaphCare contracts with local (county jails), state (departments of corrections), and federal (federal prisons/reentry centers) government agencies. The company has approximately 6,000 employees and estimated revenues in the $250M–$500M range.

NaphCare developed TechCare, described as the first corrections-specific EHR, launching it in 2004. TechCare is both used internally by NaphCare's own clinical staff and sold/licensed to correctional facilities and government agencies as a standalone technology product. The system is available through a NASPO ValuePoint contract, enabling broader government procurement. TechCare was recognized as the 2026 Top-Rated EHR Vendor for Correctional Facilities by Black Book Research.

NaphCare is not a typical ambulatory or hospital EHR vendor — it is primarily a correctional healthcare services company that built its own EHR to support its operations and now also sells it to other correctional systems.

## Product: TechCare®

CHPL ID: 10207

### What It Is

TechCare is a corrections-specific electronic health record and comprehensive medical operations system. It is purpose-built for correctional healthcare environments — jails, prisons, and detention facilities — rather than being adapted from a general-purpose ambulatory or hospital EHR. The vendor emphasizes it was "designed by correctional health clinicians, not software developers" and eliminates "unnecessary, free-world processes" in favor of correctional-specific protocols.

The certified product is TechCare Version 5.0, which earned ONC Health IT 2015 Edition Cures certification via Drummond Group. The CHPL metadata shows SED intended users as "Correctional Health."

TechCare is described as having "all modules and tools built directly into the product" without requiring third-party solutions for core functionality. It is offered as a hosted (cloud-based) solution, customized for each correctional system. It also supports offline operation — TechCare can be "fully functional offline," which is important in correctional facilities where network connectivity may be limited or intermittent.

### Users & Market

**Scale**: TechCare operates in 220+ local and state correctional facilities, managing over 200,000 active patient records daily (numbers vary across press releases from different dates, ranging from 126,000 to 245,000 active records and 134 to 229+ facilities, reflecting growth over time).

**Notable deployments**:
- **Georgia Department of Corrections**: 62 facilities, 41,000+ patient records, with simultaneous go-live and peer-to-peer training for 1,700+ health staff
- **New Mexico Corrections Department**: 5,800 residents across all state prisons, with integrations to offender management, pharmacy, lab, radiology, immunization registry, and state Health Information Exchange
- **Fairfax County, VA**: County jail deployment
- **Lee County**: County jail facilities housing ~1,600 individuals
- **Pima County Adult Detention Complex** (Tucson, AZ)
- **Pasco County Detention Facility** (FL)

**End users**: Correctional healthcare clinicians (physicians, nurse practitioners, nurses, mental health providers, pharmacists), custody/administrative staff, and — via the MyCare patient portal — incarcerated patients themselves.

**Go-to-market**: Government contracts (local, state, federal). Available through NASPO ValuePoint master agreement for streamlined government procurement. Also distributed through Carahsoft (government IT solutions provider). NaphCare both uses TechCare for its own contracted healthcare operations and sells it as a standalone technology product to facilities that handle their own healthcare delivery.

### Modules & Functionality

TechCare is described as a "complete medical operations system" — not just clinical charting but the full operational platform for running healthcare in a correctional facility. Based on vendor materials, press releases, the Carahsoft product page, and the HealthcareTechOutlook profile, the following modules and capabilities are documented:

**Clinical Documentation & Workflows**:
- Intake screening and health assessments (receiving screenings upon facility admission)
- Clinical encounter documentation and health encounter tracking
- Standardized treatment processes with compliance-aligned clinical protocols
- Chart auditing and litigation support
- Access to patient records from prior incarcerations
- Real-time patient care tracking (location, needs, status)
- Discharge planning and coordination with community providers

**Medication Management**:
- Medication Administration Records (MAR)
- TechCare GO: browser-based, offline-capable medication administration module (released September 2025) — preloads patient lists by location/timeframe, tracks medication delivery with accountability documentation, syncs when connectivity is restored
- Integration with pharmacy systems for electronic ordering
- Pharmacy Active Orders Dashboard for visibility into all active medication orders

**Mental Health & Behavioral Health**:
- Behavioral health-specific medication management
- Substance Abuse Level of Care assessment and reporting
- Substance use disorder management, detoxification tracking (Detox Dashboard)
- Medication-Assisted Treatment (MAT) support
- Suicide prevention program documentation
- Mental health stabilization unit workflows

**Patient Portal (MyCare)**:
- 24/7 patient access to personal health information via digital tablets in correctional facilities
- Fully integrated with TechCare 5.0
- Improves access to care and transparency of health information

**Pharmacy (NaphCare Rx Integration)**:
- In-house pharmacy services dedicated to correctional facilities
- Integrated electronic medication ordering
- Secure medicine delivery tracking
- Pharmacy consultation and review documentation

**Telehealth (STATCare)**:
- 24/7 telehealth with Nurse Practitioners
- Corporate nephrologist telemedicine consultations (for dialysis patients)

**Diagnostics**:
- Centralized diagnostics reporting and tracking
- Integration with laboratory services
- Integration with radiology services

**Analytics & Reporting (TechCare BI)**:
- Integrated Power BI dashboards with real-time, self-service data access
- Intake Compliance Dashboard (admission screening adherence)
- Detox Dashboard (withdrawal management, risk indicators)
- Pharmacy Active Orders Dashboard
- Completed Sick Calls Dashboard (response times, provider trends, outcomes)
- Monthly Health Services Request (HSR) Dashboard (resource planning, trend analysis)
- Daily HSR Dashboard (real-time request monitoring)
- Offsite Reporting Self-Service Dashboard (hospital/specialty care referral reports)
- NaphCare University Compliance Dashboard (staff training, continuing education)

**Administrative & Compliance**:
- Real-time compliance monitoring and reporting against national correctional healthcare standards (e.g., NCCHC)
- Staff scheduling optimization
- Claims processing
- Hospital/specialty provider network management (4,600+ hospitals in NaphCare's network)
- Medical scheduling coordination
- Offsite/hospital referral management

**System Integrations** (documented in NMCD deployment):
- Offender management systems
- Pharmacy provider systems
- Laboratory services
- Radiology services
- Immunization registry
- State Health Information Exchange (HIE)
- Inmate communication kiosks
- Food service management systems
- Medicaid processing

**Interoperability / Certified Capabilities**:
The CHPL certification covers criteria including:
- (a)(1)–(a)(5): CPOE, clinical decision support, demographics, vital signs, problem list
- (a)(12): Family health history
- (a)(14): Implantable device list
- (b)(1): Transitions of care (C-CDA)
- (b)(10): EHI export
- (b)(11): Care plan
- (c)(1): Clinical quality measures
- (g)(7)–(g)(10): API access / FHIR
- (h)(1): Direct messaging
- Various (d) criteria for privacy, security, auditing

**Emerging capabilities** (mentioned in recent press releases):
- Visual data analytics
- Artificial intelligence engines
- Chatbots based on data models
- Clinically appropriate AI recommendations

### Data & Content

Based on documented features and integrations, TechCare manages or stores:

- **Patient demographics** and identification information
- **Medical history** including records from prior incarcerations at the same or connected facilities
- **Intake screening and assessment data** (receiving screenings, health assessments upon admission)
- **Clinical encounter notes** and health encounter documentation
- **Problem lists, medication lists, allergy lists** (implied by (a)(1)–(a)(5) certification and clinical workflows)
- **Vital signs** (certified for (a)(5))
- **Family health history** (certified for (a)(12))
- **Implantable device information** (certified for (a)(14))
- **Care plans** (certified for (b)(11))
- **Medication administration records** — detailed MAR data including timing, accountability, and compliance tracking
- **Pharmacy orders** — active medication orders, electronic prescribing workflows
- **Mental health and behavioral health records** — substance abuse assessments, level of care designations, behavioral health medications, detox/withdrawal management records, suicide risk documentation
- **Diagnostic results** — laboratory and radiology results
- **Immunization records** (integrates with immunization registries)
- **Telehealth encounter records** (STATCare 24/7 telehealth sessions)
- **Patient portal activity** (MyCare interactions, health information requests)
- **Health services requests** (sick call requests — both daily and monthly volumes tracked)
- **Referral and offsite care records** (hospital referrals, specialty care visits)
- **Claims and billing data** (claims processing, Medicaid processing integration)
- **Compliance and audit records** (chart audits, compliance monitoring against NCCHC standards)
- **Staff training and credentialing records** (NaphCare University compliance tracking)
- **Scheduling data** (medical appointments, staff scheduling)
- **Transition of care documents** (C-CDA documents per (b)(1) certification)
- **Discharge planning records** (coordination with community providers)

**Data architecture note**: TechCare consolidates data from multiple integrated systems — offender management, pharmacy, lab, radiology, food service, Medicaid, and inmate communication kiosks — into "one source for real-time patient information" (Carahsoft page). This means the EHI export scope could potentially include data originating from these integrated sources.

**Gaps in research**: The vendor website and press materials are heavily focused on operational/marketing messaging and light on detailed technical documentation. There is no publicly accessible feature list with module-by-module descriptions. No third-party reviews were found on G2, KLAS, or Capterra — the correctional healthcare EHR market is niche and doesn't appear well-represented on mainstream review platforms. The Black Book recognition and HealthcareTechOutlook profiles were the most specific third-party sources available.

It's also unclear how much of NaphCare's administrative services infrastructure (claims processing, provider network management with 4,600+ hospitals, medical scheduling) is built into TechCare vs. handled by separate NaphCare administrative systems. The Carahsoft page suggests these are consolidated into TechCare ("consolidates critical systems including... hospital referrals, and Medicaid processing into one unified information source"), but this may reflect NaphCare's operational integration rather than TechCare's standalone product capabilities.

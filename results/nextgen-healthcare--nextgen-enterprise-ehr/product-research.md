# NextGen Healthcare — Product Research

Researched: 2026-02-16
Developer website: https://nextgen.com

## Overview

NextGen Healthcare is a major ambulatory-focused health IT vendor, originally founded in 1973 as Quality Systems Inc. (QSI). QSI went public in 1982, acquired the NextGen brand as a subsidiary in 2001, and eventually rebranded fully as NextGen Healthcare. In November 2023, private equity firm Thoma Bravo completed a $1.8 billion acquisition, taking the company private and delisting it from Nasdaq. At the time of acquisition, the company had approximately $680–690 million in annual revenue and roughly 3,200–3,400 employees. Thoma Bravo's stated goal was to accelerate cloud-based healthcare solutions serving over 100,000 ambulatory providers managing 65+ million patients across the US.

NextGen Healthcare offers two main product lines: **NextGen Enterprise** (for mid-size to large multi-specialty and multi-location ambulatory groups) and **NextGen Office** (formerly MediTouch, a cloud-based all-in-one for small/solo practices). Only NextGen Enterprise EHR is the subject of this certification. The company also owns Mirth Connect, an integration/interoperability engine used for public health reporting and data exchange. NextGen Healthcare's Practice Management solution has been ranked #1 by Black Book Research for nine consecutive years, and the company has received KLAS recognition for behavioral health.

## Product: NextGen Enterprise EHR

CHPL IDs: 10861 (version 6.2021.1 Cures, certified 2022-03-18), 11645 (Enterprise 8, certified 2025-06-02)

### What It Is

NextGen Enterprise EHR is a comprehensive ambulatory electronic health record and practice management platform designed for mid-size to enterprise-level healthcare organizations. It is not just an EHR module — it is a full-suite product encompassing clinical documentation (EHR), practice management (PM), revenue cycle management (RCM), patient engagement/portal, population health analytics, clearinghouse/EDI, and interoperability capabilities. The certified module is the EHR component, but the product it belongs to includes all of these integrated capabilities sold as a unified platform.

The certification is very broad: 44+ criteria across clinical data (a)(1)–(a)(15), transitions of care (b)(1)–(b)(3), EHI export (b)(10), care plan (b)(9)/(b)(11), CQMs (c)(1)–(c)(4), privacy/security (d)(1)–(d)(13), patient portal/VDT (e)(1)/(e)(3), public health reporting (f)(1)/(f)(2)/(f)(4)/(f)(5)/(f)(7), FHIR API (g)(7)–(g)(10), and Direct messaging (h)(1). SED testing was conducted with clinicians holding MD, DO, NP, or PA credentials. Enterprise 8 is the latest version, certified for HTI-1 Phase 2 compliance, making NextGen one of the first major EHR vendors to meet updated ONC interoperability standards due December 31, 2025.

### Users & Market

NextGen Enterprise targets mid-size to enterprise ambulatory practices — multi-specialty groups, large single-specialty groups, multi-site organizations, FQHCs, and community health centers. The vendor claims over 100,000 providers and 65+ million patients across the US. Over 2,400 organizations use NextGen solutions. Notable customer types visible on the website include:

- **FQHCs/Community Health Centers** (Greenville Rancheria, Morris Heights Health Center, Valle del Sol, Reno Sparks Tribal Health)
- **Behavioral health organizations** (Bowen Center, Liberty Resources)
- **Multi-specialty groups** (Hutchinson Clinic, Murfreesboro Medical Clinic, Presbyterian Medical)
- **Specialty practices** (Coastal Orthopedics, South Denver Gastro)

The vendor's specialty page lists clinical content for **26+ specialties** and earned first-place EHR ratings from Black Book Research in cardiology, community health centers/FQHC, internal medicine, and sleep medicine/pulmonary. The product is particularly strong in behavioral health (KLAS award winner), FQHCs, and integrated whole-person care delivery (medical + behavioral + dental).

Day-to-day users include physicians (MD, DO), nurse practitioners, physician assistants, nurses, billing staff, front-desk/registration, practice managers, and patients (via portal). The product can be deployed on-premise or cloud-hosted (AWS).

### Modules & Functionality

Based on vendor website, product pages, mandatory disclosures, and third-party reviews, NextGen Enterprise includes the following modules and capabilities:

**Clinical Documentation (EHR)**
- Comprehensive charting with specialty-specific templates for 26+ specialties (source: nextgen.com homepage and enterprise EHR page)
- Clinical decision support, drug-drug/drug-allergy interaction checking (certified criteria a)(1)–(a)(5))
- CPOE for medications, labs, diagnostic imaging (certified criteria a)(1)–(a)(4))
- Problem lists, medication lists, medication allergy lists (certified criteria a)(1)–(a)(5))
- Clinical quality measures (CQMs) reporting
- Demographics recording including race, ethnicity, preferred language, sex, gender identity, SOGI (certified criteria a)(5))
- Implantable device list (certified criterion a)(14))
- Social, psychological, behavioral data (certified criterion a)(12))
- Family health history (certified criterion a)(12))

**E-Prescribing**
- Electronic prescribing including controlled substances (EPCS)
- Surescripts integration (implied by e-prescribing capabilities)

**Practice Management (PM)**
- Patient registration and scheduling with multi-location support (source: nextgen.com/solutions/practice-management)
- Master Patient Index (MPI) across enterprise
- Eligibility verification (automated)
- Appointment booking, multi-provider calendars
- Cost estimation for patient responsibility
- Advanced scheduling tools

**Revenue Cycle Management (RCM) & Billing**
- Automated claim scrubbing and submission (source: PM product page)
- Automated charge review with specialty-specific rules engine
- Claims processing and EDI/clearinghouse connectivity
- Accounts receivable management
- Collections optimization
- Background Business Processor (automated 24/7 batch processing)
- Financial reporting, payer mix analysis, month-end closing tools
- Denial management
- ICD-10 coding support (with AI suggestions)
- Medical coding compliance audits

**Patient Engagement / Patient Portal**
- Patient portal for viewing records, lab results, education materials (certified criterion e)(1))
- Secure messaging
- Patient self-scheduling
- Online payments / electronic bill pay
- Digital document upload, pre-visit intake forms
- Appointment reminders and recall
- Broadcast messaging
- Virtual visits / telehealth integration
- Patient surveys
- Remote patient monitoring (mentioned on homepage)

**Interoperability & Data Exchange**
- C-CDA generation and exchange (transitions of care) (certified criteria b)(1)–(b)(3))
- Direct messaging (certified criterion h)(1))
- FHIR API access (certified criteria g)(7)–(g)(10))
- Health Information Exchange (HIE) connectivity
- Payer data exchange
- Bulk C-CDA Export Utility (mentioned in mandatory disclosures as requiring billable setup hours)
- Mirth Connect integration engine for interfaces (lab, registries, syndromic surveillance)

**Public Health Reporting**
- Immunization registry reporting (certified criterion f)(1))
- Syndromic surveillance (certified criterion f)(2))
- Cancer registry reporting (certified criterion f)(4))
- Specialized registry reporting (certified criterion f)(5))
- Electronic case reporting (certified criterion f)(7))
- Interfaces for these require separate license and implementation fees per mandatory disclosures

**Population Health & Analytics**
- Population health management with risk stratification
- Gaps-in-care identification
- Care coordination workflows
- Quality measure tracking and reporting
- Custom analytics and reporting (clinical, operational, financial)
- Data accessible via web browser or mobile

**AI & Mobile**
- NextGen Ambient Assist: AI-powered ambient listening that converts doctor-patient conversations into structured SOAP notes (smartphone-based), with AI suggestions for ICD-10, medications, lab orders, and charge capture
- NextGen Intelligent Agent: voice and text command orchestration layer for EHR tasks
- Mobile EHR access for charting, messaging, task management
- Virtual scribe and dictation services

**Behavioral Health & Human Services**
- Integrated behavioral health suite for outpatient mental health, substance use disorder, crisis intervention, residential treatment, I/DD services (source: BusinessWire press release 2022)
- Autism documentation
- Home and community-based services documentation

**Dental Integration**
- Dental care functionality integrated with medical EHR, particularly for FQHCs (source: nextgen.com/markets/specialties/fqhc)
- Unified dental-medical-behavioral health records
- QSIDental (mentioned in mandatory disclosures as relying on NextGen Ambulatory EHR)

**Healthwise Patient Education**
- Optional patient education content (Healthwise), per-provider annual cost (source: mandatory disclosures)

### Data & Content

Based on the modules and features described above, NextGen Enterprise EHR stores and manages a wide range of clinical, administrative, and financial data:

**Clinical data** (directly evidenced by certified criteria and vendor materials):
- Patient demographics (name, DOB, sex, gender identity, sexual orientation, race, ethnicity, preferred language, address, contact info)
- Problem/diagnosis lists
- Medication lists and allergy lists
- Lab orders and results
- Diagnostic imaging orders
- Clinical notes / encounter documentation (including AI-generated SOAP notes)
- Vital signs
- Immunization records
- Implantable device data
- Family health history
- Social, psychological, behavioral data (social determinants)
- Clinical quality measure data
- Care plans
- Growth charts (for pediatrics, implied by CQMs)
- Referral data

**Administrative/scheduling data** (evidenced by PM module):
- Patient registration / demographic records (MPI)
- Appointment scheduling data (multi-location, multi-provider)
- Insurance/eligibility data
- Provider schedules and calendars

**Financial/billing data** (evidenced by RCM/PM modules):
- Claims data (professional claims with CPT/HCPCS, ICD-10 codes)
- Charge capture records
- Payment/remittance data
- Accounts receivable
- Cost estimates
- Denial/rejection records
- Payer contracts and fee schedules (implied by cost estimator)
- Financial analytics/reports
- Electronic statements

**Patient engagement data** (evidenced by portal features):
- Secure messages between patients and providers
- Patient-submitted intake forms and documents
- Patient survey responses
- Appointment reminder/recall communications
- Portal access logs

**Interoperability/exchange data**:
- C-CDA documents (sent and received)
- Direct messages
- FHIR API data
- Public health reports (immunizations, syndromic surveillance, cancer registry, case reports)

**Behavioral health data** (evidenced by BH suite):
- Mental health assessments
- Substance use disorder treatment records
- Crisis intervention documentation
- Residential treatment records
- I/DD service documentation

**Dental data** (for FQHC/CHC customers using integrated dental):
- Dental encounter records, integrated with medical chart

**Notable from mandatory disclosures**: The patient portal requires a per-provider license and monthly subscription. External connectivity solutions (lab interfaces, registry reporting, syndromic surveillance) require separate software license, implementation, and annual support fees. The Bulk C-CDA Export Utility requires billable hours for setup. Healthwise patient education is optional and costs extra per provider.

---

*Note: NextGen Office (the cloud-based small-practice product) is a separate product line and is not part of this certification.*

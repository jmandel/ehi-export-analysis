# Axxess — Product Research

Researched: 2026-02-15
Developer website: https://www.axxess.com

## Overview

Axxess Technology Solutions is a Dallas, TX-based healthcare technology company specializing in home-based care software. Founded in 2007 by John Olajide as a home healthcare consulting firm, Axxess pivoted to software in 2011 and has grown into a bootstrapped unicorn with approximately 1,000 employees. The company has not raised external venture funding. Axxess serves over 9,000 organizations, with more than 800,000 users, 7 million+ patients served, and $37 billion+ in claims processed. Its core market is home health agencies, hospice providers, home care organizations, and palliative care providers across the United States. The majority of its customers are small to mid-size agencies (20–49 employees).

Axxess offers a suite of cloud-based products for healthcare-at-home: **Home Health**, **Home Care** (skilled and private-pay), **Hospice**, and **Palliative Care** software platforms, along with ancillary solutions including Revenue Cycle Management, CAHPS surveys, staffing (Axxess CARE), training/compliance (Certification+), data exchange (Axxess Exchange), business intelligence, and an AI platform (Axxess Intelligence). The company holds ACHC, HITRUST, ISO 9001, and CHAP certifications.

## Product: Axxess Palliative

CHPL IDs: 11620

### What It Is

Axxess Palliative is a cloud-based electronic health record and practice management system designed specifically for palliative care delivery. The vendor describes it as "the first custom-built software solution designed specifically for the delivery of palliative care." It is a distinct product within the broader Axxess platform ecosystem, sharing integration points with Axxess' Revenue Cycle Management and other enterprise solutions but operating as its own certified product.

The certified module covers clinical documentation, CPOE, demographics, transitions of care, clinical quality measures, FHIR APIs, and direct messaging — a broad set of 27 ONC criteria including (a)(1) CPOE, (a)(5) demographics, (a)(12) family health history, (a)(14) implantable device list, (b)(1) transitions of care, (c)(1-3) clinical quality measures, (g)(7)/(g)(10) FHIR/API, and (h)(1) direct project.

The product targets physicians and nurse practitioners delivering palliative care services, typically in home-based settings. It is designed for outpatient/ambulatory palliative care as indicated by the CHPL SED description.

### Users & Market

Day-to-day users are physicians, nurse practitioners, clinical staff, and administrative/billing personnel at palliative care organizations. The product supports the unique workflow of palliative care — focused on symptom management, health goal planning, and quality of life rather than curative treatment.

Given that Axxess serves 9,000+ organizations overall, the palliative care product represents a newer and smaller segment of their customer base. The palliative care product was certified in March 2025 (version 3.0.2022), suggesting it has been in market for several years. No specific customer counts for the palliative product alone were found. The broader Axxess platform is well-reviewed, with an 81% satisfaction rating across ~417 reviews on third-party sites, and 87% of reviewers recommending Axxess products to others.

### Modules & Functionality

Based on vendor materials, help center documentation, and the product's navigation structure, Axxess Palliative includes the following functional areas:

**Intake/Scheduling**
- Patient intake workflows from referral through admission
- Patient scheduling with calendar and list views (14-day and monthly)
- Employee scheduling by branch, employment status, and team
- Color-coded task statuses (scheduled/completed/missed/pending)
- Bulk task creation and visit history tracking
- Filtering by branch, patient status (Active, Discharged, Pending, Non-Admitted, Deceased)
- Insurance eligibility checking within patient charts (per help center)

**Clinical Documentation**
- Physician/NP-focused visit documentation
- Comprehensive Plan of Care management
- Patient demographics with banner display (name, MRN, age, code status, diagnosis, insurance)
- Medication profiles and electronic Medication Administration Records (eMAR)
- Allergy documentation
- Infectious disease tracking
- Diagnosis documentation
- Vital signs recording
- Symptom ratings/assessments
- Physician communications
- Advance directives
- Emergency preparedness documentation
- Implantable device list (per certification criteria)
- Family health history (per certification criteria)
- Medi-Span drug database integration for drug interaction checking

**Orders Management**
- Medication orders (from medication profiles or clinical visits)
- DME (Durable Medical Equipment) orders
- Supply orders
- Other orders (e.g., discharge directives)
- Order creation from multiple pathways: patient/employee schedule, patient profile, medication profile, clinical visits
- Order read-back and verification workflow
- Prescribing provider auto-population and signature management
- Medication refill workflows with refill history tracking
- Orders flow to Comprehensive Plan of Care and IDG assessments

**IDG (Interdisciplinary Group) Center**
- IDG meeting scheduling and management
- Automated agenda and summary generation
- IDG Prep Report for clinical document verification
- Patient categorization by status (admission, active, discharge, death)
- Meeting history with agendas and sign-in sheets
- Team member and group management
- Hospice physician assignments
- Patient rosters prioritized by recertification urgency

**Billing**
- Direct Medicare Part B billing through Axxess' Network Service Vendor connection to Medicare
- Multi-payer billing through integration with Axxess Revenue Cycle Management
- Claims submission automation
- CPT code selection (including mobile CPT code selector with AI-assisted selection via Axxess Intelligence)
- Electronic Remittance Advice (ERA) processing
- Billing calculators

**Administration**
- Administrator dashboard
- Authorized contacts management
- Referral tracking
- Payer/insurance information management
- Pharmacy and DME vendor management

**Mobile**
- iOS and Android mobile apps
- Offline visit documentation with sync
- Talk-to-text documentation
- Mobile scheduling
- Mobile orders management
- Mobile CPT code selection

**Axxess Intelligence (AI)**
- AI-driven CPT code suggestion on mobile
- Other AI capabilities (details limited on the palliative-specific pages)

**Integrations**
- Axxess Revenue Cycle Management integration
- Axxess Exchange (secure data exchange)
- Medicare Network Service Vendor direct connection
- Medi-Span drug database
- Direct messaging (per h(1) certification)
- FHIR API (per g(10) certification)
- 40+ interoperable integrations noted for the broader Axxess platform

### Data & Content

Based on the features and help documentation, Axxess Palliative stores and manages the following data:

**Patient Data**: Demographics, contact information, addresses, MRN, age, code status, insurance/payer information, referral source, authorized contacts, emergency preparedness details, advance directives.

**Clinical Records**: Visit notes, vital signs, symptom ratings/assessments, diagnoses (including primary and secondary), medication profiles with eMAR, allergies, infectious disease status, implantable device list, family health history, Comprehensive Plan of Care, physician communications/notes, order documentation (medications, DME, supplies).

**Scheduling & Workflow Data**: Patient and employee schedules, task assignments and statuses, visit history, co-signature and addendum tracking.

**IDG Meeting Records**: Meeting schedules, agendas, summaries, sign-in sheets, team member assignments, patient review documentation.

**Billing & Financial Data**: Medicare Part B claims, multi-payer claims, CPT codes, ERA data, insurance eligibility records, billing calculations. The revenue cycle management integration suggests claims data and payment information flow through the system.

**Administrative Data**: Employee/staff profiles, branch assignments, team structures, pharmacy and DME vendor information, referral records.

**Audit & Compliance Data**: Per certification criteria (d)(1-9), the system maintains audit logs, authentication records, and security-related data.

The website does not explicitly mention patient portal/patient-facing access (no (e)(1) certification), and there is no mention of e-prescribing (no (a)(2) certification). Public health reporting beyond clinical quality measures is not certified. The product does not appear to include lab ordering or results management based on the absence of those certification criteria.

---

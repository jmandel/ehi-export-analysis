# TenEleven Group — Product Research

Researched: 2026-02-14
Developer website: https://ensorahealth.com/product/teneleven/

## Overview

TenEleven Group LLC is a small behavioral health EHR company originally based in East Amherst (Buffalo area), New York, with roughly 25–30 employees. The company was acquired by Therapy Brands as part of a roll-up strategy of behavioral health technology companies. Therapy Brands was subsequently acquired by KKR in 2021 and rebranded as **Ensora Health** in April 2025. TenEleven is now one of several products in the Ensora Health portfolio, alongside TheraNest (mental health solo/group practices) and Fusion (rehabilitation therapy). TenEleven is positioned as the enterprise-tier behavioral health EHR within the portfolio, targeting larger agencies (10+ users) rather than solo practitioners.

The product is called **electronic Clinical Record (eCR)** and serves behavioral health and human services agencies. Per press releases, "thousands of users in hundreds of offices" use eCR. Notable customers include Greenwich House (New York City, ~15,000 clients annually), New Brunswick Counseling Center, The Lennard Clinics, and Somerset Treatment Services (all New Jersey substance use treatment providers). The product is cloud/web-based and accessible from any location. Revenue estimates for TenEleven Group itself are around $7M annually, though it now operates under the much larger Ensora Health umbrella.

## Product: electronic Clinical Record (eCR)

CHPL ID: 11200

### What It Is

eCR is a comprehensive behavioral health EHR and practice management system designed for health and human services agencies. It covers the "end-to-end business process from intake to outcomes" including referral, scheduling, treatment, billing, discharge, and aftercare. The certified module (eCR v2.4) appears to be the core product itself — not a component of a larger platform. The product is ONC-certified with a very broad set of criteria spanning clinical data (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15), care transitions (b)(1)–(b)(3), patient portal (e)(1), public health reporting (f)(1)–(f)(3),(f)(5), and FHIR API access (g)(7),(g)(9),(g)(10).

The intended user description from CHPL is "Behavioral Health Clinics." Associated software listed on the ONC disclosures page includes eRx, Inpriva, and Dynamic Health IT.

### Users & Market

**Target settings:** Behavioral health agencies serving mental health, substance use/addiction treatment, and human services. The product supports multiple levels of care:
- Inpatient / residential (with bed management)
- Outpatient
- Home and Community Based Services (HCBS)
- Medication-Assisted Treatment (MAT) programs
- Trauma Informed Care programs

**Who uses it day-to-day:** Clinicians, prescribers, front desk staff, billing staff, and administrators at behavioral health agencies. The product is designed for multi-disciplinary care teams at agencies rather than solo practitioners.

**Customer examples:**
- Greenwich House (NYC) — consolidated multiple EHRs and paper billing into eCR for their mental and behavioral health services division, including MAT
- Three New Jersey substance use treatment agencies — implemented eCR with MAT and state health information exchange integration
- The product has particular traction in the northeast US, with NJ and NY state-level integrations

**Market position:** Small vendor now part of a larger PE-backed platform (Ensora Health / KKR). Competes in the behavioral health EHR niche. User reviews give it approximately 4.2/5 stars across ~19 reviews on third-party sites. Users praise ease of use and business process compliance; criticisms focus on system performance, reporting reliability, and limitations in advanced customization.

### Modules & Functionality

Based on vendor materials, the Ensora Health knowledge base structure, press releases, and third-party review sites, eCR includes the following modules and functionality:

**Clinical Documentation & FormLab:**
- Customizable clinical templates (FormLab) for creating electronic forms
- Extensive form library for behavioral health documentation
- Treatment planning with Goal/Objective Library
- Progress notes
- Clinical event notifications
- Documentation of medical necessity of services ("Golden Thread" concept — linking clinical documentation to billing justification)

**Medication-Assisted Treatment (MAT):**
- Dosing schedules and medication management
- Prescription tracking and medication adherence monitoring
- Tapering plans
- Secure patient check-in with on-screen photo verification before dispensing
- Support for liquid and tablet medication dispensing
- DEA and CMS compliance
- This is a major differentiator for the product

**E-Prescribing:**
- Electronic prescription delivery to pharmacies
- Safety checks
- Listed as associated software: "eRx"

**E-Labs:**
- Electronic lab ordering

**Medication Administration Record (MAR):**
- Tracking of medication administration in inpatient/residential settings

**Bed Management:**
- Bed assignment, monitoring, and availability tracking
- Occupancy management for residential/inpatient facilities
- Resident status tracking

**Scheduling:**
- Client scheduling with alerts
- Appointment management with integrated calendars

**Billing & Revenue Cycle Management (RCM):**
- Electronic primary and secondary claims submission
- One-click batch claim submission
- Payment reminders to clients
- ERA and EOB file processing
- Daily billing reports
- Integrated credit card processing
- Patient statements
- Flexible billing triggers linked to clinical documentation, attendance, "head on pillow," etc.

**Patient Portal:**
- Patient access to records, schedules, and educational materials
- Certified under (e)(1) for View, Download, Transmit

**Compliance & Reporting:**
- DSM-5 compliance support
- Performance/outcomes dashboards
- Business intelligence with ad-hoc data visualizations
- Reporting services for regulatory requirements
- Alert management
- CCBHC (Certified Community Behavioral Health Clinic) support
- Integration with state systems (e.g., NJ Prescription Drug Monitoring Program, NJ Substance Abuse Monitoring System)

**Intake & Referral Management:**
- Referral intake from first call through admission

**Care Transitions:**
- Discharge planning and aftercare coordination
- Certified for (b)(1) Transitions of Care, (b)(2) Clinical Information Reconciliation, (b)(3) Electronic Prescribing

**Public Health Reporting:**
- Certified for (f)(1) Transmission to Immunization Registries, (f)(2) Transmission to Public Health Agencies — Syndromic Surveillance, (f)(3) Transmission to Public Health Agencies — Reportable Conditions, (f)(5) Cancer Case Reporting

**Interoperability:**
- Health Information Exchange integration (demonstrated in NJ deployments)
- FHIR API endpoint at fhir.10e11.com
- Certified for (g)(10) Standardized API

**Staff & User Management:**
- Access levels, user management, and permissions
- Clinician mapping

### Data & Content

Based on the features and modules described above, eCR manages a broad set of data for behavioral health agencies:

**Clinical data:** Patient demographics, visit history, treatment plans, progress notes, clinical assessments, goals/objectives, diagnoses (DSM-5), clinical forms/templates (via FormLab), clinical event notifications, and documentation of medical necessity.

**Medication data:** Prescriptions (e-prescribing), medication administration records (MAR), MAT dosing schedules, medication adherence tracking, tapering plans, dispensing records with patient verification.

**Lab data:** Lab orders (e-labs) and presumably lab results.

**Scheduling data:** Appointments, calendars, scheduling alerts.

**Billing/financial data:** Claims (primary and secondary), ERA/EOB files, payment records, credit card transactions, patient statements, daily billing reports, billing triggers linked to clinical documentation.

**Bed management data:** Bed assignments, occupancy records, resident status for inpatient/residential settings.

**Patient portal data:** Patient-facing records, educational materials, and presumably secure messaging.

**Intake/referral data:** Referral information, intake documentation through discharge and aftercare records.

**Compliance/reporting data:** Regulatory reports, performance dashboards, outcomes data, public health reporting submissions.

**Staff/administrative data:** User accounts, access levels, clinician mappings, organizational configuration.

**Notable:** The ONC disclosures mention that export formats depend on "software version in use, documentation practices, and configuration decisions" — suggesting the data model is quite flexible and varies by implementation. The FormLab feature for custom forms means that individual agencies may capture quite different data depending on their configuration.

---

## Research Gaps

- The original TenEleven website (10e11.com) now redirects to Ensora Health, so historical product detail pages are no longer directly accessible.
- Capterra returned a 403 error, so detailed user reviews could not be accessed directly (summary ratings were available via other sources).
- The behavioralis.org guide was unavailable (522 error).
- Exact customer count is not publicly disclosed beyond "hundreds of offices" and "thousands of users."
- It is unclear whether the product has distinct modules that are licensed separately vs. a single integrated platform. Pricing is custom and not publicly listed.

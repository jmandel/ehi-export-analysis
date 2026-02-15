# Juno Health — Product Research

Researched: 2026-02-14
Developer website: https://www.junohealth.com

## Overview

Juno Health is a division of Document Storage Systems, Inc. (DSS, Inc.), a healthcare IT company founded in 1991 and headquartered in North Palm Beach, Florida. DSS has deep roots in the Department of Veterans Affairs, having provided VistA-integrated software and services to the VA for over 30 years. The parent company has 700+ employees and also operates SBG Technology Solutions (acquired in 2021) as a subsidiary focused on federal services.

Juno Health was launched in 2018 as DSS's commercial EHR brand, debuting at HIMSS 2019. The product is cloud-native and positioned primarily for acute care hospitals (especially critical access and rural hospitals), behavioral health facilities, state mental health systems, and public health agencies. Juno Health was ranked #1 EHR vendor for rural hospitals by Black Book Market Research in 2025. Notable customers include state health departments (Florida, Tennessee, Idaho, New York) and rural hospitals like Bibb Medical Center and Oroville Hospital. The Tennessee Department of Health selected Juno as its statewide public health EHR.

DSS's heritage is significant context: the parent company built numerous clinical applications for the VA ecosystem, including pharmacy (RxTracker), order tracking, perioperative care, mental health, dental, dialysis, infection control (TheraDoc), and document management — all integrated with VistA/CPRS. Juno EHR represents the commercialization and modernization of this clinical software experience into a cloud-based product for non-VA markets.

## Product: Juno EHR

CHPL IDs: 11497

### What It Is

Juno EHR is a cloud-native, ONC-certified electronic health record system serving acute care, behavioral health, state mental health, and public health settings. It is the core certified product from Juno Health. The certification is broad, covering clinical data criteria (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15), transitions of care (b)(1)–(b)(2), clinical quality measures (c)(1)–(c)(3), FHIR APIs (g)(10), syndromic surveillance (f)(2), and the EHI export (b)(10)/(b)(11). Intended users are described as "clinical prescribers and staff."

The certifications page lists six separately certified ONC products/modules under the Juno/DSS umbrella:
1. **Juno EHR v24** — the core EHR (this certification)
2. **Juno ConnectEHR 22** — data exchange/interoperability module
3. **Juno CQMsolution 22** — clinical quality measure reporting
4. **RxTracker v9** — e-prescribing (originated as a VA product for VistA-integrated prescribing to retail pharmacies via Surescripts)
5. **JESS v3.2** — Juno Emergency Services Solution
6. **Juno Patient Portal v23** — patient-facing portal

It is unclear from available materials exactly how these certified modules compose into the single "Juno EHR" product offering — they may be bundled together as one integrated platform, or some may be optional add-ons.

### Users & Market

**Clinical settings:** Critical access and rural hospitals, acute care hospitals, behavioral health hospitals, state mental health facilities, public health agencies. The vendor does not appear to target ambulatory physician practices or large academic medical centers, though "ambulatory" and "population health" solutions have been mentioned in prior marketing.

**End users:** Physicians, nurses, pharmacists, behavioral health clinicians, case managers, clinical documentation staff, and (via the patient portal) patients.

**Customer scale:** The vendor serves state-level health departments (Tennessee DOH statewide, Florida, Idaho, New York) and individual hospitals. Exact customer counts are not published, but the #1 Black Book ranking for rural hospitals suggests meaningful market presence in that niche.

**Go-to-market:** Appears to be direct sales, with significant government/public-sector experience from DSS's VA heritage. The company presents at HIMSS and government health IT summits.

### Modules & Functionality

Based on vendor website, product pages, and third-party feature lists, Juno EHR includes the following modules and capabilities:

**Clinical Documentation:**
- Clinical Content Builder — low-code/no-code tool for building custom templates, assessments, and workflows without vendor involvement; 400+ pre-built templates for behavioral health, substance use, and infection control
- Clinical Action Center ("Clin Doc") — consolidated nursing workflow with customizable panels, color-coded calendars, smart task lists, flowsheets, assessments, and notes
- Build a Module (BAM) — configurable data management with custom columns, filters, and objects
- Chart Review — clinical documentation auditing and compliance tracking
- AI Scribe — captures clinical conversations on any web-connected device, supports 3+ speakers in 50+ languages

**Orders & Medications:**
- Order Management — "learns individual user behaviors and adapts to consolidate order configuration"
- E-Prescribing — native integration with Surescripts, CoverMyMeds for prior authorization, PDMP integration, EPCS with two-factor authentication, real-time drug data from First Data Bank
- Pharmacy module (behavioral health) — dual monitor support, barcode medication administration (BCMA), electronic medication administration records (eMAR), safety checks
- Medication reconciliation at admission and discharge

**Emergency Department:**
- JESS (Juno Emergency Services Solution) — automated documentation prompts, clinical decision support, real-time monitoring
- Designed for ED-specific workflows

**Behavioral Health:**
- Treatment Plans with pre-configured behavioral health templates, auto-populated diagnoses and medications, goals/objectives/interventions tracking
- Group Notes — document group therapy for multiple patients simultaneously with individualized details
- Session Manager — manages wait lists and provider availability
- "Golden Thread" concept — links admission assessment → treatment plan → clinical notes → outcomes → discharge in a continuous chain
- 150+ behavioral health assessments
- Case management via ProDash

**Surgery / Perioperative:**
- Perioperative nursing documentation compliant with AORN standards

**Public Health:**
- Immunization registry with real-time data exchange, vaccine inventory tracking, mass clinic support
- Disease surveillance and monitoring with standards-based coding (ICD-10, SNOMED, LOINC)
- Outbreak response tools
- Population health monitoring and forecasting

**Revenue Cycle Management:**
- Integrated billing with charge posting, claim submission, ERA (electronic remittance advice) processing
- Described in the acute care product feature list

**Patient Engagement:**
- Patient Portal (separately certified as Juno Patient Portal v23) — secure messaging, appointment scheduling, prescription refill requests, 24/7 health information access

**Dashboards & Analytics:**
- ProDash — real-time dashboard showing lab results, vitals, consults, new admissions, case management workload
- Customizable reports for forecasting, population health management, and quality initiatives

**Scheduling:**
- Appointment scheduling integrated with clinical workflows and treatment plans

**Interoperability:**
- ConnectEHR (separately certified) — data exchange module
- HL7 FHIR APIs, USCDI compliance
- Integrations with lab information systems, billing/RCM platforms, public health reporting systems, scheduling tools, and telehealth applications

**Quality Reporting:**
- CQMsolution (separately certified) — clinical quality measure reporting and submission

**Infrastructure:**
- Cloud-native, single-tenant architecture with isolated deployments
- Enterprise governance — customization at facility, department, or role level
- SOC 2 Type 2, HIPAA, ISO 9001, CMMI DEV Level 3 certified
- Pursuing FedRAMP High certification

### Data & Content

Based on the modules and features described above, Juno EHR manages the following categories of data:

**Clinical records:** Patient demographics, problem lists, medication lists, medication allergy lists, clinical notes and assessments (400+ templates), vital signs, lab results, flowsheets, consult records, admission/discharge records. The (a)(1)–(a)(5) certifications confirm CPOE, demographics, problem list, medication list, and medication allergy list capabilities.

**Orders and prescriptions:** Medication orders, e-prescriptions (including controlled substances via EPCS), laboratory orders, imaging orders (implied by order management). Prescription tracking via Surescripts integration. Prior authorization data via CoverMyMeds.

**Behavioral health data:** Treatment plans with goals/objectives/interventions, group therapy notes, individual session notes, behavioral health assessments (150+), substance use documentation, session scheduling and wait list data. The "Golden Thread" design suggests detailed longitudinal behavioral health records linking assessments through treatment to outcomes.

**Medication administration:** BCMA records, eMAR data, pharmacy safety check logs (behavioral health pharmacy module).

**Surgical/perioperative data:** AORN-compliant perioperative nursing documentation, surgical records.

**Emergency department data:** ED visit documentation, triage data, clinical decision support alerts.

**Public health data:** Immunization records, vaccine inventory, disease surveillance data, outbreak response records, population health metrics. Standards-based coding with ICD-10, SNOMED, LOINC.

**Revenue cycle data:** Charges, claims, electronic remittance advice (ERA), billing records. Revenue cycle management is described as integrated in the acute care product.

**Patient portal data:** Secure messages, appointment requests, prescription refill requests.

**Quality measures:** CQM data (separately certified module).

**Administrative data:** Scheduling/appointment data, user/role configurations, facility/department settings.

**Audit and compliance data:** Chart review/audit records, the (a)(12) certification for family health history, (a)(14) for implantable device list, (a)(15) for social/psychological/behavioral data.

**Notable gaps in information:** The vendor website does not describe document scanning/management capabilities in detail (despite DSS's origins in document storage). It's unclear whether imaging/radiology data is stored within the EHR or handled by external PACS. Lab interfaces are mentioned but lab result storage details are implied rather than explicit. The relationship between the separately certified modules (ConnectEHR, CQMsolution, RxTracker, JESS, Patient Portal) and the core Juno EHR certification is not fully clear — they may share a single database or operate as loosely coupled components.

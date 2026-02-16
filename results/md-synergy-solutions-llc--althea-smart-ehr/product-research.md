# MD Synergy Solutions, LLC — Product Research

Researched: 2026-02-15
Developer website: https://mdsynergy.com

## Overview

MD Synergy Solutions, LLC is a small health IT company founded in 2000 and headquartered in Calabasas, California. The company has approximately 50–70 employees (sources vary). MD Synergy offers an integrated suite of cloud-based products for ambulatory medical practices: **Althea Smart EHR** (the electronic health record) and **mds:practice** (practice management and billing). The company targets independent physician practices and multi-specialty groups across a range of ambulatory specialties including internal medicine, family medicine, pediatrics, dermatology, psychiatry, pain management, surgery, orthopedics, and podiatry.

Althea Smart EHR is marketed as an "AI-Powered Mobile EHR" with a strong emphasis on iOS/iPad accessibility, voice-to-text documentation, and telemedicine. The company has received positive ratings on Capterra, Software Advice, and GetApp. Pricing starts at $295/provider/month with tiered plans (Basic $200, Standard $540, Premium $640, Enterprise custom). The company appears to sell direct to practices; no evidence of channel partners or reseller relationships was found.

## Product: Althea Smart EHR + mds:practice

CHPL ID: 11046 (Althea Smart EHR Version 3.0, certified 2022-12-05)

### What It Is

Althea Smart EHR is a cloud-based electronic health record system designed for ambulatory and outpatient clinic settings. It is paired with **mds:practice**, a separate but integrated practice management and billing system. Together, they form MD Synergy's complete platform for running a medical practice — covering clinical documentation, e-prescribing, labs, patient engagement, scheduling, billing, and claims management.

The ONC-certified module is Althea Smart EHR, but the broader product ecosystem includes mds:practice for billing/PM. The CHPL certification covers clinical criteria (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15), transitions of care (b)(1)–(b)(3), patient portal (e)(1), clinical quality measures (c)(1)–(c)(3), FHIR APIs (g)(7), (g)(10), direct messaging (h)(1), and EHI export (b)(10). This is a broad certification indicating full-stack ambulatory EHR capabilities.

### Users & Market

**Target users**: Physicians, clinical staff, and practice administrative/billing staff at ambulatory practices. The SED intended user description is "Ambulatory, Outpatient Clinic."

**Clinical settings**: Independent practices, multi-specialty groups, health centers, and small to mid-size outpatient clinics. The vendor lists support for multi-location and multi-practice management.

**Specialties served**: Internal medicine, family medicine, pediatrics, dermatology, psychiatry, pain management, surgery specialties, orthopedics, podiatry, and others.

**Company size**: ~50–70 employees, a small niche vendor. No information was found on total customer count or number of practices/providers using the system. The company appears to serve primarily small to mid-size practices. No notable large health system deployments or case studies were found.

### Modules & Functionality

Based on vendor website and third-party review sites, the MD Synergy platform includes the following:

**Clinical Documentation (Althea Smart EHR)**
- AI-powered ambient listening that transcribes patient-clinician conversations into structured clinical notes (vendor website)
- Voice-to-text documentation powered by Nuance speech recognition (Medigy, vendor website)
- Smart phrases and customizable templates for efficient charting (vendor website)
- Encounter notes with structured fields for visits, orders, diagnoses, and treatments (FindEMR, vendor website)

**Computerized Provider Order Entry (CPOE)**
- Medication ordering with drug-drug and drug-allergy interaction checking (certified criteria (a)(1), (a)(4))
- Laboratory order entry (certified (a)(2))
- Imaging/radiology order entry (certified (a)(3))

**E-Prescribing**
- Electronic prescribing including EPCS (electronic prescribing of controlled substances) via Surescripts and NewCrop integrations (vendor interfaces page)

**Laboratory & Radiology**
- Integrated lab ordering and results with Quest Diagnostics, Labcorp, Sonora Quest (vendor interfaces page)
- Radiology integration with Arizona Diagnostic Radiology, SimonMed Imaging (vendor interfaces page)
- HL7-based interfaces for lab/radiology data exchange

**Patient Portal (Althea Health)**
- Patient access to health records, lab results, appointments, and billing details (vendor patient portal page)
- Online payment of balances via credit card
- Patient demographic and clinical information self-update
- Electronic submission of forms and consent documents
- Messaging between patients and care team
- Remote check-in with pre-visit paperwork completion
- Apple Health app data sharing — patients can share iPhone Health data directly into the EHR (vendor patient portal page)

**Telemedicine**
- Integrated HIPAA-compliant HD video/audio conferencing (vendor website)
- Real-time document sharing during virtual visits
- Patient satisfaction surveys post-visit
- Zoom integration available (vendor interfaces page)

**Scheduling & Practice Management (mds:practice)**
- Multi-location appointment scheduling with real-time calendar management (mds:practice page)
- Patient check-in/check-out tracking
- Visit pattern monitoring
- Automated appointment reminders via text and email (HIPAA-secure)
- ZocDoc integration for online scheduling (vendor interfaces page)

**Billing & Revenue Cycle (mds:practice)**
- Automated claim generation from closed clinical notes — ICD and CPT codes auto-populate (mds:practice page)
- Electronic claim submission via integrated clearinghouses: Change Healthcare, Emdeon, Trizetto, Waystar, Office Ally (vendor interfaces page)
- Electronic remittance advice (ERA) receipt and automated payment posting
- Paper HCFA claim printing
- Patient statement generation (direct print or automated via BillFlash, 6 customizable formats)
- Insurance eligibility verification (real-time, pre-visit or on-demand)
- Denial tracking
- Credit card payment processing (vendor interfaces page)

**Communication & Messaging**
- Patient SMS text messaging via Twilio integration (vendor interfaces page)
- Cloud fax functionality
- Internal chat system
- Direct messaging for care coordination (certified (h)(1))

**Health Information Exchange**
- HIE connectivity with organizations including Aledade Inc., Apple Inc., Providence, Rivet Health (vendor interfaces page)
- Transitions of care / C-CDA document exchange (certified (b)(1)–(b)(3))

**Clinical Quality & Reporting**
- Clinical quality measures (CQM) tracking — 16 CMS measures (mandatory disclosures page)
- MIPS compliance support
- Population health analysis tools
- Reporting and analytics

**Public Health Reporting**
- State immunization registry interfaces (vendor interfaces page)
- Certified for syndromic surveillance (certified (b)(11))

**FHIR API Access**
- Patient and population services FHIR APIs (certified (g)(7), (g)(9), (g)(10))

**Administrative**
- Patient kiosk system for in-office check-in
- Document management
- Compliance tracking
- Multi-location and multi-practice management

### Data & Content

Based on the features and integrations described above, the Althea Smart EHR + mds:practice platform manages the following data:

**Clinical Data** (well-evidenced by certified criteria and vendor materials):
- Patient demographics and contact information
- Clinical encounter notes and visit documentation (including AI-transcribed ambient notes)
- Problem lists, medication lists, medication allergy lists (certified (a)(5), (a)(1))
- Vital signs and growth charts (implied by ambulatory EHR)
- Diagnoses (ICD codes)
- Procedure codes (CPT codes)
- Lab orders and results (Quest, Labcorp integrations)
- Radiology/imaging orders and results
- Medication orders and prescription history (Surescripts/NewCrop)
- Clinical decision support interventions (certified (a)(12))
- Implantable device data (certified (a)(14))
- Social, psychological, and behavioral data (certified (a)(15))

**Practice Management & Financial Data** (evidenced by mds:practice features):
- Appointment schedules and visit history
- Insurance eligibility verification records
- Claims data (electronic and paper)
- ERA/remittance records
- Patient statements and balances
- Payment records (credit card transactions)
- Denial tracking data

**Patient-Generated & Portal Data**:
- Patient portal messages
- Patient-submitted forms and consent documents
- Patient self-reported demographic updates
- Apple Health app data (for iPhone users)
- Patient satisfaction survey responses

**Communication Data**:
- SMS text messages to patients (Twilio)
- Cloud fax records
- Internal chat messages
- Direct messages (care coordination)

**Reporting & Quality Data**:
- Clinical quality measure calculations
- MIPS reporting data
- Immunization registry submissions

**Notable gaps/uncertainties**:
- The website does not mention referral management in detail, though FindEMR lists it as a feature. Unclear how robust this is.
- No mention of care plan documentation beyond what's in encounter notes.
- No mention of a separate document scanning/imaging module, though "document management" is listed as a feature.
- The relationship between Althea Smart EHR and mds:practice data is somewhat opaque — it's unclear whether they share a database or are separate systems with data exchange between them. The vendor presents them as integrated but distinct products.
- No information found about data archiving, audit logs exposed to users, or how historical data is managed.

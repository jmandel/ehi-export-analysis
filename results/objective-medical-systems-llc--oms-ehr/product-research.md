# Objective Medical Systems, LLC — Product Research

Researched: 2026-02-16
Developer website: https://objectivemedicalsystems.com/

## Overview

Objective Medical Systems (OMS) is a small, privately held health IT company headquartered in Houma, Louisiana, founded in 2007–2008 by practicing cardiologists Dr. Vinod Nair, Dr. Peter Fail, and Dr. Richard Abben. The company has approximately 17 employees (per PitchBook) and focuses exclusively on cardiovascular medicine. Their tagline is "built for cardiologists, by cardiologists." Dr. Nair serves as President and Chief Software Architect; Colby LeMaire is CEO. The company was part of the New Orleans BioInnovation Center startup ecosystem, and Dr. Nair was named to the Silicon Bayou 100 list of Louisiana tech innovators.

OMS serves mid-size to large cardiology practices and hospital cardiology service lines. Their named customers include the Cardiovascular Institute of the South (CIS) — the largest single-specialty cardiology practice in Louisiana — Midwest Cardiovascular Institute, and Lane Regional Medical Center. They have a partnership with MedAxiom, described as the nation's leading cardiovascular performance community. The company has no disclosed venture funding, no G2 presence, and almost no independent reviews (one 5-star review on Software Finder from 2016). This is consistent with a very niche vendor serving a small number of specialized customers.

## Product: OMS EHR

CHPL ID: 11751 (OMS EHR Version 6, certified January 8, 2026, Drummond Group ONC-ACB)

### What It Is

OMS EHR is a cardiology-specific electronic health record with an integrated cardiovascular information system (CVIS). It is ONC-certified (HTI-1) with broad criterion coverage: clinical data (a)(1)–(a)(5), (a)(12), (a)(14); transitions of care (b)(1)–(b)(3); patient portal (e)(1); FHIR APIs (g)(7)–(g)(10); clinical quality measures (c)(1)–(c)(3); and public health reporting (f)(7). The SED intended user description is "Medical/Cardiology."

The certified module appears to be the core of a broader product ecosystem that also includes diagnostic reporting, chronic care coordination, AI-powered analytics, and remote patient monitoring — but the EHR is the central certified product.

The system runs on a **Windows/SQL Server on-premises architecture** (Windows 2008 Server R2, SQL Server 2008, .NET 4.7, IIS per the disclosures page). Cloud infrastructure is used for e-prescribing services via ClearDATA.

### Users & Market

**End users:** Cardiologists, cardiology practice staff, diagnostic technicians, and care coordinators. The SED description confirms the target is medical/cardiology users.

**Clinical settings:** Single-specialty cardiology practices ranging from individual hospital departments (Lane Regional Medical Center) to large multi-site groups (Cardiovascular Institute of the South with system-wide deployment). Also serves practices within the MedAxiom network.

**Customer count:** Not publicly disclosed. The named reference customers are CIS, Midwest Cardiovascular Institute, and Lane Regional Medical Center. The extremely thin review footprint (1 review across all platforms) suggests a small installed base, likely dozens of sites rather than hundreds.

**Market position:** Niche cardiology EHR. Appears on "best of" lists for cardiology EHR systems (EHR in Practice, FindEMR). Competes in a specialized segment against larger EHR vendors that serve cardiology among other specialties.

### Modules & Functionality

Based on the vendor website, disclosures page, third-party reviews, and press releases, OMS EHR includes:

**Core EHR:**
- Cardiology-specific charting and documentation
- Input via traditional typing, e-Ink, handwriting recognition, voice transcription (Nuance integration), and cardiology-specific templates
- Clinical decision support (drug-drug interactions, drug-allergy checks)
- Problem lists, medication management, patient demographics
- Claims to process 6,000+ data points per patient (vendor homepage)

**Cardiovascular Diagnostic Reporting (OMS Diagnostics):**
- 16 structured reporting modules covering all major cardiovascular diagnostic modalities:
  - Echocardiography
  - EKG/ECG
  - Stress testing
  - Nuclear/myocardial perfusion imaging
  - Catheterization lab / invasive cardiology (including 3D heart imaging)
  - Vascular studies
  - Holter/ambulatory monitoring
- This is a core differentiator — the CVIS is tightly integrated with the EHR, not a separate system

**e-Prescribing (CPOE):**
- Surescripts integration for electronic prescribing with real-time formulary and benefits checking
- Drug database licensing fee (noted on disclosures page)
- E-prescribing infrastructure hosted on ClearDATA HIPAA-compliant cloud

**Clinical Quality Measures:**
- Certified on 14 CQMs, heavily cardiology-relevant: CMS22v6 (preventive care/blood pressure screening), CMS50v6 (closing referral loop), CMS65v7 (hypertension improvement), CMS68v7 (documentation of current meds), CMS69v6 (BMI screening), CMS122v6 (diabetes HbA1c control), CMS134v6 (diabetes nephropathy), CMS135v6 (heart failure ACE/ARB), CMS138v6 (tobacco screening), CMS144v6 (heart failure beta-blocker), CMS145v6 (CAD beta-blocker), CMS156v6 (high-risk medications in elderly), CMS164v6 (IVD aspirin), CMS165v6 (hypertension control)

**Transitions of Care & Messaging:**
- Direct secure messaging via Updox
- C-CDA generation and receipt (certified for (b)(1)–(b)(3))

**Patient Access:**
- Patient portal / view-download-transmit (certified for (e)(1))
- Patient mobile app mentioned on vendor website

**FHIR API Access:**
- Certified for (g)(7)–(g)(10) — standardized API for patient and population services

**Coding Support:**
- ICD-9/ICD-10 coding via IMO (Intelligent Medical Objects) — service fee
- CPT coding support

**OMS C3 (Chronic Care Coordinator):**
- Remote Patient Monitoring (RPM) for chronic cardiovascular conditions
- Chronic Care Management (CCM) workflows
- Transitional Care Management (TCM)
- Bluetooth-enabled device integration for blood pressure, heart rate monitoring
- Used by Midwest Cardiovascular Institute for their "Cardio@Home" program (May 2025)
- Launched in 2017 per BusinessWire press release

**AI-Powered Features (introduced 2024):**
- **AskOMS** — AI clinical assistant
- **Diagnosis Detection** — Named entity recognition to identify diagnoses from assessment/plan text; supports coding enhancement
- **Clinical Trial Identification** — Patient-to-trial matching
- **Patient No-Show Prediction** — Predictive analytics for scheduling

**Operational Tools:**
- **Trace Analytics / Cardiolytica** — Population health analytics (launched 2018)
- **Patient Recall** — Automated patient outreach and recall
- **Smart Scan** — Automated document filing into the EHR
- **Patient Risk Assessment** — Framingham Risk Scorecard

**Revenue Cycle:**
- Revenue cycle management is mentioned on the vendor homepage as part of the product's capabilities, though detail is limited

**Lab Integration:**
- Lab results integration is referenced in the context of clinical decision support and diagnostic workflows

### Data & Content

Based on the modules and features described above, OMS EHR stores and manages:

**Clinical data (directly evidenced):**
- Patient demographics and clinical history
- Cardiovascular diagnostic reports across all modalities (echo, EKG, stress, nuclear, cath lab, vascular, Holter) — this is the product's core strength, with 16 structured reporting modules
- Problem lists, diagnoses, conditions
- Medications and prescriptions (Surescripts e-prescribing)
- Allergies and drug interactions
- Lab results
- Vital signs (including remote monitoring data — blood pressure, heart rate via Bluetooth devices)
- Clinical notes and assessments (with AI-assisted diagnosis detection)
- Immunizations (implied by (a)(14) certification)
- Care plans
- Procedures and surgical data (cath lab reporting implies procedural data)

**Documents and imaging:**
- Scanned documents (Smart Scan auto-filing)
- Diagnostic images associated with cardiovascular studies
- Binary/media content (implied by CVIS integration)

**Administrative and operational data:**
- Scheduling and appointments (patient no-show prediction implies appointment data)
- Patient recall records
- Clinical quality measure data and reporting
- Revenue cycle / billing data (mentioned but with limited detail — unclear how deep billing functionality goes vs. external billing integration)
- Referral tracking (CMS50 closing the referral loop implies referral data)
- Audit events (certified for (d)(2)–(d)(3))

**Patient-generated and remote monitoring data:**
- RPM device readings (blood pressure, heart rate) via C3 platform
- Chronic care management encounter data
- Transitional care management data

**Exchange data:**
- C-CDA documents (sent and received)
- Direct secure messages (via Updox)
- FHIR resources (via certified API endpoints)

**What's unclear:**
- The depth of billing/revenue cycle functionality — whether OMS handles full claims management, charge capture, and ERA/EOB processing, or whether billing is primarily handled by external practice management systems. The disclosures page mentions CPT coding and ICD coding fees but doesn't describe claims submission.
- Whether there is a separate practice management system or if PM functionality is embedded in the EHR
- The extent of patient portal data (messaging, appointment requests, bill pay, etc.)
- Whether clinical trial matching data and AI analytics data are stored within the EHR database or in separate systems

---

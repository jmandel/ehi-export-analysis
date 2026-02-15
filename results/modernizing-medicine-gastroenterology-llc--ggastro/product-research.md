# Modernizing Medicine Gastroenterology, LLC — Product Research

Researched: 2026-02-15
Developer website: https://www.modmed.com

## Overview

Modernizing Medicine (ModMed) is a major specialty-focused EHR vendor founded in 2010 in Boca Raton, Florida by Daniel Cane (previously co-founded Blackboard, Inc.) and Dr. Michael Sherling, a practicing dermatologist. The company's thesis is specialty-specific EHR software built by practicing physicians, rather than one-size-fits-all systems. ModMed now serves 11 medical specialties (allergy, dermatology, gastroenterology, OBGYN, ophthalmology, orthopedics, otolaryngology, pain management, plastic surgery, podiatry, and urology) plus ambulatory surgery centers (ASCs). As of early 2025, ModMed reports 40,000+ providers and 160,000+ healthcare professionals on its platform. In March 2025, Clearlake Capital acquired a majority stake at a $5.3 billion valuation — the largest healthcare-sector leveraged buyout that year. Previous majority investor was Warburg Pincus (since 2017).

The gastroenterology product line originates from **gMed, Inc.**, a Weston, FL-based GI-specific EHR vendor that ModMed acquired in September 2015. gMed was formally rebranded to "Modernizing Medicine Gastroenterology" at ACG 2018. The gGastro product is a **distinct platform** from ModMed's other main EHR platform (EMA — Electronic Medical Assistant, which serves dermatology, ophthalmology, orthopedics, and other specialties). Both platforms share branding and some infrastructure (e.g., the certified FHIR API), but gGastro has its own architecture and product history.

## Product: gGastro

CHPL IDs: 11054

### What It Is

gGastro is a **specialty-specific EHR platform for gastroenterology** — not a module within a general EHR, but a standalone product suite purpose-built for GI practices and ambulatory surgery centers. It encompasses an EHR, an endoscopy report writer (ERW), practice management, patient engagement tools, analytics, and revenue cycle management. The certified product is the full gGastro suite, not a single component.

The current version is 6.x (v6.4 deployed April 2025; the CHPL-certified version is 6, certified December 2022). gGastro is available as cloud-based SaaS, though some legacy clients still run on-premises servers. It is accessible via web, iOS, and Android.

gGastro is distinct from ModMed's EMA platform. While EMA serves dermatology, ophthalmology, orthopedics, and other specialties from a common codebase with specialty content libraries, gGastro has its own architecture inherited from the gMed acquisition. Both share the ModMed brand, the certified FHIR API, and some backend services (revenue cycle, patient engagement), but they are architecturally separate products.

### Users & Market

**Intended users:** MD, PA, MA, Nurse, Administrator (per CHPL metadata). In practice, this means gastroenterologists, physician assistants, medical assistants, nursing staff (particularly procedure/recovery nurses), and practice administrators/billing staff.

**Market position:** gGastro is the dominant GI-specialty EHR in the United States. It has ranked **#1 in gastroenterology** in the Black Book survey every year since Black Book began polling in 2010 — at least 15 consecutive years. In 2024 and 2025, ModMed ranked #1 in all 11 of its specialty EHR categories per Black Book (2025 survey: 33,516 respondents). ModMed was also the highest-ranking EHR provider in G2's 2025 Best Healthcare Software Products category.

**Customer count:** The exact number of gGastro customers is not publicly disclosed. The 6sense web-signal tracker identified ~28 companies, but this is clearly a massive undercount given 15 years of market dominance. The actual number is likely in the hundreds or low thousands of GI practices and ASCs. Named customers include Gastro Care Partners (a large MSO), Covenant Surgical Partners, Gastrointestinal Associates of Northeast Tennessee, Tri-County Gastroenterology, Digestive Disease Clinic, DiMarino-Kroop-Prieto Gastrointestinal Associates, and Woodholme Gastroenterology Associates.

**Clinical settings:** Private GI practices (solo and multi-provider), multi-site gastroenterology groups, ambulatory surgery centers (ASCs), and hospital-based endoscopy suites. The product is designed for ambulatory GI — not inpatient hospital systems.

**Competitive landscape:** Competes with general-purpose EHRs (Epic, athenahealth, eClinicalWorks, NextGen) and occasional GI-focused tools, but is the dominant purpose-built option for gastroenterology. Its primary competitive advantage is the integrated endoscopy report writer and GI-specific clinical content.

### Modules & Functionality

gGastro is sold as a suite of integrated components. Based on vendor materials and product pages:

**gGastro EHR** — The core electronic health record for gastroenterology. Cloud-based, specialty-specific. Features include:
- GI-specific clinical documentation with customizable templates
- Learning system that prioritizes common GI treatments and diagnoses based on provider preferences (draws on a large de-identified dataset)
- Suggested ICD-10 coding for billing accuracy
- Problem lists, medication management, allergy tracking
- Clinical decision support
- CPOE (computerized provider order entry) for medications, labs, and imaging
- Drug-drug and drug-allergy interaction checking
- Patient demographics and insurance information
- Medical history and family history
- Immunization records
- Implantable device tracking
- Direct messaging (transitions of care via C-CDA)
- E-prescribing (via Surescripts integration — certified for (b)(11))
- Quality measure tracking and reporting (MIPS, CMS130 Colorectal Cancer Screening)
- ModMed Scribe — AI-powered ambient listening that converts patient-provider conversations into suggested visit notes, trained to understand GI-specific language

*(Sources: modmed.com/specialties/gastroenterology/ehr/, modmed.com press releases)*

**gGastro ERW (Endoscopy Report Writer)** — The hallmark differentiator. A dedicated module for documenting endoscopic procedures:
- Single-screen interface with key procedure information
- Built-in, customizable GI templates for endoscopy and colonoscopy
- Pre-procedure and post-procedure documentation
- Anesthesia and recovery notes linked to patient charts
- Time-stamped workflow tracking (check-in, pre-op, entering endoscopy suite, entering recovery room, checkout)
- Procedure notes, referring physician letters, and discharge notes
- Nursing notes (pre-op, intra-procedure, recovery)
- Can operate standalone or integrated with gGastro EHR
- Syncs with EHR and practice management to avoid duplicate data entry
- Designed for use in private practices, ASCs, and hospital endoscopy suites

*(Sources: modmed.com/specialties/gastroenterology/endoscopy-report-writer/, modmed.com blog posts)*

**gPM (Practice Management)** — Scheduling, billing, and office operations:
- Appointment scheduling and office workflow management
- Financial dashboards and reporting
- Clearinghouse interface for claims submission
- Claim scrubbing and automated claim submissions
- Filing reminders
- Document management
- Patient eligibility verification

*(Source: modmed.com/specialties/gastroenterology/practice-management/)*

**Patient Engagement Tools:**
- **gPortal** — Patient portal (certified for (e)(1) patient access)
- **gKiosk** — Patient intake kiosk for check-in and form completion
- **gReminder** — Appointment reminders
- **gSurvey** — Patient surveys
- **gEstimator** — Out-of-pocket cost estimation for patients

*(Sources: modmed.com solutions page, product update announcements)*

**Analytics & Reporting:**
- **gInsights** — Data analytics tool
- **gAdvisor** — Advisory/decision support

**Revenue Cycle Management (RCM):** ModMed offers integrated billing services as an outsourced or technology-assisted option.

**Interoperability:**
- **ModMed Records Exchange** — A health data network for sharing records between GI practices and ASCs
- **Lab integrations** — Interfaces with Labcorp, Quest, and 150+ pathology labs nationwide (electronic lab orders added 2019)
- **Certified FHIR R4 API** — USCDI-compliant, supports SMART on FHIR, standalone and EHR-integrated apps, and bulk FHIR export (added in v6.3.0, August 2024)
- **Direct messaging** — Certified for (h)(1) direct transport
- **C-CDA support** — For transitions of care

**Mobile:** gGastro Mobile app for iOS and Android.

### Data & Content

Based on certified FHIR API resource list, product descriptions, and user reviews, gGastro stores and manages:

**Clinical data:**
- Patient demographics and insurance/coverage information
- Allergies and intolerances
- Active problems / conditions (with ICD-10 coding)
- Medications and medication requests (e-prescribing data)
- Immunization records
- Lab orders and results (interfaced with 150+ labs)
- Pathology results and tracking
- Diagnostic reports
- Clinical observations (vitals, findings)
- Procedures (especially endoscopy/colonoscopy documentation — the core use case)
- Implantable device records
- Goals and care plans
- Care team information
- Encounter records
- Clinical documents (via DocumentReference)

**Endoscopy-specific data:**
- Endoscopy procedure reports (pre-op, intra-procedure, post-procedure)
- Anesthesia records
- Nursing notes (pre-op, procedure, recovery)
- Time-stamped workflow events (check-in through checkout)
- Referring physician letters
- Discharge notes and instructions

**Practice management / billing data:**
- Appointment scheduling data
- Claims and billing codes (ICD-10, CPT)
- Financial/billing records
- Patient eligibility and insurance verification data
- Document management records

**Patient engagement data:**
- Patient portal interactions (medical history questionnaires, messaging)
- Patient intake form data (via kiosk)
- Appointment reminder data
- Patient survey responses
- Cost estimates

**Quality and compliance data:**
- Clinical quality measures (CQMs)
- MIPS/Promoting Interoperability reporting data
- Audit logs

**FHIR API resources confirmed in documentation:** AllergyIntolerance, CarePlan, CareTeam, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Group, Immunization, Location, Medication, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure.

**What's less clear:** The vendor website doesn't provide detailed information about the internal database schema or exactly what data tables exist beyond what's exposed via FHIR. The endoscopy report writer likely stores substantial structured data about procedure findings, polyp characteristics, biopsy details, and other GI-specific clinical content that may or may not map cleanly to standard FHIR resources. The practice management system stores scheduling, billing, and financial data that is typically not exposed via clinical FHIR APIs. The exact boundaries of the EHI export vs. the FHIR API coverage are not documented on the vendor website.

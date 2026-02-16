# Modernizing Medicine Inc. — Product Research

Researched: 2026-02-15
Developer website: https://www.modmed.com

## Overview

Modernizing Medicine (branded as **ModMed**) is a Boca Raton, Florida-based health IT company founded in 2010 by Daniel Cane (co-founder of Blackboard) and Dr. Michael Sherling, a practicing dermatologist. The company builds cloud-based, specialty-specific EHR and practice management software. ModMed has raised over $329M in funding, with Warburg Pincus acquiring a majority stake in 2017 ($231M Series F). In March 2025, Clearlake Capital acquired a majority stake from Warburg Pincus at a $5.3B valuation — making it one of the largest healthcare IT leveraged buyouts that year. The co-founders retained minority stakes.

ModMed serves **11 medical specialties**: allergy & immunology, dermatology, gastroenterology, OB/GYN, ophthalmology, orthopedics, otolaryngology (ENT), pain management, plastic surgery, podiatry, and urology. The company also serves ambulatory surgery centers (ASCs), particularly in gastroenterology. ModMed's own press materials reference "40,000+ providers" while financial press around the Clearlake deal cited "160,000+ specialty physicians and surgeons" — the difference likely reflects individual clinicians versus provider accounts/practices.

The company has approximately 1,950 employees and has made several acquisitions including:
- **gMed** (2015) — gastroenterology EHR, rebranded to "Modernizing Medicine Gastroenterology" at ACG 2018, now the gGastro product line
- **Exscribe** — orthopedic healthcare technology
- **Klara** (2022) — patient-provider communication platform (founded in Berlin, 2013)
- **TRAKnet** — practice management system

## Product: EMA (Electronic Medical Assistant)

CHPL IDs: 11032

### What It Is

EMA is ModMed's flagship product — an AI-powered, cloud-based, specialty-specific electronic health record system. "EMA" stands for **Electronic Medical Assistant**. It is certified under ONC 2015 Edition with a broad set of criteria covering clinical data capture (a)(1)-(a)(5), (a)(12), (a)(14), transitions of care (b)(1)-(b)(3), patient access (e)(1), (e)(3), FHIR APIs (g)(7)-(g)(10), public health reporting (f)(5), and EHI export (b)(10)/(b)(11).

EMA is not just a clinical charting module — it is the core of an **all-in-one platform** that includes EHR, practice management, billing, revenue cycle management, patient engagement, analytics, and telehealth. The certified module (EMA) is the centerpiece, but the product as a whole encompasses the full suite. The SED intended users are listed as "Providers, Medical Assistants (MAs), Ophthalmic Technicians, Administrators" — confirming this is used by both clinical and administrative staff.

The system is built natively for iPad (touch-based charting) and web, designed around specialty-specific workflows rather than generic templates adapted per specialty.

### Users & Market

**Target users**: Specialty physicians, surgeons, medical assistants, ophthalmic technicians, practice administrators, billing staff, and patients (via portal).

**Settings**: Ambulatory specialty practices ranging from solo practitioners to enterprise groups (50+ physicians). Also serves ambulatory surgery centers, particularly in gastroenterology.

**Market position**: ModMed is consistently top-rated by KLAS for specialty EHRs, particularly in dermatology and ophthalmology. Named a top healthcare software product in G2's 2025 Best Software Awards. Earned top spots on six G2 grids for EHR and RCM software in Spring 2024.

**Customer base**: 40,000+ providers across the U.S. (per ModMed press materials). The $5.3B valuation and ~1,950 employees indicate a substantial mid-market to enterprise vendor.

### Modules & Functionality

Based on vendor materials, review sites, and product pages, EMA encompasses the following modules and capabilities:

**Clinical Documentation (EMA EHR)**
- Specialty-specific templates and content libraries pre-loaded for each of the 11 supported specialties
- Interactive Anatomical Atlas and Virtual Exam Room for touch-based clinical documentation
- Adaptive learning engine that personalizes the interface based on individual provider documentation patterns — learns how providers describe diagnoses and treat patients
- Voice recognition for clinical documentation
- Reduced-click navigation optimized for high-volume specialty workflows
- Automatic generation of prescriptions, billing sheets, pathology requisitions, lab orders, and consent forms at note completion
- ICD-10 code suggestion (e.g., auto-suggests codes from diagram annotations in ophthalmology)
- MIPS intelligence platform for quality reporting

**E-Prescribing**
- Prescriptions generated at time of note completion
- Integrated with Surescripts (implied by (a)(4) certification)

**Lab Integration**
- Electronic submission of lab orders and receipt of results from connected clinical, pathology, and genetic labs
- Lab partners network for nationwide connectivity

**Pathology (Dermatology-specific)**
- Paperless pathology module that receives and tracks dermatopathology results within the system
- Specific to the dermatology product line

**Ophthalmic Image Management**
- DICOM image import from connected ophthalmic diagnostic devices (OCTs, visual fields, corneal topographers, fundus cameras)
- Centralized cloud storage and viewing of diagnostic images
- Side-by-side image comparison across visits
- Visual field viewer comparison tool
- Image annotation (freehand drawing, shapes, text, redaction)
- Images accessible directly from patient chart on iPad or web

**Practice Management**
- Hub for administrative tasks including scheduling, billing, and reporting
- Appointment management and scheduling
- Integrated with EHR — single platform, not a separate product
- Financial dashboards, tasks, and reports
- Clearinghouse interface within practice management
- Customizable claim scrubbing prior to payer submission
- Automated claim file submission
- Timely filing reminders
- Posting of remittance advice
- Reporting tools for analyzing rejections, denials, and more
- CPT code, diagnosis, referring doctor, and patient reports

**Revenue Cycle Management (RCM)**
- Full-service billing automation from claim submission to patient billing
- Automated processing and denial reduction
- Real-time financial analytics dashboards tracking revenue and KPIs
- Available as both software and managed services

**Patient Portal & Engagement**
- Patient portal (branded "APPatient") integrated with EHR
- Access to healthcare information from web or mobile app
- Secure HIPAA-compliant messaging
- Appointment scheduling
- Integrated payment options with flexible payment plans
- Patient kiosk for check-in
- Appointment reminders and patient surveys
- Integration with Apple Health and Google Fit (mobile app)

**Telehealth**
- End-to-end telehealth solution within the platform
- Supports scheduling, remote consultations, and integrated billing for virtual visits
- Accessible through patient portal

**ModMed Scribe (AI Ambient Listening)**
- AI-powered ambient documentation assistant
- Trained on 750 million patient encounters
- gScribe variant tailored for gastroenterology with GI-specific terminology
- Recent addition (announced 2024)

**AI-Powered Enhanced Faxing**
- Extracts and routes clinical data from incoming faxes directly into EMA
- Recent feature addition

**Inventory Management**
- Streamlined inventory management and supply ordering
- Expense tracking

**Analytics & Reporting**
- Customizable reporting for clinical performance and practice efficiency
- MIPS/quality measure tracking
- Financial and operational KPIs

**Gastroenterology ASC Module (gGastro)**
- Endoscopy report writer (ERW)
- ASC-specific practice management
- Anesthesia and nursing notes that auto-populate into operative reports
- Patient reminders and out-of-pocket cost estimators
- Real-time data flow between GI practice EHR and ASC
- Originally from the gMed acquisition, rebranded in 2018

### Data & Content

Based on the features described above, EMA stores and manages:

- **Clinical encounter data**: Specialty-specific clinical notes, exam findings, diagnoses (ICD-10), procedures (CPT), problem lists, medication lists, allergy lists, patient history, vital signs, growth charts
- **Prescriptions**: E-prescribing data including medication orders, controlled substance prescriptions
- **Lab data**: Lab orders and results from connected labs (clinical, pathology, genetic)
- **Pathology data**: Dermatopathology results and tracking (dermatology module)
- **Diagnostic images**: DICOM images from ophthalmic devices (OCTs, visual fields, corneal topography, fundus photography), image annotations
- **Billing and claims data**: Charge capture, claims, remittance advice, payment records, denial tracking, financial transactions
- **Scheduling data**: Appointments, scheduling templates, patient reminders
- **Patient demographics**: Registration information, insurance details, contact information
- **Patient portal data**: Patient-initiated messages, appointment requests, payment records, patient-entered health data
- **Documents and forms**: Consent forms, referral documents, faxes (with AI extraction), scanned documents
- **Inventory data**: Supply levels, ordering history, expense tracking
- **Surgical/procedural data**: Operative reports, anesthesia notes, nursing notes (ASC module)
- **Quality measure data**: MIPS performance data, clinical quality measures
- **Telehealth data**: Virtual visit records, telehealth encounter documentation
- **Analytics data**: Practice performance metrics, financial KPIs, clinical analytics
- **Communication data**: Patient-provider messages (including Klara integration for multi-channel communication)
- **Audit trails**: Required by (d)(2) certification — user actions and access logs
- **Apple Health/Google Fit data**: Patient-contributed health data via mobile app integration

The vendor's own description of "structured/actionable data optimized for value-based care under MIPS" (from EMRFinder) confirms data is stored in structured form, not just as free-text documents.

**Gaps/uncertainties**: The website doesn't clearly describe how clinical documents from external sources (e.g., referral letters, hospital discharge summaries) are stored beyond fax integration. The Klara communication platform integration is mentioned as an acquisition but the depth of messaging data integration with EMA is unclear. The specific data retention and scope differences between the various specialty versions of EMA (dermatology vs. ophthalmology vs. orthopedics etc.) are not well-documented publicly — each specialty likely has unique data elements (e.g., visual acuity for ophthalmology, body surface area mapping for dermatology) but the details require product-specific documentation.

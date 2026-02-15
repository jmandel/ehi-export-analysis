# Magilen Enterprises Inc — Product Research

Researched: 2026-02-15
Developer website: https://www.qsmartcare.com

## Overview

Magilen Enterprises Inc is the software development entity behind QSmartCare, a specialty wound care EHR. The company is essentially the technology arm of **Quality Surgical Management (QSM)**, a wound care services company founded in 1999 (some sources say 1996) by Dr. Steven Magilen, a general surgeon with 35+ years of wound care experience. QSM provides bedside wound care management in skilled nursing facilities (SNFs) and assisted living facilities across six states. QSM is the sole user of QSmartCare — the real-world testing report explicitly states "Our EHR is only used by one healthcare provider (ourselves)."

QSM is a small private company with approximately 75 employees. It has treated over 171,000 patients across 605 facilities. The company raised less than $5M in a single funding round (2020). QSM is JCAHO-certified and is headquartered in Hollywood, Florida. Dr. Magilen serves as both the CEO/Medical Director of QSM and the developer contact for the certified EHR product.

This is a classic case of a clinical practice that built its own specialty EHR for internal use and then pursued ONC certification. QSmartCare was developed "by and for wound care physicians" over 30 years, long before it was formally certified (January 2022).

## Product: QSmartCare

CHPL ID: 10803

### What It Is

QSmartCare is a cloud-based (SaaS) wound care EHR purpose-built for documenting and managing wound care encounters in skilled nursing facilities. It is not a general-purpose EHR — it is a specialty system designed around the workflow of wound care physicians, PAs, and NPs who travel to SNFs to provide bedside wound care services.

The certified module appears to be the whole product. There is a web application (app.qsmartcare.com) and a companion iOS mobile app (QSmartCare on the App Store, published by Quality Surgical Management Inc.) that allows providers to view schedules, access patient details, and capture wound photographs with auto edge detection. The mobile app connects to the web portal.

### Users & Market

**Primary users**: QSM's own wound care providers (physicians, PAs, NPs) and administrative staff (billers, coders, administrators). The SED intended user description is "Nurses, Physicians, & Staff."

**Clinical setting**: Wound care provided at the bedside in skilled nursing facilities and assisted living facilities. QSM clinicians travel to partner facilities to provide wound treatment — the EHR is used during these visits and for follow-up documentation.

**Scale**: QSM reports serving 605 facilities and treating 171,129 patients. However, the real-world testing report reveals that many certified features (Direct messaging, eCQM submission, immunization entry) had zero actual usage in CY 2023. This suggests the EHR's day-to-day use is narrowly focused on wound care documentation rather than the full spectrum of certified capabilities.

**Customer base**: QSmartCare is an internal tool — QSM is the only customer. It is not marketed or sold to external healthcare organizations.

### Modules & Functionality

Based on vendor materials, the product website, CHPL certification criteria, and integration documentation:

**Core wound care charting**: The primary function. The website emphasizes "accelerated charting" with an "intelligent workflow and interface" to reduce repetitive documentation. The charting module is described as packed with "time-saving functions" for fast documentation. This is the central purpose of the system — wound assessment, documentation, and treatment tracking.

**Wound photography**: The mobile app supports capturing wound photographs with auto edge detection and image cropping for document uploads. This is a key feature for wound care — visual documentation of wound healing progress.

**Clinical Decision Support**: The system has CDS engines with configurable rules that "provide suggestions based on standard rule defined and option for the new rule configuration on the application settings." Certified for (a)(1)–(a)(5) clinical criteria.

**Care Plans**: A care plan module that "aligns and archives the treatment plan with the patient's objectives, and formulates documentation into the pattern of a Care Plan." This is central to wound care management — treatment plans, goals, and progress tracking.

**Medication management**: The website states QSmartCare "makes the data entry and management of patient medications easy." The ONC costs page references NewCrop as a third-party integration, indicating e-prescribing capability. Certified for (b)(11) — clinical information reconciliation.

**Patient portal**: Certified for (e)(1) — view, download, transmit. There is a patient login page at qsmartcare.com/patient/. The real-world testing results suggest this has low actual usage.

**Care transitions / Interoperability**: Certified for (b)(1)–(b)(3) — transitions of care via C-CDA and Direct messaging (using Data Motion as a third-party service). The MatrixCare integration is particularly notable: QSM has a bidirectional integration with MatrixCare (a major SNF EHR) where patient face sheet data flows automatically into QSmartCare, and wound documentation flows back into MatrixCare. This is the primary interoperability workflow — exchanging data with the host facility's EHR.

**FHIR API**: Certified for (g)(7)–(g)(10). The API documentation shows a FHIR R4 API conforming to US Core 3.1, plus a legacy Patient API that returns C-CDA XML. The FHIR API exposes 21 resources including AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Location, and Procedure.

**Public health reporting**: Certified for (f)(1) immunization registry and (f)(2) syndromic surveillance, though real-world testing found zero actual usage of these features. This makes sense — wound care providers in SNFs are unlikely to be doing immunizations or reporting syndromic surveillance.

**Clinical quality measures**: Certified for (c)(1)–(c)(3) — CQM recording, exporting, and reporting. Again, real-world testing showed no actual eCQM submissions.

**EHI export**: Certified for (b)(10). The export page describes PDF (human-readable) and JSON (machine-readable) formats, with both single-patient and bulk multi-patient export capabilities. Accessible via Patient > CCDA > Export menu. Requires Author-level permissions.

### Data & Content

Based on the FHIR API resources, certified criteria, and product descriptions, QSmartCare manages:

**Clinical wound care data** (core): Wound assessments, wound measurements, wound photographs, treatment documentation, healing progress tracking. This is the heart of the system, though the specific data fields for wound documentation are not enumerated on the website.

**Patient demographics**: Patient records with face sheet data (imported from host facility EHRs like MatrixCare).

**Problems/conditions**: Diagnoses including wound-related conditions. The CDS provides suggestions "based on documentation added including diagnosis."

**Medications**: Medication lists and medication requests. E-prescribing via NewCrop integration.

**Allergies**: AllergyIntolerance is a supported FHIR resource.

**Care plans and goals**: Treatment plans, patient objectives, wound care care plans.

**Encounters**: Visit/encounter documentation for wound care visits at facilities.

**Observations**: Vital signs, lab results, and clinical observations (per FHIR API).

**Procedures**: Wound care procedures — debridement, biopsies, PEG/SPC tube management (per QSM's services description).

**Care teams**: Provider and care team information.

**Devices**: Implantable device information (per FHIR API, though relevance to wound care is unclear).

**Immunizations**: Supported per FHIR API but no real-world usage.

**Documents**: Clinical document references, C-CDA documents.

**Diagnostic reports**: Supported per FHIR API — possibly lab results or wound culture reports.

**What's unclear or absent from public materials**:
- **Billing/claims data**: The website mentions the system serves "billers" and "coders" and QSM provides "non-clinical support to streamline billing, logistics, and other administrative duties," but there is no explicit description of a billing module or claims processing within QSmartCare itself. The ONC costs page does not mention billing integrations. It's unclear whether billing is handled within QSmartCare or through a separate system.
- **Scheduling**: The mobile app shows appointment schedules and visit status, suggesting some scheduling capability, but details are thin.
- **Wound-specific structured data**: The system is purpose-built for wound care, so it almost certainly stores highly detailed wound-specific data (wound type, location, dimensions, stage/grade, wound bed characteristics, exudate, periwound condition, etc.), but the vendor website does not enumerate these fields. This is the most important data category for this product and the least documented publicly.
- **Administrative/facility data**: QSM operates across 605 facilities, so the system likely tracks facility information, but details are not described.
- **Audit logs**: Certified for (d)(1)–(d)(9) security criteria, so audit logging exists but is not described in detail.

---

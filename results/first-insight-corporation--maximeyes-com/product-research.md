# First Insight Corporation — Product Research

Researched: 2026-02-16
Developer website: https://www.maximeyes.com/ (formerly http://www.first-insight.com, which now redirects)

## Overview

First Insight Corporation is a privately held, Hillsboro, Oregon–based company founded in 1994 by Nitin Rai, who remains CEO. The company builds EHR and practice management software exclusively for eye care — ophthalmology and optometry. With approximately 50 employees, First Insight is a small, specialty-focused vendor serving "thousands" of practices across the United States, from solo practitioners to large corporate-affiliated chains. The company has been in this niche for over 30 years and has never expanded beyond eye care.

In 2025, the company rebranded its web presence from first-insight.com to maximeyes.com, signaling that "MaximEyes" is now the primary brand identity rather than the corporate name. There is no evidence of acquisition by or affiliation with a larger company — First Insight remains independent.

The company's largest known customer is U.S. Vision (including its affiliate Nationwide Vision), which selected MaximEyes for 600+ locations in 2018, converting over 3 million exam records from the prior system (ExamWRITER). The FHIR endpoint directory on their website lists 500+ distinct practice identifiers, providing a concrete lower-bound for active cloud customers.

## Product: MaximEyes.com

CHPL ID: 10470

### What It Is

MaximEyes.com is a cloud-based, browser-accessible EHR and practice management platform purpose-built for ophthalmology and optometry practices. It is hosted on Microsoft Azure. The certified module (MaximEyes.com v1.1) appears to encompass the full product — there is no evidence that the certification covers only a subset of a larger platform.

There is a historical distinction between "MaximEyes" (the original desktop/server-based SQL application, sometimes called "MaximEyes SQL") and "MaximEyes.com" (the current cloud-based version). The ONC-certified product is specifically the cloud version. The company appears to have converged on the cloud platform as the primary offering.

The product is a comprehensive eye care suite covering clinical documentation, practice management, billing/revenue cycle, optical point-of-sale, patient engagement, image management, and e-prescribing — all integrated into a single platform. This is not a narrow clinical module; it is a full-scope practice operations system for eye care.

### Users & Market

**Target users:** Ophthalmologists, optometrists, optical retail staff, billing/coding staff, front desk/schedulers, practice administrators. The SED intended user description is "Optometry & Ophthalmology Ambulatory Healthcare Providers."

**Settings:** Single-location independent practices, multi-location groups, and corporate-affiliated eye care chains. All ambulatory/outpatient — no hospital or inpatient use.

**Scale:** The vendor claims "thousands" of practices but does not disclose exact numbers. The FHIR endpoint directory lists 500+ practices. The U.S. Vision deal alone covers 600+ locations. In the 2017 Black Book survey (922 participants from 692 practices), MaximEyes ranked #2 nationwide for ophthalmology EHR.

**Pricing:** Starts at approximately $350/month (per EMRSystems). The patient portal (EyeClinic.net) and e-prescribing (DrFirst Rcopia) are separate per-provider subscriptions on top of the base.

### Modules & Functionality

The following modules and features are described on the vendor's website, in press releases, and in third-party reviews:

**EHR / Clinical Documentation:**
- Structured exam documentation with customizable templates for ophthalmology and optometry exams
- SOAP note generation (including AI-assisted via EVAA Scribe, launched September 2025)
- Visual acuity, intraocular pressure, slit lamp findings, dilated fundus exam, and other ophthalmic-specific structured data
- Coding triggers that suggest ICD/CPT codes based on exam findings
- Clinical decision support
- E&M coding integration (since 1999)
- Drug interaction checking and clinical alerts
- Problem lists, medication lists, allergy lists (certified for (a)(1), (a)(2), (a)(3))
- Family health history (certified for (a)(12))
- Implantable device list (certified for (a)(14))

**Practice Management:**
- Patient scheduling with automated reminders
- Patient registration and demographics
- Insurance verification
- Staff management
- Reporting and analytics dashboards
- Waitlist management and recall scheduling

**Revenue Cycle Management / Billing:**
- End-to-end claims management
- Electronic claims submission
- Claim scrubbing with payer-specific rules
- ERA/EOB auto-posting
- Accounts receivable tracking
- VSP (Vision Service Plan) claims and authorization integration (since 1997)

**Optical Point-of-Sale:**
- Frame catalog management
- Barcode scanning
- Inventory tracking for frames, lenses, and contact lenses
- Spectacle and contact lens dashboards
- Lab order management with real-time status tracking (online ordering since 2000)
- Insurance integration for optical benefits

**Patient Engagement (EyeClinic.net):**
- Patient portal for view/download/transmit of health records
- Online patient intake forms
- Automated appointment reminders
- Secure messaging (direct messaging protocol)
- Telehealth capabilities
- Summary of Care document access

**Image Management:**
- Integration with ophthalmic diagnostic equipment: OCTs, fundus cameras, visual field analyzers, autorefractors, tonometers, lensometers
- Cloud-based HIPAA-compliant image storage
- Side-by-side image comparison for longitudinal tracking
- Images stored with patient records

**E-Prescribing:**
- Two-way e-prescribing via DrFirst Rcopia integration
- Prescription (Rx) and contact lens (CLX) scripts
- Drug-drug and drug-allergy interaction checking
- EPCS (Electronic Prescribing for Controlled Substances) support (implied by Rcopia integration)

**AI Suite (EVAA, launched September 2025):**
- Virtual Assistant: scheduling and communications automation
- Billing Assistant: claims and coding optimization
- Scribe: voice-driven AI SOAP note generation
- Intelliscan: document recognition for digitizing paper records

**Quality Reporting:**
- Direct EHR-to-CMS reporting for PQRS/MIPS
- AAO IRIS Registry integration (American Academy of Ophthalmology)
- AOA MORE Registry integration (American Optometric Association) — MaximEyes was the first EHR to integrate
- Certified for CQMs: CMS50v8, CMS68v9, CMS131v8, CMS138v8, CMS142v8, CMS143v8, CMS156v8, CMS165v8

**Interoperability:**
- FHIR R4 API endpoints (fhir.maximeyes.com)
- HL7 and IHE standards compliance
- Summary of Care (C-CDA) generation and transmission
- Direct messaging protocol support
- USCDI data elements

**Recent Integration (November 2025):**
- Mango Voice VoIP telephony integration for front-office automation

### Data & Content

Based on the modules and features described above, MaximEyes.com stores and manages:

- **Clinical exam data:** Structured ophthalmic/optometric exam findings (visual acuity, IOP, slit lamp, fundus exam, refraction, etc.), SOAP notes, assessments, plans, diagnoses (ICD codes), procedures (CPT codes)
- **Diagnostic images:** OCT scans, fundus photographs, visual field results, autorefractor data — stored in cloud-based HIPAA-compliant storage
- **Patient demographics:** Names, contact information, insurance details, registration data
- **Medications and prescriptions:** Active medication lists, prescription history (pharmaceutical, eyeglass, contact lens), e-prescribing records via DrFirst Rcopia
- **Allergies:** Drug and other allergies
- **Problem lists:** Active and historical problems/diagnoses
- **Family health history:** Structured family history data
- **Implantable devices:** IOLs (intraocular lenses) and other ophthalmic implants
- **Scheduling data:** Appointments, recalls, waitlists, reminder history
- **Billing and financial data:** Claims, ERA/EOB records, payment history, accounts receivable, payer information
- **Optical retail data:** Frame inventory, contact lens orders, lab orders, point-of-sale transactions, spectacle and contact lens prescriptions
- **Documents:** Scanned documents, intake forms, consent forms (digitized via Intelliscan)
- **Patient portal activity:** Secure messages, portal access logs, transmitted care summaries
- **Care summaries:** C-CDA documents containing USCDI data elements
- **Quality measure data:** Clinical quality measure calculations and registry submissions (IRIS, MORE, MIPS)
- **Audit logs:** Access and activity logs (certified for (d)(2), (d)(3))

**What's less clear:** The vendor website does not specifically describe referral management as a distinct module, though it's likely embedded in the workflow given the specialty nature of the practice. Telehealth is mentioned but details on what telehealth-specific data (visit recordings, etc.) is stored are sparse. The AI-generated content (EVAA Scribe notes, Billing Assistant suggestions) presumably gets stored in the clinical record but the website doesn't detail the data lifecycle.

---

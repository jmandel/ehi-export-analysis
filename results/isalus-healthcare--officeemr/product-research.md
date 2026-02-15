# iSALUS Healthcare — Product Research

Researched: 2026-02-14
Developer website: https://isalushealthcare.com

## Overview

iSALUS Healthcare is a healthcare technology company founded in 2000 in Indianapolis, Indiana (originally as Most, LLC). The company was co-founded by Chuck Dietzen and Michael Hall. It provides a cloud-based all-in-one EHR, practice management, billing, and telehealth platform primarily for small to mid-sized ambulatory specialty practices. iSALUS was acquired by **EverCommerce** (NYSE: EVCM) in late 2018 and now operates within EverCommerce's **EverHealth** division. In early 2019, EverCommerce also acquired **AllMeds, Inc.** (an EHR vendor for ENT, orthopedics, neurosurgery, and pain management), and in October 2019 formally integrated AllMeds and iSALUS under one organization. This integration led to the launch of **ENTChoice**, a specialty EHR product for otolaryngologists. Michael Hall departed as CEO in August 2020 and was succeeded by Brent Michael as president of the combined healthcare technology division.

The company is relatively small — estimated at 51–62 employees with revenue estimates in the low single-digit millions (though exact figures are uncertain as it reports within EverCommerce). iSALUS claims to serve practices across 48 states and processes nearly half a billion dollars in medical claims annually. They primarily target private specialty practices, from solo practitioners to groups with 50+ physicians.

## Product: OfficeEMR

CHPL ID: 10914

### What It Is

OfficeEMR is a **full, all-in-one cloud-based EHR, practice management, and billing suite** designed for small and medium-sized ambulatory medical practices. It is not a component — the certified module encompasses the entire product. The platform provides a single database and single login for clinical charting, scheduling, billing, e-prescribing, patient portal, telehealth, and administrative functions. It is entirely web-based (works on any OS) and also has a mobile app (iOS and Android) supporting charge capture, e-prescribing, remote charting, telehealth, and patient image viewing.

The ONC certification (June 2022) covers 37 criteria spanning clinical data capture (a)(1)–(a)(5), (a)(12), (a)(14), transitions of care (b)(1)–(b)(3), (b)(10)–(b)(11), patient engagement (e)(1), (e)(3), public health reporting (f)(1), (f)(2), (f)(5), standardized API/FHIR (g)(10), and direct messaging (h)(1). This is a comprehensive ambulatory EHR certification.

### Users & Market

**Target users:** Physicians, practice managers, billing staff, and clinical support staff in ambulatory/outpatient settings. Not designed for inpatient or hospital use.

**Specialties:** iSALUS has purpose-built configurations for several core specialties:
- Nephrology (including a dedicated dialysis rounding feature)
- Urology
- Otolaryngology/ENT (via ENTChoice, post-AllMeds integration)
- Orthopaedics
- Neurosurgery
- Pain Management

Beyond these, the platform supports 45+ specialties through its customizable "Choice EHR" option, including cardiology, dermatology, family medicine, gastroenterology, OB-Gyn, pediatrics, psychiatry, and many others.

**Practice size:** Solo practices through organizations with 50+ physicians. The free tier suggests they pursue very small practices as an entry point.

**Customer count:** Not publicly disclosed. The company claims "thousands of healthcare providers" but no specific numbers are available. A 2012 partnership with St. Vincent Health (Indiana) to offer OfficeEMR to independent physicians throughout Indiana is one of the few named deployments.

**Reviews:** Limited online review presence — Capterra shows a 5.0/5.0 rating but with very few reviews. FindEMR shows 4/5 stars from 3 reviews. No KLAS ratings found. The small review footprint is consistent with a smaller vendor.

### Modules & Functionality

Based on vendor website, help documentation, and third-party profiles, OfficeEMR includes the following integrated modules:

**Clinical / EHR:**
- Clinical charting with pre-built and customizable templates
- Progress notes and treatment plans
- Problem list, allergies, and medication management
- Vitals recording
- Clinical reconciliation (auto-post previous medications, allergies, problems)
- Clinical decision support with customizable alert rules
- Procedure note templates (surgical documentation including type of surgery, implants/devices, blood loss, postoperative instructions)
- Specialty-specific dialysis rounding feature (vital signs, treatment details, medications with auto-populated billing codes)
- Patient image capture and viewing
- Letters/correspondence generation

**E-Prescribing:**
- E-prescribing including EPCS (Electronic Prescribing for Controlled Substances)
- Integration with CoverMyMeds for Real-Time Benefit Checks and Electronic Prior Authorization

**Scheduling:**
- iScheduler module for appointment management
- Patient recall with automated appointment reminders
- Check-in / check-out workflows

**Billing & Revenue Cycle:**
- Claims management and submission
- Clearinghouse integration
- Insurance eligibility verification (batch eligibility)
- Fee schedule management
- Integrated payment processing
- Electronic statements
- Auto-populated billing codes from clinical documentation
- MIPS/Meaningful Use reporting
- Patient cost estimator
- Optional outsourced billing/RCM services (claimed 98.1% average net collection rate)

**Patient Engagement:**
- Patient Portal (Personal Health Records for families)
- Intelligent Intake (digital patient intake forms)
- Patient surveys and online reputation management
- Patient communications

**Telehealth:**
- AnywhereCare telehealth module
- Remote patient charting

**Document Management:**
- eDocuments (scanning and document management)
- Exydoc (document management)
- RecordSync (records management)
- Electronic faxing

**Labs & Orders:**
- E-labs (electronic lab results management)
- Order entry
- Electronic referral management with two-way interfaces

**Reporting & Analytics:**
- Dynamic reporting and custom analytics
- Quality reporting (MIPS)
- Public health case reporting (immunization registry, syndromic surveillance, electronic case reporting)

**Interoperability:**
- CCDA exports
- EHI Export (single patient and all-patient)
- HL7 interface mappings
- FHIR API (g)(10) certified
- Direct messaging (h)(1)
- InfoDive data extract

**Additional Services (through iSALUS, not strictly part of OfficeEMR software):**
- Remote Patient Monitoring (RPM)
- Chronic Care Management (CCM)

### Data & Content

Based on vendor documentation (particularly the EHI Export feature documentation and knowledge base), OfficeEMR stores data across these documented categories:

- **Demographics** — patient demographic information
- **Insurance** — insurance policy details
- **Responsible Parties** — responsible party/guarantor records
- **Payer** — insurance payer information
- **Appointments** — scheduling data
- **Authorizations** — referral/authorization records
- **Emergency Contacts** — patient emergency contact details
- **Patient Comments** — notes/comments about patients
- **Vitals** — vital signs measurements
- **Allergies** — allergy records
- **Problem List** — clinical problem lists
- **Prescriptions** — medication prescription data
- **Progress Notes** — clinical documentation
- **Letters** — patient correspondence
- **eDocument Metadata** — metadata for scanned/uploaded documents
- **Patient Communications** — messages and communications
- **Fee Schedule** — billing fee information
- **Claims** — complete claims data
- **Claim Procedure Lines** — procedure-level claim details
- **Payments** — payment transaction records

This list comes from the EHI export documentation itself. The product's feature set suggests additional data domains that may or may not appear in the export — for example, lab results, orders, referrals, immunizations, procedure notes, clinical decision support rules, and patient portal activity are all described as features but are not explicitly listed as separate EHI export categories above. Whether these are subsumed under existing categories (e.g., lab results within progress notes) or potentially missing from the export will need to be evaluated in Phase 2.

The vendor's billing feature set (claims, clearinghouse integration, eligibility verification, payments, statements, fee schedules) indicates substantial financial data is stored. The telehealth module (AnywhereCare) likely stores visit records. The Intelligent Intake feature stores patient-submitted forms. Document management (eDocuments, Exydoc) stores scanned documents and metadata. The degree to which all of these are captured in the EHI export is a key question for Phase 2.

### Pricing

OfficeEMR uses a tiered pricing model:
- **Free:** Cloud EHR, appointments, chart notes, e-prescribing, e-labs, 2 hours training
- **Standard:** Adds billing, scheduling, clearinghouse, 8 hours training
- **Premium:** Unlimited claims, 20 hours training
- **Outsourced Billing:** Available as a separate service

Exact pricing is not publicly disclosed.

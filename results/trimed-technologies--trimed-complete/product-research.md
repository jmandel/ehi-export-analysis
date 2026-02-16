# TriMed Technologies — Product Research

Researched: 2026-02-16
Developer website: https://www.trimedtech.com/

## Overview

TriMed Technologies is a small, privately held healthcare IT company founded in 1996, headquartered in the United States with approximately 50 employees across three continents and estimated annual revenue around $1.7M. The company originally provided software and services to medical practices, management service organizations (MSOs), hospitals, and central billing companies. In July 2010, TriMed acquired the e-Medsys source code and trademark, transitioning from a third-party value-added reseller to a full-service software company that controls design, development, implementation, and support of its products. The product was previously known as "e-Medsys" and has been rebranded as "TriMed Complete."

TriMed's target market is independent ambulatory practices ranging from solo providers to 400+ provider groups. They have a notable specialty focus on pediatrics, marketing themselves as offering a "pediatric-specific by design" EHR rather than an adapted general-purpose system. They also serve cardiology and other specialties, as well as general primary care and multi-specialty practices. The product is cloud-hosted on Amazon Web Services (AWS).

## Product: TriMed Complete

CHPL ID: 10076
CHPL Product Number: 15.05.05.3103.TRIC.01.00.1.190820
Certification Date: 2019-08-20
Formerly known as: e-Medsys

### What It Is

TriMed Complete is an integrated, cloud-based EHR and practice management platform. It is certified for 50+ ONC criteria spanning clinical data ((a)(1)–(a)(15)), care coordination ((b)(1)–(b)(11)), clinical quality measures ((c)(1)–(c)(3)), privacy/security ((d)(1)–(d)(13)), patient portal ((e)(1)–(e)(3)), public health reporting ((f)(1), (f)(2), (f)(7)), FHIR APIs ((g)(7), (g)(9), (g)(10)), and direct messaging ((h)(1)). This is a broadly certified product covering clinical, administrative, patient engagement, interoperability, and public health functions.

The certified module appears to be the whole product — TriMed Complete is marketed as an all-in-one solution that bundles EHR, practice management, patient portal, e-prescribing, and other capabilities into a single platform. Pricing is $589/month per MD and $389/month per mid-level provider, with the all-inclusive plan bundling EHR, practice management, and revenue cycle management together.

### Users & Market

**End users** include providers (physicians, mid-levels), medical assistants, administrative staff, and clinical users — consistent with the CHPL metadata's `sed_intended_user_description` of "providers, MA's, Admin, clinical users." Patients also interact with the system through the patient portal and digital check-in modules.

**Clinical settings**: Independent ambulatory practices, from solo providers to multi-site groups with 400+ providers. The vendor emphasizes pediatric practices as a primary market, but also serves cardiology, family medicine, mental health, urgent care, and multi-specialty groups.

**Market position**: TriMed is a very small vendor in the EHR market (est. ~$1.7M revenue, ~50 employees). They claim "#1 top placement for EHR solutions among 311 other companies" on one review site and have generally positive user reviews, particularly for customer support responsiveness and ease of use. They are a niche player primarily serving small-to-mid-size independent practices.

**No notable large health system deployments** were found. The vendor's case studies and testimonials come from small practices.

### Modules & Functionality

Based on the vendor's website, feature pages, press releases, and third-party review sites, TriMed Complete includes the following modules and capabilities:

**Electronic Health Records (Clinical)**
- Interactive clinical notation / charting with customizable templates
- Specialty-specific templates (pediatrics, cardiology, family medicine, mental health, etc.)
- Clinical decision support with real-time diagnostic suggestions
- ICD-10 code predictions and medication recommendations
- Problem lists, medication lists, allergy management
- Patient history snapshots
- Growth tracking (pediatric)
- Well-child visit workflows (pediatric)
- Vaccine/immunization management and tracking
- Clinical references

**E-Prescribing**
- Integrated electronic prescribing (e-Rx)
- EPCS (Electronic Prescribing of Controlled Substances) — available as add-on
- Drug interaction checking
- Integration with Surescripts

**Computerized Provider Order Entry (CPOE)**
- Medication orders
- Laboratory orders with direct lab connectivity for ordering and receiving results
- Imaging/radiology orders

**Practice Management**
- Appointment scheduling with customizable templates (including after-hours/weekend)
- Claims management and insurance claim processing
- Eligibility verification (real-time insurance verification)
- Patient registration and demographics management
- Authorization tracking for referrals and treatment authorizations
- Advanced collections / payment recovery
- Credit posting and EDI management
- Patient recall (follow-up scheduling)
- Reporting and analytics

**Billing / Revenue Cycle Management**
- Medical billing (available as part of all-inclusive plan)
- Electronic billing / EDI
- Online bill pay through patient portal
- Consolidated family balance (especially for pediatrics)
- Credit/debit card payment processing
- TriMed also offers billing *services* (outsourced billing) — unclear if this is a separate product or part of the platform

**Patient Engagement**
- Patient portal (view records, messaging, appointments, billing)
- Online appointment booking
- Digital check-in module (patients complete forms on mobile devices)
- Patient messaging / secure communication
- Electronic patient forms
- Appointment reminders
- Online bill pay

**Document Management**
- Centralized patient document storage
- AI-powered OCR for extracting data from scanned documents, referrals, intake forms, insurance cards, and handwritten notes

**Telemedicine**
- Integrated telemedicine platform (details sparse on website, but listed as a core offering)

**Mobile**
- Mobile application ("Amplify" — web-based mobile access)
- Access patient records, e-prescribe, capture signatures, track vitals from mobile devices

**AI/Ambient Documentation**
- Integration with Amazon HealthScribe for ambient AI clinical documentation
- Auto-generates HPI, assessment, and plan summaries from patient encounters
- AI-enhanced note writing (clarity, grammar, structure)
- AI-driven smart scheduling

**Interoperability & Data Exchange**
- Surescripts Clinical Direct Messaging and Net2Net
- HL7 integration
- CCDA (XML format) for patient data export
- FHIR API access (certified for (g)(7), (g)(9), (g)(10))
- Immunization registry connectivity
- Public health agency reporting (syndromic surveillance, electronic case reporting)

**Clinical Quality Measures**
- 34+ quality metrics for preventive care, immunization tracking, and disease management

### Data & Content

Based on the features and modules described above, TriMed Complete manages and stores the following data types (evidence-based, from vendor materials and reviews):

**Clinical data**: Patient charts/encounter notes, problem lists, medication lists, allergies, vital signs (including pediatric growth data), immunization records, clinical assessments, care plans, clinical decision support alerts, AI-generated ambient documentation summaries.

**Order data**: Medication orders, lab orders and results (via direct lab connectivity), imaging/radiology orders.

**Prescription data**: E-prescriptions including controlled substances (via Surescripts integration).

**Administrative/demographic data**: Patient demographics (name, address, phone, DOB), guarantor information, family account linkages, insurance information (including scanned insurance card images via OCR), primary/secondary contacts.

**Scheduling data**: Appointment records, provider calendars, scheduling templates, patient recall records.

**Billing/financial data**: Claims, insurance eligibility verifications, authorization/referral records, payment records, collections data, EDI transactions, consolidated family balances. (Note: some user reviews describe the billing module as "cumbersome and difficult," but it is present and stores this data.)

**Documents**: Scanned documents, referrals, intake forms, insurance cards, handwritten notes (with OCR extraction), and general patient document storage.

**Patient-generated data**: Patient portal messages, self-reported demographic updates, electronic form submissions, digital check-in data, online appointment requests.

**Communication data**: Secure patient messages, Direct messages (via Surescripts), appointment reminders.

**Quality/reporting data**: Clinical quality measure calculations, clinical reports.

**Public health data**: Immunization registry submissions, syndromic surveillance data, electronic case reports.

**Telehealth data**: Telemedicine session records (details unclear from vendor materials, but telemedicine is a listed module).

**Information gaps**: The vendor website does not provide detailed database schemas or data dictionaries. The extent of audit logging data, system configuration data, or internal workflow state data stored is not described in marketing materials. The telemedicine module's specific data storage is not well documented on the website.

---

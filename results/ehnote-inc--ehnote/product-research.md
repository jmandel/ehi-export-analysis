# EHNOTE, INC — Product Research

Researched: 2026-02-15
Developer website: https://www.ehnote.com

## Overview

EHNOTE, Inc is a small healthcare technology company founded in 2018, headquartered in Plano, Texas (also listing an address at 5050 Quorum Drive, Suite 700, Dallas, TX). The company was founded by Amarnatha Reddy Midde (CEO) and Amarnath Reddy Chappidi (COO), with Dr. Kuldeep Raizada listed as an advisor. The company has an estimated 61–100 employees and operates with a global team including development resources in India.

EHNOTE builds a specialty-focused cloud EHR platform primarily targeting ophthalmology and eye care practices. The vendor claims to serve "200+ Specialty Practices in USA & India." They participate in major medical conferences including AAO (American Academy of Ophthalmology), ASCRS, and HIMSS.

Despite the SED intended user description on CHPL mentioning "wound care physicians," the EHNOTE website makes no mention of wound care functionality. The product is overwhelmingly marketed as an ophthalmology EHR, with additional support for dental, gynecology, pediatrics, and general physician specialties. The wound care reference in the CHPL metadata is likely erroneous or reflects a testing scenario description rather than the product's actual market focus.

## Product: EHNOTE

CHPL IDs: 11356 (15.04.04.3171.EHNO.01.00.1.231025)
Certification date: 2023-10-25
Version: 1.0

### What It Is

EHNOTE is an all-in-one cloud-based EHR and practice management platform built primarily for ophthalmology practices. The vendor positions it as "One Platform for Your Entire Ophthalmology Practice Ecosystem." The certified module appears to be the whole product — there is no indication of separate product lines or that the certification covers only a subset of the platform.

The product spans multiple functional areas: clinical EHR, practice management, ambulatory surgery center (ASC) charting, optical point-of-sale, patient portal, telemedicine, revenue cycle management, and analytics. It also offers specialty modules for dental, gynecology, pediatrics, and general physician practices, though ophthalmology is the clear primary focus.

The product relies on third-party components for certain functions: Carefluence Open API R4 for FHIR interoperability, DrFirst Rcopia for electronic prescribing, EMR Direct for secure email/Direct messaging, and Concurred for fax services (per the mandatory disclosures page).

### Users & Market

**Primary users**: Ophthalmologists, optometrists, opticians, and practice managers in eye care settings. The platform accommodates solo practitioners, independent practices, multi-location operations, and non-profit organizations.

**Market size**: Small vendor — 200+ specialty practices in USA and India per the vendor's website. Only 1 user review found on SoftwareFinder (5 stars, October 2023). A few customer testimonials appear on the vendor website, with users reporting 3–4 years of product usage. Very limited independent review presence on third-party platforms.

**Clinical settings**: Ambulatory ophthalmology clinics, optometry practices, optical retail locations, and ambulatory surgery centers. No hospital or inpatient presence described.

**Go-to-market**: Direct sales, appears to target small-to-mid-size eye care practices. Presence at major ophthalmology and health IT conferences. International presence (India).

### Modules & Functionality

Based on vendor website and product pages, EHNOTE includes the following modules and capabilities:

**Clinical EHR / Charting**
- Subspecialty-specific charting templates with auto-populating fields (per ophthalmology EHR page)
- Flexible one-page EHR and step-by-step EHR formats
- Multi-layered drawing pad for anatomical sketching of eye structures
- DICOM imaging integration — upload, view, compare diagnostic images with automatic extraction from ophthalmic devices
- Visual acuity graphs, IOP (intraocular pressure) tracking, refraction data
- Before/after surgery comparison reports
- Drug interaction checking and allergy alerts (via e-prescribing integration)
- ICD-11 coding standards compliance with automated ICD/CPT code generation
- Clinical decision support tools (referenced on certification disclosures page)

**E-Prescribing**
- Electronic prescription generation and transmission to pharmacy networks (via DrFirst Rcopia per disclosures)
- Drug interaction alerts and regulated medication database access

**Ambulatory Surgery Center (ASC) Charting**
- Pre-operative, intra-operative, and post-operative documentation
- Anesthesia documentation
- Automated discharge and operative note generation
- Digital signing of surgical notes (including remote signing)
- Pre-operative details, imaging results, and surgical preferences integration

**Practice Management**
- Multi-view appointment scheduling with recurring bookings
- Patient self-scheduling (portal, web portal, digital kiosk, QR codes)
- Automated appointment notifications and reminders
- Digital check-in and check-out
- Insurance eligibility verification
- Multi-location management with centralized data (eliminates duplicate patient registration)
- Staff performance tracking and employee activity monitoring
- 200+ pre-built reports for revenue, operations, and performance

**Revenue Cycle Management / Billing**
- Integrated billing and insurance claim processing
- Accounts receivable management and financial transaction tracking
- Reimbursement verification
- Integrated payment gateway for patient payments

**Optical Point-of-Sale**
- Optical retail management (eyeglasses and contact lens sales)
- Inventory management and stock tracking

**Patient Portal & Engagement**
- Patient access to personal and family health records
- Customized care plans viewable by patients
- Test results access
- Secure messaging / end-to-end communication portal
- Chatbot functionality
- Self-vision testing tools (visual acuity, Amsler Grid)
- Online eyeglasses/contacts purchasing
- Medicine reminders
- SMS broadcasting for appointments and promotions
- Educational material exchange
- Patient loyalty program
- Patient CRM with lead generation and follow-up tracking
- Patient counseling with quotations and treatment options

**Telemedicine**
- Video consultations (audio/visual) without patient app download requirement
- Pre-consultation form collection (including images and videos)
- Real-time charting during teleconsultations
- Mobile apps for iOS and Android (both physician and patient)
- Integrated payment collection for telehealth visits

**Analytics & Reporting**
- Clinical analytics: visual acuity, IOP, refraction data tracking
- Population analytics: stratification by demographics and disease patterns
- MIPS dashboard for quality measure reporting to CMS
- Revenue and financial analytics
- AI-powered analytics for clinical decision support (e.g., glaucoma detection mentioned)
- Marketing effectiveness tracking

**Health Information Exchange**
- Transitions of care via C-CDA documents (certified for (b)(1) and (b)(2))
- Direct messaging (via EMR Direct)
- FHIR API access (via Carefluence Open API R4, certified for (g)(10))
- Automated referral letter generation based on examination findings
- Fax integration (via Concurred)

**Specialty Modules (beyond ophthalmology)**
- Dental: dental charts with odontogram visualization, dental-specific billing
- Gynecology: prenatal tracking, obstetric/gynecologic records, sonographic scan management
- Pediatrics: family health profiles (parents' health, genetics), growth charts, vaccination dashboards
- General Physician: broad-based clinic management with labs and radiology integration

### Data & Content

Based on the described modules and features, EHNOTE stores and manages the following data types:

**Clinical data**: Patient demographics, medical history, family health history, examination findings, diagnoses (ICD-11 coded), treatment plans, care plans, clinical notes, surgical documentation (pre-op, intra-op, post-op, anesthesia, discharge, operative notes), referral letters, problem lists, medication lists, allergy lists, immunization records.

**Ophthalmic-specific data**: Visual acuity measurements, intraocular pressure readings, refraction data, DICOM images from diagnostic devices, anatomical drawings/sketches, before/after surgical comparison data, self-vision test results.

**Prescriptions**: E-prescriptions transmitted via DrFirst Rcopia, medication databases, drug interaction data.

**Administrative/scheduling data**: Appointments, scheduling preferences, recurring visit patterns, check-in/check-out records, multi-location scheduling.

**Financial/billing data**: Insurance information, claims, billing records, financial transactions, accounts receivable, patient payments, reimbursement data.

**Optical retail data**: Product inventory, point-of-sale transactions, eyeglasses/contact lens orders.

**Patient engagement data**: Portal messages, SMS communications, pre-consultation forms (including patient-submitted images and videos), educational materials sent, patient satisfaction/loyalty data, CRM records (leads, follow-ups, counseling notes with quotations).

**Telemedicine data**: Video consultation records, telehealth session documentation, remote payment records.

**Reporting/quality data**: MIPS quality measure data, population health analytics, staff performance metrics, revenue reports.

**Interoperability data**: C-CDA documents (transitions of care), FHIR resources, Direct messages, faxed documents.

**Notable gaps/uncertainties**:
- The website does not describe lab ordering or results management in detail, though "labs and radiology integration" is mentioned for the general physician module.
- No mention of wound care functionality despite the CHPL SED description referencing wound care physicians.
- The depth of dental, gynecology, and pediatrics modules is unclear — they appear to be specialty template overlays rather than deeply distinct product lines, but this is not certain.
- It's unclear how much clinical data is stored natively vs. passed through to third-party systems (e.g., DrFirst for prescriptions, Carefluence for FHIR).

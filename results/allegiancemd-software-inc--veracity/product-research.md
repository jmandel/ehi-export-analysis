# AllegianceMD Software, Inc. — Product Research

Researched: 2026-02-14
Developer website: https://allegiancemd.com

## Overview

AllegianceMD Software, Inc. is a privately held company based in Tulsa, Oklahoma, founded in 1996 (the website claims "28 years of expertise" and "over 20 years" of operation). They develop a cloud-based, all-in-one EHR/practice management/billing platform called **Veracity**, targeted at small-to-mid-sized ambulatory physician practices. The company describes itself as building its product "from the ground up with physician input." Company size is unclear — business databases report conflicting numbers ranging from ~29 to ~500 employees; the true figure is uncertain. The company is privately held with no disclosed funding rounds or acquisitions. The contact listed on CHPL is Mohamed ElMawi (likely the founder/CEO based on domain context).

AllegianceMD competes in the crowded ambulatory EHR space alongside products like eClinicalWorks, athenahealth, and Practice Fusion, positioning itself as an affordable, all-in-one cloud solution with no hidden fees. Third-party review aggregators show a moderate review volume (~40 reviews on FindEMR, ~24 on Capterra) with generally positive ratings (4.0–4.3 out of 5), suggesting a small but established user base rather than a large-scale deployment.

## Product: Veracity

CHPL ID: 10794
CHPL Product Number: 15.02.05.2672.ALLE.01.01.1.220117
Version: 9.1
Certification Date: 2022-01-17

### What It Is

Veracity is a cloud-based, all-in-one EHR, practice management, and billing platform. It is not a modular product where components are sold separately — the vendor emphasizes it is "one system" built as an integrated whole, not "a loosely integrated system." The certified product encompasses the full platform: clinical charting (EMR/EHR), practice management, billing/revenue cycle, patient portal, e-prescribing, telemedicine, and related modules.

The CHPL certification covers a broad set of criteria: (a)(1)–(a)(5) plus (a)(12), (a)(14)–(a)(15) for clinical data; (b)(1)–(b)(3) for transitions of care; (e)(1) and (e)(3) for patient portal/view-download-transmit; (f)(1) and (f)(5) for public health reporting; (g)(7) and (g)(10) for FHIR API access; and (c)(1)–(c)(3) for clinical quality measures. This is a comprehensive ambulatory EHR certification profile. The SED intended user description confirms: "medical practitioners and staff as an electronic medical record and practice management system."

### Users & Market

**Target users:** Physicians, clinical staff, billing staff, practice managers, and patients (via portal). The product targets small to mid-sized ambulatory practices — solo practitioners, primary care offices, multi-specialty groups, and ambulatory surgery centers.

**Specialties supported:** Veracity markets specialty-specific templates for a very broad range of specialties (50+), including: allergy/immunology, anesthesiology, cardiology, chiropractic, dermatology, emergency medicine, endocrinology, family medicine, gastroenterology, general surgery, geriatric medicine, hematology, hospitalist, infectious disease, internal medicine, nephrology, neurology, neurosurgery, OB/GYN, oncology, ophthalmology, optometry, orthopedic surgery, otolaryngology/ENT, pain management, pathology, pediatrics, physical medicine/rehabilitation, plastic surgery, podiatry, primary care, psychiatry, psychology, pulmonary disease, radiology, rheumatology, thoracic surgery, urology, and others. This breadth suggests the product is a general-purpose ambulatory EHR with customizable templates rather than a deeply specialty-specific system.

**Customer base:** The vendor does not disclose customer counts on its website. Third-party review volume is modest (~40–100 reviews across platforms), suggesting a small-to-moderate installed base. Reviews mention users including neurologists, primary care physicians, and billing staff. One review site (FindEMR) mentions behavioral health providers and multi-specialty groups as users.

**Deployment:** Cloud-hosted (SaaS). The vendor emphasizes "100% uptime" with no servers to maintain, no crashes or freezes. Mobile apps available for iOS and Android.

### Modules & Functionality

Based on vendor website descriptions and feature pages, Veracity includes the following integrated modules:

**Clinical EHR/EMR:**
- Customizable clinical templates for charting, with machine learning algorithms that remember provider treatment preferences and documentation patterns for specific diagnoses
- Clinical decision support
- Evidence-based clinical knowledge integration
- Medical calculators
- Problem list, medication list, allergy list management (implied by (a)(1)–(a)(5) certification)
- CPOE for medications and lab orders (certified (a)(1)–(a)(3))
- Drug-drug and drug-allergy interaction checking (certified (a)(4))
- Demographics recording (certified (a)(5))

**E-Prescribing:**
- Electronic prescriptions including controlled substances (EPCS)
- Online medication history
- Prescription Monitoring Program (PMP) integration
- Medication refill management (from mobile app and patient portal)

**Lab Interface:**
- Lab ordering and results retrieval with direct connections to labs
- Customizable lab ordering workflows
- HL7 integration for lab results

**Imaging:**
- Imaging results viewing (mentioned in mobile app description — "view lab/imaging results")
- Diagnostic radiology listed as a supported specialty

**Practice Management & Scheduling:**
- Appointment scheduling with provider schedule management
- Patient self-scheduling through portal
- Appointment reminders via phone, text, and email
- Color-coded schedule views
- Case management (workers' comp, medical, etc.)

**Billing & Revenue Cycle:**
- Charge capture from schedule or EHR with "visits charges memory"
- Claim creation, scrubbing, and submission (electronic claims)
- Batch claim submission or individual claims
- Integrated clearinghouse
- Automatic eligibility verification
- Rejection tracking with daily reports
- Denial and appeal management
- Electronic remittance advice (ERA) posting with color-coded EOBs
- Automatic creation of secondary claims if not forwarded by primary
- Patient statements (electronic)
- Collection module: automated collection letters, export to collection agency, ability to lock patients in collections
- Credit card processing
- Financial analytics dashboard
- Claims follow-up module with task assignment

**Patient Portal:**
- Patient demographics and insurance data entry/update
- Medical history and current medication review
- Online appointment scheduling
- Prescription refill requests
- Secure messaging with practice staff
- View medical records including appointments, clinical summaries, health maintenance, immunization records, medication lists, lab results
- Bill payment and statement viewing/history
- Self-service check-in kiosk (touchscreen for in-office use)

**Telemedicine:**
- Virtual appointment creation and video consultations
- Integrated within the EHR workflow

**Document Management:**
- Unlimited document upload with scanning
- Electronic faxing (unlimited incoming/outgoing) with automatic PDF conversion and customizable fax numbers

**Public Health Reporting:**
- Immunization reporting compatible with state/federal registries via HL7
- Certified for (f)(1) immunization registry reporting and (f)(5) cancer case reporting

**Quality Reporting:**
- MACRA/MIPS compliance tracking and quality reporting dashboard
- Certified for (c)(1)–(c)(3) clinical quality measures

**Value-Based Care:**
- Chronic Care Management (CCM) program: patient enrollment, care plan building, non-face-to-face service tracking for Medicare beneficiaries with multiple chronic conditions
- Annual Wellness Visit (AWV) documentation

**API Access:**
- Certified for (g)(7) application access — patient selection
- Certified for (g)(10) standardized FHIR API

### Data & Content

Based on the modules and features described above, Veracity stores and manages the following data types:

**Clinical data:** Patient demographics, insurance information, medical history, problem lists, medication lists, allergy lists, vital signs, clinical encounter notes/chart notes, clinical summaries, health maintenance records, immunization records, lab orders and results, imaging results, phone encounters, prescription/medication data (including controlled substance prescriptions), clinical decision support alerts, and care plans (for CCM).

**Practice management data:** Appointment schedules, provider schedules, appointment reminders, patient registration data, case management records (workers' comp, etc.), document scans and uploads, faxes (incoming and outgoing).

**Billing/financial data:** Charges, claims (submitted, rejected, denied), EOBs/remittance advice, patient statements, payment records (insurance and patient), collection records and letters, eligibility verification results, credit card transactions, financial analytics/reports.

**Patient portal data:** Patient-entered demographics, insurance data, medical history, medication lists, secure messages between patients and staff, refill requests, appointment requests, and portal access logs (implied by privacy controls where physicians determine what patients can see).

**Communication data:** Secure messages (patient-provider), phone encounter records, fax records, appointment reminder logs.

**Quality/reporting data:** Clinical quality measure calculations, MIPS/MACRA reporting data, immunization registry submissions, cancer case reports.

The vendor's about page notes the system is cloud-based with "100% uptime" claims, suggesting all data is centrally hosted. The patient portal page notes that "the patient does not have access to the doctor's records at any time" — physicians control what patients can see, indicating the clinical record contains more data than what is exposed through the portal.

One area of uncertainty: the vendor website does not describe a **referral management** module in detail, though transitions of care certification (b)(1)–(b)(3) implies the system handles C-CDA documents for care transitions. It's unclear how robust the referral tracking workflow is. The website also does not mention **prior authorization** workflows or **inventory management**, though these may not be relevant for an ambulatory EHR of this type.

# Metasolutions Inc — Product Research

Researched: 2026-02-14
Developer website: https://www.zoommd.com

## Overview

Metasolutions Inc is a small healthcare IT company based in Irvine, California, operating under the ZoomMD brand. The company has been in the healthcare operations space for approximately 18 years and has around 80+ staff members. They serve roughly 100 practices and health organizations, targeting small to mid-sized ambulatory medical offices. Their business model combines cloud-hosted software (EHR, practice management, e-prescribing) with professional services (medical billing/collections and medical transcription). The company contact listed on CHPL is P. S. L. Narashima Rao (spaluri@metasolutionsinc.com), and the phone number is 800-992-6382.

Metasolutions is a small, privately held vendor — not a major player in the EHR market. They appear to focus on providing an integrated, low-cost cloud solution for smaller practices that want EHR + billing services bundled together. Their LinkedIn presence lists both "Metasolutions Inc" and "Meta Business Solutions" profiles, suggesting possible branding overlap.

## Product: ZoomMD

CHPL ID: 11182 (15.04.04.1979.Zoom.41.01.1.221230)
Version: 4.1
Certified: 2022-12-30
SED Intended Users: Outpatient Clinic

### What It Is

ZoomMD is a cloud-based, ONC-certified integrated Electronic Health Record (EHR) and Practice Management (PM) system. It is a fully hosted, web-based solution — customers do not need to manage servers, firewalls, or IT infrastructure. The product is offered with a low monthly subscription fee (starting at $395/month) without long-term commitments. ZoomMD is the single certified product from Metasolutions and encompasses EHR, practice management, e-prescribing, and patient portal capabilities.

The product is broadly certified across 33 ONC criteria, including clinical data (a)(1)–(a)(5), (a)(12), (a)(14); transitions of care (b)(1)–(b)(3); patient portal/VDT (e)(1); clinical quality measures (c)(1)–(c)(3); public health reporting (f)(1), (f)(2), (f)(5), (f)(7); and FHIR API (g)(10). This is a comprehensive ambulatory EHR certification.

### Users & Market

ZoomMD targets small to mid-sized ambulatory medical practices. According to EMRFinder, it is designed for primary care practices including family medicine, internal medicine, pediatrics, and women's health. However, third-party review sites (Software Finder, Capterra) list support for a very broad range of specialties — over 40 — including allergy, cardiology, dermatology, gastroenterology, OB-GYN, orthopedics, psychiatry, urology, and many more. The product serves roughly 100 practices and health organizations per the vendor's own website.

The pricing model ($395/month) and no-upfront-cost structure suggest the target market is smaller, cost-sensitive practices rather than large health systems. The vendor also offers bundled professional billing services, which is a common value proposition for smaller practices that don't have dedicated billing staff.

### Modules & Functionality

**Clinical Documentation / Charting:**
- Multiple charting methods: note dictation, custom templates and macros, auto-pulling chart information into notes, and copying previous notes into current notes (per FindEMR and Software Finder)
- Custom charting capabilities per the vendor website
- Meaningful Use dashboard and patient dashboard

**E-Prescribing (ZoomMD eRx):**
- Electronic prescriptions sent to pharmacies nationwide
- Electronic Prescribing of Controlled Substances (EPCS) support
- Allergy checks, drug interaction checks, and formulary checks
- Integrates with Surescripts Network and NewCropRx (per the certifications page)

**Lab Integration:**
- Lab module with integrated national lab connectivity (per FindEMR)
- Supports CPOE for labs and imaging per ONC certification criteria (a)(2), (a)(3)

**Practice Management / Scheduling:**
- Appointment scheduler
- Patient balance display at check-in
- Insurance eligibility verification at check-in
- Real-time reporting and analytics for payment collection performance

**Billing:**
- Integrated medical billing system
- Superbill system that sends charges in real-time to billers' inboxes or to any practice management system
- Claims tracking and electronic claims submission
- Real-time eligibility verification
- In addition to the billing software, Metasolutions offers a professional medical billing & collections *service* — staffed by experienced billing professionals — that claims >95% first-pass collections and payments in <14 days

**Patient Portal:**
- Patients can log into personalized profiles
- View treatment plans and stay updated
- Two-way communication via chat, messages, conference calls (per Software Finder)
- Patient view/download/transmit per ONC certification (e)(1)

**Telehealth:**
- The vendor website homepage describes ZoomMD as "Cloud EHR, PM & Telehealth"
- However, one third-party source (FindEMR) listed telemedicine as a feature *not* included. This may reflect older information or a discrepancy in feature completeness
- The vendor clearly markets telehealth as part of the product

**Medical Transcription:**
- Dictation from any phone or device with "fast and accurate transcriptions"
- This is a professional service offered alongside the EHR, suggesting the product has workflow integration for dictated notes

**Document Management:**
- Document management system integrating paper/fax documents into the digital workflow
- "Zoom viewer" for document viewing

**Reporting & Quality:**
- 25 CMS clinical quality measures for tracking conditions like hypertension, diabetes, and cancer screening
- Real-time reporting and analytics engine
- Meaningful Use dashboard

**API Access:**
- ZoomMD API (v4.1) with read-only access to patient health data
- Returns data in C-CDA format (base64-encoded XML)
- FHIR API documentation and endpoints available
- API designed for USCDI data elements per Cures Update compliance

**Public Health Reporting:**
- Certified for immunization registries (f)(1), syndromic surveillance (f)(2), electronic case reporting (f)(5), and health care surveys (f)(7)

### Data & Content

Based on the product's feature descriptions and ONC certification, ZoomMD stores and manages:

- **Patient demographics** — required by (a)(5) certification and fundamental to the EHR
- **Clinical notes and encounter documentation** — via custom charting, templates, macros, and dictation/transcription workflow
- **Medication lists and prescriptions** — via CPOE (a)(1) and the eRx module integrated with Surescripts/NewCropRx; includes controlled substance prescribing
- **Allergy and drug interaction data** — allergy checks, drug interaction checks per eRx module
- **Lab orders and results** — via lab module with national lab connectivity and CPOE for labs (a)(2)
- **Imaging orders** — via CPOE for imaging (a)(3), though radiology results handling is less clearly described
- **Problem lists and diagnoses** — implied by (a)(4) certification (drug-diagnosis interaction checking)
- **Vital signs and clinical data** — standard EHR clinical data per (a)(14) implantable device list criteria
- **Implantable device identifiers** — per (a)(14) certification
- **Clinical quality measure data** — 25 CMS measures tracked
- **Billing data** — claims, superbills, charges, insurance eligibility, collections data through the integrated billing module
- **Scheduling data** — appointments, patient follow-ups
- **Insurance information** — eligibility verification and patient balance data
- **Patient portal data** — messages, communications, treatment plan views
- **Documents** — scanned/faxed documents managed through the document management system
- **Transcription records** — dictated notes processed through the transcription service
- **Care transition documents** — C-CDA documents per (b)(1)–(b)(3) certification
- **Public health reporting data** — immunization records, syndromic surveillance data, case reports
- **Medication reconciliation data** — per certification page reference

**Information gaps:** The vendor website and third-party sources provide limited detail on some areas. It's unclear how robust the patient portal messaging and telehealth capabilities are (one source listed telemedicine as absent). The depth of referral management, prior authorization workflows, and specialty-specific data structures is not well documented. The website does not provide detailed feature pages for individual modules — marketing is relatively sparse compared to larger vendors.

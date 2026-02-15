# Medi-EHR, LLC — Product Research

Researched: 2026-02-15
Developer website: https://medi-ehr.com/

## Overview

Medi-EHR, LLC is a small, privately-held EHR vendor headquartered in Bedminster, New Jersey (established circa 2013). The company offers a cloud-based (SaaS) EHR platform serving healthcare practices across the United States, with particular emphasis on ambulatory clinics, ambulatory surgery centers, behavioral health practices, and addiction/residential treatment facilities. The product is built on Oracle 11g and is delivered entirely via web browser — no on-premise installation.

Medi-EHR appears to be a small vendor in the EHR market. There are no publicly available user reviews on major third-party sites (SoftwareFinder, FindEMR, and Slashdot all show zero user reviews). The company does not disclose customer counts, number of users, or revenue. The contact person listed on CHPL certifications is Matthew D'alessandro. The company emphasizes "no cost for customization EVER" and "no hidden costs" as key differentiators, and offers 24/7 U.S.-based support. There is no indication of acquisition, rebranding, or white-labeling — this appears to be an independent, original product.

## Product: Medi-EHR

CHPL IDs: 10831 (version 2.1, certified 2022-02-15)

### What It Is

Medi-EHR is a comprehensive, cloud-based electronic health record system with integrated billing/practice management, scheduling, e-prescribing, patient portal, and telemedicine. It is certified across 37 ONC criteria spanning clinical data (a)(1)–(a)(14), care coordination (b)(1)–(b)(3), clinical quality measures (c)(1)–(c)(3), security (d), patient portal (e)(1), public health reporting (f)(1)–(f)(5), FHIR API (g)(7)–(g)(10), and direct messaging (h)(1). This is a broadly certified, full-featured ambulatory EHR — not a niche or single-purpose module.

The certified product "Medi-EHR" encompasses the entire platform, including all specialty modules. It is not a component of a larger product — the certification covers the whole system.

### Users & Market

Medi-EHR targets small to medium-sized healthcare practices across several clinical settings:

- **Primary care / ambulatory clinics** — the core use case, priced at $495/provider/month
- **Ambulatory Surgery Centers (ASCs)** — dedicated module at $750/OR or procedure room/month
- **Behavioral health practices** — mental health and substance abuse, at $65/user/month
- **Residential treatment facilities** — addiction treatment centers with inpatient beds, at $150/bed
- **Workers' compensation / no-fault practices** — specialized claims and documentation module

Specialties mentioned on the website include OB/GYN, cardiology, orthopedics, pediatrics, physical therapy, and maternal-fetal medicine, with customizable templates for each.

No customer counts, case studies, or notable deployments are publicly available. The lack of any third-party reviews (zero reviews on SoftwareFinder, FindEMR, and Slashdot) suggests a small install base.

### Modules & Functionality

Based on vendor website and third-party listing pages, Medi-EHR includes the following modules and features:

**Clinical EHR / Documentation:**
- Clinical charting and note-taking with customizable templates
- Problem lists, medication lists, vital signs, immunizations
- Progress notes and clinical histories
- Demographics management
- Lab results and radiology reports integration (with lab and radiology interface request forms available)
- Document management
- E/M coding support
- Consent module for managing patient consent forms
- Custom forms and reports

**E-Prescribing:**
- Electronic prescribing integrated with Surescripts
- Electronic Prescription of Controlled Substances (EPCS) with identity verification and multi-factor authentication

**Computerized Provider Order Entry (CPOE):**
- Certified for CPOE for medications (a)(1), lab orders (a)(2), and diagnostic imaging (a)(3)
- Drug-drug and drug-allergy interaction checking (a)(4)

**Scheduling:**
- Appointment management and scheduling
- Online self-scheduling (patient-facing)
- Appointment reminders

**Billing & Practice Management:**
- Integrated billing module (available standalone at $250/provider/month or $150 with EHR)
- Superbill creation
- Revenue cycle management
- Integration with Optum, Waystar, and Change Healthcare clearinghouses
- Insurance benefits verification
- Workers' comp and no-fault claims processing

**Patient Portal:**
- View/download medical records
- Secure messaging with providers
- Prescription refill requests
- Online appointment scheduling and reminders
- Bill payment
- Digital check-in

**Patient Kiosk:**
- Pre-visit intake on any device
- Clinical history capture
- Consent form completion
- Multilingual support

**Telemedicine:**
- Built-in video conferencing
- Secure messaging
- Patient engagement tools for virtual visits

**Communications:**
- SMS/texting services
- Faxing
- Email communications
- Secure messaging

**Ambulatory Surgery Center Module:**
- Pre-op to post-op patient management
- Surgical scheduling
- Reports and customizable modules
- (Details are sparse on the website — specific surgical workflows, anesthesia documentation, and operative note features are not described)

**Behavioral Health Module:**
- Mental health and substance abuse treatment documentation
- Customizable templates for behavioral health diagnoses and treatment plans
- (The website does not describe specific behavioral health assessments, screening tools, or treatment planning features in detail)

**Residential Treatment Facility Module:**
- In-facility and outpatient scheduling
- Secure tracking for addiction and mental health centers
- Compliance-focused documentation
- (Bed management details, group therapy tracking, and medication administration record features are not explicitly described)

**Integrations:**
- Surescripts (e-prescribing)
- Quest Diagnostics (lab results)
- Healthix (health information exchange)
- Optum, Waystar, Change Healthcare (claims clearinghouses)
- Lab and radiology interface support (via request)
- Health Information Exchange (HIE) connectivity
- Custom API support
- Direct messaging (certified for (h)(1))
- FHIR API (certified for (g)(7)–(g)(10))

**Mobile:**
- Web-based access on any device
- Mobile app referenced ("Practice EHR Go" mentioned in a blog post title, though this may be referencing a different product)

**Public Health Reporting:**
- Immunization registry transmission (f)(1)
- Syndromic surveillance (f)(2)
- Electronic case reporting (f)(5)

**Clinical Quality Measures:**
- CQM recording (c)(1)
- CQM export (c)(2)
- CQM reporting (c)(3)

### Data & Content

Based on the certified criteria and described features, Medi-EHR stores and manages the following categories of data:

**Clinical data** (supported by (a) criteria and product descriptions):
- Patient demographics
- Problem lists / diagnoses
- Medication lists and prescription history
- Allergies (drug-allergy interaction checking is certified)
- Vital signs
- Immunization records
- Lab orders and results (Quest Diagnostics integration)
- Radiology/diagnostic imaging orders and reports
- Progress notes and clinical documentation
- Clinical histories
- Consent forms

**Administrative/operational data:**
- Appointment schedules
- Insurance and benefits information
- Billing data: superbills, claims, payment records
- Workers' compensation and no-fault claim submissions
- Practice management data

**Patient-generated/portal data:**
- Patient portal messages
- Prescription refill requests
- Online appointment requests
- Patient intake forms (via kiosk)
- Bill payments

**Care coordination data** (supported by (b) criteria):
- Transition of care documents (C-CDA)
- Clinical information reconciliation records
- Electronic prescriptions transmitted via Surescripts
- Direct messages

**Public health data:**
- Immunization registry submissions
- Syndromic surveillance reports
- Electronic case reports

**Telemedicine data:**
- Video visit records
- Virtual encounter documentation

**Specialty-specific data:**
- Behavioral health: mental health diagnoses, treatment plans, substance abuse treatment documentation
- ASC: surgical scheduling, pre-op/post-op documentation (though details are sparse)
- Residential treatment: inpatient tracking, addiction treatment records

**Audit and security data** (supported by (d) criteria):
- Audit logs
- Access records
- Authentication records
- Amendment tracking

**Gaps and uncertainties:**
- The website provides limited detail on the ASC module's specific surgical data (operative notes, anesthesia records, pathology results, surgical instrument tracking)
- The behavioral health module's specific assessment tools, treatment plan templates, and outcome measures are not described
- The residential treatment module's bed management, medication administration records, and group therapy tracking are not detailed
- Whether the system stores scanned documents, images (clinical photos), or other unstructured content is not clear from available sources
- The "Practice EHR Go" mobile app mentioned in a blog post title may reference a different product or may be a module name — this is ambiguous
- No user reviews exist to confirm real-world data usage patterns

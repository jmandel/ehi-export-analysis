# CursaHealth LLC — Product Research

Researched: 2026-02-15
Developer website: https://cursahealth.com/

## Overview

CursaHealth LLC is a small healthcare IT company based in Greenfield, Wisconsin, with approximately 11–50 employees (per LinkedIn and ZoomInfo). The company has been in the medical technology field for over a decade, working with physicians, psychiatrists, and other healthcare professionals to develop their cloud-based platform. They offer a combined EHR, practice management, and medical billing platform targeting small-to-medium-sized ambulatory practices across several specialties including internal medicine, family medicine, OB/GYN, pediatrics, and mental health. The company is privately held with no indication of venture funding, acquisitions, or corporate parent. Their contact person for ONC matters is Faisal Shahzad. The product is priced at $199/provider/month for EHR only, or 6% of collections for an all-inclusive EHR + practice management + billing bundle, suggesting it competes on affordability for smaller practices.

## Product: CursaHealth EHR

CHPL ID: 11735 (CursaHealth EHR v2.0, certified 2025-12-29)

### What It Is

CursaHealth EHR (also marketed as "Cursa Health WebEHR") is a cloud-based, all-in-one platform combining electronic health records, practice management, medical billing, patient portal, and transcription services. The certified module appears to be the entire product — there is no indication of separate product lines or distinct platforms. The certification is broad, covering 37 criteria across clinical (a)(1)–(a)(15), transitions of care (b)(1)–(b)(2), patient portal (e)(1), public health reporting (f)(1)–(f)(3), FHIR APIs (g)(7)–(g)(10), and direct messaging (h)(1). There is no mobile application; the product is entirely web-based.

The SED intended user description lists: physicians, physician assistants, nurse practitioners, clinical pharmacists, medical assistants, clinical staff, and front desk staff — indicating this is designed as a full practice platform used by both clinical and administrative staff.

### Users & Market

CursaHealth targets small-to-medium ambulatory practices. Supported specialties explicitly listed include internal medicine, family medicine, OB/GYN, pediatrics, and mental health/psychiatry. The about page mentions working with "physicians, psychiatrists, and a myriad of other healthcare professionals," suggesting some breadth beyond those core specialties.

No customer count or specific deployment numbers were found. The company is very small (11–50 employees) and does not appear in major EHR market share analyses. A single client testimonial from Arman Tahir MD appears on their website. Third-party review sites (FindEMR, SoftwareFinder) show very few user reviews — SoftwareFinder reported 0 reviews, while another source referenced an aggregate of ~10 reviews with 4-star average ratings. This is consistent with a small vendor serving a limited customer base.

### Modules & Functionality

Based on vendor materials and third-party listings, CursaHealth EHR includes:

**Clinical Documentation / EHR:**
- Patient encounters with categorized visit data (described as eliminating paper records)
- Specialty-specific EHR modules for internal medicine, family medicine, OB/GYN, pediatrics, and mental health
- CPOE for medications, labs, and imaging (per ONC certification criteria (a)(1)–(a)(3))
- Drug interaction checks (per certification criteria (a)(4))
- Demographics recording (per (a)(5))
- Patient problem list, medication list, and allergy list (implied by (a)(5) and clinical criteria)
- Family health history (per mandatory disclosures page)
- Implantable device tracking (per (a)(14))
- Social/psychological/behavioral data (per (a)(15))
- Clinical decision support tools with configurable alerts and reminders based on evidence-based guidelines
- Immunization tracking
- Vital signs recording

**Practice Management / Scheduling:**
- Appointment scheduler with color-coded calendars
- Patient self-booking via patient portal
- Patient check-in workflows
- Payment recording
- Visit coding

**Billing:**
- Medical billing services (managed service offering, not just software)
- Accounts receivable management
- Medical coding review and assistance
- Physician credentialing services
- Insurance claims processing
- Electronic claims generation
- Three pricing tiers: EHR-only ($199/provider/month), billing-only (5% of collections), all-inclusive (6% of collections)

**Lab Integration:**
- Automated lab order and result transfer with partner laboratories
- Named lab partners include Apollo Laboratories, Quest Diagnostics, ConnectDX, LabTrack, and molecular testing labs
- Real-time lab data access within patient EHR

**Patient Portal / Personal Health Records:**
- Patient access to medications, allergies, assessments, immunizations, and vital signs
- Activity log showing patient interactions over time
- Appointment scheduling
- Form completion
- View test results
- View, download, and transmit health information (per (e)(1))

**Secure Messaging:**
- HIPAA-compliant encrypted messaging between providers and patients
- File attachment capability

**Transitions of Care:**
- Clinical information reconciliation and incorporation (per (b)(2))
- Transitions of care document support (per (b)(1))
- Direct secure messaging (per (h)(1))

**Public Health Reporting:**
- Immunization registry transmission (per (f)(1))
- Reportable lab test reporting (per (f)(2))
- Syndromic surveillance (per (f)(3))

**Quality Measures:**
- CMS quality measure support (at minimum CMS 122 — diabetes control)
- Clinical quality measure recording and reporting (per (c)(1)–(c)(3))

**Transcription Services:**
- Medical transcription with fast turnaround (listed as a service, may be a managed service rather than built-in software feature)

**FHIR API Access:**
- Standardized API for patient and population services (per (g)(7)–(g)(10))

**Notable Absence:**
- E-prescribing / EPCS (electronic prescribing for controlled substances) is not mentioned anywhere in vendor materials, third-party reviews, or the mandatory disclosures page. The certified criteria do not include (b)(3) which covers e-prescribing. This is a notable gap — it's unclear whether prescriptions are handled outside the system or simply not a certified feature.

### Data & Content

Based on the features described above, CursaHealth EHR stores and manages:

- **Patient demographics** (name, DOB, contact info, insurance — per (a)(5) certification and feature descriptions)
- **Clinical encounter data** — visit documentation stored "categorically," including chief complaints, exam findings, assessments (per vendor product page)
- **Medication lists** (per patient portal showing medications; CPOE for medications per (a)(1))
- **Allergy lists** (per patient portal showing allergies)
- **Problem/diagnosis lists** (implied by clinical criteria)
- **Vital signs** (per patient portal)
- **Immunization records** (per patient portal and public health reporting criteria)
- **Lab orders and results** (explicit lab integration with multiple partners)
- **Imaging orders** (per CPOE for imaging (a)(3))
- **Family health history** (per mandatory disclosures)
- **Social/psychological/behavioral data** (per (a)(15) certification)
- **Implantable device information** (per (a)(14) certification)
- **Clinical decision support rules and alerts** (per feature descriptions)
- **Appointment/scheduling data** (per scheduling module)
- **Billing and claims data** (per billing module — claims, payments, coding, A/R)
- **Patient portal messages** (per secure messaging feature)
- **Transitions of care documents** (C-CDAs per (b)(1))
- **Activity/audit logs** (per patient portal activity log feature)
- **Clinical quality measure data** (per (c)(1)–(c)(3))
- **Transcription records** (if transcription is stored within the EHR rather than as a separate service)

The billing component is somewhat ambiguous — it could be purely a managed service where CursaHealth staff handle billing externally, or it could be integrated software with billing data stored in the same system. The all-inclusive pricing tier (6% of collections for EHR + PM + Billing) and the description of "simplified billing processes & transparent reporting tools" suggest at least some billing data resides within the platform.

---

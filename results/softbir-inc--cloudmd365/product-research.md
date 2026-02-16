# Softbir, Inc. — Product Research

Researched: 2026-02-16
Developer website: https://softbir.com

## Overview

Softbir, Inc. is a small healthcare software company headquartered in Indianapolis, Indiana (7345 Woodland Drive, Indianapolis, IN 46278), founded in 2019. The company describes itself as providing "Medical Software Solutions for an Accelerating World." It has approximately 20–21 employees and estimated annual revenue of ~$1.8M (per ZoomInfo/Bouncewatch, as of mid-2025). The CEO is Happy Dhani, who has a background in pharmacy (Pharmaneek Pharmacy) and healthcare services (Access Therapies Inc.). The CHPL contact is Leo Obrique, who has 30+ years of IT experience and holds a B.S. in Computer Science.

Softbir operates multiple related brands/products:
- **CloudMD365** — the ONC-certified EHR product (now redirects to DocIndy)
- **DocIndy** — the current consumer-facing telemedicine brand (docindy.com)
- **iVisitDoc** — a telehealth platform and EMR system (ivisitdoc.com)
- **eMARneek** — electronic Medication Administration Record module

The company appears to be a very small vendor with minimal web presence. The main website (softbir.com) contains almost no content — just a header with "Medical Software Solutions." The CloudMD365 domain (cloudmd365.com) now 301-redirects to docindy.com. There is no evidence of a significant customer base, no third-party reviews on G2/Capterra/KLAS, and no case studies or press coverage. The company is unfunded (no disclosed investment rounds per Bouncewatch/Crunchbase).

The social media handles reference "pharmaneek," suggesting origins in the pharmacy/pharmaceutical space. The company appears to serve a dual role: developing healthcare software tools (the B2B side) and operating a direct-to-consumer telehealth service (the B2C side via DocIndy/iVisitDoc).

## Product: CloudMD365

CHPL ID: 10282

### What It Is

CloudMD365 is the ONC-certified health IT product from Softbir. Based on the abandoned trademark filing (Serial Number 90211494, filed September 2020), CloudMD365 is described as "Software for patient/healthcare monitoring and management services, namely for use in Chronic Care Management (CCM)/Transitional Care Management (TCM), Diabetes Self-Management Training (DSMT), Remote Patient Monitoring (RPM), Electronic Medication Administration Record (eMAR), Electronic Health Record (EHR) and telemedicine." First use was reported as May 2018, with first use in commerce August 2019.

The CloudMD365 domain now redirects to docindy.com, and the product appears to have been rebranded/subsumed into the DocIndy/iVisitDoc ecosystem. It is unclear whether "CloudMD365" still exists as a distinct product or whether the certification applies to the combined DocIndy/iVisitDoc platform.

The certified criteria include:
- **(a)(1)–(a)(5)**: Core clinical data — CPOE for medications, labs, diagnostic imaging; demographics; problem list; medication list; medication allergy list
- **(b)(10)**: EHI export
- **(b)(11)**: Care plan — indicating the product supports care plan data
- **(d)(1)–(d)(13)**: Security and privacy criteria (authentication, encryption, auditing, etc.)
- **(g)(3)–(g)(5), (g)(7), (g)(10)**: Safety-enhanced design, quality management, accessibility, application access (FHIR API), standardized API

Notably absent from the certification: (a)(9) clinical decision support, (a)(10) drug interactions, (a)(12)-(a)(14) family health history/patient-specific education/implantable device list, (b)(1)-(b)(3) transitions of care/clinical information exchange, (e)(1) patient portal/view-download-transmit, (f)(1)-(f)(7) public health reporting. This suggests a relatively limited clinical certification — core clinical data and FHIR API access, but not a full-featured EHR certification.

### Users & Market

The SED intended user description is simply "Healthcare Provider." Based on the iVisitDoc EMR tour (which appears to be the clinical-facing version of this platform), the target users appear to be:

- **Behavioral health / substance abuse treatment providers** — The EMR tour heavily emphasizes therapy session notes (SOAP, DAP formats), ICD-10 and DSM-5 diagnosis coding, treatment plans, pre-admission workflows, patient occupancy tracking across multiple locations, utilization review, rounds and security checks, homework planners, and aftercare management. This strongly suggests a behavioral health / residential treatment orientation.
- **Telehealth providers** — Psychiatrists, psychologists, therapists, social workers, general medicine physicians, dermatologists, and dietitians (per the provider FAQ).
- **Care coordinators** — For CCM/TCM programs, managing chronic conditions with Medicare billing codes (99490, 99487, 99489).

No customer numbers, notable deployments, or market share data could be found. Given the company's size (~20 employees, ~$1.8M revenue), the customer base is likely very small.

### Modules & Functionality

Based on the iVisitDoc EMR tour page (ivisitdoc.com/emr-tour/), the platform includes:

**Patient Management & Admissions:**
- Pre-admission and patient intake workflows
- Full-strength CRM for admissions
- Admissions with discharge visibility
- Patient occupancy tracking across multiple locations
- Verification of benefits (24/7)

**Clinical Documentation:**
- Progress notes with customizable wording templates
- Therapy session notes in SOAP and DAP formats
- ICD-10 and DSM-5 diagnosis coding
- Assessment tools (pre-loaded and customizable forms)
- Treatment plans linked to patient journeys
- Chart Check (documentation auditing)
- Outcome measures tracking
- MNDD (Medical Necessity Documentation Data generation)
- Signature level controls

**Medication & Prescription Management:**
- Medication management interface with device integration
- eRx (electronic prescribing) for pharmacy orders
- Lab interface with 90+ testing partners for order processing

**Care Coordination:**
- Appointment calendar (daily/weekly/monthly tracking)
- Utilization Review functionality
- Rounds and security checks on customized schedules
- Homework planner with pre-existing assignment templates
- Discharge planning tools
- Aftercare management

**Communication & Telehealth:**
- HIPAA-compliant messaging and telehealth
- Secure internal messaging with alerts
- Patient surveys and secure signatures (patient and/or guardian)

**Billing:**
- Integrated billing (described but not detailed on the EMR tour page)
- CCM/TCM billing (Medicare codes 99490, 99487, 99489, with reimbursements ~$40–$142)

**eMARneek (eMAR Module):**
- Automates medication administration record keeping
- Notifies nurses when it is time to reorder certain drugs
- Bar code technology that verifies current quantities and dosages of every medication

**Telehealth Services (Consumer-Facing):**
- Video and messaging-based consultations
- General medicine, mental health, dermatology, and nutrition services
- Asynchronous image-based dermatology consultations
- Integrated e-prescribing (excluding controlled substances)
- Prescription management and refills

### Data & Content

Based on the features described above, the product manages the following types of data:

**Clinical data** (confirmed by certified criteria and EMR features):
- Patient demographics (a)(2)
- Problem lists with ICD-10/DSM-5 coding (a)(3)
- Medication lists (a)(4)
- Medication allergy lists (a)(5)
- CPOE orders for medications, labs, and imaging (a)(1)
- Care plans (b)(11)
- Progress notes and session notes (SOAP, DAP)
- Treatment plans
- Assessment forms
- Outcome measures
- Clinical lab results (via lab interface with 90+ partners)

**Medication administration data** (via eMARneek):
- Medication administration records
- Drug quantities and dosage verification (bar code scanning)
- Reorder notifications

**Administrative/operational data:**
- Pre-admission and admission records
- Discharge planning records
- Patient occupancy data across locations
- Benefits verification data
- Utilization review records
- Appointment/scheduling data
- Homework assignments (behavioral health)
- Aftercare records

**Billing data:**
- Integrated billing (details sparse)
- CCM/TCM billing codes and documentation

**Communication data:**
- HIPAA-compliant messages (provider-to-provider and provider-to-patient)
- Telehealth visit records (video and messaging)
- Patient surveys
- Electronic signatures (patient and guardian)
- Dermatology consultation images

**Patient-provided data:**
- Medical history disclosures (completed before consults)
- Patient-uploaded images (dermatology)

**Gaps/Uncertainty:**
- The website does not clearly describe document management, patient portal functionality, or radiology/imaging storage beyond the dermatology use case.
- No evidence of public health reporting capabilities (no (f) criteria certified).
- No evidence of transitions of care / C-CDA document exchange (no (b)(1)-(b)(3) certified).
- The relationship between CloudMD365 (the certified product name) and the iVisitDoc EMR (the apparent current clinical platform) is unclear — it's uncertain whether they are the same system or separate systems sharing a database.
- The billing module is mentioned but not described in detail; it's unclear how comprehensive it is (claims management? ERA/EOB processing? patient statements?).
- Remote Patient Monitoring (RPM) is mentioned in the trademark filing and on older CloudMD365 marketing, but the RPM page on ivisitdoc.com returned a 404 error, suggesting this feature may have been discontinued or is not currently active.

---

## Ecosystem Notes

Softbir operates a small ecosystem of interconnected healthcare products under multiple brand names:

| Brand | Domain | Role |
|-------|--------|------|
| Softbir | softbir.com | Parent company (minimal website) |
| CloudMD365 | cloudmd365.com → docindy.com | ONC-certified product name (redirects to DocIndy) |
| DocIndy | docindy.com | Current consumer-facing telemedicine brand |
| iVisitDoc | ivisitdoc.com | Telehealth + EMR platform (also has a shop for weight-loss medications) |
| eMARneek | (module within CloudMD365/DocIndy) | Electronic Medication Administration Record |

The iVisitDoc site also operates as a direct-to-consumer telehealth marketplace (shop.docindy.com) selling weight-loss medications (compounded semaglutide, tirzepatide, Ozempic, Wegovy, Zepbound) with a provider network model. This appears to be a separate business line from the EMR/EHR certification.

The product appears to be cloud-hosted (the name "CloudMD365" implies this, and the telehealth model requires it). The company operates out of a single location in Indianapolis.

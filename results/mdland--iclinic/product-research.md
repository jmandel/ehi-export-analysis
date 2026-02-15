# MDLAND — Product Research

Researched: 2026-02-14
Developer website: https://www.mdland.com/

## Overview

MDLand International Corp is a small digital health technology company founded in 1999, headquartered in Great Neck, New York (185 Great Neck Rd, Suite 4J). The company has approximately 75 employees spread across 4 continents. MDLand brands itself as "developed by physicians for physicians" and focuses on cloud-based EHR, practice management, billing, and emerging digital health solutions for ambulatory/outpatient physician practices. Their primary product is iClinic, which comes in Professional (solo/small/medium practices) and Enterprise (large physician groups, MSOs, IPAs, ACOs) editions.

MDLand serves primarily outpatient clinics and physician practices in the United States. Notable customers mentioned in third-party databases include Northwell Health, NYC Health + Hospitals, SOMOS Community Care, and Pain Physicians NY — suggesting a concentration in the New York metro area. The vendor appears to be a small, privately held company with no evidence of recent acquisitions or mergers. Their contact person (Steve Peng) is listed on CHPL. The product is sold as an annual per-provider license with monthly subscription pricing.

## Product: iClinic

CHPL IDs: 9814

### What It Is

iClinic is a comprehensive, cloud-based ambulatory EHR and practice management system. The certified version is v12.3 (certified December 2018). It is a unified platform that combines clinical documentation, e-prescribing, billing/claims management, scheduling, patient portal, telehealth, lab interfacing, care management, and population health tools into a single system. The CHPL certification covers a broad set of criteria — clinical data (a)(1)-(a)(5), (a)(12), (a)(14); transitions of care (b)(1)-(b)(3); patient portal (e)(1), (e)(3); public health reporting (f)(1); FHIR APIs (g)(7), (g)(10); and clinical quality (c)(1)-(c)(3) — indicating this is a full-featured ambulatory EHR, not a niche or specialty-only module.

The product comes in two editions:
- **iClinic Professional** — for solo, small, and medium-sized practices
- **iClinic Enterprise** — for large physician organizations, MSOs, IPAs, ACOs, with added scalability, multi-provider network data sharing, and organizational compliance features

Both editions share the same core EHR platform.

### Users & Market

The SED intended user description is "Outpatient Clinic." Day-to-day users include physicians, clinical staff, billing staff, and practice managers. Patients interact with the system through the iClinicHealth patient-facing app.

The product targets ambulatory practices of all sizes. Third-party data suggests MDLand customers span from small practices to large healthcare organizations, concentrated in the healthcare and non-profit sectors, primarily in the United States. Notable users include large New York-based health systems (Northwell Health, NYC Health + Hospitals) and community care organizations (SOMOS Community Care). No specific total user count or practice count was found in public sources.

MDLand's go-to-market appears to be direct sales. The product is cloud-hosted, with minimum client requirements of Windows 7/Mac OS, 8GB RAM, 80GB storage, 19" monitor, and broadband internet (5M down/3M up).

### Modules & Functionality

Based on vendor website, product pages, and third-party sources, iClinic includes the following modules and capabilities:

**Clinical Documentation / EHR Core:**
- Patient demographics and registration (with photo capture, ID scanning, electronic signing)
- Medication ordering with drug interaction checking
- Allergy lists
- Problem/condition lists
- Clinical decision support
- Customizable templates for clinical documentation
- Audit logging

**E-Prescribing:**
- Electronic prescribing integrated within the EHR
- EPCS (Electronic Prescribing of Controlled Substances) via Surescripts with DUO two-factor authentication
- Medication management and renewals

**Lab & Imaging Interfacing:**
- Direct lab ordering within the EHR
- Customizable lab panels
- Abnormal result notifications
- Result trend tracking over time
- Connectivity with national and local laboratories, radiology/diagnostic imaging centers, hospitals, RHIOs, and HIEs

**Billing & Practice Management:**
- Electronic claim submission to virtually any payer/plan
- Instant claim status updates
- Electronic payment posting (1-2 week turnaround)
- Rejected/denied claim management with one-click resubmission
- Automatic insurance eligibility checking
- Integrated billing within the EHR (not a separate system)
- MACRA/MIPS and Meaningful Use quality measure reporting

**Scheduling:**
- Web-based appointment scheduling for multiple providers
- Appointment creation, tracking, and management from any location

**Document Management:**
- Centralized document repository (lab results, digital images, consultation letters, immunization records, forms)
- Scanning and uploading
- File organization

**Patient Portal / Patient Engagement (iClinicHealth):**
- Cross-platform mobile app (iOS and Android) for patients
- View medical history, visit records, vaccination records
- View lab results with notifications
- View active medications and request refills
- Book, reschedule, or cancel appointments
- Secure messaging with providers
- myMonitor — patient health data tracking that syncs into the medical chart
- Encrypted, HIPAA-compliant

**Telehealth:**
- HIPAA-compliant video visits integrated within the EHR
- Scheduling and conducting visits from iClinic EHR or iClinic Office iPad app
- Patient access via iClinicHealth app or SMS link
- Full workflow from scheduling through consultation, diagnosis, treatment, and care management

**Care Management Suite:**
- Chronic Care Management (CCM) — for patients with 2+ chronic conditions: enrollment, care plans, monitoring, automated reporting
- Remote Patient Monitoring (RPM) — home-based patient monitoring with LiveCare Link+ devices (per 2020 press release); proactive intervention to prevent hospitalizations
- Transitional Care Management (TCM) — post-discharge care coordination with required 2-business-day patient contact
- Collaborative Care Model (CoCM) — mental health treatment with shared care plans for depression and anxiety
- Principal Care Management (PCM) — for patients with a single chronic condition
- Patient consent/enrollment forms, automatic time tracking, CMS incentive program support

**Population Health & Analytics:**
- Actionable insights and analytics
- Care gap identification
- Quality score management
- Value-based care/payment program support

**Mobile Apps (Provider-Facing):**
- **iClinic Anywhere** — iPhone and Android app for providers: scheduling, inbox messages, lab/imaging results, e-prescriptions
- **iClinic Office** — HIPAA-compliant iPad app: patient sign-in, scheduling, customizable medical forms, inbox messages, lab/imaging results, e-prescriptions

**Public Health Reporting:**
- Interfaces with state and local immunization registries
- Cancer registry reporting
- Syndromic surveillance
- Electronic case reporting

**Interoperability:**
- Transitions of care / C-CDA document exchange
- FHIR API access (g)(7), (g)(10)
- HIE and RHIO connectivity
- Direct messaging

### Data & Content

Based on the features and modules described above, iClinic stores and manages:

- **Patient demographics** — registration info, photos, ID scans, electronic signatures, insurance information
- **Clinical records** — encounter notes, clinical documentation (via customizable templates), problem lists, vital signs
- **Medications** — active medication lists, prescription history, e-prescribing records (including controlled substances)
- **Allergies** — allergy and intolerance lists
- **Lab results** — ordered lab tests, results, trending data, abnormal result flags
- **Imaging** — imaging orders and results (via interfaces with radiology/diagnostic imaging centers)
- **Immunization records** — vaccination history, registry submissions
- **Documents** — scanned documents, uploaded files, consultation letters, forms, digital images
- **Scheduling data** — appointments, provider schedules
- **Billing/claims data** — electronic claims, claim statuses, payment postings, eligibility checks, denied/rejected claim records
- **Patient portal messages** — secure messaging between patients and providers
- **Telehealth records** — video visit records/documentation
- **Care management data** — CCM/RPM/TCM/CoCM/PCM enrollment, care plans, time tracking, patient monitoring data (vitals from remote devices)
- **Population health/analytics** — quality measures, care gap data, quality scores
- **Public health reports** — immunization registry submissions, syndromic surveillance data, case reports, cancer registry reports
- **Clinical decision support** — alerts, drug interaction checks
- **Audit logs** — system audit trails

The website does not clearly describe whether the system stores referral tracking data, patient education materials, or detailed procedure/surgical documentation. Given the ambulatory focus, inpatient-specific data types (bed management, OR scheduling, etc.) are not expected. The billing module appears to be built-in rather than a separate product, based on vendor descriptions of "integrated electronic billing" and user reviews confirming billing convenience within the system.

---

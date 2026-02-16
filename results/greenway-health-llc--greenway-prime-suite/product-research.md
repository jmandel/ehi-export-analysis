# Greenway Health, LLC — Product Research

Researched: 2026-02-16
Developer website: https://www.greenwayhealth.com/

## Overview

Greenway Health, LLC is a privately held ambulatory healthcare IT company headquartered in Tampa, Florida, with roots dating back to 1977 when Medical Manager Corporation launched one of the first medical practice management software systems. The company's current form emerged in 2013 when Vista Equity Partners combined three portfolio companies: Greenway Medical Technologies (acquired for $644M), Vitera Healthcare Solutions (formerly Sage Software Healthcare, which itself had acquired the Medical Manager product line), and SuccessEHS. The combined entity was rebranded as Greenway Health. Vista Equity Partners remains the owner.

Greenway serves approximately 55,000+ providers across 40+ specialties and over 10,000 partner organizations, focused exclusively on the ambulatory/outpatient market. The company employs roughly 1,000 people. Their customer base includes independent practices, multi-site groups, FQHCs, and specialty practices across primary care, OB-GYN, orthopedics, pediatrics, GI, and tribal health, among others.

Greenway maintains two core EHR platforms — **Prime Suite** and **Intergy** — with reports indicating that Prime Suite is being sunset in favor of Intergy as the go-forward platform. As of late 2025, both are still actively certified and supported.

## Product: Greenway Prime Suite

CHPL IDs: 11352 (v21, certified 2023-10-03), 11681 (v22, certified 2025-08-14)

### What It Is

Greenway Prime Suite is an integrated ambulatory EHR and practice management system designed for outpatient medical practices. It is a comprehensive platform that combines clinical documentation, practice management, billing/revenue cycle, patient engagement, and e-prescribing in a single system. The product is available as both cloud-hosted (AWS-based) and on-premise deployments.

The certified module covers clinical and administrative functionality but is part of a larger Greenway product ecosystem that includes separately branded add-ons: Greenway Patient Portal, Greenway Patient Connect (patient intake), Greenway Clinical Assist (AI documentation), Greenway Document Manager, Greenway Telehealth, Greenway Exchange (interoperability hub), and Greenway Revenue Services (outsourced RCM). The certification spans a broad set of ONC criteria including clinical data ((a)(1)–(a)(5), (a)(12), (a)(14), (a)(15)), transitions of care ((b)(1)–(b)(3)), patient access ((e)(3)), public health reporting ((f)(1)), and FHIR API access ((g)(7), (g)(9), (g)(10)), indicating a full-featured clinical and interoperability platform.

### Users & Market

The intended users are "healthcare professionals in an outpatient ambulatory setting" per the CHPL metadata. Day-to-day users include physicians, nurses, clinical staff, billing staff, practice managers, and front office schedulers. Patients interact through the patient portal.

Prime Suite serves practices across 40+ medical specialties, with particular strength in primary care, internal medicine, OB-GYN, orthopedics, pediatrics, and gastroenterology. Greenway's marketing highlights specialty-specific templates (4,000+ shareable, customizable templates) and workflows. The product also has NCQA PCMH (Patient-Centered Medical Home) pre-validation, suggesting significant use in primary care and FQHC settings.

Notable context: Greenway has indicated Prime Suite is being phased out in favor of Intergy as the consolidated platform. A 2021 press release announced "doubling investment" in both platforms, but subsequent market signals and user reports suggest Greenway is migrating Prime Suite customers to Intergy. This is relevant because it means Prime Suite has a large legacy installed base even as new sales may be winding down.

### Modules & Functionality

Based on vendor materials, third-party reviews, and product documentation, Prime Suite includes the following functional areas:

**Clinical Documentation / EHR:**
- Over 4,000 customizable, shareable clinical templates with specialty-specific configurations (greenwayhealth.com, emrsystems.net)
- Problem lists, diagnoses, medical history tracking, clinical notes (emrsystems.net reviews)
- ICD-10 coding support with E/M coding assistance (emrsystems.net, emrfinder.com)
- Clinical decision support and alerts (implied by (a)(2), (a)(4), (a)(5) certification criteria)
- Voice recognition / speech-to-text integration for documentation (ehrguide.org)
- AI-assisted clinical documentation via Greenway Clinical Assist add-on (greenwayhealth.com)

**E-Prescribing (eRx):**
- Electronic prescription generation and transmission to pharmacies
- Medication history access, formulary checks, drug interaction alerts (search results from softwarefinder, microwize.com)
- Certified for CPOE ((a)(1)) and drug-drug/drug-allergy interaction checking ((a)(4))

**Practice Management / Scheduling:**
- Appointment scheduling across multiple locations and providers
- Patient check-in and registration workflows
- Insurance eligibility verification
- Resource management across multi-site practices (search results, emrsystems.net)

**Billing & Revenue Cycle:**
- Integrated medical billing and claims management
- Claims scrubbing, submission, and denial management
- Clearinghouse integration for claims processing
- Payment processing and tracking
- Multi-location billing consolidation (emrsystems.net, emrfinder.com, greenwayhealth.com)
- Optional outsourced Revenue Cycle Management services via Greenway Revenue Services

**Patient Portal:**
- Patient access to medical records, lab results, and visit summaries
- Secure messaging between patients and providers
- Online appointment requests
- Health history forms and patient intake
- VDT (View, Download, Transmit) compliant records access
- Family/health advocate access to records on behalf of patients
- Built on SMART-on-FHIR technology (greenwayhealth.com/solutions/patient-portal)

**Patient Engagement (Greenway Patient Connect):**
- Online patient intake forms that write directly into the EHR
- Self-service scheduling and registration
- Multi-channel appointment reminders (greenwayhealth.com)

**Document Management:**
- Greenway Document Manager for digital document workflows
- Scanning and attachment of external documents to patient records (implied by product description)

**Lab Integration:**
- Bi-directional lab interfaces for ordering and receiving results
- Integration with diagnostic equipment and imaging devices
- Described as able to "seamlessly integrate with almost any type of diagnostic equipment and imaging device" (emrfinder.com)

**Interoperability & Data Exchange:**
- Greenway Exchange: hub-and-spoke interface platform for clinical and administrative data exchange with other healthcare organizations
- FHIR R4 API access (certified (g)(7), (g)(9), (g)(10))
- C-CDA document exchange for transitions of care ((b)(1), (b)(2), (b)(3))
- Direct messaging for care coordination
- Public health reporting capabilities ((f)(1) — immunization registries)

**Telehealth:**
- Greenway Telehealth integration for virtual visits, integrated with EHR workflows (greenwayhealth.com/solutions/telehealth)

**Analytics & Reporting:**
- Practice analytics and data insights
- Population health management tools
- Regulatory/quality measure reporting (MIPS, etc.)
- Value-based care analytics (greenwayhealth.com, AWS case study)
- Note: multiple user reviews describe the reporting/analytics capabilities as limited and inflexible (emrsystems.net reviews)

**Mobile Access:**
- PrimeMOBILE app for accessing EHR data on mobile devices (greenwayhealth.com press release)

### Data & Content

Based on the features and certified criteria described above, Prime Suite stores and manages the following types of data:

**Clinical data** (strongly evidenced by certified criteria and product descriptions):
- Patient demographics and registration information
- Problem lists, diagnoses (ICD-10), medical/surgical/family history
- Clinical encounter notes (4,000+ templates across 40+ specialties)
- Medication lists and prescription history (e-prescribing certified)
- Allergies and drug interaction data
- Lab orders and results (bi-directional lab interfaces)
- Diagnostic imaging orders and results (device integration described)
- Vital signs, clinical assessments
- Immunization records (certified for immunization registry reporting (f)(1))
- Care plans and clinical decision support alerts
- Scanned/attached documents (Document Manager)

**Administrative/financial data** (strongly evidenced by integrated PM/billing):
- Appointment schedules and scheduling data
- Insurance/payer information and eligibility
- Billing claims, charge capture, payment records
- Denial management records
- Multi-location practice configuration

**Patient engagement data** (evidenced by portal and Patient Connect):
- Patient portal messages (secure messaging)
- Patient-completed intake forms and health history
- Appointment requests
- Patient consent and authorization records

**Interoperability/exchange data** (evidenced by certified criteria):
- C-CDA clinical summaries (transitions of care)
- FHIR resources (USCDI data elements)
- Direct messages
- Public health submissions

**Areas of uncertainty:**
- The website does not clearly describe whether Prime Suite has a built-in fax management system or how inbound faxes are handled beyond the Document Manager
- Chronic care management (CCM) / care coordination workflows are mentioned on the Greenway website but it's unclear how deeply these are built into Prime Suite vs. being separate services
- The level of imaging data stored (PACS integration vs. just orders/results) is unclear — the product can interface with imaging devices but likely stores references/results rather than DICOM images directly
- Telehealth visit recordings/data — unclear whether video visit data is stored in Prime Suite or only in the separate Greenway Telehealth platform

---

# DocToMe, Inc. — Product Research

Researched: 2026-02-15
Developer website: https://www.ethizo.com

## Overview

DocToMe, Inc. is a very small, physician-founded EHR vendor based in Gig Harbor, Washington (near Tacoma). The company was founded around 2017 by Jawad Iqbal, MD, a hospitalist and infectious disease specialist at MultiCare Tacoma General Hospital. The product was originally called "CareCinch" (based on the Google Play package name `org.provider.carecinch`) before being rebranded to "ethizo." The company has approximately 5–9 employees and under $500K in annual revenue per Dun & Bradstreet data. There is no evidence of venture funding. Despite its tiny size, the company has achieved ONC 2015 Edition Cures Update certification across an unusually broad range of criteria and offers a surprisingly full-featured product suite. Ethizo targets ambulatory practices, FQHCs (Federally Qualified Health Centers), and PALTC (Post-Acute and Long-Term Care) settings across 20+ medical specialties. The company exhibited at the AAFP Family Medicine Experience (FMX) conference in 2023. It does not appear on any major EHR review platforms (G2, Capterra, Software Advice), and based on iOS App Store ratings (~60 provider ratings, ~32 patient ratings), the user base is likely in the dozens to low hundreds of providers.

## Product: ethizo EHR

CHPL ID: 10265 (15.05.05.3060.DOTM.01.00.1.200107)
Version: 2.0
Certification date: 2020-01-07

### What It Is

Ethizo EHR is a cloud-based, ONC-certified electronic health record and practice management platform. It is a full-stack product: the certified module encompasses the entire product, not a component of something larger. The system is hosted on HITRUST-certified infrastructure and is described as HIPAA compliant. The product is accessed via web portal (ehr.ethizo.com for providers, ipms.ethizo.com as an additional portal — possibly the practice management system) and companion mobile apps for providers and patients. There is also a separate telemedicine app called "Vezo."

The product is certified for a broad range of ONC criteria: all clinical criteria (a)(1)–(a)(14), transitions of care (b)(1)–(b)(5), clinical quality measures (c)(1)–(c)(4), patient portal (e)(1)–(e)(3), public health reporting (f)(1), (f)(2), (f)(7), FHIR API (g)(10), and direct messaging (h)(1). This breadth of certification is unusual for a company of this size.

### Users & Market

**Target users:** Physicians, clinical staff, and practice administrators at ambulatory clinics, FQHCs, and post-acute/long-term care facilities. The "About Us" page lists 20+ supported specialties including family medicine, internal medicine, pediatrics, cardiology, OB/GYN, pulmonology, gastroenterology, infectious diseases, behavioral medicine, psychiatry, geriatrics, wound care, palliative care, dentistry, podiatry, optometry, urology, nephrology, and urgent care.

**Customer base:** Very small. No customer counts are published. iOS App Store data suggests a limited user base: the provider app has ~60 ratings (3.5 stars, highly polarized) and the patient app has ~32 ratings (1.3 stars, overwhelmingly negative). No notable customer case studies or press releases were found.

**Multi-language support:** The provider app supports English, Arabic, French, and Spanish, which combined with the FQHC and PALTC focus may indicate deployment in multilingual or underserved care settings.

**PointClickCare integration:** Ethizo is listed on the PointClickCare Marketplace with a bi-directional interface, suggesting deployments where ethizo serves as the physician-side EHR communicating with PointClickCare at skilled nursing or long-term care facilities.

### Modules & Functionality

The vendor's products page (ethizo.com/products/) describes eight distinct modules:

1. **MU-3 Certified EHR** — Core clinical system including provider note documentation, clinical decision support, triage workflows, lab and radiology order management, referral management, inventory management, and scheduling with online appointment booking. Certified for CPOE (a)(1)–(a)(3), drug interaction checking (a)(4), demographics (a)(5), problem list (a)(6), medication list (a)(7), medication allergy list (a)(8), clinical decision support (a)(9 — though listed as a)(14)), implantable device list (a)(14), and other clinical data functions.

2. **Practice Management System (PMS)** — Full billing and revenue cycle management (per ethizo.com/practice-management-system/). Features include:
   - Rule-based claims scrubber with ~95% first-submission acceptance rate
   - Connectivity to multiple clearinghouses
   - Electronic Remittance Advice (ERA) posting
   - CPT macros for rapid charge entry
   - Real-time insurance eligibility verification
   - KPI dashboards (copay collection, A/R, denials, revenue)
   - Customized billing reports on revenue streams and aging cycles
   - Paper and electronic patient statement generation
   - PCI-compliant payment processing
   - Copay and outstanding balance collection integrated into demographic/billing screens

3. **Patient Portal** — Patient-facing app and web portal for appointment tracking/booking, health progress monitoring, medication tracking, secure messaging with providers, video call capability, Fitbit/device integration, smart trackers, and questionnaires.

4. **Vezo (Telemedicine)** — Separate single-click telemedicine platform with virtual rooms, waiting lists, team member participation, instant scheduling, integrated chat, and transit notes. Available as a standalone app.

5. **Hybrid eFax** — Document management merging fax, email, and e-signature. Includes signature verification, editing tools, patient document linking, and paperless workflow support.

6. **IVR (Interactive Voice Response)** — Automated phone system with intelligent call triaging based on patient rosters, call tracking, and voicemail handling. Marketed as eliminating the need for a physical call center.

7. **CCM (Chronic Care Management)** — Non-face-to-face care management for patients with multiple chronic conditions. Includes patient enrollment, care plan creation, automatic activity capturing, and automated billing generation for CCM services.

8. **RPM (Remote Patient Monitoring)** — Integrated with CCN Health's platform (ccnhealth.com/ethizo). Supports device-agnostic cellular-connected monitoring devices from manufacturers including Tenovi, Smart Meter, Dexcom CGM, Omron, Telli Health, Bodytrace, Trividia Health, and Jumper. Captures vitals (blood pressure, blood glucose, continuous glucose, pulse oximetry, weight, temperature, heart rate, ECG) via 4G LTE — no WiFi or Bluetooth required from patients.

**Additional capabilities:**
- **ePrescribing with PDMP** — e-prescriptions including controlled substances with Prescription Drug Monitoring Program integration
- **MIPS support** — Automated MIPS data collection, real-time performance dashboards (individual and group level), bi-weekly check-ins throughout program year (per ethizo.com/ethizo-mips/)
- **FHIR API** — API documentation at fhir-api.ethizo.com (page renders client-side only; content not directly accessible)
- **Direct messaging** — Certified for (h)(1) direct project
- **Public health reporting** — Certified for immunization registry (f)(1), syndromic surveillance (f)(2), and electronic case reporting (f)(7)
- **Lab integrations** — Bi-directional interface with major labs
- **State immunization registry** integration
- **Patient self-registration**

### Data & Content

Based on the vendor's described features, certified criteria, and integration partners, ethizo EHR manages the following data:

**Clinical data:**
- Patient demographics and insurance information
- Problems/diagnoses (problem list)
- Medications (medication list, ePrescriptions, PDMP data)
- Allergies (medication allergy list)
- Vital signs (both manually entered and from RPM devices)
- Lab orders and results (bi-directional lab interface)
- Radiology orders
- Immunizations (with state registry submission)
- Procedures
- Clinical notes/provider documentation
- Care plans (CCM module)
- Goals
- Implantable device data
- Clinical decision support alerts
- Clinical quality measure data (MIPS/CQM)

**Billing and financial data:**
- Insurance eligibility verification records
- Claims data with scrubbing results
- Electronic remittance advice (ERA)
- Copay and balance collection records
- Patient statements
- Revenue cycle KPIs and reports
- PCI-compliant payment transactions
- CPT/billing codes

**Communication and documents:**
- Secure patient-provider messages (patient portal)
- Fax documents (hybrid eFax)
- E-signatures
- Referral documents
- Transitions of care documents (C-CDA)
- Direct messages

**Telehealth data:**
- Telemedicine visit records (Vezo)
- Transit notes
- Video call records

**Remote patient monitoring data:**
- Blood pressure readings
- Blood glucose readings
- Continuous glucose monitor data
- Pulse oximetry (SpO2)
- Weight measurements
- Temperature readings
- Heart rate
- ECG data

**Scheduling and administrative data:**
- Appointments and scheduling data
- Patient self-registration data
- IVR call tracking and voicemail
- Inventory management records

**Public health reporting data:**
- Immunization registry submissions
- Syndromic surveillance data
- Electronic case reporting data

**Patient-generated data:**
- Fitbit/device integration data
- Questionnaire responses
- Smart tracker data

### Notable Observations

- **Mandatory disclosures page is down:** The ONC-required mandatory disclosures page at ethizo.com/onc-ehr-certified/ returns an HTTP 500 "Error establishing a database connection" error. This is a compliance issue.
- **Patient app quality:** The patient-facing app has a 1.3-star rating with 29/32 one-star reviews citing crashes, login failures, and unavailable medical records.
- **Provider app:** The provider app (3.5 stars, 60 ratings) is actively maintained — version 15.9.6 was recently released. Reviews are polarized: positive ones praise documentation efficiency ("Cut my documentation time by about 30–40%") while negative ones cite random shutdowns and unreliable microphone/AI features.
- **Possible rebrand:** The Google Play package name `org.provider.carecinch` suggests the product was originally called "CareCinch" before being rebranded to "ethizo."
- **Usability testing:** SLI Compliance conducted formal usability testing in October 2024 with 15 physicians and staff, yielding an SUS score of 86.53 (strong). Participants described the system as "user-friendly, straightforward."
- **Real World Testing:** The vendor publishes annual Real World Testing plans and results (2022–2025) at ethizo.com/real-world-testing/.

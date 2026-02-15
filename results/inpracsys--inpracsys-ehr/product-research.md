# InPracSys — Product Research

Researched: 2026-02-14
Developer website: https://www.inpracsys.com

## Overview

InPracSys (legal name: Innovative Practice Systems, Inc.) is a very small, niche EHR vendor headquartered at 2225 Lyndale Ave S, Minneapolis, MN 55405. Founded in 2003 by Dr. Ashu Kataria, the company has approximately 25 employees and an estimated annual revenue under $1 million (per Buzzfile). The product is built specifically for urology practices, with the tagline "built by urologists, with urologists in mind." Despite its small size, the product carries a broad ONC certification across 35 criteria.

Kataria also serves as CEO of RiskAssistMD (since 2018), a related company at the same address focused on reducing medical malpractice liability. The relationship between the two companies is unclear — RiskAssistMD may be a productization of InPracSys's Risk Management module. No funding history was found; the company is likely bootstrapped. InPracSys has essentially no market visibility: zero reviews on G2, Capterra, Software Advice, or KLAS, no press coverage, and only one identifiable customer from their own demo page.

## Product: InPracSys EHR

CHPL ID: 10194 (15.05.05.2762.INPS.01.00.1.191206)
Version: 9.0
Certification Date: 2019-12-06

### What It Is

InPracSys EHR is a cloud-based, full-featured EHR system designed primarily for urology practices. The certified module appears to be the whole product — there is no indication of a larger platform or separate certified components. It is accessed via web browser (any major browser), iPad, iPhone, and Android. The system uses a proprietary "Point and Click" single-page interface to minimize keyboarding, with a "FastCharting" feature that claims to allow documentation of a full renal stone consultation (HPI, ICD-10, orders, MU, PQRS, E/M codes) in under 30 seconds.

The system comes preloaded with urology-specific templates and forms. The Real World Testing documentation explicitly states: "Our application is specific to the practice of Urology." While the vendor website claims support for other specialties (Cardiology, Dermatology, Gastroenterology, OB-Gyn, Ophthalmology, Pulmonology), there is no evidence of actual deployment outside urology.

### Users & Market

**Target users:** Urologists, urology clinic staff, and their patients. The product targets small to mid-size urology practices.

**Known customer:** Comprehensive Urologic Care, S.C. in Lake Barrington, Illinois (with locations in Elgin and Hoffman Estates, IL) — identified through InPracSys's own demo page, which hosts a patient portal for this practice at `azcucptportal.inpracsys.com`.

**Customer base size:** Unknown, but almost certainly very small. The Real World Testing reports use a sample size of only 10 transactions per criterion, tested at a single "representative clinic." The RWT documents acknowledge that some certification criteria go unused by the testing clinic and must be tested in "InPracSys Lab" instead. This strongly suggests very limited deployment — possibly single-digit clinic customers.

**Market visibility:** No reviews on any major platform. No press coverage. No industry analyst mentions. No customer testimonials retrievable from the vendor's own site. The homepage mentions promoting attendance at the 2026 AUA Annual Meeting (Washington D.C., May 15–18, 2026), but no evidence of InPracSys as an exhibitor was found.

### Modules & Functionality

The following modules and features are described on the vendor website:

- **EHR / MyEMR (Core Charting):** Single-page interface with point-and-click documentation, urology-specific templates, mobile access, voice dictation via Siri/Cortana. Preloaded with urology-specific forms and clinical content.

- **FastCharting:** Rapid documentation tool — the vendor claims a full renal stone consult can be charted in under 30 seconds. This is the product's primary differentiator.

- **Care Pathways / PRACTICE iQ:** Stepped therapy programs aligned with national guidelines. Identifies qualifying patients for high-value drug programs, manages pre-authorization and billing. The vendor claims this generates $2,500–$7,500 per patient annually in additional revenue. This appears to be a significant revenue-generating feature for urology practices.

- **Risk Management:** Clinical decision support with automated alerts for urology-specific scenarios (e.g., stents placed but not removed, missed scrotal ultrasounds). Available as a standalone product for clinics using other EHRs. This module appears related to the separate RiskAssistMD company.

- **Billing:** Superbill generation, Level 1 coding, professional component anatomical pathology billing. The vendor claims a 99% clean claim rate. This appears to be billing/superbill generation within the EHR, not a full practice management/RCM system.

- **E-Prescribing:** Via SureScripts Rx HUB integration.

- **Patient Portal:** Patient-facing portal for medical records access, appointments, correspondence/messaging, and account management.

- **Data Mining / Analytics:** Custom reporting for clinical trial candidate identification and value-based payment outcome analysis.

- **Clinical Trials:** Automates patient identification for clinical trials and manages trial documentation.

- **Telemedicine:** Telehealth capabilities mentioned but details are sparse.

- **Meaningful Use / CQM Reporting:** Built-in attestation dashboard, automated CQM/PQRS reporting.

- **Integration:** Interfaces with labs, hospitals, SureScripts, and existing practice management systems. Claims to eliminate duplicate data entry. Technology partners include SureScripts, eProviderSolutions, DoseSpot (e-prescribing), and Dragon/Nuance (speech recognition).

- **FHIR API:** Patient/provider API access (security-restricted). API documentation is hosted at `ipsemrapi.inpracsys.com`.

### Data & Content

Based on certified criteria, vendor feature descriptions, and product pages, InPracSys EHR manages the following data:

**Clinical Data:**
- Patient demographics (certified (a)(5))
- Problem lists / diagnoses with ICD-10 coding (certified (a)(6))
- Medication lists and e-prescriptions via SureScripts (certified (a)(7), (a)(10))
- Medication allergy lists (certified (a)(8))
- Clinical notes and encounter documentation — HPI, ROS, exam, assessment/plan (per FastCharting feature descriptions)
- Urology-specific clinical data — the vendor explicitly mentions urine analysis, bladder scans, and TRUS (transrectal ultrasound) results in feature descriptions
- Lab orders and results (certified (a)(2), (a)(3))
- Diagnostic imaging orders/results (certified (a)(3))
- Vital signs (certified (a)(4))
- Smoking status (certified (a)(11))
- Family health history (certified (a)(12))
- Implantable device data (certified (a)(14))
- Clinical decision support rules and risk alerts (certified (a)(9); also the Risk Management module with urology-specific rules like stent tracking)

**Administrative/Financial Data:**
- E/M coding data (per FastCharting feature)
- Superbills and billing records (per Billing module description)
- Claims data (vendor cites 99% clean claim rate)
- Pre-authorization records (per Care Pathways/PRACTICE iQ module)
- Professional component anatomical pathology billing records

**Care Coordination Data:**
- C-CDA documents for transitions of care (certified (b)(1), (b)(2))
- Clinical information reconciliation data (certified (b)(2))
- Electronic referral records (certified (b)(3))
- Direct messaging (certified (h)(1))
- Care pathway / stepped therapy tracking and patient qualification records (per PRACTICE iQ module)

**Quality/Compliance Data:**
- Clinical quality measures (CQMs) (certified (c)(1))
- PQRS measures
- Meaningful Use attestation data

**Patient-Facing Data:**
- Patient portal records — view/download/transmit (certified (e)(1))
- Appointment scheduling records
- Patient-provider messaging/correspondence (per patient portal description)
- Patient account management data

**Public Health Data:**
- Syndromic surveillance data (certified (f)(2))
- Electronic case reporting data (certified (f)(5))

**Research Data:**
- Clinical trial candidate identification data (per Clinical Trials module)
- Data mining / analytics outputs (per Data Mining module)

**Notable gaps in information:** The website does not clearly describe whether the billing module is a full practice management system or just superbill/coding generation. The relationship between InPracSys billing and external practice management systems is unclear — the integration page mentions interfacing with "existing practice management systems," suggesting billing may be supplementary rather than comprehensive. It's also unclear whether the product stores scanned documents, images (e.g., cystoscopy images), or other unstructured content typical in urology workflows.

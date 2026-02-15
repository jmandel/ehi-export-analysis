# Royal Health, Inc. — Product Research

Researched: 2026-02-14
Developer website: https://royalsolutionsgroup.com/

## Overview

Royal Health, Inc. is a privately held healthcare technology company founded in 2008 by Peter Nassif, headquartered in White Plains, NY, with software operations in Nashville, TN. The company specializes exclusively in **radiology and diagnostic imaging** — it is not a general-purpose EHR vendor. Royal positions itself as "the Leader in Healthcare Consumer Engagement" and provides cloud-native software and services for radiology practices and imaging centers. The leadership team has over 180 years of collective experience spanning technology, radiology, financial services, management consulting, and billing services.

Royal's customer base consists of outpatient imaging centers and radiology practices. Notable customers include Radiology Ltd. (a division of US Radiology Specialists in Pima County, Arizona), Radiology Associates of Corpus Christi, Texas, Intermountain Medical Imaging, and most recently LucidHealth, a multi-state outpatient imaging center operator. The company appears to be a small-to-mid-size vendor focused on a well-defined niche within the radiology market. No public information on employee count or revenue was found; the company is not publicly traded. CBInsights lists the company but detailed financials were unavailable.

## Product: Royal Solutions (aka RoyalCare / Royal Enterprise Care)

CHPL ID: 10770

### What It Is

Royal Solutions v5 is the certified product name on CHPL, but the vendor markets the platform under multiple names: **RoyalCare™** (the core RIS platform), and **Royal Enterprise Care™** (the complete application stack). This is a **cloud-native Radiology Information System (RIS)** with integrated patient engagement, provider engagement, revenue cycle management, and clinical workflow modules — all in one platform. The company describes it as covering the full radiology lifecycle "from image ordered to cash in the bank."

The product is NOT a general-purpose EHR. It is purpose-built for radiology and diagnostic imaging workflows. However, it is certified under ONC criteria including (a)(1)–(a)(5), (a)(12), (a)(14), (b)(1)–(b)(2), (e)(1), (e)(3), (g)(7)–(g)(10), and (h)(1) — a broad set of clinical, interoperability, and patient access criteria. This means the product stores and manages clinical health data (demographics, problems, medications, allergies, clinical notes, implantable devices) in addition to its core radiology operational data.

The certified module appears to represent the full product — there's no evidence of separate product lines or platforms sharing this certification.

### Users & Market

The product is used by **outpatient radiology and diagnostic imaging centers**. End users include:

- **Radiologists and ordering physicians** (clinical workflow, reading, reporting)
- **Scheduling and front desk staff** (scheduling, registration, check-in)
- **Billing staff** (revenue cycle management, claims, collections)
- **Practice managers/administrators** (analytics, operational oversight)
- **Patients** (self-scheduling, pre-registration, portal for viewing images/reports, secure messaging, bill payment)
- **Referring providers** (order submission, status tracking, result viewing via RoyalMD portal)

Notable deployments:
- **Radiology Ltd. / US Radiology Specialists** (Pima County, AZ): Replaced seven separate systems with Royal Enterprise Care; described as completing "the care continuum in a single system" after a decade of incremental Royal implementations.
- **LucidHealth** (multi-state imaging centers, selected 2024): Deploying Royal as a single-vendor platform for "complex, large-scale sites" across multiple states, covering patient/physician engagement, scheduling, clinical workflows including mammography and lung tracking, billing, and analytics.
- **Radiology Associates** (Corpus Christi, TX): Deployed Royal patient portal and kiosk solution integrated with Merge RIS/IBM.
- **Intermountain Medical Imaging**: Launched Royal patient portal and online registration (2020).

### Modules & Functionality

Based on vendor materials, press releases, and customer case studies, the platform includes the following modules and capabilities:

**Core RIS / Clinical Workflow:**
- Order entry and management
- Exam scheduling (including all-exam-type self-scheduling with "scheduling algorithm")
- Patient registration (on-site, remote, mobile)
- Insurance authorization and verification
- Clinical workflow management for exam progression
- Mammography tracking
- Lung screening/tracking
- Exam protocol management ("right patient, right equipment, right protocol")
- Priors research automation
- Status tracking throughout exam progression
- Report and image distribution
- DICOM viewer / PACS viewer integration
- Screenshare capabilities for image review

**Patient Engagement (Royal Access / Royal Kiosks):**
- Self-scheduling
- Pre-registration (online, mobile)
- On-site kiosk check-in (tablet-based, with "express check-in" for pre-registered patients)
- Appointment confirmations, reminders, and notifications (Royal Alerts)
- Patient portal for viewing diagnostic reports and images
- Secure messaging between patients and staff
- Bill viewing and payment
- Patient education materials
- Cost estimates / out-of-pocket cost transparency
- Ability for patients to "lock" health records during security threats

**Provider Engagement (RoyalMD):**
- Provider portal for order submission and tracking
- Electronic order integration with existing EMR systems
- Print orders and fax OCR capabilities
- Real-time alerts and notifications
- Clinical decision support tools
- Status updates throughout exam progression for ordering providers

**Computerized Provider Order Entry (Royal Forms):**
- Electronic form submission with e-signature capture
- Multiple output formats (PDF, XML, HL7)
- Automated file delivery to internal network folders
- Referral order processing (MRI, X-ray, radiology)
- Patient screening assessments (e.g., lung cancer screening)
- Lab file and image attachments
- Multilingual support
- Historical record generation and reporting

**Revenue Cycle Management (RoyalPay / Royal Cash):**
- Insurance eligibility verification
- Prior authorization processing
- Cost estimation
- Time-of-service collections and payment processing
- Claims management
- Billing and collections
- Credit card processing (Chase Paymentech, PCI Level 1 compliant)
- Revenue analytics

**Coding Automation:**
- Automated coding workflows (mentioned on website, limited detail)

**Communication and Alerts (Royal Alerts):**
- Appointment notifications
- Prep information delivery
- Secure messaging
- Email and text notifications

**Reporting and Analytics:**
- Operational analytics suite
- Partnership with Quinsite for enhanced analytics (2025)
- Integration of clinical, financial, and operational data for insights

**Interoperability (Report Guard):**
- Encrypted report distribution
- Connectivity and interoperability services
- Direct Mail functionality
- Transitions of care (C-CDA)
- FHIR API (certified under g(7)–g(10))
- Implantable Device List (utilizing NLM API, per certifications page)
- View, Download, Transmit for patients (e)(1)
- Public health reporting (h)(1) — immunization registry

### Data & Content

Based on vendor materials, the following data types are stored and managed by the product:

**Clinical Data (evidenced by ONC certification criteria):**
- Patient demographics (a)(5)
- Problem list (a)(1) — conditions/diagnoses
- Medication list (a)(2) — active and historical medications
- Medication allergy list (a)(3)
- Clinical notes and clinical decision support data (a)(4)
- Family health history (a)(12)
- Implantable device list (a)(14)
- Transitions of care documents / C-CDA (b)(1), (b)(2)

**Radiology/Imaging Operational Data (evidenced by product features):**
- Imaging orders and referrals
- Exam scheduling data (appointments, protocols, equipment assignments)
- Patient registration and check-in data
- Clinical workflow status/tracking data
- Radiology reports
- Diagnostic images (DICOM, via PACS integration)
- Prior exam history
- Mammography tracking records
- Lung screening tracking records
- Patient screening questionnaires and assessments

**Financial/Revenue Cycle Data (evidenced by RoyalPay/billing features):**
- Insurance coverage and eligibility data
- Prior authorization records
- Cost estimates
- Payment records and transaction history
- Claims data
- Billing and collections records
- Credit card transaction data (PCI compliant)

**Patient Engagement Data (evidenced by portal/kiosk features):**
- Patient portal accounts and preferences
- Pre-registration forms and data
- Secure messages between patients and staff
- Appointment reminders/notifications history
- Patient-facing cost estimates
- Patient document uploads

**Provider Engagement Data (evidenced by RoyalMD features):**
- Referring provider information and preferences
- Electronic order submissions
- Provider portal access logs
- Fax/OCR captured documents
- Order status tracking

**Communication/Document Data:**
- HL7 messages
- C-CDA documents
- Encrypted reports (Report Guard)
- Faxed/scanned documents (OCR processed)
- E-signatures on forms
- PDF/XML document archives

**What's Less Clear:**
- The website doesn't describe detailed clinical charting or progress notes beyond what's implied by the certification criteria. It's unclear how robust the clinical documentation is versus being primarily a radiology workflow system that meets minimum certification requirements for clinical data.
- There's no mention of e-prescribing (the product is not certified for (a)(6)–(a)(11) prescribing criteria), which is consistent with a radiology-focused product.
- Lab result management is not prominently featured beyond imaging-specific results.
- The depth of the "clinical decision support" mentioned on the provider portal page is unclear — it may be limited to imaging-appropriate-use criteria rather than broad CDS.

---

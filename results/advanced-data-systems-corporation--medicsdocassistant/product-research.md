# Advanced Data Systems Corporation — Product Research

Researched: 2026-02-15
Developer website: https://www.adsc.com

## Overview

Advanced Data Systems Corporation (ADS) is a privately-held, independently-owned healthcare IT company founded in 1977 by David Barzillai in New York City. Originally created as a patient demographics database for radiology practices, the company has grown to over 300 employees operating from a 15,000 sq ft headquarters in Paramus, NJ, with additional offices in Plymouth Meeting PA, Laurel MD, and Naples FL. ADS has never been acquired, merged, or changed its name, and claims to have never discontinued a product. The company processes nearly 50 million EDI transactions annually and claims to serve "thousands of healthcare organizations" with 30,000–40,000+ providers. Medical Economics ranked ADS #21 among EHR vendors in 2013. All development, implementation, training, and support are handled in-house. Leadership includes founder David Barzillai (President), George Grodentzik (Partner EVP), and Sheryl Miller MBA (EVP Sales & Business Development).

ADS is a small-to-mid-size vendor in the ambulatory EHR market. Third-party estimates place their revenue somewhere between $17M and $46M (estimates vary widely). Enlyft data suggests roughly 0.02% healthcare IT market share, with customers skewing toward small and medium practices (70% under 1000 employees), overwhelmingly US-based (95%). The company serves over 28 clinical specialties with dedicated product configurations, with particular strength in behavioral health/addiction treatment, radiology, laboratory, and internal medicine.

## Product: MedicsDocAssistant

CHPL IDs: 10785 (version 8.0, certified 2022-01-11)

### What It Is

MedicsDocAssistant is ADS's legacy-generation ambulatory EHR, first beta-released in 1996 and in full production since 2000. The currently certified version is 8.0 (ONC 2015 Edition Cures Update, certified January 2022). It is broadly certified across 43 criteria spanning clinical data management (a)(1)-(a)(5), (a)(12), (a)(14)-(a)(15), transitions of care (b)(1)-(b)(3), clinical quality measures (c)(1)-(c)(3), patient access/portal (e)(1), (e)(3), public health reporting (f)(1)-(f)(2), (f)(4)-(f)(5), standardized APIs including FHIR (g)(2)-(g)(10), and Direct messaging (h)(1). The SED intended user description is "Internal Medicine and Other Specialities Providers and office staff."

MedicsDocAssistant is the EHR component of a larger product suite. It integrates tightly with **MedicsPremier** (practice management/billing), and is typically deployed alongside it as the "All-in-One Suite." ADS also separately certifies a newer-generation product, **MedicsCloud EHR v11.0** (CHPL ID 15.02.05.1044.AVDC.01.01.1.220111, 56 criteria), which appears to be the current go-forward platform. MedicsDocAssistant continues to be maintained and certified for existing customers. The two products share the same vendor, similar feature sets, and the same integration ecosystem, but are separately certified. The vendor's marketing pages now largely describe "MedicsCloud EHR" as the current product, with Capterra explicitly noting "MedicsCloud EHR (formerly MedicsDocAssistant EHR)."

Third-party e-prescribing is handled via **Newcrop** (for MedicsDocAssistant specifically; MedicsCloud uses Surescripts directly). Direct messaging uses **Surescripts N2N Direct Messaging**. The system also includes Meinberg NTP Daemon for time synchronization.

### Users & Market

MedicsDocAssistant targets ambulatory practices of all sizes, from solo providers to multi-site groups and enterprise health systems. The vendor claims over 28 specialties with dedicated configurations, including: internal medicine, family practice, behavioral health/addiction treatment, radiology, laboratory, cardiology, dermatology, ophthalmology, podiatry, orthopedics, neurology, psychiatry, OB/GYN, oncology, urology, pain management, gastroenterology, nephrology, pulmonology, ENT, general surgery, ambulatory surgery centers, genetics labs, infusion centers, infectious diseases, concierge medicine, physical therapy, and plastic surgery.

Named customers include Park Avenue Medical Professionals, Horizon Family Medical Group, Catholic Charities USA, Hispanic Counseling Center, New Bridge Medical Center, Podiatry Center of New Jersey, Health Management Corporation of America (HMCA — 25 radiology centers), University Diagnostic Medical Imaging, DON Recovery Services (addiction treatment), Transformations TMS Centers, and the Florida Bureau of Public Health Laboratories.

Day-to-day users include physicians, nurses, billing staff, and practice managers. The patient portal extends access to patients. The product is cloud-hosted on Equinix infrastructure, though historical versions were on-premise.

Reviews are mixed — Capterra shows 3.6/5 (11 reviews), SoftwareFinder shows 3.7/5 (23 reviews), while EMRSystems.net shows 5/5 (4 reviews, small sample). FindEMR shows 50% excellent / 45% good (32 reviews). Pricing is approximately $300/month per provider.

### Modules & Functionality

Based on vendor product pages (adsc.com/ehr-all-features, adsc.com/electronic-health-records-software, adsc.com/ehr-software-features) and third-party reviews:

**Clinical Documentation & Charting:**
- Encounter-based documentation model — physicians create clinical notes during encounters
- Specialty-specific customizable templates for 28+ specialties
- FlowText: voice-command data entry using Dragon Medical transcription, handwriting recognition, or keyboard; text automatically flows into corresponding patient record fields
- MedicsScribe AI: real-time conversational dictation/transcription with Pause & Continue, Micro Notes, Whisper X (described on vendor AI page; unclear if available in MedicsDocAssistant v8 specifically vs MedicsCloud only)
- Patient Timeline: chronological display of all items in a patient's record (praised by Capterra reviewers)
- Exit Plan: tracks impression/plan across encounters (praised by Capterra reviewers)
- Evidence-Based Medicine: "blue ribbon" indicators supporting clinical decisions

**CPOE (Computerized Provider Order Entry):**
- Medication orders transmitted electronically to pharmacies
- Lab and radiology test orders transmitted to labs/departments
- Procedure orders
- Clinical decision support: dosage suggestions, duplicate therapy warnings, drug-drug and drug-allergy interaction checking

**e-Prescribing (MedicsRx):**
- Electronic prescriptions to all connected pharmacies via Newcrop/Surescripts
- Controlled and non-controlled substances (in eligible states)
- Drug interaction and allergy alerts

**Lab Integration:**
- Automated lab orders with bidirectional results integration
- Results flow back into patient records

**Patient Portal (MedicsPortal):**
- Patient scheduling
- Online questionnaires/forms
- Secure messaging with practice
- Online payments
- View/download/transmit health records (per (e)(1) certification)

**Mobile Access:**
- Medics On-Call: provider access to patient data via iPhone/smartphone for hospital rounds or off-site use
- MedicsMobile: mobile app for patients/providers

**Public Health Reporting:**
- Immunization registry reporting (f)(1)
- Syndromic surveillance (f)(2)
- Cancer case reporting (f)(4)
- Electronic case reporting (f)(5)

**Clinical Quality Measures:**
- 25 CQMs covering depression screening, diabetes management, cancer screening, immunization tracking, medication documentation, hypertension, preventive screening
- MIPS reporting dashboard

**AI Features (described on vendor AI page — may be MedicsCloud-specific):**
- AI Rules Engine for billing/claims processing
- HCC Coding AI for risk adjustment
- Bill Code Analyzer
- AI Synopsis (real-time summaries of coding, prescriptions, diagnoses)
- AI Consult Letter Generator
- MedicsAI Fax: identifies patient demographics from incoming faxes, extracts referral types, lab reports, payer information, categorizes and routes documents

**Behavioral Health/Addiction-Specific (from adsc.com/behavioral-health-addiction-treatment):**
- ASAM-certified assessments flowing into patient timelines
- Auto-generated problem lists and treatment plans from assessments
- Support for outpatient psychiatry/therapy, MAT, IOP, PHP, inpatient residential, detox, group therapy
- Dual diagnosis program tracking
- Group therapy session documentation with attendance management
- Medics BedManager for facility operations

**Telemedicine & Remote Monitoring:**
- Built-in telemedicine/virtual care
- Remote patient monitoring with trend detection and automated alerts
- Kiosk functionality for patient check-in

**Interoperability:**
- HL7 and FHIR compliant (FHIR v4.0.1, US Core v3.1.1 per EHI export docs)
- CCDA generation and consumption
- Surescripts Direct messaging
- Medics Me app: patient-mediated health record exchange via OAuth 2

### Data & Content

Based on certified criteria, vendor feature descriptions, reviews, and press releases, MedicsDocAssistant stores or manages:

**Clinical Data (per certification criteria and feature pages):**
- Patient demographics including race, ethnicity, preferred language, sex, DOB, sexual orientation, gender identity (a)(5)
- Problem lists / diagnoses
- Medication lists and prescription history
- Allergy lists with drug-allergy interaction data
- Family health history (a)(12)
- Social, psychological, and behavioral data (a)(15) — including smoking status
- Implantable device lists (a)(14)
- Vital signs
- Lab orders and results (bidirectional integration)
- Diagnostic imaging orders
- Clinical encounter notes (template-based, voice-dictated, handwritten, or typed)
- Care plans (b)(9)
- Immunization records (with registry reporting)
- Clinical quality measure data (25 CQMs)

**Documents & Communications:**
- Transition of care documents — CCDA send and receive (b)(1), (b)(2)
- Patient portal messages (secure messaging)
- Incoming faxes (categorized and attached to patient records via AI Fax)
- Consult letters
- Referral documents

**Patient Portal Data:**
- Patient-submitted questionnaires/forms
- Appointment requests
- Payment records (portal payments)

**Public Health Data:**
- Syndromic surveillance data
- Cancer case reports
- Electronic case reports
- Immunization data for registry submission

**Audit & Security Data (per (d) criteria):**
- Authentication credentials with encryption
- Audit logs of all access/changes
- Amendment records
- Access control configurations

**What is NOT directly in MedicsDocAssistant but in the integrated suite:**

MedicsDocAssistant is the EHR component; billing, scheduling, and financial data live primarily in **MedicsPremier** (practice management), which is typically deployed alongside it. MedicsPremier manages:
- Appointment scheduling (multi-modality)
- Patient demographics (Master Patient Index)
- Insurance/payer information and eligibility
- Claims data (HCFA, UB, Workers' Comp, No-Fault formats)
- Payment/financial transactions
- Denial management records
- Inventory and sales tax tracking
- CRM/marketing campaign data
- Financial analytics and KPIs

The vendor markets these as a tightly integrated "All-in-One Suite" with shared data and no redundant data entry. For EHI export purposes under (b)(10), the question is whether MedicsDocAssistant's export includes data from MedicsPremier when deployed together, or only the EHR-side data. The EHI export documentation page (apps.medicscloud.com/B10_MedicsDocAssistant.html) describes exports in CCDA XML and FHIR v4.0.1 formats — neither of which naturally carries billing claims data, suggesting PM data may not be included.

**Radiology-specific data** (for practices using MedicsRIS alongside): radiology reports, imaging orders, mammography tracking, biopsy results, PACS-linked images. MedicsRIS is a separate product.

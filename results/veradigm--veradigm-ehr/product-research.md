# Veradigm — Product Research

Researched: 2026-02-16
Developer website: https://www.veradigm.com/

## Overview

Veradigm Inc. is the successor entity to Allscripts Healthcare Solutions, a major health IT company founded in the 1980s in Chicago. In May 2022, Allscripts sold its hospital and large physician practice business (Sunrise, Paragon, TouchWorks, dbMotion) to Harris Computer / Constellation Software for ~$700M; that segment became **Altera Digital Health**. The remaining ambulatory EHR, practice management, patient engagement, and data analytics businesses were formally rebranded as **Veradigm** in January 2023.

Veradigm has ~2,450 employees and generates approximately $585M in annual revenue across two segments: Provider (~77% of revenue, covering EHR, practice management, patient engagement, and revenue cycle management) and Payer & Life Sciences (~23%, covering data analytics and real-world evidence). The company claims over 180,000 physician users. It holds approximately 3.6% of the U.S. ambulatory EHR market — significant in the small-to-mid-size independent practice segment, though small relative to Epic (~44%).

Veradigm has been in financial turmoil since March 2023 when it disclosed a ~$20M revenue overstatement (2021-2022), triggering an SEC investigation, executive departures, and Nasdaq delisting in February 2024. Shares now trade OTC under ticker MDRX. The company continues operating and plans to relist after completing financial restatements, targeted for 2026. Despite the turmoil, Veradigm acquired Koha Health (RCM, orthopedic focus) in early 2024 and ScienceIO (AI data platform) for $140M.

Notably, Veradigm also owns **Practice Fusion** (a separate, simpler cloud-native EHR for small practices) and **FollowMyHealth** (a patient engagement platform). These are distinct ONC-certified products. This report focuses on **Veradigm EHR**, the flagship ambulatory EHR product.

## Product: Veradigm EHR

CHPL ID: 11763

### What It Is

Veradigm EHR is the direct successor to **Allscripts Professional EHR** (also known as "Allscripts Pro"), which itself descended from the "HealthMatics" EHR. It is a full-featured ambulatory EHR targeting small-to-mid-size independent physician practices and multi-location, multi-specialty organizations. It is **not** the same product as Allscripts TouchWorks (which went to Altera Digital Health and serves larger enterprises).

The certified product (Veradigm EHR version 26) has an extensive ONC certification profile with 40+ criteria spanning clinical data management (a)(1)-(a)(15), care coordination (b)(1)-(b)(11), clinical quality measures (c)(1)-(c)(3), patient access (e)(1), public health reporting (f)(1)-(f)(7), FHIR APIs (g)(7)-(g)(10), and Direct messaging (h)(1). This breadth indicates a comprehensive clinical system.

Veradigm EHR is the clinical core, but the full product ecosystem includes **Veradigm Practice Management** (billing/scheduling — separate but integrated product), **FollowMyHealth** (patient portal — EHR-agnostic, separately certified), **Veradigm ePrescribe** (also available standalone), and the **DORN** diagnostic ordering/results network. The certified EHR module is a component of this broader platform.

### Users & Market

**Target users:** Physicians, clinical staff, nurses, and practice administrators in ambulatory settings. The product supports solo practices through multi-site groups with 50+ providers.

**Specialties:** Veradigm claims support for "nearly every medical specialty" with preloaded templates and protocols. Explicitly listed specialties include: cardiology, orthopedics, neurology, dermatology, gastroenterology, endocrinology, ENT, urology, family practice, internal medicine, pediatrics, OB/GYN, psychiatry, urgent care, oncology, pulmonology, rheumatology, allergy/immunology, occupational medicine, podiatry, physical therapy, and more.

**Market position:** ~3.6% ambulatory market share. Ranked #1 by Black Book Research (2025) for ambulatory EHR in family practice and primary care. Over 180,000 physician users across the full Veradigm platform (not all on Veradigm EHR specifically — some use Practice Fusion).

**Deployment:** Cloud-based (primary), on-premise, or hybrid. Available via web browser with iOS/Android mobile apps.

**User reviews:** 3.5/5 on Capterra (66 reviews). Users praise customizability, specialty-specific templates, and lab/pharmacy integration. Common complaints include steep learning curve, slow performance (chart loading times), and variable customer support quality.

### Modules & Functionality

Based on vendor website, product pages, third-party reviews, and ONC certification criteria:

**Clinical Documentation & Charting**
- One-click visit templates that auto-populate from prior visits
- Smart Lists that learn provider ordering habits per diagnosis
- **Ambient Scribe** (launched November 2024): AI-powered documentation that captures patient conversations and generates structured clinical notes directly in the EHR, with multilingual support
- Voice recognition for documentation
- Care plan creation and patient goal tracking
- Structured diagnosis coding with HCC (Hierarchical Condition Category) alerts and RAF/risk score viewing for value-based care

**ePrescribing** (also available as standalone product, Veradigm ePrescribe)
- Integrated electronic prescribing with allergy/drug interaction checking
- EPCS (Electronic Prescribing of Controlled Substances)
- PDMP (Prescription Drug Monitoring Program) integration for state registries
- **RxTruePrice**: Real-time patient-specific medication pricing showing discounted plan/PBM prices, cash prices, therapeutic alternatives, and pharmacy price comparison
- **eAUTH**: Electronic prior authorization automation
- Patient financial assistance and coupon information at point of care
- Serves 80,000+ prescribers

**Lab & Imaging Integration (DORN)**
- **Veradigm DORN** (Diagnostic Ordering and Results Network): Cloud-based hub connecting to 500+ lab and radiology centers via a single API
- Electronic ordering from within EHR workflows
- Near real-time order status visibility
- Results delivered directly to the EHR
- Rapid lab integration (typically within 24 hours)

**Clinical Decision Support**
- HCC alerts for chronic condition documentation
- Clinical Decision Insights suggesting symptoms and care plans based on practice protocols
- AI-driven diagnosis code recommendations

**Telehealth**
- Integrated video visits with EHR documentation
- Asynchronous "email visits" (questionnaire-based consultations)

**Reporting & Compliance**
- Automated reporting for PQRS, PCMH, and FQHC requirements
- ICD-10 and CPT coding support
- Clinical quality measure reporting (certified for CQMs)
- Public health reporting: immunization registries, electronic case reporting, syndromic surveillance, cancer registry, antimicrobial use/resistance

**Transitions of Care & Interoperability**
- C-CDA document creation and consumption for care transitions
- Direct messaging (h)(1) for secure health information exchange
- FHIR R4 API access (g)(10)
- HL7 interoperability
- **Unity APIs** for third-party integration
- **App Expo Marketplace** for certified third-party applications
- Open developer portal (developer.veradigm.com)

**Mobile**
- Veradigm EHR Mobile (iOS/Android): schedule access, messaging, prescription refill management

**Practice Management** (separate product: Veradigm Practice Management)
- **Scheduling**: AI-powered "Predictive Scheduler" using 40+ metrics; handles walk-ins, cancellations, recurring appointments
- **Claims processing**: 98% first-pass clean claims rate; Claim Verification for revenue leakage prevention
- **System Rule Manager**: Real-time coding error detection and correction
- **Office Manager**: Customizable front-office and back-office workflow queues
- **Address Verification**: Patient contact validation via Melissa Data
- **Revenue Cycle Management**: Central monitoring of denial rates, A/R days, scheduling metrics across sites
- Available as software or end-to-end managed billing services
- Capterra rating: 2.9/5 (139 reviews) — lower than the EHR itself
- Veradigm also acquired **Koha Health** (January 2024) for orthopedic/MSK-focused RCM

**Patient Portal** (separate product: FollowMyHealth)
- EHR-agnostic, mobile-first patient engagement platform (also ONC-certified separately)
- Personal Health Record: medical history, prescription renewals, lab results, test images
- Secure messaging with providers
- Online appointment scheduling with confirmations, reminders, and waitlist management
- Mobile check-in with payment options
- Online bill pay
- Remote patient monitoring (device integration)
- Caregiver proxy access
- Post-visit satisfaction surveys
- Medical interpretation via Voyce partnership (240+ languages plus ASL)
- Patient-generated discrete data flows back to the EHR

### Data & Content

Based on the product's ONC certification profile and documented features, Veradigm EHR stores and manages the following data categories:

**Clinical data directly evidenced by (a) criteria certification:**
- Patient demographics (a)(5)
- Problem lists with SNOMED CT coding (a)(1)-(a)(3)
- Medication lists and medication allergy lists (a)(1)-(a)(3)
- Clinical notes and encounter documentation (a)(4), (a)(14)
- Vital signs and growth charts (a)(2)
- Lab orders and results (via DORN integration)
- Imaging orders and results (via DORN)
- Implantable device data (a)(14) — UDI
- Social determinants / social history
- Immunization records (f)(1)
- Smoking status
- Family history
- Assessment and plan of treatment
- Care plans and patient goals
- Health concerns

**Prescribing data evidenced by ePrescribe features and (b)(3) certification:**
- Prescription orders (active, historical, and discontinued)
- Controlled substance prescriptions (EPCS)
- Drug interaction and allergy alert history
- Prior authorization records (eAUTH)
- Medication pricing information (RxTruePrice)

**Administrative data evidenced by Practice Management (separate product but integrated):**
- Scheduling data (appointments, cancellations, recalls)
- Insurance and coverage information
- Claims and billing data (CPT, ICD-10 codes)
- Payment records
- A/R and denial tracking
- Practice/provider configuration

**Patient engagement data evidenced by FollowMyHealth (separate product):**
- Secure messages between patient and provider
- Patient-submitted health data (questionnaires, device data)
- Portal access and activity logs
- Online bill payments
- Appointment requests

**Reporting and exchange data evidenced by (b), (c), (f) criteria:**
- C-CDA documents (sent and received)
- CQM data and submissions
- Public health reports (immunization, syndromic surveillance, cancer registry, electronic case reporting, antimicrobial use/resistance)
- Audit logs (d)(2)

**Important note on product boundaries:** Practice Management and FollowMyHealth are separately sold products that integrate with Veradigm EHR. The ONC (b)(10) EHI export requirement applies to "all electronic health information that can be stored at the time of certification by the product, of which the Health IT Module is a part." The scope of what constitutes "the product" vs. separate products is a key question for evaluating export completeness. The CHPL listing is specifically for "Veradigm EHR" — but in practice, many customers run the EHR + PM + FollowMyHealth as an integrated suite.

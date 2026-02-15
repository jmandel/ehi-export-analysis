# Theoria Medical, PLLC — Product Research

Researched: 2026-02-15
Developer website: https://theoriamedical.com/

## Overview

Theoria Medical is a tech-enabled medical group and technology company founded in 2019, headquartered in Novi, Michigan. The company provides primary care physician services to senior living communities — including skilled nursing facilities (SNFs), assisted living facilities, continuing care retirement communities, and independent living communities — across 21 states. Theoria is not a traditional EHR vendor selling software to outside customers; rather, it is a physician group practice that built its own proprietary EHR (ChartEasy) for internal use by its own clinicians. The company employs physicians, nurse practitioners, and physician assistants who provide on-site rounding, telemedicine, medical directorship, chronic care management (CCM), and remote patient monitoring (RPM) at partner facilities.

Theoria operates as a value-based care organization, having joined the ACO REACH (High Needs) program through a partnership with Empassion Health in January 2024. In December 2024, Amulet Capital Partners invested in Theoria Management (the management services organization arm). The company has grown rapidly — employee estimates range from ~200 to 1,000+ depending on the source and timing, reflecting significant recent expansion. Theoria serves "hundreds" of senior living and care residential locations across 21 states, per press coverage. CEO Kevin Murphy leads the organization.

Critically, ChartEasy is purpose-built for Theoria's own clinicians — it is not sold as a commercial EHR product to external healthcare organizations. The facilities where Theoria physicians provide care typically use their own facility EHR systems (PointClickCare, MatrixCare, American HealthTech), and ChartEasy integrates bidirectionally with those systems.

## Product: ChartEasy

CHPL IDs: 11542

### What It Is

ChartEasy is an ONC-certified, cloud-based electronic health record developed by Theoria Medical specifically for the long-term care (LTC) and post-acute care settings. It is a physician-facing EHR — used by Theoria's own physicians, nurse practitioners, and physician assistants who provide care in SNFs and other senior living communities. The product is supported on web and iOS platforms.

ChartEasy is the certified Health IT Module, but it exists within a broader ecosystem of Theoria proprietary technology tools:
- **ChartEasy** — the EHR for clinical documentation, orders, medication management
- **ChatEasy** — secure clinical messaging platform for communication between LTC facility care teams and Theoria's medical staff
- **ProphEasy** — AI/ML clinical decision support tool for predicting return-to-hospitalization (RTH) risk
- **Theoria Telemedicine** — virtual care delivery platform
- **Remote Patient Monitoring (RPM)** — continuous vital sign monitoring with devices and automated alerts

The certified module (ChartEasy v1.5) has a broad certification profile with 34 criteria and 10 Clinical Quality Measures. The SED intended user description is "Ambulatory/Post-Acute."

### Users & Market

**Primary users**: Theoria Medical's own clinicians — physicians, nurse practitioners, and physician assistants — who provide attending physician services, medical directorship, and telemedicine at partner senior living facilities.

**Clinical settings**: Skilled nursing facilities, assisted living, continuing care retirement communities, independent living, and home health. The patient population is primarily elderly, high-acuity, Medicare-eligible residents in institutional settings.

**Scale**: Theoria serves "hundreds" of senior living locations across 21 states. The company has been growing rapidly.

**Key distinction**: ChartEasy is an internal-use EHR. It is not sold to external customers. The facilities where Theoria's clinicians work have their own EHR systems (typically PointClickCare or MatrixCare); ChartEasy serves as the physician's EHR that integrates with the facility's system.

### Modules & Functionality

Based on vendor website, product pages, partner marketplace listings, and App Store descriptions:

**Clinical Documentation**
- Physician progress notes and encounter documentation for SNF visits
- Notes are delivered instantaneously to facility EHR (e.g., MatrixCare, PointClickCare) upon signature
- Signed encounters viewable in patient portal (per App Store listing, added v2.0.4)

**Medication Management**
- Automated medication reconciliation algorithm
- Support for polypharmacy management and gradual dose reduction (GDR) — both specific to the SNF regulatory environment
- Current medication lists accessible via patient portal
- The system is certified for (a)(1) CPOE and (a)(4) drug-drug/drug-allergy interaction checks, and (a)(14) implantable device list, indicating it handles ordering workflows

**Scheduling**
- Automated patient scheduling algorithm that adheres to regulatory guidelines (likely CMS-required physician visit frequencies for SNF residents)

**Lab & Imaging**
- Integration with laboratory and imaging companies
- Real-time access to lab results (confirmed on patient portal and product page)
- Lab data exchange is bidirectional

**Clinical Decision Support**
- ProphEasy AI tool for return-to-hospitalization prediction
- Diagnosis-specific vital range alerts
- The system is certified for (a)(5) clinical decision support

**Remote Patient Monitoring**
- Two device options for facilities
- Monitors: heart rate, respiration rate, motion, presence, blood oxygen saturation
- Real-time vitals pushed to ChartEasy and facility EHR
- Abnormality alerts triggered via diagnosis-specific vital ranges
- Alerts delivered through ChartEasy and ChatEasy messaging

**Chronic Care Management (CCM)**
- Individualized care plans accessible via patient portal
- CCM module for managing chronic conditions in the SNF population

**Secure Messaging (ChatEasy)**
- Multi-channel instant messaging between medical staff and facility care teams
- Nursing receives alerts with abnormal vitals via ChatEasy
- Real-time communication for care coordination

**Telemedicine**
- Virtual care delivery infrastructure (Theoria Telemedicine platform)
- Supports remote clinical encounters

**Patient Portal**
- ChartEasy Patient Portal (web and iOS app)
- View lab results and vital signs
- View current medications
- View signed clinical encounters
- Access CCM care plans
- Download and transmit health records (PDF and CCDA formats)
- Share health information with authorized representatives and other providers

**Interoperability & Integrations**
- Bidirectional integration with PointClickCare (demographics, ADT, medications, vitals, diagnoses flow in; physician notes flow out)
- Bidirectional integration with MatrixCare (same pattern)
- Integration with American HealthTech
- Hospital EMR system integrations
- Laboratory and imaging company integrations
- Certified for (b)(1) transitions of care, (b)(2) clinical information reconciliation
- Certified for (g)(7)-(g)(10) FHIR/API access
- Certified for (e)(1) view/download/transmit, (e)(3) patient health information export
- Certified for (h)(1) direct project messaging

**Regulatory Compliance**
- Designed to align with LTC regulatory requirements (CMS conditions of participation, MDS-related workflows)
- Clinical Quality Measures (10 CQMs certified)

**Supported Terminologies** (per Medigy listing)
- ICD-9, ICD-10, SNOMED CT, LOINC, NDC, RxNorm, CPT, HCPCS, RadLex, MEDCIN

### Data & Content

Based on the evidence gathered, ChartEasy stores or manages the following types of data:

**Clinical data confirmed by product documentation:**
- Patient demographics (received from facility EHR integrations)
- ADT (admission/discharge/transfer) records (from facility integrations)
- Physician progress notes and encounter documentation
- Medication lists and reconciliation data
- Vital signs (both manual and from RPM devices)
- Lab results (from laboratory integrations)
- Diagnoses (received from facility EHR, also managed internally)
- Implantable device information (implied by (a)(14) certification)
- Clinical decision support alerts and risk predictions (ProphEasy RTH scores)
- Care plans (CCM care plans, accessible via portal)
- Scheduling data (visit scheduling per regulatory requirements)
- Patient portal access logs and patient-generated data

**Clinical messaging data:**
- ChatEasy secure messages between Theoria clinicians and facility nursing staff
- Alert notifications for abnormal vitals

**RPM device data:**
- Heart rate, respiration rate, motion, presence, blood oxygen saturation readings
- Continuous monitoring streams from RPM devices

**What is unclear or not mentioned:**
- **Billing/claims**: The website does not explicitly describe billing or claims management functionality within ChartEasy. However, CPT and HCPCS terminologies are listed as supported, and Theoria operates as a physician group that bills Medicare (fee-for-service and value-based). It is unclear whether billing is handled within ChartEasy or through a separate billing system.
- **E-prescribing**: Despite medication management being a core feature, explicit e-prescribing (Surescripts integration) is not mentioned on the website. However, (a)(1) CPOE certification and RxNorm/NDC terminology support suggest prescribing workflows exist.
- **Imaging results**: Integration with "imaging companies" is mentioned but details are sparse.
- **Referral management**: Not described.
- **Quality reporting/MDS data**: While regulatory compliance is emphasized and CQMs are certified, explicit MDS (Minimum Data Set) data management is not described — MDS is typically the facility's responsibility, not the attending physician's.
- **Historical claims data**: Theoria references having "historical claims data" for ACO REACH analytics, but it's unclear if this is stored in ChartEasy or a separate analytics platform.

---

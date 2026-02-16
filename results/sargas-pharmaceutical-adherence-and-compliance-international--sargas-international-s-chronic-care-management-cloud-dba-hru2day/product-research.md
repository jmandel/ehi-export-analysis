# Sargas Pharmaceutical Adherence and Compliance International — Product Research

Researched: 2026-02-15
Developer website: http://www.spacinternational.com

## Overview

Sargas Pharmaceutical Adherence and Compliance (SPAC) International is a small, privately held digital health company based in Bakersfield, CA, founded by Gitesh (Git) Patel. The company originally focused on helping cancer patients maintain medication adherence despite side effects, then expanded into chronic care management when CMS approved CCM reimbursement (CPT 99490 etc.) in 2015. SPAC International also operates under the brand "hru2day" (as in "how are you today").

The company is a niche vendor focused exclusively on chronic care management, remote patient monitoring, and medication therapy monitoring — it is **not** a full EHR. It serves physician practices, hospitals, health plans, ACOs, FQHCs, and home health agencies, primarily for Medicare patients with chronic conditions. According to the hru2day website, the platform serves 20,000+ patients across 200+ practices with 200,000+ recorded interactions. The company operates a 24/7 clinical call center staffed by trained professionals who provide care coordination on behalf of contracting physician practices. The business model involves contracting with physician practices and sharing Medicare CCM/PCM/RPM reimbursement revenue.

The company engaged PYA (an advisory firm) to verify compliance with Medicare billing rules for relevant CPT codes. It has no apparent acquisition history, parent company, or rebranding beyond the addition of the "hru2day" consumer-facing brand.

## Product: Sargas International's Chronic Care Management Cloud dba hru2day

CHPL ID: 10702

### What It Is

The Chronic Care Management Cloud (branded hru2day) is a cloud-based platform for managing chronic care patients, primarily under Medicare CCM, PCM (Principal Care Management), and RPM (Remote Patient Monitoring) programs. It achieved ONC HIT Modular EHR certification (version 21.9, certified October 14, 2021) — notably as a **modular** certification, not a complete EHR. The product was previously certified under the 2014 Edition as well (version 14.1).

The certified criteria are relatively focused:
- **(a)(1)–(a)(3), (a)(5)**: CPOE for medications, labs, diagnostic imaging; demographics; problem list
- **(b)(10)**: EHI export
- **(d) criteria**: Security, authentication, audit logging
- **(e)(2)**: Clinical information reconciliation (not patient portal VDT)
- **(g)(10)**: Standardized FHIR API
- **(g)(3)–(g)(5)**: Safety-enhanced design, quality management, accessibility

Notably absent from certification: e-prescribing, transitions of care (b)(1)–(b)(3), patient portal view/download/transmit (e)(1), and all public health reporting (f) criteria. This aligns with the product being a care management platform rather than a point-of-care clinical EHR.

### Users & Market

**Primary users**: Care coordinators and clinical staff at the 24/7 call center, physician practice staff, and physicians who review care plans and patient data. Patients interact through mobile apps and a patient portal.

**Clinical settings**: Ambulatory physician practices (often small to mid-size), ACOs, FQHCs, home health agencies, and hospitals — all serving Medicare populations with chronic conditions.

**Scale**: 200+ practices, 20,000+ patients, 200,000+ interactions (per the hru2day website). This is a small vendor by any measure.

**Go-to-market**: The company contracts directly with physician practices. SPAC's call center staff perform the actual CCM services (phone calls, care plan updates, medication monitoring) on behalf of the practice, and the practice bills Medicare. This is a managed-service model — SPAC is both the technology vendor and the care management service provider.

### Modules & Functionality

The platform consists of several interconnected components described across vendor materials:

**Physician Portal**: Allows physicians to review patient care plans, medication lists, health data, and care coordination activity performed by the call center staff. Provides a centralized view of patient information.

**Patient Portal / Mobile App**: Gives patients access to their care team, secure messaging, medication reminders, and the ability to report symptoms and side effects. The Drug Adherence® mobile app provides medication reminders and side effect reporting.

**Pharmacy Portal**: Enables real-time health information exchange with pharmacies. Details on specific pharmacy functionality are limited.

**Chronic Care Management (CCM)**: Core module supporting CMS CCM requirements — creation and maintenance of patient-centered care plans addressing physical, mental, cognitive, psychosocial, functional, and environmental needs. Includes structured recording of demographics, problems, medications, and allergies. Supports at least 20 minutes/month of care management per patient.

**Remote Patient Monitoring (RPM)**: Captures physiological data from FDA-approved home monitoring devices (glucose monitors, blood pressure cuffs, pulse oximeters, weight scales, heart rate monitors). Data is transmitted in real-time to the care team.

**Medication Therapy Monitoring (MTM) / Drug Adherence**: Tracks medication adherence, provides reminders, monitors for side effects, and checks for drug interactions. Originally developed for oncology medication adherence — this was the company's founding use case.

**Principal Care Management (PCM)**: Extended care management for high-risk patients requiring 30+ minutes of monthly care coordination.

**Care Transitions Management**: Coordination for patients transitioning between settings — includes emergency department follow-up and hospital discharge coordination.

**24/7 Clinical Call Center**: While not a software module per se, this is integral to how the platform operates. Trained clinical staff provide the care management services, logging all interactions in the system.

**AI/ML capabilities**: The vendor claims to use artificial intelligence and machine learning for identifying health risks and enabling preventive interventions, though specific details are not provided.

### Data & Content

Based on vendor materials, the platform manages the following data:

**Clinical data explicitly described**:
- Patient demographics
- Problem lists (chronic conditions)
- Medication lists and medication allergies
- Care plans (comprehensive, addressing physical, mental, cognitive, psychosocial, functional, and environmental domains)
- Physiological monitoring data: glucose, blood pressure, heart rate, oxygen saturation, weight (from RPM devices)
- Medication adherence records and side effect reports
- Clinical summaries

**Interaction and workflow data**:
- Care coordination logs (documenting the 20+ minutes/month of CCM services)
- Call center interaction records (200,000+ interactions logged)
- Secure messages between patients, care teams, and providers
- Referral and care transition records
- Patient consent records (required for CCM billing)

**Billing-relevant data**:
- Time tracking for CCM/PCM/RPM services (linked to CPT codes 99439, 99437, 99487, 99489, 99490, 99491 for CCM; 99424-99427 for PCM)
- Service documentation supporting Medicare reimbursement

**What's unclear or likely absent**:
- The website does not describe clinical notes/encounter documentation in the traditional EHR sense (progress notes, H&P, etc.)
- No mention of lab result storage (though CPOE for labs is certified, suggesting orders can be placed)
- No mention of diagnostic imaging results
- No mention of immunization records
- No mention of scheduling/appointment management
- No mention of billing/claims processing beyond CCM/PCM/RPM time tracking — the actual Medicare billing appears to be done by the physician practice, not through this system
- No mention of document management or scanned records

The product's data footprint is specialized: it's deep on care plans, medication monitoring, physiological data from RPM devices, and care coordination activity logs, but narrow compared to a full EHR. It does not appear to be the primary clinical documentation system for any practice — rather, it supplements the practice's existing EHR with CCM/RPM/MTM-specific capabilities.

---

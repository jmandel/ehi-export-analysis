# agilon health inc. — Product Research

Researched: 2026-02-15
Developer website: https://www.agilonhealth.com/

## Overview

agilon health, inc. (NYSE: AGL) is a publicly traded healthcare company headquartered in Westerville, Ohio, founded in 2016. agilon's core business is **value-based care enablement for primary care physicians serving Medicare seniors** — it is *not* primarily an EHR or health IT vendor. The company partners with independent primary care and multispecialty practices, providing a platform that combines "people, process, and technology" to manage the total healthcare needs of senior patients under a per-member-per-month model. As of 2024, agilon's physician network includes over 3,000 primary care physicians serving more than 700,000 senior patients across 30+ communities.

In **March 2023, agilon acquired mphrX for $45 million**. mphrX was a health IT company that built the **Minerva Healthcare Data Platform**, a FHIR-native data aggregation and patient engagement platform. Minerva is the certified product under this CHPL listing. It is important to note that Minerva is **not a traditional EHR** — it is a healthcare data interoperability platform with patient engagement capabilities. It aggregates data *from* EHRs and other clinical systems rather than being a system of record for clinical documentation.

The mphrx.com website appears to be offline as of this research date, though cached search results provide substantial detail about the platform.

## Product: Minerva

CHPL ID: 10649

### What It Is

Minerva is a **Healthcare Data Platform-as-a-Service**, built natively on FHIR, designed to help organizations unify patient data from disparate systems, make it accessible, generate insights, and support value-based care delivery. The certified criteria are limited — primarily `(b)(10)` for EHI export, `(e)(1)`/`(e)(3)` for patient access/portal, and `(g)(1)`/`(g)(7)`/`(g)(9)`/`(g)(10)` for API/FHIR access. Notably absent are all clinical criteria `(a)(1)`–`(a)(14)` and transitions-of-care criteria `(b)(1)`–`(b)(3)`, which is consistent with Minerva being a data aggregation/interoperability platform rather than a source-of-truth clinical system.

Per the ONC mandatory disclosures page, Minerva V4 has two main functional areas:
1. **Interoperability Platform**: "The Minerva platform provides ability to integrate and aggregate data from disparate healthcare IT systems to create a unified FHIR-based patient record."
2. **Patient Engagement**: "The Minerva platform provides web and mobile applications for patients and their family members to access their data, book appointments, securely message their health systems and share information."

### Users & Market

**Pre-acquisition (mphrX era):** Minerva was deployed at health systems globally across 20+ countries, managing 460+ million patient records, with 52+ million active patient accounts, 16+ million appointments booked via patient apps, and 350,000+ clinical users (per Frost & Sullivan / PR Newswire, 2020). Notable deployment included a partnership with Mount Sinai Health System (2022) for real-time clinical data sharing. mphrX won the 2020 Frost & Sullivan Global Enabling Technology Leadership Award for Minerva.

**Post-acquisition (agilon era):** Minerva was integrated into agilon's enterprise technology platform to enable faster onboarding of physician partners and rapid integration of clinical data across agilon's value-based care network. The primary users in the agilon context are the 3,000+ primary care physicians and their practice staff in agilon's partner network, plus their senior patients.

The target clinical settings include large health systems (Mount Sinai), surgical practices, and in the agilon context, independent primary care and multispecialty practices focused on Medicare populations.

### Modules & Functionality

Based on vendor materials, the Frost & Sullivan award write-up, Azure Marketplace listing, and cached mphrx.com content, Minerva includes the following modules and capabilities:

**Data Aggregation & Integration**
- Ready-to-use data connectors to ingest data from disparate clinical and claims sources (EMRs, HIS, PACS, healthcare management software)
- Supports real-time streaming and batch ingestion
- Data normalization and transformation to FHIR resources
- Stores longitudinal health records as native FHIR resources
- Vendor-neutral — aggregates across different EHR vendors

**Clinical Viewer**
- Web-based, access-controlled clinical viewer for providers
- Presents a unified longitudinal patient record aggregated from multiple sources
- Personalized and role-based views

**FHIR APIs**
- SMART on FHIR framework
- FHIR and bulk-FHIR APIs with granular access controls
- Ability for partners to build custom clinical apps on top of the platform
- Data streaming to data warehouses for analytics

**Patient Engagement / Digital Front Door**
- White-labeled mobile apps and web portal
- Patient and family member access to health data
- Appointment scheduling and management
- Secure messaging with providers
- Clinical pathways with patient-centric notifications
- Gamified patient engagement experiences
- Patient-reported data collection

**Care Coordination**
- Surgery coordination: intelligent task allocation, documents, alerts, and notifications for surgical workflows (mphrX cited reducing surgery cancellations by 50%)
- Care pathway management with adherence/compliance oversight
- Stakeholder coordination with transparent task views and timelines

**Virtual Care**
- Telemedicine capabilities
- On-demand and scheduled virtual visits
- Multi-channel patient-provider communication

**Analytics & Insights**
- Integration of third-party AI technologies for business intelligence
- Data available for analytics via FHIR APIs and warehouse streaming

### Data & Content

Based on the evidence gathered, the data Minerva manages includes:

**Aggregated clinical data** (sourced from connected EHRs, HIS, PACS, etc.):
- Patient demographics and longitudinal health records in FHIR format
- Clinical data from EMRs (the specifics depend on what's connected — could include problems, medications, allergies, lab results, clinical notes, etc.)
- Claims data (explicitly mentioned: "brings together clinical and claims data")
- Imaging references (PACS integration mentioned)

**Natively generated data** (created within Minerva itself):
- Patient-reported data and outcomes
- Appointment/scheduling data (16M+ appointments booked)
- Secure messages between patients and providers
- Patient engagement activity (pathway adherence, gamification data)
- Care coordination tasks, documents, alerts, and notifications (especially surgical coordination workflows)
- User accounts and access control data (52M+ patient accounts, 350K+ clinical users)

**Important distinction:** Much of the clinical data in Minerva is *aggregated from other systems*, not originally entered in Minerva. The platform acts as a data hub, not a primary clinical documentation system. However, it does generate its own data through patient engagement, messaging, scheduling, care coordination, and patient-reported outcomes. The EHI export obligation under (b)(10) would cover all data storable by the product, which includes both aggregated clinical data and natively generated data.

**Gaps in research:** The mphrx.com website was offline, limiting direct access to detailed product documentation. It's unclear exactly which FHIR resources Minerva stores natively, what the schema looks like for care coordination and surgical workflow data, or how granular the patient-reported data collection is. The vendor's ONC disclosure page provides only a high-level description.

---

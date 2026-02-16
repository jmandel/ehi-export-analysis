# Oracle Health — Product Research

Researched: 2026-02-16
Developer website: https://www.oracle.com/health

## Overview

Oracle Health is a division of Oracle Corporation (NYSE: ORCL), one of the world's largest enterprise software companies. Oracle Health was formed when Oracle completed its acquisition of Cerner Corporation in June 2022 for approximately $28.3 billion. Cerner, founded in 1979 and headquartered in Kansas City, Missouri, was one of the two dominant EHR vendors in the United States (alongside Epic Systems). The acquisition brought Cerner's healthcare IT portfolio — including the flagship Millennium EHR platform — under the Oracle brand, rebranded as "Oracle Health."

Oracle Health holds approximately 22.9% of the U.S. acute care hospital EHR market by number of hospitals (2024, per KLAS Research), making it the second-largest hospital EHR vendor behind Epic Systems (~42.3%). However, Oracle Health has been losing market share steadily: it experienced a net loss of 74 hospitals and over 17,000 inpatient beds in 2024 alone. The platform is deployed globally, serving hospitals, health systems, ambulatory clinics, government agencies (including the U.S. Department of Veterans Affairs and Department of Defense), and community hospitals. Notable customers include Community Health Systems, BayCare, University Health, Emirates Health Services, and the VA (which has a multibillion-dollar contract to deploy Millennium across 164 medical centers, though the rollout has been paused and is restarting in 2026).

## Product: Oracle Health Millennium (Clinical)

CHPL IDs: 11522 (version 2024), 11670 (version 2025)

### What It Is

Oracle Health Millennium (Clinical) — formerly Cerner Millennium — is a comprehensive, modular EHR platform designed for acute care hospitals, health systems, and ambulatory settings. The certified "Clinical" module is the core clinical component of a much larger Millennium platform that encompasses clinical, financial, operational, and administrative functions. The CHPL certification covers the clinical EHR capabilities, but the product as deployed at customer sites typically includes many additional modules that are part of the broader Millennium ecosystem.

The certification covers a wide range of clinical criteria: (a)(1)–(a)(5) for core clinical data (CPOE, demographics, problem list, medication list, medication allergy list), (a)(12) and (a)(14) for family health history and implantable device list, (b)(1)–(b)(3) for transitions of care, (b)(10) for EHI export, (b)(11) for care plan, (e)(3) for patient health information capture, (g)(7) and (g)(9)–(g)(10) for FHIR API access, and (h)(1) for Direct Project messaging. The SED intended user description is "Physicians."

### Users & Market

**End users**: Physicians, nurses, pharmacists, lab technicians, radiologists, surgeons, emergency department clinicians, administrative and billing staff, practice managers, and patients (via the patient portal). The SED testing focused on physicians.

**Clinical settings**: Large multi-hospital health systems, academic medical centers, community hospitals, critical access hospitals (via CommunityWorks), ambulatory clinics, emergency departments, surgical suites, and government/federal facilities (VA, DoD).

**Market position**: Second-largest acute care EHR in the U.S. (~22.9% of hospitals, 2024). Deployed at thousands of hospitals worldwide. The platform is available as on-premise, cloud-hosted, or as a fully managed SaaS solution (CommunityWorks for smaller facilities). Oracle has been investing heavily in cloud migration and AI capabilities to stem customer losses to Epic.

**Notable deployments**: Community Health Systems (one of the largest U.S. for-profit hospital operators), BayCare Health System, Oklahoma State University Medical Center, the VA (ongoing, troubled deployment), and various international customers (Emirates Health Services, OneLondon, CAMH in Canada).

### Modules & Functionality

The Millennium platform is highly modular. Based on vendor materials, third-party reviews, and industry documentation, the following modules and capabilities are part of the product:

**Core Clinical (PowerChart)**
- PowerChart is the primary clinical interface for providers. It supports chart review, clinical documentation, encounter management, vital signs recording, patient demographics, problem lists, medication lists, allergy documentation, immunization records, and growth charts. It provides the unified patient record across all care settings. (Source: oracle.com/health/clinical-suite/electronic-health-record/, softwareconnect.com, virtualizehealth.com)

**Computerized Provider Order Entry (PowerOrders / CPOE)**
- Integrated order entry for medications, labs, imaging, procedures, and other clinical orders. Includes clinical decision support with drug interaction alerts, allergy checks, and evidence-based order sets. (Source: certified criteria (a)(1), latenthq.com, virtualizehealth.com)

**Pharmacy (PharmNet)**
- Comprehensive pharmacy information system supporting closed-loop medication management: order entry, pharmacy verification, dispensing, and electronic medication administration records (eMAR). Shares a unified drug database across the platform. (Source: pharmacystandards.org, pppmag.com)

**Laboratory (PathNet)**
- Full laboratory information system covering chemistry, hematology, microbiology, blood bank, and anatomic pathology. Supports specimen collection/tracking, orders/results management, automated result reporting, instrument integration, reflex testing, and auto-validation. (Source: virtualizehealth.com)

**Radiology (RadNet)**
- Radiology information system (RIS) with scheduling, order tracking, results management, reporting, and PACS integration for image viewing within the EHR. (Source: virtualizehealth.com)

**Surgery (SurgiNet)**
- Perioperative workflow management: pre-op assessment, case planning, intraoperative documentation, anesthesia records, supply management, charge capture, and post-surgical care documentation. (Source: web search results, healthmanagement.org)

**Emergency Department (FirstNet)**
- ED-specific module for patient tracking, triage, rapid registration, clinical documentation, order entry, result viewing, and charge tracking. Designed for high-throughput emergency care workflows. (Source: healthmanagement.org, medical.drncognito.com)

**Ambulatory / Outpatient**
- Outpatient clinic management including scheduling, documentation, e-prescribing, charting, and analytics tailored for primary care and specialty clinics. Oracle Health also markets an "Ambulatory Suite" as a distinct solution area. (Source: oracle.com/health/clinical-suite/, ehrenhancify.com)

**Revenue Cycle Management / Financial Operations**
- Patient Accounting: claims processing, payments, revenue posting, insurance management, denials management, A/R tracking, financial dashboards.
- Registration Management: patient registration, insurance verification, real-time eligibility checking.
- Contract and Practice Management: payer contracts, scheduling, and financial analytics.
- The Oracle Health website explicitly lists "Financial Operations" as a major solution area: "Integrate your revenue cycle from registration through bill collection." (Source: oracle.com/health, choc.org Cerner Patient Accounting Overview, roihs.com)

**Patient Portal (HealtheLife / Consumer Experience)**
- Patient-facing portal for secure messaging with providers, appointment scheduling, viewing lab/radiology results, medication lists, visit summaries, bill payment, health education, and personalized care plans. Oracle's website describes this as "Consumer Experience" — providing "personalized tools to manage their health, connect with care team members." (Source: oracle.com/health, digitalhealth.folio3.com)

**Clinical Decision Support**
- Drug-drug interaction alerts, allergy alerts, lab alerts, evidence-based clinical guidelines, and order sets. Certified for (a)(9) via CPOE integration. (Source: softwareconnect.com, certified criteria)

**Population Health (HealtheAnalytics)**
- BI and analytics tools for population health management, care coordination, quality reporting, care management, and outcomes tracking. (Source: oracle.com/health — "Population Health" solution area)

**Interoperability**
- HL7 and FHIR R4 API support, Direct Project messaging (h)(1), C-CDA document exchange for transitions of care, interoperability management console for clinical exchange, public health reporting, labs/diagnostics. (Source: oracle.com/health, docs.oracle.com Millennium Platform APIs)

**Clinical Operations**
- Real-time health system operations: capacity/bed management, patient throughput, transfers, staffing, shift planning, communications, and enterprise-wide coordination. (Source: oracle.com/health)

**Reporting and Analytics**
- EHR-agnostic analytics, embedded AI/ML in workflows, quality metrics tracking, and operational efficiency reporting. (Source: oracle.com/health)

**CommunityWorks**
- Cloud-based, multi-tenant version of Millennium tailored for critical access, community, and specialty hospitals. Delivers the full EHR suite at a fixed-fee model with managed infrastructure. (Source: oracle.com CommunityWorks flyer)

**AI Capabilities**
- Clinical AI Agent (formerly Clinical Digital Assistant) for conversational AI, chart navigation, documentation automation, and clinical summaries. AI is described as "embedded into every layer" of the platform. (Source: oracle.com/health, healthcareitleaders.com)

**Additional Capabilities Mentioned on Vendor Website**
- Continuum of care: rehabilitation, home health, long-term care, behavioral health
- Service lines and departments: oncology, maternity, pediatrics, surgery-specific workflows
- Payer operations: data exchange and payer-provider collaboration
- Security: clinical identity management, compliance, security auditing
- Healthcare ERP, HCM, and NetSuite integration (broader Oracle ecosystem, not part of Clinical certification)

### Data & Content

Based on the modules and features documented above, Oracle Health Millennium stores and manages the following categories of data:

**Clinical data** (well-documented): Patient demographics, encounters, problem lists, medication lists, medication allergy lists, immunization records, vital signs, clinical notes/documentation, family health history, implantable device lists, care plans, clinical orders (medications, labs, imaging, procedures), clinical decision support alerts, and growth charts. These are directly evidenced by the certified criteria (a)(1)–(a)(5), (a)(12), (a)(14), (b)(11).

**Medication/pharmacy data**: Medication orders, dispensing records, eMAR (medication administration records), pharmacy verification records, drug databases. Evidenced by PharmNet module documentation.

**Laboratory data**: Lab orders, specimen tracking, lab results (across multiple disciplines — chemistry, hematology, microbiology, blood bank, anatomic pathology), instrument data. Evidenced by PathNet module documentation.

**Radiology/imaging data**: Imaging orders, radiology reports, PACS-linked images. Evidenced by RadNet module.

**Surgical/perioperative data**: Surgical case records, pre-op assessments, intraoperative documentation, anesthesia records, surgical supply usage, surgical charges. Evidenced by SurgiNet module.

**Emergency department data**: Triage records, ED encounters, ED-specific clinical documentation, ED tracking data, ED charges. Evidenced by FirstNet module.

**Financial/billing data**: Claims, charges, payments, insurance information, eligibility records, A/R data, denials, payer contracts, registration data. Evidenced by Revenue Cycle Management solution area on oracle.com and Cerner Patient Accounting documentation.

**Patient portal/messaging data**: Secure messages between patients and providers, patient-entered health information, appointment records, patient-facing billing data. Evidenced by HealtheLife portal and (e)(3) certification for patient health information capture.

**Transitions of care data**: C-CDA documents (Continuity of Care Documents, discharge summaries, referral notes), Direct messages. Evidenced by (b)(1)–(b)(3) and (h)(1) certification.

**Operational data**: Bed management records, patient throughput/tracking data, staffing/shift data, audit logs. Evidenced by Clinical Operations solution area.

**Analytics/population health data**: Aggregated quality metrics, population health records, care management data. Evidenced by HealtheAnalytics and Population Health solution areas.

**Interoperability data**: FHIR resources, HL7 messages, integration logs. Evidenced by (g)(7)–(g)(10) certification and developer documentation.

**Key observation for EHI export assessment**: The Millennium platform is an extremely broad product — it's not just a clinical EHR but a comprehensive hospital information system encompassing clinical, financial, operational, pharmacy, lab, radiology, surgical, ED, and patient engagement functions. The certified "Clinical" module is the clinical core, but the "product of which the Health IT Module is a part" (per the (b)(10) rule) arguably encompasses all of these integrated Millennium modules. This means the EHI export should cover data from all modules that are part of the Millennium product, not just the narrowly-certified clinical functions. The mandatory disclosures page confirms that Oracle Health supports both single-patient and population-level EHI export.

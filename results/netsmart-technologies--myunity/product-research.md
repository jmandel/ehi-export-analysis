# Netsmart Technologies — Product Research

Researched: 2026-02-16
Developer website: https://www.ntst.com/

## Overview

Netsmart Technologies is a major healthcare IT company headquartered in Overland Park, Kansas, with technology origins dating back to 1968 (Creative Socio-Medics, acquired 1994). The company specializes in EHR and health information technology for **behavioral health, human services, and post-acute care** — a distinct market niche compared to the acute/ambulatory EHR giants like Epic and Oracle Health. Netsmart has undergone significant private equity ownership transitions: Genstar Capital acquired it in 2010, then GI Partners and Allscripts bought it for $950M in 2016 (Allscripts merged its homecare software business into Netsmart), and in 2018 GI Partners and TA Associates acquired Allscripts' stake. Netsmart remains privately held under GI Partners.

The company reported $319M in revenue in 2018 and claims more than 23,000 customer organizations, 450,000+ care providers, and 40+ state systems as users. Its product portfolio is organized under the **CareFabric** platform and includes multiple EHR products: **myAvatar** (behavioral health), **myEvolv** (addiction/autism/IDD), **myUnity** (post-acute care), **GEHRIMED** (geriatric/LTC physician practices), and **TheraOffice** (physical therapy). Netsmart has made 17+ acquisitions, including HealthMEDX (LTC EHR, 2016), McBee (healthcare consulting, 2019), and Netalytics (addiction treatment, 2023). The company also provides AI tools (Bells AI for documentation, AlphaCoding for coding), interoperability/HIE services, workforce management, analytics, and revenue cycle management services across its platform.

## Product: myUnity

CHPL IDs: 11409

### What It Is

myUnity is Netsmart's **unified post-acute care EHR platform** — a single integrated system designed to serve the full spectrum of post-acute and senior care settings. Unlike many EHRs that target one care setting, myUnity explicitly spans:

- **Home Health**
- **Hospice**
- **Palliative Care**
- **Skilled Nursing Facilities (SNF)**
- **Senior Living** (assisted living, independent living, memory care)
- **Life Plan Communities / CCRCs** (Continuing Care Retirement Communities)
- **Personal Care / Private Duty**
- **Adult Day Care**
- **State Veterans Homes**

The certified module (CHPL #11409, version 2023) carries a broad set of ONC certifications covering clinical data (a)(1)-(a)(5), (a)(12), (a)(14); transitions of care (b)(1)-(b)(3); EHI export (b)(10)-(b)(11); clinical quality measures (c)(1)-(c)(3); patient portal/VDT (e)(1), (e)(3); public health reporting (f)(1), (f)(5); and FHIR API access (g)(7), (g)(9), (g)(10). There is also a separate "myUnity Senior Living" ONC certification mentioned on the certifications page. The product is cloud-based and part of the broader Netsmart CareFabric ecosystem.

The next-generation version, **myUnity NX**, was demonstrated at LeadingAge 2024 and features redesigned UX, integrated AI, and enhanced mobile capabilities, described as "designed by clinicians for clinicians."

### Users & Market

myUnity targets **post-acute care providers** across all care settings. Day-to-day users include:

- **Home health nurses and clinicians** performing bedside documentation during visits
- **Hospice interdisciplinary teams** (physicians, nurses, social workers, chaplains, bereavement counselors)
- **Skilled nursing facility staff** handling MDS assessments and resident care
- **Senior living administrators and caregivers** managing residents across assisted living, memory care, and independent living
- **Billing and administrative staff** across all settings
- **Practice managers and compliance officers**

Notable deployments include:
- **Interim HealthCare** agencies implementing myUnity as their EHR platform (Yahoo Finance press coverage)
- **Ohio's Hospice** implementing Netsmart EHR system across their network
- The product has **CHAP Verification** for both home health and hospice, a quality accreditation

Netsmart claims significant market share in post-acute care, receiving 28 Black Book Research awards in 2025, including #1 rankings in behavioral health, long-term care, and value-based care technology. However, KLAS research presents a more mixed picture — about two-thirds of surveyed customers said they would not buy their Netsmart solution again, citing concerns about development pace and support relative to sales emphasis.

### Modules & Functionality

myUnity is organized around care-setting-specific workflows within a single integrated platform. Key modules and capabilities found in vendor materials:

**Home Health Module:**
- Point-of-care clinical documentation on mobile devices during visits
- OASIS-E assessment compliance and completion tools
- PDGM (Patient-Driven Groupings Model) billing support
- Electronic Visit Verification (EVV) via Mobile Caregiver+
- CareRouter mobile dispatch for staff triaging and urgent visit scheduling
- Orders management with physician signature workflows
- Medication management with batch updates and reconciliation
- Care plan creation and management
- Interoperability via Carequality and HIE connections to import CCDAs, allergies, medications, diagnoses

**Hospice Module:**
- Interdisciplinary Group (IDG) meeting workflows with automated agenda development
- Bereavement care plan creation, management, and tracking
- Inpatient Unit (IPU) management including patient status, interim care, and continuous care tracking
- HOPE assessment scrubbing (compliance tool)
- Physician orders management
- Medication tracking including dosage and administration schedules
- Symptom management documentation
- Care coordination across interdisciplinary teams

**Skilled Nursing Module:**
- MDS (Minimum Data Set) assessment tools
- PDPM (Patient-Driven Payment Model) optimization via Netsmart Simple analytics
- Near real-time predictive MDS analytics (CORE Analytics)
- Staffing analytics
- Regulatory compliance workflows
- eMAR (Electronic Medication Administration Record)

**Senior Living Module (AL/IL/Memory Care):**
- Single resident record spanning all care levels within a community
- Care planning with personalized activity scheduling
- Health monitoring with real-time metrics and alert systems
- Medication management and eMAR
- Incident reporting
- Role-based customizable views
- Billing across care levels with unified patient statements

**Cross-Setting Capabilities:**
- **Scheduling**: Visit scheduling, appointment management, staff assignments across settings
- **Billing/Revenue Cycle**: Claims submission and management for Medicare, Medicaid, Medicare Advantage, commercial insurance, and private pay; payment tracking; automated eligibility checks; collections automation
- **ePrescribing**: Electronic prescribing integrated into clinical workflows
- **Analytics & Reporting**: KPI dashboards with clinical, financial, and operational metrics; ED/hospitalization alerts; trend tracking
- **Interoperability**: Integration with Epic, Cerner, Allscripts and other acute care EHRs; Carequality/HIE connectivity; secure data exchange
- **Telehealth**: Two-way HD virtual consultations (scheduled or on-demand)
- **Mobile Access**: Tablet and phone support for field clinicians with offline capabilities
- **Referral Management**: Tools for managing referrals across care settings
- **CMS Reporting**: iQIES data submission, MIPS/MACRA quality reporting, public health reporting
- **Patient/Family Engagement**: Portal capabilities certified under (e)(1) and (e)(3)
- **Secure Messaging**: Communication tools for care coordination

**AI/Automation (CareFabric ecosystem):**
- Bells AI documentation assistant
- AlphaCoding for automated coding
- Apricot: generative AI for reducing start-of-care documentation time
- AlphaCollector: RPA for prioritizing unpaid claims

### Data & Content

Based on the features described above, myUnity manages a substantial breadth of data across post-acute care settings:

**Clinical Data (evidenced by vendor materials):**
- Patient demographics and unified patient/resident records across care settings
- Clinical assessments including OASIS (home health), MDS (skilled nursing), HOPE (hospice)
- Care plans (home health, hospice, bereavement, senior living)
- Physician orders
- Medications (prescriptions, eMAR, administration records, reconciliation)
- Allergies
- Diagnoses/problem lists
- Vital signs and health monitoring data
- Clinical notes and visit documentation
- IDG meeting notes and agendas (hospice)
- Immunizations (implied by (a)(3) certification)
- Lab results/diagnostic reports (implied by clinical data criteria)
- Procedures
- Clinical decision support alerts

**Administrative/Financial Data (evidenced by vendor materials):**
- Billing records and claims data (Medicare, Medicaid, MA, commercial, private pay)
- Payment and collections data
- Insurance/eligibility information
- Scheduling and visit records
- Electronic Visit Verification (EVV) records
- Staff assignments and workforce dispatch data
- Referral records
- Revenue cycle and financial analytics

**Regulatory/Compliance Data:**
- Clinical quality measures (certified for CQM criteria)
- Public health reporting data (immunization registries, syndromic surveillance)
- Audit trails
- Compliance tracking records

**Communication/Engagement Data:**
- Secure messaging between providers
- Patient/family portal data (view, download, transmit per (e)(1) certification)
- Telehealth session records
- Care coordination communications

**Interoperability Data:**
- CCDAs imported from acute care EHRs via Carequality/HIE
- FHIR API data (certified for (g)(7), (g)(9), (g)(10))
- Transitions of care documents

The vendor website does not explicitly discuss some data types that might be present in such a comprehensive post-acute platform — for instance, wound care documentation (photos, measurements), fall risk assessments, ADL (Activities of Daily Living) tracking, dietary/nutrition records, or therapy notes. These are common in post-acute EHRs but were not specifically called out in the materials reviewed. The absence from marketing pages does not necessarily mean the data isn't stored; it may simply not be highlighted.

---

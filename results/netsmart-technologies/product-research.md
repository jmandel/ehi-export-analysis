# Netsmart Technologies — Product Research

Researched: 2026-02-14
Developer website: https://www.ntst.com/

## Overview

Netsmart Technologies is a large, privately held health IT company headquartered in Overland Park, Kansas, with ~2,500 employees and estimated annual revenue of ~$480–510 million. The company describes itself as "healthcare's largest human services and integrated care technology provider," serving 500,000+ users across 24,000+ organizations in all 50 states, covering ~25 million persons. It is owned by private equity firms GI Partners (majority, since 2016) and TA Associates (since 2018). In 2024, owners reportedly explored a sale valuing the company at $5+ billion including debt.

Netsmart's core markets are **behavioral health / human services** and **post-acute care** (home health, hospice, skilled nursing, senior living, geriatrics). Its product portfolio, branded as the **CareFabric platform**, includes eight ONC-certified products: myAvatar (behavioral health), myEvolv (addiction/autism/IDD), myUnity (post-acute facility EHR), GEHRIMED (geriatric physician EHR), TheraOffice (PT/rehab), myHealthPointe (patient portal), and CarePathways (measures reporting). Netsmart has completed 17+ acquisitions since its founding in 1992, including HealthMEDX (LTPAC EHR, 2016), GPM/GEHRIMED (geriatric EHR, 2021), TheraOffice (PT EMR, 2022), and Change Healthcare's Home Care & Hospice Solutions (2023).

## Product: GEHRIMED

CHPL ID: 11136
CHPL Product Number: 15.04.04.2816.gEHR.04.03.1.221227
Version: v.4.3
Certification Date: 2022-12-27
SED Intended Users: "LTPAC clinicians and support staff"

### What It Is

GEHRIMED (stylized "gEHRiMed") is a **cloud-based electronic health record (EHR) and practice management platform designed exclusively for long-term/post-acute care (LTPAC) and post-acute/long-term care (PALTC) practitioners** — primarily geriatricians, nurse practitioners, and physician assistants who round across multiple skilled nursing facilities, assisted living communities, and other LTPAC settings. It was originally developed by Geriatric Practice Management (GPM) Corp, a company founded in 2012 "by physicians and nurse practitioners who see patients across multiple post-acute and long-term care facilities." GPM and GEHRIMED were acquired by Netsmart in February 2021.

GEHRIMED occupies a unique niche: it is not a facility-side EHR (like PointClickCare or Netsmart's own myUnity) but rather a **physician practice EHR** for the itinerant doctors and NPs who visit patients inside those facilities. The core use case is a provider who rounds at 3–5 nursing homes in a day, seeing patients at the bedside at each one. The product emphasizes mobility, multi-facility census management, and integration with facility EHR systems.

GEHRIMED was notably the first LTPAC EHR to receive ONC certification (2011) and currently holds ONC Health IT 2015 Edition Cures Update certification. Its certified criteria span clinical data (a)(2/3/5/12/14), transitions of care (b)(1/2), EHI export (b)(10), patient portal (e)(1/3), cancer case reporting (f)(5), and FHIR API (g)(10), plus privacy/security criteria. The breadth of clinical criteria — CPOE for lab and imaging, demographics, family health history, implantable device list — indicates it functions as a full clinical EHR, not just a documentation tool.

### Users & Market

**Primary users:** Geriatricians, internal medicine and family medicine physicians doing LTPAC rounding, nurse practitioners, physician assistants, and their support/billing staff.

**Settings served:** Skilled nursing facilities (SNFs), assisted living, long-term care hospitals, continuing care retirement communities (CCRCs), memory care, rehabilitation centers, hospice, and independent living — but always from the perspective of the visiting physician practice, not the facility itself.

**Market position:** GEHRIMED ranked **#1 in Geriatrics and Gerontology EHR & Practice Management** in the 2025 Black Book Research Survey (evaluating 749 gerontology-focused practices across 58 competing solutions). Netsmart has been ranked the #1 post-acute technology vendor by Black Book for seven consecutive years. The vendor markets the product as supporting practice sizes from solo to 50+ providers.

**Customer count:** Not publicly disclosed. The Black Book survey's sample of 749 gerontology practices gives a sense of market size. Netsmart overall serves 24,000+ organizations but that includes all their products.

**Reviews:** SoftwareFinder/GetApp shows 4.3/5 overall (25 reviews, 88% positive). Reviewers cite improved clinical documentation efficiency and quality measure tracking as positives. Criticisms include UI issues and occasional system problems.

**Specialties noted in reviews:** Family Medicine, Internal Medicine, Behavioral Health, Nephrology, Physical Therapy, Podiatry, Speech Therapy — all in the context of LTPAC rounding.

### Modules & Functionality

Based on vendor materials (ntst.com geriatric EHR page, blog posts, feature announcements) and third-party reviews:

**Clinical Documentation:**
- Customizable encounter note templates specifically designed for LTPAC encounters (vendor claims ~50% reduction in documentation time)
- Structured charting workflow: history, review of systems, vitals, physical exam, diagnosis, assessment, plan
- Wound assessment module with access to historical wound details
- Photo/image capture for patient records (wound photos, etc.)
- Expanded Addendum feature allowing providers to update CPT and ICD data after encounter signature
- Medical speech-to-text via Nuance integration (add-on)
- AI-powered ambient listening for automated visit documentation (announced as upcoming feature)

**Census Manager:** Central clinical dashboard showing patient census by facility, unsigned encounters, secure messages, clinical measures, and reports. This is the primary navigation tool for providers who round at multiple facilities.

**E-Prescribing:** Integrated via Dr. First (add-on). Supports controlled and non-controlled substances, real-time benefit checks, PDMP integration, and clinical decision support.

**CPOE:** Certified for CPOE - Laboratory (a)(2) and CPOE - Diagnostic Imaging (a)(3), meaning the system can generate and transmit orders for lab tests and imaging studies.

**Billing & Revenue Cycle Management:**
- Automated billing and charge capture
- Claims submission and tracking
- Electronic remittance advice (ERA) processing
- Denial management
- Accounts receivable management
- **AlphaCollector** automation tool for AR processing (vendor claims saved 51,400+ hours between May 2022 and end of 2023)
- CPT Code Protection — place-of-service aware system restricting access to LTPAC-related codes to prevent coding errors
- Revenue cycle management services also available (outsourced option)

**Quality & Compliance:**
- MIPS dashboard with real-time Merit-based Incentive Payment System tracking and alert notifications
- MIPS Value Pathways (MVPs)
- Electronic Clinical Quality Measures (eCQMs)
- ACO quality measures support
- Cancer case reporting (certified for (f)(5))

**Communication & Interoperability:**
- Automated encounter delivery — signed encounters automatically sent to facility personnel
- Note-faxing directly from the system
- Secure internal messaging (real-time)
- **PointClickCare bi-directional integration** — described as "one of the most-used integrations on the PointClickCare marketplace"; enables real-time patient data exchange including charts, e-prescriptions, orders, clinical documentation
- Carequality integration for health information exchange
- CareConnect (Netsmart's interoperability network) connecting to regional and state HIE networks
- Updox integrated efaxing
- Telehealth capabilities (add-on)

**Patient Portal:** myHealthPointe consumer engagement portal — certified for (e)(1) View/Download/Transmit and (e)(3) Patient Health Information Capture.

**Transitions of Care:** Certified for (b)(1) Transitions of Care and (b)(2) Clinical Information Reconciliation and Incorporation — meaning it can send and receive C-CDA documents and reconcile incoming clinical information.

**Analytics:**
- Interactive data visualization dashboards for clinical, financial, and operational metrics
- Productivity monitoring for individual and partnered providers
- KPI dashboards
- Chronic Care Management (CCM) Dashboard

**Practice Management:**
- Appointment scheduling and follow-up reminders
- Patient search and management
- Custom reports

**Platforms:** Cloud-based, accessible via web browser. macOS desktop app and iPad app available (App Store listing confirmed). Designed for mobile use — laptop or tablet at the bedside.

### Data & Content

Based on the feature descriptions, certifications, and vendor materials, GEHRIMED stores and manages:

**Clinical Data:**
- Patient demographics (certified (a)(5))
- Encounter notes (structured templates + rich text)
- Vital signs
- Medications and medication lists
- E-prescriptions (via Dr. First integration)
- Allergies
- Diagnoses (ICD-10 coded)
- Problem lists (including facility-level problem lists)
- Immunizations
- Family health history (certified (a)(12))
- Implantable device list (certified (a)(14))
- Advance directives and code status
- Wound assessments (structured data with history)
- Physical exam findings, review of systems, assessment and plan
- Patient images/photos (wound photos, clinical images)
- Lab orders (certified for CPOE lab (a)(2))
- Diagnostic imaging orders (certified for CPOE imaging (a)(3))

**Administrative/Financial Data:**
- CPT procedure codes and billing charges
- Claims data (submission, tracking, remittance)
- Accounts receivable data
- Scheduling/appointment data
- Practice management data

**Communication Data:**
- Secure messages (internal messaging between providers/staff)
- Encounter delivery records (faxed/sent notes to facilities)
- Transitions of care documents (C-CDAs sent/received)

**Quality/Compliance Data:**
- MIPS measure tracking data
- eCQM data
- Cancer case reports (certified (f)(5))

**Per the EHI export documentation** (referenced but not yet reviewed in depth): the export provides data in "a computable, delimited file format native to GEHRIMED," with each database table generating its own file. Rich text documents and images may be referenced rather than directly included. A downloadable ZIP contains documentation describing all tables and column-level details.

**Notable:** The website does not mention lab results storage (only lab ordering via CPOE), suggesting that while GEHRIMED can order labs, results may flow back through facility systems rather than being stored in GEHRIMED directly. This is consistent with the physician-rounding workflow where the facility manages ongoing result tracking. However, the Carequality and CareConnect integrations could bring some external clinical data into the system. This is worth verifying during Phase 2 export review.

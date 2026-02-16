# Net Health / RestorixHealth — Product Research

Researched: 2026-02-16
Developer website: https://www.nethealth.com/

## Overview

Net Health Systems is a Pittsburgh-based healthcare software company founded in 1993 that specializes in EHR and analytics solutions for specialty care settings — primarily wound care, rehab therapy (PT/OT/SLP), employee health, and post-acute care. The company serves approximately 23,000 organizations and claims to work with 98% of the largest hospital chains. Net Health has approximately 630 employees and has raised over $1 billion in funding. In December 2017, Net Health was acquired by The Carlyle Group, Level Equity, and Silversmith Capital Partners from Spectrum Equity. The company has grown through numerous acquisitions, including Wound Care Strategies/TPS EMR (2012, which gave them dominant wound care market share), Tissue Analytics (2020, automated wound imaging), Casamba (2021, rehab therapy EMR), and PointRight (2021, skilled nursing analytics). Net Health is headquartered at 40 24th St., 1st Fl., Pittsburgh, PA 15222.

RestorixHealth is a separate company — a wound care management services company (not a software company) founded in 1997 by physicians. They develop and manage outpatient wound care centers in partnership with hospitals and health systems, providing a turnkey outsourced model. RestorixHealth partners with 280+ hospitals across 39 states, including 100+ Critical Access Hospitals. In 2021, RestorixHealth merged with American Medical Technologies (AMT), creating a combined entity serving 6,250+ facilities across all 50 states. RestorixHealth is headquartered in White Plains, NY and has had multiple private equity owners (Sverica Capital, Leonard Green & Partners, Cressey & Company, One Equity Partners).

## Product: Net Health WoundExpert

CHPL ID: 9836 (version 7.0, certified 2018-12-31)

### What It Is

WoundExpert (also marketed as "Net Health Wound Care") is a **specialty wound care EHR** — not a general-purpose EHR. It is a cloud/web-based electronic health record system purpose-built for wound care providers. Net Health claims it is "the most trusted wound care EHR" and "trusted by more wound care professionals than any other." It is designed to supplement or interface with a facility's primary hospital EHR (Epic, Cerner, etc.) rather than replace it. The product is an ASP.NET web application.

WoundExpert is ONC-certified for a broad set of criteria including clinical data (CPOE, demographics, drug interaction checking, family health history, implantable devices), transitions of care (C-CDA, clinical information reconciliation, e-prescribing), patient portal/API access (FHIR R4 via Darena Health partnership), clinical quality measures, and public health reporting. This is a comprehensive certification covering 37 criteria.

### Users & Market

**Primary users:** Hospital outpatient wound care centers, wound care management companies (like RestorixHealth), long-term care facilities, home health agencies, post-acute care settings, and private wound care practices.

**Market position:** WoundExpert is the dominant specialty EHR for wound care in the US, with claims of ~90% market penetration in wound care. One source cites over 20,000 physicians across more than 1,000 facilities; another says over 2,000 facilities supporting over $2 billion in health services annually. The 2012 acquisition of Wound Care Strategies combined two major wound care software companies, giving Net Health >50% of US wound clinics at that time. Net Health has been collecting wound care data for over 20 years, creating what they describe as "one of the largest condition-specific databases in the world."

**Day-to-day users:** Wound care physicians, nurses, clinical staff at wound care centers, billing/coding staff, and practice managers.

**Third-party ratings:** Capterra rates it 4.4/5 based on 15 reviews. It is described as "the gold standard in managing wound care." Reviews note occasional documentation-save issues, performance concerns with large data volumes, high cost for smaller practices, and some usability challenges for new users.

### Modules & Functionality

**Clinical Documentation** (per vendor materials and FindEMR listing):
- Wound assessment tools: size, depth, tissue type, wound location, etiology, healing stage progression
- Treatment plan creation and management
- Wound dressing recommendations
- Progress notes with customizable templates and automatic coding
- Evidence-based clinical practice guidelines built in
- Medication management

**Wound Imaging** (via Tissue Analytics acquisition, 2020):
- Mobile photo capture of wounds
- Automated wound measurement (reducing subjective manual measurement)
- Visual wound progression tracking over time
- Predictive analytics

**Scheduling** (per FindEMR):
- Daily, weekly, monthly schedule views
- Appointment creation, management, and rescheduling
- Automated appointment reminders

**Financial/Billing** (per FindEMR):
- Invoice generation and payment processing
- Insurance claims management
- Revenue and expense tracking
- Compliance and regulatory support for billing
- Note: RestorixHealth's case study emphasizes their revenue cycle management integration with the platform, including certified coders and denial management specialists

**Patient Engagement:**
- Patient portal (at patientportal.nethealth.com) — certified under (e)(1)
- Patient education materials
- Third-party app connectivity via FHIR API

**Analytics and Reporting:**
- Customizable reports
- Benchmarking across facilities
- Performance insights

**Interoperability** (per vendor interoperability page):
- Eight primary interface types: ADT (Admission/Discharge/Transfer), Billing, C-CDA, Clinical Documentation, Ordered Results, Scheduling, Transcription, Unsolicited Results
- Pre-built integrations with: Epic, Cerner, Allscripts, Athenahealth, MedBridge, Netsmart, PointClickCare
- FHIR R4 API (certified, via Darena Health partnership) supporting USCDI v3 data classes
- HL7 interfaces for hospital information system integration

### Data & Content

Based on certified criteria, vendor materials, and product feature descriptions, WoundExpert stores:

- **Patient demographics** — via ADT interfaces and direct entry; certified (a)(5)
- **Wound assessments** — wound size, depth, tissue type, location, etiology, healing stage; this is the core clinical data
- **Wound photographs and measurements** — via Tissue Analytics integration; automated wound imaging with progression tracking
- **Treatment plans** — wound dressings, medications, interventions, care plans
- **Progress notes and clinical documentation** — with customizable templates
- **Medication data** — certified for CPOE (a)(1) and drug interaction checking (a)(4)
- **Lab and diagnostic imaging orders/results** — certified for CPOE lab (a)(2) and CPOE diagnostic imaging (a)(3)
- **Problem lists, medication lists, allergy lists** — certified (a)(5)
- **Family health history** — certified (a)(12)
- **Implantable device list** — certified (a)(14)
- **Scheduling/appointment data** — appointment creation, reminders, rescheduling
- **Billing and financial data** — charges, claims, payments, revenue tracking
- **Transitions of care documents** — C-CDA documents, certified (b)(1), (b)(2), (b)(3)
- **Clinical quality measure data** — certified (c)(1), (c)(2), (c)(3)
- **Public health reporting data** — certified (h)(1)
- **USCDI data elements** — via FHIR R4 API (g)(10): includes allergies, medications, conditions, procedures, vital signs, etc.
- **Audit logs** — certified for (d) criteria including authentication, access logging, encryption
- **Hyperbaric oxygen therapy records** — mentioned in context of RestorixHealth's services and CutisCare acquisition

The vendor's interoperability page describes eight interface types, which imply the system stores or exchanges: ADT data, billing data, C-CDA documents, clinical documentation, ordered results, scheduling data, transcription data, and unsolicited results. The patient portal implies patient-accessible health records are maintained.

---

## Product: WoundDocs (RestorixHealth)

CHPL ID: 10234 (version 7.0, certified 2019-12-24)

### What It Is

WoundDocs is **a white-labeled/OEM instance of Net Health's WoundExpert**, branded and deployed specifically for RestorixHealth's network of wound care centers. The evidence for this is conclusive:

1. **URL path proof:** The WoundDocs login at `wounddocs.restorixhealth.com` redirects internally to paths containing `/WoundExpert/` (e.g., `/WoundExpert/Misc/OneUiRedirect.aspx` and `ReturnUrl=/WoundExpert/`).
2. **Net Health branding:** The WoundDocs login page displays the Net Health logo and Net Health browser compatibility notices.
3. **Net Health case study:** Net Health explicitly states RestorixHealth uses "Net Health Wound Care" as their EHR platform.
4. **Identical certification:** WoundDocs has exactly the same 37 certified criteria and version number (7.0) as WoundExpert, certified one year later under RestorixHealth's own developer code (2272 vs. Net Health's 2815).

RestorixHealth markets it as "WoundDocs Specialty EMR" and describes it as "an advanced, wound-specific EMR, supported by evidence-based clinical practice guidelines, that interfaces with your current EMR and provides physicians with the information they need for informed medical decision-making."

### Users & Market

WoundDocs is used across the **280+ hospitals and healthcare facilities** that partner with RestorixHealth for wound center management across 39 states. Hospitals do not typically purchase WoundDocs independently — it comes bundled with RestorixHealth's comprehensive wound center management package, which includes clinical staffing, operational support, revenue cycle management, and marketing.

Specific user populations include:
- Hospital-based outpatient wound care center clinicians managed by RestorixHealth
- Critical Access Hospital wound care staff (100+ facilities in 21 states)
- Wound care physicians and clinical staff at partner facilities
- Revenue cycle and billing staff

### Modules & Functionality

Functionally identical to WoundExpert (see above), since it is the same underlying software. RestorixHealth's website additionally emphasizes:

- **Revenue cycle management integration:** RestorixHealth has "one of the largest teams of Revenue Cycle Directors, denial management and reimbursement specialists and certified coders and auditors in the industry," all working within the WoundDocs/WoundExpert platform.
- **Standardized workflows across facilities:** The platform is configured to support RestorixHealth's standardized wound care protocols across their entire network.
- **Hospital EHR interfacing:** Emphasis on integration with existing hospital information systems at each partner site.

### Data & Content

Identical to WoundExpert (see above) — it is the same software platform. Any data WoundExpert can store, WoundDocs can store. The RestorixHealth deployment may additionally emphasize:
- Hyperbaric oxygen therapy records (RestorixHealth acquired CutisCare, a hyperbaric specialist)
- Revenue cycle and billing data specific to wound center management
- Cross-facility benchmarking data across RestorixHealth's 280+ hospital network

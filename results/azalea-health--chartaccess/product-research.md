# Azalea Health — Product Research

Researched: 2026-02-16
Developer website: https://www.azaleahealth.com

## Overview

Azalea Health is a privately held, Atlanta-based health IT company founded in 2008. It provides cloud-based EHR, practice management, billing/RCM, and patient engagement solutions primarily targeting rural hospitals, critical access hospitals, community health centers, and ambulatory clinics. The company has approximately 200–300+ employees and estimated annual revenue in the $14M–$56M range (sources vary). It has raised venture capital through multiple rounds. Azalea competes with vendors like athenahealth, eClinicalWorks, and NextGen but differentiates by focusing on rural and underserved healthcare markets with a cloud-first, low-IT-overhead approach.

Azalea Health has **two distinct certified EHR products**: **ChartAccess** (CHPL 11140, the subject of this report) and **Azalea EHR** (CHPL 11151). ChartAccess is the hospital-focused EHR, while Azalea EHR is the ambulatory/clinic-focused product. Both share the same ONC certification date (12/27/2022) and are part of the broader Azalea platform. The vendor's mandatory disclosures page lists them side-by-side as separate certified products with separate CHPL listings. Notably, the hospital product login portal lives at hospital.azaleahealth.com, suggesting a distinct application architecture.

## Product: ChartAccess ®

CHPL ID: 11140 (15.04.04.2688.Char.07.01.1.221227)
Version: 7.0
Certification date: 2022-12-27

### What It Is

ChartAccess is Azalea Health's **hospital EHR** — designed for inpatient, emergency department, and hospital-based outpatient settings. It is specifically built for rural and critical access hospitals (typically under 100 beds) with limited IT staff and tight budgets. The product is 100% cloud-based and centers on a "one patient, one record" model that connects inpatient, ED, and affiliated clinic settings in a unified platform.

ChartAccess is the certified Health IT Module, but it operates as part of the broader Azalea Health platform that also includes practice management, RCM services, patient engagement, analytics, telehealth, and HIE connectivity. The certified criteria (35+ across clinical, care coordination, patient portal, public health reporting, and FHIR API categories) confirm it covers a wide range of clinical and data exchange capabilities.

### Users & Market

**Primary users**: Clinicians, nurses, ED staff, hospital administrators, billing staff, and IT/operations teams at rural and critical access hospitals. The platform also extends to affiliated ambulatory clinics connected to these hospitals.

**Market focus**: Rural hospitals, critical access hospitals, community health centers, and small health systems. Azalea emphasizes hospitals with limited IT teams that need a cloud-hosted, low-maintenance solution. A testimonial from DeWitt Hospital and Nursing Home and multiple references to Reeves Memorial Medical Center (RMMC) suggest the customer base includes small community hospitals.

**Scale**: The vendor website doesn't provide specific customer counts for ChartAccess vs. Azalea EHR separately. Overall, Azalea Health appears to serve a mid-size customer base across its product lines, positioning as a niche player in the rural/community hospital space rather than a large enterprise vendor.

### Modules & Functionality

Based on vendor website descriptions, product pages, and third-party reviews, ChartAccess and the broader Azalea platform encompass the following capabilities:

**Clinical EHR (Hospital)**
- Unified patient record across inpatient, ED, and outpatient/clinic settings
- Clinical documentation with customizable templates
- CPOE (Computerized Provider Order Entry) — implied by (a)(1)–(a)(5) certification criteria
- Medication management and e-prescribing — certified for (a)(14) implantable device list
- Allergy documentation (screenshots show patient allergy views)
- Lab ordering and results — screenshots show lab result views; interoperability with labs mentioned
- Clinical decision support — certified for (a)(2), (a)(3), (a)(4)
- Problem lists, medication lists, demographics — certified (a)(1), (a)(5)
- Care transitions — certified (b)(1), (b)(2), (b)(3) for transitions of care / clinical information exchange

**AI Clinical Assistant** (powered by Suki)
- Ambient charting with voice-enabled transcription
- AI-generated structured notes from patient encounters
- Integrated into the EHR workflow

**Practice Management**
- Patient scheduling and registration
- Insurance verification
- Patient kiosk (iPad-based check-in with auto-population into EHR)
- Demographic and insurance data capture

**Revenue Cycle Management (RCM)**
- Integrated billing workflows
- Claim scrubbing and submission
- Denials management and appeals
- Accounts receivable management
- Patient collections
- AI Billing Assistant — automated error detection, coding suggestions, claim status tracking
- Financial analytics and reporting
- Mobile charge capture via MyPractice app (ICD & CPT code library)
- RCM is available both as built-in software and as an outsourced service with dedicated billers

**Patient Engagement**
- **myHealthspot patient portal**: allergies, medication list, history, lab results, statement viewing, online bill pay, demographic/insurance updates, appointment requests, secure messaging with providers
- **Integrated telehealth**: HIPAA-compliant video visits with real-time charting, preset templates
- **MyPractice mobile app** (provider-facing): mobile access to patient records, charge capture, face sheet sharing
- **Patient Kiosk**: iPad check-in with English/Spanish support

**Analytics (Azalea Analytics)**
- Financial, operational, and clinical KPI dashboards
- Clinical Quality Measure (CQM) scorecards
- MIPS/MACRA quality reporting
- Population health management and gaps-in-care identification
- Patient risk stratification
- Enterprise Data Warehouse with ETL processing
- Can integrate with other EHR systems (Athena, eCW, NextGen, etc.)

**Interoperability & Data Exchange**
- **AzaleaConnect HIE**: Connection to one of the nation's largest Health Information Exchanges for querying external patient records
- FHIR API access — certified (g)(7)–(g)(10)
- Public health reporting — certified (f)(1) immunization, (f)(2) syndromic surveillance, (f)(3) electronic case reporting, (f)(6) electronic reportable lab results
- C-CDA document exchange for transitions of care
- E-prescribing (Surescripts integration implied by medication management features)

**Compliance & Security**
- ONC 2015 Cures Edition certified
- Multi-factor authentication (MFA)
- Audit trails and user activity tracking
- eCQM reporting

### Data & Content

Based on the certified criteria and vendor-described features, ChartAccess stores or manages:

- **Clinical data**: Patient demographics, problem lists, medication lists, allergy lists, implantable device lists, vital signs, clinical notes (SOAP notes), lab orders and results, imaging orders, care plans, clinical decision support alerts
- **Encounter data**: Inpatient admissions, ED visits, outpatient visits, telehealth encounters (with video visit records)
- **Medication/prescribing data**: E-prescriptions, medication history — certification includes (a)(14) implantable device list but also (a)(1) CPOE for medications
- **Billing/financial data**: Claims, CPT/ICD codes, charge capture records, payment posting, accounts receivable, denial records, patient statements, insurance eligibility data
- **Patient-generated data**: Demographic updates, insurance information updates, appointment requests, secure messages to/from providers (via myHealthspot portal)
- **Documents**: C-CDA documents (for transitions of care), care summaries
- **Quality/reporting data**: CQM data, MIPS quality measures, immunization records, syndromic surveillance data, electronic case reports, reportable lab results
- **Audit data**: User activity logs, access tracking
- **Analytics data**: Enterprise Data Warehouse with aggregated clinical, financial, and operational metrics
- **HIE-sourced data**: External patient records retrieved through AzaleaConnect

The vendor clearly describes integrated billing as a core feature (not a separate product), with claims submission, denial management, and patient collections built into the platform. The myHealthspot patient portal stores patient-facing messages, appointment requests, and bill payment records. The MyPractice mobile app captures charges and face sheets.

**Gaps in research**: The vendor website doesn't provide detailed information about document/image storage (scanned documents, imaging results beyond orders), specific data retention policies, or the precise technical architecture separating ChartAccess from Azalea EHR at the database level. It's unclear whether ChartAccess and Azalea EHR share a single database or maintain separate data stores for the same patient. The certification page uses "ChartAccess" for the hospital product and "Azalea EHR" for the ambulatory product, suggesting they are at minimum separately certified modules, but the platform marketing emphasizes a unified "one record" approach.

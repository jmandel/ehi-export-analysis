# CliniComp, Intl. — Product Research

Researched: 2026-02-15
Developer website: http://www.clinicomp.com

## Overview

CliniComp, Intl. is a privately held healthcare IT company founded in 1983 in San Diego, California, by Chris Haudenschild. The company has grown organically for over 40 years without outside financing. As of mid-2025, CliniComp employs approximately 166 people across 3 continents (North America, Asia, South America).

CliniComp's core market has historically been **high-acuity hospital environments**, particularly in the **U.S. military and Veterans Administration (VA)** sectors. Their legacy product, **Essentris**, was deployed at all 59 Department of Defense inpatient treatment facilities worldwide (5,500+ beds, 24,000+ physicians, serving 9.6 million beneficiaries) starting in 2011. The DoD is transitioning to MHS Genesis (Cerner/Oracle-based), and a $429M contract was awarded in 2020 to support maintenance and eventual decommissioning of Essentris through September 2026. Meanwhile, the VA continues to expand CliniComp deployments — recent expansions include VA Hampton Health Care System (Med-Surg, August 2025) and VA San Antonio (Post Anesthesia Care Unit, June 2025). CliniComp also serves private/community hospitals and academic health systems, though its customer base appears heavily weighted toward government facilities.

The company has won multiple industry awards including the MedTech Breakthrough Award for "EHR Innovation" (two consecutive years) and recognition as a San Diego Union-Tribune Top Workplace.

## Product: CliniComp|EHR

CHPL ID: 10998

### What It Is

CliniComp|EHR is the company's current-generation, web-based, integrated EHR platform. It is the successor to the legacy **Essentris** product line (which included Essentris Acute Care, Essentris ED, Mobile Essentris, etc.). The certified product number (15.05.05.2695.CLIN.02.01.1.221013) was certified October 13, 2022, under version 213.03.

This is a **comprehensive, enterprise-wide inpatient EHR** that also extends to ambulatory, ancillary, and revenue cycle management. It is not a specialty or ambulatory-only product — it is a full hospital information system. The certified module appears to be the whole product, encompassing clinical, ancillary, and RCM functionality delivered as a unified platform.

CliniComp delivers the product as a **System as a Service (SYaaS)** — a bundled model that wraps software, hardware, and all services (implementation, training, support, maintenance, upgrades) into a single contract with transparent pricing based on bed count.

The certification is broad: clinical criteria (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); transitions of care (b)(1)–(b)(2); clinical information exchange (b)(7)–(b)(9); patient portal (e)(1), (e)(3); public health reporting (f)(1)–(f)(2); CQMs (c)(1)–(c)(4); FHIR APIs (g)(7), (g)(9)–(g)(10); and direct messaging (h)(1). This breadth confirms it is a full-featured hospital EHR.

### Users & Market

**Primary users:**
- Physicians, nurses, pharmacists, lab technicians, radiology staff, billing/coding specialists, PACU staff, perioperative teams, neonatal/perinatal specialists, ED clinicians, behavioral health staff
- Used in ICU, critical care, emergency departments, med-surg, operating rooms, PACU, labor & delivery, neonatal/pediatric units, ambulatory clinics, behavioral health settings, rehabilitation, and home health/hospice

**Key customer segments:**
- **Veterans Administration (VA)** medical centers — active and expanding deployments, including VISN 6 (53 sites, 584,000+ enrolled veterans across Virginia and North Carolina)
- **Department of Defense** — legacy Essentris at 59 military treatment facilities worldwide (transitioning to MHS Genesis)
- **Private/community hospitals and academic health systems** — CliniComp positions itself as a cost-effective alternative to large EHR vendors

**Scale:** The system handles "millions of patient records." Notable deployments include Landstuhl Army Regional Medical Center in Germany (the largest American military hospital outside the U.S.).

### Modules & Functionality

Based on vendor website, press releases, and third-party listings, CliniComp|EHR includes:

**Clinical Documentation & Charting:**
- Configurable flowsheets matching clinical workflows with data entry shortcuts
- Multidisciplinary charting across care environments (ICU, ED, med-surg, ambulatory)
- Clinical notation generation via intuitive dashboard
- Treatment planning and discharge summaries
- Comprehensive longitudinal patient record across multiple sites

**Computerized Provider Order Entry (CPOE):**
- Fully integrated order entry system
- Automated status updates as pharmacy, radiology, and lab results are processed
- Weight-based warnings and medication dosing calculations for pediatric/neonatal patients

**Medication Management:**
- Barcode Medication Administration (BCMA) on mobile devices
- Electronic verification of patients and medications
- Integration with pharmacy for drug dispensing and interaction checking

**Clinical Decision Support:**
- Configurable real-time alerts with color-coded dashboards
- Site-defined clinical limits with immediate caregiver notification
- Early Warning Dashboard for clinical surveillance
- Advanced Real-time Analytics with machine learning for pattern identification and at-risk patient detection

**Medical Device Integration:**
- Automated data capture from hundreds of bedside medical devices (monitors, ventilators, pumps, anesthesia equipment)
- Waveform, parameter, and settings capture directly into patient record
- Cardiac waveform viewing (Waves application)

**Pharmacy Information System:**
- Drug dispensing with automatic package selection and built-in rules
- Timed Flag Items for workload prioritization
- Electronic compounding records (sterile and non-sterile)
- Drug usage reporting and cost tracking
- After-hours operations support

**Laboratory Information System (LIS):**
- Lab order delivery with real-time results viewing
- Support for clinical chemistry, microbiology, molecular, and pathology results
- Specimen collection workflows
- Blood transfusion workflows
- Can function standalone or interfaced with legacy LIS

**Radiology (RIS) & Imaging (PACS):**
- Radiology Information System
- Picture Archive Communication System
- Can work with CliniComp RIS, legacy RIS, or third-party imaging services

**Perinatal/Neonatal:**
- Specialized documentation tools for neonates, infants, and children
- Specialized drug databases for accurate pediatric dosing
- Growth curves and plots
- Emergency drug sheets
- Fetal surveillance and maternal monitoring (mobile capable)

**Emergency Department:**
- ED-specific clinician documentation (previously marketed as Essentris ED)
- Integrated with the broader EHR for continuity

**Perioperative/PACU:**
- Unified patient record from pre-op through post-op recovery
- Integration across critical care, procedural areas, and post-anesthesia care

**Behavioral Health:**
- Listed as a supported clinical area on vendor website and third-party reviews
- Specific feature details are sparse on vendor website

**Revenue Cycle Management:**
- Patient access services: real-time eligibility verification, point-of-service collections, authorization filing, edit checking, coverage management
- Automated charge capture: charges drop as clinicians document, modified by payer-specific guidelines
- Medical coding: workflow application synchronized with third-party encoders, automated simple diagnostic coding
- Billing and claims: automated claims generation, payment applications, edit identification and routing
- Unified billing account view
- Robust KPI reporting from patient access through claims and payments
- Exception-based revenue cycle method for automation of routine processes

**Ambulatory:**
- Outpatient clinical documentation
- Listed as part of the integrated solution suite alongside inpatient and ancillary

**Interoperability & Data Exchange:**
- FHIR API support (g)(7), (g)(9), (g)(10)
- Direct messaging (h)(1)
- EMR Direct Data Exchange Protocol API v1.3.2
- Health Information Exchange (HIE) connectivity
- CCD/C-CDA document exchange for transitions of care

**Native AI:**
- Artificial intelligence embedded throughout the EHR, overlaying patient data and streamlining workflows (per vendor marketing — specifics are limited)

**Telehealth/Remote Access:**
- Remote access to complete patient records
- Mobile device support (PCs, tablets, smartphones)

**Reporting & Analytics:**
- Clinical Quality Measures (CQMs) compliance tracking
- Public health reporting (immunization, syndromic surveillance)
- Advanced real-time analytics with visualization tools
- Operational reporting (patient throughput, resource use, staffing needs)

### Data & Content

Based on the features and modules described above, CliniComp|EHR manages the following categories of data:

- **Patient demographics and registration data** — implied by patient access services, eligibility verification
- **Clinical documentation** — flowsheets, clinical notes, treatment plans, discharge summaries, multidisciplinary charting
- **Orders** — provider orders for medications, labs, radiology, and other services
- **Medication data** — medication lists, dispensing records, BCMA verification logs, compounding records, drug interaction alerts
- **Laboratory results** — clinical chemistry, microbiology, molecular, pathology; specimen tracking and blood bank/transfusion data
- **Radiology/imaging** — radiology orders, results, and images via integrated RIS/PACS
- **Vital signs and physiological data** — from bedside monitors, ventilators, pumps, anesthesia equipment; waveform data
- **Problem lists, allergy/intolerance lists** — certified for (a)(1)–(a)(5) criteria
- **Perinatal/neonatal data** — fetal monitoring strips, growth curves, specialized neonatal dosing records, maternal monitoring
- **Emergency department records** — ED-specific documentation
- **Perioperative/PACU records** — pre-op, intra-op, and post-op documentation
- **Behavioral health records** — listed as a supported area, though feature specifics are limited
- **Revenue cycle / billing data** — charges, claims, payments, eligibility records, authorizations, coding data
- **Clinical decision support alerts and notifications** — real-time alerts, early warning scores
- **Immunization records** — certified for (f)(1) immunization registry reporting
- **Syndromic surveillance data** — certified for (f)(2)
- **Care coordination documents** — CCD/C-CDA documents, transitions of care summaries
- **Audit trails** — certified for (d)(1)–(d)(13) security and access controls
- **Patient portal data** — certified for (e)(1) patient view/download/transmit; the website doesn't describe a specific patient portal brand, but the certification implies patient-facing data access

**Gaps/uncertainties:**
- The vendor website does not prominently describe **scheduling or appointment management** as a standalone module, though it's likely part of patient access services
- **Patient messaging** or a branded patient portal is not prominently described — the (e)(1) certification confirms patient-facing data access exists, but details are thin
- **Home health/hospice** is mentioned on the SoftwareFinder listing as a supported setting, but the vendor website doesn't elaborate on specific home health features
- **Rehabilitation** is similarly mentioned on third-party review sites but not detailed on the vendor site
- The **AI capabilities** are marketed but specifics about what data AI features generate or store are not described

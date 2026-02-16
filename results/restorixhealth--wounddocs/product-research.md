# Net Health (RestorixHealth) — Product Research

Researched: 2026-02-16
Developer website: https://www.nethealth.com/

## Overview

**Net Health Systems, Inc.** is a Pittsburgh, PA-based healthcare software company founded in 1993 that provides cloud-based EHR, EMR, and analytics solutions for **specialty healthcare providers** — specifically wound care, rehab therapy (PT/OT/SLP), occupational health, employee health, and urgent care. The company employs approximately 630 people and serves over 23,000 healthcare facilities. Net Health is privately held, backed by **The Carlyle Group**, **Level Equity**, and **Silversmith Capital Partners** (Carlyle/Level Equity acquired in 2017; Silversmith joined in 2020).

Key acquisitions include **Tissue Analytics** (May 2020, AI-powered wound imaging with FDA Breakthrough Designation), **Casamba** (March 2021, EMR for rehab therapy and home health/hospice), **Optima Healthcare Solutions** (contract therapy EMR), and **PointRight** (predictive analytics for value-based care). The wound care product line has been sold under multiple names: **WoundExpert** is the primary commercial brand, while **WoundDocs** is a white-labeled deployment used by RestorixHealth across their network of hospital wound centers. On the CHPL listing, the product appears as "WoundDocs" under the "Net Health" developer name.

**RestorixHealth** is a separate company — a wound care management organization founded in 1997, headquartered in White Plains, NY. They operate 260+ hospital wound centers across 39 states and use Net Health's WoundExpert platform branded as "WoundDocs" as their EMR. The WoundDocs login portal at `wounddocs.restorixhealth.com` has URL paths containing `/WoundExpert/`, confirming the underlying software is the same.

## Product: WoundDocs (WoundExpert)

CHPL ID: 10234

### What It Is

WoundExpert/WoundDocs is a **purpose-built, cloud-based specialty EHR designed exclusively for wound care management**. It is not a general-purpose EHR — it is a specialty clinical documentation system that integrates with hospital-wide EHR systems (Epic, Cerner, MEDITECH, etc.) via bidirectional interfaces. It functions as a **specialty overlay** that sits alongside a facility's primary EHR, exchanging data so wound care documentation flows into the patient's main medical record.

The product is delivered as SaaS, accessible via web browser. Net Health describes it as built on "the most comprehensive, proprietary wound care database in the world," covering more than 600,000 wounds. WoundExpert is reportedly used in approximately 90% of wound care market settings in the US (per vendor marketing).

The certified product (v7.0, certified December 2019 by Drummond Group) has broad ONC 2015 Edition certification covering clinical data ((a)(1)-(a)(5), (a)(12), (a)(14)), care transitions ((b)(1)-(b)(3)), EHI export ((b)(10)-(b)(11)), clinical quality measures ((c)(1)-(c)(3)), patient portal ((e)(1), (e)(3)), FHIR API ((g)(7)-(g)(10)), and direct messaging ((h)(1)). This is a comprehensive certification profile for a specialty system.

### Users & Market

**Target settings:**
- Hospital outpatient wound care centers (the primary market)
- Skilled nursing facilities (SNFs) and post-acute care
- Senior living and assisted living facilities
- Home health agencies providing wound care
- Private wound care practices
- Critical access hospitals (100+ CAH partners through RestorixHealth alone)

**End users:**
- Wound care physicians (dermatologists, vascular surgeons, podiatrists, plastic surgeons, general surgeons)
- Wound care nurse practitioners and physician assistants
- Wound care-certified nurses (WOCNs/CWCNs)
- Hyperbaric oxygen therapy (HBOT) technicians and providers
- Administrative and billing staff managing wound care claims

**Scale:** Net Health claims 25,000+ facilities across all products. WoundExpert specifically may serve around 3,000 facilities (an earlier reference), though the RestorixHealth partnership alone accounts for 260+ hospital wound centers. The product dominates the specialty wound care EHR niche.

**Notable customer:** RestorixHealth is a marquee customer, operating 260+ hospital wound centers in 39 states using the WoundDocs-branded version.

### Modules & Functionality

**Clinical Documentation and Wound Assessment** (per vendor product pages and review sites):
- Customizable clinical templates for wound documentation
- Wound assessment tools capturing wound size (length, width, depth/area/volume), tissue type (granulation, slough, eschar, epithelial), exudate characteristics, wound edges, periwound skin condition, wound bed description, pain assessment
- Visual wound progression tracking with photo documentation
- Treatment plan creation and management
- Progress notes and clinical impressions
- Evidence-based clinical practice guidelines integration
- Support for multiple wound types: diabetic ulcers, venous ulcers, arterial ulcers, pressure ulcers/injuries, surgical wounds, chronic wounds

**AI-Powered Wound Imaging (Tissue Analytics)** (per vendor blog and Dreamit Ventures blog):
- Mobile photo capture with automated wound measurement
- 3D wound imaging capabilities
- Machine learning for autonomous wound segmentation, classification, and measurement
- Less than 5% error rate (more accurate than manual ruler measurement per vendor)
- Standardized lighting/distance/angle calibration
- FDA Breakthrough Designation
- SMART on FHIR integration capability

**Scheduling and Practice Management** (per FindEMR, SoftwareFinder):
- Clinical scheduling and appointment management
- Appointment reminders
- Referral management
- Patient demographics management
- Inventory management

**Coding and Billing** (per FindEMR, SoftwareFinder, vendor website):
- Automatic coding (ICD-10, CPT)
- Claims management and insurance claim processing
- Billing and invoicing
- Payment tracking
- Revenue and expense reporting
- MIPS (Merit-based Incentive Payment System) reporting support (confirmed by vendor's 2025 MIPS configuration guide)

**Analytics and Benchmarking** (per vendor product pages):
- Real-time analysis, visualization, and benchmarking tools
- Predictive analytics for workflow efficiency and clinical outcomes
- Facility-to-facility performance comparison
- Population-level wound care analytics from the national wound treatment database

**Patient Engagement** (per FHIR API page, certification criteria):
- Patient portal for health information access (certified for (e)(1) VDT)
- Patient education materials
- Third-party app connectivity via Certified FHIR API

**Interoperability** (per Health IT Outcomes article on top seven interfaces):
- Eight interface categories: ADT (Admission/Discharge/Transfer), Billing, C-CDA, Clinical Documentation, Ordered Results, Scheduling, Transcription, Unsolicited Results
- Top seven EHR integration partners: **Cerner, Epic, Healthcare Management Systems (HMS), McKesson Horizon Patient Folder, McKesson Star, MEDITECH, Siemens Soarian Clinicals**
- Additional integrations: Athenahealth, Allscripts, Netsmart, PointClickCare, MedBridge
- HL7 and FHIR R4 APIs (Certified API, US Core IG, USCDI v3)

### Data & Content

Based on documented features, certified criteria, and third-party descriptions, WoundExpert/WoundDocs stores:

- **Patient demographics** — name, DOB, address, insurance, contact information (from ADT interface and patient registration)
- **Wound assessment data** — wound location, measurements (L/W/D/area/volume), tissue type percentages, exudate characteristics, wound edges, periwound skin condition, wound bed description, pain scores, healing trajectory. This is the core data of the product and is highly structured and detailed.
- **Wound images** — clinical photographs with automated AI-based measurements, 3D imaging data (via Tissue Analytics integration)
- **Treatment plans** — dressing selections, debridement methods, wound care interventions, wound care orders
- **Progress notes** — visit documentation, clinical impressions, healing progress narratives
- **Medications** — wound care-related medications (certified for (a)(1) CPOE medications)
- **Diagnoses** — wound-related ICD-10 codes, comorbidities (certified for (a)(4) drug-drug/drug-allergy)
- **Procedures** — wound care procedures: debridement, skin grafts, negative pressure wound therapy (NPWT), hyperbaric oxygen therapy (HBOT) sessions, other interventions
- **Lab/diagnostic results** — wound cultures, blood work related to healing (per "Ordered Results" and "Unsolicited Results" interface types)
- **Scheduling data** — appointments, follow-up schedules, recall lists
- **Billing/claims data** — CPT codes, charges, claims, payments, denials, revenue reporting
- **C-CDA documents** — clinical summaries for care transitions (certified for (b)(1)-(b)(3))
- **Allergies** — medication allergies (certified for (a)(4) drug-allergy checking)
- **Audit trails** — clinical documentation audit events
- **Quality measure data** — CQM/MIPS reporting data (certified for (c)(1)-(c)(3))
- **Direct messaging data** — secure clinical messaging (certified for (h)(1))

**What's unclear:** The vendor website and reviews don't clearly describe whether WoundExpert stores comprehensive problem lists or medical histories beyond wound-related diagnoses, or whether it handles e-prescribing independently (as opposed to through the host EHR). Given its role as a specialty overlay system, some clinical data domains (e.g., full medication management, comprehensive problem lists) may be managed primarily in the host EHR with limited wound-relevant data in WoundExpert.

### User Reviews

**SoftwareFinder:** 4.5/5 stars (4 reviews). **Strengths:** flexible cloud access, intuitive wound documentation design, strong imaging tools, good cross-facility synchronization for benchmarking. **Weaknesses:** performance issues with large data volumes (75% negative feedback on stability), intermittent save failures and system timeouts, complex EHR integration process, limited customization and advanced reporting, onboarding challenges. Capterra and Software Advice listings exist but were not accessible (403 errors). No KLAS rating was found — the product may be too niche for standard KLAS categories.

# Vohra Wound Physicians Management, LLC — Product Research

Researched: 2026-02-16
Developer website: https://vohrawoundcare.com (redirects from https://www.vohraphysicians.com)

## Overview

Vohra Wound Physicians is the largest physician-led wound care specialty practice in the United States, focused exclusively on post-acute wound care. Founded in 2000 by Dr. Ameet Vohra, the company is headquartered in Miramar, FL. Vohra employs approximately 300+ wound care physicians and ~380 total staff across 3 continents (North America, Asia, Europe), serving nearly 3,000 skilled nursing facilities across 28-30 states. The company reports 1.4 million annual patient visits and over 6 million wound cases in its historical database. Revenue is estimated at $50-100M annually.

Vohra is not a typical EHR vendor. It is primarily a **wound care physician services company** that developed a proprietary EMR internally to support its own physicians' clinical workflows. The EMR is purpose-built for wound care documentation and coding, used by Vohra's employed physicians when they visit post-acute care facilities (skilled nursing facilities, assisted living centers, long-term acute care hospitals) to provide specialist wound care services. The EMR is not sold as a standalone product to external customers — it is an internal tool supporting Vohra's service delivery model.

In December 2016, Trivest Growth Investment Fund (TGIF) made a platform investment in Vohra. The company has raised approximately $350M in total funding. Vohra also operates wound care certification/education programs (training 9,000+ nurses) and has a "Center of Excellence" designation program for partner facilities. Notably, the DOJ filed a False Claims Act complaint against Vohra in 2025, raising questions about documentation practices and EMR design related to billing compliance.

## Product: VHS Medical Documentation & Coding

CHPL IDs: 9887

### What It Is

VHS Medical Documentation & Coding is Vohra's proprietary, ONC-certified electronic health records system, designed specifically for wound care physicians practicing in post-acute care settings. The certified module (v3.5, certified 2018-12-21) is the core clinical documentation system used by Vohra's physicians when they visit skilled nursing facilities, assisted living centers, and similar post-acute settings to provide bedside wound care.

This is **not a general-purpose EHR** — it is a specialty wound care documentation and coding system built by wound care physicians for wound care physicians. The system is the technology backbone of Vohra's service delivery model. It was designed to be used at the bedside with online-offline capability (important since many post-acute facilities have unreliable internet). The certified criteria cover a moderate set of clinical functions: CPOE for medications (a)(2), demographics (a)(3), vital signs recording (a)(12), implantable device list (a)(14), family health history (a)(3), and clinical decision support (a)(5), along with transitions of care (b)(1), patient portal (e)(1), clinical quality measures (c)(1), and FHIR API access (g)(7), (g)(10).

### Users & Market

**Primary users**: Vohra's own employed wound care physicians (~300+), who use the system during bedside visits at partner skilled nursing facilities. The system is also accessible to the broader care team through the Facility Portal (for facility staff to access clinician notes, patient history, and wound care outcomes) and a Patient Portal (for patients to access wound care documents and telemedicine).

**Clinical setting**: Exclusively post-acute care — skilled nursing facilities, assisted living facilities, long-term acute care hospitals, rehabilitation centers, and increasingly home health via telemedicine. Vohra physicians typically visit facilities 1-2 times per week.

**Scale**: ~3,000 partner facilities across 28-30 states, 1.4 million annual patient visits, 300+ physicians. This is an internal-use system, not sold to external customers.

**Notable context**: Vohra is the largest wound care physician group serving the post-acute sector in the US. The EMR is integral to their value proposition — they emphasize that physicians spend "minutes per patient" on documentation and don't have to finish notes at home.

### Modules & Functionality

Based on vendor materials, the VHS Medical Documentation & Coding system includes:

**Clinical Documentation & Wound Care Workflows**:
- Wound assessment and documentation (etiology identification, staging, wound measurements)
- Treatment planning and care coordination
- Procedure documentation (surgical debridement, Doppler studies with ABI, PEG tube replacement, ultrasound mist therapy, skin substitute grafts, negative pressure therapy)
- MDS-compliant wound documentation (Minimum Data Set, required for Medicare in SNFs)
- Clinical Decision Support (CDS) that reminds physicians of relevant patient factors during treatment
- Vital signs recording
- Problem list management
- Medication list / CPOE
- Implantable device list
- Family health history

**AI/Machine Learning Features**:
- Predictive wound healing timelines based on 6M wound case database
- Outcomes-based dressing recommendations
- Treatment recommendations via mobile app
- Wound progress trajectory estimation

**Coding & Billing Support**:
- Integrated coding assistance — the system is structured to ensure physicians don't miss physical exam findings or necessary wording for appropriate billing
- The product name itself includes "Coding," indicating this is a core function
- Medicare and Medicaid compliant documentation

**Interoperability & Integration**:
- Integration with PointClickCare (standard SNF EHR platform)
- Integration with MatrixCare
- Integration with AHT, Swift, and other post-acute care EHR systems
- Transitions of care summaries (C-CDA)
- FHIR API (g)(7), (g)(10)

**Portals**:
- **Facility Portal** (facilityportal.vohrawoundteam.com): Allows partner facilities to securely download clinician notes, patient history, and wound care improvement/outcomes data
- **Patient Portal** (patient.vohrawoundteam.com): Patients can access wound care documents, manage their records, and connect via telemedicine
- **Telemedicine**: Virtual consultations for home health patients

**Offline Capability**:
- Online-offline functionality for facilities with unreliable internet access

**Outcomes & Analytics**:
- Wound outcomes reporting per patient
- Facility-level wound care improvement metrics
- Re-hospitalization rate tracking
- Healing timeline tracking
- Medicare cost savings analysis

### Data & Content

Based on vendor materials, reviews, and feature descriptions, the VHS system stores:

**Clinical wound care data**: Wound assessments (etiology, staging, measurements), wound photographs (implied by DOJ complaint discussing "photos" as documentation evidence, though not explicitly described on marketing pages), treatment plans, dressing orders and recommendations, debridement records, Doppler/ABI study results, procedure documentation for advanced wound therapies.

**Patient demographics and clinical data**: Patient demographics (certified for (a)(5)), vital signs (certified for (a)(12)), medication lists and CPOE (certified for (a)(2) — limited to medications), problem lists, implantable device lists (certified for (a)(14)), family health history (certified for (a)(3)).

**Coding and billing data**: The product name is "Medical Documentation & Coding," and physicians note that the system "assists with billing, coding and documentation" and ensures proper wording for billing. This strongly implies the system stores diagnosis codes, procedure codes, and billing-relevant documentation. A separate billing department handles patient payments (phone: 866-320-3764), but the EMR captures the coding layer.

**MDS-compliant documentation**: MDS (Minimum Data Set) is required for SNF Medicare reimbursement — the system produces MDS-compliant wound documentation.

**Transitions of care**: C-CDA documents for care transitions (certified for (b)(1)).

**Clinical quality measures**: CQM data including BMI screening, tobacco use screening, medication documentation, diabetes management, vaccination status (certified for (c)(1)).

**Outcomes and analytics data**: Healing timelines, re-hospitalization rates, dressing change frequency, nursing time metrics, Medicare cost savings data per patient and per facility.

**AI/ML training data**: 6 million historical wound cases powering predictive algorithms.

**Portal content**: Clinician notes available to facilities, patient-facing documents available through patient portal.

**What's unclear or not mentioned**:
- Whether wound photographs/images are stored directly in the EMR (likely, given wound care specialty, but marketing materials don't explicitly describe photo capture)
- Whether the system stores patient scheduling data (Vohra physicians visit facilities on schedules, but it's unclear if the EMR manages scheduling vs. a separate system)
- Whether referral/order data from primary care physicians is stored in the system (Vohra physicians are consulted by SNF primary care doctors)
- The extent of allergy data storage (not explicitly mentioned, though clinical decision support is certified)
- Whether the system stores supply chain/dressing inventory data (the system triggers "automatic supply delivery" from dressing recommendations, suggesting integration with a supply ordering system)

---

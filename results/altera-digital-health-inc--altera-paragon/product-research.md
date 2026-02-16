# Altera Digital Health — Product Research (Paragon)

Researched: 2026-02-16
Developer website: https://www.alterahealth.com

## Overview

Altera Digital Health is a healthcare IT company formed in May 2022 when N. Harris Computer Corporation (part of Constellation Software Inc.) acquired Allscripts' Hospitals and Large Physician Practices business segment for approximately $700 million. The acquired products — including Sunrise, Paragon, TouchWorks EHR, dbMotion, and others — were rebranded under the Altera Digital Health name. The remaining ambulatory-focused Allscripts segment became Veradigm and operates independently.

Altera primarily serves hospitals and health systems, with Paragon specifically targeting community, rural, and critical access hospitals. Altera holds approximately 3.7% of the U.S. hospital EHR market by number of hospitals and 4.1% by hospital beds (per Healthgrades/KLAS data), placing it behind Epic, Oracle Cerner, MEDITECH, and CPSI but ahead of Medhost. The company operates under Harris's "buy and hold forever" philosophy, emphasizing long-term product investment and stability.

**Note on CHPL metadata:** The CHPL listing shows the developer as "Providers Management, Inc." (Burton, MI) with a contact email at genesyspho.com. This appears to be a client organization or reseller, not the actual software developer. The products themselves (Paragon® Denali and Paragon® EHR) are developed by Altera Digital Health Inc. The mandatory disclosures URL (integratedproviders.com) describes a different product ("Integrated Providers Patient Portal") that requires Altera TouchWorks EHR — further confirming this is a client site, not the Paragon developer.

## Product: Paragon (including Paragon® EHR and Paragon® Denali)

CHPL IDs: 11589 (Paragon® Denali, version 1), 11761 (Paragon® EHR, version 25)

### What It Is

Paragon is a comprehensive, integrated hospital EHR platform that combines clinical, financial, revenue cycle, and ancillary departmental functionality in a single system with a unified database. Both CHPL listings share identical certified criteria (38 criteria spanning clinical, transitions of care, patient portal, public health reporting, and FHIR APIs), indicating they are the same product platform at different deployment stages:

- **Paragon® EHR (version 25):** The traditional on-premises / private cloud deployment, with a long track record (25+ year relationships cited by some customers like Ridgecrest Regional Hospital).
- **Paragon® Denali (version 1):** The cloud-native, SaaS-based re-architecture of Paragon, built on Microsoft Azure with containerized services. Generally available since late 2024. Functionally equivalent to Paragon EHR but with modernized infrastructure (updates in minutes rather than hours, reduced hardware footprint, subscription pricing).

Both versions offer the same core functionality; Denali represents a deployment and architecture evolution, not a different product.

### Users & Market

**Target market:** Community hospitals, rural hospitals, critical access hospitals, and small health systems — organizations that need a comprehensive EHR but lack the IT resources and budget for Epic or Oracle Cerner.

**End users:** Physicians, nurses, pharmacists, lab technicians, radiology staff, billing/revenue cycle staff, hospital administrators, and patients (via CarePath portal).

**Notable customers/deployments (from press releases):**
- Ridgecrest Regional Hospital — 25+ year Paragon customer
- Holzer Health System (Gallipolis, OH)
- Columbus Community Hospital (50 beds, Columbus, NE)
- Pipeline Health System (4 facilities, Los Angeles County, CA)
- Sioux Falls Specialty Hospital (SD)
- West Calcasieu Cameron Hospital (107 beds, LA)

**Go-to-market:** Direct sales to hospitals. Positioned as an alternative to large-vendor consolidation, emphasizing that hospitals can "maintain independence" and "own the system and decisions."

### Modules & Functionality

Based on vendor website product pages and press releases, Paragon includes the following integrated modules:

**Clinical:**
- Unified clinical documentation and patient records across care settings (source: alterahealth.com/solution/paragondenali-clinical/)
- CPOE (Computerized Physician Order Entry) — implied by (a)(1) certification for CPOE
- Clinical Decision Support — certified for (a)(2), (a)(3), (a)(4)
- Demographics recording — certified for (a)(5)
- Problem list, medication list, medication allergy list management — certified for (a)(1)
- Emergency Department management with coded, discrete clinical data capture (source: web search results citing vendor materials)
- Operating Room management with perioperative charting, scheduling, supply management, and charge capture (source: web search results)
- Mobile access for clinicians (source: vendor website)
- Ambient listening/AI documentation via Nabla integration — transcribes patient interactions into clinical notes (source: alterahealth.com press release on Nabla partnership)

**Ambulatory/Outpatient:**
- Integrated ambulatory care module supporting outpatient clinics and physician practices within hospital systems (source: vendor all-solutions page)
- Multi-specialty support (source: web search results)

**Ancillary Services (source: alterahealth.com/solution/paragondenali-ancillary/):**
- **Pharmacy Management:** Medication management with allergy/drug interaction alerts, integrated with clinical and financial modules
- **Radiology Management:** Procedure management, film and patient tracking (barcode or manual), department-specific workflow and reporting
- **Laboratory Management:** Order processing, specimen handling, result reporting, auto-verification, delta checking across encounters (inpatient and outpatient), statistical analysis, quality management tools

**Revenue Cycle & Financial (source: alterahealth.com/solution/paragondenali-financial/):**
- Patient registration (including downtime registration capability)
- Patient accounting, billing, collections
- Claims management with PreBill claim editing for clean-claim rates
- Automated work queues for collections
- Resource scheduling
- Customizable financial reporting
- Real-time integration with clinical modules for unified patient record

**Enterprise Resource Planning (ERP) (source: alterahealth.com/all-solutions/):**
- Altera Fiscal Management
- Altera Supply Chain Solutions
- Altera Human Capital Management
- (It's unclear whether ERP modules are bundled with Paragon or sold separately as part of the broader Altera portfolio)

**Patient Portal:**
- **CarePath** (paragoncarepath.com) — ONC-compliant patient portal providing 24/7 access to health information, clinical summaries, lab results, and provider communication. Certified for (e)(1) patient access.

**Interoperability & Data Exchange:**
- Certified for FHIR API access — (g)(7) through (g)(10)
- Transitions of care — (b)(1), (b)(2), (b)(3)
- Public health reporting — immunization (f)(1), syndromic surveillance (f)(2), electronic case reporting (f)(3), electronic reportable lab results (f)(5), transmission to cancer registries (f)(6)
- Direct messaging support for care transitions
- (h)(1) — direct project, applicability statement for transport

**Analytics (from broader Altera portfolio):**
- Altera Practice Analytics — chronic disease dashboards, provider performance visibility, gap-in-care identification. It's unclear whether this is bundled with Paragon or a separate product.

### Data & Content

Based on the modules and certifications described above, Paragon stores/manages:

- **Clinical data:** Patient demographics, problem lists, medication lists, medication allergy lists, clinical notes/documentation (including AI-transcribed ambient notes), vital signs, assessments, care plans, clinical orders (CPOE), clinical decision support alerts/interventions
- **Lab data:** Orders, specimens, results (with auto-verification and delta checking), quality management data
- **Radiology data:** Procedure records, film tracking, patient tracking within department
- **Pharmacy data:** Medication orders, dispensing records, drug interaction/allergy alerts
- **Surgical/OR data:** Perioperative charting, OR scheduling, supply usage, charge capture
- **Emergency department data:** Visit records, coded clinical data
- **Revenue cycle/financial data:** Patient registration records, billing/accounting, claims (pre- and post-submission), collections work queues, scheduling data, insurance information
- **Patient portal data:** Patient-facing health records, clinical summaries, lab results, patient-provider messages (via CarePath)
- **Public health reporting data:** Immunization records, syndromic surveillance data, case reports, reportable lab results, cancer registry submissions
- **Transitions of care:** C-CDA documents (continuity of care documents), referral/transfer records
- **ERP data (if bundled):** Financial management, supply chain, human capital management records

**Gaps/uncertainties:**
- The vendor website doesn't clearly describe **imaging/PACS** — radiology management focuses on procedure workflow and film tracking, not image storage. PACS may be a separate integrated system.
- **Behavioral health** capabilities are not specifically mentioned in vendor materials.
- Whether the **ERP modules** (fiscal management, supply chain, human capital management) are part of the certified Paragon product or separate products is unclear from the website.
- **Analytics** (Practice Analytics) appears to be a separate Altera product rather than built into Paragon.
- The website does not specifically mention **patient messaging** within the EHR itself (distinct from CarePath portal messaging), though this may exist.

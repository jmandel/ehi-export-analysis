# ezCaretech Co., Ltd. — Product Research

Researched: 2026-02-14
Developer website: http://www.ezcaretech.com/

## Overview

ezCaretech Co., Ltd. is a publicly traded South Korean healthcare IT company (KOSDAQ: 099750) founded in February 2001 as a spinoff from Seoul National University Hospital's IT department. The company specializes in hospital information systems (HIS) and electronic health records, positioning itself as "Your IT Partner for the Digital Hospital." With approximately 500 engineers, ezCaretech is Korea's largest EHR vendor, claiming 70%+ market share in Korean tertiary hospitals — supplying 8 of 12 national university hospitals and over 50 large hospital systems domestically.

Internationally, ezCaretech has made significant inroads, particularly in Saudi Arabia (a $70M MNGHA contract covering 6 hospitals and 70 clinics, deployed through a joint venture called SKHIC) and the United States (a $17.7M contract with Aurora Behavioral Healthcare covering 14–16 psychiatric hospitals). The company also operates in Japan (contract with St. Marianna University Hospital, 2021) and has a US subsidiary, ezCaretech USA, Inc. in Torrance, California (est. 2019). KLAS Research ranked ezCaretech 5th globally among non-US EMR vendors (May 2021), with KLAS scores of 87.8 (South Korea, 2022) and 82.8 (Middle East/Africa, 2021) in Acute Care EMR categories.

The system's origins at Seoul National University Bundang Hospital (SNUBH) are significant: BESTCare ("Bundang hospital Electronic System for Total Care") was co-developed with SNUBH over a 22-month period. In 2010, SNUBH became the first hospital outside North America to achieve HIMSS EMRAM Stage 7 using BESTCare. BESTCare was also the first non-North American software to achieve ONC-HIT certification (2015 Edition, subsequently 2015 Cures Edition).

## Product: BESTCare

CHPL IDs: 9665

### What It Is

BESTCare is a comprehensive, fully integrated hospital information system (HIS) designed for large hospitals, from general hospitals to university tertiary centers. The CHPL SED intended user description explicitly states "University Tertiary Hospital." The certified module (BESTCare 2.0B, certified April 2018) is part of a broader HIS platform that covers clinical, administrative, and operational functions across the entire hospital.

The product has broad ONC certification spanning 33 criteria: clinical data (a)(1)–(a)(5), (a)(12), (a)(14); transitions of care (b)(1)–(b)(2); EHI export (b)(10)–(b)(11); clinical quality measures (c)(1)–(c)(3); security/privacy (d)(1)–(d)(13); public health reporting (f)(1)–(f)(3), (f)(5)–(f)(7); and API/FHIR access (g)(2)–(g)(10). This is one of the most comprehensive certifications possible, consistent with a full hospital EHR.

ezCaretech also offers two variant products built on the same technology:
- **Behavioral Specialized EHR**: Tailored for psychiatric/behavioral health facilities, with psychiatry-specific workflows and customizable forms. This is the version deployed at Aurora Behavioral Healthcare's 14 US psychiatric hospitals.
- **BESTCare Cloud**: A SaaS/cloud-based version launched in March 2020 with SOA/MSA web architecture, aimed at facilities wanting to avoid on-premise installations.

### Users & Market

**Primary users**: Physicians, nurses, pharmacists, radiology technicians, administrative/billing staff, and hospital management at large hospitals and university medical centers.

**Market focus**: The system is built for inpatient hospital environments — tertiary/university hospitals in Korea, large general hospitals in the Middle East, and psychiatric hospitals in the US. It is not an ambulatory/office-based EHR.

**Notable deployments**:
- **Seoul National University Bundang Hospital (SNUBH)** — flagship site, HIMSS Stage 7
- **King Abdulaziz Medical City (KAMC), Saudi Arabia** — also achieved HIMSS Stage 7 with BESTCare
- **MNGHA hospitals, Saudi Arabia** — 6 hospitals and 70 clinics
- **Royal Commission Hospital, Jubail, Saudi Arabia** — $5M contract
- **Aurora Behavioral Healthcare, USA** — 14 psychiatric hospitals (launched at Charter Oak Hospital CA in 2017, Reno Psychiatric Hospital NV in 2018, Vista Del Mar Hospital CA in 2018, and Glendale AZ)
- **St. Marianna University Hospital, Japan** — first Korean HIS export to Japan (2021)

**Customer count**: Over 60 HIS implementations globally (per vendor claims). Domestically, over 50% of all Korean tertiary hospitals.

### Modules & Functionality

BESTCare is a comprehensive HIS with the following explicitly described modules (per vendor materials, the PMC-published SNUBH case study, and product pages):

**Clinical Modules**:
- **EMR / Electronic Medical Records** — 100% electronic documentation, template-based (1,989 common templates and 1,269 departmental templates at SNUBH as of 2011), chronological patient history views, dual-monitor interface
- **CPOE / Computerized Physician Order Entry** — full electronic ordering for medications, labs, imaging, and procedures
- **Clinical Decision Support System (CDSS)** — drug interaction alerts, dosage alerts, allergy checking, age/pregnancy/renal dosing contraindications, clinical pathway guidelines (104 pathways across 11 departments at SNUBH)
- **Closed-Loop Medication Administration (CLMA)** — barcode and RFID-based "five rights" verification at bedside, PDA scanning, real-time EMR documentation of administration
- **Nursing Module** — medication cautions, dosage calculators, nursing documentation
- **Pharmacy Module** — automatic tablet counters, medication dispensing, drug interaction checking (integrates Medi-Span and Lexicomp from Wolters Kluwer)
- **Radiology Module** — imaging order management and results
- **Special Clinical Examination** — specialty exam ordering and documentation
- **Clinical Pathways** — standardized care pathways with variance tracking

**Administrative/Operational Modules**:
- **Billing** — financial systems, patient billing
- **Patient Service** — registration, scheduling, patient-facing workflows
- **Inpatient Services** — bed management, inpatient workflows
- **Social Services** — social work documentation and tracking
- **Customer Relationship Management (CRM)** — patient relationship tracking
- **Activity-Based Costing (ABC)** — financial analysis
- **Integrated Management System (IMS)** — hospital administration

**Data & Analytics**:
- **Clinical Data Warehouse (CDW)** — daily extraction of patient, medical, nursing, order, and financial data; 290 clinical indicators tracked; OLAP for ad-hoc queries
- **Clinical and Business Intelligence Indicators** — performance metrics and reporting

**Infrastructure/Integration**:
- **Health Information Exchange (HIE)** — interoperability with external clinics (36 private clinics at SNUBH); HL7 V2.X and HL7 CDA support
- **NLM AccessGUDI API** integration (per ONC disclosures)
- **FHIR API** — (g)(7)–(g)(10) certified
- **Disaster Recovery** — real-time database backup

**Behavioral Health variant adds**: psychiatry-specific workflows, customizable behavioral health documentation forms, inpatient psychiatric and hospital-based outpatient program support.

### Data & Content

Based on the described modules and vendor evidence, BESTCare manages a very wide range of clinical and operational data:

**Clinical data** (strongly evidenced by modules + ONC certification):
- Patient demographics and registration data
- Clinical documentation / physician notes (template-based, 3,000+ templates)
- Orders — medication, lab, imaging, procedure orders (CPOE)
- Medication records — prescriptions, dispensing, administration records (closed-loop)
- Lab results
- Radiology/imaging orders and results
- Allergy and drug interaction data
- Clinical decision support alerts and responses
- Clinical pathway data with variance tracking
- Nursing assessments and documentation
- Vital signs and clinical observations
- Immunization data (certified for (f)(1) immunization registry reporting)
- Syndromic surveillance data (certified for (f)(2))
- Electronic case reporting data (certified for (f)(3))
- Cancer registry data (certified for (f)(5))
- Electronic prescribing (certified for (f)(7))
- Transitions of care documents / CCDs (certified for (b)(1)–(b)(2))

**Administrative/operational data** (evidenced by module descriptions):
- Billing and financial records
- Patient service/scheduling data
- Inpatient census/bed management data
- Social services records
- CRM / patient relationship data
- Activity-based costing / financial analytics

**Analytics data** (evidenced by CDW module):
- Clinical data warehouse extracts (patient, medical, nursing, order, financial)
- 290 clinical quality indicators
- OLAP analytical datasets

**Integration data**:
- HIE exchange records (HL7 V2.X, CDA)
- FHIR API data (US Core resources)
- Blood transfusion and sample tracking data (RFID-based)
- Asset and logistics management data

**What's less clear**: The vendor website and available materials do not provide detailed information about whether the US-deployed version (particularly the behavioral health variant at Aurora hospitals) includes all modules from the full Korean tertiary hospital version. The ONC certification covers the broader BESTCare product, but the behavioral health deployments may have a different functional footprint. Patient portal / patient-facing capabilities are not prominently described in available materials, though the system is certified for (e)(1) patient access — this criterion was not in the CHPL metadata but the mandatory disclosures page references it. Electronic consent (iPad/PC signature pads) is documented at SNUBH.

---

## Research Notes

- **Primary market is Korean and Middle Eastern hospitals** — US presence is relatively small, focused on behavioral health
- **The product was co-developed with SNUBH** — academic medical center origins influence the system's comprehensiveness
- **The behavioral health EHR is a variant/configuration** of BESTCare, not a separate product, tailored for psychiatric facilities
- **The vendor's English-language web presence is moderate** — the Korean site likely has more detail, but the English product pages, the PMC case study, and the ONC disclosures provide solid information
- **Some bestcare.ezcaretech.com pages had SSL certificate issues** at research time, limiting access to detailed product pages

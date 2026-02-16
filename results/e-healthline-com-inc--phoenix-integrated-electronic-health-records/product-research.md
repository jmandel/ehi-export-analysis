# E*HealthLine.com, Inc. — Product Research

Researched: 2026-02-16
Developer website: http://ehealthline.com/

## Overview

E*HealthLine.com, Inc. (EHL) is a privately held health IT company headquartered in Sacramento, California, founded in 1999. The company describes itself as "a leader in Integrated Health Care Information Management software and services and the largest independent vendor in the healthcare solutions market offering fully ONC–ACB Certified software." As of a 2014 HCI Innovation Group Top 100 Vendors profile, the company had approximately 245 employees and reported $151 million in revenue (60% software, 40% services), placing it at #51 on that list. The company's executive at the time was Peter Wong.

EHL markets a very broad portfolio of healthcare IT products spanning hospital information systems, physician practice management, managed care/health plan administration, pharmacy, laboratory, radiology, health information exchange, analytics, telehealth, and patient engagement. Their products are delivered via their "iMed Cloud" platform and marketed globally — the company website includes a country selector listing 50+ nations. The company serves hospitals, physician practices, health plans, pharmacies, and manufacturers.

However, there is limited independent validation of the company's market claims. E*HealthLine does not appear on major third-party review platforms (G2, Capterra, Software Advice), and web searches for customer case studies, user reviews, or independent press coverage yield very few results beyond the vendor's own website and the 2014 HCI Innovation Group profile. The vendor website itself shows signs of poor maintenance (several pages contain injected spam content). This raises questions about the actual scale and active customer base, though the ONC certification is active.

## Product: Phoenix© Integrated Electronic Health Records

CHPL IDs: 10832

### What It Is

Phoenix© Integrated Electronic Health Records is an ambulatory EHR system designed for physician practices. It is ONC-ACB certified (version 10.0.0, certified 2022-02-17) with a broad certification footprint covering clinical data management (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15), transitions of care (b)(1)–(b)(3), patient portal (e)(1), (e)(3), public health reporting (f)(1)–(f)(7), API/FHIR access (g)(7), (g)(9)–(g)(10), and direct messaging (h)(1). The intended users are described as "Healthcare Providers."

Phoenix© appears to be part of a broader "Physician Practices Solutions" suite within E*HealthLine's product portfolio. The certified module is the EHR component, but the full product ecosystem for physician practices includes several companion products (described below).

### Users & Market

The product targets physician practices and clinical staff. Based on the vendor's website and CHPL metadata, the intended users are healthcare providers in ambulatory settings. The vendor also offers oncology-specific and behavioral health variants of the Phoenix platform, suggesting multi-specialty use.

No specific customer counts, notable deployments, or case studies were found for Phoenix© during this research. The vendor does not appear on major EHR review sites. The company's overall revenue ($151M as of 2013–2014) and employee count (245) suggest a mid-size vendor, but it is unclear how much of this relates to the Phoenix ambulatory product vs. the broader product portfolio (hospital systems, managed care, clearinghouse, etc.).

### Modules & Functionality

Based on the vendor's website product pages:

**Phoenix© EHR (the certified module):**
- Real-time clinical documentation with pre-built and customizable templates
- Patient flow management throughout the enterprise
- Clinical decision support for quality measures and disease management
- The broad certification criteria imply support for: CPOE, demographics, problem lists, medication lists, medication allergy lists, clinical decision support, drug-drug/drug-allergy checks, implantable device lists, social/psychological/behavioral data, family health history

**Phoenix© Integrated Practice Management System** (companion product):
- Described as providing "clinical, financial, operational, and corporate management" for physician enterprises
- Specific features (scheduling, registration, claims) are not detailed on the website — only high-level descriptions

**eBilling© Integrated Billing and Revenue Management:**
- Integrated payments and accounts receivable
- Patient liability management
- Claims editing
- Summary and detail account histories
- EDI services for electronic data transfer
- Described as serving both hospital and physician practice contexts

**E*Prescription Integrated Prescription Management:**
- Electronic prescribing to patient's pharmacy of choice
- Drug-drug interaction checking
- Duplicate medication detection
- Drug allergy verification
- Formulary status checking against patient's health plan
- The website does not mention specific integrations (Surescripts, PDMP) but e-prescribing certification implies these

**Patient Portal© Integrated Personalized Connected Health:**
- Electronic access to personal health records (PHR)
- Patient-provider messaging
- Appointment scheduling
- Email notifications and reminders
- File sharing
- Health library for patient education
- Integration with video conferencing and data repositories
- Certified for (e)(1) view/download/transmit and (e)(3) patient health information capture

**Oncology variant** (Phoenix© Integrated Oncology EHR):
- Oncology-specific EHR for practice and hospital-based oncology
- Interfaces with hospital patient registration and ancillary systems
- Oncology-specific templates and workflows
- Quality measures and disease management tools

**Behavioral Health variant:**
- Listed on the product pages but the specific product page returned 404; details unavailable

**Other related products in the physician practice suite:**
- Laboratory information system (eLab©)
- Radiology information system (eRad®, PACS®)
- Clearinghouse with EDI transactions, EClaims©, EScan© for claims processing

### Data & Content

Based on the certified criteria and vendor feature descriptions, Phoenix© and its companion products manage:

**Clinical data** (implied by certification criteria):
- Patient demographics (a)(5)
- Problem lists (a)(6) — not listed in criteria, but (a)(1) CPOE and (a)(2)–(a)(4) clinical decision support imply clinical data
- Medication lists and medication allergy lists (a)(1) CPOE
- Clinical notes and documentation via templates
- Implantable device lists (a)(14)
- Social, psychological, and behavioral data (a)(15)
- Family health history (a)(12)
- Lab orders and results (via eLab© integration and CPOE certification)
- Radiology orders (via eRad® integration)

**Prescribing data:**
- Prescription records, pharmacy selection, formulary status
- Drug interaction and allergy check data

**Care coordination data** (certified (b)(1)–(b)(3)):
- Transitions of care / referral summaries (C-CDA documents)
- Care plan information

**Public health reporting data** (certified (f)(1)–(f)(7)):
- Immunization data (f)(1)
- Syndromic surveillance data (f)(2)
- Electronic case reporting (f)(3)
- Cancer registry data (f)(4) — consistent with oncology variant
- Antimicrobial use/resistance reporting (f)(6), (f)(7)
- Transmission to public health registries (f)(5)

**Patient portal data:**
- Messages between patients and providers
- Patient-entered health information (e)(3)
- Shared documents and files

**Billing/financial data** (via eBilling©):
- Claims data, account histories, payment records, patient liability
- EDI transaction data

**Practice management data** (via Phoenix PMS):
- Scheduling, registration, operational data — specifics unclear from website

**API/FHIR data** (certified (g)(7), (g)(9), (g)(10)):
- FHIR-based API access to clinical data (USCDI)

The website descriptions are quite high-level and marketing-oriented. Specific data fields, database schemas, or detailed data dictionaries were not found. The mandatory disclosures PDF could not be successfully parsed (returned as garbled binary content).

---

## Notes on Research Limitations

- The vendor website is poorly maintained; several pages contain injected spam content, and the PDF documents (transparency disclosures, product brochure) could not be successfully fetched/parsed.
- No third-party reviews were found on G2, Capterra, or Software Advice.
- No customer case studies or user testimonials were identified.
- The HCI Innovation Group 2014 profile is the most substantive independent source found, but it is over a decade old.
- It is unclear whether E*HealthLine has significant active customers for the Phoenix product in the current market. The broad product portfolio and global marketing claims are ambitious for a 245-person company, which may indicate the company is smaller or less active than its website suggests.
- The distinction between Phoenix EHR and the companion products (PMS, eBilling, E*Prescription, Patient Portal) is important: they appear to be separate modules, but the certified product name "Phoenix© Integrated Electronic Health Records" and the broad certification criteria suggest the certification covers the integrated suite.

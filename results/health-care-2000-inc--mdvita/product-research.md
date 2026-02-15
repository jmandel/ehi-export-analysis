# Health Care 2000, Inc. — Product Research

Researched: 2026-02-14
Developer website: http://www.hc2000inc.com

## Overview

Health Care 2000, Inc. is a small, family-owned healthcare IT company based in Palmetto Bay, Florida (Miami area). Founded in 1997 by Martin Gonzalez as a claim adjudication company, the company launched its software division in 2000 with a product called MD2000, a healthcare practice management application. That product evolved into MDVita, their current ONC-certified EHR and practice management suite. The company describes itself as having "more than 20 years of service in South Florida" and emphasizes low employee turnover (average tenure of 10 years).

Health Care 2000 services "hundreds of medical centers" according to their website, primarily in South Florida. Their niche is value-based care providers — specifically physicians operating under risk-based contracts with Medicare Advantage plans and other value-driven payment arrangements. Beyond software, the company provides customized financial consulting and data analysis services through in-house healthcare finance professionals. The company has no presence on major software review platforms (G2, Capterra) and appears to be a small regional vendor serving a localized market.

## Product: MDVita

CHPL ID: 11000
CHPL Product Number: 15.04.04.2904.MDVi.27.02.1.221020
Version: 27 (certified October 20, 2022, by Drummond Group)
SED Intended Users: Family Practice

### What It Is

MDVita is an ONC-certified electronic medical record (EMR) and physician practice management application. It is not a component of a larger product — MDVita is the full product, encompassing both clinical EHR and administrative practice management functionality in a single integrated suite. The product is specifically designed for value-based care providers in primary/family practice settings.

MDVita Analytics is a separately named extension module that provides financial analytics and utilization performance measurement. It appears to be offered as an add-on to the core MDVita product.

The product has a broad certification profile with 38+ criteria including clinical documentation (a)(1)–(a)(5), (a)(12), (a)(14), transitions of care (b)(1)–(b)(2), patient portal/VDT (e)(1), public health reporting (f)(1)–(f)(2), FHIR API (g)(7)–(g)(10), and Direct messaging (h)(1). This is a comprehensive certification for a small vendor.

### Users & Market

**Target users**: Physicians and clinical staff in family/general/primary care practices. The SED testing report indicates the intended user is "Family Practice."

**Customer base**: "Hundreds of medical centers" in South Florida, per the vendor website. The product is described as "a very popular application suite used in South Florida by many health care providers" (Alignable profile). No specific customer names or case studies are publicly available.

**Clinical setting**: Ambulatory primary care practices, particularly those operating under Medicare Advantage risk-based contracts and value-based payment arrangements. Not hospital-oriented.

**Company size**: Very small. Family-owned business based in Palmetto Bay, FL. No presence on major review platforms. No publicly available employee count or revenue figures; ZoomInfo has a profile but details are behind a paywall.

**Deployment**: Available as cloud-based (monthly per-provider fee), cloud-based revenue-sharing model (percentage of collections plus potential per-FTE charges), or license-based (one-time fee with monthly maintenance, customer or vendor-hosted). Mobile access is supported via RDP connections to dedicated servers.

### Modules & Functionality

Based on vendor website, disclosure pages, and Alignable profile, MDVita includes the following modules and capabilities:

**Electronic Health Records / Clinical**
- Clinical notes and documentation
- Patient chart with clinical information
- Treatment plans
- Computerized Provider Order Entry (CPOE) for medications, lab orders, and diagnostic imaging
- Drug-drug and drug-allergy interaction checking
- Clinical decision support
- Problem list management
- Vital signs documentation
- Medication and allergy management
- Family health history
- Patient demographics
- Patient education resources

**Practice Management**
- Health care practice management (scheduling, registration — implied by "practice management" module though specific sub-features not detailed)
- Revenue cycle management
- Billing management (the company originated as a claim adjudication company, and billing/revenue cycle is a core described capability)

**ePrescribe**
- Electronic prescribing functionality

**Analytics (MDVita Analytics — add-on module)**
- Financial data reporting and analysis
- Customizable reports on claim counts, average costs, paid amounts, funding reports, and key expenses
- Reports filterable by location, patient, provider, insurance, and date
- Utilization and performance measurement
- Designed to help manage revenue cycles across multiple lines of business

**Interoperability**
- Direct protocol messaging (via EMR Direct's Interoperability Engine platform, certified 2020)
- C-CDA document generation and exchange for transitions of care
- HL7 FHIR API access (Standardized API)
- Patient portal functionality (e)(1) — though the older disclosure page notes the patient portal involves a third-party component with additional costs

**Public Health Reporting**
- Immunization registry transmission (f)(1)
- Syndromic surveillance reporting (f)(2)

**Quality Measures**
- Clinical quality measure tracking and reporting
- QRDA file generation (noted as additional cost)
- 16 specific clinical quality measures supported per the older disclosure, including diabetes management, cancer screenings, and medication appropriateness
- 9 clinical quality measures per the current disclosure page

### Data & Content

Based on the described modules and certification criteria, MDVita stores and manages:

**Clinical data**: Patient demographics, medical history, family health history, problem lists, medication lists, allergy lists, vital signs, clinical notes, treatment plans, lab orders and results, diagnostic imaging orders, immunization records, patient education materials provided, and clinical quality measure data. The CPOE certification for medications, labs, and imaging (a)(1)–(a)(3) confirms these order types are stored in the system.

**Prescribing data**: Electronic prescription data, drug interaction checking data. The (a)(4) certification (drug-drug/drug-allergy checks) confirms medication and allergy data is actively managed.

**Care coordination data**: Transition of care summaries (C-CDA documents), Direct messages for care coordination, referral information (implied by (b)(1)–(b)(2) certification).

**Practice management / billing data**: The vendor's origin as a claim adjudication company and explicit listing of "revenue cycle management" and "billing management" as core modules indicates the product stores claims data, billing records, payment information, and payer/insurance data. MDVita Analytics' ability to report on "claim counts, average costs, paid amounts, funding reports, and key expenses" filtered by insurance confirms insurance/claims data is stored.

**Patient portal data**: Patient-facing data accessible through the portal (e)(1), including the ability to view, download, and transmit health information.

**Public health data**: Immunization data transmitted to registries, syndromic surveillance data — both confirmed by (f)(1) and (f)(2) certification.

**Administrative data**: Provider information, location data, scheduling data (implied by practice management module though not explicitly detailed), and audit logs (required by (d) criteria).

**What's less clear**: The vendor website does not explicitly mention document management/scanning, patient messaging/secure communications (beyond Direct protocol), or appointment scheduling details. The older disclosure page notes additional costs for "Internet Mailbox" and "File Repository" add-ons, suggesting document storage and secure messaging may be optional components. The nature of the patient portal (third-party vs. integrated) introduces some ambiguity about what patient-generated data is stored in MDVita itself vs. a third-party portal system.

---

# American Medical Solutions, Inc. — Product Research

Researched: 2026-02-14
Developer website: https://www.americanmedicalsolutions.com

## Overview

American Medical Solutions, Inc. (AMS) is a small, privately held company headquartered in the Phoenix/Tempe, Arizona area. Founded in December 2004, the company has been in business for approximately 21 years. The company is led by Anthony Puglisi, who serves as President/CEO and has been with the company for over 28 years (suggesting he may have been involved in a predecessor entity before the current incorporation). AMS describes itself as "a nationwide provider of integrated physician services and solutions" focused on helping medical practices schedule, capture, bill, and report patient data more efficiently.

AMS is a very small vendor — there is no publicly available employee count, no disclosed funding, no Crunchbase funding records, and no notable market presence on major EHR review platforms (zero user reviews on Slashdot, SourceForge, G2, or similar sites). The company is not BBB-accredited and has a C+ BBB rating. It appears to serve a small number of ambulatory medical practices, primarily in the Phoenix/Arizona area though it markets itself as a nationwide provider.

Beyond its EHR/practice management software, AMS also operates ancillary healthcare services including medical record retrieval, document scanning/imaging, release of information (ROI) services, medical staffing, and Attending Physician Statement (APS) acquisition and distribution. The company operates multiple web properties: americanmedicalsolutions.com, amsemr.com, getaps.com, and amsconnects.com.

**Important note:** AMS (American Medical Solutions) should not be confused with "American Medical Software" (americanmedical.com), which is a separate company that makes "AMS Ultra Charts," "AMS Ultra Billing," "AMS Ultra Schedules," and "AMS Ultra Portal." Despite the similar "AMS" abbreviation and similar product space, these are different companies. Some third-party review sites conflate the two.

## Product: Helios (HeliosMD / HeliosND)

CHPL ID: 10834
CHPL Product Number: 15.02.05.1086.AMEM.01.01.1.220217
Version: 2.0
Certification Date: 2022-02-17

### What It Is

Helios is a web-based, cloud-hosted EHR and practice management system designed for ambulatory clinical settings. It comes in two variants:

- **HeliosMD** — the primary EHR/practice management product for conventional medical practices, described as "an all-in-one system inclusive of practice management, document management and medical records" (per Datafied listing).
- **HeliosND** — a variant "developed specifically for Naturopathic physicians and their needs" (per Datafied listing). It appears functionally similar to HeliosMD but tailored for naturopathic practice workflows.

The CHPL-certified product is simply called "Helios" version 2.0. Based on the certification criteria, the certified module appears to be the full product (not a component of something larger), covering clinical documentation, practice management, patient portal, e-prescribing, lab integration, transitions of care, public health reporting, and FHIR API access.

The product has a broad set of 37 certified criteria spanning:
- **(a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15)**: Core clinical capabilities (CPOE, demographics, problem list, medication list, medication allergy list, family health history, patient-specific education, implantable device list)
- **(b)(1)–(b)(2), (b)(10)–(b)(11)**: Transitions of care and EHI export
- **(c)(1)–(c)(3)**: Clinical quality measures
- **(e)(1), (e)(3)**: Patient portal (view, download, transmit) and patient health information capture
- **(f)(1), (f)(5)**: Public health reporting (immunization, electronic case reporting)
- **(g)(2)–(g)(10)**: API access, FHIR, safety-enhanced design
- **(h)(1)**: Direct messaging

### Users & Market

The intended users are described as "Ambulatory Clinical" in the CHPL metadata. Based on vendor materials:

- **Specialties**: "A wide range of medical specialties, from Family Practices to General Surgeons" (per AMS about page). The Slashdot/SourceForge listings also mention charting, scheduling, and inventory management as core use cases.
- **Settings**: Small ambulatory medical practices, physician offices. The naturopathic variant (HeliosND) suggests penetration into alternative/integrative medicine practices.
- **Market size**: Appears to be very small. No customer counts are disclosed. Zero reviews on any major EHR review platform (Slashdot Software, SourceForge, G2, Capterra). The company's BBB profile lists it as a "Corporation" in the "Computer Software" category with no employee count.
- **Geography**: Based in Phoenix/Tempe, AZ; claims nationwide service but likely concentrated in the Arizona/Southwest region.

No notable customer case studies or deployments were found.

### Modules & Functionality

Based on vendor materials (amsemr.com, Datafied listings, and third-party review site listings), HeliosMD includes the following modules and features:

**Scheduling & Workflow**
- Intelligent scheduling tool handling multiple physicians and their patients
- Online appointment requests from patients
- Workflow manager showing daily appointments, appointment requests, lab orders, patient visit progress, current visit progress, and upcoming events (per Datafied HeliosMD listing)

**Clinical Documentation / EHR**
- Fully customizable encounter platform allowing physicians to enter notes in their preferred style (per Datafied)
- Voice recognition and handwriting recognition capabilities (per SourceForge listing)
- E/M coding support (per Slashdot listing)
- Web-based charting accessible from any location

**E-Prescribing**
- Electronic prescribing capability, including the ability to prescribe without requiring in-person visits (per Datafied)
- EPCS (Electronic Prescribing of Controlled Substances) certification noted on amsemr.com services page

**Lab Integration**
- Lab portal for ordering tests and reviewing results (per Datafied HeliosMD listing)
- Direct connection with major labs (per Datafied HeliosND listing)

**Billing / Practice Management**
- Integrated billing tool with fee schedules, co-pay management, and account reconciliation (per Datafied HeliosMD listing)
- Patient statement generation
- Billing analytics
- Claims submission described as "error-free" (per AMS about page)
- Insurance payment processing (per Datafied HeliosND listing)

**Patient Portal**
- Patient-facing portal for scheduling and communication between patients, physicians, and staff (per Datafied HeliosND listing)
- Certified for (e)(1) view/download/transmit and (e)(3) patient health information capture

**Document Management**
- Document scanning and imaging (a core AMS service)
- Paper-to-electronic conversion capabilities
- Secure storage and retrieval of electronic documents

**Inventory Management**
- Inventory management feature mentioned on SourceForge and Slashdot listings

**Transitions of Care / Interoperability**
- Direct messaging (certified for h(1))
- HL7 integration noted
- FHIR API endpoints (certified for g(7)–g(10))
- Transitions of care support (certified for b(1)–b(2))

**Public Health Reporting**
- Immunization registry reporting (certified for f(1))
- Electronic case reporting (certified for f(5))

**Clinical Quality Measures**
- CQM capture and export (certified for c(1)–c(3))
- MIPS reporting support noted on amsemr.com

**Security & Compliance**
- HIPAA-compliant with role-based access controls
- Multi-factor authentication
- Audit logging and access controls (certified for d-criteria)

### Data & Content

Based on the modules and features described above, Helios stores and manages:

- **Patient demographics** — certified for (a)(5), described in workflow manager
- **Clinical encounter notes** — customizable physician encounter documentation
- **Problem lists** — certified for (a)(3))
- **Medication lists and prescriptions** — certified for (a)(1) CPOE, (a)(4) medication list; e-prescribing including controlled substances
- **Medication allergy lists** — certified for (a)(2)
- **Lab orders and results** — lab portal with ordering and results tracking
- **Family health history** — certified for (a)(12)
- **Implantable device records** — certified for (a)(14)
- **Patient-specific education materials** — certified for (a)(15) (implied by certification)
- **Scheduling/appointment data** — multi-physician scheduling with online patient requests
- **Billing/claims data** — fee schedules, co-pays, account reconciliation, patient statements, billing analytics
- **Scanned documents and images** — document management and imaging
- **Immunization records** — certified for (f)(1) immunization registry reporting
- **Case reporting data** — certified for (f)(5) electronic case reporting
- **Clinical quality measure data** — certified for (c)(1)–(c)(3)
- **Patient portal messages/data** — patient communication through portal
- **Inventory data** — inventory management feature mentioned
- **Transitions of care documents** — CCDAs and care summaries via (b)(1)–(b)(2)
- **Audit logs** — security and access logging per d-criteria
- **Direct messages** — secure messaging via Direct protocol

**Information gaps**: The vendor website and third-party sources are relatively thin on detail. The vendor's main website (americanmedicalsolutions.com) simply redirects to amsemr.com. The amsemr.com services page is brief and focused more on compliance documentation than feature descriptions. The most detailed feature descriptions come from the Datafied third-party listings for HeliosMD and HeliosND, which describe the product in moderate but not exhaustive detail. It is unclear whether the system has:
- Referral tracking/management
- Integrated faxing beyond document scanning
- Patient messaging beyond the portal (e.g., SMS)
- Advanced analytics or reporting dashboards beyond billing analytics
- Templates for specific specialties
- Telehealth capabilities (one third-party listing on FindEMR mentioned telehealth but this may have been auto-generated or confused with another product)
- Order sets or clinical decision support

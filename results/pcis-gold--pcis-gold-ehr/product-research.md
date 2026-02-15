# PCIS GOLD — Product Research

Researched: 2026-02-15
Developer website: http://www.pcisgold.com

## Overview

PCIS GOLD is a healthcare software division of DHI Computing Service, Inc., a Provo, Utah-based company founded in 1954 by Bliss H. Crandall as the first data processor west of the Mississippi. DHI operates through four divisions serving different industries: Amelicor (dairy/agriculture), FPS GOLD (banking), GOLDPoint Systems (finance/lending), and PCIS GOLD (healthcare). The healthcare division originated when a Salt Lake City medical clinic approached DHI for medical data services, leading to the creation of Healthcare Processing Systems (HPS), which eventually became PCIS GOLD around 2000.

PCIS GOLD is a small vendor — employee counts range from 14 to 28 depending on source. The company targets independent ambulatory medical groups, particularly those with 10 or more physicians. It serves small to medium-sized practices from single-physician clinics to multi-specialty groups. The product is an integrated EHR and practice management platform — not a specialty-specific system. At least one customer testimonial references an eyecare practice, suggesting multi-specialty applicability with customizable templates. The company is an MGMA corporate member, Surescripts-certified, and Drummond-certified for ONC compliance.

## Product: PCIS GOLD EHR

CHPL IDs: 11137

### What It Is

PCIS GOLD EHR is an all-in-one ambulatory medical software platform that integrates electronic health records, practice management, patient engagement, and healthcare analytics into a single cohesive system. The certified product (version 2.6, certified December 2022) holds 33 ONC certification criteria spanning clinical documentation (a)(1)–(a)(5), (a)(12), (a)(14), care coordination (b)(1)–(b)(3), (b)(10)–(b)(11), clinical quality measures (c)(1)–(c)(3), patient access (e)(1), (e)(3), public health reporting (f)(1), (f)(2), (f)(4), and FHIR API access (g)(7), (g)(9), (g)(10). This is a comprehensive certification profile covering the full range of ambulatory EHR capabilities.

The certified module encompasses the full product — PCIS GOLD does not appear to sell the EHR, practice management, patient portal, or analytics as separate standalone products. They are components of one integrated platform.

### Users & Market

**Target users:** Ambulatory physicians, nurses, clinical staff, billing staff, practice managers, and front-office staff. The ONC SED testing description identifies "ambulatory physicians, nurses, and staff."

**Clinical settings:** Independent ambulatory medical groups, multi-physician practices, multi-specialty groups. The vendor explicitly targets groups with 10+ physicians, though also serves smaller practices.

**Market position:** Small/niche vendor. PCIS GOLD is not widely reviewed — Capterra, G2, and similar platforms show zero or very few user reviews. The company does not publicly disclose customer counts, revenue, or market share figures. This is consistent with a small regional vendor serving a limited customer base. The company's parent (DHI Computing Service) is a diversified data services company, not a healthcare-focused enterprise.

**Deployment:** The product appears to be available as cloud-hosted or on-premises with network storage. The vendor describes it as a "managed" solution, suggesting cloud/hosted is the primary model. The platform is accessible as a web app and supports Windows and macOS.

### Modules & Functionality

Based on vendor website, feature listings, blog posts, and third-party aggregator sites, the product includes the following functional areas:

**Electronic Health Records / Clinical Documentation:**
- Customizable charting with point-and-click, form-based data entry, speech-to-text, and keyboard shortcuts (vendor website, blog post)
- Physician-built form-based charts and custom healthcare plan macros for commonly seen items (blog post)
- Customizable screen layouts, tab locations, preference settings, and notification controls (medical charting page)
- ICD-10 compliant coding support (medical charting page)
- Clinical decision support with automated preventive care reminders and drug interaction warnings (blog post on core functions)
- Diagnostic tools to "help guide clinicians through detection of complex conditions" (blog post)
- Implantable device tracking (mandatory disclosures page)
- Family health history recording (mandatory disclosures page)

**Computerized Physician Order Entry (CPOE):**
- Electronic ordering for medications, laboratory, and imaging (mandatory disclosures page)
- Automated duplicate order detection (blog post)
- Drug interaction checking, inappropriate dose flagging, and insurance coverage verification for prescriptions (blog post)

**E-Prescribing:**
- Surescripts-certified electronic prescription transmission (vendor website, multiple sources)
- Partnership with NewCrop for electronic pharmacy transmission (blog post)
- Electronic controlled substance prescribing implied by Surescripts certification

**Lab Integration:**
- Quick access to lab results with abnormal finding detection (multiple sources)
- Automatic display of previous lab findings to reduce redundant testing (vendor website)
- Lab result ordering and tracking

**Practice Management & Billing:**
- Patient scheduling — online, in-person, and phone-based appointment management (PM page)
- Patient registration with demographic data collection (PM page)
- Insurance verification — electronic eligibility confirmation before or at point of service (PM page)
- Billing and claims management with built-in claim scrubbing tools (PM page)
- Automated accounts receivable management (PM page)
- Co-pay collection (PM page)
- Real-time revenue cycle reporting and financial performance visibility (PM page)
- Claims submission and denial reduction tools (PM page)

**Patient Engagement / Portal:**
- Patient portal with secure access to personal health records (patient engagement page)
- Mobile app for patient access (patient engagement page)
- Secure two-way text messaging between patients and providers (patient engagement page)
- Online appointment self-scheduling (patient engagement page)
- Online payment processing and flexible payment plans (patient engagement page)
- Digital patient registration and intake forms — demographics, consent documents (patient engagement page)
- Automated appointment reminders via text, email, or phone (patient engagement page)
- Patient education materials and follow-up instructions (blog post)
- E-Statements (search results mention)
- Lab and test result viewing through portal (search results)

**E-Tasking / Internal Communication:**
- Electronic task assignment, tracking, and management among staff (EHR page)
- Built-in messaging for provider-to-provider communication (blog post)

**Healthcare Analytics / Reporting:**
- Real-time analytics and data analysis tools (vendor website)
- Practice performance tracking and forecasting (vendor website)
- Clinical quality measure capture and reporting — certified for CQMs (mandatory disclosures, 38 CQMs)

**Public Health Reporting:**
- Immunization registry submissions (certified (f)(1))
- Syndromic surveillance reporting (certified (f)(2))
- Cancer case reporting (certified (f)(4))

**Care Coordination / Interoperability:**
- Transition of care summaries in standardized formats (mandatory disclosures)
- Clinical information reconciliation (mandatory disclosures)
- FHIR API access (certified (g)(7), (g)(9), (g)(10))
- Patient health information export (certified (b)(10))

**Document Management:**
- Document management capabilities (listed on SoftwareSuggest)

**Telehealth:**
- Telehealth integration listed as a feature on SoftwareSuggest, though details are sparse. FindEMR lists telemedicine as "unavailable," creating some ambiguity about whether it's natively built in or available through integration.

### Data & Content

Based on the features and certifications described above, the product manages the following data categories:

**Clinical data:** Patient demographics, allergies, medications (active and historical), diagnoses, problem lists, vital signs, immunizations, lab orders and results, imaging orders, family health history, implantable device records, clinical notes/charting documentation, clinical decision support alerts, healthcare plan macros, and custom form-based chart data.

**Prescription data:** Electronic prescriptions transmitted through Surescripts/NewCrop, including drug interaction checks, dose appropriateness flags, and insurance formulary verification. The Surescripts certification implies prescription history and medication reconciliation data.

**Administrative/financial data:** Patient registration and demographic records, insurance information and eligibility verification results, appointment schedules, billing records, claims data (with scrubbing results), accounts receivable records, co-pay and payment records, e-statements, and revenue cycle analytics.

**Communication data:** Secure patient-provider messages (via portal and two-way text), provider-to-provider internal messages (e-tasking), automated appointment reminders (text/email/phone), and patient education materials.

**Patient-generated data:** Online intake forms, consent documents, demographic updates, appointment requests, and portal activity.

**Reporting data:** Clinical quality measure data (38 CQMs), immunization registry submissions, syndromic surveillance data, cancer case reports, and practice performance analytics.

**Care coordination data:** Transition of care documents (C-CDAs), clinical reconciliation records, and FHIR-accessible patient data.

**Gaps/uncertainties:**
- The vendor website is relatively light on technical detail — it is marketing-oriented and does not enumerate specific data fields or database structures.
- Telehealth capability is ambiguous — one source lists it, another marks it unavailable.
- No mention of radiology/imaging results storage (only ordering) — unclear if results/images are stored in-system or accessed externally.
- No mention of referral management as a built-in feature (FindEMR marks it unavailable).
- Voice recognition / handwriting recognition listed on SoftwareSuggest but not detailed on the vendor site.
- No information found about integration with specific lab vendors, clearinghouses, or health information exchanges beyond Surescripts and NewCrop.
- Very few independent user reviews exist, limiting insight into real-world usage patterns.

---

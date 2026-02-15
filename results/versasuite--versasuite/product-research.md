# VersaSuite — Product Research

Researched: 2026-02-15
Developer website: https://www.versasuite.com

## Overview

VersaSuite is a comprehensive healthcare information technology platform developed by Universal Software Solutions Inc. (USSI), a privately held company founded in 1994 and headquartered in Austin, Texas. The company has been doing business as "VersaSuite" since the early 2000s. The product has been designed and programmed by a single core development team in Austin since June 1997. VersaSuite positions itself as an all-in-one HIS/EHR/EPM/ERP solution — a combined Hospital Information System, Electronic Health Record, Enterprise Practice Management, and Enterprise Resource Planning platform — running on a single database and single framework. They claim 36 integrated modules.

VersaSuite primarily targets small to mid-size hospitals, including critical access hospitals, specialty hospitals (surgical, behavioral health, LTAC, rehabilitation, hospice), acute care facilities, and ambulatory/outpatient clinics. Their ONC certification SED user description explicitly says "Small hospitals." The company appears to be a small, niche vendor — no customer counts are disclosed publicly, and reviews across platforms (Capterra, G2, SoftwareFinder) are extremely sparse (1-3 reviews total). No KLAS data was found. The product is available as both a desktop client-server application (VersaSuite) and a web-based platform (VersaWeb), and supports English and Spanish interfaces. The company reports serving clinics, surgical centers, and hospitals globally, though specifics are not disclosed.

Notable integration partners mentioned on third-party listings include AxiaMed (payment processing), Microsoft, TruCode (coding), Acuant (identity verification), CVS Caremark (pharmacy), and Eyemaginations (patient education).

## Product: VersaSuite

CHPL ID: 10299 (VersaSuite 9.0, certified 2020-02-10)

### What It Is

VersaSuite is a monolithic, all-in-one healthcare IT platform covering clinical, administrative, and financial functions for both inpatient and outpatient settings. The certified module appears to be the entire product — the company repeatedly emphasizes that it is "ONE product, built on ONE Framework, running on ONE Database." There are not separate, independently deployable products; rather, it is a single platform with modules that can be configured for different facility types and specialties.

The product is available on two delivery platforms: a Windows desktop client-server application and VersaWeb, a modern web-based interface. Both share the same database and core functionality.

### Users & Market

**Target facilities:**
- Critical access hospitals (a primary marketing focus)
- Specialty hospitals (surgical, behavioral health, LTAC, rehabilitation, hospice)
- Acute care hospitals
- Ambulatory/outpatient clinics and practices
- Urgent care facilities
- Ambulatory surgical centers
- FQHCs and RHCs (mentioned on feature pages)
- Home health
- Dental practices (mentioned as a supported specialty)

**End users:** Physicians, nurses, clinical staff, pharmacists, lab technicians, radiology technicians, billing staff, HIM professionals, administrative/financial staff, HR personnel, and patients (via patient portal).

**Market position:** VersaSuite is a small, niche vendor. No customer counts, revenue figures, or installation base numbers are publicly disclosed. Review data is minimal — Capterra shows a small number of reviews (approximately 3), with positive feedback emphasizing the product's flexibility, comprehensive feature set, and strong support. One reviewer (a Director of Informatics at a critical access hospital) praised the training and cost-effectiveness. Another noted a steep learning curve and occasional software glitches. No KLAS reviews or significant analyst coverage was found. The vendor does not appear to have significant market share compared to larger competitors.

### Modules & Functionality

VersaSuite claims 36 modules across four integrated systems. Based on vendor website content and third-party listings, these include:

**Clinical / EHR:**
- **Electronic Health Records (EHR)** — Clinical documentation with specialty-specific templates. Supports ambulatory, ED, and inpatient environments with the same interface. Features advanced drawing components, keyboard-free data entry, voice dictation integration (Dragon Medical, M*Modal), auto-generated exam summaries, graphical data visualization, and concurrent multi-patient record access.
- **Computerized Physician Order Entry (CPOE)** — Order management for medications, lab, and diagnostic imaging.
- **Electronic Medication Administration Record (EMAR)** — Medication administration tracking.
- **Electronic Treatment Administration Record (ETAR)** — Treatment authorization and administration.
- **Clinical Decision Support** — Implied by (a)(2) certification for clinical decision support interventions.
- **Emergency Department Information System (EDIS)** — Emergency department workflows (mentioned on specialty hospitals page).

**Laboratory & Imaging:**
- **Laboratory Information Management System (LIMS)** — Lab test ordering, processing, and results management.
- **Radiology Information System / PACS (RIS/PACS)** — Radiology workflow management and picture archiving/communication. One-click access from within the EHR.

**Pharmacy:**
- **Pharmacy Information Management System** — Medication management, formulary management. Electronic prescribing (certified for (b)(3) electronic prescribing). Integration with CVS Caremark noted.

**Practice Management & Billing:**
- **Enterprise Practice Management (EPM)** — Scheduling, registration, check-in, billing, accounts receivable, collections. The outpatient page describes automating "every aspect of any ambulatory clinic from scheduling and check-in through accounts receivable and collections."
- **Point of Sale (POS)** — Payment/transaction processing at point of service.
- **Automatic billing code transmission** — Billing codes pass automatically from clinical to financial systems.

**Health Information Management:**
- **Health Information Management (HIM)** — Medical records management, coding. Integration with TruCode for coding noted.
- **Document Management System (DMS)** — Records and file storage/retrieval.

**Patient & Provider Portals:**
- **Patient Portal** — Patient access to health information, including FHIR API access (certified for (e)(1) view/download/transmit and (g)(10) FHIR API). Pricing noted as $150/provider/year outpatient, $50/bed/year inpatient.
- **Provider Portal** — Clinician workflow tools.

**Nutrition:**
- **Clinical Nutrition & Food** — Dietary/nutritional services management.

**Administrative / ERP:**
- **Accounting / General Ledger** — Financial management, accounts receivable/payable reconciliation.
- **Payroll** — Employee compensation processing.
- **Human Resources (HR)** — Employee management, onboarding, evaluations.
- **Employee Time & Attendance** — Time tracking, overtime, tardy tracking.
- **Employee Scheduling** — Workforce scheduling.
- **Employee Portal** — Self-service for employees to access personnel folders, PTO, direct deposit, communicate with management.
- **Budgeting** — Financial planning.
- **Facility Management** — Operations management.
- **Procurement** — Purchasing functions.
- **Inventory & Materials Management** — Supply chain operations.
- **Risk and Compliance Management** — Regulatory oversight.

**Reporting & Analytics:**
- **Reports Module** — Custom reporting, data analytics, quality reporting. Access to "discrete and sensitive variables."
- **Reports/Letters** — Clinical and administrative documentation generation.

**Public Health Reporting:**
- Certified for (f)(1) through (f)(7) — immunization registries, electronic case reporting, public health syndromic surveillance, cancer case reporting, and other public health reporting.

**Interoperability:**
- Certified for (b)(1) transitions of care, (b)(2) clinical information reconciliation, and (b)(3) electronic prescribing.
- FHIR API support via (g)(7), (g)(9), and (g)(10) certification.
- Direct messaging for transitions of care implied by (h)(1) certification.

### Data & Content

Based on the modules, features, certifications, and vendor descriptions, VersaSuite manages an extremely broad range of data types across a single integrated database:

**Clinical data (explicitly described in vendor materials):**
- Patient demographics and registration data
- Chief complaints, problem lists, illness history
- Review of systems documentation
- Physical examination findings (including drawing/annotation)
- Assessment and plan documentation
- Medication orders, prescriptions, medication administration records (EMAR)
- Treatment administration records (ETAR)
- Laboratory orders and results (LIMS)
- Radiology/imaging orders, images, and reports (RIS/PACS)
- CPOE orders (medications, lab, diagnostic imaging)
- Clinical notes and exam summaries (auto-generated)
- Allergy information (implied by (a)(1) CPOE medications certification)
- Vital signs (implied by clinical documentation)

**Administrative/financial data (explicitly described):**
- Appointment scheduling data
- Patient check-in/registration
- Billing codes and claims data (automatic code transmission to billing)
- Accounts receivable and collections
- Point of sale transactions
- General ledger, accounts payable/receivable
- Budgets and financial plans

**Workforce/HR data (explicitly described):**
- Employee demographics and personnel records
- Payroll and compensation data (including direct deposit)
- Time and attendance records
- Employee scheduling
- PTO records
- Onboarding forms and evaluations
- Dependent and disability information

**Other data:**
- Inventory and materials/supply chain data
- Procurement records
- Facility management data
- Clinical nutrition and dietary information
- Document management (scanned/stored documents)
- Patient portal communications and access logs
- Quality/compliance reporting data
- Public health reporting data (immunizations, syndromic surveillance, cancer cases, etc.)

**Key architectural note:** The vendor's core marketing message is that all of this data resides in a single database. This is significant for EHI export assessment — if the product truly uses one database, then a comprehensive export mechanism should be able to access all clinical, administrative, and financial data without crossing system boundaries.

**Gaps / Uncertainty:**
- No specific mention of patient messaging or secure messaging beyond the employee portal communication feature and patient portal. It's unclear how robust patient-provider messaging is.
- No mention of telehealth/telemedicine capabilities.
- No mention of care plan management as a distinct feature (though it may be part of clinical documentation).
- Voice dictation integration is mentioned but it's unclear if dictated notes are stored within VersaSuite or in an external system.
- Integration with Acuant (identity verification) and Eyemaginations (patient education) is mentioned on a third-party listing but not detailed on the vendor's own site.
- The vendor website is relatively sparse on detailed feature descriptions — it's more marketing-oriented than documentation-oriented. The 36-module claim is repeated but a complete enumerated list of all 36 modules is not provided anywhere on the site.

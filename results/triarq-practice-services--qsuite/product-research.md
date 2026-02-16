# TRIARQ Practice Services — Product Research

Researched: 2026-02-15
Developer website: http://www.triarqhealth.com/

## Overview

TRIARQ Health (legally TRIARQ Practice Services) is a managed services organization (MSO) headquartered in Royal Oak, Michigan, that partners with independent specialty physician practices. The company was formed in 2015 through a merger involving gloStream, a Troy, Michigan-based EHR vendor founded around 2005 that developed the gloEMR product. TRIARQ combined gloStream's EHR technology with practice management consulting and revenue cycle management services. In August 2021, Blue Cross Blue Shield of Michigan acquired TRIARQ Health, and the company now operates as a wholly owned subsidiary of BCBSM. As of late 2021, TRIARQ had approximately 64 employees.

TRIARQ's primary focus is on independent specialty practices, particularly in orthopedics, urology, and oncology, though they also serve cardiology, neurology, neurosurgery, pediatrics, and gastroenterology practices. Their business model is an MSO: they sell comprehensive practice management services (staffing, billing, compliance, supply chain, even real estate management) bundled with their proprietary EHR/PM technology platform called QSuite. They describe their mission as "protecting the practice of independent medicine." The company is relatively small and niche, serving independent specialty practices rather than large health systems or hospitals.

## Product: QSuite

CHPL IDs: 10709

### What It Is

QSuite is TRIARQ's proprietary cloud-based integrated EHR and practice management platform. It evolved from gloStream's gloEMR product (which was originally built on Microsoft Office / Windows platform with CCHIT 2011 certification). QSuite is the technology backbone of TRIARQ's managed services offering. It is ONC-certified and Surescripts-certified. The product is hosted on Google Cloud Platform.

QSuite is not just an EHR — it is an integrated platform spanning clinical documentation, practice management, billing/RCM, patient engagement, and analytics. TRIARQ markets it as part of their broader MSO offering, but the technology itself is the certified product. The product version certified on CHPL is "Manistee" (certified November 2021).

The certified module has broad certification: 40+ criteria spanning clinical data (a)(1)-(a)(15), transitions of care (b)(1)-(b)(3), clinical information reconciliation (b)(7)-(b)(9), patient portal/VDT (e)(1)-(e)(3), public health reporting (f)(1)-(f)(2), CQMs (c)(1)-(c)(4), FHIR APIs (g)(7)-(g)(10), and the EHI export requirement (b)(10). This is a comprehensive clinical EHR certification, not a narrow single-criterion product.

### Users & Market

Target users (per CHPL SED description): "doctors, nurses, physicians assistants, medical assistants, anyone entering or accessing clinical data at an ambulatory medical practice, anyone responsible for the training users and anyone responsible for system administration or IT of a medical practice."

The product serves independent ambulatory specialty practices. Specific specialties highlighted by the vendor include orthopedics, urology, oncology, cardiology, neurology, and gastroenterology. TRIARQ emphasizes that their technology is "specialty-built" — for example, marketing an "orthopedic-built EHR" on their orthopedics page.

The company is small (64 employees as of 2021). Customer count is not publicly disclosed on the website. Third-party review sites (SoftwareFinder, FindEMR) show very few reviews (1-2), suggesting a relatively small user base. One user review on SoftwareFinder rated it 4/5, saying "it is a good EMR with potential to improve and be the best out there." A Capterra review mentioned being with the product for over 10 years and appreciating its customization and ease of use.

### Modules & Functionality

Based on vendor website, specialty pages, blog posts, and third-party review sites, QSuite includes the following modules and components:

**EMR / Clinical Documentation**
- Clinical charting and documentation
- QScribe: AI-powered ambient listening that automatically generates structured clinical notes in the EHR (relatively new feature)
- Customizable templates (inherited from gloEMR's template system)
- Voice recognition functionality (a gloEMR legacy feature)

**E-Prescribing**
- Electronic prescribing (Surescripts-certified)
- Integration with third-party EPCS (Electronic Prescribing of Controlled Substances) solutions

**Practice Management (QPM)**
- Appointment scheduling (including telehealth scheduling)
- Patient registration and intake
- Automated insurance and eligibility verification
- Prior authorization management
- Workflow automation
- Real-time dashboards and KPI monitoring

**QIntake**
- Streamlined patient intake and registration portal
- Patient-facing interface for onboarding

**Patient Portal (MyQOne)**
- Patient engagement between appointments
- Access to medical results and bills
- Treatment updates
- Scheduling and billing access for patients

**Billing / Revenue Cycle Management**
- Built-in billing, coding, and tracking
- Claims management (submission, corrections, resubmissions, appeals)
- A/R management (automatic flagging of denied, underpaid, or unpaid claims)
- Denial management
- Patient payment tools and collections
- QComplete: full-service RCM bundle combining QSuite technology with outsourced RCM team support

**QInsights (Reporting & Analytics)**
- Practice-specific financial dashboards
- Revenue gap identification
- Customizable cloud-based reporting
- Monthly scorecards
- Performance metrics and KPI tracking

**QPathways (Care Management & Referral Networks)**
- Referral network integration across providers, payers, and patients
- Care coordination tools
- Clinical and financial transparency platform
- Value-based care support

**Lab Integration**
- Lab orders and results integration
- Automatic updating of health records with new lab results
- TRIARQ Connectors for secure links between office, patients, providers, off-site labs, and other facilities

**Interoperability / Data Exchange**
- Transitions of care / C-CDA support (certified for (b)(1)-(b)(3))
- Direct messaging
- FHIR API access (certified for (g)(7)-(g)(10))
- Patient reminders
- Public health reporting (immunization, syndromic surveillance)
- MIPS quality measure reporting and attesting support

### Data & Content

Based on the features and modules described above, QSuite stores and manages:

- **Clinical data**: Patient demographics, medical histories, clinical notes (including AI-generated notes via QScribe), problems, medications, allergies, vital signs, lab orders and results, immunizations, procedures, clinical decision support data
- **Prescriptions**: E-prescribing data including controlled substance prescriptions (via EPCS integration), medication histories, Surescripts data
- **Scheduling data**: Appointments, telehealth scheduling, patient location tracking from admission to discharge
- **Patient intake/registration**: Contact information, insurance information, eligibility verification data, intake forms
- **Billing and financial data**: Claims, charge capture, coding data, A/R records, denial records, payment data, insurance eligibility responses, prior authorizations
- **Patient portal data**: Patient messages, portal access logs, shared documents and results
- **Lab data**: Lab orders, lab results (integrated from external labs)
- **Referral data**: Referral network information, care coordination records via QPathways
- **Quality/reporting data**: CQM/MIPS quality measure data, public health reporting submissions
- **Administrative data**: User accounts, staff tasks, practice configuration
- **Analytics/reporting data**: Dashboards, KPI snapshots, financial reports, scorecards

The vendor website does not specifically mention document management/scanning, imaging/PACS integration, or faxing capabilities, though these could exist without being prominently marketed. The blog post about comprehensive practice management mentions that TRIARQ handles "everything except patient examination and diagnosis," suggesting the platform touches nearly all practice operations. The integration with third-party EPCS solutions suggests some prescription workflow data may flow through external systems.

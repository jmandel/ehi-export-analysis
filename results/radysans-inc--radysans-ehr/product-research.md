# Radysans, Inc — Product Research

Researched: 2026-02-14
Developer website: https://radysans.com

## Overview

Radysans, Inc is a small, privately held healthcare IT company based in Apex, North Carolina (1701 Center St, Suite 200). The company was incorporated on November 18, 1999, and describes itself as founded by "a team of experienced Physicians and Business professionals" who understood the operational challenges of running medical practices. The BBB categorizes Radysans under "medical billing," and their Alignable listing describes them as offering "Integrated Health Records Software and RCM Services for outpatient clinics."

Radysans is a very small vendor — no employee counts or revenue figures are publicly available, and the company has no presence on major review platforms like G2, Capterra, or KLAS. Key leadership includes Raj Polavaram (President/Owner) and Shekar Raju (COO). The company operates the EHR platform at ehr.cutecharts.com (a domain that appears to be their hosted application environment). One identifiable customer is Mann ENT, an otolaryngology practice in Cary/Clayton, North Carolina, whose patient portal runs on Radysans EHR (portal.entmann.com). Dr. Charles H. Mann is described as a member of the Senior Advisory Council of Radysans, Inc, suggesting a close relationship between the vendor and at least some of its customers. The company's stated mission is to "become the most trusted and valued source for integrated Clinical Practice management solutions and services."

## Product: Radysans EHR

CHPL ID: 10253 (15.04.04.2912.Rady.05.00.1.191231)

### What It Is

Radysans EHR is an integrated ambulatory EHR and practice management platform targeting outpatient clinics and physician practices. The product is cloud-hosted (accessible via web browser at ehr.cutecharts.com) and offered as a SaaS subscription ("a single, low monthly subscription fee"). The current certified version is 5.0, though older instances (v3.0) are still visible at some customer portal URLs.

The product is broadly certified across 40+ ONC criteria, including clinical data (a)(1)–(a)(15), transitions of care (b)(1)–(b)(2), patient portal/VDT (e)(1), clinical quality measures (c)(1)–(c)(4), public health reporting (f)(1)–(f)(2), and FHIR APIs (g)(7)–(g)(10). This is a full-spectrum ambulatory certification. The intended users are described as "Ambulatory" in the CHPL metadata.

The certified module appears to cover the full product — Radysans does not appear to have separate products or distinct product lines. The EHR, practice management, billing, and patient portal are all presented as components of a single integrated platform.

### Users & Market

Radysans targets small ambulatory practices and outpatient clinics. The marketing emphasizes low cost, no upfront capital, no need for dedicated IT staff, and "local next door support" — all signals of a product designed for small, independent physician practices rather than large health systems.

The only identifiable live customer is Mann ENT, an ENT (otolaryngology) practice in the Raleigh-Durham area of North Carolina. The geographic proximity to Radysans' Apex, NC headquarters and Dr. Mann's role on the vendor's advisory council suggest Radysans may have a small, geographically concentrated customer base. No customer counts, user numbers, or market share data are publicly available. The vendor has no presence on KLAS, G2, or Capterra, which typically indicates a very small install base.

### Modules & Functionality

Based on the vendor website (Products page, Services page, eBilling page), Radysans describes the following integrated modules:

**Practice Management System (PMS):**
- Office Dashboard with real-time KPI reporting
- Enterprise Scheduling: multi-location, multi-physician appointment management with flexible time increments, automatic calculation, and cross-schedule search
- Patient Registration: check-in, tracking, scanning of patient photos, insurance cards, and regulatory documents
- Message Manager: integrated workflow/task routing to appropriate staff
- Referral Management: referral capture, tracking, and pre-authorization support
- Business Intelligence Reports: no-show/cancellation tracking, appointment histories, user productivity metrics, wait lists
- Insurance eligibility verification

**Electronic Medical Records (EMR):**
- Clinical documentation (details sparse on the website beyond listing "EMR" as a module)
- Certified for: CPOE (a)(1)–(a)(4), clinical decision support (a)(9), drug interaction checks (a)(4), demographics (a)(5), clinical information reconciliation (b)(2), implantable device list (a)(14), social/psychological/behavioral data (a)(15)
- The certification criteria imply the EMR stores: problems, medications, allergies, demographics, vital signs, lab results, clinical notes, implantable device data, smoking status, and care plans

**e-Billing:**
- Charge capture with insurance reimbursement rule monitoring
- Claim scrubbing and code checking to reduce denials
- Electronic claim submission to 2,500+ government and commercial payers
- Automated payment posting and reconciliation
- Denial tracking and rejection logging
- EOB (Explanation of Benefits) and ERA (Electronic Remittance Advice) processing
- Patient statement generation (automatic or on-demand, configurable batch rules)
- Electronic patient payment processing

**Patient Portal:**
- Patient login (requires practice code — multi-tenant design)
- Patient representative login (separate access for caregivers/proxies)
- Certified for View/Download/Transmit (e)(1) — patients can access their health information
- FHIR-based Patient API mentioned on the login page, with access to medications, allergies, care plans, diagnoses, and clinical observations

**Order Entry System:**
- Listed as a distinct module but no detailed feature description found on the website
- The (a)(1)–(a)(3) CPOE certification covers orders for medications, laboratory, and diagnostic imaging

**Transcription Services:**
- Medical transcription with "four-phase architecture" quality assurance
- Proof reading by certified transcriptionists
- 24-hour standard turnaround
- Delivery via US mail, fax, email, or modem
- Long-term data storage and retrieval of transcription documents

**Radysans Mobile:**
- Listed as a module but no details provided on the website about capabilities

**Revenue Cycle Management (RCM) Services:**
- Full outsourcing option for billing (data entry, electronic submission, delinquent account follow-up, reporting)
- Credentialing for new practitioners
- Coding and reimbursement rate change monitoring
- Tax and payroll services (surprisingly)
- 24/7/365 trained staff availability

### Data & Content

Based on the modules, certified criteria, and vendor materials, Radysans EHR stores or manages:

**Clinical Data** (evidenced by certification criteria and EMR module):
- Patient demographics, photos, insurance cards (Registration module — scanned documents)
- Problems/conditions, medications, allergies (certified criteria a)(1)–(a)(5))
- Lab orders and results (CPOE certification, order entry module)
- Diagnostic imaging orders (CPOE certification)
- Vital signs, smoking status
- Implantable device information (a)(14) certification)
- Social, psychological, and behavioral data (a)(15) certification)
- Clinical notes / transcriptions (Transcription Services module with long-term storage)
- Care plans
- Clinical decision support alerts and interactions

**Administrative/Financial Data** (evidenced by PMS and eBilling modules):
- Appointment schedules across multiple locations and providers
- Insurance eligibility and enrollment data
- Claims data (primary and secondary, electronic)
- EOBs and ERAs
- Payment records and reconciliation data
- Denial and rejection logs
- Patient statements and billing histories
- Referral and pre-authorization records
- No-show/cancellation data
- User productivity metrics

**Patient Portal Data** (evidenced by portal module and e)(1) certification):
- Patient-accessible health information (medications, allergies, care plans, diagnoses, observations)
- Patient representative access records

**Integration/Exchange Data** (evidenced by certifications):
- Transitions of care / C-CDA documents (b)(1)–(b)(2))
- Public health reporting: immunization registries (f)(1)), syndromic surveillance (f)(2))
- FHIR R4 API data (g)(7)–(g)(10)) — JSON format
- HL7 interfaces (mentioned on Security page)
- Direct messaging for clinical information exchange (h)(1))

**System/Audit Data** (evidenced by Security page):
- Audit trails with user identification, date, and time stamps for all data entries
- User-based permission records

**Notable uncertainties:**
- The website mentions Microsoft SQL Server 2005 on the Security page — this is extremely outdated (2005 was released 20+ years ago) and may indicate the website content is very old or the technology stack has not been updated
- No mention of e-prescribing (EPCS/Surescripts integration) was found on the vendor website, though the (a)(1) CPOE certification for medications implies some form of prescription ordering exists
- The "tax and payroll services" offered under RCM is unusual for an EHR vendor and may indicate this data is handled outside the EHR itself
- No mention of document management, clinical messaging/secure chat, or population health analytics beyond the basic BI reports
- The Radysans Mobile module is mentioned but completely undescribed

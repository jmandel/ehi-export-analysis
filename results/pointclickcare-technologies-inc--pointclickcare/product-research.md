# PointClickCare Technologies Inc. — Product Research

Researched: 2026-02-16
Developer website: https://pointclickcare.com/

## Overview

PointClickCare Technologies Inc. is a major cloud-based healthcare technology company specializing in long-term and post-acute care (LTPAC). Founded in 1995 (some sources say 2000) by Mike and Dave Wessinger, the company is headquartered in Mississauga, Ontario, Canada. With approximately 2,300 employees and $750M in annual revenue (as of 2025), PointClickCare is the dominant EHR vendor in the long-term care space — rated #1 Long-Term Care Software Provider by KLAS Research for six consecutive years through 2025. The company serves over 27,000 long-term and post-acute care providers, 3,100+ hospitals and health systems, 2,000+ ambulatory clinics, every major U.S. health plan, and 70+ state and government agencies. Their platform manages data for over 1.4 million active patients across 22,000+ skilled nursing facilities and 4,000+ assisted living facilities.

PointClickCare has grown significantly through acquisitions: Collective Medical (2020, care coordination for acute/ambulatory/post-acute), Audacious Inquiry (2022, $650M, connected care network for data exchange), Patient Pattern (2023, value-based care platform for Medicare Advantage SNPs, PACE, ACO REACH), and American HealthTech (2024, long-term care EHR from CPSI). The company has also partnered with Apploi for staffing/scheduling capabilities. PointClickCare is privately held and has not gone public.

The company's primary market is post-acute and long-term care: skilled nursing facilities (SNFs), assisted living, independent living, memory care, and continuing care retirement communities (CCRCs). They have expanded into adjacent markets including hospitals/health systems (for care transitions), ACOs, health plans, life sciences (de-identified data), pharmacies, and practice groups (physicians who serve LTPAC populations).

## Product: PointClickCare (Core EHR Platform)

CHPL ID: 10246

### What It Is

PointClickCare's core platform is a cloud-based, ONC-certified EHR designed primarily for skilled nursing facilities and senior living communities. It is not a single monolithic application but rather an integrated platform with numerous modules and add-ons. The certified product encompasses the core EHR functionality — clinical documentation, order management, medication administration, care planning, transitions of care, patient portal capabilities, and FHIR API access. The platform is certified across 27 criteria including clinical data (a)(1)–(a)(5), (a)(12), (a)(14), transitions of care (b)(1)–(b)(3), patient portal (e)(1), CQM (c)(1), and FHIR APIs (g)(7), (g)(9), (g)(10).

The certified module is a component of a much larger product ecosystem. The broader PointClickCare platform also includes revenue cycle management, analytics, staffing/scheduling (Apploi), CRM, care coordination network capabilities (from Collective Medical/Audacious Inquiry acquisitions), and numerous specialty modules.

### Users & Market

Day-to-day users include:
- **Nurses** (the primary charting users — documenting vitals, administering medications via eMAR, care planning, wound care tracking, shift-based documentation)
- **Medical Directors and Physicians** (order entry, encounter documentation, ePrescribing)
- **Clinical staff** (CNAs documenting ADLs, therapy staff)
- **MDS Coordinators** (completing and submitting MDS 3.0 assessments to iQIES)
- **Billing/Financial staff** (claims processing, accounts receivable, census management)
- **Administrators/Practice Managers** (dashboards, quality metrics, staffing)
- **Pharmacists** (via pharmacy integration for order management)

The SED intended user description from CHPL metadata confirms: "Clinicians, Nurses, Medical Directors, Other Healthcare Staff Roles."

Notable scale: 27,000+ LTPAC providers, making it by far the largest EHR in the long-term care segment. Aside from Epic in the broader EHR market, PointClickCare has among the largest market penetration of any EHR vendor due to its dominance in LTC/SNF.

### Modules & Functionality

Based on vendor materials, product pages, and third-party reviews, the PointClickCare platform includes the following modules and capabilities:

**Core EHR / Clinical Documentation:**
- Point-of-care (POC) charting for nurses — vital signs, weights, allergies, immunizations, treatments, condition changes
- Care plans with evidence-based protocols
- Progress notes and encounter documentation
- Physician order management (CPOE for medications, labs, imaging)
- Diagnosis management
- Assessment tools including MDS 3.0 with automated scheduling and iQIES submission
- Nursing Advantage module — comprehensive assessments and proactive clinical guidance
- Skin and wound care tracking module
- Infection prevention and control module
- Incident/event reporting

**Medication Management (QuickMAR / eMAR):**
- Electronic medication administration record
- Bar-coded medication administration (BCMA) with scanning
- Pharmacy order import and real-time connectivity with partner pharmacies
- Allergy checking and drug interaction alerts
- Omitted dose alerts
- ePrescribing including EPCS (Electronic Prescriptions for Controlled Substances) — certified for 21 CFR §1311.300

**Revenue Cycle Management (RCM):**
- Claims processing for Medicare, Medicaid, and private insurers
- PDPM (Patient-Driven Payment Model) support including "PDPM Coach" add-on
- Accounts receivable tracking
- Financial dashboards and reporting
- Census management and budgeting
- Trust fund management
- General Ledger/Accounts Payable module
- Billing optimization and collections workflows
- RCM Services (outsourced claims processing offering)

**Care Coordination & Transitions:**
- Secure messaging (Secure Conversations module)
- Hospital admission/readmission alerts (from Collective Medical acquisition)
- Electronic discharge summary exchange with hospitals
- Insurance coverage validation
- Resident status tracking and event calendar
- PAC Management tools for hospitals/health systems
- Connected Care Center — care coordination network

**Analytics & Reporting:**
- Performance Insights / Advanced Insights modules — clinical, financial, operational dashboards
- MDS Analytics
- CMS 5-star rating tracking
- Quality and compliance metrics
- Regulatory reporting (OASIS/MDS quality metrics)
- Market Insights — peer performance benchmarking against national averages
- Clinical alerts (pressure ulcers, fall risks)

**Senior Living-Specific:**
- Companion mobile app for staff (ADL documentation in under 30 seconds)
- Pharmacy Connect for medication order management
- Senior Sign (digital move-in paperwork)
- CRM for marketing/occupancy management
- Nutrition Management / Mealtime Solutions
- Document Manager
- Billing with resident-friendly statements

**Staffing & Operations:**
- Apploi Hire/Onboard (recruitment)
- Apploi Schedule (shift management)
- Automated Care Messaging

**Integrations & Interoperability:**
- HL7 interfaces, APIs, FHIR-based connectors
- 400+ marketplace integrations
- Lab and imaging ordering integration
- Pharmacy integration
- Device integration (blood pressure monitors, etc.)
- Virtual Health (telehealth) module

**Patient/Family Engagement:**
- Patient portal (View, Download, Transmit per (e)(1) certification)
- Clinician and family portals
- Automated care messaging to families

### Data & Content

Based on vendor documentation, product pages, and the de-identified data catalog, PointClickCare stores and manages the following types of data:

**Clinical Data:** Diagnoses, co-morbidities, allergies, vital signs (blood pressure, temperature, weight, etc.), immunizations, care plans, progress notes, encounter notes, nursing documentation, physician orders, treatment records, condition change documentation, wound care tracking records, infection control data, incident reports, clinical alerts, assessments (including MDS 3.0), therapy data, biomarkers, disease-specific assessments.

**Medication Data:** Medication orders, medication administration records (eMAR), drug regimens, prescription data (including controlled substances via EPCS), pharmacy orders, allergy alerts, drug interaction alerts, medication history.

**Financial/Billing Data:** Claims (Medicare, Medicaid, private insurance), accounts receivable, census data, trust fund records, PDPM scoring data, billing statements, collections data, general ledger/accounts payable, budgets.

**Administrative/Operational Data:** Staff scheduling, staffing records, recruitment/onboarding data, resident status, event calendars, insurance coverage information, digital move-in paperwork (Senior Sign), CRM/marketing data, facility-level data.

**Care Coordination Data:** Discharge summaries, transitions of care documents, hospital admission/readmission alerts, care manager notes, referral data, insurance validation data.

**Analytics/Reporting Data:** Quality metrics, CMS 5-star ratings, benchmarking data, OASIS/MDS quality measures, clinical quality measures (CQMs), operational performance metrics.

**The de-identified data catalog** (offered to life sciences companies) confirms the breadth of stored data: outcomes, biomarkers, diagnoses, co-morbidities, treatments, therapy, encounters, claims, MDS assessments, drug regimens, facility-level order data, HCP and pharmacy relationships. They claim "more clinical datapoints per patient than CMS, Registry, Ambulatory or Acute EMR datasets" with 10+ years of longitudinal data.

**Lab and imaging**: The platform has "Integrated Lab and Imaging" listed as a value package for SNFs, meaning lab and imaging orders and potentially results flow through the system — but specifics on how results data is stored vs. referenced externally were not detailed in vendor materials.

---

## Product: EHR for Practice Groups

CHPL ID: 11729

### What It Is

EHR for Practice Groups is PointClickCare's dedicated EHR offering for physician practice groups — typically practitioners who provide medical services to residents in skilled nursing and senior living facilities. This is a newer certified product (version 3, certified December 2025) that provides a practitioner-facing interface optimized for the workflows of physicians, nurse practitioners, and physician assistants who serve LTPAC populations. It is certified across 28 criteria — nearly identical to the core PointClickCare EHR, covering clinical data (a)(1)–(a)(5), (a)(12), (a)(14), transitions of care (b)(1)–(b)(3), patient portal (e)(1), CQM (c)(1), and FHIR APIs (g)(7), (g)(9), (g)(10).

This product appears to be closely related to the "Practitioner Engagement" module, which provides mobile and web access for practitioners to interact with PointClickCare's core EHR data. It is not a standalone EHR for general ambulatory practice — it is specifically designed for practice groups that serve the LTPAC population and need to interact with PointClickCare's core platform.

### Users & Market

The primary users are:
- **Physicians** serving SNF and senior living residents
- **Nurse Practitioners and Physician Assistants** providing care in LTPAC settings
- **Practice group administrators** managing documentation, billing, and value-based care arrangements

PointClickCare reports serving 2,000+ ambulatory clinics, though it's unclear how many specifically use the "EHR for Practice Groups" product vs. the broader platform. The product targets practice groups engaged in value-based care arrangements (Medicare Advantage SNPs, PACE, ACO REACH) where documentation quality and care coordination directly affect reimbursement.

### Modules & Functionality

Based on the product page, solution sheet, and certifications page:

**Clinical Documentation:**
- Automated workflows and auto-populated patient data for fast encounter documentation
- Single login access to the patient record (shared with the core PointClickCare EHR)
- Access to chart summaries including vitals, notes, lab results, medication history, progress notes
- Encounter note submission directly into the EHR

**Order Management:**
- Electronic signing of telephone and verbal orders
- Bulk order review
- Discharge order management
- ePrescribing with EPCS compliance
- Drug interaction alerts and order templates with auto-populated information

**Care Coordination:**
- Single patient record shared across the care continuum
- Communication and collaboration tools across care teams
- Support for care transitions

**Value-Based Care Support:**
- Data and reporting for value-based care arrangements
- Metrics tracking: readmission reduction, ED utilization, chronic disease management, patient satisfaction
- Revenue acceleration through improved documentation

**Security:**
- Multi-factor authentication across application access, clinical workflows, and SSO

### Data & Content

EHR for Practice Groups shares the same underlying patient record as the core PointClickCare platform. Practitioners access and contribute to the same clinical data — encounter notes, orders, prescriptions, vital signs, lab results, medication history, progress notes, chart summaries, and discharge information. The product adds the practitioner's documentation layer (encounter notes, orders, prescriptions) on top of the facility-based nursing and clinical documentation.

Given the shared data model, the data types stored are essentially the same as the core PointClickCare EHR described above, with particular emphasis on practitioner-generated content: encounter notes, orders (medications, labs, imaging), prescriptions (including controlled substances), and value-based care metrics.

The nearly identical certification criteria between this product and the core PointClickCare EHR (10246) — and the fact that they share the same EHI export documentation URL — strongly suggests these products share a common data platform.

---

## Research Notes

**Gaps and Uncertainties:**
- The exact boundary between what's in the "certified" EHR vs. add-on modules is unclear. The CHPL certification covers the core EHR, but the broader platform includes many modules (CRM, staffing, analytics) that may or may not be part of the certified product's data scope for EHI export purposes.
- Lab and imaging result storage specifics were not clearly documented — it's listed as an "Integrated Lab and Imaging" value package, but whether results are stored natively or referenced from external systems is not detailed.
- The relationship between "EHR for Practice Groups" and "Practitioner Engagement" is somewhat ambiguous — they appear to be closely related or overlapping products.
- PointClickCare's late-2025 launch of a "next-generation" senior living EHR with AI-powered analytics may represent a platform evolution that affects what data is stored.
- The American HealthTech acquisition (2024) brought another LTC EHR into the fold — it's unclear whether that product's data has been migrated into or integrated with the PointClickCare platform.

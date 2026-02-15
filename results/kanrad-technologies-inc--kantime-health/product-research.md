# Kanrad Technologies Inc — Product Research

Researched: 2026-02-15
Developer website: https://www.kantime.com

## Overview

Kanrad Technologies Inc was founded in 1997 as an IT consulting firm handling large-scale software projects for Fortune 500 companies. Around 2010, the company pivoted to a product-focused model and rebranded its post-acute care software as KanTime. The company is headquartered in the U.S. and led by CEO Sundar Kannan, COO Swami Nathan, and CTO Satheesh Kumar.

KanTime positions itself as "The #1 Home Health and Hospice Enterprise EMR Solution" and focuses exclusively on the post-acute care market — specifically home health, hospice, palliative care, pediatric home care, private duty home care, and consumer-directed (self-directed) services. Per their website, the platform serves over 912,000 patients, 210,000 users, has processed $12.9 billion in claims, and handles 70 million annual visits. SelectHub ranks KanTime #4 on its top 10 Home Health Software leaderboard. Competitors include Axxess, WellSky, MatrixCare, Alora Healthcare Systems, and Homecare Homebase. Revenue has been estimated at approximately $6.3 million (Kona Equity), suggesting a mid-size company rather than an enterprise vendor. The company holds HITRUST r2, SOC 2 Type 2, ONC Health IT, Surescripts, ACHC, and CHAP certifications/accreditations.

## Product: KanTime Health

CHPL IDs: 11219

### What It Is

KanTime Health is a cloud-based (web-based) enterprise EMR and agency management platform purpose-built for post-acute care organizations. It is a single integrated platform covering clinical, operational, financial, and HR functions — not a modular product where components are sold separately. The ONC-certified product covers the full KanTime platform; the certified criteria span clinical documentation (a)(1)-(a)(5), (a)(12), (a)(14)-(a)(15), transitions of care (b)(1)-(b)(3), patient access (e)(1), (e)(3), clinical quality measures (c)(1)-(c)(3), and FHIR APIs (g)(7)-(g)(10), indicating broad clinical EHR functionality.

The SED intended user description lists "Clinicians, Physicians, Nurses, Nurse Practitioners and Registered Nurses, Physician Assistants, Medical Assistants and Clinical Backoffice staff" — consistent with a comprehensive clinical and back-office platform.

### Users & Market

KanTime serves post-acute care agencies of varying sizes, from small home health agencies to large multi-location enterprises. The platform covers six distinct care types from a single system:

- **Home Health** — Medicare/Medicaid certified skilled home health agencies (launched 2012)
- **Hospice & Palliative Care** — end-of-life and comfort care providers (launched 2016)
- **Private Duty Home Care** — non-medical personal care services (launched 2010, the original product)
- **Pediatric Home Care** — specialized pediatric nursing and therapy services
- **Consumer-Directed / Self-Directed Care** — FMSA, F/EA, Agencies with Choice, FIs, FSEs, and Intermediary Service Organizations (launched 2018)

Their first client was Anova Home Health & Hospice (2012). Day-to-day users include field clinicians (nurses, therapists, aides) using mobile/tablet point-of-care documentation, office staff managing intake/referrals/scheduling, billing and coding staff, QA reviewers, HR/payroll administrators, and agency management using business intelligence dashboards.

The platform operates across virtually all U.S. states and Washington D.C., with EVV integrations covering state Medicaid aggregators nationwide.

### Modules & Functionality

Based on vendor website, product pages, partner listings, and third-party reviews, KanTime Health includes the following major modules and capabilities:

**Intake & Referral Management**
- Lead generation tracking through assessment, verification, and scheduling of first visit
- Referral tracking dashboard with partner integrations (CarePort, Cipher Health, Acclivity Health Solutions)
- Eligibility verification and prior authorization management
- Interactive dashboard with authorization alerts and deadline tracking

**Scheduling & Staffing**
- Advanced scheduling engine with drag-and-drop interface
- Clinician Search Wizard matching caregivers by qualifications, geography, certifications (e.g., Wound Vac, IV training), availability
- Split shift management across multiple payers/services
- Real-time patient and clinician calendar views
- Multi-discipline client calendars
- Ad hoc visit tracking (clock in/out for unscheduled visits)
- Late clock-in alerts
- Need-to-hire indicators

**Clinical Point-of-Care Documentation**
- Mobile/tablet documentation (Android and iOS) with offline/online capability
- Auto-generated 485 plans of care from SOC (Start of Care) assessments
- OASIS assessment integration with automated documentation linking to OASIS manual
- Hard stops and mandatory fields for compliance
- Vital signs, assessments, visit notes, treatment plans capture
- Autofill for repeated data
- Electronic signature capability
- Real-time audit tracking of documentation status

**E-Prescribing (KRx Module)**
- DEA-certified EPCS (Electronic Prescribing for Controlled Substances)
- Integration with Surescripts pharmacy network (nationwide)
- On-demand medication history retrieval (up to 1 year via Surescripts)
- Drug-to-drug and drug-allergy interaction checking via FirstDataBank
- 24/7 mobile prescription capability
- HIPAA compliant

**Order Tracking**
- Missing documentation tracking
- Physician order compliance monitoring
- Electronic physician order faxing with auto-mapping

**Quality Assurance**
- Active audit capabilities for real-time documentation tracking
- Compliance monitoring for state and federal regulations
- Standardized documentation enforcement

**IDT (Interdisciplinary Team) Management**
- Secure collaboration across all care roles
- Shared access to care plans and notes
- Streamlined IDT meeting workflow (particularly for hospice)
- HIPAA-compliant messaging for staff communication

**Hospice-Specific Features**
- Bereavement management with customized follow-up alerts
- Volunteer management tracking (5% volunteer service requirement)
- Hospice benefit period management
- HIS (Hospice Item Set) data collection
- Non-billable service tracking

**Billing & Revenue Cycle Management**
- Full billing lifecycle: charge entry, claim submission, remittance, accounts receivable
- Automated 837 batch claim generation
- Payer-specific billing rules to reduce errors
- Secondary payer processing
- Denial management and timely filing tracking
- Direct clearinghouse interfaces (Waystar, Ability)
- Advanced financial reporting across branches and service lines
- Integration with multiple billing/payment partners (Availity, Change Healthcare, Claim MD, HHAeXchange, Sandata)

**HR & Payroll**
- Payroll as a Service (PaaS) integrated with scheduling
- Timesheet management with clinician lock pay period
- Pay rate dispute resolution workflow
- Payment preview system
- Employee credential/license expiration alerts
- Benefits tracking
- Integration with external payroll providers (ADP, Accufund, Americas Back Office, Apex, Asure, BambooHR, BBSI, Ceridian)

**Electronic Visit Verification (EVV)**
- GPS and telephony-based visit verification
- Cures Act compliant
- Integrated with state aggregators across all 50 states + D.C.
- Proprietary EVV plus integrations with CellTrak, CareBridge

**Business Intelligence (KanTime+)**
- Clinical, financial, and operational KPI dashboards
- Drill-down analytics for management
- Multi-branch/multi-location reporting
- Benchmarking integration (Activated Insights partner)

**Additional Integrations**
- Pharmacy: AvantumRx, BetterRx (particularly for hospice)
- Medical supplies/DME: Cardinal Health, Capstone HME
- Telehealth capabilities (referenced in partner categories)
- CRM and referral management partners

### Data & Content

Based on the modules and features described above, KanTime Health stores and manages the following categories of data:

**Patient/Clinical Data:**
- Patient demographics and contact information
- Clinical assessments (including OASIS assessments for home health, HIS for hospice)
- Plans of care (auto-generated 485s)
- Visit notes and point-of-care documentation
- Vital signs
- Treatment plans
- Medication lists and prescribing history (via Surescripts integration, up to 1 year)
- Prescription records (including controlled substances via EPCS)
- Drug interaction and allergy data (via FirstDataBank)
- Physician orders
- Care coordination notes and IDT meeting documentation
- Bereavement records (hospice)

**Administrative/Operational Data:**
- Referral and intake records
- Scheduling data (visits, shifts, caregiver assignments)
- Authorization and eligibility records
- Electronic visit verification data (GPS coordinates, timestamps, telephony records)
- QA audit trails
- HIPAA-compliant staff messaging

**Financial Data:**
- Billing claims (837 format)
- Remittance and payment records
- Accounts receivable
- Denial tracking
- Payer information and billing rules
- Financial reports across branches/service lines

**HR/Workforce Data:**
- Employee/caregiver records
- Credentials and license expiration tracking
- Timesheets and payroll data
- Benefits information
- Pay rate records

**Analytics/Reporting Data:**
- Clinical, financial, and operational KPIs
- Benchmarking data
- Multi-location aggregated reporting

**Notable observations:**
- KanTime is a comprehensive all-in-one platform — billing, HR/payroll, scheduling, clinical documentation, e-prescribing, and EVV are all integrated rather than separate products. This means the EHI export should theoretically cover all of these data domains.
- The Surescripts integration for medication history and e-prescribing means prescription and medication data flows through the system.
- The vendor website does not prominently mention lab ordering/results, diagnostic imaging, or patient portal messaging as features — these are less typical for home health/hospice settings but the (e)(1) certification for patient access/VDT suggests some patient-facing data access exists.
- The (a)(14) certification criterion (implantable device list) is notable for a home health/hospice product and suggests the system tracks implantable device information.
- The (a)(12) certification (family health history) is also somewhat unusual for post-acute care and indicates this data type is supported.

---

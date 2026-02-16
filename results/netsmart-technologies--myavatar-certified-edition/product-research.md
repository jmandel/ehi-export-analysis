# Netsmart Technologies — Product Research

Researched: 2026-02-16
Developer website: https://www.ntst.com/

## Overview

Netsmart Technologies is the dominant health IT vendor in the behavioral health and human services sector. Founded in 1992 (with technology origins dating to 1968 through its 1994 acquisition of Creative Socio-Medics), the company is headquartered in Overland Park, Kansas and has approximately 2,600 employees. Netsmart reports that over 754,000 care providers across the U.S. use its platform technology, including 181 Certified Community Behavioral Health Clinics (CCBHCs) in 37 states. The company was described as the largest IT provider in behavioral healthcare by 2005.

Netsmart has been through several rounds of private equity ownership: Bessemer Venture Partners and Insight Venture Partners (2006), Genstar Capital (2010), GI Partners and Allscripts joint venture ($950M, 2016), and then GI Partners and TA Associates (2018, after buying out Allscripts' stake). As of late 2025, GI Partners and TA Associates were reportedly launching a sale process in early 2026, with the company valued at approximately $5 billion including debt (~$250M EBITDA).

Netsmart's product portfolio spans multiple EHR platforms under the "CareFabric" umbrella: **myAvatar** (behavioral health), **myEvolv** (addiction, autism, behavioral health, foster care), **myUnity** (post-acute care — home health, hospice, senior living, skilled nursing), **TheraOffice** (physical therapy), **GEHRIMED** (geriatric care), and **myInsight** (public health). They also offer myHealthPointe (consumer/patient portal), CareConnect (interoperability engine), revenue cycle management, IT managed services, workforce management, telehealth, and Bells AI (ambient clinical documentation assistant). Each of these EHR platforms serves different care communities and has its own ONC certification.

## Product: myAvatar Certified Edition

CHPL IDs: 11575

### What It Is

myAvatar is a behavioral health electronic health record (EHR) specifically designed for organizations providing behavioral health and addictions treatment services in community-based, residential, and inpatient settings. It was the first behavioral health software system to earn both Complete EHR Ambulatory and Complete EMR Inpatient certifications from the Drummond Group.

The certified module (myAvatar Certified Edition, version 5, certified 2024-12-27) is broadly certified across 40+ ONC criteria covering clinical data management (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); transitions of care (b)(1)–(b)(3); patient portal/view-download-transmit (e)(1); public health reporting (f)(1)–(f)(3), (f)(5); FHIR APIs (g)(7), (g)(10); and Direct messaging (h)(1). This is a comprehensive certification profile indicating a full-featured clinical EHR, not a narrow specialty module.

myAvatar is part of Netsmart's broader CareFabric ecosystem, which includes the myHealthPointe patient portal, CareConnect interoperability engine, revenue cycle management services, and the Bells AI documentation assistant. The certified module is the core EHR, but the full product experience includes these surrounding components.

### Users & Market

**Primary users**: Clinicians (psychiatrists, psychologists, therapists, counselors, social workers), nurses, front desk/scheduling staff, billing administrators, pharmacy staff, and executive management.

**Clinical settings**: Community mental health centers, psychiatric hospitals, substance abuse/addiction treatment programs, methadone clinics, CCBHCs, FQHCs with behavioral health programs, residential treatment facilities, autism service providers, foster care organizations, state mental health systems, and managed care organizations.

**Scale**: Netsmart claims over 18,000 customers across its product lines and 754,000+ users. myAvatar is one of several EHR platforms; the specific myAvatar customer count is not broken out, but it is described as the flagship behavioral health product. Netsmart has been ranked #1 EHR vendor for behavioral health by Black Book Research.

**Deployment**: Available as either on-premise or cloud-based (SaaS). The SaaS implementation was recently migrated to AWS.

**Notable customer types**: CCBHCs, state behavioral health agencies (e.g., Sacramento County BHS, Yolo County), and large behavioral health organizations like AltaPointe Health. Customer distribution skews toward Hospital & Health Care (28%), Nonprofit Organization Management (10%), Mental Health Care (8%), and Individual & Family Services (7%).

### Modules & Functionality

myAvatar comprises more than 20 modules (per vendor materials and third-party review sites). The following are documented in vendor feature pages, review sites, and certification materials:

**Clinical Documentation & Records**
- Patient/client records and demographics
- Progress notes (clinical documentation)
- Treatment planning with care team approval and compliance tracking
- Clinical assessments and screening tools
- Medical Note for Psychiatry (integrates lab results, vitals, and medication history)
- Specialty content for primary care visits, pediatrics, and women's health (for integrated care settings)
- Chart summarization pulling data across care settings (AI-powered)
- Ambient listening for clinical documentation (Bells AI integration)

**Medication Management & Pharmacy**
- Closed-loop medication management: order entry → pharmacy verification → dispensing → administration
- Integration with automated dispensing machines
- E-prescribing (via Surescripts network)
- Medication history retrieval (Rx Fill data via Surescripts)
- Unified medication lists shared across providers
- Medicare pharmacy billing support

**Orders & Lab**
- Computerized physician order entry (CPOE) for lab tests, medications, diet, and seclusion/restraint
- Lab results viewing and integration into clinical notes

**Scheduling**
- Patient/group appointment scheduling
- Group appointment management specific to behavioral health (group therapy sessions)
- Detoxification scheduling workflows

**Billing & Financial**
- Integrated billing for behavioral health (complex long-term intensive care episodes)
- Automated electronic remittance processing and denial management
- Claim generation with job scheduling
- Value-based reimbursement and shadow billing
- Utilization management and eligibility verification
- Integrated credit card payments
- Revenue cycle management supporting FQHC billing requirements
- Collection automation services

**Compliance & Reporting**
- Compliance monitoring with clinician alerts
- HIPAA and 42 CFR Part 2 compliance (behavioral health-specific privacy)
- Consent management and provider permissions
- Measures reporting and dashboards for UDS, PCMH, MIPS
- CCBHC regulatory reporting support
- Public health reporting (immunization, syndromic surveillance, electronic case reporting per certified criteria)
- Seclusion and restraint documentation and tracking

**Interoperability & Data Exchange**
- CareConnect Integration Engine: HL7, FHIR, and Direct Secure Messaging
- CareConnect Inbox: secure messaging for exchanging CCDs, lab results, treatment plans
- Health Information Exchange (HIE) connectivity via Carequality (4,200+ hospitals, 600,000+ providers)
- FHIR-based APIs (g)(7) and (g)(10) certified
- Netsmart QHIN (Qualified Health Information Network) designation
- Closed-loop referral management
- Datavant EHR integration available

**Patient/Consumer Portal (myHealthPointe)**
- Secure access to clinical information and lab results
- Appointment scheduling and reminders
- Medication refill requests
- HIPAA-compliant secure messaging with care team
- Assessment completion and electronic consent signing
- Personal information updates
- Telehealth appointment launch

**Operational & Analytics**
- Role-based dashboards for clinicians, administrators, and executives
- Key performance indicator tracking
- Population risk assessment
- Social determinants of health (SDoH) tracking and care coordination
- Inventory management and accounting (for inpatient facilities)
- Quick Action features for rapid data capture
- Tablet-enabled mobile workflows

**Behavioral Health-Specific Workflows**
- Detoxification management
- Emergency detention tracking
- Seclusion and restraint management
- Group therapy documentation
- Care team approval workflows
- Recovery-focused clinical decision support
- Addiction treatment workflows

### Data & Content

Based on the documented features above, myAvatar stores and manages a broad range of data types:

**Clinical data**: Patient demographics, clinical assessments, progress notes, treatment plans, problem lists, diagnoses, vitals, lab results, medication lists and history, allergy information, immunization records, clinical documents (CCDs), and psychiatry-specific medical notes integrating labs/vitals/medications.

**Medication/pharmacy data**: Prescription orders, e-prescribing transactions (via Surescripts), pharmacy verification and dispensing records, medication administration records, medication history from external sources, and automated dispensing machine interactions.

**Behavioral health-specific data**: Seclusion and restraint documentation, detoxification records, group therapy session records, treatment plan approvals, compliance tracking records, 42 CFR Part 2 consent management records, emergency detention records, and recovery/outcome measures.

**Financial/billing data**: Claims, remittance advice, denial records, eligibility verification, utilization management data, credit card payment records, shadow billing data, and FQHC-specific billing data.

**Scheduling data**: Individual and group appointments, appointment history, reminder records.

**Portal/consumer data**: Patient-reported assessments, secure messages between patients and care teams, consent signatures, personal information updates, medication refill requests.

**Interoperability/exchange data**: Transition of care documents (CCDs), Direct secure messages, FHIR-based data exchanges, referral records, and HIE transaction logs (6.5+ billion transactions processed since 2018 across the Netsmart network).

**Public health reporting data**: Immunization data, syndromic surveillance data, electronic case reports.

**Administrative data**: User access logs, audit trails, consent records, provider permissions.

The vendor website does not mention standalone imaging/radiology capabilities, which is unsurprising for a behavioral health-focused EHR. The dental EHR integration is mentioned for integrated care settings but appears to be a separate integration rather than native dental charting within myAvatar. Dietary orders are mentioned for inpatient settings but detailed dietary/nutrition documentation capabilities are not elaborated.

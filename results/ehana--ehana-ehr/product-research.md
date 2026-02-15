# eHana — Product Research

Researched: 2026-02-14
Developer website: https://www.ehana.com/

## Overview

eHana is a small, privately held software company that builds a cloud-based EHR specifically for behavioral health and human service organizations. Founded in September 2000 in Honolulu, Hawaii, the company is now headquartered in Boston, Massachusetts. It is 100% independent and founder-owned, with approximately 28–29 employees and an estimated $6.1 million in annual revenue (per ZoomInfo/RocketReach). Despite its small size, eHana has a strong footprint in Massachusetts: over 10,000 monthly active users across 900+ sites statewide, serving 150,000+ clients. The company powers 23 of 27 MassHealth Community Partners and serves 56% of Adult Community Clinical Services (ACCS) clients in Massachusetts. eHana is an associate member of the Association for Behavioral Healthcare (ABH) of Massachusetts.

The company's name derives from Hawaiian — "hana" means business/work and "ohana" means family. eHana describes itself as still feeling like a startup with an agile culture, despite being over two decades old. The company appears to have no acquisition history and no parent company.

## Product: eHana EHR

CHPL ID: 10200
CHPL Product Number: 15.04.04.2594.eHan.19.00.1.191206
Version: v2019-MU
Certification Date: 2019-12-06

### What It Is

eHana EHR is a 100% cloud-based, web-delivered (SaaS) electronic health records platform purpose-built for behavioral health and human service provider organizations. It is the company's sole product platform, though it has been extended with a Care Management module for Massachusetts Community Partners and a specialized CBHC (Community Behavioral Health Center) configuration. The certified module appears to be the core product itself, not a subset.

The system is ONC-certified for ambulatory settings with a broad set of criteria: clinical data management (a)(1)–(a)(5), (a)(12), (a)(14)–(a)(15); transitions of care (b)(1)–(b)(2); patient portal/view-download-transmit (e)(1), (e)(3); clinical quality measures (c)(1)–(c)(3); public health reporting (f)(1), (f)(5); and FHIR APIs (g)(7), (g)(10). It also holds (h)(1) for direct messaging.

The EHR is hosted on IBM-managed infrastructure with bank-level encryption and HIPAA-certified hosting. It supports Windows, Mac, and common browsers (Edge, Chrome, Firefox, Safari) plus mobile devices (iPad, Android, Surface) without plugins or installation.

### Users & Market

**Primary users**: Clinicians, case managers, billing staff, front-desk staff, supervisors, and administrators at behavioral health and human services organizations. The intended users per CHPL metadata are "Ambulatory Users."

**Customer base**: Predominantly Massachusetts-based nonprofit behavioral health and human service providers. Named customers include Bay Cove Human Services, Eliot Community Human Services, JRI, and OpenSky Community Services. eHana serves 50+ Massachusetts nonprofit providers.

**Practice disciplines** (per vendor website): Outpatient mental health, SUD/Addiction, ESP/MCI (Emergency Services Program/Mobile Crisis Intervention), CCS (Continuous Clinical Support), CBHI/CSA/IHT/TM/ICC (Children's Behavioral Health Initiative programs), I/DD (Intellectual/Developmental Disabilities), Residential Services, Community-Based Programs, Justice-Involved Services, Elder Services, and Housing & Homelessness.

**Scale**: 10,000+ monthly active users writing 600,000+ documents per month across 250,000+ patient enrollments.

**Market position**: Small, niche vendor with deep Massachusetts behavioral health market penetration. Not a national-scale EHR. The system is highly specialized — it does not appear to target general medical, hospital, or surgical settings.

**Reviews**: Limited external reviews. Capterra shows a "fair" 60% satisfaction rating based on only 2 reviews. Noted strengths include organized records and thorough documentation; weaknesses include limited paperwork customization, no recurring appointment scheduling, and slow page loading. The very small review sample makes these unreliable indicators.

### Modules & Functionality

Based on the vendor's features page, CBHC resource hub, and third-party descriptions, eHana EHR includes the following functional areas:

**Clinical Record Management**
- Integrated multi-program client demographics and clinical record
- Support for diverse program types within a single client record (e.g., a client in both outpatient and residential programs)
- Electronic signatures on clinical documentation
- Incident logging and reporting
- Customizable documentation templates
- Service documentation with date/time, service type, location, program code, and modifiers

**E-Prescribing**
- Integrated e-prescribing including PDMP (Prescription Drug Monitoring Program) integration
- Controlled substance e-prescribing (EPCS)
- ScriptRX compatibility

**Scheduling & Front Desk**
- Client and employee scheduling with calendar syncing
- Front-desk check-in module with SMS alerts
- Appointment management (though recurring appointments reportedly not supported per reviews)

**Billing & Revenue Cycle**
- Automated claims generation directly from clinical notes
- HIPAA-compliant 837/835 processing
- Eligibility management and verification
- Comprehensive billing dashboards
- Support for complex behavioral health billing rules
- Zero-paid and bundled claims (eHana has transmitted over 2 million zero-paid claims — relevant to Massachusetts behavioral health Medicaid billing)

**Care Coordination & Messaging**
- Cross-program notifications and messaging
- Secure messaging for staff collaboration
- DIRECT-capable messaging for HIE integration
- Patient/client portal with secure communication, appointment features, and access to records

**Staff & Workforce Management**
- Employee demographics tracking
- Supervision tracking
- Productivity monitoring
- Timesheets
- Customizable document signoff workflows
- Role-, site-, and program-based organizational controls

**Compliance & Quality**
- Automated quality assurance processes
- Utilization review workflows
- Multidisciplinary team documentation review
- Chart-completeness management
- Read-only auditor roles
- Full activity/audit logging
- CANS (Child and Adolescent Needs and Strengths) integration

**Document Management**
- Scanning and filing with OCR integration
- Scanned documents embedded in client charts
- Password-protected "chart extracts" via PDF export

**Analytics & Reporting**
- Role-specific dashboards with real-time data widgets
- Business intelligence and cloud-based analytics
- Configurable reports for strategic planning

**Interoperability**
- HL7 messaging
- HIPAA EDI
- CCD/CCR document exchange
- DIRECT messaging
- FHIR API (SMART on FHIR)
- SAML 2.0 authentication for SSO
- Integration with Massachusetts laboratories
- Integration with Collective Medical event notification systems
- Integration with Massachusetts ACOs

**Telehealth**
- Integrated telehealth capabilities (mentioned in third-party descriptions)

### Data & Content

Based on the features and workflows described above, eHana EHR stores and manages:

**Client/Patient Data**: Multi-program client demographics, enrollment information across programs, clinical records spanning the care continuum. Given the 250,000+ patient enrollments figure, the system manages substantial patient identity and demographic data.

**Clinical Documentation**: Service notes, clinical assessments, treatment plans, incident reports, progress notes, CANS assessments, and other behavioral health clinical documentation. The 600,000+ documents per month figure indicates high-volume clinical note generation.

**Medication Data**: Prescription data via integrated e-prescribing, including controlled substance prescriptions and PDMP queries.

**Billing/Claims Data**: Claims (837), remittance (835), eligibility data, billing rules, and financial dashboards. The zero-paid and bundled claims capability is specific to Massachusetts behavioral health Medicaid billing.

**Scheduling Data**: Client appointments and employee scheduling.

**Staff/HR Data**: Employee demographics, supervision records, productivity metrics, timesheets, and credentials.

**Scanned Documents**: OCR-processed scanned documents filed into client charts.

**Messaging/Communication**: Secure messages between staff and with patients via the client portal; DIRECT messages for HIE.

**Audit/Compliance Data**: Activity logs, quality assurance records, utilization review data, chart completeness tracking.

**What's unclear**: The website does not specifically mention lab results storage (beyond lab integration), allergy lists, problem lists, or vital signs as distinct features — though these are implied by ONC certification criteria (a)(1) CPOE, (a)(3) CPOE for diagnostic imaging, (a)(5) demographics, (a)(14) implantable device list. The system's behavioral health focus means some standard medical EHR data types (e.g., surgical history, detailed vital signs) may be less emphasized than clinical notes and service documentation, though they are likely present given the certified criteria. The vendor's materials are more focused on behavioral health workflows and program management than on granular clinical data fields.

**EHI Export**: Per the certification documentation page, EHI export is available in XML format using Consolidated-Clinical Document Architecture (C-CDA) standards aligned with HL7 specifications. This is notable — C-CDA is a clinical summary format and may not capture all data types (e.g., billing, staff, scanned documents, audit logs).

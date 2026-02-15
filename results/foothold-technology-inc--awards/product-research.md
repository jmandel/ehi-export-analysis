# Foothold Technology, Inc. — Product Research

Researched: 2026-02-15
Developer website: http://footholdtechnology.com

## Overview

Foothold Technology, Inc. is a New York City-based software company that builds electronic health record and case management software for the **human services and behavioral health** sector. Founded in 2000 by three social service agencies that needed case management software, Foothold has grown to serve over 1,000 provider agencies across 28 states plus Guam and Puerto Rico. The company has a particularly strong presence in New York and New Jersey, where it serves more agencies than any other EHR vendor in the behavioral health/human services space.

In 2017, Foothold was acquired by **Alpine Software Group (ASG)**, a division of private equity firm Alpine Investors. In July 2021, ASG launched **Radicle Health** as an umbrella brand grouping several human services software companies: Foothold Technology (behavioral health EHR + HMIS), Exym (behavioral health EHR, California-focused), KCare/extendedReach (child & family welfare), Link2Feed (food bank/poverty relief), SaraWorks (client communication, joined 2024), and Stabilify (child welfare). Tyler Hoffman serves as CEO of both Foothold Technology and as Group CEO of Radicle Health. The CHPL contact email (jpalmer@radicle-health.com) confirms the corporate relationship. Each company maintains its own brand and product under the Radicle Health umbrella. This is a classic PE buy-and-build strategy in vertical human services software.

Foothold was formerly a Certified B Corporation and has described itself as achieving "one of the highest scores ever seen" in HIPAA security testing. Estimated annual revenue is in the $5–25M range (~$15.8M per one estimate). The company has approximately 36–200 employees (sources vary, likely reflecting growth under Radicle Health).

## Product: AWARDS

CHPL ID: 9267 (`15.04.04.1500.AWAR.03.00.1.171220`)

### What It Is

AWARDS is a **web-based EHR and case management system purpose-built for nonprofit human services and behavioral health organizations**. It is not a traditional ambulatory or hospital EHR — its primary users are community-based behavioral health providers, homeless services agencies, residential programs, and developmental disability service providers. A key distinguishing feature: AWARDS is described as the **only record-keeping system federally certified as both a Behavioral Health EHR and a Homeless Management Information System (HMIS)** — the latter being a HUD-mandated data system for homeless services.

The certified product is the full AWARDS platform — it is not a module of a larger system. However, some features (e-prescribing, e-labs, business intelligence) are sold as add-on modules. The product is cloud/SaaS-hosted (the help center is on Zendesk at awards1.zendesk.com, and a demo database domain demodb.footholdtechnology.com was observed).

The ONC certification is broad, covering clinical data capabilities (a)(1)–(a)(5), (a)(12), (a)(14), transitions of care (b)(1)–(b)(3), patient portal (e)(1), FHIR API (g)(7), (g)(9), (g)(10), clinical quality measures (c)(1)–(c)(3), immunization registry reporting (h)(1), and a full security suite. This breadth reflects a product that spans clinical, administrative, and interoperability functions.

### Users & Market

**Target users**: Staff at nonprofit human services agencies — clinicians (psychiatrists, therapists, social workers, counselors), case managers, program directors, billing staff, administrative personnel, and agency leadership. The SED intended user description is simply "Varied," reflecting the breadth of user roles.

**Clinical settings and service verticals**:
- Mental health (outpatient, residential, community-based)
- Alcohol and substance use disorder treatment
- Homeless services and supportive housing
- Developmental disabilities / intellectual disabilities (I/DD)
- Home and Community Based Services (HCBS)
- Day habilitation programs
- Supported employment services
- Youth and family services
- Senior services
- Employment and training programs
- Veterans services

**Scale**: 1,000+ provider agencies across 28 states plus territories. The HMIS module alone is deployed at 50+ HUD Continua of Care around the country. Strongest presence in New York and New Jersey.

**Notable customers/case studies**:
- **BRC** (NYC homelessness outreach — 7,500 monthly contacts)
- **Hudson Guild** (NYC mental health services)
- **MHY Family Services**
- **NYC Department of Homelessness** (HMIS deployments)
- **Goodwill Industries** (referenced in search results)
- **Mental Health Association of Columbia-Greene Counties, NY**
- **CARES of NY** (collaborative HMIS)

**Competitive landscape**: Competes with Netsmart, Qualifacts/Credible, Therapy Partner, and other behavioral health EHR vendors. AWARDS' differentiator is its dual EHR + HMIS certification and its focus on multi-program human services agencies rather than clinical-only behavioral health practices.

### Modules & Functionality

The following modules and features were found described across vendor materials, product pages, customer case studies, and third-party listings:

**Core Clinical/Case Management**:
- **Treatment Plans & Case Management**: Multi-service, connected caregiving coordination across programs. Supports treatment planning workflows for behavioral health and human services.
- **Service Documentation**: Workflow-consistent clinical documentation for staff, tied to specific services and programs.
- **Progress Notes**: Clinical progress notes with customizable templates.
- **Intake & Assessment**: Patient health status determination, medical history, conditions. Supports intake workflows for new clients/consumers.
- **Medication Management**: Medication administration records (MARs), medication history, medication allergy tracking, alerts.
- **Vital Signs**: Clinical vital signs tracking.
- **Problem Lists**: Diagnosis and problem tracking (certified (a)(3)).
- **Demographics**: Patient/client demographics capture (certified (a)(5)).
- **Family Health History**: Certified (a)(12).

**HMIS Module** (HUD-Compliant):
- Client demographics and contact information
- Housing status and history
- Homelessness episodes tracking
- Services provided documentation
- Income and benefits tracking
- Health insurance status
- Disabilities documentation
- Domestic violence indicators
- Program entry/exit data
- HUD Universal Data Elements
- CoC, ESG, PATH, SSVF reporting compliance

**Administrative**:
- **Billing Integration**: Billing tied directly to service documentation; automated billing workflows. This is built into the core platform, not a separate product.
- **Facilities Maintenance**: Building/property management for residential programs — a module reflecting AWARDS' focus on residential and housing providers.
- **Human Resources**: Staff management and HR functions.
- **Scheduling & Alerts**: Calendar events, task tracking, color-coded alerts.
- **Audit Reports**: Compliance and audit trail reporting.

**Reporting & Analytics**:
- **ReportBuilder**: Custom ad-hoc reports using any data field in the system.
- **DataBridge**: Direct database querying capability for ad-hoc reporting.
- **InSights**: Business intelligence add-on for advanced analytics.
- **100+ pre-built reports** geared to behavioral health and I/DD providers.
- **ExportBuilders**: Data export functionality (this is the mechanism referenced in the EHI export documentation URL).

**Configurable Tools**:
- **FormBuilder**: Agencies can build custom forms and attach them to intake, discharge, progress notes, and other workflows. This is significant — it means AWARDS stores agency-defined custom data structures beyond its standard fields.
- **Configurable workflows**: Programs can be set up independently or globally across agencies.

**Add-On Modules/Services**:
- **E-Prescribing**: Electronic prescribing including controlled substances (EPCS), with IMO (Intelligent Medical Objects) integration for medication coding.
- **E-Labs**: Electronic lab orders to LabCorp, Quest, and hundreds of other labs; results integration back into the chart.
- **Patient Portal**: Patient-facing access to health information (certified under (e)(1)). Limited details found on the portal's specific functionality.

**Interoperability**:
- **Health Information Exchange (HIE)** participation via IHE-certified protocols.
- **C-CDA document creation and reconciliation** (certified (b)(1)–(b)(3)).
- **FHIR API** (certified (g)(7), (g)(9), (g)(10)). No public developer documentation or API endpoint details were found.
- **Immunization registry reporting** (certified (h)(1)).
- **Clinical quality measure recording, export, and reporting** (certified (c)(1)–(c)(3)).
- Partnership with **IMSNY** (Interoperability Collaborative for Managed Service in New York) for behavioral health data sharing.
- Integration with **Hixny** (New York state HIE).
- InterSystems-based interoperability engine.

Sources: Foothold Technology website (footholdtechnology.com), product detail pages on resources.footholdtechnology.com, Alpine SG portfolio page, Capterra/GetApp search snippets, press releases, and HMIS proposal documents.

### Data & Content

Based on described features, certified criteria, and observed modules, AWARDS manages the following categories of data:

**Clinical health records**:
- Patient/client demographics and contact information
- Problem lists / diagnoses
- Medication lists and medication allergy lists
- Medication administration records (MARs)
- Prescription data (via e-prescribing module)
- Lab orders and lab results (via e-labs module)
- Vital signs
- Clinical progress notes
- Treatment plans
- Assessment data (intake, ongoing, discharge)
- Immunization records
- Family health history
- Clinical quality measure data

**Case management and program data**:
- Service documentation (tied to specific programs and billing)
- Program enrollment, participation, and discharge records
- Scheduling and calendar events
- Multi-program coordination data (clients may be enrolled in multiple programs simultaneously)

**HMIS/housing data** (HUD-mandated elements):
- Housing status and history
- Homelessness episodes
- Income and benefits information
- Health insurance status
- Disability information
- Domestic violence indicators
- HUD Universal Data Elements (a standardized set of ~30+ data fields mandated by HUD)

**Administrative and operational data**:
- Billing records and claims (integrated with service documentation)
- Staff/HR records
- Facility maintenance records (for residential programs)
- Audit trails and compliance logs

**Custom/agency-defined data**:
- Custom forms built via FormBuilder (these can contain any fields the agency defines)
- Custom assessments and instruments

**Interoperability and exchange data**:
- C-CDA documents (sent and received)
- HIE exchange records
- FHIR resources (US Core profiles per (g)(10))

**Reporting data**:
- Saved reports and report configurations
- DataBridge queries
- ExportBuilder configurations and exports

**Key observations for EHI export assessment**:
1. The **FormBuilder** custom forms are a significant data source — agencies can define arbitrary data structures, and all that data would need to be exportable.
2. The **HMIS data** is distinctive to this product — housing status, homelessness episodes, income, benefits, domestic violence indicators are not standard EHR data fields and may or may not be covered by standard export mechanisms.
3. The **facilities maintenance** module stores data about buildings/properties, which is unusual for an EHR.
4. **Billing is integrated**, not separate — so billing/claims data is part of the product and should be in scope for EHI export.
5. The product serves clients enrolled in **multiple programs simultaneously**, so program-level data structures may be complex.

**Gaps in research**:
- The Foothold Technology website is heavily JavaScript-rendered, making direct content extraction from most pages difficult. Search engine snippets and cached content provided the bulk of useful information.
- No detailed description of the **Patient Portal's** specific features was found beyond the fact that it exists and is certified for (e)(1).
- No public **FHIR API developer documentation** was found.
- **Pricing** is not publicly disclosed.
- The specific data model and database structure are not documented publicly.

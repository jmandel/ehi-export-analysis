# The Echo Group (Ensora Health) — Product Research

Researched: 2026-02-16
Developer website: https://ensorahealth.com/product/echovantage/

## Overview

The Echo Group is a behavioral health EHR vendor founded in 1980 (some sources say 1981) and headquartered in Conway, New Hampshire, with additional offices in California, North Carolina, and Ohio. In November 2022, Therapy Brands — a private-equity-backed health IT company focused on mental, behavioral, and rehabilitative therapy — acquired The Echo Group. Therapy Brands subsequently rebranded to **Ensora Health** in early 2025, unifying its portfolio of therapy-focused software products under a single brand.

Ensora Health's broader portfolio includes TheraNest (mental health practice management), Fusion (PT/OT/speech therapy practice management), and EchoVantage. The Ensora parent describes serving "over 30,000 therapy practices" across its entire portfolio, though it's unclear how many of those specifically use EchoVantage versus other Ensora products.

EchoVantage is specifically positioned for **community behavioral health agencies** — a distinct market from solo/small-group private practices (which TheraNest targets). EchoVantage serves organizations ranging from small community behavioral health agencies to comprehensive enterprise-wide organizations, including mental health clinics, substance use recovery (SUR) centers, intellectual and developmental disabilities (I/DD) services, drug and alcohol centers, crisis intervention departments, foster care, residential care, correctional health facilities, and county-level behavioral health programs.

## Product: EchoVantage

CHPL ID: 11129

### What It Is

EchoVantage is a **web-based, integrated EHR, billing, and practice management platform** purpose-built for behavioral healthcare. Its signature feature is the **Visual Health Record (VHR)** — a graphical timeline interface that presents clinical information (progress notes, medications, assessments, treatment plans) along a visual continuum of care, showing events in relationship to each other to support clinical understanding.

The certified product appears to be the complete EchoVantage platform, not a module of something larger. It is available as both cloud-based and on-premise deployment. Within Ensora Health's portfolio, EchoVantage is the product aimed at larger community behavioral health organizations, whereas TheraNest serves smaller private practices and Fusion serves rehab therapy — these are distinct products, not modules of EchoVantage.

The certified criteria cover clinical documentation (a)(3), (a)(5), (a)(12), (a)(14), (a)(15); transitions of care (b)(1); FHIR APIs (g)(7), (g)(10); and direct messaging (h)(1). Notably absent from certification are CPOE criteria (a)(1)-(a)(2), drug interaction checking (a)(4), lab results (a)(9), patient portal/VDT (e)(1), and public health reporting (f) criteria — consistent with EchoVantage being a behavioral health system rather than a general ambulatory EHR.

### Users & Market

**Target organizations:**
- Community mental health centers/agencies (CMHCs)
- Substance use recovery / drug and alcohol treatment centers
- Intellectual and developmental disabilities (I/DD) service providers
- Crisis intervention and prevention departments
- Foster care and residential care programs
- Correctional health facilities
- County behavioral health programs

**Day-to-day users include:**
- **Clinicians/therapists** — for clinical documentation, treatment planning, assessments, progress notes
- **Prescribers** — for e-prescribing (via DrFirst integration)
- **Billing staff** — for claims submission, eligibility verification, payment processing
- **Administrators** — for scheduling, workflow configuration, compliance
- **Executives/managers** — for reporting dashboards, productivity metrics, financial oversight
- **Supervisors** — for reviewing staff activity, caseloads, and performance

**Market position:** EchoVantage occupies a niche in the community behavioral health market — larger and more complex organizations than solo/small-group practices (which use products like TheraNest) but generally not hospital systems. The Echo Group has been in this space since the early 1980s, giving it deep domain expertise. Specific customer counts for EchoVantage are not publicly disclosed. Third-party review sites show limited review volume (roughly 10-15 reviews on sites like Capterra and Crozdesk), suggesting a relatively small but specialized user base. The product has a user satisfaction rating of approximately 86% based on limited reviews.

No specific notable customer case studies were found publicly available.

### Modules & Functionality

Based on vendor materials, press releases, and third-party review sites, EchoVantage includes the following functional areas:

**Clinical / EHR:**
- **Visual Health Record (VHR):** Graphical timeline showing all clinical events — progress notes, medications, assessments, treatment plans — in chronological relationship to each other
- **Clinical Intelligence Engine:** Decision-support tool that helps therapists identify treatment approaches and connect treatment plans to intended outcomes
- **Treatment Plans:** Creation and tracking of behavioral health treatment plans with outcome linkage
- **Progress Notes:** Clinical documentation for therapy sessions
- **Assessments:** Pre-built assessment templates and a framework for building custom assessments; tracks assessment scores and dates over time
- **Client Intake:** Intake workflows including intake assessments for patient health status, medical history, and conditions
- **Forms Designer:** Customizable form creation for assessments, progress notes, and other documentation needs (enhanced forms designer on roadmap)
- **MedlinePlus Integration:** Educational resources surfaced based on diagnosis codes and current medications
- **Eleos Health AI Integration:** Voice-based NLU technology that converts behavioral health session conversations into notes and clinical insights, with automatic identification of evidence-based techniques and recurring themes

**e-Prescribing:**
- Electronic prescribing via DrFirst integration
- Access to client medication histories
- Medication interaction checking
- Direct pharmacy transmission

**Billing & Revenue Cycle Management:**
- Visual billing dashboard for fiscal overview
- Claims submission through integrated Apex Clearinghouse
- Bulk claim processing
- Eligibility verification
- Payment posting and remittance processing
- Credit balance refunds and small balance write-offs
- Enhanced charge creation workflows
- AI-powered billing accuracy tools (on roadmap) for procedure code mapping

**Scheduling:**
- Appointment scheduling with customizable templates
- Appointment reminders (client engagement feature)
- Medication alerts

**Telehealth:**
- HIPAA-compliant video telehealth
- Supports individual and group sessions

**Reporting & Analytics:**
- Customizable reporting dashboards (30+ presets available, plus custom designs)
- Practice health metrics
- Client outcomes tracking
- Real-time productivity and financial data
- Staff activity, caseload, and performance visibility for supervisors

**State Reporting:**
- State-specific reporting capability for community mental health and substance abuse compliance requirements
- Configured per state to address specific mandatory reporting formats

**Medication Assisted Treatment (MAT) Module** (announced for H1 2025):
- Liquid Methadone dosing, dispensing, and tracking
- Real-time coordination between front desk, medical, counseling, and billing staff
- Designed for substance use recovery organizations

**Document Management:**
- Document storage and management integrated with the clinical record

**Lab Integration:**
- Lab integration capability mentioned in feature lists (limited detail available)

**Voice Recognition:**
- Voice recognition for clinical documentation (mentioned in feature lists)

### Data & Content

Based on the features and functionality described above, EchoVantage stores and manages the following types of data:

- **Client/patient demographics and intake information** — health status, medical history, conditions captured during intake
- **Clinical documentation** — progress notes, therapy session notes, clinical narratives
- **Treatment plans** — structured treatment plans linked to outcomes and assessments
- **Assessments** — standardized and custom assessment instruments with scored results tracked over time
- **Diagnoses** — diagnosis codes used for clinical decision support and MedlinePlus integration
- **Medications and prescriptions** — medication histories, active prescriptions, e-prescribing records sent to pharmacies via DrFirst
- **Appointment/scheduling data** — appointments, scheduling templates, appointment reminders
- **Billing and claims data** — charges, claims (submitted via Apex Clearinghouse), eligibility checks, payment remittances, credit balances, accounts receivable
- **Telehealth session records** — individual and group telehealth session data
- **State reporting data** — state-specific mandatory reporting datasets for behavioral health compliance
- **Documents** — uploaded and generated documents attached to client records
- **Lab results** — lab data (mentioned but limited detail; lab integration is listed as a feature)
- **Reporting/analytics data** — dashboards, productivity metrics, financial reports, client outcome data
- **User/staff data** — staff activity, caseloads, performance metrics visible to supervisors
- **AI-generated content** (via Eleos integration) — AI-generated session notes, session intelligence, evidence-based technique identification

**Notable gaps/uncertainties:**
- **Patient portal:** EchoVantage is not certified for (e)(1) patient portal/VDT criteria. It's unclear whether there is any patient-facing portal or if patient engagement is limited to appointment reminders and medication alerts.
- **Direct messaging:** The product is certified for (h)(1) direct messaging, suggesting it supports clinical information exchange via Direct protocol, but specific details about this were not found in marketing materials.
- **Lab integration depth:** Lab integration is mentioned but specifics are thin — it's unclear how deep the lab ordering/results workflow goes.
- **Imaging/radiology:** No mention of imaging or radiology data — expected for a behavioral health system.
- **Care coordination/referral data:** Not explicitly described, though transitions of care certification (b)(1) implies some structured clinical summary exchange capability.
- **Consent and authorization records:** Not explicitly described, though likely present given behavioral health regulatory requirements.
- **Specific customer count:** Not publicly available for EchoVantage specifically; the "30,000+ practices" figure refers to the entire Ensora Health portfolio.

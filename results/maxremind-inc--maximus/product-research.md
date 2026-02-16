# MaxRemind Inc — Product Research

Researched: 2026-02-15
Developer website: https://maxremind.com

## Overview

MaxRemind Inc is a small healthcare IT company headquartered in Richardson/Carrollton, Texas (the website lists both locations). The company positions itself primarily as a medical billing and revenue cycle management (RCM) services provider, claiming "over 20 years of experience" in healthcare. More recently, MaxRemind has expanded into the EHR product space with Maximus EHR. Employee counts vary across sources (estimates range from ~25 to ~200, with some sources suggesting offshore staff across 3 continents including Asia and Europe). Revenue estimates range from $1M–$25M depending on the source — likely on the smaller end. The company is privately held and appears to be a small vendor.

MaxRemind's core business has historically been medical billing, coding, credentialing, and practice management services. Maximus EHR is described as the company's "flagship product" and appears to be a relatively recent addition to their portfolio — certified in October 2023. The company also offers companion products: Max Charting App (mobile charting), MaxCoder (AI-powered coding), MaxRPM (remote patient monitoring), and a Provider Portal (billing/claims dashboard). They also separately market a "Home Health Software" product on TrustRadius. The contact email uses an Outlook domain (maxremindhealth@outlook.com), which, combined with the variable company size estimates, suggests a small operation.

## Product: Maximus

CHPL ID: 11360

### What It Is

Maximus EHR is a cloud-based, ONC-certified electronic health record system marketed as an "all-in-one" platform for clinical documentation, practice management, and billing. It is described as AI-powered, with features spanning clinical workflows, scheduling, billing/claims, patient engagement, and reporting. The product claims support for 75+ medical specialties.

The certified product appears to be the full EHR platform itself — not a submodule of a larger system. However, MaxRemind markets several companion products (Max Charting App, MaxCoder, MaxRPM, Provider Portal) that extend the platform's capabilities. It's unclear how tightly integrated these are with the core Maximus EHR vs. standalone tools.

The product has a broad certification footprint: 35+ ONC criteria covering clinical data ((a)(1)–(a)(15)), care coordination ((b)(1)–(b)(2)), patient portal ((e)(1), (e)(3)), public health reporting ((f)(1)–(f)(3)), FHIR APIs ((g)(7), (g)(10)), and the EHI export ((b)(10)).

### Users & Market

Maximus EHR targets ambulatory practices of all sizes — from solo practitioners to multi-location healthcare networks. The vendor materials mention specialty practices, clinics, medical centers, and hospital systems. The case study on the website features **Wound Healing Partners**, a specialty wound care clinic in Texas, describing improved follow-up workflows and documentation.

The vendor's SED (Safety-Enhanced Design) description lists intended users as: healthcare providers (physicians, nurses, clinical staff), health IT administrators, patients (via patient portal), healthcare payers (claims processing), pharmacists (medication management), and public health officials (reporting). This is an unusually broad user description for a product of this size.

Customer count is not disclosed. No major health system deployments or notable customer logos were found. The product has **zero reviews** on Capterra and TrustRadius. A few testimonials on the vendor's own website mention ease of use and comparison to eClinicalWorks and Epic, but these are unverified. The market presence appears very limited.

### Modules & Functionality

Based on vendor website, maximus.care, and third-party listings, the following modules and capabilities are described:

**Clinical Documentation & Charting**
- Pre-built templates and customizable workflows for clinical documentation
- Voice recognition and smart templates for simplified documentation (described in blog post)
- Real-time clinical charting
- Support for 75+ specialties (dentistry, dialysis, mental health, wound care, etc.)
- AI-powered clinical decision support with "smart recommendations"

**Scheduling & Practice Management**
- Appointment scheduling and registration management
- Follow-up workflow management (highlighted in wound care case study)
- Task management and multi-location support
- Activity dashboards
- Electronic eligibility verification

**Billing & Revenue Cycle**
- Automated billing and claims processing (AI-powered)
- Coding assistance (also available as standalone MaxCoder product)
- Claims management and submission
- Revenue cycle management
- Payment processing

**Patient Engagement**
- Patient portal with secure messaging
- Appointment reminders and alerts
- Patient access to health records
- Appointment self-scheduling (implied)

**E-Prescribing & Pharmacy**
- E-prescribing functionality (listed on maximus.care and SoftwareFinder)

**Lab & Referral Management**
- Lab integration (listed on maximus.care)
- Referral management

**Care Coordination & Interoperability**
- Transitions of care (certified for (b)(1) and (b)(2))
- Direct Project messaging
- FHIR API support ((g)(7), (g)(10))
- Document and file management
- Report sharing between providers

**Telemedicine**
- Telemedicine capabilities (listed on SoftwareFinder)

**Remote Patient Monitoring**
- MaxRPM companion product for remote monitoring (blood pressure, weight, pulse, glucose)
- Real-time data collection with alerts for anomalies

**Public Health Reporting**
- Immunization registry reporting ((f)(1))
- Syndromic surveillance ((f)(2))
- Electronic case reporting ((f)(3))

**Security & Compliance**
- HIPAA-compliant cloud hosting
- Multi-factor authentication
- Encryption, audit logs, access controls
- Automatic backups

**Reporting & Analytics**
- AI-powered reporting and analytics
- Financial analysis
- Real-time statistics and KPIs
- Practice performance insights

**Mobile Access**
- Max Charting App (iOS and Android) for mobile documentation
- Provider Portal mobile apps (iOS and Android) for billing/claims

### Data & Content

Based on the certified criteria and vendor descriptions, Maximus EHR stores and manages the following data types:

**Clinical data** (per certification criteria): Patient demographics, medication lists, medication allergy lists, problem lists, clinical notes, family health history, implantable device information, social/psychological/behavioral data, clinical quality measures, and laboratory data. The (a)(1)–(a)(15) certifications confirm the system manages core structured clinical data.

**Orders and prescriptions**: The system is certified for CPOE ((a)(1)–(a)(3)) covering medications, lab orders, and diagnostic imaging. E-prescribing is listed as a feature.

**Documents and images**: Document management and file management are listed on maximus.care. The charting app implies clinical document storage.

**Billing and financial data**: Claims, billing records, payment details, patient balances, ICD/CPT codes, eligibility verification data. The Provider Portal specifically focuses on billing data management. The vendor's core business is medical billing, so this integration is a key part of the platform.

**Scheduling data**: Appointments, follow-up schedules, appointment reminders.

**Patient portal data**: Secure messages between patients and providers, patient access logs.

**Remote monitoring data**: Via MaxRPM — vitals like blood pressure, weight, pulse, glucose (though integration with the core EHR is unclear).

**Care coordination data**: Transitions of care documents (C-CDAs), Direct messages, referrals.

**Public health reporting data**: Immunization records, syndromic surveillance data, electronic case reports.

**What's unclear**: The website doesn't provide detail on whether the system stores clinical images (radiology, pathology), scanned documents, faxes, or detailed encounter-level billing (charge capture vs. claim submission). The relationship between the standalone companion products (MaxCoder, MaxRPM, Provider Portal) and the core EHR database is not well documented — it's unclear whether these share a common data store or operate independently. The Home Health Software product listed on TrustRadius is also of uncertain relationship to Maximus EHR.

---

## Research Notes

MaxRemind presents as a small vendor whose core competency is medical billing services, with Maximus EHR as a more recent product offering. The product is broadly certified but has minimal market presence — zero third-party reviews, no recognizable customer logos, and limited case study evidence. The vendor's website is marketing-heavy with significant use of AI buzzwords but relatively thin on specific technical or functional detail. The companion product ecosystem (Max Charting, MaxCoder, MaxRPM, Provider Portal) suggests either a modular architecture or separately developed tools, but the integration story between them is not well documented. The discrepancy between the broad SED user description (payers, pharmacists, public health officials) and the apparent product scope warrants attention during EHI export evaluation.

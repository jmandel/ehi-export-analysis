# MedicalMine Inc. — Product Research

Researched: 2026-02-15
Developer website: https://www.charmhealth.com

## Overview

MedicalMine Inc. is a privately held health IT company founded in 2007 by Dr. Pramila Srinivasan (PhD, Purdue), based in Pleasanton, California. The company operates under the brand name **CharmHealth** and builds a cloud-based, all-in-one healthcare platform targeting ambulatory practices — particularly independent clinics, small-to-medium practices, and integrative/functional medicine providers. The company has approximately 23 employees (as of late 2023) and has not disclosed external funding rounds. At least 5,000 licensed physicians are active CharmHealth EHR users (based on a 2023 CharmHealthSquare community launch announcement referencing "approximately 5,000 licensed physicians who are existing CharmHealth EHR users"). The company has a medical advisory board of 13+ physicians across multiple specialties.

CharmHealth has expanded internationally through a partnership with EMDI to distribute in the Gulf Cooperation Council (GCC) region, and in 2022 announced the CharmHealth + Bioverge Digital Transformation Fund, a venture fund focused on early-stage digital health companies. The product is marketed as "founded and designed by doctors" and has been recognized as "Best Free EMR of 2024" by Software Advice. It is hosted on Zoho's cloud infrastructure.

## Product: CharmHealth EHR

CHPL ID: 9741

### What It Is

CharmHealth EHR is a cloud-based, ONC-certified electronic health record system that is part of a broader integrated suite including practice management, revenue cycle management, patient engagement portal, telehealth, secure messaging (CharmConnect), and an app marketplace (CharmHealthHub). The certified module (CharmHealth EHR v1.2, certified 2018-11-15) appears to be the clinical EHR component, but the broader product under which it operates encompasses billing, scheduling, patient portal, telehealth, and more. The CHPL certification spans a broad set of criteria: clinical data capabilities (a)(1)-(a)(5), (a)(12), (a)(14); transitions of care (b)(1)-(b)(3); patient portal (e)(1), (e)(3); public health reporting (f)(1)-(f)(2); FHIR APIs (g)(7), (g)(10); and direct messaging (h)(1). The SED intended user description is "Outpatient Clinic."

Integrated third-party components listed on the mandatory disclosures page: AccessGUDID (drug/device identification), Surescripts eRx (electronic prescribing), IronBridge PubHub (data management), and DataMotion Direct (secure messaging).

### Users & Market

CharmHealth targets independent and small-to-medium ambulatory practices. It has particular traction with **integrative medicine** and **functional medicine** providers — this is a distinguishing niche. The vendor lists supported specialties including family practice, urgent care, internal medicine, pediatrics, psychiatry, integrative medicine, gynecology, dental, bariatrics, cardiology, dermatology, emergency medicine, gastroenterology, and others.

A case study on the CharmHealth website describes Capital Integrative Health, an integrative/primary care practice with 10 practitioners that grew from 0 to 930 patients within 7 months of implementing CharmHealth. Users in reviews frequently mention using it for integrative and functional medicine practices.

Reviews on Capterra, GetApp, and FindEMR characterize CharmHealth as cost-effective and well-suited for smaller practices. Users appreciate the customizable templates and affordable pricing. Common criticisms include occasional system slowness, limited billing functionality compared to larger EHRs, and inconsistent customer support responsiveness.

The pricing model includes a free tier (50 encounters/month, 1 provider, 5 users), an encounter-based plan ($0.50/encounter, $25/month minimum), and a provider-based plan ($200/provider/month). Add-ons are priced separately for e-prescribing ($10/provider/month), telehealth ($20/provider/month), document scanning ($10/month), eCommerce (1% transaction fee), and AI Scribe ($125/provider/month or $2/encounter).

### Modules & Functionality

Based on vendor website, feature pages, pricing tiers, case studies, and third-party review sites, CharmHealth includes the following modules and capabilities:

**Clinical Documentation (EHR)**
- SOAP note templates customizable by specialty
- Image annotation tools
- QuickText macros for faster documentation
- Clinical decision support with customizable decision trees
- Flowsheets for tracking vitals and lab results across visits
- Smart navigation and AI-assisted features
- CharmAI Scribe: ambient listening to auto-generate clinical notes, categorize transcriptions, update chart sections, and suggest diagnosis codes
- CharmAssist: AI assistant for clinical suggestions, referral letter generation, lab result interpretation

**E-Prescribing**
- Electronic prescribing including EPCS (controlled substances)
- Connection to 70,000+ pharmacies via Surescripts
- Drug-drug, drug-food, drug-allergy interaction checking
- Drug-herb interaction database (notable for integrative medicine)
- Prescription refill management

**Lab Integration**
- Pre-built interfaces for LabCorp, Quest, and other major labs
- Standard HL7-based connections for additional laboratories
- Lab results flow into patient records and patient portal

**Immunization Registry**
- Electronic transmission of vaccine data to state registries (certified for (f)(1))

**Practice Management**
- Multi-facility appointment scheduling with resource management (rooms, IV chairs, etc.)
- Color-coded calendar
- Patient self-scheduling via portal and website
- iPad kiosk check-in
- Pre-appointment questionnaires
- Task management
- Text and voice appointment notifications/reminders
- Role-based access control with automatic audit logging
- Multi-facility support
- Business analytics and reporting

**Medical Billing**
- SuperBill generation
- CMS 1500 forms
- Billing profiles
- Automated invoice generation from clinical notes
- Real-time insurance eligibility verification
- Electronic claims submission with status tracking
- Credit card payment processing
- Patient account statements
- Electronic remittance advice (ERA) processing

**Revenue Cycle Management (RCM)**
- RCM dashboard with infographic views of claims, collections, receivables, denials
- Provider credentialing
- Medical coding with NCCI edits compliance
- Claims scrubbing (demographics, insurance, procedure codes, modifiers)
- Payment posting and EOB processing
- Denial management with root cause analysis and resubmission
- A/R follow-up and patient outreach
- Multi-facility claims tracking

**Patient Engagement Portal**
- Patient portal for viewing visit summaries, lab results, medical records
- Secure messaging between patients and providers
- Appointment requests and self-scheduling
- Prescription refill requests
- Pre-screening and intake forms/questionnaires
- Health literature about conditions and medications
- Personal health record with wellness tracking and goal-setting
- Document sharing between patients and providers

**Telehealth**
- Integrated audio/video for live consultations
- Adaptive bandwidth (auto-switches to audio on slow connections)
- Screen sharing for patients to share records
- Multi-user sessions (multiple participants)
- Local recording capability
- TeleHealth kiosk functionality for remote centers
- Consent document generation before sessions
- No software installation required (browser-based)

**Secure Messaging (CharmConnect)**
- End-to-end encrypted HIPAA-compliant messaging
- Group and private chats
- Audio/video calls with screen sharing
- Patient-specific channels
- Document sharing (X-rays, lab results)
- External chat for inter-practice communication
- Integration with CharmHealth EHR for retrieving patient records in conversations

**Inventory Management**
- Medication and supplement inventory tracking
- Stock level threshold alerts
- Expiration date monitoring
- Useful for practices dispensing vaccines, OTC drugs, supplements, and lab kits

**Document Management**
- Secure document storage with tagging and folder organization
- Electronic fax capabilities (add-on)
- Document scanning (add-on)

**App Marketplace (CharmHealthHub)**
- Marketplace launched in 2024/2025 with "hundreds of apps, partners and API options"
- Third-party integrations with Change Healthcare, DoctorConnect, Docere Systems, MDScripts, LabCorp
- Categories include AI-enabled solutions, devices, patient engagement, administrative tools, clinical decision support
- Developer API access for building custom integrations

**Reporting & Analytics**
- Practice statistics and analytics
- Patient data reporting
- Meaningful Use / MIPS reporting
- 30 clinical quality measures (CQMs)
- Customizable reports

### Data & Content

Based on the features described above and vendor documentation, CharmHealth stores and manages the following data types:

- **Clinical records**: SOAP notes, visit summaries, treatment plans, clinical decision support outputs, flowsheet data (vitals over time)
- **Patient demographics**: Contact information, insurance details, medical history
- **Medications & prescriptions**: Active/historical prescriptions, refill history, drug interaction checks, drug-herb interactions
- **Lab data**: Lab orders, results from LabCorp/Quest/others via HL7 interfaces
- **Immunization records**: Vaccine administration data, registry submissions
- **Documents & images**: Uploaded documents, scanned files, image annotations, X-rays shared via Connect
- **Billing & claims data**: SuperBills, CMS 1500 forms, claims, ERA/EOB data, payment records, eligibility verification results, denial records, A/R data
- **Scheduling data**: Appointments, resource allocations, provider schedules
- **Patient portal data**: Patient messages, appointment requests, refill requests, intake form responses, health goals, wellness tracking data
- **Telehealth data**: Session records, consent documents, possibly recorded sessions
- **Messaging data**: Provider-to-provider and provider-to-patient encrypted messages, chat history, shared documents
- **Inventory data**: Medication/supplement stock levels, expiration dates, dispensing records
- **Audit logs**: User actions, access logs (automatically generated per role-based access)
- **Analytics/reporting data**: CQM measures, practice statistics, MIPS data
- **AI Scribe transcriptions**: Ambient recording transcriptions, auto-generated notes, suggested codes

The vendor website is notably more detailed about clinical and practice management features than about the specific data architecture. The product is cloud-based (hosted on Zoho infrastructure) with 256-bit encryption and daily/weekly backups. There is no mention of on-premise deployment options.

One notable aspect for later EHI export assessment: the breadth of this product is significant — it's not just an EHR but includes billing/RCM, patient portal, telehealth, secure messaging, inventory, and an app marketplace. The (b)(10) export would need to cover all data stored by the product of which the certified EHR module is a part, which could include all of the above.

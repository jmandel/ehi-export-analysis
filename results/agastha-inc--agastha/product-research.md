# Agastha, Inc. — Product Research

Researched: 2026-02-16
Developer website: http://www.agastha.com

## Overview

Agastha, Inc. is a small healthcare IT company founded in 2003 and headquartered in Charlotte, North Carolina. According to business directory sources, the company has approximately 18 employees and ~$10M in revenue. It also has a related entity, Agastha Healthsoft Pvt. Ltd., which operates in India. The company has a notably global footprint for its size, with operations in the USA, India, Nigeria, Gambia, Liberia, and Ivory Coast. The founder is Mohan Korrapati.

Agastha develops the "Agastha Enterprise Healthcare Software," a cloud-based, integrated healthcare platform that combines EHR, practice management, pharmacy management, laboratory information system (LIS), patient portal, billing, telehealth, and e-prescribing capabilities. The product targets ambulatory practices, multi-specialty clinics, hospitals, pharmacies, and laboratories. Named customers include Carolina Blood and Cancer Care and The Neurological Institute. The product serves diverse specialties including primary care, internal medicine, oncology, neurology, dermatology, emergency medicine, family practice, general surgery, mental health, and pediatrics. Pricing reportedly starts at $50/user/month for smaller practices, with custom quotes for larger organizations.

Agastha is a very small vendor in the EHR market. It has only 6 reviews across major review platforms (with a 4.7 rating). Its global presence — particularly in West Africa — is somewhat unusual for a US-based ONC-certified EHR vendor and suggests the product may be architected to support diverse regulatory and clinical environments.

## Product: Agastha Enterprise Healthcare Software

CHPL IDs: 11152 (version 20.1, certified 2022-12-28), 11616 (version 25.1, certified 2025-03-25)

### What It Is

Agastha Enterprise Healthcare Software is an integrated, cloud-based healthcare platform that combines electronic health records with practice management, pharmacy management, laboratory information management, billing, patient portal, and telehealth capabilities into a single product. The SED intended user description is "Ambulatory," and the product is certified across a broad range of ONC criteria: clinical data (a)(1)–(a)(14), transitions of care (b)(1)–(b)(3), patient portal/VDT (e)(1), public health reporting (f)(1)/(f)(2)/(f)(4)/(f)(7), and FHIR API access (g)(7)/(g)(9)/(g)(10)). The newer v25.1 certification also adds (b)(11) for care plan exchange.

The certified module appears to be the whole product — Agastha does not market separate products or modules with distinct names. Everything (EHR, PMS, LIS, billing, patient portal, pharmacy) is part of one integrated platform.

### Users & Market

The product serves ambulatory practices, clinics, hospitals, pharmacies, and laboratories. Typical end users include physicians, nurses, pharmacists, lab technicians, billing staff, and practice managers. Patients interact through a patient portal. Specialties mentioned in vendor materials and third-party listings include primary care, internal medicine, oncology, neurology, dermatology, emergency medicine, family practice, general surgery, mental health, and pediatrics.

The company is very small (~18 employees). Customer count is not publicly disclosed but appears modest based on the very low number of online reviews (6 total across review platforms). Named customers include Carolina Blood and Cancer Care and The Neurological Institute. The international presence (India, West Africa) suggests some customer base outside the US, though the ONC certification applies to US deployments.

### Modules & Functionality

Based on the vendor website, product pages, and third-party review sites, the product includes these integrated modules:

**Electronic Health Records (EHR/EMR)**
- Patient encounter documentation with medical history, prescriptions, lab results, allergies
- Customizable clinical documentation templates
- Voice recognition for data entry (highlighted positively in user reviews)
- Clinical decision support with drug interaction checks, alerts, and reminders
- Immunization and allergy tracking
- Problem lists, medication lists, clinical notes
- Role-based dashboards with customizable views

**Practice Management**
- Appointment scheduling with provider availability management
- Patient registration and demographics
- Multi-location support
- Document management
- Compliance tracking

**Billing & Claims**
- Invoicing and payment processing
- Insurance claim eligibility verification
- Claims management and submission
- Revenue cycle management (described as "country-specific" customization)
- Online payment processing through patient portal
- Insurance claim status monitoring

**E-Prescribing**
- Electronic prescription transmission directly from provider dashboard to linked pharmacies
- Drug interaction checking
- EPCS (Electronic Prescribing of Controlled Substances) with multi-factor authentication
- Integration with pharmacies via Surescripts (implied by EPCS certification)

**Pharmacy Management System**
- Inventory tracking with stock expiry alerts
- Procurement and supply chain monitoring
- Real-time prescription refills
- Sales and billing for pharmacy operations
- Multi-location pharmacy support
- Online medicine delivery ordering

**Laboratory Information System (LIS)**
- Lab order management
- Device connectivity for automated data capture
- Personalized barcode generation for sample collection
- Result notifications to providers
- Integration with diagnostic labs and imaging centers

**Patient Portal**
- Online access to medical records (read-only)
- Appointment scheduling
- Secure messaging with providers
- E-prescription viewing
- Online bill payment and insurance claim status monitoring
- Appointment reminders
- Access via link sent to email or mobile number

**Telehealth / Remote Patient Monitoring**
- Virtual medical consultations
- Remote patient monitoring capabilities
- Cloud-based remote access for providers

**Communication & Notifications**
- WhatsApp and SMS integration for alerts and reminders
- Internal messaging between providers, patients, and pharmacists
- Automated communication and personalized patient assessments

**Reporting & Analytics**
- Customizable reports
- Performance metrics and data analytics
- Automated sales and stock analysis (pharmacy module)
- Patient outcome tracking and compliance metrics

**Technical / Platform**
- Cloud-based (web browser access)
- Mobile access via iOS and Android apps
- Kiosk integration support
- AI and machine learning capabilities (mentioned but details sparse)
- Open Patient API for third-party developers
- FHIR API (g)(10) certified

### Data & Content

Based on the described modules and features, the product manages:

- **Clinical data**: Patient encounter records, medical history, problem lists, medication lists, allergies, immunizations, vital signs, clinical notes, assessment and plan documentation. These are confirmed by the (a)(1)–(a)(14) certifications and vendor feature descriptions.
- **Prescription data**: Electronic prescriptions including controlled substances (EPCS), drug interaction records, prescription history, refill requests. Confirmed by e-prescribing module descriptions and EPCS/MFA mandatory disclosure.
- **Lab data**: Lab orders, lab results, specimen/barcode data, device integration data. Confirmed by LIS module description and (b)(3) certification.
- **Pharmacy data**: Medication inventory, stock levels, expiry dates, procurement records, sales/billing records, supply chain data. Confirmed by pharmacy management module description.
- **Billing & financial data**: Claims, invoices, insurance eligibility records, payment records, revenue cycle data. Confirmed by billing module and patient portal payment features.
- **Scheduling data**: Appointments, provider availability, appointment reminders. Confirmed by practice management module.
- **Patient demographics**: Registration data, contact information, insurance information. Implied by practice management and billing modules.
- **Patient portal data**: Secure messages between patients and providers, patient portal access logs. Confirmed by patient portal feature descriptions.
- **Documents**: Clinical and administrative documents. Confirmed by "document management" feature listing.
- **Communication records**: WhatsApp/SMS message logs, internal provider messaging. Confirmed by communication features on vendor website.
- **Telehealth data**: Virtual visit records, remote monitoring data. Mentioned on vendor site but details are sparse — unclear how much structured data is captured vs. just video sessions.
- **Public health reporting data**: Immunization registry submissions, syndromic surveillance, cancer registry, and electronic lab reporting data. Confirmed by (f)(1), (f)(2), (f)(4), (f)(7) certifications.
- **Audit data**: Authentication logs, access logs, MFA records. Implied by (d)(1)–(d)(9) certifications and MFA mandatory disclosure.

**Gaps in research**: The vendor website is fairly high-level and marketing-oriented. Detailed data models, specific field-level documentation, and comprehensive module descriptions are not publicly available. The very small number of user reviews (6 total) limits insight from real-world usage reports. It is unclear how deep the AI/ML capabilities go or what additional data they might generate/store. The international deployments may involve different data models than the US ONC-certified version.

---

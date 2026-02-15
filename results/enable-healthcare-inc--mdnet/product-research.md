# Enable Healthcare Inc. — Product Research

Researched: 2026-02-14
Developer website: https://www.ehiehr.com/

## Overview

Enable Healthcare Inc. is a private healthcare IT company headquartered in East Hanover, New Jersey. The company was founded around 2006–2008 (sources conflict on exact year) and has been in the EHR market for approximately 15+ years. They develop the MDnet EHR platform and provide medical billing services. The company is small-to-midsize — employee counts vary across sources from ~187–194 (PitchBook) to 501–1,000 (LinkedIn), suggesting the higher figure may include contracted billing staff. Enable Healthcare positions itself as a provider of EMR, practice management, and revenue cycle management (RCM) solutions for small to large ambulatory practices across multiple specialties.

Their website (ehiehr.com) is Wix-based and rendered almost entirely client-side, making it difficult to scrape directly; product information was gathered primarily from third-party review sites, app store listings, and search engine snippets of the vendor site. The company also operates under the domain ehiconnect.com for its portal and app infrastructure.

Recently, Enable Healthcare has branded a suite of AI-powered companion tools under the "ariaone" umbrella, with sub-products including Lumina (clinical intelligence/documentation AI) and revQ (AI-driven billing/revenue cycle platform). These appear to be enhancements layered onto the core MDnet platform rather than separate products.

## Product: MDnet

CHPL ID: 10247 (CHPL Product Number: 15.04.04.2719.MDne.10.01.1.191231)

### What It Is

MDnet is a cloud-based, ONC-certified Electronic Health Records platform designed as an integrated clinical, administrative, and financial management system for ambulatory healthcare providers. The certified module appears to be the full product — MDnet encompasses the EHR, practice management, billing, patient portal, e-prescribing, and telehealth in a single platform. The certification covers a broad set of criteria: (a)(1)–(a)(5) for clinical data management (CPOE, demographics, problem list, medication list, medication allergy list), (a)(12) for family health history, (a)(14) for implantable device list, plus transitions of care (b)(1)–(b)(3)), patient portal/VDT (e)(1), (e)(3)), public health reporting (f)(1)–(f)(2)), FHIR/API access (g)(7)–(g)(10)), clinical quality measures (c)(1)–(c)(3)), and direct messaging (h)(1)). This broad certification profile is consistent with a full-featured ambulatory EHR.

The product is web-based and also available as a mobile app (iOS and Android). The iOS app (MDNet, by Enable Healthcare Inc.) supports iPhone, iPad, Apple Watch, and Apple Vision, and lists features including touch-based EHR, voice recognition, telehealth, e-prescribing, electronic lab results, and integrated chat.

### Users & Market

MDnet targets ambulatory practices ranging from solo providers to multi-site, multi-specialty organizations. According to third-party review sites, it is popular among:
- Mental and behavioral health clinicians
- Pediatricians
- Cardiologists
- Internal medicine providers
- Urgent care centers
- OBGYN practices
- Community health centers

The intended user description from the CHPL listing is "Admin and Medical staff," suggesting both clinical and administrative users. Pricing starts at $250/provider/month (Essential plan), with Pro at $400/month and Enterprise at $550/month. Bundle options that include practice management and RCM are also available (e.g., Pro Bundle at 6% of monthly collections plus transaction fees), indicating that billing/RCM services can be bundled or purchased separately.

Enable Healthcare also positions itself as a medical billing company — their website explicitly advertises "Medical Billing services" alongside the EHR product, particularly targeting New Jersey-based practices. This dual identity as both a software vendor and a billing services company is notable.

No specific customer counts or notable deployments were found in the research. User reviews on Capterra, Software Advice, and GetApp exist but are relatively few in number, consistent with a smaller vendor.

### Modules & Functionality

Based on vendor materials, third-party review sites, and app store descriptions, MDnet includes the following functional areas:

**Clinical / EHR:**
- Patient encounter documentation with charting
- AI-powered charting via "enableAssist" / "Lumina" (ariaone's clinical intelligence platform) — generates structured SOAP notes, transcribes real-time patient conversations in 60+ languages
- Problem list, medication list, medication allergy list management
- Immunization and allergy tracking
- Family health history
- Implantable device tracking (per (a)(14) certification)
- Clinical decision support
- Customizable reports and analytics
- Real-time patient analytics at point of service

**E-Prescribing:**
- Electronic prescription transmission to pharmacies (per (a)(1) certification for CPOE and multiple review site confirmations)

**Lab Integration:**
- Electronic lab results access (confirmed via App Store listing)

**Practice Management / Scheduling:**
- Appointment management and scheduling (solo or multi-physician practices)
- Online appointment booking (website integration)
- Patient self-check-in process
- Rescheduling and follow-up management

**Medical Billing & Revenue Cycle:**
- Insurance eligibility verification
- Claim submission and management
- Revenue cycle management — now branded as "revQ" (ariaone's AI-driven billing platform)
- Claims scrubbing and denial management (implied by "faster claims, fewer denials")
- Billing and claims management

**Patient Portal:**
- Medical record access for patients
- Appointment scheduling by patients
- Secure messaging
- Co-payment management
- Self-check-in
- (Portal URL: emr.ehiconnect.com/p based on search results referencing "MDNet PHR | Login Page")

**Telehealth:**
- Integrated telehealth/telemedicine capabilities (cloud-based)

**Care Coordination & Population Health:**
- Chronic Care Management (CCM)
- Remote Patient Monitoring (RPM)
- Population Health management
- Annual Wellness Visits
- Care coordination across providers

**Transitions of Care / Interoperability:**
- C-CDA document exchange (per (b)(1)–(b)(3) certification)
- Direct messaging (per (h)(1) certification)
- FHIR API access (per (g)(7)–(g)(10) certification)

**Public Health Reporting:**
- Immunization registry reporting (per (f)(1))
- Syndromic surveillance reporting (per (f)(2))

**Document Management:**
- Scanning of paper records
- Document management capabilities

**Mobile Access:**
- Mobile EHR app (iOS, Android)
- Touch-based interface
- Cloud-based voice recognition

### Data & Content

Based on the features and certifications described above, MDnet stores and manages the following categories of data:

- **Patient demographics** — per (a)(5) certification and core EHR function
- **Clinical encounter documentation** — SOAP notes, charting, visit records (confirmed by AI charting features and user reviews describing encounter documentation workflows)
- **Problem lists** — per (a)(3) certification
- **Medication lists and prescriptions** — per (a)(4) certification and e-prescribing feature
- **Medication allergies** — per (a)(2) certification
- **Immunization records** — per feature list and (f)(1) public health reporting certification
- **Family health history** — per (a)(12) certification
- **Implantable device information** — per (a)(14) certification
- **Lab results** — confirmed via App Store listing ("Electronic Lab Results")
- **Prescription/e-prescribing data** — electronic prescriptions sent to pharmacies
- **Appointment/scheduling data** — scheduling module with online booking and self-check-in
- **Billing and claims data** — insurance verification, claim submissions, RCM data; Enable Healthcare also offers billing services, so claims data is a core part of the product
- **Patient portal messages** — secure messaging between patients and providers
- **Patient-generated data** — co-payment management, self-check-in data via portal
- **Scanned documents** — paper record scanning and document management
- **C-CDA clinical documents** — transitions of care documents per (b)(1)–(b)(3)
- **Care coordination data** — CCM, RPM, population health, and AWV program data
- **Clinical quality measure data** — per (c)(1)–(c)(3) certification
- **Telehealth session data** — integrated telehealth implies records of telehealth encounters
- **Audit logs** — per (d) criteria certification for privacy and security

**Gaps/Uncertainties:**
- **Imaging/radiology:** No specific mention of imaging ordering or results management was found, though the broad certification profile doesn't explicitly exclude it. The website doesn't describe radiology or imaging features.
- **Referral management:** One review mentioned referral documentation, but it's not prominently featured as a module. Unclear how robust referral tracking is.
- **Specific specialty workflows:** While the product serves multiple specialties (behavioral health, cardiology, pediatrics, etc.), it's unclear whether it has specialty-specific templates or modules, or relies on general-purpose charting. Some reviews noted the system "lacks mental health friendliness," suggesting limited specialty customization despite behavioral health being listed as a target specialty.
- **Clinical notes detail:** While AI-powered SOAP note generation is advertised, the depth of structured clinical data (vitals, growth charts, assessments, clinical decision support rules) is not well-documented on public sources.
- **User counts:** No customer count or market share data was found. The relatively small number of reviews on third-party sites suggests a modest user base.

---

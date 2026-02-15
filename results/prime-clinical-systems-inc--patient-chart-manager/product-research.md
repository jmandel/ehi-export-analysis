# Prime Clinical Systems, Inc. — Product Research

Researched: 2026-02-15
Developer website: https://primeclinical.com/ (note: site was in maintenance mode during research; much information gathered from third-party sources and cached content)

## Overview

Prime Clinical Systems, Inc. was founded in 1983 by Barry Ardelan and is headquartered in Pasadena, California (3675 E. Huntington Dr, Suite A), with a regional office in Dublin, Ireland. The company has operated continuously for over 40 years without merging, changing names, or relying on venture capital — a rarity in the EHR space. They claim to serve more than 10,000 physicians across the country.

Prime Clinical is a small, privately held vendor focused on the ambulatory physician practice market. They provide integrated practice management and EHR software, primarily targeting solo practitioners through mid-sized multi-specialty groups (up to ~50-100 providers). Their notable customers include NSR Medical, Advanced Radiology of Beverly Hills, Pomona Pediatrics, and Pediatric Care Medical Group (Huntington Beach, a 25+ year customer). The company differentiates itself through in-house development of all products (not acquired), integrated systems sharing a common database, and long-term customer relationships.

## Product: Patient Chart Manager

CHPL ID: 10791

### What It Is

Patient Chart Manager is Prime Clinical's certified EHR (electronic health record) software. It is part of a broader integrated platform that also includes practice management (previously branded "OnSTAFF," later "Intellect," and most recently a web-based billing/scheduling system called "WebSTAFF"). The certified module covers the EHR/clinical documentation side, but the full product offering is a combined EHR + practice management solution — the CHPL metadata describes the intended users as "Healthcare providers in ambulatory health care settings."

The certification is broad, covering 37 criteria across clinical data (a)(1)-(a)(14), transitions of care (b)(1)-(b)(3), clinical quality measures (c)(1)-(c)(3), patient portal (e)(1), public health reporting (f)(1)-(f)(4), FHIR APIs (g)(7)-(g)(10)), and direct messaging (h)(1). This indicates a full-featured ambulatory EHR, not a niche or specialty-only module.

Patient Chart Manager is available as both cloud-based and on-premise deployments. It is compatible with HL7 for clinical data exchange and DICOM for medical imaging.

### Users & Market

**Target users:** Ambulatory physicians, clinical staff, and practice administrators. The product is designed for solo practices through multi-specialty groups of up to ~100 providers.

**Supported specialties:** The product is explicitly marketed for Allergy, Cardiology, Dermatology, Family Practice, Gastroenterology, Internal Medicine, OB/GYN, Ophthalmology, Orthopedics, Otolaryngology (ENT), Pediatrics, Podiatry, Psychiatry, and Surgery. It also supports multi-specialty practices. It is not specialty-specific — it uses a customizable interface adapted to each specialty.

**Customer base:** More than 10,000 physicians per the vendor's claim (from 2008 silver anniversary press release; current numbers unknown). The company has emphasized long-term customer retention. Known customers include radiology, pediatrics, and multi-specialty practices.

**Market position:** Small/niche vendor in the ambulatory EHR market. Not widely reviewed on major platforms — limited presence on Capterra, G2, etc. User reviews are mixed: some praise the feature richness and long-term reliability; others criticize the interface as dated, with too many sub-menus and pop-ups, and report customer support issues.

### Modules & Functionality

Based on vendor materials, third-party profiles, and documentation fragments, Patient Chart Manager and its integrated practice management platform include:

**Clinical Documentation / EHR (Patient Chart Manager):**
- Electronic patient charting with multiple input methods: keyboard templating, stylus/handwriting on tablet PCs, voice recognition/dictation, and scanned paper documents
- Customizable user interface that can be adapted per user role and specialty — "individual users are not presented with unnecessary options"
- Patient chart search and navigation
- Auto-filing tools for organizing clinical documents
- Digital image integration (DICOM compatible)
- Paperless fax and email input with automatic routing to patient charts
- Clinical decision support functionality (announced as a feature addition)
- Care planning tools

**E-Prescribing:**
- Electronic prescribing, certified and integrated
- Paperless prescription routing to pharmacies
- Pharmacy renewal request handling
- Prescription history tracking

**Lab & Orders:**
- Lab report integration and tracking
- Laboratory interface capabilities
- Allergy tracking

**Patient Portal (certified under (e)(1)):**
- Patient-facing portal for accessing health information
- (Specific portal features were not available due to website maintenance, but certification under (e)(1) confirms view/download/transmit of health information)

**Practice Management (Intellect / OnSTAFF / WebSTAFF):**
- Appointment scheduling (including multi-location scheduling, double-booking support)
- Patient registration and demographics
- Insurance eligibility verification (real-time and batch)
- Medical billing and claims processing (to 1,300+ insurance companies)
- Claim scrubbing
- CMS-1500 claim form generation
- ICD-10 compliant coding
- CPT code reimbursement tracking
- Payment posting and reporting
- Aging reports (auto-generated)
- Payment reminder generation
- Appointment reminders via email, phone, and text
- Monthly, quarterly, and yearly stacked reporting
- Multi-location data sharing for scheduling and billing
- Charge posting

**Transitions of Care / Interoperability:**
- HL7 data exchange
- CCDA document exchange (certified for (b)(1)-(b)(3))
- Direct messaging (certified for (h)(1))
- FHIR API access (certified for (g)(7)-(g)(10))

**Public Health Reporting:**
- Immunization registry reporting (f)(1)
- Syndromic surveillance reporting (f)(2)
- Cancer registry reporting (f)(4)

**Document Management:**
- Document scanning and attachment to patient records
- Digital document and image management
- Integration with external medical equipment and information systems

### Data & Content

Based on the features and certifications described above, the product manages the following data types (with evidence sources):

**Clinical data** (per vendor feature pages and OphthalmologyWeb profile):
- Patient chart records and clinical documentation
- Appointment history
- Prescription history and e-prescribing records
- Lab reports and results
- Allergy lists
- Medical images (DICOM-compatible)
- Scanned documents and faxes
- Care plans
- Clinical decision support alerts/rules

**Administrative/practice management data** (per Intellect PM documentation and Business-Software.com):
- Patient demographics and registration data
- Insurance information and eligibility records
- Appointment/scheduling data
- Billing records, claims, and charge data (CMS-1500 forms)
- Payment records and remittance data
- Aging reports
- CPT/ICD-10 coding data

**Patient portal data** (implied by (e)(1) certification):
- Patient-accessible health summaries
- View/download/transmit records

**Public health reporting data** (per certification criteria):
- Immunization records
- Syndromic surveillance data
- Cancer case reporting data

**Interoperability/exchange data** (per certification criteria):
- CCDA documents (transitions of care)
- Direct messages
- FHIR resources

**Gaps in research:** The vendor's main website was entirely in maintenance mode during this research, so detailed feature pages, screenshots, and current product documentation were not accessible. The practice management components (Intellect, OnSTAFF, WebSTAFF) appear to be separate but tightly integrated products sharing a common database — it is not entirely clear whether the (b)(10) EHI export covers just the Patient Chart Manager EHR data or also the practice management data. The product branding history is somewhat confusing: OnSTAFF appears to be the original practice management product, Intellect a later iteration, and WebSTAFF a web-based version — it's unclear which is current. The Crunchbase profile and other sources indicate the company is small (estimated 11-50 employees based on LinkedIn), and there has been little recent press coverage or product announcements visible online.

---

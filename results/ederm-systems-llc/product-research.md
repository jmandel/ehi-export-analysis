# eDerm Systems LLC — Product Research

Researched: 2026-02-15
Developer website: https://www.edermehr.com/

## Overview

eDerm Systems LLC is a small, privately held EHR vendor based in Boca Raton, Florida, that builds a dermatology-specific EHR and practice management platform. The company describes itself as "built by dermatologists" and positions its product as the "only EMR software company that thinks the way dermatologists think." The company appears to be a niche player focused exclusively on the dermatology specialty. No information about company size (employees, revenue) or customer count is available on their website or third-party sources; the product has only 8 ratings on the Apple App Store and zero reviews on Software Finder, suggesting a relatively small installed base. The company's older domain (edermsystems.org) now redirects to edermehr.com.

The product was ONC certified in October 2019 (v2.8.0) and is actively maintained — the iPad app was last updated in January 2026. The ONC certification page lists "NLM API" and "Updox" as additional integrated software, indicating the product relies on Updox (a third-party patient communication platform) for patient portal / secure messaging functionality.

## Product: eDerm Systems

CHPL ID: 10149

### What It Is

eDerm Systems is an integrated cloud-based EHR, practice management, and revenue cycle management platform designed exclusively for dermatology practices. It is a single product with three main functional areas (EHR, Practice Management, RCM), though the vendor describes these as separately purchasable modules that integrate together. The EHR component runs as a native iPad application, while the Practice Management and Revenue Cycle Management modules run as web applications in a browser (historically Internet Explorer on Windows PCs). All components communicate with a cloud backend.

The certified module encompasses the full eDerm product — there is no indication of separate product lines or platforms sharing this certification.

### Users & Market

**Target users**: Dermatologists and dermatology practice staff (physicians, nurses, billing staff, front desk/schedulers).

**Clinical settings** (per Software Finder and vendor materials):
- Dermatology clinics
- Cosmetic dermatology centers
- Mohs surgery practices
- Dermatopathology labs
- Practice sizes of 1–50 physicians

**SED intended user description** from CHPL: "Ambulatory"

No customer count, site count, or notable customer references were found on the vendor website, third-party review sites, or press releases. The 8 App Store ratings and absence of reviews on major EHR comparison platforms (Capterra, G2) suggest this is a small-footprint product. Custom pricing is used (no published pricing tiers).

### Modules & Functionality

Based on the vendor website (edermehr.com), App Store listing, FAQ page, ehrinpractice.com profile, and softwarefinder.com profile:

**EHR / Clinical Documentation**
- **One-Touch Charting**: Uses a 3D anatomical map where providers tap impressions and body locations for automatic documentation. Designed to mirror paper-based dermatology workflows.
- **Smart Learning**: The system learns and adapts to individual provider preferences over time, customizing the documentation experience.
- **Physical Exam documentation**: Structured dermatology exam templates.
- **Patient Chart**: Comprehensive patient record viewable in chronological order or by subsection (e.g., diagnoses, encounters).
- **Clinical Photography**: Integrated photo capture and management, with unlimited photos automatically associated with patient encounters and records. This is a key dermatology-specific feature.
- **Dermatology Knowledge Base**: Built-in reference including disease descriptions, differential diagnoses, treatment plans, and patient education materials. No template setup required — ships with dermatology-specific content.
- **Patient Education**: Materials available for patient engagement during encounters.
- **Pathology Life Cycle**: A biopsy/pathology tracking module that manages every stage from biopsy order/requisition through results to treatment plan and actual treatment. Includes a biopsy log sortable by patient, disease, laboratory, date range, and pathology status. This is a distinctive dermatology-specific feature.
- **Cancer patient tracking**: Specific functionality for managing and following up on patients with cancer diagnoses (per the practice management page).
- **Document scanning**: Ability to scan and digitize paper documents into the patient record.
- **Consent forms**: Automated consent form generation.
- **Offline capability**: The iPad EHR app continues to function without internet connectivity and syncs when reconnected.

**Practice Management**
- **Patient registration** and demographics management.
- **Scheduling**: Multi-provider, multi-location appointment scheduling with color coding, wait list management, and recall list management. Customizable scheduling templates by physician and location.
- **Insurance verification**: Real-time electronic verification of patient insurance, deductible, co-pay, and account balance at registration and arrival.
- **Document management**: Electronic consent forms, prescriptions, requisitions, pathology reports.
- **Phone messages**: Providers can view and respond to phone messages.
- **Multi-practice/multi-location support**.

**Revenue Cycle Management / Billing**
- **Smart Coder**: Automated coding tool that analyzes clinical notes to suggest billing codes (CPT/ICD-10), designed to "eliminate the need for an experienced coder."
- **Claims processing**: Electronic filing of primary, secondary, and tertiary claims. 98% first-pass rate claimed via their clearinghouse.
- **Claims approval workflow**.
- **Automatic payment posting** from insurers.
- **Collections management**.
- **Financial reporting**.
- **Real-time co-pay and deductible calculation**.

**Patient Portal / Communication (via Updox)**
- The ONC certification page lists Updox as integrated additional software. Updox is a third-party HIPAA-compliant patient communication platform that provides a patient portal, secure messaging, telehealth video, electronic fax, and patient text messaging.
- The eDerm FAQ page states that the patient portal provides "access to medical records only" — no self-registration or payment through the portal.
- This means patient portal/messaging data flows through the Updox platform, which may or may not be fully reflected in eDerm's own data stores.

**Integrations**
- **Surescripts**: Mentioned on softwarefinder.com, suggesting e-prescribing capability (though the vendor website does not prominently feature e-prescribing).
- **NLM API**: Listed as additional integrated software on the ONC certification page, likely used for drug/clinical terminology lookups.
- **Lab interfaces**: The FAQ mentions lab interfaces exist for multiple laboratories, with new ones added regularly.
- **Updox**: Patient portal and communication.
- Third-party "bridges" available if practices prefer not to use eDerm's Practice Management system.

**Certified Criteria** (per CHPL metadata):
- Clinical data: (a)(2) CPOE for lab, (a)(5) demographics, (a)(12) family health history, (a)(14) implantable device list
- Transitions of care: (b)(1) and (b)(2)
- EHI export: (b)(10)
- Care plan: (b)(11) — not listed in metadata but mentioned on ONC page
- CQMs: (c)(1)
- Patient portal: (e)(1)
- FHIR API: (g)(7), (g)(9), (g)(10)
- Security/privacy: multiple (d) criteria

Notable: The certified criteria include (a)(2) CPOE for lab orders, which confirms the system has computerized order entry for laboratory tests. However, CPOE for medications ((a)(1)) is NOT listed, which is notable — this may mean e-prescribing is handled externally (possibly through Surescripts integration) rather than being a certified capability of the eDerm module itself.

### Data & Content

Based on the features described above, the eDerm system stores and manages:

**Clinical data** (evidenced by vendor website and certified criteria):
- Patient demographics (certified (a)(5))
- Family health history (certified (a)(12))
- Implantable device list (certified (a)(14))
- Clinical encounter notes / charting documentation
- Physical exam findings
- Diagnoses (ICD-10)
- Clinical photographs (unlimited, linked to encounters)
- Pathology orders, requisitions, results, and lifecycle tracking (biopsy logs)
- Lab orders (certified (a)(2) CPOE for lab)
- Scanned documents
- Consent forms
- Patient education materials delivered
- Cancer tracking / follow-up data
- Dermatology knowledge base content (disease descriptions, differentials, treatment plans)
- Clinical quality measure data (certified (c)(1))

**Practice management data** (evidenced by vendor website):
- Patient registration and demographics
- Appointment scheduling data (multi-provider, multi-location)
- Insurance information and verification results
- Phone messages
- Wait lists and recall lists
- Provider schedules and templates

**Billing/financial data** (evidenced by vendor website):
- CPT and ICD-10 codes (generated by Smart Coder)
- Insurance claims (primary, secondary, tertiary)
- Payment posting records
- Collections data
- Co-pay and deductible calculations
- Financial reports

**Patient portal / communication data** (via Updox integration):
- Patient portal access to medical records
- Secure messages (unclear whether stored in eDerm or only in Updox)

**Data architecture note**: The EHR runs on iPad communicating to a cloud backend, while PM and RCM run as browser-based web apps against the same cloud. All patient data is cloud-hosted. The Updox integration means some patient communication data may reside in a separate system.

**Gaps / Uncertainties**:
- **E-prescribing**: The vendor website does not prominently describe e-prescribing as a feature, though Surescripts integration is mentioned on one third-party site. CPOE for medications ((a)(1)) is NOT a certified criterion. It's unclear whether prescription data is stored in eDerm or managed externally.
- **Allergies and medication lists**: Not specifically mentioned on the vendor website, though one would expect them in any EHR. Not specifically certified for (a)(1) medication CPOE, (a)(6) problem list, (a)(7) medication list, or (a)(8) allergy list — these are notable absences.
- **Problem list**: Not specifically described as a feature and (a)(6) is not among the certified criteria.
- **Vital signs**: Not specifically mentioned on the vendor website.
- **Referral management**: Not mentioned.
- **Clinical decision support**: The dermatology knowledge base may serve this role, but (a)(9) clinical decision support is not a certified criterion.
- **Immunization data**: Not mentioned, and public health reporting criteria ((f) criteria) are not certified.
- **The vendor website is marketing-focused** and relatively sparse on technical detail. The FAQ page appears somewhat dated (still referencing "Meaningful Use Stage 2" as a future goal, and Internet Explorer as a requirement).

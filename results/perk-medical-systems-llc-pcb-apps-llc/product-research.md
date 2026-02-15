# Perk Medical Systems LLC (PCB Apps LLC) — Product Research

Researched: 2026-02-14
Developer website: https://www.pcbapps.com/

## Overview

Perk Medical Systems LLC (also listed as PCB Apps LLC) is a very small entity that appears to straddle two worlds: a tiny primary care medical clinic in Somerset, NJ, and a health IT software developer. According to Dun & Bradstreet, Perk Medical Systems was founded in 2009, is incorporated, has approximately 3 employees, $230K annual revenue, and is classified under SIC code 80110205 (Primary Care Medical Clinic) at 1 Executive Dr, Somerset, NJ. The same Somerset, NJ address is shared by PCB Apps, a much larger enterprise IT consulting firm (established 2003) that specializes in Oracle, SAP, and other ERP implementations across 22 countries. PCB Apps' main website makes no mention of healthcare EHR products — it focuses on enterprise application consulting for manufacturing, supply chain, life sciences, eCommerce, and finance verticals. The CHPL contact, Ashok Chinthala, appears on LinkedIn as a "TeamLead" or "Lead Consultant" at PCB Apps / Perk Data Systems in Bengaluru, India.

The connection between these entities is opaque but suggests that PCB Apps provides the technical development resources for Perk Medical Systems' EHR product, ezPractice, which is hosted and marketed through a separate domain, penn-clinical.com ("PennClinical — Simplified Healthcare IT"). The product has been in development since at least 2005 (per copyright notices on the live application at jfk.penn-clinical.com). PennClinical's website is minimal, describing "simplified health care IT" with a focus on patient-centered care, telehealth, and wellness management. There is virtually no public marketing, no third-party reviews (G2, Capterra, KLAS), and no visible customer base beyond what appears to be a single practice or very small number of sites. The former perkmedicalsystems.com domain now redirects to an unrelated company (silibrain.com), further suggesting the product has an extremely limited market presence.

The SED (Safety-Enhanced Design) intended user description in CHPL metadata says "Pediatric," indicating the product is designed for or tested with pediatric practices.

## Product: ezPractice

CHPL ID: 11237 (15.07.04.2154.Ezpr.15.01.1.230208)

### What It Is

ezPractice is a certified EHR system developed by Perk Medical Systems, hosted and documented through the penn-clinical.com domain. Based on its broad set of ONC certification criteria, it appears to be a full ambulatory EHR with clinical, interoperability, and patient engagement capabilities — not just a narrow module. The product has been under development since at least 2005 and is currently at version 15.1 (certified February 2023), with a version 14.1 still visible on a live instance (jfk.penn-clinical.com).

The SED metadata indicates the product is designed for pediatric use, though it is unclear whether it is exclusively pediatric-focused or a general ambulatory EHR with pediatric customizations.

### Users & Market

This product has an extremely limited and opaque market presence:

- **No third-party reviews** found on G2, Capterra, KLAS, Software Advice, or any EHR comparison site.
- **No visible customer testimonials or case studies** on the penn-clinical.com website.
- **No marketing materials** describing the product's features in detail.
- The Dun & Bradstreet listing for Perk Medical Systems describes a 3-employee primary care clinic with $230K revenue — the entity may primarily be a physician practice that developed and uses its own EHR software.
- The "jfk" subdomain on the live application instance (jfk.penn-clinical.com) could suggest use at a specific clinical site, though this is speculative.
- Given the lack of any public market presence, ezPractice likely serves a very small number of practices — possibly only the developer's own practice(s).

### Modules & Functionality

Based on the ONC certification criteria and mandatory disclosures, ezPractice is certified for a broad range of ambulatory EHR capabilities:

**Clinical capabilities (a-criteria):**
- (a)(1) CPOE — Medications: Computerized provider order entry for medications
- (a)(2) CPOE — Laboratory: Computerized provider order entry for lab orders
- (a)(3) CPOE — Diagnostic Imaging: Computerized provider order entry for imaging orders
- (a)(4) Drug-Drug, Drug-Allergy Interaction Checks
- (a)(5) Demographics: Recording patient demographics
- (a)(9) Clinical Decision Support
- (a)(12) Family Health History
- (a)(14) Implantable Device List

**Interoperability (b-criteria):**
- (b)(1) Transitions of Care: Sending and receiving C-CDA documents
- (b)(10) EHI Export

**Clinical quality (c-criteria):**
- (c)(1) Clinical Quality Measures: CQMs tested (68v11)

**Patient engagement (e-criteria):**
- (e)(3) Patient Health Information Capture

**API and technical (g-criteria):**
- (g)(3)-(g)(7), (g)(9)-(g)(10): Full FHIR API support, safety-enhanced design, standardized API for patient and population services

**Direct messaging (h-criteria):**
- (h)(1) Direct Project: Direct secure messaging for clinical information exchange

**Third-party dependencies** (from mandatory disclosures):
- **DrFirst Rcopia 4.0**: Used for e-prescribing functionality. Additional per-provider costs apply.
- **EMR Direct Interoperability Engine**: Used for Direct messaging and interoperability requirements. Additional costs apply.

**Not certified for** (notable absences):
- (a)(6) Problem List — not listed, though this is a common ambulatory capability
- (a)(7) Medication List — not listed
- (a)(8) Medication Allergy List — not listed
- (a)(10) Electronic Prescribing — relies on DrFirst Rcopia (listed as third-party dependency)
- (b)(2), (b)(3) — Clinical information reconciliation and electronic prescribing interoperability not certified
- (e)(1) View, Download, and Transmit — patient portal/VDT not certified
- (f)(1)-(f)(7) — No public health reporting criteria certified

The website mentions telehealth capabilities and wellness tracking, though no detail is provided on implementation.

### Data & Content

Based on the certified criteria and product documentation, ezPractice stores and manages:

**Clinical data (from certification criteria):**
- Patient demographics (a)(5)
- Medication orders via CPOE (a)(1) and e-prescribing via DrFirst Rcopia
- Laboratory orders (a)(2)
- Diagnostic imaging orders (a)(3)
- Drug and allergy interaction data (a)(4)
- Clinical decision support rules and alerts (a)(9)
- Family health history (a)(12)
- Implantable device records (a)(14)
- Clinical quality measure data (c)(1) — 68 CQMs tested

**Interoperability/exchange data:**
- C-CDA documents for transitions of care (b)(1)
- Direct messaging content (h)(1)
- FHIR resources via standardized API (g)(10) — the specific FHIR resources supported are documented in a downloadable PDF on penn-clinical.com/api-documentation, not displayed inline

**Patient engagement data:**
- Patient-submitted health information (e)(3)

**What's unclear:**
- **Billing and practice management**: The website does not mention billing, claims, or revenue cycle management. It is unclear whether ezPractice includes integrated billing or whether that is handled separately. Given the small scale of the operation, billing could be a separate system.
- **Scheduling**: No mention of appointment scheduling on the website or in certification criteria.
- **Patient portal**: Not certified for (e)(1) View/Download/Transmit, so it's unclear whether patients have portal access. The penn-clinical.com homepage mentions getting "started on the path to health" and telehealth, which could imply some patient-facing functionality.
- **Notes and documentation**: No specific mention of clinical note templates, progress notes, or encounter documentation, though this is implied by the clinical CPOE and CDS certifications.
- **Immunizations**: Not specifically certified under public health criteria, though pediatric practices typically track immunizations heavily. This may be managed within the system but not separately certified.
- **Growth charts / pediatric-specific features**: The SED metadata says "Pediatric" but no pediatric-specific features (growth charts, well-child visit templates, vaccine schedules) are described anywhere in public materials.

The penn-clinical.com website is notably sparse — the product information page is essentially just the ONC mandatory disclosure, and the API documentation is behind downloadable PDFs. There is no public feature list, module description, or product tour. This makes it difficult to assess the full scope of data managed by the system beyond what can be inferred from certification criteria.

---

## Research Notes

This was an unusually difficult vendor to research due to the extremely limited public information:
- PCB Apps' main website (pcbapps.com) is entirely about enterprise IT consulting and makes no mention of healthcare/EHR products
- PennClinical's website (penn-clinical.com) is minimal with almost no product information beyond ONC compliance pages
- No third-party reviews or market analysis found for ezPractice on any platform
- The vendor appears to be a very small operation — possibly a medical practice that built its own EHR with technical support from the PCB Apps consulting team in India
- The perkmedicalsystems.com domain has been abandoned (redirects to unrelated site)
- The relationship between Perk Medical Systems LLC, PCB Apps LLC, and PennClinical is not clearly documented anywhere

# Lunar Systems, Inc. — Product Research

Researched: 2026-02-15
Developer website: https://golunar.com

## Overview

Lunar Systems, Inc. is a venture-backed stealth startup founded in 2020, headquartered in San Francisco, CA. The company describes itself as building "the world's first AI-native hospital information system" — a ground-up rebuild of hospital IT infrastructure rather than an incremental improvement on legacy systems. The founding team includes doctors, engineers, designers, and hospital operations executives. Lunar is backed by Andreessen Horowitz, Better Tomorrow Ventures, Crossover VC, Rogue Capital, and SNR. The company appears to be early-stage with 11–50 employees (per Wellfound) and remains largely in stealth mode, with very limited public information about specific product capabilities, customer deployments, or feature details.

Lunar specifically targets **smaller hospitals**, positioning its cloud platform as an accessible alternative to the large enterprise EHR vendors. The product spans inpatient, emergency department, and ambulatory settings per its ONC certification description. The company's public messaging emphasizes AI, automation, and modern data architecture as differentiators.

## Product: Lunar Cloud Platform

CHPL IDs: 11698

### What It Is

The Lunar Cloud Platform is a cloud-hosted, comprehensive hospital information system (HIS) designed to serve as the core operational backbone for health systems. It is positioned as an all-in-one platform rather than a modular system — covering clinical, financial, and operational functions across the hospital. The certified module appears to be the platform itself, not a subset of a larger product.

The platform is certified for a broad range of ONC criteria (30+ criteria) spanning clinical data management (a)(1)–(a)(5), (a)(12), (a)(14), transitions of care (b)(1)–(b)(2), patient access (e)(1), (e)(3), clinical quality measures (c)(1)–(c)(3), public health reporting (h)(1), and FHIR-based API access (g)(7), (g)(9), (g)(10). This is a broad certification profile consistent with a full-featured EHR, not a point solution.

The product was certified on September 17, 2025 (version 2.6), making it a very recently certified product.

### Users & Market

**Target users**: Doctors, nurses, pharmacists, lab technicians, coders, billers, supply chain staff, and patients — per Lunar's own marketing language. The SED intended user description explicitly calls out "US-based hospitals, clinics, and health systems in an inpatient, ED, and ambulatory setting."

**Target market**: Smaller hospitals. Lunar positions itself as an alternative to the legacy enterprise EHR vendors (Epic, Oracle Health/Cerner, MEDITECH) that dominate the large health system market.

**Customer information**: No specific customer deployments are publicly disclosed. Job listings reference "partner health systems" and implementation work, suggesting the product is in early deployment or pilot stages. The company's stealth posture makes it unclear how many live sites exist.

**Company size**: Small (11–50 employees per Wellfound). This is a startup, not an established vendor.

**No third-party reviews found**: The product does not appear on G2, Capterra, KLAS, or other review platforms. This is consistent with a pre-market or very early-market product.

### Modules & Functionality

Lunar's public information is deliberately vague about specific modules. The company describes its platform as "powering everything" across the hospital but does not publish a module list or feature breakdown on its website. What we can piece together from multiple sources:

**Clinical (inferred from certifications and job listings)**:
- The ONC certification covers CPOE for medications (a)(1), CPOE for lab orders (a)(2), CPOE for diagnostic imaging (a)(3), drug-drug/drug-allergy interaction checks (a)(4), demographics (a)(5), family health history (a)(12), and implantable device list (a)(14). This implies the product supports core clinical workflows: ordering, documentation, medication management, and clinical decision support.
- Job listings for "Clinical Workflow Informaticist" and "Fractional Clinical Nursing Informaticist" confirm active work on clinical workflows and nursing informatics.

**Revenue cycle / billing (inferred from job listings)**:
- A "Fractional Revenue Cycle Specialist" role is listed, and the company repeatedly mentions "coders" and "billers" as platform users. This strongly suggests the platform includes revenue cycle management functionality — coding, billing, and potentially claims processing.

**Pharmacy**:
- "Pharmacists" are explicitly listed as users. Combined with (a)(1) CPOE for medications and (a)(4) drug interaction checks, the platform appears to support pharmacy workflows.

**Lab**:
- "Lab technicians" are listed as users. Combined with (a)(2) CPOE for lab orders, the platform supports laboratory ordering and likely results management.

**Supply chain**:
- "Supply chain" staff are listed as users, suggesting the platform includes supply chain or materials management capabilities — unusual for an EHR and more typical of a full hospital information system.

**Patient access**:
- Certified for (e)(1) view/download/transmit, meaning there is a patient-facing portal or access mechanism.

**Interoperability**:
- FHIR R4 API via EMR Direct's HealthToGo/Interoperability Engine (endpoint at `api.healthtogo.me`). The API is described as read-only. This is a third-party interoperability layer, not a proprietary API.
- Certified for Direct messaging (h)(1), transitions of care (b)(1)–(b)(2), and clinical information reconciliation (b)(11).

**AI / automation**:
- The company's core differentiator is AI integration. They describe the platform as "AI-native" and emphasize "smarter automation" and "sensible machine learning." No specific AI features are detailed publicly.

### Data & Content

Based on the certification criteria and public descriptions, the Lunar Cloud Platform stores and manages:

- **Clinical data**: Patient demographics, medication lists, allergy lists, problem lists, vital signs, lab orders and results, diagnostic imaging orders, implantable device records, family health history, clinical notes (implied by CPOE and CDS certifications).
- **Medication data**: Prescription data, drug interaction records, medication administration records (implied by (a)(1) and (a)(4) certifications).
- **Order data**: CPOE for medications, labs, and diagnostic imaging.
- **Transitions of care**: C-CDAs and care summaries for transitions (b)(1)–(b)(2).
- **Quality measures**: CQM data per (c)(1)–(c)(3) certifications.
- **Revenue cycle data**: Billing, coding, and likely claims data (based on job listings for Revenue Cycle Specialist and references to "coders" and "billers" as users).
- **Supply chain data**: Likely inventory or materials management data (based on "supply chain" staff being listed as users).
- **Patient portal data**: Patient-accessible health records, and likely messaging (per (e)(1) certification).
- **Audit/security data**: Certified for multiple (d) criteria including audit logging (d)(1)–(d)(2), authentication (d)(3)–(d)(5), encryption (d)(7)–(d)(9), and trusted connection (d)(12)–(d)(13).
- **Interoperability data**: FHIR resources, Direct messages, care documents.

**Gaps in knowledge**: The vendor's stealth posture means we have very little detail on the actual data model, specific clinical documentation capabilities (e.g., whether it supports specialized templates, voice dictation, or structured vs. free-text notes), the depth of revenue cycle features, or what supply chain data specifically looks like. The website is intentionally sparse, and there are no user reviews, case studies, or detailed product documentation available publicly.

**Notable**: The FHIR API is provided through EMR Direct's HealthToGo platform (`api.healthtogo.me`), not through a proprietary Lunar API. This suggests Lunar may be relying on third-party infrastructure for some interoperability capabilities rather than building everything in-house.

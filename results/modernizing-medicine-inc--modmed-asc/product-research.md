# Modernizing Medicine Inc. — Product Research

Researched: 2026-02-15
Developer website: https://www.modmed.com

## Overview

Modernizing Medicine (branded as ModMed) is a healthcare SaaS company founded in 2010 by Daniel Cane (co-founder of Blackboard, Inc.) and Dr. Michael Sherling (a practicing dermatologist). The company is headquartered in Boca Raton, Florida and develops AI-powered, specialty-specific EHR and practice management software. ModMed serves over 40,000 healthcare providers across 11+ medical specialties: dermatology, gastroenterology, ophthalmology, orthopedics, otolaryngology (ENT), allergy/immunology, OB/GYN, pain management, plastic surgery, podiatry, and urology.

ModMed employs approximately 1,900–3,400 people (depending on source and inclusion of contingent workers). The company was previously backed by Warburg Pincus for about eight years, and in April 2025 Clearlake Capital completed a majority investment at a reported ~$5.3 billion valuation. ModMed is not publicly traded. The company's core EHR product is EMA (Electronic Medical Assistant), and for gastroenterology specifically, they offer gGastro. ModMed ASC is a distinct product focused on ambulatory surgery centers. Note: the company was formerly associated with gMed (a GI-focused EHR vendor it acquired/merged with).

## Product: ModMed ASC

CHPL IDs: 11701

### What It Is

ModMed ASC is a cloud-based software platform purpose-built for ambulatory surgery centers (ASCs). It is not a standalone full EHR in the traditional sense — it is an ASC-specific charting, documentation, scheduling, and billing system that connects with and pulls data from ModMed's broader practice EHR products (EMA for most specialties, gGastro for gastroenterology). The certified product number (15.04.04.2002.mASC.06.11.0.250902) identifies it as "ModMed ASC" version 6, certified September 2025.

The product is certified across a broad set of ONC criteria including clinical data (a)(1)–(a)(5), (a)(12), (a)(14); transitions of care (b)(1)–(b)(2), (b)(10)–(b)(11); clinical quality measures (c)(1)–(c)(3); patient portal/VDT (e)(1), (e)(3); public health (f)(5), (f)(7); and API/FHIR (g)(2)–(g)(7), (g)(9)–(g)(10). This broad certification indicates it functions as a comprehensive clinical system for the ASC setting, not just a peripheral charting tool.

The SED intended users are MDs, PAs, MAs, Nurses, and Administrators — reflecting the multi-role workflows in a surgery center.

### Users & Market

ModMed ASC is used primarily by:
- **Ophthalmology ASCs** — surgery centers doing cataracts, retinal procedures, blepharoplasty, etc.
- **Gastroenterology ASCs** — endoscopy centers doing colonoscopies, EGDs, biopsies, polypectomies
- Potentially other specialties (orthopedics, pain management) though marketing emphasis is strongest on ophthalmology and GI

Day-to-day users include surgeons/physicians, nurses, anesthesiologists, medical assistants, and administrative/billing staff. The Empire Surgery Center case study (ophthalmology) and the Tri-County Gastroenterology case study illustrate typical deployments — small to mid-size specialty surgery centers replacing paper-based or fragmented systems with integrated digital documentation.

ModMed does not publish specific customer counts for the ASC product separately from their overall 40,000+ provider base.

### Modules & Functionality

Based on vendor materials, case studies, and third-party profiles, ModMed ASC includes or integrates with the following modules and capabilities:

**Surgical Documentation & Charting**
- Specialty-specific surgical narrative templates (customizable per procedure type — e.g., different templates for cataract extraction vs. blepharoplasty)
- Concurrent charting: nurses, anesthesiologists, and physicians can document simultaneously
- Anesthesia notes and nursing notes that auto-populate into the operative report
- Pre-operative, intra-operative, and post-operative nursing documentation
- Discharge records and summaries
- Endoscopy Report Writer (ERW) for GI — generates procedure notes, discharge summaries, and referral letters
- Data from vital signs monitors and medical imaging equipment can interface directly into the procedure note
- Intelligent prompting: e.g., when documenting a polyp finding, system prompts for follow-up intervals

**Scheduling**
- Surgical case scheduling
- Out-of-pocket cost estimates for patients
- Schedule data flows from practice management into the ASC system

**Billing & Revenue Cycle**
- Integrated billing for professional, office, ASC, and facility charges on the same platform
- Automated insurance eligibility checks
- Claims scrubbing
- ICD-10 and CPT coding support (auto-suggested based on exam content)

**Compliance & Quality Reporting**
- Built-in ASC Quality Reporting (ASCQR) measures and tracking
- Supports Joint Commission, AAAHC, Quad A, CMS, and ACHC accreditation requirements
- GIQuIC reporting for GI endoscopy quality
- OAS CAHPS (Outpatient and Ambulatory Surgery Consumer Assessment) survey data collection
- Quality assurance reports, surgical flow delay tracking

**Patient Engagement**
- Patient portal (gPortal for GI; ModMed patient portal for other specialties) — patients can view charts, access diagnoses, visit notes, educational handouts, test results, request refills, send encrypted messages
- Digital kiosks for patient check-in
- Online patient intake forms
- Automated reminders

**Integration with Practice EHR**
- Patient medical/social history, scheduling information, and demographics flow from EMA or gGastro EHR and ModMed Practice Management into ModMed ASC in real time
- Clinical data from the office EHR syncs to the ASC to reduce re-entry
- Cloud-based — data syncs in near-real time across all facilities

**Analytics & Reporting**
- Procedural quality metrics
- Efficiency tracking (e.g., check-in to discharge times)
- Compliance reporting
- Referral pattern analysis
- Staff performance metrics

**Communication**
- Time-stamped signature capabilities
- Pre-surgical chart checks
- Direct messaging
- Document faxing

**E-Prescribing**
- Certified through Surescripts for e-prescribing (per the EMA EHR; unclear if ASC module directly includes this or inherits it from the practice EHR)

**Lab Integration**
- Electronic lab orders and results exchange (via EMA EHR; the ASC product likely inherits lab connectivity through the practice EHR integration)

**FHIR API Access**
- Certified for (g)(10) Standardized API for patient and population services — FHIR-based API access

### Data & Content

Based on the features, case studies, and vendor descriptions, ModMed ASC manages or has access to the following data types:

- **Patient demographics** and registration information
- **Medical and social history** (pulled from practice EHR)
- **Insurance and eligibility data**
- **Surgical schedules and case details**
- **Pre-operative assessments and clearances**
- **Consent forms**
- **Medication lists** (medications entered on pre-procedure notes populate anesthesia notes in real time)
- **Anesthesia documentation** (anesthesia notes, vital signs, medication administration)
- **Nursing notes** (pre-op, intra-op, post-op)
- **Operative/procedure reports** (surgical narratives, endoscopy reports)
- **Vital signs** (interfaced from monitors)
- **Medical imaging data** (interfaced from imaging equipment)
- **Findings and diagnoses** (e.g., polyp characteristics, pathology referrals)
- **Discharge records and instructions**
- **Billing data** — claims, charges (professional, facility, ASC), insurance eligibility, scrubbed claims
- **Quality measure data** (ASCQR, GIQuIC, OAS CAHPS)
- **Patient portal content** — messages, educational materials, visit summaries, test results
- **Referral letters and correspondence**
- **Analytics data** — efficiency metrics, quality metrics, referral patterns
- **Audit trails** (time-stamped signatures, documentation timestamps)

The case study evidence is clear that this is a comprehensive system — the Empire Surgery Center case study specifically notes it replaced paper-based operative reports and nursing documentation, and administrators can retrieve "comprehensive patient and procedure information in seconds." The GI blog post confirms that office EHR, ASC EHR (ERW), and practice management billing all operate on the same platform.

**Gaps/uncertainties:**
- It's unclear how much clinical decision support (CDS) the ASC module provides independently vs. relying on the practice EHR
- The extent of CPOE (computerized physician order entry) within the ASC context is not well documented — most ASC procedures involve standing orders and protocols rather than extensive order entry
- Whether the ASC product stores its own independent patient record or primarily references the practice EHR record is somewhat ambiguous — the integration seems tight, but the certification as a separate product suggests it has its own data store
- The vendor website is not particularly detailed about technical architecture — most content is marketing-oriented

# Mendelson Kornblum Orthopedic & Spine Specialists — Product Research

Researched: 2026-02-14
Developer website: http://www.mendelsonortho.com/ (redirects to https://synergyhealth.org/)

## Overview

Mendelson Kornblum Orthopedic & Spine Specialists (MKO) is a multi-location orthopedic practice group in Southeast Michigan, founded in 1963 by Dr. Herbert Mendelson. The practice has grown from a small family orthopedic office specializing in spine, neck, and back pain into a large musculoskeletal care organization with over 20 physicians across multiple locations (Livonia, Sterling Heights, Southfield, Port Huron, and others). The practice has rebranded under the umbrella of **Synergy Health Partners** (SHP), which is described as "Michigan's only integrated musculoskeletal care provider." MKO remains the premier orthopedic practice within SHP. The Mendelson family continues in leadership — three sons of the founder (David, Jeffrey, and Stephen Mendelson) are orthopedic surgeons who co-own and manage the practice along with Dr. Martin Kornblum.

OrthoplexEMR is a **custom-built, single-organization EMR** — it was developed specifically for MKO/SHP and is not a commercially sold product. The mandatory disclosures page explicitly states "there are currently no plans for its sale." The EMR was built by **Proactive Technology Management**, a small managed IT services company based in Bingham Farms, Michigan (Metro Detroit), which is co-founded and owned by **Michael Weinberger**. Weinberger serves as CTO of both Proactive Technology Management and Synergy Health Partners MSO, LLC, making him the technical architect for both the IT infrastructure and the EMR. The CHPL contact, **Jurgen B. Jansen** (jjansen@synergyhealth.org), is an IT Project Manager at SynergyHealth. This is an unusually tight coupling between a clinical practice, its IT services provider, and its certified EMR — essentially an in-house software project.

## Product: OrthoplexEMR

CHPL ID: 9349
CHPL Product Number: 15.04.04.3014.Orth.01.00.1.180101
Certification Date: 2018-01-01

### What It Is

OrthoplexEMR is a proprietary, custom-built electronic medical records application developed by Proactive Technology Management for use exclusively by Mendelson Kornblum Orthopedic & Spine Specialists / Synergy Health Partners. It is certified as a complete Health IT Module with a broad set of ONC certifications covering clinical data management, care transitions, patient portal, public health reporting, and FHIR APIs.

The certified product is the entire EMR — there is no separate commercial product suite. The SED (Safety-enhanced Design) intended user description is simply "Orthopedic Clinc" [sic], confirming the narrow target audience.

### Users & Market

- **Single customer**: MKO/Synergy Health Partners. This is not a commercial EMR product.
- **End users**: Orthopedic surgeons, spine specialists, pain management physicians, podiatrists, and clinical staff at MKO/SHP locations across Southeast Michigan.
- **Setting**: Multi-site orthopedic practice group with 20+ physicians, including outpatient clinics, physical/occupational therapy sites, MRI imaging centers, and ambulatory surgery centers.
- **No commercial market**: The disclosure page states there are no plans to sell the software.

### Modules & Functionality

Because OrthoplexEMR is a custom in-house product, there is very limited public documentation of its features beyond what can be inferred from its ONC certification criteria and required dependencies. The product does not have a marketing website, feature pages, or third-party reviews.

**What the certification criteria tell us:**
- **(a)(1)–(a)(5)**: CPOE for medications, labs, imaging; drug-drug/drug-allergy interaction checks; demographics; vital signs; problem list — standard clinical documentation capabilities
- **(a)(12)**: Family health history
- **(a)(14)**: Implantable device list — particularly relevant for an orthopedic practice performing joint replacements
- **(b)(1)–(b)(3)**: Transitions of care, clinical information reconciliation — C-CDA document generation and consumption
- **(b)(10)–(b)(11)**: EHI export and care plan functionality
- **(c)(1)–(c)(3)**: Clinical quality measures — specifically CMS50v6, CMS68v7, CMS123v6, CMS134v6, CMS138v6, CMS139v6 (covering referrals, medication documentation, diabetes care, chronic kidney disease, tobacco, and falls screening)
- **(e)(1), (e)(3)**: Patient portal / view-download-transmit; patient health information capture
- **(f)(1), (f)(4)**: Immunization registry and syndromic surveillance public health reporting
- **(g)(3)–(g)(7), (g)(9)–(g)(10)**: Safety-enhanced design, quality management, accessibility, consolidated CDA creation, application access, and FHIR API access
- **(h)(1)**: Direct Project messaging

**Required dependencies (from mandatory disclosures):**
- **MDToolbox**: E-prescribing module (electronic prescribing, EPCS, prior authorization). This tells us prescribing workflows are not native to OrthoplexEMR — they use MDToolbox as an integrated third-party service.
- **EMRDirect**: Direct messaging HISP service for secure clinical data exchange (C-CDA transmission). This handles the (h)(1) Direct Project requirements.
- **e-IMO (Intelligent Medical Objects)**: Clinical terminology and vocabulary service. IMO provides clinician-friendly diagnosis terms mapped to ICD, SNOMED CT, and other code sets. This means the system uses IMO for problem list, diagnosis coding, and likely billing code selection.
- **SMTP (generic)**: Email integration for notifications and secure messaging.

**What the EHI export page reveals about system content:**
The EHI export documentation describes C-CDA–based exports containing: demographics, encounters, medications, problems, allergies/adverse reactions, vital signs, care team information, immunizations, social history, medical equipment, test results, procedures, goals, health concerns, and treatment plans. This suggests these are the core clinical data domains the system manages.

### Data & Content

Based on the evidence gathered, OrthoplexEMR stores and manages:

**Clinical data (confirmed by certification + EHI export page):**
- Patient demographics
- Problem lists / diagnoses (using IMO terminology mapped to ICD/SNOMED)
- Medication lists and prescribing data (via MDToolbox integration)
- Allergy and adverse reaction records
- Vital signs
- Encounter records
- Procedures
- Test/lab results
- Immunization records
- Social history
- Medical equipment / implantable devices (especially relevant for orthopedic implants)
- Care team information
- Goals, health concerns, and treatment plans
- Family health history
- Clinical quality measure data

**Likely stored but not directly confirmed from public sources:**
- Clinical notes and documentation (implied by EMR use in a 20+ physician practice)
- Imaging orders and possibly results (certified for CPOE imaging orders; MKO operates MRI centers)
- Referral data (CMS50v6 is a referral measure)
- Patient portal messages and patient-submitted health information (certified for (e)(1) and (e)(3))
- Documents exchanged via Direct messaging (via EMRDirect)

**Unclear / not confirmed:**
- **Billing and claims data**: The website and disclosures do not mention whether OrthoplexEMR includes billing/practice management functionality. Michael Weinberger's bio mentions expertise in "medical billing, scheduling, and credentialing systems," and the intake portal (intake.mendelsonortho.com) exists as a separate system, suggesting the practice may use separate systems for scheduling, billing, and intake. It is unclear whether these functions are part of OrthoplexEMR or handled by separate software.
- **Scheduling**: The practice has a separate intake portal; scheduling may be separate from the EMR.
- **Imaging/PACS**: MKO operates MRI centers, but whether PACS data is integrated into OrthoplexEMR or managed separately is unknown.
- **Surgical records**: As an orthopedic surgery practice with ambulatory surgery centers, operative notes and surgical records are presumably part of the EMR, but this is not documented publicly.
- **Physical/occupational therapy records**: SHP includes PT/OT services; whether those notes are in OrthoplexEMR or a separate system is unknown.

### Research Gaps

This is an exceptionally difficult product to research because:
1. It is a custom in-house EMR with no commercial presence, marketing materials, or public feature documentation.
2. There are no third-party reviews on G2, Capterra, KLAS, or similar platforms.
3. The vendor website (mendelsonortho.com) redirects to the clinical practice's site (synergyhealth.org), which focuses on patient-facing information and says nothing about the EMR.
4. The developer (Proactive Technology Management) does not mention OrthoplexEMR on its own website.
5. The only technical documentation available is the ONC mandatory disclosures page and the EHI export page.

The product's scope and data coverage must therefore be inferred primarily from its ONC certification criteria, required dependencies, and the clinical context of a large multi-site orthopedic practice group with surgery centers, imaging, PT/OT, and pain management services.

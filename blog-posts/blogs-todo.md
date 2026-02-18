# Blog Post Series: Planned Content

## Published / Near-Final

1. **"Your C-CDA Is Exquisitely Unlikely to Be a Satisfactory EHI Export"** (`ccda-is-not-ehi.md`)
   - Status: Published
   - Angle: C-CDA as format ≠ C-CDA as complete EHI export

2. **"Five Ways EHR Vendors Fail at EHI Export Documentation"** (`worst-of-the-worst.md`)
   - Status: Published
   - Angle: Five named F-grade failure modes (link rot, 62 words, no docs, screenshots only, footnote)

3. **"What 217 Certified EHRs Actually Export"** (`state-of-ehi-export.md`)
   - Status: Near-final draft
   - Angle: Flagship findings piece (grades, billing litmus test, specialty gaps, BH, portal messages, policy recs)

---

## Planned Posts

### 4. How We Analyzed 217 EHR Exports with AI Agents

**File:** `pipeline-post.md`
**Audience:** Technical, AI/ML, health IT developers
**Distinct from flagship because:** The flagship says *what* we found; this says *how* we found it.

**Outline:**

- **The problem:** 217 vendors, each with a different documentation URL pointing to PDFs, HTML pages, zip files, or nothing. How do you systematically evaluate all of them?
- **Pipeline architecture:** Four-stage cascade, each stage autonomous
  - Phase 1 (research): AI agent researches vendor/product, navigates to CHPL-registered URL
  - Phase 2 (download): Agent downloads everything it finds (PDFs, HTML, data dictionaries, zips)
  - Phase 3 (analysis): Deep narrative assessment against what the product stores
  - Phase 4 (summary): Structured JSON extraction from analysis using a TypeScript schema
- **The prompt engineering:** How each stage's prompt defines quality expectations (not just "go download stuff" but detailed output specs for navigation journals, coverage assessments, enrichment scripts)
- **Fixup workflow:** When an agent misses something, a repair agent diagnoses the root-cause stage, fixes it, and cascades downstream automatically
- **The enrichment pattern:** When agents download a 12MB zip of 7,672 HTML files (Epic), they write extraction scripts on the fly to parse them into structured JSON
- **Grading with schema-driven extraction:** The TypeScript interface *is* the prompt. Add a field with JSDoc comments and the pipeline picks it up. Schema-agnostic extraction.
- **What went wrong:** Common failure modes (SPAs that need browser rendering, PDF viewers that hide the actual PDF URL, vendors who put docs behind auth walls). The stale-output watchdog. Timeout tuning.
- **Reproducibility:** Everything is open source. Prompts, raw data, analysis outputs, the loop controller. Anyone can rerun or audit.
- **What this approach can and can't do:** It evaluates *documentation*, not actual exports. We can tell you what the vendor says the export contains; we can't tell you what a real patient receives.

**Key artifacts to reference:** `wiggum/loop.ts`, prompt templates, `abstraction/ehi-summary-schema.ts`, `architecture.svg`, pipeline diagram

---

### 5. What A-Grade EHI Exports Actually Look Like

**File:** `what-good-looks-like.md`
**Audience:** Health IT developers, EHR vendors, policy/regulatory
**Distinct from flagship because:** The flagship uses A-grades as contrast; this post is a constructive deep dive into what "good" actually means in practice, with enough detail for a vendor to use as a blueprint.

**Outline:**

- **The thesis:** 28 product families got it right. They span the full range of vendor size, specialty, and technical approach. There is no excuse for not doing this.
- **Four architectures that work:**
  1. **Native database dump** (Epic, Oracle Health, eClinicalWorks, Greenway): Export the internal data model as-is (TSV, CSV, SQL). Pros: complete by construction, easy to implement if you have a reporting DB. Cons: documentation burden is huge (Epic has 63,121 field descriptions to maintain).
  2. **Purpose-built FHIR mapping** (athenahealth): Invent custom FHIR resource types for billing, scheduling, and other domains that standard FHIR doesn't cover. 9 custom financial resources with 506 fields. Pros: interoperable format, self-describing. Cons: significant mapping investment.
  3. **Hybrid** (several): FHIR or C-CDA for clinical data + native format for billing/specialty/admin. Best of both worlds if documented well.
  4. **Small vendor, big effort** (Crystal Practice Management, nAbleMD, OpenEMR): Proves size doesn't determine quality. Crystal has 80 entities and a 921-page data dictionary. nAbleMD has 30 IVF-specific entities with fields like `CleftChin` and `catheter_depth`.
- **What the documentation looks like for each:** Walk through what a developer receiving one of these exports would actually see. Field descriptions, types, relationships, value sets, sample data.
- **Common patterns among A-grades:**
  - Billing is always present (94%)
  - Entity counts vary enormously (48 to 7,672) but coverage relative to product scope is high
  - Most have field-level descriptions (not just table names)
  - Almost none provide sample data (this is the universal gap even among A-grades)
  - Several still exclude patient communications (the last mile)
- **The documentation quality spectrum:** Even among A-grades there's a range. Oracle Health at 130,853 columns with 99.9% descriptions vs. vendors with table names but no field docs.
- **Takeaway for vendors:** You don't need to be Epic. You need to (1) enumerate what your product stores, (2) export all of it, (3) document the fields. A 50-table product with complete documentation is an A. A 7,000-table product with no descriptions would be a B at best.

---

### 6. Deregulation and the EHI Feedback Loop

**File:** `deregulation-and-ehi.md`
**Audience:** Policy, regulatory, patient advocates
**Distinct from flagship because:** The flagship's "So now what" section sketches three recommendations in a paragraph each. This post goes deep on the structural problem (no feedback loop) and the specific regulatory levers.

**Outline:**

- **The structural problem:** There is no functioning feedback loop for EHI export quality.
  - (b)(10) is attestation-based; no test lab runs an export
  - Documentation URLs are public but nobody reviews them systematically
  - The only way to discover a broken export today is for a patient to request their records, wait weeks, receive the export, have the technical sophistication to evaluate it, and then figure out where to complain
  - That loop is too long, too rare, and too quiet to drive vendor behavior
- **The API fix:** A patient-facing EHI export API (same SMART on FHIR authorization as g(10), with a full-EHI scope) would collapse the feedback loop
  - Every health app that can pull USCDI today could also pull EHI
  - Automated comparison across vendors becomes trivial
  - "Many eyes make broken exports hard to hide"
  - Incremental infrastructure cost is low: every vendor in the CPOE+(g)(10) cohort already has the auth framework; the new piece is scope expansion
  - This is the single highest-leverage regulatory change ONC could make
- **Existing oversight tools that need no new rulemaking:**
  - ONC-ACB in-the-field surveillance: ACBs can already request documentation and verify products perform as certified
  - ONC direct review: ONC can review any product when there's reason to believe it's noncompliant
  - These powers exist; they just haven't been aimed at (b)(10) documentation content
  - Proactive use of these tools could shift vendor posture without any new regulation
- **The HTI-5 risk:** The proposed HTI-5 rule would roll back Real World Testing requirements for (b)(10)
  - RWT is already thin (vendors report "number of exports run," not content quality)
  - But eliminating it entirely removes even that minimal visibility
  - At a moment when the data shows 54% of products are delivering stubs, reducing oversight is the wrong direction
- **What accountability looks like in practice:**
  - Public documentation review (which this project demonstrates is feasible at scale)
  - API-enabled ecosystem testing (which (g)(10) has proven works for USCDI)
  - The precedent: (g)(10) compliance improved dramatically once apps could actually call the APIs and report problems. The same dynamic would work for (b)(10) if there were an API to call.
- **Tone:** Constructive, not adversarial. Frame as: the tools exist, the data is clear, the fix is architectural (API) + operational (use existing oversight powers). Not calling for new bureaucracy; calling for using what's already there.

---

## Possible Future Posts (Not Yet Outlined)

- **"The g(10) Relabel"**: Quantify the specific pattern of pointing (b)(10) documentation at existing (g)(10) FHIR API specs. Different from C-CDA post because it's about API specs, not clinical documents.
- **"What Patients Actually Receive"**: Non-technical, patient-facing. Walk through the experience of requesting records from a D-grade vendor.
- **"Native vs. Standards-Based: A False Debate"**: The approach axis is orthogonal to quality. Some native exports are stubs; some FHIR exports are comprehensive.
- **Vendor response tracker**: As vendors improve in response to this analysis, track and credit the changes.

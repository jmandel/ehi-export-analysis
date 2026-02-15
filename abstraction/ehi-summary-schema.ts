/**
 * EHI Export Summary Schema
 *
 * This TypeScript interface defines the structured JSON output extracted from
 * each vendor's analysis.md file. The LLM reads this interface (including all
 * comments) and produces a conforming JSON object.
 *
 * To add new fields: add them to the interface with JSDoc comments explaining
 * exactly how to derive the value. Then re-run the summary pipeline — it will
 * pick up the new fields automatically.
 */

export interface EhiExportSummary {
  /** Vendor directory slug (e.g., "aarista-technology-llc") */
  vendor_slug: string;

  /** Product name as stated in analysis.md header */
  product_name: string;

  /**
   * Holistic quality score from 0 to 10 (integer or half-point, e.g. 7.5).
   *
   * This is a single comprehensive rating of how well the vendor has met the
   * §170.315(b)(10) EHI export requirement. It should reflect a balanced
   * assessment across ALL of the following dimensions:
   *
   * **Coverage (weight ~30%)**:
   * - What fraction of the product's known data domains are represented in the
   *   export? Check Section 5b's domain coverage table.
   * - Are there certified capabilities (e.g., care plans under (b)(11),
   *   implantable devices under (a)(14)) with NO export representation?
   * - Does the export cover clinical, billing, administrative, and specialty data?
   *
   * **Documentation quality (weight ~25%)**:
   * - What percentage of fields have descriptions? (Section 7 Summary Stats)
   * - Are value sets / code systems documented?
   * - Are relationships / foreign keys documented?
   * - Is the export file format clearly specified?
   * - Is there sample data?
   *
   * **Data structure quality (weight ~20%)**:
   * - Is the data structured and coded, or are clinical fields free-text blobs?
   * - Are multi-valued fields properly normalized (separate rows) or packed into
   *   single delimited strings?
   * - Is the export a native database model (good) or a C-CDA/FHIR repackaging
   *   that only covers ~20% of the product's data?
   *
   * **Usability / developer experience (weight ~15%)**:
   * - Could a developer build an import from the documentation alone?
   * - Are there machine-readable schemas (JSON Schema, DDL, XSD)?
   * - Is the export self-service or does it require vendor assistance?
   *
   * **Regulatory alignment (weight ~10%)**:
   * - Does the export cover the full Designated Record Set, or just clinical
   *   summaries?
   * - Is the export available without fees or excessive restrictions?
   * - Has the documentation been maintained since certification?
   *
   * **Scoring guide**:
   * - 0–1: No meaningful export (empty docs, just a paragraph saying "we comply")
   * - 2–3: Minimal stub (a few pages, covers <20% of data, no usable detail)
   * - 4–5: Partial effort (some documentation exists but major gaps in coverage
   *   or quality — e.g., fields without descriptions, free-text blobs, missing
   *   domains)
   * - 6–7: Solid but incomplete (good coverage of core domains, reasonable docs,
   *   but notable gaps — missing specialty data, no sample data, thin billing)
   * - 8–9: Comprehensive (native database export, high field coverage, good
   *   descriptions, most domains covered, minor gaps only)
   * - 10: Exceptional (exhaustive native export, 100% described fields, sample
   *   data, machine-readable schemas, relationships documented, all domains)
   *
   * Derive this score from the analysis.md's Section 7 (Overall Assessment),
   * Section 5b (coverage table), Section 6 (documentation quality), and the
   * Summary Stats block. Cross-reference the classification:
   * - "minimal_stub" → typically 0–2
   * - "standard_projection" → typically 2–4
   * - "partial_native" → typically 3–6
   * - "comprehensive_native" → typically 7–10
   */
  holistic_score: number;
}

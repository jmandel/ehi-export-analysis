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
   * A Zagat-style pithy summary of the vendor's EHI export quality.
   *
   * Write 2-3 punchy sentences in the style of a Zagat restaurant review:
   * opinionated, vivid, and information-dense. Use sentence fragments freely.
   * Capture what makes this vendor's export distinctive — both good and bad.
   *
   * Focus on the most striking/notable aspects:
   * - What kind of export is it? (native DB dump, deep FHIR mapping, C-CDA stub)
   * - What's the single biggest strength or gap?
   * - Any notable quirks, ironies, or red flags?
   *
   * Keep it under 300 characters. Be direct and specific — every word
   * should convey information.
   */
  summary: string;

  /**
   * Letter grade for overall (b)(10) EHI export quality.
   *
   * This is an absolute grade (not curved) reflecting how well the vendor
   * meets the §170.315(b)(10) requirement. Use +/- modifiers for precision.
   *
   * The grade should reflect a balanced assessment across:
   * - **Coverage** (~40%): What fraction of the product's data domains are
   *   in the export? Must go beyond USCDI to score well — USCDI is a floor
   *   for clinical exchange, not EHI completeness. Check Section 5b.
   * - **Documentation quality** (~25%): Field descriptions, value sets,
   *   relationships, format specs, sample data. Check Section 6.
   * - **Data structure quality** (~20%): Structured/coded data vs free-text
   *   blobs? Normalized or packed? Machine-parseable?
   * - **Usability** (~15%): Could a developer build an import from the docs
   *   alone? Machine-readable schemas? Self-service export?
   *
   * **Grading rubric**:
   * - **A/A-**: Purpose-built export, comprehensive coverage of product's
   *   data domains (clinical + billing + specialty + administrative as
   *   applicable), well-documented with field descriptions, machine-readable.
   *   A = exceptional (sample data, relationships, value sets). A- = strong
   *   but minor gaps.
   * - **B+/B/B-**: Genuine effort with notable limitations. Might have broad
   *   coverage but thin documentation, or excellent documentation but missing
   *   domains. B+ = close to A-. B- = clear gaps but real substance.
   * - **C+/C/C-**: Partial effort. Some domains covered, some documentation
   *   exists, but significant gaps in coverage or quality. Not just a stub,
   *   but not thorough. C+ = leans toward adequate. C- = barely above D.
   * - **D+/D/D-**: Minimal effort. Very thin documentation, very limited
   *   coverage, or export that barely goes beyond a clinical summary.
   *   D+ = some evidence of trying. D- = essentially a stub with a veneer.
   * - **F**: No meaningful export. Empty docs, a paragraph saying "we comply,"
   *   or documentation so thin that you cannot determine what's exported.
   *
   * Derive from analysis.md Sections 5b, 6, and 7. The grade must be
   * independently defensible from the evidence.
   */
  grade: "A" | "A-" | "B+" | "B" | "B-" | "C+" | "C" | "C-" | "D+" | "D" | "D-" | "F";

  /**
   * How much of the product's stored data the export covers.
   *
   * Coverage is about BREADTH — what fraction of the product's data domains
   * appear in the export. This is independent of format or approach: a FHIR
   * export mapping 50+ resource types across clinical, billing, and specialty
   * domains is "comprehensive" even though it uses a standard format. A native
   * database dump that only exports clinical tables is "partial" even though
   * it uses the vendor's own schema.
   *
   * Coverage is relative to the product's capabilities (a simple charting
   * tool has fewer domains than a full hospital EHR). Must go meaningfully
   * beyond USCDI — USCDI is a floor for clinical exchange, not EHI
   * completeness.
   *
   * - "comprehensive" — Export covers most/all applicable data domains
   * - "partial" — Some domains covered well, but significant gaps relative
   *   to what the product stores
   * - "minimal_stub_unclear" — Too thin to assess, or clearly covers only
   *   a tiny fraction of what the product stores
   *
   * Derive from Section 5b (domain coverage table) cross-referenced with
   * Section 1 (product context).
   */
  coverage: "comprehensive" | "partial" | "minimal_stub_unclear";

  /**
   * What data model the export uses.
   *
   * This describes the structural approach — whose schema is the data in?
   * This is INDEPENDENT of quality or coverage. A native export can be thin;
   * a standards-based export can be comprehensive. The format does NOT
   * determine whether an export is genuine (b)(10).
   *
   * Key example: A vendor that maps 50+ EHR-specific concepts to FHIR
   * resources (including billing, custom forms, specialty data) is
   * "standards_based" AND likely "comprehensive" — this is fundamentally
   * different from a vendor pointing at their existing (g)(10) FHIR API,
   * which is also "standards_based" but "partial" or "minimal_stub_unclear."
   * The coverage axis distinguishes those cases, not this one.
   *
   * - "native" — Export uses the product's own data structures: proprietary
   *   tables, internal entity models, database dumps, vendor-defined schemas.
   * - "standards_based" — Export uses established health data standards as the
   *   data model: FHIR resources, C-CDA sections, HL7v2, etc. This includes
   *   both lazy g(10) relabels AND deep purpose-built FHIR/CDA mappings.
   * - "hybrid" — Mix of native and standards-based formats (e.g., FHIR bundle
   *   for clinical data + CSV/TSV for billing, or C-CDA + native database
   *   supplements).
   * - "unclear" — Cannot determine from documentation.
   *
   * Derive from Sections 3-4 (export mechanics and content).
   */
  approach: "native" | "standards_based" | "hybrid" | "unclear";

  /**
   * Export file format(s) used.
   *
   * List all formats present in the export. Use short canonical names.
   * Order from most prominent to least.
   *
   * Common values: "CSV", "TSV", "FHIR NDJSON", "FHIR JSON", "C-CDA",
   * "JSON", "XML", "PDF", "SQL", "XLSX", "HTML"
   *
   * Derive from Section 3 (export mechanics).
   */
  export_formats: string[];

  /**
   * Number of entities (tables, resources, sections) documented in the export.
   * null if no data dictionary or structured documentation exists.
   * Derive from Section 7 Summary Stats or Section 4.
   */
  entity_count: number | null;

  /**
   * Total fields/columns documented across all entities.
   * null if no field-level documentation exists.
   * Derive from Section 7 Summary Stats or Section 4.
   */
  field_count: number | null;

  /**
   * Whether the vendor provides a data dictionary — a structured listing
   * of entities and fields with at least field names and types.
   * Derive from Section 6 (documentation quality).
   */
  has_data_dictionary: boolean;

  /**
   * Whether sample/example export files are provided in the documentation.
   * Derive from Section 6 or artifacts in downloads/.
   */
  has_sample_data: boolean;

  /**
   * Whether billing/financial data (claims, charges, payments, insurance,
   * revenue cycle) is included in the export.
   *
   * This is a critical signal for (b)(10) seriousness — most EHRs store
   * billing data, and its absence from the export is a major gap.
   *
   * - true — Billing entities/fields are present in the export
   * - false — Product does billing but export omits it
   * - null — Cannot determine, or product does not do billing
   *
   * Derive from Section 5b (domain coverage table) for billing/claims domains,
   * cross-referenced with Section 1 (does the product do billing?).
   */
  billing_included: boolean | null;

  /**
   * Whether patient-provider communications that the product manages are
   * represented in the EHI export.
   *
   * Many EHR products include patient portals, secure messaging, phone call
   * logging, or other communication tools. These communications are part of
   * the designated record set (used for care decisions) and should be in the
   * export. Derive this by comparing what communication features the product
   * offers (Section 1 product context) against what appears in the export
   * (Sections 4-5).
   *
   * - "not_applicable" — Product has no patient communication features
   * - "included" — Communications are present in the export with meaningful
   *   structure
   * - "partial" — Some communication data appears but is incomplete
   * - "excluded" — Product supports communications but they are absent
   * - "unclear" — Cannot determine from available documentation
   */
  patient_communications: "not_applicable" | "included" | "partial" | "excluded" | "unclear";
}

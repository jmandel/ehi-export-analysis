import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";
import type { Vendor } from "./types";
import { gradeColor, gradeBucket } from "./Histogram";
import { Footer } from "./App";

const COVERAGE_LABELS: Record<string, string> = {
  comprehensive: "Comprehensive",
  partial: "Partial coverage",
  minimal_stub_unclear: "Minimal/Stub",
};

const APPROACH_LABELS: Record<string, string> = {
  native: "Native export",
  standards_based: "Standards-based",
  hybrid: "Hybrid",
  unclear: "Unclear approach",
};

const COMMS_LABELS: Record<string, string> = {
  not_applicable: "No messaging features",
  included: "Messaging included",
  partial: "Messaging partial",
  excluded: "Messaging excluded",
  unclear: "Messaging unclear",
};

export function DetailView({
  vendor,
}: {
  vendor: Vendor | null;
}) {
  const [analysisContent, setAnalysisContent] = useState<string>("");

  useEffect(() => {
    if (!vendor) return;
    fetch(`data/analyses/${vendor.slug}.md`)
      .then((r) => (r.ok ? r.text() : "*No analysis available.*"))
      .then(setAnalysisContent);
  }, [vendor?.slug]);

  if (!vendor) {
    return (
      <div className="detail">
        <p>Vendor not found.</p>
      </div>
    );
  }

  const scoreColor = gradeColor(vendor.grade);
  const baseUrl = `${window.location.origin}${window.location.pathname}`;

  return (
    <div className="detail">
      <header className="detail-header">
        <div>
          <h1>
            <span
              className="score-badge large"
              style={{ backgroundColor: scoreColor }}
            >
              {gradeBucket(vendor.grade)}
            </span>
            {vendor.developer} — {vendor.family}
          </h1>
          <p className="detail-product">{vendor.product_name}</p>
          <p className="detail-summary">{vendor.summary}</p>
          <div className="detail-pills">
            {vendor.coverage && (
              <span className={`pill coverage-${vendor.coverage}`}>
                {COVERAGE_LABELS[vendor.coverage] ?? vendor.coverage}
              </span>
            )}
            {vendor.approach && (
              <span className={`pill approach-${vendor.approach}`}>
                {APPROACH_LABELS[vendor.approach] ?? vendor.approach}
              </span>
            )}
            {vendor.patient_communications && (
              <span className={`pill comms-${vendor.patient_communications}`}>
                {COMMS_LABELS[vendor.patient_communications] ?? vendor.patient_communications}
              </span>
            )}
            {vendor.export_formats && vendor.export_formats.length > 0 && (
              <span className="pill format">{vendor.export_formats.join(", ")}</span>
            )}
            {vendor.entity_count != null && (
              <span className="pill stat">{vendor.entity_count} entities</span>
            )}
            {vendor.field_count != null && (
              <span className="pill stat">{vendor.field_count} fields</span>
            )}
            {vendor.has_data_dictionary && (
              <span className="pill stat">Data dictionary</span>
            )}
            {vendor.billing_included === true && (
              <span className="pill stat">Billing included</span>
            )}
            {vendor.billing_included === false && (
              <span className="pill stat warning">No billing</span>
            )}
          </div>
        </div>
      </header>

      <div className="detail-sections">
        <div className="detail-section">
          <h3 className="detail-section-title">Sources</h3>
          <nav className="detail-links">
            {vendor.ehi_documentation_url && (
              <a href={vendor.ehi_documentation_url} target="_blank">
                EHI Export Documentation ↗
              </a>
            )}
            {vendor.chpl_ids.map((id) => (
              <a key={id} href={`https://chpl.healthit.gov/#/listing/${id}`} target="_blank">
                CHPL #{id}
              </a>
            ))}
            {(vendor.download_files.length > 0 || vendor.analysis_files.length > 0) && (
              <a href={`#archive/${vendor.slug}`}>
                File Archive
              </a>
            )}
          </nav>
        </div>

        <div className="detail-section">
          <h3 className="detail-section-title"><span className="ai-tag">AI</span> Reports</h3>
          <nav className="detail-links">
            {vendor.has_research && (
              <a href={`#doc/data/research/${vendor.slug}.md`}>Product Research</a>
            )}
            {vendor.has_report && (
              <a href={`#doc/data/reports/${vendor.slug}.md`}>Download/Retrieval Report</a>
            )}
            {vendor.has_entity_inventory && (
              <a href={`data/analysis-scripts/${vendor.slug}/entity-inventory-full.json`} target="_blank">
                Full Entity Inventory
              </a>
            )}
            {vendor.has_analysis_stats && (
              <a href={`data/analysis-scripts/${vendor.slug}/analysis-stats.json`} target="_blank">
                Analysis Stats
              </a>
            )}
          </nav>
        </div>
      </div>

      <article className="analysis-inline">
        <ReactMarkdown remarkPlugins={[remarkGfm, remarkBreaks]}>
          {analysisContent}
        </ReactMarkdown>
      </article>
    </div>
  );
}

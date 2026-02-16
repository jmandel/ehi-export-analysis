import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";
import type { Vendor } from "./types";
import { toBin, toGrade, BIN_COLORS } from "./Histogram";
import { Footer } from "./App";

const FIDELITY_LABELS: Record<string, string> = {
  native: "Native export",
  summary_with_supplements: "Summary with supplements",
  summary_only: "Summary only",
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
  scoreRange,
}: {
  vendor: Vendor | null;
  scoreRange: [number, number];
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

  const bin = toBin(vendor.holistic_score, scoreRange[0], scoreRange[1]);
  const grade = toGrade(vendor.holistic_score, scoreRange[0], scoreRange[1]);
  const scoreColor = BIN_COLORS[bin];
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
              {grade}
            </span>
            {vendor.developer} — {vendor.family}
          </h1>
          <p className="detail-product">{vendor.product_name}</p>
          <p className="detail-summary">{vendor.summary}</p>
          <div className="detail-pills">
            {vendor.export_fidelity && (
              <span className={`pill fidelity-${vendor.export_fidelity}`}>
                {FIDELITY_LABELS[vendor.export_fidelity] ?? vendor.export_fidelity}
              </span>
            )}
            {vendor.patient_communications && (
              <span className={`pill comms-${vendor.patient_communications}`}>
                {COMMS_LABELS[vendor.patient_communications] ?? vendor.patient_communications}
              </span>
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
              <a href={`data/analysis-scripts/${vendor.slug}/full-entity-inventory.json`} target="_blank">
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

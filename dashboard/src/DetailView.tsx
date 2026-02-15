import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Vendor } from "./types";
import { toBin } from "./Histogram";

const BIN_COLORS = ["", "#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#27ae60"];

export function DetailView({
  vendor,
  scoreRange,
  onBack,
}: {
  vendor: Vendor | null;
  scoreRange: [number, number];
  onBack: () => void;
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
        <button className="back-btn" onClick={onBack}>
          ← Back
        </button>
        <p>Vendor not found.</p>
      </div>
    );
  }

  const bin = toBin(vendor.holistic_score, scoreRange[0], scoreRange[1]);
  const scoreColor = BIN_COLORS[bin];
  const baseUrl = `${window.location.origin}${window.location.pathname}`;

  return (
    <div className="detail">
      <button className="back-btn" onClick={onBack}>
        ← Back to dashboard
      </button>

      <header className="detail-header">
        <span
          className="score-badge large"
          style={{ backgroundColor: scoreColor }}
        >
          {bin}
        </span>
        <div>
          <h1>
            {vendor.developer} — {vendor.family}
          </h1>
          <p className="detail-product">{vendor.product_name}</p>
          <p className="detail-summary">{vendor.summary}</p>
        </div>
      </header>

      <nav className="detail-links">
        {vendor.chpl_ids.map((id) => (
          <a
            key={id}
            href={`https://chpl.healthit.gov/#/listing/${id}`}
            target="_blank"
          >
            🏥 CHPL #{id}
          </a>
        ))}
      </nav>

      <nav className="detail-links ai-links">
        {vendor.has_research && (
          <a
            href={`${baseUrl}md.html?src=data/research/${vendor.slug}.md`}
            target="_blank"
          >
            <span className="ai-tag">AI</span> Product Research
          </a>
        )}
        {vendor.has_report && (
          <a
            href={`${baseUrl}md.html?src=data/reports/${vendor.slug}.md`}
            target="_blank"
          >
            <span className="ai-tag">AI</span> Download/Retrieval Report
          </a>
        )}
      </nav>

      {vendor.download_files.length > 0 && (
        <details className="file-list">
          <summary>
            📁 Downloaded artifacts ({vendor.download_files.length})
          </summary>
          <ul>
            {vendor.download_files.map((f) => (
              <li key={f}>
                <a
                  href={`data/downloads/${vendor.slug}/${f}`}
                  target="_blank"
                >
                  {f}
                </a>
              </li>
            ))}
          </ul>
        </details>
      )}

      {vendor.analysis_files.length > 0 && (
        <details className="file-list">
          <summary>
            🔬 Analysis scripts ({vendor.analysis_files.length})
          </summary>
          <ul>
            {vendor.analysis_files.map((f) => (
              <li key={f}>
                <a
                  href={`data/analysis-scripts/${vendor.slug}/${f}`}
                  target="_blank"
                >
                  {f}
                </a>
              </li>
            ))}
          </ul>
        </details>
      )}

      <article className="analysis-content">
        <h2><span className="ai-tag">AI</span> Export Analysis</h2>
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {analysisContent}
        </ReactMarkdown>
      </article>
    </div>
  );
}

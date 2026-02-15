import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Vendor } from "./types";

export function DetailView({
  vendor,
  onBack,
}: {
  vendor: Vendor | null;
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

  let scoreColor = "#e74c3c";
  if (vendor.holistic_score > 2) scoreColor = "#e67e22";
  if (vendor.holistic_score > 4) scoreColor = "#f1c40f";
  if (vendor.holistic_score > 6) scoreColor = "#2ecc71";
  if (vendor.holistic_score > 8) scoreColor = "#27ae60";

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
          {vendor.holistic_score}
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
        {vendor.has_research && (
          <a
            href={`${baseUrl}md.html?src=data/research/${vendor.slug}.md`}
            target="_blank"
          >
            📋 Product Research
          </a>
        )}
        {vendor.has_report && (
          <a
            href={`${baseUrl}md.html?src=data/reports/${vendor.slug}.md`}
            target="_blank"
          >
            📊 Download/Retrieval Report
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
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {analysisContent}
        </ReactMarkdown>
      </article>
    </div>
  );
}

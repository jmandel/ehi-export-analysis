import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Vendor } from "./types";

type MdView = "analysis" | "research" | "report";

export function DetailView({
  vendor,
  onBack,
}: {
  vendor: Vendor | null;
  onBack: () => void;
}) {
  const [mdContent, setMdContent] = useState<string>("");
  const [activeView, setActiveView] = useState<MdView>("analysis");

  useEffect(() => {
    if (!vendor) return;
    const paths: Record<MdView, string> = {
      analysis: `data/analyses/${vendor.slug}.md`,
      research: `data/research/${vendor.slug}.md`,
      report: `data/reports/${vendor.slug}.md`,
    };
    fetch(paths[activeView])
      .then((r) => (r.ok ? r.text() : "*No content available.*"))
      .then(setMdContent);
  }, [vendor?.slug, activeView]);

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
      </nav>

      <nav className="view-tabs">
        <button
          className={activeView === "analysis" ? "active" : ""}
          onClick={() => setActiveView("analysis")}
        >
          📝 Analysis
        </button>
        {vendor.has_research && (
          <button
            className={activeView === "research" ? "active" : ""}
            onClick={() => setActiveView("research")}
          >
            📋 Product Research
          </button>
        )}
        {vendor.has_report && (
          <button
            className={activeView === "report" ? "active" : ""}
            onClick={() => setActiveView("report")}
          >
            📊 Download/Retrieval Report
          </button>
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
          {mdContent}
        </ReactMarkdown>
      </article>
    </div>
  );
}

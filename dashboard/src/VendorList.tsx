import type { Vendor } from "./types";

function scoreBadge(score: number) {
  let color = "#e74c3c";
  if (score > 2) color = "#e67e22";
  if (score > 4) color = "#f1c40f";
  if (score > 6) color = "#2ecc71";
  if (score > 8) color = "#27ae60";
  return (
    <span className="score-badge" style={{ backgroundColor: color }}>
      {score}
    </span>
  );
}

export function VendorList({
  vendors,
  selectedScore,
  onClearFilter,
}: {
  vendors: Vendor[];
  selectedScore: number | null;
  onClearFilter: () => void;
}) {
  const sorted = [...vendors].sort((a, b) => a.holistic_score - b.holistic_score);

  return (
    <section className="vendor-list">
      <div className="list-header">
        <h2>
          {selectedScore !== null ? (
            <>
              Score {selectedScore} ({vendors.length}){" "}
              <button className="clear-btn" onClick={onClearFilter}>
                Show all
              </button>
            </>
          ) : (
            `All vendors (${vendors.length})`
          )}
        </h2>
      </div>
      <div className="vendors">
        {sorted.map((v) => (
          <a
            key={v.slug}
            className="vendor-card"
            href={`${window.location.origin}${window.location.pathname}#${v.slug}`}
            target="_blank"
            rel="noopener"
          >
            {scoreBadge(v.holistic_score)}
            <div className="vendor-info">
              <div className="vendor-name">
                {v.developer} — {v.family}
              </div>
              <div className="vendor-product">{v.product_name}</div>
              <div className="vendor-summary">{v.summary}</div>
            </div>
          </a>
        ))}
      </div>
    </section>
  );
}

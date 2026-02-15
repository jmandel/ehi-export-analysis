import type { Vendor } from "./types";
import { toBin } from "./Histogram";

const BIN_COLORS = ["", "#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#27ae60"];

function scoreBadge(bin: number) {
  return (
    <span className="score-badge" style={{ backgroundColor: BIN_COLORS[bin] }}>
      {bin}
    </span>
  );
}

export function VendorList({
  vendors,
  selectedScore,
  scoreRange,
  onClearFilter,
}: {
  vendors: Vendor[];
  selectedScore: number | null;
  scoreRange: [number, number];
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
            {scoreBadge(toBin(v.holistic_score, scoreRange[0], scoreRange[1]))}
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

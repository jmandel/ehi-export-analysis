import type { Vendor } from "./types";
import { toBin, toGrade, BIN_COLORS, BIN_GRADES } from "./Histogram";

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

function fidelityPill(value: string) {
  if (!value) return null;
  return <span className={`pill fidelity-${value}`}>{FIDELITY_LABELS[value] ?? value}</span>;
}

function commsPill(value: string) {
  if (!value) return null;
  return <span className={`pill comms-${value}`}>{COMMS_LABELS[value] ?? value}</span>;
}

function scoreBadge(bin: number, grade: string) {
  return (
    <span className="score-badge" style={{ backgroundColor: BIN_COLORS[bin] }}>
      {grade}
    </span>
  );
}

export function VendorList({
  vendors,
  scoreRange,
  hasFilters,
  onClearFilters,
}: {
  vendors: Vendor[];
  scoreRange: [number, number];
  hasFilters: boolean;
  onClearFilters: () => void;
}) {
  const sorted = [...vendors].sort((a, b) => b.holistic_score - a.holistic_score);

  return (
    <section className="vendor-list">
      <div className="list-header">
        <h2>
          {hasFilters ? (
            <>
              Filtered ({vendors.length}){" "}
              <button className="clear-btn" onClick={onClearFilters}>
                Clear filters
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
            href={`#vendor/${v.slug}`}
          >
            {scoreBadge(toBin(v.holistic_score, scoreRange[0], scoreRange[1]), toGrade(v.holistic_score, scoreRange[0], scoreRange[1]))}
            <div className="vendor-info">
              <div className="vendor-name">
                {v.developer} — {v.family}
              </div>
              <div className="vendor-product">{v.product_name}</div>
              <div className="vendor-summary">
                {v.summary}
                <span className="vendor-pills">
                  {fidelityPill(v.export_fidelity)}
                  {commsPill(v.patient_communications)}
                </span>
              </div>
            </div>
          </a>
        ))}
      </div>
    </section>
  );
}

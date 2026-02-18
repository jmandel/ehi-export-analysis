import type { Vendor } from "./types";
import { gradeBucket, gradeColor } from "./Histogram";

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

function coveragePill(value: string) {
  if (!value) return null;
  return <span className={`pill coverage-${value}`}>{COVERAGE_LABELS[value] ?? value}</span>;
}

function approachPill(value: string) {
  if (!value) return null;
  return <span className={`pill approach-${value}`}>{APPROACH_LABELS[value] ?? value}</span>;
}

function commsPill(value: string) {
  if (!value) return null;
  return <span className={`pill comms-${value}`}>{COMMS_LABELS[value] ?? value}</span>;
}

// Grade sort order: A, B, C, D, F
const GRADE_ORDER = ["A", "B", "C", "D", "F"];
function gradeRank(grade: string): number {
  const idx = GRADE_ORDER.indexOf(grade);
  return idx >= 0 ? idx : GRADE_ORDER.length;
}

function scoreBadge(grade: string) {
  return (
    <span className="score-badge" style={{ backgroundColor: gradeColor(grade) }}>
      {gradeBucket(grade)}
    </span>
  );
}

export function VendorList({
  vendors,
  hasFilters,
  onClearFilters,
}: {
  vendors: Vendor[];
  hasFilters: boolean;
  onClearFilters: () => void;
}) {
  const sorted = [...vendors].sort((a, b) => {
    const g = gradeRank(a.grade) - gradeRank(b.grade);
    if (g !== 0) return g;
    return a.developer.localeCompare(b.developer);
  });

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
            {scoreBadge(v.grade)}
            <div className="vendor-info">
              <div className="vendor-name">
                {v.developer} — {v.family}
              </div>
              <div className="vendor-product">{v.product_name}</div>
              <div className="vendor-summary">
                {v.summary}
                <span className="vendor-pills">
                  {coveragePill(v.coverage)}
                  {approachPill(v.approach)}
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

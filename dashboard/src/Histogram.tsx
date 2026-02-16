import type { Vendor } from "./types";

// Letter grades bucketed to A/B/C/D/F for histogram (strip +/-)
const GRADE_BUCKETS = ["F", "D", "C", "B", "A"] as const;
const GRADE_COLORS: Record<string, string> = {
  A: "#27ae60",
  B: "#2ecc71",
  C: "#f1c40f",
  D: "#e67e22",
  F: "#e74c3c",
};

function gradeBucket(grade: string): string {
  if (!grade) return "F";
  return grade.charAt(0); // "A-" → "A", "B+" → "B", etc.
}

function gradeColor(grade: string): string {
  return GRADE_COLORS[gradeBucket(grade)] ?? GRADE_COLORS.F;
}

const COVERAGE_OPTIONS: [string, string][] = [
  ["comprehensive", "Comprehensive"],
  ["partial", "Partial"],
  ["minimal_stub_unclear", "Minimal/Stub"],
];

const APPROACH_OPTIONS: [string, string][] = [
  ["native", "Native"],
  ["standards_based", "Standards-based"],
  ["hybrid", "Hybrid"],
  ["unclear", "Unclear"],
];

const COMMS_OPTIONS: [string, string][] = [
  ["included", "Included"],
  ["partial", "Partial"],
  ["excluded", "Excluded"],
  ["not_applicable", "N/A"],
  ["unclear", "Unclear"],
];

export function FacetSidebar({
  vendors,
  gradeFilter,
  coverageFilter,
  approachFilter,
  commsFilter,
  onToggleGrade,
  onToggleCoverage,
  onToggleApproach,
  onToggleComms,
  onClearGrade,
  onClearCoverage,
  onClearApproach,
  onClearComms,
  onClearAll,
}: {
  vendors: Vendor[];
  gradeFilter: Set<string>;
  coverageFilter: Set<string>;
  approachFilter: Set<string>;
  commsFilter: Set<string>;
  onToggleGrade: (g: string) => void;
  onToggleCoverage: (c: string) => void;
  onToggleApproach: (a: string) => void;
  onToggleComms: (c: string) => void;
  onClearGrade: () => void;
  onClearCoverage: () => void;
  onClearApproach: () => void;
  onClearComms: () => void;
  onClearAll: () => void;
}) {
  const anyFilter = gradeFilter.size > 0 || coverageFilter.size > 0 || approachFilter.size > 0 || commsFilter.size > 0;

  // Cross-filtered counts
  const gradeCounts: Record<string, number> = {};
  const coverageCounts: Record<string, number> = {};
  const approachCounts: Record<string, number> = {};
  const commsCounts: Record<string, number> = {};

  for (const v of vendors) {
    const bucket = gradeBucket(v.grade);
    const cov = v.coverage || "";
    const app = v.approach || "";
    const com = v.patient_communications || "";
    const matchGrade = gradeFilter.size === 0 || gradeFilter.has(bucket);
    const matchCov = coverageFilter.size === 0 || coverageFilter.has(cov);
    const matchApp = approachFilter.size === 0 || approachFilter.has(app);
    const matchCom = commsFilter.size === 0 || commsFilter.has(com);

    if (matchCov && matchApp && matchCom) gradeCounts[bucket] = (gradeCounts[bucket] || 0) + 1;
    if (matchGrade && matchApp && matchCom) coverageCounts[cov] = (coverageCounts[cov] || 0) + 1;
    if (matchGrade && matchCov && matchCom) approachCounts[app] = (approachCounts[app] || 0) + 1;
    if (matchGrade && matchCov && matchApp) commsCounts[com] = (commsCounts[com] || 0) + 1;
  }

  const maxGrade = Math.max(...Object.values(gradeCounts), 1);
  const maxCoverage = Math.max(...Object.values(coverageCounts), 1);
  const maxApproach = Math.max(...Object.values(approachCounts), 1);
  const maxComms = Math.max(...Object.values(commsCounts), 1);

  return (
    <aside className="facet-sidebar">
      <button className="facet-clear-all" onClick={onClearAll} disabled={!anyFilter}>Clear filters</button>
      <div className="facet-group">
        <h3 onClick={gradeFilter.size > 0 ? onClearGrade : undefined} className={gradeFilter.size > 0 ? "clearable" : ""}>Grade <span className="facet-clear" style={{ visibility: gradeFilter.size > 0 ? "visible" : "hidden" }}>&times;</span></h3>
        {[...GRADE_BUCKETS].reverse().map((bucket) => {
          const count = gradeCounts[bucket] || 0;
          const pct = `${(count / maxGrade) * 100}%`;
          const active = gradeFilter.has(bucket);
          return (
            <div
              key={bucket}
              className={`facet-option ${active ? "active" : ""}`}
              onClick={() => onToggleGrade(bucket)}
              style={{
                backgroundImage: `linear-gradient(to right, ${GRADE_COLORS[bucket]}, ${GRADE_COLORS[bucket]})`,
                backgroundSize: `${pct} 100%`,
              }}
            >
              <span className="grade-letter">{bucket}</span>
              <span className="facet-label" />
              <span className="facet-count">{count}</span>
            </div>
          );
        })}
      </div>

      <div className="facet-group">
        <h3 onClick={coverageFilter.size > 0 ? onClearCoverage : undefined} className={coverageFilter.size > 0 ? "clearable" : ""}>Coverage <span className="facet-clear" style={{ visibility: coverageFilter.size > 0 ? "visible" : "hidden" }}>&times;</span></h3>
        {COVERAGE_OPTIONS.map(([val, label]) => {
          const count = coverageCounts[val] || 0;
          const active = coverageFilter.has(val);
          const pct = `${(count / maxCoverage) * 100}%`;
          return (
            <div key={val} className={`facet-option ${active ? "active" : ""}`} onClick={() => onToggleCoverage(val)} style={{ backgroundSize: `${pct} 100%` }}>
              <span className="facet-label">{label}</span>
              <span className="facet-count">{count}</span>
            </div>
          );
        })}
      </div>

      <div className="facet-group">
        <h3 onClick={approachFilter.size > 0 ? onClearApproach : undefined} className={approachFilter.size > 0 ? "clearable" : ""}>Approach <span className="facet-clear" style={{ visibility: approachFilter.size > 0 ? "visible" : "hidden" }}>&times;</span></h3>
        {APPROACH_OPTIONS.map(([val, label]) => {
          const count = approachCounts[val] || 0;
          const active = approachFilter.has(val);
          const pct = `${(count / maxApproach) * 100}%`;
          return (
            <div key={val} className={`facet-option ${active ? "active" : ""}`} onClick={() => onToggleApproach(val)} style={{ backgroundSize: `${pct} 100%` }}>
              <span className="facet-label">{label}</span>
              <span className="facet-count">{count}</span>
            </div>
          );
        })}
      </div>

      <div className="facet-group">
        <h3 onClick={commsFilter.size > 0 ? onClearComms : undefined} className={commsFilter.size > 0 ? "clearable" : ""}>Patient messaging <span className="facet-clear" style={{ visibility: commsFilter.size > 0 ? "visible" : "hidden" }}>&times;</span></h3>
        {COMMS_OPTIONS.map(([val, label]) => {
          const count = commsCounts[val] || 0;
          const active = commsFilter.has(val);
          const pct = `${(count / maxComms) * 100}%`;
          return (
            <div key={val} className={`facet-option ${active ? "active" : ""}`} onClick={() => onToggleComms(val)} style={{ backgroundSize: `${pct} 100%` }}>
              <span className="facet-label">{label}</span>
              <span className="facet-count">{count}</span>
            </div>
          );
        })}
      </div>
    </aside>
  );
}

export { gradeBucket, gradeColor, GRADE_BUCKETS, GRADE_COLORS };

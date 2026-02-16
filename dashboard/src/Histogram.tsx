import type { Vendor } from "./types";

const NUM_BINS = 5;
const BIN_GRADES = ["", "F", "D", "C", "B", "A"];
const BIN_COLORS = ["", "#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#27ae60"];

function toBin(score: number, min: number, max: number): number {
  if (max === min) return 1;
  const normalized = (score - min) / (max - min);
  return Math.min(NUM_BINS, Math.max(1, Math.ceil(normalized * NUM_BINS)));
}

function toGrade(score: number, min: number, max: number): string {
  return BIN_GRADES[toBin(score, min, max)];
}

const FIDELITY_OPTIONS: [string, string][] = [
  ["", "All"],
  ["native", "Native"],
  ["summary_with_supplements", "Summary +"],
  ["summary_only", "Summary only"],
];

const COMMS_OPTIONS: [string, string][] = [
  ["", "All"],
  ["included", "Included"],
  ["partial", "Partial"],
  ["excluded", "Excluded"],
  ["not_applicable", "N/A"],
  ["unclear", "Unclear"],
];

export function FacetSidebar({
  vendors,
  scoreRange,
  gradeFilter,
  fidelityFilter,
  commsFilter,
  onToggleGrade,
  onToggleFidelity,
  onToggleComms,
  onClearGrade,
  onClearFidelity,
  onClearComms,
  onClearAll,
}: {
  vendors: Vendor[];
  scoreRange: [number, number];
  gradeFilter: Set<number>;
  fidelityFilter: Set<string>;
  commsFilter: Set<string>;
  onToggleGrade: (g: number) => void;
  onToggleFidelity: (f: string) => void;
  onToggleComms: (c: string) => void;
  onClearGrade: () => void;
  onClearFidelity: () => void;
  onClearComms: () => void;
  onClearAll: () => void;
}) {
  const anyFilter = gradeFilter.size > 0 || fidelityFilter.size > 0 || commsFilter.size > 0;
  const [min, max] = scoreRange;

  // Cross-filtered counts: each facet counts vendors matching the OTHER filters
  // so you can see how many results each option would contribute
  const gradeCountsArr = new Array(NUM_BINS + 1).fill(0);
  const fidelityCounts: Record<string, number> = {};
  const commsCounts: Record<string, number> = {};

  for (const v of vendors) {
    const bin = toBin(v.holistic_score, min, max);
    const fid = v.export_fidelity || "";
    const com = v.patient_communications || "";
    const matchGrade = gradeFilter.size === 0 || gradeFilter.has(bin);
    const matchFid = fidelityFilter.size === 0 || fidelityFilter.has(fid);
    const matchCom = commsFilter.size === 0 || commsFilter.has(com);

    // Grade counts: apply fidelity + comms filters only
    if (matchFid && matchCom) gradeCountsArr[bin]++;
    // Fidelity counts: apply grade + comms filters only
    if (matchGrade && matchCom) fidelityCounts[fid] = (fidelityCounts[fid] || 0) + 1;
    // Comms counts: apply grade + fidelity filters only
    if (matchGrade && matchFid) commsCounts[com] = (commsCounts[com] || 0) + 1;
  }

  const maxGrade = Math.max(...gradeCountsArr, 1);
  const maxFidelity = Math.max(...Object.values(fidelityCounts), 1);
  const maxComms = Math.max(...Object.values(commsCounts), 1);

  return (
    <aside className="facet-sidebar">
      <button className="facet-clear-all" onClick={onClearAll} disabled={!anyFilter}>Clear filters</button>
      <div className="facet-group">
        <h3 onClick={gradeFilter.size > 0 ? onClearGrade : undefined} className={gradeFilter.size > 0 ? "clearable" : ""}>Grade <span className="facet-clear" style={{ visibility: gradeFilter.size > 0 ? "visible" : "hidden" }}>&times;</span></h3>
        {Array.from({ length: NUM_BINS }, (_, i) => NUM_BINS - i).map((bin) => {
          const count = gradeCountsArr[bin];
          const pct = `${(count / maxGrade) * 100}%`;
          const active = gradeFilter.has(bin);
          return (
            <div
              key={bin}
              className={`facet-option ${active ? "active" : ""}`}
              onClick={() => onToggleGrade(bin)}
              style={{
                backgroundImage: `linear-gradient(to right, ${BIN_COLORS[bin]}, ${BIN_COLORS[bin]})`,
                backgroundSize: `${pct} 100%`,
              }}
            >
              <span className="grade-letter">{BIN_GRADES[bin]}</span>
              <span className="facet-label" />
              <span className="facet-count">{count}</span>
            </div>
          );
        })}
      </div>

      <div className="facet-group">
        <h3 onClick={fidelityFilter.size > 0 ? onClearFidelity : undefined} className={fidelityFilter.size > 0 ? "clearable" : ""}>Export fidelity <span className="facet-clear" style={{ visibility: fidelityFilter.size > 0 ? "visible" : "hidden" }}>&times;</span></h3>
        {FIDELITY_OPTIONS.slice(1).map(([val, label]) => {
          const count = fidelityCounts[val] || 0;
          const active = fidelityFilter.has(val);
          const pct = `${(count / maxFidelity) * 100}%`;
          return (
            <div key={val} className={`facet-option ${active ? "active" : ""}`} onClick={() => onToggleFidelity(val)} style={{ backgroundSize: `${pct} 100%` }}>
              <span className="facet-label">{label}</span>
              <span className="facet-count">{count}</span>
            </div>
          );
        })}
      </div>

      <div className="facet-group">
        <h3 onClick={commsFilter.size > 0 ? onClearComms : undefined} className={commsFilter.size > 0 ? "clearable" : ""}>Patient messaging <span className="facet-clear" style={{ visibility: commsFilter.size > 0 ? "visible" : "hidden" }}>&times;</span></h3>
        {COMMS_OPTIONS.slice(1).map(([val, label]) => {
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

export { toBin, toGrade, BIN_GRADES, BIN_COLORS };

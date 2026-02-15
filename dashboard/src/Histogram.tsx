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

export function Histogram({
  vendors,
  selectedScore,
  onSelect,
}: {
  vendors: Vendor[];
  selectedScore: number | null;
  onSelect: (score: number) => void;
}) {
  const scores = vendors.map((v) => v.holistic_score);
  const min = Math.min(...scores, 0);
  const max = Math.max(...scores, 1);

  const buckets = new Array(NUM_BINS + 1).fill(0);
  for (const v of vendors) buckets[toBin(v.holistic_score, min, max)]++;
  const maxCount = Math.max(...buckets, 1);

  const sorted = [...scores].sort((a, b) => a - b);
  const medianScore =
    sorted.length > 0
      ? sorted.length % 2 === 0
        ? (sorted[sorted.length / 2 - 1] + sorted[sorted.length / 2]) / 2
        : sorted[Math.floor(sorted.length / 2)]
      : 0;
  const medianGrade = BIN_GRADES[toBin(medianScore, min, max)];

  return (
    <section className="histogram">
      <div className="stats">
        <span>{vendors.length} vendors</span>
        <span>median {medianGrade}</span>
      </div>
      <div className="bars">
        {Array.from({ length: NUM_BINS }, (_, i) => NUM_BINS - i).map((bin) => (
          <div
            key={bin}
            className={`bar-col ${selectedScore === bin ? "selected" : ""}`}
            onClick={() => onSelect(bin)}
          >
            <span className="bar-count">{buckets[bin] || ""}</span>
            <div
              className="bar"
              style={{
                height: `${(buckets[bin] / maxCount) * 200}px`,
                backgroundColor: BIN_COLORS[bin],
                opacity: selectedScore !== null && selectedScore !== bin ? 0.3 : 1,
              }}
            />
            <span className="bar-label">{BIN_GRADES[bin]}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

export { toBin, toGrade, BIN_GRADES, BIN_COLORS };

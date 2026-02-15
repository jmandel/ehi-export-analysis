import type { Vendor } from "./types";

const NUM_BINS = 5;

function toBin(score: number, min: number, max: number): number {
  if (max === min) return 1;
  const normalized = (score - min) / (max - min);
  return Math.min(NUM_BINS, Math.max(1, Math.ceil(normalized * NUM_BINS)));
}

const BIN_COLORS = ["", "#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#27ae60"];

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

  const mean =
    vendors.length > 0
      ? vendors.reduce((s, v) => s + v.holistic_score, 0) / vendors.length
      : 0;
  const sorted = [...scores].sort((a, b) => a - b);
  const median =
    sorted.length > 0
      ? sorted.length % 2 === 0
        ? (sorted[sorted.length / 2 - 1] + sorted[sorted.length / 2]) / 2
        : sorted[Math.floor(sorted.length / 2)]
      : 0;

  // Bin edge labels
  const binLabel = (bin: number) => `${bin}`;

  return (
    <section className="histogram">
      <div className="stats">
        <span>{vendors.length} vendors</span>
        <span>mean {mean.toFixed(1)}</span>
        <span>median {median.toFixed(1)}</span>
      </div>
      <div className="bars">
        {Array.from({ length: NUM_BINS }, (_, i) => i + 1).map((bin) => (
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
            <span className="bar-label">{binLabel(bin)}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

export { toBin };

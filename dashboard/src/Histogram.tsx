import type { Vendor } from "./types";

function scoreColor(score: number): string {
  if (score <= 2) return "#e74c3c";
  if (score <= 4) return "#e67e22";
  if (score <= 6) return "#f1c40f";
  if (score <= 8) return "#2ecc71";
  return "#27ae60";
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
  // Bucket by integer score
  const buckets = new Array(11).fill(0);
  for (const v of vendors) {
    const b = Math.min(10, Math.max(0, Math.floor(v.holistic_score)));
    buckets[b]++;
  }
  const maxCount = Math.max(...buckets, 1);

  const mean =
    vendors.length > 0
      ? vendors.reduce((s, v) => s + v.holistic_score, 0) / vendors.length
      : 0;
  const sorted = [...vendors].sort((a, b) => a.holistic_score - b.holistic_score);
  const median =
    sorted.length > 0
      ? sorted.length % 2 === 0
        ? (sorted[sorted.length / 2 - 1].holistic_score +
            sorted[sorted.length / 2].holistic_score) /
          2
        : sorted[Math.floor(sorted.length / 2)].holistic_score
      : 0;

  return (
    <section className="histogram">
      <div className="stats">
        <span>{vendors.length} vendors</span>
        <span>mean {mean.toFixed(1)}</span>
        <span>median {median.toFixed(1)}</span>
      </div>
      <div className="bars">
        {buckets.map((count, score) => (
          <div
            key={score}
            className={`bar-col ${selectedScore === score ? "selected" : ""}`}
            onClick={() => onSelect(score)}
          >
            <span className="bar-count">{count || ""}</span>
            <div
              className="bar"
              style={{
                height: `${(count / maxCount) * 200}px`,
                backgroundColor: scoreColor(score),
                opacity: selectedScore !== null && selectedScore !== score ? 0.3 : 1,
              }}
            />
            <span className="bar-label">{score}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

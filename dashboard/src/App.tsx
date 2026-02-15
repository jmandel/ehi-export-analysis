import { useState, useEffect } from "react";
import type { Vendor } from "./types";
import { Histogram } from "./Histogram";
import { VendorList } from "./VendorList";
import { DetailView } from "./DetailView";

export function App() {
  const [vendors, setVendors] = useState<Vendor[]>([]);
  const [selectedScore, setSelectedScore] = useState<number | null>(null);
  const [detailSlug, setDetailSlug] = useState<string | null>(null);

  useEffect(() => {
    fetch("data/vendors.json")
      .then((r) => r.json())
      .then(setVendors);
  }, []);

  // Check URL hash for detail view
  useEffect(() => {
    const onHash = () => {
      const hash = window.location.hash.slice(1);
      setDetailSlug(hash || null);
    };
    onHash();
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);

  if (detailSlug) {
    const vendor = vendors.find((v) => v.slug === detailSlug);
    return (
      <DetailView
        vendor={vendor ?? null}
        onBack={() => {
          window.location.hash = "";
        }}
      />
    );
  }

  const filtered =
    selectedScore !== null
      ? vendors.filter((v) => Math.floor(v.holistic_score) === selectedScore)
      : vendors;

  return (
    <div className="app">
      <header>
        <h1>EHI Export Quality Dashboard</h1>
        <p className="subtitle">
          §170.315(b)(10) compliance analysis across {vendors.length} certified
          EHR products
        </p>
      </header>
      <Histogram
        vendors={vendors}
        selectedScore={selectedScore}
        onSelect={(s) => setSelectedScore(s === selectedScore ? null : s)}
      />
      <VendorList
        vendors={filtered}
        selectedScore={selectedScore}
        onClearFilter={() => setSelectedScore(null)}
      />
    </div>
  );
}

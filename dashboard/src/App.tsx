import { useState, useEffect } from "react";
import type { Vendor } from "./types";
import { FacetSidebar, toBin } from "./Histogram";
import { VendorList } from "./VendorList";
import { DetailView } from "./DetailView";
import { MdViewer } from "./MdViewer";
import { FileViewer } from "./FileViewer";
import { Shell } from "./Shell";

type Route =
  | { page: "dashboard" }
  | { page: "vendor"; slug: string }
  | { page: "about" }
  | { page: "doc"; src: string }
  | { page: "files"; folder: string }
  | { page: "archive"; slug: string };

function parseHash(hash: string): Route {
  const h = hash.replace(/^#\/?/, "");
  if (!h) return { page: "dashboard" };
  if (h === "about") return { page: "about" };
  if (h.startsWith("vendor/")) return { page: "vendor", slug: h.slice(7) };
  if (h.startsWith("doc/")) return { page: "doc", src: h.slice(4) };
  if (h.startsWith("files/")) return { page: "files", folder: h.slice(6) };
  if (h.startsWith("archive/")) return { page: "archive", slug: h.slice(8) };
  // Legacy: bare slug (no prefix) → vendor detail
  if (h.includes("--")) return { page: "vendor", slug: h };
  return { page: "dashboard" };
}

function toggle<T>(set: Set<T>, val: T): Set<T> {
  const next = new Set(set);
  if (next.has(val)) next.delete(val); else next.add(val);
  return next;
}

export function App() {
  const [vendors, setVendors] = useState<Vendor[]>([]);
  const [gradeFilter, setGradeFilter] = useState<Set<number>>(new Set());
  const [route, setRoute] = useState<Route>(() => parseHash(window.location.hash));
  const [fidelityFilter, setFidelityFilter] = useState<Set<string>>(new Set());
  const [commsFilter, setCommsFilter] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetch("data/vendors.json")
      .then((r) => r.json())
      .then(setVendors);
  }, []);

  useEffect(() => {
    const onHash = () => setRoute(parseHash(window.location.hash));
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);

  const scores = vendors.map((v) => v.holistic_score);
  const min = Math.min(...scores, 0);
  const max = Math.max(...scores, 1);

  if (route.page === "about") {
    return <Shell><MdViewer src="about.md" /></Shell>;
  }

  if (route.page === "doc") {
    return <Shell><MdViewer src={route.src} /></Shell>;
  }

  if (route.page === "files") {
    return <Shell><FileViewer folder={route.folder} /></Shell>;
  }

  if (route.page === "archive") {
    return <Shell><FileViewer slug={route.slug} /></Shell>;
  }

  if (route.page === "vendor") {
    const vendor = vendors.find((v) => v.slug === route.slug);
    return (
      <Shell>
        <DetailView
          vendor={vendor ?? null}
          scoreRange={[min, max]}
        />
      </Shell>
    );
  }

  const displayed = vendors
    .filter((v) => gradeFilter.size === 0 || gradeFilter.has(toBin(v.holistic_score, min, max)))
    .filter((v) => fidelityFilter.size === 0 || fidelityFilter.has(v.export_fidelity || ""))
    .filter((v) => commsFilter.size === 0 || commsFilter.has(v.patient_communications || ""));

  return (
    <Shell>
      <div className="dashboard-page">
        <div className="main-layout">
          <FacetSidebar
            vendors={vendors}
            scoreRange={[min, max]}
            gradeFilter={gradeFilter}
            fidelityFilter={fidelityFilter}
            commsFilter={commsFilter}
            onToggleGrade={(g) => setGradeFilter(toggle(gradeFilter, g))}
            onToggleFidelity={(f) => setFidelityFilter(toggle(fidelityFilter, f))}
            onToggleComms={(c) => setCommsFilter(toggle(commsFilter, c))}
            onClearGrade={() => setGradeFilter(new Set())}
            onClearFidelity={() => setFidelityFilter(new Set())}
            onClearComms={() => setCommsFilter(new Set())}
            onClearAll={() => { setGradeFilter(new Set()); setFidelityFilter(new Set()); setCommsFilter(new Set()); }}
          />
          <div className="main-content">
            <VendorList
              vendors={displayed}
              scoreRange={[min, max]}
              hasFilters={gradeFilter.size > 0 || fidelityFilter.size > 0 || commsFilter.size > 0}
              onClearFilters={() => { setGradeFilter(new Set()); setFidelityFilter(new Set()); setCommsFilter(new Set()); }}
            />
          </div>
        </div>
      </div>
    </Shell>
  );
}

import { useState, useEffect } from "react";

interface DirEntry { name: string; type: "file" | "dir"; children?: DirEntry[]; }
interface FileIndex {
  [slug: string]: {
    downloads: DirEntry[];
    analysis: DirEntry[];
  };
}

function isViewable(f: string) {
  return /\.(md|txt|csv|tsv|xml|py|ts|js|sh|sql)$/i.test(f);
}

function EntryList({ entries, basePath }: { entries: DirEntry[]; basePath: string }) {
  return (
    <ul className="file-viewer-list">
      {entries.map((e) =>
        e.type === "dir" ? (
          <li key={e.name} className="file-viewer-dir-item">
            <div className="file-viewer-dir">📁 {e.name}/</div>
            {e.children && e.children.length > 0 && (
              <EntryList entries={e.children} basePath={`${basePath}/${e.name}`} />
            )}
          </li>
        ) : (
          <li key={e.name}>
            {isViewable(e.name) ? (
              <a href={`#doc/${basePath}/${e.name}`}>{e.name}</a>
            ) : (
              <a href={`${basePath}/${e.name}`} target="_blank" rel="noopener">{e.name}</a>
            )}
            <span className="file-type">{e.name.split(".").pop()?.toUpperCase()}</span>
          </li>
        )
      )}
    </ul>
  );
}

/** Check if a DirEntry[] contains a top-level "enrichment" directory */
function extractEnrichment(entries: DirEntry[]): { enrichment: DirEntry[] | null; rest: DirEntry[] } {
  const enrichDir = entries.find((e) => e.type === "dir" && e.name === "enrichment");
  if (!enrichDir || !enrichDir.children?.length) return { enrichment: null, rest: entries };
  return {
    enrichment: enrichDir.children,
    rest: entries.filter((e) => e !== enrichDir),
  };
}

function ArchiveSection({ icon, label, entries, basePath }: {
  icon: string; label: string; entries: DirEntry[]; basePath: string;
}) {
  const [open, setOpen] = useState(true);
  return (
    <div className="archive-section">
      <div className="archive-section-header" onClick={() => setOpen(!open)}>
        <span className="archive-toggle">{open ? "▾" : "▸"}</span>
        <span className="archive-icon">{icon}</span>
        <span className="archive-section-label">{label}</span>
        <span className="archive-section-count">{entries.length}</span>
      </div>
      {open && <EntryList entries={entries} basePath={basePath} />}
    </div>
  );
}

function ArchiveView({ slug, data }: { slug: string; data: FileIndex }) {
  const entry = data[slug];
  if (!entry) return <p>No files found for this vendor.</p>;

  const { enrichment, rest: downloads } = extractEnrichment(entry.downloads);
  const analysisScripts = entry.analysis.filter(
    (e) => e.type === "dir" || /\.(py|ts|js|sh|sql|md)$/i.test(e.name),
  );
  const analysisResults = entry.analysis.filter(
    (e) => e.type === "file" && /\.(json|csv|tsv|txt)$/i.test(e.name),
  );
  const hasDownloads = downloads.length > 0;

  return (
    <div className="archive-paper">
      <h2>File Archive</h2>
      <p className="archive-slug">{slug}</p>
      {hasDownloads && (
        <ArchiveSection
          icon="📥"
          label="Downloaded Artifacts"
          entries={downloads}
          basePath={`data/downloads/${slug}`}
        />
      )}
      {enrichment && (
        <ArchiveSection
          icon="🔬"
          label="Enrichments"
          entries={enrichment}
          basePath={`data/downloads/${slug}/enrichment`}
        />
      )}
      {analysisResults.length > 0 && (
        <ArchiveSection
          icon="📊"
          label="Analysis Results"
          entries={analysisResults}
          basePath={`data/analysis-scripts/${slug}`}
        />
      )}
      {analysisScripts.length > 0 && (
        <ArchiveSection
          icon="🔧"
          label="Analysis Scripts"
          entries={analysisScripts}
          basePath={`data/analysis-scripts/${slug}`}
        />
      )}
    </div>
  );
}

export function FileViewer({ folder, slug }: { folder?: string; slug?: string }) {
  const [data, setData] = useState<FileIndex | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("data/file-index.json")
      .then((r) => r.json())
      .then((d: FileIndex) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ maxWidth: 800, margin: "0 auto" }}><p>Loading…</p></div>;
  if (!data) return <div style={{ maxWidth: 800, margin: "0 auto" }}><p>Failed to load file index.</p></div>;

  // Archive mode: virtual filesystem with all sections
  if (slug) {
    return (
      <div style={{ maxWidth: 800, margin: "0 auto" }}>
        <nav style={{ marginBottom: "0.5rem" }}>
          <a href={`#vendor/${slug}`} style={{ color: "#0066cc", fontSize: "0.9rem", textDecoration: "none" }}>
            ← Back to vendor
          </a>
        </nav>
        <ArchiveView slug={slug} data={data} />
      </div>
    );
  }

  // Legacy folder mode
  if (folder) {
    const parts = folder.split("/");
    const typeIdx = parts.indexOf("downloads") !== -1 ? parts.indexOf("downloads") : parts.indexOf("analysis-scripts");
    const folderSlug = parts[typeIdx + 1] || "";
    const type = parts[typeIdx] || "downloads";
    const label = type === "downloads" ? "Downloaded artifacts" : "Analysis scripts";
    const entry = data[folderSlug];
    const entries = entry ? (type === "downloads" ? entry.downloads : entry.analysis) : [];

    return (
      <div style={{ maxWidth: 800, margin: "0 auto" }}>
        <nav style={{ marginBottom: "1rem" }}>
          <a href={`#vendor/${folderSlug}`} style={{ color: "#0066cc", fontSize: "0.9rem", textDecoration: "none" }}>
            ← Back to {folderSlug}
          </a>
        </nav>
        <h2>{label}</h2>
        <p style={{ color: "#666", fontSize: "0.85rem", marginBottom: "1rem" }}>{folderSlug}</p>
        {entries.length === 0 ? <p>No files found.</p> : (
          <EntryList entries={entries} basePath={`data/${type}/${folderSlug}`} />
        )}
      </div>
    );
  }

  return <p>No file view specified.</p>;
}

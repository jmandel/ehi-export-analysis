import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export function MdViewer() {
  const [content, setContent] = useState<string>("Loading…");
  const src = new URLSearchParams(window.location.search).get("src");

  useEffect(() => {
    if (!src) {
      setContent("*No document specified.*");
      return;
    }
    fetch(src)
      .then((r) => (r.ok ? r.text() : "*Document not found.*"))
      .then((text) => {
        setContent(text);
        const m = text.match(/^#\s+(.+)/m);
        if (m) document.title = m[1];
      });
  }, [src]);

  return (
    <div className="detail" style={{ maxWidth: 900, margin: "0 auto", padding: "2rem" }}>
      <article className="analysis-content">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
      </article>
    </div>
  );
}

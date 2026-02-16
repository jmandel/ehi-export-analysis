import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Prism from "prismjs";
import "prismjs/components/prism-python";
import "prismjs/components/prism-typescript";
import "prismjs/components/prism-javascript";
import "prismjs/components/prism-bash";
import "prismjs/components/prism-json";
import "prismjs/components/prism-sql";
import "prismjs/components/prism-markup";

const CODE_EXTS: Record<string, string> = {
  py: "python", ts: "typescript", tsx: "typescript", js: "javascript",
  jsx: "javascript", sh: "bash", bash: "bash", sql: "sql",
};

function isCodeFile(path: string): string | null {
  const ext = path.split(".").pop()?.toLowerCase() ?? "";
  return CODE_EXTS[ext] ?? null;
}

export function MdViewer({ src }: { src: string }) {
  const [content, setContent] = useState<string>("Loading…");

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
        else {
          const fname = src.split("/").pop() ?? src;
          document.title = fname;
        }
      });
  }, [src]);

  const lang = isCodeFile(src);
  if (lang) {
    const grammar = Prism.languages[lang];
    const highlighted = grammar
      ? Prism.highlight(content, grammar, lang)
      : content;
    return (
      <article className="md-page code-viewer">
        <div className="code-filename">
          {src.split("/").pop()}
          <a href={src} download className="download-btn">⬇ Download</a>
        </div>
        <pre className={`language-${lang}`}>
          <code dangerouslySetInnerHTML={{ __html: highlighted }} />
        </pre>
      </article>
    );
  }

  return (
    <article className="md-page">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    </article>
  );
}

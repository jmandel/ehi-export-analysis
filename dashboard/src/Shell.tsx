import type { ReactNode } from "react";

export function Shell({ children }: { children: ReactNode }) {
  const isAbout = window.location.hash === "#about";
  return (
    <div className="app-shell">
      <header className="site-header">
        <div className="site-header-inner">
          <a href="#" className="site-title">
            <img src="favicon.svg" alt="" className="site-logo" />
            EHI Export Quality Dashboard
          </a>
          <nav className="site-nav">
            {!isAbout && <a href="#about">About</a>}
          </nav>
        </div>
      </header>
      <main>{children}</main>
      <footer className="site-footer">
        <p>
          <a href="https://github.com/jmandel-bot/ehi-export-analysis" target="_blank" rel="noopener">
            Open source
          </a>{" · "}
          Analyses are AI-generated and may contain errors.{" "}
          <a href="https://github.com/jmandel-bot/ehi-export-analysis/issues/new" target="_blank" rel="noopener">
            Report an issue
          </a>
        </p>
      </footer>
    </div>
  );
}

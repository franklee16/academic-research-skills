import { useEffect, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  AlertTriangle,
  BookOpen,
  CheckCircle2,
  CircleDot,
  ExternalLink,
  FileText,
  Files,
  GitBranch,
  ListChecks,
  Search,
  ShieldAlert
} from "lucide-react";
import { loadManifest, loadMarkdown, loadSourceIndex, loadSummaries } from "./data";
import type {
  DisplayCategory,
  ModuleSummary,
  PresentationManifest,
  PresentationModule,
  SourceFile,
  SourceIndex
} from "./types";

const categoryLabels: Record<DisplayCategory, string> = {
  "primary-display": "Primary",
  "summarize-then-link": "Summary",
  "link-only": "Linked"
};

function categoryClass(category?: DisplayCategory): string {
  return category ? `badge badge-${category}` : "badge";
}

function statusClass(status?: string): string {
  return `badge status-${(status ?? "unknown").replace(/[^a-z0-9]+/gi, "-").toLowerCase()}`;
}

function findSource(sourceIndex: SourceIndex | null, id: string): SourceFile | undefined {
  return sourceIndex?.files.find((file) => file.id === id);
}

function SourceChips({
  sourceFileIds,
  sourceIndex,
  onSelect
}: {
  sourceFileIds?: string[];
  sourceIndex: SourceIndex | null;
  onSelect: (source: SourceFile) => void;
}) {
  if (!sourceFileIds?.length) {
    return null;
  }

  return (
    <div className="source-chip-row">
      {sourceFileIds.map((id) => {
        const source = findSource(sourceIndex, id);
        return (
          <button
            className="source-chip"
            key={id}
            type="button"
            onClick={() => source && onSelect(source)}
            disabled={!source}
            title={source?.path ?? id}
          >
            <FileText size={14} />
            <span>{source?.label ?? id}</span>
          </button>
        );
      })}
    </div>
  );
}

function ModulePanel({
  module,
  summary,
  sourceIndex,
  onSelectSource
}: {
  module: PresentationModule;
  summary?: ModuleSummary;
  sourceIndex: SourceIndex | null;
  onSelectSource: (source: SourceFile) => void;
}) {
  return (
    <section className="module-panel" id={module.id}>
      <div className="module-header">
        <div>
          <div className="eyebrow-row">
            <span className={categoryClass(module.displayCategory)}>{categoryLabels[module.displayCategory]}</span>
            {module.workflow && <span className="badge badge-workflow">{module.workflow}</span>}
            {summary?.status && <span className={statusClass(summary.status)}>{summary.status}</span>}
          </div>
          <h3>{module.title}</h3>
        </div>
        <SourceChips sourceFileIds={module.sourceFileIds} sourceIndex={sourceIndex} onSelect={onSelectSource} />
      </div>

      <p className="module-summary">{summary?.summary ?? "No generated summary is available for this module yet."}</p>

      {summary?.takeaways?.length ? (
        <div className="content-block">
          <h4>
            <CheckCircle2 size={16} />
            Takeaways
          </h4>
          <ul className="clean-list">
            {summary.takeaways.map((takeaway) => (
              <li key={takeaway}>{takeaway}</li>
            ))}
          </ul>
        </div>
      ) : null}

      {summary?.structuredItems?.length ? (
        <div className="content-block">
          <h4>
            <ListChecks size={16} />
            Structured View
          </h4>
          <div className="field-table">
            {summary.structuredItems.map((item) => (
              <div className="field-row" key={`${item.label}-${item.value}`}>
                <div className="field-label">
                  <span>{item.label}</span>
                  {item.status && <span className={statusClass(item.status)}>{item.status}</span>}
                </div>
                <div className="field-value">
                  <p>{item.value}</p>
                  <SourceChips sourceFileIds={item.sourceFileIds} sourceIndex={sourceIndex} onSelect={onSelectSource} />
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {summary?.risks?.length ? (
        <div className="content-block">
          <h4>
            <ShieldAlert size={16} />
            Risks & Gaps
          </h4>
          <div className="risk-list">
            {summary.risks.map((risk) => (
              <div className={`risk-item severity-${risk.severity ?? "medium"}`} key={`${risk.label}-${risk.description}`}>
                <div className="risk-title">
                  <AlertTriangle size={15} />
                  <span>{risk.label}</span>
                  {risk.severity && <span className="badge">{risk.severity}</span>}
                </div>
                <p>{risk.description}</p>
                <SourceChips sourceFileIds={risk.sourceFileIds} sourceIndex={sourceIndex} onSelect={onSelectSource} />
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {summary?.nextActions?.length ? (
        <div className="content-block">
          <h4>
            <CircleDot size={16} />
            Next Actions
          </h4>
          <ul className="action-list">
            {summary.nextActions.map((action) => (
              <li key={action.label}>
                <span>{action.label}</span>
                {action.status && <span className={statusClass(action.status)}>{action.status}</span>}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </section>
  );
}

function SourcePreview({ source }: { source: SourceFile | null }) {
  const [markdown, setMarkdown] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    setMarkdown("");
    setError("");

    if (!source?.readUrl) {
      return;
    }

    loadMarkdown(source.readUrl)
      .then((content) => {
        if (!cancelled) setMarkdown(content);
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Unable to load source file.");
      });

    return () => {
      cancelled = true;
    };
  }, [source]);

  if (!source) {
    return (
      <aside className="source-panel">
        <h2>Source Preview</h2>
        <p className="muted">Select a source chip or source file to preview markdown here.</p>
      </aside>
    );
  }

  return (
    <aside className="source-panel">
      <div className="source-panel-header">
        <div>
          <span className={categoryClass(source.displayCategory)}>{source.displayCategory ?? "source"}</span>
          <h2>{source.label}</h2>
        </div>
        {source.openHref && (
          <a className="icon-link" href={source.openHref} title="Open source link">
            <ExternalLink size={16} />
          </a>
        )}
      </div>
      <p className="source-path">{source.relativePath ?? source.path}</p>
      {error && <p className="error-text">{error}</p>}
      {!error && !markdown && <p className="muted">Loading source markdown...</p>}
      {markdown && (
        <div className="markdown-preview">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{markdown}</ReactMarkdown>
        </div>
      )}
    </aside>
  );
}

function SourceFilesView({
  files,
  search,
  onSelect
}: {
  files: SourceFile[];
  search: string;
  onSelect: (source: SourceFile) => void;
}) {
  const filtered = files.filter((file) => {
    const target = `${file.label} ${file.relativePath ?? ""} ${file.workflow ?? ""}`.toLowerCase();
    return target.includes(search.toLowerCase());
  });

  return (
    <section className="module-panel">
      <div className="module-header">
        <div>
          <span className="badge badge-workflow">{filtered.length} files</span>
          <h3>Source Files</h3>
        </div>
      </div>
      <div className="source-file-list">
        {filtered.map((file) => (
          <button className="source-file-row" key={file.id} type="button" onClick={() => onSelect(file)}>
            <FileText size={16} />
            <span>{file.label}</span>
            <small>{file.relativePath ?? file.path}</small>
          </button>
        ))}
      </div>
    </section>
  );
}

function LoadingState() {
  return (
    <main className="empty-state">
      <BookOpen size={40} />
      <h1>Loading Workspace Presentation</h1>
      <p>Reading generated manifest, module summaries, and source index.</p>
    </main>
  );
}

function ErrorState({ error }: { error: string }) {
  return (
    <main className="empty-state">
      <AlertTriangle size={40} />
      <h1>Presentation metadata is missing</h1>
      <p>{error}</p>
      <p>Generate `public/presentation-manifest.json`, `public/source-index.json`, and module summaries before using this app.</p>
    </main>
  );
}

export default function App() {
  const [manifest, setManifest] = useState<PresentationManifest | null>(null);
  const [sourceIndex, setSourceIndex] = useState<SourceIndex | null>(null);
  const [summaries, setSummaries] = useState<Record<string, ModuleSummary>>({});
  const [activeSectionId, setActiveSectionId] = useState("overview");
  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState<DisplayCategory | "all">("all");
  const [selectedSource, setSelectedSource] = useState<SourceFile | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const loadedManifest = await loadManifest();
        const loadedSourceIndex = await loadSourceIndex();
        const loadedSummaries = await loadSummaries(loadedManifest);

        if (!cancelled) {
          setManifest(loadedManifest);
          setSourceIndex(loadedSourceIndex);
          setSummaries(loadedSummaries);
          setActiveSectionId(loadedManifest.sections[0]?.id ?? "overview");
        }
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : "Unable to load presentation metadata.");
      }
    }

    load();

    return () => {
      cancelled = true;
    };
  }, []);

  const activeSection = manifest?.sections.find((section) => section.id === activeSectionId);
  const filteredModules = useMemo(() => {
    if (!manifest) return [];
    return manifest.modules.filter((module) => {
      const summary = summaries[module.id];
      const text = `${module.title} ${module.workflow ?? ""} ${summary?.summary ?? ""}`.toLowerCase();
      const matchesSearch = text.includes(search.toLowerCase());
      const matchesCategory = categoryFilter === "all" || module.displayCategory === categoryFilter;
      return module.sectionId === activeSectionId && matchesSearch && matchesCategory;
    });
  }, [activeSectionId, categoryFilter, manifest, search, summaries]);

  if (error) return <ErrorState error={error} />;
  if (!manifest || !sourceIndex) return <LoadingState />;

  const overviewSummary = summaries.overview;
  const isSourceSection = activeSectionId === "source-files";

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <div className="eyebrow-row">
            <span className="badge badge-workflow">{manifest.presentation.sourceKind}</span>
            {manifest.presentation.status && <span className={statusClass(manifest.presentation.status)}>{manifest.presentation.status}</span>}
          </div>
          <h1>{manifest.presentation.title}</h1>
          <p>{manifest.presentation.description ?? manifest.presentation.sourceLabel ?? manifest.presentation.sourcePath}</p>
        </div>
        <div className="topbar-meta">
          <span>Generated {manifest.presentation.generatedAt}</span>
          <span>{manifest.presentation.sourceLabel ?? manifest.presentation.sourcePath}</span>
        </div>
      </header>

      <div className="workspace-layout">
        <nav className="sidebar" aria-label="Presentation sections">
          <div className="sidebar-title">
            <GitBranch size={18} />
            Sections
          </div>
          {manifest.sections.map((section) => (
            <button
              className={section.id === activeSectionId ? "nav-item active" : "nav-item"}
              key={section.id}
              type="button"
              onClick={() => setActiveSectionId(section.id)}
            >
              <span>{section.title}</span>
            </button>
          ))}
          <div className="filter-panel">
            <label>
              <Search size={15} />
              <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search modules" />
            </label>
            <select value={categoryFilter} onChange={(event) => setCategoryFilter(event.target.value as DisplayCategory | "all")}>
              <option value="all">All categories</option>
              <option value="primary-display">Primary</option>
              <option value="summarize-then-link">Summary</option>
              <option value="link-only">Linked</option>
            </select>
          </div>
        </nav>

        <main className="reader">
          {activeSectionId === "overview" && overviewSummary ? (
            <section className="overview-panel">
              <div>
                <span className="badge badge-primary-display">Overview</span>
                <h2>Research State Overview</h2>
                <p>{overviewSummary.summary}</p>
              </div>
              <div className="overview-grid">
                {(overviewSummary.takeaways ?? []).map((takeaway) => (
                  <div className="overview-item" key={takeaway}>
                    <CheckCircle2 size={18} />
                    <span>{takeaway}</span>
                  </div>
                ))}
              </div>
            </section>
          ) : null}

          <div className="section-heading">
            <div>
              <h2>{activeSection?.title ?? "Presentation"}</h2>
              <p>{isSourceSection ? "All source files exposed by this presentation." : "Generated modules are source-linked and safe to regenerate."}</p>
            </div>
            <span className="badge">{isSourceSection ? sourceIndex.files.length : filteredModules.length} items</span>
          </div>

          {isSourceSection ? (
            <SourceFilesView files={sourceIndex.files} search={search} onSelect={setSelectedSource} />
          ) : (
            filteredModules.map((module) => (
              <ModulePanel
                key={module.id}
                module={module}
                summary={summaries[module.id]}
                sourceIndex={sourceIndex}
                onSelectSource={setSelectedSource}
              />
            ))
          )}

          {!isSourceSection && filteredModules.length === 0 ? (
            <section className="module-panel empty-module">
              <Files size={28} />
              <h3>No modules match the current filters.</h3>
            </section>
          ) : null}
        </main>

        <SourcePreview source={selectedSource} />
      </div>
    </div>
  );
}

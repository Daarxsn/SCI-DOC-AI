import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Badge, Card, Button } from "../components/ui";
import { ApiError, api, type ResultArtifact, type ResultResponse } from "../services/api";

export function DocumentWorkspacePage() {
  const { documentId } = useParams();
  const [result, setResult] = useState<ResultResponse | null>(null);
  const [loading, setLoading] = useState(Boolean(documentId));
  const [error, setError] = useState<string | null>(null);

  const loadResults = async () => {
    if (!documentId) return;
    setLoading(true);
    setError(null);
    try {
      setResult(await api.getResults(documentId));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Unable to load document results.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadResults();
  }, [documentId]);

  if (!documentId) {
    return <EmptyWorkspace message="No document ID was provided." />;
  }

  return (
    <div>
      <header className="page-header">
        <p className="eyebrow">Document workspace</p>
        <div className="section-heading">
          <div>
            <h1>{documentId}</h1>
            <p className="lead">
              Results returned by the SCI-DOC AI document-results contract.
            </p>
          </div>
          {result ? <Badge tone={result.status === "available" ? "success" : "info"}>{result.status}</Badge> : null}
        </div>
        <div className="page-actions">
          <Button variant="secondary" onClick={() => void loadResults()} disabled={loading}>
            {loading ? "Refreshing…" : "Refresh results"}
          </Button>
        </div>
      </header>

      {error ? (
        <Card className="status-panel status-panel--error" role="alert">
          <strong>Results unavailable</strong>
          <p>{error}</p>
          <span>The API may require a valid API key and documents:read scope.</span>
        </Card>
      ) : null}

      {loading ? (
        <Card><span className="loading-state">Loading document results…</span></Card>
      ) : result ? (
        <ResultsView result={result} />
      ) : !error ? (
        <EmptyWorkspace message="No result payload is available." />
      ) : null}
    </div>
  );
}

function ResultsView({ result }: { result: ResultResponse }) {
  const [query, setQuery] = useState("");
  const [format, setFormat] = useState("all");
  const [sort, setSort] = useState<"newest" | "largest" | "format">("newest");

  const formats = Array.from(new Set(result.artifacts.map((artifact) => artifact.format))).sort();
  const filtered = result.artifacts
    .filter((artifact) => format === "all" || artifact.format === format)
    .filter((artifact) => {
      const needle = query.trim().toLowerCase();
      if (!needle) return true;
      return [artifact.artifact_id, artifact.format, artifact.path, artifact.checksum ?? ""].some((value) =>
        value.toLowerCase().includes(needle),
      );
    })
    .sort((a, b) => {
      if (sort === "largest") return b.size_bytes - a.size_bytes;
      if (sort === "format") return a.format.localeCompare(b.format) || a.artifact_id.localeCompare(b.artifact_id);
      return 0;
    });

  return (
    <section className="results-workspace">
      <div className="system-grid">
        <Card><div className="system-card__label">Document ID</div><div className="system-card__value workspace-value">{result.document_id}</div></Card>
        <Card><div className="system-card__label">Result status</div><div className="system-card__value">{result.status}</div></Card>
        <Card><div className="system-card__label">Artifacts</div><div className="system-card__value">{result.artifacts.length}</div></Card>
      </div>

      <Card className="artifact-card">
        <div className="section-heading">
          <div><h2>Artifacts</h2><p className="result-note">Review metadata returned by the results API.</p></div>
          <Badge tone="info">{filtered.length} shown</Badge>
        </div>

        {result.artifacts.length === 0 ? (
          <div className="empty-state"><strong>No artifacts yet</strong><span>The backend returned an empty artifact collection for this document.</span></div>
        ) : (
          <>
            <div className="artifact-toolbar" aria-label="Artifact filters">
              <label className="artifact-search">Search<input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="ID, format, path, checksum" /></label>
              <label>Format<select value={format} onChange={(event) => setFormat(event.target.value)}><option value="all">All formats</option>{formats.map((item) => <option key={item} value={item}>{item}</option>)}</select></label>
              <label>Sort<select value={sort} onChange={(event) => setSort(event.target.value as typeof sort)}><option value="newest">API order</option><option value="largest">Largest first</option><option value="format">Format</option></select></label>
            </div>
            {filtered.length === 0 ? (
              <div className="empty-state"><strong>No matching artifacts</strong><span>Try a different search or format filter.</span></div>
            ) : (
              <div className="artifact-list">
                {filtered.map((artifact, index) => <ArtifactItem key={artifact.artifact_id} artifact={artifact} index={index + 1} />)}
              </div>
            )}
          </>
        )}
      </Card>
    </section>
  );
}

function formatBytes(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  const units = ["KB", "MB", "GB"];
  let value = bytes / 1024;
  let unit = units[0];
  for (let index = 1; value >= 1024 && index < units.length; index += 1) {
    value /= 1024;
    unit = units[index];
  }
  return `${value.toFixed(value >= 10 ? 0 : 1)} ${unit}`;
}

function EmptyWorkspace({ message }: { message: string }) {
  return (
    <Card className="empty-state">
      <strong>Document workspace</strong>
      <span>{message}</span>
    </Card>
  );
}

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
  return (
    <section className="results-workspace">
      <div className="system-grid">
        <Card>
          <div className="system-card__label">Document ID</div>
          <div className="system-card__value workspace-value">{result.document_id}</div>
        </Card>
        <Card>
          <div className="system-card__label">Result status</div>
          <div className="system-card__value">{result.status}</div>
        </Card>
        <Card>
          <div className="system-card__label">Artifacts</div>
          <div className="system-card__value">{result.artifacts.length}</div>
        </Card>
      </div>

      <Card className="artifact-card">
        <div className="section-heading">
          <h2>Artifacts</h2>
          <Badge tone="info">{result.artifacts.length} returned</Badge>
        </div>

        {result.artifacts.length === 0 ? (
          <div className="empty-state">
            <strong>No artifacts yet</strong>
            <span>The backend returned an empty artifact collection for this document.</span>
          </div>
        ) : (
          <div className="artifact-list">
            {result.artifacts.map((artifact, index) => (
              <ArtifactItem key={index} artifact={artifact} index={index + 1} />
            ))}
          </div>
        )}
      </Card>
    </section>
  );
}

function ArtifactItem({ artifact, index }: { artifact: ResultArtifact; index: number }) {
  return (
    <details className="artifact-item" open={index === 1}>
      <summary>
        <strong>Artifact {index}</strong>
        <Badge tone="neutral">{Object.keys(artifact).length} fields</Badge>
      </summary>
      <pre>{JSON.stringify(artifact, null, 2)}</pre>
    </details>
  );
}

function EmptyWorkspace({ message }: { message: string }) {
  return (
    <Card className="empty-state">
      <strong>Document workspace</strong>
      <span>{message}</span>
    </Card>
  );
}

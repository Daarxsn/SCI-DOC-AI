import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Badge, Button, Card, TextField } from "../components/ui";
import { ApiError, api, type JobStatusResponse } from "../services/api";

const TERMINAL = new Set(["completed", "failed"]);
const JOB_DOCUMENT_KEY = "sci-doc-ai.job-document.";

export function JobPage() {
  const { jobId: routeJobId } = useParams();
  const [documentId, setDocumentId] = useState("");
  const [targetLanguage, setTargetLanguage] = useState("Hindi");
  const [domain, setDomain] = useState("general");
  const [jobId, setJobId] = useState(routeJobId ?? "");
  const [job, setJob] = useState<JobStatusResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);
  const [loadingJob, setLoadingJob] = useState(Boolean(routeJobId));

  const loadJob = async (id: string) => {
    setLoadingJob(true);
    setError(null);
    try {
      const latest = await api.getJob(id);
      setJobId(id);
      setJob(latest);
      const storedDocumentId = window.localStorage.getItem(JOB_DOCUMENT_KEY + id);
      if (storedDocumentId) setDocumentId(storedDocumentId);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Unable to load the job.");
    } finally {
      setLoadingJob(false);
    }
  };

  useEffect(() => {
    if (routeJobId) void loadJob(routeJobId);
  }, [routeJobId]);

  const createJob = async () => {
    const normalizedDocumentId = documentId.trim();
    if (!normalizedDocumentId) {
      setError("Document ID is required by the current backend contract.");
      return;
    }
    setCreating(true);
    setError(null);
    try {
      const created = await api.createJob({
        document_id: normalizedDocumentId,
        target_language: targetLanguage.trim(),
        domain: domain.trim(),
        idempotency_key: crypto.randomUUID(),
      });
      window.localStorage.setItem(JOB_DOCUMENT_KEY + created.job_id, normalizedDocumentId);
      setJobId(created.job_id);
      setJob(created);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Unable to create the job.");
    } finally {
      setCreating(false);
    }
  };

  useEffect(() => {
    if (!jobId || !job || TERMINAL.has(job.status)) return;
    const timer = window.setInterval(async () => {
      try {
        const latest = await api.getJob(jobId);
        setJob(latest);
        if (TERMINAL.has(latest.status)) window.clearInterval(timer);
      } catch (err) {
        setError(err instanceof ApiError ? err.message : "Unable to refresh job status.");
        window.clearInterval(timer);
      }
    }, 2000);
    return () => window.clearInterval(timer);
  }, [jobId, job?.status]);

  return (
    <div>
      <header className="page-header">
        <p className="eyebrow">Processing</p>
        <h1>Job control</h1>
        <p className="lead">
          Create and monitor a document-processing job using the existing protected job API.
          The document ID must come from a valid backend document lifecycle.
        </p>
      </header>

      <Card className="job-form">
        <div className="form-grid">
          <TextField label="Document ID" placeholder="Backend document ID" value={documentId}
            onChange={(event) => setDocumentId(event.target.value)} hint="Required by POST /v1/jobs." />
          <TextField label="Target language" value={targetLanguage}
            onChange={(event) => setTargetLanguage(event.target.value)} />
          <TextField label="Domain" value={domain}
            onChange={(event) => setDomain(event.target.value)} />
        </div>
        <div className="page-actions">
          <Button size="lg" onClick={() => void createJob()} disabled={creating}>
            {creating ? "Creating…" : "Create processing job"}
          </Button>
          {jobId ? <Link className="button button--secondary button--lg" to={`/jobs/${jobId}`}>Open job route</Link> : null}
        </div>
        {error ? (
          <div className="status-panel status-panel--error" role="alert">
            <strong>Job request failed</strong><p>{error}</p>
          </div>
        ) : null}
      </Card>

      {loadingJob ? <Card className="job-status"><span className="loading-state">Loading job…</span></Card> : null}
      {job ? <JobStatus job={job} documentId={documentId} /> : null}
    </div>
  );
}

function JobStatus({ job, documentId }: { job: JobStatusResponse; documentId: string }) {
  const tone = job.status === "completed" ? "success" : job.status === "failed" ? "danger" : "info";
  return (
    <section className="job-status">
      <div className="section-heading">
        <div><p className="eyebrow">Live job status</p><h2>{job.job_id}</h2></div>
        <Badge tone={tone}>{job.status}</Badge>
      </div>
      <Card className="progress-card">
        <div className="progress-header"><strong>{job.stage}</strong><span>{job.progress}%</span></div>
        <div className="progress-track" role="progressbar" aria-valuenow={job.progress} aria-valuemin={0} aria-valuemax={100}>
          <div className="progress-fill" style={{ width: `${job.progress}%` }} />
        </div>
        {job.error ? <p className="job-error">{job.error}</p> : null}
        <div className="job-actions">
          {documentId ? <Link className="button button--secondary" to={`/documents/${encodeURIComponent(documentId)}`}>Open document results</Link> : null}
          {!TERMINAL.has(job.status) ? <p className="result-note">Refreshing every 2 seconds while the job is active.</p> : null}
        </div>
        <p className="result-note">The job API does not currently return document_id, so this UI retains the document ID locally when the job is created.</p>
      </Card>
    </section>
  );
}

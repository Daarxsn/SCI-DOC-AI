import { useEffect, useState } from "react";
import { Badge, Button, Card, TextField } from "../components/ui";
import { ApiError, api, type JobStatusResponse } from "../services/api";

const TERMINAL = new Set(["completed", "failed"]);

export function JobPage() {
  const [documentId, setDocumentId] = useState("");
  const [targetLanguage, setTargetLanguage] = useState("Hindi");
  const [domain, setDomain] = useState("general");
  const [jobId, setJobId] = useState("");
  const [job, setJob] = useState<JobStatusResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);

  const createJob = async () => {
    if (!documentId.trim()) {
      setError("Document ID is required by the current backend contract.");
      return;
    }
    setCreating(true);
    setError(null);
    try {
      const created = await api.createJob({
        document_id: documentId.trim(),
        target_language: targetLanguage.trim(),
        domain: domain.trim(),
        idempotency_key: crypto.randomUUID(),
      });
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
        </div>
        {error ? (
          <div className="status-panel status-panel--error" role="alert">
            <strong>Job request failed</strong><p>{error}</p>
          </div>
        ) : null}
      </Card>
      {job ? <JobStatus job={job} /> : null}
    </div>
  );
}

function JobStatus({ job }: { job: JobStatusResponse }) {
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
        {!TERMINAL.has(job.status) ? <p className="result-note">Refreshing every 2 seconds while the job is active.</p> : null}
      </Card>
    </section>
  );
}

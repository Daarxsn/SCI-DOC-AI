import { useEffect, useState } from "react";
import { Badge, Button, Card } from "../components/ui";
import { api, type HealthResponse, type ReadinessResponse, type RuntimeResponse } from "../services/api";

type PlatformState = { loading: boolean; health?: HealthResponse; readiness?: ReadinessResponse; runtime?: RuntimeResponse; error?: string; };

export function DashboardPage() {
  const [platform, setPlatform] = useState<PlatformState>({ loading: true });
  const loadPlatformStatus = async () => {
    setPlatform({ loading: true });
    try {
      const [health, readiness, runtime] = await Promise.all([api.health(), api.ready(), api.runtime()]);
      setPlatform({ loading: false, health, readiness, runtime });
    } catch (error) {
      setPlatform({ loading: false, error: error instanceof Error ? error.message : "Unable to reach the API" });
    }
  };
  useEffect(() => { void loadPlatformStatus(); }, []);
  const apiAvailable = platform.health?.status === "ok";
  const ready = platform.readiness?.status === "ready";
  return (
    <div>
      <header className="page-header">
        <p className="eyebrow">SCI-DOC AI</p><h1>Scientific document intelligence</h1>
        <p className="lead">A focused workspace for scientific document processing, translation, validation, and reconstruction.</p>
        <div className="page-actions"><Button>Open documents</Button><Button variant="secondary" onClick={() => void loadPlatformStatus()} disabled={platform.loading}>{platform.loading ? "Checking…" : "Refresh platform status"}</Button></div>
      </header>
      <section className="system-grid" aria-label="Platform status">
        <Card interactive><div className="system-card__label">API connectivity</div><div className="system-card__value">{platform.loading ? "Checking…" : apiAvailable ? "Online" : "Unavailable"}</div><div className="system-card__meta"><Badge tone={apiAvailable ? "success" : platform.loading ? "neutral" : "danger"}>{platform.loading ? "Checking" : apiAvailable ? "Healthy" : "Offline"}</Badge></div></Card>
        <Card interactive><div className="system-card__label">Production readiness</div><div className="system-card__value">{platform.loading ? "Checking…" : ready ? "Ready" : "Not ready"}</div><div className="system-card__meta"><Badge tone={ready ? "success" : platform.loading ? "neutral" : "warning"}>{platform.loading ? "Checking" : ready ? "Ready" : "Review checks"}</Badge></div></Card>
        <Card interactive><div className="system-card__label">API boundary</div><div className="system-card__value">Typed client</div><div className="system-card__meta"><Badge tone="info">F03 active</Badge></div></Card>
      </section>
      {platform.readiness && !platform.readiness.status.includes("ready") ? <Card className="diagnostics-card"><div className="section-heading"><h2>Readiness diagnostics</h2><Badge tone="warning">{platform.readiness.errors.length} issue{platform.readiness.errors.length === 1 ? "" : "s"}</Badge></div><div className="diagnostic-list">{Object.entries(platform.readiness.checks).map(([name, passed]) => <div className="diagnostic-row" key={name}><span>{name}</span><Badge tone={passed ? "success" : "danger"}>{passed ? "Pass" : "Fail"}</Badge></div>)}</div>{platform.readiness.errors.length > 0 ? <div className="diagnostic-errors">{platform.readiness.errors.map((item, index) => <p key={index}>{item}</p>)}</div> : null}</Card> : null}
      {platform.runtime ? <Card className="diagnostics-card"><div className="section-heading"><h2>Runtime diagnostics</h2><Badge tone="info">Backend supplied</Badge></div><div className="runtime-grid">{Object.entries(platform.runtime).filter(([key]) => key !== "service").map(([key,value]) => <div key={key}><span>{key}</span><strong>{typeof value === "object" ? JSON.stringify(value) : String(value)}</strong></div>)}</div></Card> : null}
      {platform.error ? <Card className="status-panel status-panel--error"><strong>API connection unavailable</strong><p>{platform.error}</p><span>Start the SCI-DOC AI backend at the configured VITE_API_BASE_URL.</span></Card> : null}
    </div>
  );
}
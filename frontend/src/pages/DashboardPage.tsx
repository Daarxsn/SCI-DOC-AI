import { useEffect, useState } from "react";
import { Badge, Button, Card } from "../components/ui";
import { api, type HealthResponse, type ReadinessResponse } from "../services/api";

type PlatformState = {
  loading: boolean;
  health?: HealthResponse;
  readiness?: ReadinessResponse;
  error?: string;
};

export function DashboardPage() {
  const [platform, setPlatform] = useState<PlatformState>({ loading: true });

  const loadPlatformStatus = async () => {
    setPlatform({ loading: true });
    try {
      const [health, readiness] = await Promise.all([api.health(), api.ready()]);
      setPlatform({ loading: false, health, readiness });
    } catch (error) {
      setPlatform({
        loading: false,
        error: error instanceof Error ? error.message : "Unable to reach the API",
      });
    }
  };

  useEffect(() => {
    void loadPlatformStatus();
  }, []);

  const apiAvailable = platform.health?.status === "ok";
  const ready = platform.readiness?.status === "ready";

  return (
    <div>
      <header className="page-header">
        <p className="eyebrow">SCI-DOC AI</p>
        <h1>Scientific document intelligence</h1>
        <p className="lead">
          A focused workspace for scientific document processing, translation,
          validation, and reconstruction.
        </p>
        <div className="page-actions">
          <Button>Open documents</Button>
          <Button variant="secondary" onClick={() => void loadPlatformStatus()}>
            Refresh platform status
          </Button>
        </div>
      </header>

      <section className="system-grid" aria-label="Platform status">
        <Card interactive>
          <div className="system-card__label">API connectivity</div>
          <div className="system-card__value">
            {platform.loading ? "Checking…" : apiAvailable ? "Online" : "Unavailable"}
          </div>
          <div className="system-card__meta">
            <Badge tone={apiAvailable ? "success" : platform.loading ? "neutral" : "danger"}>
              {platform.loading ? "Checking" : apiAvailable ? "Healthy" : "Offline"}
            </Badge>
          </div>
        </Card>

        <Card interactive>
          <div className="system-card__label">Production readiness</div>
          <div className="system-card__value">
            {platform.loading ? "Checking…" : ready ? "Ready" : "Not ready"}
          </div>
          <div className="system-card__meta">
            <Badge tone={ready ? "success" : platform.loading ? "neutral" : "warning"}>
              {platform.loading ? "Checking" : ready ? "Ready" : "Review checks"}
            </Badge>
          </div>
        </Card>

        <Card interactive>
          <div className="system-card__label">API boundary</div>
          <div className="system-card__value">Typed client</div>
          <div className="system-card__meta">
            <Badge tone="info">F03 active</Badge>
          </div>
        </Card>
      </section>

      {platform.error ? (
        <Card className="status-panel">
          <strong>API connection unavailable</strong>
          <p>{platform.error}</p>
          <span>Start the SCI-DOC AI backend at the configured VITE_API_BASE_URL.</span>
        </Card>
      ) : null}
    </div>
  );
}

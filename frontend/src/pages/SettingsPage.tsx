import { Badge, Card } from "../components/ui";
import { apiConfig } from "../services/api";

export function SettingsPage() {
  const configuredKey = Boolean(apiConfig.apiKey);
  return <div>
    <header className="page-header"><p className="eyebrow">Configuration</p><h1>Settings</h1><p className="lead">Runtime configuration visible to the frontend. Secret values are never rendered.</p></header>
    <Card className="config-card"><div className="section-heading"><h2>API connection</h2><Badge tone={configuredKey ? "success" : "neutral"}>{configuredKey ? "Protected" : "No API key"}</Badge></div>
      <div className="config-list"><div><span>API base URL</span><strong className="config-value">{apiConfig.baseUrl}</strong></div><div><span>API key</span><strong>{configuredKey ? "Configured (value hidden)" : "Not configured"}</strong></div></div>
      <p className="result-note">Configuration comes from VITE_API_BASE_URL and VITE_API_KEY at build time. Change the frontend environment and rebuild to apply changes.</p>
    </Card>
    <Card className="config-card"><div className="section-heading"><h2>Operational boundary</h2><Badge tone="info">F11</Badge></div><p className="result-note">Dashboard diagnostics are sourced from the backend health, readiness, and runtime endpoints. This page never exposes the API key itself.</p></Card>
  </div>;
}
import { Badge, Button, Card } from "../components/ui";

export function DashboardPage() {
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
          <Button variant="secondary">View platform status</Button>
        </div>
      </header>

      <section className="system-grid" aria-label="Platform foundation">
        <Card interactive>
          <div className="system-card__label">Frontend foundation</div>
          <div className="system-card__value">React + TypeScript</div>
          <div className="system-card__meta"><Badge tone="success">Ready</Badge></div>
        </Card>
        <Card interactive>
          <div className="system-card__label">API boundary</div>
          <div className="system-card__value">Typed fetch client</div>
          <div className="system-card__meta"><Badge tone="info">Configured</Badge></div>
        </Card>
        <Card interactive>
          <div className="system-card__label">Design system</div>
          <div className="system-card__value">F02 foundation</div>
          <div className="system-card__meta"><Badge tone="success">Active</Badge></div>
        </Card>
      </section>
    </div>
  );
}

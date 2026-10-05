# Phase 37 — Production Observability & Monitoring Contract

Phase 37 establishes the observability contract required for operating SCI-DOC AI safely in production.

## Required controls

- structured logging;
- correlation IDs across requests/jobs/pipeline stages;
- tenant-safe telemetry;
- latency metrics;
- error metrics;
- audit events;
- health/alert contract.

Telemetry events use a stable schema and must never require raw document contents to identify a request.

## Evidence rule

A passing Phase 37 gate proves that the observability contract is implemented and mechanically validated. It does not prove that a live production monitoring stack is deployed.

## Run

    python scripts/check_phase37_observability.py --manifest phase37-observability-manifest.json --output phase37-observability-readiness.json

CI uses synthetic manifests and event fixtures only.

# Frontend Phase 11 — Observability & Operational Diagnostics

## Objective
Expose backend health, readiness, runtime, and safe frontend configuration information in a review-friendly operational surface.

## Scope
- Dashboard consumes the real `/runtime` endpoint in addition to `/health` and `/ready`.
- Readiness checks and backend-supplied errors are shown when the platform is not ready.
- Runtime fields are displayed as backend-supplied diagnostics.
- Settings shows the configured API base URL and whether an API key exists without exposing the key value.
- Configuration changes are documented as build-time frontend environment changes.

## Contract boundary
Diagnostics are observational. The frontend does not reinterpret backend readiness, invent health states, or expose secret values.

## Acceptance criteria
1. Dashboard requests real health, readiness, and runtime endpoints.
2. Readiness failures show their backend-supplied checks/errors.
3. Runtime information is visibly sourced from the backend.
4. API key values are never rendered.
5. API base URL is visible for operational troubleshooting.
6. Production build passes in CI.

## Evidence boundary
Passing F11 proves operational diagnostics integration in the frontend. It does not prove uptime, monitoring coverage, alert delivery, production infrastructure health, or security compliance.

# Enterprise API — M7

SCI-DOC AI exposes a versioned /v1 API boundary.

## Authentication
API-key authentication uses the X-API-Key header and constant-time comparison.

## Jobs
POST /v1/jobs creates an asynchronous processing job and returns HTTP 202.
GET /v1/jobs/{job_id}?tenant_id=... returns tenant-scoped status.

Job states: queued, processing, review, validating, completed, failed.

## Security
M7 introduces API-key authentication, tenant-scoped job access, cross-tenant denial, health, and readiness endpoints.

Production hardening should use a secret manager, TLS, rate limiting, durable job storage, OAuth/OIDC or signed service credentials where appropriate, and centralized audit logging.

## Architecture
Client -> API Gateway -> Authentication -> Tenant Context -> Job Service -> Pipeline Workers -> UDR -> Translation -> M5 -> Review -> Reconstruction.

The current job store is in-process and intended for development. Production should replace it with a durable queue/database.

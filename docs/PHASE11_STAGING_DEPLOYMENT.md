# Phase 11 — Staging Deployment

## Objective

Establish a reproducible staging stack for SCI-DOC AI after the v1.0.0 production-candidate release.

## Stack

- FastAPI API container
- PostgreSQL 16
- Redis 7
- MinIO object-storage-compatible service
- Docker Compose orchestration
- Health checks for every infrastructure dependency
- Environment-driven secrets and staging configuration

## Start locally

1. Copy `.env.staging.example` to `.env.staging`.
2. Replace every `replace-with-...` value with local staging values.
3. Start the stack:

```bash
docker compose --env-file .env.staging -f docker-compose.staging.yml up -d --build
```

4. Verify the API:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
```

5. Stop the stack when finished:

```bash
docker compose --env-file .env.staging -f docker-compose.staging.yml down
```

Use `down -v` only when intentionally deleting staging volumes.

## Phase 11 boundary

This phase provisions the staging infrastructure and verifies that the API can start against the staging service topology.

The current job, audit, and artifact implementations still use in-memory adapters. PostgreSQL, Redis, and MinIO are therefore **staging infrastructure dependencies**, not yet the application's persistent data path. Persistent adapter integration is intentionally left for subsequent work.

Likewise, the heavy ML runtime is not enabled by this phase. Phase 12 connects and validates the real model runtime.

## Verification

The Phase 11 workflow performs:

1. Python dependency installation.
2. Full test suite.
3. Phase 11 structural verification.
4. Docker Compose configuration validation.
5. API image build.
6. Full staging stack startup.
7. Health endpoint verification.
8. Readiness endpoint verification.
9. Clean stack shutdown.

No client accuracy or production performance claim is made by this phase.

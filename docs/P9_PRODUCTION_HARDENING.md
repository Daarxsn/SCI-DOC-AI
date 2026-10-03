# P9 — Production Hardening

P9 turns the P7 security boundaries and P8 pilot contracts into deployment-grade operational checks.

## Production boundaries

- Tenant identity is derived from the authenticated principal, never from a result request parameter.
- Result artifacts remain tenant-scoped.
- Artifact payloads can be verified using SHA-256 checksums.
- Job retries have an explicit maximum-attempt policy.
- Production readiness checks required credentials and requires DEBUG=false.

## Persistence

The current in-memory implementations remain development/test adapters. Production deployment must inject durable PostgreSQL/Redis/object-storage implementations.

## Secrets and identity

Production API keys/secrets must be supplied through a secret manager or equivalent deployment secret mechanism. They must not be committed to source control.

## Deployment acceptance

A production deployment should verify:

1. API authentication and tenant isolation.
2. Durable job repository and queue.
3. Durable document/result storage.
4. Artifact checksum verification.
5. Bounded retry behavior.
6. Readiness checks.
7. TLS termination and secret management.
8. Audit-log persistence and retention.
9. Resource limits and worker concurrency.
10. Backup and recovery procedures.

P9 CI tests verify the code-level hardening contracts only; they do not prove that external infrastructure is configured.

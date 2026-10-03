# P10 — Production Release

## Release

**SCI-DOC AI v1.0.0**  
Channel: production-candidate  
API: v1

P10 packages the completed engineering phases into a reproducible release candidate.

## Release contents

- versioned release manifest;
- production Docker Compose contract;
- production secret requirements;
- API health endpoint;
- readiness endpoint;
- release verification tests;
- GitHub Actions release gate.

## Deployment sequence

1. Build the container from the repository commit.
2. Supply secrets through the deployment secret manager.
3. Provision durable PostgreSQL/Redis/object storage implementations.
4. Configure TLS at the ingress/load-balancer boundary.
5. Configure worker concurrency and resource limits.
6. Run `/health` and `/ready` smoke checks.
7. Run the agreed real-client pilot dataset.
8. Review validation/review failures.
9. Approve the deployment using the pilot acceptance criteria.

## Release integrity

The release manifest records the supported scope, pipeline stages, security controls, verified phase gates and known limitations.

## What CI proves

P10 CI proves that the release package is structurally consistent and its release contract tests pass.

CI does **not** prove:

- live cloud infrastructure;
- production database/queue/object storage;
- TLS configuration;
- secret-manager configuration;
- heavy ML model availability;
- real-client accuracy.

## Release status

P10 is an engineering release-candidate gate. A live production launch remains dependent on the external deployment and real-client acceptance steps above.
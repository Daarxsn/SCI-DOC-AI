# Phase 42 — Cloud Deployment & Environment Promotion

Phase 42 establishes the environment-promotion contract required to move
SCI-DOC AI from engineering readiness toward a real cloud deployment.

## Required controls

- immutable/pinned container image;
- environment configuration;
- secret injection;
- TLS termination;
- health and readiness checks;
- persistent storage;
- queue/worker topology;
- network boundary;
- observability export;
- backup policy;
- rollback strategy;
- migration strategy;
- artifact registry;
- deployment approval.

The manifest also requires an explicit environment, image reference, and
rollback version.

## Evidence boundary

A passing Phase 42 CI gate validates the deployment contract only. It does
**not** claim that AWS, Azure, GCP, NIC Cloud, or any other cloud deployment
exists, and it does not claim that a live endpoint has been exercised.

The report therefore keeps:

- `deployment_claim=false`;
- `live_cloud_deployment_verified=false`;
- `live_endpoint_verified=false`;
- `rollback_verified=false`.

The checked-in deployment manifest is a synthetic engineering fixture.

## Promotion sequence

1. Build the production container.
2. Push an immutable image digest to the approved registry.
3. Inject secrets through the deployment platform's secret manager.
4. Provision durable storage and queue/worker infrastructure.
5. Configure TLS and network boundaries.
6. Deploy to staging.
7. Run health/readiness and Phase 36 smoke checks.
8. Run representative load/security checks.
9. Obtain deployment approval.
10. Promote the exact image digest to production.
11. Verify the production endpoint.
12. Record rollback evidence.

## Run

    python scripts/check_phase42_deployment.py \
      --manifest datasets/golden/phase42-deployment-manifest.json \
      --output phase42-deployment-readiness.json

# Phase 36 — Deployment Smoke Test & Service Contract

Phase 36 defines the first post-readiness smoke-test gate for a deployable SCI-DOC AI environment.

## Required checks

- health endpoint contract;
- readiness endpoint contract;
- authentication contract;
- tenant-isolation contract;
- artifact-integrity contract;
- end-to-end pipeline contract.

Every required check must explicitly pass.

## Evidence rule

Phase 36 validates a supplied smoke-test manifest. CI fixtures prove the mechanics of the gate only.

A passing CI workflow does not prove that a live server exists. The report therefore keeps:
- deployment_claim: false
- live_deployment_verified: false

until an actual deployed environment is externally exercised.

## Run

    python scripts/run_phase36_smoke_test.py --manifest phase36-smoke-manifest.json --output phase36-smoke-report.json

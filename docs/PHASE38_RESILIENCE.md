# Phase 38 — Reliability, Resilience & Failure Recovery

Phase 38 establishes the resilience contract required before operating SCI-DOC AI under real production load.

## Required controls

- bounded retries;
- idempotent jobs;
- queue recovery;
- artifact recovery;
- dependency timeouts;
- graceful degradation;
- failure isolation.

These controls address repeated jobs, worker interruption, partial failures, external dependency failures, and recoverable artifact processing.

## Evidence rule

A passing Phase 38 gate proves that the resilience contract is represented and mechanically validated. It does not prove that a live deployment has survived a production failure or load test.

The report therefore keeps deployment_claim and live_resilience_verified false until real environment chaos/load testing is performed.

## Run

    python scripts/check_phase38_resilience.py --manifest phase38-resilience-manifest.json --output phase38-resilience-readiness.json

CI uses synthetic manifests only.

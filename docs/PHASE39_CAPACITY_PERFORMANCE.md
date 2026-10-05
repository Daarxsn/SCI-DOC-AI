# Phase 39 — Capacity, Load & Performance Engineering

Phase 39 establishes a measurable capacity/performance contract before live
production load testing.

## Required controls

- load-test plan;
- latency SLO;
- throughput SLO;
- explicit concurrency limit;
- queue capacity;
- resource-headroom target;
- performance observability;
- numeric targets for concurrency, throughput, p95 latency, and error rate.

The contract makes performance expectations explicit and provides the inputs
for a later environment-specific load test.

## Evidence boundary

A passing Phase 39 CI gate proves that the capacity contract is present and
mechanically validated. It does **not** prove live throughput, latency,
capacity, autoscaling behavior, or production SLO attainment.

The readiness report therefore keeps:

- `deployment_claim=false`;
- `live_load_test_verified=false`;
- `production_slo_verified=false`.

The checked-in manifest is a synthetic engineering fixture, not a client or
production performance result.

## Example

    python scripts/check_phase39_capacity.py \
      --manifest datasets/golden/phase39-capacity-manifest.json \
      --output phase39-capacity-readiness.json

## Next operational step

A real deployment should execute an environment-specific load test using
representative document sizes, model providers, queue/worker topology, and
tenant concurrency. Its measured p50/p95/p99 latency, throughput, error rate,
queue depth, CPU/GPU/memory utilization, and saturation point should then be
registered as evidence separately from this CI gate.

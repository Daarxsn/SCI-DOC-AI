# Phase 26 — Benchmark Run Registry & Experiment Tracking

Phase 26 records every benchmark execution against an immutable dataset freeze.

## Recorded provenance

- unique run ID;
- UTC creation timestamp;
- dataset ID/version;
- dataset freeze fingerprint;
- environment fingerprint;
- benchmark result fingerprint;
- complete benchmark result when available;
- final run fingerprint.

The run record is independently verifiable and detects post-run tampering.

## Run

python scripts/register_phase26_run.py --freeze phase25-freeze.json --output phase26-run.json --environment-json '{"python":"3.12","provider":"staging"}'

For a completed benchmark:
python scripts/register_phase26_run.py --freeze phase25-freeze.json --benchmark-result phase22-release/phase22-result.json --output phase26-run.json

Verify:
python scripts/verify_phase26_run.py --run phase26-run.json

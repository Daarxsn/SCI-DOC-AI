# Phase 29 — Benchmark Eligibility & Ground-Truth Integrity

Phase 29 is the integrity gate between verified ground truth and an executable scientific benchmark.

## What it verifies

For every Phase 27/28 case, Phase 29 verifies:
- Phase 27 intake status is INTAKE_VALIDATED;
- Phase 28 status is GROUND_TRUTH_VERIFIED;
- case IDs match exactly;
- the source document SHA-256 still matches the Phase 27 intake;
- the Phase 28 source SHA-256 matches the actual source;
- reference and annotation files still match their recorded SHA-256 hashes;
- ground truth remains explicitly VERIFIED;
- no scientific accuracy claim is introduced by the integrity gate.

A passing case receives benchmark_eligible: true.

## Fail-closed behavior

Phase 29 rejects missing assets, tampering, hash mismatches, case-set mismatches, invalid upstream status, or any attempt to turn ground-truth verification into an accuracy claim.

## Run

    python scripts/run_phase29_eligibility.py --intake phase27-intake.json --ground-truth phase28-ground-truth.json --root . --output phase29-benchmark-eligibility.json

CI fixtures are synthetic integrity tests only and are not scientific benchmark results.

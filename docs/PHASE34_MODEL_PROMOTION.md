# Phase 34 — Benchmark-Validated Model Promotion

Phase 34 creates the controlled promotion gate between experimentation and a deployable model/configuration profile.

## Promotion requirements

A candidate must:
- come from a completed Phase 33 comparison;
- pass the Phase 33 candidate acceptance rule;
- include explicit configuration provenance;
- include an explicit human approver.

The promotion record contains fingerprints for both the candidate configuration and comparison evidence.

## Evidence rule

Promotion does not itself create a scientific accuracy claim. It records that the candidate passed the configured benchmark-comparison gate and was explicitly approved for the next deployment stage.

A tampered or incomplete promotion record fails verification.

## Run

    python scripts/promote_phase34_candidate.py --comparison phase33-comparison.json --config candidate-config.json --approver "reviewer" --output phase34-promotion.json
    python scripts/verify_phase34_promotion.py --promotion phase34-promotion.json

CI uses synthetic evidence only and is not a scientific performance result.

# Phase 23 — Real Benchmark Result Validation

Phase 23 validates the integrity of a Phase 22 executed-result package before it can be treated as a release evidence record.

Checks include:
- real execution status;
- explicit accuracy claim;
- required OCR and translation metrics;
- finite metric values and thresholds;
- overall-score consistency;
- benchmark pass-state consistency;
- evidence-manifest hash presence.

A validation pass does not create or improve scientific accuracy. It only establishes that the supplied measured result is internally consistent and auditable.

## Run

python scripts/validate_phase23_release.py --release phase22-release/phase22-result.json --output phase23-validation.json

CI validates synthetic contract fixtures only. It does not claim a real benchmark result.

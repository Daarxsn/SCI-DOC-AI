# Phase 31 — Failure Analysis & Error Taxonomy

Phase 31 converts an executed benchmark result into a structured failure-analysis report.

## Failure categories

- OCR
- TRANSLATION
- MATHEMATICS
- DIAGRAM
- LAYOUT
- VALIDATION
- RECONSTRUCTION
- PIPELINE

## What is classified

Phase 31 can identify:

- metric failures below their configured threshold;
- scientific validation failure;
- explicit pipeline-stage failure;
- blocked execution, without falsely attributing a scientific failure.

Each issue contains a stable code, severity, category, message, and measured value/threshold when applicable.

## Accuracy rule

Phase 31 does not create new model accuracy. It only analyzes an existing Phase 30 benchmark result. A blocked/non-executed run cannot be treated as a scientific failure analysis.

## Run

    python scripts/run_phase31_failure_analysis.py --result phase30-result/benchmark-result.json --output phase31-failure-analysis.json

CI uses synthetic benchmark payloads only. They are mechanics tests and are not scientific performance evidence.

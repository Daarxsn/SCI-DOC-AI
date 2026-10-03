# Phase 32 — Model Optimization & Routing

Phase 32 introduces the model-optimization control layer.

## Scope

- benchmark-driven optimization recommendations;
- task-specific primary/fallback model routes;
- confidence floors;
- explicit runtime profiles;
- fail-closed behavior when no executed benchmark exists.

Supported optimization areas:

- OCR;
- translation;
- mathematics/equations;
- diagrams;
- reconstruction.

## Important evidence rule

Phase 32 does not claim that a model was improved merely because an optimization plan was generated. A recommendation becomes an actual optimization only after the selected provider/configuration is executed and re-measured against the benchmark.

No fine-tuning or model-quality claim is made by this phase.

## Run

    python scripts/run_phase32_optimization.py --result phase30-result/benchmark-result.json --output phase32-optimization.json

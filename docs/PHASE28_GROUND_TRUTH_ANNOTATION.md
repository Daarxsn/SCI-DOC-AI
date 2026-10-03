# Phase 28 — Ground Truth & Annotation

Phase 28 establishes the verified reference layer required before scientific benchmarking.

## Required evidence per case

- source document from Phase 27;
- verified OCR/text reference;
- verified equations where applicable;
- verified diagram and layout annotations;
- matching case IDs;
- SHA-256 hashes for source, reference and annotation assets.

## Fail-closed rules

A case is rejected when the Phase 27 intake is not validated, assets are missing, case IDs mismatch, or reference/annotation verification is not explicit.

Phase 28 records GROUND_TRUTH_VERIFIED, but makes no scientific accuracy claim. Verification means the supplied ground truth was explicitly marked and structurally validated.

Run:

    python scripts/run_phase28_ground_truth.py --intake phase27-intake.json --root . --output phase28-ground-truth.json

CI fixtures are synthetic mechanics tests only and are never scientific benchmark evidence.

# Phase 30 — Real Benchmark v1

Phase 30 is the execution gate for the first measured scientific-document benchmark.

## Readiness
Exactly one case must originate from Phase 27, be marked REAL_DOCUMENT_VERIFIED, have Phase 28 GROUND_TRUTH_VERIFIED status, Phase 29 BENCHMARK_ELIGIBLE status, and contain verified source/reference/annotation assets. The reference must contain ocr_text and translation_text.

## Execution
Phase 30 builds a compatible benchmark manifest and invokes the existing Phase 19 ScientificDocumentPipeline. The measured result records OCR CER-score, translation Token-F1, validation state, model configuration, hashes and reconstruction metadata.

## Accuracy rule
accuracy_claim=true is emitted only after the real pipeline executes successfully against the verified case. CI fixtures test readiness only and are never scientific accuracy evidence.

Run:
    python scripts/run_phase30_benchmark.py --intake phase27-intake.json --ground-truth phase28-ground-truth.json --eligibility phase29-benchmark-eligibility.json --root . --output-dir phase30-result

A blocked result is expected until a real scientific document and verified measured reference are supplied.

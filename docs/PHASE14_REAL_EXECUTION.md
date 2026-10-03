# Phase 14 — Real Dataset Ingestion + Actual Model Benchmark Execution

Phase 14 adds the executable benchmark path. It invokes the real ScientificDocumentPipeline and computes metrics from actual model output.

Each manifest case requires an input document and an authorized reference JSON containing ocr_text and translation_text. Optional SHA-256 checksums are supported.

Run on the ML staging host:
python scripts/run_phase14_real_benchmark.py --manifest datasets/golden/phase13-manifest.example.json --root . --output phase14-results.json

The runner verifies assets and checksums, verifies ML dependencies, runs the real pipeline, extracts OCR and translation text from the UDR, computes OCR CER-derived score and translation token F1, and records validation and model configuration.

accuracy_claim=true is emitted only after actual case execution. Missing assets, missing model dependencies, or failed execution stop the benchmark.

CI validates only the execution contract; it does not manufacture benchmark scores.

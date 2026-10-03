# Phase 19 — First Real Benchmark Result

Phase 19 is the first result-producing execution boundary. A verified single golden case is processed through the real ScientificDocumentPipeline with reconstruction requested.

The result records OCR CER-derived score, translation token F1, overall score/pass state, pipeline stage status, validation outcome, model configuration, source/reference/annotation SHA-256 values, and reconstruction artifact metadata.

Run on the ML staging host:
`python scripts/run_phase19_benchmark.py --manifest datasets/golden/phase17-first-case.manifest.json --root . --output-dir phase19-result`

No score is generated when required assets, ground truth, annotations, checksums, or model dependencies are missing. CI tests the fail-closed contract only.

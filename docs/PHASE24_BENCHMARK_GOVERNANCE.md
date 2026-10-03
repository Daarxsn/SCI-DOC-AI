# Phase 24 — Benchmark Governance & Dataset Readiness

Phase 24 establishes the governance gate before a scientific benchmark dataset can be treated as executable.

Required controls: dataset ID/version, source asset, human-verified reference, human-verified annotation, SHA-256 verification, per-case readiness, and explicit benchmark eligibility.

The readiness report does not create benchmark scores; it establishes whether the registered dataset is sufficiently controlled for execution.

Run:
python scripts/check_phase24_readiness.py --manifest datasets/golden/phase17-first-case.manifest.json --root . --output phase24-readiness.json

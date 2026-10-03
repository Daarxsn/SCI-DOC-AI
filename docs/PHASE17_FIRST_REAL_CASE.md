# Phase 17 — First Real Golden Case

## Acceptance target
The first case is one real, authorized scientific document, initially intended to be Mathematics → Hindi unless another domain/language is selected.

## Required evidence
- original PDF/PNG/JPG/JPEG;
- SHA-256 checksum;
- human-verified English OCR transcription;
- human-verified Hindi/Marathi translation;
- structured annotations for equations, diagrams, tables and layout where present;
- explicit VERIFIED status.

## Gate
`verify_phase17_first_case.py` rejects the case unless the source exists, metadata is valid, the case is marked VERIFIED, benchmark_ready is true, and the recorded SHA-256 matches the source.

## Current status
The available uploaded file for this phase is a GitHub CI screenshot, not a scientific document, so it is not registered as a benchmark case. No benchmark score is generated from it.

## Completion criterion
After a real authorized scientific document is supplied and ground truth is verified, the case can be registered, passed through Phase 14 execution, and produce the first genuine measured benchmark result.

# Phase 22 — Real Document Execution & Evidence Package

Phase 22 is the end-to-end execution wrapper for the first real scientific document.

## Flow

1. Phase 20 validates that exactly one case has a real source asset, verified reference and verified annotation.
2. Phase 20 executes the real pipeline and writes the benchmark result.
3. Phase 21 packages that executed result into an auditable evidence bundle.
4. Phase 22 writes a single release-level `phase22-result.json`.

## Fail-closed behavior

If the source document, ground truth, annotation, or checksum is unavailable/invalid, Phase 22 returns `BLOCKED` with `accuracy_claim=false`. It never turns CI fixtures or screenshots into benchmark evidence.

## Run

```bash
python scripts/run_phase22.py \
  --manifest datasets/golden/phase17-first-case.manifest.json \
  --root . \
  --output-dir phase22-release
```

## Successful release evidence

A successful execution contains:
- measured benchmark metrics;
- validation state;
- reconstruction evidence;
- source/reference/annotation checksums;
- benchmark summary;
- evidence manifest;
- phase22-result.json.

The repository CI validates the orchestration contract only. A real scientific result requires the authorized document and verified ground truth on the ML execution host.

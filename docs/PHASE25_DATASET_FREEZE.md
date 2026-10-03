# Phase 25 — Dataset Lock, Benchmark Freeze & Reproducibility

Phase 25 creates a reproducibility freeze for a benchmark dataset.

## Freeze records

- dataset ID and version;
- ordered case IDs;
- canonical manifest SHA-256;
- execution environment metadata;
- combined freeze fingerprint.

## Reproducibility

A frozen dataset is valid only while the dataset ID, version and canonical manifest fingerprint match the original freeze.

Changing the manifest version or case definition invalidates the freeze and requires a new benchmark freeze.

## Run

python scripts/freeze_phase25_dataset.py --manifest datasets/golden/phase17-first-case.manifest.json --root . --output phase25-freeze.json --environment-json '{"python":"3.12"}'

Verify:

python scripts/verify_phase25_freeze.py --freeze phase25-freeze.json --manifest datasets/golden/phase17-first-case.manifest.json --root .

A freeze does not claim scientific accuracy; it establishes reproducibility metadata.

# Phase 20 — First Real Scientific Document + Measured Result

Phase 20 is the final execution gate for the first measured SCI-DOC AI result.

## Readiness
Exactly one case must be registered. Its source asset, reference JSON and annotation JSON must exist. Reference and annotation must both be VERIFIED. A registered source checksum must match the asset.

## Execution
When ready, Phase 20 invokes the Phase 19 benchmark pipeline. The result contains measured OCR/translation metrics, validation state, model configuration and reconstruction evidence.

## Fail-closed rule
If the scientific document or ground truth is unavailable, Phase 20 returns BLOCKED and accuracy_claim=false. CI fixtures never produce a scientific accuracy claim.

## Current repository state
The available conversation files are screenshots and repository artifacts, not a verified scientific benchmark document. Therefore the current Phase 20 execution state is expected to remain BLOCKED until an authorized scientific document is supplied and annotated.

## Run
python scripts/run_phase20.py --manifest datasets/golden/phase17-first-case.manifest.json --root . --output-dir phase20-result

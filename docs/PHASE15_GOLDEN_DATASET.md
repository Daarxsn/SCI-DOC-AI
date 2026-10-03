# Phase 15 — Golden Dataset Creation & Ground-Truth Annotation

Phase 15 defines the controlled golden-dataset contract for genuine SCI-DOC AI evaluation.

## Matrix
Six initial test cases cover Mathematics, Physics and Biology, each English to Hindi and English to Marathi.

## Ground truth
Each case has a source asset, trusted reference JSON, and structured annotation JSON. Annotation covers text, equations, diagrams, tables and layout geometry.

## Integrity
When an asset is available, its SHA-256 checksum is recorded. Missing externally mounted assets are not benchmark-ready until supplied and checked.

## Governance
Do not commit confidential client documents or copyrighted examination papers without redistribution rights. Restricted assets should remain in controlled storage.

## Release rule
A dataset version is benchmark-ready only when every case has an accessible source asset, matching checksum, reference JSON, annotation JSON, and verified schema.

CI passing this contract does not constitute a model accuracy claim.

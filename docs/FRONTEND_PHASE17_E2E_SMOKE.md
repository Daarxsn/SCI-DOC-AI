# Phase 17 — Local E2E Smoke Verification

Run from the repository root while the backend is running:

`SCI_DOC_API_KEY='<local-key>' ./scripts/phase17-smoke.sh`

The smoke test verifies health, readiness, upload acceptance and backend document ID generation, authenticated job creation, and results retrieval.

It deliberately does not claim OCR, translation, equation, diagram, or reconstruction quality because the current backend job queue does not execute those scientific processing stages.

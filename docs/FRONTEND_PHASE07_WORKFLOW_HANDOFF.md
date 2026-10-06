# Frontend Phase 7 — Workflow Handoff

## Objective
Connect the existing document, job, and results routes into a coherent frontend workflow while preserving current backend contract boundaries.

## Scope
- Deep-linkable `/jobs/{job_id}` route.
- Load an existing job from the real jobs API.
- Preserve the document ID locally when a job is created.
- Provide a direct handoff from a job to its document-results workspace.
- Preserve explicit API-contract limitations.

## Contract boundary
The current job responses do not contain `document_id`. F07 therefore stores the user-supplied document ID locally, keyed by the backend-generated job ID. It does not infer or fabricate document IDs.

## Acceptance criteria
1. Existing job IDs can be opened directly.
2. Job state is loaded from the backend.
3. Created jobs retain their supplied document ID locally.
4. A job can navigate to its document results when that ID is known.
5. Existing polling and terminal-state handling remain intact.
6. No backend behavior is fabricated.
7. Production build passes in CI.

## Evidence boundary
Passing F07 proves frontend workflow/navigation integration. It does not prove backend processing completion, OCR/translation quality, or scientific reconstruction correctness.

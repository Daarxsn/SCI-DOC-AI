# Frontend Phase 9 — Artifact Review Controls

## Objective
Make the existing artifact metadata collection easier to inspect at document-review scale without changing backend semantics.

## Scope
- Search artifacts by ID, format, path, or checksum.
- Filter by backend-supplied format values.
- Sort by API order, size, or format.
- Preserve read-only artifact provenance.
- Explicit no-match state.

## Contract boundary
F09 operates only on the `artifacts[]` metadata already returned by `GET /v1/documents/{document_id}/results`. It does not fetch, mutate, download, or reinterpret artifact contents.

## Acceptance criteria
1. Search is client-side over real artifact metadata.
2. Format filters are derived from backend responses.
3. Sorting uses backend-supplied fields only.
4. No-match state is explicit.
5. Existing provenance/integrity presentation remains intact.
6. Production build passes in CI.

## Evidence boundary
Passing F09 proves review controls over artifact metadata. It does not prove scientific artifact contents, OCR/translation quality, or reconstruction fidelity.

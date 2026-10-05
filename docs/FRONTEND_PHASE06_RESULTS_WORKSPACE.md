# Frontend Phase 6 — Results & Document Workspace

## Objective
Expose the existing document-results contract through the document workspace without inventing scientific artifact semantics.

## Scope
- Real `GET /v1/documents/{document_id}/results`.
- Typed result response.
- Loading, empty, refresh, and API error states.
- Result status and artifact count.
- Safe structured artifact inspection.
- Explicit API-key/scope guidance on authorization failures.

## Contract boundary
The backend currently returns opaque artifact objects. F06 renders those objects as structured JSON and does not label them as OCR, translation, validation, diagram, or reconstructed output unless the backend supplies that semantics.

## F06 acceptance criteria
1. Document workspace calls the real results endpoint.
2. Results status and artifact count are backend-derived.
3. Empty results are handled explicitly.
4. Artifact objects are inspectable without data fabrication.
5. Authorization/API failures are visible.
6. F01–F05 architecture remains intact.
7. Production build passes in CI.

## Evidence boundary
Passing F06 proves frontend results-contract integration and workspace behavior. It does not prove scientific artifact quality, OCR/translation correctness, or reconstruction fidelity.

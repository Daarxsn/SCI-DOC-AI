# Frontend Phase 3 — API Integration & Runtime State

## Objective
Connect the Phase 1/2 frontend foundation to the existing SCI-DOC AI backend contracts using a typed, centralized API client.

## Integrated backend contracts
- `GET /health`
- `GET /ready`
- `GET /runtime`
- `POST /api/v1/documents/upload`
- `POST /v1/jobs`
- `GET /v1/jobs/{job_id}`
- `GET /v1/documents/{document_id}/results`

No new backend endpoints are introduced.

## Client capabilities
- Environment-configurable API base URL.
- Optional `VITE_API_KEY` for protected job/result endpoints.
- Typed request/response models for current contracts.
- Multipart document upload support.
- Job creation and status retrieval.
- Result retrieval.
- Normalized `ApiError` with HTTP status.
- Safe API error parsing.
- Dashboard health/readiness status surface.

## F03 acceptance criteria
1. Existing Phase 1 API boundary is expanded into typed real backend contracts.
2. Document upload is supported with multipart FormData.
3. Protected jobs/results calls can send the configured API key.
4. API failures become typed `ApiError` instances with status codes.
5. Dashboard reads actual health/readiness endpoints.
6. No backend endpoint is mocked or invented.
7. Existing F01/F02 routes and UI primitives remain intact.
8. Production build passes in CI.

## Evidence boundary
Passing F03 proves frontend-to-backend contract integration and build correctness. It does not prove successful OCR, translation, validation, reconstruction, authentication, or production deployment.

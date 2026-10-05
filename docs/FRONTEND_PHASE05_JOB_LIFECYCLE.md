# Frontend Phase 5 — Job Lifecycle

## Objective
Expose the existing SCI-DOC AI job contract as a usable frontend workflow for creating and monitoring processing jobs.

## Scope
- Job creation through `POST /v1/jobs`.
- Real job ID returned by the backend.
- Status retrieval through `GET /v1/jobs/{job_id}`.
- Progress and stage presentation.
- Active-job polling at a 2-second interval.
- Terminal handling for `completed` and `failed`.
- Backend error presentation.
- Existing API-key authentication boundary is reused.

## Important contract boundary
The current upload endpoint does not return a document ID. F05 therefore does not automatically chain upload → job creation and does not fabricate a document identifier.

## F05 acceptance criteria
1. Jobs route is available in the frontend.
2. Job creation uses the existing typed API client.
3. Returned job ID/status/progress/stage are rendered from backend data.
4. Active jobs are refreshed through the real GET job endpoint.
5. Failed jobs surface backend error details.
6. No job or document state is mocked.
7. F01–F04 architecture remains intact.
8. Production build passes in CI.

## Evidence boundary
Passing F05 proves frontend job-lifecycle integration and build correctness. It does not prove actual OCR/translation execution quality, persistence, reconstruction, or production deployment.

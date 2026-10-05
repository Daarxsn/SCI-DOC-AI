# Frontend Phase 1 — Architecture

## Objective
Establish the production frontend foundation for SCI-DOC AI without changing the existing backend architecture.

## Decisions
- Frontend: React 19 + TypeScript + Vite.
- Routing: React Router.
- API boundary: typed fetch wrapper using `VITE_API_BASE_URL`.
- Backend remains the source of truth for document, job, result, runtime, and readiness contracts.
- Frontend is isolated under `frontend/`.
- No backend API is mocked as a substitute for integration.

## Initial routes
- `/dashboard`
- `/documents`
- `/documents/:documentId`
- `/settings`

## F01 acceptance criteria
1. Frontend source exists independently under `frontend/`.
2. TypeScript is strict.
3. Vite production build is defined.
4. Application routing is established.
5. API base URL is environment-configurable.
6. The initial application shell renders without requiring backend data.
7. CI runs the frontend production build.

## Evidence boundary
Passing this phase proves the frontend architecture and build contract. It does not prove document translation, OCR, validation, reconstruction, authentication, or production deployment. Those belong to later frontend phases.

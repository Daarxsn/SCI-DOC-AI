# Frontend Phase 4 — Document Intake

## Objective
Deliver the first real document interaction: validated file selection and upload through the existing SCI-DOC AI ingestion contract.

## Scope
- File selection for PDF, PNG, JPEG, TIFF, and WebP.
- Client-side 50 MB guard.
- Real multipart upload to `POST /api/v1/documents/upload`.
- Upload loading state and API error presentation.
- Backend-returned inspection metadata and page information.
- Explicit handling that the current upload contract does not return a document ID.

## F04 acceptance criteria
1. Documents route contains a real upload workflow.
2. Upload uses the existing typed API client.
3. Unsupported files are rejected before network submission.
4. Upload/API failures are visible and recoverable.
5. Backend-returned metadata is rendered without fabricated values.
6. No document ID is invented.
7. F01/F02/F03 architecture remains intact.
8. Production build passes in CI.

## Evidence boundary
Passing F04 proves document intake UX and integration with the current ingestion endpoint. It does not prove OCR quality, translation quality, job execution, persistence, or reconstructed output.

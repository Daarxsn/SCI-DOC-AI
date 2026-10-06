# Frontend Phase 8 — Artifact Provenance & Review

## Objective
Present the real backend artifact metadata in a structured, review-friendly document workspace.

## Scope
- Strongly typed artifact contract matching `backend/results/models.py`.
- Artifact ID, format, path, size, checksum, and document metadata.
- Read-only provenance presentation.
- Explicit checksum-present/absent state.
- Responsive artifact review layout.

## Contract boundary
The backend currently exposes artifact metadata only. F08 does not download, render, translate, validate, or reinterpret artifact contents.

## Acceptance criteria
1. Frontend artifact typing matches the backend result model.
2. Artifact provenance fields are displayed without fabrication.
3. Size is formatted from the backend value.
4. Checksum presence is explicitly represented.
5. Artifact metadata remains read-only.
6. Production build passes in CI.

## Evidence boundary
Passing F08 proves artifact metadata integration and review presentation. It does not prove artifact content correctness, OCR quality, translation quality, or reconstruction fidelity.

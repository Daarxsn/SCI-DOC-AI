# Human Review — M6

M6 provides the human-in-the-loop layer between automated translation/validation and final export.

## Review lifecycle

`PENDING → IN_REVIEW → APPROVED / REJECTED / SKIPPED`

## Review queue

Each item records:

- document and element ID;
- source and machine text;
- confidence;
- reason;
- scientific domain;
- target language;
- priority;
- reviewer assignment;
- timestamps;
- metadata.

## Reviewer actions

- **Accept** — approve machine output.
- **Edit** — replace machine output with reviewer text and approve.
- **Reject** — mark the translation/content as not approved.
- **Skip** — defer the item without approving it.

Every decision creates an immutable action record in the in-memory service history.

## Document integration

Approved review text can be applied back to the UDR. Unresolved review IDs are exposed so downstream export orchestration can require completion.

## UI contract

A frontend can build a review workspace from:

- review item list;
- item status and priority;
- source/machine/reviewed text;
- confidence and reason;
- reviewer assignment;
- action history;
- document-level counts.

## Safety

Human review does not bypass scientific validation. After approved edits are applied, the document should pass M5 again before export.

## M6 acceptance criteria

- [x] Review item model
- [x] Priority queue
- [x] Reviewer assignment
- [x] Accept/edit/reject/skip
- [x] Action audit trail
- [x] Document workspace
- [x] Apply approved edits to UDR
- [x] Unresolved review detection
- [x] Frontend-ready data contract

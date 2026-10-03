# P5 — Review Application

## Workflow

`AI output → validation → review queue → reviewer decision → apply approved edits → re-validation → export gate`

Phase 5 establishes one canonical workflow around the existing review primitives.

### Validation findings

Warnings, errors and critical findings that have an element ID become review items. The review item retains:

- source text;
- machine translation;
- confidence;
- validation stage/code;
- document/domain/language;
- reviewer assignment;
- action history.

### Reviewer actions

- **Accept** — accepts the machine output.
- **Edit** — stores reviewer text and applies it to the UDR.
- **Reject** — leaves the item unresolved and blocks export.
- **Skip** — explicitly resolves the item without changing its text.

### Re-validation

Approved/skipped review items are resolved first. The edited UDR is then passed through the complete unified validator again.

A review workflow can export only when:

- no review items remain unresolved; and
- the post-review validation report allows export.

### CI

Phase 5 has a dedicated GitHub Actions verification workflow covering review lifecycle, translation review, validation-to-review conversion, reviewer edits, re-validation and export gating.

## Current limitation

Review state is currently in-memory. Production deployment should persist reviews/actions in PostgreSQL or another transactional store and authenticate the reviewer through the enterprise identity provider.

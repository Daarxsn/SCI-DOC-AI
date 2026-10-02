# Scientific Validation — M5

M5 adds a cross-domain validation layer over the UDR after translation and before reconstruction.

## Validation areas

- document/language compatibility;
- question and subquestion integrity;
- duplicate question numbers;
- equation representation and LaTeX structure;
- diagram structural completeness;
- translation confidence and review state.

## Severity

- **critical** — structural/scientific integrity is unsafe; export is blocked.
- **error** — document integrity is invalid; export is blocked.
- **warning** — human review is required.
- **info** — informational diagnostic.

## Export policy

A document is exportable only when it has no critical/error issues and no warning-level review requirements.

This is intentionally conservative for scientific documents: a translated exam paper should not be released automatically when the system detects unresolved scientific or translation uncertainty.

## M5 foundation

The validator is domain-aware through the UDR element types and document domain. Specialized mathematics, physics, biology, terminology, and translation checks can be plugged into the same report.

The next M5 slices can add:
- equation semantic equivalence;
- diagram relationship integrity;
- translation source/target consistency;
- reconstruction-layout validation integration;
- validation provenance and model versions.

# Scientific Document Validation

Validation is the quality gate between processing/translation and reconstruction.

## Validation Categories

### Scientific

- equation representation exists;
- mathematics validation errors are absent;
- specialized scientific elements are not silently degraded.

### Structural

- question numbers are not duplicated;
- question numbering gaps are reported;
- required source text exists.

### Translation

- low-confidence translation is routed to review;
- specialized elements are not sent through generic translation.

### Confidence

Elements below the automatic acceptance threshold are flagged.

## Review Gate

A document can only be auto-exported when it has:

- zero critical issues;
- zero warnings requiring review.

The threshold and rules will become configurable after the golden evaluation dataset is established.

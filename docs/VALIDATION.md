# Scientific Validation — M5 Complete

M5 is the unified validation stage between translation and reconstruction/export.

## Layers
1. Scientific structure and question integrity.
2. Mathematical representation validation.
3. Diagram relationship integrity.
4. Translation consistency.
5. Provenance/model diagnostics.
6. Reconstruction layout validation.
7. Unified export decision.

## Severity
- critical/error: export blocked.
- warning: human review required.
- info: diagnostic only.

The export decision is true only when no blocking or review-required findings exist.

## Mathematical boundary
The current equivalence check is deliberately conservative: it normalizes whitespace, braces, and a small notation set. It does not claim algebraic equivalence, theorem proving, or CAS-level semantics.

## Provenance
Missing extractor/model provenance is surfaced rather than invented.

## Acceptance criteria
- [x] Cross-domain scientific validation
- [x] Mathematical representation validation
- [x] Diagram relationship integrity
- [x] Translation consistency
- [x] Provenance/model diagnostics
- [x] Reconstruction layout validation
- [x] Unified report
- [x] Explicit export decision
- [x] Complete-pipeline tests

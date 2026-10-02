# Evaluation & Benchmarking — M8

M8 makes SCI-DOC AI measurable against a reproducible golden dataset.

## Benchmark dimensions

### OCR
Character-level accuracy is represented through a CER-derived score.

### Translation
Token F1 provides a deterministic baseline metric. Production evaluation should additionally use human scientific adequacy/fluency review and terminology accuracy.

### Layout
Bounding-box IoU measures preservation of element geometry.

### Mathematics
Exact representation matching is available as a conservative baseline. This is not a substitute for symbolic mathematical equivalence.

### Diagrams
Diagram integrity is evaluated through structured relationship checks from M5. A future benchmark can add object detection precision/recall and label localization.

### Reconstruction
A reconstruction fidelity score can be supplied by visual/layout comparison against reference output.

## Golden dataset

Each benchmark case identifies:
- source document;
- domain;
- language pair;
- reference artifact;
- annotations.

Recommended initial dataset composition:
- English → Hindi;
- English → Marathi;
- Mathematics, Physics, Biology;
- clean scans, noisy scans, skewed pages, mixed text/equations, diagrams, tables.

## Regression gate

Default allowed metric degradation is 2 percentage points.

A model/pipeline change should not be accepted automatically when a tracked benchmark metric falls beyond its allowed regression.

## Benchmark reporting

Reports contain:
- benchmark ID;
- task;
- individual metrics;
- thresholds;
- sample counts;
- overall score;
- pass/fail;
- metadata/model versions.

## Important evaluation principle

Do not optimize only for generic translation metrics. SCI-DOC AI must evaluate scientific meaning, equation preservation, terminology consistency, diagram integrity, and document layout alongside language quality.

## M8 acceptance criteria

- [x] Golden dataset registry
- [x] OCR metric
- [x] Translation metric
- [x] Layout metric
- [x] Mathematics metric baseline
- [x] Diagram evaluation contract
- [x] Reconstruction evaluation contract
- [x] Unified benchmark report
- [x] Regression gate
- [x] Evaluation tests

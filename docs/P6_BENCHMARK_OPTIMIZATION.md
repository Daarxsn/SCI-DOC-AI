# P6 — Benchmark + Optimization

P6 turns evaluation into a repeatable optimization loop:

golden cases → batch benchmark → provider/model comparison → regression gate → optimization report.

## Capabilities
- batch text benchmarking with case IDs;
- provider/model candidate comparison;
- baseline regression checks;
- machine-readable optimization summaries;
- quality-gate status;
- geometry regression coverage for layout IoU.

## Quality gate
A run passes only when every candidate report passes its thresholds and every supplied baseline regression stays within the configured regression allowance.

The comparison report records the highest metric value for informational comparison; it does not make a global product-quality judgment.

## Runtime truth
P6 infrastructure does not claim model accuracy. Real scores require populated golden cases and actual model predictions.

Recommended benchmark partitions:
- English → Hindi;
- English → Marathi;
- mathematics;
- physics;
- biology;
- OCR/layout;
- equations;
- diagrams;
- reconstruction.

Reports should retain dataset version, provider/model version, configuration, and case IDs.

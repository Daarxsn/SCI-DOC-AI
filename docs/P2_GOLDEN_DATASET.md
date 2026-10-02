# P2 — Golden Dataset & Evaluation

## Status

P2 foundation is implementation-complete. Real benchmark execution remains pending until approved document assets and annotations are populated.

## What was added

- Versioned `DatasetManifest` and `BenchmarkCase` contracts.
- Dataset splits: train, validation, test.
- Supported initial domains: Mathematics, Physics, Biology.
- Supported language set: English, Hindi, Marathi.
- Annotation contract for text, layout, equations, diagrams, tables and document metadata.
- Dataset validator with duplicate/path/reference checks.
- Coverage summary by domain, language and split.
- SHA-256 helper for dataset asset integrity.
- Golden dataset directory and manifest.
- Explicit distinction between structural fixtures and real benchmark data.
- Benchmark metric naming clarified: `ocr_cer_score` is a higher-is-better 1-CER score.
- Length validation for prediction/reference pairs.
- Benchmark metadata remains available for model/provider/version provenance.

## Required annotation content

For each real case, annotate as applicable:

1. OCR source text.
2. Text/block bounding boxes.
3. Reading order.
4. Equation LaTeX and/or MathML.
5. Diagram objects.
6. Diagram labels.
7. Diagram relationships.
8. Table structure and cell content.
9. Hindi reference translation.
10. Marathi reference translation.
11. Reconstruction/layout reference.

## Recommended collection matrix

At minimum, build cases across:

- Mathematics × Hindi
- Mathematics × Marathi
- Physics × Hindi
- Physics × Marathi
- Biology × Hindi
- Biology × Marathi

Each language/domain combination should eventually include multiple document conditions rather than one representative page.

## Benchmark integrity rules

- Do not report benchmark scores from fixture metadata.
- Do not claim model accuracy until real assets and ground-truth annotations have been evaluated.
- Record dataset version, annotation version, model/provider versions and benchmark ID with each run.
- Keep confidential client documents outside the public repository unless redistribution rights are confirmed.
- Changes to annotations should increment the annotation/dataset version.

## Next phase

P3 will wire the real raw-document path through ingestion → preprocessing → OCR → UDR → scientific enrichment → translation → validation → reconstruction, then connect that output to this golden benchmark.

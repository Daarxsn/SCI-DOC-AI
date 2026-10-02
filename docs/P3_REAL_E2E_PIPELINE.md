# P3 — Real End-to-End Pipeline

## Pipeline

A real document can now enter the pipeline as one PDF/JPG/PNG file:

`source document → preprocessing → OCR → UDR → scientific enrichment → translation → validation → reconstruction`

The orchestrator is `ScientificDocumentPipeline`.

## Input handling

- PDF is rendered into page images by `PreprocessingService`.
- JPG/JPEG/PNG is normalized into a processed page artifact.
- OCR receives the processed page images.
- OCR output is converted into UDR.
- Mathematical and diagram enrichment runs against the page images.
- Translation operates on the UDR.
- Unified validation runs before export.
- Reconstruction is allowed only when validation permits export.

## Stage reporting

Every run returns `stage_status`:

- input
- preprocessing
- OCR
- UDR
- scientific enrichment
- translation
- validation
- reconstruction

This makes failures observable instead of treating the pipeline as a black box.

## Verification

P3 has lightweight orchestration tests and a GitHub Actions workflow. Heavy model accuracy is deliberately not asserted by these tests because PaddleOCR, NLLB, Pix2Tex and YOLO require model runtimes/weights.

Real AI verification will be performed after the ML runtime and approved golden documents are available.

## Current P3 status

**Implementation:** complete for the real document orchestration path.

**Heavy-model runtime verification:** pending.

**Scientific accuracy:** not claimed until real benchmark cases are executed.

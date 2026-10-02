# P1 — Real AI Model Integration

P1 moves SCI-DOC AI from development adapters toward real model-backed processing.

## Scope

- OCR: PaddleOCR for English scanned documents
- Translation: Meta NLLB-200 through Hugging Face Transformers
- Existing Tesseract and rule-based adapters remain available as development fallbacks
- Model selection is configuration-driven

## Flow

Document -> Preprocessing -> OCR -> UDR -> Translation -> Validation

## Configuration

    OCR_PROVIDER=paddleocr
    OCR_LANGUAGE=en
    TRANSLATION_PROVIDER=huggingface-nllb
    TRANSLATION_MODEL=facebook/nllb-200-distilled-600M

Model files are downloaded on first use unless deployment uses a local model cache.

## Confidence

NLLB does not expose a calibrated document-level translation confidence score.
The adapter therefore returns a conservative provisional confidence of 0.75 for
non-empty translations. This is not an accuracy claim. P2/P6 will calibrate
confidence against the SCI-DOC AI golden dataset.

## P1 execution checklist

- Install model runtimes in a controlled environment.
- Run Tesseract and PaddleOCR on representative question-paper pages.
- Compare OCR CER, reading order, equation retention, table handling and latency.
- Run English -> Hindi and English -> Marathi samples.
- Add scientific terminology and domain-specific evaluation cases.
- Select the production OCR/model combination using measured results.

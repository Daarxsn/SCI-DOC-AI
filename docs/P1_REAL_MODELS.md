# P1 — Real AI Model Integration

P1 moves SCI-DOC AI from development adapters toward real model-backed processing.

## Scope
- OCR: PaddleOCR for English scanned documents
- Translation: Meta NLLB-200 through Hugging Face Transformers
- Existing Tesseract and rule-based adapters remain available as development fallbacks
- Model selection is configuration-driven

## Flow
Document -> Preprocessing -> OCR -> UDR -> Translation -> Validation

## ML environment

The core backend/requirements.txt intentionally contains only the lightweight runtime dependencies. P1 model dependencies are isolated in requirements-p1.txt:

- PaddleOCR
- PyTorch
- Hugging Face Transformers
- SentencePiece

Install the P1 environment separately:

    pip install -r requirements.txt
    pip install -r requirements-p1.txt

For CPU-only development, use the PyTorch wheel appropriate to the installed Python version and operating system. For NVIDIA GPU deployments, install the PyTorch build matching the host CUDA runtime instead of assuming a universal CUDA wheel.

SCI-DOC AI does not require the optional ML packages merely to start the lightweight API or use the existing Tesseract/rule-based development adapters.

## Runtime diagnostics

backend/core/ml_runtime.py provides a lightweight package-availability check. It does not download models or perform heavyweight imports. This makes it safe for startup diagnostics and CI environments.

## Configuration
    OCR_PROVIDER=paddleocr
    OCR_LANGUAGE=en
    TRANSLATION_PROVIDER=huggingface-nllb
    TRANSLATION_MODEL=facebook/nllb-200-distilled-600M

Model files are downloaded on first use unless deployment uses a local model cache.

## Model-cache guidance

For repeatable development and production deployments, configure a persistent Hugging Face/model cache rather than downloading model weights on every container start. Production deployments should pin model revisions and record the selected revision in model provenance.

## Confidence

NLLB does not expose a calibrated document-level translation confidence score. The adapter therefore returns a conservative provisional confidence of 0.75 for non-empty translations. This is not an accuracy claim. P2/P6 will calibrate confidence against the SCI-DOC AI golden dataset.

## P1 execution checklist
- [x] Add isolated ML dependency manifest.
- [x] Add lightweight ML runtime diagnostics.
- [ ] Install and verify ML packages in the target environment.
- [ ] Verify PaddleOCR model loading.
- [ ] Verify NLLB model/tokenizer loading.
- [ ] Run Tesseract and PaddleOCR on representative question-paper pages.
- [ ] Compare OCR CER, reading order, equation retention, table handling and latency.
- [ ] Run English -> Hindi and English -> Marathi samples.
- [ ] Add scientific terminology and domain-specific evaluation cases.
- [ ] Select the production OCR/model combination using measured results.

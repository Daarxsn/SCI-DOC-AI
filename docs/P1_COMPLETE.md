# P1 — Real AI Model Integration

P1 now contains the model-provider architecture and an end-to-end orchestration path.

## Implemented

- Optional ML manifest: PaddlePaddle, PaddleOCR, PyTorch, Transformers, SentencePiece, Ultralytics, Pix2Tex.
- Runtime package detection and CPU/CUDA device selection.
- Tesseract and PaddleOCR OCR providers.
- Hugging Face NLLB-200 for English, Hindi and Marathi.
- Scientific terminology for Mathematics, Physics and Biology.
- Human-review routing for low-confidence translations.
- Optional Pix2Tex image-to-LaTeX equation recognition.
- Optional Ultralytics/YOLO scientific diagram detection.
- UDR enrichment for equations and diagrams.
- End-to-end scanned-page -> preprocessing -> OCR -> UDR -> scientific enrichment -> translation -> validation -> reconstruction pipeline.

## Example real-model configuration

    OCR_PROVIDER=paddleocr
    OCR_LANGUAGE=en
    TRANSLATION_PROVIDER=huggingface-nllb
    TRANSLATION_MODEL=facebook/nllb-200-distilled-600M
    EQUATION_PROVIDER=pix2tex
    DIAGRAM_PROVIDER=ultralytics
    DIAGRAM_MODEL=/models/scientific-diagram.pt
    ML_DEVICE=auto

## Verification status

The repository architecture and adapters are implemented, but the current development environment does not have PaddleOCR/PaddlePaddle or Transformers installed and cannot download their model weights. No real OCR or translation accuracy numbers are being claimed.

Runtime verification requires installing requirements-p1.txt, loading the configured models, and running representative Mathematics, Physics and Biology pages against a verified golden dataset. Final provider selection must use measured OCR CER, reading order, translation quality, equation accuracy, diagram integrity and reconstruction fidelity.

**P1 status: implementation-complete; real-model runtime verification pending.**
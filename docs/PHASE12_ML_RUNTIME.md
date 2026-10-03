# Phase 12 — Real AI Model Runtime

SCI-DOC AI now has a dedicated runtime boundary for its real ML providers.

Providers:
- OCR: PaddleOCR + PaddlePaddle
- Translation: Hugging Face NLLB, default model facebook/nllb-200-distilled-600M
- Equations: pix2tex / LatexOCR
- Diagrams: Ultralytics with a supplied trained model

The existing factories and adapters remain the model integration boundary. The new registry reports configured providers and dependency availability without downloading model weights.

Lightweight API mode remains the default with ML_RUNTIME_ENABLED=false and ML_PRELOAD=false.

ML mode uses Dockerfile.ml and docker-compose.ml.yml. Model weights are lazy-loaded by adapters and cached under /model-cache.

GET /runtime reports providers, model names, dependency readiness, device, cache directory, and preload configuration.

The Phase 12 CI gate validates the runtime contract and ML Compose configuration without downloading multi-gigabyte model weights. Actual model-weight activation is a staging-host operation and must be followed by representative benchmark measurements; this phase makes no accuracy or client-performance claim.

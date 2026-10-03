# Phase 13 — Real Model Activation & First Scientific Benchmark

## Goal
Move from model-runtime infrastructure to controlled activation of real model weights and reproducible benchmarking on authorized scientific-document assets.

## Activation
Run on the staging ML host with the desired provider configured:
python scripts/activate_phase13_models.py --model ocr
python scripts/activate_phase13_models.py --model translation
python scripts/activate_phase13_models.py --model equation
python scripts/activate_phase13_models.py --model diagram

Activation can download or load model weights. Diagram activation requires DIAGRAM_MODEL to point to a trained model.

## Benchmark
The example manifest covers Mathematics, Physics and Biology, each with English to Hindi and English to Marathi cases.

Run:
python scripts/run_phase13_benchmark.py --manifest datasets/golden/phase13-manifest.example.json --root . --output phase13-report.json

The runner validates input existence and optional SHA-256 checksums, then records runtime configuration and a deterministic provenance fingerprint.

## Acceptance gates
- Real provider activation is explicit and model-specific.
- Heavy model downloads do not run in ordinary CI.
- Every benchmark case has an auditable identity and input checksum when assets are finalized.
- Runtime configuration and model identifiers are fingerprinted.
- Missing assets block execution instead of producing fake scores.
- No accuracy or client-performance claim is made without real benchmark execution.

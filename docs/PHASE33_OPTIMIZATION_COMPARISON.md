# Phase 33 — Optimization Experiment & Regression Comparison

Phase 33 validates whether a Phase 32 optimization candidate actually improves measured benchmark performance.

## Gate

Two executed benchmark results are required:

1. baseline configuration;
2. candidate optimized configuration.

Each common metric is compared as candidate minus baseline.

A candidate is accepted only when at least one metric improves and no comparable metric regresses.

## Evidence

The comparison records:
- baseline and candidate metric values;
- per-metric deltas;
- improvement/regression counts;
- deterministic fingerprints of both benchmark result files.

Phase 33 does not create a new scientific accuracy claim. It establishes whether an optimization candidate is supported by measured benchmark evidence.

CI uses synthetic benchmark payloads only.

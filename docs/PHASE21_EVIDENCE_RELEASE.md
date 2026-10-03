# Phase 21 — Benchmark Evidence & Release Packaging

Phase 21 packages a completed real benchmark execution into an auditable evidence bundle.

## Required input

The input must be a Phase 19/20 benchmark result with:
- execution_status = EXECUTED;
- accuracy_claim = true;
- at least one measured metric.

Blocked runs and CI fixture outputs cannot be packaged as scientific results.

## Output

The package contains:
- benchmark-summary.json;
- evidence-manifest.json;
- SHA-256 hashes for the source result and generated evidence.

The summary preserves benchmark ID, task, overall score, pass state, metrics and execution metadata.

## Run

```bash
python scripts/package_phase21_result.py \
  --result phase20-result/benchmark-result.json \
  --output-dir phase21-release
```

Phase 21 creates no benchmark data by itself. It only packages evidence from a genuine executed run.

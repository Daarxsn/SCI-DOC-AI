# Phase 18 — First Actual Scientific Document Processing

Phase 18 is the execution boundary between the verified golden case and the real SCI-DOC AI pipeline.

## Execution contract

Exactly one verified case is accepted. The runner requires:
- source PDF/PNG/JPG/JPEG;
- matching source checksum;
- reference JSON;
- structured annotation JSON.

It then invokes the existing real `ScientificDocumentPipeline` through the Phase 14 benchmark path and writes an auditable evidence bundle containing source/reference/annotation checksums, stage status, model configuration and measured metrics.

## Run

```bash
python scripts/run_phase18_case.py \
  --manifest datasets/golden/phase17-first-case.manifest.json \
  --root . \
  --output-dir phase18-evidence
```

Real model weights and authorized benchmark assets must be available on the ML staging host. CI only verifies the execution gate; it does not create scientific benchmark scores.

## Completion

Phase 18 is considered data-complete only when a real verified scientific case has been executed successfully. Repository code completion alone does not constitute a scientific accuracy result.

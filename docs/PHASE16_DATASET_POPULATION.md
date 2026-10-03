# Phase 16 — Real Dataset Population & Human Ground Truth

## Workflow

1. Obtain an authorized scientific source document.
2. Register it with `scripts/intake_phase16_case.py`.
3. Human-verify the complete English transcription.
4. Human-verify the Hindi or Marathi translation reference.
5. Annotate page geometry and scientific structures.
6. Mark both reference and annotation artifacts `ground_truth_status: VERIFIED`.
7. Validate the case.
8. Record the source SHA-256 in the manifest.
9. Run the dataset readiness report.
10. Only a fully verified dataset proceeds to Phase 14 real benchmarking.

## Intake

```bash
python scripts/intake_phase16_case.py --source /controlled/document.png --case-id physics-hi-001 --domain physics --target-language hi
```

The intake command copies the authorized asset into controlled dataset storage and creates pending reference/annotation files. It does not mark them verified.

## Case verification

```bash
python scripts/validate_phase16_case.py --reference datasets/golden/references/physics-hi-001.json --annotation datasets/golden/annotations/physics-hi-001.json
```

Verification requires non-empty human ground truth, schema-valid annotations, matching case IDs, and explicit VERIFIED status.

## Readiness

```bash
python scripts/verify_phase16_dataset.py
```

Missing or pending cases are reported as pending. No accuracy score is generated.

## Governance

Only use documents for which the team has permission to store and evaluate the source material. Keep confidential/copyright-restricted assets in controlled storage when repository redistribution is not authorized.

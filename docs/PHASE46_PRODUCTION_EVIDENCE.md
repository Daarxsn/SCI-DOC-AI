# Phase 46 — Production Evidence & Customer Acceptance Readiness

Phase 46 defines the evidence package required after real deployment,
real-document execution, and customer/pilot acceptance activity.

## Required evidence

- deployment evidence;
- endpoint smoke evidence;
- real-document execution;
- benchmark evidence;
- security evidence;
- performance evidence;
- resilience evidence;
- artifact-integrity evidence;
- audit evidence;
- customer-acceptance evidence;
- support handoff evidence;
- rollback evidence.

The package also requires deployment ID, release version, evidence owner, and
customer/pilot identifier.

## Evidence boundary

The checked-in manifest is deliberately a synthetic fixture. A passing CI
workflow validates only the shape of the evidence contract.

It does **not** prove that a deployment exists, that a real scientific document
was processed, that benchmark targets were achieved, or that a customer
accepted the system.

The report therefore keeps:

- `deployment_claim=false`;
- `real_production_evidence_verified=false`;
- `customer_acceptance_verified=false`;
- `benchmark_result_verified=false`.

## Real evidence package

For an actual launch, replace the fixture with immutable evidence containing:

1. deployment/image digest and environment;
2. endpoint and smoke-test results;
3. source-document checksum;
4. UDR/pipeline execution identifiers;
5. measured OCR/translation/equation/diagram/layout results;
6. validation and reconstruction artifacts;
7. security-test output;
8. performance/load results;
9. resilience/rollback evidence;
10. audit trail;
11. customer/pilot acceptance record;
12. support handoff record.

## Run

    python scripts/check_phase46_production_evidence.py \
      --manifest datasets/golden/phase46-production-evidence-manifest.json \
      --output phase46-production-evidence-readiness.json

# Phase 45 — Production Go-Live Governance & Readiness

Phase 45 establishes a fail-closed launch gate for SCI-DOC AI. It consolidates
the operational evidence expected before an enterprise production release.

## Required controls

- approved release candidate;
- security, capacity, resilience, deployment, and observability gates;
- smoke-test plan;
- rollback plan;
- backup/restore plan;
- incident-response plan;
- named on-call ownership;
- support escalation path;
- data-retention policy;
- change-management record;
- explicit go-live approval.

The manifest also requires release version, deployment environment, release
commit, approver, and go-live window.

## Evidence boundary

A passing Phase 45 CI gate means the launch contract is complete and
mechanically validated. It does **not** mean SCI-DOC AI has been deployed to
production, that customers have accepted it, or that any compliance
certification has been obtained.

The report therefore keeps:

- `deployment_claim=false`;
- `live_production_verified=false`;
- `customer_acceptance_verified=false`;
- `compliance_certification_verified=false`.

The checked-in manifest is a synthetic engineering fixture and must be
replaced by real release evidence before an actual go-live decision.

## Recommended go-live sequence

1. Freeze the release commit and image digest.
2. Verify security, resilience, capacity, and deployment evidence.
3. Deploy to staging and execute smoke tests.
4. Restore a backup in a non-production environment.
5. Exercise rollback.
6. Confirm monitoring and on-call routing.
7. Obtain named go-live approval.
8. Promote the exact approved artifact.
9. Execute production smoke checks.
10. Record real production evidence and customer acceptance separately.

## Run

    python scripts/check_phase45_go_live.py \
      --manifest datasets/golden/phase45-go-live-manifest.json \
      --output phase45-go-live-readiness.json

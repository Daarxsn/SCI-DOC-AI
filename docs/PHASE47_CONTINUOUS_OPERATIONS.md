# Phase 47 — Continuous Operations & Service-Level Governance

Phase 47 establishes the operating model required after launch. It turns the
earlier readiness gates into recurring operational controls.

## Required controls

- SLO ownership and alerting;
- incident management and on-call;
- vulnerability remediation;
- dependency-update process;
- backup verification and restore drills;
- access and audit reviews;
- model-version review;
- benchmark regression review;
- capacity review;
- security review;
- evidence retention.

The manifest also requires an explicit service owner, incident channel, review
cadence, and escalation policy.

## Evidence boundary

A passing CI gate validates the operating-model contract. It does **not**
prove that alerts are firing in production, that incidents have been
exercised, that backups restore successfully, or that service-level targets
are being met.

The report therefore keeps:

- `deployment_claim=false`;
- `live_operations_verified=false`;
- `service_level_verified=false`.

The checked-in manifest is a synthetic engineering fixture.

## Operating cadence

At minimum, the live service should perform:

- continuous alert evaluation;
- incident/on-call coverage;
- weekly vulnerability/dependency review;
- monthly access, audit, capacity, security, and model review;
- scheduled restore drills;
- benchmark regression checks before model changes;
- evidence retention for operational decisions.

## Run

    python scripts/check_phase47_operations.py \
      --manifest datasets/golden/phase47-operations-manifest.json \
      --output phase47-operations-readiness.json

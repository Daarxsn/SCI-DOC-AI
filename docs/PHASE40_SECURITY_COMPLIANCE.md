# Phase 40 — Security & Compliance Hardening

Phase 40 establishes the security-control baseline required before handling
sensitive enterprise scientific documents in a production environment.

## Required controls

- authentication;
- least-privilege authorization;
- tenant isolation;
- TLS for data in transit;
- encryption at rest;
- secret management;
- upload validation;
- rate limiting;
- audit logging;
- sensitive-data redaction;
- explicit retention policy;
- dependency security scanning;
- software supply-chain integrity;
- incident-response readiness;
- security testing.

The manifest also requires explicit upload-size and retention limits.

## Evidence boundary

A passing Phase 40 CI gate proves that the security contract is represented
and mechanically validated. It does **not** prove penetration-test results,
cloud configuration security, encryption configuration in a live environment,
or compliance certification.

The report therefore keeps:

- `deployment_claim=false`;
- `compliance_claim=false`;
- `live_security_assessment_verified=false`.

The checked-in manifest is an engineering fixture, not evidence of GDPR,
ISO 27001, SOC 2, HIPAA, or any other regulatory/certification status.

## Operational requirements

Before a real enterprise deployment, the team should separately verify:
secret rotation, TLS certificates, KMS/key-management configuration, network
segmentation, durable audit storage, retention enforcement, vulnerability
scanning, dependency provenance, container/image scanning, backup security,
access reviews, incident-response exercises, and an independent security test.

## Run

    python scripts/check_phase40_security.py \
      --manifest datasets/golden/phase40-security-manifest.json \
      --output phase40-security-readiness.json

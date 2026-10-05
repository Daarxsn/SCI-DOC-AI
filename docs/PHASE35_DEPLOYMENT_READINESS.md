# Phase 35 — Production Deployment Readiness

Phase 35 establishes a fail-closed deployment-readiness gate for the production-candidate release.

## Required runtime controls

- API key configuration
- tenant isolation configuration
- TLS configuration
- durable storage configuration
- queue/worker configuration
- ML runtime/model configuration

## Release requirement

The release must identify a supported production-candidate or production channel.

## Evidence rule

A passing Phase 35 gate means the declared deployment controls are configured in the supplied runtime manifest. It does not prove that a live cloud deployment exists.

live_deployment_verified therefore remains false until an actual external deployment and smoke test are performed.

## Run

python scripts/check_phase35_deployment.py --release release-manifest.json --runtime runtime-manifest.json --output phase35-deployment-readiness.json

CI uses synthetic runtime manifests only and is not evidence of a live deployment.

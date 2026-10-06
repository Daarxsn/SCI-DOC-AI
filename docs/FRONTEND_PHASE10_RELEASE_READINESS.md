# Frontend Phase 10 — Production Release Readiness

## Objective
Make the frontend release candidate reproducible and explicitly verifiable without claiming a deployment has occurred.

## Scope
- Dedicated `verify:release` command.
- TypeScript + Vite production build as the release gate.
- Verification that the generated `dist/index.html` exists and is non-empty.
- Documented runtime environment configuration.
- Explicit distinction between build readiness and production deployment readiness.

## Release command
From `frontend/`:

```bash
npm install
npm run verify:release
```

The command runs the production build and verifies that the generated application entrypoint exists.

## Runtime configuration
The frontend supports:

- `VITE_API_BASE_URL` — backend API origin.
- `VITE_API_KEY` — optional protected API key for the current jobs/results boundary.

Secrets must not be committed to the repository.

## Acceptance criteria
1. `npm run build` passes.
2. `dist/index.html` is generated and non-empty.
3. Release verification is available as one command.
4. Environment configuration is documented.
5. No production deployment is claimed without deployment evidence.

## Evidence boundary
Passing F10 proves reproducible frontend release-build verification. It does not prove cloud deployment, TLS, CDN configuration, authentication infrastructure, backend production readiness, browser compatibility across every target, or scientific model quality.

# Frontend Phase 12 — Security Hardening

## Objective
Harden browser-side API behavior and make the frontend secret/configuration boundary explicit.

## Scope
- Validate `VITE_API_BASE_URL` as an HTTP(S) URL before use.
- Normalize the configured API origin.
- Use `cache: no-store` for API requests.
- Explicitly omit browser credentials/cookies from cross-origin API requests.
- Use `no-referrer` for API requests.
- Document that `VITE_*` variables are embedded into browser bundles.
- Prevent the README/example configuration from implying that `VITE_API_KEY` is a production secret.

## Security boundary
A Vite `VITE_*` variable is client-visible by design. Therefore `VITE_API_KEY` is suitable only for development or controlled environments where exposure is acceptable. Production authentication should use a server-side/proxy boundary or another mechanism that keeps credentials out of the browser bundle.

## Acceptance criteria
1. Invalid API base URLs fail early with an explicit configuration error.
2. API requests use no-store caching.
3. API requests omit ambient browser credentials.
4. API requests use a no-referrer policy.
5. Example configuration clearly warns against putting production secrets in `VITE_*` variables.
6. Production release verification passes in CI.

## Evidence boundary
Passing F12 proves browser-side request/configuration hardening. It does not prove complete application security, backend authorization, TLS configuration, secret management, CSP deployment, penetration-test results, or enterprise compliance.

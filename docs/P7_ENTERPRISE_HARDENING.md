# P7 — Enterprise Hardening

## Security boundary

API keys are mapped to an AuthPrincipal containing tenant ID, subject and scopes. Job creation no longer accepts tenant ID from the request body.

## Tenant isolation

Jobs are retrieved by job ID plus tenant ID. Idempotency lookup is tenant-scoped through the repository contract. Result artifacts are stored and listed by tenant ID plus document ID.

## Operational controls

- in-memory rate limiting by tenant/action;
- audit events for job creation and reads;
- explicit API scopes;
- structured authentication principal.

## Persistence boundary

Repositories remain in-memory implementations behind interfaces. Production deployment must provide transactional PostgreSQL/Redis/object-storage implementations rather than treating memory as durable enterprise storage.

## Acceptance criteria

- Client cannot choose job tenant
- Job idempotency is repository-scoped
- Artifact ownership is tenant-scoped
- API principal contains tenant and scopes
- Rate limiting boundary exists
- Audit-event boundary exists
- Dedicated CI verification
- Production persistence requirements documented

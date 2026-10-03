from backend.api.security import ApiKeyAuthenticator, authenticate_api_key
from backend.jobs.models import Job
from backend.jobs.storage import InMemoryJobRepository
from backend.results.models import ResultArtifact
from backend.results.storage import InMemoryArtifactStore
from backend.security.audit import AuditEvent, InMemoryAuditLog
from backend.security.principal import AuthPrincipal
from backend.security.rate_limit import InMemoryRateLimiter

def test_api_key_creates_tenant_bound_principal():
    principal = authenticate_api_key(
        "secret", ApiKeyAuthenticator(expected_key="secret", tenant_id="tenant-a", subject="svc")
    )
    assert principal == AuthPrincipal("tenant-a", "svc", frozenset({"documents:read", "documents:write", "jobs:read", "jobs:write"}))

def test_job_repository_is_tenant_scoped():
    repo = InMemoryJobRepository()
    repo.save(Job(job_id="j1", tenant_id="tenant-a", document_id="d1"))
    assert repo.get("j1", "tenant-a") is not None
    assert repo.get("j1", "tenant-b") is None

def test_artifact_store_is_tenant_scoped():
    store = InMemoryArtifactStore()
    store.put(ResultArtifact(tenant_id="tenant-a", document_id="d1", artifact_id="a1", format="pdf", path="/tmp/a", size_bytes=1))
    assert len(store.list("d1", "tenant-a")) == 1
    assert store.list("d1", "tenant-b") == []

def test_rate_limiter_blocks_after_limit():
    limiter = InMemoryRateLimiter(limit=2, window_seconds=60)
    assert limiter.allow("tenant-a")
    assert limiter.allow("tenant-a")
    assert not limiter.allow("tenant-a")

def test_audit_log_is_tenant_scoped():
    log = InMemoryAuditLog()
    log.record(AuditEvent("job.created", "tenant-a", "svc", "job", "j1"))
    log.record(AuditEvent("job.created", "tenant-b", "svc", "job", "j2"))
    assert [e.resource_id for e in log.for_tenant("tenant-a")] == ["j1"]
from backend.api.security import ApiKeyAuthenticator
from backend.core.tenant import TenantContext, TenantGuard
from backend.jobs.models import JobStatus
from backend.jobs.service import JobService

def test_api_key_authentication():
    auth=ApiKeyAuthenticator("secret")
    assert auth.authenticate("secret")
    assert not auth.authenticate("wrong")

def test_tenant_guard_blocks_cross_tenant_access():
    try: TenantGuard().require("tenant-a", TenantContext("tenant-b"))
    except PermissionError: pass
    else: raise AssertionError("Expected tenant boundary violation")

def test_job_is_tenant_scoped():
    service=JobService()
    job=service.create("tenant-a","doc-1","hi","biology")
    assert service.get(job.job_id,"tenant-a").status == JobStatus.QUEUED
    assert service.get(job.job_id,"tenant-b") is None

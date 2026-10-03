from fastapi import APIRouter, Header, HTTPException
from backend.api.security import authenticate_api_key
from backend.jobs.models import JobCreateRequest, JobStatusResponse
from backend.jobs.service import JobService
from backend.security.audit import AuditEvent, InMemoryAuditLog
from backend.security.rate_limit import InMemoryRateLimiter

router=APIRouter(prefix="/v1/jobs",tags=["jobs"])
job_service=JobService(); audit_log=InMemoryAuditLog(); rate_limiter=InMemoryRateLimiter()

def _principal(key):
    try: return authenticate_api_key(key)
    except PermissionError as exc: raise HTTPException(status_code=401,detail=str(exc))

@router.post("",response_model=JobStatusResponse,status_code=202)
def create_job(request:JobCreateRequest,x_api_key:str|None=Header(default=None)):
    principal=_principal(x_api_key)
    if not principal.allows("jobs:write"): raise HTTPException(status_code=403,detail="Insufficient scope")
    if not rate_limiter.allow(f"{principal.tenant_id}:jobs:create"): raise HTTPException(status_code=429,detail="Rate limit exceeded")
    job=job_service.create(principal.tenant_id,request.document_id,request.target_language,request.domain,request.idempotency_key)
    audit_log.record(AuditEvent("job.created",principal.tenant_id,principal.subject,"job",job.job_id))
    return JobStatusResponse(job_id=job.job_id,status=job.status,progress=job.progress,stage=job.stage)

@router.get("/{job_id}",response_model=JobStatusResponse)
def get_job(job_id:str,x_api_key:str|None=Header(default=None)):
    principal=_principal(x_api_key)
    if not principal.allows("jobs:read"): raise HTTPException(status_code=403,detail="Insufficient scope")
    job=job_service.get(job_id,principal.tenant_id)
    if not job: raise HTTPException(status_code=404,detail="Job not found")
    audit_log.record(AuditEvent("job.read",principal.tenant_id,principal.subject,"job",job.job_id))
    return JobStatusResponse(job_id=job.job_id,status=job.status,progress=job.progress,stage=job.stage,error=job.error)

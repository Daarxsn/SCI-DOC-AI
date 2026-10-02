from fastapi import APIRouter, Header, HTTPException
from backend.api.security import require_api_key
from backend.jobs.models import JobCreateRequest, JobStatusResponse
from backend.jobs.service import JobService

router = APIRouter(prefix="/v1/jobs", tags=["jobs"])
job_service = JobService()

@router.post("", response_model=JobStatusResponse, status_code=202)
def create_job(request: JobCreateRequest, x_api_key: str | None = Header(default=None)):
    try: require_api_key(x_api_key)
    except PermissionError as exc: raise HTTPException(status_code=401, detail=str(exc))
    job = job_service.create(request.tenant_id, request.document_id, request.target_language, request.domain)
    return JobStatusResponse(job_id=job.job_id,status=job.status,progress=job.progress,stage=job.stage)

@router.get("/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str, tenant_id: str, x_api_key: str | None = Header(default=None)):
    try: require_api_key(x_api_key)
    except PermissionError as exc: raise HTTPException(status_code=401, detail=str(exc))
    job = job_service.get(job_id, tenant_id)
    if not job: raise HTTPException(status_code=404, detail="Job not found")
    return JobStatusResponse(job_id=job.job_id,status=job.status,progress=job.progress,stage=job.stage,error=job.error)

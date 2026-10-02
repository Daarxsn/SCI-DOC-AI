from datetime import datetime, timezone
from uuid import uuid4
from backend.jobs.models import Job, JobStatus

class JobService:
    def __init__(self):
        self._jobs = {}

    def create(self, tenant_id, document_id, target_language, domain):
        job = Job(job_id=str(uuid4()), tenant_id=tenant_id, document_id=document_id,
                  metadata={"target_language": target_language, "domain": domain})
        self._jobs[job.job_id] = job
        return job

    def get(self, job_id, tenant_id):
        job = self._jobs.get(job_id)
        if not job or job.tenant_id != tenant_id:
            return None
        return job

    def update(self, job_id, tenant_id, *, status=None, progress=None, stage=None, error=None):
        job = self._jobs[job_id]
        if job.tenant_id != tenant_id:
            raise PermissionError("Tenant boundary violation")
        if status is not None: job.status = status
        if progress is not None: job.progress = progress
        if stage is not None: job.stage = stage
        if error is not None: job.error = error
        job.updated_at = datetime.now(timezone.utc).isoformat()
        return job

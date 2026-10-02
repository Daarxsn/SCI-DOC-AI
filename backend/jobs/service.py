from datetime import datetime, timezone
from uuid import uuid4

from backend.jobs.models import Job, JobStatus
from backend.jobs.queue import InMemoryJobQueue, JobQueue
from backend.jobs.storage import InMemoryJobRepository, JobRepository


class JobService:
    def __init__(self, repository: JobRepository | None = None, queue: JobQueue | None = None):
        self.repository = repository or InMemoryJobRepository()
        self.queue = queue or InMemoryJobQueue()

    def create(self, tenant_id, document_id, target_language, domain, idempotency_key=None):
        if idempotency_key:
            existing = self.find_by_idempotency(tenant_id, idempotency_key)
            if existing:
                return existing

        job = Job(
            job_id=str(uuid4()),
            tenant_id=tenant_id,
            document_id=document_id,
            metadata={
                "target_language": target_language,
                "domain": domain,
                "idempotency_key": idempotency_key,
                "retry_count": 0,
            },
        )
        self.repository.save(job)
        self.queue.enqueue(job.job_id)
        return job

    def find_by_idempotency(self, tenant_id, key):
        jobs = getattr(self.repository, "_jobs", {}).values()
        for job in jobs:
            if job.tenant_id == tenant_id and job.metadata.get("idempotency_key") == key:
                return job
        return None

    def get(self, job_id, tenant_id):
        return self.repository.get(job_id, tenant_id)

    def update(self, job_id, tenant_id, *, status=None, progress=None, stage=None, error=None):
        job = self.repository.get(job_id, tenant_id)
        if not job:
            raise KeyError("Job not found")
        if status is not None: job.status = status
        if progress is not None: job.progress = progress
        if stage is not None: job.stage = stage
        if error is not None: job.error = error
        job.updated_at = datetime.now(timezone.utc).isoformat()
        return self.repository.update(job)

    def retry(self, job_id, tenant_id):
        job = self.repository.get(job_id, tenant_id)
        if not job:
            raise KeyError("Job not found")
        job.metadata["retry_count"] = int(job.metadata.get("retry_count", 0)) + 1
        job.status = JobStatus.QUEUED
        job.progress = 0
        job.stage = "queued"
        job.error = None
        job.updated_at = datetime.now(timezone.utc).isoformat()
        self.repository.update(job)
        self.queue.enqueue(job.job_id)
        return job

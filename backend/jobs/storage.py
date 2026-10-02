from abc import ABC, abstractmethod
from backend.jobs.models import Job


class JobRepository(ABC):
    @abstractmethod
    def save(self, job: Job) -> Job: ...
    @abstractmethod
    def get(self, job_id: str, tenant_id: str) -> Job | None: ...
    @abstractmethod
    def update(self, job: Job) -> Job: ...


class InMemoryJobRepository(JobRepository):
    def __init__(self):
        self._jobs = {}

    def save(self, job):
        self._jobs[job.job_id] = job
        return job

    def get(self, job_id, tenant_id):
        job = self._jobs.get(job_id)
        return job if job and job.tenant_id == tenant_id else None

    def update(self, job):
        return self.save(job)

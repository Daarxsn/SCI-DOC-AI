from abc import ABC, abstractmethod


class JobQueue(ABC):
    @abstractmethod
    def enqueue(self, job_id: str) -> None: ...


class InMemoryJobQueue(JobQueue):
    def __init__(self):
        self.items = []

    def enqueue(self, job_id: str) -> None:
        self.items.append(job_id)

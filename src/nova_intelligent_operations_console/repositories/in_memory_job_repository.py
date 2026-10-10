from nova_intelligent_operations_console.domain.job import Job
from nova_intelligent_operations_console.repositories.job_repository import (
    JobRepository,
)


class InMemoryJobRepository(JobRepository):
    def __init__(self) -> None:
        self._jobs: dict[int, Job] = {}

    def save(self, job : Job) -> None:
        self._jobs[job.job_id] = job

    def get(self, job_id: int) -> Job | None:
        return self._jobs.get(job_id)

    def get_all(self) -> list[Job]:
        return list(self._jobs.values())

    def delete(self, job_id: int) -> None:
        self._jobs.pop(job_id,None)
        
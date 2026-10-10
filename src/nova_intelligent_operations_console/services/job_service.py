from nova_intelligent_operations_console.domain.job import (
    Job,
    JobPriority,
    JobStatus,
)
from nova_intelligent_operations_console.repositories.job_repository import (
    JobRepository,
)


class JobService:

    def __init__(self, repository : JobRepository):
        self.repository = repository


    def create_job(
            self,
            job_id:int,
            name:str,
            priority:JobPriority,
    ) -> Job:

        existing_job = self.repository.get(job_id)

        if existing_job is not None:
            raise ValueError(f"Job with Id {job_id} Already Exists")

        job = Job(
            job_id = job_id,
            name = name,
            priority = priority,
        )
        
        self.repository.save(job)

        return job

    def get_job(self, job_id: int) -> Job | None:
        return self.repository.get(job_id)

    def list_jobs(self)-> list[Job]:
        return self.repository.get_all()

    def delete_job(self, job_id: int)-> None:
        self.repository.delete(job_id)

    def update_job_status(
            self,
            job_id: int,
            status: JobStatus,
    ) -> Job | None:
        job = self.repository.get(job_id)

        if job is None:
            return None

        job.status = status
        self.repository.save(job)

        return job
from abc import ABC, abstractmethod

from nova_intelligent_operations_console.domain.job import Job


class JobRepository(ABC):
    @abstractmethod
    def add(self, job : Job)-> None:
        """Insert a new job, Reject an ID that already exists."""
        raise NotImplementedError

    @abstractmethod
    def update(self, job: Job)-> None:
        """"Update an existing job. Reject an ID that does not exists."""
        raise NotImplementedError

    @abstractmethod
    def get(self, job_id: int)->Job | None:
        """"Return a job by ID, or none if its not exist."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self)->list[Job]:
        """"Return all stored jobs."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, job_id: int)-> None:
        """"Delete a job by ID, or none if its not exist."""
        raise NotImplementedError
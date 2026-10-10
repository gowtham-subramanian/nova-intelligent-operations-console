from abc import ABC, abstractmethod

from nova_intelligent_operations_console.domain.job import Job


class JobRepository(ABC):
    @abstractmethod
    def save(self, job: Job) -> None:
        pass

    @abstractmethod
    def get(self, job_id: int) -> Job | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Job]:
        pass

    @abstractmethod
    def delete(self, job_id: int) -> None:
        pass
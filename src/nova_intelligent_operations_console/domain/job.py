
from dataclasses import dataclass
from enum import StrEnum


class JobStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class JobPriority(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


_ALLOWED_TRANSITIONS: dict[JobStatus, frozenset[JobStatus]] = {
    JobStatus.PENDING: frozenset({
        JobStatus.RUNNING,
    }),
    JobStatus.RUNNING: frozenset({
        JobStatus.COMPLETED,
        JobStatus.FAILED,
    }),
    JobStatus.COMPLETED: frozenset(),
    JobStatus.FAILED: frozenset(),
}

@dataclass
class Job:
    job_id: int
    name: str
    priority: JobPriority
    status: JobStatus = JobStatus.PENDING

    def transition_to(self, new_status: JobStatus) -> None:
        if new_status == self.status:
            return

        allowed_statuses = _ALLOWED_TRANSITIONS[self.status]

        if new_status not in allowed_statuses:
            raise ValueError(
                "Invalid job status transition: "
                f"{self.status.value} -> {new_status.value}"
            )

        self.status = new_status

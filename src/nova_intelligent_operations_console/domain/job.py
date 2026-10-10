
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

@dataclass
class Job:
    job_id: int
    name: str
    priority: JobPriority
    status: JobStatus = JobStatus.PENDING

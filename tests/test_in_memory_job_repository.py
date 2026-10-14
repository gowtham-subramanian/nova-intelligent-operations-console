import pytest

from nova_intelligent_operations_console.domain.job import (
    Job,
    JobPriority,
    JobStatus,
)
from nova_intelligent_operations_console.repositories.in_memory_job_repository import (
    InMemoryJobRepository,
)


def test_add_stores_new_job():
    repository = InMemoryJobRepository()

    job = Job(
        job_id = 101,
        name = "Daily Sales Report",
        priority = JobPriority.HIGH,
    )
    repository.add(job)

    assert repository.get(101) == job

def test_add_duplicate_rejects_without_overwriting_original():
    repository = InMemoryJobRepository()
    original_job = Job(
        job_id = 101,
        name = "Daily sales report",
        priority = JobPriority.HIGH,
    )
    duplicate_job = Job(
        job_id=101,
        name="Inventory Report",
        priority=JobPriority.MEDIUM,
    )

    repository.add(original_job)

    with pytest.raises(
        ValueError, match = "Job with ID 101 Already Exists.",
    ):
        repository.add(duplicate_job)

    stored_job = repository.get(101)

    assert stored_job is not None
    assert stored_job == original_job
    assert stored_job.name == "Daily sales report"
    assert stored_job.priority == JobPriority.HIGH

def test_update_replaces_existing_job():
    repository = InMemoryJobRepository()

    original_job = Job(
        job_id=101,
        name="Daily Sales Report",
        priority=JobPriority.HIGH,
    )
    updated_job = Job(
        job_id=101,
        name="Daily Sales Report",
        priority=JobPriority.HIGH,
        status=JobStatus.RUNNING,
    )
    repository.add(original_job)
    repository.update(updated_job)

    stored_job = repository.get(101)

    assert stored_job is not None
    assert stored_job == updated_job
    assert stored_job.priority == JobPriority.HIGH
    assert stored_job.status == JobStatus.RUNNING


def test_updated_rejects_missing_job():
    repository = InMemoryJobRepository()

    missing_job = Job(
        job_id = 999,
        name = "missing job",
        priority = JobPriority.LOW,
    )

    with pytest.raises(ValueError, match = "Job with ID 999 does not exist."):
        repository.update(missing_job)

    assert repository.get(999) is None

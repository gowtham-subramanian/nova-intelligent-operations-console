
import pytest

from nova_intelligent_operations_console.domain.job import (
    JobPriority,
    JobStatus,
)
from nova_intelligent_operations_console.repositories.in_memory_job_repository import (
    InMemoryJobRepository,
)
from nova_intelligent_operations_console.services.job_service import JobService


def test_create_job():
    repository = InMemoryJobRepository()
    service = JobService(repository)

    job = service.create_job(
        job_id=101,
        name="Generate today's sales report",
        priority=JobPriority.HIGH,
    )

    assert job.job_id == 101
    assert job.name == "Generate today's sales report"
    assert job.priority == JobPriority.HIGH
    assert job.status == JobStatus.PENDING


def test_get_job():
    repository = InMemoryJobRepository()
    service = JobService(repository)

    service.create_job(
        job_id=101,
        name="Generate today's sales report",
        priority=JobPriority.HIGH,
    )

    job = service.get_job(101)

    assert job is not None
    assert job.job_id == 101
    assert job.name == "Generate today's sales report"
    assert job.priority == JobPriority.HIGH
    assert job.status == JobStatus.PENDING


def test_list_jobs():
    repository = InMemoryJobRepository()
    service = JobService(repository)

    service.create_job(
        job_id=101,
        name="Generate today's sales report",
        priority=JobPriority.HIGH,
    )

    service.create_job(
        job_id=102,
        name="Create customer backup",
        priority=JobPriority.MEDIUM,
    )

    jobs = service.list_jobs()

    assert len(jobs) == 2
    assert jobs[0].job_id == 101
    assert jobs[1].job_id == 102


def test_update_job_status():
    repository = InMemoryJobRepository()
    service = JobService(repository)

    service.create_job(
        job_id=101,
        name="Generate today's sales report",
        priority=JobPriority.HIGH,
    )

    job = service.update_job_status(
        job_id=101,
        status=JobStatus.RUNNING,
    )

    assert job is not None
    assert job.status == JobStatus.RUNNING


def test_update_missing_job_returns_none():
    repository = InMemoryJobRepository()
    service = JobService(repository)

    job = service.update_job_status(
        job_id=999,
        status=JobStatus.RUNNING,
    )

    assert job is None


def test_delete_job():
    repository = InMemoryJobRepository()
    service = JobService(repository)

    service.create_job(
        job_id=101,
        name="Generate today's sales report",
        priority=JobPriority.HIGH,
    )

    service.delete_job(101)

    job = service.get_job(101)

    assert job is None


def test_create_job_rejects_duplicate_job():
    repository = InMemoryJobRepository()
    service = JobService(repository)

    original_job = service.create_job(
        job_id=101,
        name="Generate today's sales report",
        priority=JobPriority.HIGH,
    )

    with pytest.raises(
        ValueError,
        match="Job with ID 101 Already Exists",
    ):
        service.create_job(
            job_id=101,
            name="Inventory report",
            priority=JobPriority.MEDIUM,
        )

    stored_job = service.get_job(101)

    assert stored_job is not None
    assert stored_job == original_job
    assert stored_job.name == "Generate today's sales report"
    assert stored_job.priority == JobPriority.HIGH


@pytest.mark.parametrize(
    "target_status",
    [
        JobStatus.COMPLETED,
        JobStatus.FAILED,
    ],
)
def test_running_job_can_transition_to_terminal_status(target_status):
    repository = InMemoryJobRepository()
    service = JobService(repository)

    service.create_job(
        job_id=101,
        name="Generate today's sales report",
        priority=JobPriority.HIGH,
    )

    service.update_job_status(
        job_id=101,
        status=JobStatus.RUNNING,
    )

    job = service.update_job_status(
        job_id=101,
        status=target_status,
    )

    assert job is not None
    assert job.status == target_status


def test_same_status_transition_is_a_no_op():
    repository = InMemoryJobRepository()
    service = JobService(repository)

    service.create_job(
        job_id=101,
        name="Generate today's sales report",
        priority=JobPriority.HIGH,
    )

    job = service.update_job_status(
        job_id=101,
        status=JobStatus.PENDING,
    )

    assert job is not None
    assert job.status == JobStatus.PENDING


@pytest.mark.parametrize(
    ("initial_status", "target_status"),
    [
        (JobStatus.PENDING, JobStatus.COMPLETED),
        (JobStatus.COMPLETED, JobStatus.RUNNING),
        (JobStatus.COMPLETED, JobStatus.FAILED),
        (JobStatus.FAILED, JobStatus.RUNNING),
        (JobStatus.FAILED, JobStatus.COMPLETED),
        (JobStatus.PENDING, JobStatus.FAILED),
        (JobStatus.RUNNING, JobStatus.PENDING),
        (JobStatus.COMPLETED, JobStatus.PENDING),
        (JobStatus.FAILED, JobStatus.PENDING),
    ],
)
def test_invalid_status_transition_is_rejected_and_status_is_preserved(
    initial_status,
    target_status,
):
    repository = InMemoryJobRepository()
    service = JobService(repository)

    service.create_job(
        job_id=101,
        name="Generate today's sales report",
        priority=JobPriority.HIGH,
    )

    if initial_status != JobStatus.PENDING:
        service.update_job_status(
            job_id=101,
            status=JobStatus.RUNNING,
        )

    if initial_status in (JobStatus.COMPLETED, JobStatus.FAILED):
        service.update_job_status(
            job_id=101,
            status=initial_status,
        )

    job_before_attempt = service.get_job(101)

    assert job_before_attempt is not None
    assert job_before_attempt.status == initial_status

    with pytest.raises(
        ValueError,
        match="Invalid job status transition",
    ):
        service.update_job_status(
            job_id=101,
            status=target_status,
        )

    job_after_attempt = service.get_job(101)

    assert job_after_attempt is not None
    assert job_after_attempt.status == initial_status

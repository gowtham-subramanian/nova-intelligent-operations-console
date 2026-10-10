# NOVA — Intelligent Operations Console

NOVA is a Python-based operations management system designed to centralize the lifecycle of operational jobs.

The project is being developed using an incremental, test-driven approach, with an emphasis on readable Python, clear separation of responsibilities, automated testing, and maintainable software architecture.

## Current Capabilities

- Create operational jobs.
- Retrieve a job by its ID.
- List all stored jobs.
- Update a job's status.
- Delete a job.
- Reject duplicate job IDs through the service layer.
- Preserve the original job when duplicate creation is rejected.
- Run automated tests using pytest.

## Current Architecture

NOVA currently uses a simple layered design.

```text
NOVA
├── src/
│   └── nova_intelligent_operations_console/
│       ├── domain/
│       │   └── job.py
│       ├── repositories/
│       │   ├── job_repository.py
│       │   └── in_memory_job_repository.py
│       └── services/
│           └── job_service.py
├── tests/
│   └── test_job_service.py
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
```

### Domain

Defines the `Job` model and the job status and priority values.

### Repository

Defines the job storage contract and its current in-memory implementation.

### Service

Coordinates job operations and applies the duplicate-ID business rule during job creation.

### Tests

Verifies the behavior of job creation, retrieval, listing, status updates, deletion, and duplicate-ID rejection.

## Technology Stack

- Python 3.11+
- uv for project and environment management
- pytest for automated testing
- Git for version control

## Prerequisites

Install Python 3.11 or a compatible newer version and uv.

## Setup

Clone the repository, then navigate to its root directory.

Synchronize the project environment:

```powershell
uv sync
```

Run the automated test suite:

```powershell
uv run pytest -v
```

## Current Storage Limitation

The current repository stores jobs in memory. Job data is not persisted across application restarts.

The service prevents duplicate IDs when jobs are created through its `create_job()` operation. The current repository's `save()` method can replace an existing dictionary entry when called directly with the same ID.

Database-backed persistence, stronger storage integrity guarantees, an API, and a user interface are future development areas, not current capabilities.

## Development Principles

NOVA is developed with the following engineering principles:

- Business requirements before implementation.
- Clear separation of domain, service, and repository responsibilities.
- Readable and explicit Python code.
- Automated testing of business behavior.
- Incremental changes with reviewable Git history.
- Documented architectural decisions and trade-offs.

## Project Status

**Early development — repository and CRUD hardening.**

The next development work will strengthen the job lifecycle rules, edge-case handling, repository behavior, and automated test coverage.

NOVA is intended to evolve incrementally into a production-oriented operations platform.

from __future__ import annotations

from services.common.models import Job, JobStatus


def test_health_endpoints(client):
    for path in ["/", "/health/live", "/health/ready"]:
        response = client.get(path)
        assert response.status_code == 200


def test_create_and_read_case_and_job(client):
    create_response = client.post(
        "/cases",
        json={
            "title": "Cannot login to dashboard",
            "description": "User cannot access the dashboard after a password reset.",
        },
    )
    assert create_response.status_code == 201

    payload = create_response.json()
    case_id = payload["case"]["id"]
    job_id = payload["job"]["id"]

    assert payload["case"]["status"] == "queued"
    assert payload["job"]["status"] == "pending"
    assert payload["job"]["job_type"] == "triage_case"
    assert payload["job"]["case_id"] == case_id

    list_response = client.get("/cases")
    assert list_response.status_code == 200
    assert any(item["id"] == case_id for item in list_response.json())

    case_response = client.get(f"/cases/{case_id}")
    assert case_response.status_code == 200
    assert case_response.json()["title"] == "Cannot login to dashboard"

    job_response = client.get(f"/jobs/{job_id}")
    assert job_response.status_code == 200
    assert job_response.json()["case_id"] == case_id


def test_list_jobs_can_filter_by_status(client, db_session):
    first_response = client.post(
        "/cases",
        json={
            "title": "First support case",
            "description": "The first case creates a job for filtering.",
        },
    )
    second_response = client.post(
        "/cases",
        json={
            "title": "Second support case",
            "description": "The second case creates another job for filtering.",
        },
    )

    first_job_id = first_response.json()["job"]["id"]
    second_job_id = second_response.json()["job"]["id"]
    first_job = db_session.get(Job, first_job_id)
    assert first_job is not None
    first_job.status = JobStatus.COMPLETED.value
    db_session.commit()

    pending_response = client.get("/jobs", params={"status": "pending"})
    assert pending_response.status_code == 200
    assert [job["id"] for job in pending_response.json()] == [second_job_id]

    completed_response = client.get("/jobs", params={"status": "completed"})
    assert completed_response.status_code == 200
    assert [job["id"] for job in completed_response.json()] == [first_job_id]


def test_list_jobs_rejects_invalid_status_and_limit(client):
    invalid_status = client.get("/jobs", params={"status": "unknown"})
    assert invalid_status.status_code == 422

    invalid_limit = client.get("/jobs", params={"limit": 0})
    assert invalid_limit.status_code == 422

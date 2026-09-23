# Week 3 Submission - Individual Readiness Lab

## Student information

- Name: ZHANG, Boxiang
- Student ID: 21344801
- Repository: https://github.com/BoxiangZ/starterMAIE600C
- Checkpoint tag: `w03-readiness`
- Checkpoint commit: resolve with `git rev-parse 'w03-readiness^{commit}'`

## 1. What I changed

I added `GET /jobs`, a small API endpoint that lists jobs newest-first. It supports an
optional `status` filter (`pending`, `claimed`, `completed`, or `failed`) and a validated
`limit` from 1 to 100. Invalid filter values return FastAPI's standard `422` response.

I also updated the Docker image to include the development dependencies and test files so
the documented container-based verification command is reproducible.

## 2. Files touched

- `services/api/app/main.py`
- `tests/integration/test_api_case_flow.py`
- `Dockerfile`
- `submissions/week03/README.md`

## 3. How to run it

1. Copy `.env.example` to `.env` if a local environment file does not exist.
2. Run `docker compose up --build` from the repository root.
3. Open the API documentation at `http://localhost:8000/docs`, or use the value of
   `API_HOST_PORT` from `.env` if the host port was changed.
4. Create a case with `POST /cases`, then inspect its background job with
   `GET /jobs/{job_id}` or list jobs with `GET /jobs?status=pending&limit=20`.

## 4. How I verified it

- `docker compose config --quiet` completed successfully.
- `docker compose build --no-cache api` completed successfully.
- Container test discovery confirmed the files under `/app/tests`.
- `docker compose run --rm --no-deps api pytest -q tests/unit tests/integration` passed:
  6 tests passed with 2 third-party deprecation warnings.
- `docker compose run --rm --no-deps api ruff check .` passed with no errors.
- Started the full stack and confirmed API liveness and readiness both returned `200` on
  the configured host port `8001`.
- Traced case `56ba50f9-a31f-4d28-9415-5f9919985ecc` end-to-end: it reached `triaged`
  with label `access`; job `3` reached `completed` with `attempts` equal to `1`.
- Called `GET /jobs?status=completed&limit=1` and received the completed job; an unknown
  status returned `422`.
- `git diff --check` passed with no whitespace errors.

## 5. Known limitations or notes

- The endpoint uses limit-only listing and does not yet provide cursor or offset pagination.
- Filtering supports one exact job status at a time.

## 6. AI Use Statement

OpenAI Codex was used to inspect the starter repository and Lab 3 brief, implement the
bounded endpoint and tests, update the container verification setup, and draft this summary.
The result was checked with the project's automated tests, live API requests, and lint checks.
I remain responsible for reviewing, explaining, and defending the submitted work.

# Glasgow Live Sim

Glasgow Live Sim is a V1 FastAPI site for exploring Glasgow wildfire, smoke, and resilience scenarios using only approved open or explicitly reusable data.

## Milestone status

- M0 repository guidance: no in-repo `AGENTS.md` or IDE-referenced planning files were present when this continuation started; repository guardrails are captured here, in docs, tests, and CI.
- M1 open-data and licence register: see [`docs/open-data-register.md`](docs/open-data-register.md), `/data`, and `/api/datasets`.
- M2 architecture boundaries: FastAPI app code is isolated under `app/`, tests under `tests/`, and provenance docs under `docs/`.
- M3-M7 V1 product criteria: scenario pages, methodology, accessibility, privacy, SEO/AEO, JSON APIs, testing, CI, and production smoke checks are implemented for the shippable prototype.

## Run locally

```bash
uv sync
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Checks

```bash
uv run ruff check .
uv run pytest
uv run python scripts/check_bloat.py
```

## Production smoke

```bash
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:8000/
curl -fsS http://127.0.0.1:8000/scenarios
curl -fsS http://127.0.0.1:8000/scenarios/m74-smoke-plume
curl -fsS http://127.0.0.1:8000/methodology
curl -fsS http://127.0.0.1:8000/data
curl -fsS http://127.0.0.1:8000/privacy
curl -fsS http://127.0.0.1:8000/accessibility
curl -fsS http://127.0.0.1:8000/api/scenarios
curl -fsS http://127.0.0.1:8000/api/datasets
curl -fsS http://127.0.0.1:8000/robots.txt
curl -fsS http://127.0.0.1:8000/sitemap.xml
curl -fsS http://127.0.0.1:8000/site.webmanifest
# or run the scripted smoke check
BASE_URL=http://127.0.0.1:8000 ./scripts/smoke.sh
```

## Container and PostGIS development

```bash
docker compose up --build
BASE_URL=http://127.0.0.1:8000 ./scripts/smoke.sh
```

Production launch gates are documented in [`docs/production-launch-checklist.md`](docs/production-launch-checklist.md).

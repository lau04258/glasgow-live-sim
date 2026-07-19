# Architecture boundaries

- `app/main.py` owns HTTP routes, JSON APIs, and response composition.
- `app/data.py` owns static demonstrator scenario records, metrics, methodology copy, and approved-dataset metadata.
- `app/config.py` owns environment configuration and PostgreSQL/PostGIS connection settings.
- Templates remain presentational; they do not fetch external data or embed third-party tracking.
- PostgreSQL/PostGIS is the target production persistence boundary, but V1 keeps demo data static until approved data pipelines are added.
- Public pages and machine-readable API endpoints are both covered by smoke tests.
- New external providers, credentials, or non-open datasets require explicit approval before implementation.

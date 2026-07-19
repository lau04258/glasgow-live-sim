# Production launch checklist

## Required before public launch

- Confirm every dataset in `docs/open-data-register.md` is still available under its documented open licence.
- Replace local demonstration PostgreSQL credentials with secret-managed production credentials.
- Run `uv run ruff check .`, `uv run pytest`, `uv run python scripts/check_bloat.py`, and `BASE_URL=<production URL> ./scripts/smoke.sh`.
- Confirm `/privacy` still matches analytics configuration and any deployed analytics provider.
- Confirm `/accessibility` reflects the latest manual accessibility audit status.
- Confirm the service is not marketed as an official emergency alert channel.

## External-provider pause points

Pause for explicit approval before adding credentials, proprietary datasets, paid APIs, tracking pixels, destructive database migrations, or unreviewed emergency-alert integrations.

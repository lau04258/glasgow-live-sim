from pathlib import Path


def test_container_and_postgis_packaging_are_documented() -> None:
    dockerfile = Path("Dockerfile").read_text()
    compose = Path("compose.yml").read_text()
    checklist = Path("docs/production-launch-checklist.md").read_text()

    assert "uv sync --frozen --no-dev" in dockerfile
    assert "postgis/postgis" in compose
    assert "DATABASE_URL" in compose
    assert "Production launch checklist" in checklist
    assert "External-provider pause points" in checklist


def test_smoke_script_is_strict_mode() -> None:
    smoke = Path("scripts/smoke.sh").read_text()
    assert "set -euo pipefail" in smoke
    assert "/api/scenarios" in smoke
    assert "/sitemap.xml" in smoke

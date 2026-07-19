from app.data import SCENARIOS, approved_datasets, dataset_map, scenario_by_id
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

CORE_PATHS = [
    "/",
    "/scenarios",
    "/scenarios/m74-smoke-plume",
    "/methodology",
    "/data",
    "/privacy",
    "/accessibility",
    "/robots.txt",
    "/sitemap.xml",
    "/site.webmanifest",
]


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_core_pages_render() -> None:
    for path in CORE_PATHS:
        response = client.get(path)
        assert response.status_code == 200, path


def test_json_api_endpoints_render() -> None:
    scenarios = client.get("/api/scenarios")
    datasets = client.get("/api/datasets")
    detail = client.get("/api/scenarios/m74-smoke-plume")

    assert scenarios.status_code == 200
    assert datasets.status_code == 200
    assert detail.status_code == 200
    assert scenarios.json()["count"] == len(SCENARIOS)
    assert datasets.json()["count"] == len(approved_datasets())
    assert detail.json()["provenance"]


def test_unknown_scenario_returns_404() -> None:
    assert client.get("/scenarios/not-a-scenario").status_code == 404
    assert client.get("/api/scenarios/not-a-scenario").status_code == 404


def test_only_approved_open_datasets_are_exposed() -> None:
    datasets = approved_datasets()
    assert datasets
    assert all(dataset["reuse"] == "approved-open" for dataset in datasets)
    assert all(dataset["contains_personal_data"] is False for dataset in datasets)
    assert all("licence" in dataset and "source_url" in dataset for dataset in datasets)


def test_every_scenario_references_registered_datasets() -> None:
    datasets = dataset_map()
    for scenario in SCENARIOS:
        assert scenario_by_id(scenario["id"]) == scenario
        assert scenario["datasets"]
        assert all(dataset_id in datasets for dataset_id in scenario["datasets"])


def test_accessibility_landmarks() -> None:
    response = client.get("/")
    assert 'href="#main"' in response.text
    assert '<main id="main">' in response.text
    assert 'aria-label="Primary"' in response.text
    assert "prefers-reduced-motion" in client.get("/static/css/styles.css").text


def test_sitemap_lists_public_pages() -> None:
    response = client.get("/sitemap.xml")
    for path in ["/scenarios", "/methodology", "/accessibility"]:
        assert f"<loc>{path}</loc>" in response.text


def test_security_headers_are_present() -> None:
    response = client.get("/")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert "geolocation=()" in response.headers["permissions-policy"]


def test_html_404_page_and_api_404_shape() -> None:
    page = client.get("/missing-page")
    api = client.get("/api/scenarios/missing-page")
    assert page.status_code == 404
    assert "Page not found" in page.text
    assert api.status_code == 404
    assert api.json()["detail"] == "Scenario not found"


def test_site_manifest_is_csp_compatible() -> None:
    response = client.get("/site.webmanifest")
    assert response.status_code == 200
    assert response.json()["short_name"] == "Glasgow Sim"
    assert '<script type="application/ld+json">' not in client.get("/").text

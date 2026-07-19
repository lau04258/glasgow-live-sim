from typing import Any

DATASETS: list[dict[str, Any]] = [
    {
        "id": "os-open-greenspace",
        "name": "OS Open Greenspace",
        "publisher": "Ordnance Survey",
        "licence": "Open Government Licence v3.0",
        "reuse": "approved-open",
        "source_url": "https://www.ordnancesurvey.co.uk/products/os-open-greenspace",
        "purpose": "Parks and accessible open-space context for heat and smoke refuge planning.",
        "contains_personal_data": False,
        "refresh": "Manual register review before ingestion",
    },
    {
        "id": "os-open-roads",
        "name": "OS Open Roads",
        "publisher": "Ordnance Survey",
        "licence": "Open Government Licence v3.0",
        "reuse": "approved-open",
        "source_url": "https://www.ordnancesurvey.co.uk/products/os-open-roads",
        "purpose": "Routing context for response and evacuation modelling boundaries.",
        "contains_personal_data": False,
        "refresh": "Manual register review before ingestion",
    },
    {
        "id": "scotgov-urban-rural-classification",
        "name": "Scottish Government Urban Rural Classification",
        "publisher": "Scottish Government",
        "licence": "Open Government Licence v3.0",
        "reuse": "approved-open",
        "source_url": "https://www.gov.scot/publications/scottish-government-urban-rural-classification-2020/",
        "purpose": "Regional context for scenario assumptions.",
        "contains_personal_data": False,
        "refresh": "Manual register review before ingestion",
    },
]

SCENARIOS: list[dict[str, Any]] = [
    {
        "id": "m74-smoke-plume",
        "title": "M74 corridor smoke plume",
        "summary": (
            "A roadside grass ignition creates a smoke plume affecting commuter visibility "
            "and nearby neighbourhood air quality."
        ),
        "risk": "Air quality and visibility disruption",
        "status": "demo",
        "last_updated": "2026-07-18",
        "confidence": 72,
        "severity": "medium",
        "area": "South and east Glasgow",
        "time_horizon": "0–6 hours",
        "recommended_actions": [
            "Prioritise public warnings for vulnerable residents downwind.",
            "Review alternative routes before closing strategic road links.",
            "Use parks and community assets as clean-air messaging anchors.",
        ],
        "datasets": ["os-open-roads", "os-open-greenspace"],
    },
    {
        "id": "kelvin-park-heat",
        "title": "Kelvin corridor dry-grass ignition",
        "summary": (
            "Extended dry weather raises ignition sensitivity around parks, paths, "
            "and river-corridor vegetation."
        ),
        "risk": "Urban-wildland interface around parks",
        "status": "demo",
        "last_updated": "2026-07-18",
        "confidence": 68,
        "severity": "medium",
        "area": "West End and Kelvin corridor",
        "time_horizon": "24–72 hours",
        "recommended_actions": [
            "Target prevention messaging at high-footfall park entrances.",
            "Plan accessible refuge and hydration wayfinding.",
            "Escalate monitoring if wind and dry-grass indicators align.",
        ],
        "datasets": ["os-open-greenspace", "scotgov-urban-rural-classification"],
    },
    {
        "id": "clyde-event-evacuation",
        "title": "Clyde event dispersal under smoke alert",
        "summary": (
            "A riverside event coincides with smoke-alert messaging and requires "
            "accessible dispersal planning."
        ),
        "risk": "Crowd movement, accessible routing, and public information load",
        "status": "demo",
        "last_updated": "2026-07-18",
        "confidence": 61,
        "severity": "low",
        "area": "City centre and Clyde corridor",
        "time_horizon": "0–3 hours",
        "recommended_actions": [
            "Keep instructions plain-language and consistent across channels.",
            "Prioritise step-free dispersal routes and rest points.",
            "Publish uncertainty alongside recommended protective actions.",
        ],
        "datasets": ["os-open-roads", "os-open-greenspace"],
    },
]

METRICS: list[dict[str, str | int]] = [
    {"label": "Approved datasets", "value": len(DATASETS), "detail": "All OGL-compatible"},
    {"label": "Demo scenarios", "value": len(SCENARIOS), "detail": "Human-reviewed"},
    {"label": "Personal data fields", "value": 0, "detail": "None collected for V1"},
]

METHODOLOGY_STEPS: list[dict[str, str]] = [
    {
        "title": "Register before use",
        "body": (
            "Every dataset must be documented with publisher, licence, purpose, "
            "and personal-data status before it can be referenced by a scenario."
        ),
    },
    {
        "title": "Separate demo assumptions from facts",
        "body": (
            "Scenario text is demonstrator content; it does not claim to be a live "
            "emergency feed or official instruction."
        ),
    },
    {
        "title": "Show uncertainty",
        "body": (
            "Each scenario displays a confidence score, status, time horizon, "
            "and recommended operational review actions."
        ),
    },
    {
        "title": "Smoke before launch",
        "body": (
            "Health, core pages, machine-readable API endpoints, robots, and sitemap "
            "are checked against a running server."
        ),
    },
]


def approved_datasets() -> list[dict[str, Any]]:
    return [dataset for dataset in DATASETS if dataset["reuse"] == "approved-open"]


def scenario_by_id(scenario_id: str) -> dict[str, Any] | None:
    return next((scenario for scenario in SCENARIOS if scenario["id"] == scenario_id), None)


def dataset_map() -> dict[str, dict[str, Any]]:
    return {dataset["id"]: dataset for dataset in approved_datasets()}

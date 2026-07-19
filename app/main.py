from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.data import (
    METHODOLOGY_STEPS,
    METRICS,
    SCENARIOS,
    approved_datasets,
    dataset_map,
    scenario_by_id,
)
from app.services.security import SecurityHeadersMiddleware

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description="Open-data Glasgow city simulation for resilience planning.",
    version="0.2.0",
)
app.add_middleware(SecurityHeadersMiddleware)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/health", response_class=JSONResponse)
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name, "environment": settings.environment}


@app.get("/api/scenarios", response_class=JSONResponse)
def api_scenarios() -> dict[str, object]:
    return {"scenarios": SCENARIOS, "count": len(SCENARIOS)}


@app.get("/api/scenarios/{scenario_id}", response_class=JSONResponse)
def api_scenario(scenario_id: str) -> dict[str, object]:
    scenario = scenario_by_id(scenario_id)
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    datasets = dataset_map()
    return {
        "scenario": scenario,
        "provenance": [datasets[dataset_id] for dataset_id in scenario["datasets"]],
    }


@app.get("/api/datasets", response_class=JSONResponse)
def api_datasets() -> dict[str, object]:
    return {"datasets": approved_datasets(), "count": len(approved_datasets())}


@app.get("/site.webmanifest", response_class=JSONResponse)
def site_manifest() -> dict[str, object]:
    return {
        "name": settings.app_name,
        "short_name": "Glasgow Sim",
        "description": "Open-data Glasgow wildfire, smoke, and resilience scenario simulator.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#f6fbf8",
        "theme_color": "#122118",
    }


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots() -> str:
    return "User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n"


@app.get("/sitemap.xml", response_class=PlainTextResponse)
def sitemap() -> str:
    urls = ["/", "/scenarios", "/methodology", "/data", "/privacy", "/accessibility"]
    url_nodes = "\n".join(f"  <url><loc>{url}</loc></url>" for url in urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{url_nodes}
</urlset>
"""


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "scenarios": SCENARIOS,
            "datasets": approved_datasets(),
            "metrics": METRICS,
            "analytics": settings.analytics_enabled,
        },
    )


@app.get("/scenarios", response_class=HTMLResponse)
def scenarios(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "scenarios.html",
        {"scenarios": SCENARIOS, "datasets": dataset_map()},
    )


@app.get("/scenarios/{scenario_id}", response_class=HTMLResponse)
def scenario_detail(request: Request, scenario_id: str) -> HTMLResponse:
    scenario = scenario_by_id(scenario_id)
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    datasets = dataset_map()
    return templates.TemplateResponse(
        request,
        "scenario_detail.html",
        {
            "scenario": scenario,
            "provenance": [datasets[dataset_id] for dataset_id in scenario["datasets"]],
        },
    )


@app.get("/methodology", response_class=HTMLResponse)
def methodology(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "methodology.html",
        {"steps": METHODOLOGY_STEPS},
    )


@app.get("/data", response_class=HTMLResponse)
def data_register(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "data.html", {"datasets": approved_datasets()})


@app.get("/privacy", response_class=HTMLResponse)
def privacy(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "privacy.html",
        {"analytics": settings.analytics_enabled},
    )


@app.get("/accessibility", response_class=HTMLResponse)
def accessibility(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "accessibility.html")


@app.exception_handler(404)
async def not_found(request: Request, exc: HTTPException) -> HTMLResponse:
    if request.url.path.startswith("/api/"):
        return await http_exception_handler(request, exc)
    return templates.TemplateResponse(request, "404.html", status_code=404)

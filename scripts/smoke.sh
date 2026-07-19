#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"
paths=(
  /health
  /
  /scenarios
  /scenarios/m74-smoke-plume
  /methodology
  /data
  /privacy
  /accessibility
  /api/scenarios
  /api/datasets
  /robots.txt
  /sitemap.xml
  /site.webmanifest
)
for path in "${paths[@]}"; do
  curl -fsS "${BASE_URL}${path}" >/dev/null
  printf 'ok %s\n' "${path}"
done
python - <<'PY'
import json
import os
import urllib.request

base_url = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
with urllib.request.urlopen(f"{base_url}/api/scenarios") as response:
    payload = json.load(response)
assert payload["count"] >= 3
with urllib.request.urlopen(f"{base_url}/api/datasets") as response:
    payload = json.load(response)
assert all(dataset["reuse"] == "approved-open" for dataset in payload["datasets"])
print("production smoke passed")
PY

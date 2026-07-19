# V1 acceptance criteria

- Health endpoint returns HTTP 200 JSON.
- Home, scenario library, scenario detail, methodology, data register, privacy, accessibility, robots, and sitemap endpoints render successfully.
- JSON API endpoints expose scenario and dataset records for product smoke checks.
- Every dataset used by the app is approved-open in the licence register and records licence, source URL, purpose, refresh, and personal-data status.
- Analytics are disabled by default and require explicit configuration.
- Pages include semantic landmarks, skip link, visible focus styling, responsive tables, and reduced-motion handling.
- CI runs linting and tests on every push and pull request.
- Production smoke checks pass against a locally launched ASGI server.
- Scenario pages clearly state demonstrator status and avoid presenting content as official emergency guidance.

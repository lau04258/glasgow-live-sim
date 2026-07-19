from pathlib import Path

LIMITS = {
    "app/static/css/styles.css": 16_000,
    "app/data.py": 32_000,
}

failures = []
for file_name, limit in LIMITS.items():
    size = Path(file_name).stat().st_size
    if size > limit:
        failures.append(f"{file_name} is {size} bytes; limit is {limit} bytes")

if failures:
    raise SystemExit("\n".join(failures))

print("bloat check passed")

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required = [
    "docker-compose.staging.yml",
    ".env.staging.example",
    "docs/PHASE11_STAGING_DEPLOYMENT.md",
    "tests/test_p11_staging.py",
]

for relative in required:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"missing Phase 11 file: {relative}")

compose = (ROOT / "docker-compose.staging.yml").read_text(encoding="utf-8")
for service in ("api:", "postgres:", "redis:", "minio:"):
    if service not in compose:
        raise SystemExit(f"missing staging service: {service}")

for marker in ("healthcheck:", "depends_on:", "postgres_staging_data", "redis_staging_data", "object_staging_data"):
    if marker not in compose:
        raise SystemExit(f"missing staging configuration marker: {marker}")

env = (ROOT / ".env.staging.example").read_text(encoding="utf-8")
for marker in ("SCI_DOC_API_KEY=", "SCI_DOC_TENANT_ID=", "POSTGRES_PASSWORD=", "MINIO_ROOT_PASSWORD="):
    if marker not in env:
        raise SystemExit(f"missing staging environment setting: {marker}")

print("Phase 11 structural verification: PASS")

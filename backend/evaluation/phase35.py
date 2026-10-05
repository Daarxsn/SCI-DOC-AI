import json
from pathlib import Path
from typing import Any

REQUIRED_RELEASE_FIELDS = {"version", "release_channel"}
REQUIRED_RUNTIME_FIELDS = {"api_key_configured", "tenant_isolation_configured", "tls_configured", "durable_storage_configured", "queue_configured", "ml_runtime_configured"}

def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def assess_deployment_readiness(release: dict[str, Any], runtime: dict[str, Any]) -> dict[str, Any]:
    missing_release = sorted(REQUIRED_RELEASE_FIELDS - set(release))
    missing_runtime = sorted(REQUIRED_RUNTIME_FIELDS - set(runtime))
    checks = [{"check": field, "configured": runtime.get(field) is True} for field in sorted(REQUIRED_RUNTIME_FIELDS)]
    blockers = [c["check"] for c in checks if not c["configured"]]
    blockers.extend(f"release.{x}" for x in missing_release)
    blockers.extend(f"runtime.{x}" for x in missing_runtime)
    ready = not blockers and release.get("release_channel") in {"production-candidate", "production"}
    return {"schema_version":"1.0","phase":35,"status":"DEPLOYMENT_READY" if ready else "DEPLOYMENT_BLOCKED","deployment_claim":False,"release":release,"checks":checks,"blockers":blockers,"live_deployment_verified":False}

def assess_from_files(release_path: str | Path, runtime_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    report = assess_deployment_readiness(load_json(release_path), load_json(runtime_path))
    Path(output_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report

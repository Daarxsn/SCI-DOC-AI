import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED_CHECKS = ("health", "readiness", "authentication", "tenant_isolation", "artifact_integrity", "pipeline_contract")

def fingerprint(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def run_smoke_checks(manifest: dict[str, Any]) -> dict[str, Any]:
    checks = []
    for name in REQUIRED_CHECKS:
        value = manifest.get(name)
        passed = value is True
        checks.append({"check": name, "passed": passed})
    failures = [c["check"] for c in checks if not c["passed"]]
    return {
        "schema_version": "1.0",
        "phase": 36,
        "status": "SMOKE_TEST_PASSED" if not failures else "SMOKE_TEST_FAILED",
        "deployment_claim": False,
        "live_deployment_verified": False,
        "checks": checks,
        "failures": failures,
        "manifest_fingerprint": fingerprint(manifest),
    }

def run_from_file(manifest_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    report = run_smoke_checks(manifest)
    Path(output_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report

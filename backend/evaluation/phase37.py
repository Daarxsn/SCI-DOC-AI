import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED_OBSERVABILITY_CONTROLS = (
    "structured_logging",
    "correlation_ids",
    "tenant_safe_telemetry",
    "latency_metrics",
    "error_metrics",
    "audit_events",
    "health_alert_contract",
)

def fingerprint(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def assess_observability(manifest: dict[str, Any]) -> dict[str, Any]:
    checks = [{"check": name, "configured": manifest.get(name) is True} for name in REQUIRED_OBSERVABILITY_CONTROLS]
    failures = [item["check"] for item in checks if not item["configured"]]
    return {
        "schema_version": "1.0",
        "phase": 37,
        "status": "OBSERVABILITY_READY" if not failures else "OBSERVABILITY_BLOCKED",
        "deployment_claim": False,
        "checks": checks,
        "failures": failures,
        "manifest_fingerprint": fingerprint(manifest),
    }

def assess_from_file(manifest_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    report = assess_observability(manifest)
    Path(output_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report

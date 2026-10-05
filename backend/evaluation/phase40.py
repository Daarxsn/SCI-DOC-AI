"""Phase 40 security and compliance readiness assessment.

Validates a declared security-control contract without claiming certification,
regulatory compliance, or a live security assessment.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

REQUIRED_CONTROLS = (
    "authentication",
    "authorization_least_privilege",
    "tenant_isolation",
    "tls_in_transit",
    "encryption_at_rest",
    "secret_management",
    "upload_validation",
    "rate_limiting",
    "audit_logging",
    "sensitive_data_redaction",
    "retention_policy",
    "dependency_security_scanning",
    "supply_chain_integrity",
    "incident_response",
    "security_testing",
)

REQUIRED_NUMERIC_CONTROLS = (
    "max_upload_size_mb",
    "retention_days",
)

def fingerprint(value: Any) -> str:
    canonical = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()

def assess_security(manifest: Mapping[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    for name in REQUIRED_CONTROLS:
        configured = manifest.get(name) is True
        checks.append({"check": name, "configured": configured})
        if not configured:
            failures.append(name)

    for name in REQUIRED_NUMERIC_CONTROLS:
        value = manifest.get(name)
        valid = isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0
        checks.append({"check": name, "configured": valid, "value": value})
        if not valid:
            failures.append(name)

    return {
        "schema_version": "1.0",
        "phase": 40,
        "status": "SECURITY_READY" if not failures else "SECURITY_BLOCKED",
        "deployment_claim": False,
        "compliance_claim": False,
        "live_security_assessment_verified": False,
        "checks": checks,
        "failures": sorted(set(failures)),
        "manifest_fingerprint": fingerprint(dict(manifest)),
    }

def assess_from_file(source: str | Path, output: str | Path) -> dict[str, Any]:
    source_path = Path(source)
    output_path = Path(output)
    manifest = json.loads(source_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("Phase 40 security manifest must be a JSON object")
    report = assess_security(manifest)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report

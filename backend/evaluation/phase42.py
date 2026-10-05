"""Phase 42 cloud deployment and environment-promotion readiness.

Validates the deployment contract needed to promote SCI-DOC AI through
staging/production environments. This gate does not claim that a live cloud
deployment exists.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

REQUIRED_CONTROLS = (
    "container_image_pinned",
    "environment_configuration",
    "secret_injection",
    "tls_termination",
    "health_check",
    "readiness_check",
    "persistent_storage",
    "queue_worker_topology",
    "network_boundary",
    "observability_export",
    "backup_policy",
    "rollback_strategy",
    "migration_strategy",
    "artifact_registry",
    "deployment_approval",
)

REQUIRED_TEXT_CONTROLS = (
    "environment",
    "image_reference",
    "rollback_version",
)

def fingerprint(value: Any) -> str:
    canonical = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()

def assess_deployment(manifest: Mapping[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    for name in REQUIRED_CONTROLS:
        configured = manifest.get(name) is True
        checks.append({"check": name, "configured": configured})
        if not configured:
            failures.append(name)

    for name in REQUIRED_TEXT_CONTROLS:
        value = manifest.get(name)
        configured = isinstance(value, str) and bool(value.strip())
        checks.append({"check": name, "configured": configured})
        if not configured:
            failures.append(name)

    return {
        "schema_version": "1.0",
        "phase": 42,
        "status": "DEPLOYMENT_CONTRACT_READY" if not failures else "DEPLOYMENT_CONTRACT_BLOCKED",
        "deployment_claim": False,
        "live_cloud_deployment_verified": False,
        "live_endpoint_verified": False,
        "rollback_verified": False,
        "checks": checks,
        "failures": sorted(set(failures)),
        "manifest_fingerprint": fingerprint(dict(manifest)),
    }

def assess_from_file(source: str | Path, output: str | Path) -> dict[str, Any]:
    source_path = Path(source)
    output_path = Path(output)
    manifest = json.loads(source_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("Phase 42 deployment manifest must be a JSON object")
    report = assess_deployment(manifest)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report

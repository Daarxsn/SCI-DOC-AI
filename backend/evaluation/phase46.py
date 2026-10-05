"""Phase 46 production evidence and customer acceptance readiness.

Validates the evidence contract required after a real deployment or pilot
execution. This gate never converts synthetic fixtures into live evidence.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

REQUIRED_CONTROLS = (
    "deployment_evidence",
    "endpoint_smoke_evidence",
    "real_document_execution",
    "benchmark_evidence",
    "security_evidence",
    "performance_evidence",
    "resilience_evidence",
    "artifact_integrity_evidence",
    "audit_evidence",
    "customer_acceptance_evidence",
    "support_handoff_evidence",
    "rollback_evidence",
)

REQUIRED_TEXT_CONTROLS = (
    "deployment_id",
    "release_version",
    "evidence_owner",
    "customer_or_pilot_id",
)

def fingerprint(value: Any) -> str:
    canonical = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()

def assess_production_evidence(manifest: Mapping[str, Any]) -> dict[str, Any]:
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
        "phase": 46,
        "status": "PRODUCTION_EVIDENCE_READY" if not failures else "PRODUCTION_EVIDENCE_BLOCKED",
        "deployment_claim": False,
        "real_production_evidence_verified": False,
        "customer_acceptance_verified": False,
        "benchmark_result_verified": False,
        "checks": checks,
        "failures": sorted(set(failures)),
        "manifest_fingerprint": fingerprint(dict(manifest)),
    }

def assess_from_file(source: str | Path, output: str | Path) -> dict[str, Any]:
    source_path = Path(source)
    output_path = Path(output)
    manifest = json.loads(source_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("Phase 46 production evidence manifest must be a JSON object")
    report = assess_production_evidence(manifest)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report

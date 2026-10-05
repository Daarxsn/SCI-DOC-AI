"""Phase 47 continuous operations and service-level governance readiness.

Validates the contract for operating SCI-DOC AI after launch: SLO ownership,
alerting, incident management, scheduled reviews, vulnerability remediation,
backup verification, and evidence retention.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

REQUIRED_CONTROLS = (
    "slo_ownership",
    "alerting_rules",
    "incident_management",
    "on_call_schedule",
    "vulnerability_remediation",
    "dependency_update_process",
    "backup_verification",
    "restore_drill_schedule",
    "access_review_schedule",
    "audit_review_schedule",
    "model_version_review",
    "benchmark_regression_review",
    "capacity_review",
    "security_review",
    "evidence_retention",
)

REQUIRED_TEXT_CONTROLS = (
    "service_owner",
    "incident_channel",
    "review_cadence",
    "escalation_policy",
)

def fingerprint(value: Any) -> str:
    canonical = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()

def assess_operations(manifest: Mapping[str, Any]) -> dict[str, Any]:
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
        "phase": 47,
        "status": "OPERATIONS_READY" if not failures else "OPERATIONS_BLOCKED",
        "deployment_claim": False,
        "live_operations_verified": False,
        "service_level_verified": False,
        "checks": checks,
        "failures": sorted(set(failures)),
        "manifest_fingerprint": fingerprint(dict(manifest)),
    }

def assess_from_file(source: str | Path, output: str | Path) -> dict[str, Any]:
    source_path = Path(source)
    output_path = Path(output)
    manifest = json.loads(source_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("Phase 47 operations manifest must be a JSON object")
    report = assess_operations(manifest)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report

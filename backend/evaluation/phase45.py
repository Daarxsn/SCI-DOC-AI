"""Phase 45 production launch governance and go-live readiness.

Validates the evidence contract required before an enterprise production
launch. This gate is intentionally fail-closed and does not claim that a live
deployment, customer acceptance, or regulatory certification exists.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

REQUIRED_CONTROLS = (
    "release_candidate_approved",
    "security_gate_passed",
    "capacity_gate_passed",
    "resilience_gate_passed",
    "deployment_contract_passed",
    "observability_gate_passed",
    "smoke_test_plan",
    "rollback_plan",
    "backup_restore_plan",
    "incident_response_plan",
    "on_call_ownership",
    "support_escalation_path",
    "data_retention_policy",
    "change_management_record",
    "go_live_approval",
)

REQUIRED_TEXT_CONTROLS = (
    "release_version",
    "deployment_environment",
    "release_commit",
    "approved_by",
    "go_live_window",
)

def fingerprint(value: Any) -> str:
    canonical = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()

def assess_go_live(manifest: Mapping[str, Any]) -> dict[str, Any]:
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
        "phase": 45,
        "status": "GO_LIVE_READY" if not failures else "GO_LIVE_BLOCKED",
        "deployment_claim": False,
        "live_production_verified": False,
        "customer_acceptance_verified": False,
        "compliance_certification_verified": False,
        "checks": checks,
        "failures": sorted(set(failures)),
        "manifest_fingerprint": fingerprint(dict(manifest)),
    }

def assess_from_file(source: str | Path, output: str | Path) -> dict[str, Any]:
    source_path = Path(source)
    output_path = Path(output)
    manifest = json.loads(source_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("Phase 45 go-live manifest must be a JSON object")
    report = assess_go_live(manifest)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report

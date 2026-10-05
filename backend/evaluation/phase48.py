"""Phase 48 operational excellence and continuous-improvement readiness.

Validates the governance contract for turning recurring operational evidence
into controlled improvement: postmortems, corrective actions, change-failure
review, customer feedback, runbook review, risk management, cost review,
improvement backlog, and accountable ownership.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

REQUIRED_CONTROLS = (
    "postmortem_process",
    "corrective_action_tracking",
    "change_failure_review",
    "customer_feedback_review",
    "runbook_review",
    "risk_register_review",
    "cost_efficiency_review",
    "improvement_backlog",
)
REQUIRED_TEXT_CONTROLS = (
    "improvement_owner",
    "improvement_cadence",
    "postmortem_sla",
    "decision_record_location",
)

def fingerprint(value: Any) -> str:
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()

def assess_improvement(manifest: Mapping[str, Any]) -> dict[str, Any]:
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
        "phase": 48,
        "status": "IMPROVEMENT_READY" if not failures else "IMPROVEMENT_BLOCKED",
        "deployment_claim": False,
        "live_improvement_verified": False,
        "business_outcomes_verified": False,
        "checks": checks,
        "failures": sorted(set(failures)),
        "manifest_fingerprint": fingerprint(dict(manifest)),
    }

def assess_from_file(source: str | Path, output: str | Path) -> dict[str, Any]:
    source_path = Path(source)
    output_path = Path(output)
    manifest = json.loads(source_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("Phase 48 improvement manifest must be a JSON object")
    report = assess_improvement(manifest)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report

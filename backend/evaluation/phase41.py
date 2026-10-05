"""Phase 41 enterprise client experience and operations readiness assessment.

Validates the contract required for a usable enterprise operations surface:
job visibility, human review, results/artifacts, tenant-safe responses,
operational diagnostics, and API discoverability.

This gate does not claim that a production UI is deployed or that real users
have completed acceptance testing.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

REQUIRED_CONTROLS = (
    "job_status_visibility",
    "human_review_queue",
    "result_artifact_access",
    "tenant_scoped_responses",
    "correlation_id_visibility",
    "structured_error_contract",
    "idempotency_visibility",
    "audit_event_visibility",
    "health_readiness_visibility",
    "api_documentation",
    "pagination_contract",
    "empty_state_contract",
    "accessibility_baseline",
    "responsive_layout_baseline",
    "user_acceptance_plan",
)

def fingerprint(value: Any) -> str:
    canonical = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()

def assess_client_experience(manifest: Mapping[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    for name in REQUIRED_CONTROLS:
        configured = manifest.get(name) is True
        checks.append({"check": name, "configured": configured})
        if not configured:
            failures.append(name)

    return {
        "schema_version": "1.0",
        "phase": 41,
        "status": "CLIENT_EXPERIENCE_READY" if not failures else "CLIENT_EXPERIENCE_BLOCKED",
        "deployment_claim": False,
        "ui_deployment_verified": False,
        "user_acceptance_verified": False,
        "checks": checks,
        "failures": sorted(set(failures)),
        "manifest_fingerprint": fingerprint(dict(manifest)),
    }

def assess_from_file(source: str | Path, output: str | Path) -> dict[str, Any]:
    source_path = Path(source)
    output_path = Path(output)
    manifest = json.loads(source_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("Phase 41 client experience manifest must be a JSON object")
    report = assess_client_experience(manifest)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report

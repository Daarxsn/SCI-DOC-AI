"""Phase 38 resilience readiness assessment.

This module validates that the production pipeline declares the minimum
resilience controls before live load/chaos verification.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

REQUIRED_CONTROLS = (
    "bounded_retries",
    "idempotent_jobs",
    "queue_recovery",
    "artifact_recovery",
    "dependency_timeout",
    "graceful_degradation",
    "failure_isolation",
)


def fingerprint(value: Any) -> str:
    """Return a deterministic SHA-256 fingerprint for JSON-compatible data."""
    canonical = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def assess_resilience(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Assess the declared resilience contract without claiming live resilience."""
    failures: list[str] = []

    for control in REQUIRED_CONTROLS:
        if manifest.get(control) is not True:
            failures.append(control)

    return {
        "schema_version": "1.0",
        "phase": 38,
        "status": "RESILIENCE_READY" if not failures else "RESILIENCE_BLOCKED",
        "deployment_claim": False,
        "live_resilience_verified": False,
        "checks": {control: manifest.get(control) is True for control in REQUIRED_CONTROLS},
        "failures": failures,
        "manifest_fingerprint": fingerprint(dict(manifest)),
    }


def assess_from_file(source: str | Path, output: str | Path) -> dict[str, Any]:
    """Load a JSON resilience manifest and write its readiness report."""
    source_path = Path(source)
    output_path = Path(output)

    manifest = json.loads(source_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("Phase 38 manifest must be a JSON object")

    report = assess_resilience(manifest)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report

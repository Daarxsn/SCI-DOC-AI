"""Phase 39 capacity and performance readiness assessment.

Validates a declared performance/SLO contract without claiming that the
service has been load-tested in a live environment.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

REQUIRED_BOOLEAN_CONTROLS = (
    "load_test_plan",
    "latency_slo",
    "throughput_slo",
    "concurrency_limit",
    "queue_capacity",
    "resource_headroom",
    "performance_observability",
)

REQUIRED_NUMERIC_CONTROLS = (
    "target_concurrency",
    "target_requests_per_second",
    "p95_latency_ms",
    "max_error_rate_percent",
)

def fingerprint(value: Any) -> str:
    canonical = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()

def assess_capacity(manifest: Mapping[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    for name in REQUIRED_BOOLEAN_CONTROLS:
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

    # Keep the gate internally consistent: a capacity contract must define
    # a non-zero concurrency target and a non-zero throughput target.
    if manifest.get("target_concurrency", 0) < 1:
        if "target_concurrency" not in failures:
            failures.append("target_concurrency")
    if manifest.get("target_requests_per_second", 0) < 1:
        if "target_requests_per_second" not in failures:
            failures.append("target_requests_per_second")

    return {
        "schema_version": "1.0",
        "phase": 39,
        "status": "CAPACITY_READY" if not failures else "CAPACITY_BLOCKED",
        "deployment_claim": False,
        "live_load_test_verified": False,
        "production_slo_verified": False,
        "checks": checks,
        "failures": sorted(set(failures)),
        "manifest_fingerprint": fingerprint(dict(manifest)),
    }

def assess_from_file(source: str | Path, output: str | Path) -> dict[str, Any]:
    source_path = Path(source)
    output_path = Path(output)
    manifest = json.loads(source_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("Phase 39 manifest must be a JSON object")
    report = assess_capacity(manifest)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report

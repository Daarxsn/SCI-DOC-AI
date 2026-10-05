import json
from pathlib import Path

from backend.evaluation.phase39 import assess_capacity, assess_from_file

BOOLEAN_CONTROLS = (
    "load_test_plan",
    "latency_slo",
    "throughput_slo",
    "concurrency_limit",
    "queue_capacity",
    "resource_headroom",
    "performance_observability",
)

NUMERIC_CONTROLS = (
    "target_concurrency",
    "target_requests_per_second",
    "p95_latency_ms",
    "max_error_rate_percent",
)

def valid_manifest():
    manifest = {name: True for name in BOOLEAN_CONTROLS}
    manifest.update({
        "target_concurrency": 20,
        "target_requests_per_second": 5,
        "p95_latency_ms": 500,
        "max_error_rate_percent": 2,
    })
    return manifest

def test_phase39_accepts_complete_capacity_contract():
    report = assess_capacity(valid_manifest())
    assert report["status"] == "CAPACITY_READY"
    assert report["failures"] == []
    assert report["deployment_claim"] is False
    assert report["live_load_test_verified"] is False
    assert report["production_slo_verified"] is False

def test_phase39_blocks_missing_load_test_plan():
    manifest = valid_manifest()
    manifest["load_test_plan"] = False
    report = assess_capacity(manifest)
    assert report["status"] == "CAPACITY_BLOCKED"
    assert "load_test_plan" in report["failures"]

def test_phase39_blocks_invalid_numeric_budget():
    manifest = valid_manifest()
    manifest["p95_latency_ms"] = 0
    report = assess_capacity(manifest)
    assert report["status"] == "CAPACITY_BLOCKED"
    assert "p95_latency_ms" in report["failures"]

def test_phase39_blocks_missing_concurrency_target():
    manifest = valid_manifest()
    del manifest["target_concurrency"]
    report = assess_capacity(manifest)
    assert "target_concurrency" in report["failures"]

def test_phase39_fingerprints_manifest_deterministically():
    first = assess_capacity(valid_manifest())
    second = assess_capacity(dict(reversed(list(valid_manifest().items()))))
    assert first["manifest_fingerprint"] == second["manifest_fingerprint"]

def test_phase39_file_runner(tmp_path: Path):
    source = tmp_path / "manifest.json"
    output = tmp_path / "report.json"
    source.write_text(json.dumps(valid_manifest()), encoding="utf-8")
    result = assess_from_file(source, output)
    assert output.exists()
    assert result["status"] == "CAPACITY_READY"
    assert result["manifest_fingerprint"]

import json
from pathlib import Path

from backend.evaluation.phase37 import assess_observability, assess_from_file
from backend.monitoring.observability import TelemetryEvent, serialize_event

REQUIRED = (
    "structured_logging", "correlation_ids", "tenant_safe_telemetry",
    "latency_metrics", "error_metrics", "audit_events", "health_alert_contract",
)

def valid_manifest():
    return {name: True for name in REQUIRED}

def test_phase37_accepts_complete_observability_contract():
    report = assess_observability(valid_manifest())
    assert report["status"] == "OBSERVABILITY_READY"
    assert report["failures"] == []
    assert report["deployment_claim"] is False

def test_phase37_blocks_missing_telemetry_control():
    manifest = valid_manifest()
    manifest["tenant_safe_telemetry"] = False
    report = assess_observability(manifest)
    assert report["status"] == "OBSERVABILITY_BLOCKED"
    assert "tenant_safe_telemetry" in report["failures"]

def test_phase37_serializes_structured_event():
    event = TelemetryEvent("pipeline.completed", "sci-doc-api", "corr-123", "tenant-a", "success", 42.5, {"job_id": "job-1"})
    payload = json.loads(serialize_event(event))
    assert payload["correlation_id"] == "corr-123"
    assert payload["tenant_id"] == "tenant-a"
    assert payload["duration_ms"] == 42.5

def test_phase37_file_runner(tmp_path: Path):
    source = tmp_path / "manifest.json"
    output = tmp_path / "report.json"
    source.write_text(json.dumps(valid_manifest()))
    result = assess_from_file(source, output)
    assert output.exists()
    assert result["manifest_fingerprint"]

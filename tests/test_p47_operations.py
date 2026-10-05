import json
from pathlib import Path

from backend.evaluation.phase47 import assess_operations, assess_from_file

REQUIRED = (
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

def valid_manifest():
    manifest = {name: True for name in REQUIRED}
    manifest.update({
        "service_owner": "platform-owner",
        "incident_channel": "ops-oncall",
        "review_cadence": "monthly",
        "escalation_policy": "sev1-sev4",
    })
    return manifest

def test_phase47_accepts_complete_operations_contract():
    report = assess_operations(valid_manifest())
    assert report["status"] == "OPERATIONS_READY"
    assert report["failures"] == []
    assert report["deployment_claim"] is False
    assert report["live_operations_verified"] is False
    assert report["service_level_verified"] is False

def test_phase47_blocks_missing_alerting():
    manifest = valid_manifest()
    manifest["alerting_rules"] = False
    report = assess_operations(manifest)
    assert report["status"] == "OPERATIONS_BLOCKED"
    assert "alerting_rules" in report["failures"]

def test_phase47_blocks_missing_restore_drills():
    manifest = valid_manifest()
    manifest["restore_drill_schedule"] = False
    report = assess_operations(manifest)
    assert "restore_drill_schedule" in report["failures"]

def test_phase47_blocks_missing_owner():
    manifest = valid_manifest()
    del manifest["service_owner"]
    report = assess_operations(manifest)
    assert "service_owner" in report["failures"]

def test_phase47_fingerprint_is_deterministic():
    first = assess_operations(valid_manifest())
    second = assess_operations(dict(reversed(list(valid_manifest().items()))))
    assert first["manifest_fingerprint"] == second["manifest_fingerprint"]

def test_phase47_file_runner(tmp_path: Path):
    source = tmp_path / "manifest.json"
    output = tmp_path / "report.json"
    source.write_text(json.dumps(valid_manifest()), encoding="utf-8")
    result = assess_from_file(source, output)
    assert output.exists()
    assert result["status"] == "OPERATIONS_READY"

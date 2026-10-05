import json
from pathlib import Path

from backend.evaluation.phase45 import assess_go_live, assess_from_file

REQUIRED = (
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

def valid_manifest():
    manifest = {name: True for name in REQUIRED}
    manifest.update({
        "release_version": "1.0.0",
        "deployment_environment": "production",
        "release_commit": "example-release-commit",
        "approved_by": "release-manager",
        "go_live_window": "2026-10-05T18:00:00+05:30",
    })
    return manifest

def test_phase45_accepts_complete_go_live_contract():
    report = assess_go_live(valid_manifest())
    assert report["status"] == "GO_LIVE_READY"
    assert report["failures"] == []
    assert report["deployment_claim"] is False
    assert report["live_production_verified"] is False
    assert report["customer_acceptance_verified"] is False

def test_phase45_blocks_missing_rollback():
    manifest = valid_manifest()
    manifest["rollback_plan"] = False
    report = assess_go_live(manifest)
    assert report["status"] == "GO_LIVE_BLOCKED"
    assert "rollback_plan" in report["failures"]

def test_phase45_blocks_missing_approval():
    manifest = valid_manifest()
    manifest["go_live_approval"] = False
    report = assess_go_live(manifest)
    assert "go_live_approval" in report["failures"]

def test_phase45_blocks_missing_release_version():
    manifest = valid_manifest()
    del manifest["release_version"]
    report = assess_go_live(manifest)
    assert "release_version" in report["failures"]

def test_phase45_fingerprint_is_deterministic():
    first = assess_go_live(valid_manifest())
    second = assess_go_live(dict(reversed(list(valid_manifest().items()))))
    assert first["manifest_fingerprint"] == second["manifest_fingerprint"]

def test_phase45_file_runner(tmp_path: Path):
    source = tmp_path / "manifest.json"
    output = tmp_path / "report.json"
    source.write_text(json.dumps(valid_manifest()), encoding="utf-8")
    result = assess_from_file(source, output)
    assert output.exists()
    assert result["status"] == "GO_LIVE_READY"

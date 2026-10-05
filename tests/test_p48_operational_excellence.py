import json
from pathlib import Path
from backend.evaluation.phase48 import assess_improvement, assess_from_file

REQUIRED = (
    "postmortem_process",
    "corrective_action_tracking",
    "change_failure_review",
    "customer_feedback_review",
    "runbook_review",
    "risk_register_review",
    "cost_efficiency_review",
    "improvement_backlog",
)

def valid_manifest():
    manifest = {name: True for name in REQUIRED}
    manifest.update({
        "improvement_owner": "platform-owner",
        "improvement_cadence": "monthly",
        "postmortem_sla": "five-business-days",
        "decision_record_location": "docs/decisions",
    })
    return manifest

def test_phase48_accepts_complete_improvement_contract():
    report = assess_improvement(valid_manifest())
    assert report["status"] == "IMPROVEMENT_READY"
    assert report["failures"] == []
    assert report["deployment_claim"] is False
    assert report["live_improvement_verified"] is False
    assert report["business_outcomes_verified"] is False

def test_phase48_blocks_missing_postmortem_process():
    manifest = valid_manifest()
    manifest["postmortem_process"] = False
    report = assess_improvement(manifest)
    assert report["status"] == "IMPROVEMENT_BLOCKED"
    assert "postmortem_process" in report["failures"]

def test_phase48_blocks_missing_cost_review():
    manifest = valid_manifest()
    manifest["cost_efficiency_review"] = False
    report = assess_improvement(manifest)
    assert "cost_efficiency_review" in report["failures"]

def test_phase48_blocks_missing_owner():
    manifest = valid_manifest()
    del manifest["improvement_owner"]
    report = assess_improvement(manifest)
    assert "improvement_owner" in report["failures"]

def test_phase48_fingerprint_is_deterministic():
    first = assess_improvement(valid_manifest())
    second = assess_improvement(dict(reversed(list(valid_manifest().items()))))
    assert first["manifest_fingerprint"] == second["manifest_fingerprint"]

def test_phase48_file_runner(tmp_path: Path):
    source = tmp_path / "manifest.json"
    output = tmp_path / "report.json"
    source.write_text(json.dumps(valid_manifest()), encoding="utf-8")
    result = assess_from_file(source, output)
    assert output.exists()
    assert result["status"] == "IMPROVEMENT_READY"

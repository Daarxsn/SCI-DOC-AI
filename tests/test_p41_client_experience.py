import json
from pathlib import Path

from backend.evaluation.phase41 import assess_client_experience, assess_from_file

REQUIRED = (
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

def valid_manifest():
    return {name: True for name in REQUIRED}

def test_phase41_accepts_complete_client_experience_contract():
    report = assess_client_experience(valid_manifest())
    assert report["status"] == "CLIENT_EXPERIENCE_READY"
    assert report["failures"] == []
    assert report["deployment_claim"] is False
    assert report["ui_deployment_verified"] is False
    assert report["user_acceptance_verified"] is False

def test_phase41_blocks_missing_review_queue():
    manifest = valid_manifest()
    manifest["human_review_queue"] = False
    report = assess_client_experience(manifest)
    assert report["status"] == "CLIENT_EXPERIENCE_BLOCKED"
    assert "human_review_queue" in report["failures"]

def test_phase41_blocks_missing_tenant_scoping():
    manifest = valid_manifest()
    manifest["tenant_scoped_responses"] = False
    report = assess_client_experience(manifest)
    assert "tenant_scoped_responses" in report["failures"]

def test_phase41_blocks_missing_accessibility_baseline():
    manifest = valid_manifest()
    del manifest["accessibility_baseline"]
    report = assess_client_experience(manifest)
    assert "accessibility_baseline" in report["failures"]

def test_phase41_fingerprint_is_deterministic():
    first = assess_client_experience(valid_manifest())
    second = assess_client_experience(dict(reversed(list(valid_manifest().items()))))
    assert first["manifest_fingerprint"] == second["manifest_fingerprint"]

def test_phase41_file_runner(tmp_path: Path):
    source = tmp_path / "manifest.json"
    output = tmp_path / "report.json"
    source.write_text(json.dumps(valid_manifest()), encoding="utf-8")
    result = assess_from_file(source, output)
    assert output.exists()
    assert result["status"] == "CLIENT_EXPERIENCE_READY"

import json
from pathlib import Path

from backend.evaluation.phase40 import assess_security, assess_from_file

REQUIRED = (
    "authentication",
    "authorization_least_privilege",
    "tenant_isolation",
    "tls_in_transit",
    "encryption_at_rest",
    "secret_management",
    "upload_validation",
    "rate_limiting",
    "audit_logging",
    "sensitive_data_redaction",
    "retention_policy",
    "dependency_security_scanning",
    "supply_chain_integrity",
    "incident_response",
    "security_testing",
)

def valid_manifest():
    manifest = {name: True for name in REQUIRED}
    manifest.update({"max_upload_size_mb": 50, "retention_days": 30})
    return manifest

def test_phase40_accepts_complete_security_contract():
    report = assess_security(valid_manifest())
    assert report["status"] == "SECURITY_READY"
    assert report["failures"] == []
    assert report["deployment_claim"] is False
    assert report["compliance_claim"] is False
    assert report["live_security_assessment_verified"] is False

def test_phase40_blocks_missing_authentication():
    manifest = valid_manifest()
    manifest["authentication"] = False
    report = assess_security(manifest)
    assert report["status"] == "SECURITY_BLOCKED"
    assert "authentication" in report["failures"]

def test_phase40_blocks_invalid_retention():
    manifest = valid_manifest()
    manifest["retention_days"] = 0
    report = assess_security(manifest)
    assert report["status"] == "SECURITY_BLOCKED"
    assert "retention_days" in report["failures"]

def test_phase40_blocks_missing_control():
    manifest = valid_manifest()
    del manifest["supply_chain_integrity"]
    report = assess_security(manifest)
    assert "supply_chain_integrity" in report["failures"]

def test_phase40_fingerprint_is_deterministic():
    first = assess_security(valid_manifest())
    second = assess_security(dict(reversed(list(valid_manifest().items()))))
    assert first["manifest_fingerprint"] == second["manifest_fingerprint"]

def test_phase40_file_runner(tmp_path: Path):
    source = tmp_path / "manifest.json"
    output = tmp_path / "report.json"
    source.write_text(json.dumps(valid_manifest()), encoding="utf-8")
    result = assess_from_file(source, output)
    assert output.exists()
    assert result["status"] == "SECURITY_READY"

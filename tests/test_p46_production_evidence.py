import json
from pathlib import Path

from backend.evaluation.phase46 import assess_production_evidence, assess_from_file

REQUIRED = (
    "deployment_evidence",
    "endpoint_smoke_evidence",
    "real_document_execution",
    "benchmark_evidence",
    "security_evidence",
    "performance_evidence",
    "resilience_evidence",
    "artifact_integrity_evidence",
    "audit_evidence",
    "customer_acceptance_evidence",
    "support_handoff_evidence",
    "rollback_evidence",
)

def valid_manifest():
    manifest = {name: True for name in REQUIRED}
    manifest.update({
        "deployment_id": "deployment-evidence-placeholder",
        "release_version": "1.0.0",
        "evidence_owner": "release-manager",
        "customer_or_pilot_id": "pilot-placeholder",
    })
    return manifest

def test_phase46_accepts_complete_evidence_contract():
    report = assess_production_evidence(valid_manifest())
    assert report["status"] == "PRODUCTION_EVIDENCE_READY"
    assert report["failures"] == []
    assert report["deployment_claim"] is False
    assert report["real_production_evidence_verified"] is False
    assert report["customer_acceptance_verified"] is False

def test_phase46_blocks_missing_real_document_execution():
    manifest = valid_manifest()
    manifest["real_document_execution"] = False
    report = assess_production_evidence(manifest)
    assert report["status"] == "PRODUCTION_EVIDENCE_BLOCKED"
    assert "real_document_execution" in report["failures"]

def test_phase46_blocks_missing_customer_acceptance():
    manifest = valid_manifest()
    manifest["customer_acceptance_evidence"] = False
    report = assess_production_evidence(manifest)
    assert "customer_acceptance_evidence" in report["failures"]

def test_phase46_blocks_missing_deployment_id():
    manifest = valid_manifest()
    del manifest["deployment_id"]
    report = assess_production_evidence(manifest)
    assert "deployment_id" in report["failures"]

def test_phase46_fingerprint_is_deterministic():
    first = assess_production_evidence(valid_manifest())
    second = assess_production_evidence(dict(reversed(list(valid_manifest().items()))))
    assert first["manifest_fingerprint"] == second["manifest_fingerprint"]

def test_phase46_file_runner(tmp_path: Path):
    source = tmp_path / "manifest.json"
    output = tmp_path / "report.json"
    source.write_text(json.dumps(valid_manifest()), encoding="utf-8")
    result = assess_from_file(source, output)
    assert output.exists()
    assert result["status"] == "PRODUCTION_EVIDENCE_READY"

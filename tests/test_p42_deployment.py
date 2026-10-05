import json
from pathlib import Path

from backend.evaluation.phase42 import assess_deployment, assess_from_file

REQUIRED = (
    "container_image_pinned",
    "environment_configuration",
    "secret_injection",
    "tls_termination",
    "health_check",
    "readiness_check",
    "persistent_storage",
    "queue_worker_topology",
    "network_boundary",
    "observability_export",
    "backup_policy",
    "rollback_strategy",
    "migration_strategy",
    "artifact_registry",
    "deployment_approval",
)

def valid_manifest():
    manifest = {name: True for name in REQUIRED}
    manifest.update({
        "environment": "staging",
        "image_reference": "registry.example/sci-doc-ai@sha256:example",
        "rollback_version": "1.0.0",
    })
    return manifest

def test_phase42_accepts_complete_deployment_contract():
    report = assess_deployment(valid_manifest())
    assert report["status"] == "DEPLOYMENT_CONTRACT_READY"
    assert report["failures"] == []
    assert report["deployment_claim"] is False
    assert report["live_cloud_deployment_verified"] is False

def test_phase42_blocks_missing_rollback():
    manifest = valid_manifest()
    manifest["rollback_strategy"] = False
    report = assess_deployment(manifest)
    assert report["status"] == "DEPLOYMENT_CONTRACT_BLOCKED"
    assert "rollback_strategy" in report["failures"]

def test_phase42_blocks_missing_environment():
    manifest = valid_manifest()
    del manifest["environment"]
    report = assess_deployment(manifest)
    assert "environment" in report["failures"]

def test_phase42_blocks_missing_storage():
    manifest = valid_manifest()
    manifest["persistent_storage"] = False
    report = assess_deployment(manifest)
    assert "persistent_storage" in report["failures"]

def test_phase42_fingerprint_is_deterministic():
    first = assess_deployment(valid_manifest())
    second = assess_deployment(dict(reversed(list(valid_manifest().items()))))
    assert first["manifest_fingerprint"] == second["manifest_fingerprint"]

def test_phase42_file_runner(tmp_path: Path):
    source = tmp_path / "manifest.json"
    output = tmp_path / "report.json"
    source.write_text(json.dumps(valid_manifest()), encoding="utf-8")
    result = assess_from_file(source, output)
    assert output.exists()
    assert result["status"] == "DEPLOYMENT_CONTRACT_READY"

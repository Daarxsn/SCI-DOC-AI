import json
from pathlib import Path
from backend.evaluation.phase36 import run_smoke_checks, run_from_file

def valid_manifest():
    return {name: True for name in ("health","readiness","authentication","tenant_isolation","artifact_integrity","pipeline_contract")}

def test_phase36_passes_complete_smoke_manifest():
    report = run_smoke_checks(valid_manifest())
    assert report["status"] == "SMOKE_TEST_PASSED"
    assert report["deployment_claim"] is False
    assert report["live_deployment_verified"] is False
    assert report["failures"] == []

def test_phase36_fails_missing_authentication():
    manifest = valid_manifest()
    manifest["authentication"] = False
    report = run_smoke_checks(manifest)
    assert report["status"] == "SMOKE_TEST_FAILED"
    assert "authentication" in report["failures"]

def test_phase36_fails_missing_field():
    manifest = valid_manifest()
    del manifest["pipeline_contract"]
    report = run_smoke_checks(manifest)
    assert report["status"] == "SMOKE_TEST_FAILED"
    assert "pipeline_contract" in report["failures"]

def test_phase36_file_runner(tmp_path: Path):
    manifest = valid_manifest()
    source = tmp_path / "manifest.json"
    output = tmp_path / "report.json"
    source.write_text(json.dumps(manifest))
    result = run_from_file(source, output)
    assert output.exists()
    assert result["manifest_fingerprint"]

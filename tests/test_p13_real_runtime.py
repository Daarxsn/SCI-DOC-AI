import json
from pathlib import Path
from backend.evaluation.phase13 import build_phase13_report, load_manifest, validate_cases

def test_phase13_manifest_validation_and_checksum(tmp_path):
    asset = tmp_path / "sample.png"
    asset.write_bytes(b"phase13-fixture")
    manifest = {"dataset_id": "phase13-fixture", "version": "1.0.0", "cases": [{"case_id": "physics-hi-001", "input_path": "sample.png", "domain": "physics", "target_language": "hi"}]}
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    cases = validate_cases(load_manifest(manifest_path), tmp_path)
    assert cases[0]["ready"] is True
    assert cases[0]["checksum_sha256"]

def test_phase13_missing_assets_block_execution():
    manifest = {"dataset_id": "phase13-fixture", "version": "1.0.0", "cases": [{"case_id": "biology-mr-001", "input_path": "missing.png", "domain": "biology", "target_language": "mr"}]}
    report = build_phase13_report(manifest, validate_cases(manifest, Path(".")))
    assert report["execution_status"] == "BLOCKED_MISSING_ASSETS"
    assert report["accuracy_claim"] is False
    assert len(report["provenance"]["fingerprint"]) == 64

import json
from backend.evaluation.phase22 import execute_phase22

def test_phase22_fails_closed_and_records_readiness(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({
        "dataset_id": "x",
        "version": "1",
        "cases": [{
            "case_id": "mathematics-hi-001",
            "input_path": "missing.png",
            "reference_path": "missing.json",
            "annotation_path": "missing.json"
        }]
    }))
    result = execute_phase22(manifest, tmp_path, tmp_path / "release")
    assert result["execution_status"] == "BLOCKED"
    assert result["accuracy_claim"] is False
    assert result["evidence_packaged"] is False
    saved = json.loads((tmp_path / "release" / "phase22-result.json").read_text())
    assert saved["execution_status"] == "BLOCKED"

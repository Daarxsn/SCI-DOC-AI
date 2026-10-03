import json
from pathlib import Path
import pytest
from backend.evaluation.phase27 import build_intake_manifest

def write_metadata(tmp_path: Path, case: dict) -> Path:
    path = tmp_path / "metadata.json"
    path.write_text(json.dumps({"dataset_id": "test-intake", "version": "1.0.0", "cases": [case]}))
    return path

def valid_case():
    return {
        "case_id": "mathematics-hi-test-001",
        "source_path": "source/sample.png",
        "domain": "mathematics",
        "source_language": "en",
        "target_language": "hi",
        "rights_status": "owned",
        "scientific_document_status": "REAL_DOCUMENT_PENDING_VERIFICATION",
    }

def test_phase27_validates_and_hashes_source(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "sample.png").write_bytes(b"scientific-document-fixture")
    metadata = write_metadata(tmp_path, valid_case())
    output = tmp_path / "intake.json"
    manifest = build_intake_manifest(metadata, tmp_path, output)
    assert manifest["status"] == "INTAKE_VALIDATED"
    assert manifest["scientific_accuracy_claim"] is False
    assert manifest["case_count"] == 1
    assert len(manifest["cases"][0]["source_sha256"]) == 64
    assert output.exists()

def test_phase27_rejects_missing_source(tmp_path):
    metadata = write_metadata(tmp_path, valid_case())
    with pytest.raises(ValueError, match="does not exist"):
        build_intake_manifest(metadata, tmp_path, tmp_path / "out.json")

def test_phase27_rejects_unverified_rights(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "sample.png").write_bytes(b"x")
    case = valid_case()
    case["rights_status"] = "unknown"
    metadata = write_metadata(tmp_path, case)
    with pytest.raises(ValueError, match="rights status"):
        build_intake_manifest(metadata, tmp_path, tmp_path / "out.json")

def test_phase27_rejects_non_science_domain(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "sample.png").write_bytes(b"x")
    case = valid_case()
    case["domain"] = "history"
    metadata = write_metadata(tmp_path, case)
    with pytest.raises(ValueError, match="unsupported domain"):
        build_intake_manifest(metadata, tmp_path, tmp_path / "out.json")

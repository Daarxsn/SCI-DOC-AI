import json
from pathlib import Path
import pytest
from backend.evaluation.phase28 import build_ground_truth_manifest

def setup_case(tmp_path: Path, verified=True):
    source = tmp_path / "source"
    refs = tmp_path / "references"
    anns = tmp_path / "annotations"
    source.mkdir()
    refs.mkdir()
    anns.mkdir()
    (source / "sample.png").write_bytes(b"real-document-fixture")
    case = {
        "case_id": "mathematics-hi-001",
        "source_path": "source/sample.png",
        "scientific_document_status": "REAL_DOCUMENT_PENDING_VERIFICATION",
        "reference_path": "references/sample.json",
        "annotation_path": "annotations/sample.json",
    }
    (refs / "sample.json").write_text(json.dumps({
        "case_id": case["case_id"], "text": "Solve x + 2 = 5.", "verified": verified
    }))
    (anns / "sample.json").write_text(json.dumps({
        "case_id": case["case_id"], "verified": verified,
        "equations": [{"id": "eq-1", "ground_truth": "x+2=5"}],
        "diagrams": [], "layout": [{"type": "text", "bbox": [0, 0, 100, 50]}]
    }))
    intake = tmp_path / "intake.json"
    intake.write_text(json.dumps({
        "dataset_id": "sci-doc-real-intake", "version": "1.0.0",
        "status": "INTAKE_VALIDATED", "cases": [case]
    }))
    return intake

def test_phase28_verifies_ground_truth(tmp_path):
    intake = setup_case(tmp_path)
    result = build_ground_truth_manifest(intake, tmp_path, tmp_path / "out.json")
    assert result["status"] == "GROUND_TRUTH_VERIFIED"
    assert result["scientific_accuracy_claim"] is False
    assert result["cases"][0]["ground_truth_status"] == "VERIFIED"

def test_phase28_rejects_unverified_reference(tmp_path):
    intake = setup_case(tmp_path, verified=False)
    with pytest.raises(ValueError, match="ground truth must be VERIFIED"):
        build_ground_truth_manifest(intake, tmp_path, tmp_path / "out.json")

def test_phase28_rejects_missing_annotation(tmp_path):
    intake = setup_case(tmp_path)
    (tmp_path / "annotations/sample.json").unlink()
    with pytest.raises(ValueError, match="annotation file does not exist"):
        build_ground_truth_manifest(intake, tmp_path, tmp_path / "out.json")

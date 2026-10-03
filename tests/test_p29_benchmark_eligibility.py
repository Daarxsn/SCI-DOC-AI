import json
from pathlib import Path
import pytest

from backend.evaluation.phase28 import build_ground_truth_manifest, sha256_file
from backend.evaluation.phase29 import build_benchmark_eligibility_manifest

def setup_case(tmp_path: Path):
    source = tmp_path / "source"
    refs = tmp_path / "references"
    anns = tmp_path / "annotations"
    source.mkdir()
    refs.mkdir()
    anns.mkdir()
    source_file = source / "sample.png"
    source_file.write_bytes(b"real-document-fixture")
    case = {
        "case_id": "mathematics-hi-001",
        "source_path": "source/sample.png",
        "domain": "mathematics",
        "source_language": "en",
        "target_language": "hi",
        "rights_status": "permission_granted",
        "scientific_document_status": "REAL_DOCUMENT_PENDING_VERIFICATION",
        "reference_path": "references/sample.json",
        "annotation_path": "annotations/sample.json",
    }
    (refs / "sample.json").write_text(json.dumps({"case_id": case["case_id"], "text": "Solve x + 2 = 5.", "verified": True}))
    (anns / "sample.json").write_text(json.dumps({
        "case_id": case["case_id"], "verified": True,
        "equations": [{"id": "eq-1", "ground_truth": "x+2=5"}],
        "diagrams": [], "layout": [{"type": "text", "bbox": [0, 0, 100, 50]}]
    }))
    case["source_sha256"] = sha256_file(source_file)
    intake = tmp_path / "intake.json"
    intake.write_text(json.dumps({"dataset_id": "sci-doc-real-intake", "version": "1.0.0", "status": "INTAKE_VALIDATED", "cases": [case]}))
    gt = tmp_path / "ground-truth.json"
    build_ground_truth_manifest(intake, tmp_path, gt)
    return intake, gt

def test_phase29_marks_verified_case_eligible(tmp_path):
    intake, gt = setup_case(tmp_path)
    result = build_benchmark_eligibility_manifest(intake, gt, tmp_path, tmp_path / "eligible.json")
    assert result["status"] == "BENCHMARK_ELIGIBLE"
    assert result["scientific_accuracy_claim"] is False
    assert result["cases"][0]["benchmark_eligible"] is True

def test_phase29_rejects_source_tampering(tmp_path):
    intake, gt = setup_case(tmp_path)
    (tmp_path / "source/sample.png").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        build_benchmark_eligibility_manifest(intake, gt, tmp_path, tmp_path / "out.json")

def test_phase29_rejects_case_set_mismatch(tmp_path):
    intake, gt = setup_case(tmp_path)
    payload = json.loads(gt.read_text())
    payload["cases"][0]["case_id"] = "different-case"
    gt.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="case IDs do not match"):
        build_benchmark_eligibility_manifest(intake, gt, tmp_path, tmp_path / "out.json")

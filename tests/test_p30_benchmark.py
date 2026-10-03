import json
from pathlib import Path
from backend.evaluation.phase30 import readiness, build_phase19_manifest

def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")

def setup_case(tmp_path: Path):
    source = tmp_path / "source/sample.png"
    reference = tmp_path / "references/sample.json"
    annotation = tmp_path / "annotations/sample.json"
    source.parent.mkdir(parents=True); reference.parent.mkdir(parents=True); annotation.parent.mkdir(parents=True)
    source.write_bytes(b"REAL-SCIENTIFIC-DOCUMENT-FIXTURE")
    write_json(reference, {"case_id":"mathematics-hi-real-001","verified":True,"ocr_text":"Solve x + 2 = 5.","translation_text":"x + 2 = 5 हल करें।"})
    write_json(annotation, {"case_id":"mathematics-hi-real-001","verified":True,"equations":[],"diagrams":[],"layout":[]})
    import hashlib
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    case={"case_id":"mathematics-hi-real-001","source_path":"source/sample.png","source_sha256":sha,"scientific_document_status":"REAL_DOCUMENT_VERIFIED","domain":"mathematics","source_language":"en","target_language":"hi","rights_status":"permission_granted"}
    intake=tmp_path/"intake.json"; write_json(intake,{"status":"INTAKE_VALIDATED","dataset_id":"real-intake","version":"1.0.0","cases":[case]})
    gt=tmp_path/"ground-truth.json"; write_json(gt,{"status":"GROUND_TRUTH_VERIFIED","dataset_id":"real-intake","version":"1.0.0","scientific_accuracy_claim":False,"cases":[{"case_id":"mathematics-hi-real-001","source_sha256":sha,"reference":{"path":"references/sample.json","sha256":hashlib.sha256(reference.read_bytes()).hexdigest()},"annotations":{"path":"annotations/sample.json","sha256":hashlib.sha256(annotation.read_bytes()).hexdigest()},"ground_truth_status":"VERIFIED"}]})
    eligibility=tmp_path/"eligibility.json"; write_json(eligibility,{"status":"BENCHMARK_ELIGIBLE","cases":[{"case_id":"mathematics-hi-real-001"}]})
    return intake,gt,eligibility

def test_phase30_requires_verified_real_document(tmp_path):
    intake,gt,eligibility=setup_case(tmp_path); payload=json.loads(intake.read_text()); payload["cases"][0]["scientific_document_status"]="REAL_DOCUMENT_PENDING_VERIFICATION"; intake.write_text(json.dumps(payload))
    result=readiness(intake,gt,eligibility,tmp_path)
    assert result["ready"] is False and "REAL_DOCUMENT_VERIFIED" in result["reason"]

def test_phase30_requires_measured_reference_fields(tmp_path):
    intake,gt,eligibility=setup_case(tmp_path); reference=tmp_path/"references/sample.json"; payload=json.loads(reference.read_text()); del payload["translation_text"]; reference.write_text(json.dumps(payload))
    result=readiness(intake,gt,eligibility,tmp_path)
    assert result["ready"] is False and "ocr_text and translation_text" in result["reason"]

def test_phase30_builds_benchmark_manifest(tmp_path):
    intake,gt,eligibility=setup_case(tmp_path); result=readiness(intake,gt,eligibility,tmp_path)
    assert result["ready"] is True
    manifest=build_phase19_manifest(intake,gt,tmp_path)
    assert manifest["cases"][0]["input_path"]=="source/sample.png"

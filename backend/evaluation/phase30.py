import json
from pathlib import Path
from typing import Any
from backend.core.config import Settings
from backend.evaluation.phase19 import execute_benchmark_result

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def readiness(intake_path: str | Path, ground_truth_path: str | Path, eligibility_path: str | Path, root: str | Path) -> dict[str, Any]:
    root_path = Path(root)
    intake = load_json(Path(intake_path))
    ground_truth = load_json(Path(ground_truth_path))
    eligibility = load_json(Path(eligibility_path))
    if intake.get("status") != "INTAKE_VALIDATED":
        return {"ready": False, "reason": "Phase 27 intake is not validated"}
    if ground_truth.get("status") != "GROUND_TRUTH_VERIFIED":
        return {"ready": False, "reason": "Phase 28 ground truth is not verified"}
    if eligibility.get("status") != "BENCHMARK_ELIGIBLE":
        return {"ready": False, "reason": "Phase 29 benchmark eligibility is not established"}
    cases = intake.get("cases", [])
    if len(cases) != 1:
        return {"ready": False, "reason": "Phase 30 requires exactly one real benchmark case", "case_count": len(cases)}
    case = cases[0]
    if case.get("scientific_document_status") != "REAL_DOCUMENT_VERIFIED":
        return {"ready": False, "reason": "source is not marked REAL_DOCUMENT_VERIFIED", "case_id": case.get("case_id")}
    gt_cases = {c["case_id"]: c for c in ground_truth.get("cases", [])}
    eligible_cases = {c["case_id"]: c for c in eligibility.get("cases", [])}
    case_id = case["case_id"]
    if case_id not in gt_cases or case_id not in eligible_cases:
        return {"ready": False, "reason": "case is missing from Phase 28 or Phase 29 manifests", "case_id": case_id}
    reference_path = root_path / gt_cases[case_id]["reference"]["path"]
    annotation_path = root_path / gt_cases[case_id]["annotations"]["path"]
    source_path = root_path / case["source_path"]
    missing = [str(p) for p in (source_path, reference_path, annotation_path) if not p.is_file()]
    if missing:
        return {"ready": False, "reason": "required benchmark assets are missing", "missing": missing, "case_id": case_id}
    reference = load_json(reference_path)
    annotation = load_json(annotation_path)
    if reference.get("verified") is not True or annotation.get("verified") is not True:
        return {"ready": False, "reason": "reference and annotation must be explicitly verified", "case_id": case_id}
    if not reference.get("ocr_text") or not reference.get("translation_text"):
        return {"ready": False, "reason": "reference requires ocr_text and translation_text for measured benchmarking", "case_id": case_id}
    return {"ready": True, "case_id": case_id, "source_path": case["source_path"], "reference_path": gt_cases[case_id]["reference"]["path"], "annotation_path": gt_cases[case_id]["annotations"]["path"], "source_sha256": case["source_sha256"]}

def build_phase19_manifest(intake_path: str | Path, ground_truth_path: str | Path, root: str | Path) -> dict[str, Any]:
    intake = load_json(Path(intake_path))
    ground_truth = load_json(Path(ground_truth_path))
    case = intake["cases"][0]
    gt = {c["case_id"]: c for c in ground_truth["cases"]}[case["case_id"]]
    return {"dataset_id": ground_truth["dataset_id"], "version": ground_truth["version"], "benchmark_id": f"phase30-{ground_truth['dataset_id']}-{ground_truth['version']}", "cases": [{
        "case_id": case["case_id"], "input_path": case["source_path"], "reference_path": gt["reference"]["path"], "annotation_path": gt["annotations"]["path"], "checksum_sha256": case["source_sha256"], "source_language": case["source_language"], "target_language": case["target_language"], "domain": case["domain"], "document_type": case.get("document_type", "question_paper")
    }]}

def execute_phase30(intake_path: str | Path, ground_truth_path: str | Path, eligibility_path: str | Path, root: str | Path, output_dir: str | Path, config: Settings) -> dict[str, Any]:
    state = readiness(intake_path, ground_truth_path, eligibility_path, root)
    if not state["ready"]:
        return {"phase": 30, "execution_status": "BLOCKED", "accuracy_claim": False, "readiness": state}
    manifest = build_phase19_manifest(intake_path, ground_truth_path, root)
    manifest_path = Path(output_dir) / "phase30-benchmark-manifest.json"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    result = execute_benchmark_result(manifest_path, root, output_dir, config)
    return {"phase": 30, "execution_status": "EXECUTED", "accuracy_claim": True, "readiness": state, "benchmark": result["benchmark"], "benchmark_result_path": str(Path(output_dir) / "benchmark-result.json")}

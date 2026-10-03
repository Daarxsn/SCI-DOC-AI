import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def verify_asset(path: Path, expected_sha256: str, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"{label} file does not exist: {path}")
    actual = sha256_file(path)
    if actual != expected_sha256:
        raise ValueError(f"{label} SHA-256 mismatch")
    return {"path": str(path), "sha256": actual}

def build_benchmark_eligibility_manifest(intake_path: str | Path, ground_truth_path: str | Path, root: str | Path, output_path: str | Path) -> dict[str, Any]:
    root_path = Path(root)
    intake = load_json(Path(intake_path))
    ground_truth = load_json(Path(ground_truth_path))
    if intake.get("status") != "INTAKE_VALIDATED":
        raise ValueError("Phase 29 requires an INTAKE_VALIDATED Phase 27 manifest")
    if ground_truth.get("status") != "GROUND_TRUTH_VERIFIED":
        raise ValueError("Phase 29 requires a GROUND_TRUTH_VERIFIED Phase 28 manifest")
    if ground_truth.get("scientific_accuracy_claim") is not False:
        raise ValueError("Phase 29 ground-truth manifest must not claim scientific accuracy")
    intake_cases = {case["case_id"]: case for case in intake.get("cases", [])}
    gt_cases = {case["case_id"]: case for case in ground_truth.get("cases", [])}
    if not intake_cases:
        raise ValueError("Phase 29 requires at least one intake case")
    if set(intake_cases) != set(gt_cases):
        raise ValueError("Phase 27 and Phase 28 case IDs do not match")
    normalized = []
    for case_id, intake_case in intake_cases.items():
        gt_case = gt_cases[case_id]
        if gt_case.get("ground_truth_status") != "VERIFIED":
            raise ValueError(f"ground truth is not VERIFIED for case {case_id}")
        source = root_path / intake_case["source_path"]
        source_asset = verify_asset(source, intake_case["source_sha256"], f"source for {case_id}")
        if gt_case.get("source_sha256") != source_asset["sha256"]:
            raise ValueError(f"Phase 28 source SHA-256 does not match Phase 27 for case {case_id}")
        reference_asset = verify_asset(root_path / gt_case["reference"]["path"], gt_case["reference"]["sha256"], f"reference for {case_id}")
        annotation_asset = verify_asset(root_path / gt_case["annotations"]["path"], gt_case["annotations"]["sha256"], f"annotation for {case_id}")
        normalized.append({
            "case_id": case_id,
            "source_sha256": source_asset["sha256"],
            "reference_sha256": reference_asset["sha256"],
            "annotation_sha256": annotation_asset["sha256"],
            "domain": intake_case["domain"],
            "source_language": intake_case["source_language"],
            "target_language": intake_case["target_language"],
            "rights_status": intake_case["rights_status"],
            "benchmark_eligible": True,
        })
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "phase": 29,
        "dataset_id": ground_truth["dataset_id"],
        "version": ground_truth["version"],
        "status": "BENCHMARK_ELIGIBLE",
        "scientific_accuracy_claim": False,
        "case_count": len(normalized),
        "cases": normalized,
    }
    Path(output_path).write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest

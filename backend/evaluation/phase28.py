import hashlib
import json
from pathlib import Path
from typing import Any

ANNOTATION_SCHEMA_VERSION = "1.0"
REQUIRED_REFERENCE_FIELDS = {"case_id", "text", "verified"}
REQUIRED_ANNOTATION_FIELDS = {"case_id", "verified"}

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def validate_reference(case: dict[str, Any], path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"reference file does not exist: {path}")
    reference = load_json(path)
    missing = sorted(REQUIRED_REFERENCE_FIELDS - set(reference))
    if missing:
        raise ValueError(f"reference missing required fields: {missing}")
    if reference["case_id"] != case["case_id"]:
        raise ValueError("reference case_id does not match intake case")
    if reference["verified"] is not True:
        raise ValueError("reference ground truth must be VERIFIED")
    if not isinstance(reference["text"], str) or not reference["text"].strip():
        raise ValueError("reference text must be non-empty")
    return {"path": str(case["reference_path"]), "sha256": sha256_file(path), "verified": True}

def validate_annotations(case: dict[str, Any], path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"annotation file does not exist: {path}")
    annotation = load_json(path)
    missing = sorted(REQUIRED_ANNOTATION_FIELDS - set(annotation))
    if missing:
        raise ValueError(f"annotation missing required fields: {missing}")
    if annotation["case_id"] != case["case_id"]:
        raise ValueError("annotation case_id does not match intake case")
    if annotation["verified"] is not True:
        raise ValueError("scientific annotations must be VERIFIED")
    for field in ("equations", "diagrams", "layout"):
        if field in annotation and not isinstance(annotation[field], list):
            raise ValueError(f"annotation field '{field}' must be a list")
    return {"path": str(case["annotation_path"]), "sha256": sha256_file(path), "verified": True}

def build_ground_truth_manifest(intake_path: str | Path, root: str | Path, output_path: str | Path) -> dict[str, Any]:
    root_path = Path(root)
    intake = load_json(Path(intake_path))
    if intake.get("status") != "INTAKE_VALIDATED":
        raise ValueError("Phase 28 requires an INTAKE_VALIDATED Phase 27 manifest")
    cases = intake.get("cases", [])
    if not cases:
        raise ValueError("Phase 28 requires at least one intake case")
    normalized = []
    for case in cases:
        if case.get("scientific_document_status") not in {"REAL_DOCUMENT_PENDING_VERIFICATION", "REAL_DOCUMENT_VERIFIED"}:
            raise ValueError("case is not eligible for ground-truth annotation")
        reference = validate_reference(case, root_path / case["reference_path"])
        annotations = validate_annotations(case, root_path / case["annotation_path"])
        normalized.append({
            "case_id": case["case_id"],
            "source_sha256": case["source_sha256"],
            "reference": reference,
            "annotations": annotations,
            "ground_truth_status": "VERIFIED",
        })
    manifest = {
        "schema_version": ANNOTATION_SCHEMA_VERSION,
        "phase": 28,
        "dataset_id": intake["dataset_id"],
        "version": intake["version"],
        "status": "GROUND_TRUTH_VERIFIED",
        "scientific_accuracy_claim": False,
        "case_count": len(normalized),
        "cases": normalized,
    }
    Path(output_path).write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest

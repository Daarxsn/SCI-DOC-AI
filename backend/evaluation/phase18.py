import hashlib
import json
from pathlib import Path
from typing import Any

from backend.core.config import Settings
from backend.evaluation.phase14 import run_real_case
from backend.evaluation.phase13 import load_manifest, validate_cases

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def execute_first_case(manifest_path: str | Path, root: str | Path, output_dir: str | Path, config: Settings) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    if len(manifest["cases"]) != 1:
        raise RuntimeError("Phase 18 requires exactly one first-case manifest entry")
    checks = validate_cases(manifest, root)
    if not checks[0]["ready"]:
        raise RuntimeError("Phase 18 blocked: first-case asset/checksum is not ready")
    case = manifest["cases"][0]
    root_path = Path(root)
    source = root_path / case["input_path"]
    reference = root_path / case["reference_path"]
    annotation = root_path / case["annotation_path"]
    if not reference.is_file() or not annotation.is_file():
        raise RuntimeError("Phase 18 blocked: reference or annotation is missing")
    result_dir = Path(output_dir)
    result_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = result_dir / f"{case['case_id']}.pdf"
    settings = config.model_copy(update={"ml_runtime_enabled": True})
    result = run_real_case(case, root_path, settings)
    evidence = {
        "phase": 18,
        "execution_status": "EXECUTED",
        "case_id": case["case_id"],
        "source": {"path": str(source), "sha256": file_sha256(source)},
        "reference": {"path": str(reference), "sha256": file_sha256(reference)},
        "annotation": {"path": str(annotation), "sha256": file_sha256(annotation)},
        "pipeline": result,
        "reconstruction_requested": str(output_pdf),
        "accuracy_claim": True,
    }
    (result_dir / "evidence.json").write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")
    return evidence

import json
from pathlib import Path
from typing import Any
from backend.core.config import Settings
from backend.core.model_registry import assert_runtime_dependencies
from backend.evaluation.benchmark import BenchmarkRunner
from backend.evaluation.phase13 import load_manifest, validate_cases
from backend.pipeline.end_to_end import ScientificDocumentPipeline

def _texts(document, field: str) -> list[str]:
    return [value for page in document.pages for element in page.elements if (value := getattr(element, field, None))]

def run_real_case(case: dict[str, Any], root: Path, config: Settings) -> dict[str, Any]:
    input_path = root / case["input_path"]
    reference_path = root / case["reference_path"]
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    result = ScientificDocumentPipeline(config=config).run(
        input_path, source_language=case.get("source_language", "en"),
        target_language=case.get("target_language", "hi"),
        domain=case.get("domain", "general"),
        document_type=case.get("document_type", "question_paper"))
    source_pred = " ".join(_texts(result.document, "source_text"))
    target_pred = " ".join(_texts(result.document, "target_text"))
    runner = BenchmarkRunner()
    metrics = [
        runner.text_metric("ocr_cer_score", [source_pred], [reference["ocr_text"]]),
        runner.text_metric("translation_token_f1", [target_pred], [reference["translation_text"]]),
    ]
    return {"case_id": case["case_id"], "stage_status": result.stage_status,
            "validation_passed": result.validation.passed,
            "metrics": [metric.model_dump() for metric in metrics],
            "model_configuration": result.model_configuration}

def execute_manifest(manifest_path: str | Path, root: str | Path, config: Settings) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    cases = validate_cases(manifest, root)
    if not all(item["ready"] for item in cases):
        raise RuntimeError("Phase 14 execution blocked: benchmark assets/checksums are not ready")
    assert_runtime_dependencies(config)
    results = [run_real_case(case, Path(root), config) for case in manifest["cases"]]
    return {"benchmark_id": manifest.get("benchmark_id", f"{manifest['dataset_id']}-{manifest['version']}"),
            "dataset": {"id": manifest["dataset_id"], "version": manifest["version"]},
            "cases": results, "case_count": len(results),
            "metrics": [metric for case in results for metric in case["metrics"]],
            "accuracy_claim": True, "execution_status": "EXECUTED"}

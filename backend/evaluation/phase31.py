import json
from pathlib import Path
from typing import Any

CATEGORIES = {
    "ocr": "OCR",
    "translation": "TRANSLATION",
    "mathematics": "MATHEMATICS",
    "diagram": "DIAGRAM",
    "layout": "LAYOUT",
    "validation": "VALIDATION",
    "reconstruction": "RECONSTRUCTION",
    "pipeline": "PIPELINE",
}

def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def _metric_map(benchmark: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {m.get("name"): m for m in benchmark.get("metrics", []) if isinstance(m, dict)}

def classify_benchmark_result(result: dict[str, Any]) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    if result.get("execution_status") != "EXECUTED":
        issues.append({
            "category": CATEGORIES["pipeline"],
            "code": "EXECUTION_BLOCKED",
            "severity": "critical",
            "message": "Benchmark did not execute; no scientific failure attribution is permitted.",
        })
        return _report(result, issues, False)

    benchmark = result.get("benchmark", {})
    metrics = _metric_map(benchmark)
    mapping = {
        "ocr_cer_score": ("ocr", "OCR_BELOW_THRESHOLD", "OCR score is below its benchmark threshold."),
        "translation_token_f1": ("translation", "TRANSLATION_BELOW_THRESHOLD", "Translation Token-F1 is below its benchmark threshold."),
        "equation_exact": ("mathematics", "EQUATION_BELOW_THRESHOLD", "Equation exact-match score is below its benchmark threshold."),
        "diagram_integrity": ("diagram", "DIAGRAM_BELOW_THRESHOLD", "Diagram integrity score is below its benchmark threshold."),
        "layout_iou": ("layout", "LAYOUT_BELOW_THRESHOLD", "Layout IoU is below its benchmark threshold."),
        "reconstruction_fidelity": ("reconstruction", "RECONSTRUCTION_BELOW_THRESHOLD", "Reconstruction fidelity is below its benchmark threshold."),
    }
    for metric_name, (category, code, message) in mapping.items():
        metric = metrics.get(metric_name)
        if metric is not None and metric.get("passed") is False:
            issues.append({
                "category": CATEGORIES[category],
                "code": code,
                "severity": "error",
                "metric": metric_name,
                "value": metric.get("value"),
                "threshold": metric.get("threshold"),
                "message": message,
            })

    metadata = benchmark.get("metadata", {})
    validation_passed = metadata.get("validation_passed")
    if validation_passed is False:
        issues.append({
            "category": CATEGORIES["validation"],
            "code": "VALIDATION_FAILED",
            "severity": "error",
            "message": "The scientific document validation stage reported failure.",
            "validation_issue_count": metadata.get("validation_issues"),
        })

    stages = metadata.get("stage_status", {})
    for stage, status in stages.items():
        if status in {"failed", "error"}:
            category = stage if stage in CATEGORIES else "pipeline"
            issues.append({
                "category": CATEGORIES[category],
                "code": f"{stage.upper()}_STAGE_FAILED",
                "severity": "critical",
                "message": f"Pipeline stage '{stage}' reported {status}.",
            })

    return _report(result, issues, True)

def _report(result: dict[str, Any], issues: list[dict[str, Any]], attribution_allowed: bool) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for issue in issues:
        counts[issue["category"]] = counts.get(issue["category"], 0) + 1
    return {
        "phase": 31,
        "schema_version": "1.0",
        "status": "ANALYZED",
        "attribution_allowed": attribution_allowed,
        "scientific_accuracy_claim": result.get("accuracy_claim") is True and result.get("execution_status") == "EXECUTED",
        "issue_count": len(issues),
        "category_counts": counts,
        "issues": issues,
        "source_execution_status": result.get("execution_status"),
    }

def analyze_result(result_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    result = load_json(result_path)
    report = classify_benchmark_result(result)
    Path(output_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report

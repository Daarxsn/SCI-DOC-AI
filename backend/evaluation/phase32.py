import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

@dataclass(frozen=True)
class ModelProfile:
    task: str
    provider: str
    enabled: bool
    confidence_floor: float
    fallback: str | None = None

DEFAULT_PROFILES = (
    ModelProfile("ocr", "tesseract", True, 0.80, "paddleocr"),
    ModelProfile("translation", "rule-based-dev", True, 0.80, "huggingface-nllb"),
    ModelProfile("mathematics", "baseline", True, 0.75, "pix2tex"),
    ModelProfile("diagram", "baseline", True, 0.70, "ultralytics"),
    ModelProfile("reconstruction", "reportlab", True, 0.90, None),
)

def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def recommend_profiles(benchmark: dict[str, Any], profiles=DEFAULT_PROFILES) -> dict[str, Any]:
    metrics = {m.get("name"): m for m in benchmark.get("metrics", []) if isinstance(m, dict)}
    recommendations = []
    for profile in profiles:
        metric_name = {
            "ocr": "ocr_cer_score",
            "translation": "translation_token_f1",
            "mathematics": "equation_exact",
            "diagram": "diagram_integrity",
            "reconstruction": "reconstruction_fidelity",
        }.get(profile.task)
        metric = metrics.get(metric_name) if metric_name else None
        action = "keep"
        reason = "No failing measured metric requires a profile change."
        if metric and metric.get("passed") is False:
            action = "activate_fallback" if profile.fallback else "tune"
            reason = f"{metric_name} is below threshold."
        recommendations.append({
            **asdict(profile),
            "action": action,
            "reason": reason,
            "measured_value": metric.get("value") if metric else None,
            "threshold": metric.get("threshold") if metric else None,
        })
    return {
        "schema_version": "1.0",
        "phase": 32,
        "status": "OPTIMIZATION_RECOMMENDED",
        "accuracy_claim": False,
        "recommendations": recommendations,
    }

def build_optimization_plan(result_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    result = load_json(result_path)
    if result.get("execution_status") != "EXECUTED":
        report = {
            "schema_version": "1.0",
            "phase": 32,
            "status": "BLOCKED",
            "accuracy_claim": False,
            "reason": "Optimization requires an executed benchmark result.",
        }
    else:
        report = recommend_profiles(result.get("benchmark", {}))
    Path(output_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report

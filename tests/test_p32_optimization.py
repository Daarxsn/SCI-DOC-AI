import json
from pathlib import Path

from backend.core.model_routing import route_for
from backend.evaluation.phase32 import build_optimization_plan, recommend_profiles

def benchmark():
    return {
        "metrics": [
            {"name": "ocr_cer_score", "value": 0.72, "threshold": 0.90, "passed": False},
            {"name": "translation_token_f1", "value": 0.91, "threshold": 0.80, "passed": True},
            {"name": "equation_exact", "value": 0.94, "threshold": 0.95, "passed": False},
            {"name": "diagram_integrity", "value": 0.96, "threshold": 0.95, "passed": True},
            {"name": "reconstruction_fidelity", "value": 0.93, "threshold": 0.90, "passed": True},
        ]
    }

def test_phase32_recommends_fallback_for_failed_metrics():
    report = recommend_profiles(benchmark())
    by_task = {x["task"]: x for x in report["recommendations"]}
    assert by_task["ocr"]["action"] == "activate_fallback"
    assert by_task["mathematics"]["action"] == "activate_fallback"
    assert by_task["translation"]["action"] == "keep"

def test_phase32_blocks_without_executed_result(tmp_path: Path):
    result = tmp_path / "result.json"
    output = tmp_path / "optimization.json"
    result.write_text(json.dumps({"execution_status": "BLOCKED"}))
    report = build_optimization_plan(result, output)
    assert report["status"] == "BLOCKED"
    assert report["accuracy_claim"] is False

def test_phase32_routing_contract():
    route = route_for("translation")
    assert route.primary == "rule-based-dev"
    assert route.fallback == "huggingface-nllb"
    assert route.confidence_floor == 0.80

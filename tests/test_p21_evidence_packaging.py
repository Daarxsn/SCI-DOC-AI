import json
from pathlib import Path
import pytest
from backend.evaluation.phase21 import package_benchmark_result

def test_phase21_rejects_blocked_result(tmp_path):
    result = tmp_path / "result.json"
    result.write_text(json.dumps({"execution_status": "BLOCKED", "accuracy_claim": False}))
    with pytest.raises(RuntimeError, match="executed real run"):
        package_benchmark_result(result, tmp_path / "out")

def test_phase21_packages_executed_result(tmp_path):
    result = tmp_path / "result.json"
    result.write_text(json.dumps({
        "execution_status": "EXECUTED",
        "accuracy_claim": True,
        "benchmark": {
            "benchmark_id": "phase20-test",
            "task": "end_to_end",
            "overall_score": 0.91,
            "passed": True,
            "metrics": [{"name": "ocr_cer_score", "value": 0.92, "threshold": 0.90, "passed": True, "sample_count": 1}],
            "metadata": {"case_id": "test-001"}
        }
    }))
    evidence = package_benchmark_result(result, tmp_path / "out")
    assert evidence["packaging_status"] == "COMPLETE"
    assert (tmp_path / "out" / "benchmark-summary.json").is_file()
    assert (tmp_path / "out" / "evidence-manifest.json").is_file()

import json
from pathlib import Path
import pytest
from backend.evaluation.phase33 import compare_benchmarks, compare_result_files

def benchmark(ocr=0.90, translation=0.80):
    return {"metrics":[
        {"name":"ocr_cer_score","value":ocr},
        {"name":"translation_token_f1","value":translation},
    ]}

def test_phase33_accepts_candidate_with_improvement_and_no_regression():
    result = compare_benchmarks(benchmark(), benchmark(0.94, 0.82))
    assert result["status"] == "COMPARED"
    assert result["improvement_count"] == 2
    assert result["regression_count"] == 0
    assert result["candidate_accepted"] is True
    assert result["scientific_accuracy_claim"] is False

def test_phase33_rejects_regression():
    result = compare_benchmarks(benchmark(), benchmark(0.94, 0.79))
    assert result["candidate_accepted"] is False
    assert result["regression_count"] == 1

def test_phase33_requires_executed_results(tmp_path: Path):
    baseline=tmp_path/"baseline.json"; candidate=tmp_path/"candidate.json"
    baseline.write_text(json.dumps({"execution_status":"BLOCKED"}))
    candidate.write_text(json.dumps({"execution_status":"EXECUTED","benchmark":benchmark()}))
    with pytest.raises(ValueError, match="EXECUTED"):
        compare_result_files(baseline,candidate,tmp_path/"out.json")

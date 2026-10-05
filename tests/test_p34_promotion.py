import json
from pathlib import Path
import pytest
from backend.evaluation.phase34 import promote_candidate, verify_promotion

def accepted_comparison():
    return {
        "schema_version":"1.0",
        "phase":33,
        "status":"COMPARED",
        "candidate_accepted":True,
        "improvement_count":2,
        "regression_count":0,
        "metrics":[{"name":"ocr_cer_score","baseline":0.90,"candidate":0.94,"delta":0.04,"improved":True,"regressed":False}],
    }

def test_phase34_promotes_accepted_candidate():
    result=promote_candidate(accepted_comparison(), {"profile":"scientific","ocr_provider":"paddleocr"}, "reviewer@example.com")
    assert result["status"]=="PROMOTED"
    assert result["promotion_type"]=="BENCHMARK_VALIDATED_CANDIDATE"
    assert result["scientific_accuracy_claim"] is False
    assert result["candidate_config_fingerprint"]

def test_phase34_rejects_unaccepted_candidate():
    comparison=accepted_comparison()
    comparison["candidate_accepted"]=False
    with pytest.raises(ValueError, match="acceptance gate"):
        promote_candidate(comparison, {"profile":"scientific"}, "reviewer")

def test_phase34_requires_approver():
    with pytest.raises(ValueError, match="approver"):
        promote_candidate(accepted_comparison(), {"profile":"scientific"}, "")

def test_phase34_detects_tampering(tmp_path: Path):
    result=promote_candidate(accepted_comparison(), {"profile":"scientific"}, "reviewer")
    path=tmp_path/"promotion.json"
    path.write_text(json.dumps(result))
    assert verify_promotion(path)["valid"] is True
    result["approver"]="attacker"
    path.write_text(json.dumps(result))
    assert verify_promotion(path)["status"]=="TAMPERED"

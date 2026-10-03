import json
from backend.evaluation.phase23 import validate_phase22_release

def valid_payload():
    return {
        "execution_status":"EXECUTED",
        "accuracy_claim":True,
        "benchmark":{
            "benchmark_id":"real-001",
            "overall_score":0.86,
            "passed":True,
            "metrics":[
                {"name":"ocr_cer_score","value":0.92,"threshold":0.90,"passed":True},
                {"name":"translation_token_f1","value":0.80,"threshold":0.80,"passed":True}
            ]
        },
        "evidence":{"evidence_manifest_sha256":"abc"}
    }

def test_phase23_validates_consistent_release(tmp_path):
    p=tmp_path/"release.json"; p.write_text(json.dumps(valid_payload()))
    result=validate_phase22_release(p)
    assert result["valid"] is True
    assert result["status"]=="VALIDATED"

def test_phase23_rejects_inconsistent_overall_score(tmp_path):
    payload=valid_payload(); payload["benchmark"]["overall_score"]=0.5
    p=tmp_path/"release.json"; p.write_text(json.dumps(payload))
    result=validate_phase22_release(p)
    assert result["valid"] is False
    assert "overall score" in result["reason"]

def test_phase23_rejects_missing_required_metric(tmp_path):
    payload=valid_payload(); payload["benchmark"]["metrics"]=payload["benchmark"]["metrics"][:1]
    p=tmp_path/"release.json"; p.write_text(json.dumps(payload))
    result=validate_phase22_release(p)
    assert result["valid"] is False
    assert "missing" in result["reason"]

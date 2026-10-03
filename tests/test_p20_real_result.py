import json
from backend.evaluation.phase20 import execute_phase20
def test_phase20_fails_closed_without_real_case(tmp_path):
    manifest=tmp_path/"manifest.json"
    manifest.write_text(json.dumps({"dataset_id":"x","version":"1","cases":[{"case_id":"mathematics-hi-001","input_path":"missing.png","reference_path":"missing.json","annotation_path":"missing.json"}]}))
    result=execute_phase20(manifest,tmp_path,tmp_path/"out",object())
    assert result["execution_status"]=="BLOCKED"
    assert result["accuracy_claim"] is False
def test_phase20_rejects_multiple_cases(tmp_path):
    manifest=tmp_path/"manifest.json"
    manifest.write_text(json.dumps({"dataset_id":"x","version":"1","cases":[{},{}]}))
    result=execute_phase20(manifest,tmp_path,tmp_path/"out",object())
    assert result["execution_status"]=="BLOCKED"
    assert "exactly one" in result["readiness"]["reason"]

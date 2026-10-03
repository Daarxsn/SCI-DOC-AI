import json
from backend.evaluation.phase26 import create_run_record, verify_run_record

def freeze():
    return {"dataset":{"dataset_id":"golden","version":"1.2.0"},"freeze_fingerprint":"freeze-abc"}

def test_phase26_run_is_verifiable(tmp_path):
    record=create_run_record(freeze(),environment={"python":"3.12"})
    p=tmp_path/"run.json"; p.write_text(json.dumps(record))
    result=verify_run_record(p)
    assert result["valid"] is True
    assert result["status"]=="VALID"

def test_phase26_detects_tampering(tmp_path):
    record=create_run_record(freeze(),environment={"python":"3.12"})
    record["dataset"]["version"]="tampered"
    p=tmp_path/"run.json"; p.write_text(json.dumps(record))
    result=verify_run_record(p)
    assert result["valid"] is False
    assert result["status"]=="TAMPERED"

def test_phase26_rejects_non_executed_result(tmp_path):
    freeze_path=tmp_path/"freeze.json"; freeze_path.write_text(json.dumps(freeze()))
    result_path=tmp_path/"result.json"; result_path.write_text(json.dumps({"execution_status":"BLOCKED"}))
    try:
        from backend.evaluation.phase26 import register_run
        register_run(freeze_path,tmp_path/"out.json",result_path)
        assert False
    except RuntimeError:
        assert True

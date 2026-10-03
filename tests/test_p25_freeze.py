import json
from backend.evaluation.phase25 import dataset_fingerprint, freeze_dataset, verify_freeze

def manifest(tmp_path):
    p=tmp_path/"manifest.json"
    p.write_text(json.dumps({"dataset_id":"golden","version":"1.2.0","cases":[{"case_id":"m-hi-001","domain":"mathematics","source_language":"en","target_language":"hi","input_path":"a.png","reference_path":"r.json","annotation_path":"a.json","checksum_sha256":"abc"}]}))
    return p

def test_fingerprint_is_deterministic(tmp_path):
    p=manifest(tmp_path)
    assert dataset_fingerprint(p,tmp_path)["manifest_sha256"] == dataset_fingerprint(p,tmp_path)["manifest_sha256"]

def test_freeze_matches_current_manifest(tmp_path):
    p=manifest(tmp_path); out=tmp_path/"freeze.json"
    freeze_dataset(p,tmp_path,out,{"python":"3.12"})
    result=verify_freeze(out,p,tmp_path)
    assert result["valid"] is True

def test_freeze_detects_manifest_change(tmp_path):
    p=manifest(tmp_path); out=tmp_path/"freeze.json"
    freeze_dataset(p,tmp_path,out,{})
    data=json.loads(p.read_text()); data["version"]="1.3.0"; p.write_text(json.dumps(data))
    result=verify_freeze(out,p,tmp_path)
    assert result["valid"] is False

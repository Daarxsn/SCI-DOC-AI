import json,hashlib
from backend.evaluation.phase24 import assess_dataset
def test_phase24_blocks_missing_case_assets(tmp_path):
 p=tmp_path/"manifest.json"; p.write_text(json.dumps({"dataset_id":"x","version":"1","cases":[{"case_id":"m","input_path":"missing.png","reference_path":"missing.json","annotation_path":"missing.json"}]}))
 r=assess_dataset(p,tmp_path); assert r["ready"] is False; assert r["benchmark_eligible"] is False
def test_phase24_accepts_verified_case(tmp_path):
 s=tmp_path/"source.png"; s.write_bytes(b"authorized-scientific-document"); sha=hashlib.sha256(s.read_bytes()).hexdigest()
 ref=tmp_path/"ref.json"; ann=tmp_path/"ann.json"; ref.write_text(json.dumps({"metadata":{"ground_truth_status":"VERIFIED"}})); ann.write_text(json.dumps({"metadata":{"ground_truth_status":"VERIFIED"}}))
 p=tmp_path/"manifest.json"; p.write_text(json.dumps({"dataset_id":"x","version":"1","cases":[{"case_id":"m","input_path":"source.png","reference_path":"ref.json","annotation_path":"ann.json","checksum_sha256":sha}]}))
 r=assess_dataset(p,tmp_path); assert r["ready"] is True; assert r["benchmark_eligible"] is True

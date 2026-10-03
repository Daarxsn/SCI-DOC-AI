import json
import pytest
from backend.evaluation.phase19 import execute_benchmark_result

def test_phase19_requires_one_case(tmp_path):
 p=tmp_path/'m.json'; p.write_text(json.dumps({'dataset_id':'x','version':'1','cases':[]}))
 with pytest.raises(ValueError,match='at least one case'): execute_benchmark_result(p,tmp_path,tmp_path/'out',object())

def test_phase19_blocks_missing_source(tmp_path):
 p=tmp_path/'m.json'; p.write_text(json.dumps({'dataset_id':'x','version':'1','cases':[{'case_id':'mathematics-hi-001','input_path':'missing.png','reference_path':'r.json','annotation_path':'a.json'}]}))
 with pytest.raises(RuntimeError,match='source asset'): execute_benchmark_result(p,tmp_path,tmp_path/'out',object())

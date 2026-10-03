import json
from pathlib import Path
import pytest
from subprocess import run

def test_first_case_gate_rejects_unverified_case(tmp_path):
    source=tmp_path/"scientific.png"; source.write_bytes(b"authorized-placeholder")
    case={"case_id":"mathematics-hi-001","domain":"mathematics","source_language":"en","target_language":"hi","source_path":str(source),"status":"AWAITING_GROUND_TRUTH","benchmark_ready":False}
    path=tmp_path/"case.json"; path.write_text(json.dumps(case))
    result=run(["python","scripts/verify_phase17_first_case.py","--case",str(path)],capture_output=True,text=True)
    assert result.returncode != 0
    assert "FIRST_CASE_BLOCKED" in result.stderr or "FIRST_CASE_BLOCKED" in result.stdout

def test_phase17_prepare_script_exists():
    assert Path("scripts/prepare_phase17_case.py").is_file()

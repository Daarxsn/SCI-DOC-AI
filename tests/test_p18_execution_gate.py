import json
from pathlib import Path
import pytest
from backend.evaluation.phase18 import execute_first_case

def test_phase18_requires_exactly_one_case(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"dataset_id":"x","version":"1","cases":[]}))
    with pytest.raises(RuntimeError, match="exactly one"):
        execute_first_case(manifest, tmp_path, tmp_path/"out", object())

def test_phase18_blocks_unready_asset(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"dataset_id":"x","version":"1","cases":[{
        "case_id":"mathematics-hi-001","input_path":"missing.png",
        "reference_path":"ref.json","annotation_path":"ann.json"}]}))
    with pytest.raises(RuntimeError, match="asset"):
        execute_first_case(manifest, tmp_path, tmp_path/"out", object())

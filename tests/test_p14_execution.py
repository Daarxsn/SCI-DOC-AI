import json
from pathlib import Path
import pytest
from backend.evaluation.phase14 import execute_manifest

def test_phase14_blocks_missing_real_assets(tmp_path):
    manifest = {"dataset_id": "phase14-test", "version": "1.0.0", "cases": [{
        "case_id": "mathematics-hi-001", "domain": "mathematics", "source_language": "en",
        "target_language": "hi", "input_path": "missing.png", "reference_path": "missing.json"}]}
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(RuntimeError, match="assets"):
        execute_manifest(path, tmp_path, object())

def test_reference_schema_contains_required_fields():
    schema = json.loads(Path("datasets/golden/phase14-reference.schema.json").read_text(encoding="utf-8"))
    assert set(schema["required"]) == {"ocr_text", "translation_text"}

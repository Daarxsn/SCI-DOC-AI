import json
from pathlib import Path

def test_phase16_templates_exist():
    for name in ["datasets/golden/phase16-case-template.reference.json","datasets/golden/phase16-case-template.annotation.json"]:
        data=json.loads(Path(name).read_text())
        assert data["metadata"]["ground_truth_status"]=="VERIFIED"

def test_phase16_verifier_script_exists():
    assert Path("scripts/verify_phase16_dataset.py").is_file()
    assert Path("scripts/intake_phase16_case.py").is_file()
    assert Path("scripts/validate_phase16_case.py").is_file()

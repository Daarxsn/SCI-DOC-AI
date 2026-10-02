"""Local Phase 2 verification.

Run:
    python scripts/verify_phase2.py

This checks the benchmark contract and test suite without requiring heavy ML models.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest_path = ROOT / "datasets" / "golden" / "manifest.json"

def main():
    print("=== SCI-DOC AI | PHASE 2 VERIFICATION ===")
    print("[1/3] Checking golden manifest...")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cases = manifest.get("cases", [])
    assert manifest["dataset_id"] == "sci-doc-golden"
    assert len(cases) == 6
    assert {c["domain"] for c in cases} == {"mathematics", "physics", "biology"}
    assert {c["target_language"] for c in cases} == {"hi", "mr"}
    print("      PASS — 6 structural benchmark cases")

    print("[2/3] Checking annotation schema...")
    schema = json.loads(
        (ROOT / "datasets" / "golden" / "schema" / "annotation.schema.json").read_text(
            encoding="utf-8"
        )
    )
    assert "annotations" in schema["properties"]
    print("      PASS — annotation schema present")

    print("[3/3] Running evaluation tests...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_evaluation.py", "tests/test_phase2_dataset.py", "-q"],
        cwd=ROOT,
    )
    if result.returncode != 0:
        print("      FAIL — pytest failed")
        return result.returncode

    print("      PASS — evaluation and dataset tests")
    print()
    print("PHASE 2 VERIFICATION: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

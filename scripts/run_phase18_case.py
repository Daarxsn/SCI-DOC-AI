import argparse
import json
from pathlib import Path

from backend.core.config import Settings
from backend.evaluation.phase18 import execute_first_case

def main():
    p = argparse.ArgumentParser(description="Execute exactly one verified SCI-DOC AI golden case.")
    p.add_argument("--manifest", required=True)
    p.add_argument("--root", default=".")
    p.add_argument("--output-dir", default="phase18-evidence")
    a = p.parse_args()
    report = execute_first_case(a.manifest, a.root, a.output_dir, Settings())
    print(json.dumps({
        "execution_status": report["execution_status"],
        "case_id": report["case_id"],
        "accuracy_claim": report["accuracy_claim"],
        "evidence": str(Path(a.output_dir) / "evidence.json"),
    }, indent=2))

if __name__ == "__main__":
    main()

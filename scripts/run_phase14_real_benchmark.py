import argparse
import json
from pathlib import Path
from backend.core.config import Settings
from backend.evaluation.phase14 import execute_manifest

def main():
    parser = argparse.ArgumentParser(description="Execute the SCI-DOC AI real scientific-document benchmark.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="phase14-results.json")
    args = parser.parse_args()
    report = execute_manifest(args.manifest, args.root, Settings(ml_runtime_enabled=True))
    Path(args.output).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"benchmark_id": report["benchmark_id"], "execution_status": report["execution_status"], "case_count": report["case_count"], "accuracy_claim": report["accuracy_claim"]}, indent=2))

if __name__ == "__main__":
    main()

import argparse
import json
from backend.core.config import Settings
from backend.evaluation.phase30 import execute_phase30

def main():
    parser = argparse.ArgumentParser(description="Run SCI-DOC AI Phase 30 measured benchmark.")
    parser.add_argument("--intake", required=True)
    parser.add_argument("--ground-truth", required=True)
    parser.add_argument("--eligibility", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--output-dir", default="phase30-result")
    args = parser.parse_args()
    result = execute_phase30(args.intake, args.ground_truth, args.eligibility, args.root, args.output_dir, Settings(ml_runtime_enabled=True))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["execution_status"] == "BLOCKED":
        raise SystemExit(2)

if __name__ == "__main__":
    main()

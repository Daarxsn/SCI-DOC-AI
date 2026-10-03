import argparse
import json
from backend.evaluation.phase29 import build_benchmark_eligibility_manifest

def main():
    parser = argparse.ArgumentParser(description="Validate SCI-DOC AI Phase 29 benchmark eligibility.")
    parser.add_argument("--intake", required=True)
    parser.add_argument("--ground-truth", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", default="phase29-benchmark-eligibility.json")
    args = parser.parse_args()
    result = build_benchmark_eligibility_manifest(args.intake, args.ground_truth, args.root, args.output)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

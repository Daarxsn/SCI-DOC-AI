import argparse
import json
from backend.evaluation.phase28 import build_ground_truth_manifest

def main():
    parser = argparse.ArgumentParser(description="Validate SCI-DOC AI Phase 28 scientific ground truth.")
    parser.add_argument("--intake", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", default="phase28-ground-truth.json")
    args = parser.parse_args()
    result = build_ground_truth_manifest(args.intake, args.root, args.output)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

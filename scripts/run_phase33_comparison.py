import argparse
import json
from backend.evaluation.phase33 import compare_result_files

def main():
    parser = argparse.ArgumentParser(description="Compare SCI-DOC AI baseline and optimized benchmark results.")
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--output", default="phase33-comparison.json")
    args = parser.parse_args()
    result = compare_result_files(args.baseline, args.candidate, args.output)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

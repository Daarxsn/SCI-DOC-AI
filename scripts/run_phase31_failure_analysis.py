import argparse
import json
from backend.evaluation.phase31 import analyze_result

def main():
    parser = argparse.ArgumentParser(description="Analyze SCI-DOC AI benchmark failures.")
    parser.add_argument("--result", required=True)
    parser.add_argument("--output", default="phase31-failure-analysis.json")
    args = parser.parse_args()
    report = analyze_result(args.result, args.output)
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

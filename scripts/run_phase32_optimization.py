import argparse
import json
from backend.evaluation.phase32 import build_optimization_plan

def main():
    parser = argparse.ArgumentParser(description="Build SCI-DOC AI Phase 32 model optimization plan.")
    parser.add_argument("--result", required=True)
    parser.add_argument("--output", default="phase32-optimization.json")
    args = parser.parse_args()
    report = build_optimization_plan(args.result, args.output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["status"] == "BLOCKED":
        raise SystemExit(2)

if __name__ == "__main__":
    main()

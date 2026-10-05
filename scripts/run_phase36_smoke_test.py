import argparse
import json
from backend.evaluation.phase36 import run_from_file

def main():
    parser = argparse.ArgumentParser(description="Run SCI-DOC AI Phase 36 deployment smoke checks.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", default="phase36-smoke-report.json")
    args = parser.parse_args()
    report = run_from_file(args.manifest, args.output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["status"] == "SMOKE_TEST_PASSED" else 1)

if __name__ == "__main__":
    main()

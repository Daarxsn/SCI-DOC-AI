import argparse
import json
from backend.evaluation.phase35 import assess_from_files

def main():
    parser = argparse.ArgumentParser(description="Check SCI-DOC AI Phase 35 deployment readiness.")
    parser.add_argument("--release", required=True)
    parser.add_argument("--runtime", required=True)
    parser.add_argument("--output", default="phase35-deployment-readiness.json")
    args = parser.parse_args()
    report = assess_from_files(args.release, args.runtime, args.output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["status"] == "DEPLOYMENT_READY" else 2)

if __name__ == "__main__":
    main()

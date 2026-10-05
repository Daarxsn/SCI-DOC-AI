import argparse
import json
from backend.evaluation.phase37 import assess_from_file

def main():
    parser = argparse.ArgumentParser(description="Check SCI-DOC AI Phase 37 observability readiness.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", default="phase37-observability-readiness.json")
    args = parser.parse_args()
    report = assess_from_file(args.manifest, args.output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["status"] == "OBSERVABILITY_READY" else 2)

if __name__ == "__main__":
    main()

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.evaluation.phase42 import assess_from_file

def main():
    parser = argparse.ArgumentParser(
        description="Check SCI-DOC AI Phase 42 deployment contract readiness."
    )
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", default="phase42-deployment-readiness.json")
    args = parser.parse_args()
    report = assess_from_file(args.manifest, args.output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["status"] == "DEPLOYMENT_CONTRACT_READY" else 2)

if __name__ == "__main__":
    main()

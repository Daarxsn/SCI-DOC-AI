import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.evaluation.phase47 import assess_from_file

def main():
    parser = argparse.ArgumentParser(
        description="Check SCI-DOC AI Phase 47 continuous operations readiness."
    )
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", default="phase47-operations-readiness.json")
    args = parser.parse_args()
    report = assess_from_file(args.manifest, args.output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["status"] == "OPERATIONS_READY" else 2)

if __name__ == "__main__":
    main()

import argparse
import json
from backend.evaluation.phase23 import write_validation_report

def main():
    p = argparse.ArgumentParser(description="Validate a Phase 22 real benchmark release.")
    p.add_argument("--release", required=True)
    p.add_argument("--output", default="phase23-validation.json")
    args = p.parse_args()
    report = write_validation_report(args.release, args.output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not report["valid"]:
        raise SystemExit(2)

if __name__ == "__main__":
    main()

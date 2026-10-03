import argparse
import json
from pathlib import Path
from backend.evaluation.phase13 import build_phase13_report, load_manifest, validate_cases

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="phase13-report.json")
    args = parser.parse_args()
    manifest = load_manifest(args.manifest)
    report = build_phase13_report(manifest, validate_cases(manifest, args.root))
    Path(args.output).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ["benchmark_id", "execution_status", "ready_case_count", "case_count", "accuracy_claim"]}, indent=2))
    if report["execution_status"] != "READY_FOR_EXECUTION":
        raise SystemExit(2)

if __name__ == "__main__":
    main()

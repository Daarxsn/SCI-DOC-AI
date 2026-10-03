import argparse
import json
from backend.evaluation.phase22 import execute_phase22

def main():
    p = argparse.ArgumentParser(description="Execute and package one real SCI-DOC AI document run.")
    p.add_argument("--manifest", required=True)
    p.add_argument("--root", default=".")
    p.add_argument("--output-dir", default="phase22-release")
    args = p.parse_args()
    result = execute_phase22(args.manifest, args.root, args.output_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["execution_status"] == "BLOCKED":
        raise SystemExit(2)

if __name__ == "__main__":
    main()

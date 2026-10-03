import argparse
import json
from backend.evaluation.phase21 import package_benchmark_result

def main():
    p = argparse.ArgumentParser(description="Package an executed SCI-DOC AI benchmark result.")
    p.add_argument("--result", required=True)
    p.add_argument("--output-dir", default="phase21-release")
    args = p.parse_args()
    evidence = package_benchmark_result(args.result, args.output_dir)
    print(json.dumps(evidence, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

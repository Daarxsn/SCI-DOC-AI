import argparse
import json
from backend.evaluation.phase34 import promote_from_files

def main():
    parser = argparse.ArgumentParser(description="Promote a benchmark-validated SCI-DOC AI candidate.")
    parser.add_argument("--comparison", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--approver", required=True)
    parser.add_argument("--output", default="phase34-promotion.json")
    args = parser.parse_args()
    result = promote_from_files(args.comparison, args.config, args.output, args.approver)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

import argparse
import json
from backend.evaluation.phase34 import verify_promotion

def main():
    parser = argparse.ArgumentParser(description="Verify a Phase 34 promotion record.")
    parser.add_argument("--promotion", required=True)
    args = parser.parse_args()
    result = verify_promotion(args.promotion)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["valid"] else 1)

if __name__ == "__main__":
    main()

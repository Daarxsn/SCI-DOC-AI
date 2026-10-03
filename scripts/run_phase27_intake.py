import argparse
import json
from backend.evaluation.phase27 import build_intake_manifest

def main():
    parser = argparse.ArgumentParser(description="Validate SCI-DOC AI Phase 27 real-document intake.")
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", default="phase27-intake.json")
    args = parser.parse_args()
    manifest = build_intake_manifest(args.metadata, args.root, args.output)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

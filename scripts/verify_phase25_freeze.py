import argparse
import json
from backend.evaluation.phase25 import verify_freeze

def main():
    p=argparse.ArgumentParser(description="Verify a frozen SCI-DOC AI benchmark dataset.")
    p.add_argument("--freeze",required=True); p.add_argument("--manifest",required=True); p.add_argument("--root",default=".")
    a=p.parse_args()
    result=verify_freeze(a.freeze,a.manifest,a.root)
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if not result["valid"]: raise SystemExit(2)

if __name__=="__main__": main()

import argparse
import json
from backend.evaluation.phase26 import verify_run_record

def main():
    p=argparse.ArgumentParser(description="Verify SCI-DOC AI benchmark run provenance.")
    p.add_argument("--run",required=True); a=p.parse_args()
    result=verify_run_record(a.run)
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if not result["valid"]: raise SystemExit(2)

if __name__=="__main__": main()

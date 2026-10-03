import argparse,json
from backend.evaluation.phase24 import write_readiness_report
def main():
 p=argparse.ArgumentParser(); p.add_argument("--manifest",required=True); p.add_argument("--root",default="."); p.add_argument("--output",default="phase24-readiness.json"); a=p.parse_args()
 r=write_readiness_report(a.manifest,a.root,a.output); print(json.dumps(r,indent=2,ensure_ascii=False))
 if not r["ready"]: raise SystemExit(2)
if __name__=="__main__": main()

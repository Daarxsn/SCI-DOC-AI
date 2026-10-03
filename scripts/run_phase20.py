import argparse,json
from backend.core.config import Settings
from backend.evaluation.phase20 import execute_phase20
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--manifest",required=True); parser.add_argument("--root",default="."); parser.add_argument("--output-dir",default="phase20-result")
    args=parser.parse_args()
    result=execute_phase20(args.manifest,args.root,args.output_dir,Settings(ml_runtime_enabled=True))
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if result["execution_status"]=="BLOCKED": raise SystemExit(2)
if __name__=="__main__": main()

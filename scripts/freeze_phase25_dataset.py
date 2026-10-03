import argparse
import json
from backend.evaluation.phase25 import freeze_dataset

def main():
    p=argparse.ArgumentParser(description="Freeze a SCI-DOC AI benchmark dataset for reproducibility.")
    p.add_argument("--manifest",required=True); p.add_argument("--root",default="."); p.add_argument("--output",default="phase25-freeze.json")
    p.add_argument("--environment-json",default="{}")
    a=p.parse_args()
    result=freeze_dataset(a.manifest,a.root,a.output,json.loads(a.environment_json))
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=="__main__": main()

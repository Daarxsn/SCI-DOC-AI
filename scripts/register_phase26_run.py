import argparse
import json
from backend.evaluation.phase26 import register_run

def main():
    p=argparse.ArgumentParser(description="Register a reproducible SCI-DOC AI benchmark run.")
    p.add_argument("--freeze",required=True); p.add_argument("--output",default="phase26-run.json")
    p.add_argument("--benchmark-result"); p.add_argument("--environment-json",default="{}")
    a=p.parse_args()
    result=register_run(a.freeze,a.output,a.benchmark_result,json.loads(a.environment_json))
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=="__main__": main()

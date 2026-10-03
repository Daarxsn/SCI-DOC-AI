import argparse,json
from backend.core.config import Settings
from backend.evaluation.phase19 import execute_benchmark_result

def main():
 p=argparse.ArgumentParser(); p.add_argument('--manifest',required=True); p.add_argument('--root',default='.'); p.add_argument('--output-dir',default='phase19-result'); a=p.parse_args()
 r=execute_benchmark_result(a.manifest,a.root,a.output_dir,Settings(ml_runtime_enabled=True))
 print(json.dumps({'execution_status':r['execution_status'],'benchmark_id':r['benchmark']['benchmark_id'],'overall_score':r['benchmark']['overall_score'],'passed':r['benchmark']['passed'],'accuracy_claim':r['accuracy_claim']},indent=2))
if __name__=='__main__': main()

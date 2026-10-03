import argparse
import json
from pathlib import Path

ALLOWED={".pdf",".png",".jpg",".jpeg"}

def main():
    p=argparse.ArgumentParser(description="Prepare the first real SCI-DOC AI golden case.")
    p.add_argument("--source",required=True)
    p.add_argument("--case-id",default="mathematics-hi-001")
    p.add_argument("--domain",choices=["mathematics","physics","biology"],default="mathematics")
    p.add_argument("--target-language",choices=["hi","mr"],default="hi")
    p.add_argument("--output",default="phase17-case.json")
    a=p.parse_args()
    source=Path(a.source)
    if not source.is_file(): raise SystemExit("SOURCE_NOT_FOUND")
    if source.suffix.lower() not in ALLOWED: raise SystemExit("UNSUPPORTED_SOURCE_FORMAT")
    result={"case_id":a.case_id,"domain":a.domain,"source_language":"en","target_language":a.target_language,
            "source_path":str(source),"status":"AWAITING_GROUND_TRUTH","benchmark_ready":False,
            "required":["source asset","human-verified OCR","human-verified translation","structured annotations","SHA-256 checksum"]}
    Path(a.output).write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=="__main__": main()

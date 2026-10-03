import argparse
import hashlib
import json
from pathlib import Path

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--case",required=True)
    args=p.parse_args()
    data=json.loads(Path(args.case).read_text(encoding="utf-8"))
    required={"case_id","domain","source_language","target_language","source_path","status","benchmark_ready"}
    missing=required-set(data)
    if missing: raise SystemExit("missing case fields: "+",".join(sorted(missing)))
    source=Path(data["source_path"])
    if not source.is_file(): raise SystemExit("FIRST_CASE_BLOCKED: source asset is unavailable")
    if data["source_language"]!="en": raise SystemExit("FIRST_CASE_BLOCKED: source language must be English")
    if data["target_language"] not in {"hi","mr"}: raise SystemExit("FIRST_CASE_BLOCKED: target language must be Hindi or Marathi")
    if data["status"]!="VERIFIED" or data["benchmark_ready"] is not True:
        raise SystemExit("FIRST_CASE_BLOCKED: human ground truth has not been verified")
    if data.get("checksum_sha256") != sha256(source):
        raise SystemExit("FIRST_CASE_BLOCKED: checksum mismatch")
    print(json.dumps({"status":"FIRST_CASE_READY","case_id":data["case_id"],"checksum_sha256":data["checksum_sha256"]},indent=2))

if __name__=="__main__": main()

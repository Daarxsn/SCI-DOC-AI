import argparse,hashlib,json
from pathlib import Path
REQUIRED_DOMAINS={"mathematics","physics","biology"}; REQUIRED_TARGETS={"hi","mr"}
def sha256(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument("--manifest",default="datasets/golden/phase15-manifest.example.json"); p.add_argument("--root",default="."); a=p.parse_args()
 root=Path(a.root); manifest=json.loads((root/a.manifest).read_text(encoding="utf-8")); cases=manifest["cases"]; ids=[c["case_id"] for c in cases]
 if len(ids)!=len(set(ids)): raise SystemExit("duplicate case_id")
 coverage={(c["domain"],c["target_language"]) for c in cases}; expected={(d,t) for d in REQUIRED_DOMAINS for t in REQUIRED_TARGETS}
 if not expected.issubset(coverage): raise SystemExit("required domain/language coverage is incomplete")
 for c in cases:
  if c["source_language"]!="en": raise SystemExit(f"unsupported source language: {c['case_id']}")
  for key in ("input_path","reference_path","annotation_path"):
   if not c.get(key): raise SystemExit(f"missing {key}: {c['case_id']}")
  input_path=root/c["input_path"]
  if input_path.is_file() and c.get("checksum_sha256") and sha256(input_path)!=c["checksum_sha256"]: raise SystemExit(f"checksum mismatch: {c['case_id']}")
 print(f"Phase 15 dataset contract: PASS ({len(cases)} cases, assets may be externally mounted)")
if __name__=="__main__": main()

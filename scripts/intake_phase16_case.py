import argparse
import hashlib
import json
from pathlib import Path

DOMAINS={"mathematics","physics","biology"}
TARGETS={"hi","mr"}
EXTENSIONS={".pdf",".png",".jpg",".jpeg"}

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser(description="Register one authorized Phase 16 golden-dataset case.")
    p.add_argument("--source",required=True)
    p.add_argument("--case-id",required=True)
    p.add_argument("--domain",required=True,choices=sorted(DOMAINS))
    p.add_argument("--target-language",required=True,choices=sorted(TARGETS))
    p.add_argument("--dataset-version",default="1.2.0")
    p.add_argument("--output-dir",default="datasets/golden")
    args=p.parse_args()

    source=Path(args.source)
    if not source.is_file(): raise SystemExit(f"source asset not found: {source}")
    if source.suffix.lower() not in EXTENSIONS: raise SystemExit("unsupported source format; use PDF, PNG, JPG or JPEG")

    root=Path(args.output_dir)
    asset_dir=root/"assets"; ref_dir=root/"references"; ann_dir=root/"annotations"
    for d in (asset_dir,ref_dir,ann_dir): d.mkdir(parents=True,exist_ok=True)

    destination=asset_dir/f"{args.case_id}{source.suffix.lower()}"
    if destination.exists(): raise SystemExit(f"destination already exists: {destination}")
    destination.write_bytes(source.read_bytes())

    reference={
        "case_id":args.case_id,"reference_schema_version":"1.0",
        "ocr_text":"","translation_text":"","metadata":{
            "source_language":"en","target_language":args.target_language,"domain":args.domain,
            "ground_truth_status":"PENDING_HUMAN_REVIEW"
        }
    }
    annotation={
        "case_id":args.case_id,"annotation_schema_version":"1.0","pages":[],
        "metadata":{"ground_truth_status":"PENDING_HUMAN_REVIEW"}
    }
    (ref_dir/f"{args.case_id}.json").write_text(json.dumps(reference,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (ann_dir/f"{args.case_id}.json").write_text(json.dumps(annotation,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

    case={
        "case_id":args.case_id,"domain":args.domain,"source_language":"en",
        "target_language":args.target_language,"split":"test",
        "input_path":str(destination.as_posix()),"reference_path":str((ref_dir/f"{args.case_id}.json").as_posix()),
        "annotation_path":str((ann_dir/f"{args.case_id}.json").as_posix()),
        "checksum_sha256":sha256(destination),
        "metadata":{"dataset_version":args.dataset_version,"ground_truth_status":"PENDING_HUMAN_REVIEW"}
    }
    print(json.dumps(case,indent=2,ensure_ascii=False))

if __name__=="__main__": main()

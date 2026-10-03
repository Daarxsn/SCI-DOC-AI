import argparse,json
from pathlib import Path

from jsonschema import Draft202012Validator

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--reference",required=True)
    p.add_argument("--annotation",required=True)
    p.add_argument("--annotation-schema",default="datasets/golden/phase15-annotation.schema.json")
    args=p.parse_args()

    reference=json.loads(Path(args.reference).read_text(encoding="utf-8"))
    annotation=json.loads(Path(args.annotation).read_text(encoding="utf-8"))
    if not reference.get("case_id"): raise SystemExit("reference missing case_id")
    if not reference.get("ocr_text","").strip(): raise SystemExit("reference OCR ground truth is empty")
    if not reference.get("translation_text","").strip(): raise SystemExit("reference translation ground truth is empty")
    errors=list(Draft202012Validator(json.loads(Path(args.annotation_schema).read_text(encoding="utf-8"))).iter_errors(annotation))
    if errors: raise SystemExit("annotation schema validation failed: "+errors[0].message)
    if annotation.get("case_id")!=reference.get("case_id"): raise SystemExit("reference/annotation case_id mismatch")
    if annotation.get("metadata",{}).get("ground_truth_status")!="VERIFIED": raise SystemExit("annotation is not marked VERIFIED")
    if reference.get("metadata",{}).get("ground_truth_status")!="VERIFIED": raise SystemExit("reference is not marked VERIFIED")
    print("Phase 16 case validation: PASS")

if __name__=="__main__": main()

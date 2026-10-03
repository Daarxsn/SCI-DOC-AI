import argparse,json
from pathlib import Path
from jsonschema import Draft202012Validator

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",default="datasets/golden/phase15-manifest.example.json")
    p.add_argument("--root",default=".")
    args=p.parse_args()
    root=Path(args.root); manifest=json.loads((root/args.manifest).read_text(encoding="utf-8"))
    schema=json.loads((root/"datasets/golden/phase15-annotation.schema.json").read_text(encoding="utf-8"))
    ready=0; pending=0
    for case in manifest["cases"]:
        paths=[root/case["input_path"],root/case["reference_path"],root/case["annotation_path"]]
        if not all(p.is_file() for p in paths):
            pending+=1; continue
        ref=json.loads(paths[1].read_text(encoding="utf-8")); ann=json.loads(paths[2].read_text(encoding="utf-8"))
        errors=list(Draft202012Validator(schema).iter_errors(ann))
        verified=(ref.get("metadata",{}).get("ground_truth_status")=="VERIFIED" and ann.get("metadata",{}).get("ground_truth_status")=="VERIFIED" and bool(ref.get("ocr_text","").strip()) and bool(ref.get("translation_text","").strip()) and not errors)
        if verified: ready+=1
        else: pending+=1
    print(json.dumps({"dataset_id":manifest["dataset_id"],"version":manifest["version"],"total_cases":len(manifest["cases"]),"verified_cases":ready,"pending_cases":pending,"benchmark_ready":pending==0},indent=2))
if __name__=="__main__": main()

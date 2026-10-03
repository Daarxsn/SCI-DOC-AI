import hashlib
import json
from pathlib import Path
from typing import Any
REQUIRED_STATUS = "VERIFIED"
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""): h.update(chunk)
    return h.hexdigest()
def assess_dataset(manifest_path: str | Path, root: str | Path) -> dict[str, Any]:
    mf, root_path = Path(manifest_path), Path(root)
    if not mf.is_file(): return {"ready": False, "reason": "manifest is missing"}
    manifest = json.loads(mf.read_text(encoding="utf-8")); cases = manifest.get("cases", [])
    if not cases: return {"ready": False, "reason": "dataset contains no cases"}
    if not manifest.get("dataset_id") or not manifest.get("version"): return {"ready": False, "reason": "dataset_id and version are required"}
    results=[]
    for case in cases:
        required={k: root_path / case.get(k, "") for k in ("input_path","reference_path","annotation_path")}
        missing=[k for k,p in required.items() if not p.is_file()]
        if missing:
            results.append({"case_id":case.get("case_id"),"ready":False,"reason":"missing assets","missing":missing}); continue
        ref=json.loads(required["reference_path"].read_text(encoding="utf-8")); ann=json.loads(required["annotation_path"].read_text(encoding="utf-8"))
        actual=sha256_file(required["input_path"]); expected=case.get("checksum_sha256")
        ready=(ref.get("metadata",{}).get("ground_truth_status")==REQUIRED_STATUS and ann.get("metadata",{}).get("ground_truth_status")==REQUIRED_STATUS and (not expected or expected==actual))
        results.append({"case_id":case.get("case_id"),"ready":ready,"ground_truth_status":{"reference":ref.get("metadata",{}).get("ground_truth_status"),"annotation":ann.get("metadata",{}).get("ground_truth_status")},"source_sha256":actual,"checksum_verified":not expected or expected==actual})
    ready_count=sum(x["ready"] for x in results)
    return {"ready":ready_count==len(results),"dataset_id":manifest["dataset_id"],"version":manifest["version"],"case_count":len(results),"ready_cases":ready_count,"blocked_cases":len(results)-ready_count,"cases":results,"benchmark_eligible":ready_count==len(results)}
def write_readiness_report(manifest_path, root, output_path):
    report=assess_dataset(manifest_path,root); Path(output_path).write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8"); return report

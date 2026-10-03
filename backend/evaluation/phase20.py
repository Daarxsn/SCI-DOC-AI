import hashlib
import json
from pathlib import Path
from typing import Any
from backend.core.config import Settings
from backend.evaluation.phase19 import execute_benchmark_result
from backend.evaluation.phase13 import load_manifest

def sha256_file(path: Path) -> str:
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024*1024), b""): digest.update(chunk)
    return digest.hexdigest()

def readiness(manifest_path: str|Path, root: str|Path) -> dict[str,Any]:
    manifest=load_manifest(manifest_path)
    if len(manifest["cases"])!=1:
        return {"ready":False,"reason":"exactly one case is required","case_count":len(manifest["cases"])}
    case=manifest["cases"][0]; root_path=Path(root)
    required={key:root_path/case[key] for key in ("input_path","reference_path","annotation_path")}
    missing=[key for key,path in required.items() if not path.is_file()]
    if missing: return {"ready":False,"reason":"required assets are missing","missing":missing,"case_id":case["case_id"]}
    reference=json.loads(required["reference_path"].read_text(encoding="utf-8"))
    annotation=json.loads(required["annotation_path"].read_text(encoding="utf-8"))
    if reference.get("metadata",{}).get("ground_truth_status")!="VERIFIED":
        return {"ready":False,"reason":"reference ground truth is not VERIFIED","case_id":case["case_id"]}
    if annotation.get("metadata",{}).get("ground_truth_status")!="VERIFIED":
        return {"ready":False,"reason":"annotation ground truth is not VERIFIED","case_id":case["case_id"]}
    actual=sha256_file(required["input_path"]); expected=case.get("checksum_sha256")
    if expected and expected!=actual:
        return {"ready":False,"reason":"source checksum mismatch","case_id":case["case_id"],"expected":expected,"actual":actual}
    return {"ready":True,"case_id":case["case_id"],"source_sha256":actual}

def execute_phase20(manifest_path, root, output_dir, config: Settings):
    state=readiness(manifest_path,root)
    if not state["ready"]:
        return {"phase":20,"execution_status":"BLOCKED","accuracy_claim":False,"readiness":state}
    result=execute_benchmark_result(manifest_path,root,output_dir,config)
    return {"phase":20,"execution_status":"EXECUTED","accuracy_claim":True,"readiness":state,"benchmark":result["benchmark"]}

import hashlib
import json
from pathlib import Path
from typing import Any

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def dataset_fingerprint(manifest_path: str | Path, root: str | Path) -> dict[str, Any]:
    manifest_file = Path(manifest_path)
    root_path = Path(root)
    if not manifest_file.is_file():
        raise FileNotFoundError("manifest is missing")
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    if not manifest.get("dataset_id") or not manifest.get("version"):
        raise ValueError("dataset_id and version are required")
    cases = []
    for case in manifest.get("cases", []):
        item = {
            "case_id": case.get("case_id"),
            "domain": case.get("domain"),
            "source_language": case.get("source_language"),
            "target_language": case.get("target_language"),
            "input_path": case.get("input_path"),
            "reference_path": case.get("reference_path"),
            "annotation_path": case.get("annotation_path"),
            "checksum_sha256": case.get("checksum_sha256"),
        }
        cases.append(item)
    canonical = {"dataset_id": manifest["dataset_id"], "version": manifest["version"], "cases": cases}
    return {
        "dataset_id": manifest["dataset_id"],
        "version": manifest["version"],
        "case_count": len(cases),
        "manifest_sha256": sha256_bytes(canonical_json(canonical)),
        "case_ids": [case["case_id"] for case in cases],
    }

def freeze_dataset(manifest_path: str | Path, root: str | Path, output_path: str | Path, environment: dict[str, Any] | None = None) -> dict[str, Any]:
    fingerprint = dataset_fingerprint(manifest_path, root)
    freeze = {
        "freeze_schema_version": "1.0",
        "status": "FROZEN",
        "dataset": fingerprint,
        "environment": environment or {},
        "freeze_fingerprint": sha256_bytes(canonical_json({"dataset": fingerprint, "environment": environment or {}})),
    }
    Path(output_path).write_text(json.dumps(freeze, indent=2, ensure_ascii=False), encoding="utf-8")
    return freeze

def verify_freeze(freeze_path: str | Path, manifest_path: str | Path, root: str | Path) -> dict[str, Any]:
    freeze = json.loads(Path(freeze_path).read_text(encoding="utf-8"))
    current = dataset_fingerprint(manifest_path, root)
    expected = freeze.get("dataset", {})
    valid = expected.get("manifest_sha256") == current["manifest_sha256"] and expected.get("dataset_id") == current["dataset_id"] and expected.get("version") == current["version"]
    return {"valid": valid, "status": "MATCHED" if valid else "MISMATCHED", "expected": expected, "current": current}

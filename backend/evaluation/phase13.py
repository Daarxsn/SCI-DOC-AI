import hashlib
import json
from pathlib import Path
from typing import Any
from backend.core.model_registry import runtime_status
from backend.evaluation.provenance import build_provenance

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def load_manifest(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not data.get("dataset_id") or not data.get("version"):
        raise ValueError("Benchmark manifest requires dataset_id and version")
    if not data.get("cases"):
        raise ValueError("Benchmark manifest must contain at least one case")
    return data

def validate_cases(manifest: dict[str, Any], root: str | Path) -> list[dict[str, Any]]:
    root_path = Path(root)
    results = []
    for case in manifest["cases"]:
        input_path = root_path / case["input_path"]
        exists = input_path.is_file()
        checksum = sha256_file(input_path) if exists else None
        expected = case.get("checksum_sha256")
        results.append({"case_id": case["case_id"], "input_path": str(input_path), "exists": exists, "checksum_sha256": checksum, "checksum_match": expected is None or checksum == expected, "ready": exists and (expected is None or checksum == expected)})
    return results

def build_phase13_report(manifest: dict[str, Any], case_results: list[dict[str, Any]]) -> dict[str, Any]:
    status = runtime_status()
    configured = [m for m in status["models"] if m["configured"]]
    provenance = build_provenance(
        dataset_id=manifest["dataset_id"], dataset_version=manifest["version"],
        provider="sci-doc-ai-real-runtime",
        model_version=",".join(f"{m['key']}:{m['model_name']}" for m in configured) or "baseline",
        configuration={"runtime_enabled": status["runtime_enabled"], "device": status["device"], "cache_dir": status["cache_dir"], "preload": status["preload"]},
        case_ids=[case["case_id"] for case in manifest["cases"]],
    )
    ready_cases = sum(item["ready"] for item in case_results)
    return {
        "benchmark_id": manifest.get("benchmark_id", f"{manifest['dataset_id']}-{manifest['version']}"),
        "dataset": {"id": manifest["dataset_id"], "version": manifest["version"]},
        "runtime": status, "cases": case_results,
        "ready_case_count": ready_cases, "case_count": len(case_results),
        "execution_status": "READY_FOR_EXECUTION" if ready_cases == len(case_results) else "BLOCKED_MISSING_ASSETS",
        "provenance": {"fingerprint": provenance.fingerprint(), "dataset_id": provenance.dataset_id, "dataset_version": provenance.dataset_version, "provider": provenance.provider, "model_version": provenance.model_version, "configuration": provenance.configuration, "case_ids": list(provenance.case_ids)},
        "metrics": [], "accuracy_claim": False,
    }

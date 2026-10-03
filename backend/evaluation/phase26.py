import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()

def create_run_record(
    dataset_freeze: dict[str, Any],
    benchmark_result: dict[str, Any] | None = None,
    environment: dict[str, Any] | None = None,
) -> dict[str, Any]:
    run_id = "run-" + uuid.uuid4().hex
    result_fingerprint = fingerprint(benchmark_result) if benchmark_result else None
    config_fingerprint = fingerprint(environment or {})
    record = {
        "schema_version": "1.0",
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "COMPLETED" if benchmark_result else "REGISTERED",
        "dataset": {
            "dataset_id": dataset_freeze.get("dataset", {}).get("dataset_id"),
            "version": dataset_freeze.get("dataset", {}).get("version"),
            "freeze_fingerprint": dataset_freeze.get("freeze_fingerprint"),
        },
        "environment": environment or {},
        "environment_fingerprint": config_fingerprint,
        "benchmark_result_fingerprint": result_fingerprint,
        "benchmark_result": benchmark_result,
    }
    record["run_fingerprint"] = fingerprint({
        "run_id": run_id,
        "dataset": record["dataset"],
        "environment_fingerprint": config_fingerprint,
        "benchmark_result_fingerprint": result_fingerprint,
    })
    return record

def register_run(
    freeze_path: str | Path,
    output_path: str | Path,
    benchmark_result_path: str | Path | None = None,
    environment: dict[str, Any] | None = None,
) -> dict[str, Any]:
    freeze = json.loads(Path(freeze_path).read_text(encoding="utf-8"))
    result = None
    if benchmark_result_path:
        result = json.loads(Path(benchmark_result_path).read_text(encoding="utf-8"))
        if result.get("execution_status") != "EXECUTED":
            raise RuntimeError("Phase 26 refuses to register a non-executed benchmark result")
    record = create_run_record(freeze, result, environment)
    Path(output_path).write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    return record

def verify_run_record(run_path: str | Path) -> dict[str, Any]:
    record = json.loads(Path(run_path).read_text(encoding="utf-8"))
    required = {"schema_version", "run_id", "created_at", "status", "dataset", "environment_fingerprint", "run_fingerprint"}
    missing = sorted(required - set(record))
    if missing:
        return {"valid": False, "reason": "missing required fields", "missing": missing}
    expected = fingerprint({
        "run_id": record["run_id"],
        "dataset": record["dataset"],
        "environment_fingerprint": record["environment_fingerprint"],
        "benchmark_result_fingerprint": record.get("benchmark_result_fingerprint"),
    })
    return {
        "valid": expected == record["run_fingerprint"],
        "status": "VALID" if expected == record["run_fingerprint"] else "TAMPERED",
        "run_id": record["run_id"],
    }

import hashlib
import json
from pathlib import Path
from typing import Any

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def package_benchmark_result(result_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    source = Path(result_path)
    if not source.is_file():
        raise FileNotFoundError(f"benchmark result not found: {source}")
    payload = json.loads(source.read_text(encoding="utf-8"))
    if payload.get("execution_status") != "EXECUTED":
        raise RuntimeError("Phase 21 blocked: benchmark result is not an executed real run")
    if payload.get("accuracy_claim") is not True:
        raise RuntimeError("Phase 21 blocked: result does not contain an explicit accuracy claim")
    benchmark = payload.get("benchmark")
    if not isinstance(benchmark, dict):
        raise RuntimeError("Phase 21 blocked: benchmark payload is missing")
    metrics = benchmark.get("metrics", [])
    if not metrics:
        raise RuntimeError("Phase 21 blocked: no measured metrics are present")

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    result_sha = sha256_file(source)
    summary = {
        "product": "SCI-DOC AI",
        "phase": 21,
        "status": "MEASURED_RESULT_PACKAGED",
        "benchmark_id": benchmark.get("benchmark_id"),
        "task": benchmark.get("task"),
        "overall_score": benchmark.get("overall_score"),
        "passed": benchmark.get("passed"),
        "metric_count": len(metrics),
        "metrics": metrics,
        "source_result_sha256": result_sha,
        "metadata": benchmark.get("metadata", {}),
    }
    (out / "benchmark-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    evidence = {
        "phase": 21,
        "result_file": str(source),
        "result_sha256": result_sha,
        "summary_file": str(out / "benchmark-summary.json"),
        "summary_sha256": sha256_file(out / "benchmark-summary.json"),
        "benchmark_id": benchmark.get("benchmark_id"),
        "packaging_status": "COMPLETE",
    }
    (out / "evidence-manifest.json").write_text(
        json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    evidence["evidence_manifest_sha256"] = sha256_file(out / "evidence-manifest.json")
    return evidence

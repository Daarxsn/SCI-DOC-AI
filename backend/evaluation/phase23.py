import json
import math
from pathlib import Path
from typing import Any

REQUIRED_METRICS = {"ocr_cer_score", "translation_token_f1"}

def validate_phase22_release(release_path: str | Path) -> dict[str, Any]:
    source = Path(release_path)
    if not source.is_file():
        return {"valid": False, "reason": "release result is missing"}

    payload = json.loads(source.read_text(encoding="utf-8"))
    if payload.get("execution_status") != "EXECUTED":
        return {"valid": False, "reason": "release is not an executed real run"}
    if payload.get("accuracy_claim") is not True:
        return {"valid": False, "reason": "accuracy claim is not explicitly true"}

    benchmark = payload.get("benchmark")
    evidence = payload.get("evidence")
    if not isinstance(benchmark, dict):
        return {"valid": False, "reason": "benchmark payload is missing"}
    if not isinstance(evidence, dict):
        return {"valid": False, "reason": "evidence payload is missing"}

    metrics = benchmark.get("metrics", [])
    names = {metric.get("name") for metric in metrics if isinstance(metric, dict)}
    missing = sorted(REQUIRED_METRICS - names)
    if missing:
        return {"valid": False, "reason": "required measured metrics are missing", "missing_metrics": missing}

    for metric in metrics:
        value = metric.get("value")
        threshold = metric.get("threshold")
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            return {"valid": False, "reason": f"invalid metric value: {metric.get('name')}"}
        if not isinstance(threshold, (int, float)) or not math.isfinite(threshold):
            return {"valid": False, "reason": f"invalid metric threshold: {metric.get('name')}"}

    overall = benchmark.get("overall_score")
    if not isinstance(overall, (int, float)) or not math.isfinite(overall):
        return {"valid": False, "reason": "invalid overall score"}

    calculated = sum(metric["value"] for metric in metrics) / len(metrics)
    if abs(calculated - overall) > 1e-9:
        return {"valid": False, "reason": "overall score does not match metric mean"}

    if benchmark.get("passed") is not all(metric.get("passed") is True for metric in metrics):
        return {"valid": False, "reason": "benchmark pass state is inconsistent with metric states"}

    evidence_manifest = evidence.get("evidence_manifest_sha256")
    if not evidence_manifest:
        return {"valid": False, "reason": "evidence manifest hash is missing"}

    return {
        "valid": True,
        "status": "VALIDATED",
        "benchmark_id": benchmark.get("benchmark_id"),
        "metric_count": len(metrics),
        "required_metrics_present": True,
        "overall_score": overall,
        "passed": benchmark.get("passed"),
        "evidence_manifest_sha256": evidence_manifest,
    }

def write_validation_report(release_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    report = validate_phase22_release(release_path)
    Path(output_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report

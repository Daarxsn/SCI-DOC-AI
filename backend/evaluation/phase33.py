import hashlib
import json
from pathlib import Path
from typing import Any

def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def fingerprint(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(canonical).hexdigest()

def metric_map(benchmark: dict[str, Any]) -> dict[str, float]:
    return {
        m["name"]: float(m["value"])
        for m in benchmark.get("metrics", [])
        if isinstance(m, dict) and "name" in m and isinstance(m.get("value"), (int, float))
    }

def compare_benchmarks(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    base = metric_map(baseline)
    cand = metric_map(candidate)
    names = sorted(set(base) | set(cand))
    metrics = []
    for name in names:
        if name not in base or name not in cand:
            metrics.append({"name": name, "status": "MISSING", "baseline": base.get(name), "candidate": cand.get(name)})
            continue
        delta = cand[name] - base[name]
        metrics.append({
            "name": name,
            "baseline": base[name],
            "candidate": cand[name],
            "delta": delta,
            "improved": delta > 0,
            "regressed": delta < 0,
        })
    comparable = [m for m in metrics if m["status"] if False] if False else [m for m in metrics if m["status"] if "status" in m and m["status"] != "MISSING"]
    regressions = [m for m in metrics if m.get("regressed")]
    improvements = [m for m in metrics if m.get("improved")]
    return {
        "schema_version": "1.0",
        "phase": 33,
        "status": "COMPARED",
        "scientific_accuracy_claim": False,
        "metric_count": len(metrics),
        "improvement_count": len(improvements),
        "regression_count": len(regressions),
        "metrics": metrics,
        "candidate_accepted": bool(comparable) and not regressions and len(improvements) > 0,
    }

def compare_result_files(baseline_path: str | Path, candidate_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    baseline = load_json(baseline_path)
    candidate = load_json(candidate_path)
    if baseline.get("execution_status") != "EXECUTED" or candidate.get("execution_status") != "EXECUTED":
        raise ValueError("Phase 33 requires two EXECUTED benchmark results")
    report = compare_benchmarks(baseline.get("benchmark", {}), candidate.get("benchmark", {}))
    report["baseline_fingerprint"] = fingerprint(baseline)
    report["candidate_fingerprint"] = fingerprint(candidate)
    Path(output_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report

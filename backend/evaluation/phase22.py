import json
from pathlib import Path
from typing import Any

from backend.core.config import Settings
from backend.evaluation.phase20 import execute_phase20
from backend.evaluation.phase21 import package_benchmark_result

def execute_phase22(manifest_path: str | Path, root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    phase20_dir = out / "phase20"
    result = execute_phase20(
        manifest_path,
        root,
        phase20_dir,
        Settings(ml_runtime_enabled=True),
    )

    if result["execution_status"] != "EXECUTED":
        blocked = {
            "phase": 22,
            "execution_status": "BLOCKED",
            "accuracy_claim": False,
            "reason": result.get("readiness", {}).get("reason", "Phase 20 did not execute"),
            "readiness": result.get("readiness", {}),
            "evidence_packaged": False,
        }
        (out / "phase22-result.json").write_text(
            json.dumps(blocked, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return blocked

    benchmark_result = phase20_dir / "benchmark-result.json"
    evidence = package_benchmark_result(benchmark_result, out / "evidence")
    completed = {
        "phase": 22,
        "execution_status": "EXECUTED",
        "accuracy_claim": True,
        "benchmark": result["benchmark"],
        "evidence": evidence,
    }
    (out / "phase22-result.json").write_text(
        json.dumps(completed, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return completed

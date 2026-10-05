import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()

def promote_candidate(comparison: dict[str, Any], candidate_config: dict[str, Any], approver: str) -> dict[str, Any]:
    if comparison.get("status") != "COMPARED":
        raise ValueError("Phase 34 requires a completed Phase 33 comparison")
    if comparison.get("candidate_accepted") is not True:
        raise ValueError("Phase 34 refuses to promote a candidate that failed the Phase 33 acceptance gate")
    if not approver.strip():
        raise ValueError("Phase 34 requires an explicit approver")
    if not candidate_config:
        raise ValueError("Phase 34 requires candidate configuration provenance")

    promotion = {
        "schema_version": "1.0",
        "phase": 34,
        "status": "PROMOTED",
        "promotion_type": "BENCHMARK_VALIDATED_CANDIDATE",
        "promoted_at": datetime.now(timezone.utc).isoformat(),
        "approver": approver.strip(),
        "candidate_config": candidate_config,
        "candidate_config_fingerprint": fingerprint(candidate_config),
        "comparison_fingerprint": fingerprint(comparison),
        "scientific_accuracy_claim": False,
    }
    promotion["promotion_fingerprint"] = fingerprint({
        "phase": promotion["phase"],
        "promotion_type": promotion["promotion_type"],
        "approver": promotion["approver"],
        "candidate_config_fingerprint": promotion["candidate_config_fingerprint"],
        "comparison_fingerprint": promotion["comparison_fingerprint"],
    })
    return promotion

def promote_from_files(comparison_path: str | Path, config_path: str | Path, output_path: str | Path, approver: str) -> dict[str, Any]:
    comparison = json.loads(Path(comparison_path).read_text(encoding="utf-8"))
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    result = promote_candidate(comparison, config, approver)
    Path(output_path).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result

def verify_promotion(path: str | Path) -> dict[str, Any]:
    promotion = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {
        "schema_version", "phase", "status", "promotion_type", "promoted_at",
        "approver", "candidate_config_fingerprint", "comparison_fingerprint",
        "promotion_fingerprint",
    }
    missing = sorted(required - set(promotion))
    if missing:
        return {"valid": False, "status": "INVALID", "missing": missing}
    expected = fingerprint({
        "phase": promotion["phase"],
        "promotion_type": promotion["promotion_type"],
        "approver": promotion["approver"],
        "candidate_config_fingerprint": promotion["candidate_config_fingerprint"],
        "comparison_fingerprint": promotion["comparison_fingerprint"],
    })
    valid = expected == promotion["promotion_fingerprint"] and promotion["status"] == "PROMOTED"
    return {"valid": valid, "status": "VALID" if valid else "TAMPERED"}

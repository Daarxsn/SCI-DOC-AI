import json
from pathlib import Path
from backend.evaluation.phase38 import assess_resilience, assess_from_file

REQUIRED=("bounded_retries","idempotent_jobs","queue_recovery","artifact_recovery","dependency_timeout","graceful_degradation","failure_isolation")

def valid_manifest():
    return {name: True for name in REQUIRED}

def test_phase38_accepts_complete_resilience_contract():
    report=assess_resilience(valid_manifest())
    assert report["status"]=="RESILIENCE_READY"
    assert report["failures"]==[]
    assert report["deployment_claim"] is False
    assert report["live_resilience_verified"] is False

def test_phase38_blocks_unbounded_retry_control():
    manifest=valid_manifest(); manifest["bounded_retries"]=False
    report=assess_resilience(manifest)
    assert report["status"]=="RESILIENCE_BLOCKED"
    assert "bounded_retries" in report["failures"]

def test_phase38_blocks_missing_control():
    manifest=valid_manifest(); del manifest["failure_isolation"]
    report=assess_resilience(manifest)
    assert "failure_isolation" in report["failures"]

def test_phase38_file_runner(tmp_path: Path):
    source=tmp_path/"manifest.json"; output=tmp_path/"report.json"
    source.write_text(json.dumps(valid_manifest()))
    result=assess_from_file(source, output)
    assert output.exists()
    assert result["manifest_fingerprint"]

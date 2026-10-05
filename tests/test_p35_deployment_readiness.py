from backend.evaluation.phase35 import assess_deployment_readiness

def release():
    return {"version":"1.0.0","release_channel":"production-candidate"}

def runtime(**overrides):
    base={"api_key_configured":True,"tenant_isolation_configured":True,"tls_configured":True,"durable_storage_configured":True,"queue_configured":True,"ml_runtime_configured":True}
    base.update(overrides)
    return base

def test_phase35_ready_when_all_controls_configured():
    result=assess_deployment_readiness(release(), runtime())
    assert result["status"]=="DEPLOYMENT_READY"
    assert result["deployment_claim"] is False
    assert result["live_deployment_verified"] is False
    assert result["blockers"]==[]

def test_phase35_blocks_missing_tls():
    result=assess_deployment_readiness(release(), runtime(tls_configured=False))
    assert result["status"]=="DEPLOYMENT_BLOCKED"
    assert "tls_configured" in result["blockers"]

def test_phase35_blocks_missing_runtime_field():
    result=assess_deployment_readiness(release(), {"api_key_configured":True})
    assert result["status"]=="DEPLOYMENT_BLOCKED"
    assert any(x.startswith("runtime.") for x in result["blockers"])

def test_phase35_blocks_invalid_release_channel():
    result=assess_deployment_readiness({"version":"1.0.0","release_channel":"development"}, runtime())
    assert result["status"]=="DEPLOYMENT_BLOCKED"

from backend.core.config import Settings
from backend.core.model_registry import configured_models, runtime_status

def test_model_registry_contains_all_scientific_runtime_slots():
    assert {item.key for item in configured_models(Settings())} == {"ocr", "translation", "equation", "diagram"}

def test_default_runtime_is_safe_without_heavy_model_loading():
    status = runtime_status(Settings())
    assert status["runtime_enabled"] is False
    assert status["preload"] is False
    assert len(status["models"]) == 4

def test_configured_nllb_reports_dependency_state_without_loading_weights():
    status = runtime_status(Settings(translation_provider="huggingface-nllb", ml_runtime_enabled=True))
    item = next(model for model in status["models"] if model["key"] == "translation")
    assert item["configured"] is True
    assert "dependency_ready" in item
    assert "ready_for_load" in item

def test_runtime_endpoint_contract_exists():
    from backend.api.main import app
    assert "/runtime" in {route.path for route in app.routes}

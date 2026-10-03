from dataclasses import dataclass
from importlib.util import find_spec
from backend.core.config import Settings, settings

@dataclass(frozen=True)
class ModelSpec:
    key: str
    provider: str
    model_name: str
    package: str
    configured: bool

def _available(package: str) -> bool:
    return find_spec(package) is not None

def configured_models(config: Settings = settings) -> list[ModelSpec]:
    return [
        ModelSpec("ocr", config.ocr_provider, "PaddleOCR", "paddleocr", config.ocr_provider.lower() == "paddleocr"),
        ModelSpec("translation", config.translation_provider, config.translation_model, "transformers", config.translation_provider.lower() == "huggingface-nllb"),
        ModelSpec("equation", config.equation_provider, "pix2tex", "pix2tex", config.equation_provider.lower() == "pix2tex"),
        ModelSpec("diagram", config.diagram_provider, config.diagram_model or "configured-custom-yolo", "ultralytics", config.diagram_provider.lower() == "ultralytics"),
    ]

def runtime_status(config: Settings = settings) -> dict:
    models = []
    for spec in configured_models(config):
        dependency_ready = _available(spec.package) if spec.configured else True
        models.append({
            "key": spec.key, "provider": spec.provider, "model_name": spec.model_name,
            "configured": spec.configured, "dependency_ready": dependency_ready,
            "ready_for_load": (not spec.configured) or dependency_ready,
        })
    return {
        "runtime_enabled": config.ml_runtime_enabled,
        "device": config.ml_device,
        "cache_dir": config.model_cache_dir,
        "preload": config.ml_preload,
        "models": models,
    }

def assert_runtime_dependencies(config: Settings = settings) -> None:
    failures = [
        f"{item['key']}: {item['provider']} requires its ML dependency"
        for item in runtime_status(config)["models"]
        if item["configured"] and not item["dependency_ready"]
    ]
    if failures:
        raise RuntimeError("ML runtime dependencies are missing: " + "; ".join(failures))

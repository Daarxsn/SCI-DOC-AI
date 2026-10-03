from dataclasses import dataclass

@dataclass(frozen=True)
class ModelRoute:
    task: str
    primary: str
    fallback: str | None
    confidence_floor: float

DEFAULT_ROUTES = {
    "ocr": ModelRoute("ocr", "tesseract", "paddleocr", 0.80),
    "translation": ModelRoute("translation", "rule-based-dev", "huggingface-nllb", 0.80),
    "mathematics": ModelRoute("mathematics", "baseline", "pix2tex", 0.75),
    "diagram": ModelRoute("diagram", "baseline", "ultralytics", 0.70),
}

def route_for(task: str) -> ModelRoute:
    if task not in DEFAULT_ROUTES:
        raise ValueError(f"Unknown model-routing task: {task}")
    return DEFAULT_ROUTES[task]

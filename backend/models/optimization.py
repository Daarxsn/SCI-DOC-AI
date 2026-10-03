from dataclasses import dataclass

@dataclass(frozen=True)
class RuntimeProfile:
    name: str
    ocr_provider: str
    translation_provider: str
    equation_provider: str
    diagram_provider: str

PROFILES = {
    "baseline": RuntimeProfile("baseline", "tesseract", "rule-based-dev", "baseline", "baseline"),
    "scientific": RuntimeProfile("scientific", "paddleocr", "huggingface-nllb", "pix2tex", "ultralytics"),
}

def get_profile(name: str) -> RuntimeProfile:
    try:
        return PROFILES[name]
    except KeyError as exc:
        raise ValueError(f"Unknown runtime profile: {name}") from exc

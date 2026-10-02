from backend.core.config import Settings, settings
from backend.ocr.base import OcrAdapter
from backend.ocr.paddle_adapter import PaddleOcrAdapter
from backend.ocr.tesseract_adapter import TesseractAdapter


def create_ocr_adapter(config: Settings = settings) -> OcrAdapter:
    provider = config.ocr_provider.strip().lower()
    if provider == "tesseract":
        return TesseractAdapter(language=config.ocr_language)
    if provider == "paddleocr":
        return PaddleOcrAdapter(language=config.ocr_language, device=config.ml_device)
    raise ValueError(
        f"Unsupported OCR provider '{config.ocr_provider}'. "
        "Supported providers: tesseract, paddleocr."
    )

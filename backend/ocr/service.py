from pathlib import Path

from backend.ocr.base import OcrAdapter
from backend.ocr.models import OcrPageResult


class OcrService:
    def __init__(self, adapter: OcrAdapter) -> None:
        self.adapter = adapter

    def process_page(self, image_path: str | Path) -> OcrPageResult:
        return self.adapter.extract(image_path)
